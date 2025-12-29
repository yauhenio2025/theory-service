"""
Coherence Monitor Prompts

Prompts for detecting predicaments (tensions, gaps, inconsistencies) in
theoretical frameworks and generating analytical grids to resolve them.
"""

# =============================================================================
# QUICK COHERENCE SCAN (Sonnet, minimal thinking)
# =============================================================================

QUICK_SCAN_PROMPT = """You are a theoretical coherence analyst. Quickly scan this framework for obvious tensions, gaps, or inconsistencies.

DOMAIN: {domain_name}
CORE QUESTION: {core_question}

UNITS IN FRAMEWORK:
{units_summary}

EVIDENCE FRAGMENTS (that may surface tensions):
{evidence_summary}

---

Identify any obvious predicaments in this framework. A predicament is:
- THEORETICAL: Unresolved tension between concepts/assumptions
- EMPIRICAL: Evidence that the theory can't explain
- CONCEPTUAL: A concept that doesn't carve reality well
- PRAXIS: Theory that can't guide action

Return a JSON array of predicaments found (return empty array if none):

```json
[
  {{
    "title": "Short title for the predicament",
    "description": "Full description of the issue",
    "predicament_type": "theoretical|empirical|conceptual|praxis",
    "severity": "low|medium|high|critical",
    "pole_a": "First side of the tension (for theoretical predicaments)",
    "pole_b": "Second side of the tension (for theoretical predicaments)",
    "source_unit_names": ["List of unit names involved"],
    "suggested_resolution": "Brief suggestion for how to resolve"
  }}
]
```

Return ONLY valid JSON array."""


# =============================================================================
# DEEP COHERENCE ANALYSIS (Opus 4.5, extended thinking)
# =============================================================================

DEEP_ANALYSIS_PROMPT = """You are a theoretical coherence analyst conducting a deep analysis of this framework. Use careful reasoning to identify all tensions, gaps, and inconsistencies.

DOMAIN: {domain_name}
CORE QUESTION: {core_question}
SUCCESS LOOKS LIKE: {success_criteria}

VOCABULARY:
{vocabulary}

---

CONCEPTS ({concept_count}):
{concepts_detail}

---

DIALECTICS ({dialectic_count}):
{dialectics_detail}

---

ACTORS ({actor_count}):
{actors_detail}

---

GRID CONTENT (showing analytical depth):
{grids_summary}

---

EVIDENCE FRAGMENTS AND THEIR ANALYSIS STATUS:
{evidence_detail}

---

TASK: Conduct a comprehensive coherence analysis of this framework.

Think deeply about:
1. Do the concepts form a coherent whole, or do they pull in different directions?
2. Are there implicit assumptions that conflict with each other?
3. Does the evidence support the theoretical apparatus, or does some evidence resist integration?
4. Can this framework guide practical action, or is it purely descriptive?
5. Are there important distinctions the framework fails to make?
6. Are there cross-references between units that reveal hidden tensions?

Return a JSON object with your analysis:

```json
{{
  "overall_coherence": 0.0-1.0,
  "coherence_assessment": "Narrative assessment of framework coherence",
  "predicaments": [
    {{
      "title": "Short title",
      "description": "Full description",
      "predicament_type": "theoretical|empirical|conceptual|praxis",
      "severity": "low|medium|high|critical",
      "pole_a": "First side (if theoretical tension)",
      "pole_b": "Second side (if theoretical tension)",
      "source_unit_names": ["Units involved"],
      "source_evidence_locations": ["Evidence that revealed this"],
      "why_this_matters": "Why resolving this is important",
      "suggested_resolution_approach": "How this might be resolved",
      "would_require_new_concept": true/false,
      "recommended_grid_type": "LOGICAL|ACTOR|TEMPORAL|CAUSAL|etc. for analysis"
    }}
  ],
  "missing_concepts": [
    {{
      "suggested_name": "Name for missing concept",
      "why_needed": "Why the framework needs this",
      "where_gap_appears": "Where the absence is felt"
    }}
  ],
  "framework_strengths": ["What the framework does well"],
  "priority_issues": ["Top 3 issues to address first"]
}}
```

Return ONLY valid JSON."""


