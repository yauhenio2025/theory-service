"""
Theory Service - FastAPI Application
Central knowledge base for theoretical concepts, dialectics, and claims.
Provides API for essay-flow to query theory and post challenges.
"""

import os
from datetime import datetime
from typing import List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, text
from sqlalchemy.orm import selectinload

from .database import get_db, init_db, close_db
from .models import (
    TheorySource, Concept, Dialectic, Claim, Challenge, Refinement,
    EmergingConcept, EmergingDialectic, ChallengeCluster, ChallengeClusterMember
)
from .models import (
    ConceptStatus, DialecticStatus, ChallengeStatus,
    EmergingStatus, ClusterStatus, ClusterType, RecommendedAction
)
from .schemas import (
    TheorySourceCreate, TheorySourceResponse,
    ConceptCreate, ConceptUpdate, ConceptResponse,
    DialecticCreate, DialecticUpdate, DialecticResponse,
    ClaimCreate, ClaimUpdate, ClaimResponse,
    ChallengeCreate, ChallengeResponse, ChallengeReview,
    TheorySyncResponse, BulkChallengeCreate, BulkChallengeResponse,
    # Emerging theory schemas
    EmergingConceptCreate, EmergingConceptUpdate, EmergingConceptResponse,
    EmergingDialecticCreate, EmergingDialecticUpdate, EmergingDialecticResponse,
    BulkEmergingConceptCreate, BulkEmergingConceptResponse,
    BulkEmergingDialecticCreate, BulkEmergingDialecticResponse,
    # Clustering schemas
    ChallengeClusterResponse, ChallengeClusterMemberResponse, ChallengeClusterResolve,
    ClusteringRequest, ClusteringResponse, ChallengeDashboardStats,
    EmergingStatus as EmergingStatusSchema, ClusterStatus as ClusterStatusSchema,
    ClusterType as ClusterTypeSchema
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup resources."""
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title="Theory Service",
    description="Central knowledge base for theoretical concepts, dialectics, and claims",
    version="1.0.0",
    lifespan=lifespan
)

# CORS - allow essay-flow to access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# HEALTH CHECK
# =============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "theory-service"}


# =============================================================================
# ADMIN - MIGRATIONS
# =============================================================================

@app.post("/admin/migrate")
async def run_migrations(db: AsyncSession = Depends(get_db)):
    """Run pending database migrations (adds new columns to existing tables)."""
    migrations_run = []

    # Check and add source_project_name to challenges
    result = await db.execute(text("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'challenges' AND column_name = 'source_project_name'
    """))
    if not result.fetchone():
        await db.execute(text("ALTER TABLE challenges ADD COLUMN source_project_name VARCHAR(200)"))
        migrations_run.append("Added source_project_name to challenges")

    # Check and add cluster_group_id to challenges
    result = await db.execute(text("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'challenges' AND column_name = 'cluster_group_id'
    """))
    if not result.fetchone():
        await db.execute(text("ALTER TABLE challenges ADD COLUMN cluster_group_id INTEGER"))
        migrations_run.append("Added cluster_group_id to challenges")

    # Create index if not exists
    await db.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_challenges_cluster_group ON challenges(cluster_group_id)
    """))
    migrations_run.append("Ensured idx_challenges_cluster_group index exists")

    # Fix evidence_strength column type (VARCHAR -> TEXT for unlimited length)
    result = await db.execute(text("""
        SELECT data_type FROM information_schema.columns
        WHERE table_name = 'emerging_concepts' AND column_name = 'evidence_strength'
    """))
    row = result.fetchone()
    if row and row[0] and row[0] != 'text':
        await db.execute(text("ALTER TABLE emerging_concepts ALTER COLUMN evidence_strength TYPE TEXT"))
        await db.execute(text("ALTER TABLE emerging_dialectics ALTER COLUMN evidence_strength TYPE TEXT"))
        migrations_run.append("Changed evidence_strength column to TEXT")

    await db.commit()

    return {
        "status": "success",
        "migrations_run": migrations_run if migrations_run else ["No migrations needed"]
    }


# =============================================================================
# THEORY SOURCES
# =============================================================================

@app.get("/sources", response_model=List[TheorySourceResponse])
async def list_sources(db: AsyncSession = Depends(get_db)):
    """List all theory sources."""
    result = await db.execute(select(TheorySource).order_by(TheorySource.title))
    sources = result.scalars().all()

    responses = []
    for s in sources:
        concept_count = await db.scalar(
            select(func.count(Concept.id)).where(Concept.source_id == s.id)
        )
        dialectic_count = await db.scalar(
            select(func.count(Dialectic.id)).where(Dialectic.source_id == s.id)
        )
        claim_count = await db.scalar(
            select(func.count(Claim.id)).where(Claim.source_id == s.id)
        )

        resp = TheorySourceResponse.model_validate(s)
        resp.concept_count = concept_count or 0
        resp.dialectic_count = dialectic_count or 0
        resp.claim_count = claim_count or 0
        responses.append(resp)

    return responses


