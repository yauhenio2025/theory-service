"""
Concept Evidence LLM Integration

Handles LLM calls for:
1. Extracting fragments from sources
2. Analyzing fragments against existing concept
3. Generating interpretations for ambiguous cases
4. Adding commitment/foreclosure statements
"""

import json
import logging
from typing import List, Dict, Optional, Tuple
from anthropic import Anthropic
import os

from .concept_evidence_prompts import (
    EVIDENCE_EXTRACTION_PROMPT,
    EVIDENCE_ANALYSIS_PROMPT,
    INTERPRETATION_GENERATION_PROMPT,
    COMMITMENT_FORECLOSURE_PROMPT,
    format_items_for_prompt,
    format_analysis_for_prompt
)

logger = logging.getLogger(__name__)

# Model configuration
MODEL = "claude-sonnet-4-5-20250929"
MAX_TOKENS = 4000

_client = None

def get_claude_client():
    """Get Claude client, raising helpful error if API key missing."""
    global _client
    if _client is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        _client = Anthropic(api_key=api_key)
    return _client


async def extract_fragments_from_source(
    concept_term: str,
    concept_definition: str,
    concept_summary: str,
    source_name: str,
    source_type: str,
    source_content: str
) -> List[Dict]:
    """
    Extract relevant fragments from a source document.

    Returns list of fragment dicts with:
    - content: The extracted claim
    - source_location: Where in the document
    - likely_dimension: Which dimension it relates to
    - extraction_note: Why it's relevant
    """
    prompt = EVIDENCE_EXTRACTION_PROMPT.format(
        concept_term=concept_term,
        concept_definition=concept_definition or "No definition provided",
        concept_summary=concept_summary or "No summary available",
        source_name=source_name,
        source_type=source_type,
        source_content=source_content[:15000]  # Limit content length
    )

    client = get_claude_client()

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract JSON from response
        content = response.content[0].text

        # Try to find JSON in response
        json_start = content.find('{')
        json_end = content.rfind('}') + 1

        if json_start >= 0 and json_end > json_start:
            json_str = content[json_start:json_end]
            result = json.loads(json_str)
            return result.get("fragments", [])
        else:
            logger.error(f"No JSON found in extraction response: {content[:500]}")
            return []

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse extraction response: {e}")
        return []
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise


async def analyze_fragment(
    concept_term: str,
    concept_definition: str,
    fragment_content: str,
    source_name: str,
    dimension_name: str,
    current_analysis: dict,
    existing_items: List[dict]
) -> Dict:
    """
    Analyze how a fragment relates to existing concept analysis.

    Returns dict with:
    - relationship_type: How it relates
    - target_operation_name: Which operation
    - confidence: 0.0-1.0
    - is_ambiguous: bool
    - why_needs_decision: explanation if ambiguous
    - auto_integration_content: content to add if auto-integrating
    """
    prompt = EVIDENCE_ANALYSIS_PROMPT.format(
        concept_term=concept_term,
        concept_definition=concept_definition or "No definition provided",
        fragment_content=fragment_content,
        source_name=source_name,
        dimension_name=dimension_name,
        current_analysis=format_analysis_for_prompt(current_analysis),
        existing_items=format_items_for_prompt(existing_items)
    )

    client = get_claude_client()

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.content[0].text

        # Extract JSON
        json_start = content.find('{')
        json_end = content.rfind('}') + 1

        if json_start >= 0 and json_end > json_start:
            json_str = content[json_start:json_end]
            return json.loads(json_str)
        else:
            logger.error(f"No JSON found in analysis response")
            return {
                "relationship_type": "illustrates",
                "confidence": 0.5,
                "is_ambiguous": True,
                "why_needs_decision": "Failed to parse LLM response"
            }

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse analysis response: {e}")
        return {
            "relationship_type": "illustrates",
            "confidence": 0.5,
            "is_ambiguous": True,
            "why_needs_decision": f"Parse error: {e}"
        }
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise


async def generate_interpretations(
    concept_term: str,
    fragment_content: str,
    source_name: str,
    why_ambiguous: str,
    current_analysis: dict,
    existing_items: List[dict]
) -> List[Dict]:
    """
    Generate multiple valid interpretations for ambiguous evidence.

    Returns list of interpretation dicts with:
    - key: a, b, c...
    - title: Short title
    - strategy: What this interpretation means
    - rationale: Why it's valid
    - relationship_type: The implied relationship
    - is_recommended: bool
    - structural_changes: list of changes
    """
    prompt = INTERPRETATION_GENERATION_PROMPT.format(
        concept_term=concept_term,
        fragment_content=fragment_content,
        source_name=source_name,
        why_ambiguous=why_ambiguous,
        current_analysis=format_analysis_for_prompt(current_analysis),
        existing_items=format_items_for_prompt(existing_items)
    )

    client = get_claude_client()

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.content[0].text

        json_start = content.find('{')
        json_end = content.rfind('}') + 1

        if json_start >= 0 and json_end > json_start:
            json_str = content[json_start:json_end]
            result = json.loads(json_str)
            return result.get("interpretations", [])
        else:
            logger.error(f"No JSON found in interpretation response")
            return []

    except Exception as e:
        logger.error(f"Interpretation generation failed: {e}")
        raise


async def add_commitment_foreclosure(
    concept_term: str,
    fragment_content: str,
    interpretations: List[Dict]
) -> Dict:
    """
    Add commitment and foreclosure statements to interpretations.

    Returns dict mapping interpretation key to:
    - commitment_statement: What you commit to
    - foreclosure_statements: What you give up
    """
    prompt = COMMITMENT_FORECLOSURE_PROMPT.format(
        concept_term=concept_term,
        fragment_content=fragment_content,
        interpretations_json=json.dumps(interpretations, indent=2)
    )

    client = get_claude_client()

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.content[0].text

        json_start = content.find('{')
        json_end = content.rfind('}') + 1

        if json_start >= 0 and json_end > json_start:
            json_str = content[json_start:json_end]
            result = json.loads(json_str)

            # Convert to dict keyed by interpretation key
            cf_by_key = {}
            for interp in result.get("interpretations", []):
                cf_by_key[interp["key"]] = {
                    "commitment_statement": interp.get("commitment_statement", ""),
                    "foreclosure_statements": interp.get("foreclosure_statements", [])
                }
            return cf_by_key
        else:
            return {}

    except Exception as e:
        logger.error(f"Commitment/foreclosure generation failed: {e}")
        return {}


# Mapping from dimension names to likely item types
DIMENSION_TO_ITEM_TYPES = {
    "positional": ["forward_inferences", "backward_inferences", "contradictions", "lateral_connections"],
    "genealogical": ["origin_claims", "predecessor_concepts", "historical_context"],
    "presuppositional": ["hidden_assumptions", "tacit_premises", "taken_for_granted"],
    "commitment": ["commitments", "obligations", "entailments"],
    "affordance": ["enables", "allows", "makes_possible"],
    "normalization": ["normalizes", "naturalizes", "deviation_criteria"],
    "boundary": ["edge_cases", "limits", "scope_conditions"],
    "dynamic": ["evolution_stages", "transformations", "temporal_changes"],
}


def get_likely_item_type(dimension: str, relationship_type: str) -> str:
    """Determine the most appropriate item type for auto-integration."""
    dimension_lower = dimension.lower()

    if dimension_lower in DIMENSION_TO_ITEM_TYPES:
        item_types = DIMENSION_TO_ITEM_TYPES[dimension_lower]

        # Map relationship type to position in item types
        if relationship_type == "challenges":
            return "contradictions" if "contradictions" in item_types else item_types[0]
        elif relationship_type == "limits":
            return "scope_conditions" if "scope_conditions" in item_types else "edge_cases"
        elif relationship_type == "bridges":
            return "lateral_connections" if "lateral_connections" in item_types else item_types[-1]
        else:
            return item_types[0]

    return "evidence_insight"