# =============================================================================
# PREDICAMENT GRID GENERATION
# =============================================================================

PREDICAMENT_GRID_PROMPT = """You are a theoretical framework architect. Generate an analytical MATRIX to help resolve this predicament.

DOMAIN: {domain_name}
CORE QUESTION: {core_question}

PREDICAMENT TO ANALYZE:
Title: {predicament_title}
Type: {predicament_type}
Description: {predicament_description}

Pole A: {pole_a}
Pole B: {pole_b}

SOURCE UNITS INVOLVED:
{source_units_detail}

SOURCE EVIDENCE:
{source_evidence_detail}

---

Create an analytical MATRIX (not just text slots) to schematically represent the complexity of this predicament.

Choose a matrix structure appropriate to the predicament type:

- For THEORETICAL predicaments: Rows = key assumptions, Columns = implications for each pole
- For EMPIRICAL predicaments: Rows = types of evidence, Columns = how well each pole explains it
- For CONCEPTUAL predicaments: Rows = dimensions/aspects, Columns = how each framing handles them
- For PRAXIS predicaments: Rows = key actors/stakeholders, Columns = capabilities/constraints/actions

The matrix should reveal patterns, gaps, and asymmetries at a glance using a rating system:
- "strong" = green (well-supported/high capability)
- "moderate" = blue (partial support/medium capability)
- "weak" = yellow (limited support/low capability)
- "empty" = red (no support/no capability/blocked)

Return a JSON object:

```json
{{
  "grid_type": "PREDICAMENT_MATRIX",
  "grid_name": "Name for this analytical matrix",
  "grid_description": "What patterns this matrix reveals",
  "matrix": {{
    "row_header": "What rows represent (e.g., 'Actor', 'Evidence Type', 'Assumption')",
    "column_header": "What columns represent (e.g., 'Capability Dimension', 'Pole Support', 'Aspect')",
    "rows": [
      {{
        "id": "row_1",
        "label": "Row label",
        "description": "What this row represents"
      }}
    ],
    "columns": [
      {{
        "id": "col_1",
        "label": "Column label",
        "description": "What this column measures"
      }}
    ],
    "cells": [
      {{
        "row_id": "row_1",
        "col_id": "col_1",
        "rating": "strong|moderate|weak|empty",
        "content": "Brief explanation (1-2 sentences max)",
        "evidence_note": "What evidence supports this rating"
      }}
    ]
  }},
  "overall_row": {{
    "label": "OVERALL",
    "aggregation": "Summary row showing aggregate patterns across all rows"
  }},
  "key_patterns": [
    "Pattern 1 revealed by the matrix",
    "Pattern 2 revealed by the matrix"
  ],
  "resolution_implications": "What the matrix suggests about resolution paths"
}}
```

IMPORTANT: The matrix should have 4-6 rows and 4-6 columns. Each cell MUST have a rating and brief content.

Return ONLY valid JSON."""


# =============================================================================
# RESOLUTION TO DIALECTIC
# =============================================================================

