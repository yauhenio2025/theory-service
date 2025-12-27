"""
Strategizer Evidence LLM Service

LLM functions for evidence extraction, analysis, and interpretation.
Following the LLM-first philosophy: Python gathers → LLM judges → Python executes.
"""

import json
import logging
from typing import List, Dict, Optional
from anthropic import Anthropic
import os

from ..prompts.evidence_prompts import (
    EVIDENCE_EXTRACTION_PROMPT,
    EVIDENCE_ANALYSIS_PROMPT,
    INTERPRETATION_GENERATION_PROMPT,
    COMMITMENT_FORECLOSURE_PROMPT,
    format_units_for_prompt,
    format_grid_slots_for_prompt,
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


def _parse_json_response(content: str) -> Optional[Dict]:
    """Parse JSON from LLM response, handling markdown code blocks."""
    # Try to find JSON in response
    # First check for ```json blocks
    if "```json" in content:
        start = content.find("```json") + 7
        end = content.find("```", start)
        if end > start:
            json_str = content[start:end].strip()
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass

    # Try to find raw JSON
    json_start = content.find('{')
    json_end = content.rfind('}') + 1

    if json_start >= 0 and json_end > json_start:
        json_str = content[json_start:json_end]
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            return None

    return None


async def extract_fragments_from_source(
    domain_name: str,
    core_question: str,
    units: List[Dict],
    source_name: str,
    source_type: str,
    source_content: str
) -> List[Dict]:
    """
    Extract strategic insights from a source document.

    Returns list of fragment dicts with:
    - content: The extracted claim
    - source_location: Where in the document
    - likely_unit_type: concept/dialectic/actor
    - likely_unit_name: Related unit if obvious
    - extraction_note: Why it's relevant
    """
    prompt = EVIDENCE_EXTRACTION_PROMPT.format(
        domain_name=domain_name or "Strategic Analysis",
        core_question=core_question or "General strategic analysis",
        units_summary=format_units_for_prompt(units),
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

        result = _parse_json_response(response.content[0].text)
        if result:
            return result.get("fragments", [])
        else:
            logger.error(f"No JSON found in extraction response")
            return []

    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise


async def analyze_fragment(
    domain_name: str,
    core_question: str,
    unit_type: str,
    unit_name: str,
    unit_definition: str,
    grids: List[Dict],
    source_name: str,
    fragment_content: str
) -> Dict:
    """
    Analyze how a fragment relates to a strategic unit.

    Returns dict with:
    - relationship_type: How it relates
    - target_grid_slot: Which slot (e.g., "LOGICAL.premise")
    - confidence: 0.0-1.0
    - is_ambiguous: bool
    - why_needs_decision: explanation if ambiguous
    - integration_suggestion: content if high confidence
    """
    prompt = EVIDENCE_ANALYSIS_PROMPT.format(
        domain_name=domain_name or "Strategic Analysis",
        core_question=core_question or "General strategic analysis",
        unit_type=unit_type,
        unit_name=unit_name,
        unit_definition=unit_definition or "No definition provided",
        grid_slots=format_grid_slots_for_prompt(grids),
        source_name=source_name,
        fragment_content=fragment_content
    )

    client = get_claude_client()

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}]
        )

        result = _parse_json_response(response.content[0].text)
        if result:
            return result
        else:
            return {
                "relationship_type": "new_insight",
                "target_grid_slot": None,
                "confidence": 0.3,
                "is_ambiguous": True,
                "why_needs_decision": "Failed to parse analysis response"
            }

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise


async def generate_interpretations(
    domain_name: str,
    core_question: str,
    unit_type: str,
    unit_name: str,
    unit_definition: str,
    grids: List[Dict],
    source_name: str,
    fragment_content: str,
    why_ambiguous: str
) -> Dict:
    """
    Generate interpretation options for an ambiguous fragment.

    Returns dict with:
    - interpretations: List of interpretation options
    - decision_context: What the user should consider
    """
    prompt = INTERPRETATION_GENERATION_PROMPT.format(
        domain_name=domain_name or "Strategic Analysis",
        core_question=core_question or "General strategic analysis",
        unit_type=unit_type,
        unit_name=unit_name,
        unit_definition=unit_definition or "No definition provided",
        grid_slots=format_grid_slots_for_prompt(grids),
        source_name=source_name,
        fragment_content=fragment_content,
        why_ambiguous=why_ambiguous or "Multiple possible readings"
    )

    client = get_claude_client()

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}]
        )

        result = _parse_json_response(response.content[0].text)
        if result:
            return result
        else:
            return {
                "interpretations": [],
                "decision_context": "Failed to generate interpretations"
            }

    except Exception as e:
        logger.error(f"Interpretation generation failed: {e}")
        raise


async def add_commitment_foreclosure(
    interpretation_title: str,
    interpretation_strategy: str,
    target_slot: str,
    relationship_type: str,
    unit_name: str,
    current_slot_content: str
) -> Dict:
    """
    Add commitment/foreclosure analysis to an interpretation.

    Returns dict with:
    - commitment_statement: What accepting commits to
    - foreclosure_statements: What it forecloses
    - risk_level: low/medium/high
    - reversibility: How hard to undo
    """
    prompt = COMMITMENT_FORECLOSURE_PROMPT.format(
        interpretation_title=interpretation_title,
        interpretation_strategy=interpretation_strategy,
        target_slot=target_slot or "General unit content",
        relationship_type=relationship_type,
        unit_name=unit_name,
        current_slot_content=current_slot_content or "Empty slot"
    )

    client = get_claude_client()

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}]
        )

        result = _parse_json_response(response.content[0].text)
        if result:
            return result
        else:
            return {
                "commitment_statement": "Accepting this interpretation",
                "foreclosure_statements": [],
                "risk_level": "medium",
                "reversibility": "Unknown"
            }

    except Exception as e:
        logger.error(f"Commitment/foreclosure analysis failed: {e}")
        raise


async def suggest_target_unit(
    domain_name: str,
    core_question: str,
    units: List[Dict],
    fragment_content: str,
    source_name: str
) -> Dict:
    """
    Suggest which unit a fragment should be analyzed against.

    Used when no explicit target is provided.

    Returns dict with:
    - unit_id: Suggested unit ID
    - unit_name: Suggested unit name
    - confidence: How confident in the suggestion
    - rationale: Why this unit
    - alternative_units: Other possible units
    """
    prompt = f"""You are matching an evidence fragment to the most relevant strategic unit.

## Project Context

**Domain:** {domain_name or "Strategic Analysis"}
**Core Question:** {core_question or "General strategic analysis"}

## Available Units

{format_units_for_prompt(units)}

## Evidence Fragment

**Source:** {source_name}
**Content:** "{fragment_content}"

## Your Task

Determine which unit this fragment is most relevant to.

Return JSON:
```json
{{
  "unit_name": "Name of the most relevant unit",
  "confidence": 0.85,
  "rationale": "Why this unit is the best match",
  "alternative_units": ["Other possible units"],
  "should_create_new": false,
  "new_unit_suggestion": null
}}
```

If the fragment doesn't fit any existing unit well (confidence < 0.5),
suggest creating a new unit with `should_create_new: true`.
"""

    client = get_claude_client()

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}]
        )

        result = _parse_json_response(response.content[0].text)
        if result:
            return result
        else:
            return {
                "unit_name": None,
                "confidence": 0.0,
                "rationale": "Failed to suggest unit",
                "alternative_units": [],
                "should_create_new": True,
                "new_unit_suggestion": None
            }

    except Exception as e:
        logger.error(f"Unit suggestion failed: {e}")
        raise
