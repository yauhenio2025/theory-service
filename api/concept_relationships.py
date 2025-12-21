"""
Concept Relationships Router
API endpoints for managing relationships between concepts (internal and external).
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from .database import get_db
from .models import (
    Concept, ExternalConcept, ConceptRelationship,
    RelationshipType as RelationshipTypeModel
)
from .schemas import (
    ExternalConceptCreate, ExternalConceptUpdate, ExternalConceptResponse,
    ConceptRelationshipCreate, ConceptRelationshipUpdate, ConceptRelationshipResponse,
    RelationshipType
)

router = APIRouter(prefix="/concept-relationships", tags=["Concept Relationships"])


# =============================================================================
# EXTERNAL CONCEPTS
# =============================================================================

@router.get("/external-concepts", response_model=List[ExternalConceptResponse])
async def list_external_concepts(
    author: Optional[str] = None,
    paradigm: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = Query(default=50, le=200),
    db: AsyncSession = Depends(get_db)
):
    """List external concepts, optionally filtered."""
    query = select(ExternalConcept)

    if author:
        query = query.where(ExternalConcept.author.ilike(f"%{author}%"))
    if paradigm:
        query = query.where(ExternalConcept.paradigm.ilike(f"%{paradigm}%"))
    if search:
        query = query.where(
            or_(
                ExternalConcept.term.ilike(f"%{search}%"),
                ExternalConcept.brief_definition.ilike(f"%{search}%"),
                ExternalConcept.author.ilike(f"%{search}%")
            )
        )

    query = query.order_by(ExternalConcept.term).limit(limit)
    result = await db.execute(query)
    concepts = result.scalars().all()

    return [ExternalConceptResponse.model_validate(c) for c in concepts]


@router.get("/external-concepts/{concept_id}", response_model=ExternalConceptResponse)
async def get_external_concept(concept_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific external concept."""
    result = await db.execute(
        select(ExternalConcept).where(ExternalConcept.id == concept_id)
    )
    concept = result.scalar_one_or_none()
    if not concept:
        raise HTTPException(status_code=404, detail="External concept not found")

    return ExternalConceptResponse.model_validate(concept)


