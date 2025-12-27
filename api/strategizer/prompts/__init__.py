"""
Strategizer LLM Prompts Module
"""

from .grid_prompts import (
    GRID_FILL_PROMPT,
    GRID_FRICTION_PROMPT,
    GRID_COMPATIBILITY_PROMPT,
    GRID_AUTO_APPLY_PROMPT,
)

from .evidence_prompts import (
    EVIDENCE_EXTRACTION_PROMPT,
    EVIDENCE_ANALYSIS_PROMPT,
    INTERPRETATION_GENERATION_PROMPT,
    COMMITMENT_FORECLOSURE_PROMPT,
    format_units_for_prompt,
    format_grid_slots_for_prompt,
)

__all__ = [
    # Grid prompts
    "GRID_FILL_PROMPT",
    "GRID_FRICTION_PROMPT",
    "GRID_COMPATIBILITY_PROMPT",
    "GRID_AUTO_APPLY_PROMPT",
    # Evidence prompts
    "EVIDENCE_EXTRACTION_PROMPT",
    "EVIDENCE_ANALYSIS_PROMPT",
    "INTERPRETATION_GENERATION_PROMPT",
    "COMMITMENT_FORECLOSURE_PROMPT",
    "format_units_for_prompt",
    "format_grid_slots_for_prompt",
]