RESOLUTION_PROMPT = """You are a theoretical framework architect. Transform this resolved predicament into a dialectic unit that captures the synthesis.

DOMAIN: {domain_name}

PREDICAMENT THAT WAS RESOLVED:
Title: {predicament_title}
Type: {predicament_type}
Description: {predicament_description}
Pole A: {pole_a}
Pole B: {pole_b}

RESOLUTION APPROACH:
{resolution_approach}

RESOLUTION NOTES:
{resolution_notes}

ANALYTICAL GRID CONTENT (if available):
{grid_content}

---

Create a dialectic unit that captures this resolved predicament as part of the permanent framework.

The dialectic should:
1. Preserve the tension (pole A ↔ pole B) as an ongoing dynamic
2. Incorporate the synthesis/resolution as navigation strategies
3. Be usable for future analysis in this domain
4. Reference the source predicament for learning

Return a JSON object:

```json
{{
  "name": "Dialectic name (format: 'Pole A ↔ Pole B' or similar)",
  "definition": "One-sentence definition of this dialectic",
  "content": {{
    "pole_a": {{
      "name": "Name of pole A",
      "description": "What pole A represents"
    }},
    "pole_b": {{
      "name": "Name of pole B",
      "description": "What pole B represents"
    }},
    "synthesis_approach": "How the tension can be navigated",
    "navigation_strategies": ["Strategy 1", "Strategy 2"],
    "when_prioritize_a": "Conditions favoring pole A",
    "when_prioritize_b": "Conditions favoring pole B",
    "emerged_from": {{
      "predicament_type": "{predicament_type}",
      "original_description": "{predicament_description}"
    }}
  }},
  "grids_to_generate": ["List of grid types that should be generated for this dialectic"]
}}
```

Return ONLY valid JSON."""


# =============================================================================
# SLOT FILL FOR PREDICAMENT GRID
# =============================================================================

PREDICAMENT_SLOT_FILL_PROMPT = """You are analyzing a predicament using a structured grid. Fill the following slot based on the predicament context.

DOMAIN: {domain_name}
PREDICAMENT: {predicament_title}
PREDICAMENT TYPE: {predicament_type}
DESCRIPTION: {predicament_description}

POLE A: {pole_a}
POLE B: {pole_b}

SLOT TO FILL:
Name: {slot_name}
Description: {slot_description}
Prompt: {slot_prompt}

CONTEXT FROM OTHER SLOTS:
{other_slots_context}

---

Provide thoughtful content for this slot. Your response should:
1. Directly address the slot's purpose
2. Draw on the predicament context
3. Advance the analysis toward resolution

Return a JSON object:

```json
{{
  "content": "Your content for this slot",
  "confidence": 0.0-1.0,
  "notes": "Any notes about this analysis"
}}
```

Return ONLY valid JSON."""


# =============================================================================
# CELL ACTION PROMPTS - Strategic Actions on Matrix Intersections
# =============================================================================

# =============================================================================
# DYNAMIC ACTION GENERATION - Context-specific actions for selected cells
# =============================================================================

GENERATE_CELL_ACTIONS_PROMPT = """You are a strategic analyst generating context-specific analytical actions.

DOMAIN: {domain_name}
CORE QUESTION: {core_question}

PREDICAMENT BEING ANALYZED:
Title: {predicament_title}
Type: {predicament_type}
Description: {predicament_description}
Pole A: {pole_a}
Pole B: {pole_b}

MATRIX STRUCTURE:
- Rows represent: {row_header}
- Columns represent: {col_header}

SELECTED CELL(S):
{selected_cells_detail}

FULL MATRIX CONTEXT:
{matrix_summary}

---

TASK: Generate 3-5 specific analytical actions that would be most valuable for understanding or resolving this particular intersection in the context of the predicament.

These actions should be:
1. SPECIFIC to this exact intersection (not generic "analyze" or "explore")
2. ACTIONABLE - something the LLM can actually produce
3. RELEVANT to resolving the predicament/incoherence
4. STRATEGIC - helping the analyst make progress on the core question

Consider what would be most useful:
- If the cell is WEAK/EMPTY: What would reveal why it's weak? What would strengthen it?
- If the cell is STRONG: What makes it robust? How does it relate to weak areas?
- Given the predicament: What analysis would help resolve the tension?

Examples of GOOD context-specific actions:
- "Map the specific mechanisms by which [row entity] could influence [column dimension]"
- "Identify the 3 key actors who could shift this intersection from weak to strong"
- "Draft policy recommendations that would address the gap at this intersection"
- "Analyze what evidence would change our assessment of this cell"
- "Compare this intersection's dynamics with [related cell] to find leverage points"

Examples of BAD generic actions (avoid these):
- "Deep analysis" (too vague)
- "Generate scenarios" (not specific enough)
- "Explore assumptions" (generic)

Return a JSON array of action objects:

```json
[
  {{
    "id": "action_1",
    "label": "Short action name (3-5 words)",
    "description": "Detailed description of what this action will produce and why it's valuable for resolving the predicament",
    "icon": "bootstrap-icon-name",
    "output_type": "analysis|recommendations|comparison|evidence_map|stakeholder_analysis|policy_draft|scenario|synthesis"
  }}
]
```

Choose appropriate Bootstrap icons: lightbulb, search, people, diagram-3, list-check, file-text, signpost-split, puzzle, bullseye, graph-up, shield-check, globe, building, etc.

Return ONLY valid JSON."""

