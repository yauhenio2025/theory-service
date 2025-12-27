"""
Strategizer API Router

Main router for the Strategizer system.
Includes project management, domain bootstrapping, units, and dialogue.
"""

from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.attributes import flag_modified

from ..database import get_db
from .models import (
    StrategizerProject, StrategizerDomain, StrategizerSeedContent,
    StrategizerUnit, StrategizerGridInstance, StrategizerDialogueTurn,
    UnitType, UnitStatus, DialogueTurnType
)
from .schemas import (
    ProjectCreate, ProjectUpdate, ProjectSummary, ProjectResponse,
    DomainBootstrapRequest, DomainBootstrapResponse, DomainResponse,
    SeedAcceptReject, SeedContentResponse,
    UnitCreate, UnitUpdate, UnitResponse, UnitRefineRequest,
    DialogueAskRequest, DialogueResponse, DialogueTurnResponse, DialogueHistoryResponse,
    SuggestRequest, SuggestionResponse, SuggestedAction, VocabularyMapping,
    # Grid schemas
    GridCreate, GridSlotUpdate, GridResponse, GridTier,
    GridAutoApplyRequest, GridAutoApplyResponse,
    FrictionEvent, FrictionDetectionResponse,
    ApplicableGridsResponse, GridDefinitionResponse, SlotDefinition, SlotContent
)
from .services.llm import StrategizerLLM
from .grids import get_grid_definition, get_applicable_grids, TIER_1_GRIDS, TIER_2_GRIDS

router = APIRouter(prefix="/api/strategizer", tags=["strategizer"])


# =============================================================================
# HEALTH CHECK
# =============================================================================

@router.get("/health")
async def strategizer_health():
    """Health check for Strategizer module."""
    return {"status": "healthy", "module": "strategizer"}


# =============================================================================
# PROJECTS
# =============================================================================

