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
from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload

from .database import get_db, init_db, close_db
from .models import Concept, Dialectic, Claim, Challenge, Refinement
from .models import ConceptStatus, DialecticStatus, ChallengeStatus
from .schemas import (
    ConceptCreate, ConceptUpdate, ConceptResponse,
    DialecticCreate, DialecticUpdate, DialecticResponse,
    ClaimCreate, ClaimUpdate, ClaimResponse,
    ChallengeCreate, ChallengeResponse, ChallengeReview,
    TheorySyncResponse, BulkChallengeCreate, BulkChallengeResponse
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
# CONCEPTS
# =============================================================================

@app.get("/concepts", response_model=List[ConceptResponse])
async def list_concepts(
    status: Optional[ConceptStatus] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all concepts, optionally filtered."""
    query = select(Concept)

    if status:
        query = query.where(Concept.status == status)
    if category:
        query = query.where(Concept.category == category)
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

    # Add challenge counts
    responses = []
    for c in concepts:
        challenge_count = await db.scalar(
            select(func.count(Challenge.id)).where(Challenge.concept_id == c.id)
        )
        resp = ConceptResponse.model_validate(c)
        resp.challenge_count = challenge_count or 0
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
    db: AsyncSession = Depends(get_db)
):
    """List all dialectics."""
    query = select(Dialectic)

    if status:
        query = query.where(Dialectic.status == status)
    if category:
        query = query.where(Dialectic.category == category)

    query = query.order_by(Dialectic.name)
    result = await db.execute(query)
    dialectics = result.scalars().all()

    responses = []
    for d in dialectics:
        challenge_count = await db.scalar(
            select(func.count(Challenge.id)).where(Challenge.dialectic_id == d.id)
        )
        resp = DialecticResponse.model_validate(d)
        resp.challenge_count = challenge_count or 0
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
    db: AsyncSession = Depends(get_db)
):
    """List all claims."""
    query = select(Claim)

    if active_only:
        query = query.where(Claim.is_active == True)
    if category:
        query = query.where(Claim.category == category)

    query = query.order_by(Claim.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


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
    db: AsyncSession = Depends(get_db)
):
    """
    Get complete theory state for essay-flow to sync.
    Returns all active concepts, dialectics, and claims.
    """
    # Get concepts
    concept_query = select(Concept)
    if not include_inactive:
        concept_query = concept_query.where(Concept.status.in_([ConceptStatus.ACTIVE, ConceptStatus.CHALLENGED]))
    concept_result = await db.execute(concept_query.order_by(Concept.term))
    concepts = concept_result.scalars().all()

    # Get dialectics
    dialectic_query = select(Dialectic)
    if not include_inactive:
        dialectic_query = dialectic_query.where(Dialectic.status.in_([DialecticStatus.ACTIVE]))
    dialectic_result = await db.execute(dialectic_query.order_by(Dialectic.name))
    dialectics = dialectic_result.scalars().all()

    # Get claims
    claim_query = select(Claim)
    if not include_inactive:
        claim_query = claim_query.where(Claim.is_active == True)
    claim_result = await db.execute(claim_query.order_by(Claim.created_at.desc()))
    claims = claim_result.scalars().all()

    return TheorySyncResponse(
        concepts=[ConceptResponse.model_validate(c) for c in concepts],
        dialectics=[DialecticResponse.model_validate(d) for d in dialectics],
        claims=[ClaimResponse.model_validate(c) for c in claims],
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
