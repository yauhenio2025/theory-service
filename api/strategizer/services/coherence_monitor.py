"""
Coherence Monitor Service

Proactive LLM-based detection of theoretical predicaments (tensions, gaps, inconsistencies)
in strategic frameworks. Uses two modes:

1. Quick Scan (Sonnet): Light auto-check on framework changes
2. Deep Analysis (Opus 4.5 + Extended Thinking): Comprehensive coherence review

Predicament lifecycle: DETECTED → ANALYZING → RESOLVED → DIALECTIC (or DEFERRED)
"""

import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

from anthropic import Anthropic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..models import (
    StrategizerProject,
    StrategizerDomain,
    StrategizerUnit,
    StrategizerGridInstance,
    StrategizerEvidenceFragment,
    StrategizerPredicament,
    PredicamentType,
    PredicamentSeverity,
    PredicamentStatus,
    UnitType,
    UnitTier,
    UnitStatus,
)
from ..prompts.coherence_prompts import (
    QUICK_SCAN_PROMPT,
    DEEP_ANALYSIS_PROMPT,
    PREDICAMENT_GRID_PROMPT,
    RESOLUTION_PROMPT,
    PREDICAMENT_SLOT_FILL_PROMPT,
)


# Model configuration
SONNET_MODEL = os.getenv("STRATEGIZER_MODEL", "claude-sonnet-4-5-20250929")
OPUS_MODEL = "claude-opus-4-5-20251101"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


