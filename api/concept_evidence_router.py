"""
Concept Evidence Router - Evidence Integration API

This router provides endpoints for evidence-driven concept refinement,
including source management, fragment analysis, and decision handling.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func, update
from sqlalchemy.orm import selectinload
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

from .database import get_db
from .concept_analysis_models import (
    AnalyzedConcept, AnalyticalOperation, AnalyticalDimension, AnalysisItem, ConceptAnalysis,
    ConceptEvidenceSource, ConceptEvidenceFragment, ConceptEvidenceInterpretation,
    ConceptStructuralChange, ConceptEvidenceDecision, ConceptEvidenceProgress,
    EvidenceSourceType, ExtractionStatus, AnalysisStatus, EvidenceRelationship,
    ChangeType, ProvenanceType
)

router = APIRouter(prefix="/concepts/{concept_id}/evidence", tags=["Concept Evidence"])


# ==================== PYDANTIC SCHEMAS ====================

class EvidenceSourceCreate(BaseModel):
    source_type: str = Field(..., description="Type: article, book, news, thinker_work, url, manual")
    source_name: str = Field(..., description="Name/citation of the source")
    source_url: Optional[str] = None
    source_date: Optional[datetime] = None
    source_content: str = Field(..., description="Full text or excerpt to analyze")


class EvidenceSourceResponse(BaseModel):
    id: int
    concept_id: int
    source_type: str
    source_name: str
    source_url: Optional[str] = None
    source_date: Optional[datetime] = None
    extraction_status: str
    extraction_error: Optional[str] = None
    extracted_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class EvidenceFragmentResponse(BaseModel):
    id: int
    source_id: int
    content: str
    source_location: Optional[str] = None
    analysis_status: str
    relationship_type: Optional[str] = None
    target_operation_id: Optional[int] = None
    target_operation_name: Optional[str] = None
    target_dimension_name: Optional[str] = None
    confidence: Optional[float] = None
    is_ambiguous: bool = False
    why_needs_decision: Optional[str] = None
    source_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class StructuralChangeResponse(BaseModel):
    id: int
    change_type: str
    target_operation_id: Optional[int] = None
    target_operation_name: Optional[str] = None
    target_item_id: Optional[int] = None
    before_content: Optional[str] = None
    after_content: Optional[str] = None
    commitment_statement: Optional[str] = None
    foreclosure_statements: Optional[List[str]] = None
    display_order: int = 0

    class Config:
        from_attributes = True


class InterpretationResponse(BaseModel):
    id: int
    fragment_id: int
    interpretation_key: Optional[str] = None
    title: str
    strategy: Optional[str] = None
    rationale: Optional[str] = None
    relationship_type: Optional[str] = None
    target_operation_id: Optional[int] = None
    target_operation_name: Optional[str] = None
    is_selected: bool = False
    is_recommended: bool = False
    recommendation_rationale: Optional[str] = None
    display_order: int = 0
    structural_changes: List[StructuralChangeResponse] = []

    class Config:
        from_attributes = True


class PendingDecisionResponse(BaseModel):
    fragment: EvidenceFragmentResponse
    interpretations: List[InterpretationResponse]
    decision_index: int  # 1-based index for "Decision X of Y"
    total_pending: int


class DecisionSubmit(BaseModel):
    interpretation_id: int
    accepted_change_ids: List[int] = []
    rejected_change_ids: List[int] = []
    decision_notes: Optional[str] = None


class EvidenceProgressResponse(BaseModel):
    concept_id: int
    total_sources: int = 0
    total_fragments: int = 0
    auto_integrated_count: int = 0
    needs_decision_count: int = 0
    resolved_count: int = 0
    skipped_count: int = 0
    last_updated: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== HELPER FUNCTIONS ====================

async def get_or_create_progress(db: AsyncSession, concept_id: int) -> ConceptEvidenceProgress:
    """Get or create evidence progress record for a concept."""
    result = await db.execute(
        select(ConceptEvidenceProgress).where(ConceptEvidenceProgress.concept_id == concept_id)
    )
    progress = result.scalar_one_or_none()

    if not progress:
        progress = ConceptEvidenceProgress(concept_id=concept_id)
        db.add(progress)
        await db.flush()

    return progress


async def update_progress_counts(db: AsyncSession, concept_id: int):
    """Recalculate and update progress counts."""
    progress = await get_or_create_progress(db, concept_id)

    # Count sources
    sources_result = await db.execute(
        select(sql_func.count(ConceptEvidenceSource.id))
        .where(ConceptEvidenceSource.concept_id == concept_id)
    )
    progress.total_sources = sources_result.scalar() or 0

    # Count all fragments for this concept's sources
    fragments_result = await db.execute(
        select(sql_func.count(ConceptEvidenceFragment.id))
        .join(ConceptEvidenceSource)
        .where(ConceptEvidenceSource.concept_id == concept_id)
    )
    progress.total_fragments = fragments_result.scalar() or 0

    # Count by status
    for status, attr in [
        (AnalysisStatus.AUTO_INTEGRATED, 'auto_integrated_count'),
        (AnalysisStatus.NEEDS_DECISION, 'needs_decision_count'),
        (AnalysisStatus.RESOLVED, 'resolved_count'),
    ]:
        count_result = await db.execute(
            select(sql_func.count(ConceptEvidenceFragment.id))
            .join(ConceptEvidenceSource)
            .where(
                ConceptEvidenceSource.concept_id == concept_id,
                ConceptEvidenceFragment.analysis_status == status
            )
        )
        setattr(progress, attr, count_result.scalar() or 0)

    # Count skipped decisions
    skipped_result = await db.execute(
        select(sql_func.count(ConceptEvidenceDecision.id))
        .where(
            ConceptEvidenceDecision.concept_id == concept_id,
            ConceptEvidenceDecision.skipped == True
        )
    )
    progress.skipped_count = skipped_result.scalar() or 0

    await db.flush()


# ==================== ENDPOINTS ====================

# --- Source Management ---

@router.post("/sources", response_model=EvidenceSourceResponse)
async def add_evidence_source(
    concept_id: int,
    source: EvidenceSourceCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Add a new evidence source to analyze.

    The source content will be queued for extraction.
    """
    # Verify concept exists
    concept_result = await db.execute(
        select(AnalyzedConcept).where(AnalyzedConcept.id == concept_id)
    )
    if not concept_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Concept not found")

    # Validate source type
    try:
        source_type_enum = EvidenceSourceType(source.source_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid source_type. Must be one of: {[e.value for e in EvidenceSourceType]}"
        )

    # Create source
    new_source = ConceptEvidenceSource(
        concept_id=concept_id,
        source_type=source_type_enum,
        source_name=source.source_name,
        source_url=source.source_url,
        source_date=source.source_date,
        source_content=source.source_content,
        extraction_status=ExtractionStatus.PENDING
    )
    db.add(new_source)
    await db.flush()
    await db.refresh(new_source)

    # Update progress
    await update_progress_counts(db, concept_id)
    await db.commit()

    return EvidenceSourceResponse(
        id=new_source.id,
        concept_id=new_source.concept_id,
        source_type=new_source.source_type.value,
        source_name=new_source.source_name,
        source_url=new_source.source_url,
        source_date=new_source.source_date,
        extraction_status=new_source.extraction_status.value,
        extraction_error=new_source.extraction_error,
        extracted_count=new_source.extracted_count,
        created_at=new_source.created_at
    )


