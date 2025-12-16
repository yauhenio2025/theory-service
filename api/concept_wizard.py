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
    notes: str  # User's initial notes - REQUIRED for preprocessing
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

NOTES_PREPROCESSING_PROMPT = """You are an expert in conceptual analysis helping a user articulate a novel theoretical concept.

The user has provided initial notes about a concept they're developing called "{concept_name}". Your task is to:
1. Extract what can be inferred from these notes
2. Probe the GENEALOGY of this concept - its intellectual origins and inspirations
3. Pre-fill answers to Stage 1 questions where possible
4. Identify what's still unclear and needs direct questioning

## User's Notes:
{notes}

## GENEALOGY EXTRACTION (Critical)
Look for any mentions of:
- Thinkers, philosophers, or theorists who inspired this concept
- Existing theoretical frameworks or traditions it builds on
- The context (academic, professional, personal) in which this concept emerged
- How long the user has been developing this concept
- Key readings, experiences, or observations that sparked this concept

## Stage 1 Questions to Pre-fill:
1. genesis_type: How would you characterize the origin of this concept?
   Options: theoretical_innovation, empirical_discovery, synthesis, reconceptualization, normative_reframing

2. core_definition: In one paragraph, provide your working definition of this concept.

3. problem_addressed: What problem or gap does this concept address?

4. adjacent_concepts: Which existing concepts come closest to what you're describing?
   (Can suggest specific concepts mentioned or implied in notes)

5. distinguishing_feature: What most clearly distinguishes this concept from adjacent ones?

Analyze the notes and produce a JSON response:
{{
    "notes_analysis": {{
        "summary": "Brief summary of what the user is trying to articulate (2-3 sentences)",
        "key_insights": ["Main ideas extracted from the notes"],
        "preliminary_definition": "A working definition extracted/synthesized from the notes"
    }},
    "genealogy": {{
        "detected_influences": [
            {{
                "name": "Thinker/Framework name",
                "type": "thinker|framework|tradition|concept",
                "relationship": "How this influenced the user's concept",
                "confidence": "high|medium|low",
                "source_excerpt": "Quote from notes if available"
            }}
        ],
        "emergence_context": {{
            "domain": "academic|professional|personal|mixed",
            "field": "Specific field if detectable (e.g., political theory, STS, IR)",
            "timeframe": "How long user has been developing this, if mentioned",
            "trigger": "What sparked this concept, if mentioned"
        }},
        "needs_probing": ["Aspects of genealogy not clear from notes that should be asked about"]
    }},
    "prefilled_answers": [
        {{
            "question_id": "genesis_type",
            "suggested_value": "theoretical_innovation|empirical_discovery|synthesis|reconceptualization|normative_reframing|null",
            "confidence": "high|medium|low",
            "reasoning": "Why this seems to be the origin type based on the notes",
            "source_excerpt": "Quote from notes that supports this"
        }},
        {{
            "question_id": "core_definition",
            "suggested_value": "Extracted or synthesized definition from notes, or null if unclear",
            "confidence": "high|medium|low",
            "reasoning": "How this was derived"
        }},
        {{
            "question_id": "problem_addressed",
            "suggested_value": "The problem/gap the user seems to be addressing, or null",
            "confidence": "high|medium|low",
            "reasoning": "Evidence from notes"
        }},
        {{
            "question_id": "adjacent_concepts",
            "suggested_values": ["List of concepts mentioned or implied in notes"],
            "confidence": "high|medium|low",
            "reasoning": "Why these seem related"
        }},
        {{
            "question_id": "distinguishing_feature",
            "suggested_value": "What makes this concept unique based on notes, or null",
            "confidence": "high|medium|low",
            "reasoning": "Evidence from notes"
        }}
    ],
    "questions_to_prioritize": ["question_ids that need user clarification because notes were unclear"],
    "potential_tensions": ["Any contradictions or tensions detected in the notes that could be productive dialectics"]
}}

Be conservative: only suggest values when you have clear evidence from the notes. Mark confidence appropriately.
If the notes don't provide enough information for a question, set suggested_value to null.
For genealogy, actively look for intellectual influences even if not explicitly stated - note when you're inferring vs quoting."""


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
    # User-validated data from wizard stages
    validated_cases: Optional[List[Dict[str, Any]]] = None  # Cases user approved
    validated_markers: Optional[List[Dict[str, Any]]] = None  # Markers user approved
    approved_tensions: Optional[List[Dict[str, Any]]] = None  # Tensions from understanding validation
    source_id: Optional[int] = None


class RegenerateUnderstandingRequest(BaseModel):
    """Request to regenerate understanding with user feedback."""
    concept_name: str
    notes: str
    previous_understanding: Dict[str, Any]
    user_rating: int  # 1-5 stars
    user_correction: str
    source_id: Optional[int] = None


class GenerateCaseStudiesRequest(BaseModel):
    """Request to generate paradigmatic case studies."""
    concept_name: str
    concept_definition: str  # Working definition from earlier stages
    context: str  # Additional context from answers
    source_id: Optional[int] = None


class GenerateRecognitionMarkersRequest(BaseModel):
    """Request to generate recognition markers."""
    concept_name: str
    concept_definition: str
    paradigmatic_cases: List[Dict[str, Any]]  # Approved/selected cases
    source_id: Optional[int] = None


class RegenerateSectionRequest(BaseModel):
    """Request to regenerate a specific section of the 9-dimension draft."""
    concept_name: str
    section: str  # genesis, problem_space, definition, core_claims, etc.
    current_value: Any  # Current value of the section
    feedback: str  # User feedback for regeneration
    full_context: Dict[str, Any]  # all_answers, interim_analysis, dialectics
    source_id: Optional[int] = None


class RegenerateInsightRequest(BaseModel):
    """Request to regenerate a specific key insight."""
    concept_name: str
    notes: str
    insight_index: int
    current_insight: str
    feedback: str
    all_insights: List[str]


class GenerateTensionsRequest(BaseModel):
    """Request to generate additional tensions."""
    concept_name: str
    notes: str
    existing_tensions: List[Any]  # Can be strings or objects
    approved_tensions: List[Any]
    notes_analysis: Dict[str, Any]


class RegenerateTensionRequest(BaseModel):
    """Request to regenerate a specific tension."""
    concept_name: str
    notes: str
    tension_index: int
    current_tension: str
    feedback: str
    all_tensions: List[str]


class RefineWithFeedbackRequest(BaseModel):
    """Request to refine pre-filled answers based on Understanding Validation feedback."""
    concept_name: str
    notes: str
    original_understanding: Dict[str, Any]  # The notes_analysis from stage1
    insight_feedback: Dict[str, Any]  # { index: { status: 'approved'|'rejected', comment: '' } }
    tension_feedback: Dict[str, Any]  # { index: { status: 'approved'|..., comment: '' } }
    original_questions: List[Dict[str, Any]]  # Original stage 1 questions with pre-fills
    # Genealogy user input
    genealogy_answers: Optional[Dict[str, str]] = None  # User answers to probing questions
    user_influences: Optional[List[str]] = None  # User-added influences not detected
    source_id: Optional[int] = None


