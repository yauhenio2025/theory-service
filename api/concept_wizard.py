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
import tempfile
import uuid
from typing import Optional, List, Dict, Any
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form

# Set up logging
logger = logging.getLogger(__name__)
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import attributes
from anthropic import Anthropic

from .database import get_db, AsyncSessionLocal
from .models import WizardSession
from enum import Enum

# PDF extraction (optional - graceful fallback)
try:
    import PyPDF2
    HAS_PDF_SUPPORT = True
except ImportError:
    HAS_PDF_SUPPORT = False
    logger.warning("PyPDF2 not installed - PDF upload will extract text only")

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

# Sonnet 4.5 for document analysis (1M token context)
SONNET_MODEL = "claude-sonnet-4-5-20250929"
SONNET_MAX_OUTPUT = 64000


# =============================================================================
# POSIT TYPE ENUM - 12-Dimension Grounded Typology
# =============================================================================

class PosItType(str, Enum):
    """
    Types of preliminary posits (claims detected in user's notes).
    Grounded in a 12-dimensional philosophical framework.

    Core 9 dimensions from our conceptual analysis framework,
    plus 3 additional dimensions for complex research programs.
    """
    # Sellarsian - Manifest vs Scientific image
    DEFINITIONAL = "definitional"  # What the concept IS (manifest/scientific formulation)

    # Brandomian - Inferential commitments
    INFERENTIAL = "inferential"  # What follows from accepting the concept
    INCOMPATIBILITY = "incompatibility"  # What the concept rules out

    # Carey + Blumenberg - Conceptual inheritance
    GENEALOGICAL = "genealogical"  # Where the concept comes from

    # Deleuzian - Lines of flight, deterritorialization
    TRANSFORMATIONAL = "transformational"  # What change/becoming this enables

    # Bachelardian - Epistemological breaks
    EPISTEMOLOGICAL_BREAK = "epistemological_break"  # What discontinuity it marks

    # Hacking - Styles of reasoning
    METHODOLOGICAL = "methodological"  # How to study/apply the concept

    # Canguilhem - Vital norms
    NORMATIVE = "normative"  # Evaluative/prescriptive claims

    # Quinean - Web of belief
    POSITIONAL = "positional"  # Where it sits in the belief web

    # === NEW: Extended dimensions for complex research programs ===

    # Kuhnian - Paradigm structure
    PARADIGMATIC = "paradigmatic"  # How concept relates to paradigm structure

    # Pragmatist - Performative consequences
    PERFORMATIVE = "performative"  # What using this concept DOES/enables

    # Foucauldian - Power-knowledge relations
    POWER_RELATIONAL = "power_relational"  # What power relations it naturalizes/contests


# Mapping from posit type to display labels and colors
POSIT_TYPE_METADATA = {
    PosItType.DEFINITIONAL: {
        "label": "Definitional",
        "description": "What the concept IS",
        "dimension": "Sellarsian",
        "color": "blue"
    },
    PosItType.INFERENTIAL: {
        "label": "Inferential",
        "description": "What follows from this",
        "dimension": "Brandomian",
        "color": "purple"
    },
    PosItType.INCOMPATIBILITY: {
        "label": "Incompatibility",
        "description": "What this rules out",
        "dimension": "Brandomian",
        "color": "red"
    },
    PosItType.GENEALOGICAL: {
        "label": "Genealogical",
        "description": "Where this comes from",
        "dimension": "Carey/Blumenberg",
        "color": "amber"
    },
    PosItType.TRANSFORMATIONAL: {
        "label": "Transformational",
        "description": "What change this enables",
        "dimension": "Deleuzian",
        "color": "green"
    },
    PosItType.EPISTEMOLOGICAL_BREAK: {
        "label": "Break",
        "description": "What discontinuity this marks",
        "dimension": "Bachelardian",
        "color": "orange"
    },
    PosItType.METHODOLOGICAL: {
        "label": "Methodological",
        "description": "How to study/apply this",
        "dimension": "Hacking",
        "color": "cyan"
    },
    PosItType.NORMATIVE: {
        "label": "Normative",
        "description": "Evaluative claims",
        "dimension": "Canguilhem",
        "color": "pink"
    },
    PosItType.POSITIONAL: {
        "label": "Positional",
        "description": "Where this sits in belief web",
        "dimension": "Quinean",
        "color": "gray"
    },
    # New dimensions for complex research programs
    PosItType.PARADIGMATIC: {
        "label": "Paradigmatic",
        "description": "How this relates to paradigm structure",
        "dimension": "Kuhnian",
        "color": "indigo"
    },
    PosItType.PERFORMATIVE: {
        "label": "Performative",
        "description": "What using this concept DOES",
        "dimension": "Pragmatist",
        "color": "teal"
    },
    PosItType.POWER_RELATIONAL: {
        "label": "Power-Relational",
        "description": "Power relations it naturalizes/contests",
        "dimension": "Foucauldian",
        "color": "rose"
    }
}


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


class EpistemicBlindSpot(BaseModel):
    """An epistemic gap or clarification need detected from notes/answers.

    Categories (epistemic, not ontological):
    - ambiguity: Terms/phrases with multiple valid readings
    - presupposition: What's being treated as "given" that isn't justified
    - paradigm_dependency: Where different epistemes produce different conclusions
    - likely_misreading: Common ways this concept could be misunderstood
    - gray_zone: Boundary cases where application is uncertain
    - unfilled_slot: Placeholder structures awaiting elaboration
    - unconfronted_challenge: Objections/problems not yet addressed
    """
    category: str = "ambiguity"  # One of the 7 epistemic categories
    description: str
    what_unclear: Optional[str] = None  # The unclear aspect
    what_would_help: Optional[str] = None  # What clarification would provide
    source: Optional[str] = None  # Which answer/note revealed this
    user_note: Optional[str] = None
    # Legacy support for existing sessions
    type: Optional[str] = None  # Maps to category for backward compat
    pole_a: Optional[str] = None  # Maps to what_unclear
    pole_b: Optional[str] = None  # Maps to what_would_help
    marked_as_dialectic: bool = False  # Deprecated but kept for compat


# Alias for backward compatibility
NewTensionFromAnswers = EpistemicBlindSpot


# =============================================================================
# CURATOR-SHARPENER TWO-STAGE QUESTIONING SYSTEM
# =============================================================================

class BlindSpotSlot(BaseModel):
    """A single question slot in the blind spots queue."""
    slot_id: str  # e.g., "slot_01"
    category: str  # One of 7 epistemic categories
    depth: int = 1  # 1=initial, 2=follow-up, 3=deep-dive
    question: Optional[str] = None
    status: str = "pending"  # pending, active, answered, skipped
    answer: Optional[str] = None
    generated_by: str = "curator"  # curator or sharpener
    parent_slot_id: Optional[str] = None  # For follow-ups (links to answered slot)
    blind_spot_ref: Optional[str] = None  # Reference to identified blind spot


class CuratorAllocation(BaseModel):
    """Curator's analysis and slot allocation plan."""
    total_slots: int  # Max 16
    category_weights: Dict[str, float]  # e.g., {"ambiguity": 0.25, "presupposition": 0.3}
    slot_sequence: List[str]  # Interleaved category order
    emphasis_rationale: str  # Why this allocation
    identified_blind_spots: List[EpistemicBlindSpot]  # All detected blind spots
    slots: List[BlindSpotSlot]  # Pre-generated initial questions


class BlindSpotsQueue(BaseModel):
    """The full question queue with dynamic updates."""
    slots: List[BlindSpotSlot]
    current_index: int = 0
    sharpener_pending: List[str] = []  # Slot IDs being generated
    completed_count: int = 0
    skipped_count: int = 0


class CurateBlindSpotsRequest(BaseModel):
    """Request to curate blind spots from notes."""
    concept_name: str
    notes: str
    notes_understanding: Optional[Dict[str, Any]] = None  # From notes preprocessing
    session_id: Optional[str] = None


class SharpenQuestionRequest(BaseModel):
    """Request to generate a deeper follow-up question."""
    session_id: str
    slot_id: str  # The slot that was just answered
    answer: str  # User's answer
    concept_name: str
    notes_context: Optional[str] = None
    previous_answers: Optional[List[Dict[str, Any]]] = None  # Context from other answers


class SubmitBlindSpotAnswerRequest(BaseModel):
    """Request to submit an answer to a blind spot question."""
    session_id: str
    slot_id: str
    answer: str
    skip: bool = False  # True if user skipped this question


class FinishBlindSpotsRequest(BaseModel):
    """Request to finish blind spots questioning early."""
    session_id: str


class GenerateAnswerOptionsRequest(BaseModel):
    """Request to generate multiple choice answer options for a blind spot question."""
    question: str
    category: str  # One of 7 epistemic categories
    concept_name: str
    notes_context: Optional[str] = None
    previous_answers: Optional[List[Dict[str, Any]]] = None


class AnswerOption(BaseModel):
    """A single answer option for multiple choice."""
    id: str  # e.g., "opt_1"
    text: str  # The answer text
    stance: str  # Type key: "assertive", "synthetic", "genealogical", etc.
    label: Optional[str] = None  # Display label: "ASSERTIVE", "SYNTHETIC", etc. (dynamically curated)


class GenerateAnswerOptionsResponse(BaseModel):
    """Response with generated answer options."""
    options: List[AnswerOption]
    guidance: str  # Brief guidance on how to use/interpret options
    mutually_exclusive: bool = True  # If True, user can only select one; if False, multi-select allowed
    exclusivity_reason: Optional[str] = None  # Why options are/aren't mutually exclusive


class BlindSpotAnswer(BaseModel):
    """A single blind spot question with its answer."""
    slot_id: str
    category: str  # One of 7 epistemic categories
    question: str
    answer: str
    depth: int = 1  # Question depth (1=original, 2=sharpened, 3=deep follow-up)


class GenerateInformedHypothesesRequest(BaseModel):
    """Request to generate hypothesis cards informed by blind spots answers."""
    concept_name: str
    notes: str
    blind_spots_answers: List[BlindSpotAnswer]
    session_id: Optional[str] = None


# Validity thresholds for graceful completion
MINIMUM_ANSWERS_FOR_VALIDITY = 3
IDEAL_ANSWERS_FOR_QUALITY = 8

QUALITY_MESSAGES = {
    'insufficient': "You've answered fewer than 3 questions. Consider answering a few more to help clarify your concept's epistemic positioning.",
    'minimal': "You've provided enough answers for a basic understanding. More answers would help refine the analysis.",
    'adequate': "Good coverage. We have enough to work with for meaningful blind spot analysis.",
    'comprehensive': "Excellent! Comprehensive answers will enable deep epistemic analysis."
}


def assess_completion_quality(queue: BlindSpotsQueue) -> str:
    """Returns: 'insufficient', 'minimal', 'adequate', 'comprehensive'"""
    answered = queue.completed_count
    if answered < 3:
        return 'insufficient'
    elif answered < 6:
        return 'minimal'
    elif answered < 10:
        return 'adequate'
    else:
        return 'comprehensive'


def interleave_slots(category_counts: Dict[str, int]) -> List[str]:
    """
    Distribute categories evenly across the sequence.
    Uses round-robin with remainder distribution.

    Example: {"ambiguity": 3, "presupposition": 2} ->
             ["ambiguity", "presupposition", "ambiguity", "presupposition", "ambiguity"]
    """
    result = []
    remaining = {k: v for k, v in category_counts.items() if v > 0}

    while remaining:
        for cat in list(remaining.keys()):
            result.append(cat)
            remaining[cat] -= 1
            if remaining[cat] == 0:
                del remaining[cat]

    return result


class InterimAnalysis(BaseModel):
    """Intermediate understanding shown between stages.

    Accepts multiple field name formats for backward compatibility:
    - epistemic_blind_spots (current)
    - new_tensions_from_answers (legacy v2)
    - tensions_detected, gaps_identified (legacy v1)
    """
    understanding_summary: str  # "Based on your answers, I understand..."
    key_commitments: List[str]  # Core positions you've taken
    # Current field name
    epistemic_blind_spots: Optional[List[EpistemicBlindSpot]] = None  # Epistemic gaps from answers
    # Legacy v2 field names (for backward compatibility)
    new_tensions_from_answers: Optional[List[EpistemicBlindSpot]] = None  # Alias for epistemic_blind_spots
    areas_needing_clarification: Optional[List[str]] = None  # Areas needing clarification
    # Legacy v1 field names (oldest format)
    tensions_detected: Optional[List[Tension]] = None  # Potential dialectics (old format)
    gaps_identified: Optional[List[str]] = None  # What we still need to know (old format)
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


class DeepCommitmentsRequest(BaseModel):
    """Request to generate deep philosophical commitment questions."""
    concept_name: str
    notes_summary: str
    genealogy: Any  # Can be dict or empty object
    stage1_answers: Any  # Can be list of answers or dict
    stage2_answers: Optional[Any] = None  # Can be list of answers or dict
    dimensional_extraction: Optional[Dict[str, Any]] = None  # From documents/notes
    source_id: Optional[int] = None


class Phase2QuestionsRequest(BaseModel):
    """Request to generate Phase 2 follow-up questions based on Phase 1 answers."""
    concept_name: str
    notes_summary: Optional[str] = None
    phase1_questions: List[Dict[str, Any]]  # Questions from Phase 1
    phase1_answers: Dict[str, Any]  # Answers to Phase 1 questions
    stage1_answers: Optional[List[Dict[str, Any]]] = None
    stage2_answers: Optional[List[Dict[str, Any]]] = None
    stage3_answers: Optional[List[Dict[str, Any]]] = None
    genealogy: Optional[List[Dict[str, Any]]] = None  # Approved genealogy
    dimensional_extraction: Optional[Dict[str, Any]] = None


class Phase3QuestionsRequest(BaseModel):
    """Request to generate Phase 3 synthesis/verification questions."""
    concept_name: str
    notes_summary: Optional[str] = None
    phase1_questions: List[Dict[str, Any]]
    phase1_answers: Dict[str, Any]
    phase2_questions: List[Dict[str, Any]]
    phase2_answers: Dict[str, Any]
    stage1_answers: Optional[List[Dict[str, Any]]] = None
    stage2_answers: Optional[List[Dict[str, Any]]] = None
    stage3_answers: Optional[List[Dict[str, Any]]] = None
    genealogy: Optional[List[Dict[str, Any]]] = None
    dimensional_extraction: Optional[Dict[str, Any]] = None


class DocumentAnalysisRequest(BaseModel):
    """Request to analyze an uploaded document."""
    concept_name: str
    existing_context: Optional[Dict[str, Any]] = None  # Notes analysis so far


class TransformCardRequest(BaseModel):
    """Request to transform a hypothesis/genealogy/differentiation card."""
    card_id: str
    card_type: str  # hypothesis, genealogy, differentiation, commitment
    card_content: str  # Current content of the card
    mode: str  # sharpen, generalize, radicalize, historicize, deepen
    guidance: Optional[str] = None  # Optional user guidance for transformation
    notes_context: Optional[str] = None  # Original notes for grounding
    concept_name: Optional[str] = None


class GenerateOptionsRequest(BaseModel):
    """Request to generate answer options for an open-ended question."""
    concept_name: str
    question_id: str
    question_text: str
    notes: Optional[str] = None  # User's original notes
    hypothesis_cards: Optional[List[Dict[str, Any]]] = None  # Validated hypothesis cards
    differentiation_cards: Optional[List[Dict[str, Any]]] = None  # Differentiation cards
    previous_answers: Optional[List[Dict[str, Any]]] = None  # Answers to earlier questions
    notes_understanding: Optional[Dict[str, Any]] = None  # LLM's understanding of notes


class GenerateGenealogyRequest(BaseModel):
    """Request to generate intellectual genealogy hypotheses."""
    concept_name: str
    notes: Optional[str] = None
    hypothesis_cards: Optional[List[Dict[str, Any]]] = None
    differentiation_cards: Optional[List[Dict[str, Any]]] = None
    stage1_answers: Optional[List[Dict[str, Any]]] = None
    stage2_answers: Optional[List[Dict[str, Any]]] = None
    stage3_answers: Optional[List[Dict[str, Any]]] = None
    notes_understanding: Optional[Dict[str, Any]] = None


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

## GENEALOGY INFERENCE (Critical - Use Your Knowledge!)
You are Claude Opus 4.5 with extensive knowledge of intellectual history, philosophy, social sciences, and academic traditions.
USE THIS KNOWLEDGE to HYPOTHESIZE the likely genealogy of this concept.

Based on the concept's:
- Domain and field (what academic traditions does this touch?)
- Terminology used (what frameworks use similar language?)
- Problem framing (what traditions address similar problems?)
- Adjacent concepts mentioned (who else has worked on related ideas?)

ACTIVELY INFER likely influences even if NOT explicitly stated. The user may not know the intellectual lineage of their own ideas - help them discover it.

For example:
- If discussing "power dynamics in tech" → likely influenced by Foucault, STS, critical theory
- If framing "sovereignty" in non-territorial terms → IR theory, Krasner, Ruggie, possibly Agamben
- If synthesizing economics + politics → political economy tradition, possibly IPE
- If discussing "recognition" or "identity" → likely Hegel, Taylor, Honneth tradition

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
        "hypothesized_influences": [
            {{
                "name": "Thinker/Framework name",
                "type": "thinker|framework|tradition|concept",
                "why_hypothesized": "Why you infer this influence (terminology, framing, domain)",
                "confidence": "high|medium|low",
                "source_excerpt": "Quote from notes if explicitly mentioned, or null if inferred"
            }}
        ],
        "emergence_context": {{
            "domain": "academic|professional|personal|mixed",
            "field": "Specific field (e.g., political theory, STS, IR)",
            "inferred_trigger": "Best guess at what sparked this concept"
        }},
        "genealogy_questions": [
            {{
                "id": "primary_tradition",
                "question": "Which intellectual tradition does this concept most draw from?",
                "type": "multiple_choice",
                "options": [
                    {{"value": "tradition_1", "label": "Tradition Name", "description": "Brief explanation"}},
                    {{"value": "tradition_2", "label": "Another Tradition", "description": "Why this might fit"}}
                ],
                "rationale": "Why you're asking this - what it will clarify"
            }},
            {{
                "id": "key_thinker",
                "question": "Whose work does this concept most resemble or build on?",
                "type": "multiple_choice",
                "options": [
                    {{"value": "thinker_1", "label": "Thinker Name", "description": "Their relevant contribution"}},
                    {{"value": "thinker_2", "label": "Another Thinker", "description": "How they relate"}}
                ],
                "rationale": "Why identifying the key influence matters"
            }},
            {{
                "id": "genesis_experience",
                "question": "What type of experience primarily shaped this concept?",
                "type": "multiple_choice",
                "options": [
                    {{"value": "academic_reading", "label": "Academic reading/research", "description": "Scholarly engagement"}},
                    {{"value": "professional_practice", "label": "Professional practice", "description": "Work experience"}},
                    {{"value": "personal_observation", "label": "Personal observation", "description": "Life experience"}},
                    {{"value": "theoretical_gap", "label": "Theoretical gap identified", "description": "Saw what was missing"}}
                ],
                "rationale": "Understanding origin helps frame the concept appropriately"
            }}
        ],
        "open_ended_question": {{
            "question": "One focused question that cannot be answered via MC - only if truly necessary",
            "why_needed": "Explain why this can't be inferred or offered as options"
        }}
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
    "epistemic_blind_spots": [
        {{
            "category": "ambiguity|presupposition|paradigm_dependency|likely_misreading|gray_zone|unfilled_slot|unconfronted_challenge",
            "description": "Description of this epistemic gap - what the user hasn't yet made explicit",
            "what_unclear": "The specific aspect that needs clarification",
            "what_would_help": "What kind of clarification would help surface the user's positioning",
            "productive_potential": "Why exploring this would help the user articulate their priors"
        }}
    ],

    "hypothesis_cards": [
        {{
            "id": "hyp_001",
            "content": "A specific thesis/claim you detect in the notes - stated as a concrete proposition, not a question",
            "type": "thesis|assumption|tension|methodological|normative",
            "source_excerpts": ["Direct quotes from notes that support this inference"],
            "confidence": "high|medium|low",
            "rationale": "Why you think this is a central claim (1-2 sentences)"
        }}
    ],

    "genealogy_cards": [
        {{
            "id": "gen_001",
            "thinker": "Specific Thinker Name (e.g., Karl Polanyi, not 'political economists')",
            "tradition": "Specific tradition this thinker belongs to",
            "connection": "Your concept [X] resembles/extends/builds on [thinker's] idea of [specific concept] because [specific reason]",
            "source_excerpts": ["Quote from notes if explicitly mentioned, or null if inferred"],
            "confidence": "high|medium|low",
            "why_relevant": "Why this genealogical connection matters for the user's project"
        }}
    ],

    "differentiation_cards": [
        {{
            "id": "diff_001",
            "your_concept": "The user's concept name",
            "contrasted_with": "Specific adjacent concept/framework to differentiate from",
            "thinker_associated": "Who is most associated with the adjacent concept",
            "difference": "Your concept is NOT [X] because [specific difference in mechanism, scope, or approach]",
            "source_excerpts": ["Quote from notes that supports this differentiation"],
            "confidence": "high|medium|low"
        }}
    ],

    "dimensional_signals": {{
        "quinean": {{
            "inferences_detected": ["Any 'if X then Y' patterns in notes"],
            "centrality_hint": "core|intermediate|peripheral|unknown",
            "confidence": "high|medium|low"
        }},
        "sellarsian": {{
            "givenness_markers": ["Phrases like 'obviously', 'naturally', 'clearly' that suggest treating as given"],
            "hidden_assumptions": ["Assumptions not argued for"],
            "confidence": "high|medium|low"
        }},
        "brandomian": {{
            "implicit_commitments": ["What using this concept commits one to"],
            "implicit_entitlements": ["What claims the concept enables"],
            "confidence": "high|medium|low"
        }},
        "deleuzian": {{
            "problem_addressed": "Core tension/problem the concept navigates",
            "tension_poles": ["Pole A", "Pole B"],
            "becomings_enabled": ["Transformations the concept enables"],
            "becomings_blocked": ["Transformations foreclosed"],
            "confidence": "high|medium|low"
        }},
        "bachelardian": {{
            "breaking_from": "What framework/concept is being ruptured",
            "why_inadequate": "What's wrong with the old way",
            "obstacle_risk": "Could this concept become an obstacle itself?",
            "confidence": "high|medium|low"
        }},
        "canguilhem": {{
            "values_embedded": ["Values implicit in the concept"],
            "whose_interests": "Who benefits from this concept",
            "what_excluded": "What gets marked as abnormal",
            "confidence": "high|medium|low"
        }},
        "davidson": {{
            "reasoning_style": "quantitative|historical|structural|phenomenological|dialectical|mixed",
            "makes_visible": ["What this lens reveals"],
            "makes_invisible": ["What it might obscure"],
            "confidence": "high|medium|low"
        }},
        "blumenberg": {{
            "root_metaphor": "Any underlying metaphor detected",
            "source_domain": "Where the metaphor comes from",
            "metaphor_work": "Conceptual work being done",
            "confidence": "high|medium|low"
        }},
        "carey": {{
            "component_concepts": ["Simpler concepts this is built from"],
            "combination_type": "aggregation|interaction|emergence|unknown",
            "what_emerges": "What's new beyond the components",
            "confidence": "high|medium|low"
        }},
        "kuhnian": {{
            "paradigm_position": "normal_science|anomaly|crisis|revolutionary|post_revolutionary",
            "exemplars": ["Paradigmatic cases that define proper use"],
            "puzzle_solving_rules": ["What counts as legitimate puzzles/solutions"],
            "incommensurabilities": ["What frameworks cannot communicate with this concept"],
            "disciplinary_matrix": "What shared commitments enable this concept's use",
            "confidence": "high|medium|low"
        }},
        "foucauldian": {{
            "power_knowledge_nexus": "What power relations does this concept encode/enable",
            "governmentality_mode": "discipline|security|sovereign|pastoral|neoliberal|other",
            "subjectification_effects": ["What kinds of subjects does this concept produce"],
            "discourse_formation": "What statements become possible/impossible",
            "resistance_points": ["Where might this power-knowledge be contested"],
            "confidence": "high|medium|low"
        }},
        "pragmatist": {{
            "practical_consequences": ["What difference does accepting this concept make in practice"],
            "cash_value": "The concept's practical meaning in experiential terms",
            "performative_effects": ["What does using this concept DO in the world"],
            "habit_formations": ["What patterns of action does this concept enable/block"],
            "inquiry_context": "What problematic situation generated this concept",
            "confidence": "high|medium|low"
        }}
    }}
}}

Be conservative with pre-fills: only suggest values when you have clear evidence from the notes.
If the notes don't provide enough information for a question, set suggested_value to null.

## 12-DIMENSIONAL EXTRACTION INSTRUCTIONS:
Extract preliminary signals for ALL 12 philosophical dimensions. Even if notes are sparse:
- QUINEAN: Look for logical implications ("if X then Y", "X implies Y")
- SELLARSIAN: Spot "givenness" language (obviously, naturally, clearly, of course)
- BRANDOMIAN: What does using this concept commit you to? What does it entitle you to claim?
- DELEUZIAN: What problem/tension does this navigate? What transformations enabled/blocked?
- BACHELARDIAN: What is this BREAKING FROM? What's wrong with the old way?
- CANGUILHEM: What values are embedded? Whose interests served? What excluded?
- DAVIDSON: What reasoning style does this require? What becomes visible/invisible?
- BLUMENBERG: Is there a root metaphor underlying the concept?
- CAREY: What simpler concepts is this built from?
- KUHNIAN: Is this normal science or paradigm-challenging? What exemplars define it? What's incommensurable?
- FOUCAULDIAN: What power-knowledge relations does this encode? What subjects does it produce? What discourse rules?
- PRAGMATIST: What practical difference does this make? What does using it DO? What habits does it form?

