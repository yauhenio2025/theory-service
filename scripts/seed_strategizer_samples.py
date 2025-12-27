#!/usr/bin/env python3
"""
Seed script for Strategizer Sample Projects

Creates 4 comprehensive sample projects across different domains:
1. Climate Tech Investment Strategy
2. Moldova Independent Media Strategy
3. Heritage Luxury Fashion House Strategy
4. Metropolitan Urban Mobility Strategy

Each project includes:
- Bootstrapped domain with vocabulary
- 8-15 units (concepts, dialectics, actors)
- Multiple grids per unit (LOGICAL, ACTOR, TEMPORAL)
- Evidence sources with fragments
- Mix of INTEGRATED, NEEDS_DECISION, ANALYZED, and PENDING fragments
- Interpretation options for ambiguous fragments

Usage:
    python scripts/seed_strategizer_samples.py                    # Seed all projects
    python scripts/seed_strategizer_samples.py --project climate  # Seed specific project
    python scripts/seed_strategizer_samples.py --clear            # Clear and re-seed
"""

import os
import sys
import argparse
import asyncio
from datetime import datetime, timezone

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from api.strategizer.models import (
    Base,
    StrategizerProject, StrategizerDomain, StrategizerUnit, StrategizerGridInstance,
    StrategizerEvidenceSource, StrategizerEvidenceFragment, StrategizerEvidenceInterpretation,
    UnitType, UnitTier, UnitStatus, GridTier,
    EvidenceSourceType, ExtractionStatus, AnalysisStatus, EvidenceRelationship,
    generate_uuid
)


# =============================================================================
# DATABASE SETUP
# =============================================================================

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql:///essay_genre_db")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# =============================================================================
# SEEDING FUNCTIONS
# =============================================================================

async def clear_strategizer_data(session: AsyncSession):
    """Clear all existing Strategizer data."""
    print("Clearing existing Strategizer data...")

    # Delete in reverse order of dependencies
    await session.execute(delete(StrategizerEvidenceInterpretation))
    await session.execute(delete(StrategizerEvidenceFragment))
    await session.execute(delete(StrategizerEvidenceSource))
    await session.execute(delete(StrategizerGridInstance))
    await session.execute(delete(StrategizerUnit))
    await session.execute(delete(StrategizerDomain))
    await session.execute(delete(StrategizerProject))

    await session.commit()
    print("  Cleared all data.")


async def seed_project(session: AsyncSession, project_data: dict) -> StrategizerProject:
    """Seed a single project with all its data."""
    project_name = project_data["name"]
    print(f"\nSeeding project: {project_name}")

    # 1. Create Project
    project = StrategizerProject(
        id=generate_uuid(),
        name=project_name,
        brief=project_data["brief"],
    )
    session.add(project)
    await session.flush()
    print(f"  Created project: {project.id}")

    # 2. Create Domain
    domain_data = project_data["domain"]
    domain = StrategizerDomain(
        id=generate_uuid(),
        project_id=project.id,
        name=domain_data["name"],
        core_question=domain_data["core_question"],
        success_looks_like=domain_data["success_looks_like"],
        vocabulary=domain_data["vocabulary"],
        template_base=domain_data.get("template_base"),
    )
    session.add(domain)
    await session.flush()
    print(f"  Created domain: {domain.name}")

    # 3. Create Units with Grids
    unit_name_to_id = {}  # For linking evidence fragments
    unit_count = 0
    grid_count = 0

    for unit_data in project_data["units"]:
        unit = StrategizerUnit(
            id=generate_uuid(),
            project_id=project.id,
            unit_type=unit_data["unit_type"],
            display_type=unit_data.get("display_type"),
            tier=unit_data.get("tier", UnitTier.DOMAIN),
            name=unit_data["name"],
            definition=unit_data.get("definition"),
            content=unit_data.get("content", {}),
            status=UnitStatus.DRAFT,
        )
        session.add(unit)
        await session.flush()
        unit_name_to_id[unit.name] = unit.id
        unit_count += 1

        # Create grids for this unit
        grids_data = unit_data.get("grids", {})
        for grid_type, slots in grids_data.items():
            # Format slots properly
            formatted_slots = {}
            for slot_name, content in slots.items():
                formatted_slots[slot_name] = {
                    "content": content,
                    "confidence": 0.75,  # Default confidence
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                }

            grid = StrategizerGridInstance(
                id=generate_uuid(),
                unit_id=unit.id,
                grid_type=grid_type,
                tier=GridTier.REQUIRED if grid_type in ["LOGICAL", "ACTOR", "TEMPORAL"] else GridTier.FLEXIBLE,
                slots=formatted_slots,
            )
            session.add(grid)
            grid_count += 1

    await session.flush()
    print(f"  Created {unit_count} units with {grid_count} grids")

    # 4. Create Evidence Sources and Fragments
    source_count = 0
    fragment_count = 0
    interpretation_count = 0

    for source_data in project_data.get("evidence_sources", []):
        source = StrategizerEvidenceSource(
            id=generate_uuid(),
            project_id=project.id,
            source_type=source_data["source_type"],
            source_name=source_data["source_name"],
            source_content=source_data.get("source_content"),
            extraction_status=ExtractionStatus.COMPLETED,
            extracted_count=len(source_data.get("fragments", [])),
        )
        session.add(source)
        await session.flush()
        source_count += 1

        # Create fragments for this source
        for frag_data in source_data.get("fragments", []):
            # Look up target unit ID if specified
            target_unit_id = None
            if "target_unit_name" in frag_data:
                target_unit_id = unit_name_to_id.get(frag_data["target_unit_name"])

            fragment = StrategizerEvidenceFragment(
                id=generate_uuid(),
                source_id=source.id,
                content=frag_data["content"],
                source_location=frag_data.get("source_location"),
                analysis_status=frag_data.get("status", AnalysisStatus.PENDING),
                relationship_type=frag_data.get("relationship_type"),
                target_unit_id=target_unit_id,
                target_grid_slot=frag_data.get("target_grid_slot"),
                confidence=frag_data.get("confidence"),
                is_ambiguous=frag_data.get("status") == AnalysisStatus.NEEDS_DECISION,
                why_needs_decision=frag_data.get("why_needs_decision"),
            )
            session.add(fragment)
            await session.flush()
            fragment_count += 1

            # Create interpretations for NEEDS_DECISION fragments
            for interp_data in frag_data.get("interpretations", []):
                # Look up target unit ID for this interpretation
                interp_target_unit_id = None
                if "target_unit_name" in interp_data:
                    interp_target_unit_id = unit_name_to_id.get(interp_data["target_unit_name"])

                interpretation = StrategizerEvidenceInterpretation(
                    id=generate_uuid(),
                    fragment_id=fragment.id,
                    interpretation_key=interp_data["key"],
                    title=interp_data["title"],
                    strategy=interp_data.get("strategy"),
                    rationale=interp_data.get("rationale"),
                    relationship_type=interp_data.get("relationship_type"),
                    target_unit_id=interp_target_unit_id,
                    target_grid_slot=interp_data.get("target_grid_slot"),
                    is_recommended=interp_data.get("is_recommended", False),
                    commitment_statement=interp_data.get("commitment_statement"),
                    foreclosure_statements=interp_data.get("foreclosure_statements"),
                )
                session.add(interpretation)
                interpretation_count += 1

    await session.flush()
    print(f"  Created {source_count} sources, {fragment_count} fragments, {interpretation_count} interpretations")

    return project


