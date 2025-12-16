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
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

# Set up logging
logger = logging.getLogger(__name__)
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from anthropic import Anthropic

from .database import get_db

router = APIRouter(prefix="/concepts/wizard", tags=["concept-wizard"])

# Claude client - initialize lazily to handle missing API key gracefully
_client = None

def get_claude_client():
    """Get Claude client, raising helpful error if API key missing."""
    global _client
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set. Please configure it in Render.")
    if _client is None:
        _client = Anthropic(api_key=api_key)
    return _client

# Model configuration
MODEL = "claude-opus-4-5-20251101"  # Correct model ID for Opus 4.5
THINKING_BUDGET = 32000
MAX_OUTPUT = 64000  # Must be > THINKING_BUDGET


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
    """Enhanced option for multiple choice questions."""
    value: str
    label: str
    description: Optional[str] = None
    exclusivity_group: Optional[int] = None  # Mutually exclusive options share same group
    implications: Optional[str] = None       # What choosing this option implies for the concept


class WizardQuestion(BaseModel):
    """Enhanced wizard question with adaptive features."""
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

    # Enhanced features for adaptive questioning
    allow_custom_response: bool = True  # Enable write-in for choice questions
    custom_response_categories: Optional[List[str]] = None  # ["Alternative Answer", "Comment", "Refinement"]
    allow_mark_dialectic: bool = False  # Can user mark this as a productive tension
    dialectic_hint: Optional[str] = None  # Hint for when to mark as dialectic
    depends_on: Optional[List[str]] = None  # Question IDs this depends on
    skip_if: Optional[Dict[str, Any]] = None  # Conditional skip logic


class Tension(BaseModel):
    """A detected or user-marked productive tension."""
    description: str
    pole_a: str
    pole_b: str
    marked_as_dialectic: bool = False
    user_note: Optional[str] = None


class InterimAnalysis(BaseModel):
    """Intermediate understanding shown between stages."""
    understanding_summary: str  # "Based on your answers, I understand..."
    key_commitments: List[str]  # Core positions you've taken
    tensions_detected: List[Tension]  # Potential dialectics
    gaps_identified: List[str]  # What we still need to know
    preliminary_definition: str  # Working definition so far


class InterimAnalysisResponse(BaseModel):
    """Response containing interim analysis and next stage questions."""
    interim_analysis: InterimAnalysis
    next_stage_questions: List['WizardQuestion']


class AnswerWithMeta(BaseModel):
    """Answer with metadata for custom responses and dialectics."""
    question_id: str
    selected_options: Optional[List[str]] = None  # For choice questions
    text_answer: Optional[str] = None  # For open-ended
    custom_response: Optional[str] = None  # Write-in text
    custom_response_category: Optional[str] = None  # Category of write-in
    is_dialectic: bool = False
    dialectic_pole_a: Optional[str] = None
    dialectic_pole_b: Optional[str] = None
    dialectic_note: Optional[str] = None


# =============================================================================
# STAGE 1 QUESTIONS: Genesis & Problem Space
# =============================================================================

