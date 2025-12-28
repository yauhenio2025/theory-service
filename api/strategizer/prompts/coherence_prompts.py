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

PREDICAMENT_GRID_PROMPT = """You are a theoretical framework architect. Generate an analytical grid to help resolve this predicament.

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

Create an analytical grid that will help think through and resolve this predicament.

The grid should have 4-8 slots, each designed to systematically work through the predicament.
Choose a grid structure appropriate to the predicament type:

- For THEORETICAL predicaments: Focus on assumptions, implications, synthesis possibilities
- For EMPIRICAL predicaments: Focus on evidence, explanatory gaps, theory modification options
- For CONCEPTUAL predicaments: Focus on distinctions, edge cases, alternative carve-ups
- For PRAXIS predicaments: Focus on decision criteria, action options, trade-offs

Return a JSON object:

```json
{{
  "grid_type": "PREDICAMENT_ANALYSIS",
  "grid_name": "Name for this analytical grid",
  "grid_description": "What this grid helps analyze",
  "slots": [
    {{
      "name": "slot_name",
      "description": "What this slot captures",
      "prompt": "Question or prompt to fill this slot",
      "initial_content": "Pre-filled content based on the predicament context"
    }}
  ],
  "analysis_sequence": "Recommended order to work through the slots",
  "resolution_criteria": "How to know when the predicament is resolved"
}}
```

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
