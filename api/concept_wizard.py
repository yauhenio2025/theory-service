"""
Concept Setup Wizard API - Novel Concept Creation with Claude Opus 4.5

Uses extended thinking (32k budget) to:
1. Analyze user notes and generate adaptive questions
2. Process answers into comprehensive concept data
3. Populate Genesis dimension tables

Design Principles:
- prn_staged_adaptive_interrogation: Questions build on previous answers
- prn_proactive_insufficiency_signaling: Signal when more input needed
- prn_precision_forcing_interrogation: Force definitional precision
"""

import os
import json
import asyncio
from typing import Optional, List, Dict, Any
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from anthropic import Anthropic

from .database import get_db

router = APIRouter(prefix="/concepts/wizard", tags=["concept-wizard"])

# Claude client
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Model configuration
MODEL = "claude-opus-4-5-20250514"
THINKING_BUDGET = 32000
MAX_OUTPUT = 16000


# =============================================================================
# SCHEMAS
# =============================================================================

class AnalyzeNotesRequest(BaseModel):
    concept_name: str
    notes: Optional[str] = None
    source_id: Optional[int] = None


class StartWizardRequest(BaseModel):
    concept_name: str
    source_id: Optional[int] = None


class ProcessAnswersRequest(BaseModel):
    concept_name: str
    notes: Optional[str] = None
    answers: Dict[str, Any]
    source_id: Optional[int] = None


class SaveConceptRequest(BaseModel):
    concept_data: Dict[str, Any]
    source_id: Optional[int] = None


class QuestionOption(BaseModel):
    value: str
    label: str
    description: Optional[str] = None


class WizardQuestion(BaseModel):
    id: str
    text: str
    type: str = "open_ended"  # open_ended, multiple_choice, multi_select, scale
    stage: int = 1
    options: Optional[List[QuestionOption]] = None
    help: Optional[str] = None
    example: Optional[str] = None
    rationale: Optional[str] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    placeholder: Optional[str] = None
    rows: Optional[int] = None
    required: bool = True


# =============================================================================
# DEFAULT QUESTIONS (used when no notes provided)
# =============================================================================

