"""
Grid Type Definitions for Strategizer

Three-tier grid system:
- Tier 1 (REQUIRED): Always applied to units of certain types
- Tier 2 (FLEXIBLE): Applied based on domain/unit type, user can customize
- Tier 3 (WILDCARD): LLM-proposed during work, can be promoted
"""

from typing import Dict, List, Any, Optional


# =============================================================================
# TIER 1: REQUIRED GRIDS
# =============================================================================
# These grids are always applicable to any unit type

TIER_1_GRIDS: Dict[str, Dict[str, Any]] = {
    "LOGICAL": {
        "name": "Logical Structure",
        "description": "Toulmin argument structure - claim, evidence, warrant, counter, rebuttal",
        "slots": [
            {"name": "claim", "description": "The core assertion or thesis"},
            {"name": "evidence", "description": "Supporting data or facts"},
            {"name": "warrant", "description": "The reasoning connecting evidence to claim"},
            {"name": "counter", "description": "Potential objections or counterarguments"},
            {"name": "rebuttal", "description": "Response to counterarguments"},
        ],
        "applicable_to": ["concept", "dialectic", "actor"],
    },
    "ACTOR": {
        "name": "Stakeholder Mapping",
        "description": "Who has agency and interest in this unit",
        "slots": [
            {"name": "proponents", "description": "Who supports or advances this"},
            {"name": "opponents", "description": "Who resists or opposes this"},
            {"name": "regulators", "description": "Who has power to enable/constrain"},
            {"name": "beneficiaries", "description": "Who gains if this succeeds"},
            {"name": "casualties", "description": "Who loses or is harmed"},
        ],
        "applicable_to": ["concept", "dialectic", "actor"],
    },
    "TEMPORAL": {
        "name": "Time Trajectory",
        "description": "How this unit relates to time and change",
        "slots": [
            {"name": "origins", "description": "Where this came from, historical roots"},
            {"name": "current_state", "description": "Present situation and dynamics"},
            {"name": "trajectory", "description": "Where this is heading"},
            {"name": "inflection_points", "description": "Key moments of potential change"},
            {"name": "end_states", "description": "Possible futures or resolutions"},
        ],
        "applicable_to": ["concept", "dialectic", "actor"],
    },
}


# =============================================================================
# TIER 2: FLEXIBLE GRIDS
# =============================================================================
# These grids are suggested based on unit type but can be customized

TIER_2_GRIDS: Dict[str, Dict[str, Any]] = {
    # Concept-specific grids
    "GENEALOGICAL": {
        "name": "Conceptual Genealogy",
        "description": "Intellectual lineage and influences",
        "slots": [
            {"name": "precursors", "description": "Earlier concepts this builds on"},
            {"name": "influences", "description": "Thinkers or traditions that shaped this"},
            {"name": "derivatives", "description": "Concepts derived from this"},
            {"name": "tensions", "description": "Conceptual tensions with other ideas"},
        ],
        "applicable_to": ["concept"],
    },
    "FUNCTIONAL": {
        "name": "Functional Analysis",
        "description": "What this concept does in practice",
        "slots": [
            {"name": "enables", "description": "What this makes possible"},
            {"name": "forecloses", "description": "What this rules out or prevents"},
            {"name": "reveals", "description": "What becomes visible through this lens"},
            {"name": "obscures", "description": "What gets hidden or ignored"},
        ],
        "applicable_to": ["concept"],
    },

    # Dialectic-specific grids
    "SYNTHESIS": {
        "name": "Dialectical Synthesis",
        "description": "Ways to navigate the tension",
        "slots": [
            {"name": "thesis_strengths", "description": "What pole A gets right"},
            {"name": "antithesis_strengths", "description": "What pole B gets right"},
            {"name": "synthesis_paths", "description": "Ways to transcend the opposition"},
            {"name": "productive_tension", "description": "Why maintaining tension may be valuable"},
        ],
        "applicable_to": ["dialectic"],
    },
    "CONTEXTUAL": {
        "name": "Contextual Navigation",
        "description": "When to favor each pole",
        "slots": [
            {"name": "favor_a_when", "description": "Conditions that favor pole A"},
            {"name": "favor_b_when", "description": "Conditions that favor pole B"},
            {"name": "balance_when", "description": "Conditions requiring balance"},
            {"name": "warning_signs", "description": "Signs of overcommitment to either pole"},
        ],
        "applicable_to": ["dialectic"],
    },

    # Actor-specific grids
    "INFLUENCE": {
        "name": "Influence Network",
        "description": "How this actor exerts and receives influence",
        "slots": [
            {"name": "power_sources", "description": "Where their power comes from"},
            {"name": "influence_mechanisms", "description": "How they exert influence"},
            {"name": "dependencies", "description": "What they depend on"},
            {"name": "vulnerabilities", "description": "Where they can be influenced"},
        ],
        "applicable_to": ["actor"],
    },
    "COALITION": {
        "name": "Coalition Dynamics",
        "description": "Alliance and opposition patterns",
        "slots": [
            {"name": "allies", "description": "Natural allies and why"},
            {"name": "rivals", "description": "Natural opponents and why"},
            {"name": "swing_actors", "description": "Actors who could go either way"},
            {"name": "coalition_triggers", "description": "What could shift alliances"},
        ],
        "applicable_to": ["actor"],
    },
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_grid_definition(grid_type: str) -> Optional[Dict[str, Any]]:
    """Get the full definition for a grid type."""
    if grid_type in TIER_1_GRIDS:
        return {**TIER_1_GRIDS[grid_type], "tier": "required"}
    if grid_type in TIER_2_GRIDS:
        return {**TIER_2_GRIDS[grid_type], "tier": "flexible"}
    return None


def get_applicable_grids(unit_type: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get grids applicable to a unit type, organized by tier.

    Returns:
        {
            "required": [list of tier 1 grids],
            "flexible": [list of tier 2 grids],
        }
    """
    result = {"required": [], "flexible": []}

    for grid_name, grid_def in TIER_1_GRIDS.items():
        if unit_type in grid_def.get("applicable_to", []):
            result["required"].append({
                "grid_type": grid_name,
                **grid_def,
            })

    for grid_name, grid_def in TIER_2_GRIDS.items():
        if unit_type in grid_def.get("applicable_to", []):
            result["flexible"].append({
                "grid_type": grid_name,
                **grid_def,
            })

    return result


def get_all_grid_types() -> List[str]:
    """Get all defined grid type names."""
    return list(TIER_1_GRIDS.keys()) + list(TIER_2_GRIDS.keys())


def get_slot_names(grid_type: str) -> List[str]:
    """Get slot names for a grid type."""
    grid_def = get_grid_definition(grid_type)
    if grid_def:
        return [slot["name"] for slot in grid_def.get("slots", [])]
    return []