@router.post("/external-concepts", response_model=ExternalConceptResponse, status_code=201)
async def create_external_concept(
    data: ExternalConceptCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new external concept."""
    concept = ExternalConcept(**data.model_dump())
    db.add(concept)
    await db.commit()
    await db.refresh(concept)
    return ExternalConceptResponse.model_validate(concept)


@router.patch("/external-concepts/{concept_id}", response_model=ExternalConceptResponse)
async def update_external_concept(
    concept_id: int,
    data: ExternalConceptUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an external concept."""
    result = await db.execute(
        select(ExternalConcept).where(ExternalConcept.id == concept_id)
    )
    concept = result.scalar_one_or_none()
    if not concept:
        raise HTTPException(status_code=404, detail="External concept not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(concept, field, value)

    await db.commit()
    await db.refresh(concept)
    return ExternalConceptResponse.model_validate(concept)


@router.delete("/external-concepts/{concept_id}", status_code=204)
async def delete_external_concept(concept_id: int, db: AsyncSession = Depends(get_db)):
    """Delete an external concept."""
    result = await db.execute(
        select(ExternalConcept).where(ExternalConcept.id == concept_id)
    )
    concept = result.scalar_one_or_none()
    if not concept:
        raise HTTPException(status_code=404, detail="External concept not found")

    await db.delete(concept)
    await db.commit()


# =============================================================================
# CONCEPT RELATIONSHIPS
# =============================================================================

@router.get("/relationships", response_model=List[ConceptRelationshipResponse])
async def list_relationships(
    concept_id: Optional[int] = None,
    external_concept_id: Optional[int] = None,
    relationship_type: Optional[RelationshipType] = None,
    limit: int = Query(default=50, le=200),
    db: AsyncSession = Depends(get_db)
):
    """
    List concept relationships, optionally filtered.

    If concept_id or external_concept_id is provided, returns relationships
    where that concept appears as either source or target.
    """
    query = select(ConceptRelationship)

    if concept_id:
        query = query.where(
            or_(
                ConceptRelationship.concept_id == concept_id,
                ConceptRelationship.related_concept_id == concept_id
            )
        )
    if external_concept_id:
        query = query.where(
            or_(
                ConceptRelationship.external_concept_id == external_concept_id,
                ConceptRelationship.related_external_concept_id == external_concept_id
            )
        )
    if relationship_type:
        query = query.where(ConceptRelationship.relationship_type == relationship_type)

    query = query.order_by(ConceptRelationship.created_at.desc()).limit(limit)
    result = await db.execute(query)
    relationships = result.scalars().all()

    # Enrich with concept terms for display
    responses = []
    for rel in relationships:
        resp = ConceptRelationshipResponse.model_validate(rel)

        # Load related concept terms
        if rel.concept_id:
            concept = await db.get(Concept, rel.concept_id)
            if concept:
                resp.concept_term = concept.term

        if rel.external_concept_id:
            ext_concept = await db.get(ExternalConcept, rel.external_concept_id)
            if ext_concept:
                resp.external_concept_term = ext_concept.term

        if rel.related_concept_id:
            related = await db.get(Concept, rel.related_concept_id)
            if related:
                resp.related_concept_term = related.term

        if rel.related_external_concept_id:
            related_ext = await db.get(ExternalConcept, rel.related_external_concept_id)
            if related_ext:
                resp.related_external_concept_term = related_ext.term

        responses.append(resp)

    return responses


@router.get("/relationships/{relationship_id}", response_model=ConceptRelationshipResponse)
async def get_relationship(relationship_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific concept relationship."""
    result = await db.execute(
        select(ConceptRelationship).where(ConceptRelationship.id == relationship_id)
    )
    rel = result.scalar_one_or_none()
    if not rel:
        raise HTTPException(status_code=404, detail="Relationship not found")

    resp = ConceptRelationshipResponse.model_validate(rel)

    # Load related concept terms
    if rel.concept_id:
        concept = await db.get(Concept, rel.concept_id)
        if concept:
            resp.concept_term = concept.term

    if rel.external_concept_id:
        ext_concept = await db.get(ExternalConcept, rel.external_concept_id)
        if ext_concept:
            resp.external_concept_term = ext_concept.term

    if rel.related_concept_id:
        related = await db.get(Concept, rel.related_concept_id)
        if related:
            resp.related_concept_term = related.term

    if rel.related_external_concept_id:
        related_ext = await db.get(ExternalConcept, rel.related_external_concept_id)
        if related_ext:
            resp.related_external_concept_term = related_ext.term

    return resp


@router.post("/relationships", response_model=ConceptRelationshipResponse, status_code=201)
async def create_relationship(
    data: ConceptRelationshipCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new concept relationship."""
    # Validate source concept
    if not data.concept_id and not data.external_concept_id:
        raise HTTPException(
            status_code=400,
            detail="Either concept_id or external_concept_id must be provided"
        )
    if data.concept_id and data.external_concept_id:
        raise HTTPException(
            status_code=400,
            detail="Only one of concept_id or external_concept_id can be provided"
        )

    # Validate target concept
    if not data.related_concept_id and not data.related_external_concept_id:
        raise HTTPException(
            status_code=400,
            detail="Either related_concept_id or related_external_concept_id must be provided"
        )
    if data.related_concept_id and data.related_external_concept_id:
        raise HTTPException(
            status_code=400,
            detail="Only one of related_concept_id or related_external_concept_id can be provided"
        )

    # Convert Pydantic dimensional models to dicts for JSON storage
    rel_data = data.model_dump()
    for dim in ['sellarsian', 'brandomian', 'deleuzian', 'hacking',
                'bachelardian', 'quinean', 'carey', 'blumenberg', 'canguilhem']:
        if rel_data.get(dim):
            rel_data[dim] = dict(rel_data[dim])

    relationship = ConceptRelationship(**rel_data)
    db.add(relationship)
    await db.commit()
    await db.refresh(relationship)

    return ConceptRelationshipResponse.model_validate(relationship)


@router.patch("/relationships/{relationship_id}", response_model=ConceptRelationshipResponse)
async def update_relationship(
    relationship_id: int,
    data: ConceptRelationshipUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a concept relationship."""
    result = await db.execute(
        select(ConceptRelationship).where(ConceptRelationship.id == relationship_id)
    )
    rel = result.scalar_one_or_none()
    if not rel:
        raise HTTPException(status_code=404, detail="Relationship not found")

    update_data = data.model_dump(exclude_unset=True)

    # Convert Pydantic dimensional models to dicts for JSON storage
    for dim in ['sellarsian', 'brandomian', 'deleuzian', 'hacking',
                'bachelardian', 'quinean', 'carey', 'blumenberg', 'canguilhem']:
        if dim in update_data and update_data[dim]:
            update_data[dim] = dict(update_data[dim])

    for field, value in update_data.items():
        setattr(rel, field, value)

    await db.commit()
    await db.refresh(rel)
    return ConceptRelationshipResponse.model_validate(rel)


@router.delete("/relationships/{relationship_id}", status_code=204)
async def delete_relationship(relationship_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a concept relationship."""
    result = await db.execute(
        select(ConceptRelationship).where(ConceptRelationship.id == relationship_id)
    )
    rel = result.scalar_one_or_none()
    if not rel:
        raise HTTPException(status_code=404, detail="Relationship not found")

    await db.delete(rel)
    await db.commit()


# =============================================================================
# RELATIONSHIP QUERIES
# =============================================================================

@router.get("/concepts/{concept_id}/relationships", response_model=List[ConceptRelationshipResponse])
async def get_concept_relationships(
    concept_id: int,
    relationship_type: Optional[RelationshipType] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all relationships for a specific internal concept."""
    # Verify concept exists
    concept = await db.get(Concept, concept_id)
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")

    query = select(ConceptRelationship).where(
        or_(
            ConceptRelationship.concept_id == concept_id,
            ConceptRelationship.related_concept_id == concept_id
        )
    )

    if relationship_type:
        query = query.where(ConceptRelationship.relationship_type == relationship_type)

    result = await db.execute(query)
    relationships = result.scalars().all()

    # Enrich with concept terms
    responses = []
    for rel in relationships:
        resp = ConceptRelationshipResponse.model_validate(rel)

        if rel.concept_id:
            c = await db.get(Concept, rel.concept_id)
            if c:
                resp.concept_term = c.term

        if rel.external_concept_id:
            ext = await db.get(ExternalConcept, rel.external_concept_id)
            if ext:
                resp.external_concept_term = ext.term

        if rel.related_concept_id:
            rc = await db.get(Concept, rel.related_concept_id)
            if rc:
                resp.related_concept_term = rc.term

        if rel.related_external_concept_id:
            rec = await db.get(ExternalConcept, rel.related_external_concept_id)
            if rec:
                resp.related_external_concept_term = rec.term

        responses.append(resp)

    return responses


@router.get("/relationships/by-type/{relationship_type}", response_model=List[ConceptRelationshipResponse])
async def get_relationships_by_type(
    relationship_type: RelationshipType,
    limit: int = Query(default=50, le=200),
    db: AsyncSession = Depends(get_db)
):
    """Get all relationships of a specific type."""
    result = await db.execute(
        select(ConceptRelationship)
        .where(ConceptRelationship.relationship_type == relationship_type)
        .order_by(ConceptRelationship.created_at.desc())
        .limit(limit)
    )
    relationships = result.scalars().all()

    responses = []
    for rel in relationships:
        resp = ConceptRelationshipResponse.model_validate(rel)

        if rel.concept_id:
            c = await db.get(Concept, rel.concept_id)
            if c:
                resp.concept_term = c.term

        if rel.external_concept_id:
            ext = await db.get(ExternalConcept, rel.external_concept_id)
            if ext:
                resp.external_concept_term = ext.term

        if rel.related_concept_id:
            rc = await db.get(Concept, rel.related_concept_id)
            if rc:
                resp.related_concept_term = rc.term

        if rel.related_external_concept_id:
            rec = await db.get(ExternalConcept, rel.related_external_concept_id)
            if rec:
                resp.related_external_concept_term = rec.term

        responses.append(resp)

    return responses