# Prompt for executing a dynamically generated action
EXECUTE_DYNAMIC_ACTION_PROMPT = """You are a strategic analyst executing a specific analytical action.

DOMAIN: {domain_name}
CORE QUESTION: {core_question}

PREDICAMENT:
Title: {predicament_title}
Type: {predicament_type}
Description: {predicament_description}
Pole A: {pole_a}
Pole B: {pole_b}

MATRIX CONTEXT:
- Rows: {row_header}
- Columns: {col_header}

SELECTED CELL(S):
{selected_cells_detail}

FULL MATRIX:
{matrix_summary}

---

ACTION TO EXECUTE:
Name: {action_label}
Description: {action_description}
Expected Output: {output_type}

---

Execute this action thoroughly. Provide substantive, specific analysis that helps resolve the predicament.

Your output should:
1. Be directly actionable for the analyst
2. Reference specific elements from the matrix and predicament
3. Provide concrete insights, not generic observations
4. Help make progress on the core question

Return a JSON object with your analysis:

```json
{{
  "title": "Title of your analysis",
  "summary": "2-3 sentence executive summary",
  "main_content": "Your detailed analysis (can be multiple paragraphs, use markdown)",
  "key_insights": ["Insight 1", "Insight 2", "Insight 3"],
  "next_steps": ["Recommended next step 1", "Step 2"],
  "confidence": "high|medium|low",
  "confidence_rationale": "Why this confidence level"
}}
```

Return ONLY valid JSON."""

# Base context template for all cell actions
CELL_ACTION_CONTEXT = """DOMAIN: {domain_name}
CORE QUESTION: {core_question}

PREDICAMENT: {predicament_title}
TYPE: {predicament_type}
DESCRIPTION: {predicament_description}

MATRIX CONTEXT:
- Rows represent: {row_header}
- Columns represent: {col_header}

SELECTED CELL(S):
{selected_cells_detail}

FULL MATRIX FOR REFERENCE:
{matrix_summary}
"""

# =============================================================================
# SINGLE CELL ACTIONS
# =============================================================================

CELL_ACTION_WHAT_WOULD_IT_TAKE = """You are a strategic analyst helping transform structural gaps into actionable opportunities.

{context}

---

This cell is rated "{rating}" - indicating a gap or weakness at the intersection of "{row_label}" and "{col_label}".

TASK: Analyze what it would take to strengthen this intersection from {rating} to "strong".

Think strategically about:
1. What structural barriers create this gap?
2. What resources, capabilities, or conditions would be needed?
3. Who would need to act, and what incentives would move them?
4. What's the realistic timeline and sequencing?
5. What would be early indicators of progress?

Return a JSON object:

```json
{{
  "current_state_analysis": "Why this intersection is currently {rating}",
  "structural_barriers": [
    {{"barrier": "Description", "severity": "high|medium|low"}}
  ],
  "required_conditions": [
    {{"condition": "What's needed", "category": "resource|capability|political|institutional|technical"}}
  ],
  "key_actors": [
    {{"actor": "Who", "required_action": "What they'd need to do", "incentive": "Why they might"}}
  ],
  "intervention_options": [
    {{
      "intervention": "Specific action",
      "feasibility": "high|medium|low",
      "impact": "high|medium|low",
      "timeframe": "short|medium|long-term"
    }}
  ],
  "first_steps": ["Immediate actions to begin the transformation"],
  "success_indicators": ["How we'd know it's working"],
  "risks_and_obstacles": ["What could derail this"]
}}
```

Return ONLY valid JSON."""


