"""
Strategizer LLM Service

Claude API integration for domain bootstrapping and Q&A dialogue.
Uses the LLM-First Philosophy: Python gathers → LLM judges → Python executes.
"""

import os
import json
from typing import Dict, Any, List, Optional

from anthropic import Anthropic


# Claude configuration
CLAUDE_MODEL = os.getenv("STRATEGIZER_MODEL", "claude-sonnet-4-5-20250929")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


class StrategizerLLM:
    """LLM service for Strategizer operations."""

    def __init__(self):
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
        self.model = CLAUDE_MODEL

    async def bootstrap_domain(
        self,
        project_name: str,
        project_brief: str
    ) -> Dict[str, Any]:
        """
        Bootstrap a domain from a project brief.

        The LLM analyzes the brief and proposes:
        - Domain name and core question
        - Success criteria
        - Vocabulary mapping (how to name concepts, tensions, actors in this domain)
        - Seed content (3-5 concepts, 2-3 dialectics)

        Args:
            project_name: Name of the project
            project_brief: Full project brief/description

        Returns:
            Dict with domain structure and seed content
        """
        prompt = self._build_bootstrap_prompt(project_name, project_brief)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract JSON from response
        response_text = response.content[0].text
        return self._parse_bootstrap_response(response_text)

    async def answer_question(
        self,
        question: str,
        domain_context: Dict[str, Any],
        units: List[Dict[str, Any]],
        dialogue_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Answer a strategic question using the framework context.

        Args:
            question: The user's question
            domain_context: Domain info (name, vocabulary, core question)
            units: List of existing units (concepts, dialectics, actors)
            dialogue_history: Recent dialogue turns

        Returns:
            Dict with response, implications, and suggested actions
        """
        prompt = self._build_qa_prompt(question, domain_context, units, dialogue_history)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = response.content[0].text
        return self._parse_qa_response(response_text)

    async def suggest_next_steps(
        self,
        domain_context: Dict[str, Any],
        units: List[Dict[str, Any]],
        focus: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Suggest next steps for framework development.

        Args:
            domain_context: Domain info
            units: Existing units
            focus: Optional focus area

        Returns:
            Dict with suggestions and priority actions
        """
        prompt = self._build_suggestion_prompt(domain_context, units, focus)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = response.content[0].text
        return self._parse_suggestion_response(response_text)

    def _build_bootstrap_prompt(self, project_name: str, project_brief: str) -> str:
        """Build the domain bootstrapping prompt."""
        return f"""You are a strategic framework architect. Analyze this project brief and propose a domain structure.

PROJECT NAME: {project_name}

PROJECT BRIEF:
{project_brief}

---

Analyze this brief and propose a strategic domain structure. Return a JSON object with:

1. **domain_name**: A concise name for this strategic domain (e.g., "Climate Tech Investment", "Brand Positioning", "Policy Reform")

2. **core_question**: The central question this framework helps answer (e.g., "Where should we deploy capital for maximum climate impact?")

3. **success_looks_like**: A concrete description of what success means in this domain

4. **vocabulary**: Domain-specific terms for the three unit types:
   - concept: What to call strategic concepts in this domain (e.g., "Thesis", "Principle", "Driver")
   - dialectic: What to call tensions/trade-offs (e.g., "Trade-off", "Tension", "Dilemma")
   - actor: What to call actors/stakeholders (e.g., "Player", "Stakeholder", "Agent")

5. **template_base**: Which template family fits best (one of: "investment", "brand", "policy", "theory", "foundation", or null if none fit)

6. **seed_concepts**: 3-5 fundamental concepts for this domain, each with:
   - name: The concept name
   - definition: One-sentence definition
   - why_fundamental: Why this is essential to this domain

7. **seed_dialectics**: 2-3 core tensions in this domain, each with:
   - name: "Pole A ↔ Pole B" format
   - pole_a: Description of first pole
   - pole_b: Description of second pole
   - why_fundamental: Why this tension is central

Return ONLY valid JSON, no markdown code blocks or explanation.

Example structure:
{{
  "domain_name": "Example Domain",
  "core_question": "What is the central question?",
  "success_looks_like": "What success means",
  "vocabulary": {{
    "concept": "Thesis",
    "dialectic": "Trade-off",
    "actor": "Player"
  }},
  "template_base": "investment",
  "seed_concepts": [
    {{
      "name": "Example Concept",
      "definition": "What this concept means",
      "why_fundamental": "Why it matters"
    }}
  ],
  "seed_dialectics": [
    {{
      "name": "Pole A ↔ Pole B",
      "pole_a": "Description of first pole",
      "pole_b": "Description of second pole",
      "why_fundamental": "Why this tension exists"
    }}
  ]
}}"""

    def _build_qa_prompt(
        self,
        question: str,
        domain_context: Dict[str, Any],
        units: List[Dict[str, Any]],
        dialogue_history: List[Dict[str, Any]]
    ) -> str:
        """Build the Q&A prompt."""
        # Format units by type
        concepts = [u for u in units if u.get("unit_type") == "concept"]
        dialectics = [u for u in units if u.get("unit_type") == "dialectic"]
        actors = [u for u in units if u.get("unit_type") == "actor"]

        vocab = domain_context.get("vocabulary", {})
        concept_term = vocab.get("concept", "Concept")
        dialectic_term = vocab.get("dialectic", "Tension")
        actor_term = vocab.get("actor", "Actor")

        # Format recent dialogue
        recent_dialogue = ""
        if dialogue_history:
            for turn in dialogue_history[-5:]:  # Last 5 turns
                role = "User" if turn.get("turn_type") == "user_question" else "System"
                recent_dialogue += f"{role}: {turn.get('content', '')}\n\n"

        return f"""You are a strategic thinking assistant working within a specific domain framework.

DOMAIN: {domain_context.get('name', 'Unknown')}
CORE QUESTION: {domain_context.get('core_question', 'Unknown')}

CURRENT FRAMEWORK:

{concept_term}s ({len(concepts)}):
{self._format_units(concepts)}

{dialectic_term}s ({len(dialectics)}):
{self._format_units(dialectics)}

{actor_term}s ({len(actors)}):
{self._format_units(actors)}

{f"RECENT DIALOGUE:{chr(10)}{recent_dialogue}" if recent_dialogue else ""}

---

USER QUESTION: {question}

---

Respond to this question using the framework context. Your response should:
1. Draw on existing concepts, tensions, and actors when relevant
2. Identify implications for the framework
3. Suggest concrete next actions if appropriate

Return a JSON object with:
{{
  "response": "Your thoughtful response to the question",
  "implications": "What this means for the strategic framework (or null if none)",
  "framework_references": ["List of unit names referenced in your response"],
  "suggested_actions": [
    {{
      "action_type": "create_concept|create_dialectic|create_actor|refine_unit|ask_followup",
      "parameters": {{"name": "...", "definition": "...", etc.}},
      "rationale": "Why this action"
    }}
  ]
}}

Return ONLY valid JSON."""

    def _build_suggestion_prompt(
        self,
        domain_context: Dict[str, Any],
        units: List[Dict[str, Any]],
        focus: Optional[str]
    ) -> str:
        """Build the suggestion prompt."""
        vocab = domain_context.get("vocabulary", {})

        concepts = [u for u in units if u.get("unit_type") == "concept"]
        dialectics = [u for u in units if u.get("unit_type") == "dialectic"]
        actors = [u for u in units if u.get("unit_type") == "actor"]

        return f"""You are a strategic framework development advisor.

DOMAIN: {domain_context.get('name', 'Unknown')}
CORE QUESTION: {domain_context.get('core_question', 'Unknown')}

CURRENT STATE:
- {vocab.get('concept', 'Concept')}s: {len(concepts)}
- {vocab.get('dialectic', 'Tension')}s: {len(dialectics)}
- {vocab.get('actor', 'Actor')}s: {len(actors)}

EXISTING UNITS:
{self._format_units(units)}

{f"FOCUS AREA: {focus}" if focus else ""}

---

Based on the current state of this strategic framework, suggest next steps for development.

Return a JSON object with:
{{
  "assessment": "Brief assessment of framework maturity and gaps",
  "suggestions": ["List of 3-5 actionable suggestions in natural language"],
  "priority_actions": [
    {{
      "action_type": "create_concept|create_dialectic|create_actor|refine_unit|explore_question",
      "parameters": {{"name": "...", "definition": "...", etc.}},
      "rationale": "Why this is a priority"
    }}
  ]
}}

Return ONLY valid JSON."""

    def _format_units(self, units: List[Dict[str, Any]]) -> str:
        """Format units for prompt context."""
        if not units:
            return "(none yet)"

        lines = []
        for u in units:
            name = u.get("name", "Unnamed")
            definition = u.get("definition", "")
            if definition:
                lines.append(f"- {name}: {definition[:100]}...")
            else:
                lines.append(f"- {name}")
        return "\n".join(lines)

    def _parse_bootstrap_response(self, response_text: str) -> Dict[str, Any]:
        """Parse bootstrap response JSON."""
        try:
            # Try to find JSON in the response
            text = response_text.strip()

            # Remove markdown code blocks if present
            if text.startswith("```"):
                lines = text.split("\n")
                # Find start and end of code block
                start = 1 if lines[0].startswith("```") else 0
                end = len(lines) - 1 if lines[-1].strip() == "```" else len(lines)
                text = "\n".join(lines[start:end])

            return json.loads(text)
        except json.JSONDecodeError as e:
            # Return error structure
            return {
                "error": f"Failed to parse LLM response: {str(e)}",
                "raw_response": response_text[:500]
            }

    def _parse_qa_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Q&A response JSON."""
        try:
            text = response_text.strip()
            if text.startswith("```"):
                lines = text.split("\n")
                start = 1 if lines[0].startswith("```") else 0
                end = len(lines) - 1 if lines[-1].strip() == "```" else len(lines)
                text = "\n".join(lines[start:end])

            return json.loads(text)
        except json.JSONDecodeError:
            # Fallback: return raw response as text
            return {
                "response": response_text,
                "implications": None,
                "suggested_actions": []
            }

    def _parse_suggestion_response(self, response_text: str) -> Dict[str, Any]:
        """Parse suggestion response JSON."""
        try:
            text = response_text.strip()
            if text.startswith("```"):
                lines = text.split("\n")
                start = 1 if lines[0].startswith("```") else 0
                end = len(lines) - 1 if lines[-1].strip() == "```" else len(lines)
                text = "\n".join(lines[start:end])

            return json.loads(text)
        except json.JSONDecodeError:
            return {
                "suggestions": ["Unable to generate suggestions at this time"],
                "priority_actions": []
            }