@router.get("/sources", response_model=List[EvidenceSourceResponse])
async def list_evidence_sources(
    concept_id: int,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all evidence sources for a concept."""
    query = select(ConceptEvidenceSource).where(
        ConceptEvidenceSource.concept_id == concept_id
    )

    if status:
        try:
            status_enum = ExtractionStatus(status)
            query = query.where(ConceptEvidenceSource.extraction_status == status_enum)
        except ValueError:
            pass

    query = query.order_by(ConceptEvidenceSource.created_at.desc())

    result = await db.execute(query)
    sources = result.scalars().all()

    return [
        EvidenceSourceResponse(
            id=s.id,
            concept_id=s.concept_id,
            source_type=s.source_type.value,
            source_name=s.source_name,
            source_url=s.source_url,
            source_date=s.source_date,
            extraction_status=s.extraction_status.value,
            extraction_error=s.extraction_error,
            extracted_count=s.extracted_count,
            created_at=s.created_at
        )
        for s in sources
    ]


@router.delete("/sources/{source_id}")
async def delete_evidence_source(
    concept_id: int,
    source_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete an evidence source and all its fragments."""
    result = await db.execute(
        select(ConceptEvidenceSource).where(
            ConceptEvidenceSource.id == source_id,
            ConceptEvidenceSource.concept_id == concept_id
        )
    )
    source = result.scalar_one_or_none()

    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    await db.delete(source)
    await update_progress_counts(db, concept_id)
    await db.commit()

    return {"status": "deleted", "source_id": source_id}


# --- Fragment Management ---

@router.get("/fragments", response_model=List[EvidenceFragmentResponse])
async def list_fragments(
    concept_id: int,
    status: Optional[str] = None,
    source_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    List evidence fragments for a concept.

    Filter by analysis status or source.
    """
    query = (
        select(ConceptEvidenceFragment)
        .join(ConceptEvidenceSource)
        .options(
            selectinload(ConceptEvidenceFragment.source),
            selectinload(ConceptEvidenceFragment.target_operation).selectinload(AnalyticalOperation.dimension)
        )
        .where(ConceptEvidenceSource.concept_id == concept_id)
    )

    if status:
        try:
            status_enum = AnalysisStatus(status)
            query = query.where(ConceptEvidenceFragment.analysis_status == status_enum)
        except ValueError:
            pass

    if source_id:
        query = query.where(ConceptEvidenceFragment.source_id == source_id)

    query = query.order_by(ConceptEvidenceFragment.created_at.desc())

    result = await db.execute(query)
    fragments = result.scalars().all()

    return [
        EvidenceFragmentResponse(
            id=f.id,
            source_id=f.source_id,
            content=f.content,
            source_location=f.source_location,
            analysis_status=f.analysis_status.value if f.analysis_status else "pending",
            relationship_type=f.relationship_type.value if f.relationship_type else None,
            target_operation_id=f.target_operation_id,
            target_operation_name=f.target_operation.name if f.target_operation else None,
            target_dimension_name=f.target_operation.dimension.name if f.target_operation and f.target_operation.dimension else None,
            confidence=f.confidence,
            is_ambiguous=f.is_ambiguous,
            why_needs_decision=f.why_needs_decision,
            source_name=f.source.source_name if f.source else None,
            created_at=f.created_at
        )
        for f in fragments
    ]


# --- Pending Decisions ---

@router.get("/decisions/pending", response_model=Optional[PendingDecisionResponse])
async def get_pending_decision(
    concept_id: int,
    index: int = Query(0, ge=0, description="Zero-based index into pending decisions"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific pending decision by index.

    Returns the fragment with its interpretations and structural changes.
    """
    # Get all pending fragments
    query = (
        select(ConceptEvidenceFragment)
        .join(ConceptEvidenceSource)
        .options(
            selectinload(ConceptEvidenceFragment.source),
            selectinload(ConceptEvidenceFragment.target_operation).selectinload(AnalyticalOperation.dimension),
            selectinload(ConceptEvidenceFragment.interpretations).selectinload(
                ConceptEvidenceInterpretation.structural_changes
            ).selectinload(ConceptStructuralChange.target_operation)
        )
        .where(
            ConceptEvidenceSource.concept_id == concept_id,
            ConceptEvidenceFragment.analysis_status == AnalysisStatus.NEEDS_DECISION
        )
        .order_by(ConceptEvidenceFragment.created_at)
    )

    result = await db.execute(query)
    pending = result.scalars().all()

    if not pending:
        return None

    total = len(pending)
    if index >= total:
        index = total - 1

    fragment = pending[index]

    # Build response
    interpretations = []
    for interp in sorted(fragment.interpretations, key=lambda x: x.display_order):
        changes = []
        for change in sorted(interp.structural_changes, key=lambda x: x.display_order):
            changes.append(StructuralChangeResponse(
                id=change.id,
                change_type=change.change_type.value if change.change_type else "revision",
                target_operation_id=change.target_operation_id,
                target_operation_name=change.target_operation.name if change.target_operation else None,
                target_item_id=change.target_item_id,
                before_content=change.before_content,
                after_content=change.after_content,
                commitment_statement=change.commitment_statement,
                foreclosure_statements=change.foreclosure_statements,
                display_order=change.display_order
            ))

        # Get operation name for interpretation
        op_name = None
        if interp.target_operation_id:
            op_result = await db.execute(
                select(AnalyticalOperation).where(AnalyticalOperation.id == interp.target_operation_id)
            )
            op = op_result.scalar_one_or_none()
            if op:
                op_name = op.name

        interpretations.append(InterpretationResponse(
            id=interp.id,
            fragment_id=interp.fragment_id,
            interpretation_key=interp.interpretation_key,
            title=interp.title,
            strategy=interp.strategy,
            rationale=interp.rationale,
            relationship_type=interp.relationship_type.value if interp.relationship_type else None,
            target_operation_id=interp.target_operation_id,
            target_operation_name=op_name,
            is_selected=interp.is_selected,
            is_recommended=interp.is_recommended,
            recommendation_rationale=interp.recommendation_rationale,
            display_order=interp.display_order,
            structural_changes=changes
        ))

    return PendingDecisionResponse(
        fragment=EvidenceFragmentResponse(
            id=fragment.id,
            source_id=fragment.source_id,
            content=fragment.content,
            source_location=fragment.source_location,
            analysis_status=fragment.analysis_status.value,
            relationship_type=fragment.relationship_type.value if fragment.relationship_type else None,
            target_operation_id=fragment.target_operation_id,
            target_operation_name=fragment.target_operation.name if fragment.target_operation else None,
            target_dimension_name=fragment.target_operation.dimension.name if fragment.target_operation and fragment.target_operation.dimension else None,
            confidence=fragment.confidence,
            is_ambiguous=fragment.is_ambiguous,
            why_needs_decision=fragment.why_needs_decision,
            source_name=fragment.source.source_name if fragment.source else None,
            created_at=fragment.created_at
        ),
        interpretations=interpretations,
        decision_index=index + 1,
        total_pending=total
    )


@router.post("/decisions")
async def submit_decision(
    concept_id: int,
    decision: DecisionSubmit,
    db: AsyncSession = Depends(get_db)
):
    """
    Submit a decision for a pending evidence fragment.

    This applies the selected interpretation and structural changes.
    """
    # Get the interpretation
    interp_result = await db.execute(
        select(ConceptEvidenceInterpretation)
        .options(
            selectinload(ConceptEvidenceInterpretation.fragment),
            selectinload(ConceptEvidenceInterpretation.structural_changes)
        )
        .where(ConceptEvidenceInterpretation.id == decision.interpretation_id)
    )
    interpretation = interp_result.scalar_one_or_none()

    if not interpretation:
        raise HTTPException(status_code=404, detail="Interpretation not found")

    fragment = interpretation.fragment

    # Mark interpretation as selected
    interpretation.is_selected = True

    # Create decision record
    evidence_decision = ConceptEvidenceDecision(
        concept_id=concept_id,
        fragment_id=fragment.id,
        selected_interpretation_id=interpretation.id,
        accepted_change_ids=decision.accepted_change_ids,
        rejected_change_ids=decision.rejected_change_ids,
        decision_notes=decision.decision_notes,
        skipped=False
    )
    db.add(evidence_decision)
    await db.flush()

    # Apply accepted structural changes
    for change in interpretation.structural_changes:
        if change.id in decision.accepted_change_ids:
            await apply_structural_change(db, concept_id, fragment, change, evidence_decision.id)

    # Update fragment status
    fragment.analysis_status = AnalysisStatus.RESOLVED

    # Update progress
    await update_progress_counts(db, concept_id)
    await db.commit()

    return {
        "status": "applied",
        "fragment_id": fragment.id,
        "interpretation_id": interpretation.id,
        "changes_applied": len(decision.accepted_change_ids),
        "changes_rejected": len(decision.rejected_change_ids)
    }


@router.post("/decisions/{fragment_id}/skip")
async def skip_decision(
    concept_id: int,
    fragment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Skip a pending decision without applying any changes."""
    # Get fragment
    result = await db.execute(
        select(ConceptEvidenceFragment)
        .join(ConceptEvidenceSource)
        .where(
            ConceptEvidenceFragment.id == fragment_id,
            ConceptEvidenceSource.concept_id == concept_id
        )
    )
    fragment = result.scalar_one_or_none()

    if not fragment:
        raise HTTPException(status_code=404, detail="Fragment not found")

    # Create skipped decision record
    decision = ConceptEvidenceDecision(
        concept_id=concept_id,
        fragment_id=fragment_id,
        skipped=True
    )
    db.add(decision)

    # Keep status as needs_decision but track skip
    await update_progress_counts(db, concept_id)
    await db.commit()

    return {"status": "skipped", "fragment_id": fragment_id}


async def apply_structural_change(
    db: AsyncSession,
    concept_id: int,
    fragment: ConceptEvidenceFragment,
    change: ConceptStructuralChange,
    decision_id: int
):
    """Apply a structural change to the concept analysis."""
    if change.change_type == ChangeType.ADDITION:
        # Get the analysis for this operation
        analysis_result = await db.execute(
            select(ConceptAnalysis).where(
                ConceptAnalysis.concept_id == concept_id,
                ConceptAnalysis.operation_id == change.target_operation_id
            )
        )
        analysis = analysis_result.scalar_one_or_none()

        if analysis:
            # Create new item with provenance
            new_item = AnalysisItem(
                analysis_id=analysis.id,
                item_type="evidence_addition",
                content=change.after_content,
                provenance_type=ProvenanceType.EVIDENCE,
                provenance_source_id=fragment.id,
                provenance_decision_id=decision_id,
                created_via="evidence_decision"
            )
            db.add(new_item)

    elif change.change_type == ChangeType.REVISION and change.target_item_id:
        # Get the existing item
        item_result = await db.execute(
            select(AnalysisItem).where(AnalysisItem.id == change.target_item_id)
        )
        existing_item = item_result.scalar_one_or_none()

        if existing_item:
            # Mark old item as superseded
            existing_item.is_active = False

            # Create new item that supersedes it
            new_item = AnalysisItem(
                analysis_id=existing_item.analysis_id,
                item_type=existing_item.item_type,
                content=change.after_content,
                strength=existing_item.strength,
                severity=existing_item.severity,
                subtype=existing_item.subtype,
                extra_data=existing_item.extra_data,
                sequence_order=existing_item.sequence_order,
                provenance_type=ProvenanceType.EVIDENCE,
                provenance_source_id=fragment.id,
                provenance_decision_id=decision_id,
                created_via="evidence_decision",
                supersedes_item_id=existing_item.id,
                is_active=True
            )
            db.add(new_item)

    elif change.change_type == ChangeType.DELETION and change.target_item_id:
        # Mark item as inactive
        await db.execute(
            update(AnalysisItem)
            .where(AnalysisItem.id == change.target_item_id)
            .values(is_active=False)
        )


# --- Progress ---

@router.get("/progress", response_model=EvidenceProgressResponse)
async def get_evidence_progress(
    concept_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get evidence integration progress for a concept."""
    progress = await get_or_create_progress(db, concept_id)
    await update_progress_counts(db, concept_id)
    await db.commit()

    return EvidenceProgressResponse(
        concept_id=progress.concept_id,
        total_sources=progress.total_sources,
        total_fragments=progress.total_fragments,
        auto_integrated_count=progress.auto_integrated_count,
        needs_decision_count=progress.needs_decision_count,
        resolved_count=progress.resolved_count,
        skipped_count=progress.skipped_count,
        last_updated=progress.last_updated
    )


# --- LLM-Powered Extraction and Analysis ---

from .concept_evidence_llm import (
    extract_fragments_from_source as llm_extract_fragments,
    analyze_fragment as llm_analyze_fragment,
    generate_interpretations as llm_generate_interpretations,
    add_commitment_foreclosure as llm_add_commitment_foreclosure,
    get_likely_item_type
)


def get_concept_summary(concept, analyses) -> str:
    """Build a summary of current concept analysis for LLM context."""
    parts = [f"Concept: {concept.term}"]
    if concept.definition:
        parts.append(f"Definition: {concept.definition}")

    for analysis in analyses[:5]:
        if analysis.canonical_statement:
            parts.append(f"- {analysis.canonical_statement[:200]}")

    return "\n".join(parts)


@router.post("/sources/{source_id}/extract")
async def extract_from_source(
    concept_id: int,
    source_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Extract fragments from a source using LLM analysis.

    This processes the source content and creates evidence fragments
    that can then be analyzed for integration into the concept.
    """
    # Get source
    result = await db.execute(
        select(ConceptEvidenceSource).where(
            ConceptEvidenceSource.id == source_id,
            ConceptEvidenceSource.concept_id == concept_id
        )
    )
    source = result.scalar_one_or_none()

    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    # Get concept
    concept_result = await db.execute(
        select(AnalyzedConcept)
        .options(selectinload(AnalyzedConcept.analyses))
        .where(AnalyzedConcept.id == concept_id)
    )
    concept = concept_result.scalar_one_or_none()

    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")

    # Update status to processing
    source.extraction_status = ExtractionStatus.PROCESSING
    await db.flush()

    try:
        # Call LLM to extract fragments
        fragments_data = await llm_extract_fragments(
            concept_term=concept.term,
            concept_definition=concept.definition or "",
            concept_summary=get_concept_summary(concept, concept.analyses),
            source_name=source.source_name,
            source_type=source.source_type.value,
            source_content=source.source_content
        )

        # Create fragment records
        created_fragments = []
        for frag_data in fragments_data:
            fragment = ConceptEvidenceFragment(
                source_id=source_id,
                content=frag_data.get("content", ""),
                source_location=frag_data.get("source_location"),
                analysis_status=AnalysisStatus.PENDING,
                extraction_metadata={
                    "likely_dimension": frag_data.get("likely_dimension"),
                    "extraction_note": frag_data.get("extraction_note")
                }
            )
            db.add(fragment)
            created_fragments.append(fragment)

        # Update source
        source.extraction_status = ExtractionStatus.COMPLETED
        source.extracted_count = len(created_fragments)

        await update_progress_counts(db, concept_id)
        await db.commit()

        return {
            "status": "completed",
            "source_id": source_id,
            "fragments_extracted": len(created_fragments),
            "message": f"Extracted {len(created_fragments)} fragments. Use POST /fragments/{{id}}/analyze to analyze each."
        }

    except Exception as e:
        source.extraction_status = ExtractionStatus.FAILED
        source.extraction_error = str(e)
        await db.commit()
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


@router.post("/fragments/{fragment_id}/analyze")
async def analyze_fragment_endpoint(
    concept_id: int,
    fragment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Analyze a fragment to determine how it relates to the concept.

    High-confidence, non-ambiguous fragments are auto-integrated.
    Ambiguous fragments get interpretations generated for user decision.
    """
    # Get fragment with source
    result = await db.execute(
        select(ConceptEvidenceFragment)
        .options(selectinload(ConceptEvidenceFragment.source))
        .join(ConceptEvidenceSource)
        .where(
            ConceptEvidenceFragment.id == fragment_id,
            ConceptEvidenceSource.concept_id == concept_id
        )
    )
    fragment = result.scalar_one_or_none()

    if not fragment:
        raise HTTPException(status_code=404, detail="Fragment not found")

    # Get concept with analyses
    concept_result = await db.execute(
        select(AnalyzedConcept)
        .options(
            selectinload(AnalyzedConcept.analyses)
            .selectinload(ConceptAnalysis.operation)
            .selectinload(AnalyticalOperation.dimension)
        )
        .where(AnalyzedConcept.id == concept_id)
    )
    concept = concept_result.scalar_one_or_none()

    # Determine likely dimension from extraction metadata
    likely_dimension = fragment.extraction_metadata.get("likely_dimension", "positional") if fragment.extraction_metadata else "positional"

    # Find relevant operation for this dimension
    dimension_operations = []
    for analysis in concept.analyses:
        if analysis.operation and analysis.operation.dimension:
            if analysis.operation.dimension.type.value.lower() == likely_dimension.lower():
                dimension_operations.append(analysis)

    # Get existing items for context
    existing_items = []
    current_analysis = {}

    if dimension_operations:
        target_analysis = dimension_operations[0]
        current_analysis = target_analysis.analysis_data or {}

        # Get items
        items_result = await db.execute(
            select(AnalysisItem)
            .where(AnalysisItem.analysis_id == target_analysis.id)
            .order_by(AnalysisItem.sequence_order)
        )
        items = items_result.scalars().all()
        existing_items = [{"id": i.id, "content": i.content, "item_type": i.item_type} for i in items]

    try:
        # Analyze fragment
        analysis_result = await llm_analyze_fragment(
            concept_term=concept.term,
            concept_definition=concept.definition or "",
            fragment_content=fragment.content,
            source_name=fragment.source.source_name if fragment.source else "Unknown",
            dimension_name=likely_dimension,
            current_analysis=current_analysis,
            existing_items=existing_items
        )

        # Update fragment with analysis results
        fragment.relationship_type = EvidenceRelationship(analysis_result.get("relationship_type", "illustrates"))
        fragment.confidence = analysis_result.get("confidence", 0.5)
        fragment.is_ambiguous = analysis_result.get("is_ambiguous", True)
        fragment.why_needs_decision = analysis_result.get("why_needs_decision")

        # Find target operation
        if analysis_result.get("target_operation_name") and dimension_operations:
            for analysis in dimension_operations:
                if analysis.operation.name.lower() == analysis_result["target_operation_name"].lower():
                    fragment.target_operation_id = analysis.operation.id
                    break

        if not fragment.target_operation_id and dimension_operations:
            fragment.target_operation_id = dimension_operations[0].operation.id

        # Decision: auto-integrate or generate interpretations
        if fragment.confidence >= 0.85 and not fragment.is_ambiguous:
            # AUTO-INTEGRATE
            auto_content = analysis_result.get("auto_integration_content", fragment.content)
            auto_item_type = analysis_result.get("auto_integration_item_type", get_likely_item_type(likely_dimension, fragment.relationship_type.value))

            # Find or create analysis for this operation
            if fragment.target_operation_id:
                analysis_record = await db.execute(
                    select(ConceptAnalysis).where(
                        ConceptAnalysis.concept_id == concept_id,
                        ConceptAnalysis.operation_id == fragment.target_operation_id
                    )
                )
                target_analysis = analysis_record.scalar_one_or_none()

                if target_analysis:
                    new_item = AnalysisItem(
                        analysis_id=target_analysis.id,
                        item_type=auto_item_type,
                        content=auto_content,
                        provenance_type=ProvenanceType.EVIDENCE,
                        provenance_source_id=fragment.id,
                        created_via="evidence_auto_integrate"
                    )
                    db.add(new_item)

            fragment.analysis_status = AnalysisStatus.AUTO_INTEGRATED
            await update_progress_counts(db, concept_id)
            await db.commit()

            return {
                "status": "auto_integrated",
                "fragment_id": fragment_id,
                "relationship_type": fragment.relationship_type.value,
                "confidence": fragment.confidence,
                "message": "Fragment auto-integrated based on high confidence."
            }

        else:
            # GENERATE INTERPRETATIONS for user decision
            interpretations_data = await llm_generate_interpretations(
                concept_term=concept.term,
                fragment_content=fragment.content,
                source_name=fragment.source.source_name if fragment.source else "Unknown",
                why_ambiguous=fragment.why_needs_decision or "Multiple valid interpretations possible",
                current_analysis=current_analysis,
                existing_items=existing_items
            )

            # Add commitment/foreclosure
            cf_data = await llm_add_commitment_foreclosure(
                concept_term=concept.term,
                fragment_content=fragment.content,
                interpretations=interpretations_data
            )

            # Create interpretation records
            for i, interp_data in enumerate(interpretations_data):
                interp = ConceptEvidenceInterpretation(
                    fragment_id=fragment_id,
                    interpretation_key=interp_data.get("key", chr(ord('a') + i)),
                    title=interp_data.get("title", f"Interpretation {i+1}"),
                    strategy=interp_data.get("strategy"),
                    rationale=interp_data.get("rationale"),
                    relationship_type=EvidenceRelationship(interp_data.get("relationship_type", "illustrates")) if interp_data.get("relationship_type") else None,
                    is_recommended=interp_data.get("is_recommended", False),
                    recommendation_rationale=interp_data.get("recommendation_rationale"),
                    display_order=i
                )

                # Add commitment/foreclosure from separate call
                key = interp_data.get("key", chr(ord('a') + i))
                if key in cf_data:
                    interp.commitment_statement = cf_data[key].get("commitment_statement")
                    interp.foreclosure_statements = cf_data[key].get("foreclosure_statements", [])

                db.add(interp)
                await db.flush()

                # Create structural changes
                for j, change_data in enumerate(interp_data.get("structural_changes", [])):
                    # Find target operation
                    target_op_id = None
                    if change_data.get("target_operation_name"):
                        for analysis in concept.analyses:
                            if analysis.operation and analysis.operation.name.lower() == change_data["target_operation_name"].lower():
                                target_op_id = analysis.operation.id
                                break

                    change = ConceptStructuralChange(
                        interpretation_id=interp.id,
                        change_type=ChangeType(change_data.get("change_type", "addition")),
                        target_operation_id=target_op_id or fragment.target_operation_id,
                        target_item_id=change_data.get("target_item_id"),
                        before_content=change_data.get("before_content"),
                        after_content=change_data.get("after_content"),
                        commitment_statement=cf_data.get(key, {}).get("commitment_statement"),
                        foreclosure_statements=cf_data.get(key, {}).get("foreclosure_statements", []),
                        display_order=j
                    )
                    db.add(change)

            fragment.analysis_status = AnalysisStatus.NEEDS_DECISION
            await update_progress_counts(db, concept_id)
            await db.commit()

            return {
                "status": "needs_decision",
                "fragment_id": fragment_id,
                "relationship_type": fragment.relationship_type.value,
                "confidence": fragment.confidence,
                "interpretations_count": len(interpretations_data),
                "message": "Fragment requires decision. Use GET /decisions/pending to review."
            }

    except Exception as e:
        fragment.analysis_status = AnalysisStatus.PENDING
        await db.commit()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/sources/{source_id}/extract-and-analyze")
async def extract_and_analyze_source(
    concept_id: int,
    source_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Full pipeline: extract fragments from source, then analyze each.

    Convenience endpoint that combines extraction and analysis in one call.
    """
    # First extract
    extract_result = await extract_from_source(concept_id, source_id, db)

    if extract_result["status"] != "completed":
        return extract_result

    # Get all fragments for this source
    fragments_result = await db.execute(
        select(ConceptEvidenceFragment)
        .where(ConceptEvidenceFragment.source_id == source_id)
    )
    fragments = fragments_result.scalars().all()

    # Analyze each
    results = {
        "auto_integrated": 0,
        "needs_decision": 0,
        "failed": 0
    }

    for fragment in fragments:
        try:
            analysis_result = await analyze_fragment_endpoint(concept_id, fragment.id, db)
            if analysis_result["status"] == "auto_integrated":
                results["auto_integrated"] += 1
            else:
                results["needs_decision"] += 1
        except Exception as e:
            results["failed"] += 1

    return {
        "status": "completed",
        "source_id": source_id,
        "fragments_extracted": extract_result["fragments_extracted"],
        "auto_integrated": results["auto_integrated"],
        "needs_decision": results["needs_decision"],
        "failed": results["failed"],
        "message": f"Processed {extract_result['fragments_extracted']} fragments."
    }


# ==================== WIZARD BRIDGE ENDPOINTS ====================
# These endpoints bridge wizard outputs to the 8D schema

class WizardBridgeRequest(BaseModel):
    """Request to bridge wizard data to 8D schema."""
    wizard_data: dict = Field(..., description="Full wizard output with hypothesis_cards, genealogy_cards, etc.")


class WizardBridgeResponse(BaseModel):
    """Response from wizard bridge operation."""
    analyzed_concept_id: Optional[int] = None
    analyses_created: int = 0
    items_created: int = 0
    relationships_created: int = 0
    errors: List[str] = []


@router.post("/bridge-wizard", response_model=WizardBridgeResponse)
async def bridge_wizard_to_schema(
    concept_id: int,
    request: WizardBridgeRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Bridge wizard outputs to 8D schema for an existing analyzed concept.

    This endpoint is useful for:
    1. Retroactively populating 8D schema for concepts created before the bridge
    2. Re-processing wizard outputs after schema updates
    3. Testing the bridge logic

    The wizard_data should include:
    - hypothesis_cards: List of detected theses/claims
    - genealogy_cards: List of thinker influences
    - differentiation_cards: List of concept differentiations
    - dimensional_signals: Per-dimension signals (quinean, sellarsian, etc.)
    - epistemic_blind_spots: Areas needing clarification
    - Stage answers: core_definition, problem_addressed, etc.
    """
    from .wizard_to_schema_bridge import bridge_wizard_to_schema as do_bridge

    # Get the existing analyzed concept
    result = await db.execute(
        select(AnalyzedConcept).where(AnalyzedConcept.id == concept_id)
    )
    analyzed_concept = result.scalar_one_or_none()

    if not analyzed_concept:
        raise HTTPException(status_code=404, detail=f"Analyzed concept {concept_id} not found")

    # Run the bridge
    bridge_result = await do_bridge(
        db=db,
        concept_name=analyzed_concept.term,
        wizard_data=request.wizard_data,
        wizard_session_id=None  # No wizard session for retroactive bridge
    )

    return WizardBridgeResponse(
        analyzed_concept_id=bridge_result.get("analyzed_concept_id"),
        analyses_created=bridge_result.get("analyses_created", 0),
        items_created=bridge_result.get("items_created", 0),
        relationships_created=bridge_result.get("relationships_created", 0),
        errors=bridge_result.get("errors", [])
    )