DEFAULT_QUESTIONS = [
    WizardQuestion(
        id="core_definition",
        text="In one paragraph, provide your working definition of this concept.",
        type="open_ended",
        stage=1,
        help="This doesn't need to be perfect. We'll refine it throughout the process. Aim for clarity over comprehensiveness.",
        example="Technological sovereignty refers to the capacity of a political entity to exercise meaningful control over the technological systems upon which its economy, security, and social functioning depend...",
        min_length=100,
        rows=5,
        rationale="Forces initial precision; becomes anchor for later refinement"
    ),
    WizardQuestion(
        id="genesis_type",
        text="How would you characterize the origin of this concept?",
        type="multiple_choice",
        stage=1,
        options=[
            QuestionOption(value="theoretical_innovation", label="A new theoretical framework or lens", description="You are proposing a new way of understanding something"),
            QuestionOption(value="empirical_discovery", label="A pattern discovered through observation", description="You noticed something in the world that needs naming"),
            QuestionOption(value="synthetic_unification", label="A synthesis of previously separate ideas", description="You are combining existing concepts in a new way"),
            QuestionOption(value="paradigm_shift", label="A fundamental reconceptualization", description="You are challenging basic assumptions in a field"),
        ],
        help="This helps us understand what kind of support and validation your concept needs.",
        rationale="Understanding origin type shapes how we approach validation"
    ),
    WizardQuestion(
        id="problem_space",
        text="What problem or gap in understanding does this concept address? Why do we need a new concept for this?",
        type="open_ended",
        stage=2,
        help="A concept needs to DO something. What can we understand, explain, or do with this concept that we couldn't before?",
        min_length=100,
        rows=4,
        rationale="Justifies concept's existence; clarifies its purpose"
    ),
    WizardQuestion(
        id="failed_alternatives",
        text="What existing concepts have you tried using for this phenomenon? Why are they inadequate?",
        type="open_ended",
        stage=2,
        help="List at least 2-3 existing concepts you considered and explain why each falls short.",
        example="Digital sovereignty: too narrow, focused on data/software. National security: too broad, loses technological specificity...",
        min_length=80,
        rows=4,
        rationale="Forces confrontation with existing vocabulary"
    ),
    WizardQuestion(
        id="most_confused_with",
        text="What existing concept is this MOST likely to be confused with?",
        type="open_ended",
        stage=3,
        help="Pick ONE concept that poses the greatest confusion risk.",
        placeholder="e.g., Digital Sovereignty",
        rationale="Identifies primary differentiation target"
    ),
    WizardQuestion(
        id="confusion_consequence",
        text="Why is this confusion problematic? What understanding is lost if someone treats your concept as equivalent to the one you just mentioned?",
        type="open_ended",
        stage=3,
        help="Be specific about what analysis, insight, or action would be missed.",
        min_length=80,
        rows=4,
        rationale="Makes differentiation concrete and consequential"
    ),
    WizardQuestion(
        id="paradigmatic_case",
        text="What is the single best example that captures the essence of this concept? Describe it in detail.",
        type="open_ended",
        stage=4,
        help="Think: if you had to explain this concept to someone new and could only use ONE example, what would it be?",
        example="The European 5G and Huawei dilemma. European nations faced decisions about allowing Huawei equipment in their 5G networks...",
        min_length=150,
        rows=6,
        rationale="Paradigmatic cases are crucial for concept teaching"
    ),
    WizardQuestion(
        id="implicit_domain",
        text="In what domain do you see this concept operating WITHOUT being explicitly named? What proxy terms or euphemisms are used instead?",
        type="open_ended",
        stage=4,
        help="Where do people discuss this phenomenon without having the vocabulary? What words do they use instead?",
        example="Semiconductor policy: discussions of 'supply chain security,' 'strategic autonomy,' 'onshoring' all circle around technological sovereignty without naming it...",
        min_length=100,
        rows=4,
        rationale="Essential for document search and implicit instance discovery"
    ),
    WizardQuestion(
        id="core_claim",
        text="What is the most fundamental claim about reality that your concept makes? What must be TRUE for this concept to be meaningful?",
        type="open_ended",
        stage=5,
        help="A concept makes claims about how the world works. What's yours?",
        example="Technological dependencies can constitute a form of sovereignty loss that is distinct from and not reducible to economic, political, or military dependencies.",
        min_length=80,
        rows=4,
        rationale="Forces articulation of core commitment; enables testing"
    ),
    WizardQuestion(
        id="falsification_condition",
        text="What would prove this concept useless or wrong? What would have to be true for you to abandon it?",
        type="open_ended",
        stage=5,
        help="Be honest about what would make you give up this concept. A concept that can't be wrong isn't saying anything.",
        min_length=80,
        rows=4,
        rationale="Forces intellectual honesty; enables refutation"
    ),
    WizardQuestion(
        id="recognition_pattern",
        text="How can we recognize an implicit instance of this concept in a text that doesn't use the term? What patterns should we look for?",
        type="open_ended",
        stage=6,
        help="Describe linguistic patterns, argument structures, or situational descriptions that indicate this concept is in play.",
        example="Look for: arguments that technology choices have political/sovereignty implications beyond economics; descriptions of lock-in that constrains strategic options...",
        min_length=100,
        rows=5,
        rationale="Essential for LLM-assisted document analysis"
    ),
]


# =============================================================================
# STREAMING HELPERS
# =============================================================================

async def stream_thinking_response(messages: List[dict], system: str = None):
    """
    Stream response with extended thinking from Opus 4.5.
    Yields SSE events for thinking and text blocks.
    """
    try:
        # Use streaming for extended thinking
        with client.messages.stream(
            model=MODEL,
            max_tokens=MAX_OUTPUT,
            thinking={
                "type": "enabled",
                "budget_tokens": THINKING_BUDGET
            },
            system=system or "You are helping a user articulate a novel theoretical concept.",
            messages=messages
        ) as stream:
            for event in stream:
                if event.type == "content_block_start":
                    if hasattr(event.content_block, 'type'):
                        if event.content_block.type == "thinking":
                            yield f"data: {json.dumps({'type': 'thinking_start'})}\n\n"
                        elif event.content_block.type == "text":
                            yield f"data: {json.dumps({'type': 'text_start'})}\n\n"

                elif event.type == "content_block_delta":
                    if hasattr(event.delta, 'thinking'):
                        yield f"data: {json.dumps({'type': 'thinking', 'content': event.delta.thinking})}\n\n"
                    elif hasattr(event.delta, 'text'):
                        yield f"data: {json.dumps({'type': 'text', 'content': event.delta.text})}\n\n"

            # Get final message for complete data
            final = stream.get_final_message()

            # Extract the text content
            response_text = ""
            for block in final.content:
                if hasattr(block, 'text'):
                    response_text = block.text
                    break

            yield f"data: {json.dumps({'type': 'complete', 'data': parse_wizard_response(response_text)})}\n\n"

    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    yield "data: [DONE]\n\n"


