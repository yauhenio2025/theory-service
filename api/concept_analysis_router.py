"""
Concept Analysis Router - Operation-Indexed Schema API

This router provides endpoints for the 8-dimensional concept analysis framework,
where concepts are analyzed through analytical operations rather than thinker-indexed dimensions.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from datetime import datetime

from .database import get_db
from .concept_analysis_models import (
    AnalyticalDimension, AnalyticalOperation, TheoreticalInfluence,
    AnalyzedConcept, ConceptAnalysis, AnalysisItem, ConceptAnalysisHistory,
    ItemReasoningScaffold, ItemRelationship, DimensionType, OutputType, SourceType,
    WebCentrality, InferenceType, ItemRelationType, RelationshipSource, operation_influences
)

router = APIRouter(prefix="/concept-analysis", tags=["Concept Analysis"])


# ==================== PYDANTIC SCHEMAS ====================

class TheoreticalInfluenceResponse(BaseModel):
    id: int
    short_name: str
    full_name: str
    years: Optional[str] = None
    key_works: Optional[list] = None
    core_insight: Optional[str] = None
    wikipedia_url: Optional[str] = None
    contribution_note: Optional[str] = None  # How this thinker contributes to an operation

    class Config:
        from_attributes = True


class AnalyticalOperationResponse(BaseModel):
    id: int
    dimension_id: int
    name: str
    description: Optional[str] = None
    key_questions: Optional[list] = None
    output_type: Optional[str] = None
    example_prompt: Optional[str] = None
    sequence_order: int = 0
    influences: List[TheoreticalInfluenceResponse] = []

    class Config:
        from_attributes = True


class AnalyticalDimensionResponse(BaseModel):
    id: int
    dimension_type: str
    name: str
    core_question: str
    description: Optional[str] = None
    color_scheme: Optional[str] = None
    icon: Optional[str] = None
    sequence_order: int = 0
    operations: List[AnalyticalOperationResponse] = []

    class Config:
        from_attributes = True


class ReasoningScaffoldResponse(BaseModel):
    """Quinean intermediate reasoning layer for an analysis item."""
    id: int

    # Derivation chain
    inference_type: Optional[str] = None  # deductive, material, default, abductive, etc.
    inference_rule: Optional[str] = None
    premises: Optional[list] = None  # [{claim, claim_type, centrality, source}]
    reasoning_trace: Optional[str] = None

    # Source context
    derivation_trigger: Optional[str] = None
    source_passage: Optional[str] = None
    source_location: Optional[str] = None

    # Alternatives considered
    alternatives_rejected: Optional[list] = None

    # Strength decomposition
    premise_confidence: Optional[float] = None
    inference_validity: Optional[float] = None
    source_quality: Optional[float] = None
    web_coherence: Optional[float] = None
    confidence_explanation: Optional[str] = None

    # Revisability
    revisability_cost: Optional[str] = None
    dependent_claims: Optional[list] = None

    # Web connections
    supports_items: Optional[list] = None
    supported_by_items: Optional[list] = None
    tension_with_items: Optional[list] = None

    class Config:
        from_attributes = True


class ItemRelationshipResponse(BaseModel):
    """Response model for item relationships."""
    id: int
    related_item_id: int
    related_item_content: str
    relationship_type: str
    direction: str  # 'outgoing' or 'incoming'
    confidence: float = 0.8
    explanation: Optional[str] = None
    discovered_via: Optional[str] = None

    class Config:
        from_attributes = True


class AnalysisItemResponse(BaseModel):
    id: int
    item_type: str
    content: str
    strength: Optional[float] = None
    severity: Optional[str] = None
    subtype: Optional[str] = None
    extra_data: Optional[dict] = None
    sequence_order: int = 0

    # Quinean web of belief fields
    web_centrality: Optional[str] = None
    observation_proximity: Optional[float] = None
    coherence_score: Optional[float] = None

    # Provenance
    provenance_type: Optional[str] = None
    created_via: Optional[str] = None

    # Reasoning scaffold (optional, for rich reasoning display)
    reasoning_scaffold: Optional[ReasoningScaffoldResponse] = None

    # Item relationships (linked items)
    relationships: List[ItemRelationshipResponse] = []

    class Config:
        from_attributes = True


class ConceptAnalysisResponse(BaseModel):
    id: int
    concept_id: int
    operation_id: int
    canonical_statement: Optional[str] = None
    analysis_data: Optional[dict] = None
    version: str = "1.0"
    confidence: float = 0.8
    source_type: str = "llm_generated"
    notes: Optional[str] = None
    items: List[AnalysisItemResponse] = []

    # Nested info for convenience
    operation_name: Optional[str] = None
    dimension_name: Optional[str] = None
    dimension_type: Optional[str] = None

    class Config:
        from_attributes = True


class AnalyzedConceptResponse(BaseModel):
    id: int
    term: str
    definition: Optional[str] = None
    author: Optional[str] = None
    source_work: Optional[str] = None
    year: Optional[int] = None
    is_user_concept: bool = True
    paradigm: Optional[str] = None
    disciplinary_home: Optional[str] = None
    analysis_count: int = 0

    class Config:
        from_attributes = True


class FullConceptAnalysisResponse(BaseModel):
    """Complete analysis of a concept across all dimensions and operations."""
    concept: AnalyzedConceptResponse
    dimensions: List[AnalyticalDimensionResponse]
    analyses_by_dimension: dict  # dimension_type -> list of analyses


# ==================== ENDPOINTS ====================

@router.get("/dimensions", response_model=List[AnalyticalDimensionResponse])
async def list_dimensions(
    include_operations: bool = True,
    db: AsyncSession = Depends(get_db)
):
    """
    List all analytical dimensions.

    Optionally includes operations within each dimension.
    """
    query = select(AnalyticalDimension).order_by(AnalyticalDimension.sequence_order)

    if include_operations:
        query = query.options(
            selectinload(AnalyticalDimension.operations).selectinload(AnalyticalOperation.influences)
        )

    result = await db.execute(query)
    dimensions = result.scalars().all()

    responses = []
    for dim in dimensions:
        dim_resp = AnalyticalDimensionResponse(
            id=dim.id,
            dimension_type=dim.dimension_type.value,
            name=dim.name,
            core_question=dim.core_question,
            description=dim.description,
            color_scheme=dim.color_scheme,
            icon=dim.icon,
            sequence_order=dim.sequence_order,
            operations=[]
        )

        if include_operations and dim.operations:
            for op in sorted(dim.operations, key=lambda x: x.sequence_order):
                op_resp = AnalyticalOperationResponse(
                    id=op.id,
                    dimension_id=op.dimension_id,
                    name=op.name,
                    description=op.description,
                    key_questions=op.key_questions,
                    output_type=op.output_type.value if op.output_type else None,
                    example_prompt=op.example_prompt,
                    sequence_order=op.sequence_order,
                    influences=[
                        TheoreticalInfluenceResponse(
                            id=inf.id,
                            short_name=inf.short_name,
                            full_name=inf.full_name,
                            years=inf.years,
                            key_works=inf.key_works,
                            core_insight=inf.core_insight,
                            wikipedia_url=inf.wikipedia_url
                        )
                        for inf in op.influences
                    ]
                )
                dim_resp.operations.append(op_resp)

        responses.append(dim_resp)

    return responses


@router.get("/dimensions/{dimension_type}", response_model=AnalyticalDimensionResponse)
async def get_dimension(
    dimension_type: DimensionType,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific dimension with its operations."""
    result = await db.execute(
        select(AnalyticalDimension)
        .options(selectinload(AnalyticalDimension.operations).selectinload(AnalyticalOperation.influences))
        .where(AnalyticalDimension.dimension_type == dimension_type)
    )
    dim = result.scalar_one_or_none()

    if not dim:
        raise HTTPException(status_code=404, detail=f"Dimension {dimension_type} not found")

    return AnalyticalDimensionResponse(
        id=dim.id,
        dimension_type=dim.dimension_type.value,
        name=dim.name,
        core_question=dim.core_question,
        description=dim.description,
        color_scheme=dim.color_scheme,
        icon=dim.icon,
        sequence_order=dim.sequence_order,
        operations=[
            AnalyticalOperationResponse(
                id=op.id,
                dimension_id=op.dimension_id,
                name=op.name,
                description=op.description,
                key_questions=op.key_questions,
                output_type=op.output_type.value if op.output_type else None,
                example_prompt=op.example_prompt,
                sequence_order=op.sequence_order,
                influences=[
                    TheoreticalInfluenceResponse(
                        id=inf.id,
                        short_name=inf.short_name,
                        full_name=inf.full_name,
                        years=inf.years,
                        key_works=inf.key_works,
                        core_insight=inf.core_insight,
                        wikipedia_url=inf.wikipedia_url
                    )
                    for inf in op.influences
                ]
            )
            for op in sorted(dim.operations, key=lambda x: x.sequence_order)
        ]
    )