STAGE1_QUESTIONS = [
    WizardQuestion(
        id="genesis_type",
        text="How would you characterize the origin of this concept?",
        type="multiple_choice",
        stage=1,
        options=[
            QuestionOption(
                value="theoretical_innovation",
                label="A new theoretical framework or lens",
                description="You are proposing a new way of understanding something",
                implications="Needs strong theoretical grounding and clear differentiation from existing frameworks"
            ),
            QuestionOption(
                value="empirical_discovery",
                label="A pattern discovered through observation",
                description="You noticed something in the world that needs naming",
                implications="Needs concrete examples and documented evidence of the pattern"
            ),
            QuestionOption(
                value="synthetic_unification",
                label="A synthesis of previously separate ideas",
                description="You are combining existing concepts in a new way",
                implications="Needs to show what's gained by the synthesis that separate concepts miss"
            ),
            QuestionOption(
                value="paradigm_shift",
                label="A fundamental reconceptualization",
                description="You are challenging basic assumptions in a field",
                implications="Needs to identify what assumptions are challenged and why"
            ),
            QuestionOption(
                value="normative_reframing",
                label="A normative or evaluative reframing",
                description="You are proposing a new way to evaluate or judge something",
                implications="Needs clear criteria and distinction from related evaluative concepts"
            ),
        ],
        help="This helps us understand what kind of support and validation your concept needs.",
        rationale="Understanding origin type shapes how we approach validation",
        allow_custom_response=True,
        custom_response_categories=["Mixed/Complex origin", "Other type"],
        allow_mark_dialectic=True,
        dialectic_hint="If you're torn between origins (e.g., both theoretical AND empirical), this may be a productive tension worth exploring"
    ),
    WizardQuestion(
        id="core_definition",
        text="In one paragraph, provide your working definition of this concept.",
        type="open_ended",
        stage=1,
        help="This doesn't need to be perfect. We'll refine it throughout the process. Aim for clarity over comprehensiveness.",
        example="Technological sovereignty refers to the capacity of a political entity to exercise meaningful control over the technological systems upon which its economy, security, and social functioning depend...",
        min_length=100,
        rows=5,
        rationale="Forces initial precision; becomes anchor for later refinement",
        allow_custom_response=False  # Already open-ended
    ),
    WizardQuestion(
        id="problem_addressed",
        text="What problem or gap in understanding does this concept address?",
        type="open_ended",
        stage=1,
        help="A concept needs to DO something. What can we understand, explain, or do with this concept that we couldn't before?",
        min_length=80,
        rows=4,
        rationale="Justifies concept's existence; clarifies its purpose",
        allow_custom_response=False
    ),
    WizardQuestion(
        id="adjacent_concepts",
        text="Which existing concepts come closest to what you're describing?",
        type="multi_select",
        stage=1,
        options=[
            # Common conceptual neighbors - user can add their own
            QuestionOption(value="sovereignty", label="Sovereignty", description="Control over territory/decisions", exclusivity_group=None),
            QuestionOption(value="autonomy", label="Autonomy", description="Self-governance, independence", exclusivity_group=None),
            QuestionOption(value="dependency", label="Dependency", description="Reliance on external entities", exclusivity_group=None),
            QuestionOption(value="power", label="Power", description="Capacity to influence or control", exclusivity_group=None),
            QuestionOption(value="agency", label="Agency", description="Capacity for action", exclusivity_group=None),
            QuestionOption(value="resilience", label="Resilience", description="Ability to recover from setbacks", exclusivity_group=None),
            QuestionOption(value="security", label="Security", description="Protection from threats", exclusivity_group=None),
            QuestionOption(value="freedom", label="Freedom", description="Absence of constraints", exclusivity_group=None),
        ],
        help="Select all that seem related - we'll explore differences in the next stage",
        rationale="Identifies differentiation targets for Stage 2",
        allow_custom_response=True,
        custom_response_categories=["Add concept not listed"]
    ),
    WizardQuestion(
        id="domain_scope",
        text="What is the primary domain or scope of this concept?",
        type="multiple_choice",
        stage=1,
        options=[
            QuestionOption(
                value="domain_specific",
                label="Domain-specific (applies to one field)",
                description="The concept is primarily relevant to a specific domain",
                implications="Will need to specify the domain and may need domain-specific validation",
                exclusivity_group=1
            ),
            QuestionOption(
                value="cross_domain",
                label="Cross-domain (applies across multiple fields)",
                description="The concept spans multiple domains or disciplines",
                implications="Will need examples from multiple domains and care about different manifestations",
                exclusivity_group=1
            ),
            QuestionOption(
                value="meta_level",
                label="Meta-level (about how we think/analyze)",
                description="The concept is about methodology or cognition itself",
                implications="Will need to show its applicability and avoid being merely abstract",
                exclusivity_group=1
            ),
        ],
        help="Choose the scope that best fits. This affects how we approach examples and validation.",
        rationale="Scope determines validation approach",
        allow_custom_response=True,
        custom_response_categories=["Complex scope"],
        allow_mark_dialectic=True,
        dialectic_hint="If the concept operates at multiple levels (both domain-specific and meta), that's worth noting"
    ),
]


# =============================================================================
# STAGE 3 QUESTIONS: Grounding & Recognition (predefined, refined by Stage 2)
# =============================================================================

