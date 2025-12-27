"""
Strategizer Evidence LLM Prompts

Prompts for evidence extraction, analysis, and interpretation generation.
Following the LLM-first philosophy: Python gathers → LLM judges → Python executes.
"""


EVIDENCE_EXTRACTION_PROMPT = """You are analyzing a document to extract strategic insights for a strategic project.

## Project Context

**Domain:** {domain_name}
**Core Question:** {core_question}

**Existing Strategic Units:**
{units_summary}

## Source Document

**Source:** {source_name}
**Type:** {source_type}

**Content:**
{source_content}

## Your Task

Extract 3-10 strategic insights from this document that are relevant to the project's core question and existing units.

For each insight, identify:
1. The key claim or insight (verbatim or paraphrased)
2. Where in the document it appears
3. Which unit type it most likely relates to (concept/dialectic/actor)
4. Why this insight matters for the strategic project

Return JSON:
```json
{{
  "fragments": [
    {{
      "content": "The extracted insight or claim",
      "source_location": "Page 3, paragraph 2",
      "likely_unit_type": "concept",
      "likely_unit_name": "Name of related unit if obvious, or null",
      "extraction_note": "Why this is strategically relevant"
    }}
  ],
  "extraction_summary": "Brief summary of what was found"
}}
```

Focus on insights that:
- Challenge or support existing strategic units
- Reveal new strategic considerations
- Highlight tensions, trade-offs, or opportunities
- Identify key actors or forces

Only extract genuinely strategic content. Skip purely descriptive or tangential information.
"""


EVIDENCE_ANALYSIS_PROMPT = """You are analyzing how an evidence fragment relates to an existing strategic unit.

## Project Context

**Domain:** {domain_name}
**Core Question:** {core_question}

## Target Unit

**Type:** {unit_type}
**Name:** {unit_name}
**Definition:** {unit_definition}

**Current Grids:**
{grid_slots}

## Evidence Fragment

**Source:** {source_name}
**Content:** "{fragment_content}"

## Your Task

Analyze how this evidence fragment relates to the target unit and its grid slots.

Consider:
1. Does this evidence support existing slot content?
2. Does it contradict something in the slots?
3. Does it extend/nuance existing understanding?
4. Does it reveal a gap in current grid coverage?
5. Is it genuinely relevant to this unit, or should it go elsewhere?

Return JSON:
```json
{{
  "relationship_type": "supports|contradicts|extends|qualifies|new_insight",
  "target_grid_slot": "GRID_TYPE.slot_name (e.g., LOGICAL.premise) or null",
  "confidence": 0.85,
  "is_ambiguous": false,
  "why_needs_decision": "Explanation if ambiguous",
  "integration_suggestion": "How to update the slot (if high confidence)",
  "alternative_slots": ["Other slots this might fit", "if ambiguous"]
}}
```

Confidence thresholds:
- 0.85+: Auto-integrate (clear relationship)
- 0.60-0.84: Needs confirmation
- <0.60: Generate interpretations

Be conservative. Strategic knowledge requires careful validation.
"""


INTERPRETATION_GENERATION_PROMPT = """You are generating interpretation options for an ambiguous evidence fragment.

## Project Context

**Domain:** {domain_name}
**Core Question:** {core_question}

## Target Unit

**Type:** {unit_type}
**Name:** {unit_name}
**Definition:** {unit_definition}

**Current Grids:**
{grid_slots}

## Ambiguous Fragment

**Source:** {source_name}
**Content:** "{fragment_content}"
**Why Ambiguous:** {why_ambiguous}

## Your Task

Generate 2-4 distinct interpretations of how this evidence could be integrated.

Each interpretation should represent a genuinely different reading or strategic choice.
These are not just different phrasings—they represent different commitments.

Return JSON:
```json
{{
  "interpretations": [
    {{
      "key": "a",
      "title": "Short title for this interpretation",
      "strategy": "How this would be integrated",
      "rationale": "Why someone might choose this reading",
      "relationship_type": "supports|contradicts|extends|qualifies|new_insight",
      "target_grid_slot": "GRID_TYPE.slot_name",
      "is_recommended": true,
      "recommendation_rationale": "Why this is recommended (if applicable)"
    }}
  ],
  "decision_context": "What the user should consider when choosing"
}}
```

Make each interpretation meaningfully different:
- Different target slots
- Different relationship types
- Different strategic implications

Mark exactly one as recommended if there's a clear best choice.
"""


COMMITMENT_FORECLOSURE_PROMPT = """You are analyzing what strategic commitments and foreclosures come with accepting an interpretation.

## Interpretation Being Analyzed

**Title:** {interpretation_title}
**Strategy:** {interpretation_strategy}
**Target Slot:** {target_slot}
**Relationship:** {relationship_type}

## Unit Context

**Unit:** {unit_name}
**Current Slot Content:** {current_slot_content}

## Your Task

Articulate:
1. What accepting this interpretation commits the strategist to
2. What alternatives or options this forecloses

Return JSON:
```json
{{
  "commitment_statement": "By accepting this interpretation, you are committing to...",
  "foreclosure_statements": [
    "This forecloses the possibility of...",
    "You can no longer easily claim that..."
  ],
  "risk_level": "low|medium|high",
  "reversibility": "How hard it would be to undo this choice"
}}
```

Be concrete and specific. Help the user understand the stakes.
"""


def format_units_for_prompt(units: list) -> str:
    """Format units for inclusion in prompts."""
    if not units:
        return "No units defined yet."

    lines = []
    for unit in units:
        unit_type = unit.get("unit_type", "unknown")
        name = unit.get("name", "Unnamed")
        definition = unit.get("definition", "")[:100]
        lines.append(f"- [{unit_type.upper()}] {name}: {definition}...")

    return "\n".join(lines)


def format_grid_slots_for_prompt(grids: list) -> str:
    """Format grid slots for inclusion in prompts."""
    if not grids:
        return "No grids applied yet."

    lines = []
    for grid in grids:
        grid_type = grid.get("grid_type", "UNKNOWN")
        slots = grid.get("slots", {})
        lines.append(f"\n**{grid_type} Grid:**")
        for slot_name, slot_data in slots.items():
            content = slot_data.get("content", "")[:100] if isinstance(slot_data, dict) else str(slot_data)[:100]
            confidence = slot_data.get("confidence", 0) if isinstance(slot_data, dict) else 0
            lines.append(f"  - {slot_name}: {content}... (confidence: {confidence:.1%})")

    return "\n".join(lines) if lines else "No grid slots filled."
