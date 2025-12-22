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
    DimensionType, OutputType, SourceType, operation_influences
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


class AnalysisItemResponse(BaseModel):
    id: int
    item_type: str
    content: str
    strength: Optional[float] = None
    severity: Optional[str] = None
    subtype: Optional[str] = None
    extra_data: Optional[dict] = None
    sequence_order: int = 0

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
            selectinload(ConceptAnalysis.items)
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
                    sequence_order=item.sequence_order
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

    # Get analyses
    analyses_result = await db.execute(
        select(ConceptAnalysis)
        .options(
            selectinload(ConceptAnalysis.operation),
            selectinload(ConceptAnalysis.items)
        )
        .where(
            ConceptAnalysis.concept_id == concept_id,
            ConceptAnalysis.operation_id.in_(operation_ids)
        )
    )
    analyses = analyses_result.scalars().all()

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
                        sequence_order=item.sequence_order
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