class CoherenceMonitor:
    """
    LLM-powered coherence monitoring for theoretical frameworks.

    Detects predicaments (tensions, gaps, inconsistencies) and generates
    analytical grids to help resolve them.
    """

    def __init__(self):
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
        self.sonnet_model = SONNET_MODEL
        self.opus_model = OPUS_MODEL

    # =========================================================================
    # QUICK COHERENCE SCAN (Sonnet, minimal thinking)
    # =========================================================================

    async def quick_coherence_scan(
        self,
        db: AsyncSession,
        project_id: str
    ) -> Dict[str, Any]:
        """
        Light coherence check triggered on framework changes.

        Uses Sonnet for fast detection of obvious tensions.
        Suitable for auto-triggering after unit/grid/evidence updates.

        Returns:
            Dict with predicaments found and summary
        """
        # Gather framework context
        context = await self._gather_framework_context(db, project_id, full_detail=False)
        if "error" in context:
            return context

        # Build prompt
        prompt = QUICK_SCAN_PROMPT.format(
            domain_name=context["domain_name"],
            core_question=context["core_question"],
            units_summary=context["units_summary"],
            evidence_summary=context["evidence_summary"]
        )

        # Call Sonnet (fast, minimal thinking)
        response = self.client.messages.create(
            model=self.sonnet_model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = response.content[0].text
        predicaments = self._parse_json_response(response_text, [])

        # Save new predicaments to database
        new_predicaments = await self._save_predicaments(
            db, project_id, predicaments, context["unit_name_to_id"]
        )

        return {
            "analysis_depth": "quick",
            "predicaments_found": predicaments,
            "new_detected": len(new_predicaments),
            "total_found": len(predicaments),
            "thinking_tokens_used": None  # Quick scan doesn't use extended thinking
        }

    # =========================================================================
    # DEEP COHERENCE ANALYSIS (Opus 4.5 + Extended Thinking)
    # =========================================================================

    async def deep_coherence_analysis(
        self,
        db: AsyncSession,
        project_id: str,
        focus_unit_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive coherence analysis with Opus 4.5 and extended thinking.

        Uses 10K thinking token budget for deep reasoning about:
        - Cross-concept tensions
        - Empirical gaps
        - Missing distinctions
        - Praxis limitations

        Args:
            db: Database session
            project_id: Project to analyze
            focus_unit_ids: Optional list of unit IDs to focus on

        Returns:
            Dict with full coherence report including predicaments
        """
        # Gather detailed framework context
        context = await self._gather_framework_context(db, project_id, full_detail=True)
        if "error" in context:
            return context

        # Build comprehensive prompt
        prompt = DEEP_ANALYSIS_PROMPT.format(
            domain_name=context["domain_name"],
            core_question=context["core_question"],
            success_criteria=context.get("success_criteria", "Not specified"),
            vocabulary=json.dumps(context.get("vocabulary", {})),
            concept_count=context["concept_count"],
            concepts_detail=context["concepts_detail"],
            dialectic_count=context["dialectic_count"],
            dialectics_detail=context["dialectics_detail"],
            actor_count=context["actor_count"],
            actors_detail=context["actors_detail"],
            grids_summary=context["grids_summary"],
            evidence_detail=context["evidence_detail"]
        )

        # Use streaming for Opus 4.5 with extended thinking
        thinking_content = ""
        response_text = ""
        thinking_tokens = 0

        with self.client.messages.stream(
            model=self.opus_model,
            max_tokens=16000,
            thinking={
                "type": "enabled",
                "budget_tokens": 10000  # Generous thinking budget
            },
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            for event in stream:
                if hasattr(event, 'type'):
                    if event.type == 'content_block_delta':
                        if hasattr(event.delta, 'thinking'):
                            thinking_content += event.delta.thinking
                        elif hasattr(event.delta, 'text'):
                            response_text += event.delta.text

            # Get final message for usage stats
            final_message = stream.get_final_message()
            if hasattr(final_message, 'usage'):
                # Extended thinking tokens are tracked separately
                thinking_tokens = getattr(final_message.usage, 'thinking_tokens', 0)

        # Parse the analysis
        analysis = self._parse_json_response(response_text, {
            "overall_coherence": 0.5,
            "coherence_assessment": "Unable to complete analysis",
            "predicaments": [],
            "missing_concepts": [],
            "framework_strengths": [],
            "priority_issues": []
        })

        # Save predicaments
        predicaments = analysis.get("predicaments", [])
        new_predicaments = await self._save_predicaments(
            db, project_id, predicaments, context["unit_name_to_id"]
        )

        return {
            "analysis_depth": "deep",
            "overall_coherence": analysis.get("overall_coherence", 0.5),
            "coherence_assessment": analysis.get("coherence_assessment", ""),
            "predicaments_found": predicaments,
            "new_detected": len(new_predicaments),
            "total_found": len(predicaments),
            "missing_concepts": analysis.get("missing_concepts", []),
            "framework_strengths": analysis.get("framework_strengths", []),
            "priority_issues": analysis.get("priority_issues", []),
            "thinking_tokens_used": thinking_tokens,
            "thinking_summary": thinking_content[:500] if thinking_content else None
        }

    # =========================================================================
    # PREDICAMENT GRID GENERATION
    # =========================================================================

    async def generate_predicament_grid(
        self,
        db: AsyncSession,
        predicament_id: str
    ) -> Dict[str, Any]:
        """
        Generate a custom analytical grid for resolving a predicament.

        The grid is tailored to the predicament type:
        - THEORETICAL: Focus on assumptions, implications, synthesis
        - EMPIRICAL: Focus on evidence, explanatory gaps, theory modifications
        - CONCEPTUAL: Focus on distinctions, edge cases, alternative framings
        - PRAXIS: Focus on decision criteria, action options, trade-offs

        Returns:
            Dict with generated grid structure and initial slot content
        """
        # Load predicament with context
        result = await db.execute(
            select(StrategizerPredicament)
            .where(StrategizerPredicament.id == predicament_id)
        )
        predicament = result.scalar_one_or_none()
        if not predicament:
            return {"error": f"Predicament {predicament_id} not found"}

        # Load project context
        context = await self._gather_framework_context(
            db, predicament.project_id, full_detail=False
        )

        # Load source units
        source_units_detail = ""
        if predicament.source_unit_ids:
            result = await db.execute(
                select(StrategizerUnit)
                .where(StrategizerUnit.id.in_(predicament.source_unit_ids))
            )
            source_units = result.scalars().all()
            source_units_detail = "\n".join([
                f"- {u.name} ({u.unit_type.value}): {u.definition or 'No definition'}"
                for u in source_units
            ])

        # Load source evidence
        source_evidence_detail = ""
        if predicament.source_evidence_ids:
            result = await db.execute(
                select(StrategizerEvidenceFragment)
                .where(StrategizerEvidenceFragment.id.in_(predicament.source_evidence_ids))
            )
            source_evidence = result.scalars().all()
            source_evidence_detail = "\n".join([
                f"- {e.content[:200]}..."
                for e in source_evidence
            ])

        # Build prompt
        prompt = PREDICAMENT_GRID_PROMPT.format(
            domain_name=context["domain_name"],
            core_question=context["core_question"],
            predicament_title=predicament.title,
            predicament_type=predicament.predicament_type.value,
            predicament_description=predicament.description,
            pole_a=predicament.pole_a or "Not specified",
            pole_b=predicament.pole_b or "Not specified",
            source_units_detail=source_units_detail or "(no specific units)",
            source_evidence_detail=source_evidence_detail or "(no specific evidence)"
        )

        # Generate grid (Sonnet is fine for this)
        response = self.client.messages.create(
            model=self.sonnet_model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = response.content[0].text
        grid_spec = self._parse_json_response(response_text, {
            "grid_type": "PREDICAMENT_ANALYSIS",
            "grid_name": f"Analysis Grid for: {predicament.title}",
            "grid_description": "Failed to generate grid",
            "slots": [],
            "analysis_sequence": "Unable to determine",
            "resolution_criteria": "Unable to determine"
        })

        # Create grid instance in database
        grid_instance = await self._create_predicament_grid(
            db, predicament, grid_spec
        )

        # Update predicament status and link grid
        predicament.status = PredicamentStatus.ANALYZING
        predicament.generated_grid_id = grid_instance.id
        predicament.updated_at = datetime.utcnow()
        await db.commit()

        return {
            "predicament_id": predicament_id,
            "grid_id": grid_instance.id,
            "grid_spec": grid_spec,
            "status": "analyzing"
        }

    # =========================================================================
    # PREDICAMENT RESOLUTION → DIALECTIC
    # =========================================================================

    async def resolve_to_dialectic(
        self,
        db: AsyncSession,
        predicament_id: str,
        resolution_approach: str,
        dialectic_name: str,
        resolution_notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Transform a resolved predicament into a dialectic unit.

        This captures the tension as a permanent part of the framework,
        turning a problem into a navigable dynamic.

        Args:
            db: Database session
            predicament_id: The predicament to resolve
            resolution_approach: How the predicament was resolved
            dialectic_name: Name for the new dialectic
            resolution_notes: Additional notes

        Returns:
            Dict with the new dialectic unit
        """
        # Load predicament
        result = await db.execute(
            select(StrategizerPredicament)
            .options(selectinload(StrategizerPredicament.generated_grid))
            .where(StrategizerPredicament.id == predicament_id)
        )
        predicament = result.scalar_one_or_none()
        if not predicament:
            return {"error": f"Predicament {predicament_id} not found"}

        # Load project context
        context = await self._gather_framework_context(
            db, predicament.project_id, full_detail=False
        )

        # Get grid content if available
        grid_content = ""
        if predicament.generated_grid:
            slots = predicament.generated_grid.slots or {}
            grid_content = json.dumps(slots, indent=2)

        # Build prompt for LLM to help structure the dialectic
        prompt = RESOLUTION_PROMPT.format(
            domain_name=context["domain_name"],
            predicament_title=predicament.title,
            predicament_type=predicament.predicament_type.value,
            predicament_description=predicament.description,
            pole_a=predicament.pole_a or "Not specified",
            pole_b=predicament.pole_b or "Not specified",
            resolution_approach=resolution_approach,
            resolution_notes=resolution_notes or "(none)",
            grid_content=grid_content or "(no grid)"
        )

        # Get LLM guidance on dialectic structure
        response = self.client.messages.create(
            model=self.sonnet_model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = response.content[0].text
        dialectic_spec = self._parse_json_response(response_text, {
            "name": dialectic_name,
            "definition": predicament.description,
            "content": {
                "pole_a": {"name": "Pole A", "description": predicament.pole_a or ""},
                "pole_b": {"name": "Pole B", "description": predicament.pole_b or ""},
                "synthesis_approach": resolution_approach,
                "navigation_strategies": [],
            },
            "grids_to_generate": ["LOGICAL"]
        })

        # Create the dialectic unit
        dialectic = StrategizerUnit(
            project_id=predicament.project_id,
            unit_type=UnitType.DIALECTIC,
            tier=UnitTier.EMERGENT,
            name=dialectic_spec.get("name", dialectic_name),
            definition=dialectic_spec.get("definition", predicament.description),
            content={
                **dialectic_spec.get("content", {}),
                "emerged_from_predicament": {
                    "predicament_id": predicament_id,
                    "predicament_type": predicament.predicament_type.value,
                    "original_description": predicament.description,
                    "resolution_approach": resolution_approach
                }
            },
            status=UnitStatus.TESTED  # Already tested through predicament analysis
        )
        db.add(dialectic)
        await db.flush()

        # Update predicament
        predicament.status = PredicamentStatus.RESOLVED
        predicament.resolution_notes = resolution_notes
        predicament.resulting_dialectic_id = dialectic.id
        predicament.resolved_at = datetime.utcnow()
        predicament.updated_at = datetime.utcnow()

        await db.commit()

        return {
            "predicament_id": predicament_id,
            "predicament_status": "resolved",
            "dialectic_id": dialectic.id,
            "dialectic_name": dialectic.name,
            "dialectic_content": dialectic.content,
            "grids_to_generate": dialectic_spec.get("grids_to_generate", [])
        }

    # =========================================================================
    # PREDICAMENT GRID SLOT FILLING
    # =========================================================================

    async def fill_predicament_grid_slot(
        self,
        db: AsyncSession,
        predicament_id: str,
        slot_name: str
    ) -> Dict[str, Any]:
        """
        Auto-fill a single slot in a predicament's analytical grid.

        Uses the predicament context and other slot content to generate
        thoughtful content for the specified slot.
        """
        # Load predicament with grid
        result = await db.execute(
            select(StrategizerPredicament)
            .options(selectinload(StrategizerPredicament.generated_grid))
            .where(StrategizerPredicament.id == predicament_id)
        )
        predicament = result.scalar_one_or_none()
        if not predicament:
            return {"error": f"Predicament {predicament_id} not found"}

        if not predicament.generated_grid:
            return {"error": "Predicament has no generated grid"}

        grid = predicament.generated_grid
        slots = grid.slots or {}

        # Find slot definition (stored in grid metadata or inferred)
        slot_description = f"Slot for analyzing {slot_name}"
        slot_prompt = f"What should we consider for {slot_name}?"

        # Get other slots context
        other_slots = {k: v for k, v in slots.items() if k != slot_name}
        other_slots_context = json.dumps(other_slots, indent=2) if other_slots else "(no other slots filled)"

        # Load project context
        context = await self._gather_framework_context(
            db, predicament.project_id, full_detail=False
        )

        prompt = PREDICAMENT_SLOT_FILL_PROMPT.format(
            domain_name=context["domain_name"],
            predicament_title=predicament.title,
            predicament_type=predicament.predicament_type.value,
            predicament_description=predicament.description,
            pole_a=predicament.pole_a or "Not specified",
            pole_b=predicament.pole_b or "Not specified",
            slot_name=slot_name,
            slot_description=slot_description,
            slot_prompt=slot_prompt,
            other_slots_context=other_slots_context
        )

        response = self.client.messages.create(
            model=self.sonnet_model,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = response.content[0].text
        slot_content = self._parse_json_response(response_text, {
            "content": "Unable to generate content",
            "confidence": 0.5,
            "notes": None
        })

        # Update grid slot
        slots[slot_name] = {
            "content": slot_content.get("content", ""),
            "confidence": slot_content.get("confidence", 0.5),
            "evidence_notes": slot_content.get("notes")
        }
        grid.slots = slots
        grid.updated_at = datetime.utcnow()
        await db.commit()

        return {
            "predicament_id": predicament_id,
            "grid_id": grid.id,
            "slot_name": slot_name,
            "slot_content": slots[slot_name]
        }

    # =========================================================================
    # HELPER METHODS
    # =========================================================================

    async def _gather_framework_context(
        self,
        db: AsyncSession,
        project_id: str,
        full_detail: bool = False
    ) -> Dict[str, Any]:
        """Gather framework context for coherence analysis."""
        # Load project with domain
        result = await db.execute(
            select(StrategizerProject)
            .options(selectinload(StrategizerProject.domain))
            .where(StrategizerProject.id == project_id)
        )
        project = result.scalar_one_or_none()
        if not project:
            return {"error": f"Project {project_id} not found"}

        domain = project.domain
        if not domain:
            return {"error": "Project has no domain bootstrapped"}

        # Load all units
        result = await db.execute(
            select(StrategizerUnit)
            .where(StrategizerUnit.project_id == project_id)
        )
        units = result.scalars().all()

        # Build unit name to ID mapping
        unit_name_to_id = {u.name: u.id for u in units}

        # Categorize units
        concepts = [u for u in units if u.unit_type == UnitType.CONCEPT]
        dialectics = [u for u in units if u.unit_type == UnitType.DIALECTIC]
        actors = [u for u in units if u.unit_type == UnitType.ACTOR]

        # Load evidence fragments
        result = await db.execute(
            select(StrategizerEvidenceFragment)
            .join(StrategizerEvidenceFragment.source)
            .where(StrategizerEvidenceFragment.source.has(project_id=project_id))
        )
        fragments = result.scalars().all()

        # Build context dict
        context = {
            "project_id": project_id,
            "domain_name": domain.name,
            "core_question": domain.core_question or "Not specified",
            "success_criteria": domain.success_looks_like,
            "vocabulary": domain.vocabulary or {},
            "unit_name_to_id": unit_name_to_id,
            "concept_count": len(concepts),
            "dialectic_count": len(dialectics),
            "actor_count": len(actors),
        }

        if full_detail:
            # Detailed unit descriptions
            context["concepts_detail"] = self._format_units_detail(concepts)
            context["dialectics_detail"] = self._format_units_detail(dialectics)
            context["actors_detail"] = self._format_units_detail(actors)

            # Load grids for summary
            result = await db.execute(
                select(StrategizerGridInstance)
                .where(StrategizerGridInstance.unit_id.in_([u.id for u in units]))
            )
            grids = result.scalars().all()
            context["grids_summary"] = self._format_grids_summary(grids, units)

            # Detailed evidence
            context["evidence_detail"] = self._format_evidence_detail(fragments)
        else:
            # Summary only
            context["units_summary"] = self._format_units_summary(units)
            context["evidence_summary"] = self._format_evidence_summary(fragments)

        return context

    def _format_units_summary(self, units: List[StrategizerUnit]) -> str:
        """Format units as a brief summary."""
        lines = []
        for u in units:
            lines.append(f"- [{u.unit_type.value.upper()}] {u.name}: {u.definition or '(no definition)'}".strip())
        return "\n".join(lines) or "(no units yet)"

    def _format_units_detail(self, units: List[StrategizerUnit]) -> str:
        """Format units with full detail."""
        if not units:
            return "(none)"
        lines = []
        for u in units:
            lines.append(f"## {u.name}")
            lines.append(f"Definition: {u.definition or '(none)'}")
            if u.content:
                lines.append(f"Content: {json.dumps(u.content, indent=2)}")
            lines.append("")
        return "\n".join(lines)

    def _format_grids_summary(
        self,
        grids: List[StrategizerGridInstance],
        units: List[StrategizerUnit]
    ) -> str:
        """Format grids summary showing slot fill status."""
        if not grids:
            return "(no grids yet)"

        unit_map = {u.id: u.name for u in units}
        lines = []
        for g in grids[:20]:  # Limit to first 20
            unit_name = unit_map.get(g.unit_id, "Unknown")
            slots = g.slots or {}
            filled = sum(1 for v in slots.values() if v.get("content"))
            lines.append(f"- {unit_name} / {g.grid_type}: {filled} slots filled")
        if len(grids) > 20:
            lines.append(f"... and {len(grids) - 20} more grids")
        return "\n".join(lines)

    def _format_evidence_summary(self, fragments: List[StrategizerEvidenceFragment]) -> str:
        """Format evidence as brief summary."""
        if not fragments:
            return "(no evidence yet)"
        lines = []
        for f in fragments[:10]:
            status = f.analysis_status.value if hasattr(f.analysis_status, 'value') else str(f.analysis_status)
            lines.append(f"- [{status}] {f.content[:100]}...")
        if len(fragments) > 10:
            lines.append(f"... and {len(fragments) - 10} more fragments")
        return "\n".join(lines)

    def _format_evidence_detail(self, fragments: List[StrategizerEvidenceFragment]) -> str:
        """Format evidence with analysis status."""
        if not fragments:
            return "(no evidence yet)"
        lines = []
        for f in fragments:
            status = f.analysis_status.value if hasattr(f.analysis_status, 'value') else str(f.analysis_status)
            lines.append(f"## Fragment [{status}]")
            lines.append(f"Content: {f.content[:300]}...")
            if f.why_needs_decision:
                lines.append(f"Decision needed: {f.why_needs_decision}")
            lines.append("")
        return "\n".join(lines)

    async def _save_predicaments(
        self,
        db: AsyncSession,
        project_id: str,
        predicaments: List[Dict[str, Any]],
        unit_name_to_id: Dict[str, str]
    ) -> List[StrategizerPredicament]:
        """Save detected predicaments to database."""
        new_predicaments = []

        for p in predicaments:
            # Map predicament type
            pred_type_str = p.get("predicament_type", "theoretical").lower()
            try:
                pred_type = PredicamentType(pred_type_str)
            except ValueError:
                pred_type = PredicamentType.THEORETICAL

            # Map severity
            severity_str = p.get("severity", "medium").lower()
            try:
                severity = PredicamentSeverity(severity_str)
            except ValueError:
                severity = PredicamentSeverity.MEDIUM

            # Map unit names to IDs
            source_unit_names = p.get("source_unit_names", [])
            source_unit_ids = [
                unit_name_to_id[name]
                for name in source_unit_names
                if name in unit_name_to_id
            ]

            # Check if similar predicament already exists
            existing = await db.execute(
                select(StrategizerPredicament)
                .where(
                    StrategizerPredicament.project_id == project_id,
                    StrategizerPredicament.title == p.get("title", "Untitled"),
                    StrategizerPredicament.status != PredicamentStatus.RESOLVED
                )
            )
            if existing.scalar_one_or_none():
                continue  # Skip duplicates

            predicament = StrategizerPredicament(
                project_id=project_id,
                title=p.get("title", "Untitled Predicament"),
                description=p.get("description", ""),
                predicament_type=pred_type,
                severity=severity,
                pole_a=p.get("pole_a"),
                pole_b=p.get("pole_b"),
                source_unit_ids=source_unit_ids,
                source_evidence_ids=[],  # Can be populated from evidence locations
            )
            db.add(predicament)
            new_predicaments.append(predicament)

        if new_predicaments:
            await db.commit()

        return new_predicaments

    async def _create_predicament_grid(
        self,
        db: AsyncSession,
        predicament: StrategizerPredicament,
        grid_spec: Dict[str, Any]
    ) -> StrategizerGridInstance:
        """Create a grid instance for a predicament."""
        # We need a unit to attach the grid to - use a "virtual" approach
        # by creating a special unit type or using the first source unit
        # For now, create grid with placeholder unit_id (first source unit)

        unit_id = None
        if predicament.source_unit_ids:
            unit_id = predicament.source_unit_ids[0]
        else:
            # Create a placeholder - we'll need to handle this in the schema
            # For now, find any unit in the project
            result = await db.execute(
                select(StrategizerUnit)
                .where(StrategizerUnit.project_id == predicament.project_id)
                .limit(1)
            )
            unit = result.scalar_one_or_none()
            if unit:
                unit_id = unit.id

        if not unit_id:
            raise ValueError("Cannot create grid: no units in project")

        # Initialize slots from spec
        initial_slots = {}
        for slot in grid_spec.get("slots", []):
            initial_slots[slot.get("name", "unnamed")] = {
                "content": slot.get("initial_content", ""),
                "confidence": 0.0,
                "evidence_notes": None
            }

        grid = StrategizerGridInstance(
            unit_id=unit_id,
            grid_type=grid_spec.get("grid_type", "PREDICAMENT_ANALYSIS"),
            tier="wildcard",  # Predicament grids are special
            slots=initial_slots
        )
        db.add(grid)
        await db.flush()

        return grid

    def _parse_json_response(
        self,
        response_text: str,
        fallback: Any
    ) -> Any:
        """Parse JSON response with fallback."""
        try:
            text = response_text.strip()
            # Remove markdown code blocks if present
            if text.startswith("```"):
                lines = text.split("\n")
                start = 1 if lines[0].startswith("```") else 0
                end = len(lines) - 1 if lines[-1].strip() == "```" else len(lines)
                text = "\n".join(lines[start:end])

            return json.loads(text)
        except json.JSONDecodeError:
            return fallback


# =============================================================================
# BACKGROUND AUTO-CHECK HELPER
# =============================================================================

import logging

logger = logging.getLogger(__name__)


async def run_background_coherence_check(project_id: str, trigger_reason: str) -> None:
    """
    Run a coherence check in the background using FastAPI BackgroundTasks.

    This creates a new database session and runs a quick scan.
    Should be called via: background_tasks.add_task(run_background_coherence_check, project_id, reason)

    Args:
        project_id: Project to check
        trigger_reason: What triggered this check (for logging)
    """
    # Import here to avoid circular imports
    from ...database import AsyncSessionLocal

    try:
        logger.info(f"Background coherence check starting for project {project_id} (reason: {trigger_reason})")

        async with AsyncSessionLocal() as db:
            monitor = CoherenceMonitor()
            result = await monitor.quick_coherence_scan(db, project_id)

            if "error" in result:
                logger.warning(f"Background coherence check failed: {result['error']}")
                return

            new_count = result.get("new_detected", 0)
            total_count = result.get("total_found", 0)
            if new_count > 0:
                logger.info(
                    f"Background coherence check found {new_count} new predicaments "
                    f"(total: {total_count}) in project {project_id}"
                )
            else:
                logger.debug(
                    f"Background coherence check completed for project {project_id} - "
                    f"no new predicaments (existing: {total_count})"
                )

    except Exception as e:
        # Log but don't raise - this is a background task
        logger.error(f"Background coherence check error for project {project_id}: {str(e)}")