STAGE3_QUESTIONS = [
    WizardQuestion(
        id="paradigmatic_case",
        text="What is the single best example that captures the essence of this concept?",
        type="open_ended",
        stage=3,
        help="If you had to explain this concept using only ONE example, what would it be? Describe it in detail.",
        example="The European 5G and Huawei dilemma. European nations faced decisions about allowing Huawei equipment in their 5G networks...",
        min_length=150,
        rows=6,
        rationale="Paradigmatic cases are crucial for concept teaching",
        allow_custom_response=False
    ),
    WizardQuestion(
        id="implicit_domain",
        text="Where do you see this concept operating WITHOUT being explicitly named?",
        type="open_ended",
        stage=3,
        help="Where do people discuss this phenomenon without having the vocabulary? What proxy terms or euphemisms are used?",
        example="Semiconductor policy discussions use terms like 'supply chain security,' 'strategic autonomy,' 'onshoring' that circle around technological sovereignty without naming it...",
        min_length=100,
        rows=4,
        rationale="Essential for document search and implicit instance discovery",
        allow_custom_response=False
    ),
    WizardQuestion(
        id="recognition_markers",
        text="How can we recognize an implicit instance of this concept in a text that doesn't use the term?",
        type="open_ended",
        stage=3,
        help="Describe linguistic patterns, argument structures, or situational descriptions that indicate this concept is in play.",
        example="Look for: arguments that technology choices have political implications beyond economics; descriptions of lock-in that constrains strategic options...",
        min_length=100,
        rows=5,
        rationale="Essential for LLM-assisted document analysis",
        allow_custom_response=False
    ),
    WizardQuestion(
        id="core_claim",
        text="What is the most fundamental claim about reality that your concept makes?",
        type="open_ended",
        stage=3,
        help="A concept makes claims about how the world works. What must be TRUE for this concept to be meaningful?",
        example="Technological dependencies can constitute a form of sovereignty loss that is distinct from and not reducible to economic, political, or military dependencies.",
        min_length=80,
        rows=4,
        rationale="Forces articulation of core commitment; enables testing",
        allow_custom_response=False,
        allow_mark_dialectic=True,
        dialectic_hint="If your core claim exists in tension with another valid claim, that may be a productive dialectic"
    ),
    WizardQuestion(
        id="falsification_condition",
        text="What would prove this concept useless or wrong?",
        type="open_ended",
        stage=3,
        help="Be honest about what would make you give up this concept. A concept that can't be wrong isn't saying anything.",
        min_length=80,
        rows=4,
        rationale="Forces intellectual honesty; enables refutation",
        allow_custom_response=False
    ),
]


# =============================================================================
# DEFAULT QUESTIONS (legacy - used for backward compatibility)
# =============================================================================

DEFAULT_QUESTIONS = STAGE1_QUESTIONS + STAGE3_QUESTIONS


# =============================================================================
# STREAMING HELPERS
# =============================================================================

async def stream_thinking_response(messages: List[dict], system: str = None):
    """
    Stream response with extended thinking from Opus 4.5.
    Yields SSE events for thinking and text blocks.
    """
    try:
        # Get client (will raise if API key missing)
        client = get_claude_client()
        logger.info(f"Starting Claude stream with model {MODEL}, thinking budget {THINKING_BUDGET}")

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
        logger.error(f"Error in stream_thinking_response: {e}", exc_info=True)
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
# STAGED WIZARD PROMPTS
# =============================================================================

INTERIM_ANALYSIS_PROMPT = """You are an expert in conceptual analysis helping a user articulate a novel theoretical concept.

The user has completed Stage 1 questions about their concept "{concept_name}". Your task is to:
1. Synthesize their answers into an interim understanding
2. Identify key commitments they've made
3. Detect potential tensions (which might become productive dialectics)
4. Identify gaps that need addressing in Stage 2

## User's Stage 1 Answers:
{stage1_answers}

## Dialectics Marked by User:
{marked_dialectics}

Produce a JSON response with:
{{
    "interim_analysis": {{
        "understanding_summary": "Based on your answers, I understand that [concept_name] is... (2-3 sentences)",
        "key_commitments": ["List 3-5 core positions the user has taken"],
        "tensions_detected": [
            {{
                "description": "Brief description of the tension",
                "pole_a": "One side of the tension",
                "pole_b": "The opposing side",
                "marked_as_dialectic": true/false
            }}
        ],
        "gaps_identified": ["Aspects that need more exploration in Stage 2"],
        "preliminary_definition": "A working 1-paragraph definition based on what we know so far"
    }}
}}

Be specific to what the user actually said. Don't fabricate or assume beyond their answers."""