# =============================================================================
# REGENERATE UNDERSTANDING PROMPT
# =============================================================================

REGENERATE_UNDERSTANDING_PROMPT = """You are an expert in conceptual analysis helping a user articulate a novel theoretical concept.

The user has provided initial notes about a concept they're developing called "{concept_name}".

Previously, you analyzed these notes and produced an understanding. The user has reviewed this and provided feedback.

## User's Original Notes:
{notes}

## Your Previous Understanding:
{previous_understanding}

## User's Rating: {user_rating}/5 stars

## User's Corrections/Clarifications:
{user_correction}

Your task is to:
1. Carefully consider the user's feedback and corrections
2. Revise your understanding to address their concerns
3. Re-extract what can be inferred from notes WITH their corrections in mind
4. Generate improved pre-filled answers for Stage 1 questions

## Stage 1 Questions to Pre-fill:
1. genesis_type: How would you characterize the origin of this concept?
   Options: theoretical_innovation, empirical_discovery, synthesis, reconceptualization, normative_reframing

2. core_definition: In one paragraph, provide your working definition of this concept.

3. problem_addressed: What problem or gap does this concept address?

4. adjacent_concepts: Which existing concepts come closest to what you're describing?

5. distinguishing_feature: What most clearly distinguishes this concept from adjacent ones?

Analyze the notes with the user's corrections in mind and produce a JSON response:
{{
    "notes_analysis": {{
        "summary": "REVISED summary based on user feedback (2-3 sentences)",
        "key_insights": ["REVISED key ideas incorporating corrections"],
        "preliminary_definition": "REVISED working definition"
    }},
    "prefilled_answers": [
        {{
            "question_id": "genesis_type",
            "suggested_value": "theoretical_innovation|empirical_discovery|synthesis|reconceptualization|normative_reframing|null",
            "confidence": "high|medium|low",
            "reasoning": "How this was derived, noting any user corrections considered",
            "source_excerpt": "Quote from notes or user correction that supports this"
        }},
        {{
            "question_id": "core_definition",
            "suggested_value": "REVISED extracted/synthesized definition",
            "confidence": "high|medium|low",
            "reasoning": "How user feedback influenced this"
        }},
        {{
            "question_id": "problem_addressed",
            "suggested_value": "REVISED problem/gap description",
            "confidence": "high|medium|low",
            "reasoning": "Evidence from notes and user corrections"
        }},
        {{
            "question_id": "adjacent_concepts",
            "suggested_values": ["REVISED list of concepts"],
            "confidence": "high|medium|low",
            "reasoning": "Why these seem related, considering user feedback"
        }},
        {{
            "question_id": "distinguishing_feature",
            "suggested_value": "REVISED distinguishing feature",
            "confidence": "high|medium|low",
            "reasoning": "Evidence from notes and user corrections"
        }}
    ],
    "questions_to_prioritize": ["question_ids that still need user clarification"],
    "potential_tensions": ["Any contradictions or tensions detected, including from user feedback"],
    "changes_made": ["List of specific changes made based on user feedback"]
}}

Be responsive to user feedback - if they rated poorly or provided corrections, make significant adjustments."""


GENERATE_CASE_STUDIES_PROMPT = """You are an expert in conceptual analysis helping generate paradigmatic case studies.

Given a concept definition and context, generate 3-5 candidate paradigmatic cases that could serve as examples of this concept.

## Concept Name: {concept_name}

## Concept Definition So Far:
{concept_definition}

## Context from User's Answers:
{context}

Generate paradigmatic case studies. For each case:
1. Title - A brief identifying name
2. Description - 2-3 sentences explaining the case
3. Relevance - Why this exemplifies the concept
4. Domain - What field/context this case comes from

Return as JSON:
{{
    "generated_cases": [
        {{
            "id": "case_1",
            "title": "Short title for the case",
            "description": "2-3 sentence description of what happened/what this case involves",
            "relevance": "Why this is a good example of the concept",
            "domain": "field/context (e.g., 'Technology Policy', 'International Relations')"
        }}
    ],
    "generation_note": "Brief note about what types of cases were generated and why"
}}

Generate diverse cases across different domains if possible. Include both well-known public examples and more subtle/implicit cases where the concept operates without being named."""


STAGE3_GENERATION_PROMPT = """You are an expert in conceptual analysis generating context-specific Stage 3 questions.

Stage 3 focuses on: Grounding & Recognition - establishing paradigmatic cases, recognition markers, and falsification conditions.

## Concept Name: {concept_name}

## Summary of Stage 1 & 2 (what we know so far):
{all_stages_summary}

## Key elements to reference in questions:
- Adjacent concepts mentioned: {adjacent_concepts}
- Key differentiations established: {differentiations}
- Dialectics/tensions identified: {dialectics}

Generate 3-4 context-specific Stage 3 questions that:
1. Reference specific concepts, cases, or tensions already discussed
2. Ask for paradigmatic examples that illustrate the specific differentiations identified
3. Probe for recognition markers based on the concept's unique features
4. Explore falsification conditions specific to the concept's claims

Return as JSON:
{{
    "stage3_questions": [
        {{
            "id": "paradigmatic_case",
            "text": "Given [reference specific concept features], what case best exemplifies [specific aspect]?",
            "type": "open_ended",
            "help": "Context-specific help text",
            "example": "Context-specific example",
            "min_length": 150,
            "rows": 6,
            "context_references": ["list of specific concepts/terms from earlier stages that this question references"]
        }},
        {{
            "id": "recognition_markers",
            "text": "How would you recognize [concept] operating in texts that discuss [specific adjacent domain]?",
            "type": "open_ended",
            "help": "Context-specific help",
            "min_length": 100,
            "rows": 5,
            "context_references": []
        }},
        {{
            "id": "implicit_domain",
            "text": "Where do you see debates about [specific tension/dialectic] without the term '[concept name]' being used?",
            "type": "open_ended",
            "help": "Context-specific help",
            "min_length": 100,
            "rows": 4,
            "context_references": []
        }},
        {{
            "id": "core_claim",
            "text": "Given that you've distinguished [concept] from [adjacent concept] by [key differentiation], what is the fundamental claim about reality?",
            "type": "open_ended",
            "help": "Context-specific help",
            "min_length": 100,
            "rows": 4,
            "context_references": []
        }}
    ],
    "generation_note": "Brief note about how questions were tailored to this specific concept"
}}

Make questions specific and grounded in what the user has already shared. Avoid generic questions that could apply to any concept."""