@router.get("/operations", response_model=List[AnalyticalOperationResponse])
async def list_operations(
    dimension_type: Optional[DimensionType] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    List all analytical operations.

    Optionally filter by dimension type.
    """
    query = select(AnalyticalOperation).options(
        selectinload(AnalyticalOperation.influences),
        selectinload(AnalyticalOperation.dimension)
    )

    if dimension_type:
        query = query.join(AnalyticalDimension).where(
            AnalyticalDimension.dimension_type == dimension_type
        )

    query = query.order_by(AnalyticalOperation.dimension_id, AnalyticalOperation.sequence_order)

    result = await db.execute(query)
    operations = result.scalars().all()

    return [
        AnalyticalOperationResponse(
            id=op.id,
            dimension_id=op.dimension_id,
            name=op.name,
            description=op.description,
            key_questions=op.key_questions,
            output_type=op.output_type.value if op.output_type else None,
            example_prompt=op.example_prompt,
            sequence_order=op.sequence_order,
            influences=[
                TheoreticalInfluenceResponse(
                    id=inf.id,
                    short_name=inf.short_name,
                    full_name=inf.full_name,
                    years=inf.years,
                    key_works=inf.key_works,
                    core_insight=inf.core_insight,
                    wikipedia_url=inf.wikipedia_url
                )
                for inf in op.influences
            ]
        )
        for op in operations
    ]


@router.get("/influences", response_model=List[TheoreticalInfluenceResponse])
async def list_influences(db: AsyncSession = Depends(get_db)):
    """List all theoretical influences (thinkers)."""
    result = await db.execute(
        select(TheoreticalInfluence).order_by(TheoreticalInfluence.short_name)
    )
    influences = result.scalars().all()

    return [
        TheoreticalInfluenceResponse(
            id=inf.id,
            short_name=inf.short_name,
            full_name=inf.full_name,
            years=inf.years,
            key_works=inf.key_works,
            core_insight=inf.core_insight,
            wikipedia_url=inf.wikipedia_url
        )
        for inf in influences
    ]


@router.get("/concepts", response_model=List[AnalyzedConceptResponse])
async def list_concepts(
    search: Optional[str] = None,
    paradigm: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all analyzed concepts."""
    query = select(AnalyzedConcept)

    if search:
        query = query.where(AnalyzedConcept.term.ilike(f"%{search}%"))
    if paradigm:
        query = query.where(AnalyzedConcept.paradigm == paradigm)

    query = query.order_by(AnalyzedConcept.term)

    result = await db.execute(query)
    concepts = result.scalars().all()

    responses = []
    for c in concepts:
        # Get analysis count
        count_result = await db.execute(
            select(ConceptAnalysis).where(ConceptAnalysis.concept_id == c.id)
        )
        analysis_count = len(count_result.scalars().all())

        responses.append(AnalyzedConceptResponse(
            id=c.id,
            term=c.term,
            definition=c.definition,
            author=c.author,
            source_work=c.source_work,
            year=c.year,
            is_user_concept=c.is_user_concept,
            paradigm=c.paradigm,
            disciplinary_home=c.disciplinary_home,
            analysis_count=analysis_count
        ))

    return responses


@router.get("/concepts/{concept_id}", response_model=FullConceptAnalysisResponse)
async def get_concept_full_analysis(
    concept_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a concept with its full analysis across all dimensions.

    This is the main endpoint for viewing a complete concept analysis.
    """
    # Get concept
    concept_result = await db.execute(
        select(AnalyzedConcept).where(AnalyzedConcept.id == concept_id)
    )
    concept = concept_result.scalar_one_or_none()

    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")

    # Get all dimensions with operations
    dims_result = await db.execute(
        select(AnalyticalDimension)
        .options(selectinload(AnalyticalDimension.operations).selectinload(AnalyticalOperation.influences))
        .order_by(AnalyticalDimension.sequence_order)
    )
    dimensions = dims_result.scalars().all()

    # Get all analyses for this concept
    analyses_result = await db.execute(
        select(ConceptAnalysis)
        .options(
            selectinload(ConceptAnalysis.operation).selectinload(AnalyticalOperation.dimension),
            selectinload(ConceptAnalysis.items).selectinload(AnalysisItem.reasoning_scaffold)
        )
        .where(ConceptAnalysis.concept_id == concept_id)
    )
    analyses = analyses_result.scalars().all()

    # Group analyses by dimension
    analyses_by_dimension = {}
    for analysis in analyses:
        dim_type = analysis.operation.dimension.dimension_type.value
        if dim_type not in analyses_by_dimension:
            analyses_by_dimension[dim_type] = []

        analyses_by_dimension[dim_type].append(ConceptAnalysisResponse(
            id=analysis.id,
            concept_id=analysis.concept_id,
            operation_id=analysis.operation_id,
            canonical_statement=analysis.canonical_statement,
            analysis_data=analysis.analysis_data,
            version=analysis.version,
            confidence=analysis.confidence,
            source_type=analysis.source_type.value if analysis.source_type else "llm_generated",
            notes=analysis.notes,
            operation_name=analysis.operation.name,
            dimension_name=analysis.operation.dimension.name,
            dimension_type=dim_type,
            items=[
                AnalysisItemResponse(
                    id=item.id,
                    item_type=item.item_type,
                    content=item.content,
                    strength=item.strength,
                    severity=item.severity,
                    subtype=item.subtype,
                    extra_data=item.extra_data,
                    sequence_order=item.sequence_order,
                    web_centrality=item.web_centrality.value if item.web_centrality else None,
                    observation_proximity=item.observation_proximity,
                    coherence_score=item.coherence_score,
                    provenance_type=item.provenance_type.value if item.provenance_type else None,
                    created_via=item.created_via,
                    reasoning_scaffold=ReasoningScaffoldResponse(
                        id=item.reasoning_scaffold.id,
                        inference_type=item.reasoning_scaffold.inference_type.value if item.reasoning_scaffold.inference_type else None,
                        inference_rule=item.reasoning_scaffold.inference_rule,
                        premises=item.reasoning_scaffold.premises,
                        reasoning_trace=item.reasoning_scaffold.reasoning_trace,
                        derivation_trigger=item.reasoning_scaffold.derivation_trigger,
                        source_passage=item.reasoning_scaffold.source_passage,
                        source_location=item.reasoning_scaffold.source_location,
                        alternatives_rejected=item.reasoning_scaffold.alternatives_rejected,
                        premise_confidence=item.reasoning_scaffold.premise_confidence,
                        inference_validity=item.reasoning_scaffold.inference_validity,
                        source_quality=item.reasoning_scaffold.source_quality,
                        web_coherence=item.reasoning_scaffold.web_coherence,
                        confidence_explanation=item.reasoning_scaffold.confidence_explanation,
                        revisability_cost=item.reasoning_scaffold.revisability_cost,
                        dependent_claims=item.reasoning_scaffold.dependent_claims,
                        supports_items=item.reasoning_scaffold.supports_items,
                        supported_by_items=item.reasoning_scaffold.supported_by_items,
                        tension_with_items=item.reasoning_scaffold.tension_with_items,
                    ) if item.reasoning_scaffold else None
                )
                for item in sorted(analysis.items, key=lambda x: x.sequence_order)
            ]
        ))

    # Build dimension responses
    dimension_responses = []
    for dim in dimensions:
        dim_resp = AnalyticalDimensionResponse(
            id=dim.id,
            dimension_type=dim.dimension_type.value,
            name=dim.name,
            core_question=dim.core_question,
            description=dim.description,
            color_scheme=dim.color_scheme,
            icon=dim.icon,
            sequence_order=dim.sequence_order,
            operations=[
                AnalyticalOperationResponse(
                    id=op.id,
                    dimension_id=op.dimension_id,
                    name=op.name,
                    description=op.description,
                    key_questions=op.key_questions,
                    output_type=op.output_type.value if op.output_type else None,
                    example_prompt=op.example_prompt,
                    sequence_order=op.sequence_order,
                    influences=[
                        TheoreticalInfluenceResponse(
                            id=inf.id,
                            short_name=inf.short_name,
                            full_name=inf.full_name,
                            years=inf.years,
                            key_works=inf.key_works,
                            core_insight=inf.core_insight,
                            wikipedia_url=inf.wikipedia_url
                        )
                        for inf in op.influences
                    ]
                )
                for op in sorted(dim.operations, key=lambda x: x.sequence_order)
            ]
        )
        dimension_responses.append(dim_resp)

    # Count analyses for concept response
    analysis_count = len(analyses)

    return FullConceptAnalysisResponse(
        concept=AnalyzedConceptResponse(
            id=concept.id,
            term=concept.term,
            definition=concept.definition,
            author=concept.author,
            source_work=concept.source_work,
            year=concept.year,
            is_user_concept=concept.is_user_concept,
            paradigm=concept.paradigm,
            disciplinary_home=concept.disciplinary_home,
            analysis_count=analysis_count
        ),
        dimensions=dimension_responses,
        analyses_by_dimension=analyses_by_dimension
    )


@router.get("/concepts/{concept_id}/dimension/{dimension_type}")
async def get_concept_dimension_analysis(
    concept_id: int,
    dimension_type: DimensionType,
    db: AsyncSession = Depends(get_db)
):
    """Get all analyses for a concept within a specific dimension."""
    # Get dimension
    dim_result = await db.execute(
        select(AnalyticalDimension)
        .options(selectinload(AnalyticalDimension.operations))
        .where(AnalyticalDimension.dimension_type == dimension_type)
    )
    dimension = dim_result.scalar_one_or_none()

    if not dimension:
        raise HTTPException(status_code=404, detail=f"Dimension {dimension_type} not found")

    operation_ids = [op.id for op in dimension.operations]

    # Get analyses with items, scaffolds, and relationships
    analyses_result = await db.execute(
        select(ConceptAnalysis)
        .options(
            selectinload(ConceptAnalysis.operation),
            selectinload(ConceptAnalysis.items)
                .selectinload(AnalysisItem.reasoning_scaffold),
            selectinload(ConceptAnalysis.items)
                .selectinload(AnalysisItem.outgoing_relationships)
                .selectinload(ItemRelationship.target_item),
            selectinload(ConceptAnalysis.items)
                .selectinload(AnalysisItem.incoming_relationships)
                .selectinload(ItemRelationship.source_item),
        )
        .where(
            ConceptAnalysis.concept_id == concept_id,
            ConceptAnalysis.operation_id.in_(operation_ids)
        )
    )
    analyses = analyses_result.scalars().all()

    # Helper to build relationships for an item
    def build_relationships(item):
        relationships = []
        # Outgoing relationships (this item -> other items)
        for rel in getattr(item, 'outgoing_relationships', []):
            if rel.is_active:
                relationships.append(ItemRelationshipResponse(
                    id=rel.id,
                    related_item_id=rel.target_item_id,
                    related_item_content=rel.target_item.content[:100] if rel.target_item else "",
                    relationship_type=rel.relationship_type.value,
                    direction='outgoing',
                    confidence=rel.confidence or 0.8,
                    explanation=rel.explanation,
                    discovered_via=rel.discovered_via.value if rel.discovered_via else None,
                ))
        # Incoming relationships (other items -> this item)
        for rel in getattr(item, 'incoming_relationships', []):
            if rel.is_active:
                relationships.append(ItemRelationshipResponse(
                    id=rel.id,
                    related_item_id=rel.source_item_id,
                    related_item_content=rel.source_item.content[:100] if rel.source_item else "",
                    relationship_type=rel.relationship_type.value,
                    direction='incoming',
                    confidence=rel.confidence or 0.8,
                    explanation=rel.explanation,
                    discovered_via=rel.discovered_via.value if rel.discovered_via else None,
                ))
        return relationships

    return {
        "dimension": {
            "type": dimension_type.value,
            "name": dimension.name,
            "core_question": dimension.core_question
        },
        "analyses": [
            ConceptAnalysisResponse(
                id=a.id,
                concept_id=a.concept_id,
                operation_id=a.operation_id,
                canonical_statement=a.canonical_statement,
                analysis_data=a.analysis_data,
                version=a.version,
                confidence=a.confidence,
                source_type=a.source_type.value if a.source_type else "llm_generated",
                notes=a.notes,
                operation_name=a.operation.name,
                dimension_name=dimension.name,
                dimension_type=dimension_type.value,
                items=[
                    AnalysisItemResponse(
                        id=item.id,
                        item_type=item.item_type,
                        content=item.content,
                        strength=item.strength,
                        severity=item.severity,
                        subtype=item.subtype,
                        extra_data=item.extra_data,
                        sequence_order=item.sequence_order,
                        web_centrality=item.web_centrality.value if item.web_centrality else None,
                        observation_proximity=item.observation_proximity,
                        coherence_score=item.coherence_score,
                        provenance_type=item.provenance_type.value if item.provenance_type else None,
                        created_via=item.created_via,
                        reasoning_scaffold=ReasoningScaffoldResponse(
                            id=item.reasoning_scaffold.id,
                            inference_type=item.reasoning_scaffold.inference_type.value if item.reasoning_scaffold.inference_type else None,
                            inference_rule=item.reasoning_scaffold.inference_rule,
                            premises=item.reasoning_scaffold.premises,
                            reasoning_trace=item.reasoning_scaffold.reasoning_trace,
                            derivation_trigger=item.reasoning_scaffold.derivation_trigger,
                            source_passage=item.reasoning_scaffold.source_passage,
                            source_location=item.reasoning_scaffold.source_location,
                            alternatives_rejected=item.reasoning_scaffold.alternatives_rejected,
                            premise_confidence=item.reasoning_scaffold.premise_confidence,
                            inference_validity=item.reasoning_scaffold.inference_validity,
                            source_quality=item.reasoning_scaffold.source_quality,
                            web_coherence=item.reasoning_scaffold.web_coherence,
                            confidence_explanation=item.reasoning_scaffold.confidence_explanation,
                            revisability_cost=item.reasoning_scaffold.revisability_cost,
                            dependent_claims=item.reasoning_scaffold.dependent_claims,
                            supports_items=item.reasoning_scaffold.supports_items,
                            supported_by_items=item.reasoning_scaffold.supported_by_items,
                            tension_with_items=item.reasoning_scaffold.tension_with_items,
                        ) if item.reasoning_scaffold else None,
                        relationships=build_relationships(item)
                    )
                    for item in sorted(a.items, key=lambda x: x.sequence_order)
                ]
            )
            for a in analyses
        ]
    }


@router.get("/schema-overview")
async def get_schema_overview(db: AsyncSession = Depends(get_db)):
    """
    Get a high-level overview of the analytical schema.

    Returns counts and summary statistics for dimensions, operations, influences, and concepts.
    """
    # Count dimensions
    dims_result = await db.execute(select(AnalyticalDimension))
    dimensions = dims_result.scalars().all()

    # Count operations
    ops_result = await db.execute(select(AnalyticalOperation))
    operations = ops_result.scalars().all()

    # Count influences
    infs_result = await db.execute(select(TheoreticalInfluence))
    influences = infs_result.scalars().all()

    # Count concepts
    concepts_result = await db.execute(select(AnalyzedConcept))
    concepts = concepts_result.scalars().all()

    # Count analyses
    analyses_result = await db.execute(select(ConceptAnalysis))
    analyses = analyses_result.scalars().all()

    return {
        "dimensions_count": len(dimensions),
        "operations_count": len(operations),
        "influences_count": len(influences),
        "concepts_count": len(concepts),
        "analyses_count": len(analyses),
        "dimensions": [
            {
                "type": d.dimension_type.value,
                "name": d.name,
                "core_question": d.core_question
            }
            for d in sorted(dimensions, key=lambda x: x.sequence_order)
        ],
        "influences": [
            {
                "short_name": i.short_name,
                "full_name": i.full_name
            }
            for i in sorted(influences, key=lambda x: x.short_name)
        ]
    }