CELL_ACTION_DEEP_ANALYSIS = """You are a strategic analyst conducting deep examination of a critical intersection.

{context}

---

TASK: Provide comprehensive analysis of the intersection between "{row_label}" and "{col_label}" (currently rated: {rating}).

Examine this intersection from multiple angles:
1. WHY does this rating exist? What underlying dynamics produce it?
2. WHAT are the implications for the broader predicament?
3. HOW does this cell relate to other cells in the matrix?
4. WHAT assumptions are embedded in how we're framing this?
5. WHAT would change our assessment of this cell?

Return a JSON object:

```json
{{
  "intersection_meaning": "What this intersection fundamentally represents",
  "rating_explanation": "Deep analysis of why this cell has rating '{rating}'",
  "causal_dynamics": [
    {{"dynamic": "Description of cause-effect relationship", "evidence": "What supports this"}}
  ],
  "implications": {{
    "for_row_entity": "What this means for {row_label}",
    "for_column_dimension": "What this means for {col_label}",
    "for_predicament": "How this affects the overall predicament"
  }},
  "connections_to_other_cells": [
    {{"related_cell": "Row × Column", "relationship": "How they interact"}}
  ],
  "hidden_assumptions": ["Assumptions we're making about this intersection"],
  "what_would_change_assessment": ["Evidence or events that would shift our rating"],
  "key_insight": "The single most important thing to understand about this intersection",
  "strategic_significance": "Why this cell matters for resolving the predicament"
}}
```

Return ONLY valid JSON."""


CELL_ACTION_GENERATE_ARGUMENTS = """You are a strategic communicator generating compelling arguments.

{context}

---

TASK: Generate talking points and arguments about the intersection of "{row_label}" and "{col_label}" (rated: {rating}).

Create arguments suitable for:
- Strategic documents and memos
- Stakeholder presentations
- Essay paragraphs
- Policy briefs
- Investment theses

Return a JSON object:

```json
{{
  "headline_claim": "The single most powerful statement about this intersection",
  "supporting_arguments": [
    {{
      "argument": "The claim",
      "evidence_type": "empirical|logical|analogical|authoritative",
      "supporting_detail": "Elaboration",
      "potential_counterargument": "What skeptics might say",
      "rebuttal": "How to respond"
    }}
  ],
  "narrative_framing": {{
    "problem_framing": "How to frame this as a problem",
    "opportunity_framing": "How to frame this as an opportunity",
    "urgency_framing": "Why this matters now"
  }},
  "audience_adaptations": {{
    "for_executives": "Key point for decision-makers",
    "for_technical_audience": "Key point for specialists",
    "for_general_audience": "Key point for broader stakeholders"
  }},
  "quotable_lines": ["Memorable phrases that capture the essence"],
  "draft_paragraph": "A polished paragraph suitable for a strategic document"
}}
```

Return ONLY valid JSON."""


CELL_ACTION_SCENARIO_EXPLORATION = """You are a strategic foresight analyst exploring alternative futures.

{context}

---

TASK: Explore scenarios where the intersection of "{row_label}" and "{col_label}" changes from its current state ({rating}).

Consider:
1. What if this became STRONG? (Best case)
2. What if this became EMPTY? (Worst case)
3. What's the most likely trajectory?
4. What wild cards could disrupt the current state?

Return a JSON object:

```json
{{
  "current_trajectory": {{
    "description": "Where this intersection is likely heading without intervention",
    "timeline": "Expected timeframe",
    "confidence": 0.0-1.0
  }},
  "best_case_scenario": {{
    "description": "What 'strong' would look like here",
    "how_it_happens": "Path to this outcome",
    "enabling_conditions": ["What would need to be true"],
    "probability": 0.0-1.0,
    "implications": "What this would mean for the predicament"
  }},
  "worst_case_scenario": {{
    "description": "What deterioration would look like",
    "how_it_happens": "Path to this outcome",
    "warning_signs": ["Early indicators"],
    "probability": 0.0-1.0,
    "implications": "What this would mean for the predicament"
  }},
  "wild_cards": [
    {{
      "event": "Unexpected development",
      "probability": "low|medium",
      "impact_if_occurs": "How it would change this cell",
      "who_controls": "Who could make this happen"
    }}
  ],
  "strategic_options": [
    {{
      "option": "What we could do",
      "target_scenario": "Which scenario it pushes toward",
      "cost": "What it requires",
      "reversibility": "Can we change course if wrong?"
    }}
  ],
  "key_uncertainties": ["What we don't know that matters most"]
}}
```

Return ONLY valid JSON."""


