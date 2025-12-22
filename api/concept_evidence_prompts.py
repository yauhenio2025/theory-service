"""
Concept Evidence Prompts - LLM Prompts for Evidence Integration

These prompts guide the LLM through evidence extraction, analysis,
interpretation generation, and commitment/foreclosure articulation.
"""

# ==================== EXTRACTION PROMPT ====================

EVIDENCE_EXTRACTION_PROMPT = """You are analyzing a text source to extract claims and insights relevant to a specific concept.

CONCEPT BEING ANALYZED:
Term: {concept_term}
Definition: {concept_definition}
Current analysis summary:
{concept_summary}

SOURCE TO ANALYZE:
Name: {source_name}
Type: {source_type}
Content:
---
{source_content}
---

TASK:
Extract 3-8 distinct claims, insights, or observations from this source that are relevant to the concept "{concept_term}".

For each extracted fragment:
1. Quote or paraphrase the specific claim (keep it concise, 1-3 sentences)
2. Note the approximate location in the source (beginning/middle/end, or paragraph number if clear)
3. Identify which analytical dimension it most relates to:
   - POSITIONAL: How the concept is placed in discourse/debates
   - GENEALOGICAL: Historical origins, predecessors, emergence
   - PRESUPPOSITIONAL: Hidden assumptions, taken-for-granted premises
   - COMMITMENT: What accepting this concept commits you to
   - AFFORDANCE: What the concept enables or allows
   - NORMALIZATION: How it shapes what counts as normal/deviant
   - BOUNDARY: Edge cases, limits, tensions
   - DYNAMIC: How the concept changes over time, evolves

OUTPUT FORMAT (JSON):
{{
  "fragments": [
    {{
      "content": "The extracted claim or insight",
      "source_location": "paragraph 3" or "middle of text",
      "likely_dimension": "positional|genealogical|presuppositional|commitment|affordance|normalization|boundary|dynamic",
      "extraction_note": "Brief note on why this is relevant to the concept"
    }}
  ]
}}
"""


# ==================== ANALYSIS PROMPT ====================

EVIDENCE_ANALYSIS_PROMPT = """You are analyzing how an extracted evidence fragment relates to an existing concept analysis.

CONCEPT: {concept_term}
DEFINITION: {concept_definition}

EVIDENCE FRAGMENT:
"{fragment_content}"
Source: {source_name}

CURRENT ANALYSIS STATE FOR THIS DIMENSION ({dimension_name}):
{current_analysis}

EXISTING ITEMS IN THIS DIMENSION:
{existing_items}

TASK:
Analyze how this evidence fragment relates to the existing analysis. Determine:

1. RELATIONSHIP TYPE - How does this evidence relate?
   - ILLUSTRATES: Provides a concrete example that makes the analysis more vivid
   - DEEPENS: Adds nuance, complexity, or refinement to existing understanding
   - CHALLENGES: Contradicts or problematizes a key premise or claim
   - LIMITS: Establishes a boundary or scope condition
   - BRIDGES: Connects this dimension to another previously unconnected dimension
   - INVERTS: Suggests the relationship works opposite to what was assumed

2. TARGET - Which specific operation or item does this relate to most?

3. CONFIDENCE - How clear is the relationship? (0.0-1.0)
   - 0.85+ : Clear, unambiguous relationship → can auto-integrate
   - 0.60-0.84 : Moderately clear but some interpretation needed → needs decision
   - Below 0.60 : Ambiguous, multiple valid readings → definitely needs decision

4. AMBIGUITY CHECK - Is there more than one valid way to integrate this evidence?

OUTPUT FORMAT (JSON):
{{
  "relationship_type": "illustrates|deepens|challenges|limits|bridges|inverts",
  "target_operation_name": "name of the most relevant operation",
  "target_item_id": null or ID if targeting specific existing item,
  "confidence": 0.0-1.0,
  "is_ambiguous": true/false,
  "why_needs_decision": "Explanation if ambiguous, null otherwise",
  "auto_integration_content": "If not ambiguous and confidence >= 0.85, what content to add",
  "auto_integration_item_type": "If auto-integrating, what item_type"
}}
"""


# ==================== INTERPRETATION GENERATION PROMPT ====================

