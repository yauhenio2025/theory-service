"""
LLM Prompts for Grid Operations

These prompts follow the LLM-First philosophy:
Python gathers context -> LLM makes judgments -> Python executes
"""


GRID_FILL_PROMPT = """You are filling slots in an analytical grid for a strategic unit.

DOMAIN CONTEXT:
Domain: {domain_name}
Core Question: {core_question}

UNIT DETAILS:
Type: {unit_type} (displayed as: {display_type})
Name: {unit_name}
Definition: {unit_definition}
Content: {unit_content}

GRID TO FILL:
Type: {grid_type}
Description: {grid_description}
Slots: {slots_list}

---

Fill each slot with substantive analysis. For each slot, provide:
1. content: A thoughtful analysis (1-3 sentences)
2. confidence: Your confidence in this analysis (0.0-1.0)
3. evidence_notes: Any evidence or reasoning supporting this (optional)

Return ONLY valid JSON:
{{
    "slots": {{
        "slot_name": {{
            "content": "Your analysis here...",
            "confidence": 0.85,
            "evidence_notes": "Optional supporting notes"
        }}
    }}
}}
"""


GRID_COMPATIBILITY_PROMPT = """You are assessing whether an analytical grid is compatible with a strategic unit.

UNIT DETAILS:
Type: {unit_type}
Name: {unit_name}
Definition: {unit_definition}
Content Summary: {unit_content_summary}

GRID TO ASSESS:
Type: {grid_type}
Name: {grid_name}
Description: {grid_description}
Slots: {slots_list}

---

Assess whether this grid would provide valuable analytical structure for this unit.

Consider:
1. Does the grid's analytical lens match the unit's nature?
2. Would filling these slots reveal useful insights?
3. Are there any slots that don't apply to this unit?

Return JSON:
{{
    "compatible": true/false,
    "compatibility_score": 0.0-1.0,
    "rationale": "Why this grid is/isn't a good fit",
    "applicable_slots": ["slot1", "slot2"],
    "inapplicable_slots": ["slot3"],
    "alternative_grids": ["GRID_TYPE"] // if not compatible, suggest better options
}}
"""


GRID_FRICTION_PROMPT = """You are analyzing grids for friction - contradictions, gaps, or tensions that need attention.

DOMAIN CONTEXT:
Domain: {domain_name}
Core Question: {core_question}

UNIT: {unit_name} ({unit_type})

GRIDS ON THIS UNIT:
{grids_json}

---

Analyze these grids for:
1. Cross-slot contradictions (e.g., LOGICAL.claim vs TEMPORAL.trajectory)
2. Information gaps (slots that should be connected but aren't)
3. Uncaptured content (important aspects not fitting any slot)
4. Tensions requiring user decision

Return JSON:
{{
    "friction_events": [
        {{
            "type": "contradiction|gap|uncaptured|tension",
            "description": "What the friction is",
            "slots_involved": ["GRID.slot1", "GRID.slot2"],
            "severity": "low|medium|high",
            "suggested_resolution": "How to address this"
        }}
    ],
    "overall_coherence": 0.0-1.0,
    "summary": "Overall assessment of grid coherence"
}}
"""


GRID_AUTO_APPLY_PROMPT = """You are selecting which analytical grids to apply to a strategic unit.

DOMAIN CONTEXT:
Domain: {domain_name}
Vocabulary: {vocabulary}

UNIT DETAILS:
Type: {unit_type}
Name: {unit_name}
Definition: {unit_definition}
Content: {unit_content}

AVAILABLE GRIDS:
Required (Tier 1): {tier1_grids}
Flexible (Tier 2): {tier2_grids}

EXISTING GRIDS ON THIS UNIT: {existing_grids}

---

Recommend which grids to apply. Required grids should always be included unless already present.
For Flexible grids, only include those that would provide genuine analytical value.

Return JSON:
{{
    "grids_to_apply": [
        {{
            "grid_type": "GRID_TYPE",
            "tier": "required|flexible",
            "rationale": "Why this grid is valuable for this unit",
            "auto_fill": true/false  // Should we auto-fill slots now?
        }}
    ],
    "grids_to_skip": [
        {{
            "grid_type": "GRID_TYPE",
            "reason": "Why this grid doesn't fit"
        }}
    ]
}}
"""