CELL_ACTION_SURFACE_ASSUMPTIONS = """You are a critical analyst uncovering hidden premises.

{context}

---

TASK: Surface the assumptions embedded in how we're understanding the intersection of "{row_label}" and "{col_label}" (rated: {rating}).

Examine:
1. What are we taking for granted about this row entity?
2. What are we assuming about this column dimension?
3. What framings or mental models are shaping our rating?
4. What alternative interpretations exist?

Return a JSON object:

```json
{{
  "assumptions_about_row": [
    {{
      "assumption": "What we assume about {row_label}",
      "why_we_assume_it": "Source of this belief",
      "if_wrong": "What changes if this assumption is false",
      "how_to_test": "How we could validate this"
    }}
  ],
  "assumptions_about_column": [
    {{
      "assumption": "What we assume about {col_label}",
      "why_we_assume_it": "Source of this belief",
      "if_wrong": "What changes if this assumption is false",
      "how_to_test": "How we could validate this"
    }}
  ],
  "assumptions_about_relationship": [
    {{
      "assumption": "What we assume about how row and column interact",
      "if_wrong": "What changes",
      "alternative_framing": "Different way to see this relationship"
    }}
  ],
  "rating_assumptions": {{
    "what_strong_means": "Our implicit definition of 'strong' here",
    "what_empty_means": "Our implicit definition of 'empty' here",
    "measurement_basis": "How we're judging this (explicit or implicit)"
  }},
  "blind_spots": ["What we might be missing entirely"],
  "most_dangerous_assumption": "The assumption most likely to mislead us",
  "recommended_validation": "Most important thing to verify"
}}
```

Return ONLY valid JSON."""


# =============================================================================
# MULTI-CELL ACTIONS
# =============================================================================

CELL_ACTION_FIND_CONNECTIONS = """You are a systems analyst identifying relationships between intersections.

{context}

---

TASK: Analyze the connections between the selected cells and identify patterns.

Look for:
1. Causal relationships (does one cell's state affect another?)
2. Common underlying factors
3. Complementary or contradictory dynamics
4. Leverage points where change in one affects others

Return a JSON object:

```json
{{
  "pattern_summary": "The overarching pattern connecting these cells",
  "relationships": [
    {{
      "from_cell": "Row1 × Column1",
      "to_cell": "Row2 × Column2",
      "relationship_type": "causal|correlated|complementary|contradictory|enabling|blocking",
      "description": "How these cells relate",
      "strength": "strong|moderate|weak",
      "direction": "bidirectional|unidirectional"
    }}
  ],
  "common_factors": [
    {{
      "factor": "What links these cells",
      "how_it_manifests": "How it shows up in each cell"
    }}
  ],
  "system_dynamics": "How these cells function as a system",
  "leverage_points": [
    {{
      "cell": "Which cell",
      "why_leverage": "Why changing this would affect the others",
      "expected_cascade": "What would happen downstream"
    }}
  ],
  "tension_points": ["Where these cells create contradictions or conflicts"],
  "synthesis": "Higher-order insight that emerges from seeing these together",
  "strategic_implication": "What this pattern means for action"
}}
```

Return ONLY valid JSON."""


