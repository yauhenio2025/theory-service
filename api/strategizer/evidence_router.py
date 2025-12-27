"""
Strategizer Evidence Router

Evidence integration API for PDF upload, fragment extraction, and decision handling.
Follows the confidence routing pattern:
- 0.85+: Auto-integrate to grid slot
- 0.60-0.84: Needs user confirmation
- <0.60: Generate interpretation options
"""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func
from sqlalchemy.orm import selectinload

from ..database import get_db
from .models import (
    StrategizerProject, StrategizerDomain, StrategizerUnit, StrategizerGridInstance,
    StrategizerEvidenceSource, StrategizerEvidenceFragment,
    StrategizerEvidenceInterpretation, StrategizerEvidenceDecision,
    EvidenceSourceType, ExtractionStatus, AnalysisStatus, EvidenceRelationship
)
from .schemas import (
    EvidenceSourceCreate, EvidenceSourceResponse,
    EvidenceFragmentResponse, InterpretationResponse,
    PendingDecisionResponse, DecisionRequest, DecisionResponse,
    EvidenceProgressResponse, ExtractRequest
)
from .services.evidence_llm import (
    extract_fragments_from_source,
    analyze_fragment,
    generate_interpretations,
    add_commitment_foreclosure,
    suggest_target_unit
)

router = APIRouter(prefix="/projects/{project_id}/evidence", tags=["Strategizer Evidence"])


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