Set confidence to "low" if you're inferring without explicit evidence.

## EPISTEMIC BLIND SPOTS INSTRUCTIONS (CRITICAL - Surface User's Positioning):
These are NOT problems with the concept itself, but places where the USER'S epistemic positioning isn't yet explicit.
The goal is to help users articulate their priors, confront structural limits of their framing, and grasp conditions of possibility.

Generate 3-6 epistemic blind spots across these 7 categories (use the 9D analysis to inform):

1. **AMBIGUITY** - Terms/phrases with multiple valid readings
   - Look for key terms that could mean different things in different contexts
   - Source: Brandomian (perspectival content), Blumenberg (metaphors that do conceptual work)
   - Example: "The term 'sovereignty' in your notes could mean Westphalian territorial sovereignty OR decisionist authority OR popular sovereignty"

2. **PRESUPPOSITION** - What's being treated as "given" that isn't justified
   - Look for Sellarsian markers: "obviously," "naturally," "clearly," "of course"
   - What's assumed without argument? What's the "plane" enabling this thinking?
   - Source: Sellarsian (givenness), Deleuzian (plane assumptions)
   - Example: "You seem to assume that digital platforms inherently tend toward monopoly - this requires argument"

3. **PARADIGM_DEPENDENCY** - Where different epistemes would produce different conclusions
   - What reasoning style is being used? What would a different tradition see?
   - Source: Hacking (reasoning styles), Bachelardian (regional rationality)
   - Example: "A Marxist reading would emphasize class dynamics while a Foucauldian reading would focus on governmentality - which is your frame?"

4. **LIKELY_MISREADING** - Common ways this concept could be misunderstood
   - What de dicto/de re confusions might arise? What incommensurabilities exist?
   - Source: Brandomian (perspectival content), Carey (incommensurability)
   - Example: "Readers might confuse your 'organic capitalism' with Polanyi's 'embedded economy' - they differ in X"

5. **GRAY_ZONE** - Boundary cases where application is uncertain
   - Where are the edges of the concept's applicability?
   - Source: Quinean (web tensions), Canguilhem (milieu boundaries)
   - Example: "It's unclear whether your concept applies to pre-digital platform capitalism (Sears, etc.)"

6. **UNFILLED_SLOT** - Placeholder structures awaiting elaboration
   - What conceptual slots haven't been filled in yet?
   - Source: Carey (placeholder structures), Quinean (missing inferences)
   - Example: "You identify three modes but only elaborate two - what's the third?"

7. **UNCONFRONTED_CHALLENGE** - Objections/problems not yet addressed
   - What obvious objections could be raised? What obstacles might block understanding?
   - Source: Brandomian (challenges), Bachelardian (epistemological obstacles)
   - Example: "The concept seems vulnerable to the objection that all capitalism is already 'organic' in some sense"