CELL_ACTION_COALITION_DESIGN = """You are a strategic coalition architect.

{context}

---

TASK: Design a coalition strategy that addresses the selected cells, bringing together actors and capabilities to create change.

Consider:
1. Which actors (rows) have complementary strengths?
2. What dimensions (columns) need coordinated action?
3. How can strengths compensate for weaknesses?
4. What shared interests could unite diverse actors?

Return a JSON object:

```json
{{
  "coalition_thesis": "The core logic of why this coalition could work",
  "member_roles": [
    {{
      "actor": "Row entity from selected cells",
      "contributes": "What they bring to the coalition",
      "gains": "What they get from participating",
      "risk_of_defection": "Why they might not join or might leave"
    }}
  ],
  "capability_map": {{
    "strong_capabilities": ["What the coalition can do well together"],
    "weak_capabilities": ["Gaps the coalition still has"],
    "how_to_address_gaps": "Strategy for capability gaps"
  }},
  "coordination_mechanisms": [
    {{
      "mechanism": "How members coordinate",
      "purpose": "What it achieves",
      "challenges": "What could go wrong"
    }}
  ],
  "shared_interests": ["Common ground that unites the coalition"],
  "potential_conflicts": ["Where member interests diverge"],
  "conflict_resolution": "How to manage internal tensions",
  "first_joint_action": "What the coalition should do first",
  "success_metrics": ["How to measure coalition effectiveness"],
  "failure_modes": ["How this coalition could fall apart"]
}}
```

Return ONLY valid JSON."""


CELL_ACTION_PRIORITIZE = """You are a strategic prioritization advisor.

{context}

---

TASK: Prioritize the selected cells for action, determining which intersections matter most and should be addressed first.

Consider:
1. Impact: Which cells most affect the overall predicament?
2. Feasibility: Which cells are most amenable to change?
3. Urgency: Which cells are deteriorating or have time pressure?
4. Leverage: Which cells would create positive cascades?
5. Risk: Which cells pose the greatest downside if ignored?

Return a JSON object:

```json
{{
  "prioritization_framework": "The logic used to prioritize",
  "priority_ranking": [
    {{
      "rank": 1,
      "cell": "Row × Column",
      "current_rating": "strong|moderate|weak|empty",
      "priority_score": 0.0-1.0,
      "rationale": "Why this ranks here",
      "impact_if_addressed": "What changes if we focus here",
      "impact_if_ignored": "What happens if we don't"
    }}
  ],
  "sequencing_recommendation": {{
    "immediate": ["Cells to address in 0-3 months"],
    "near_term": ["Cells to address in 3-12 months"],
    "long_term": ["Cells for ongoing attention"],
    "sequencing_logic": "Why this order"
  }},
  "quick_wins": ["Cells where rapid progress is possible"],
  "strategic_bets": ["Cells requiring sustained investment for big payoff"],
  "watch_list": ["Cells to monitor but not actively address yet"],
  "resource_allocation": "How to divide attention across these cells",
  "decision_criteria": "When to shift priorities"
}}
```

Return ONLY valid JSON."""


CELL_ACTION_SYNTHESIZE_CONCEPT = """You are a theoretical architect synthesizing new frameworks.

{context}

---

TASK: Synthesize a new concept, framework, or mental model that emerges from the pattern across the selected cells.

The goal is to create intellectual infrastructure - a new way of thinking that captures what these cells reveal together.

Consider:
1. What phenomenon do these cells collectively illuminate?
2. What name would capture this pattern?
3. How could this concept be used in analysis and strategy?
4. What are the concept's key dimensions or components?

Return a JSON object:

```json
{{
  "concept_name": "Proposed name for this new concept",
  "definition": "One-sentence definition",
  "extended_description": "Fuller explanation of what this concept captures",
  "emerges_from": "How this concept arises from the selected cells",
  "key_components": [
    {{
      "component": "Element of the concept",
      "description": "What it means",
      "relates_to_cells": "Which cells illuminate this component"
    }}
  ],
  "diagnostic_questions": ["Questions this concept helps you ask"],
  "application_domains": ["Where this concept would be useful beyond this predicament"],
  "related_concepts": ["Existing concepts this relates to or extends"],
  "visual_metaphor": "An image or metaphor that captures the concept",
  "what_it_predicts": ["Observable implications if this concept is valid"],
  "limitations": ["Where this concept breaks down or doesn't apply"],
  "next_steps": ["How to develop and validate this concept further"]
}}
```

Return ONLY valid JSON."""


