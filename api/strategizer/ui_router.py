"""
Strategizer Web UI Router

FastAPI routes for the web interface using Jinja2 templates.
"""

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from ..database import get_db
from .models import (
    StrategizerProject, StrategizerDomain, StrategizerUnit,
    StrategizerGridInstance, StrategizerEvidenceSource,
    StrategizerEvidenceFragment, AnalysisStatus,
    StrategizerPredicament, PredicamentStatus, PredicamentSeverity, PredicamentType
)

# Set up templates directory
TEMPLATE_DIR = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

router = APIRouter(tags=["strategizer-ui"])


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

async def get_project_context(project_id: str, db: AsyncSession):
    """Load project with all related data for templates."""
    result = await db.execute(
        select(StrategizerProject)
        .options(
            selectinload(StrategizerProject.domain),
            selectinload(StrategizerProject.units)
        )
        .where(StrategizerProject.id == project_id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Get evidence stats
    pending_decisions_result = await db.execute(
        select(func.count(StrategizerEvidenceFragment.id))
        .join(StrategizerEvidenceSource)
        .where(
            StrategizerEvidenceSource.project_id == project_id,
            StrategizerEvidenceFragment.analysis_status == AnalysisStatus.NEEDS_DECISION
        )
    )
    pending_decisions = pending_decisions_result.scalar() or 0

    return project, pending_decisions


async def get_coherence_stats(project_id: str, db: AsyncSession) -> dict:
    """Get coherence statistics for a project."""
    # Count active predicaments (not resolved or deferred)
    active_result = await db.execute(
        select(func.count(StrategizerPredicament.id))
        .where(
            StrategizerPredicament.project_id == project_id,
            StrategizerPredicament.status.in_([PredicamentStatus.DETECTED, PredicamentStatus.ANALYZING])
        )
    )
    active_predicaments = active_result.scalar() or 0

    # Count by severity (only active)
    severity_counts = {}
    for severity in [PredicamentSeverity.CRITICAL, PredicamentSeverity.HIGH, PredicamentSeverity.MEDIUM, PredicamentSeverity.LOW]:
        count_result = await db.execute(
            select(func.count(StrategizerPredicament.id))
            .where(
                StrategizerPredicament.project_id == project_id,
                StrategizerPredicament.status.in_([PredicamentStatus.DETECTED, PredicamentStatus.ANALYZING]),
                StrategizerPredicament.severity == severity
            )
        )
        severity_counts[severity.value] = count_result.scalar() or 0

    return {
        "active_predicaments": active_predicaments,
        "critical_count": severity_counts.get("critical", 0),
        "high_count": severity_counts.get("high", 0),
        "medium_count": severity_counts.get("medium", 0),
        "low_count": severity_counts.get("low", 0)
    }


# =============================================================================
# PROJECT LIST
# =============================================================================

@router.get("/ui/", response_class=HTMLResponse)
async def projects_page(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Project list page."""
    result = await db.execute(
        select(StrategizerProject)
        .options(selectinload(StrategizerProject.domain))
        .order_by(StrategizerProject.updated_at.desc())
    )
    projects = result.scalars().all()

    # Enrich with unit counts
    projects_data = []
    for project in projects:
        unit_count_result = await db.execute(
            select(func.count(StrategizerUnit.id))
            .where(StrategizerUnit.project_id == project.id)
        )
        unit_count = unit_count_result.scalar() or 0

        projects_data.append({
            "id": str(project.id),
            "name": project.name,
            "brief": project.brief[:150] + "..." if len(project.brief) > 150 else project.brief,
            "domain_name": project.domain.name if project.domain else None,
            "unit_count": unit_count,
            "created_at": project.created_at,
            "updated_at": project.updated_at
        })

    return templates.TemplateResponse("projects.html", {
        "request": request,
        "projects": projects_data,
        "active_page": "projects"
    })


# =============================================================================
# PROJECT DETAIL / WORKSPACE
# =============================================================================

@router.get("/ui/projects/{project_id}", response_class=HTMLResponse)
async def project_detail_page(
    request: Request,
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Main project workspace page."""
    project, pending_decisions = await get_project_context(project_id, db)

    # Group units by type
    units_by_type = {
        "concept": [],
        "dialectic": [],
        "actor": []
    }

    for unit in project.units:
        unit_type = unit.unit_type.value
        if unit_type in units_by_type:
            units_by_type[unit_type].append({
                "id": str(unit.id),
                "name": unit.name,
                "definition": unit.definition[:100] + "..." if len(unit.definition) > 100 else unit.definition,
                "status": unit.status.value,
                "tier": unit.tier
            })

    # Get source count
    source_count_result = await db.execute(
        select(func.count(StrategizerEvidenceSource.id))
        .where(StrategizerEvidenceSource.project_id == project_id)
    )
    source_count = source_count_result.scalar() or 0

    # Get coherence stats
    coherence_stats = await get_coherence_stats(project_id, db)

    return templates.TemplateResponse("project_detail.html", {
        "request": request,
        "project": {
            "id": str(project.id),
            "name": project.name,
            "brief": project.brief,
            "domain": {
                "name": project.domain.name,
                "core_question": project.domain.core_question,
                "vocabulary": project.domain.vocabulary
            } if project.domain else None
        },
        "units_by_type": units_by_type,
        "source_count": source_count,
        "pending_decisions": pending_decisions,
        "coherence_stats": coherence_stats,
        "active_page": "project"
    })


# =============================================================================
# UNIT DETAIL / GRIDS
# =============================================================================

@router.get("/ui/projects/{project_id}/units/{unit_id}", response_class=HTMLResponse)
async def unit_detail_page(
    request: Request,
    project_id: str,
    unit_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Unit detail page with grid editing."""
    project, pending_decisions = await get_project_context(project_id, db)

    # Get unit with grids
    unit_result = await db.execute(
        select(StrategizerUnit)
        .options(selectinload(StrategizerUnit.grids))
        .where(
            StrategizerUnit.id == unit_id,
            StrategizerUnit.project_id == project_id
        )
    )
    unit = unit_result.scalar_one_or_none()

    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    # Import grid definitions
    from .grids import get_grid_definition, get_applicable_grids

    # Build grid data
    grids_data = []
    for grid in unit.grids:
        grid_def = get_grid_definition(grid.grid_type)
        slots_data = []

        if grid_def:
            for slot_def in grid_def["slots"]:
                slot_name = slot_def["name"]
                slot_data = (grid.slots or {}).get(slot_name, {})
                slots_data.append({
                    "name": slot_name,
                    "description": slot_def.get("description", ""),
                    "content": slot_data.get("content", ""),
                    "confidence": slot_data.get("confidence", 0),
                    "evidence_notes": slot_data.get("evidence_notes")
                })

        grids_data.append({
            "id": str(grid.id),
            "grid_type": grid.grid_type,
            "name": grid_def["name"] if grid_def else grid.grid_type,
            "description": grid_def["description"] if grid_def else "",
            "tier": grid.tier.value,
            "slots": slots_data,
            "created_at": grid.created_at
        })

    # Get applicable grids not yet added
    applicable = get_applicable_grids(unit.unit_type.value)
    existing_types = {g.grid_type for g in unit.grids}
    available_grids = []

    for grid_info in applicable["required"] + applicable["flexible"]:
        if grid_info["grid_type"] not in existing_types:
            available_grids.append({
                "grid_type": grid_info["grid_type"],
                "name": grid_info["name"],
                "description": grid_info["description"],
                "tier": "required" if grid_info in applicable["required"] else "flexible"
            })

    return templates.TemplateResponse("unit_detail.html", {
        "request": request,
        "project": {
            "id": str(project.id),
            "name": project.name
        },
        "unit": {
            "id": str(unit.id),
            "name": unit.name,
            "definition": unit.definition,
            "unit_type": unit.unit_type.value,
            "display_type": unit.display_type,
            "status": unit.status.value,
            "content": unit.content or {}
        },
        "grids": grids_data,
        "available_grids": available_grids,
        "pending_decisions": pending_decisions,
        "active_page": "unit"
    })


# =============================================================================
# EVIDENCE MANAGEMENT
# =============================================================================

@router.get("/ui/projects/{project_id}/evidence", response_class=HTMLResponse)
async def evidence_page(
    request: Request,
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Evidence sources and fragments page."""
    project, pending_decisions = await get_project_context(project_id, db)

    # Get sources with fragment counts
    sources_result = await db.execute(
        select(StrategizerEvidenceSource)
        .where(StrategizerEvidenceSource.project_id == project_id)
        .order_by(StrategizerEvidenceSource.created_at.desc())
    )
    sources = sources_result.scalars().all()

    sources_data = []
    for source in sources:
        # Count fragments by status
        fragment_counts_result = await db.execute(
            select(
                StrategizerEvidenceFragment.analysis_status,
                func.count(StrategizerEvidenceFragment.id)
            )
            .where(StrategizerEvidenceFragment.source_id == source.id)
            .group_by(StrategizerEvidenceFragment.analysis_status)
        )
        counts = {row[0].value: row[1] for row in fragment_counts_result.fetchall()}

        sources_data.append({
            "id": str(source.id),
            "source_type": source.source_type,
            "source_name": source.source_name,
            "extraction_status": source.extraction_status,
            "extracted_count": source.extracted_count or 0,
            "created_at": source.created_at,
            "fragment_counts": counts
        })

    # Get recent fragments
    fragments_result = await db.execute(
        select(StrategizerEvidenceFragment)
        .join(StrategizerEvidenceSource)
        .where(StrategizerEvidenceSource.project_id == project_id)
        .order_by(StrategizerEvidenceFragment.created_at.desc())
        .limit(20)
    )
    fragments = fragments_result.scalars().all()

    fragments_data = [
        {
            "id": str(f.id),
            "content": f.content[:200] + "..." if len(f.content) > 200 else f.content,
            "status": f.analysis_status.value,
            "relationship_type": f.relationship_type.value if f.relationship_type else None,
            "confidence": f.confidence,
            "created_at": f.created_at
        }
        for f in fragments
    ]

    return templates.TemplateResponse("evidence.html", {
        "request": request,
        "project": {
            "id": str(project.id),
            "name": project.name
        },
        "sources": sources_data,
        "fragments": fragments_data,
        "pending_decisions": pending_decisions,
        "active_page": "evidence"
    })


# =============================================================================
# PENDING DECISIONS
# =============================================================================

@router.get("/ui/projects/{project_id}/decisions", response_class=HTMLResponse)
async def decisions_page(
    request: Request,
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Pending decisions page."""
    project, pending_decisions = await get_project_context(project_id, db)

    # Get fragments needing decisions with interpretations
    from .models import StrategizerEvidenceInterpretation

    fragments_result = await db.execute(
        select(StrategizerEvidenceFragment)
        .join(StrategizerEvidenceSource)
        .options(selectinload(StrategizerEvidenceFragment.interpretations))
        .where(
            StrategizerEvidenceSource.project_id == project_id,
            StrategizerEvidenceFragment.analysis_status == AnalysisStatus.NEEDS_DECISION
        )
        .order_by(StrategizerEvidenceFragment.created_at.desc())
    )
    fragments = fragments_result.scalars().all()

    decisions_data = []
    for fragment in fragments:
        interpretations = [
            {
                "id": str(interp.id),
                "interpretation_key": interp.interpretation_key,
                "title": interp.title,
                "strategy": interp.strategy,
                "target_unit_id": str(interp.target_unit_id) if interp.target_unit_id else None,
                "target_grid_slot": interp.target_grid_slot,
                "is_recommended": interp.is_recommended,
                "commitment_statement": interp.commitment_statement,
                "foreclosure_statements": interp.foreclosure_statements or []
            }
            for interp in fragment.interpretations
        ]

        decisions_data.append({
            "fragment_id": str(fragment.id),
            "content": fragment.content,
            "why_needs_decision": fragment.why_needs_decision,
            "interpretations": interpretations
        })

    return templates.TemplateResponse("decisions.html", {
        "request": request,
        "project": {
            "id": str(project.id),
            "name": project.name
        },
        "decisions": decisions_data,
        "pending_count": len(decisions_data),
        "active_page": "decisions"
    })


# =============================================================================
# COHERENCE MONITORING
# =============================================================================

@router.get("/ui/projects/{project_id}/coherence", response_class=HTMLResponse)
async def coherence_page(
    request: Request,
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Coherence monitoring page with predicaments list."""
    project, pending_decisions = await get_project_context(project_id, db)

    # Get active predicaments
    active_result = await db.execute(
        select(StrategizerPredicament)
        .where(
            StrategizerPredicament.project_id == project_id,
            StrategizerPredicament.status.in_([PredicamentStatus.DETECTED, PredicamentStatus.ANALYZING])
        )
        .order_by(StrategizerPredicament.severity.desc(), StrategizerPredicament.detected_at.desc())
    )
    active_predicaments = active_result.scalars().all()

    # Get resolved predicaments
    resolved_result = await db.execute(
        select(StrategizerPredicament)
        .where(
            StrategizerPredicament.project_id == project_id,
            StrategizerPredicament.status == PredicamentStatus.RESOLVED
        )
        .order_by(StrategizerPredicament.resolved_at.desc())
        .limit(10)
    )
    resolved_predicaments = resolved_result.scalars().all()

    # Build predicaments data
    predicaments_data = []
    for pred in active_predicaments:
        predicaments_data.append({
            "id": str(pred.id),
            "title": pred.title,
            "description": pred.description,
            "predicament_type": pred.predicament_type.value,
            "severity": pred.severity.value,
            "status": pred.status.value,
            "pole_a": pred.pole_a,
            "pole_b": pred.pole_b,
            "detected_at": pred.detected_at,
            "has_grid": pred.generated_grid_id is not None,
            "source_unit_count": len(pred.source_unit_ids or [])
        })

    resolved_data = []
    for pred in resolved_predicaments:
        resolved_data.append({
            "id": str(pred.id),
            "title": pred.title,
            "description": pred.description,
            "predicament_type": pred.predicament_type.value,
            "resolution_notes": pred.resolution_notes,
            "resolved_at": pred.resolved_at,
            "resulting_dialectic_id": str(pred.resulting_dialectic_id) if pred.resulting_dialectic_id else None
        })

    # Get full stats
    stats = {
        "active": len(active_predicaments),
        "resolved": len(resolved_predicaments),
        "critical": sum(1 for p in active_predicaments if p.severity == PredicamentSeverity.CRITICAL),
        "high": sum(1 for p in active_predicaments if p.severity == PredicamentSeverity.HIGH),
        "medium": sum(1 for p in active_predicaments if p.severity == PredicamentSeverity.MEDIUM),
        "low": sum(1 for p in active_predicaments if p.severity == PredicamentSeverity.LOW),
        "theoretical": sum(1 for p in active_predicaments if p.predicament_type == PredicamentType.THEORETICAL),
        "empirical": sum(1 for p in active_predicaments if p.predicament_type == PredicamentType.EMPIRICAL),
        "conceptual": sum(1 for p in active_predicaments if p.predicament_type == PredicamentType.CONCEPTUAL),
        "praxis": sum(1 for p in active_predicaments if p.predicament_type == PredicamentType.PRAXIS),
    }

    return templates.TemplateResponse("coherence.html", {
        "request": request,
        "project": {
            "id": str(project.id),
            "name": project.name
        },
        "predicaments": predicaments_data,
        "resolved_predicaments": resolved_data,
        "stats": stats,
        "active_page": "coherence"
    })


@router.get("/ui/projects/{project_id}/predicaments/{predicament_id}", response_class=HTMLResponse)
async def predicament_detail_page(
    request: Request,
    project_id: str,
    predicament_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Predicament detail page with analytical grid."""
    project, pending_decisions = await get_project_context(project_id, db)

    # Get predicament with grid
    pred_result = await db.execute(
        select(StrategizerPredicament)
        .where(
            StrategizerPredicament.id == predicament_id,
            StrategizerPredicament.project_id == project_id
        )
    )
    predicament = pred_result.scalar_one_or_none()

    if not predicament:
        raise HTTPException(status_code=404, detail="Predicament not found")

    # Get generated grid if exists
    grid_data = None
    if predicament.generated_grid_id:
        grid_result = await db.execute(
            select(StrategizerGridInstance)
            .where(StrategizerGridInstance.id == predicament.generated_grid_id)
        )
        grid = grid_result.scalar_one_or_none()
        if grid:
            from .grids import get_grid_definition
            grid_def = get_grid_definition(grid.grid_type)

            slots_data = []
            if grid_def:
                for slot_def in grid_def["slots"]:
                    slot_name = slot_def["name"]
                    slot_content = (grid.slots or {}).get(slot_name, {})
                    slots_data.append({
                        "name": slot_name,
                        "description": slot_def.get("description", ""),
                        "content": slot_content.get("content", ""),
                        "confidence": slot_content.get("confidence", 0)
                    })

            grid_data = {
                "id": str(grid.id),
                "grid_type": grid.grid_type,
                "name": grid_def["name"] if grid_def else grid.grid_type,
                "description": grid_def["description"] if grid_def else "",
                "slots": slots_data,
                "analysis_sequence": grid_def.get("analysis_sequence") if grid_def else None,
                "resolution_criteria": grid_def.get("resolution_criteria") if grid_def else None
            }

    # Get source units
    source_units = []
    if predicament.source_unit_ids:
        units_result = await db.execute(
            select(StrategizerUnit)
            .where(StrategizerUnit.id.in_(predicament.source_unit_ids))
        )
        for unit in units_result.scalars().all():
            source_units.append({
                "id": str(unit.id),
                "name": unit.name,
                "unit_type": unit.unit_type.value
            })

    # Get source evidence
    source_evidence = []
    if predicament.source_evidence_ids:
        ev_result = await db.execute(
            select(StrategizerEvidenceFragment)
            .options(selectinload(StrategizerEvidenceFragment.source))
            .where(StrategizerEvidenceFragment.id.in_(predicament.source_evidence_ids))
        )
        for ev in ev_result.scalars().all():
            source_evidence.append({
                "id": str(ev.id),
                "content": ev.content,
                "source_name": ev.source.source_name if ev.source else "Unknown"
            })

    # Get resulting dialectic if resolved
    resulting_dialectic = None
    if predicament.resulting_dialectic_id:
        dialectic_result = await db.execute(
            select(StrategizerUnit)
            .where(StrategizerUnit.id == predicament.resulting_dialectic_id)
        )
        dialectic = dialectic_result.scalar_one_or_none()
        if dialectic:
            resulting_dialectic = {
                "id": str(dialectic.id),
                "name": dialectic.name
            }

    return templates.TemplateResponse("predicament_detail.html", {
        "request": request,
        "project": {
            "id": str(project.id),
            "name": project.name
        },
        "predicament": {
            "id": str(predicament.id),
            "title": predicament.title,
            "description": predicament.description,
            "predicament_type": predicament.predicament_type.value,
            "severity": predicament.severity.value,
            "status": predicament.status.value,
            "pole_a": predicament.pole_a,
            "pole_b": predicament.pole_b,
            "detected_at": predicament.detected_at,
            "resolved_at": predicament.resolved_at,
            "resolution_notes": predicament.resolution_notes
        },
        "grid": grid_data,
        "source_units": source_units,
        "source_evidence": source_evidence,
        "resulting_dialectic": resulting_dialectic,
        "active_page": "coherence"
    })