IMPORTANT: These are EPISTEMIC (about the user's grasp/positioning) not ONTOLOGICAL (about the object itself being indeterminate).
Dialectics/tensions belong in the Dialectics section. Epistemic blind spots are about what WE haven't yet worked through.

GENEALOGY CRITICAL INSTRUCTIONS:
1. HYPOTHESIZE influences aggressively using your knowledge - the user may not know their own intellectual lineage
2. Generate 2-4 MULTIPLE CHOICE questions with domain-specific options (not generic)
   - Options should reflect YOUR HYPOTHESIS about likely influences based on the concept
   - Each option should be a real thinker, tradition, or framework relevant to this specific concept
3. Only include ONE open_ended_question if absolutely necessary - and explain why it can't be MC
4. If notes are rich enough, open_ended_question can be null
5. The goal: user validates/corrects your hypotheses rather than generating from scratch

## CARD GENERATION INSTRUCTIONS (CRITICAL - THIS IS THE CORE OUTPUT):

### HYPOTHESIS CARDS (Generate 5-8):
These are CLAIMS/THESES you detect in the notes. NOT questions. Concrete propositions the user can approve/reject.
- Each card is a specific claim stated as an assertion
- Pull source_excerpts directly from the notes
- Types: thesis (core argument), assumption (implicit premise), tension (internal conflict), methodological (how to study), normative (what should be)
- Example: "Your concept argues that platform-mediated capitalism exercises planning and control while maintaining market appearances"

### GENEALOGY CARDS (Generate 3-5):
These identify SPECIFIC thinkers/frameworks the concept builds on. NOT traditions - PEOPLE with NAMES.
- Each card names a specific thinker and their specific contribution
- Example: NOT "critical theory" but "Theodor Adorno's concept of the culture industry"
- The connection field should explain the SPECIFIC link: "Your concept of X resembles/extends/inverts Y's idea of Z"
- If notes explicitly mention a thinker, quote it. If inferring, explain your reasoning.

### DIFFERENTIATION CARDS (Generate 4-6):
These show what the concept is NOT. Help user clarify by contrast.
- Identify adjacent concepts that might be confused with the user's concept
- Name the thinker most associated with that adjacent concept
- State the key difference: scope, mechanism, focus, politics, etc.
- Example: "Your concept is NOT surveillance capitalism (Zuboff) because you emphasize production/planning while Zuboff emphasizes extraction/prediction"

REMEMBER: Cards are for user to APPROVE/REJECT/TRANSFORM - not questions to answer. Generate claims the user can validate."""


# =============================================================================
# INITIAL ANALYSIS PROMPT - Used before blind spots (no hypothesis cards)
# =============================================================================
INITIAL_ANALYSIS_PROMPT = """You are an expert in conceptual analysis helping a user articulate a novel theoretical concept.

The user has provided initial notes about a concept they're developing called "{concept_name}". Your task is to:
1. Extract what can be inferred from these notes
2. Identify epistemic blind spots - where the user's positioning isn't yet explicit
3. Prepare the ground for deeper questioning

## User's Notes:
{notes}

## 9-DIMENSIONAL EXTRACTION INSTRUCTIONS:
Extract preliminary signals for ALL 9 philosophical dimensions. Even if notes are sparse:
- QUINEAN: Look for logical implications ("if X then Y", "X implies Y")
- SELLARSIAN: Spot "givenness" language (obviously, naturally, clearly, of course)
- BRANDOMIAN: What does using this concept commit you to? What does it entitle you to claim?
- DELEUZIAN: What problem/tension does this navigate? What transformations enabled/blocked?
- BACHELARDIAN: What is this BREAKING FROM? What's wrong with the old way?
- CANGUILHEM: What values are embedded? Whose interests served? What excluded?
- DAVIDSON: What reasoning style does this require? What becomes visible/invisible?
- BLUMENBERG: Is there a root metaphor underlying the concept?
- CAREY: What simpler concepts is this built from?

Set confidence to "low" if you're inferring without explicit evidence.

## EPISTEMIC BLIND SPOTS INSTRUCTIONS (CRITICAL - Surface User's Positioning):
These are NOT problems with the concept itself, but places where the USER'S epistemic positioning isn't yet explicit.
The goal is to help users articulate their priors, confront structural limits of their framing, and grasp conditions of possibility.

Generate 3-6 epistemic blind spots across these 7 categories (use the 9D analysis to inform):

1. **AMBIGUITY** - Terms/phrases with multiple valid readings
   - Look for key terms that could mean different things in different contexts
   - Source: Brandomian (perspectival content), Blumenberg (metaphors that do conceptual work)

2. **PRESUPPOSITION** - What's being treated as "given" that isn't justified
   - Look for Sellarsian markers: "obviously," "naturally," "clearly," "of course"
   - What's assumed without argument? What's the "plane" enabling this thinking?
   - Source: Sellarsian (givenness), Deleuzian (plane assumptions)

3. **PARADIGM_DEPENDENCY** - Where different epistemes would produce different conclusions
   - What reasoning style is being used? What would a different tradition see?
   - Source: Hacking (reasoning styles), Bachelardian (regional rationality)

4. **LIKELY_MISREADING** - Common ways this concept could be misunderstood
   - What de dicto/de re confusions might arise? What incommensurabilities exist?
   - Source: Brandomian (perspectival content), Carey (incommensurability)

5. **GRAY_ZONE** - Boundary cases where application is uncertain
   - Where are the edges of the concept's applicability?
   - Source: Quinean (web tensions), Canguilhem (milieu boundaries)

6. **UNFILLED_SLOT** - Placeholder structures awaiting elaboration
   - What conceptual slots haven't been filled in yet?
   - Source: Carey (placeholder structures), Quinean (missing inferences)

7. **UNCONFRONTED_CHALLENGE** - Objections/problems not yet addressed
   - What obvious objections could be raised? What obstacles might block understanding?
   - Source: Brandomian (challenges), Bachelardian (epistemological obstacles)

IMPORTANT: These are EPISTEMIC (about the user's grasp/positioning) not ONTOLOGICAL (about the object itself being indeterminate).

Analyze the notes and produce a JSON response:
{{
    "notes_analysis": {{
        "summary": "Brief summary of what the user is trying to articulate (2-3 sentences)",
        "key_insights": ["Main ideas extracted from the notes"],
        "preliminary_definition": "A working definition extracted/synthesized from the notes"
    }},
    "epistemic_blind_spots": [
        {{
            "category": "ambiguity|presupposition|paradigm_dependency|likely_misreading|gray_zone|unfilled_slot|unconfronted_challenge",
            "description": "Description of this epistemic gap - what the user hasn't yet made explicit",
            "what_unclear": "The specific aspect that needs clarification",
            "what_would_help": "What kind of clarification would help surface the user's positioning",
            "productive_potential": "Why exploring this would help the user articulate their priors"
        }}
    ],
    "dimensional_signals": {{
        "quinean": {{
            "inferences_detected": ["Any 'if X then Y' patterns in notes"],
            "centrality_hint": "core|intermediate|peripheral|unknown",
            "confidence": "high|medium|low"
        }},
        "sellarsian": {{
            "givenness_markers": ["Phrases like 'obviously', 'naturally', 'clearly' that suggest treating as given"],
            "hidden_assumptions": ["Assumptions not argued for"],
            "confidence": "high|medium|low"
        }},
        "brandomian": {{
            "implicit_commitments": ["What using this concept commits one to"],
            "implicit_entitlements": ["What claims the concept enables"],
            "confidence": "high|medium|low"
        }},
        "deleuzian": {{
            "problem_addressed": "Core tension/problem the concept navigates",
            "tension_poles": ["Pole A", "Pole B"],
            "becomings_enabled": ["Transformations the concept enables"],
            "becomings_blocked": ["Transformations foreclosed"],
            "confidence": "high|medium|low"
        }},
        "bachelardian": {{
            "breaking_from": "What framework/concept is being ruptured",
            "why_inadequate": "What's wrong with the old way",
            "obstacle_risk": "Could this concept become an obstacle itself?",
            "confidence": "high|medium|low"
        }},
        "canguilhem": {{
            "values_embedded": ["Values implicit in the concept"],
            "whose_interests": "Who benefits from this concept",
            "what_excluded": "What gets marked as abnormal",
            "confidence": "high|medium|low"
        }},
        "davidson": {{
            "reasoning_style": "quantitative|historical|structural|phenomenological|dialectical|mixed",
            "makes_visible": ["What this lens reveals"],
            "makes_invisible": ["What it might obscure"],
            "confidence": "high|medium|low"
        }},
        "blumenberg": {{
            "root_metaphor": "Any underlying metaphor detected",
            "source_domain": "Where the metaphor comes from",
            "metaphor_work": "Conceptual work being done",
            "confidence": "high|medium|low"
        }},
        "carey": {{
            "component_concepts": ["Simpler concepts this is built from"],
            "combination_type": "aggregation|interaction|emergence|unknown",
            "what_emerges": "What's new beyond the components",
            "confidence": "high|medium|low"
        }},
        "kuhnian": {{
            "paradigm_position": "normal_science|anomaly|crisis|revolutionary|post_revolutionary",
            "exemplars": ["Paradigmatic cases that define proper use"],
            "puzzle_solving_rules": ["What counts as legitimate puzzles/solutions"],
            "incommensurabilities": ["What frameworks cannot communicate with this concept"],
            "disciplinary_matrix": "What shared commitments enable this concept's use",
            "confidence": "high|medium|low"
        }},
        "foucauldian": {{
            "power_knowledge_nexus": "What power relations does this concept encode/enable",
            "governmentality_mode": "discipline|security|sovereign|pastoral|neoliberal|other",
            "subjectification_effects": ["What kinds of subjects does this concept produce"],
            "discourse_formation": "What statements become possible/impossible",
            "resistance_points": ["Where might this power-knowledge be contested"],
            "confidence": "high|medium|low"
        }},
        "pragmatist": {{
            "practical_consequences": ["What difference does accepting this concept make in practice"],
            "cash_value": "The concept's practical meaning in experiential terms",
            "performative_effects": ["What does using this concept DO in the world"],
            "habit_formations": ["What patterns of action does this concept enable/block"],
            "inquiry_context": "What problematic situation generated this concept",
            "confidence": "high|medium|low"
        }}
    }}
}}

Be thorough with epistemic blind spots - they will inform the questioning phase that follows.
The goal is to surface what needs to be explored with the user, not to generate hypotheses yet."""


# =============================================================================
# INFORMED HYPOTHESIS GENERATION PROMPT - Used AFTER blind spots questioning
# =============================================================================
INFORMED_HYPOTHESIS_GENERATION_PROMPT = """You are an expert in conceptual analysis helping a user articulate a novel theoretical concept.

The user has provided initial notes about their concept "{concept_name}" and has completed a round of epistemic blind spots questioning. Based on their answers to blind spots questions, you now have insight into their actual theoretical agenda.

Your task: Generate POSIT cards (preliminary claims), genealogy cards, and differentiation cards INFORMED by what the user revealed through their blind spots answers.

## User's Original Notes:
{notes}

## Blind Spots Questions and User's Answers (CRITICAL CONTEXT):
{blind_spots_context}

## What This Reveals About the User's Theoretical Agenda:
Based on their answers, pay attention to:
- Which blind spots they found most relevant (reveals what they care about)
- Positions they articulated (reveals their actual commitments)
- Tensions they acknowledged (reveals dialectics they're navigating)
- Presuppositions they confirmed or rejected (reveals their epistemic stance)

## POSIT CARD TYPOLOGY (12-Dimension Grounded):
Each posit card has a TYPE grounded in our philosophical framework:

### Core 9 Dimensions:

1. **definitional** (Sellarsian) - What the concept IS in manifest/scientific terms
   Example: "Organic capitalism synthesizes planning and market forms through platform coordination"

2. **inferential** (Brandomian) - What follows from accepting this concept
   Example: "If organic capitalism is correct, then the market/plan dichotomy collapses"

3. **incompatibility** (Brandomian) - What the concept rules out
   Example: "Incompatible with accounts treating platforms as mere intermediaries"

4. **genealogical** (Carey/Blumenberg) - Where the concept comes from
   Example: "Transforms Hilferding's 'organized capitalism' for the platform age"

5. **transformational** (Deleuzian) - What change/becoming this enables
   Example: "Deterritorializes the market/plan binary by showing their co-constitution"

6. **epistemological_break** (Bachelardian) - What discontinuity it marks
   Example: "Marks a break with classical political economy's dichotomies"

7. **methodological** (Hacking) - How to study/apply the concept
   Example: "Requires tracing both computational and organizational mechanisms"

8. **normative** (Canguilhem) - Evaluative/prescriptive claims
   Example: "Platform coordination represents a pathological form of economic organization"

9. **positional** (Quinean) - Where it sits in the belief web
   Example: "Central to understanding contemporary capitalism, peripheral to orthodox Marxism"

### Extended Dimensions (for complex research programs):

10. **paradigmatic** (Kuhnian) - How concept relates to paradigm structure
    Example: "Paradigm-constitutive for platform studies; anomalous for orthodox Marxist periodization"

11. **performative** (Pragmatist) - What using this concept DOES/enables in practice
    Example: "Using 'organic capitalism' reframes policy debates from market-vs-state to coordination-vs-autonomy"

12. **power_relational** (Foucauldian) - What power relations it naturalizes or contests
    Example: "Denaturalizes platform power as 'mere market efficiency'; reveals it as managerial coordination"

## GENEALOGY INFERENCE (Use User's Revealed Positions):
You are Claude Opus 4.5 with extensive knowledge of intellectual history.
USE THIS KNOWLEDGE to HYPOTHESIZE the likely genealogy - but now INFORMED by what the user actually cares about.

Based on their blind spots answers, you know more about:
- What traditions they're drawing from (from their presupposition responses)
- What distinctions matter to them (from their ambiguity responses)
- What challenges they recognize (from their unconfronted_challenge responses)

Generate a JSON response:
{{
    "posit_cards": [
        {{
            "id": "pos_001",
            "content": "A specific claim that addresses what the user revealed they care about",
            "type": "definitional|inferential|incompatibility|genealogical|transformational|epistemological_break|methodological|normative|positional|paradigmatic|performative|power_relational",
            "dimension": "Sellarsian|Brandomian|Carey/Blumenberg|Deleuzian|Bachelardian|Hacking|Canguilhem|Quinean|Kuhnian|Pragmatist|Foucauldian",
            "source_excerpts": ["Direct quotes from notes that support this"],
            "informed_by": "Which blind spot answer(s) helped refine this posit",
            "confidence": "high|medium|low",
            "rationale": "Why this is a central claim based on both notes AND blind spots answers"
        }}
    ],

    "genealogy_cards": [
        {{
            "id": "gen_001",
            "thinker": "Specific Thinker Name (e.g., Karl Polanyi, not 'political economists')",
            "tradition": "Specific tradition this thinker belongs to",
            "connection": "Your concept [X] resembles/extends/builds on [thinker's] idea of [specific concept] because [specific reason]",
            "informed_by": "How user's blind spot answers informed this genealogical connection",
            "source_excerpts": ["Quote from notes if explicitly mentioned, or null if inferred"],
            "confidence": "high|medium|low",
            "why_relevant": "Why this genealogical connection matters for what the user is trying to do"
        }}
    ],

    "differentiation_cards": [
        {{
            "id": "diff_001",
            "your_concept": "The user's concept name",
            "contrasted_with": "Specific adjacent concept/framework to differentiate from",
            "thinker_associated": "Who is most associated with the adjacent concept",
            "difference": "Your concept is NOT [X] because [specific difference]",
            "informed_by": "Which blind spot responses help clarify this distinction",
            "source_excerpts": ["Quote from notes that supports this differentiation"],
            "confidence": "high|medium|low"
        }}
    ],

    "genealogy_questions": [
        {{
            "id": "primary_tradition",
            "question": "Question about intellectual tradition, refined by what we learned",
            "type": "multiple_choice",
            "options": [
                {{"value": "tradition_1", "label": "Tradition Name", "description": "Brief explanation"}}
            ],
            "rationale": "Why you're asking this based on what the user revealed"
        }}
    ]
}}

CRITICAL INSTRUCTIONS:
1. Generate 10-15 posit cards using the 12-TYPE TYPOLOGY above
2. ENSURE COVERAGE: Include at least one posit from each of these dimension groups:
   - Definitional/Inferential/Incompatibility (Sellarsian/Brandomian)
   - Genealogical/Transformational/Break (Carey/Deleuzian/Bachelardian)
   - Methodological/Normative/Positional (Hacking/Canguilhem/Quinean)
   - Paradigmatic/Performative/Power-Relational (Kuhnian/Pragmatist/Foucauldian)
3. Generate 3-5 genealogy cards linking to SPECIFIC thinkers relevant to user's revealed agenda
4. Generate 4-6 differentiation cards that clarify distinctions the user is navigating
5. Each card should reference how blind spots answers informed it
6. Be SPECIFIC - use the user's actual terminology and concerns from their answers
7. Don't cluster all cards in one type - spread across dimensions for comprehensive coverage

The cards should feel tailored to this specific user's project, not generic philosophical categories."""


INTERIM_ANALYSIS_PROMPT = """You are an expert in conceptual analysis helping a user articulate a novel theoretical concept.

The user has completed Stage 1 questions about their concept "{concept_name}". Your task is to:
1. Synthesize their answers into an interim understanding
2. Identify key commitments they've made
3. Detect NEW epistemic blind spots DIFFERENT from those already identified (see below)
4. Identify areas that need addressing in Stage 2

## User's Stage 1 Answers:
{stage1_answers}

## Dialectics Marked by User During Stage 1:
{marked_dialectics}

## IMPORTANT - Epistemic Blind Spots Already Identified (DO NOT DUPLICATE):
{already_identified_tensions}

The items listed above were already identified during the initial notes analysis and confirmed by the user.
You must identify NEW epistemic blind spots that emerged from the Stage 1 answers - different from those already listed.
Look for blind spots that arise specifically from the ANSWERS provided, not from the original notes.

## The 7 Epistemic Categories:
1. AMBIGUITY - Terms with multiple valid readings
2. PRESUPPOSITION - What's treated as "given" without justification
3. PARADIGM_DEPENDENCY - Where different epistemes produce different conclusions
4. LIKELY_MISREADING - Common ways this could be misunderstood
5. GRAY_ZONE - Boundary cases where application is uncertain
6. UNFILLED_SLOT - Placeholder structures awaiting elaboration
7. UNCONFRONTED_CHALLENGE - Objections not yet addressed

Produce a JSON response with:
{{
    "interim_analysis": {{
        "understanding_summary": "Based on your answers, I understand that [concept_name] is... (2-3 sentences)",
        "key_commitments": ["List 3-5 core positions the user has taken"],
        "epistemic_blind_spots": [
            {{
                "category": "ambiguity|presupposition|paradigm_dependency|likely_misreading|gray_zone|unfilled_slot|unconfronted_challenge",
                "description": "Brief description of this NEW epistemic blind spot",
                "what_unclear": "The specific aspect that needs clarification",
                "what_would_help": "What clarification would surface the user's positioning",
                "source": "Which Stage 1 answer(s) revealed this"
            }}
        ],
        "areas_needing_clarification": ["Aspects that need more exploration in Stage 2"],
        "preliminary_definition": "A working 1-paragraph definition based on what we know so far"
    }}
}}

Be specific to what the user actually said. Don't fabricate or assume beyond their answers.
Remember: NEW blind spots only - do not repeat items from the "Already Identified" list above.
These are EPISTEMIC (about user's positioning) not ONTOLOGICAL (about the object being indeterminate).
The goal is to help users articulate their priors and grasp conditions of possibility for their thinking."""


STAGE2_GENERATION_PROMPT = """Based on the user's Stage 1 answers about their novel concept "{concept_name}":

## Stage 1 Responses:
{stage1_summary}

## Interim Analysis:
{interim_analysis}

## Adjacent Concepts Selected:
{adjacent_concepts}

## Confirmed Epistemic Blind Spots to Address:
{approved_items}

Generate 4-6 Stage 2 questions that:
1. **Surface presuppositions** - Questions that help make explicit what the user is treating as "given"
2. **Clarify paradigm positioning** - Questions that help the user articulate which epistemic framework they're operating in
3. **Address ambiguities** - Questions that force clarification of terms with multiple valid readings
4. **Anticipate misreadings** - Questions that help the user distinguish their concept from likely confusions
5. **Sharpen distinctions** from adjacent concepts
6. **Test commitments** they've made to see if they hold under scrutiny

PRIORITY: Questions should directly address the epistemic blind spots the user has confirmed as relevant.
The goal is to help the user articulate their priors and positioning, not to resolve uncertainties prematurely.

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

## Gaps, Tensions & Open Questions:
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
        "areas_still_developing": ["Gaps, tensions, or questions that are still being explored"],
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
    # Tensions already identified from notes preprocessing (Validate Understanding stage)
    approved_tensions_from_notes: Optional[List[str]] = None


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
    # Deep Commitments from 9-dimensional probing (Stage 4)
    deep_commitments: Optional[Dict[str, Any]] = None  # Answers to deep philosophical questions
    dimensional_extraction: Optional[Dict[str, Any]] = None  # 9-dim data from documents/notes
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
# WIZARD SESSION SCHEMAS (Cross-device persistence)
# =============================================================================

class WizardSessionCreate(BaseModel):
    """Create or update a wizard session."""
    session_key: Optional[str] = None  # If None, generates new UUID
    concept_name: str
    session_state: Dict[str, Any]  # Full wizard state
    stage: Optional[str] = None
    source_id: Optional[int] = None


class WizardSessionResponse(BaseModel):
    """Response for wizard session."""
    id: int
    session_key: str
    concept_name: str
    session_state: Dict[str, Any]
    stage: Optional[str] = None
    source_id: Optional[int] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WizardSessionListItem(BaseModel):
    """Summary item for session list."""
    id: int
    session_key: str
    concept_name: str
    stage: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


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
    "gaps_tensions_questions": [
        {{
            "type": "gap|tension|question",
            "description": "Description of the gap, tension, or open question detected",
            "pole_a": "For tensions: one side. For gaps/questions: what's unclear",
            "pole_b": "For tensions: opposing side. For gaps/questions: what clarification would help",
            "productive_potential": "Why exploring this would help develop the concept"
        }}
    ],
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


GENERATE_BLIND_SPOTS_PROMPT = """You are an expert in conceptual analysis helping identify EPISTEMIC BLIND SPOTS in a novel concept.

## Concept Name: {concept_name}

## User's Notes:
{notes}

## Current Understanding Summary:
{understanding_summary}

## Preliminary Definition:
{preliminary_definition}

## Existing Blind Spots Already Identified:
{existing_tensions}

## Blind Spots Already Confirmed by User:
{approved_tensions}

Generate 2-3 ADDITIONAL epistemic blind spots. These are NOT problems with the concept itself, but places where the USER'S epistemic positioning isn't yet explicit.

## The 7 Epistemic Categories:

1. **AMBIGUITY** - Terms/phrases with multiple valid readings
   - Key terms that could mean different things in different contexts

2. **PRESUPPOSITION** - What's being treated as "given" that isn't justified
   - Look for: "obviously," "naturally," "clearly," "of course"
   - What's assumed without argument?

3. **PARADIGM_DEPENDENCY** - Where different epistemes would produce different conclusions
   - What reasoning style is being used? What would a different tradition see?

4. **LIKELY_MISREADING** - Common ways this concept could be misunderstood
   - What confusions might arise? What adjacent concepts might it be conflated with?

5. **GRAY_ZONE** - Boundary cases where application is uncertain
   - Where are the edges of the concept's applicability?

6. **UNFILLED_SLOT** - Placeholder structures awaiting elaboration
   - What conceptual slots haven't been filled in yet?

7. **UNCONFRONTED_CHALLENGE** - Objections/problems not yet addressed
   - What obvious objections could be raised?

DO NOT duplicate items already identified. Generate truly new ones.

Return as JSON:
{{
    "generated_blind_spots": [
        {{
            "category": "ambiguity|presupposition|paradigm_dependency|likely_misreading|gray_zone|unfilled_slot|unconfronted_challenge",
            "description": "Description of this epistemic gap - what the user hasn't yet made explicit",
            "what_unclear": "The specific aspect that needs clarification",
            "what_would_help": "What kind of clarification would help surface the user's positioning",
            "productive_potential": "Why exploring this would help the user articulate their priors"
        }}
    ],
    "generation_note": "Brief note about what epistemic gaps were identified"
}}

IMPORTANT: These are EPISTEMIC (about the user's grasp/positioning) not ONTOLOGICAL (about the object being indeterminate).
The goal is to help users articulate their priors, confront structural limits, and grasp conditions of possibility."""

# Legacy alias for backward compatibility
GENERATE_TENSIONS_PROMPT = GENERATE_BLIND_SPOTS_PROMPT


REGENERATE_BLIND_SPOT_PROMPT = """You are an expert in conceptual analysis helping refine an epistemic blind spot based on user feedback.

## Concept Name: {concept_name}

## User's Notes:
{notes}

## Current Blind Spot to Regenerate:
{current_tension}

## User's Feedback for Regeneration:
{feedback}

## Other Blind Spots in This Concept (for context, avoid duplication):
{other_tensions}

Your task is to regenerate this epistemic blind spot based on the user's feedback. The user wants a NEW formulation that incorporates their feedback - not just the original with a comment appended.

## The 7 Epistemic Categories:
1. AMBIGUITY - Terms with multiple valid readings
2. PRESUPPOSITION - What's treated as "given" without justification
3. PARADIGM_DEPENDENCY - Where different epistemes produce different conclusions
4. LIKELY_MISREADING - Common ways this could be misunderstood
5. GRAY_ZONE - Boundary cases where application is uncertain
6. UNFILLED_SLOT - Placeholder structures awaiting elaboration
7. UNCONFRONTED_CHALLENGE - Objections not yet addressed

Consider:
1. What aspect does the user want emphasized or changed?
2. Is this correctly categorized? Should it be a different epistemic category?
3. Is it at the right level of abstraction?
4. Does it genuinely help surface the user's epistemic positioning?

Return as JSON:
{{
    "regenerated_blind_spot": {{
        "category": "ambiguity|presupposition|paradigm_dependency|likely_misreading|gray_zone|unfilled_slot|unconfronted_challenge",
        "description": "Regenerated description based on feedback",
        "what_unclear": "The specific aspect that needs clarification",
        "what_would_help": "What kind of clarification would surface the user's positioning",
        "productive_potential": "Why exploring this helps the user articulate their priors"
    }},
    "regeneration_note": "Brief note about what was changed based on feedback"
}}

Generate an item that reflects the user's feedback while maintaining theoretical rigor.
Remember: These are EPISTEMIC (about the user's positioning) not ONTOLOGICAL (about the object itself)."""

# Legacy alias for backward compatibility
REGENERATE_TENSION_PROMPT = REGENERATE_BLIND_SPOT_PROMPT


# =============================================================================
# DOCUMENT ANALYSIS - Full 9-Dimensional Extraction (Uses Sonnet 4.5 1M)
# =============================================================================

DOCUMENT_ANALYSIS_PROMPT = """You are Claude analyzing materials about a novel concept called "{concept_name}".

Your task is to extract EVERYTHING we can populate in our 9-dimensional concept schema.
Use your extensive knowledge of intellectual history, philosophy, and social sciences to INFER beyond what's explicit.

## Document Content:
{document_content}

## Existing Context (if any):
{existing_context}

## EXTRACTION TARGETS - ALL 9 PHILOSOPHICAL DIMENSIONS:

### 1. QUINEAN (Inferential Web)
- What can be inferred FROM this concept? ("If X, then...")
- What can be inferred TO this concept? ("If Y, then X")
- What would CONTRADICT this concept?
- How CENTRAL is it to the author's framework? (core/intermediate/peripheral)

### 2. SELLARSIAN (Givenness Analysis)
- Is this concept treated as "obvious" or self-evident?
- What phrases suggest givenness? ("obviously", "naturally", "of course")
- What SHOULD this concept be inferred from (but isn't justified)?
- What ASSUMPTIONS are embedded without argument?

### 3. BRANDOMIAN (Commitments & Entitlements)
- What claims does using this concept COMMIT you to?
- What claims is the concept-user ENTITLED to make?
- What is INCOMPATIBLE with this concept?
- Are any commitments violated in the materials?

### 4. DELEUZIAN (Problems, Plane & Becomings)
- What PROBLEM or tension does this concept address?
- What are the POLES of this tension?
- What transformations (becomings) does the concept ENABLE?
- What transformations does it BLOCK or foreclose?
- What UNQUESTIONED ASSUMPTIONS form the "plane" (background conditions)?
- What becomes THINKABLE with this concept?
- What becomes UNTHINKABLE?

### 5. BACHELARDIAN (Rupture & Obstacles)
- What existing framework is this concept BREAKING FROM?
- WHY is the old framework inadequate?
- Could this concept itself become an OBSTACLE to future understanding?
- What questions might become UNASKABLE if we adopt this concept?
- What would TRIGGER abandonment of this concept?

### 6. CANGUILHEM (Life History & Normative Stakes)
- How has this concept (or precursors) EVOLVED historically?
- What PROBLEMS drove changes in its meaning?
- What VALUES are embedded in this concept?
- Whose INTERESTS does this concept serve?
- What/who gets marked as "abnormal" or EXCLUDED?

### 7. DAVIDSON (Reasoning Style)
- What REASONING STYLE does this concept require?
- What becomes VISIBLE with this lens?
- What becomes INVISIBLE or systematically hidden?
- What kinds of EVIDENCE does this concept privilege?
- What INFERENCE PATTERNS are characteristic?

### 8. BLUMENBERG (Metaphorology)
- What ROOT METAPHOR underlies this concept?
- What DOMAIN does the metaphor come from?
- What does the metaphor ENABLE thinking about?
- What does it OBSCURE or hide?
- Is there conceptual WORK being done to transform the concept?

### 9. CAREY (Bootstrapping Hierarchy)
- What SIMPLER CONCEPTS is this built from?
- How do they COMBINE? (aggregation, interaction, emergence)
- What EMERGES that wasn't in the parts?
- How TRANSPARENT is the construction?

Return as JSON with confidence levels (high/medium/low/speculative):
{{
  "document_summary": "Brief summary of the document's relevance to the concept",
  "key_excerpts": ["Relevant quotes from the document"],

  "quinean": {{
    "forward_inferences": [{{"statement": "If {concept_name} then...", "confidence": "medium"}}],
    "backward_inferences": [{{"statement": "If X then {concept_name}...", "confidence": "medium"}}],
    "contradictions": [{{"statement": "...", "confidence": "low"}}],
    "centrality": "core|intermediate|peripheral",
    "web_coherence_note": "How this fits the broader conceptual web"
  }},

  "sellarsian": {{
    "treated_as_given": true,
    "givenness_markers": ["obviously", "naturally"],
    "should_be_inferred_from": "What justification is missing",
    "hidden_assumptions": ["Assumption 1", "Assumption 2"],
    "what_givenness_enables": "What treating as given allows",
    "what_givenness_blocks": "What questions become unaskable"
  }},

  "brandomian": {{
    "commitments": [{{"claim": "...", "type": "ontological|causal|normative", "confidence": "high"}}],
    "entitlements": [{{"claim": "...", "confidence": "medium"}}],
    "incompatibilities": [{{"claim": "...", "confidence": "medium"}}],
    "violations_found": null
  }},

  "deleuzian": {{
    "problem_addressed": "The core tension/problem",
    "tension_poles": ["Pole A", "Pole B"],
    "becomings_enabled": ["Transformation 1"],
    "becomings_blocked": ["Foreclosed transformation"],
    "plane_assumptions": [{{"assumption": "...", "makes_possible": ["..."], "makes_impossible": ["..."]}}],
    "creative_responses": ["How concept navigates the problem"]
  }},

  "bachelardian": {{
    "breaking_from": {{"framework": "...", "why_inadequate": "..."}},
    "break_rationale": "Detailed reason for rupture",
    "obstacle_potential": {{
      "is_obstacle_risk": true,
      "what_it_might_block": ["Future understanding 1"],
      "why_persists": "Ideological function",
      "rupture_trigger": "What would force abandonment"
    }}
  }},

  "canguilhem": {{
    "evolution_stages": [{{"period": "...", "transformation": "...", "problem_driving": "..."}}],
    "health_status": "healthy|strained|dying|being_born",
    "values_embedded": ["Value 1"],
    "whose_interests": "Whose interests served",
    "what_excluded": "What marked as abnormal"
  }},

  "davidson": {{
    "reasoning_style": "quantitative|historical|structural|phenomenological|dialectical",
    "makes_visible": ["What becomes visible"],
    "makes_invisible": ["What's systematically hidden"],
    "evidence_privileged": ["Type of evidence privileged"],
    "inference_patterns": ["Characteristic reasoning moves"]
  }},

  "blumenberg": {{
    "root_metaphor": "The underlying metaphor",
    "source_domain": "Where metaphor comes from",
    "metaphor_enables": ["What it helps think"],
    "metaphor_hides": ["What it obscures"],
    "resists_conceptualization": false,
    "conceptual_work": "Any transformation work being done"
  }},

  "carey": {{
    "built_from": ["Component concept 1", "Component concept 2"],
    "combination_type": "aggregation|interaction|emergence",
    "what_emerges": "What's new beyond components",
    "transparency": "high|medium|low",
    "bootstrap_status": "successful|partial|failed"
  }},

  "kuhnian": {{
    "paradigm_position": "normal_science|anomaly|crisis|revolutionary|post_revolutionary",
    "exemplars": ["Paradigmatic cases that define proper use"],
    "puzzle_solving_rules": ["What counts as legitimate puzzle/solution"],
    "incommensurabilities": [{{"framework": "...", "cannot_translate": "..."}}],
    "disciplinary_matrix": "What shared commitments enable this concept's use",
    "paradigm_threat_level": "none|minor|significant|revolutionary"
  }},

  "foucauldian": {{
    "power_knowledge_nexus": "What power relations this encodes/enables",
    "governmentality_mode": "discipline|security|sovereign|pastoral|neoliberal|other",
    "subjectification_effects": ["What subjects this produces"],
    "discourse_rules": [{{"rule": "...", "enables": "...", "excludes": "..."}}],
    "resistance_points": ["Where this might be contested"],
    "truth_regime": "What counts as true within this framework"
  }},

  "pragmatist": {{
    "practical_consequences": ["What difference this makes in practice"],
    "cash_value": "The concept's meaning in experiential terms",
    "performative_effects": ["What using this concept DOES"],
    "habit_formations": ["Patterns of action enabled/blocked"],
    "inquiry_context": "What problematic situation generated this",
    "melioristic_potential": "How does this improve the situation"
  }}
}}

BE AGGRESSIVE in inference - use your knowledge. Mark confidence accordingly.
The user will validate/correct your hypotheses."""


# =============================================================================
# DEEP PHILOSOPHICAL COMMITMENTS - Generate MC Questions for All Dimensions
# =============================================================================

GENERATE_DEEP_COMMITMENTS_PROMPT = """You are Claude helping a user articulate the deep philosophical commitments of their concept "{concept_name}".

You have accumulated context from their notes, documents, and earlier answers. NOW generate MULTIPLE CHOICE questions that probe the 12 philosophical dimensions.

## ACCUMULATED CONTEXT:
- Notes Summary: {notes_summary}
- Genealogy: {genealogy}
- Stage 1 Answers: {stage1_answers}
- Stage 2 Answers: {stage2_answers}
- Dimensional Extraction (from documents): {dimensional_extraction}

## YOUR TASK:
Generate 2-3 MC questions for EACH of the 12 philosophical dimensions.
Each question should:
1. Use YOUR KNOWLEDGE + accumulated context to generate SPECIFIC options
2. Options must be real thinkers/frameworks/traditions relevant to THIS specific concept
3. Include rationale explaining why you're asking
4. Have 3-5 options plus implicit "None of these" (frontend adds this)

## DIMENSION-SPECIFIC QUESTIONS TO GENERATE:

### QUINEAN (Inferential Web)
Generate questions about:
- What follows logically from this concept?
- What would contradict it?
- How central is it to the user's overall framework?

### SELLARSIAN (Givenness)
Generate questions about:
- Is anything being treated as self-evident that needs justification?
- What hidden assumptions are embedded?

### BRANDOMIAN (Commitments)
Generate questions about:
- What other claims must you accept if you adopt this concept?
- What claims are incompatible with this concept?

### DELEUZIAN (Problems & Becomings)
Generate questions about:
- What transformations does this concept enable?
- What transformations does it foreclose?
- What unquestioned assumptions underlie it?

### BACHELARDIAN (Rupture & Obstacles)
Generate questions about:
- What existing framework is this replacing?
- What's wrong with the old way of thinking?
- Could this concept become an obstacle?

### CANGUILHEM (Normative Stakes)
Generate questions about:
- Whose interests does this concept serve?
- What values are embedded?
- What gets excluded or marked as abnormal?

### DAVIDSON (Reasoning Style)
Generate questions about:
- What kind of reasoning does this concept require?
- What does it make visible?
- What might it obscure?

### BLUMENBERG (Metaphorology)
Generate questions about:
- What's the root metaphor?
- What does the metaphor reveal vs hide?

### CAREY (Bootstrapping)
Generate questions about:
- What simpler concepts is this built from?
- What emerges from the combination?

### KUHNIAN (Paradigm Structure)
Generate questions about:
- What paradigm does this concept belong to?
- What would count as an anomaly for this concept?
- What problems does this paradigm make solvable vs invisible?
- Is this concept normal science or revolutionary?
- INCOMMENSURABILITY: How does this concept relate to rival paradigms? Can it be translated into their terms or is there fundamental incommensurability?
- CRISIS INDICATORS: What would trigger a paradigm crisis for this concept? What accumulation of anomalies would force abandonment?
- DISCIPLINARY MATRIX: What shared commitments, values, and exemplars do practitioners of this concept share?

### PRAGMATIST (Performative Consequences)
Generate questions about:
- What does USING this concept enable you to DO?
- What practical difference does adopting it make?
- What actions or interventions become possible/impossible?
- How does it change what you can say or propose?
- HABITS OF ACTION: What habits of thought and practice does using this concept cultivate? What dispositions does it form?
- VOCABULARY GAMES (Rorty): What new things can you SAY with this concept that you couldn't say before? What conversations does it open?
- INQUIRY PROCESS (Dewey): How does this concept structure problem-solving? What does it make into a "problem" and what does it treat as "solved"?

### FOUCAULDIAN (Power-Knowledge Relations)
Generate questions about:
- What power relations does this concept naturalize or make invisible?
- What does it make governable or manageable?
- Whose authority does it legitimize?
- What populations or phenomena does it bring under scrutiny?
- DISCURSIVE FORMATIONS: What statements become possible/impossible within the discourse this concept enables? What are its rules of formation?
- REGIMES OF TRUTH: What counts as TRUE within the framework this concept establishes? Who gets to speak with authority?
- ARCHAEOLOGY: How did this concept emerge? What discursive conditions made it possible? What did it replace or displace?

Return as JSON:
{{
  "deep_commitment_questions": [
    {{
      "id": "quinean_inferences",
      "dimension": "quinean",
      "question": "If {concept_name} is valid, which of these claims would also follow?",
      "options": [
        {{"value": "inference_1", "label": "Specific claim A", "description": "Why this follows"}},
        {{"value": "inference_2", "label": "Specific claim B", "description": "Why this follows"}},
        {{"value": "inference_3", "label": "Specific claim C", "description": "Why this follows"}}
      ],
      "rationale": "Understanding what follows helps clarify the concept's implications",
      "allow_multiple": false
    }},
    {{
      "id": "quinean_contradictions",
      "dimension": "quinean",
      "question": "What would CONTRADICT {concept_name}?",
      "options": [
        {{"value": "contra_1", "label": "Contradiction A", "description": "Why this contradicts"}},
        {{"value": "contra_2", "label": "Contradiction B", "description": "Why this contradicts"}}
      ],
      "rationale": "Knowing what contradicts helps define boundaries",
      "allow_multiple": true
    }},
    {{
      "id": "brandomian_commitments",
      "dimension": "brandomian",
      "question": "If you adopt {concept_name}, you must ALSO accept:",
      "options": [
        {{"value": "commit_1", "label": "Commitment A", "description": "Why this is required"}},
        {{"value": "commit_2", "label": "Commitment B", "description": "Why this is required"}}
      ],
      "rationale": "Concepts carry hidden commitments",
      "allow_multiple": true
    }},
    {{
      "id": "deleuzian_enables",
      "dimension": "deleuzian",
      "question": "What transformation does {concept_name} ENABLE that was previously blocked?",
      "options": [
        {{"value": "becoming_1", "label": "Transformation A", "description": "How this becomes possible"}},
        {{"value": "becoming_2", "label": "Transformation B", "description": "How this becomes possible"}}
      ],
      "rationale": "Concepts are tools for change",
      "allow_multiple": true
    }},
    {{
      "id": "deleuzian_blocks",
      "dimension": "deleuzian",
      "question": "What might {concept_name} FORECLOSE or make harder to think?",
      "options": [
        {{"value": "block_1", "label": "Foreclosure A", "description": "Why this becomes unthinkable"}},
        {{"value": "block_2", "label": "Foreclosure B", "description": "Why this becomes unthinkable"}}
      ],
      "rationale": "Every lens has blind spots",
      "allow_multiple": true
    }},
    {{
      "id": "bachelardian_rupture",
      "dimension": "bachelardian",
      "question": "What existing framework is {concept_name} BREAKING FROM?",
      "options": [
        {{"value": "rupture_1", "label": "Framework A", "description": "What's wrong with it"}},
        {{"value": "rupture_2", "label": "Framework B", "description": "What's wrong with it"}}
      ],
      "rationale": "New concepts replace old ways of thinking",
      "allow_multiple": false
    }},
    {{
      "id": "canguilhem_interests",
      "dimension": "canguilhem",
      "question": "Whose INTERESTS does {concept_name} primarily serve?",
      "options": [
        {{"value": "interest_1", "label": "Stakeholder A", "description": "How they benefit"}},
        {{"value": "interest_2", "label": "Stakeholder B", "description": "How they benefit"}},
        {{"value": "neutral", "label": "Genuinely neutral", "description": "Serves no particular interest"}}
      ],
      "rationale": "Concepts are never politically innocent",
      "allow_multiple": true
    }},
    {{
      "id": "davidson_visibility",
      "dimension": "davidson",
      "question": "What does {concept_name} make VISIBLE that was hidden before?",
      "options": [
        {{"value": "visible_1", "label": "Visibility A", "description": "What becomes apparent"}},
        {{"value": "visible_2", "label": "Visibility B", "description": "What becomes apparent"}}
      ],
      "rationale": "Every concept is a lens",
      "allow_multiple": true
    }},
    {{
      "id": "davidson_invisibility",
      "dimension": "davidson",
      "question": "What might {concept_name} make INVISIBLE or harder to see?",
      "options": [
        {{"value": "invisible_1", "label": "Hidden A", "description": "Why it's obscured"}},
        {{"value": "invisible_2", "label": "Hidden B", "description": "Why it's obscured"}}
      ],
      "rationale": "Lenses have blind spots",
      "allow_multiple": true
    }},
    {{
      "id": "blumenberg_metaphor",
      "dimension": "blumenberg",
      "question": "What ROOT METAPHOR underlies {concept_name}?",
      "options": [
        {{"value": "metaphor_1", "label": "Metaphor A", "description": "From domain X"}},
        {{"value": "metaphor_2", "label": "Metaphor B", "description": "From domain Y"}}
      ],
      "rationale": "Concepts carry hidden metaphorical baggage",
      "allow_multiple": false
    }},
    {{
      "id": "carey_components",
      "dimension": "carey",
      "question": "What simpler concepts COMBINE to make {concept_name}?",
      "options": [
        {{"value": "component_1", "label": "Component A + B", "description": "How they combine"}},
        {{"value": "component_2", "label": "Component C + D", "description": "How they combine"}}
      ],
      "rationale": "Complex concepts are bootstrapped from simpler ones",
      "allow_multiple": false
    }},
    {{
      "id": "kuhnian_paradigm",
      "dimension": "kuhnian",
      "question": "What PARADIGM does {concept_name} belong to?",
      "options": [
        {{"value": "paradigm_1", "label": "Paradigm A", "description": "What this paradigm assumes"}},
        {{"value": "paradigm_2", "label": "Paradigm B", "description": "What this paradigm assumes"}}
      ],
      "rationale": "Concepts operate within paradigmatic frameworks",
      "allow_multiple": false
    }},
    {{
      "id": "kuhnian_anomalies",
      "dimension": "kuhnian",
      "question": "What would count as an ANOMALY for {concept_name}?",
      "options": [
        {{"value": "anomaly_1", "label": "Anomaly A", "description": "Why this would challenge the concept"}},
        {{"value": "anomaly_2", "label": "Anomaly B", "description": "Why this would challenge the concept"}}
      ],
      "rationale": "Understanding anomalies reveals paradigm boundaries",
      "allow_multiple": true
    }},
    {{
      "id": "pragmatist_enables",
      "dimension": "pragmatist",
      "question": "What does USING {concept_name} enable you to DO?",
      "options": [
        {{"value": "action_1", "label": "Action/Intervention A", "description": "How this becomes possible"}},
        {{"value": "action_2", "label": "Action/Intervention B", "description": "How this becomes possible"}}
      ],
      "rationale": "Concepts are tools for action",
      "allow_multiple": true
    }},
    {{
      "id": "pragmatist_practical",
      "dimension": "pragmatist",
      "question": "What PRACTICAL DIFFERENCE does adopting {concept_name} make?",
      "options": [
        {{"value": "difference_1", "label": "Difference A", "description": "What changes"}},
        {{"value": "difference_2", "label": "Difference B", "description": "What changes"}}
      ],
      "rationale": "The meaning of a concept lies in its practical effects",
      "allow_multiple": true
    }},
    {{
      "id": "foucauldian_power",
      "dimension": "foucauldian",
      "question": "What POWER RELATIONS does {concept_name} naturalize or make invisible?",
      "options": [
        {{"value": "power_1", "label": "Power relation A", "description": "How it's naturalized"}},
        {{"value": "power_2", "label": "Power relation B", "description": "How it's naturalized"}}
      ],
      "rationale": "Concepts embed and legitimize power relations",
      "allow_multiple": true
    }},
    {{
      "id": "foucauldian_governable",
      "dimension": "foucauldian",
      "question": "What does {concept_name} make GOVERNABLE or manageable?",
      "options": [
        {{"value": "govern_1", "label": "Population/Phenomenon A", "description": "How it becomes manageable"}},
        {{"value": "govern_2", "label": "Population/Phenomenon B", "description": "How it becomes manageable"}}
      ],
      "rationale": "Concepts are tools of governance and management",
      "allow_multiple": true
    }}
  ],
  "generation_note": "Brief note about what dimensions had strongest signal from context"
}}

CRITICAL: Generate SPECIFIC options based on THIS concept and accumulated context.
Do NOT use generic placeholders. Each option should be a real, specific claim/framework/thinker.
The goal: USER VALIDATES your hypotheses, not generates from scratch."""


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
# CURATOR-SHARPENER PROMPTS
# =============================================================================

EPISTEMIC_CATEGORIES_REGISTRY = """
## The 7 Epistemic Categories

These categories surface gaps in the USER'S epistemic positioning (not the object itself).

### 1. AMBIGUITY
Terms/phrases with multiple valid readings that the user hasn't explicitly resolved.
- What to probe: "Do you mean X or Y when you say Z?"
- Derived from: Brandomian perspectival content, Blumenberg metaphor theory
- Example: "Sovereignty" could mean territorial, decisionist, or popular - which?

### 2. PRESUPPOSITION
What's being treated as "given" without justification.
- What to probe: "You seem to assume X - what's your basis for this?"
- Derived from: Sellarsian givenness critique, Deleuzian plane assumptions
- Example: "You assume digital platforms tend toward monopoly - this requires argument"

### 3. PARADIGM_DEPENDENCY
Where different intellectual traditions would produce different conclusions.
- What to probe: "A [tradition] reading would see X, but you're implying Y - which frame are you using?"
- Derived from: Hacking reasoning styles, Bachelardian regional rationality
- Example: "Marxist vs Foucauldian reading of power dynamics here"

### 4. LIKELY_MISREADING
Common ways this concept could be misunderstood by others.
- What to probe: "Readers might confuse this with X - how do you distinguish?"
- Derived from: Brandomian de dicto/de re, Carey incommensurability
- Example: "This might be confused with Polanyi's embedded economy"

### 5. GRAY_ZONE
Boundary cases where application is uncertain.
- What to probe: "Does this apply to [edge case]? Where does it stop?"
- Derived from: Quinean web tensions, Canguilhem milieu boundaries
- Example: "Does your concept apply to pre-digital platform capitalism?"

### 6. UNFILLED_SLOT
Placeholder structures awaiting elaboration.
- What to probe: "You mention X modes but only explain two - what's the third?"
- Derived from: Carey placeholder structures, Quinean missing inferences
- Example: "You identify causes but not mechanisms"

### 7. UNCONFRONTED_CHALLENGE
Objections or problems the user hasn't yet addressed.
- What to probe: "What would [critic] say to this? How would you respond?"
- Derived from: Bachelardian epistemological obstacles
- Example: "Critics would say this reduces to mere economics - your response?"
"""

CURATOR_PROMPT = """You are an epistemic curator analyzing concept notes to identify blind spots and allocate questioning slots.

{categories_registry}

## User's Concept: {concept_name}

## User's Notes:
{notes}

{notes_understanding_section}

## Your Task

1. **Analyze the notes** against each of the 7 epistemic categories
2. **Identify specific blind spots** - concrete instances where user positioning is unclear
3. **Determine category weights** - which categories are most important for THIS concept
4. **Allocate question slots** (maximum 16 total) based on weights
5. **Generate initial questions** for each allocated slot
6. **Design an INTERLEAVED sequence** - distribute categories across the session

## Allocation Guidelines

- Total slots: 8-16 depending on complexity
- Minimum 1 slot per relevant category
- Maximum 4 slots per category
- Categories with more identified blind spots get more slots
- Weights should sum to 1.0

## Interleaving Rule (CRITICAL)

Questions must be DISTRIBUTED, not clustered by category.

If allocating 3 ambiguity slots and 2 presupposition slots:
- BAD: [amb, amb, amb, pre, pre]
- GOOD: [amb, pre, amb, pre, amb]

This prevents user fatigue and allows reflection between similar questions.

## Question Generation Guidelines

For each slot, generate a question that:
- Is specific to the user's concept (not generic)
- Can be answered in 2-3 sentences
- Focuses on ARTICULATION, not RESOLUTION
- Helps the user make their positioning explicit
- References specific content from their notes

DO NOT ask questions whose answers are obvious from the notes.

## Output Format

Return valid JSON:
{{
    "total_slots": 12,
    "category_weights": {{
        "ambiguity": 0.25,
        "presupposition": 0.2,
        "paradigm_dependency": 0.15,
        "likely_misreading": 0.1,
        "gray_zone": 0.15,
        "unfilled_slot": 0.1,
        "unconfronted_challenge": 0.05
    }},
    "emphasis_rationale": "Why this allocation - e.g., 'The concept heavily relies on contested terms (ambiguity) and makes strong assumptions about market dynamics (presupposition)'",
    "identified_blind_spots": [
        {{
            "category": "ambiguity",
            "description": "The term 'sovereignty' appears 12 times but could mean different things",
            "what_unclear": "Whether sovereignty here is territorial, decisionist, or popular",
            "what_would_help": "Explicit statement of which sovereignty tradition is being drawn from"
        }}
    ],
    "slots": [
        {{
            "slot_id": "slot_01",
            "category": "ambiguity",
            "depth": 1,
            "question": "When you write about 'technological sovereignty', do you mean control over infrastructure (territorial), authority to make technology decisions (decisionist), or collective technological self-determination (popular)?",
            "status": "pending",
            "generated_by": "curator",
            "blind_spot_ref": "The term 'sovereignty' appears 12 times..."
        }},
        {{
            "slot_id": "slot_02",
            "category": "presupposition",
            "depth": 1,
            "question": "You seem to assume that states can meaningfully regulate transnational tech platforms. What's the basis for this assumption given platform mobility?",
            "status": "pending",
            "generated_by": "curator",
            "blind_spot_ref": "Assumes state regulatory capacity..."
        }}
    ],
    "slot_sequence": ["ambiguity", "presupposition", "paradigm_dependency", "ambiguity", "gray_zone", "presupposition", "unfilled_slot", "ambiguity", "likely_misreading", "gray_zone", "unconfronted_challenge", "presupposition"]
}}

Generate thoughtful, specific questions that will genuinely help the user articulate their epistemic positioning."""

SHARPENER_PROMPT = """You are an epistemic sharpener generating deeper follow-up questions.

{categories_registry}

## Context

**Concept:** {concept_name}

**Original Question (depth {depth}):**
{original_question}

**User's Answer:**
{user_answer}

**Category:** {category}

**Original Notes (for grounding):**
{notes_context}

**Other Answers So Far:**
{context_answers}

## Your Task

Generate ONE follow-up question that:

1. **Builds directly on their specific answer** - reference their actual words
2. **Probes ONE level deeper** into this epistemic gap
3. **Helps them articulate what's still implicit** in their response
4. **Does NOT repeat** what's already been explored
5. **Remains within the same category** ({category})

## Depth Guidelines

- Depth 1 (initial): Surface-level clarification
- Depth 2 (follow-up): Probing assumptions behind their answer
- Depth 3 (deep-dive): Connecting to broader commitments or implications

You are generating a depth {next_depth} question.

## Question Style

- Be specific to THEIR answer (quote them if relevant)
- 1-2 sentences maximum
- Focus on ARTICULATION not RESOLUTION
- Answerable in 2-3 sentences

## Output Format

Return valid JSON:
{{
    "question": "Your follow-up question here",
    "rationale": "Why this probes deeper - what it will reveal",
    "connects_to": "What aspect of their answer this builds on"
}}

Generate a question that genuinely advances their epistemic self-understanding."""


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
            # Support new (epistemic_blind_spots), intermediate (gaps_tensions_questions), and old (potential_tensions) field names
            epistemic_blind_spots = analysis_data.get("epistemic_blind_spots",
                analysis_data.get("gaps_tensions_questions",
                    analysis_data.get("potential_tensions", [])))
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
                    'epistemic_blind_spots': epistemic_blind_spots,
                    'gaps_tensions_questions': epistemic_blind_spots,  # Legacy alias for frontend compatibility
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

            # Parse response - support both new and old field names
            blind_spots_data = parse_wizard_response(response_text)
            generated_blind_spots = blind_spots_data.get("generated_blind_spots",
                blind_spots_data.get("generated_tensions", []))
            generation_note = blind_spots_data.get("generation_note", "")

            complete_data = {
                'type': 'complete',
                'data': {
                    'generated_blind_spots': generated_blind_spots,
                    'generated_tensions': generated_blind_spots,  # Legacy alias for frontend compatibility
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

            # Parse response - support both new and old field names
            blind_spot_data = parse_wizard_response(response_text)
            regenerated_blind_spot = blind_spot_data.get("regenerated_blind_spot",
                blind_spot_data.get("regenerated_tension", {}))
            regeneration_note = blind_spot_data.get("regeneration_note", "")

            complete_data = {
                'type': 'complete',
                'data': {
                    'regenerated_blind_spot': regenerated_blind_spot,
                    'regenerated_tension': regenerated_blind_spot,  # Legacy alias for frontend compatibility
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
    """Save the completed concept to the database.

    This endpoint:
    1. Creates the basic Concept record (legacy models.py)
    2. Bridges wizard outputs to 8D schema (AnalyzedConcept, ConceptAnalysis, AnalysisItem)
    """
    from .models import Concept, ConceptStatus
    from .wizard_to_schema_bridge import finalize_wizard_concept

    concept_data = request.concept_data

    # Create the main concept (legacy Concept model)
    concept = Concept(
        term=concept_data.get("name", "Untitled Concept"),
        definition=concept_data.get("definition", ""),
        category=concept_data.get("category"),
        status=ConceptStatus.DRAFT,
        source_id=request.source_id,
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

    # Bridge to 8D schema: Create AnalyzedConcept + ConceptAnalysis + AnalysisItem records
    # This populates the structured analysis schema with wizard outputs
    bridge_result = None
    try:
        bridge_result = await finalize_wizard_concept(
            db=db,
            concept_name=concept_data.get("name", "Untitled Concept"),
            wizard_output=concept_data,
            wizard_session_id=concept.id  # Use concept ID as session reference
        )
        logger.info(f"Bridged wizard to 8D schema: {bridge_result}")
    except Exception as e:
        logger.error(f"Error bridging wizard to 8D schema: {e}", exc_info=True)
        # Don't fail the save - the basic concept is still saved

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
        },
        "schema_bridge": bridge_result  # Include bridge result in response
    }


# =============================================================================
# STAGED WIZARD ENDPOINTS
# =============================================================================

@router.post("/stage1")
async def get_stage1_questions(request: StartWizardRequest):
    """
    Pre-process user notes with Claude - initial analysis only.
    Hypothesis/genealogy/differentiation cards are generated AFTER blind spots questioning.
    """
    async def stream_notes_analysis():
        try:
            # Phase 1: Analyzing notes (initial analysis only - no cards yet)
            yield f"data: {json.dumps({'type': 'phase', 'phase': 'analyzing_notes'})}\n\n"

            # Use INITIAL_ANALYSIS_PROMPT - generates blind spots but NOT hypothesis cards
            prompt = INITIAL_ANALYSIS_PROMPT.format(
                concept_name=request.concept_name,
                notes=request.notes
            )

            # Call Claude with extended thinking to analyze notes
            client = get_claude_client()
            notes_analysis = {}

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
            # Support new (epistemic_blind_spots), intermediate (gaps_tensions_questions), and old (potential_tensions) field names
            epistemic_blind_spots = analysis_data.get("epistemic_blind_spots",
                analysis_data.get("gaps_tensions_questions",
                    analysis_data.get("potential_tensions", [])))
            dimensional_signals = analysis_data.get("dimensional_signals", {})

            # Return analysis with blind spots - cards will be generated AFTER blind spots questioning
            complete_data = {
                'type': 'complete',
                'data': {
                    'status': 'analysis_ready',  # New flow: analysis ready, cards come later
                    'concept_name': request.concept_name,
                    'stage': 1,
                    'stage_title': 'Initial Analysis Complete',
                    'stage_description': "We've analyzed your notes and identified epistemic blind spots. Next: explore these blind spots to inform hypothesis generation.",
                    'notes_analysis': notes_analysis,
                    'epistemic_blind_spots': epistemic_blind_spots,
                    'gaps_tensions_questions': epistemic_blind_spots,  # Legacy alias for frontend compatibility
                    'dimensional_signals': dimensional_signals,

                    # Cards are NOT generated here anymore - they come after blind spots
                    'hypothesis_cards': [],
                    'genealogy_cards': [],
                    'differentiation_cards': []
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

    # Format already-identified tensions from notes preprocessing
    already_identified = "None - this is the first time identifying tensions."
    if request.approved_tensions_from_notes and len(request.approved_tensions_from_notes) > 0:
        already_identified = "\n".join([
            f"- {tension}" for tension in request.approved_tensions_from_notes
        ])

    # First LLM call: Generate interim analysis
    interim_prompt = INTERIM_ANALYSIS_PROMPT.format(
        concept_name=request.concept_name,
        stage1_answers=stage1_text,
        marked_dialectics=dialectics_text,
        already_identified_tensions=already_identified
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

            # Format approved gaps/tensions/questions for Stage 2 generation
            approved_items_text = "None confirmed yet."
            if request.approved_tensions_from_notes and len(request.approved_tensions_from_notes) > 0:
                approved_items_text = "\n".join([
                    f"- {item}" for item in request.approved_tensions_from_notes
                ])

            stage2_prompt = STAGE2_GENERATION_PROMPT.format(
                concept_name=request.concept_name,
                stage1_summary=stage1_text,
                interim_analysis=json.dumps(interim_analysis, indent=2),
                adjacent_concepts=adjacent_concepts,
                approved_items=approved_items_text
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

    # Format deep commitment answers (9-dimensional probing)
    deep_commitments_str = ""
    if request.deep_commitments:
        sections = []
        for question_id, answer_data in request.deep_commitments.items():
            if isinstance(answer_data, dict):
                dimension = answer_data.get('dimension', 'unknown')
                selected = answer_data.get('selected_option', {})
                comment = answer_data.get('comment', '')
                q_text = answer_data.get('question_text', question_id)

                section = f"### {dimension.upper()} Dimension\n"
                section += f"Q: {q_text}\n"
                if selected:
                    section += f"A: {selected.get('label', str(selected))}\n"
                    if selected.get('description'):
                        section += f"   (Meaning: {selected['description']})\n"
                if comment:
                    section += f"   User Comment: {comment}\n"
                sections.append(section)
        deep_commitments_str = "\n".join(sections)

    # Format dimensional extraction from document analysis
    dimensional_extraction_str = ""
    if request.dimensional_extraction:
        dim_sections = []
        for dim_name, dim_data in request.dimensional_extraction.items():
            if dim_data and isinstance(dim_data, dict):
                dim_sections.append(f"### {dim_name.upper()}")
                for key, value in dim_data.items():
                    if value:
                        dim_sections.append(f"  {key}: {value}")
        dimensional_extraction_str = "\n".join(dim_sections)

    async def stream_final_synthesis():
        try:
            client = get_claude_client()

            yield f"data: {json.dumps({'type': 'phase', 'phase': 'final_synthesis'})}\n\n"

            synthesis_prompt = f"""Synthesize all the user's answers into a comprehensive 9-DIMENSIONAL concept definition for "{request.concept_name}".

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

## Deep Philosophical Commitments (9-Dimensional Probing):
{deep_commitments_str or "(No deep commitment answers provided)"}

## Dimensional Extraction from Documents/Analysis:
{dimensional_extraction_str or "(No dimensional extraction available)"}

Create a complete 9-DIMENSIONAL concept definition following the philosophical frameworks:
1. QUINEAN - Web of belief, inferential connections, centrality
2. SELLARSIAN - Givenness analysis, what's treated as foundational
3. BRANDOMIAN - Commitments, entitlements, incompatibilities
4. DELEUZIAN - Problems, tensions, becomings, plane assumptions
5. BACHELARDIAN - Obstacles, ruptures, what blocks understanding
6. CANGUILHEM - Life history, evolution, health status, normative dimensions
7. DAVIDSON - Reasoning styles, what becomes visible/invisible
8. BLUMENBERG - Root metaphors, conceptual work being done
9. CAREY - Bootstrapping hierarchy, what primitives it's built from

IMPORTANT:
- USE the user-validated cases, markers, and tensions provided above
- INTEGRATE the deep philosophical commitments into the appropriate dimension sections
- POPULATE ALL 9 dimensions based on available data

Output a complete JSON with ALL dimensions:

{{
  "concept": {{
    "name": "Concept name",
    "definition": "Full 2-3 paragraph definition",

    "genesis": {{
      "type": "theoretical_innovation|empirical_discovery|synthetic_unification|paradigm_shift",
      "lineage": "theoretical traditions it builds on",
      "break_from": "what it breaks from (Bachelardian rupture)",
      "break_rationale": "why it breaks from that",
      "originator_type": "individual|collective|institutional|emergent",
      "novelty_type": "terminological|conceptual|paradigmatic|methodological"
    }},

    "problem_space": {{
      "gap_type": "descriptive|explanatory|normative|practical|methodological",
      "gap_description": "the gap this concept fills",
      "failed_alternatives": ["concepts that failed", "and why"],
      "problem_domains": "where this gap is felt",
      "urgency_rationale": "why we need this concept now"
    }},

    "differentiations": [
      {{
        "confused_with": "Other Concept",
        "confusion_type": "synonym_collapse|subset_reduction|superset_expansion|false_opposition",
        "differentiation_axis": "the axis along which they differ",
        "this_concept_position": "where this concept sits on that axis",
        "other_concept_position": "where the other concept sits",
        "what_would_be_lost": "what we lose if we collapse them",
        "surface_similarity": "why they seem similar",
        "deep_difference": "why they're fundamentally different"
      }}
    ],

    "paradigmatic_cases": [
      {{
        "title": "Case name",
        "case_type": "historical|contemporary|hypothetical|composite",
        "description": "Full description",
        "why_paradigmatic": "why this exemplifies the concept",
        "features_exhibited": ["list of concept features this shows"],
        "features_absent": "limitations of this case"
      }}
    ],

    "recognition_markers": [
      {{
        "marker_type": "linguistic|structural|behavioral|situational|argumentative",
        "description": "Pattern to look for",
        "positive_indicator": "what confirms this is the concept",
        "negative_indicator": "what rules it out",
        "false_positive_risk": "what might be confused for this"
      }}
    ],

    "quinean": {{
      "centrality": "core|intermediate|peripheral",
      "web_coherence_impact": "how changing this affects other concepts",
      "forward_inferences": ["if this concept, then X"],
      "backward_inferences": ["this concept because Y"],
      "lateral_connections": ["related to Z via..."],
      "contradictions": ["contradicts W because..."]
    }},

    "sellarsian": {{
      "is_myth_of_given": true|false,
      "givenness_markers": ["phrases that treat this as foundational"],
      "should_be_inferred_from": "what evidence should support it",
      "theoretical_commitments_embedded": ["hidden assumptions"],
      "what_givenness_enables": "what treating as given allows",
      "what_givenness_blocks": "what questions become unaskable"
    }},

    "brandomian": {{
      "commitments": [
        {{ "statement": "what using this concept commits you to", "is_honored": true|false }}
      ],
      "entitlements": [
        {{ "statement": "what using this concept entitles you to claim" }}
      ],
      "incompatibilities": ["claims incompatible with this concept"]
    }},

    "deleuzian": {{
      "problems_addressed": [
        {{
          "problem": "tension or problem this navigates",
          "pole_a": "one pole of the tension",
          "pole_b": "other pole"
        }}
      ],
      "becomings_enabled": ["transformations this concept enables"],
      "becomings_blocked": ["transformations this concept prevents"],
      "plane_assumptions": [
        {{
          "assumption": "unquestioned background assumption",
          "makes_possible": ["what this enables"],
          "makes_impossible": ["what this forecloses"]
        }}
      ]
    }},

    "bachelardian": {{
      "is_obstacle": true|false,
      "obstacle_type": "experience|verbal|pragmatic|quantitative|substantialist",
      "what_it_blocks": ["understanding it prevents"],
      "evidence_of_inadequacy": ["empirical challenges"],
      "why_persists": "ideological function",
      "rupture_would_enable": "what becomes thinkable after rupture",
      "rupture_trigger": "what would force abandonment"
    }},

    "canguilhem": {{
      "health_status": "healthy|strained|dying|being_born",
      "birth_period": "when concept emerged",
      "birth_problem": "what problem it was created to solve",
      "evolution": [
        {{
          "period": "time period",
          "transformation": "what changed",
          "problem_driving": "what drove the change"
        }}
      ],
      "normative_dimensions": [
        {{
          "value_embedded": "what value is embedded",
          "whose_values": "whose interests this serves",
          "what_excluded": "what's marked as abnormal"
        }}
      ]
    }},

    "davidson": {{
      "style_required": "financial|geopolitical|technical|etc",
      "what_visible": ["what this reasoning style makes visible"],
      "what_invisible": ["what's systematically hidden"],
      "evidence_types_privileged": ["what counts as evidence"],
      "inference_patterns": ["characteristic reasoning moves"]
    }},

    "blumenberg": {{
      "root_metaphors": [
        {{
          "metaphor": "e.g. 'market as organism'",
          "source_domain": "where metaphor comes from",
          "what_enables": ["thinking it makes possible"],
          "what_hides": ["what it obscures"],
          "resists_conceptualization": true|false,
          "why_resists": "why it can't be made precise"
        }}
      ],
      "conceptual_work_in_progress": {{
        "original_meaning": "what concept meant originally",
        "current_work": "what transformation is being attempted",
        "who_doing_work": "intellectual tradition doing this work",
        "work_status": "succeeding|failing|ongoing"
      }}
    }},

    "carey": {{
      "hierarchy_level": 0|1|2|3,
      "bootstrap_status": "successful|partial|failed|attempted",
      "built_from": ["primitive concepts this is built from"],
      "combination_type": "simple_aggregation|interactive|qualitative_leap",
      "transparency": "high|medium|low",
      "bootstrap_failure_reason": "if failed, why",
      "what_would_fix": "what would make bootstrap succeed"
    }},

    "kuhnian": {{
      "paradigm_position": "normal_science|anomaly|crisis|revolutionary|post_revolutionary",
      "exemplars": ["paradigmatic cases that define proper use"],
      "puzzle_solving_rules": ["what counts as legitimate puzzle/solution"],
      "incommensurabilities": [
        {{
          "other_paradigm": "incompatible framework",
          "translation_failure": "what cannot be translated",
          "talk_past_reason": "why adherents talk past each other"
        }}
      ],
      "disciplinary_matrix": {{
        "symbolic_generalizations": ["shared formal expressions"],
        "models": ["shared heuristic models"],
        "values": ["shared epistemic values"],
        "exemplars": ["shared paradigmatic problem-solutions"]
      }},
      "paradigm_threat": {{
        "anomalies_detected": ["empirical challenges"],
        "crisis_indicators": ["signs of paradigm strain"],
        "revolutionary_potential": "none|low|medium|high"
      }}
    }},

    "foucauldian": {{
      "power_knowledge": {{
        "what_power_enables": "what knowledge becomes possible",
        "what_knowledge_enables": "what power relations it supports",
        "mutual_constitution": "how they reinforce each other"
      }},
      "governmentality": {{
        "mode": "discipline|security|sovereign|pastoral|neoliberal",
        "technologies": ["specific techniques of government"],
        "rationality": "underlying logic/reason",
        "subjects_produced": ["kinds of subjects this creates"]
      }},
      "discourse_formation": {{
        "rules_of_formation": ["what can be said"],
        "exclusion_procedures": ["what cannot be said"],
        "rarefaction": ["who can speak authoritatively"],
        "archive": "conditions of possibility for statements"
      }},
      "resistance": {{
        "points_of_reversal": ["where power can be contested"],
        "counter_conducts": ["alternative subject positions"],
        "specific_struggles": ["concrete sites of resistance"]
      }}
    }},

    "pragmatist": {{
      "practical_consequences": {{
        "if_true": ["what follows if we accept this"],
        "if_false": ["what follows if we reject this"],
        "difference_in_practice": "what changes in conduct"
      }},
      "cash_value": "the concept's meaning in experiential terms",
      "performative_dimension": {{
        "speech_acts": ["what saying this does"],
        "social_effects": ["how it changes social reality"],
        "world_making": "what reality it helps constitute"
      }},
      "habit_formation": {{
        "habits_enabled": ["patterns of action it supports"],
        "habits_blocked": ["patterns it makes difficult"],
        "disposition_changes": "how it reshapes conduct"
      }},
      "inquiry_context": {{
        "problematic_situation": "what problem generated this concept",
        "doubt_resolved": "what uncertainty it addresses",
        "belief_fixation": "how it settles inquiry"
      }},
      "meliorism": {{
        "improvement_enabled": "what gets better",
        "regression_risk": "what might get worse",
        "incremental_vs_revolutionary": "scope of change possible"
      }}
    }},

    "core_claims": {{
      "ontological": "What this concept says exists or is real",
      "causal": "What causal relationships it asserts",
      "normative": "What values or norms it implies",
      "methodological": "What methods it validates or requires"
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
- ALL dimensional sections are REQUIRED - populate based on available data
- paradigmatic_cases, recognition_markers, dialectics MUST be arrays
- USE user-validated data where provided
- INTEGRATE deep philosophical commitments into the relevant dimensional sections
- For missing data, make reasonable inferences based on the concept definition"""

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


# =============================================================================
# DOCUMENT UPLOAD & ANALYSIS - Sonnet 4.5 with 1M Token Context
# =============================================================================

@router.post("/analyze-document")
async def analyze_document(
    file: UploadFile = File(...),
    concept_name: str = Form(...),
    existing_context: str = Form(None)  # JSON string of existing context
):
    """
    Analyze an uploaded document using Claude Sonnet 4.5 with 1M token context.
    Extracts ALL 9 philosophical dimensions from the document.
    """
    # Read file content
    content = await file.read()
    filename = file.filename or "document"

    # Extract text based on file type
    if filename.lower().endswith('.pdf'):
        if not HAS_PDF_SUPPORT:
            raise HTTPException(
                status_code=400,
                detail="PDF support not available. Please install PyPDF2."
            )
        try:
            import io
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            document_text = ""
            for page in pdf_reader.pages:
                document_text += page.extract_text() + "\n\n"
        except Exception as e:
            logger.error(f"Error reading PDF: {e}")
            raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")
    elif filename.lower().endswith(('.txt', '.md', '.markdown')):
        document_text = content.decode('utf-8')
    else:
        # Try to decode as text
        try:
            document_text = content.decode('utf-8')
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Please upload PDF, TXT, or Markdown."
            )

    # Parse existing context if provided
    existing_ctx = {}
    if existing_context:
        try:
            existing_ctx = json.loads(existing_context)
        except json.JSONDecodeError:
            existing_ctx = {"raw": existing_context}

    # Truncate document if too long (though 1M should handle most docs)
    MAX_CHARS = 3_500_000  # ~1M tokens worth
    if len(document_text) > MAX_CHARS:
        document_text = document_text[:MAX_CHARS] + "\n\n[DOCUMENT TRUNCATED]"

    async def stream_document_analysis():
        try:
            client = get_claude_client()

            yield f"data: {json.dumps({'type': 'phase', 'phase': 'document_analysis', 'filename': filename})}\n\n"
            yield f"data: {json.dumps({'type': 'status', 'message': f'Analyzing document ({len(document_text)} characters)...'})}\n\n"

            prompt = DOCUMENT_ANALYSIS_PROMPT.format(
                concept_name=concept_name,
                document_content=document_text,
                existing_context=json.dumps(existing_ctx, indent=2) if existing_ctx else "(No existing context)"
            )

            # Use Sonnet 4.5 with 1M context beta
            # Beta header for Sonnet 4.5: context-1m-2025-08-07
            with client.beta.messages.stream(
                model=SONNET_MODEL,
                max_tokens=SONNET_MAX_OUTPUT,
                messages=[{"role": "user", "content": prompt}],
                betas=["context-1m-2025-08-07"]  # Sonnet 4.5 1M context beta
            ) as stream:
                full_text = ""
                for event in stream:
                    if event.type == "content_block_delta":
                        if hasattr(event.delta, 'text'):
                            full_text += event.delta.text
                            yield f"data: {json.dumps({'type': 'text', 'content': event.delta.text})}\n\n"

            # Parse the JSON response
            extraction = parse_wizard_response(full_text)

            yield f"data: {json.dumps({'type': 'complete', 'data': extraction})}\n\n"

        except Exception as e:
            logger.error(f"Error analyzing document: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_document_analysis(),
        media_type="text/event-stream"
    )


# =============================================================================
# DEEP PHILOSOPHICAL COMMITMENTS - Generate MC Questions for All 9 Dimensions
# =============================================================================

@router.post("/generate-deep-commitments")
async def generate_deep_commitments(request: DeepCommitmentsRequest):
    """
    Generate MC questions probing all 9 philosophical dimensions.
    Uses accumulated context to generate SPECIFIC, informed options.
    This should be called LATE in the wizard after context has accumulated.
    """
    async def stream_deep_commitments():
        try:
            client = get_claude_client()

            yield f"data: {json.dumps({'type': 'phase', 'phase': 'deep_commitments'})}\n\n"
            yield f"data: {json.dumps({'type': 'status', 'message': 'Generating philosophical dimension questions...'})}\n\n"

            prompt = GENERATE_DEEP_COMMITMENTS_PROMPT.format(
                concept_name=request.concept_name,
                notes_summary=request.notes_summary or "(No notes)",
                genealogy=json.dumps(request.genealogy, indent=2),
                stage1_answers=json.dumps(request.stage1_answers, indent=2),
                stage2_answers=json.dumps(request.stage2_answers, indent=2) if request.stage2_answers else "(Not yet answered)",
                dimensional_extraction=json.dumps(request.dimensional_extraction, indent=2) if request.dimensional_extraction else "(No document analysis yet)"
            )

            # Use Opus with extended thinking for sophisticated question generation
            with client.messages.stream(
                model=MODEL,
                max_tokens=MAX_OUTPUT,
                thinking={
                    "type": "enabled",
                    "budget_tokens": THINKING_BUDGET
                },
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                full_text = ""
                for event in stream:
                    if event.type == "content_block_delta":
                        if hasattr(event.delta, 'thinking'):
                            yield f"data: {json.dumps({'type': 'thinking', 'content': event.delta.thinking})}\n\n"
                        elif hasattr(event.delta, 'text'):
                            full_text += event.delta.text
                            yield f"data: {json.dumps({'type': 'text', 'content': event.delta.text})}\n\n"

            # Parse the questions
            questions_data = parse_wizard_response(full_text)

            # Structure the output
            result = {
                "deep_commitment_questions": questions_data.get("deep_commitment_questions", []),
                "generation_note": questions_data.get("generation_note", ""),
                "dimensions_covered": list(set([
                    q.get("dimension") for q in questions_data.get("deep_commitment_questions", [])
                    if q.get("dimension")
                ]))
            }

            yield f"data: {json.dumps({'type': 'complete', 'data': result})}\n\n"

        except Exception as e:
            logger.error(f"Error generating deep commitments: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_deep_commitments(),
        media_type="text/event-stream"
    )


# =============================================================================
# CARD TRANSFORMATION - Sharpen/Generalize/Radicalize/Historicize/Deepen
# =============================================================================

TRANSFORM_CARD_PROMPT = """You are an expert in conceptual analysis helping refine a hypothesis card.

## Transformation Mode: {mode}

{mode_instructions}

## Card to Transform
Type: {card_type}
Current Content: {card_content}

{notes_context_section}

{guidance_section}

## Instructions
Transform the card content according to the mode above.
Maintain the same general subject matter but apply the transformation.
Output ONLY the transformed content as a single paragraph or sentence - no JSON, no explanation, just the new card content.
The result should be a direct replacement for the original card content."""

MODE_INSTRUCTIONS = {
    'sharpen': """Make the claim MORE SPECIFIC and PRECISE:
- Add concrete details and specifics
- Narrow to a clearer, more pointed claim
- Replace vague or abstract terms with precise ones
- Name specific mechanisms, actors, or processes
- If referencing the user's notes, pull in specific quotes or examples""",

    'generalize': """Make the claim MORE GENERAL and ABSTRACT:
- Broaden to a wider pattern, principle, or phenomenon
- Remove overly specific details that limit applicability
- Connect to larger theoretical frameworks or traditions
- Identify the underlying logic that could apply to other cases
- Move from specific instance to general category""",

    'radicalize': """Push the claim to a MORE PROVOCATIVE position:
- Strengthen to its logical extreme
- Challenge implicit assumptions or unstated premises
- Make the stakes clearer and higher
- Remove hedging language and qualifications
- State the most challenging version of the claim""",

    'historicize': """Ground the claim in HISTORICAL PROCESS and CONTINGENCY:
- Situate in longer historical trajectory
- Identify conditions of emergence (when/why did this become thinkable?)
- Show contingency rather than naturalness
- Connect to specific historical developments or transformations
- Denaturalize what might seem obvious or inevitable""",

    'deepen': """Dig into UNDERLYING MECHANISMS and EXPLANATIONS:
- Identify the actual mechanisms at play
- Expose transmission channels and causal pathways
- Move from description/observation to explanation
- Ask "how does this actually work?"
- Uncover the infrastructure behind the phenomenon"""
}


@router.post("/transform-card")
async def transform_card(request: TransformCardRequest):
    """
    Transform a hypothesis/genealogy/differentiation/commitment card
    using one of five modes: sharpen, generalize, radicalize, historicize, deepen.

    This replicates the essay-flow transformation pattern for conceptual work.
    """
    async def stream_transformation():
        try:
            client = get_claude_client()

            # Validate mode
            if request.mode not in MODE_INSTRUCTIONS:
                yield f"data: {json.dumps({'type': 'error', 'message': f'Invalid mode: {request.mode}. Must be one of: sharpen, generalize, radicalize, historicize, deepen'})}\n\n"
                yield "data: [DONE]\n\n"
                return

            yield f"data: {json.dumps({'type': 'status', 'message': f'Applying {request.mode} transformation...'})}\n\n"

            # Build context sections
            notes_context_section = ""
            if request.notes_context:
                notes_context_section = f"""## Relevant Context from Notes
{request.notes_context[:2000]}  # Truncate to avoid context overflow
"""

            guidance_section = ""
            if request.guidance:
                guidance_section = f"""## User Guidance
{request.guidance}
"""

            prompt = TRANSFORM_CARD_PROMPT.format(
                mode=request.mode.upper(),
                mode_instructions=MODE_INSTRUCTIONS[request.mode],
                card_type=request.card_type,
                card_content=request.card_content,
                notes_context_section=notes_context_section,
                guidance_section=guidance_section
            )

            # Use Sonnet for faster transformation (doesn't need extended thinking)
            with client.messages.stream(
                model=SONNET_MODEL,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                transformed_content = ""
                for event in stream:
                    if event.type == "content_block_delta":
                        if hasattr(event.delta, 'text'):
                            transformed_content += event.delta.text
                            yield f"data: {json.dumps({'type': 'text', 'content': event.delta.text})}\n\n"

            # Clean up the response
            transformed_content = transformed_content.strip()

            result = {
                "card_id": request.card_id,
                "original_content": request.card_content,
                "transformed_content": transformed_content,
                "mode": request.mode,
                "guidance_used": request.guidance
            }

            yield f"data: {json.dumps({'type': 'complete', 'data': result})}\n\n"

        except Exception as e:
            logger.error(f"Error transforming card: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_transformation(),
        media_type="text/event-stream"
    )


# =============================================================================
# GENERATE OPTIONS FOR OPEN-ENDED QUESTIONS
# =============================================================================

GENERATE_OPTIONS_PROMPT = """You are helping a user develop a novel concept called "{concept_name}".

They are now answering this question:
## Question
{question_text}

Based on their notes and earlier responses, generate 4-5 SPECIFIC answer options they can choose from.

## Context from User's Notes
{notes_context}

## Validated Hypothesis Cards (things they've confirmed about their concept)
{hypothesis_context}

## Differentiation Cards (how their concept differs from others)
{differentiation_context}

## Previous Answers
{previous_answers_context}

## Your Task
Generate 4-5 distinct answer options that:
1. Are SPECIFIC to their concept (not generic answers that could apply to any concept)
2. Draw directly from their notes and validated cards
3. Represent meaningfully different positions/approaches
4. Are written as complete, articulate answers (not just labels)
5. Include a brief rationale for each option

Output JSON:
{{
  "options": [
    {{
      "id": "opt_1",
      "content": "The specific answer text that addresses the question based on their notes...",
      "rationale": "Why this option makes sense given their notes and validated cards...",
      "confidence": "high" | "medium" | "low"
    }}
  ]
}}

Be specific. Use their exact terminology from the notes. Reference concrete ideas they've already articulated."""


@router.post("/generate-options")
async def generate_options(request: GenerateOptionsRequest):
    """
    Generate multiple choice options for an open-ended question based on
    the user's notes, validated cards, and previous answers.

    This allows users to select from AI-generated options rather than
    writing everything from scratch.
    """
    async def stream_options():
        try:
            client = get_claude_client()

            yield f"data: {json.dumps({'type': 'status', 'message': 'Analyzing your notes and responses...'})}\n\n"

            # Build context sections
            notes_context = "No notes provided."
            if request.notes:
                # Truncate to reasonable size
                notes_context = request.notes[:8000]

            hypothesis_context = "No hypothesis cards validated yet."
            if request.hypothesis_cards:
                approved = [c for c in request.hypothesis_cards if c.get('status') == 'approved']
                if approved:
                    hypothesis_context = "\n".join([
                        f"- {c.get('content', c.get('text', ''))}"
                        for c in approved[:10]
                    ])

            differentiation_context = "No differentiation cards validated yet."
            if request.differentiation_cards:
                approved = [c for c in request.differentiation_cards if c.get('status') == 'approved']
                if approved:
                    differentiation_context = "\n".join([
                        f"- NOT {c.get('contrasted_with', '')}: {c.get('difference', c.get('content', ''))}"
                        for c in approved[:10]
                    ])

            previous_answers_context = "No previous answers."
            if request.previous_answers:
                prev = []
                for ans in request.previous_answers[:10]:
                    q = ans.get('question', ans.get('question_id', 'Unknown'))
                    a = ans.get('answer', ans.get('text_answer', ans.get('selected_options', '')))
                    if a:
                        prev.append(f"Q: {q}\nA: {a}")
                if prev:
                    previous_answers_context = "\n\n".join(prev)

            prompt = GENERATE_OPTIONS_PROMPT.format(
                concept_name=request.concept_name,
                question_text=request.question_text,
                notes_context=notes_context,
                hypothesis_context=hypothesis_context,
                differentiation_context=differentiation_context,
                previous_answers_context=previous_answers_context
            )

            yield f"data: {json.dumps({'type': 'status', 'message': 'Generating answer options...'})}\n\n"

            # Use Sonnet for fast option generation
            with client.messages.stream(
                model=SONNET_MODEL,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                response_text = ""
                for event in stream:
                    if event.type == "content_block_delta":
                        if hasattr(event.delta, 'text'):
                            response_text += event.delta.text

            # Parse the JSON response
            try:
                # Extract JSON from response (handle markdown code blocks)
                json_text = response_text
                if "```json" in json_text:
                    json_text = json_text.split("```json")[1].split("```")[0]
                elif "```" in json_text:
                    json_text = json_text.split("```")[1].split("```")[0]

                result = json.loads(json_text.strip())
                options = result.get("options", [])

                yield f"data: {json.dumps({'type': 'options', 'data': options})}\n\n"

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse options JSON: {e}")
                logger.error(f"Raw response: {response_text[:500]}")
                yield f"data: {json.dumps({'type': 'error', 'message': 'Failed to parse generated options'})}\n\n"

        except Exception as e:
            logger.error(f"Error generating options: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_options(),
        media_type="text/event-stream"
    )


# =============================================================================
# GENERATE INTELLECTUAL GENEALOGY
# =============================================================================

GENERATE_GENEALOGY_PROMPT = """You are helping a user develop a novel concept called "{concept_name}".

They have now completed several stages of concept development. Based on everything they've told you,
generate hypotheses about the INTELLECTUAL GENEALOGY of their concept.

## User's Notes
{notes_context}

## Validated Theses About Their Concept
{hypothesis_context}

## How They Differentiate Their Concept
{differentiation_context}

## Their Answers to Stage 1-3 Questions
{answers_context}

## Your Task: Generate Genealogy Hypotheses

For each hypothesis, identify:
1. **Type**: One of:
   - "thinker" - A specific thinker/philosopher/theorist
   - "concept" - A specific concept their idea descends from or responds to
   - "framework" - A theoretical framework they're working within or against
   - "debate" - An intellectual debate their concept intervenes in
   - "failed_alternative" - A concept/framework that failed, prompting theirs

2. **Name**: The specific thinker, concept, framework, or debate

3. **Connection**: HOW it relates to their concept (2-3 sentences, specific)

4. **Confidence**: high/medium/low based on explicit mentions vs inference

5. **Source Evidence**: Quote or reference from their notes if available

Generate 6-10 genealogy hypotheses. Be SPECIFIC:
- Not "critical theory" but "Adorno's concept of the culture industry"
- Not "Marxism" but "Marx's concept of commodity fetishism" or "Polanyi's embeddedness"
- Not "platform studies" but "Srnicek's platform capitalism" or "Zuboff's surveillance capitalism"

Think about:
- What thinkers do they explicitly or implicitly reference?
- What concepts does their concept seem to descend from or critique?
- What frameworks are they working within?
- What debates does their concept intervene in?
- What alternatives failed, creating the need for their concept?

Output JSON:
{{
  "genealogy_hypotheses": [
    {{
      "id": "gen_001",
      "type": "thinker",
      "name": "Karl Polanyi",
      "connection": "Your concept of 'organic capitalism' extends Polanyi's idea of embedded/disembedded economies. You're arguing platforms re-embed economic relations while appearing disembedded.",
      "confidence": "high",
      "source_evidence": "User explicitly mentions embeddedness...",
      "why_relevant": "Central to understanding the 'organic' dimension"
    }}
  ]
}}"""


@router.post("/generate-genealogy")
async def generate_genealogy(request: GenerateGenealogyRequest):
    """
    Generate intellectual genealogy hypotheses based on all previous wizard responses.

    This generates specific hypotheses about:
    - Thinkers who influenced the concept
    - Conceptual ancestors
    - Frameworks being used or critiqued
    - Debates the concept intervenes in
    - Failed alternatives that motivated the concept
    """
    async def stream_genealogy():
        try:
            client = get_claude_client()

            yield f"data: {json.dumps({'type': 'status', 'message': 'Analyzing your concept development for intellectual genealogy...'})}\n\n"

            # Build context from all inputs
            notes_context = request.notes[:12000] if request.notes else "No notes provided."

            hypothesis_context = "No hypothesis cards."
            if request.hypothesis_cards:
                approved = [c for c in request.hypothesis_cards if c.get('status') == 'approved']
                if approved:
                    hypothesis_context = "\n".join([
                        f"- {c.get('content', c.get('text', ''))}"
                        for c in approved[:15]
                    ])

            differentiation_context = "No differentiation cards."
            if request.differentiation_cards:
                approved = [c for c in request.differentiation_cards if c.get('status') == 'approved']
                if approved:
                    differentiation_context = "\n".join([
                        f"- NOT {c.get('contrasted_with', '')}: {c.get('difference', c.get('content', ''))}"
                        for c in approved[:10]
                    ])

            # Compile all stage answers
            answers_parts = []
            for stage_name, answers in [
                ("Stage 1 (Genesis)", request.stage1_answers),
                ("Stage 2 (Differentiation)", request.stage2_answers),
                ("Stage 3 (Methodology)", request.stage3_answers)
            ]:
                if answers:
                    stage_text = f"\n### {stage_name}\n"
                    for ans in answers[:10]:
                        q = ans.get('question', ans.get('question_id', 'Q'))
                        a = ans.get('answer', ans.get('text_answer', ans.get('selected_options', '')))
                        if isinstance(a, list):
                            a = ', '.join(str(x) for x in a)
                        if a:
                            stage_text += f"Q: {q}\nA: {a}\n\n"
                    answers_parts.append(stage_text)

            answers_context = "\n".join(answers_parts) if answers_parts else "No stage answers yet."

            prompt = GENERATE_GENEALOGY_PROMPT.format(
                concept_name=request.concept_name,
                notes_context=notes_context,
                hypothesis_context=hypothesis_context,
                differentiation_context=differentiation_context,
                answers_context=answers_context
            )

            yield f"data: {json.dumps({'type': 'status', 'message': 'Generating genealogy hypotheses...'})}\n\n"

            # Use Sonnet for fast generation with extended context
            with client.messages.stream(
                model=SONNET_MODEL,
                max_tokens=8192,
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                response_text = ""
                for event in stream:
                    if event.type == "content_block_delta":
                        if hasattr(event.delta, 'text'):
                            response_text += event.delta.text

            # Parse JSON response
            try:
                json_text = response_text
                if "```json" in json_text:
                    json_text = json_text.split("```json")[1].split("```")[0]
                elif "```" in json_text:
                    json_text = json_text.split("```")[1].split("```")[0]

                result = json.loads(json_text.strip())
                hypotheses = result.get("genealogy_hypotheses", [])

                yield f"data: {json.dumps({'type': 'genealogy', 'data': hypotheses})}\n\n"

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse genealogy JSON: {e}")
                logger.error(f"Raw response: {response_text[:500]}")
                yield f"data: {json.dumps({'type': 'error', 'message': 'Failed to parse genealogy hypotheses'})}\n\n"

        except Exception as e:
            logger.error(f"Error generating genealogy: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_genealogy(),
        media_type="text/event-stream"
    )


# =============================================================================
# PHASE 2: TARGETED FOLLOW-UP QUESTIONS
# =============================================================================

GENERATE_PHASE2_PROMPT = """You are Claude helping a user sharpen their philosophical commitments for the concept "{concept_name}".

The user just completed Phase 1 of the philosophical interrogation. You have their answers.
Your job: Generate TARGETED FOLLOW-UP questions based on their Phase 1 answers.

## ACCUMULATED CONTEXT:
Notes Summary: {notes_summary}
Genealogy (approved influences): {genealogy}
Earlier Stage Answers: {stage_answers}

## PHASE 1 QUESTIONS AND ANSWERS:
{phase1_qa}

## YOUR TASK:
Analyze each Phase 1 answer and identify:
1. Answers that need clarification or sharpening
2. Answers that reveal tensions with other commitments
3. Answers where "None of these" was selected (need custom exploration)
4. Implicit commitments that deserve explicit questioning
5. Gaps in the dimensional coverage

Generate 4-8 FOLLOW-UP questions that:
- Explicitly reference and build on their Phase 1 answers
- Are SHARPER and more SPECIFIC than Phase 1
- Probe tensions, clarify ambiguities, fill gaps
- Use concrete options derived from the user's context

For each question include:
- `follow_up_to`: Brief description of which Phase 1 answer this follows up on
- `rationale`: Why this follow-up is needed

Return as JSON:
{{
  "questions": [
    {{
      "id": "p2_q1",
      "dimension": "quinean",
      "follow_up_to": "They said X about inferential commitments, but...",
      "question": "Specific follow-up question text?",
      "rationale": "This matters because...",
      "options": [
        {{"value": "opt_a", "label": "Sharp option A", "description": "What this means"}},
        {{"value": "opt_b", "label": "Sharp option B", "description": "What this means"}},
        {{"value": "opt_c", "label": "Sharp option C", "description": "What this means"}}
      ]
    }}
  ],
  "generation_note": "Summary of what Phase 2 is probing"
}}"""


@router.post("/generate-phase2-questions")
async def generate_phase2_questions(request: Phase2QuestionsRequest):
    """
    Generate Phase 2 follow-up questions based on Phase 1 answers.
    These questions are sharper and more targeted based on the user's specific responses.
    """
    async def stream_phase2():
        try:
            client = get_claude_client()

            yield f"data: {json.dumps({'type': 'phase', 'phase': 'phase2_generation'})}\n\n"
            yield f"data: {json.dumps({'type': 'status', 'message': 'Analyzing Phase 1 answers...'})}\n\n"

            # Build Phase 1 Q&A context
            phase1_qa_lines = []
            for q in request.phase1_questions:
                q_id = q.get("id", "unknown")
                q_text = q.get("question", "")
                q_dim = q.get("dimension", "")
                answer = request.phase1_answers.get(q_id, {})
                selected = answer.get("selected", "(no answer)")
                comment = answer.get("comment", "")

                phase1_qa_lines.append(f"Q [{q_dim}]: {q_text}")
                phase1_qa_lines.append(f"A: {selected}")
                if comment:
                    phase1_qa_lines.append(f"Comment: {comment}")
                phase1_qa_lines.append("")

            # Build stage answers context
            stage_answers = []
            if request.stage1_answers:
                stage_answers.extend([f"Stage 1: {json.dumps(a)}" for a in request.stage1_answers[:3]])
            if request.stage2_answers:
                stage_answers.extend([f"Stage 2: {json.dumps(a)}" for a in request.stage2_answers[:3]])
            if request.stage3_answers:
                stage_answers.extend([f"Stage 3: {json.dumps(a)}" for a in request.stage3_answers[:3]])

            prompt = GENERATE_PHASE2_PROMPT.format(
                concept_name=request.concept_name,
                notes_summary=request.notes_summary or "(No notes)",
                genealogy=json.dumps(request.genealogy or [], indent=2),
                stage_answers="\\n".join(stage_answers) if stage_answers else "(No earlier answers)",
                phase1_qa="\\n".join(phase1_qa_lines)
            )

            # Use Sonnet for speed
            with client.messages.stream(
                model=SONNET_MODEL,
                max_tokens=8192,
                thinking={
                    "type": "enabled",
                    "budget_tokens": 8000
                },
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                response_text = ""
                for event in stream:
                    if event.type == "content_block_delta":
                        if hasattr(event.delta, 'thinking'):
                            yield f"data: {json.dumps({'type': 'thinking', 'content': event.delta.thinking})}\n\n"
                        elif hasattr(event.delta, 'text'):
                            response_text += event.delta.text

            # Parse JSON response
            try:
                json_text = response_text
                if "```json" in json_text:
                    json_text = json_text.split("```json")[1].split("```")[0]
                elif "```" in json_text:
                    json_text = json_text.split("```")[1].split("```")[0]

                result = json.loads(json_text.strip())

                yield f"data: {json.dumps({'type': 'complete', 'data': result})}\n\n"

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse Phase 2 JSON: {e}")
                logger.error(f"Raw response: {response_text[:500]}")
                yield f"data: {json.dumps({'type': 'error', 'message': 'Failed to parse follow-up questions'})}\n\n"

        except Exception as e:
            logger.error(f"Error generating Phase 2 questions: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_phase2(),
        media_type="text/event-stream"
    )


# =============================================================================
# PHASE 3: SYNTHESIS AND VERIFICATION QUESTIONS
# =============================================================================

GENERATE_PHASE3_PROMPT = """You are Claude helping a user finalize the philosophical commitments of their concept "{concept_name}".

The user has completed Phases 1 and 2 of the philosophical interrogation. You have all their answers.
Your job: Generate FINAL SYNTHESIS questions that verify coherence and resolve any remaining tensions.

## ACCUMULATED CONTEXT:
Notes Summary: {notes_summary}
Genealogy (approved influences): {genealogy}

## PHASE 1 QUESTIONS AND ANSWERS:
{phase1_qa}

## PHASE 2 QUESTIONS AND ANSWERS:
{phase2_qa}

## YOUR TASK:
Generate 3-5 FINAL questions that:
1. VERIFY key commitments by presenting them back for confirmation
2. RESOLVE any remaining tensions between different answers
3. SYNTHESIZE across dimensions to check for coherence
4. Ask about edge cases or limiting conditions
5. Confirm the user's overall philosophical stance

Each question should:
- Reference specific answers from P1/P2
- Present a synthesis or verification check
- Have 2-4 sharp options that crystallize different stances

Include for each question:
- `synthesis_context`: What aspects of their answers this synthesizes or verifies

Return as JSON:
{{
  "questions": [
    {{
      "id": "p3_q1",
      "dimension": "synthesis",
      "synthesis_context": "Your answers suggest X (from Quinean) but also Y (from Deleuzian)...",
      "question": "Which better captures your overall position?",
      "rationale": "Resolving this tension will clarify...",
      "options": [
        {{"value": "synthesis_a", "label": "Position A (emphasizing X)", "description": "This means..."}},
        {{"value": "synthesis_b", "label": "Position B (emphasizing Y)", "description": "This means..."}},
        {{"value": "synthesis_c", "label": "Both can coexist because...", "description": "Explain how"}}
      ]
    }}
  ],
  "generation_note": "Summary of what Phase 3 synthesizes"
}}"""


@router.post("/generate-phase3-questions")
async def generate_phase3_questions(request: Phase3QuestionsRequest):
    """
    Generate Phase 3 synthesis/verification questions.
    These questions verify coherence and resolve tensions from Phases 1 and 2.
    """
    async def stream_phase3():
        try:
            client = get_claude_client()

            yield f"data: {json.dumps({'type': 'phase', 'phase': 'phase3_generation'})}\n\n"
            yield f"data: {json.dumps({'type': 'status', 'message': 'Synthesizing all answers...'})}\n\n"

            # Build Phase 1 Q&A context
            phase1_qa_lines = []
            for q in request.phase1_questions:
                q_id = q.get("id", "unknown")
                q_text = q.get("question", "")
                q_dim = q.get("dimension", "")
                answer = request.phase1_answers.get(q_id, {})
                selected = answer.get("selected", "(no answer)")
                comment = answer.get("comment", "")

                phase1_qa_lines.append(f"Q [{q_dim}]: {q_text}")
                phase1_qa_lines.append(f"A: {selected}")
                if comment:
                    phase1_qa_lines.append(f"Comment: {comment}")
                phase1_qa_lines.append("")

            # Build Phase 2 Q&A context
            phase2_qa_lines = []
            for q in request.phase2_questions:
                q_id = q.get("id", "unknown")
                q_text = q.get("question", "")
                q_dim = q.get("dimension", "")
                answer = request.phase2_answers.get(q_id, {})
                selected = answer.get("selected", "(no answer)")
                comment = answer.get("comment", "")

                phase2_qa_lines.append(f"Q [{q_dim}]: {q_text}")
                phase2_qa_lines.append(f"A: {selected}")
                if comment:
                    phase2_qa_lines.append(f"Comment: {comment}")
                phase2_qa_lines.append("")

            prompt = GENERATE_PHASE3_PROMPT.format(
                concept_name=request.concept_name,
                notes_summary=request.notes_summary or "(No notes)",
                genealogy=json.dumps(request.genealogy or [], indent=2),
                phase1_qa="\\n".join(phase1_qa_lines),
                phase2_qa="\\n".join(phase2_qa_lines)
            )

            # Use Sonnet for speed
            with client.messages.stream(
                model=SONNET_MODEL,
                max_tokens=8192,
                thinking={
                    "type": "enabled",
                    "budget_tokens": 8000
                },
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                response_text = ""
                for event in stream:
                    if event.type == "content_block_delta":
                        if hasattr(event.delta, 'thinking'):
                            yield f"data: {json.dumps({'type': 'thinking', 'content': event.delta.thinking})}\n\n"
                        elif hasattr(event.delta, 'text'):
                            response_text += event.delta.text

            # Parse JSON response
            try:
                json_text = response_text
                if "```json" in json_text:
                    json_text = json_text.split("```json")[1].split("```")[0]
                elif "```" in json_text:
                    json_text = json_text.split("```")[1].split("```")[0]

                result = json.loads(json_text.strip())

                yield f"data: {json.dumps({'type': 'complete', 'data': result})}\n\n"

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse Phase 3 JSON: {e}")
                logger.error(f"Raw response: {response_text[:500]}")
                yield f"data: {json.dumps({'type': 'error', 'message': 'Failed to parse synthesis questions'})}\n\n"

        except Exception as e:
            logger.error(f"Error generating Phase 3 questions: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_phase3(),
        media_type="text/event-stream"
    )


# =============================================================================
# POSIT TYPES ENDPOINT
# =============================================================================

@router.get("/posit-types")
async def get_posit_types():
    """
    Get the posit type typology with metadata for frontend display.

    Returns all 9 posit types with their labels, descriptions, dimensions, and colors.
    Used by the frontend to render posit cards with proper styling.
    """
    return {
        "types": [
            {
                "value": posit_type.value,
                "label": metadata["label"],
                "description": metadata["description"],
                "dimension": metadata["dimension"],
                "color": metadata["color"]
            }
            for posit_type, metadata in POSIT_TYPE_METADATA.items()
        ],
        "description": "9-dimension grounded typology for preliminary posits (claims detected in user's notes)"
    }


# =============================================================================
# WIZARD SESSION ENDPOINTS (Cross-device persistence)
# =============================================================================

@router.get("/sessions", response_model=List[WizardSessionListItem])
async def list_sessions(
    status: Optional[str] = "active",
    db: AsyncSession = Depends(get_db)
):
    """List all wizard sessions, optionally filtered by status."""
    try:
        query = select(WizardSession).order_by(WizardSession.updated_at.desc())
        if status:
            query = query.where(WizardSession.status == status)

        result = await db.execute(query)
        sessions = result.scalars().all()

        return [
            WizardSessionListItem(
                id=s.id,
                session_key=s.session_key,
                concept_name=s.concept_name,
                stage=s.stage,
                status=s.status,
                created_at=s.created_at,
                updated_at=s.updated_at
            )
            for s in sessions
        ]
    except Exception as e:
        logger.error(f"Error listing sessions: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{session_key}", response_model=WizardSessionResponse)
async def get_session(
    session_key: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific wizard session by session key."""
    try:
        result = await db.execute(
            select(WizardSession).where(WizardSession.session_key == session_key)
        )
        session = result.scalar_one_or_none()

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Update last_accessed_at
        session.last_accessed_at = datetime.utcnow()
        await db.commit()
        await db.refresh(session)  # Reload to avoid lazy-load issues in async context

        return WizardSessionResponse(
            id=session.id,
            session_key=session.session_key,
            concept_name=session.concept_name,
            session_state=session.session_state,
            stage=session.stage,
            source_id=session.source_id,
            status=session.status,
            created_at=session.created_at,
            updated_at=session.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sessions", response_model=WizardSessionResponse)
async def save_session(
    request: WizardSessionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create or update a wizard session."""
    try:
        session_key = request.session_key or str(uuid.uuid4())

        # Check if session exists
        result = await db.execute(
            select(WizardSession).where(WizardSession.session_key == session_key)
        )
        existing = result.scalar_one_or_none()

        if existing:
            # Update existing session
            existing.concept_name = request.concept_name
            # MERGE session_state instead of overwrite to preserve curator/sharpener data
            # This prevents frontend debounced saves from wiping out blind_spots_queue
            merged_state = dict(existing.session_state or {})
            new_state = dict(request.session_state or {})
            # Preserve backend-generated fields that frontend doesn't track
            for key in ['curator_allocation', 'blind_spots_queue', 'sharpener_results']:
                if key in merged_state and key not in new_state:
                    new_state[key] = merged_state[key]
            existing.session_state = new_state
            # Explicitly flag the JSON column as modified
            attributes.flag_modified(existing, 'session_state')
            existing.stage = request.stage
            existing.source_id = request.source_id
            existing.last_accessed_at = datetime.utcnow()
            session = existing
        else:
            # Create new session
            session = WizardSession(
                session_key=session_key,
                concept_name=request.concept_name,
                session_state=request.session_state,
                stage=request.stage,
                source_id=request.source_id,
                status="active"
            )
            db.add(session)

        await db.commit()
        await db.refresh(session)

        return WizardSessionResponse(
            id=session.id,
            session_key=session.session_key,
            concept_name=session.concept_name,
            session_state=session.session_state,
            stage=session.stage,
            source_id=session.source_id,
            status=session.status,
            created_at=session.created_at,
            updated_at=session.updated_at
        )
    except Exception as e:
        logger.error(f"Error saving session: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/sessions/{session_key}")
async def delete_session(
    session_key: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete a wizard session."""
    try:
        result = await db.execute(
            select(WizardSession).where(WizardSession.session_key == session_key)
        )
        session = result.scalar_one_or_none()

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        await db.delete(session)
        await db.commit()

        return {"status": "deleted", "session_key": session_key}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting session: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/sessions/{session_key}/status")
async def update_session_status(
    session_key: str,
    status: str,
    db: AsyncSession = Depends(get_db)
):
    """Update a session's status (active, completed, abandoned)."""
    try:
        if status not in ["active", "completed", "abandoned"]:
            raise HTTPException(status_code=400, detail="Invalid status")

        result = await db.execute(
            select(WizardSession).where(WizardSession.session_key == session_key)
        )
        session = result.scalar_one_or_none()

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        session.status = status
        await db.commit()

        return {"status": status, "session_key": session_key}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating session status: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# CURATOR-SHARPENER ENDPOINTS
# =============================================================================

# In-memory storage for sharpener tasks (in production, use Redis)
_sharpener_tasks: Dict[str, Dict[str, Any]] = {}


@router.post("/curate-blind-spots")
async def curate_blind_spots(request: CurateBlindSpotsRequest, db: AsyncSession = Depends(get_db)):
    """
    Curator Service: Analyzes notes against 7-category registry.
    Returns allocation plan with initial questions.
    """
    async def stream_curator_response():
        try:
            yield f"data: {json.dumps({'type': 'phase', 'phase': 'curating_blind_spots'})}\n\n"

            # Build notes understanding section if provided
            notes_understanding_section = ""
            if request.notes_understanding:
                notes_understanding_section = f"""
## Notes Understanding (from previous analysis):
{json.dumps(request.notes_understanding, indent=2)}
"""

            # Format the prompt
            prompt = CURATOR_PROMPT.format(
                categories_registry=EPISTEMIC_CATEGORIES_REGISTRY,
                concept_name=request.concept_name,
                notes=request.notes,
                notes_understanding_section=notes_understanding_section
            )

            yield f"data: {json.dumps({'type': 'phase', 'phase': 'calling_claude'})}\n\n"

            client = get_claude_client()

            # Use streaming for extended thinking
            allocation_data = None
            thinking_content = ""

            with client.messages.stream(
                model=MODEL,
                max_tokens=MAX_OUTPUT,
                thinking={
                    "type": "enabled",
                    "budget_tokens": THINKING_BUDGET
                },
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                full_text = ""
                for event in stream:
                    if hasattr(event, 'type'):
                        if event.type == 'content_block_delta':
                            if hasattr(event.delta, 'thinking'):
                                thinking_content += event.delta.thinking
                            elif hasattr(event.delta, 'text'):
                                full_text += event.delta.text

                # Parse JSON from response
                if full_text:
                    # Find JSON in response
                    json_start = full_text.find('{')
                    json_end = full_text.rfind('}') + 1
                    if json_start >= 0 and json_end > json_start:
                        json_str = full_text[json_start:json_end]
                        allocation_data = json.loads(json_str)

            if not allocation_data:
                raise ValueError("Failed to parse curator response")

            yield f"data: {json.dumps({'type': 'phase', 'phase': 'processing_allocation'})}\n\n"

            # Validate and structure the response
            total_slots = allocation_data.get('total_slots', 12)
            category_weights = allocation_data.get('category_weights', {})
            emphasis_rationale = allocation_data.get('emphasis_rationale', '')
            identified_blind_spots = allocation_data.get('identified_blind_spots', [])
            slots = allocation_data.get('slots', [])
            slot_sequence = allocation_data.get('slot_sequence', [])

            # Use our interleaving algorithm if LLM didn't follow the rule well
            if slots:
                # Count categories in slots
                category_counts = {}
                for slot in slots:
                    cat = slot.get('category', 'ambiguity')
                    category_counts[cat] = category_counts.get(cat, 0) + 1

                # Generate proper interleaved sequence
                proper_sequence = interleave_slots(category_counts)

                # Reorder slots to match interleaved sequence
                slots_by_category: Dict[str, List[Dict]] = {}
                for slot in slots:
                    cat = slot.get('category', 'ambiguity')
                    if cat not in slots_by_category:
                        slots_by_category[cat] = []
                    slots_by_category[cat].append(slot)

                # Rebuild slots in interleaved order
                reordered_slots = []
                category_indices = {cat: 0 for cat in slots_by_category}
                for cat in proper_sequence:
                    if cat in slots_by_category and category_indices[cat] < len(slots_by_category[cat]):
                        slot = slots_by_category[cat][category_indices[cat]]
                        slot['slot_id'] = f"slot_{len(reordered_slots) + 1:02d}"
                        reordered_slots.append(slot)
                        category_indices[cat] += 1

                slots = reordered_slots
                slot_sequence = proper_sequence

            # Build the response
            curator_allocation = {
                'total_slots': total_slots,
                'category_weights': category_weights,
                'slot_sequence': slot_sequence,
                'emphasis_rationale': emphasis_rationale,
                'identified_blind_spots': identified_blind_spots,
                'slots': slots
            }

            # Build the initial queue
            blind_spots_queue = {
                'slots': slots,
                'current_index': 0,
                'sharpener_pending': [],
                'completed_count': 0,
                'skipped_count': 0
            }

            # If session_id provided, save to database
            # Use fresh session inside generator (db from Depends may be closed)
            if request.session_id:
                try:
                    async with AsyncSessionLocal() as db_session:
                        result = await db_session.execute(
                            select(WizardSession).where(WizardSession.session_key == request.session_id)
                        )
                        session = result.scalar_one_or_none()
                        if session:
                            # Create a NEW dict to ensure SQLAlchemy detects the change
                            session_state = dict(session.session_state or {})
                            session_state['curator_allocation'] = curator_allocation
                            session_state['blind_spots_queue'] = blind_spots_queue
                            session.session_state = session_state
                            # Explicitly flag the JSON column as modified
                            attributes.flag_modified(session, 'session_state')
                            await db_session.commit()
                            logger.info(f"Saved curator state for session {request.session_id} with {len(slots)} slots")
                        else:
                            logger.warning(f"Session not found for session_id: {request.session_id}")
                except Exception as e:
                    logger.error(f"Error saving curator state: {e}", exc_info=True)

            yield f"data: {json.dumps({'type': 'curator_complete', 'data': {'curator_allocation': curator_allocation, 'blind_spots_queue': blind_spots_queue}})}\n\n"
            yield "data: [DONE]\n\n"

        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error in curator: {e}")
            yield f"data: {json.dumps({'type': 'error', 'error': f'Failed to parse curator response: {str(e)}'})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            logger.error(f"Curator error: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_curator_response(),
        media_type="text/event-stream"
    )


@router.post("/submit-blind-spot-answer")
async def submit_blind_spot_answer(request: SubmitBlindSpotAnswerRequest, db: AsyncSession = Depends(get_db)):
    """
    Submit an answer to a blind spot question.
    Updates queue state and triggers sharpener if appropriate.
    """
    try:
        logger.info(f"[submit-blind-spot-answer] session_id={request.session_id}, slot_id={request.slot_id}")

        # Load session
        result = await db.execute(
            select(WizardSession).where(WizardSession.session_key == request.session_id)
        )
        session = result.scalar_one_or_none()
        if not session:
            logger.error(f"[submit-blind-spot-answer] Session not found: {request.session_id}")
            raise HTTPException(status_code=404, detail="Session not found")

        session_state = session.session_state or {}
        logger.info(f"[submit-blind-spot-answer] session_state keys: {list(session_state.keys())}")

        # Handle both camelCase (frontend) and snake_case naming
        queue = session_state.get('blind_spots_queue') or session_state.get('blindSpotsQueue', {})
        slots = queue.get('slots', [])
        logger.info(f"[submit-blind-spot-answer] queue has {len(slots)} slots")

        # Find and update the slot
        slot_found = False
        answered_slot = None
        for slot in slots:
            if slot.get('slot_id') == request.slot_id:
                slot_found = True
                answered_slot = slot
                if request.skip:
                    slot['status'] = 'skipped'
                    queue['skipped_count'] = queue.get('skipped_count', 0) + 1
                else:
                    slot['status'] = 'answered'
                    slot['answer'] = request.answer
                    queue['completed_count'] = queue.get('completed_count', 0) + 1
                break

        if not slot_found:
            available_ids = [s.get('slot_id') for s in slots]
            logger.error(f"[submit-blind-spot-answer] Slot not found. Requested: {request.slot_id}, Available: {available_ids}")
            raise HTTPException(status_code=404, detail=f"Slot not found. Requested: {request.slot_id}, Available: {available_ids}")

        # Move to next slot
        queue['current_index'] = queue.get('current_index', 0) + 1

        # Save updated state
        session_state['blind_spots_queue'] = queue
        session.session_state = session_state
        attributes.flag_modified(session, 'session_state')
        await db.commit()

        # Determine if we should trigger sharpener
        should_sharpen = False
        if not request.skip and answered_slot:
            depth = answered_slot.get('depth', 1)
            if depth < 3:  # Max depth is 3
                should_sharpen = True

        # Check completion status
        quality = assess_completion_quality(BlindSpotsQueue(**queue))
        is_complete = queue['current_index'] >= len(slots)

        response = {
            'status': 'answer_received',
            'slot_id': request.slot_id,
            'skipped': request.skip,
            'queue_state': queue,
            'should_sharpen': should_sharpen,
            'is_complete': is_complete,
            'quality': quality if is_complete else None
        }

        # If sharpener should run, include the context needed
        if should_sharpen:
            response['sharpener_context'] = {
                'slot_id': request.slot_id,
                'category': answered_slot.get('category'),
                'depth': answered_slot.get('depth', 1),
                'question': answered_slot.get('question'),
                'answer': request.answer
            }

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting answer: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sharpen-question")
async def sharpen_question(request: SharpenQuestionRequest, db: AsyncSession = Depends(get_db)):
    """
    Sharpener Service: Generates a deeper follow-up question.
    Called asynchronously while user answers other questions.
    """
    async def stream_sharpener_response():
        try:
            yield f"data: {json.dumps({'type': 'phase', 'phase': 'sharpening'})}\n\n"

            # Load session for context
            result = await db.execute(
                select(WizardSession).where(WizardSession.session_key == request.session_id)
            )
            session = result.scalar_one_or_none()

            session_state = session.session_state if session else {}
            # Handle both camelCase (frontend) and snake_case naming
            queue = session_state.get('blind_spots_queue') or session_state.get('blindSpotsQueue', {})
            slots = queue.get('slots', [])

            # Find the original slot
            original_slot = None
            for slot in slots:
                if slot.get('slot_id') == request.slot_id:
                    original_slot = slot
                    break

            if not original_slot:
                yield f"data: {json.dumps({'type': 'error', 'error': 'Original slot not found'})}\n\n"
                yield "data: [DONE]\n\n"
                return

            # Gather context from other answers
            context_answers = []
            for slot in slots:
                if slot.get('status') == 'answered' and slot.get('slot_id') != request.slot_id:
                    context_answers.append({
                        'category': slot.get('category'),
                        'question': slot.get('question'),
                        'answer': slot.get('answer')
                    })

            context_answers_str = json.dumps(context_answers, indent=2) if context_answers else "No other answers yet."

            # Get notes context
            notes_context = request.notes_context or session_state.get('notes', '') or "Notes not available."

            current_depth = original_slot.get('depth', 1)
            next_depth = current_depth + 1

            # Format the sharpener prompt
            prompt = SHARPENER_PROMPT.format(
                categories_registry=EPISTEMIC_CATEGORIES_REGISTRY,
                concept_name=request.concept_name,
                original_question=original_slot.get('question', ''),
                user_answer=request.answer,
                category=original_slot.get('category', 'ambiguity'),
                depth=current_depth,
                next_depth=next_depth,
                notes_context=notes_context[:2000],  # Truncate if too long
                context_answers=context_answers_str[:3000]  # Truncate if too long
            )

            yield f"data: {json.dumps({'type': 'phase', 'phase': 'calling_claude'})}\n\n"

            client = get_claude_client()

            # Use a smaller model for faster response (or same model with less thinking)
            sharpener_result = None

            with client.messages.stream(
                model=SONNET_MODEL,  # Use Sonnet for speed
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                full_text = ""
                for event in stream:
                    if hasattr(event, 'type'):
                        if event.type == 'content_block_delta':
                            if hasattr(event.delta, 'text'):
                                full_text += event.delta.text

                # Parse JSON from response
                if full_text:
                    json_start = full_text.find('{')
                    json_end = full_text.rfind('}') + 1
                    if json_start >= 0 and json_end > json_start:
                        json_str = full_text[json_start:json_end]
                        sharpener_result = json.loads(json_str)

            if not sharpener_result:
                yield f"data: {json.dumps({'type': 'error', 'error': 'Failed to parse sharpener response'})}\n\n"
                yield "data: [DONE]\n\n"
                return

            # Create new slot for the follow-up question
            new_slot_id = f"slot_{len(slots) + 1:02d}"
            new_slot = {
                'slot_id': new_slot_id,
                'category': original_slot.get('category', 'ambiguity'),
                'depth': next_depth,
                'question': sharpener_result.get('question', ''),
                'status': 'pending',
                'generated_by': 'sharpener',
                'parent_slot_id': request.slot_id,
                'blind_spot_ref': sharpener_result.get('connects_to', '')
            }

            # Determine insert position (after current position but not immediately)
            current_index = queue.get('current_index', 0)
            # Insert 2-3 slots ahead to give user variety
            insert_position = min(current_index + 2, len(slots))

            # Update session state with new slot
            if session:
                slots.insert(insert_position, new_slot)
                queue['slots'] = slots
                session_state['blind_spots_queue'] = queue
                session.session_state = session_state
                await db.commit()

            yield f"data: {json.dumps({'type': 'sharpener_complete', 'data': {'new_slot': new_slot, 'insert_position': insert_position, 'queue_length': len(slots), 'rationale': sharpener_result.get('rationale', '')}})}\n\n"
            yield "data: [DONE]\n\n"

        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error in sharpener: {e}")
            yield f"data: {json.dumps({'type': 'error', 'error': f'Failed to parse sharpener response: {str(e)}'})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            logger.error(f"Sharpener error: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_sharpener_response(),
        media_type="text/event-stream"
    )


@router.post("/finish-blind-spots")
async def finish_blind_spots(request: FinishBlindSpotsRequest, db: AsyncSession = Depends(get_db)):
    """
    Finish blind spots questioning early.
    Returns completion assessment.
    """
    try:
        # Load session
        result = await db.execute(
            select(WizardSession).where(WizardSession.session_key == request.session_id)
        )
        session = result.scalar_one_or_none()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        session_state = session.session_state or {}
        # Handle both camelCase (frontend) and snake_case naming
        queue_data = session_state.get('blind_spots_queue') or session_state.get('blindSpotsQueue', {})
        queue = BlindSpotsQueue(**queue_data)

        # Assess completion quality
        quality = assess_completion_quality(queue)

        # Mark remaining slots as skipped
        for slot in queue_data.get('slots', []):
            if slot.get('status') == 'pending':
                slot['status'] = 'skipped'

        # Update session
        session_state['blind_spots_queue'] = queue_data
        session_state['blind_spots_completed'] = True
        session_state['blind_spots_quality'] = quality
        session.session_state = session_state
        await db.commit()

        return {
            'status': 'finished',
            'quality': quality,
            'answered_count': queue.completed_count,
            'skipped_count': queue.skipped_count,
            'total_slots': len(queue.slots),
            'message': QUALITY_MESSAGES.get(quality, '')
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error finishing blind spots: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


def format_blind_spots_for_prompt(answers: List[BlindSpotAnswer]) -> str:
    """Format blind spots answers for the informed hypothesis generation prompt."""
    if not answers:
        return "No blind spots answers provided."

    # Group by category
    by_category = {}
    for ans in answers:
        cat = ans.category
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(ans)

    formatted = []
    for category, items in by_category.items():
        formatted.append(f"\n### {category.upper().replace('_', ' ')}")
        for item in items:
            depth_label = ["", " (follow-up)", " (deep follow-up)"][min(item.depth - 1, 2)]
            formatted.append(f"**Q{depth_label}:** {item.question}")
            formatted.append(f"**A:** {item.answer}\n")

    return "\n".join(formatted)


@router.post("/generate-informed-hypotheses")
async def generate_informed_hypotheses(request: GenerateInformedHypothesesRequest):
    """
    Generate hypothesis, genealogy, and differentiation cards INFORMED by blind spots answers.
    This is called AFTER blind spots questioning to generate targeted cards.
    """
    async def stream_hypothesis_generation():
        try:
            yield f"data: {json.dumps({'type': 'phase', 'phase': 'generating_hypotheses'})}\n\n"

            # Format blind spots context
            blind_spots_context = format_blind_spots_for_prompt(request.blind_spots_answers)

            # Build the prompt
            prompt = INFORMED_HYPOTHESIS_GENERATION_PROMPT.format(
                concept_name=request.concept_name,
                notes=request.notes,
                blind_spots_context=blind_spots_context
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

                # Get final message
                final_message = stream.get_final_message()
                for block in final_message.content:
                    if hasattr(block, 'text'):
                        response_text = block.text
                        break

            # Parse the response
            analysis_data = parse_wizard_response(response_text)

            # Extract cards - support both new posit_cards and legacy hypothesis_cards
            posit_cards = analysis_data.get("posit_cards", [])
            hypothesis_cards = analysis_data.get("hypothesis_cards", [])

            # If LLM returned posit_cards, use those; otherwise fall back to hypothesis_cards
            primary_cards = posit_cards if posit_cards else hypothesis_cards

            genealogy_cards = analysis_data.get("genealogy_cards", [])
            differentiation_cards = analysis_data.get("differentiation_cards", [])
            genealogy_questions = analysis_data.get("genealogy_questions", [])

            # Ensure primary cards have proper status and metadata
            for card in primary_cards:
                card["status"] = "pending"
                card["transformation_history"] = []
                # Add posit type metadata if present
                if card.get("type"):
                    posit_type = card["type"]
                    for pt, metadata in POSIT_TYPE_METADATA.items():
                        if pt.value == posit_type:
                            card["type_label"] = metadata["label"]
                            card["type_color"] = metadata["color"]
                            card["type_dimension"] = metadata["dimension"]
                            break

            for card in genealogy_cards:
                card["status"] = "pending"
                card["transformation_history"] = []

            for card in differentiation_cards:
                card["status"] = "pending"
                card["transformation_history"] = []

            # Return complete response - use posit_cards AND hypothesis_cards for backward compat
            complete_data = {
                'type': 'complete',
                'data': {
                    'status': 'cards_ready',
                    'concept_name': request.concept_name,
                    'stage_title': 'Review Generated Posits',
                    'stage_description': "Based on your blind spots exploration, we've generated these informed posits (preliminary claims). Approve, reject, or transform each card.",
                    'posit_cards': primary_cards,  # New field
                    'hypothesis_cards': primary_cards,  # Backward compat
                    'genealogy_cards': genealogy_cards,
                    'differentiation_cards': differentiation_cards,
                    'genealogy_questions': genealogy_questions,
                    'posit_types': [  # Include type metadata for frontend
                        {
                            "value": pt.value,
                            "label": meta["label"],
                            "dimension": meta["dimension"],
                            "color": meta["color"]
                        }
                        for pt, meta in POSIT_TYPE_METADATA.items()
                    ]
                }
            }
            yield f"data: {json.dumps(complete_data)}\n\n"

        except Exception as e:
            logger.error(f"Error generating informed hypotheses: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_hypothesis_generation(),
        media_type="text/event-stream"
    )


# =============================================================================
# DYNAMIC ANSWER TYPOLOGY SYSTEM
# =============================================================================
# Instead of fixed categories (assertive/exploratory/qualified/provocative),
# we curate 4 types from a bank of 16+ based on the specific question context.

ANSWER_TYPOLOGY_BANK = {
    # Epistemic Stances
    "assertive": {
        "label": "ASSERTIVE",
        "description": "A confident, definitive claim. 'I believe X because Y.'",
        "best_for": ["definitional questions", "core commitments", "where user has clarity"]
    },
    "exploratory": {
        "label": "EXPLORATORY",
        "description": "Open questioning stance. 'I'm uncertain but drawn to...'",
        "best_for": ["new territory", "genuine uncertainty", "early-stage thinking"]
    },
    "qualified": {
        "label": "QUALIFIED",
        "description": "Nuanced position with caveats. 'In some contexts X, but in others Y...'",
        "best_for": ["complex tradeoffs", "context-dependent claims", "scope limitations"]
    },
    "provocative": {
        "label": "PROVOCATIVE",
        "description": "Counterintuitive or challenging take. 'Against common intuition...'",
        "best_for": ["paradigm challenges", "contrarian positions", "disrupting assumptions"]
    },

    # Relational Stances
    "synthetic": {
        "label": "SYNTHETIC",
        "description": "Combining or reconciling views. 'Both X and Y are true because...'",
        "best_for": ["apparent contradictions", "multiple valid perspectives", "dialectical tensions"]
    },
    "contrastive": {
        "label": "CONTRASTIVE",
        "description": "Defining by what it's NOT. 'Unlike X, my concept emphasizes...'",
        "best_for": ["differentiation questions", "competitor concepts", "boundary drawing"]
    },
    "concessive": {
        "label": "CONCESSIVE",
        "description": "Acknowledging valid criticism. 'Critics are right that X, but...'",
        "best_for": ["addressing objections", "steel-manning opponents", "honest limitations"]
    },
    "analogical": {
        "label": "ANALOGICAL",
        "description": "Drawing illuminating parallels. 'This is like X in that...'",
        "best_for": ["abstract concepts", "cross-domain insight", "making unfamiliar familiar"]
    },

    # Methodological Stances
    "empirical": {
        "label": "EMPIRICAL",
        "description": "Evidence-based positioning. 'The data/cases suggest...'",
        "best_for": ["factual disputes", "testable claims", "grounding in observation"]
    },
    "theoretical": {
        "label": "THEORETICAL",
        "description": "Conceptual/logical reasoning. 'The framework implies...'",
        "best_for": ["abstract questions", "logical entailments", "definitional matters"]
    },
    "pragmatic": {
        "label": "PRAGMATIC",
        "description": "Focus on practical consequences. 'What matters is whether...'",
        "best_for": ["action-oriented questions", "policy implications", "real-world stakes"]
    },
    "genealogical": {
        "label": "GENEALOGICAL",
        "description": "Tracing origins and development. 'This emerged from...'",
        "best_for": ["historical questions", "intellectual lineage", "how concepts evolved"]
    },

    # Strategic Stances
    "diagnostic": {
        "label": "DIAGNOSTIC",
        "description": "Identifying the real problem. 'The actual issue here is...'",
        "best_for": ["problem framing", "root cause analysis", "reframing questions"]
    },
    "prescriptive": {
        "label": "PRESCRIPTIVE",
        "description": "Recommending action or approach. 'We should...'",
        "best_for": ["normative questions", "recommendations", "what-to-do queries"]
    },
    "agnostic": {
        "label": "AGNOSTIC",
        "description": "Principled suspension of judgment. 'This may be undecidable...'",
        "best_for": ["genuine unknowables", "where premature closure is risky", "epistemic humility"]
    },
    "reframing": {
        "label": "REFRAMING",
        "description": "Shifting the question itself. 'The better question is...'",
        "best_for": ["poorly posed questions", "false dichotomies", "paradigm shifts"]
    },

    # Wildcards (curator can define custom types)
    "wildcard_1": {
        "label": "CUSTOM",
        "description": "Curator-defined type tailored to this specific question",
        "best_for": ["unusual questions", "domain-specific stances", "emergent categories"]
    },
    "wildcard_2": {
        "label": "CUSTOM",
        "description": "Curator-defined type tailored to this specific question",
        "best_for": ["unusual questions", "domain-specific stances", "emergent categories"]
    }
}

# Curator prompt: selects 4 best types for this question
ANSWER_TYPE_CURATOR_PROMPT = """You are an epistemic curator helping select the most appropriate answer TYPES for a specific question.

## The Question
Concept: {concept_name}
Category: {category}
Question: {question}

## User's Context
{notes_context}

{previous_answers_context}

## Available Answer Types (pick 4)
{typology_descriptions}

## Your Task
Analyze the question and context, then select the 4 answer types that would be MOST USEFUL for this specific question.

Consider:
1. What kind of epistemic move does this question call for?
2. What stances would reveal the user's actual position most clearly?
3. What would be genuinely distinct and helpful (not just variety for variety's sake)?
4. Does the question suggest a particular domain (empirical vs theoretical, historical vs prescriptive)?

You may also define up to 2 CUSTOM types if the standard types don't fit well.

## Output Format
Return valid JSON:
{{
  "selected_types": [
    {{
      "type_key": "assertive|exploratory|...|wildcard_1",
      "label": "ASSERTIVE" or custom label,
      "tailored_description": "How this type applies to THIS question specifically",
      "why_selected": "Why this type is valuable for this question"
    }},
    ... (4 types total)
  ],
  "curation_rationale": "Brief explanation of why these 4 types form a useful set for this question"
}}"""

# Dynamic answer generation prompt (uses curated types)
DYNAMIC_ANSWER_OPTIONS_PROMPT = """You are helping a user articulate their response to a question about their concept.

## Context
Concept: {concept_name}
Category: {category}
Question: {question}

{notes_context}
{previous_answers_context}

## Curated Answer Types for This Question
{curated_types_description}

## Task
Generate 4 answer options, one for each curated type above. Each option should:
1. Be 2-3 sentences long
2. Embody the specified stance/type authentically
3. Be specific to THIS question and THIS concept (not generic)
4. Help the user discover and articulate their actual position

## Mutual Exclusivity
Determine whether these options are mutually exclusive or can be combined.
Default to mutually_exclusive: false unless the options are logically contradictory.

## Output Format
Return valid JSON:
{{
  "options": [
    {{"id": "opt_1", "text": "...", "stance": "{type_1_key}", "label": "{type_1_label}"}},
    {{"id": "opt_2", "text": "...", "stance": "{type_2_key}", "label": "{type_2_label}"}},
    {{"id": "opt_3", "text": "...", "stance": "{type_3_key}", "label": "{type_3_label}"}},
    {{"id": "opt_4", "text": "...", "stance": "{type_4_key}", "label": "{type_4_label}"}}
  ],
  "guidance": "Brief note on how these options differ and what choosing each would signal.",
  "mutually_exclusive": false,
  "exclusivity_reason": "Brief explanation"
}}"""

# Legacy prompt (kept for fallback)
GENERATE_ANSWER_OPTIONS_PROMPT = """You are helping a user articulate their response to a question about their concept's epistemic blind spots.

## Context
Concept: {concept_name}
Category: {category}
Question: {question}

{notes_context}
{previous_answers_context}

## Task
Generate 4 distinct answer options that the user might choose from. Each option should:
1. Be 2-3 sentences long
2. Take a different STANCE toward the question
3. Help the user discover and articulate their actual position

## The 4 Stances
1. **Assertive**: A confident, definitive position. "I believe X because Y."
2. **Exploratory**: An open, questioning stance. "I'm uncertain about X, but I'm drawn to Y..."
3. **Qualified**: A nuanced position with caveats. "In some contexts X, but in others Y..."
4. **Provocative**: A counterintuitive or challenging take. "Against common intuition, I think X..."

## Mutual Exclusivity Analysis
Determine whether these options are MUTUALLY EXCLUSIVE or can be combined:
- **mutually_exclusive: true** = Options represent incompatible positions (e.g., "X is true" vs "X is false")
- **mutually_exclusive: false** = Options can be held together, user might select multiple to give richer context

For blind spots questions, options are often NOT mutually exclusive because:
- User might hold multiple partial views
- User might see merit in several framings
- Selecting multiple gives us richer epistemic context

Default to mutually_exclusive: false unless the options are logically contradictory.

## Output Format
Return valid JSON:
{{
  "options": [
    {{"id": "opt_1", "text": "...", "stance": "assertive"}},
    {{"id": "opt_2", "text": "...", "stance": "exploratory"}},
    {{"id": "opt_3", "text": "...", "stance": "qualified"}},
    {{"id": "opt_4", "text": "...", "stance": "provocative"}}
  ],
  "guidance": "Brief note on how these options differ and what choosing each would signal about the user's position.",
  "mutually_exclusive": false,
  "exclusivity_reason": "Brief explanation of why options can/cannot be combined"
}}

Generate options that are genuinely distinct and would help the user discover which resonates with their actual thinking."""


def _build_typology_descriptions() -> str:
    """Build formatted description of all available answer types for the curator."""
    lines = []
    for key, data in ANSWER_TYPOLOGY_BANK.items():
        if key.startswith("wildcard"):
            continue  # Skip wildcards in the list - curator can use them if needed
        lines.append(f"- **{key}** ({data['label']}): {data['description']}")
        lines.append(f"  Best for: {', '.join(data['best_for'])}")
    lines.append("")
    lines.append("- **wildcard_1/wildcard_2**: Define your own custom type if needed")
    return "\n".join(lines)


async def _curate_answer_types(
    client,
    concept_name: str,
    category: str,
    question: str,
    notes_context: str,
    previous_answers_context: str
) -> List[dict]:
    """
    Step 1: Use an LLM to curate which 4 answer types are most appropriate
    for this specific question.
    """
    typology_descriptions = _build_typology_descriptions()

    curator_prompt = ANSWER_TYPE_CURATOR_PROMPT.format(
        concept_name=concept_name,
        category=category,
        question=question,
        notes_context=notes_context,
        previous_answers_context=previous_answers_context,
        typology_descriptions=typology_descriptions
    )

    # Use Haiku for fast curation (it's just selecting types, not generating content)
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[{"role": "user", "content": curator_prompt}]
    )

    response_text = response.content[0].text.strip()

    # Parse curator response
    import re
    json_match = re.search(r'\{[\s\S]*\}', response_text)
    if json_match:
        parsed = json.loads(json_match.group())
        return parsed.get('selected_types', [])

    # Fallback to default types if parsing fails
    return [
        {"type_key": "assertive", "label": "ASSERTIVE", "tailored_description": "A confident position"},
        {"type_key": "exploratory", "label": "EXPLORATORY", "tailored_description": "An open exploration"},
        {"type_key": "qualified", "label": "QUALIFIED", "tailored_description": "A nuanced stance"},
        {"type_key": "provocative", "label": "PROVOCATIVE", "tailored_description": "A challenging take"}
    ]


async def _generate_options_for_curated_types(
    client,
    concept_name: str,
    category: str,
    question: str,
    notes_context: str,
    previous_answers_context: str,
    curated_types: List[dict]
) -> dict:
    """
    Step 2: Generate actual answer options using the curated types.
    """
    # Build description of curated types for the generator
    curated_types_description = "\n".join([
        f"{i+1}. **{t.get('label', t.get('type_key', 'TYPE').upper())}** ({t.get('type_key', 'unknown')})\n   {t.get('tailored_description', t.get('description', 'No description'))}"
        for i, t in enumerate(curated_types[:4])
    ])

    # Build placeholder values for the prompt
    type_keys = [t.get('type_key', f'type_{i}') for i, t in enumerate(curated_types[:4])]
    type_labels = [t.get('label', t.get('type_key', 'TYPE').upper()) for t in curated_types[:4]]

    # Pad if fewer than 4 types
    while len(type_keys) < 4:
        type_keys.append("fallback")
        type_labels.append("FALLBACK")

    generation_prompt = DYNAMIC_ANSWER_OPTIONS_PROMPT.format(
        concept_name=concept_name,
        category=category,
        question=question,
        notes_context=notes_context,
        previous_answers_context=previous_answers_context,
        curated_types_description=curated_types_description,
        type_1_key=type_keys[0], type_1_label=type_labels[0],
        type_2_key=type_keys[1], type_2_label=type_labels[1],
        type_3_key=type_keys[2], type_3_label=type_labels[2],
        type_4_key=type_keys[3], type_4_label=type_labels[3]
    )

    # Use Sonnet for the actual content generation
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1500,
        messages=[{"role": "user", "content": generation_prompt}]
    )

    response_text = response.content[0].text.strip()

    # Parse response
    import re
    json_match = re.search(r'\{[\s\S]*\}', response_text)
    if json_match:
        return json.loads(json_match.group())

    return None


@router.post("/generate-answer-options")
async def generate_answer_options(request: GenerateAnswerOptionsRequest):
    """
    Generate multiple choice answer options for a blind spot question.

    Two-step process implementing prn_dynamic_typology_curation:
    1. Curator LLM selects 4 best answer types from bank of 16+ for THIS question
    2. Generator LLM creates answers for those dynamically-selected types

    This avoids the straightjacket of fixed categories (assertive/exploratory/etc.)
    """
    try:
        client = get_claude_client()

        # Build context sections
        notes_context = ""
        if request.notes_context:
            notes_context = f"## User's Notes (context)\n{request.notes_context[:3000]}..."

        previous_answers_context = ""
        if request.previous_answers:
            answers_text = "\n".join([
                f"- {a.get('question', 'Q')}: {a.get('answer', 'A')[:200]}"
                for a in request.previous_answers[-5:]  # Last 5 answers for richer context
            ])
            previous_answers_context = f"## Previous Answers\n{answers_text}"

        # Step 1: Curate answer types for this question
        logger.info(f"[generate-answer-options] Step 1: Curating types for question in category '{request.category}'")
        curated_types = await _curate_answer_types(
            client,
            request.concept_name,
            request.category,
            request.question,
            notes_context,
            previous_answers_context
        )
        logger.info(f"[generate-answer-options] Curated types: {[t.get('label') for t in curated_types]}")

        # Step 2: Generate answers for curated types
        logger.info(f"[generate-answer-options] Step 2: Generating answers for curated types")
        generated = await _generate_options_for_curated_types(
            client,
            request.concept_name,
            request.category,
            request.question,
            notes_context,
            previous_answers_context,
            curated_types
        )

        if generated:
            # Ensure each option has a label (from curated types if not in response)
            options = generated.get('options', [])
            for i, opt in enumerate(options):
                if 'label' not in opt and i < len(curated_types):
                    opt['label'] = curated_types[i].get('label', opt.get('stance', 'TYPE').upper())

            return GenerateAnswerOptionsResponse(
                options=[AnswerOption(**opt) for opt in options],
                guidance=generated.get('guidance', 'Choose the option that best resonates with your thinking.'),
                mutually_exclusive=generated.get('mutually_exclusive', False),
                exclusivity_reason=generated.get('exclusivity_reason', None)
            )

        # Fallback if generation fails
        logger.warning("[generate-answer-options] Generation failed, using fallback")
        return GenerateAnswerOptionsResponse(
            options=[
                AnswerOption(id="opt_1", text="I have a clear position on this that I can articulate.", stance="assertive", label="ASSERTIVE"),
                AnswerOption(id="opt_2", text="I'm still exploring this area and don't have a fixed view yet.", stance="exploratory", label="EXPLORATORY"),
                AnswerOption(id="opt_3", text="My position depends on the specific context or framing.", stance="qualified", label="QUALIFIED"),
                AnswerOption(id="opt_4", text="I want to challenge the premise of this question.", stance="provocative", label="PROVOCATIVE")
            ],
            guidance="Select the stance that feels closest to your position, then refine the text.",
            mutually_exclusive=False,
            exclusivity_reason="These stances can be combined for a richer response."
        )

    except Exception as e:
        logger.error(f"Error generating answer options: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ===== CONCEPT EXPORT FOR INTELLIGENCE ENGINE =====

class ConceptExportRequest(BaseModel):
    """Request to export a concept for Intelligence Engine import."""
    session_key: str
    include_blind_spots: bool = True
    include_posits: bool = True
    include_external_relations: bool = True
    ie_target_container: str = "THEORY"  # THEORY, FOUNDATIONS, or SPECULATION


class DimensionalStatement(BaseModel):
    """Canonical statement for one dimension."""
    dimension: str
    canonical_statement: str
    key_insights: List[str] = []
    confidence: float = 0.8


class ConceptExportResponse(BaseModel):
    """Exported concept in IE-compatible format."""
    # Core identity
    term: str
    definition: str
    author: str = "User"
    created_at: str

    # 12-dimensional analysis
    dimensional_statements: List[DimensionalStatement]

    # Posits (approved hypotheses)
    posits: List[dict] = []

    # Blind spots and user responses
    blind_spots_explored: List[dict] = []

    # External concept relationships
    external_relations: List[dict] = []

    # IE metadata
    ie_target_container: str
    completeness_score: float
    dimensions_covered: List[str]
    export_ready: bool
    export_notes: str = ""


def generate_canonical_statement_for_dimension(
    concept_name: str,
    dimension: str,
    dimensional_data: dict
) -> str:
    """Generate a canonical one-sentence statement for a dimension based on collected data."""
    # This would ideally use the data to synthesize a statement
    # For now, return a placeholder that indicates synthesis is needed

    dimension_templates = {
        "quinean": f"In the web of belief, {concept_name} connects to [inferences] and contradicts [contradictions].",
        "sellarsian": f"{concept_name} treats [assumptions] as given, which actually requires justification.",
        "brandomian": f"Adopting {concept_name} commits you to [commitments] and licenses [inferences].",
        "deleuzian": f"{concept_name} enables [transformations] by [mechanism].",
        "bachelardian": f"{concept_name} marks an epistemological break from [predecessor] by [nature of break].",
        "canguilhem": f"{concept_name} establishes [norm] as normal, treating [alternative] as pathological.",
        "hacking": f"{concept_name} makes [phenomena] visible through [style of reasoning].",
        "blumenberg": f"{concept_name} operates through the metaphor of [metaphor], which reveals [insight] and conceals [hidden].",
        "carey": f"{concept_name} is bootstrapped from [simpler concepts] through [mechanism].",
        "kuhnian": f"{concept_name} belongs to the [paradigm] paradigm; anomalies include [anomalies].",
        "pragmatist": f"Using {concept_name} enables [actions] and opens conversations about [topics].",
        "foucauldian": f"{concept_name} naturalizes [power relations] and makes [phenomena] governable."
    }

    return dimension_templates.get(dimension, f"{concept_name} from the {dimension} perspective.")


@router.get("/export/{session_key}")
async def export_concept_for_ie(
    session_key: str,
    include_blind_spots: bool = True,
    include_posits: bool = True,
    include_external_relations: bool = True,
    ie_target_container: str = "THEORY"
):
    """
    Export a concept in a format suitable for Intelligence Engine import.

    The export includes:
    - Core concept identity (term, definition)
    - Canonical statements for each of the 12 dimensions
    - Approved posits
    - Blind spots exploration results
    - External concept relationships
    - Completeness metadata

    This enables seamless transfer from Concept Wizard to IE's THEORY container.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Fetch session data
        cursor.execute("""
            SELECT * FROM wizard_sessions WHERE session_key = %s
        """, (session_key,))
        session = cursor.fetchone()

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        data = session.get('data', {})
        concept_name = data.get('concept_name', 'Unknown Concept')

        # Build dimensional statements from available data
        dimensional_statements = []
        dimensions_covered = []

        # Check what dimensional data we have
        dimensional_keys = [
            "quinean", "sellarsian", "brandomian", "deleuzian",
            "bachelardian", "canguilhem", "hacking", "blumenberg",
            "carey", "kuhnian", "pragmatist", "foucauldian"
        ]

        # Extract dimensional data from session
        for dim in dimensional_keys:
            dim_data = data.get(f'{dim}_analysis', {})
            if dim_data or data.get('deep_commitments', {}).get(dim):
                dimensions_covered.append(dim)

                # Get key insights from posits of this dimension type
                dim_posits = [
                    p for p in data.get('posits', [])
                    if p.get('type') == dim or p.get('dimension') == dim
                ]
                key_insights = [p.get('statement', '') for p in dim_posits[:3]]

                dimensional_statements.append(DimensionalStatement(
                    dimension=dim,
                    canonical_statement=generate_canonical_statement_for_dimension(
                        concept_name, dim, dim_data
                    ),
                    key_insights=key_insights,
                    confidence=0.7 if dim_data else 0.5
                ))

        # Extract posits if requested
        posits = []
        if include_posits:
            raw_posits = data.get('posits', []) or data.get('hypothesis_cards', [])
            for p in raw_posits:
                if p.get('approved', True):  # Include approved or default to include
                    posits.append({
                        "statement": p.get('statement', p.get('text', '')),
                        "type": p.get('type', 'unknown'),
                        "dimension": p.get('dimension', p.get('type', 'unknown')),
                        "confidence": p.get('confidence', 0.7),
                        "source": "wizard_detection"
                    })

        # Extract blind spots if requested
        blind_spots_explored = []
        if include_blind_spots:
            bs_answers = data.get('blind_spots_answers', [])
            for bs in bs_answers:
                blind_spots_explored.append({
                    "category": bs.get('category', 'unknown'),
                    "question": bs.get('question', ''),
                    "answer": bs.get('answer', ''),
                    "depth": bs.get('depth', 1)
                })

        # Extract external relations if requested
        external_relations = []
        if include_external_relations:
            # Check for external concept relationships in session
            relations = data.get('external_relations', [])
            for rel in relations:
                external_relations.append({
                    "target_concept": rel.get('target', ''),
                    "target_author": rel.get('author', ''),
                    "relationship_type": rel.get('type', 'relates_to'),
                    "description": rel.get('description', '')
                })

        # Calculate completeness score
        total_dimensions = len(dimensional_keys)
        covered_dimensions = len(dimensions_covered)
        posit_coverage = min(1.0, len(posits) / 12.0)  # Aim for at least 12 posits
        blind_spots_coverage = min(1.0, len(blind_spots_explored) / 8.0)  # Aim for 8+ answers

        completeness_score = (
            (covered_dimensions / total_dimensions) * 0.5 +
            posit_coverage * 0.3 +
            blind_spots_coverage * 0.2
        )

        export_ready = completeness_score >= 0.6 and covered_dimensions >= 6

        # Build export notes
        export_notes_parts = []
        if covered_dimensions < 6:
            export_notes_parts.append(f"Only {covered_dimensions}/12 dimensions covered. Consider deeper analysis.")
        if len(posits) < 9:
            export_notes_parts.append(f"Only {len(posits)} posits detected. May need more hypothesis exploration.")
        if len(blind_spots_explored) < 5:
            export_notes_parts.append(f"Only {len(blind_spots_explored)} blind spots explored. Consider more epistemic grounding.")

        cursor.close()
        conn.close()

        return ConceptExportResponse(
            term=concept_name,
            definition=data.get('definition', data.get('concept_definition', '')),
            author=data.get('author', 'User'),
            created_at=str(session.get('created_at', '')),
            dimensional_statements=dimensional_statements,
            posits=posits,
            blind_spots_explored=blind_spots_explored,
            external_relations=external_relations,
            ie_target_container=ie_target_container,
            completeness_score=round(completeness_score, 2),
            dimensions_covered=dimensions_covered,
            export_ready=export_ready,
            export_notes=" | ".join(export_notes_parts) if export_notes_parts else "Ready for IE import."
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting concept: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# DYNAMIC QUESTION GENERATION SYSTEM
# =============================================================================
# This system implements rolling question generation for sections 6-11:
# - Questions are generated one at a time (or in small batches)
# - Pre-fetches 1-2 questions ahead while user answers current question
# - User answers feed into subsequent question generation
# - Uses Sonnet 4.5 for fast (~3-5s) generation
# =============================================================================

# Section configurations for dynamic generation
DYNAMIC_SECTION_CONFIG = {
    'stage2': {
        'label': 'Differentiation',
        'target_questions': 5,
        'max_questions': 8,
        'min_questions': 3,
        'focus': 'differentiating concept from adjacent concepts and surfacing presuppositions'
    },
    'stage3': {
        'label': 'Methodology',
        'target_questions': 5,
        'max_questions': 7,
        'min_questions': 3,
        'focus': 'grounding the concept with paradigmatic cases, recognition markers, and falsification conditions'
    },
    'implications': {
        'label': 'Implications',
        'target_questions': 4,
        'max_questions': 6,
        'min_questions': 2,
        'focus': 'exploring what follows from the concept and what it enables or forecloses'
    },
    'genealogy': {
        'label': 'Genealogy',
        'target_questions': 4,
        'max_questions': 6,
        'min_questions': 2,
        'focus': 'tracing intellectual influences, ancestors, and debates the concept engages with'
    },
    'philosophy_p1': {
        'label': 'Philosophy P1',
        'target_questions': 12,
        'max_questions': 15,
        'min_questions': 9,
        'focus': 'probing the 12 philosophical dimensions (Quinean, Sellarsian, Brandomian, etc.)'
    },
    'philosophy_p2': {
        'label': 'Philosophy P2',
        'target_questions': 6,
        'max_questions': 9,
        'min_questions': 4,
        'focus': 'targeted follow-up questions based on P1 answers'
    },
    'philosophy_p3': {
        'label': 'Philosophy P3',
        'target_questions': 4,
        'max_questions': 6,
        'min_questions': 3,
        'focus': 'synthesis and verification of philosophical commitments'
    }
}


class DynamicSectionSlot(BaseModel):
    """A single question slot in a dynamic section queue."""
    slot_id: str
    status: str = 'pending'  # pending, answered, skipped
    question: Optional[Dict[str, Any]] = None
    answer: Optional[Dict[str, Any]] = None
    generated_at: Optional[str] = None
    answered_at: Optional[str] = None


class DynamicSectionQueue(BaseModel):
    """Queue state for a dynamic section."""
    section_id: str
    slots: List[DynamicSectionSlot] = []
    current_index: int = 0
    target_questions: int = 5
    max_questions: int = 8
    completed_count: int = 0
    skipped_count: int = 0
    generation_context: Optional[Dict[str, Any]] = None


class InitDynamicSectionRequest(BaseModel):
    """Request to initialize a dynamic section."""
    session_id: str
    section_id: str  # stage2, stage3, implications, genealogy, philosophy_p1, philosophy_p2, philosophy_p3
    concept_name: str
    notes_summary: Optional[str] = None
    # Context from previous sections
    stage1_answers: Optional[List[Dict[str, Any]]] = None
    stage2_answers: Optional[List[Dict[str, Any]]] = None
    stage3_answers: Optional[List[Dict[str, Any]]] = None
    interim_analysis: Optional[Dict[str, Any]] = None
    genealogy: Optional[List[Dict[str, Any]]] = None
    blind_spots_answers: Optional[List[Dict[str, Any]]] = None
    hypothesis_cards: Optional[List[Dict[str, Any]]] = None
    philosophy_p1_answers: Optional[Dict[str, Any]] = None
    philosophy_p2_answers: Optional[Dict[str, Any]] = None


class SubmitDynamicAnswerRequest(BaseModel):
    """Request to submit an answer to a dynamic section question."""
    session_id: str
    section_id: str
    slot_id: str
    answer: Dict[str, Any]  # {selected: str, comment: str, custom_response?: str}


class GenerateNextQuestionRequest(BaseModel):
    """Request to pre-generate the next question for a section."""
    session_id: str
    section_id: str
    # Current accumulated answers in this section
    section_answers: List[Dict[str, Any]]
    # Full context
    concept_name: str
    notes_summary: Optional[str] = None
    stage1_answers: Optional[List[Dict[str, Any]]] = None
    stage2_answers: Optional[List[Dict[str, Any]]] = None
    stage3_answers: Optional[List[Dict[str, Any]]] = None
    genealogy: Optional[List[Dict[str, Any]]] = None
    philosophy_p1_answers: Optional[Dict[str, Any]] = None
    philosophy_p2_answers: Optional[Dict[str, Any]] = None


# =============================================================================
# PROMPTS FOR SINGLE-QUESTION DYNAMIC GENERATION
# =============================================================================

DYNAMIC_STAGE2_QUESTION_PROMPT = """You are Claude generating a SINGLE differentiation question for the concept "{concept_name}".

## ACCUMULATED CONTEXT:
Notes Summary: {notes_summary}
Interim Analysis: {interim_analysis}
Adjacent Concepts: {adjacent_concepts}
Blind Spots Explored: {blind_spots_summary}

## QUESTIONS ALREADY ASKED IN THIS SECTION:
{previous_questions_summary}

## ANSWERS SO FAR IN THIS SECTION:
{section_answers_summary}

## YOUR TASK:
Generate ONE NEW differentiation question that:
1. Is DIFFERENT from questions already asked (see list above)
2. BUILDS ON the answers already given (see answers above)
3. Addresses one of: presuppositions, paradigm positioning, ambiguities, anticipated misreadings, or adjacent concept distinctions
4. Uses the accumulated context to make it SPECIFIC to this concept

If {questions_asked} questions have been asked and answers are converging well, you may set "section_complete": true.

Return JSON:
{{
  "question": {{
    "id": "stage2_q{next_question_num}",
    "text": "The specific question text referencing their prior answers...",
    "type": "multiple_choice",
    "options": [
      {{"value": "opt_a", "label": "Option A", "description": "What this means...", "implications": "Choosing this implies..."}},
      {{"value": "opt_b", "label": "Option B", "description": "What this means...", "implications": "Choosing this implies..."}},
      {{"value": "opt_c", "label": "Option C", "description": "What this means...", "implications": "Choosing this implies..."}}
    ],
    "rationale": "Why this question matters given their prior answers",
    "allow_custom_response": true,
    "allow_comment": true
  }},
  "section_complete": false,
  "completion_reason": null
}}"""


DYNAMIC_STAGE3_QUESTION_PROMPT = """You are Claude generating a SINGLE methodology/grounding question for the concept "{concept_name}".

## ACCUMULATED CONTEXT:
Notes Summary: {notes_summary}
Differentiation Answers (Stage 2): {stage2_summary}
Implications Preview: {implications_preview}

## QUESTIONS ALREADY ASKED IN THIS SECTION:
{previous_questions_summary}

## ANSWERS SO FAR IN THIS SECTION:
{section_answers_summary}

## YOUR TASK:
Generate ONE NEW methodology question that:
1. Is DIFFERENT from questions already asked
2. BUILDS ON the answers already given
3. Addresses one of: paradigmatic cases, implicit domains, recognition markers, core claims, or falsification conditions
4. Makes it SPECIFIC to this concept and their prior differentiation choices

CRITICAL: You MUST generate MULTIPLE-CHOICE questions with PRE-POPULATED OPTIONS derived from context.
DO NOT generate open-ended questions requiring free-text typing.

For paradigmatic cases: Generate 3-4 specific candidate cases inferred from the notes and context.
For recognition markers: Generate 4-5 specific linguistic/structural patterns inferred from the concept.
For core claims: Generate 3-4 specific claims the concept makes, derived from context.
For falsification conditions: Generate 3-4 specific conditions that would disprove the concept.
For implicit domains: Generate 3-4 specific domains where the concept could apply.

Each option should be DETAILED and SPECIFIC to this concept - not generic placeholders.
The user should be able to select the best-fitting option without typing anything.
Always include allow_custom_response: true so user CAN type if none fit.

Return JSON:
{{
  "question": {{
    "id": "stage3_q{next_question_num}",
    "text": "The specific question...",
    "type": "multiple_choice",
    "options": [
      {{
        "value": "opt_a",
        "label": "Short descriptive label",
        "description": "Detailed 2-3 sentence description of this specific answer derived from the concept context"
      }},
      {{
        "value": "opt_b",
        "label": "Another specific option",
        "description": "Detailed description showing you understand the concept..."
      }},
      {{
        "value": "opt_c",
        "label": "Third distinct option",
        "description": "Another detailed, context-specific answer..."
      }}
    ],
    "allow_multiple": false,  // true for recognition markers
    "allow_custom_response": true,
    "allow_comment": true,
    "rationale": "Why this matters..."
  }},
  "section_complete": false,
  "completion_reason": null
}}"""


DYNAMIC_PHILOSOPHY_QUESTION_PROMPT = """You are Claude generating a SINGLE philosophical dimension question for the concept "{concept_name}".

## THE 12 PHILOSOPHICAL DIMENSIONS:
1. QUINEAN (Inferential Web) - What follows logically? What contradicts?
2. SELLARSIAN (Givenness) - What's treated as self-evident?
3. BRANDOMIAN (Commitments) - What must you accept if you adopt this?
4. DELEUZIAN (Problems & Becomings) - What transformations enabled/foreclosed?
5. BACHELARDIAN (Rupture) - What framework is being replaced?
6. CANGUILHEM (Normative Stakes) - Whose interests served?
7. DAVIDSON (Reasoning Style) - What made visible/obscured?
8. BLUMENBERG (Metaphorology) - What's the root metaphor?
9. CAREY (Bootstrapping) - What simpler concepts is this built from?
10. KUHNIAN (Paradigm Structure) - What paradigm? What anomalies?
11. PRAGMATIST (Performative) - What can you DO with this concept?
12. FOUCAULDIAN (Power-Knowledge) - What power relations naturalized?

## ACCUMULATED CONTEXT:
Notes Summary: {notes_summary}
Genealogy: {genealogy_summary}
Stage 1-3 Synthesis: {stages_summary}

## DIMENSIONS ALREADY COVERED:
{dimensions_covered}

## QUESTIONS ALREADY ASKED:
{previous_questions_summary}

## ANSWERS SO FAR:
{section_answers_summary}

## YOUR TASK:
Generate ONE NEW philosophical dimension question that:
1. Covers a dimension NOT YET covered (see list above)
2. Is SPECIFIC to this concept using accumulated context
3. Has 3-5 distinct options representing real philosophical positions
4. Builds on their prior answers where relevant

Return JSON:
{{
  "question": {{
    "id": "phil_q{next_question_num}",
    "dimension": "quinean",  // the dimension being probed
    "text": "If {concept_name} is valid, which of these claims would also follow?",
    "options": [
      {{"value": "opt_a", "label": "Position A", "description": "Why this follows..."}},
      {{"value": "opt_b", "label": "Position B", "description": "Why this follows..."}},
      {{"value": "opt_c", "label": "Position C", "description": "Why this follows..."}}
    ],
    "rationale": "Understanding what follows helps clarify...",
    "allow_multiple": false,
    "allow_comment": true
  }},
  "section_complete": false,
  "completion_reason": null
}}"""


# =============================================================================
# HELPER FUNCTIONS FOR DYNAMIC GENERATION
# =============================================================================

def _build_section_answers_summary(answers: List[Dict[str, Any]]) -> str:
    """Build a summary of answers given in this section."""
    if not answers:
        return "(No answers yet)"

    lines = []
    for i, ans in enumerate(answers):
        q_text = ans.get('question_text', ans.get('question', 'Unknown question'))
        selected = ans.get('selected', ans.get('answer', '(no selection)'))
        comment = ans.get('comment', '')
        lines.append(f"Q{i+1}: {q_text}")
        lines.append(f"A: {selected}")
        if comment:
            lines.append(f"Comment: {comment}")
        lines.append("")
    return "\n".join(lines)


def _build_previous_questions_summary(questions: List[Dict[str, Any]]) -> str:
    """Build a summary of questions already asked."""
    if not questions:
        return "(No questions asked yet)"

    lines = []
    for i, q in enumerate(questions):
        q_text = q.get('text', q.get('question', 'Unknown'))
        q_type = q.get('type', 'unknown')
        lines.append(f"{i+1}. [{q_type}] {q_text}")
    return "\n".join(lines)


def _get_dimensions_covered(answers: Dict[str, Any]) -> List[str]:
    """Extract which philosophical dimensions have been covered."""
    dimensions = []
    for q_id, ans in answers.items():
        if 'dimension' in ans:
            dimensions.append(ans['dimension'])
    return list(set(dimensions))


async def _generate_single_question(
    client,
    section_id: str,
    concept_name: str,
    context: Dict[str, Any],
    section_answers: List[Dict[str, Any]],
    previous_questions: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Generate a single question for a dynamic section.
    Uses Sonnet 4.5 for fast (~3-5s) generation.
    """
    questions_asked = len(previous_questions)
    next_question_num = questions_asked + 1

    # Build context strings
    section_answers_summary = _build_section_answers_summary(section_answers)
    previous_questions_summary = _build_previous_questions_summary(previous_questions)

    # Select prompt based on section
    if section_id == 'stage2':
        prompt = DYNAMIC_STAGE2_QUESTION_PROMPT.format(
            concept_name=concept_name,
            notes_summary=context.get('notes_summary', '(No notes)'),
            interim_analysis=json.dumps(context.get('interim_analysis', {}), indent=2)[:2000],
            adjacent_concepts=json.dumps(context.get('adjacent_concepts', []))[:500],
            blind_spots_summary=json.dumps(context.get('blind_spots_answers', []))[:1500],
            previous_questions_summary=previous_questions_summary,
            section_answers_summary=section_answers_summary,
            questions_asked=questions_asked,
            next_question_num=next_question_num
        )
    elif section_id == 'stage3':
        prompt = DYNAMIC_STAGE3_QUESTION_PROMPT.format(
            concept_name=concept_name,
            notes_summary=context.get('notes_summary', '(No notes)'),
            stage2_summary=json.dumps(context.get('stage2_answers', []))[:2000],
            implications_preview=context.get('implications_preview', '(No preview)'),
            previous_questions_summary=previous_questions_summary,
            section_answers_summary=section_answers_summary,
            next_question_num=next_question_num
        )
    elif section_id in ['philosophy_p1', 'philosophy_p2', 'philosophy_p3']:
        dimensions_covered = _get_dimensions_covered(dict(enumerate(section_answers)))
        stages_summary = f"""
Stage 1: {json.dumps(context.get('stage1_answers', []))[:800]}
Stage 2: {json.dumps(context.get('stage2_answers', []))[:800]}
Stage 3: {json.dumps(context.get('stage3_answers', []))[:800]}
"""
        prompt = DYNAMIC_PHILOSOPHY_QUESTION_PROMPT.format(
            concept_name=concept_name,
            notes_summary=context.get('notes_summary', '(No notes)'),
            genealogy_summary=json.dumps(context.get('genealogy', []))[:1000],
            stages_summary=stages_summary,
            dimensions_covered=", ".join(dimensions_covered) if dimensions_covered else "(None yet)",
            previous_questions_summary=previous_questions_summary,
            section_answers_summary=section_answers_summary,
            next_question_num=next_question_num
        )
    else:
        # Generic fallback
        prompt = f"""Generate a single question for section '{section_id}' about concept '{concept_name}'.
Previous questions: {previous_questions_summary}
Previous answers: {section_answers_summary}
Return JSON with 'question' and 'section_complete' fields."""

    # Use Sonnet 4.5 for speed
    response = client.messages.create(
        model=SONNET_MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = response.content[0].text.strip()

    # Parse JSON from response
    json_start = response_text.find('{')
    json_end = response_text.rfind('}') + 1
    if json_start >= 0 and json_end > json_start:
        return json.loads(response_text[json_start:json_end])

    raise ValueError(f"Failed to parse question generation response: {response_text[:200]}")


# =============================================================================
# DYNAMIC SECTION ENDPOINTS
# =============================================================================

@router.post("/init-dynamic-section")
async def init_dynamic_section(request: InitDynamicSectionRequest, db: AsyncSession = Depends(get_db)):
    """
    Initialize a dynamic section with the first 2 questions.
    This allows immediate display while more questions are pre-generated.
    """
    async def stream_init():
        try:
            section_id = request.section_id
            config = DYNAMIC_SECTION_CONFIG.get(section_id)

            if not config:
                yield f"data: {json.dumps({'type': 'error', 'error': f'Unknown section: {section_id}'})}\n\n"
                yield "data: [DONE]\n\n"
                return

            yield f"data: {json.dumps({'type': 'phase', 'phase': 'initializing_section', 'section': config['label']})}\n\n"

            client = get_claude_client()

            # Build context for question generation
            context = {
                'notes_summary': request.notes_summary,
                'stage1_answers': request.stage1_answers,
                'stage2_answers': request.stage2_answers,
                'stage3_answers': request.stage3_answers,
                'interim_analysis': request.interim_analysis,
                'genealogy': request.genealogy,
                'blind_spots_answers': request.blind_spots_answers,
                'hypothesis_cards': request.hypothesis_cards,
                'philosophy_p1_answers': request.philosophy_p1_answers,
                'philosophy_p2_answers': request.philosophy_p2_answers
            }

            # Generate first 2 questions
            initial_questions = []
            for i in range(2):
                yield f"data: {json.dumps({'type': 'status', 'message': f'Generating question {i+1}...'})}\n\n"

                try:
                    result = await _generate_single_question(
                        client=client,
                        section_id=section_id,
                        concept_name=request.concept_name,
                        context=context,
                        section_answers=[],  # No answers yet for initial questions
                        previous_questions=initial_questions
                    )

                    question = result.get('question')
                    if question:
                        initial_questions.append(question)
                        yield f"data: {json.dumps({'type': 'question_generated', 'index': i, 'question': question})}\n\n"

                    if result.get('section_complete'):
                        break

                except Exception as e:
                    logger.error(f"Error generating initial question {i+1}: {e}")
                    # Continue with fewer questions

            if not initial_questions:
                yield f"data: {json.dumps({'type': 'error', 'error': 'Failed to generate initial questions'})}\n\n"
                yield "data: [DONE]\n\n"
                return

            # Build queue structure
            slots = []
            for i, q in enumerate(initial_questions):
                slots.append({
                    'slot_id': f"{section_id}_slot_{i:02d}",
                    'status': 'pending',
                    'question': q,
                    'answer': None,
                    'generated_at': datetime.now().isoformat()
                })

            queue = {
                'section_id': section_id,
                'slots': slots,
                'current_index': 0,
                'target_questions': config['target_questions'],
                'max_questions': config['max_questions'],
                'completed_count': 0,
                'skipped_count': 0,
                'generation_context': context
            }

            # Save to database
            try:
                print(f"[init-dynamic-section] Saving queue for session_id={request.session_id}, section={section_id}", flush=True)
                async with AsyncSessionLocal() as db_session:
                    result = await db_session.execute(
                        select(WizardSession).where(WizardSession.session_key == request.session_id)
                    )
                    session = result.scalar_one_or_none()
                    if session:
                        print(f"[init-dynamic-section] Found session id={session.id}, current stage={session.stage}", flush=True)

                        # Get a fresh copy of session_state and add queue
                        current_state = dict(session.session_state or {})
                        queue_key = f'dynamic_queue_{section_id}'
                        current_state[queue_key] = queue

                        print(f"[init-dynamic-section] State keys before update: {list(current_state.keys())}", flush=True)

                        # Use explicit UPDATE statement instead of ORM update
                        from sqlalchemy import update
                        await db_session.execute(
                            update(WizardSession)
                            .where(WizardSession.id == session.id)
                            .values(session_state=current_state)
                        )
                        await db_session.commit()

                        # Verify save
                        verify_result = await db_session.execute(
                            select(WizardSession.session_state).where(WizardSession.id == session.id)
                        )
                        verify_state = verify_result.scalar_one()
                        print(f"[init-dynamic-section] VERIFIED - queue key exists: {queue_key in (verify_state or {})}", flush=True)
                        print(f"[init-dynamic-section] COMMITTED queue for {section_id} with {len(slots)} questions", flush=True)
                    else:
                        print(f"[init-dynamic-section] SESSION NOT FOUND for session_id={request.session_id}", flush=True)
            except Exception as e:
                print(f"[init-dynamic-section] ERROR saving queue: {e}", flush=True)
                import traceback
                traceback.print_exc()

            yield f"data: {json.dumps({'type': 'init_complete', 'queue': queue})}\n\n"
            yield "data: [DONE]\n\n"

        except Exception as e:
            logger.error(f"Error initializing dynamic section: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_init(),
        media_type="text/event-stream"
    )


@router.post("/submit-dynamic-answer")
async def submit_dynamic_answer(request: SubmitDynamicAnswerRequest, db: AsyncSession = Depends(get_db)):
    """
    Submit an answer to a dynamic section question.
    Updates queue state in database and returns next question info.
    """
    try:
        logger.info(f"[submit-dynamic-answer] session={request.session_id}, section={request.section_id}, slot={request.slot_id}")

        # Load session
        result = await db.execute(
            select(WizardSession).where(WizardSession.session_key == request.session_id)
        )
        session = result.scalar_one_or_none()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        session_state = dict(session.session_state or {})
        queue_key = f'dynamic_queue_{request.section_id}'
        queue = session_state.get(queue_key)

        if not queue:
            raise HTTPException(status_code=404, detail=f"No dynamic queue found for section {request.section_id}")

        # Find the slot and update it
        slot_found = False
        for slot in queue['slots']:
            if slot['slot_id'] == request.slot_id:
                slot['status'] = 'answered'
                slot['answer'] = request.answer
                slot['answered_at'] = datetime.now().isoformat()
                slot_found = True
                break

        if not slot_found:
            raise HTTPException(status_code=404, detail=f"Slot {request.slot_id} not found")

        # Update queue stats
        queue['completed_count'] = sum(1 for s in queue['slots'] if s['status'] == 'answered')
        queue['current_index'] = queue['completed_count']  # Move to next unanswered

        # Determine if section is complete
        config = DYNAMIC_SECTION_CONFIG.get(request.section_id, {})
        target = config.get('target_questions', 5)
        max_q = config.get('max_questions', 8)

        section_complete = (
            queue['completed_count'] >= target or
            queue['current_index'] >= len(queue['slots']) and len(queue['slots']) >= target
        )

        # Check if there are more questions available
        has_next = queue['current_index'] < len(queue['slots'])
        next_question = None
        if has_next:
            next_question = queue['slots'][queue['current_index']]['question']

        # Can generate more?
        can_generate_more = len(queue['slots']) < max_q

        # Save updated queue using explicit UPDATE (more reliable for JSON columns)
        session_state[queue_key] = queue
        from sqlalchemy import update
        await db.execute(
            update(WizardSession)
            .where(WizardSession.id == session.id)
            .values(session_state=session_state)
        )
        await db.commit()

        logger.info(f"[submit-dynamic-answer] Updated queue: completed={queue['completed_count']}, has_next={has_next}, section_complete={section_complete}")

        return {
            'success': True,
            'queue': queue,
            'has_next': has_next,
            'next_question': next_question,
            'section_complete': section_complete,
            'can_generate_more': can_generate_more,
            'completed_count': queue['completed_count'],
            'total_slots': len(queue['slots'])
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting dynamic answer: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-next-question")
async def generate_next_question(request: GenerateNextQuestionRequest, db: AsyncSession = Depends(get_db)):
    """
    Pre-generate the next question for a dynamic section.
    Called in background while user is answering current question.
    """
    try:
        logger.info(f"[generate-next-question] session={request.session_id}, section={request.section_id}")

        # Load session
        result = await db.execute(
            select(WizardSession).where(WizardSession.session_key == request.session_id)
        )
        session = result.scalar_one_or_none()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        session_state = dict(session.session_state or {})
        queue_key = f'dynamic_queue_{request.section_id}'
        queue = session_state.get(queue_key)

        if not queue:
            raise HTTPException(status_code=404, detail=f"No dynamic queue found for section {request.section_id}")

        config = DYNAMIC_SECTION_CONFIG.get(request.section_id, {})
        max_q = config.get('max_questions', 8)

        # Check if we can generate more
        if len(queue['slots']) >= max_q:
            return {
                'success': False,
                'reason': 'max_questions_reached',
                'queue': queue
            }

        # Build context
        context = queue.get('generation_context', {})
        context.update({
            'notes_summary': request.notes_summary,
            'stage1_answers': request.stage1_answers,
            'stage2_answers': request.stage2_answers,
            'stage3_answers': request.stage3_answers,
            'genealogy': request.genealogy,
            'philosophy_p1_answers': request.philosophy_p1_answers,
            'philosophy_p2_answers': request.philosophy_p2_answers
        })

        # Get previous questions from queue
        previous_questions = [s['question'] for s in queue['slots'] if s.get('question')]

        # Generate next question
        client = get_claude_client()
        result = await _generate_single_question(
            client=client,
            section_id=request.section_id,
            concept_name=request.concept_name,
            context=context,
            section_answers=request.section_answers,
            previous_questions=previous_questions
        )

        question = result.get('question')
        section_complete = result.get('section_complete', False)

        if question and not section_complete:
            # Add new slot to queue
            new_slot = {
                'slot_id': f"{request.section_id}_slot_{len(queue['slots']):02d}",
                'status': 'pending',
                'question': question,
                'answer': None,
                'generated_at': datetime.now().isoformat()
            }
            queue['slots'].append(new_slot)

            # Save updated queue using explicit UPDATE (more reliable for JSON columns)
            session_state[queue_key] = queue
            from sqlalchemy import update
            await db.execute(
                update(WizardSession)
                .where(WizardSession.id == session.id)
                .values(session_state=session_state)
            )
            await db.commit()

            logger.info(f"[generate-next-question] Added new question, queue now has {len(queue['slots'])} slots")

            return {
                'success': True,
                'question': question,
                'slot_id': new_slot['slot_id'],
                'section_complete': False,
                'queue': queue
            }
        else:
            return {
                'success': True,
                'question': None,
                'section_complete': True,
                'completion_reason': result.get('completion_reason', 'Questions converged'),
                'queue': queue
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating next question: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dynamic-section-queue/{session_id}/{section_id}")
async def get_dynamic_section_queue(session_id: str, section_id: str, db: AsyncSession = Depends(get_db)):
    """
    Retrieve the current queue state for a dynamic section.
    Used for session restoration and status checks.
    """
    try:
        result = await db.execute(
            select(WizardSession).where(WizardSession.session_key == session_id)
        )
        session = result.scalar_one_or_none()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        session_state = session.session_state or {}
        queue_key = f'dynamic_queue_{section_id}'
        queue = session_state.get(queue_key)

        if not queue:
            return {
                'exists': False,
                'queue': None
            }

        return {
            'exists': True,
            'queue': queue
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting dynamic section queue: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
