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
    # Dynamic cell action prompts (new approach)
    GENERATE_CELL_ACTIONS_PROMPT,
    EXECUTE_DYNAMIC_ACTION_PROMPT,
    # Legacy cell action prompts (kept for reference)
    CELL_ACTION_CONTEXT,
    CELL_ACTION_WHAT_WOULD_IT_TAKE,
    CELL_ACTION_DEEP_ANALYSIS,
    CELL_ACTION_GENERATE_ARGUMENTS,
    CELL_ACTION_SCENARIO_EXPLORATION,
    CELL_ACTION_SURFACE_ASSUMPTIONS,
    CELL_ACTION_FIND_CONNECTIONS,
    CELL_ACTION_COALITION_DESIGN,
    CELL_ACTION_PRIORITIZE,
    CELL_ACTION_SYNTHESIZE_CONCEPT,
    CELL_ACTION_DRAFT_CONTENT,
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
        predicament_id: str,
        refinement: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a custom analytical grid for resolving a predicament.

        The grid is tailored to the predicament type:
        - THEORETICAL: Focus on assumptions, implications, synthesis
        - EMPIRICAL: Focus on evidence, explanatory gaps, theory modifications
        - CONCEPTUAL: Focus on distinctions, edge cases, alternative framings
        - PRAXIS: Focus on decision criteria, action options, trade-offs

        Args:
            refinement: Optional dict with dimension refinement instructions:
                - row_refinement: How to adjust rows (more_granular, broader, axis_*, etc.)
                - row_custom: Custom description for rows
                - col_refinement: How to adjust columns
                - col_custom: Custom description for columns
                - custom_instruction: Free-form guidance for the LLM

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

        # Build refinement instruction if provided
        refinement_instruction = ""
        if refinement:
            refinement_parts = []

            # Row refinement
            row_ref = refinement.get("row_refinement")
            row_custom = refinement.get("row_custom")
            if row_ref:
                row_map = {
                    "more_granular": "Make the rows MORE GRANULAR - split existing categories into more specific sub-categories",
                    "broader": "Make the rows BROADER - aggregate into fewer, more general categories",
                    "axis_actors": "Use ACTORS/STAKEHOLDERS as rows (key players, institutions, groups)",
                    "axis_assumptions": "Use KEY ASSUMPTIONS as rows (underlying beliefs, premises, axioms)",
                    "axis_evidence": "Use EVIDENCE TYPES as rows (empirical data, case studies, theoretical support)",
                    "axis_temporal": "Use TEMPORAL PHASES as rows (past, present, future; or stages of development)",
                    "axis_mechanisms": "Use CAUSAL MECHANISMS as rows (how things work, pathways of influence)",
                    "axis_scenarios": "Use SCENARIOS/FUTURES as rows (possible outcomes, alternative trajectories)",
                    "add_row": f"ADD SPECIFIC ROW: {row_custom}" if row_custom else "Add a new specific row",
                    "custom_row": f"CUSTOM ROW STRUCTURE: {row_custom}" if row_custom else "Use custom row structure"
                }
                refinement_parts.append(f"ROWS: {row_map.get(row_ref, row_ref)}")

            # Column refinement
            col_ref = refinement.get("col_refinement")
            col_custom = refinement.get("col_custom")
            if col_ref:
                col_map = {
                    "more_granular": "Make the columns MORE GRANULAR - split into finer-grained dimensions",
                    "broader": "Make the columns BROADER - aggregate into fewer, more general dimensions",
                    "axis_capabilities": "Use CAPABILITY DIMENSIONS as columns (what entities can do)",
                    "axis_poles": "Use POLE SUPPORT as columns (how well each pole is supported)",
                    "axis_impact": "Use IMPACT AREAS as columns (different domains of effect)",
                    "axis_feasibility": "Use FEASIBILITY FACTORS as columns (technical, political, economic, etc.)",
                    "axis_resources": "Use RESOURCE TYPES as columns (material, informational, social, etc.)",
                    "axis_leverage": "Use LEVERAGE POINTS as columns (where intervention is possible)",
                    "add_col": f"ADD SPECIFIC COLUMN: {col_custom}" if col_custom else "Add a new specific column",
                    "custom_col": f"CUSTOM COLUMN STRUCTURE: {col_custom}" if col_custom else "Use custom column structure"
                }
                refinement_parts.append(f"COLUMNS: {col_map.get(col_ref, col_ref)}")

            # Custom instruction
            custom_inst = refinement.get("custom_instruction")
            if custom_inst:
                refinement_parts.append(f"CUSTOM GUIDANCE: {custom_inst}")

            if refinement_parts:
                refinement_instruction = "\n\n---\n\nUSER REFINEMENT INSTRUCTIONS:\n" + "\n".join(refinement_parts) + "\n\nApply these refinements while maintaining analytical rigor and ensuring the matrix reveals meaningful patterns."

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

        # Append refinement instructions if provided
        if refinement_instruction:
            prompt = prompt + refinement_instruction

        # Generate grid (Sonnet is fine for this)
        response = self.client.messages.create(
            model=self.sonnet_model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = response.content[0].text
        grid_spec = self._parse_json_response(response_text, {
            "grid_type": "PREDICAMENT_MATRIX",
            "grid_name": f"Analysis Matrix for: {predicament.title}",
            "grid_description": "Failed to generate matrix",
            "matrix": {
                "row_header": "Entity",
                "column_header": "Dimension",
                "rows": [],
                "columns": [],
                "cells": []
            },
            "key_patterns": [],
            "resolution_implications": "Unable to determine"
        })

        # Create grid instance in database (stores matrix data)
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
    # CELL ACTIONS
    # =========================================================================

    async def execute_cell_action(
        self,
        db: AsyncSession,
        predicament: StrategizerPredicament,
        action_type: str,
        cells: List[Dict[str, Any]],
        custom_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute a strategic action on selected matrix cells.

        Uses Opus 4.5 with extended thinking for deep analysis.

        Args:
            db: Database session
            predicament: The predicament containing the matrix
            action_type: One of the cell action types
            cells: List of cell info dicts with row_id, col_id, labels, rating, content
            custom_context: Optional additional context from user

        Returns:
            Dict with result and optional thinking summary
        """
        # Map action types to prompts
        prompt_map = {
            "what_would_it_take": CELL_ACTION_WHAT_WOULD_IT_TAKE,
            "deep_analysis": CELL_ACTION_DEEP_ANALYSIS,
            "generate_arguments": CELL_ACTION_GENERATE_ARGUMENTS,
            "scenario_exploration": CELL_ACTION_SCENARIO_EXPLORATION,
            "surface_assumptions": CELL_ACTION_SURFACE_ASSUMPTIONS,
            "find_connections": CELL_ACTION_FIND_CONNECTIONS,
            "coalition_design": CELL_ACTION_COALITION_DESIGN,
            "prioritize": CELL_ACTION_PRIORITIZE,
            "synthesize_concept": CELL_ACTION_SYNTHESIZE_CONCEPT,
            "draft_content": CELL_ACTION_DRAFT_CONTENT,
        }

        if action_type not in prompt_map:
            return {"error": f"Unknown action type: {action_type}"}

        # Get domain info from project
        domain_result = await db.execute(
            select(StrategizerDomain).where(
                StrategizerDomain.project_id == predicament.project_id
            )
        )
        domain = domain_result.scalar_one_or_none()
        domain_name = domain.name if domain else "Strategic Analysis"
        core_question = domain.core_question if domain else "How should we approach this situation?"

        # Get matrix data from predicament grid
        row_header = "Rows"
        col_header = "Columns"
        matrix_summary = "Matrix not available"

        if predicament.generated_grid and predicament.generated_grid.slots:
            stored_data = predicament.generated_grid.slots
            if "_matrix" in stored_data:
                matrix_data = stored_data["_matrix"]
                row_header = matrix_data.get('row_header', 'Rows')
                col_header = matrix_data.get('column_header', 'Columns')

                # Build matrix summary
                rows = matrix_data.get('rows', [])
                cols = matrix_data.get('columns', [])
                matrix_cells = matrix_data.get('cells', [])  # List of cell dicts

                # Build cell lookup for faster access
                cells_lookup = {}
                for cell in matrix_cells:
                    key = f"{cell.get('row_id', '')}_{cell.get('col_id', '')}"
                    cells_lookup[key] = cell

                summary_lines = []
                for row in rows:
                    row_id = row.get('id', '')
                    row_label = row.get('label', '')
                    for col in cols:
                        col_id = col.get('id', '')
                        col_label = col.get('label', '')
                        cell_key = f"{row_id}_{col_id}"
                        cell = cells_lookup.get(cell_key, {})
                        rating = cell.get('rating', 'empty')
                        summary_lines.append(f"- {row_label} × {col_label}: {rating}")
                matrix_summary = "\n".join(summary_lines) if summary_lines else "No matrix cells"

        # Format selected cells detail
        selected_cells_detail = self._format_cells_for_prompt(cells)

        # Build the context using the template
        context = CELL_ACTION_CONTEXT.format(
            domain_name=domain_name,
            core_question=core_question,
            predicament_title=predicament.title,
            predicament_type=predicament.predicament_type.value if predicament.predicament_type else "theoretical",
            predicament_description=predicament.description,
            row_header=row_header,
            col_header=col_header,
            selected_cells_detail=selected_cells_detail,
            matrix_summary=matrix_summary
        )

        # Get the action-specific prompt template
        action_prompt_template = prompt_map[action_type]

        # For single cell actions, use first cell's info; for multi-cell, use summary
        if len(cells) == 1:
            cell = cells[0]
            row_label = cell.get('row_label', 'Unknown')
            col_label = cell.get('col_label', 'Unknown')
            rating = cell.get('rating', 'unknown')
        else:
            # For multi-cell actions, use combined labels
            row_labels = list(set(c.get('row_label', 'Unknown') for c in cells))
            col_labels = list(set(c.get('col_label', 'Unknown') for c in cells))
            row_label = ", ".join(row_labels)
            col_label = ", ".join(col_labels)
            rating = "multiple"

        # Format the action prompt with both context and cell-specific info
        try:
            full_prompt = action_prompt_template.format(
                context=context,
                row_label=row_label,
                col_label=col_label,
                rating=rating
            )
        except KeyError as e:
            # Some prompts may not use all variables - use safe formatting
            full_prompt = action_prompt_template.replace("{context}", context)
            full_prompt = full_prompt.replace("{row_label}", row_label)
            full_prompt = full_prompt.replace("{col_label}", col_label)
            full_prompt = full_prompt.replace("{rating}", rating)

        # Use streaming for extended thinking (may take a while)
        try:
            thinking_content = ""
            text_content = ""

            with self.client.messages.stream(
                model=self.opus_model,
                max_tokens=16000,
                thinking={
                    "type": "enabled",
                    "budget_tokens": 8000  # Generous thinking for strategic analysis
                },
                messages=[{"role": "user", "content": full_prompt}]
            ) as stream:
                for event in stream:
                    if hasattr(event, 'type'):
                        if event.type == 'content_block_delta':
                            if hasattr(event, 'delta'):
                                if hasattr(event.delta, 'thinking'):
                                    thinking_content += event.delta.thinking
                                elif hasattr(event.delta, 'text'):
                                    text_content += event.delta.text

            # Parse the JSON result from text content
            result = self._parse_json_response(text_content, {"raw_response": text_content})

            # Summarize thinking (first 500 chars)
            thinking_summary = None
            if thinking_content:
                thinking_summary = thinking_content[:500]
                if len(thinking_content) > 500:
                    thinking_summary += "..."

            return {
                "result": result,
                "thinking_summary": thinking_summary
            }

        except Exception as e:
            return {"error": f"LLM call failed: {str(e)}"}

    def _format_cells_for_prompt(self, cells: List[Dict[str, Any]]) -> str:
        """Format cell data for inclusion in prompt."""
        lines = []
        for i, cell in enumerate(cells, 1):
            rating_emoji = {
                "strong": "🟢",
                "moderate": "🔵",
                "weak": "🟡",
                "empty": "🔴"
            }.get(cell.get("rating", ""), "⚪")

            lines.append(f"""
Cell {i}: {cell.get('row_label', 'Unknown')} × {cell.get('col_label', 'Unknown')}
Rating: {rating_emoji} {cell.get('rating', 'unknown')}
Content: {cell.get('content', 'No analysis provided')}
""")
        return "\n".join(lines)

    # =========================================================================
    # DYNAMIC CELL ACTIONS - Context-specific action generation
    # =========================================================================

    async def generate_cell_actions(
        self,
        db: AsyncSession,
        predicament: StrategizerPredicament,
        cells: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate context-specific actions for selected matrix cells.

        Instead of fixed generic actions, generates meaningful actions
        tailored to the predicament and selected cells.

        Uses Sonnet for fast generation.

        Returns:
            Dict with list of generated actions
        """
        # Get domain info
        domain_result = await db.execute(
            select(StrategizerDomain).where(
                StrategizerDomain.project_id == predicament.project_id
            )
        )
        domain = domain_result.scalar_one_or_none()
        domain_name = domain.name if domain else "Strategic Analysis"
        core_question = domain.core_question if domain else "How should we approach this?"

        # Get matrix data
        row_header = "Rows"
        col_header = "Columns"
        matrix_summary = "Matrix not available"

        if predicament.generated_grid and predicament.generated_grid.slots:
            stored_data = predicament.generated_grid.slots
            if "_matrix" in stored_data:
                matrix_data = stored_data["_matrix"]
                row_header = matrix_data.get('row_header', 'Rows')
                col_header = matrix_data.get('column_header', 'Columns')

                rows = matrix_data.get('rows', [])
                cols = matrix_data.get('columns', [])
                matrix_cells = matrix_data.get('cells', [])

                cells_lookup = {f"{c.get('row_id', '')}_{c.get('col_id', '')}": c for c in matrix_cells}

                summary_lines = []
                for row in rows:
                    row_id = row.get('id', '')
                    row_label = row.get('label', '')
                    for col in cols:
                        col_id = col.get('id', '')
                        col_label = col.get('label', '')
                        cell = cells_lookup.get(f"{row_id}_{col_id}", {})
                        rating = cell.get('rating', 'empty')
                        summary_lines.append(f"- {row_label} × {col_label}: {rating}")
                matrix_summary = "\n".join(summary_lines)

        # Format selected cells
        selected_cells_detail = self._format_cells_for_prompt(cells)

        # Build prompt
        prompt = GENERATE_CELL_ACTIONS_PROMPT.format(
            domain_name=domain_name,
            core_question=core_question,
            predicament_title=predicament.title,
            predicament_type=predicament.predicament_type.value if predicament.predicament_type else "theoretical",
            predicament_description=predicament.description,
            pole_a=predicament.pole_a or "",
            pole_b=predicament.pole_b or "",
            row_header=row_header,
            col_header=col_header,
            selected_cells_detail=selected_cells_detail,
            matrix_summary=matrix_summary
        )

        try:
            # Use Sonnet for fast action generation
            response = self.client.messages.create(
                model=self.sonnet_model,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text
            actions = self._parse_json_response(response_text, [])

            # Validate and normalize actions
            normalized_actions = []
            for i, action in enumerate(actions):
                if isinstance(action, dict):
                    normalized_actions.append({
                        "id": action.get("id", f"action_{i}"),
                        "label": action.get("label", "Analyze"),
                        "description": action.get("description", ""),
                        "icon": action.get("icon", "lightbulb"),
                        "output_type": action.get("output_type", "analysis")
                    })

            return {"actions": normalized_actions}

        except Exception as e:
            return {"error": f"Failed to generate actions: {str(e)}"}

    async def execute_dynamic_action(
        self,
        db: AsyncSession,
        predicament: StrategizerPredicament,
        cells: List[Dict[str, Any]],
        action: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a dynamically generated action on selected cells.

        Uses Opus 4.5 with extended thinking for deep analysis.

        Args:
            predicament: The predicament context
            cells: Selected cells
            action: The action to execute (from generate_cell_actions)

        Returns:
            Dict with result and optional thinking summary
        """
        # Get domain info
        domain_result = await db.execute(
            select(StrategizerDomain).where(
                StrategizerDomain.project_id == predicament.project_id
            )
        )
        domain = domain_result.scalar_one_or_none()
        domain_name = domain.name if domain else "Strategic Analysis"
        core_question = domain.core_question if domain else "How should we approach this?"

        # Get matrix data
        row_header = "Rows"
        col_header = "Columns"
        matrix_summary = "Matrix not available"

        if predicament.generated_grid and predicament.generated_grid.slots:
            stored_data = predicament.generated_grid.slots
            if "_matrix" in stored_data:
                matrix_data = stored_data["_matrix"]
                row_header = matrix_data.get('row_header', 'Rows')
                col_header = matrix_data.get('column_header', 'Columns')

                rows = matrix_data.get('rows', [])
                cols = matrix_data.get('columns', [])
                matrix_cells = matrix_data.get('cells', [])

                cells_lookup = {f"{c.get('row_id', '')}_{c.get('col_id', '')}": c for c in matrix_cells}

                summary_lines = []
                for row in rows:
                    row_id = row.get('id', '')
                    row_label = row.get('label', '')
                    for col in cols:
                        col_id = col.get('id', '')
                        col_label = col.get('label', '')
                        cell = cells_lookup.get(f"{row_id}_{col_id}", {})
                        rating = cell.get('rating', 'empty')
                        summary_lines.append(f"- {row_label} × {col_label}: {rating}")
                matrix_summary = "\n".join(summary_lines)

        # Format selected cells
        selected_cells_detail = self._format_cells_for_prompt(cells)

        # Build prompt
        prompt = EXECUTE_DYNAMIC_ACTION_PROMPT.format(
            domain_name=domain_name,
            core_question=core_question,
            predicament_title=predicament.title,
            predicament_type=predicament.predicament_type.value if predicament.predicament_type else "theoretical",
            predicament_description=predicament.description,
            pole_a=predicament.pole_a or "",
            pole_b=predicament.pole_b or "",
            row_header=row_header,
            col_header=col_header,
            selected_cells_detail=selected_cells_detail,
            matrix_summary=matrix_summary,
            action_label=action.get("label", "Analyze"),
            action_description=action.get("description", ""),
            output_type=action.get("output_type", "analysis")
        )

        try:
            thinking_content = ""
            text_content = ""

            # Use Opus 4.5 with extended thinking
            with self.client.messages.stream(
                model=self.opus_model,
                max_tokens=16000,
                thinking={
                    "type": "enabled",
                    "budget_tokens": 8000
                },
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                for event in stream:
                    if hasattr(event, 'type'):
                        if event.type == 'content_block_delta':
                            if hasattr(event, 'delta'):
                                if hasattr(event.delta, 'thinking'):
                                    thinking_content += event.delta.thinking
                                elif hasattr(event.delta, 'text'):
                                    text_content += event.delta.text

            result = self._parse_json_response(text_content, {"raw_response": text_content})

            thinking_summary = None
            if thinking_content:
                thinking_summary = thinking_content[:500]
                if len(thinking_content) > 500:
                    thinking_summary += "..."

            return {
                "result": result,
                "thinking_summary": thinking_summary,
                "action_executed": action
            }

        except Exception as e:
            return {"error": f"Action execution failed: {str(e)}"}

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

        # Store entire grid spec including matrix data
        grid_data = {
            "_metadata": {
                "grid_name": grid_spec.get("grid_name", f"Analysis Matrix for: {predicament.title}"),
                "grid_description": grid_spec.get("grid_description", ""),
                "key_patterns": grid_spec.get("key_patterns", []),
                "resolution_implications": grid_spec.get("resolution_implications", ""),
                "overall_row": grid_spec.get("overall_row", {})
            },
            "_matrix": grid_spec.get("matrix", {
                "row_header": "Entity",
                "column_header": "Dimension",
                "rows": [],
                "columns": [],
                "cells": []
            })
        }

        # Also store legacy slot format for backwards compatibility
        for slot in grid_spec.get("slots", []):
            grid_data[slot.get("name", "unnamed")] = {
                "content": slot.get("initial_content", ""),
                "description": slot.get("description", ""),
                "confidence": 0.0,
                "evidence_notes": None
            }

        initial_slots = grid_data

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