# =============================================================================
# DIALECTIC GENERATION FROM NOTE - LLM-powered dialectic extraction
# =============================================================================

DIALECTIC_FROM_NOTE_PROMPT = """You are a theoretical framework architect. Your task is to extract a dialectical structure from analytical notes.

A dialectic captures a fundamental tension between two poles that cannot be simply resolved but must be navigated. Good dialectics are:
- Non-trivial: Not "good vs bad" but genuine competing values/approaches
- Generative: The tension produces insight when examined
- Navigable: Both poles have merit depending on context

PREDICAMENT CONTEXT:
Title: {predicament_title}
Type: {predicament_type}
Description: {predicament_description}
Existing Pole A: {existing_pole_a}
Existing Pole B: {existing_pole_b}

NOTE TO ANALYZE:
Title: {note_title}
Action Performed: {note_action}
Cells Analyzed: {note_cells}
Content: {note_content}
Thinking Summary: {note_thinking}

---

TASK: Extract a dialectical structure from this analysis. The dialectic should capture the core tension revealed by the note.

Provide:
1. A clear, memorable NAME for the dialectic (format: "Pole A ↔ Pole B" or a conceptual name)
2. A one-sentence DEFINITION that captures what this dialectic is about
3. Well-articulated POLES (thesis and antithesis) - improve upon existing poles if they're vague
4. Initial thoughts on SYNTHESIS or navigation strategies

Return a JSON object:

```json
{{
  "dialectic_name": "Name for the dialectic (can use ↔ format or conceptual name)",
  "definition": "One-sentence definition of what this dialectic captures",
  "pole_a": {{
    "name": "Short name for thesis (2-4 words)",
    "description": "What this pole represents and when it's prioritized"
  }},
  "pole_b": {{
    "name": "Short name for antithesis (2-4 words)",
    "description": "What this pole represents and when it's prioritized"
  }},
  "synthesis_notes": "Initial thoughts on how to navigate this tension",
  "navigation_strategies": ["Strategy 1 for balancing the poles", "Strategy 2"],
  "why_this_dialectic": "Why this is the right dialectical framing for the note's insights",
  "confidence": 0.0-1.0
}}
```

IMPORTANT:
- The dialectic should emerge from the NOTE content, not just repeat the predicament
- Make the poles specific and substantive, not generic
- The definition should be actionable - someone should understand what they're navigating

Return ONLY valid JSON."""


CELL_ACTION_DRAFT_CONTENT = """You are a strategic writer crafting analytical content.

{context}

---

TASK: Draft polished analytical content about the selected cell(s) that could be used in strategic documents, essays, reports, or presentations.

Create content that:
1. Is intellectually rigorous but accessible
2. Makes a clear analytical point
3. Is suitable for professional/academic contexts
4. Can stand alone or be integrated into larger documents

Return a JSON object:

```json
{{
  "headline": "A compelling title or header for this content",
  "executive_summary": "One paragraph capturing the key insight (3-4 sentences)",
  "full_analysis": "Extended analytical content (2-3 paragraphs)",
  "key_quotes": ["Quotable sentences that capture main points"],
  "supporting_evidence": ["Specific evidence or examples to cite"],
  "visual_suggestion": {{
    "type": "chart|diagram|table|infographic",
    "description": "What visual would complement this text"
  }},
  "call_to_action": "What the reader should think or do after reading",
  "tone_variations": {{
    "academic": "Version for scholarly context",
    "executive": "Version for business/policy context",
    "general": "Version for broader audience"
  }},
  "integration_suggestions": ["Where in a larger document this could fit"]
}}
```

Return ONLY valid JSON."""