GENERATE_RECOGNITION_MARKERS_PROMPT = """You are an expert in conceptual analysis helping generate recognition markers.

Given a concept definition and paradigmatic cases, generate linguistic patterns and markers that indicate when this concept is operating in a text.

## Concept Name: {concept_name}

## Concept Definition:
{concept_definition}

## Paradigmatic Cases:
{paradigmatic_cases}

Generate recognition markers - linguistic patterns that indicate this concept is in play. For each marker:
1. Pattern - The linguistic pattern or phrase type
2. Example - A concrete example of this pattern
3. Reliability - How reliably this indicates the concept (high/medium/low)

Return as JSON:
{{
    "generated_markers": [
        {{
            "id": "marker_1",
            "pattern": "Description of the linguistic pattern",
            "example": "A concrete example phrase or sentence",
            "reliability": "high|medium|low",
            "notes": "Additional context about when this marker applies"
        }}
    ],
    "generation_note": "Brief note about the types of markers generated"
}}

Include different types of markers:
- Explicit terminology patterns
- Argument structure patterns
- Situational description patterns
- Proxy terms and euphemisms"""


REGENERATE_SECTION_PROMPT = """You are an expert in conceptual analysis helping refine a specific section of a 9-dimensional concept definition.

## Concept Name: {concept_name}

## Section to Regenerate: {section}

## Current Value:
{current_value}

## User's Feedback:
{feedback}

## Full Context (all answers from wizard):
{full_context}

Based on the user's feedback, regenerate ONLY the {section} section. Maintain the same structure/format but incorporate the feedback.

Return as JSON with the regenerated value:
{{
    "regenerated_value": <the new value for this section, matching the original structure>
}}

Section formats:
- genesis: {{"type": "...", "lineage": "...", "break_from": "..."}}
- problem_space: {{"gap": "...", "failed_alternatives": "..."}}
- definition: "string"
- core_claims: {{"ontological": "...", "causal": "..."}}

For list sections (differentiations, paradigmatic_cases, recognition_markers, falsification_conditions, dialectics), return the full regenerated list."""


REGENERATE_INSIGHT_PROMPT = """You are an expert in conceptual analysis helping refine a specific key insight.

## Concept Name: {concept_name}

## User's Notes:
{notes}

## Current Insight Being Refined (Index {insight_index}):
{current_insight}

## User's Feedback:
{feedback}

## Other Insights (for context, don't duplicate):
{other_insights}

Based on the user's feedback, regenerate THIS SPECIFIC insight. The regenerated insight should:
1. Address the user's feedback directly
2. Be distinct from the other insights
3. Accurately reflect what's in the user's notes
4. Be concise but informative (1-2 sentences)

Return as JSON:
{{
    "regenerated_insight": "The improved insight text..."
}}

Only return the single regenerated insight, not the whole list."""


GENERATE_TENSIONS_PROMPT = """You are an expert in conceptual analysis helping identify productive tensions (dialectics) in a novel concept.

## Concept Name: {concept_name}

## User's Notes:
{notes}

## Current Understanding Summary:
{understanding_summary}

## Preliminary Definition:
{preliminary_definition}

## Existing Tensions Already Identified:
{existing_tensions}

## Tensions Already Approved by User:
{approved_tensions}

Generate 2-3 ADDITIONAL productive tensions that could exist in this concept. Look for:
1. Tensions between different aspects or implications of the concept
2. Trade-offs inherent in how the concept operates
3. Dialectics between the concept and related concepts
4. Tensions between theoretical and practical applications
5. Methodological tensions in how the concept should be applied

DO NOT duplicate tensions already identified. Generate truly new ones.

Return as JSON:
{{
    "generated_tensions": [
        {{
            "description": "Brief description of the tension",
            "pole_a": "One side of the tension",
            "pole_b": "The opposing side",
            "productive_potential": "Why this tension could be productive for the concept"
        }}
    ],
    "generation_note": "Brief note about what types of tensions were identified"
}}

Focus on tensions that would be productive dialectics - not contradictions to resolve, but creative tensions to preserve."""


REGENERATE_TENSION_PROMPT = """You are an expert in conceptual analysis helping refine a productive tension (dialectic) based on user feedback.

## Concept Name: {concept_name}

## User's Notes:
{notes}

## Current Tension to Regenerate:
{current_tension}

## User's Feedback for Regeneration:
{feedback}

## Other Tensions in This Concept (for context, avoid duplication):
{other_tensions}

Your task is to regenerate this tension based on the user's feedback. The user wants a NEW formulation that incorporates their feedback - not just the original with a comment appended.

Consider:
1. What aspect of the tension does the user want emphasized or changed?
2. Are the poles (opposing sides) correctly identified?
3. Is the tension at the right level of abstraction?
4. Does it capture a genuinely productive dialectic?

Return as JSON:
{{
    "regenerated_tension": {{
        "description": "Regenerated description of the tension based on feedback",
        "pole_a": "One side of the tension",
        "pole_b": "The opposing side",
        "productive_potential": "Why this tension is productive for the concept"
    }},
    "regeneration_note": "Brief note about what was changed based on feedback"
}}

Generate a tension that reflects the user's feedback while maintaining theoretical rigor."""


REFINE_WITH_FEEDBACK_PROMPT = """You are an expert in conceptual analysis helping refine understanding based on user validation feedback.

## Concept Name: {concept_name}

## User's Original Notes:
{notes}

## Original Understanding Summary:
{original_summary}

## Original Key Insights:
{original_insights}

## User's Feedback on Insights:
{insight_feedback_summary}

## Approved Tensions (to preserve as dialectics):
{approved_tensions}

## Original Pre-filled Answers:
{original_prefills}

## INTELLECTUAL GENEALOGY
The user was asked about the intellectual origins and influences behind their concept.

### Detected Influences (from notes analysis):
{detected_influences}

### User's Answers to Genealogy Probing Questions:
{genealogy_answers}

### User-Declared Additional Influences:
{user_influences}

Your task is to generate REFINED pre-filled answers for Stage 1 questions that:
1. Incorporate the user's approved insights (give them more weight)
2. EXCLUDE or de-emphasize rejected insights
3. Consider the comments/refinements the user provided
4. Include the approved tensions as productive dialectics to preserve
5. **CRITICAL**: Integrate the genealogy information - the intellectual lineage should inform:
   - genesis_type (theoretical_innovation if building on frameworks, synthesis if combining traditions, etc.)
   - adjacent_concepts (include the thinkers/frameworks mentioned as influences)
   - The overall definition and framing

## Stage 1 Questions to Pre-fill:
1. genesis_type: How would you characterize the origin of this concept?
   Options: theoretical_innovation, empirical_discovery, synthesis, reconceptualization, normative_reframing

2. core_definition: In one paragraph, provide your working definition of this concept.

3. problem_addressed: What problem or gap does this concept address?

4. adjacent_concepts: Which existing concepts come closest to what you're describing?

5. distinguishing_feature: What most clearly distinguishes this concept from adjacent ones?

6. domain_scope: In which domains does this concept apply?

Return your analysis as JSON:
{{
    "refined_summary": "Updated summary incorporating user feedback...",
    "refined_definition": "Updated working definition...",
    "refined_insights": ["list", "of", "approved/refined", "insights"],
    "refined_genealogy": {{
        "key_influences": ["Thinker/framework 1", "Tradition 2"],
        "lineage_summary": "Brief description of intellectual lineage",
        "emergence_context": "Context in which this concept emerged"
    }},
    "prefilled_answers": [
        {{
            "question_id": "genesis_type",
            "value": "theoretical_innovation",
            "confidence": "high|medium|low",
            "reasoning": "Why this answer, considering user feedback and genealogy...",
            "source_excerpt": "relevant quote from notes if any"
        }},
        {{
            "question_id": "core_definition",
            "value": "The refined definition incorporating feedback...",
            "confidence": "high",
            "reasoning": "How feedback shaped this..."
        }}
    ],
    "validation_note": "Brief note about what feedback was incorporated"
}}"""


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