INTERPRETATION_GENERATION_PROMPT = """You are generating multiple valid interpretations for how ambiguous evidence can be integrated into a concept analysis.

CONCEPT: {concept_term}

EVIDENCE FRAGMENT:
"{fragment_content}"
Source: {source_name}

WHY THIS IS AMBIGUOUS:
{why_ambiguous}

CURRENT ANALYSIS STATE:
{current_analysis}

EXISTING ITEMS THAT MIGHT BE AFFECTED:
{existing_items}

TASK:
Generate 2-4 distinct, valid interpretations for how to integrate this evidence. Each interpretation should represent a genuinely different approach, not just minor variations.

For each interpretation:
1. Give it a clear title (e.g., "Revise the core definition", "Add as complementary framing")
2. Explain the strategy - what does this interpretation mean?
3. Provide the rationale - why is this a valid reading?
4. Specify the relationship type this interpretation implies
5. List the specific structural changes this would require
6. Mark if you recommend this interpretation (only one should be recommended)

INTERPRETATION ARCHETYPES TO CONSIDER:
- REVISE: Update existing content to incorporate new perspective
- EXTEND: Add new content without changing existing
- SCOPE: Add boundary/limitation rather than changing core
- SYNTHESIZE: Merge with existing to create richer understanding
- DEFER: Acknowledge but postpone full integration

OUTPUT FORMAT (JSON):
{{
  "interpretations": [
    {{
      "key": "a",
      "title": "Short descriptive title",
      "strategy": "What this interpretation means",
      "rationale": "Why this reading is valid",
      "relationship_type": "illustrates|deepens|challenges|limits|bridges|inverts",
      "target_operation_name": "which operation this affects",
      "is_recommended": true/false,
      "recommendation_rationale": "Why recommended (if applicable)",
      "structural_changes": [
        {{
          "change_type": "revision|addition|strengthening|scope_limitation|deletion",
          "target_operation_name": "operation name",
          "target_item_id": null or ID,
          "before_content": "Current content (for revisions)",
          "after_content": "Proposed new content"
        }}
      ]
    }}
  ]
}}
"""


# ==================== COMMITMENT/FORECLOSURE PROMPT ====================

COMMITMENT_FORECLOSURE_PROMPT = """You are articulating the commitments and foreclosures for each interpretation of evidence integration.

CONCEPT: {concept_term}

EVIDENCE FRAGMENT:
"{fragment_content}"

INTERPRETATIONS TO ANALYZE:
{interpretations_json}

TASK:
For each interpretation, articulate:

1. COMMITMENT STATEMENT: What are you committing to by choosing this interpretation?
   - Be specific about the theoretical or practical implications
   - Focus on what this choice means going forward

2. FORECLOSURE STATEMENTS: What options are you giving up?
   - What alternative framings become unavailable?
   - What nuances or distinctions are lost?
   - What future directions become harder?

The goal is to help the user make an informed choice by clearly seeing the trade-offs of each option.

OUTPUT FORMAT (JSON):
{{
  "interpretations": [
    {{
      "key": "a",
      "commitment_statement": "By choosing this, you commit to...",
      "foreclosure_statements": [
        "You lose the ability to...",
        "This precludes treating X as...",
        "Future extensions in direction Y become harder"
      ]
    }}
  ]
}}
"""


# ==================== BATCH SYNTHESIS PROMPT ====================

BATCH_SYNTHESIS_PROMPT = """You are synthesizing multiple evidence fragments into coherent themes or clusters.

CONCEPT: {concept_term}

FRAGMENTS TO SYNTHESIZE:
{fragments_json}

CURRENT CONCEPT ANALYSIS SUMMARY:
{concept_summary}

TASK:
Analyze these fragments together and identify:

1. CLUSTERS: Groups of fragments that point to the same insight or theme
   - Give each cluster a descriptive name
   - Note which fragments belong to it
   - Summarize the collective insight

2. TENSIONS: Where do fragments conflict with each other or with existing analysis?
   - Identify the specific tension
   - Note which fragments are involved
   - Rate severity (minor/significant/critical)

3. BLACK SWANS: Any fragments that don't fit patterns but are notably significant
   - Why is this fragment unusual?
   - What might it signal?

4. RECOMMENDED PROCESSING ORDER: In what order should these be processed?
   - Consider dependencies (some decisions might affect others)
   - Consider impact (high-impact decisions first?)

OUTPUT FORMAT (JSON):
{{
  "clusters": [
    {{
      "name": "Cluster theme name",
      "fragment_ids": [1, 3, 5],
      "collective_insight": "What these fragments together suggest",
      "confidence": 0.0-1.0,
      "suggested_action": "auto_integrate|needs_decision"
    }}
  ],
  "tensions": [
    {{
      "description": "The tension identified",
      "fragment_ids": [2, 4],
      "severity": "minor|significant|critical",
      "resolution_hint": "Possible way to resolve"
    }}
  ],
  "black_swans": [
    {{
      "fragment_id": 6,
      "why_notable": "Why this stands out",
      "impact_level": "low|medium|high"
    }}
  ],
  "processing_order": [1, 3, 5, 2, 4, 6]
}}
"""


# ==================== HELPER FUNCTION ====================

def format_items_for_prompt(items: list) -> str:
    """Format analysis items for inclusion in prompts."""
    if not items:
        return "No existing items."

    lines = []
    for i, item in enumerate(items, 1):
        content = item.get('content', item.get('text', ''))[:200]
        item_type = item.get('item_type', item.get('type', 'item'))
        lines.append(f"{i}. [{item_type}] {content}")

    return "\n".join(lines)


def format_analysis_for_prompt(analysis_data: dict) -> str:
    """Format analysis data for inclusion in prompts."""
    if not analysis_data:
        return "No existing analysis."

    parts = []
    if 'canonical_statement' in analysis_data:
        parts.append(f"Core: {analysis_data['canonical_statement']}")

    if 'key_points' in analysis_data:
        parts.append("Key points:")
        for point in analysis_data['key_points'][:5]:
            parts.append(f"  - {point[:100]}")

    return "\n".join(parts) if parts else str(analysis_data)[:500]