STAGE2_GENERATION_PROMPT = """Based on the user's Stage 1 answers about their novel concept "{concept_name}":

## Stage 1 Responses:
{stage1_summary}

## Interim Analysis:
{interim_analysis}

## Adjacent Concepts Selected:
{adjacent_concepts}

Generate 4-6 Stage 2 questions that:
1. **Probe specific gaps** identified in the interim analysis
2. **Sharpen distinctions** from the adjacent concepts they mentioned
3. **Test commitments** they've made to see if they hold under scrutiny
4. **Explore tensions** they flagged as dialectics or that you detected

For each question:
- Decide if it should be multiple_choice (when there are clear alternatives), multi_select, or open_ended
- For multiple choice: specify which options are mutually exclusive (same exclusivity_group number)
- Include "implications" for each option - what that choice means for the concept
- Set allow_mark_dialectic=true for questions that might reveal productive tensions

Output JSON array of questions:
{{
    "stage2_questions": [
        {{
            "id": "differentiation_from_X",
            "text": "How does {concept_name} differ from [adjacent concept]?",
            "type": "multiple_choice",
            "stage": 2,
            "options": [
                {{
                    "value": "narrower_scope",
                    "label": "Narrower scope",
                    "description": "Applies to a subset of cases",
                    "exclusivity_group": 1,
                    "implications": "Will need to specify what's included/excluded"
                }},
                {{
                    "value": "broader_scope",
                    "label": "Broader scope",
                    "description": "Encompasses more phenomena",
                    "exclusivity_group": 1,
                    "implications": "Must show what's gained by the broader framing"
                }}
            ],
            "help": "This distinction is important because...",
            "rationale": "Why we're asking this",
            "allow_custom_response": true,
            "custom_response_categories": ["Different relationship", "Complex"],
            "allow_mark_dialectic": true,
            "dialectic_hint": "Hint for when this might be a dialectic"
        }}
    ]
}}

Generate questions that are specific to THIS concept and what the user has said. Don't ask generic questions."""


STAGE3_REFINEMENT_PROMPT = """Based on the user's Stage 2 answers about "{concept_name}":

## Stage 1 + Stage 2 Context:
{full_context}

## Differentiations Made:
{differentiations}

## Tensions/Dialectics:
{dialectics}

The user will now answer Stage 3 questions about grounding and recognition.

Before they do, generate an "implications preview" that shows them what their Stage 2 choices mean:

{{
    "implications_preview": {{
        "definition_trajectory": "Based on your choices, the concept is moving toward... (summarize the definitional direction)",
        "key_differentiations": [
            {{
                "from_concept": "Adjacent concept",
                "distinction": "The key distinction",
                "consequence": "This means..."
            }}
        ],
        "remaining_tensions": ["Tensions that are still unresolved"],
        "grounding_focus": "For Stage 3, focus on... (guide for what examples/evidence to provide)"
    }}
}}

Be concrete and specific to what the user has actually said."""


# =============================================================================
# REQUEST SCHEMAS FOR STAGED WIZARD
# =============================================================================

class Stage1AnswersRequest(BaseModel):
    concept_name: str
    notes: Optional[str] = None
    answers: List[AnswerWithMeta]
    source_id: Optional[int] = None


class Stage2AnswersRequest(BaseModel):
    concept_name: str
    notes: Optional[str] = None
    stage1_answers: List[AnswerWithMeta]
    stage2_answers: List[AnswerWithMeta]
    interim_analysis: InterimAnalysis
    source_id: Optional[int] = None


class FinalizeRequest(BaseModel):
    concept_name: str
    notes: Optional[str] = None
    all_answers: Dict[str, List[AnswerWithMeta]]  # stage1, stage2, stage3
    interim_analysis: InterimAnalysis
    dialectics: List[Tension]
    source_id: Optional[int] = None


# =============================================================================
# ENDPOINTS
# =============================================================================

async def sse_response(data: dict):
    """Properly formatted SSE async generator."""
    yield f"data: {json.dumps({'type': 'complete', 'data': data})}\n\n"
    yield "data: [DONE]\n\n"


@router.post("/start")
async def start_wizard(request: StartWizardRequest):
    """Start wizard without notes - return default questions."""
    # Return default questions (convert to dict format)
    questions = [q.model_dump() for q in DEFAULT_QUESTIONS]

    response_data = {
        "status": "ready",
        "concept_name": request.concept_name,
        "questions": questions
    }
    return StreamingResponse(
        sse_response(response_data),
        media_type="text/event-stream"
    )