@router.post("/regenerate-understanding")
async def regenerate_understanding(request: RegenerateUnderstandingRequest):
    """
    Regenerate notes analysis with user feedback incorporated.
    User provides rating and corrections, we re-run analysis with that context.
    """
    async def stream_regenerated_analysis():
        try:
            yield f"data: {json.dumps({'type': 'phase', 'phase': 'regenerating_understanding'})}\n\n"

            # Format previous understanding for prompt
            prev_understanding_str = json.dumps(request.previous_understanding, indent=2)

            prompt = REGENERATE_UNDERSTANDING_PROMPT.format(
                concept_name=request.concept_name,
                notes=request.notes,
                previous_understanding=prev_understanding_str,
                user_rating=request.user_rating,
                user_correction=request.user_correction or "(No specific correction provided)"
            )

            # Call Claude with extended thinking
            client = get_claude_client()

            with client.messages.stream(
                model=MODEL,
                max_tokens=MAX_OUTPUT,
                thinking={
                    "type": "enabled",
                    "budget_tokens": THINKING_BUDGET
                },
                system="You are an expert in conceptual analysis. Incorporate user feedback to improve your understanding.",
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                response_text = ""
                for event in stream:
                    if hasattr(event, 'type'):
                        if event.type == "content_block_delta":
                            if hasattr(event, 'delta'):
                                if hasattr(event.delta, 'thinking'):
                                    yield f"data: {json.dumps({'type': 'thinking', 'content': event.delta.thinking})}\n\n"
                                elif hasattr(event.delta, 'text'):
                                    response_text += event.delta.text

                final_message = stream.get_final_message()
                for block in final_message.content:
                    if hasattr(block, 'text'):
                        response_text = block.text
                        break

            # Parse the regenerated analysis
            analysis_data = parse_wizard_response(response_text)
            notes_analysis = analysis_data.get("notes_analysis", {})
            prefilled_answers = analysis_data.get("prefilled_answers", [])
            questions_to_prioritize = analysis_data.get("questions_to_prioritize", [])
            potential_tensions = analysis_data.get("potential_tensions", [])
            changes_made = analysis_data.get("changes_made", [])

            # Build questions with pre-filled values
            questions = []
            for q in STAGE1_QUESTIONS:
                q_dict = q.model_dump()

                for prefill in prefilled_answers:
                    if prefill.get("question_id") == q.id:
                        q_dict["prefilled"] = {
                            "value": prefill.get("suggested_value") or prefill.get("suggested_values"),
                            "confidence": prefill.get("confidence", "low"),
                            "reasoning": prefill.get("reasoning", ""),
                            "source_excerpt": prefill.get("source_excerpt", "")
                        }
                        break

                if q.id in questions_to_prioritize:
                    q_dict["needs_clarification"] = True

                questions.append(q_dict)

            complete_data = {
                'type': 'complete',
                'data': {
                    'status': 'stage1_ready',
                    'concept_name': request.concept_name,
                    'stage': 1,
                    'stage_title': 'Genesis & Problem Space',
                    'stage_description': "I've revised my understanding based on your feedback.",
                    'notes_analysis': notes_analysis,
                    'potential_tensions': potential_tensions,
                    'changes_made': changes_made,
                    'questions': questions,
                    'regenerated': True
                }
            }
            yield f"data: {json.dumps(complete_data)}\n\n"

        except Exception as e:
            logger.error(f"Error in regenerate_understanding: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_regenerated_analysis(),
        media_type="text/event-stream"
    )


@router.post("/regenerate-insight")
async def regenerate_insight(request: RegenerateInsightRequest):
    """
    Regenerate a specific key insight with user feedback.
    """
    async def stream_regenerated_insight():
        try:
            yield f"data: {json.dumps({'type': 'phase', 'phase': 'regenerating_insight'})}\n\n"

            # Build list of other insights (excluding the one being regenerated)
            other_insights = [
                insight for i, insight in enumerate(request.all_insights)
                if i != request.insight_index
            ]

            prompt = REGENERATE_INSIGHT_PROMPT.format(
                concept_name=request.concept_name,
                notes=request.notes,
                insight_index=request.insight_index,
                current_insight=request.current_insight,
                feedback=request.feedback,
                other_insights="\n".join([f"- {ins}" for ins in other_insights]) if other_insights else "(No other insights)"
            )

            client = get_claude_client()

            with client.messages.stream(
                model=MODEL,
                max_tokens=MAX_OUTPUT,
                thinking={
                    "type": "enabled",
                    "budget_tokens": THINKING_BUDGET
                },
                system="You are an expert in conceptual analysis helping refine key insights.",
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                response_text = ""
                for event in stream:
                    if hasattr(event, 'type'):
                        if event.type == "content_block_delta":
                            if hasattr(event, 'delta'):
                                if hasattr(event.delta, 'thinking'):
                                    yield f"data: {json.dumps({'type': 'thinking', 'content': event.delta.thinking})}\n\n"
                                elif hasattr(event.delta, 'text'):
                                    response_text += event.delta.text

                final_message = stream.get_final_message()
                for block in final_message.content:
                    if hasattr(block, 'text'):
                        response_text = block.text
                        break

            # Parse response
            insight_data = parse_wizard_response(response_text)
            regenerated_insight = insight_data.get("regenerated_insight", request.current_insight)

            complete_data = {
                'type': 'complete',
                'data': {
                    'regenerated_insight': regenerated_insight
                }
            }
            yield f"data: {json.dumps(complete_data)}\n\n"

        except Exception as e:
            logger.error(f"Error in regenerate_insight: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_regenerated_insight(),
        media_type="text/event-stream"
    )


@router.post("/generate-tensions")
async def generate_tensions(request: GenerateTensionsRequest):
    """
    Generate additional productive tensions based on current understanding.
    """
    async def stream_tensions():
        try:
            yield f"data: {json.dumps({'type': 'phase', 'phase': 'generating_tensions'})}\n\n"

            # Format existing tensions for the prompt
            def format_tension(t):
                if isinstance(t, str):
                    return t
                elif isinstance(t, dict):
                    return t.get('description', t.get('tension', str(t)))
                return str(t)

            existing_str = "\n".join([f"- {format_tension(t)}" for t in request.existing_tensions]) if request.existing_tensions else "(None yet)"
            approved_str = "\n".join([f"- {format_tension(t)}" for t in request.approved_tensions]) if request.approved_tensions else "(None approved yet)"

            prompt = GENERATE_TENSIONS_PROMPT.format(
                concept_name=request.concept_name,
                notes=request.notes,
                understanding_summary=request.notes_analysis.get('summary', ''),
                preliminary_definition=request.notes_analysis.get('preliminaryDefinition', ''),
                existing_tensions=existing_str,
                approved_tensions=approved_str
            )

            client = get_claude_client()

            with client.messages.stream(
                model=MODEL,
                max_tokens=MAX_OUTPUT,
                thinking={
                    "type": "enabled",
                    "budget_tokens": THINKING_BUDGET
                },
                system="You are an expert in conceptual analysis helping identify productive tensions and dialectics.",
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                response_text = ""
                for event in stream:
                    if hasattr(event, 'type'):
                        if event.type == "content_block_delta":
                            if hasattr(event, 'delta'):
                                if hasattr(event.delta, 'thinking'):
                                    yield f"data: {json.dumps({'type': 'thinking', 'content': event.delta.thinking})}\n\n"
                                elif hasattr(event.delta, 'text'):
                                    response_text += event.delta.text

                final_message = stream.get_final_message()
                for block in final_message.content:
                    if hasattr(block, 'text'):
                        response_text = block.text
                        break

            # Parse response
            tensions_data = parse_wizard_response(response_text)
            generated_tensions = tensions_data.get("generated_tensions", [])
            generation_note = tensions_data.get("generation_note", "")

            complete_data = {
                'type': 'complete',
                'data': {
                    'generated_tensions': generated_tensions,
                    'generation_note': generation_note
                }
            }
            yield f"data: {json.dumps(complete_data)}\n\n"

        except Exception as e:
            logger.error(f"Error in generate_tensions: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_tensions(),
        media_type="text/event-stream"
    )


@router.post("/regenerate-tension")
async def regenerate_tension(request: RegenerateTensionRequest):
    """
    Regenerate a specific tension using user feedback as context.
    Unlike 'approve with comment' which preserves the original, this creates a new formulation.
    """
    async def stream_regenerated_tension():
        try:
            yield f"data: {json.dumps({'type': 'phase', 'phase': 'regenerating_tension'})}\n\n"

            # Format other tensions for context
            other_tensions = [t for i, t in enumerate(request.all_tensions) if i != request.tension_index]
            other_tensions_str = "\n".join([f"- {t}" for t in other_tensions]) if other_tensions else "(No other tensions)"

            prompt = REGENERATE_TENSION_PROMPT.format(
                concept_name=request.concept_name,
                notes=request.notes,
                current_tension=request.current_tension,
                feedback=request.feedback,
                other_tensions=other_tensions_str
            )

            client = get_claude_client()

            with client.messages.stream(
                model=MODEL,
                max_tokens=MAX_OUTPUT,
                thinking={
                    "type": "enabled",
                    "budget_tokens": THINKING_BUDGET
                },
                system="You are an expert in conceptual analysis helping refine productive tensions and dialectics.",
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                response_text = ""
                for event in stream:
                    if hasattr(event, 'type'):
                        if event.type == "content_block_delta":
                            if hasattr(event, 'delta'):
                                if hasattr(event.delta, 'thinking'):
                                    yield f"data: {json.dumps({'type': 'thinking', 'content': event.delta.thinking})}\n\n"
                                elif hasattr(event.delta, 'text'):
                                    response_text += event.delta.text

                final_message = stream.get_final_message()
                for block in final_message.content:
                    if hasattr(block, 'text'):
                        response_text = block.text
                        break

            # Parse response
            tension_data = parse_wizard_response(response_text)
            regenerated_tension = tension_data.get("regenerated_tension", {})
            regeneration_note = tension_data.get("regeneration_note", "")

            complete_data = {
                'type': 'complete',
                'data': {
                    'regenerated_tension': regenerated_tension,
                    'regeneration_note': regeneration_note
                }
            }
            yield f"data: {json.dumps(complete_data)}\n\n"

        except Exception as e:
            logger.error(f"Error in regenerate_tension: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_regenerated_tension(),
        media_type="text/event-stream"
    )


@router.post("/refine-with-feedback")
async def refine_with_feedback(request: RefineWithFeedbackRequest):
    """
    Refine pre-filled answers based on Understanding Validation feedback.
    This is called when user clicks "Accept & Continue" after validating understanding.
    """
    async def stream_refined():
        try:
            yield f"data: {json.dumps({'type': 'phase', 'phase': 'refining_with_feedback'})}\n\n"

            # Build insight feedback summary
            original_insights = request.original_understanding.get('key_insights', [])
            insight_lines = []
            approved_insights = []

            for i, insight in enumerate(original_insights):
                feedback = request.insight_feedback.get(str(i), {})
                status = feedback.get('status', 'pending')
                comment = feedback.get('comment', '')

                if status == 'approved':
                    insight_lines.append(f"✓ APPROVED: {insight}")
                    approved_insights.append(insight)
                elif status == 'rejected':
                    insight_lines.append(f"✗ REJECTED: {insight}" + (f" (Reason: {comment})" if comment else ""))
                else:
                    # Pending - include with neutral marker
                    insight_lines.append(f"~ PENDING: {insight}")
                    approved_insights.append(insight)  # Include pending as approved by default

                if comment and status != 'rejected':
                    insight_lines.append(f"  User comment: {comment}")

            insight_feedback_summary = "\n".join(insight_lines) if insight_lines else "(No feedback provided)"

            # Build approved tensions summary
            original_tensions = request.original_understanding.get('potentialTensions', [])
            approved_tensions_list = []

            for i, tension in enumerate(original_tensions):
                feedback = request.tension_feedback.get(str(i), {})
                status = feedback.get('status', 'pending')
                comment = feedback.get('comment', '')

                if status in ['approved', 'approved_with_comment', 'pending']:
                    tension_text = tension if isinstance(tension, str) else tension.get('description', tension.get('tension', str(tension)))
                    if comment:
                        approved_tensions_list.append(f"- {tension_text} (User note: {comment})")
                    else:
                        approved_tensions_list.append(f"- {tension_text}")

            approved_tensions_str = "\n".join(approved_tensions_list) if approved_tensions_list else "(No tensions approved)"

            # Format original prefills
            original_prefills = []
            for q in request.original_questions:
                if q.get('prefilled'):
                    original_prefills.append(f"- {q['id']}: {q['prefilled'].get('value', 'N/A')} (confidence: {q['prefilled'].get('confidence', 'unknown')})")

            original_prefills_str = "\n".join(original_prefills) if original_prefills else "(No pre-fills)"

            # Build genealogy summaries
            genealogy_data = request.original_understanding.get('genealogy', {})
            detected_influences_list = genealogy_data.get('detected_influences', [])
            detected_influences_str = ""
            if detected_influences_list:
                for inf in detected_influences_list:
                    name = inf.get('name', 'Unknown')
                    inf_type = inf.get('type', 'influence')
                    relationship = inf.get('relationship', '')
                    detected_influences_str += f"- {name} ({inf_type}): {relationship}\n"
            else:
                detected_influences_str = "(No influences detected from notes)"

            # Format user's genealogy answers
            genealogy_answers_str = ""
            if request.genealogy_answers:
                probing_questions = genealogy_data.get('needs_probing', [])
                for idx_str, answer in request.genealogy_answers.items():
                    idx = int(idx_str)
                    question = probing_questions[idx] if idx < len(probing_questions) else f"Probing question {idx}"
                    genealogy_answers_str += f"Q: {question}\nA: {answer}\n\n"
            else:
                genealogy_answers_str = "(No probing questions answered)"

            # Format user-declared additional influences
            user_influences_str = ""
            if request.user_influences:
                user_influences_str = "\n".join([f"- {inf}" for inf in request.user_influences])
            else:
                user_influences_str = "(No additional influences declared)"

            prompt = REFINE_WITH_FEEDBACK_PROMPT.format(
                concept_name=request.concept_name,
                notes=request.notes,
                original_summary=request.original_understanding.get('summary', ''),
                original_insights="\n".join([f"- {ins}" for ins in original_insights]),
                insight_feedback_summary=insight_feedback_summary,
                approved_tensions=approved_tensions_str,
                original_prefills=original_prefills_str,
                detected_influences=detected_influences_str,
                genealogy_answers=genealogy_answers_str,
                user_influences=user_influences_str
            )

            client = get_claude_client()

            with client.messages.stream(
                model=MODEL,
                max_tokens=MAX_OUTPUT,
                thinking={
                    "type": "enabled",
                    "budget_tokens": THINKING_BUDGET
                },
                system="You are an expert in conceptual analysis helping refine understanding based on user validation.",
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                response_text = ""
                for event in stream:
                    if hasattr(event, 'type'):
                        if event.type == "content_block_delta":
                            if hasattr(event, 'delta'):
                                if hasattr(event.delta, 'thinking'):
                                    yield f"data: {json.dumps({'type': 'thinking', 'content': event.delta.thinking})}\n\n"
                                elif hasattr(event.delta, 'text'):
                                    response_text += event.delta.text

                final_message = stream.get_final_message()
                for block in final_message.content:
                    if hasattr(block, 'text'):
                        response_text = block.text
                        break

            # Parse response
            refined_data = parse_wizard_response(response_text)

            # Build refined questions with new pre-fills
            refined_questions = []
            prefilled_map = {p['question_id']: p for p in refined_data.get('prefilled_answers', [])}

            for q in request.original_questions:
                q_copy = dict(q)
                if q['id'] in prefilled_map:
                    prefill = prefilled_map[q['id']]
                    q_copy['prefilled'] = {
                        'value': prefill.get('value'),
                        'confidence': prefill.get('confidence', 'medium'),
                        'reasoning': prefill.get('reasoning', ''),
                        'source_excerpt': prefill.get('source_excerpt'),
                        'refined_from_feedback': True
                    }
                refined_questions.append(q_copy)

            # Build refined understanding
            refined_understanding = {
                'summary': refined_data.get('refined_summary', request.original_understanding.get('summary')),
                'preliminary_definition': refined_data.get('refined_definition', request.original_understanding.get('preliminaryDefinition')),
                'key_insights': refined_data.get('refined_insights', approved_insights),
                'validation_note': refined_data.get('validation_note', '')
            }

            complete_data = {
                'type': 'complete',
                'data': {
                    'refined_questions': refined_questions,
                    'refined_understanding': refined_understanding,
                    'approved_tensions': approved_tensions_list,
                    'validation_note': refined_data.get('validation_note', 'Feedback incorporated')
                }
            }
            yield f"data: {json.dumps(complete_data)}\n\n"

        except Exception as e:
            logger.error(f"Error in refine_with_feedback: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_refined(),
        media_type="text/event-stream"
    )


@router.post("/generate-case-studies")
async def generate_case_studies(request: GenerateCaseStudiesRequest):
    """
    Generate candidate paradigmatic case studies for the user to validate.
    """
    async def stream_case_studies():
        try:
            yield f"data: {json.dumps({'type': 'phase', 'phase': 'generating_cases'})}\n\n"

            prompt = GENERATE_CASE_STUDIES_PROMPT.format(
                concept_name=request.concept_name,
                concept_definition=request.concept_definition,
                context=request.context
            )

            client = get_claude_client()

            with client.messages.stream(
                model=MODEL,
                max_tokens=MAX_OUTPUT,
                thinking={
                    "type": "enabled",
                    "budget_tokens": THINKING_BUDGET
                },
                system="You are an expert at generating relevant paradigmatic cases for novel concepts.",
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                response_text = ""
                for event in stream:
                    if hasattr(event, 'type'):
                        if event.type == "content_block_delta":
                            if hasattr(event, 'delta'):
                                if hasattr(event.delta, 'thinking'):
                                    yield f"data: {json.dumps({'type': 'thinking', 'content': event.delta.thinking})}\n\n"
                                elif hasattr(event.delta, 'text'):
                                    response_text += event.delta.text

                final_message = stream.get_final_message()
                for block in final_message.content:
                    if hasattr(block, 'text'):
                        response_text = block.text
                        break

            # Parse the generated cases
            cases_data = parse_wizard_response(response_text)
            generated_cases = cases_data.get("generated_cases", [])
            generation_note = cases_data.get("generation_note", "")

            complete_data = {
                'type': 'complete',
                'data': {
                    'generated_cases': generated_cases,
                    'generation_note': generation_note
                }
            }
            yield f"data: {json.dumps(complete_data)}\n\n"

        except Exception as e:
            logger.error(f"Error in generate_case_studies: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_case_studies(),
        media_type="text/event-stream"
    )


@router.post("/generate-recognition-markers")
async def generate_recognition_markers(request: GenerateRecognitionMarkersRequest):
    """
    Generate candidate recognition markers for the user to validate.
    """
    async def stream_markers():
        try:
            yield f"data: {json.dumps({'type': 'phase', 'phase': 'generating_markers'})}\n\n"

            # Format paradigmatic cases for the prompt
            cases_text = json.dumps(request.paradigmatic_cases, indent=2)

            prompt = GENERATE_RECOGNITION_MARKERS_PROMPT.format(
                concept_name=request.concept_name,
                concept_definition=request.concept_definition,
                paradigmatic_cases=cases_text
            )

            client = get_claude_client()

            with client.messages.stream(
                model=MODEL,
                max_tokens=MAX_OUTPUT,
                thinking={
                    "type": "enabled",
                    "budget_tokens": THINKING_BUDGET
                },
                system="You are an expert at identifying linguistic patterns and recognition markers for concepts.",
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                response_text = ""
                for event in stream:
                    if hasattr(event, 'type'):
                        if event.type == "content_block_delta":
                            if hasattr(event, 'delta'):
                                if hasattr(event.delta, 'thinking'):
                                    yield f"data: {json.dumps({'type': 'thinking', 'content': event.delta.thinking})}\n\n"
                                elif hasattr(event.delta, 'text'):
                                    response_text += event.delta.text

                final_message = stream.get_final_message()
                for block in final_message.content:
                    if hasattr(block, 'text'):
                        response_text = block.text
                        break

            # Parse the generated markers
            markers_data = parse_wizard_response(response_text)
            generated_markers = markers_data.get("generated_markers", [])
            generation_note = markers_data.get("generation_note", "")

            complete_data = {
                'type': 'complete',
                'data': {
                    'generated_markers': generated_markers,
                    'generation_note': generation_note
                }
            }
            yield f"data: {json.dumps(complete_data)}\n\n"

        except Exception as e:
            logger.error(f"Error in generate_recognition_markers: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_markers(),
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
    """
    Pre-process user notes with Claude, then return Stage 1 questions
    with pre-filled answers where the notes provide enough information.
    """
    async def stream_notes_analysis():
        try:
            # Phase 1: Analyzing notes
            yield f"data: {json.dumps({'type': 'phase', 'phase': 'analyzing_notes'})}\n\n"

            prompt = NOTES_PREPROCESSING_PROMPT.format(
                concept_name=request.concept_name,
                notes=request.notes
            )

            # Call Claude with extended thinking to analyze notes
            client = get_claude_client()
            notes_analysis = {}
            prefilled_answers = []

            with client.messages.stream(
                model=MODEL,
                max_tokens=MAX_OUTPUT,
                thinking={
                    "type": "enabled",
                    "budget_tokens": THINKING_BUDGET
                },
                system="You are an expert in conceptual analysis helping articulate novel theoretical concepts.",
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                response_text = ""
                for event in stream:
                    if hasattr(event, 'type'):
                        if event.type == "content_block_delta":
                            if hasattr(event, 'delta'):
                                if hasattr(event.delta, 'thinking'):
                                    yield f"data: {json.dumps({'type': 'thinking', 'content': event.delta.thinking})}\n\n"
                                elif hasattr(event.delta, 'text'):
                                    response_text += event.delta.text

                # Get final message for text content
                final_message = stream.get_final_message()
                for block in final_message.content:
                    if hasattr(block, 'text'):
                        response_text = block.text
                        break

            # Parse the analysis
            analysis_data = parse_wizard_response(response_text)
            notes_analysis = analysis_data.get("notes_analysis", {})
            prefilled_answers = analysis_data.get("prefilled_answers", [])
            questions_to_prioritize = analysis_data.get("questions_to_prioritize", [])
            potential_tensions = analysis_data.get("potential_tensions", [])

            # Build questions with pre-filled values
            questions = []
            for q in STAGE1_QUESTIONS:
                q_dict = q.model_dump()

                # Find if we have a prefilled answer for this question
                for prefill in prefilled_answers:
                    if prefill.get("question_id") == q.id:
                        q_dict["prefilled"] = {
                            "value": prefill.get("suggested_value") or prefill.get("suggested_values"),
                            "confidence": prefill.get("confidence", "low"),
                            "reasoning": prefill.get("reasoning", ""),
                            "source_excerpt": prefill.get("source_excerpt", "")
                        }
                        break

                # Mark if this question needs priority attention
                if q.id in questions_to_prioritize:
                    q_dict["needs_clarification"] = True

                questions.append(q_dict)

            # Return complete response with analysis and questions
            complete_data = {
                'type': 'complete',
                'data': {
                    'status': 'stage1_ready',
                    'concept_name': request.concept_name,
                    'stage': 1,
                    'stage_title': 'Genesis & Problem Space',
                    'stage_description': "Let's verify and refine what we extracted from your notes.",
                    'notes_analysis': notes_analysis,
                    'potential_tensions': potential_tensions,
                    'questions': questions
                }
            }
            yield f"data: {json.dumps(complete_data)}\n\n"

        except Exception as e:
            logger.error(f"Error in stage1 notes preprocessing: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_notes_analysis(),
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


def build_stages_summary(stage1_answers: List[AnswerWithMeta], stage2_answers: List[AnswerWithMeta]) -> str:
    """Build a comprehensive summary of Stage 1 and Stage 2 answers for context-specific generation."""
    summary_parts = []

    summary_parts.append("### Stage 1 - Genesis & Foundations:")
    for ans in stage1_answers:
        if ans.selected_options or ans.text_answer:
            answer_text = ans.text_answer or ", ".join(ans.selected_options)
            summary_parts.append(f"- {ans.question_id}: {answer_text}")
            if ans.custom_response:
                summary_parts.append(f"  User addition ({ans.custom_response_category or 'note'}): {ans.custom_response}")
            if ans.is_dialectic:
                summary_parts.append(f"  MARKED AS DIALECTIC: {ans.dialectic_pole_a} vs {ans.dialectic_pole_b}")

    summary_parts.append("\n### Stage 2 - Differentiation & Clarification:")
    for ans in stage2_answers:
        if ans.selected_options or ans.text_answer:
            answer_text = ans.text_answer or ", ".join(ans.selected_options)
            summary_parts.append(f"- {ans.question_id}: {answer_text}")
            if ans.custom_response:
                summary_parts.append(f"  User addition ({ans.custom_response_category or 'note'}): {ans.custom_response}")
            if ans.is_dialectic:
                summary_parts.append(f"  MARKED AS DIALECTIC: {ans.dialectic_pole_a} vs {ans.dialectic_pole_b}")

    return "\n".join(summary_parts)


def format_differentiations(differentiations: List[dict]) -> str:
    """Format differentiations for Stage 3 generation prompt."""
    if not differentiations:
        return "No specific differentiations established yet"

    formatted = []
    for diff in differentiations:
        parts = [f"- {diff.get('question', 'Unknown differentiation')}"]
        if diff.get('choice'):
            parts.append(f"  Choice: {diff['choice']}")
        if diff.get('custom_note'):
            parts.append(f"  Note: {diff['custom_note']}")
        formatted.append("\n".join(parts))

    return "\n".join(formatted)


def format_dialectics_for_stage3(dialectics: List[Tension]) -> str:
    """Format dialectics for Stage 3 generation prompt."""
    if not dialectics:
        return "No dialectics/tensions identified yet"

    formatted = []
    for d in dialectics:
        tension_text = f"- {d.pole_a} vs {d.pole_b}"
        if d.user_note:
            tension_text += f" ({d.user_note})"
        formatted.append(tension_text)

    return "\n".join(formatted)


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

            # Generate context-specific Stage 3 questions
            yield f"data: {json.dumps({'type': 'phase', 'phase': 'generating_stage3'})}\n\n"

            # Build context summary from all answers
            all_stages_summary = build_stages_summary(request.stage1_answers, request.stage2_answers)

            # Extract adjacent concepts from Stage 1 answers
            adjacent_concepts = extract_adjacent_concepts(request.stage1_answers)

            # Format differentiations
            differentiations_summary = format_differentiations(differentiations)

            # Format dialectics
            dialectics_summary = format_dialectics_for_stage3(all_dialectics)

            stage3_gen_prompt = STAGE3_GENERATION_PROMPT.format(
                concept_name=request.concept_name,
                all_stages_summary=all_stages_summary,
                adjacent_concepts=adjacent_concepts,
                differentiations=differentiations_summary,
                dialectics=dialectics_summary
            )

            with client.messages.stream(
                model=MODEL,
                max_tokens=MAX_OUTPUT,
                thinking={
                    "type": "enabled",
                    "budget_tokens": THINKING_BUDGET
                },
                system="You are an expert in conceptual analysis generating context-specific questions.",
                messages=[{"role": "user", "content": stage3_gen_prompt}]
            ) as stream:
                for event in stream:
                    if event.type == "content_block_delta":
                        if hasattr(event.delta, 'thinking'):
                            yield f"data: {json.dumps({'type': 'thinking', 'content': event.delta.thinking})}\n\n"

                final = stream.get_final_message()
                stage3_gen_text = ""
                for block in final.content:
                    if hasattr(block, 'text'):
                        stage3_gen_text = block.text
                        break

            stage3_gen_data = parse_wizard_response(stage3_gen_text)
            stage3_questions = stage3_gen_data.get("stage3_questions", [])

            # Fall back to predefined questions if generation failed
            if not stage3_questions:
                logger.warning("Stage 3 question generation failed, falling back to predefined questions")
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


@router.post("/regenerate-section")
async def regenerate_section(request: RegenerateSectionRequest):
    """
    Regenerate a specific section of the 9-dimension draft with user feedback.
    """
    try:
        client = get_claude_client()

        # Format context
        full_context_str = json.dumps(request.full_context, indent=2)
        current_value_str = json.dumps(request.current_value, indent=2) if isinstance(request.current_value, (dict, list)) else str(request.current_value)

        prompt = REGENERATE_SECTION_PROMPT.format(
            concept_name=request.concept_name,
            section=request.section,
            current_value=current_value_str,
            feedback=request.feedback,
            full_context=full_context_str
        )

        with client.messages.stream(
            model=MODEL,
            max_tokens=MAX_OUTPUT,
            thinking={
                "type": "enabled",
                "budget_tokens": THINKING_BUDGET
            },
            system="You are an expert in conceptual analysis helping refine concept definitions.",
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            final = stream.get_final_message()
            response_text = ""
            for block in final.content:
                if hasattr(block, 'text'):
                    response_text = block.text
                    break

        # Parse response
        response_data = parse_wizard_response(response_text)
        regenerated_value = response_data.get("regenerated_value", request.current_value)

        return {"regenerated_value": regenerated_value}

    except Exception as e:
        logger.error(f"Error regenerating section: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


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

    # Format validated data for the prompt
    validated_cases_str = ""
    if request.validated_cases:
        validated_cases_str = "\n".join([
            f"- {c.get('title', 'Case')}: {c.get('description', '')} (Rating: {c.get('rating', 'approved')})"
            for c in request.validated_cases
        ])

    validated_markers_str = ""
    if request.validated_markers:
        validated_markers_str = "\n".join([
            f"- {m.get('pattern', m.get('marker', str(m)))}"
            for m in request.validated_markers
        ])

    approved_tensions_str = ""
    if request.approved_tensions:
        approved_tensions_str = "\n".join([
            f"- {t.get('description', t.get('tension', str(t)))}" +
            (f" (User note: {t.get('comment', '')})" if t.get('comment') else "")
            for t in request.approved_tensions
        ])

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

## User-Validated Paradigmatic Cases:
{validated_cases_str or "(User will provide paradigmatic cases)"}

## User-Validated Recognition Markers:
{validated_markers_str or "(Generate recognition markers based on definition)"}

## Approved Tensions/Dialectics from Understanding Validation:
{approved_tensions_str or "(None specifically approved)"}

## Additional Dialectics/Tensions Marked During Questions:
{json.dumps([d.model_dump() for d in request.dialectics], indent=2)}

Create a complete concept definition following the Genesis Dimension schema.

IMPORTANT:
- For paradigmatic_cases: USE the user-validated cases above if provided. These are cases the user has explicitly approved as good examples of this concept.
- For recognition_markers: USE the user-validated markers above if provided.
- For dialectics: COMBINE both the approved tensions from understanding validation AND the tensions marked during questions. These are productive tensions the user wants to preserve.
- For falsification_conditions: Generate clear conditions under which this concept would be proven false or inapplicable.

Include ALL of the following in your JSON output:

{{
  "concept": {{
    "name": "Concept name",
    "definition": "Full 2-3 paragraph definition",
    "genesis": {{
      "type": "genesis type",
      "lineage": "theoretical traditions",
      "break_from": "what it breaks from"
    }},
    "problem_space": {{
      "gap": "the gap this fills",
      "failed_alternatives": "concepts that failed"
    }},
    "differentiations": [
      {{ "confused_with": "Other Concept", "difference": "Key distinction" }}
    ],
    "paradigmatic_cases": [
      {{ "title": "Case name", "description": "Description", "relevance": "Why paradigmatic" }}
    ],
    "recognition_markers": [
      {{ "description": "Pattern to look for", "context": "Where to look" }}
    ],
    "core_claims": {{
      "ontological": "What this concept says exists or is real",
      "causal": "What causal relationships it asserts"
    }},
    "falsification_conditions": [
      "Condition under which this concept would be proven false"
    ],
    "dialectics": [
      {{ "description": "Tension description", "pole_a": "One pole", "pole_b": "Other pole" }}
    ]
  }}
}}

CRITICAL:
- paradigmatic_cases MUST be an array with title/description for each case. USE the user-validated cases provided above.
- recognition_markers MUST be an array with description field for each marker. USE the user-validated markers provided above.
- dialectics MUST be an array combining approved tensions AND marked tensions.
- falsification_conditions MUST be an array of strings."""

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