def parse_wizard_response(text: str) -> dict:
    """Parse JSON from LLM response, handling markdown code blocks."""
    # Try to find JSON in the response
    if "```json" in text:
        start = text.find("```json") + 7
        end = text.find("```", start)
        text = text[start:end].strip()
    elif "```" in text:
        start = text.find("```") + 3
        end = text.find("```", start)
        text = text[start:end].strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Return as raw text if not JSON
        return {"raw_response": text}


# =============================================================================
# PROMPTS
# =============================================================================

ANALYZE_NOTES_SYSTEM = """You are an expert in conceptual analysis and knowledge elicitation, helping users articulate novel theoretical concepts that don't yet exist in public discourse.

Your task is to analyze the user's notes about their concept and generate adaptive follow-up questions that will help fully articulate the concept.

Design Principles:
- Staged Adaptive Interrogation: Generate questions that build on what you learn from their notes
- Precision-Forcing: Ask questions that force definitional clarity
- Proactive Insufficiency Signaling: Identify gaps in the notes and ask about them

Output Format: Return a JSON object with:
{
  "analysis_summary": "Brief summary of what you understood from the notes",
  "identified_gaps": ["list", "of", "gaps"],
  "questions": [
    {
      "id": "unique_id",
      "text": "The question to ask",
      "type": "open_ended|multiple_choice|multi_select|scale",
      "stage": 1-6,
      "options": [...] // for choice questions
      "help": "Help text for the user",
      "example": "Example answer if helpful",
      "rationale": "Why this question matters",
      "min_length": 100, // for open_ended
      "rows": 4 // textarea rows
    }
  ]
}

Generate 8-12 questions that are tailored to what the user has already told you. Skip questions whose answers are clearly provided in the notes. Focus on gaps and areas needing elaboration."""


PROCESS_ANSWERS_SYSTEM = """You are an expert in conceptual analysis, synthesizing user answers into a comprehensive concept definition.

Your task is to take the user's answers to wizard questions and synthesize them into a structured concept definition that populates the "Genesis Dimension" schema.

The user is introducing a NOVEL concept that doesn't exist in public discourse yet. This means:
- You cannot rely on external knowledge about this concept
- Everything must come from what the user has provided
- You should flag areas where more information would be helpful

Output Format: Return a JSON object with:
{
  "more_questions": false, // Set to true if critical gaps need addressing
  "questions": [...], // Only if more_questions is true
  "concept": {
    "name": "Concept Name",
    "definition": "Full synthesized definition (2-3 paragraphs)",
    "category": "Category if determinable",
    "genesis": {
      "type": "theoretical_innovation|empirical_discovery|synthetic_unification|paradigm_shift",
      "lineage": "Theoretical traditions it builds on",
      "break_from": "What it breaks from (if applicable)",
      "novelty_claim": "Why this is genuinely new"
    },
    "problem_space": {
      "gap": "The gap this concept fills",
      "failed_alternatives": ["concepts", "that", "failed"],
      "urgency": "Why now"
    },
    "differentiations": [
      {
        "confused_with": "Other Concept",
        "confusion_type": "subset|superset|synonym|false_opposition",
        "difference": "Key distinction",
        "what_lost": "What's lost in confusion"
      }
    ],
    "paradigmatic_case": {
      "name": "Case name",
      "description": "Full description",
      "why": "Why this is paradigmatic",
      "features": ["exhibited", "features"]
    },
    "implicit_domains": [
      {
        "domain": "Domain name",
        "type": "academic|policy|industry|media|everyday",
        "proxy_terms": ["terms", "used", "instead"],
        "manifestation": "How concept appears here"
      }
    ],
    "core_claims": [
      {
        "type": "ontological|causal|normative|methodological",
        "statement": "The claim",
        "if_false": "Consequence if false"
      }
    ],
    "recognition_markers": [
      {
        "type": "linguistic|structural|situational|argumentative",
        "description": "How to recognize implicit instances",
        "pattern": "Search pattern if applicable"
      }
    ],
    "schema_gaps": ["Areas", "needing", "more", "data"]
  }
}

Be thorough but only include what can be derived from the user's answers. Don't fabricate details."""