async def get_project_with_domain(db: AsyncSession, project_id: str):
    """Get project with domain loaded."""
    result = await db.execute(
        select(StrategizerProject)
        .options(selectinload(StrategizerProject.domain))
        .where(StrategizerProject.id == project_id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


async def get_units_as_dicts(db: AsyncSession, project_id: str) -> List[dict]:
    """Get units as list of dicts for LLM context."""
    result = await db.execute(
        select(StrategizerUnit).where(StrategizerUnit.project_id == project_id)
    )
    units = result.scalars().all()
    return [
        {
            "id": u.id,
            "unit_type": u.unit_type.value,
            "name": u.name,
            "definition": u.definition
        }
        for u in units
    ]


async def get_unit_with_grids(db: AsyncSession, unit_id: str):
    """Get unit with grids loaded."""
    result = await db.execute(
        select(StrategizerUnit)
        .options(selectinload(StrategizerUnit.grids))
        .where(StrategizerUnit.id == unit_id)
    )
    return result.scalar_one_or_none()


def grids_to_dicts(grids) -> List[dict]:
    """Convert grid instances to dicts for LLM context."""
    return [
        {
            "grid_type": g.grid_type,
            "tier": g.tier.value if g.tier else "required",
            "slots": g.slots or {}
        }
        for g in grids
    ]


# =============================================================================
# SOURCE MANAGEMENT
# =============================================================================

@router.post("/sources", response_model=EvidenceSourceResponse)
async def add_evidence_source(
    project_id: str,
    source: EvidenceSourceCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Add a new evidence source to analyze.

    Accepts PDF upload (content as base64 or text), URL, or manual text input.
    """
    # Verify project exists
    project = await get_project_with_domain(db, project_id)

    # Validate source type
    try:
        source_type_enum = EvidenceSourceType(source.source_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid source_type. Must be one of: {[e.value for e in EvidenceSourceType]}"
        )

    # Create source
    new_source = StrategizerEvidenceSource(
        project_id=project_id,
        source_type=source_type_enum,
        source_name=source.source_name,
        source_url=source.source_url,
        source_content=source.source_content,
        extraction_status=ExtractionStatus.PENDING
    )
    db.add(new_source)
    await db.flush()
    await db.refresh(new_source)
    await db.commit()

    return EvidenceSourceResponse(
        id=new_source.id,
        project_id=new_source.project_id,
        source_type=new_source.source_type.value,
        source_name=new_source.source_name,
        source_url=new_source.source_url,
        extraction_status=new_source.extraction_status.value,
        extraction_error=new_source.extraction_error,
        extracted_count=new_source.extracted_count,
        created_at=new_source.created_at,
        updated_at=new_source.updated_at
    )


@router.get("/sources", response_model=List[EvidenceSourceResponse])
async def list_evidence_sources(
    project_id: str,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all evidence sources for a project."""
    query = select(StrategizerEvidenceSource).where(
        StrategizerEvidenceSource.project_id == project_id
    )

    if status:
        try:
            status_enum = ExtractionStatus(status)
            query = query.where(StrategizerEvidenceSource.extraction_status == status_enum)
        except ValueError:
            pass

    query = query.order_by(StrategizerEvidenceSource.created_at.desc())

    result = await db.execute(query)
    sources = result.scalars().all()

    return [
        EvidenceSourceResponse(
            id=s.id,
            project_id=s.project_id,
            source_type=s.source_type.value,
            source_name=s.source_name,
            source_url=s.source_url,
            extraction_status=s.extraction_status.value,
            extraction_error=s.extraction_error,
            extracted_count=s.extracted_count,
            created_at=s.created_at,
            updated_at=s.updated_at
        )
        for s in sources
    ]


@router.delete("/sources/{source_id}")
async def delete_evidence_source(
    project_id: str,
    source_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete an evidence source and all its fragments."""
    result = await db.execute(
        select(StrategizerEvidenceSource).where(
            StrategizerEvidenceSource.id == source_id,
            StrategizerEvidenceSource.project_id == project_id
        )
    )
    source = result.scalar_one_or_none()

    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    await db.delete(source)
    await db.commit()

    return {"status": "deleted", "source_id": source_id}


# =============================================================================
# EXTRACTION
# =============================================================================

@router.post("/sources/{source_id}/extract")
async def extract_from_source(
    project_id: str,
    source_id: str,
    request: ExtractRequest = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Extract fragments from a source using LLM analysis.

    Creates evidence fragments that can then be analyzed for integration.
    """
    if request is None:
        request = ExtractRequest()

    # Get source
    result = await db.execute(
        select(StrategizerEvidenceSource).where(
            StrategizerEvidenceSource.id == source_id,
            StrategizerEvidenceSource.project_id == project_id
        )
    )
    source = result.scalar_one_or_none()

    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    # Check if already extracted (unless force)
    if source.extraction_status == ExtractionStatus.COMPLETED and not request.force:
        return {
            "status": "already_extracted",
            "source_id": source_id,
            "fragments_count": source.extracted_count,
            "message": "Use force=true to re-extract"
        }

    # Get project with domain
    project = await get_project_with_domain(db, project_id)

    # Get existing units for context
    units = await get_units_as_dicts(db, project_id)

    # Update status to processing
    source.extraction_status = ExtractionStatus.PROCESSING
    await db.flush()

    try:
        # Call LLM to extract fragments
        domain_name = project.domain.name if project.domain else None
        core_question = project.domain.core_question if project.domain else project.brief

        fragments_data = await extract_fragments_from_source(
            domain_name=domain_name,
            core_question=core_question,
            units=units,
            source_name=source.source_name,
            source_type=source.source_type.value,
            source_content=source.source_content or ""
        )

        # Delete old fragments if re-extracting
        if request.force:
            old_fragments = await db.execute(
                select(StrategizerEvidenceFragment).where(
                    StrategizerEvidenceFragment.source_id == source_id
                )
            )
            for frag in old_fragments.scalars().all():
                await db.delete(frag)

        # Create fragment records
        created_fragments = []
        for frag_data in fragments_data:
            fragment = StrategizerEvidenceFragment(
                source_id=source_id,
                content=frag_data.get("content", ""),
                source_location=frag_data.get("source_location"),
                analysis_status=AnalysisStatus.PENDING,
                extraction_metadata={
                    "likely_unit_type": frag_data.get("likely_unit_type"),
                    "likely_unit_name": frag_data.get("likely_unit_name"),
                    "extraction_note": frag_data.get("extraction_note")
                }
            )
            db.add(fragment)
            created_fragments.append(fragment)

        # Update source
        source.extraction_status = ExtractionStatus.COMPLETED
        source.extracted_count = len(created_fragments)
        source.extraction_error = None

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


# =============================================================================
# FRAGMENT MANAGEMENT
# =============================================================================

@router.get("/fragments", response_model=List[EvidenceFragmentResponse])
async def list_fragments(
    project_id: str,
    status: Optional[str] = None,
    source_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List evidence fragments with optional filtering."""
    query = (
        select(StrategizerEvidenceFragment)
        .join(StrategizerEvidenceSource)
        .options(selectinload(StrategizerEvidenceFragment.source))
        .where(StrategizerEvidenceSource.project_id == project_id)
    )

    if status:
        try:
            status_enum = AnalysisStatus(status)
            query = query.where(StrategizerEvidenceFragment.analysis_status == status_enum)
        except ValueError:
            pass

    if source_id:
        query = query.where(StrategizerEvidenceFragment.source_id == source_id)

    query = query.order_by(StrategizerEvidenceFragment.created_at.desc())

    result = await db.execute(query)
    fragments = result.scalars().all()

    return [
        EvidenceFragmentResponse(
            id=f.id,
            source_id=f.source_id,
            content=f.content,
            source_location=f.source_location,
            analysis_status=f.analysis_status.value,
            relationship_type=f.relationship_type.value if f.relationship_type else None,
            target_unit_id=f.target_unit_id,
            target_grid_slot=f.target_grid_slot,
            confidence=f.confidence,
            is_ambiguous=f.is_ambiguous,
            why_needs_decision=f.why_needs_decision,
            source_name=f.source.source_name if f.source else None,
            created_at=f.created_at
        )
        for f in fragments
    ]


@router.post("/fragments/{fragment_id}/analyze")
async def analyze_fragment_endpoint(
    project_id: str,
    fragment_id: str,
    target_unit_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Analyze a fragment to determine how it relates to strategic units.

    High-confidence fragments are auto-integrated.
    Ambiguous fragments get interpretations generated.
    """
    # Get fragment with source
    result = await db.execute(
        select(StrategizerEvidenceFragment)
        .options(selectinload(StrategizerEvidenceFragment.source))
        .where(StrategizerEvidenceFragment.id == fragment_id)
    )
    fragment = result.scalar_one_or_none()

    if not fragment:
        raise HTTPException(status_code=404, detail="Fragment not found")

    # Verify project ownership
    if fragment.source.project_id != project_id:
        raise HTTPException(status_code=404, detail="Fragment not found in this project")

    # Get project context
    project = await get_project_with_domain(db, project_id)
    domain_name = project.domain.name if project.domain else None
    core_question = project.domain.core_question if project.domain else project.brief

    # Determine target unit
    if not target_unit_id:
        # Use LLM to suggest unit
        units = await get_units_as_dicts(db, project_id)
        suggestion = await suggest_target_unit(
            domain_name=domain_name,
            core_question=core_question,
            units=units,
            fragment_content=fragment.content,
            source_name=fragment.source.source_name
        )

        # Find unit by name
        if suggestion.get("unit_name"):
            unit_result = await db.execute(
                select(StrategizerUnit).where(
                    StrategizerUnit.project_id == project_id,
                    StrategizerUnit.name == suggestion["unit_name"]
                )
            )
            target_unit = unit_result.scalar_one_or_none()
            if target_unit:
                target_unit_id = target_unit.id

    # Get target unit with grids
    target_unit = None
    if target_unit_id:
        target_unit = await get_unit_with_grids(db, target_unit_id)

    if not target_unit:
        # No target unit found - mark as needing manual assignment
        fragment.analysis_status = AnalysisStatus.NEEDS_DECISION
        fragment.is_ambiguous = True
        fragment.why_needs_decision = "Could not automatically determine which strategic unit this evidence relates to. Please assign manually."
        await db.commit()

        return {
            "status": "needs_assignment",
            "fragment_id": fragment_id,
            "message": "Fragment needs manual unit assignment"
        }

    # Analyze fragment against target unit
    analysis_result = await analyze_fragment(
        domain_name=domain_name,
        core_question=core_question,
        unit_type=target_unit.unit_type.value,
        unit_name=target_unit.name,
        unit_definition=target_unit.definition,
        grids=grids_to_dicts(target_unit.grids),
        source_name=fragment.source.source_name,
        fragment_content=fragment.content
    )

    # Update fragment with analysis results
    try:
        fragment.relationship_type = EvidenceRelationship(analysis_result.get("relationship_type", "new_insight"))
    except ValueError:
        fragment.relationship_type = EvidenceRelationship.NEW_INSIGHT

    fragment.target_unit_id = target_unit_id
    fragment.target_grid_slot = analysis_result.get("target_grid_slot")
    fragment.confidence = analysis_result.get("confidence", 0.5)
    fragment.is_ambiguous = analysis_result.get("is_ambiguous", True)
    fragment.why_needs_decision = analysis_result.get("why_needs_decision")

    confidence = fragment.confidence

    if confidence >= 0.85 and not fragment.is_ambiguous:
        # Auto-integrate
        fragment.analysis_status = AnalysisStatus.INTEGRATED
        # TODO: Actually update the grid slot
        await db.commit()

        return {
            "status": "auto_integrated",
            "fragment_id": fragment_id,
            "target_unit": target_unit.name,
            "target_slot": fragment.target_grid_slot,
            "confidence": confidence,
            "relationship": fragment.relationship_type.value
        }

    elif confidence >= 0.60:
        # Needs confirmation
        fragment.analysis_status = AnalysisStatus.NEEDS_DECISION
        await db.commit()

        return {
            "status": "needs_confirmation",
            "fragment_id": fragment_id,
            "target_unit": target_unit.name,
            "target_slot": fragment.target_grid_slot,
            "confidence": confidence,
            "suggestion": analysis_result.get("integration_suggestion"),
            "message": "Please confirm or reject this integration"
        }

    else:
        # Generate interpretations
        fragment.analysis_status = AnalysisStatus.NEEDS_DECISION

        interp_result = await generate_interpretations(
            domain_name=domain_name,
            core_question=core_question,
            unit_type=target_unit.unit_type.value,
            unit_name=target_unit.name,
            unit_definition=target_unit.definition,
            grids=grids_to_dicts(target_unit.grids),
            source_name=fragment.source.source_name,
            fragment_content=fragment.content,
            why_ambiguous=fragment.why_needs_decision or "Low confidence match"
        )

        # Create interpretation records
        interpretations_created = []
        for i, interp_data in enumerate(interp_result.get("interpretations", [])):
            interpretation = StrategizerEvidenceInterpretation(
                fragment_id=fragment_id,
                interpretation_key=interp_data.get("key", chr(97 + i)),  # a, b, c, d
                title=interp_data.get("title", f"Interpretation {chr(65 + i)}"),
                strategy=interp_data.get("strategy"),
                rationale=interp_data.get("rationale"),
                target_unit_id=target_unit_id,
                target_grid_slot=interp_data.get("target_grid_slot"),
                is_recommended=interp_data.get("is_recommended", False)
            )

            # Try to set relationship type
            try:
                interpretation.relationship_type = EvidenceRelationship(
                    interp_data.get("relationship_type", "new_insight")
                )
            except ValueError:
                interpretation.relationship_type = EvidenceRelationship.NEW_INSIGHT

            db.add(interpretation)
            interpretations_created.append(interpretation)

        await db.commit()

        return {
            "status": "interpretations_generated",
            "fragment_id": fragment_id,
            "target_unit": target_unit.name,
            "interpretations_count": len(interpretations_created),
            "decision_context": interp_result.get("decision_context"),
            "message": "Multiple interpretations available. Use GET /decisions/pending to review."
        }


# =============================================================================
# DECISION HANDLING
# =============================================================================

@router.get("/decisions/pending", response_model=Optional[PendingDecisionResponse])
async def get_pending_decision(
    project_id: str,
    index: int = Query(0, ge=0, description="Index of pending decision (0-based)"),
    db: AsyncSession = Depends(get_db)
):
    """Get a pending decision for review."""
    # Get all pending fragments for this project
    query = (
        select(StrategizerEvidenceFragment)
        .join(StrategizerEvidenceSource)
        .options(
            selectinload(StrategizerEvidenceFragment.source),
            selectinload(StrategizerEvidenceFragment.interpretations)
        )
        .where(
            StrategizerEvidenceSource.project_id == project_id,
            StrategizerEvidenceFragment.analysis_status == AnalysisStatus.NEEDS_DECISION
        )
        .order_by(StrategizerEvidenceFragment.created_at)
    )

    result = await db.execute(query)
    pending = result.scalars().all()

    if not pending:
        return None

    total = len(pending)
    if index >= total:
        index = total - 1

    fragment = pending[index]

    # Build interpretations response
    interpretations = []
    for interp in sorted(fragment.interpretations, key=lambda x: x.interpretation_key or "z"):
        interpretations.append(InterpretationResponse(
            id=interp.id,
            fragment_id=interp.fragment_id,
            interpretation_key=interp.interpretation_key,
            title=interp.title,
            strategy=interp.strategy,
            rationale=interp.rationale,
            relationship_type=interp.relationship_type.value if interp.relationship_type else None,
            target_unit_id=interp.target_unit_id,
            target_grid_slot=interp.target_grid_slot,
            is_recommended=interp.is_recommended,
            commitment_statement=interp.commitment_statement,
            foreclosure_statements=interp.foreclosure_statements
        ))

    return PendingDecisionResponse(
        fragment=EvidenceFragmentResponse(
            id=fragment.id,
            source_id=fragment.source_id,
            content=fragment.content,
            source_location=fragment.source_location,
            analysis_status=fragment.analysis_status.value,
            relationship_type=fragment.relationship_type.value if fragment.relationship_type else None,
            target_unit_id=fragment.target_unit_id,
            target_grid_slot=fragment.target_grid_slot,
            confidence=fragment.confidence,
            is_ambiguous=fragment.is_ambiguous,
            why_needs_decision=fragment.why_needs_decision,
            source_name=fragment.source.source_name if fragment.source else None,
            created_at=fragment.created_at
        ),
        interpretations=interpretations
    )


# =============================================================================
# GRID INTEGRATION HELPERS
# =============================================================================

async def _apply_evidence_to_grid(
    db: AsyncSession,
    unit_id: str,
    grid_slot: str,
    evidence_content: str,
    fragment_id: str
) -> bool:
    """
    Apply evidence content to a grid slot.

    grid_slot format: "GRID_TYPE.slot_name" (e.g., "LOGICAL.evidence")

    Returns True if successfully applied.
    """
    # Parse grid_slot
    if "." in grid_slot:
        grid_type, slot_name = grid_slot.split(".", 1)
    else:
        # If no grid type specified, try to find an existing grid with this slot
        grid_type = None
        slot_name = grid_slot

    # Get the unit's grid instance
    query = select(StrategizerGridInstance).where(
        StrategizerGridInstance.unit_id == unit_id
    )
    if grid_type:
        query = query.where(StrategizerGridInstance.grid_type == grid_type)

    result = await db.execute(query)
    grid_instance = result.scalar_one_or_none()

    if not grid_instance:
        # Create new grid instance if it doesn't exist
        if not grid_type:
            grid_type = "LOGICAL"  # Default to LOGICAL grid

        grid_instance = StrategizerGridInstance(
            unit_id=unit_id,
            grid_type=grid_type,
            slots={
                slot_name: evidence_content
            }
        )
        db.add(grid_instance)
    else:
        # Update existing grid's slot
        slots = grid_instance.slots or {}
        existing_content = slots.get(slot_name, "")

        # Append new evidence, keeping existing content
        if existing_content:
            # Add separator for multiple evidence pieces
            slots[slot_name] = f"{existing_content}\n\n[Evidence #{fragment_id[:8]}]:\n{evidence_content}"
        else:
            slots[slot_name] = evidence_content

        grid_instance.slots = slots

    return True


@router.post("/decisions/{fragment_id}/resolve", response_model=DecisionResponse)
async def resolve_decision(
    project_id: str,
    fragment_id: str,
    decision: DecisionRequest,
    db: AsyncSession = Depends(get_db)
):
    """Resolve a pending decision by accepting an interpretation or rejecting all."""
    # Get fragment
    result = await db.execute(
        select(StrategizerEvidenceFragment)
        .join(StrategizerEvidenceSource)
        .where(
            StrategizerEvidenceFragment.id == fragment_id,
            StrategizerEvidenceSource.project_id == project_id
        )
    )
    fragment = result.scalar_one_or_none()

    if not fragment:
        raise HTTPException(status_code=404, detail="Fragment not found")

    # Create decision record
    evidence_decision = StrategizerEvidenceDecision(
        fragment_id=fragment_id,
        interpretation_id=decision.interpretation_id,
        decision_type=decision.decision_type,
        decision_notes=decision.decision_notes
    )
    db.add(evidence_decision)

    if decision.decision_type == "accept_interpretation" and decision.interpretation_id:
        # Get interpretation
        interp_result = await db.execute(
            select(StrategizerEvidenceInterpretation).where(
                StrategizerEvidenceInterpretation.id == decision.interpretation_id
            )
        )
        interpretation = interp_result.scalar_one_or_none()

        if interpretation:
            # Apply evidence to the target grid slot
            if interpretation.target_unit_id and interpretation.target_grid_slot:
                await _apply_evidence_to_grid(
                    db=db,
                    unit_id=interpretation.target_unit_id,
                    grid_slot=interpretation.target_grid_slot,
                    evidence_content=fragment.content,
                    fragment_id=fragment_id
                )
            fragment.analysis_status = AnalysisStatus.INTEGRATED
            fragment.target_grid_slot = interpretation.target_grid_slot
        else:
            fragment.analysis_status = AnalysisStatus.INTEGRATED

    elif decision.decision_type == "reject_all":
        fragment.analysis_status = AnalysisStatus.REJECTED

    else:
        # manual_override
        fragment.analysis_status = AnalysisStatus.INTEGRATED

    await db.flush()
    await db.refresh(evidence_decision)
    await db.commit()

    return DecisionResponse(
        id=evidence_decision.id,
        fragment_id=fragment_id,
        decision_type=decision.decision_type,
        decision_notes=decision.decision_notes,
        created_at=evidence_decision.created_at
    )


# =============================================================================
# PROGRESS
# =============================================================================

@router.get("/progress", response_model=EvidenceProgressResponse)
async def get_evidence_progress(
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get evidence processing progress for a project."""
    # Verify project exists
    await get_project_with_domain(db, project_id)

    # Count sources
    sources_result = await db.execute(
        select(sql_func.count(StrategizerEvidenceSource.id))
        .where(StrategizerEvidenceSource.project_id == project_id)
    )
    sources_count = sources_result.scalar() or 0

    # Count fragments (via sources)
    fragments_result = await db.execute(
        select(sql_func.count(StrategizerEvidenceFragment.id))
        .join(StrategizerEvidenceSource)
        .where(StrategizerEvidenceSource.project_id == project_id)
    )
    fragments_count = fragments_result.scalar() or 0

    # Count by status
    pending_extraction = await db.execute(
        select(sql_func.count(StrategizerEvidenceSource.id))
        .where(
            StrategizerEvidenceSource.project_id == project_id,
            StrategizerEvidenceSource.extraction_status == ExtractionStatus.PENDING
        )
    )

    pending_analysis = await db.execute(
        select(sql_func.count(StrategizerEvidenceFragment.id))
        .join(StrategizerEvidenceSource)
        .where(
            StrategizerEvidenceSource.project_id == project_id,
            StrategizerEvidenceFragment.analysis_status == AnalysisStatus.PENDING
        )
    )

    pending_decisions = await db.execute(
        select(sql_func.count(StrategizerEvidenceFragment.id))
        .join(StrategizerEvidenceSource)
        .where(
            StrategizerEvidenceSource.project_id == project_id,
            StrategizerEvidenceFragment.analysis_status == AnalysisStatus.NEEDS_DECISION
        )
    )

    integrated = await db.execute(
        select(sql_func.count(StrategizerEvidenceFragment.id))
        .join(StrategizerEvidenceSource)
        .where(
            StrategizerEvidenceSource.project_id == project_id,
            StrategizerEvidenceFragment.analysis_status == AnalysisStatus.INTEGRATED
        )
    )

    return EvidenceProgressResponse(
        sources_count=sources_count,
        fragments_count=fragments_count,
        pending_extraction=pending_extraction.scalar() or 0,
        pending_analysis=pending_analysis.scalar() or 0,
        pending_decisions=pending_decisions.scalar() or 0,
        integrated_count=integrated.scalar() or 0
    )
