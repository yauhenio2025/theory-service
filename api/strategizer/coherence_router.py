"""
Strategizer Coherence API Router

Endpoints for coherence monitoring, predicament detection, and resolution.
"""

from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from ..database import get_db
from .models import (
    StrategizerPredicament,
    StrategizerUnit,
    StrategizerGridInstance,
    StrategizerEvidenceFragment,
    PredicamentType,
    PredicamentSeverity,
    PredicamentStatus,
)
from .schemas import (
    PredicamentCreate,
    PredicamentUpdate,
    PredicamentSummary,
    PredicamentResponse,
    PredicamentWithContext,
    CoherenceCheckRequest,
    CoherenceCheckResponse,
    PredicamentResolveRequest,
    PredicamentResolveResponse,
    GenerateGridRequest,
    UnitResponse,
    GridResponse,
    SlotContent,
    EvidenceFragmentResponse,
)
from .services.coherence_monitor import CoherenceMonitor


router = APIRouter(tags=["strategizer-coherence"])


# =============================================================================
# COHERENCE CHECK ENDPOINTS
# =============================================================================

@router.post(
    "/projects/{project_id}/coherence/quick-scan",
    response_model=CoherenceCheckResponse
)
async def quick_coherence_scan(
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Quick coherence scan using Sonnet.

    Fast detection of obvious tensions, suitable for auto-triggering
    after framework changes.
    """
    monitor = CoherenceMonitor()
    result = await monitor.quick_coherence_scan(db, project_id)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    # Convert predicaments to summary format
    predicament_summaries = []
    for p in result.get("predicaments_found", []):
        predicament_summaries.append(PredicamentSummary(
            id=p.get("id", "pending"),
            title=p.get("title", "Untitled"),
            predicament_type=PredicamentType(p.get("predicament_type", "theoretical")),
            severity=PredicamentSeverity(p.get("severity", "medium")),
            status=PredicamentStatus.DETECTED,
            source_unit_count=len(p.get("source_unit_names", [])),
            has_grid=False,
            detected_at=datetime.utcnow()
        ))

    return CoherenceCheckResponse(
        predicaments_found=predicament_summaries,
        total_found=result.get("total_found", 0),
        new_detected=result.get("new_detected", 0),
        analysis_depth="quick",
        thinking_tokens_used=None
    )


@router.post(
    "/projects/{project_id}/coherence/deep-analysis",
    response_model=CoherenceCheckResponse
)
async def deep_coherence_analysis(
    project_id: str,
    request: CoherenceCheckRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Deep coherence analysis using Opus 4.5 with extended thinking.

    Comprehensive framework review with 10K thinking token budget.
    May take several minutes for complex frameworks.
    """
    monitor = CoherenceMonitor()
    result = await monitor.deep_coherence_analysis(
        db,
        project_id,
        focus_unit_ids=request.focus_unit_ids if request.focus_unit_ids else None
    )

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    # Convert predicaments to summary format
    predicament_summaries = []
    for p in result.get("predicaments_found", []):
        predicament_summaries.append(PredicamentSummary(
            id=p.get("id", "pending"),
            title=p.get("title", "Untitled"),
            predicament_type=PredicamentType(p.get("predicament_type", "theoretical")),
            severity=PredicamentSeverity(p.get("severity", "medium")),
            status=PredicamentStatus.DETECTED,
            source_unit_count=len(p.get("source_unit_names", [])),
            has_grid=False,
            detected_at=datetime.utcnow()
        ))

    return CoherenceCheckResponse(
        predicaments_found=predicament_summaries,
        total_found=result.get("total_found", 0),
        new_detected=result.get("new_detected", 0),
        analysis_depth="deep",
        thinking_tokens_used=result.get("thinking_tokens_used")
    )


# =============================================================================
# PREDICAMENT CRUD ENDPOINTS
# =============================================================================

@router.get(
    "/projects/{project_id}/predicaments",
    response_model=List[PredicamentSummary]
)
async def list_predicaments(
    project_id: str,
    status: Optional[PredicamentStatus] = None,
    predicament_type: Optional[PredicamentType] = None,
    severity: Optional[PredicamentSeverity] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all predicaments for a project with optional filters."""
    query = select(StrategizerPredicament).where(
        StrategizerPredicament.project_id == project_id
    )

    if status:
        query = query.where(StrategizerPredicament.status == status)
    if predicament_type:
        query = query.where(StrategizerPredicament.predicament_type == predicament_type)
    if severity:
        query = query.where(StrategizerPredicament.severity == severity)

    query = query.order_by(StrategizerPredicament.detected_at.desc())

    result = await db.execute(query)
    predicaments = result.scalars().all()

    summaries = []
    for p in predicaments:
        summaries.append(PredicamentSummary(
            id=p.id,
            title=p.title,
            predicament_type=p.predicament_type,
            severity=p.severity,
            status=p.status,
            source_unit_count=len(p.source_unit_ids or []),
            has_grid=p.generated_grid_id is not None,
            detected_at=p.detected_at
        ))

    return summaries


@router.get(
    "/projects/{project_id}/predicaments/{predicament_id}",
    response_model=PredicamentWithContext
)
async def get_predicament(
    project_id: str,
    predicament_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a predicament with full context including source units and evidence."""
    result = await db.execute(
        select(StrategizerPredicament)
        .options(
            selectinload(StrategizerPredicament.generated_grid)
        )
        .where(
            StrategizerPredicament.id == predicament_id,
            StrategizerPredicament.project_id == project_id
        )
    )
    predicament = result.scalar_one_or_none()

    if not predicament:
        raise HTTPException(status_code=404, detail="Predicament not found")

    # Load source units
    source_units = []
    if predicament.source_unit_ids:
        result = await db.execute(
            select(StrategizerUnit)
            .where(StrategizerUnit.id.in_(predicament.source_unit_ids))
        )
        units = result.scalars().all()
        source_units = [
            UnitResponse(
                id=u.id,
                unit_type=u.unit_type,
                display_type=u.display_type,
                tier=u.tier,
                name=u.name,
                definition=u.definition,
                content=u.content or {},
                status=u.status,
                version=u.version,
                created_at=u.created_at,
                updated_at=u.updated_at
            )
            for u in units
        ]

    # Load source evidence
    source_evidence = []
    if predicament.source_evidence_ids:
        result = await db.execute(
            select(StrategizerEvidenceFragment)
            .where(StrategizerEvidenceFragment.id.in_(predicament.source_evidence_ids))
        )
        fragments = result.scalars().all()
        source_evidence = [
            EvidenceFragmentResponse(
                id=f.id,
                source_id=f.source_id,
                content=f.content,
                source_location=f.source_location,
                analysis_status=f.analysis_status.value if hasattr(f.analysis_status, 'value') else str(f.analysis_status),
                relationship_type=f.relationship_type.value if f.relationship_type and hasattr(f.relationship_type, 'value') else None,
                target_unit_id=f.target_unit_id,
                target_grid_slot=f.target_grid_slot,
                confidence=f.confidence,
                is_ambiguous=f.is_ambiguous,
                why_needs_decision=f.why_needs_decision,
                created_at=f.created_at
            )
            for f in fragments
        ]

    # Build grid response
    grid_response = None
    if predicament.generated_grid:
        g = predicament.generated_grid
        grid_response = GridResponse(
            id=g.id,
            unit_id=g.unit_id,
            grid_type=g.grid_type,
            tier=g.tier,
            slots={
                name: SlotContent(
                    content=slot.get("content", ""),
                    confidence=slot.get("confidence", 0.0),
                    evidence_notes=slot.get("evidence_notes")
                )
                for name, slot in (g.slots or {}).items()
            },
            created_at=g.created_at,
            updated_at=g.updated_at
        )

    return PredicamentWithContext(
        predicament=PredicamentResponse(
            id=predicament.id,
            project_id=predicament.project_id,
            title=predicament.title,
            description=predicament.description,
            predicament_type=predicament.predicament_type,
            severity=predicament.severity,
            status=predicament.status,
            pole_a=predicament.pole_a,
            pole_b=predicament.pole_b,
            source_unit_ids=predicament.source_unit_ids or [],
            source_evidence_ids=predicament.source_evidence_ids or [],
            generated_grid_id=predicament.generated_grid_id,
            resolution_notes=predicament.resolution_notes,
            resulting_dialectic_id=predicament.resulting_dialectic_id,
            detected_at=predicament.detected_at,
            resolved_at=predicament.resolved_at,
            created_at=predicament.created_at,
            updated_at=predicament.updated_at
        ),
        source_units=source_units,
        source_evidence=source_evidence,
        generated_grid=grid_response
    )


@router.post(
    "/projects/{project_id}/predicaments",
    response_model=PredicamentResponse
)
async def create_predicament(
    project_id: str,
    predicament: PredicamentCreate,
    db: AsyncSession = Depends(get_db)
):
    """Manually create a predicament."""
    db_predicament = StrategizerPredicament(
        project_id=project_id,
        title=predicament.title,
        description=predicament.description,
        predicament_type=predicament.predicament_type,
        severity=predicament.severity,
        pole_a=predicament.pole_a,
        pole_b=predicament.pole_b,
        source_unit_ids=predicament.source_unit_ids,
        source_evidence_ids=predicament.source_evidence_ids
    )
    db.add(db_predicament)
    await db.commit()
    await db.refresh(db_predicament)

    return PredicamentResponse(
        id=db_predicament.id,
        project_id=db_predicament.project_id,
        title=db_predicament.title,
        description=db_predicament.description,
        predicament_type=db_predicament.predicament_type,
        severity=db_predicament.severity,
        status=db_predicament.status,
        pole_a=db_predicament.pole_a,
        pole_b=db_predicament.pole_b,
        source_unit_ids=db_predicament.source_unit_ids or [],
        source_evidence_ids=db_predicament.source_evidence_ids or [],
        generated_grid_id=db_predicament.generated_grid_id,
        resolution_notes=db_predicament.resolution_notes,
        resulting_dialectic_id=db_predicament.resulting_dialectic_id,
        detected_at=db_predicament.detected_at,
        resolved_at=db_predicament.resolved_at,
        created_at=db_predicament.created_at,
        updated_at=db_predicament.updated_at
    )


@router.patch(
    "/projects/{project_id}/predicaments/{predicament_id}",
    response_model=PredicamentResponse
)
async def update_predicament(
    project_id: str,
    predicament_id: str,
    update: PredicamentUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a predicament."""
    result = await db.execute(
        select(StrategizerPredicament)
        .where(
            StrategizerPredicament.id == predicament_id,
            StrategizerPredicament.project_id == project_id
        )
    )
    predicament = result.scalar_one_or_none()

    if not predicament:
        raise HTTPException(status_code=404, detail="Predicament not found")

    # Apply updates
    if update.title is not None:
        predicament.title = update.title
    if update.description is not None:
        predicament.description = update.description
    if update.severity is not None:
        predicament.severity = update.severity
    if update.status is not None:
        predicament.status = update.status
        if update.status == PredicamentStatus.RESOLVED:
            predicament.resolved_at = datetime.utcnow()
    if update.pole_a is not None:
        predicament.pole_a = update.pole_a
    if update.pole_b is not None:
        predicament.pole_b = update.pole_b
    if update.resolution_notes is not None:
        predicament.resolution_notes = update.resolution_notes

    predicament.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(predicament)

    return PredicamentResponse(
        id=predicament.id,
        project_id=predicament.project_id,
        title=predicament.title,
        description=predicament.description,
        predicament_type=predicament.predicament_type,
        severity=predicament.severity,
        status=predicament.status,
        pole_a=predicament.pole_a,
        pole_b=predicament.pole_b,
        source_unit_ids=predicament.source_unit_ids or [],
        source_evidence_ids=predicament.source_evidence_ids or [],
        generated_grid_id=predicament.generated_grid_id,
        resolution_notes=predicament.resolution_notes,
        resulting_dialectic_id=predicament.resulting_dialectic_id,
        detected_at=predicament.detected_at,
        resolved_at=predicament.resolved_at,
        created_at=predicament.created_at,
        updated_at=predicament.updated_at
    )


# =============================================================================
# PREDICAMENT GRID OPERATIONS
# =============================================================================

@router.post(
    "/projects/{project_id}/predicaments/{predicament_id}/generate-grid"
)
async def generate_predicament_grid(
    project_id: str,
    predicament_id: str,
    request: Optional[GenerateGridRequest] = None,
    db: AsyncSession = Depends(get_db)
):
    """Generate an analytical grid for resolving this predicament.

    Optionally accepts refinement parameters to customize the matrix dimensions:
    - row_refinement: How to adjust rows (more_granular, broader, axis_*, add_row, custom_row)
    - col_refinement: How to adjust columns (more_granular, broader, axis_*, add_col, custom_col)
    - row_custom/col_custom: Custom descriptions when using add_row/col or custom_row/col
    - custom_instruction: Free-form instruction to guide the LLM's analysis
    """
    # Verify predicament exists
    result = await db.execute(
        select(StrategizerPredicament)
        .where(
            StrategizerPredicament.id == predicament_id,
            StrategizerPredicament.project_id == project_id
        )
    )
    predicament = result.scalar_one_or_none()

    if not predicament:
        raise HTTPException(status_code=404, detail="Predicament not found")

    # Extract refinement options if provided
    refinement = None
    if request:
        refinement = {
            "row_refinement": request.row_refinement,
            "row_custom": request.row_custom,
            "col_refinement": request.col_refinement,
            "col_custom": request.col_custom,
            "custom_instruction": request.custom_instruction
        }
        # Only pass refinement if at least one option is set
        if not any(v for v in refinement.values()):
            refinement = None

    monitor = CoherenceMonitor()
    result = await monitor.generate_predicament_grid(db, predicament_id, refinement=refinement)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@router.post(
    "/projects/{project_id}/predicaments/{predicament_id}/fill-slot/{slot_name}"
)
async def fill_predicament_grid_slot(
    project_id: str,
    predicament_id: str,
    slot_name: str,
    db: AsyncSession = Depends(get_db)
):
    """Auto-fill a specific slot in the predicament's analytical grid."""
    monitor = CoherenceMonitor()
    result = await monitor.fill_predicament_grid_slot(db, predicament_id, slot_name)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


# =============================================================================
# CELL ACTIONS
# =============================================================================

from .schemas import CellActionRequest, CellActionResponse

@router.post(
    "/projects/{project_id}/predicaments/{predicament_id}/cell-action",
    response_model=CellActionResponse
)
async def execute_cell_action(
    project_id: str,
    predicament_id: str,
    request: CellActionRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Execute a strategic action on selected matrix cells.

    Available actions:
    - Single cell: what_would_it_take, deep_analysis, generate_arguments,
                   scenario_exploration, surface_assumptions
    - Multi-cell: find_connections, coalition_design, prioritize,
                  synthesize_concept, draft_content
    """
    # Verify predicament exists
    result = await db.execute(
        select(StrategizerPredicament)
        .options(selectinload(StrategizerPredicament.generated_grid))
        .where(
            StrategizerPredicament.id == predicament_id,
            StrategizerPredicament.project_id == project_id
        )
    )
    predicament = result.scalar_one_or_none()

    if not predicament:
        raise HTTPException(status_code=404, detail="Predicament not found")

    monitor = CoherenceMonitor()
    action_result = await monitor.execute_cell_action(
        db=db,
        predicament=predicament,
        action_type=request.action_type.value,
        cells=[c.model_dump() for c in request.cells],
        custom_context=request.custom_context
    )

    if "error" in action_result:
        raise HTTPException(status_code=400, detail=action_result["error"])

    return CellActionResponse(
        action_type=request.action_type.value,
        cells_analyzed=len(request.cells),
        result=action_result.get("result", {}),
        thinking_summary=action_result.get("thinking_summary")
    )


# =============================================================================
# DYNAMIC CELL ACTIONS - Context-specific action generation
# =============================================================================

from .schemas import (
    GenerateCellActionsRequest,
    GenerateCellActionsResponse,
    GeneratedAction,
    ExecuteDynamicActionRequest,
    ExecuteDynamicActionResponse
)

@router.post(
    "/projects/{project_id}/predicaments/{predicament_id}/generate-actions",
    response_model=GenerateCellActionsResponse
)
async def generate_cell_actions(
    project_id: str,
    predicament_id: str,
    request: GenerateCellActionsRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Generate context-specific actions for selected matrix cells.

    Instead of generic actions like "Deep Analysis" or "Scenarios",
    generates actions tailored to:
    - The specific predicament being analyzed
    - The selected cell(s) and their position in the matrix
    - The overall project context
    - What would actually help resolve the tension

    Returns 3-5 actionable, specific analysis options.
    """
    # Verify predicament exists
    result = await db.execute(
        select(StrategizerPredicament)
        .options(selectinload(StrategizerPredicament.generated_grid))
        .where(
            StrategizerPredicament.id == predicament_id,
            StrategizerPredicament.project_id == project_id
        )
    )
    predicament = result.scalar_one_or_none()

    if not predicament:
        raise HTTPException(status_code=404, detail="Predicament not found")

    monitor = CoherenceMonitor()
    action_result = await monitor.generate_cell_actions(
        db=db,
        predicament=predicament,
        cells=[c.model_dump() for c in request.cells]
    )

    if "error" in action_result:
        raise HTTPException(status_code=400, detail=action_result["error"])

    # Convert to GeneratedAction objects
    actions = [
        GeneratedAction(**a) for a in action_result.get("actions", [])
    ]

    return GenerateCellActionsResponse(
        actions=actions,
        cells_count=len(request.cells)
    )


@router.post(
    "/projects/{project_id}/predicaments/{predicament_id}/execute-action",
    response_model=ExecuteDynamicActionResponse
)
async def execute_dynamic_action(
    project_id: str,
    predicament_id: str,
    request: ExecuteDynamicActionRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Execute a dynamically generated action on selected cells.

    Uses Opus 4.5 with extended thinking to produce deep,
    context-specific analysis tailored to the action and predicament.
    """
    # Verify predicament exists
    result = await db.execute(
        select(StrategizerPredicament)
        .options(selectinload(StrategizerPredicament.generated_grid))
        .where(
            StrategizerPredicament.id == predicament_id,
            StrategizerPredicament.project_id == project_id
        )
    )
    predicament = result.scalar_one_or_none()

    if not predicament:
        raise HTTPException(status_code=404, detail="Predicament not found")

    monitor = CoherenceMonitor()
    action_result = await monitor.execute_dynamic_action(
        db=db,
        predicament=predicament,
        cells=[c.model_dump() for c in request.cells],
        action=request.action.model_dump()
    )

    if "error" in action_result:
        raise HTTPException(status_code=400, detail=action_result["error"])

    return ExecuteDynamicActionResponse(
        action_executed=request.action,
        cells_analyzed=len(request.cells),
        result=action_result.get("result", {}),
        thinking_summary=action_result.get("thinking_summary")
    )


# =============================================================================
# PREDICAMENT NOTES - Save insights from cell actions
# =============================================================================

from .schemas import (
    PredicamentNote,
    SaveNoteRequest,
    SaveNoteResponse,
    NotesList,
    SpawnDialecticFromNoteRequest,
    SpawnDialecticFromNoteResponse
)
import uuid


@router.post(
    "/projects/{project_id}/predicaments/{predicament_id}/notes",
    response_model=SaveNoteResponse
)
async def save_note(
    project_id: str,
    predicament_id: str,
    request: SaveNoteRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Save a cell action result as a note on the predicament.

    Notes capture valuable insights from matrix analysis that can be:
    - Referenced later during resolution
    - Transformed into dialectics
    - Used as evidence for framework development
    """
    # Verify predicament exists
    result = await db.execute(
        select(StrategizerPredicament)
        .where(
            StrategizerPredicament.id == predicament_id,
            StrategizerPredicament.project_id == project_id
        )
    )
    predicament = result.scalar_one_or_none()

    if not predicament:
        raise HTTPException(status_code=404, detail="Predicament not found")

    # Create the note
    note = PredicamentNote(
        id=str(uuid.uuid4()),
        title=request.title,
        content=request.content,
        action=request.action,
        cells=request.cells,
        thinking_summary=request.thinking_summary
    )

    # Add to predicament notes (ensure it's a list)
    notes = predicament.notes or []
    # Use mode='json' to serialize datetime to ISO format string
    notes.append(note.model_dump(mode='json'))
    predicament.notes = notes

    await db.commit()

    return SaveNoteResponse(note=note)


@router.get(
    "/projects/{project_id}/predicaments/{predicament_id}/notes",
    response_model=NotesList
)
async def list_notes(
    project_id: str,
    predicament_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    List all notes saved on a predicament.
    """
    result = await db.execute(
        select(StrategizerPredicament)
        .where(
            StrategizerPredicament.id == predicament_id,
            StrategizerPredicament.project_id == project_id
        )
    )
    predicament = result.scalar_one_or_none()

    if not predicament:
        raise HTTPException(status_code=404, detail="Predicament not found")

    notes_data = predicament.notes or []
    notes = [PredicamentNote(**n) for n in notes_data]

    return NotesList(notes=notes, count=len(notes))


@router.delete(
    "/projects/{project_id}/predicaments/{predicament_id}/notes/{note_id}"
)
async def delete_note(
    project_id: str,
    predicament_id: str,
    note_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a note from a predicament.
    """
    result = await db.execute(
        select(StrategizerPredicament)
        .where(
            StrategizerPredicament.id == predicament_id,
            StrategizerPredicament.project_id == project_id
        )
    )
    predicament = result.scalar_one_or_none()

    if not predicament:
        raise HTTPException(status_code=404, detail="Predicament not found")

    notes = predicament.notes or []
    original_count = len(notes)
    notes = [n for n in notes if n.get("id") != note_id]

    if len(notes) == original_count:
        raise HTTPException(status_code=404, detail="Note not found")

    predicament.notes = notes
    await db.commit()

    return {"message": "Note deleted", "note_id": note_id}


@router.post(
    "/projects/{project_id}/predicaments/{predicament_id}/notes/{note_id}/spawn-dialectic",
    response_model=SpawnDialecticFromNoteResponse
)
async def spawn_dialectic_from_note(
    project_id: str,
    predicament_id: str,
    note_id: str,
    request: SpawnDialecticFromNoteRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Transform a saved note into a new dialectic unit using LLM analysis.

    When auto_generate is True (default), the LLM analyzes the note content
    to generate a well-structured dialectic with clear poles and definition.
    User-provided values override the generated ones.
    """
    from .models import StrategizerUnit, UnitType, UnitTier, UnitStatus
    from .services.coherence_monitor import CoherenceMonitor

    # Verify predicament and find note
    result = await db.execute(
        select(StrategizerPredicament)
        .where(
            StrategizerPredicament.id == predicament_id,
            StrategizerPredicament.project_id == project_id
        )
    )
    predicament = result.scalar_one_or_none()

    if not predicament:
        raise HTTPException(status_code=404, detail="Predicament not found")

    notes = predicament.notes or []
    note_data = next((n for n in notes if n.get("id") == note_id), None)

    if not note_data:
        raise HTTPException(status_code=404, detail="Note not found")

    note = PredicamentNote(**note_data)

    # Determine if we need LLM generation
    llm_generated = False
    generation_confidence = None
    generated = None

    # Use LLM generation if auto_generate is True and any field is empty
    if request.auto_generate and (
        not request.dialectic_name or
        not request.definition or
        not request.pole_a or
        not request.pole_b
    ):
        try:
            monitor = CoherenceMonitor()
            generated = await monitor.generate_dialectic_from_note(
                predicament=predicament,
                note_data=note_data
            )
            llm_generated = True
            generation_confidence = generated.get("confidence", 0.5)
        except Exception as e:
            # If LLM fails, fall back to simple extraction
            import logging
            logging.getLogger(__name__).warning(f"LLM generation failed: {e}")
            generated = None

    # Build final values: user input > LLM generated > fallback
    if generated:
        # Use generated pole structures
        pole_a_gen = generated.get("pole_a", {})
        pole_b_gen = generated.get("pole_b", {})

        dialectic_name = request.dialectic_name or generated.get("dialectic_name") or f"Dialectic from: {note.title}"
        definition = request.definition or generated.get("definition") or predicament.description

        # For poles, use the name from generated structure if available
        pole_a = request.pole_a or pole_a_gen.get("name") or predicament.pole_a or "Pole A"
        pole_b = request.pole_b or pole_b_gen.get("name") or predicament.pole_b or "Pole B"

        # Rich content from LLM
        dialectic_content = {
            "thesis": pole_a,
            "thesis_description": pole_a_gen.get("description", ""),
            "antithesis": pole_b,
            "antithesis_description": pole_b_gen.get("description", ""),
            "synthesis_notes": generated.get("synthesis_notes", ""),
            "navigation_strategies": generated.get("navigation_strategies", []),
            "why_this_dialectic": generated.get("why_this_dialectic", ""),
            "spawned_from_note": note_id,
            "spawned_from_predicament": predicament_id,
            "source_analysis": {
                "action": note.action.model_dump() if hasattr(note.action, 'model_dump') else note.action,
                "cells": [c.model_dump() if hasattr(c, 'model_dump') else c for c in note.cells],
                "thinking_summary": note.thinking_summary
            },
            "llm_generated": True,
            "generation_confidence": generation_confidence
        }
    else:
        # Fallback to simple extraction (no LLM)
        dialectic_name = request.dialectic_name or f"Dialectic from: {note.title}"

        # Try to extract definition from note content
        definition = request.definition
        if not definition:
            content = note.content
            if isinstance(content, dict):
                definition = (
                    content.get("summary") or
                    content.get("overview") or
                    content.get("key_insight") or
                    content.get("main_finding") or
                    f"Dialectic spawned from analysis: {note.title}"
                )
            else:
                definition = f"Dialectic spawned from analysis: {note.title}"

        pole_a = request.pole_a or predicament.pole_a or "Pole A"
        pole_b = request.pole_b or predicament.pole_b or "Pole B"

        dialectic_content = {
            "thesis": pole_a,
            "antithesis": pole_b,
            "synthesis": None,
            "spawned_from_note": note_id,
            "spawned_from_predicament": predicament_id,
            "source_analysis": {
                "action": note.action.model_dump() if hasattr(note.action, 'model_dump') else note.action,
                "cells": [c.model_dump() if hasattr(c, 'model_dump') else c for c in note.cells],
                "thinking_summary": note.thinking_summary
            }
        }

    # Create the dialectic unit
    dialectic = StrategizerUnit(
        id=str(uuid.uuid4()),
        project_id=project_id,
        unit_type=UnitType.DIALECTIC,
        display_type="Dialectic",
        tier=UnitTier.EMERGENT,
        name=dialectic_name,
        definition=definition,
        content=dialectic_content,
        status=UnitStatus.DRAFT
    )

    db.add(dialectic)
    await db.commit()
    await db.refresh(dialectic)

    # Build response
    from .schemas import UnitResponse
    dialectic_response = UnitResponse(
        id=dialectic.id,
        project_id=dialectic.project_id,
        unit_type=dialectic.unit_type.value,
        display_type=dialectic.display_type,
        tier=dialectic.tier.value,
        name=dialectic.name,
        definition=dialectic.definition,
        content=dialectic.content,
        status=dialectic.status.value,
        version=dialectic.version,
        created_at=dialectic.created_at,
        updated_at=dialectic.updated_at
    )

    message = f"Dialectic '{dialectic_name}' created from note"
    if llm_generated:
        message += f" (LLM-generated, confidence: {generation_confidence:.0%})"

    return SpawnDialecticFromNoteResponse(
        dialectic=dialectic_response,
        note_id=note_id,
        message=message,
        llm_generated=llm_generated,
        generation_confidence=generation_confidence
    )


# =============================================================================
# PREDICAMENT RESOLUTION
# =============================================================================

@router.post(
    "/projects/{project_id}/predicaments/{predicament_id}/resolve",
    response_model=PredicamentResolveResponse
)
async def resolve_predicament(
    project_id: str,
    predicament_id: str,
    request: PredicamentResolveRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Resolve a predicament by transforming it into a dialectic.

    The predicament becomes a permanent part of the framework as a navigable
    tension rather than an unresolved problem.
    """
    # Verify predicament exists
    result = await db.execute(
        select(StrategizerPredicament)
        .where(
            StrategizerPredicament.id == predicament_id,
            StrategizerPredicament.project_id == project_id
        )
    )
    predicament = result.scalar_one_or_none()

    if not predicament:
        raise HTTPException(status_code=404, detail="Predicament not found")

    if predicament.status == PredicamentStatus.RESOLVED:
        raise HTTPException(status_code=400, detail="Predicament already resolved")

    monitor = CoherenceMonitor()
    result = await monitor.resolve_to_dialectic(
        db,
        predicament_id,
        request.resolution_approach,
        request.dialectic_name,
        request.resolution_notes
    )

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    # Build dialectic response
    dialectic_result = await db.execute(
        select(StrategizerUnit)
        .where(StrategizerUnit.id == result["dialectic_id"])
    )
    dialectic = dialectic_result.scalar_one()

    return PredicamentResolveResponse(
        predicament_id=predicament_id,
        resulting_dialectic=UnitResponse(
            id=dialectic.id,
            unit_type=dialectic.unit_type,
            display_type=dialectic.display_type,
            tier=dialectic.tier,
            name=dialectic.name,
            definition=dialectic.definition,
            content=dialectic.content or {},
            status=dialectic.status,
            version=dialectic.version,
            created_at=dialectic.created_at,
            updated_at=dialectic.updated_at
        ),
        message=f"Predicament resolved and transformed into dialectic: {dialectic.name}"
    )


@router.post(
    "/projects/{project_id}/predicaments/{predicament_id}/defer"
)
async def defer_predicament(
    project_id: str,
    predicament_id: str,
    notes: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Defer a predicament - acknowledge it but don't resolve now.

    Useful for predicaments that are recognized but not yet ready to address.
    """
    result = await db.execute(
        select(StrategizerPredicament)
        .where(
            StrategizerPredicament.id == predicament_id,
            StrategizerPredicament.project_id == project_id
        )
    )
    predicament = result.scalar_one_or_none()

    if not predicament:
        raise HTTPException(status_code=404, detail="Predicament not found")

    predicament.status = PredicamentStatus.DEFERRED
    predicament.resolution_notes = notes or "Deferred for later consideration"
    predicament.updated_at = datetime.utcnow()

    await db.commit()

    return {
        "predicament_id": predicament_id,
        "status": "deferred",
        "notes": predicament.resolution_notes
    }


# =============================================================================
# COHERENCE STATS
# =============================================================================

@router.get("/projects/{project_id}/coherence/stats")
async def get_coherence_stats(
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get coherence statistics for a project."""
    # Count predicaments by status
    status_counts = {}
    for status in PredicamentStatus:
        result = await db.execute(
            select(func.count(StrategizerPredicament.id))
            .where(
                StrategizerPredicament.project_id == project_id,
                StrategizerPredicament.status == status
            )
        )
        status_counts[status.value] = result.scalar() or 0

    # Count by type
    type_counts = {}
    for pred_type in PredicamentType:
        result = await db.execute(
            select(func.count(StrategizerPredicament.id))
            .where(
                StrategizerPredicament.project_id == project_id,
                StrategizerPredicament.predicament_type == pred_type
            )
        )
        type_counts[pred_type.value] = result.scalar() or 0

    # Count by severity (for active predicaments)
    severity_counts = {}
    for severity in PredicamentSeverity:
        result = await db.execute(
            select(func.count(StrategizerPredicament.id))
            .where(
                StrategizerPredicament.project_id == project_id,
                StrategizerPredicament.severity == severity,
                StrategizerPredicament.status.in_([
                    PredicamentStatus.DETECTED,
                    PredicamentStatus.ANALYZING
                ])
            )
        )
        severity_counts[severity.value] = result.scalar() or 0

    total = sum(status_counts.values())
    active = status_counts.get("detected", 0) + status_counts.get("analyzing", 0)

    return {
        "total_predicaments": total,
        "active_predicaments": active,
        "by_status": status_counts,
        "by_type": type_counts,
        "by_severity": severity_counts,
        "health_indicator": "healthy" if active == 0 else (
            "attention" if severity_counts.get("critical", 0) == 0 else "critical"
        )
    }