@app.get("/sources/{source_id}", response_model=TheorySourceResponse)
async def get_source(source_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific theory source."""
    result = await db.execute(select(TheorySource).where(TheorySource.id == source_id))
    source = result.scalar_one_or_none()
    if not source:
        raise HTTPException(status_code=404, detail="Theory source not found")

    concept_count = await db.scalar(
        select(func.count(Concept.id)).where(Concept.source_id == source_id)
    )
    dialectic_count = await db.scalar(
        select(func.count(Dialectic.id)).where(Dialectic.source_id == source_id)
    )
    claim_count = await db.scalar(
        select(func.count(Claim.id)).where(Claim.source_id == source_id)
    )

    resp = TheorySourceResponse.model_validate(source)
    resp.concept_count = concept_count or 0
    resp.dialectic_count = dialectic_count or 0
    resp.claim_count = claim_count or 0
    return resp


@app.post("/sources", response_model=TheorySourceResponse, status_code=201)
async def create_source(data: TheorySourceCreate, db: AsyncSession = Depends(get_db)):
    """Create a new theory source."""
    source = TheorySource(**data.model_dump())
    db.add(source)
    await db.commit()
    await db.refresh(source)
    return TheorySourceResponse.model_validate(source)


# =============================================================================
# CONCEPTS
# =============================================================================

@app.get("/concepts", response_model=List[ConceptResponse])
async def list_concepts(
    status: Optional[ConceptStatus] = None,
    category: Optional[str] = None,
    source_id: Optional[int] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all concepts, optionally filtered by status, category, source, or search term."""
    query = select(Concept)

    if status:
        query = query.where(Concept.status == status)
    if category:
        query = query.where(Concept.category == category)
    if source_id:
        query = query.where(Concept.source_id == source_id)
    if search:
        query = query.where(
            or_(
                Concept.term.ilike(f"%{search}%"),
                Concept.definition.ilike(f"%{search}%")
            )
        )

    query = query.order_by(Concept.term)
    result = await db.execute(query)
    concepts = result.scalars().all()

    # Build source title cache
    source_titles = {}
    source_ids = set(c.source_id for c in concepts if c.source_id)
    if source_ids:
        source_result = await db.execute(
            select(TheorySource).where(TheorySource.id.in_(source_ids))
        )
        for s in source_result.scalars():
            source_titles[s.id] = s.short_name or s.title

    # Add challenge counts and source titles
    responses = []
    for c in concepts:
        challenge_count = await db.scalar(
            select(func.count(Challenge.id)).where(Challenge.concept_id == c.id)
        )
        resp = ConceptResponse.model_validate(c)
        resp.challenge_count = challenge_count or 0
        resp.source_title = source_titles.get(c.source_id)
        responses.append(resp)

    return responses


@app.get("/concepts/{concept_id}", response_model=ConceptResponse)
async def get_concept(concept_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific concept."""
    result = await db.execute(select(Concept).where(Concept.id == concept_id))
    concept = result.scalar_one_or_none()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")

    challenge_count = await db.scalar(
        select(func.count(Challenge.id)).where(Challenge.concept_id == concept_id)
    )
    resp = ConceptResponse.model_validate(concept)
    resp.challenge_count = challenge_count or 0
    return resp


@app.post("/concepts", response_model=ConceptResponse, status_code=201)
async def create_concept(data: ConceptCreate, db: AsyncSession = Depends(get_db)):
    """Create a new concept."""
    concept = Concept(**data.model_dump())
    db.add(concept)
    await db.commit()
    await db.refresh(concept)
    return ConceptResponse.model_validate(concept)


@app.patch("/concepts/{concept_id}", response_model=ConceptResponse)
async def update_concept(
    concept_id: int,
    data: ConceptUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a concept."""
    result = await db.execute(select(Concept).where(Concept.id == concept_id))
    concept = result.scalar_one_or_none()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(concept, field, value)

    await db.commit()
    await db.refresh(concept)
    return ConceptResponse.model_validate(concept)


@app.delete("/concepts/{concept_id}", status_code=204)
async def delete_concept(concept_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a concept."""
    result = await db.execute(select(Concept).where(Concept.id == concept_id))
    concept = result.scalar_one_or_none()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")

    await db.delete(concept)
    await db.commit()


# =============================================================================
# DIALECTICS
# =============================================================================

@app.get("/dialectics", response_model=List[DialecticResponse])
async def list_dialectics(
    status: Optional[DialecticStatus] = None,
    category: Optional[str] = None,
    source_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all dialectics, optionally filtered by status, category, or source."""
    query = select(Dialectic)

    if status:
        query = query.where(Dialectic.status == status)
    if category:
        query = query.where(Dialectic.category == category)
    if source_id:
        query = query.where(Dialectic.source_id == source_id)

    query = query.order_by(Dialectic.name)
    result = await db.execute(query)
    dialectics = result.scalars().all()

    # Build source title cache
    source_titles = {}
    source_ids = set(d.source_id for d in dialectics if d.source_id)
    if source_ids:
        source_result = await db.execute(
            select(TheorySource).where(TheorySource.id.in_(source_ids))
        )
        for s in source_result.scalars():
            source_titles[s.id] = s.short_name or s.title

    responses = []
    for d in dialectics:
        challenge_count = await db.scalar(
            select(func.count(Challenge.id)).where(Challenge.dialectic_id == d.id)
        )
        resp = DialecticResponse.model_validate(d)
        resp.challenge_count = challenge_count or 0
        resp.source_title = source_titles.get(d.source_id)
        responses.append(resp)

    return responses


@app.get("/dialectics/{dialectic_id}", response_model=DialecticResponse)
async def get_dialectic(dialectic_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific dialectic."""
    result = await db.execute(select(Dialectic).where(Dialectic.id == dialectic_id))
    dialectic = result.scalar_one_or_none()
    if not dialectic:
        raise HTTPException(status_code=404, detail="Dialectic not found")

    challenge_count = await db.scalar(
        select(func.count(Challenge.id)).where(Challenge.dialectic_id == dialectic_id)
    )
    resp = DialecticResponse.model_validate(dialectic)
    resp.challenge_count = challenge_count or 0
    return resp


@app.post("/dialectics", response_model=DialecticResponse, status_code=201)
async def create_dialectic(data: DialecticCreate, db: AsyncSession = Depends(get_db)):
    """Create a new dialectic."""
    dialectic = Dialectic(**data.model_dump())
    db.add(dialectic)
    await db.commit()
    await db.refresh(dialectic)
    return DialecticResponse.model_validate(dialectic)


@app.patch("/dialectics/{dialectic_id}", response_model=DialecticResponse)
async def update_dialectic(
    dialectic_id: int,
    data: DialecticUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a dialectic."""
    result = await db.execute(select(Dialectic).where(Dialectic.id == dialectic_id))
    dialectic = result.scalar_one_or_none()
    if not dialectic:
        raise HTTPException(status_code=404, detail="Dialectic not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(dialectic, field, value)

    await db.commit()
    await db.refresh(dialectic)
    return DialecticResponse.model_validate(dialectic)


# =============================================================================
# CLAIMS
# =============================================================================

@app.get("/claims", response_model=List[ClaimResponse])
async def list_claims(
    active_only: bool = True,
    category: Optional[str] = None,
    source_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all claims, optionally filtered by active status, category, or source."""
    query = select(Claim)

    if active_only:
        query = query.where(Claim.is_active == True)
    if category:
        query = query.where(Claim.category == category)
    if source_id:
        query = query.where(Claim.source_id == source_id)

    query = query.order_by(Claim.created_at.desc())
    result = await db.execute(query)
    claims = result.scalars().all()

    # Build source title cache
    source_titles = {}
    source_ids = set(c.source_id for c in claims if c.source_id)
    if source_ids:
        source_result = await db.execute(
            select(TheorySource).where(TheorySource.id.in_(source_ids))
        )
        for s in source_result.scalars():
            source_titles[s.id] = s.short_name or s.title

    responses = []
    for c in claims:
        resp = ClaimResponse.model_validate(c)
        resp.source_title = source_titles.get(c.source_id)
        responses.append(resp)

    return responses


@app.post("/claims", response_model=ClaimResponse, status_code=201)
async def create_claim(data: ClaimCreate, db: AsyncSession = Depends(get_db)):
    """Create a new claim."""
    claim = Claim(**data.model_dump())
    db.add(claim)
    await db.commit()
    await db.refresh(claim)
    return claim


@app.patch("/claims/{claim_id}", response_model=ClaimResponse)
async def update_claim(
    claim_id: int,
    data: ClaimUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a claim."""
    result = await db.execute(select(Claim).where(Claim.id == claim_id))
    claim = result.scalar_one_or_none()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(claim, field, value)

    await db.commit()
    await db.refresh(claim)
    return claim


# =============================================================================
# CHALLENGES (from essay-flow)
# =============================================================================

@app.get("/challenges", response_model=List[ChallengeResponse])
async def list_challenges(
    status: Optional[ChallengeStatus] = None,
    source_project_id: Optional[int] = None,
    concept_id: Optional[int] = None,
    dialectic_id: Optional[int] = None,
    limit: int = Query(default=50, le=200),
    db: AsyncSession = Depends(get_db)
):
    """List challenges, optionally filtered."""
    query = select(Challenge)

    if status:
        query = query.where(Challenge.status == status)
    if source_project_id:
        query = query.where(Challenge.source_project_id == source_project_id)
    if concept_id:
        query = query.where(Challenge.concept_id == concept_id)
    if dialectic_id:
        query = query.where(Challenge.dialectic_id == dialectic_id)

    query = query.order_by(Challenge.created_at.desc()).limit(limit)
    result = await db.execute(query)
    challenges = result.scalars().all()

    # Enrich with related entity names
    responses = []
    for ch in challenges:
        resp = ChallengeResponse.model_validate(ch)

        if ch.concept_id:
            concept = await db.get(Concept, ch.concept_id)
            if concept:
                resp.concept_term = concept.term

        if ch.dialectic_id:
            dialectic = await db.get(Dialectic, ch.dialectic_id)
            if dialectic:
                resp.dialectic_name = dialectic.name

        if ch.claim_id:
            claim = await db.get(Claim, ch.claim_id)
            if claim:
                resp.claim_statement = claim.statement[:100] + "..." if len(claim.statement) > 100 else claim.statement

        responses.append(resp)

    return responses


@app.post("/challenges", response_model=ChallengeResponse, status_code=201)
async def create_challenge(data: ChallengeCreate, db: AsyncSession = Depends(get_db)):
    """Create a new challenge (posted by essay-flow)."""
    # Validate that at least one target is specified
    if not any([data.concept_id, data.dialectic_id, data.claim_id]):
        raise HTTPException(
            status_code=400,
            detail="At least one of concept_id, dialectic_id, or claim_id must be specified"
        )

    challenge = Challenge(**data.model_dump())
    db.add(challenge)
    await db.commit()
    await db.refresh(challenge)

    # Update concept/dialectic status if challenged
    if challenge.concept_id:
        concept = await db.get(Concept, challenge.concept_id)
        if concept and concept.status == ConceptStatus.ACTIVE:
            concept.status = ConceptStatus.CHALLENGED
            await db.commit()

    return ChallengeResponse.model_validate(challenge)


@app.post("/challenges/bulk", response_model=BulkChallengeResponse, status_code=201)
async def create_challenges_bulk(
    data: BulkChallengeCreate,
    db: AsyncSession = Depends(get_db)
):
    """Bulk create challenges (for batch posting from essay-flow)."""
    created_ids = []

    for ch_data in data.challenges:
        challenge = Challenge(**ch_data.model_dump())
        db.add(challenge)
        await db.flush()  # Get ID without committing
        created_ids.append(challenge.id)

    await db.commit()

    return BulkChallengeResponse(
        created_count=len(created_ids),
        challenge_ids=created_ids
    )


@app.patch("/challenges/{challenge_id}/review", response_model=ChallengeResponse)
async def review_challenge(
    challenge_id: int,
    data: ChallengeReview,
    db: AsyncSession = Depends(get_db)
):
    """Review a challenge (accept, reject, integrate)."""
    result = await db.execute(select(Challenge).where(Challenge.id == challenge_id))
    challenge = result.scalar_one_or_none()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    challenge.status = data.status
    if data.reviewer_notes:
        challenge.reviewer_notes = data.reviewer_notes
    challenge.reviewed_at = datetime.utcnow()

    # If integrated, apply the refinement
    if data.status == ChallengeStatus.INTEGRATED and challenge.concept_id and challenge.proposed_refinement:
        concept = await db.get(Concept, challenge.concept_id)
        if concept:
            # Create refinement record
            refinement = Refinement(
                concept_id=concept.id,
                previous_definition=concept.definition,
                new_definition=challenge.proposed_refinement,
                change_rationale=challenge.refinement_rationale,
                source_challenge_id=challenge.id
            )
            db.add(refinement)

            # Update concept
            concept.definition = challenge.proposed_refinement
            concept.status = ConceptStatus.ACTIVE

    await db.commit()
    await db.refresh(challenge)
    return ChallengeResponse.model_validate(challenge)


# =============================================================================
# SYNC ENDPOINT (for essay-flow to fetch all theory)
# =============================================================================

@app.get("/sync", response_model=TheorySyncResponse)
async def sync_theory(
    include_inactive: bool = False,
    source_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get complete theory state for essay-flow to sync.
    Returns all sources, concepts, dialectics, and claims.
    Optionally filter by source_id for a specific theory.
    """
    # Get sources
    source_result = await db.execute(select(TheorySource).order_by(TheorySource.title))
    sources = source_result.scalars().all()

    # Build source title cache
    source_titles = {s.id: s.short_name or s.title for s in sources}

    # Get concepts
    concept_query = select(Concept)
    if not include_inactive:
        concept_query = concept_query.where(Concept.status.in_([ConceptStatus.ACTIVE, ConceptStatus.CHALLENGED]))
    if source_id:
        concept_query = concept_query.where(Concept.source_id == source_id)
    concept_result = await db.execute(concept_query.order_by(Concept.term))
    concepts = concept_result.scalars().all()

    # Get dialectics
    dialectic_query = select(Dialectic)
    if not include_inactive:
        dialectic_query = dialectic_query.where(Dialectic.status.in_([DialecticStatus.ACTIVE]))
    if source_id:
        dialectic_query = dialectic_query.where(Dialectic.source_id == source_id)
    dialectic_result = await db.execute(dialectic_query.order_by(Dialectic.name))
    dialectics = dialectic_result.scalars().all()

    # Get claims
    claim_query = select(Claim)
    if not include_inactive:
        claim_query = claim_query.where(Claim.is_active == True)
    if source_id:
        claim_query = claim_query.where(Claim.source_id == source_id)
    claim_result = await db.execute(claim_query.order_by(Claim.created_at.desc()))
    claims = claim_result.scalars().all()

    # Build responses with source titles
    concept_responses = []
    for c in concepts:
        resp = ConceptResponse.model_validate(c)
        resp.source_title = source_titles.get(c.source_id)
        concept_responses.append(resp)

    dialectic_responses = []
    for d in dialectics:
        resp = DialecticResponse.model_validate(d)
        resp.source_title = source_titles.get(d.source_id)
        dialectic_responses.append(resp)

    claim_responses = []
    for c in claims:
        resp = ClaimResponse.model_validate(c)
        resp.source_title = source_titles.get(c.source_id)
        claim_responses.append(resp)

    # Build source responses with counts
    source_responses = []
    for s in sources:
        resp = TheorySourceResponse.model_validate(s)
        resp.concept_count = sum(1 for c in concepts if c.source_id == s.id)
        resp.dialectic_count = sum(1 for d in dialectics if d.source_id == s.id)
        resp.claim_count = sum(1 for c in claims if c.source_id == s.id)
        source_responses.append(resp)

    return TheorySyncResponse(
        sources=source_responses,
        concepts=concept_responses,
        dialectics=dialectic_responses,
        claims=claim_responses,
        synced_at=datetime.utcnow()
    )


# =============================================================================
# STATISTICS
# =============================================================================

@app.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    """Get theory statistics."""
    concept_count = await db.scalar(select(func.count(Concept.id)))
    dialectic_count = await db.scalar(select(func.count(Dialectic.id)))
    claim_count = await db.scalar(select(func.count(Claim.id)))
    pending_challenges = await db.scalar(
        select(func.count(Challenge.id)).where(Challenge.status == ChallengeStatus.PENDING)
    )

    return {
        "concepts": concept_count,
        "dialectics": dialectic_count,
        "claims": claim_count,
        "pending_challenges": pending_challenges
    }


# =============================================================================
# EMERGING CONCEPTS
# =============================================================================

@app.get("/emerging-concepts", response_model=List[EmergingConceptResponse])
async def list_emerging_concepts(
    status: Optional[EmergingStatusSchema] = None,
    source_project_id: Optional[int] = None,
    cluster_group_id: Optional[int] = None,
    limit: int = Query(default=50, le=200),
    db: AsyncSession = Depends(get_db)
):
    """List emerging concepts, optionally filtered."""
    query = select(EmergingConcept)

    if status:
        query = query.where(EmergingConcept.status == status)
    if source_project_id:
        query = query.where(EmergingConcept.source_project_id == source_project_id)
    if cluster_group_id:
        query = query.where(EmergingConcept.cluster_group_id == cluster_group_id)

    query = query.order_by(EmergingConcept.created_at.desc()).limit(limit)
    result = await db.execute(query)
    emerging = result.scalars().all()

    # Enrich with related concept names
    responses = []
    for ec in emerging:
        resp = EmergingConceptResponse.model_validate(ec)

        # Get related concept names
        if ec.related_concept_ids:
            related_result = await db.execute(
                select(Concept.term).where(Concept.id.in_(ec.related_concept_ids))
            )
            resp.related_concept_names = [r[0] for r in related_result.fetchall()]

        responses.append(resp)

    return responses


@app.get("/emerging-concepts/{ec_id}", response_model=EmergingConceptResponse)
async def get_emerging_concept(ec_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific emerging concept."""
    result = await db.execute(select(EmergingConcept).where(EmergingConcept.id == ec_id))
    ec = result.scalar_one_or_none()
    if not ec:
        raise HTTPException(status_code=404, detail="Emerging concept not found")

    resp = EmergingConceptResponse.model_validate(ec)

    if ec.related_concept_ids:
        related_result = await db.execute(
            select(Concept.term).where(Concept.id.in_(ec.related_concept_ids))
        )
        resp.related_concept_names = [r[0] for r in related_result.fetchall()]

    return resp


@app.post("/emerging-concepts", response_model=EmergingConceptResponse, status_code=201)
async def create_emerging_concept(
    data: EmergingConceptCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new emerging concept (posted by essay-flow)."""
    ec = EmergingConcept(**data.model_dump())
    db.add(ec)
    await db.commit()
    await db.refresh(ec)
    return EmergingConceptResponse.model_validate(ec)


@app.post("/emerging-concepts/bulk", response_model=BulkEmergingConceptResponse, status_code=201)
async def create_emerging_concepts_bulk(
    data: BulkEmergingConceptCreate,
    db: AsyncSession = Depends(get_db)
):
    """Bulk create emerging concepts."""
    created_ids = []

    for ec_data in data.emerging_concepts:
        ec = EmergingConcept(**ec_data.model_dump())
        db.add(ec)
        await db.flush()
        created_ids.append(ec.id)

    await db.commit()

    return BulkEmergingConceptResponse(
        created_count=len(created_ids),
        emerging_concept_ids=created_ids
    )


@app.patch("/emerging-concepts/{ec_id}", response_model=EmergingConceptResponse)
async def update_emerging_concept(
    ec_id: int,
    data: EmergingConceptUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an emerging concept (review, promote, etc.)."""
    result = await db.execute(select(EmergingConcept).where(EmergingConcept.id == ec_id))
    ec = result.scalar_one_or_none()
    if not ec:
        raise HTTPException(status_code=404, detail="Emerging concept not found")

    update_data = data.model_dump(exclude_unset=True)

    # Handle promotion to concept
    if data.status == EmergingStatusSchema.PROMOTED:
        if not data.promoted_to_concept_id:
            # Create a new concept from this emerging concept
            new_concept = Concept(
                term=ec.proposed_name,
                definition=ec.proposed_definition or ec.emergence_rationale,
                category="emerging",  # Mark as from emerging
                status=ConceptStatus.ACTIVE,
                confidence=ec.confidence,
                source_notes=f"Promoted from emerging concept #{ec.id}"
            )
            db.add(new_concept)
            await db.flush()
            update_data["promoted_to_concept_id"] = new_concept.id

        ec.reviewed_at = datetime.utcnow()

    for field, value in update_data.items():
        setattr(ec, field, value)

    await db.commit()
    await db.refresh(ec)
    return EmergingConceptResponse.model_validate(ec)


# =============================================================================
# EMERGING DIALECTICS
# =============================================================================

@app.get("/emerging-dialectics", response_model=List[EmergingDialecticResponse])
async def list_emerging_dialectics(
    status: Optional[EmergingStatusSchema] = None,
    source_project_id: Optional[int] = None,
    cluster_group_id: Optional[int] = None,
    limit: int = Query(default=50, le=200),
    db: AsyncSession = Depends(get_db)
):
    """List emerging dialectics, optionally filtered."""
    query = select(EmergingDialectic)

    if status:
        query = query.where(EmergingDialectic.status == status)
    if source_project_id:
        query = query.where(EmergingDialectic.source_project_id == source_project_id)
    if cluster_group_id:
        query = query.where(EmergingDialectic.cluster_group_id == cluster_group_id)

    query = query.order_by(EmergingDialectic.created_at.desc()).limit(limit)
    result = await db.execute(query)
    emerging = result.scalars().all()

    # Enrich with related dialectic names
    responses = []
    for ed in emerging:
        resp = EmergingDialecticResponse.model_validate(ed)

        if ed.related_dialectic_ids:
            related_result = await db.execute(
                select(Dialectic.name).where(Dialectic.id.in_(ed.related_dialectic_ids))
            )
            resp.related_dialectic_names = [r[0] for r in related_result.fetchall()]

        responses.append(resp)

    return responses


@app.get("/emerging-dialectics/{ed_id}", response_model=EmergingDialecticResponse)
async def get_emerging_dialectic(ed_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific emerging dialectic."""
    result = await db.execute(select(EmergingDialectic).where(EmergingDialectic.id == ed_id))
    ed = result.scalar_one_or_none()
    if not ed:
        raise HTTPException(status_code=404, detail="Emerging dialectic not found")

    resp = EmergingDialecticResponse.model_validate(ed)

    if ed.related_dialectic_ids:
        related_result = await db.execute(
            select(Dialectic.name).where(Dialectic.id.in_(ed.related_dialectic_ids))
        )
        resp.related_dialectic_names = [r[0] for r in related_result.fetchall()]

    return resp


@app.post("/emerging-dialectics", response_model=EmergingDialecticResponse, status_code=201)
async def create_emerging_dialectic(
    data: EmergingDialecticCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new emerging dialectic (posted by essay-flow)."""
    ed = EmergingDialectic(**data.model_dump())
    db.add(ed)
    await db.commit()
    await db.refresh(ed)
    return EmergingDialecticResponse.model_validate(ed)


@app.post("/emerging-dialectics/bulk", response_model=BulkEmergingDialecticResponse, status_code=201)
async def create_emerging_dialectics_bulk(
    data: BulkEmergingDialecticCreate,
    db: AsyncSession = Depends(get_db)
):
    """Bulk create emerging dialectics."""
    created_ids = []

    for ed_data in data.emerging_dialectics:
        ed = EmergingDialectic(**ed_data.model_dump())
        db.add(ed)
        await db.flush()
        created_ids.append(ed.id)

    await db.commit()

    return BulkEmergingDialecticResponse(
        created_count=len(created_ids),
        emerging_dialectic_ids=created_ids
    )


@app.patch("/emerging-dialectics/{ed_id}", response_model=EmergingDialecticResponse)
async def update_emerging_dialectic(
    ed_id: int,
    data: EmergingDialecticUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an emerging dialectic (review, promote, etc.)."""
    result = await db.execute(select(EmergingDialectic).where(EmergingDialectic.id == ed_id))
    ed = result.scalar_one_or_none()
    if not ed:
        raise HTTPException(status_code=404, detail="Emerging dialectic not found")

    update_data = data.model_dump(exclude_unset=True)

    # Handle promotion to dialectic
    if data.status == EmergingStatusSchema.PROMOTED:
        if not data.promoted_to_dialectic_id:
            # Create a new dialectic from this emerging dialectic
            new_dialectic = Dialectic(
                name=f"Emerging: {ed.proposed_question or ed.proposed_tension_a[:50]}",
                tension_a=ed.proposed_tension_a,
                tension_b=ed.proposed_tension_b,
                description=ed.proposed_question,
                category="emerging",
                status=DialecticStatus.ACTIVE,
                source_notes=f"Promoted from emerging dialectic #{ed.id}"
            )
            db.add(new_dialectic)
            await db.flush()
            update_data["promoted_to_dialectic_id"] = new_dialectic.id

        ed.reviewed_at = datetime.utcnow()

    for field, value in update_data.items():
        setattr(ed, field, value)

    await db.commit()
    await db.refresh(ed)
    return EmergingDialecticResponse.model_validate(ed)


# =============================================================================
# CHALLENGE CLUSTERS
# =============================================================================

@app.get("/challenge-clusters", response_model=List[ChallengeClusterResponse])
async def list_challenge_clusters(
    status: Optional[ClusterStatusSchema] = None,
    cluster_type: Optional[ClusterTypeSchema] = None,
    target_concept_id: Optional[int] = None,
    target_dialectic_id: Optional[int] = None,
    limit: int = Query(default=50, le=200),
    db: AsyncSession = Depends(get_db)
):
    """List challenge clusters, optionally filtered."""
    # Eagerly load members and their nested relationships
    query = select(ChallengeCluster).options(
        selectinload(ChallengeCluster.members).selectinload(ChallengeClusterMember.challenge),
        selectinload(ChallengeCluster.members).selectinload(ChallengeClusterMember.emerging_concept),
        selectinload(ChallengeCluster.members).selectinload(ChallengeClusterMember.emerging_dialectic),
    )

    if status:
        query = query.where(ChallengeCluster.status == status)
    if cluster_type:
        query = query.where(ChallengeCluster.cluster_type == cluster_type)
    if target_concept_id:
        query = query.where(ChallengeCluster.target_concept_id == target_concept_id)
    if target_dialectic_id:
        query = query.where(ChallengeCluster.target_dialectic_id == target_dialectic_id)

    query = query.order_by(ChallengeCluster.created_at.desc()).limit(limit)
    result = await db.execute(query)
    clusters = result.scalars().all()

    responses = []
    for cluster in clusters:
        resp = ChallengeClusterResponse.model_validate(cluster)

        # Get target entity names
        if cluster.target_concept_id:
            concept = await db.get(Concept, cluster.target_concept_id)
            if concept:
                resp.target_concept_term = concept.term

        if cluster.target_dialectic_id:
            dialectic = await db.get(Dialectic, cluster.target_dialectic_id)
            if dialectic:
                resp.target_dialectic_name = dialectic.name

        responses.append(resp)

    return responses


@app.get("/challenge-clusters/{cluster_id}", response_model=ChallengeClusterResponse)
async def get_challenge_cluster(
    cluster_id: int,
    include_members: bool = True,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific challenge cluster with optional members."""
    result = await db.execute(
        select(ChallengeCluster)
        .options(
            selectinload(ChallengeCluster.members).selectinload(ChallengeClusterMember.challenge),
            selectinload(ChallengeCluster.members).selectinload(ChallengeClusterMember.emerging_concept),
            selectinload(ChallengeCluster.members).selectinload(ChallengeClusterMember.emerging_dialectic),
        )
        .where(ChallengeCluster.id == cluster_id)
    )
    cluster = result.scalar_one_or_none()
    if not cluster:
        raise HTTPException(status_code=404, detail="Challenge cluster not found")

    resp = ChallengeClusterResponse.model_validate(cluster)

    # Get target entity names
    if cluster.target_concept_id:
        concept = await db.get(Concept, cluster.target_concept_id)
        if concept:
            resp.target_concept_term = concept.term

    if cluster.target_dialectic_id:
        dialectic = await db.get(Dialectic, cluster.target_dialectic_id)
        if dialectic:
            resp.target_dialectic_name = dialectic.name

    # Load members if requested
    if include_members:
        members_result = await db.execute(
            select(ChallengeClusterMember).where(
                ChallengeClusterMember.cluster_id == cluster_id
            )
        )
        members = members_result.scalars().all()

        member_responses = []
        for member in members:
            member_resp = ChallengeClusterMemberResponse.model_validate(member)

            # Load the referenced entity
            if member.challenge_id:
                challenge = await db.get(Challenge, member.challenge_id)
                if challenge:
                    member_resp.challenge = ChallengeResponse.model_validate(challenge)

            if member.emerging_concept_id:
                ec = await db.get(EmergingConcept, member.emerging_concept_id)
                if ec:
                    member_resp.emerging_concept = EmergingConceptResponse.model_validate(ec)

            if member.emerging_dialectic_id:
                ed = await db.get(EmergingDialectic, member.emerging_dialectic_id)
                if ed:
                    member_resp.emerging_dialectic = EmergingDialecticResponse.model_validate(ed)

            member_responses.append(member_resp)

        resp.members = member_responses

    return resp


@app.patch("/challenge-clusters/{cluster_id}", response_model=ChallengeClusterResponse)
async def resolve_challenge_cluster(
    cluster_id: int,
    data: ChallengeClusterResolve,
    db: AsyncSession = Depends(get_db)
):
    """Resolve a challenge cluster (batch accept/reject)."""
    result = await db.execute(
        select(ChallengeCluster).where(ChallengeCluster.id == cluster_id)
    )
    cluster = result.scalar_one_or_none()
    if not cluster:
        raise HTTPException(status_code=404, detail="Challenge cluster not found")

    cluster.status = data.status
    if data.resolution_notes:
        cluster.resolution_notes = data.resolution_notes

    if data.status == ClusterStatusSchema.RESOLVED:
        cluster.resolved_at = datetime.utcnow()

        # Apply action to all members if specified
        if data.member_action in ["accept", "reject"]:
            members_result = await db.execute(
                select(ChallengeClusterMember).where(
                    ChallengeClusterMember.cluster_id == cluster_id
                )
            )
            members = members_result.scalars().all()

            new_status = (
                ChallengeStatus.ACCEPTED if data.member_action == "accept"
                else ChallengeStatus.REJECTED
            )
            new_emerging_status = (
                EmergingStatus.ACCEPTED if data.member_action == "accept"
                else EmergingStatus.REJECTED
            )

            for member in members:
                if member.challenge_id:
                    challenge = await db.get(Challenge, member.challenge_id)
                    if challenge:
                        challenge.status = new_status
                        challenge.reviewed_at = datetime.utcnow()

                if member.emerging_concept_id:
                    ec = await db.get(EmergingConcept, member.emerging_concept_id)
                    if ec:
                        ec.status = new_emerging_status
                        ec.reviewed_at = datetime.utcnow()

                if member.emerging_dialectic_id:
                    ed = await db.get(EmergingDialectic, member.emerging_dialectic_id)
                    if ed:
                        ed.status = new_emerging_status
                        ed.reviewed_at = datetime.utcnow()

    await db.commit()
    await db.refresh(cluster)
    return ChallengeClusterResponse.model_validate(cluster)


# =============================================================================
# CHALLENGE DASHBOARD
# =============================================================================

# =============================================================================
# CLUSTERING OPERATIONS
# =============================================================================

@app.post("/challenges/cluster", response_model=ClusteringResponse)
async def trigger_clustering(
    request: ClusteringRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Trigger LLM clustering on pending challenges.

    This groups similar challenges from multiple projects for batch review.
    Uses Claude Opus 4.5 for intelligent similarity analysis.
    """
    from .clustering import run_full_clustering

    start_time = datetime.utcnow()

    result = await run_full_clustering(db)

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return ClusteringResponse(
        clusters_created=result.get("total_clusters_created", 0),
        challenges_clustered=result.get("total_items_clustered", 0),
        emerging_concepts_clustered=result.get("emerging_concept_clusters", {}).get("clustered", 0) if result.get("emerging_concept_clusters") else 0,
        emerging_dialectics_clustered=0,  # TODO: implement
        processing_time_seconds=result.get("processing_time_seconds", 0)
    )


@app.get("/challenges/dashboard", response_model=ChallengeDashboardStats)
async def get_challenge_dashboard(db: AsyncSession = Depends(get_db)):
    """Get challenge dashboard statistics."""
    # Count challenges by type (concept vs dialectic)
    concept_impacts = await db.scalar(
        select(func.count(Challenge.id)).where(Challenge.concept_id.isnot(None))
    )
    dialectic_impacts = await db.scalar(
        select(func.count(Challenge.id)).where(Challenge.dialectic_id.isnot(None))
    )

    # Count emerging
    emerging_concepts = await db.scalar(select(func.count(EmergingConcept.id)))
    emerging_dialectics = await db.scalar(select(func.count(EmergingDialectic.id)))

    # Pending counts
    pending_challenges = await db.scalar(
        select(func.count(Challenge.id)).where(Challenge.status == ChallengeStatus.PENDING)
    )
    pending_clusters = await db.scalar(
        select(func.count(ChallengeCluster.id)).where(ChallengeCluster.status == ClusterStatus.PENDING)
    )

    # Resolved this week (simplified - just count resolved)
    resolved_this_week = await db.scalar(
        select(func.count(ChallengeCluster.id)).where(
            ChallengeCluster.status == ClusterStatus.RESOLVED
        )
    )

    # Source projects
    project_result = await db.execute(
        select(
            Challenge.source_project_id,
            Challenge.source_project_name,
            func.count(Challenge.id).label('count')
        ).group_by(
            Challenge.source_project_id,
            Challenge.source_project_name
        )
    )
    source_projects = [
        {"id": row[0], "name": row[1] or f"Project {row[0]}", "count": row[2]}
        for row in project_result.fetchall()
    ]

    return ChallengeDashboardStats(
        concept_impacts=concept_impacts or 0,
        dialectic_impacts=dialectic_impacts or 0,
        emerging_concepts=emerging_concepts or 0,
        emerging_dialectics=emerging_dialectics or 0,
        pending_challenges=pending_challenges or 0,
        pending_clusters=pending_clusters or 0,
        resolved_this_week=resolved_this_week or 0,
        source_projects=source_projects
    )