async def seed_all_projects(clear: bool = False, project_filter: str = None):
    """Seed all sample projects."""
    # Import sample data
    from scripts.sample_data import ALL_PROJECTS

    async with AsyncSessionLocal() as session:
        try:
            if clear:
                await clear_strategizer_data(session)

            # Filter projects if specified
            projects_to_seed = ALL_PROJECTS
            if project_filter:
                filter_lower = project_filter.lower()
                projects_to_seed = [
                    p for p in ALL_PROJECTS
                    if filter_lower in p["name"].lower()
                ]
                if not projects_to_seed:
                    print(f"No projects matching '{project_filter}' found.")
                    print(f"Available projects: {[p['name'] for p in ALL_PROJECTS]}")
                    return

            # Seed each project
            for project_data in projects_to_seed:
                await seed_project(session, project_data)

            await session.commit()

            # Print summary
            print("\n" + "=" * 60)
            print("SEEDING COMPLETE")
            print("=" * 60)

            # Count totals
            projects = await session.execute(select(StrategizerProject))
            units = await session.execute(select(StrategizerUnit))
            grids = await session.execute(select(StrategizerGridInstance))
            sources = await session.execute(select(StrategizerEvidenceSource))
            fragments = await session.execute(select(StrategizerEvidenceFragment))
            interpretations = await session.execute(select(StrategizerEvidenceInterpretation))

            # Get counts for different fragment statuses
            needs_decision = await session.execute(
                select(StrategizerEvidenceFragment).where(
                    StrategizerEvidenceFragment.analysis_status == AnalysisStatus.NEEDS_DECISION
                )
            )

            print(f"Projects: {len(projects.all())}")
            print(f"Units: {len(units.all())}")
            print(f"Grid Instances: {len(grids.all())}")
            print(f"Evidence Sources: {len(sources.all())}")
            print(f"Evidence Fragments: {len(fragments.all())}")
            print(f"  - NEEDS_DECISION: {len(needs_decision.all())}")
            print(f"Interpretations: {len(interpretations.all())}")
            print("=" * 60)
            print("\nView projects at: /api/strategizer/ui/")

        except Exception as e:
            await session.rollback()
            print(f"\nError during seeding: {e}")
            import traceback
            traceback.print_exc()
            raise


def main():
    parser = argparse.ArgumentParser(description="Seed Strategizer sample projects")
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear existing data before seeding"
    )
    parser.add_argument(
        "--project",
        type=str,
        help="Seed only projects matching this name (partial match)"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("STRATEGIZER SAMPLE DATA SEEDING")
    print("=" * 60)
    print(f"Database: {DATABASE_URL}")
    print(f"Clear existing: {args.clear}")
    print(f"Project filter: {args.project or 'All'}")
    print("=" * 60)

    asyncio.run(seed_all_projects(clear=args.clear, project_filter=args.project))


if __name__ == "__main__":
    main()