# =============================================================================
# ENDPOINTS
# =============================================================================

@router.post("/start")
async def start_wizard(request: StartWizardRequest):
    """Start wizard without notes - return default questions."""
    # Return default questions (convert to dict format)
    questions = [q.model_dump() for q in DEFAULT_QUESTIONS]

    return {
        "status": "ready",
        "concept_name": request.concept_name,
        "questions": questions
    }


@router.post("/analyze-notes")
async def analyze_notes(request: AnalyzeNotesRequest):
    """Analyze user notes and generate adaptive questions."""
    if not request.notes or len(request.notes.strip()) < 50:
        # Not enough notes - return default questions
        questions = [q.model_dump() for q in DEFAULT_QUESTIONS]
        return StreamingResponse(
            iter([f"data: {json.dumps({'type': 'complete', 'data': {'questions': questions}})}\n\ndata: [DONE]\n\n"]),
            media_type="text/event-stream"
        )

    # Prepare messages for LLM
    messages = [
        {
            "role": "user",
            "content": f"""I'm introducing a novel concept called "{request.concept_name}".

Here are my initial notes about this concept:

{request.notes}

Please analyze these notes and generate adaptive follow-up questions that will help me fully articulate this concept. Focus on gaps and areas needing elaboration. Skip questions whose answers are already clear from my notes."""
        }
    ]

    return StreamingResponse(
        stream_thinking_response(messages, ANALYZE_NOTES_SYSTEM),
        media_type="text/event-stream"
    )


@router.post("/process")
async def process_answers(request: ProcessAnswersRequest):
    """Process wizard answers into concept data."""

    # Build context from notes and answers
    context_parts = []

    if request.notes:
        context_parts.append(f"Initial Notes:\n{request.notes}")

    context_parts.append("Wizard Answers:")
    for q_id, answer in request.answers.items():
        if isinstance(answer, list):
            answer_str = ", ".join(answer)
        else:
            answer_str = str(answer)
        context_parts.append(f"- {q_id}: {answer_str}")

    user_content = f"""I'm creating a novel concept called "{request.concept_name}".

{chr(10).join(context_parts)}

Please synthesize these answers into a comprehensive concept definition. If critical information is missing, set more_questions to true and provide follow-up questions."""

    messages = [{"role": "user", "content": user_content}]

    return StreamingResponse(
        stream_thinking_response(messages, PROCESS_ANSWERS_SYSTEM),
        media_type="text/event-stream"
    )


@router.post("/save")
async def save_concept(request: SaveConceptRequest, db: AsyncSession = Depends(get_db)):
    """Save the completed concept to the database."""
    from .models import Concept, ConceptStatus

    concept_data = request.concept_data

    # Create the main concept
    concept = Concept(
        term=concept_data.get("name", "Untitled Concept"),
        definition=concept_data.get("definition", ""),
        category=concept_data.get("category"),
        status=ConceptStatus.DRAFT,
        source_id=request.source_id,
        # Store Genesis data in metadata (or separate tables if they exist)
        # For now, we'll add key fields to the definition
    )

    # Enrich definition with genesis info if available
    if concept_data.get("genesis"):
        genesis = concept_data["genesis"]
        enriched_def = concept.definition
        if genesis.get("lineage"):
            enriched_def += f"\n\n**Theoretical Lineage:** {genesis['lineage']}"
        if genesis.get("novelty_claim"):
            enriched_def += f"\n\n**Novelty Claim:** {genesis['novelty_claim']}"
        concept.definition = enriched_def

    db.add(concept)
    await db.commit()
    await db.refresh(concept)

    # TODO: If Genesis dimension tables exist, populate them here
    # For now, return success with the basic concept

    return {
        "status": "success",
        "concept": {
            "id": concept.id,
            "term": concept.term,
            "definition": concept.definition,
            "status": concept.status.value,
            "genesis_data": concept_data.get("genesis"),
            "differentiations": concept_data.get("differentiations"),
            "recognition_markers": concept_data.get("recognition_markers")
        }
    }