@router.post("/projects", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new strategic project."""
    db_project = StrategizerProject(
        name=project.name,
        brief=project.brief
    )
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)

    return ProjectResponse(
        id=db_project.id,
        name=db_project.name,
        brief=db_project.brief,
        created_at=db_project.created_at,
        updated_at=db_project.updated_at,
        domain=None,
        units=[]
    )


@router.get("/projects", response_model=List[ProjectSummary])
async def list_projects(
    db: AsyncSession = Depends(get_db)
):
    """List all projects."""
    # Query projects with domain and unit count
    result = await db.execute(
        select(StrategizerProject)
        .options(selectinload(StrategizerProject.domain))
        .order_by(StrategizerProject.updated_at.desc())
    )
    projects = result.scalars().all()

    summaries = []
    for project in projects:
        # Count units
        unit_count_result = await db.execute(
            select(func.count(StrategizerUnit.id))
            .where(StrategizerUnit.project_id == project.id)
        )
        unit_count = unit_count_result.scalar() or 0

        summaries.append(ProjectSummary(
            id=project.id,
            name=project.name,
            brief=project.brief[:200] + "..." if len(project.brief) > 200 else project.brief,
            domain_name=project.domain.name if project.domain else None,
            unit_count=unit_count,
            created_at=project.created_at,
            updated_at=project.updated_at
        ))

    return summaries


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a project with its domain and units."""
    result = await db.execute(
        select(StrategizerProject)
        .options(
            selectinload(StrategizerProject.domain).selectinload(StrategizerDomain.seed_content),
            selectinload(StrategizerProject.units)
        )
        .where(StrategizerProject.id == project_id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Build domain response
    domain_response = None
    if project.domain:
        domain_response = DomainResponse(
            id=project.domain.id,
            name=project.domain.name,
            core_question=project.domain.core_question,
            success_looks_like=project.domain.success_looks_like,
            vocabulary=VocabularyMapping(**(project.domain.vocabulary or {})),
            template_base=project.domain.template_base,
            seed_content=[
                SeedContentResponse(
                    id=seed.id,
                    content_type=seed.content_type,
                    content=seed.content,
                    accepted=seed.accepted
                )
                for seed in project.domain.seed_content
            ],
            created_at=project.domain.created_at
        )

    # Build unit responses
    unit_responses = [
        UnitResponse(
            id=unit.id,
            unit_type=unit.unit_type,
            display_type=unit.display_type,
            tier=unit.tier,
            name=unit.name,
            definition=unit.definition,
            content=unit.content or {},
            status=unit.status,
            version=unit.version,
            created_at=unit.created_at,
            updated_at=unit.updated_at
        )
        for unit in project.units
    ]

    return ProjectResponse(
        id=project.id,
        name=project.name,
        brief=project.brief,
        created_at=project.created_at,
        updated_at=project.updated_at,
        domain=domain_response,
        units=unit_responses
    )


@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    update: ProjectUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a project."""
    result = await db.execute(
        select(StrategizerProject)
        .where(StrategizerProject.id == project_id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if update.name is not None:
        project.name = update.name
    if update.brief is not None:
        project.brief = update.brief

    project.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(project)

    return await get_project(project_id, db)


@router.delete("/projects/{project_id}")
async def delete_project(
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete a project and all its data."""
    result = await db.execute(
        select(StrategizerProject)
        .where(StrategizerProject.id == project_id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    await db.delete(project)
    await db.commit()

    return {"message": "Project deleted successfully"}


# =============================================================================
# DOMAIN BOOTSTRAPPING (Placeholder - Step 4)
# =============================================================================

@router.post("/projects/{project_id}/bootstrap", response_model=DomainBootstrapResponse)
async def bootstrap_domain(
    project_id: str,
    request: DomainBootstrapRequest = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Bootstrap a domain from the project brief.
    Uses LLM to analyze brief and propose domain structure.
    """
    # Get project
    result = await db.execute(
        select(StrategizerProject)
        .options(selectinload(StrategizerProject.domain))
        .where(StrategizerProject.id == project_id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.domain:
        raise HTTPException(status_code=400, detail="Domain already exists. Delete it first to re-bootstrap.")

    # Call LLM to bootstrap domain
    try:
        llm = StrategizerLLM()
        bootstrap_result = await llm.bootstrap_domain(project.name, project.brief)

        if "error" in bootstrap_result:
            raise HTTPException(status_code=500, detail=f"LLM error: {bootstrap_result['error']}")

    except ValueError as e:
        # API key not set - use fallback
        bootstrap_result = {
            "domain_name": f"{project.name} Domain",
            "core_question": f"What is the core strategic question for {project.name}?",
            "success_looks_like": "[Configure ANTHROPIC_API_KEY for LLM analysis]",
            "vocabulary": {"concept": "Concept", "dialectic": "Tension", "actor": "Actor"},
            "template_base": None,
            "seed_concepts": [],
            "seed_dialectics": []
        }

    # Create domain
    domain = StrategizerDomain(
        project_id=project_id,
        name=bootstrap_result.get("domain_name", f"{project.name} Domain"),
        core_question=bootstrap_result.get("core_question"),
        success_looks_like=bootstrap_result.get("success_looks_like"),
        vocabulary=bootstrap_result.get("vocabulary", {
            "concept": "Concept",
            "dialectic": "Tension",
            "actor": "Actor"
        }),
        template_base=bootstrap_result.get("template_base")
    )
    db.add(domain)
    await db.flush()

    # Create seed content
    seed_content_list = []

    # Add seed concepts
    for concept in bootstrap_result.get("seed_concepts", []):
        seed = StrategizerSeedContent(
            domain_id=domain.id,
            content_type="concept",
            content={
                "name": concept.get("name"),
                "definition": concept.get("definition"),
                "why_fundamental": concept.get("why_fundamental")
            },
            accepted=None  # Pending user decision
        )
        db.add(seed)
        seed_content_list.append(seed)

    # Add seed dialectics
    for dialectic in bootstrap_result.get("seed_dialectics", []):
        seed = StrategizerSeedContent(
            domain_id=domain.id,
            content_type="dialectic",
            content={
                "name": dialectic.get("name"),
                "pole_a": dialectic.get("pole_a"),
                "pole_b": dialectic.get("pole_b"),
                "why_fundamental": dialectic.get("why_fundamental")
            },
            accepted=None
        )
        db.add(seed)
        seed_content_list.append(seed)

    await db.commit()
    await db.refresh(domain)

    return DomainBootstrapResponse(
        domain=DomainResponse(
            id=domain.id,
            name=domain.name,
            core_question=domain.core_question,
            success_looks_like=domain.success_looks_like,
            vocabulary=VocabularyMapping(**domain.vocabulary),
            template_base=domain.template_base,
            seed_content=[
                SeedContentResponse(
                    id=seed.id,
                    content_type=seed.content_type,
                    content=seed.content,
                    accepted=seed.accepted
                )
                for seed in seed_content_list
            ],
            created_at=domain.created_at
        ),
        message=f"Domain bootstrapped with {len(seed_content_list)} seed items"
    )


@router.get("/projects/{project_id}/domain", response_model=DomainResponse)
async def get_domain(
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get domain details for a project."""
    result = await db.execute(
        select(StrategizerDomain)
        .options(selectinload(StrategizerDomain.seed_content))
        .where(StrategizerDomain.project_id == project_id)
    )
    domain = result.scalar_one_or_none()

    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found. Bootstrap first.")

    return DomainResponse(
        id=domain.id,
        name=domain.name,
        core_question=domain.core_question,
        success_looks_like=domain.success_looks_like,
        vocabulary=VocabularyMapping(**(domain.vocabulary or {})),
        template_base=domain.template_base,
        seed_content=[
            SeedContentResponse(
                id=seed.id,
                content_type=seed.content_type,
                content=seed.content,
                accepted=seed.accepted
            )
            for seed in domain.seed_content
        ],
        created_at=domain.created_at
    )


@router.delete("/projects/{project_id}/domain")
async def delete_domain(
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete a domain to allow re-bootstrapping."""
    result = await db.execute(
        select(StrategizerDomain)
        .where(StrategizerDomain.project_id == project_id)
    )
    domain = result.scalar_one_or_none()

    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")

    await db.delete(domain)
    await db.commit()

    return {"message": "Domain deleted successfully"}


@router.post("/projects/{project_id}/domain/seeds/accept")
async def accept_reject_seeds(
    project_id: str,
    request: SeedAcceptReject,
    db: AsyncSession = Depends(get_db)
):
    """Accept or reject seed content."""
    result = await db.execute(
        select(StrategizerDomain)
        .where(StrategizerDomain.project_id == project_id)
    )
    domain = result.scalar_one_or_none()

    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")

    # Update seed content
    for seed_id in request.seed_ids:
        seed_result = await db.execute(
            select(StrategizerSeedContent)
            .where(
                StrategizerSeedContent.id == seed_id,
                StrategizerSeedContent.domain_id == domain.id
            )
        )
        seed = seed_result.scalar_one_or_none()
        if seed:
            seed.accepted = request.accept

            # If accepted, create the unit
            if request.accept and seed.content_type in ["concept", "dialectic", "actor"]:
                unit = StrategizerUnit(
                    project_id=project_id,
                    unit_type=UnitType(seed.content_type),
                    display_type=domain.vocabulary.get(seed.content_type, seed.content_type.title()),
                    name=seed.content.get("name", "Unnamed"),
                    definition=seed.content.get("definition", ""),
                    content=seed.content,
                    status=UnitStatus.DRAFT
                )
                db.add(unit)

    await db.commit()

    return {"message": f"Seeds {'accepted' if request.accept else 'rejected'} successfully"}


# =============================================================================
# UNITS (Step 2 - Basic CRUD)
# =============================================================================

@router.post("/projects/{project_id}/units", response_model=UnitResponse)
async def create_unit(
    project_id: str,
    unit: UnitCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new unit."""
    # Verify project exists and get domain for vocabulary
    result = await db.execute(
        select(StrategizerProject)
        .options(selectinload(StrategizerProject.domain))
        .where(StrategizerProject.id == project_id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Get display type from domain vocabulary
    display_type = unit.unit_type.value.title()
    if project.domain and project.domain.vocabulary:
        display_type = project.domain.vocabulary.get(unit.unit_type.value, display_type)

    db_unit = StrategizerUnit(
        project_id=project_id,
        unit_type=unit.unit_type,
        display_type=display_type,
        name=unit.name,
        definition=unit.definition,
        content=unit.content or {},
        status=UnitStatus.DRAFT
    )
    db.add(db_unit)
    await db.commit()
    await db.refresh(db_unit)

    return UnitResponse(
        id=db_unit.id,
        unit_type=db_unit.unit_type,
        display_type=db_unit.display_type,
        tier=db_unit.tier,
        name=db_unit.name,
        definition=db_unit.definition,
        content=db_unit.content or {},
        status=db_unit.status,
        version=db_unit.version,
        created_at=db_unit.created_at,
        updated_at=db_unit.updated_at
    )


@router.get("/projects/{project_id}/units", response_model=List[UnitResponse])
async def list_units(
    project_id: str,
    unit_type: Optional[UnitType] = None,
    status: Optional[UnitStatus] = None,
    db: AsyncSession = Depends(get_db)
):
    """List units for a project."""
    query = select(StrategizerUnit).where(StrategizerUnit.project_id == project_id)

    if unit_type:
        query = query.where(StrategizerUnit.unit_type == unit_type)
    if status:
        query = query.where(StrategizerUnit.status == status)

    query = query.order_by(StrategizerUnit.created_at.desc())

    result = await db.execute(query)
    units = result.scalars().all()

    return [
        UnitResponse(
            id=unit.id,
            unit_type=unit.unit_type,
            display_type=unit.display_type,
            tier=unit.tier,
            name=unit.name,
            definition=unit.definition,
            content=unit.content or {},
            status=unit.status,
            version=unit.version,
            created_at=unit.created_at,
            updated_at=unit.updated_at
        )
        for unit in units
    ]


@router.get("/projects/{project_id}/units/{unit_id}", response_model=UnitResponse)
async def get_unit(
    project_id: str,
    unit_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a unit by ID."""
    result = await db.execute(
        select(StrategizerUnit)
        .where(
            StrategizerUnit.id == unit_id,
            StrategizerUnit.project_id == project_id
        )
    )
    unit = result.scalar_one_or_none()

    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    return UnitResponse(
        id=unit.id,
        unit_type=unit.unit_type,
        display_type=unit.display_type,
        tier=unit.tier,
        name=unit.name,
        definition=unit.definition,
        content=unit.content or {},
        status=unit.status,
        version=unit.version,
        created_at=unit.created_at,
        updated_at=unit.updated_at
    )


@router.put("/projects/{project_id}/units/{unit_id}", response_model=UnitResponse)
async def update_unit(
    project_id: str,
    unit_id: str,
    update: UnitUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a unit."""
    result = await db.execute(
        select(StrategizerUnit)
        .where(
            StrategizerUnit.id == unit_id,
            StrategizerUnit.project_id == project_id
        )
    )
    unit = result.scalar_one_or_none()

    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    if update.name is not None:
        unit.name = update.name
    if update.definition is not None:
        unit.definition = update.definition
    if update.content is not None:
        unit.content = update.content
    if update.status is not None:
        unit.status = update.status

    unit.version += 1
    unit.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(unit)

    return UnitResponse(
        id=unit.id,
        unit_type=unit.unit_type,
        display_type=unit.display_type,
        tier=unit.tier,
        name=unit.name,
        definition=unit.definition,
        content=unit.content or {},
        status=unit.status,
        version=unit.version,
        created_at=unit.created_at,
        updated_at=unit.updated_at
    )


@router.delete("/projects/{project_id}/units/{unit_id}")
async def delete_unit(
    project_id: str,
    unit_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete a unit."""
    result = await db.execute(
        select(StrategizerUnit)
        .where(
            StrategizerUnit.id == unit_id,
            StrategizerUnit.project_id == project_id
        )
    )
    unit = result.scalar_one_or_none()

    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    await db.delete(unit)
    await db.commit()

    return {"message": "Unit deleted successfully"}


# =============================================================================
# GRIDS (Phase 2 - Multi-Grid Analytics)
# =============================================================================

@router.get("/grids/definitions")
async def list_grid_definitions():
    """List all available grid type definitions."""
    all_grids = []

    for grid_type, grid_def in TIER_1_GRIDS.items():
        all_grids.append(GridDefinitionResponse(
            grid_type=grid_type,
            name=grid_def["name"],
            description=grid_def["description"],
            slots=[SlotDefinition(**s) for s in grid_def["slots"]],
            tier="required",
            applicable_to=grid_def["applicable_to"]
        ))

    for grid_type, grid_def in TIER_2_GRIDS.items():
        all_grids.append(GridDefinitionResponse(
            grid_type=grid_type,
            name=grid_def["name"],
            description=grid_def["description"],
            slots=[SlotDefinition(**s) for s in grid_def["slots"]],
            tier="flexible",
            applicable_to=grid_def["applicable_to"]
        ))

    return all_grids


@router.get("/grids/applicable/{unit_type}", response_model=ApplicableGridsResponse)
async def get_grids_for_unit_type(unit_type: str):
    """Get grids applicable to a specific unit type."""
    applicable = get_applicable_grids(unit_type)

    return ApplicableGridsResponse(
        unit_type=unit_type,
        required=[
            GridDefinitionResponse(
                grid_type=g["grid_type"],
                name=g["name"],
                description=g["description"],
                slots=[SlotDefinition(**s) for s in g["slots"]],
                tier="required",
                applicable_to=g["applicable_to"]
            )
            for g in applicable["required"]
        ],
        flexible=[
            GridDefinitionResponse(
                grid_type=g["grid_type"],
                name=g["name"],
                description=g["description"],
                slots=[SlotDefinition(**s) for s in g["slots"]],
                tier="flexible",
                applicable_to=g["applicable_to"]
            )
            for g in applicable["flexible"]
        ]
    )


@router.post("/projects/{project_id}/units/{unit_id}/grids", response_model=GridResponse)
async def create_grid(
    project_id: str,
    unit_id: str,
    grid_create: GridCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new grid instance on a unit."""
    # Verify unit exists
    result = await db.execute(
        select(StrategizerUnit)
        .options(selectinload(StrategizerUnit.grids))
        .where(
            StrategizerUnit.id == unit_id,
            StrategizerUnit.project_id == project_id
        )
    )
    unit = result.scalar_one_or_none()

    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    # Validate grid type
    grid_def = get_grid_definition(grid_create.grid_type)
    if not grid_def:
        raise HTTPException(status_code=400, detail=f"Unknown grid type: {grid_create.grid_type}")

    # Check if grid already exists on this unit
    existing = [g for g in unit.grids if g.grid_type == grid_create.grid_type]
    if existing:
        raise HTTPException(status_code=400, detail=f"Grid {grid_create.grid_type} already exists on this unit")

    # Determine tier from definition
    tier_value = grid_def.get("tier", "flexible")
    grid_tier = GridTier.REQUIRED if tier_value == "required" else GridTier.FLEXIBLE

    # Initialize empty slots
    initial_slots = {
        slot["name"]: {"content": "", "confidence": 0.0, "evidence_notes": None}
        for slot in grid_def["slots"]
    }

    # Create grid instance
    grid_instance = StrategizerGridInstance(
        unit_id=unit_id,
        grid_type=grid_create.grid_type,
        tier=grid_tier,
        slots=initial_slots
    )
    db.add(grid_instance)

    # Auto-fill with LLM if requested
    if grid_create.auto_fill:
        try:
            # Get project context
            proj_result = await db.execute(
                select(StrategizerProject)
                .options(selectinload(StrategizerProject.domain))
                .where(StrategizerProject.id == project_id)
            )
            project = proj_result.scalar_one_or_none()

            llm = StrategizerLLM()
            fill_result = await llm.auto_fill_grid(
                domain_context={
                    "name": project.domain.name if project.domain else "Unknown",
                    "core_question": project.domain.core_question if project.domain else None
                },
                unit={
                    "unit_type": unit.unit_type.value,
                    "display_type": unit.display_type,
                    "name": unit.name,
                    "definition": unit.definition,
                    "content": unit.content
                },
                grid_definition={
                    "grid_type": grid_create.grid_type,
                    **grid_def
                }
            )
            if "slots" in fill_result:
                grid_instance.slots = fill_result["slots"]
        except (ValueError, Exception) as e:
            # LLM not available or error - leave slots empty
            pass

    await db.commit()
    await db.refresh(grid_instance)

    # Convert slots to SlotContent objects
    slots_response = {
        name: SlotContent(
            content=data.get("content", ""),
            confidence=data.get("confidence", 0.0),
            evidence_notes=data.get("evidence_notes")
        )
        for name, data in (grid_instance.slots or {}).items()
    }

    return GridResponse(
        id=grid_instance.id,
        unit_id=grid_instance.unit_id,
        grid_type=grid_instance.grid_type,
        tier=grid_instance.tier,
        slots=slots_response,
        created_at=grid_instance.created_at,
        updated_at=grid_instance.updated_at
    )


@router.get("/projects/{project_id}/units/{unit_id}/grids", response_model=List[GridResponse])
async def list_unit_grids(
    project_id: str,
    unit_id: str,
    db: AsyncSession = Depends(get_db)
):
    """List all grids on a unit."""
    result = await db.execute(
        select(StrategizerGridInstance)
        .where(StrategizerGridInstance.unit_id == unit_id)
        .order_by(StrategizerGridInstance.created_at)
    )
    grids = result.scalars().all()

    return [
        GridResponse(
            id=grid.id,
            unit_id=grid.unit_id,
            grid_type=grid.grid_type,
            tier=grid.tier,
            slots={
                name: SlotContent(
                    content=data.get("content", ""),
                    confidence=data.get("confidence", 0.0),
                    evidence_notes=data.get("evidence_notes")
                )
                for name, data in (grid.slots or {}).items()
            },
            created_at=grid.created_at,
            updated_at=grid.updated_at
        )
        for grid in grids
    ]


@router.get("/projects/{project_id}/units/{unit_id}/grids/{grid_id}", response_model=GridResponse)
async def get_grid(
    project_id: str,
    unit_id: str,
    grid_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific grid instance."""
    result = await db.execute(
        select(StrategizerGridInstance)
        .where(
            StrategizerGridInstance.id == grid_id,
            StrategizerGridInstance.unit_id == unit_id
        )
    )
    grid = result.scalar_one_or_none()

    if not grid:
        raise HTTPException(status_code=404, detail="Grid not found")

    return GridResponse(
        id=grid.id,
        unit_id=grid.unit_id,
        grid_type=grid.grid_type,
        tier=grid.tier,
        slots={
            name: SlotContent(
                content=data.get("content", ""),
                confidence=data.get("confidence", 0.0),
                evidence_notes=data.get("evidence_notes")
            )
            for name, data in (grid.slots or {}).items()
        },
        created_at=grid.created_at,
        updated_at=grid.updated_at
    )


@router.put("/projects/{project_id}/units/{unit_id}/grids/{grid_id}/slots/{slot_name}")
async def update_grid_slot(
    project_id: str,
    unit_id: str,
    grid_id: str,
    slot_name: str,
    update: GridSlotUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a single slot in a grid."""
    result = await db.execute(
        select(StrategizerGridInstance)
        .where(
            StrategizerGridInstance.id == grid_id,
            StrategizerGridInstance.unit_id == unit_id
        )
    )
    grid = result.scalar_one_or_none()

    if not grid:
        raise HTTPException(status_code=404, detail="Grid not found")

    # Validate slot exists in grid definition
    grid_def = get_grid_definition(grid.grid_type)
    valid_slots = [s["name"] for s in grid_def["slots"]] if grid_def else []
    if slot_name not in valid_slots:
        raise HTTPException(status_code=400, detail=f"Invalid slot name: {slot_name}")

    # Update the slot - make a copy to ensure SQLAlchemy detects the change
    slots = dict(grid.slots or {})
    slots[slot_name] = {
        "content": update.content,
        "confidence": update.confidence if update.confidence is not None else 0.0,
        "evidence_notes": update.evidence_notes
    }
    grid.slots = slots
    grid.updated_at = datetime.utcnow()
    flag_modified(grid, "slots")

    await db.commit()

    return {"message": f"Slot '{slot_name}' updated successfully"}


@router.delete("/projects/{project_id}/units/{unit_id}/grids/{grid_id}")
async def delete_grid(
    project_id: str,
    unit_id: str,
    grid_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete a grid from a unit."""
    result = await db.execute(
        select(StrategizerGridInstance)
        .where(
            StrategizerGridInstance.id == grid_id,
            StrategizerGridInstance.unit_id == unit_id
        )
    )
    grid = result.scalar_one_or_none()

    if not grid:
        raise HTTPException(status_code=404, detail="Grid not found")

    await db.delete(grid)
    await db.commit()

    return {"message": "Grid deleted successfully"}


@router.post("/projects/{project_id}/units/{unit_id}/grids/auto-apply", response_model=GridAutoApplyResponse)
async def auto_apply_grids(
    project_id: str,
    unit_id: str,
    request: GridAutoApplyRequest = None,
    db: AsyncSession = Depends(get_db)
):
    """Auto-apply appropriate grids to a unit using LLM."""
    # Get unit with existing grids
    result = await db.execute(
        select(StrategizerUnit)
        .options(selectinload(StrategizerUnit.grids))
        .where(
            StrategizerUnit.id == unit_id,
            StrategizerUnit.project_id == project_id
        )
    )
    unit = result.scalar_one_or_none()

    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    # Get applicable grids
    applicable = get_applicable_grids(unit.unit_type.value)
    existing_types = {g.grid_type for g in unit.grids}

    grids_applied = []
    grids_skipped = []

    include_flexible = request.include_flexible if request else True
    auto_fill = request.auto_fill if request else True

    # Apply required grids
    for grid_info in applicable["required"]:
        grid_type = grid_info["grid_type"]
        if grid_type in existing_types:
            grids_skipped.append({"grid_type": grid_type, "reason": "Already exists"})
            continue

        # Create the grid
        grid_create = GridCreate(grid_type=grid_type, auto_fill=auto_fill)
        grid_response = await create_grid(project_id, unit_id, grid_create, db)
        grids_applied.append(grid_response)

    # Apply flexible grids if requested
    if include_flexible:
        for grid_info in applicable["flexible"]:
            grid_type = grid_info["grid_type"]
            if grid_type in existing_types:
                grids_skipped.append({"grid_type": grid_type, "reason": "Already exists"})
                continue

            grid_create = GridCreate(grid_type=grid_type, auto_fill=auto_fill)
            grid_response = await create_grid(project_id, unit_id, grid_create, db)
            grids_applied.append(grid_response)

    return GridAutoApplyResponse(
        grids_applied=grids_applied,
        grids_skipped=grids_skipped,
        message=f"Applied {len(grids_applied)} grids, skipped {len(grids_skipped)}"
    )


@router.post("/projects/{project_id}/grids/detect-friction", response_model=FrictionDetectionResponse)
async def detect_grid_friction(
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Detect friction (contradictions, gaps) across all grids in a project."""
    # Get all units with grids
    result = await db.execute(
        select(StrategizerUnit)
        .options(selectinload(StrategizerUnit.grids))
        .where(StrategizerUnit.project_id == project_id)
    )
    units = result.scalars().all()

    if not units:
        return FrictionDetectionResponse(
            friction_events=[],
            overall_coherence=1.0,
            summary="No units found in project"
        )

    # Collect all grids
    all_grids_data = []
    for unit in units:
        for grid in unit.grids:
            all_grids_data.append({
                "unit_name": unit.name,
                "unit_type": unit.unit_type.value,
                "grid_type": grid.grid_type,
                "slots": grid.slots
            })

    if not all_grids_data:
        return FrictionDetectionResponse(
            friction_events=[],
            overall_coherence=1.0,
            summary="No grids found on units"
        )

    # Try LLM friction detection
    try:
        # Get project context
        proj_result = await db.execute(
            select(StrategizerProject)
            .options(selectinload(StrategizerProject.domain))
            .where(StrategizerProject.id == project_id)
        )
        project = proj_result.scalar_one_or_none()

        llm = StrategizerLLM()
        friction_result = await llm.detect_grid_friction(
            grids=all_grids_data,
            domain_context={
                "name": project.domain.name if project.domain else "Unknown",
                "core_question": project.domain.core_question if project.domain else None
            }
        )

        return FrictionDetectionResponse(
            friction_events=[
                FrictionEvent(
                    type=e.get("type", "unknown"),
                    description=e.get("description", ""),
                    slots_involved=e.get("slots_involved", []),
                    severity=e.get("severity", "low"),
                    suggested_resolution=e.get("suggested_resolution", "")
                )
                for e in friction_result.get("friction_events", [])
            ],
            overall_coherence=friction_result.get("overall_coherence", 0.5),
            summary=friction_result.get("summary", "Analysis completed")
        )

    except (ValueError, Exception):
        # LLM not available - return basic analysis
        return FrictionDetectionResponse(
            friction_events=[],
            overall_coherence=0.5,
            summary="[LLM not configured] Basic analysis: Found {} grids across {} units".format(
                len(all_grids_data), len(units)
            )
        )


# =============================================================================
# DIALOGUE (Placeholder - Step 6)
# =============================================================================

@router.post("/projects/{project_id}/ask", response_model=DialogueResponse)
async def ask_question(
    project_id: str,
    request: DialogueAskRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Ask a question and get a framework-aware response.
    """
    # Get project with domain and units
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

    # Store the user's question
    user_turn = StrategizerDialogueTurn(
        project_id=project_id,
        turn_type=DialogueTurnType.USER_QUESTION,
        content=request.question,
        context=request.context or {}
    )
    db.add(user_turn)
    await db.flush()

    # Get recent dialogue history
    history_result = await db.execute(
        select(StrategizerDialogueTurn)
        .where(StrategizerDialogueTurn.project_id == project_id)
        .order_by(StrategizerDialogueTurn.created_at.desc())
        .limit(10)
    )
    dialogue_history = [
        {"turn_type": t.turn_type.value, "content": t.content}
        for t in reversed(history_result.scalars().all())
    ]

    # Build context for LLM
    domain_context = {}
    if project.domain:
        domain_context = {
            "name": project.domain.name,
            "core_question": project.domain.core_question,
            "vocabulary": project.domain.vocabulary or {}
        }

    units = [
        {
            "unit_type": u.unit_type.value,
            "name": u.name,
            "definition": u.definition
        }
        for u in project.units
    ]

    # Call LLM
    try:
        llm = StrategizerLLM()
        qa_result = await llm.answer_question(
            request.question,
            domain_context,
            units,
            dialogue_history
        )
        response_text = qa_result.get("response", "No response generated")
        implications = qa_result.get("implications")
        suggested_actions = [
            SuggestedAction(
                action_type=a.get("action_type", ""),
                parameters=a.get("parameters", {}),
                rationale=a.get("rationale")
            )
            for a in qa_result.get("suggested_actions", [])
        ]
        actions_proposed = qa_result.get("suggested_actions", [])

    except ValueError:
        # API key not set
        response_text = f"[LLM not configured] You asked: '{request.question}'. Configure ANTHROPIC_API_KEY to enable AI responses."
        implications = None
        suggested_actions = []
        actions_proposed = []

    # Store the system response
    system_turn = StrategizerDialogueTurn(
        project_id=project_id,
        turn_type=DialogueTurnType.SYSTEM_RESPONSE,
        content=response_text,
        context={"in_response_to": user_turn.id},
        actions_proposed=actions_proposed
    )
    db.add(system_turn)

    await db.commit()

    return DialogueResponse(
        response=response_text,
        implications=implications,
        suggested_actions=suggested_actions
    )


@router.get("/projects/{project_id}/dialogue", response_model=DialogueHistoryResponse)
async def get_dialogue_history(
    project_id: str,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """Get dialogue history for a project."""
    # Count total
    count_result = await db.execute(
        select(func.count(StrategizerDialogueTurn.id))
        .where(StrategizerDialogueTurn.project_id == project_id)
    )
    total_count = count_result.scalar() or 0

    # Get turns
    result = await db.execute(
        select(StrategizerDialogueTurn)
        .where(StrategizerDialogueTurn.project_id == project_id)
        .order_by(StrategizerDialogueTurn.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    turns = result.scalars().all()

    return DialogueHistoryResponse(
        turns=[
            DialogueTurnResponse(
                id=turn.id,
                turn_type=turn.turn_type,
                content=turn.content,
                context=turn.context or {},
                actions_proposed=turn.actions_proposed or [],
                actions_taken=turn.actions_taken or [],
                created_at=turn.created_at
            )
            for turn in reversed(turns)  # Chronological order
        ],
        total_count=total_count
    )


@router.post("/projects/{project_id}/suggest", response_model=SuggestionResponse)
async def get_suggestions(
    project_id: str,
    request: SuggestRequest = None,
    db: AsyncSession = Depends(get_db)
):
    """Get suggestions for next steps."""
    # Get project with domain and units
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

    # If no domain, return bootstrap suggestion
    if not project.domain:
        return SuggestionResponse(
            suggestions=["Bootstrap a domain from your project brief to get started"],
            priority_actions=[SuggestedAction(
                action_type="bootstrap_domain",
                parameters={},
                rationale="You need a domain before building your framework"
            )]
        )

    # Build context
    domain_context = {
        "name": project.domain.name,
        "core_question": project.domain.core_question,
        "vocabulary": project.domain.vocabulary or {}
    }

    units = [
        {
            "unit_type": u.unit_type.value,
            "name": u.name,
            "definition": u.definition
        }
        for u in project.units
    ]

    focus = request.focus if request else None

    # Try LLM suggestions
    try:
        llm = StrategizerLLM()
        suggestion_result = await llm.suggest_next_steps(domain_context, units, focus)

        suggestions = suggestion_result.get("suggestions", [])
        priority_actions = [
            SuggestedAction(
                action_type=a.get("action_type", ""),
                parameters=a.get("parameters", {}),
                rationale=a.get("rationale")
            )
            for a in suggestion_result.get("priority_actions", [])
        ]

    except ValueError:
        # API key not set - use basic heuristics
        suggestions = []
        priority_actions = []

        vocab = project.domain.vocabulary or {}
        concept_count = len([u for u in project.units if u.unit_type == UnitType.CONCEPT])
        dialectic_count = len([u for u in project.units if u.unit_type == UnitType.DIALECTIC])
        actor_count = len([u for u in project.units if u.unit_type == UnitType.ACTOR])

        if concept_count < 3:
            suggestions.append(f"Add more {vocab.get('concept', 'concepts')} (currently {concept_count})")
        if dialectic_count < 2:
            suggestions.append(f"Identify key {vocab.get('dialectic', 'tensions')} (currently {dialectic_count})")
        if actor_count < 2:
            suggestions.append(f"Map important {vocab.get('actor', 'actors')} (currently {actor_count})")

        if not suggestions:
            suggestions.append("Your framework is taking shape! Ask questions to refine it further.")

    return SuggestionResponse(
        suggestions=suggestions,
        priority_actions=priority_actions
    )