@router.post("/analyze-notes")
async def analyze_notes(request: AnalyzeNotesRequest):
    """Analyze user notes and generate adaptive questions."""
    if not request.notes or len(request.notes.strip()) < 50:
        # Not enough notes - return default questions
        questions = [q.model_dump() for q in DEFAULT_QUESTIONS]
        return StreamingResponse(
            sse_response({'questions': questions}),
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


# =============================================================================
# STAGED WIZARD ENDPOINTS
# =============================================================================

@router.post("/stage1")
async def get_stage1_questions(request: StartWizardRequest):
    """Get Stage 1 questions (Genesis & Problem Space)."""
    questions = [q.model_dump() for q in STAGE1_QUESTIONS]

    response_data = {
        "status": "stage1_ready",
        "concept_name": request.concept_name,
        "stage": 1,
        "stage_title": "Genesis & Problem Space",
        "stage_description": "Let's understand the origin and purpose of your concept.",
        "questions": questions
    }
    return StreamingResponse(
        sse_response(response_data),
        media_type="text/event-stream"
    )


def format_answers_for_prompt(answers: List[AnswerWithMeta]) -> str:
    """Format answers for LLM prompt."""
    formatted = []
    for ans in answers:
        parts = [f"Question: {ans.question_id}"]
        if ans.selected_options:
            parts.append(f"Selected: {', '.join(ans.selected_options)}")
        if ans.text_answer:
            parts.append(f"Answer: {ans.text_answer}")
        if ans.custom_response:
            category = ans.custom_response_category or "Custom"
            parts.append(f"[{category}]: {ans.custom_response}")
        if ans.is_dialectic:
            parts.append(f"DIALECTIC MARKED: {ans.dialectic_pole_a} vs {ans.dialectic_pole_b}")
            if ans.dialectic_note:
                parts.append(f"Note: {ans.dialectic_note}")
        formatted.append("\n".join(parts))
    return "\n\n".join(formatted)


def extract_dialectics_from_answers(answers: List[AnswerWithMeta]) -> List[Tension]:
    """Extract user-marked dialectics from answers."""
    dialectics = []
    for ans in answers:
        if ans.is_dialectic and ans.dialectic_pole_a and ans.dialectic_pole_b:
            dialectics.append(Tension(
                description=f"Tension in {ans.question_id}",
                pole_a=ans.dialectic_pole_a,
                pole_b=ans.dialectic_pole_b,
                marked_as_dialectic=True,
                user_note=ans.dialectic_note
            ))
    return dialectics


def extract_adjacent_concepts(answers: List[AnswerWithMeta]) -> str:
    """Extract adjacent concepts from Stage 1 answers."""
    for ans in answers:
        if ans.question_id == "adjacent_concepts":
            concepts = []
            if ans.selected_options:
                concepts.extend(ans.selected_options)
            if ans.custom_response:
                concepts.append(ans.custom_response)
            return ", ".join(concepts) if concepts else "None specified"
    return "None specified"


@router.post("/analyze-stage1")
async def analyze_stage1(request: Stage1AnswersRequest):
    """
    Analyze Stage 1 answers and generate:
    1. Interim analysis (what we understand so far)
    2. Dynamically generated Stage 2 questions
    """
    # Format answers for prompt
    stage1_text = format_answers_for_prompt(request.answers)
    marked_dialectics = extract_dialectics_from_answers(request.answers)
    adjacent_concepts = extract_adjacent_concepts(request.answers)

    dialectics_text = "\n".join([
        f"- {d.pole_a} vs {d.pole_b} ({d.user_note or 'no note'})"
        for d in marked_dialectics
    ]) if marked_dialectics else "None marked"

    # First LLM call: Generate interim analysis
    interim_prompt = INTERIM_ANALYSIS_PROMPT.format(
        concept_name=request.concept_name,
        stage1_answers=stage1_text,
        marked_dialectics=dialectics_text
    )

    # Second LLM call: Generate Stage 2 questions (will use interim analysis)
    async def stream_analysis_and_questions():
        try:
            client = get_claude_client()
            logger.info("Starting Stage 1 analysis with interim + Stage 2 generation")

            # Phase 1: Generate interim analysis
            yield f"data: {json.dumps({'type': 'phase', 'phase': 'interim_analysis'})}\n\n"

            with client.messages.stream(
                model=MODEL,
                max_tokens=MAX_OUTPUT,
                thinking={
                    "type": "enabled",
                    "budget_tokens": THINKING_BUDGET
                },
                system="You are an expert in conceptual analysis helping articulate novel theoretical concepts.",
                messages=[{"role": "user", "content": interim_prompt}]
            ) as stream:
                thinking_text = ""
                for event in stream:
                    if event.type == "content_block_delta":
                        if hasattr(event.delta, 'thinking'):
                            thinking_text += event.delta.thinking
                            yield f"data: {json.dumps({'type': 'thinking', 'content': event.delta.thinking})}\n\n"

                final = stream.get_final_message()
                interim_text = ""
                for block in final.content:
                    if hasattr(block, 'text'):
                        interim_text = block.text
                        break

            interim_data = parse_wizard_response(interim_text)
            interim_analysis = interim_data.get("interim_analysis", {})

            yield f"data: {json.dumps({'type': 'interim_complete', 'data': interim_analysis})}\n\n"

            # Phase 2: Generate Stage 2 questions based on interim
            yield f"data: {json.dumps({'type': 'phase', 'phase': 'stage2_generation'})}\n\n"

            stage2_prompt = STAGE2_GENERATION_PROMPT.format(
                concept_name=request.concept_name,
                stage1_summary=stage1_text,
                interim_analysis=json.dumps(interim_analysis, indent=2),
                adjacent_concepts=adjacent_concepts
            )

            with client.messages.stream(
                model=MODEL,
                max_tokens=MAX_OUTPUT,
                thinking={
                    "type": "enabled",
                    "budget_tokens": THINKING_BUDGET
                },
                system="You are an expert in conceptual analysis generating adaptive follow-up questions.",
                messages=[{"role": "user", "content": stage2_prompt}]
            ) as stream:
                for event in stream:
                    if event.type == "content_block_delta":
                        if hasattr(event.delta, 'thinking'):
                            yield f"data: {json.dumps({'type': 'thinking', 'content': event.delta.thinking})}\n\n"

                final = stream.get_final_message()
                stage2_text = ""
                for block in final.content:
                    if hasattr(block, 'text'):
                        stage2_text = block.text
                        break

            stage2_data = parse_wizard_response(stage2_text)
            stage2_questions = stage2_data.get("stage2_questions", [])

            # Return complete response
            complete_data = {
                'type': 'complete',
                'data': {
                    'status': 'stage2_ready',
                    'concept_name': request.concept_name,
                    'stage': 2,
                    'stage_title': 'Differentiation & Clarification',
                    'stage_description': "Let's sharpen the distinctions and explore tensions.",
                    'interim_analysis': interim_analysis,
                    'marked_dialectics': [d.model_dump() for d in marked_dialectics],
                    'questions': stage2_questions
                }
            }
            yield f"data: {json.dumps(complete_data)}\n\n"

        except Exception as e:
            logger.error(f"Error in analyze_stage1: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_analysis_and_questions(),
        media_type="text/event-stream"
    )


@router.post("/analyze-stage2")
async def analyze_stage2(request: Stage2AnswersRequest):
    """
    Analyze Stage 2 answers and generate:
    1. Implications preview (what the choices mean)
    2. Refined Stage 3 questions
    """
    # Combine Stage 1 and Stage 2 answers
    all_answers = request.stage1_answers + request.stage2_answers
    full_context = format_answers_for_prompt(all_answers)
    all_dialectics = extract_dialectics_from_answers(all_answers)

    # Extract differentiation info from Stage 2 answers
    differentiations = []
    for ans in request.stage2_answers:
        if "differentiation" in ans.question_id:
            diff_info = {
                "question": ans.question_id,
                "choice": ", ".join(ans.selected_options) if ans.selected_options else ans.text_answer,
                "custom_note": ans.custom_response
            }
            differentiations.append(diff_info)

    async def stream_implications_and_stage3():
        try:
            client = get_claude_client()

            yield f"data: {json.dumps({'type': 'phase', 'phase': 'implications_preview'})}\n\n"

            implications_prompt = STAGE3_REFINEMENT_PROMPT.format(
                concept_name=request.concept_name,
                full_context=full_context,
                differentiations=json.dumps(differentiations, indent=2),
                dialectics=json.dumps([d.model_dump() for d in all_dialectics], indent=2)
            )

            with client.messages.stream(
                model=MODEL,
                max_tokens=MAX_OUTPUT,
                thinking={
                    "type": "enabled",
                    "budget_tokens": THINKING_BUDGET
                },
                system="You are an expert in conceptual analysis showing implications of definitional choices.",
                messages=[{"role": "user", "content": implications_prompt}]
            ) as stream:
                for event in stream:
                    if event.type == "content_block_delta":
                        if hasattr(event.delta, 'thinking'):
                            yield f"data: {json.dumps({'type': 'thinking', 'content': event.delta.thinking})}\n\n"

                final = stream.get_final_message()
                impl_text = ""
                for block in final.content:
                    if hasattr(block, 'text'):
                        impl_text = block.text
                        break

            impl_data = parse_wizard_response(impl_text)
            implications_preview = impl_data.get("implications_preview", {})

            # Return Stage 3 questions (predefined but could be customized based on context)
            stage3_questions = [q.model_dump() for q in STAGE3_QUESTIONS]

            complete_data = {
                'type': 'complete',
                'data': {
                    'status': 'stage3_ready',
                    'concept_name': request.concept_name,
                    'stage': 3,
                    'stage_title': 'Grounding & Recognition',
                    'stage_description': "Let's establish how to recognize and validate this concept.",
                    'implications_preview': implications_preview,
                    'dialectics': [d.model_dump() for d in all_dialectics],
                    'questions': stage3_questions
                }
            }
            yield f"data: {json.dumps(complete_data)}\n\n"

        except Exception as e:
            logger.error(f"Error in analyze_stage2: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_implications_and_stage3(),
        media_type="text/event-stream"
    )


@router.post("/finalize")
async def finalize_concept(request: FinalizeRequest):
    """
    Final synthesis of all stages into a complete concept definition.
    """
    # Combine all answers
    all_answers_flat = []
    for stage_name, answers in request.all_answers.items():
        all_answers_flat.extend(answers)

    full_context = format_answers_for_prompt(all_answers_flat)

    async def stream_final_synthesis():
        try:
            client = get_claude_client()

            yield f"data: {json.dumps({'type': 'phase', 'phase': 'final_synthesis'})}\n\n"

            synthesis_prompt = f"""Synthesize all the user's answers into a comprehensive concept definition for "{request.concept_name}".

## User's Initial Notes:
{request.notes or "(No initial notes provided)"}

## All Wizard Answers (Stages 1-3):
{full_context}

## Interim Analysis:
{json.dumps(request.interim_analysis.model_dump(), indent=2)}

## Dialectics/Tensions Identified:
{json.dumps([d.model_dump() for d in request.dialectics], indent=2)}

Create a complete concept definition following the Genesis Dimension schema. Include:
- Full definition
- Genesis type and lineage
- Problem space and failed alternatives
- All differentiations
- Paradigmatic case
- Recognition markers
- Dialectics to preserve (productive tensions)

Output comprehensive JSON matching the PROCESS_ANSWERS_SYSTEM schema."""

            with client.messages.stream(
                model=MODEL,
                max_tokens=MAX_OUTPUT,
                thinking={
                    "type": "enabled",
                    "budget_tokens": THINKING_BUDGET
                },
                system=PROCESS_ANSWERS_SYSTEM,
                messages=[{"role": "user", "content": synthesis_prompt}]
            ) as stream:
                for event in stream:
                    if event.type == "content_block_delta":
                        if hasattr(event.delta, 'thinking'):
                            yield f"data: {json.dumps({'type': 'thinking', 'content': event.delta.thinking})}\n\n"
                        elif hasattr(event.delta, 'text'):
                            yield f"data: {json.dumps({'type': 'text', 'content': event.delta.text})}\n\n"

                final = stream.get_final_message()
                synthesis_text = ""
                for block in final.content:
                    if hasattr(block, 'text'):
                        synthesis_text = block.text
                        break

            concept_data = parse_wizard_response(synthesis_text)

            complete_data = {
                'type': 'complete',
                'data': {
                    'status': 'complete',
                    'concept_name': request.concept_name,
                    'concept': concept_data.get('concept', concept_data),
                    'dialectics_preserved': [d.model_dump() for d in request.dialectics]
                }
            }
            yield f"data: {json.dumps(complete_data)}\n\n"

        except Exception as e:
            logger.error(f"Error in finalize_concept: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_final_synthesis(),
        media_type="text/event-stream"
    )
