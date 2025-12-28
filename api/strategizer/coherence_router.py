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
    """Generate an analytical grid for resolving this predicament."""
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

    monitor = CoherenceMonitor()
    result = await monitor.generate_predicament_grid(db, predicament_id)

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
