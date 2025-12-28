"""
Strategizer Pydantic Schemas

Request and response models for the Strategizer API.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum

from pydantic import BaseModel, Field


# =============================================================================
# ENUMS (mirroring SQLAlchemy enums)
# =============================================================================

class UnitType(str, Enum):
    CONCEPT = "concept"
    DIALECTIC = "dialectic"
    ACTOR = "actor"


class UnitTier(str, Enum):
    UNIVERSAL = "universal"
    DOMAIN = "domain"
    EMERGENT = "emergent"


class UnitStatus(str, Enum):
    DRAFT = "draft"
    TESTED = "tested"
    CANONICAL = "canonical"


class GridTier(str, Enum):
    REQUIRED = "required"
    FLEXIBLE = "flexible"
    WILDCARD = "wildcard"


class DialogueTurnType(str, Enum):
    USER_QUESTION = "user_question"
    SYSTEM_RESPONSE = "system_response"
    SUGGESTION = "suggestion"


# =============================================================================
# PROJECT SCHEMAS
# =============================================================================

class ProjectCreate(BaseModel):
    """Create a new project."""
    name: str = Field(..., min_length=1, max_length=255)
    brief: str = Field(..., min_length=10, description="Project description/brief")


class ProjectUpdate(BaseModel):
    """Update a project."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    brief: Optional[str] = None


class ProjectSummary(BaseModel):
    """Project summary for list view."""
    id: str
    name: str
    brief: str
    domain_name: Optional[str] = None
    unit_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectResponse(BaseModel):
    """Full project response."""
    id: str
    name: str
    brief: str
    created_at: datetime
    updated_at: datetime
    domain: Optional["DomainResponse"] = None
    units: List["UnitResponse"] = []

    class Config:
        from_attributes = True


# =============================================================================
# DOMAIN SCHEMAS
# =============================================================================

class DomainBootstrapRequest(BaseModel):
    """Request to bootstrap a domain from project brief."""
    # No additional fields needed - uses project brief
    pass


class VocabularyMapping(BaseModel):
    """Vocabulary mapping for domain-specific terms."""
    concept: str = "Concept"
    dialectic: str = "Tension"
    actor: str = "Actor"


class SeedConceptContent(BaseModel):
    """Seed concept content."""
    name: str
    definition: str
    why_fundamental: Optional[str] = None


class SeedDialecticContent(BaseModel):
    """Seed dialectic content."""
    name: str  # "Pole A ↔ Pole B" format
    pole_a: str
    pole_b: str
    why_fundamental: Optional[str] = None


class SeedContentResponse(BaseModel):
    """Seed content item."""
    id: str
    content_type: str
    content: Dict[str, Any]
    accepted: Optional[bool] = None

    class Config:
        from_attributes = True


class DomainResponse(BaseModel):
    """Domain response."""
    id: str
    name: str
    core_question: Optional[str] = None
    success_looks_like: Optional[str] = None
    vocabulary: VocabularyMapping
    template_base: Optional[str] = None
    seed_content: List[SeedContentResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True


class DomainBootstrapResponse(BaseModel):
    """Response from domain bootstrapping."""
    domain: DomainResponse
    message: str = "Domain bootstrapped successfully"


class SeedAcceptReject(BaseModel):
    """Accept or reject seed content."""
    seed_ids: List[str]
    accept: bool


# =============================================================================
# UNIT SCHEMAS
# =============================================================================

class ConceptContent(BaseModel):
    """Content for a Concept unit."""
    what_it_enables: List[str] = []
    what_it_forecloses: List[str] = []
    conditions_of_application: List[str] = []


class DialecticPole(BaseModel):
    """A pole in a dialectic."""
    name: str
    description: str


class DialecticContent(BaseModel):
    """Content for a Dialectic unit."""
    pole_a: DialecticPole
    pole_b: DialecticPole
    navigation_strategies: List[str] = []
    when_prioritize_a: Optional[str] = None
    when_prioritize_b: Optional[str] = None


class ActorContent(BaseModel):
    """Content for an Actor unit."""
    actor_type: str = "institution"  # institution, individual, collective, market_force
    interests: List[str] = []
    capabilities: List[str] = []
    constraints: List[str] = []
    likely_responses: Dict[str, str] = {}


class UnitCreate(BaseModel):
    """Create a new unit."""
    unit_type: UnitType
    name: str = Field(..., min_length=1, max_length=255)
    definition: Optional[str] = None
    content: Optional[Dict[str, Any]] = None


class UnitUpdate(BaseModel):
    """Update a unit."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    definition: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    status: Optional[UnitStatus] = None


class UnitResponse(BaseModel):
    """Unit response."""
    id: str
    unit_type: UnitType
    display_type: Optional[str] = None
    tier: UnitTier
    name: str
    definition: Optional[str] = None
    content: Dict[str, Any] = {}
    status: UnitStatus
    version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UnitRefineRequest(BaseModel):
    """Request to refine a unit with LLM assistance."""
    refinement_notes: str = Field(..., min_length=1, description="What to refine")


# =============================================================================
# DIALOGUE SCHEMAS
# =============================================================================

class DialogueAskRequest(BaseModel):
    """Ask a question."""
    question: str = Field(..., min_length=1)
    context: Optional[Dict[str, Any]] = None


class SuggestedAction(BaseModel):
    """An action suggested by the system."""
    action_type: str  # create_concept, create_dialectic, create_actor, refine_unit, ask_followup
    parameters: Dict[str, Any]
    rationale: Optional[str] = None


class DialogueResponse(BaseModel):
    """Response to a dialogue question."""
    response: str
    implications: Optional[str] = None
    suggested_actions: List[SuggestedAction] = []


class DialogueTurnResponse(BaseModel):
    """A dialogue turn."""
    id: str
    turn_type: DialogueTurnType
    content: str
    context: Dict[str, Any] = {}
    actions_proposed: List[Dict[str, Any]] = []
    actions_taken: List[Dict[str, Any]] = []
    created_at: datetime

    class Config:
        from_attributes = True


class DialogueHistoryResponse(BaseModel):
    """Dialogue history for a project."""
    turns: List[DialogueTurnResponse]
    total_count: int


# =============================================================================
# SUGGESTION SCHEMAS
# =============================================================================

class SuggestRequest(BaseModel):
    """Request suggestions for next steps."""
    focus: Optional[str] = None  # Optional focus area


class SuggestionResponse(BaseModel):
    """Suggestions for next steps."""
    suggestions: List[str]
    priority_actions: List[SuggestedAction] = []


# =============================================================================
# GRID SCHEMAS
# =============================================================================

class SlotDefinition(BaseModel):
    """A slot definition within a grid."""
    name: str
    description: str


class GridDefinitionResponse(BaseModel):
    """A grid type definition."""
    grid_type: str
    name: str
    description: str
    slots: List[SlotDefinition]
    tier: str  # "required" or "flexible"
    applicable_to: List[str]


class ApplicableGridsResponse(BaseModel):
    """Grids applicable to a unit type."""
    unit_type: str
    required: List[GridDefinitionResponse]
    flexible: List[GridDefinitionResponse]


class SlotContent(BaseModel):
    """Content for a single slot."""
    content: str
    confidence: float = 0.0
    evidence_notes: Optional[str] = None


class GridCreate(BaseModel):
    """Create a new grid instance on a unit."""
    grid_type: str = Field(..., description="Grid type (e.g., LOGICAL, ACTOR, TEMPORAL)")
    auto_fill: bool = Field(False, description="Use LLM to auto-fill slots")


class GridSlotUpdate(BaseModel):
    """Update a single slot in a grid."""
    content: str
    confidence: Optional[float] = None
    evidence_notes: Optional[str] = None


class GridResponse(BaseModel):
    """Grid instance response."""
    id: str
    unit_id: str
    grid_type: str
    tier: GridTier
    slots: Dict[str, SlotContent] = {}
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GridAutoApplyRequest(BaseModel):
    """Request to auto-apply grids to a unit."""
    include_flexible: bool = Field(True, description="Include flexible tier grids")
    auto_fill: bool = Field(True, description="Auto-fill slots with LLM")


class GridAutoApplyResponse(BaseModel):
    """Response from auto-applying grids."""
    grids_applied: List[GridResponse]
    grids_skipped: List[Dict[str, str]]  # {"grid_type": "...", "reason": "..."}
    message: str


class FrictionEvent(BaseModel):
    """A friction event detected across grids."""
    type: str  # contradiction, gap, uncaptured, tension
    description: str
    slots_involved: List[str]
    severity: str  # low, medium, high
    suggested_resolution: str


class FrictionDetectionResponse(BaseModel):
    """Response from friction detection."""
    friction_events: List[FrictionEvent]
    overall_coherence: float
    summary: str


# =============================================================================
# EVIDENCE SCHEMAS
# =============================================================================

class EvidenceSourceCreate(BaseModel):
    """Create an evidence source."""
    source_type: str = Field(..., description="Type: pdf, url, manual")
    source_name: str = Field(..., description="Name/citation of the source")
    source_url: Optional[str] = None
    source_content: Optional[str] = None  # For manual input


class EvidenceSourceResponse(BaseModel):
    """Evidence source response."""
    id: str
    project_id: str
    source_type: str
    source_name: str
    source_url: Optional[str] = None
    extraction_status: str
    extraction_error: Optional[str] = None
    extracted_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EvidenceFragmentResponse(BaseModel):
    """Evidence fragment response."""
    id: str
    source_id: str
    content: str
    source_location: Optional[str] = None
    analysis_status: str
    relationship_type: Optional[str] = None
    target_unit_id: Optional[str] = None
    target_grid_slot: Optional[str] = None
    confidence: Optional[int] = None
    is_ambiguous: bool = False
    why_needs_decision: Optional[str] = None
    source_name: Optional[str] = None  # Populated from source
    created_at: datetime

    class Config:
        from_attributes = True


class InterpretationResponse(BaseModel):
    """Evidence interpretation response."""
    id: str
    fragment_id: str
    interpretation_key: Optional[str] = None
    title: str
    strategy: Optional[str] = None
    rationale: Optional[str] = None
    relationship_type: Optional[str] = None
    target_unit_id: Optional[str] = None
    target_grid_slot: Optional[str] = None
    is_recommended: bool = False
    commitment_statement: Optional[str] = None
    foreclosure_statements: Optional[List[str]] = None

    class Config:
        from_attributes = True


class PendingDecisionResponse(BaseModel):
    """A pending decision requiring user input."""
    fragment: EvidenceFragmentResponse
    interpretations: List[InterpretationResponse]


class DecisionRequest(BaseModel):
    """Request to resolve a decision."""
    interpretation_id: Optional[str] = None  # None if rejecting all
    decision_type: str = Field(..., description="accept_interpretation, reject_all, or manual_override")
    decision_notes: Optional[str] = None


class DecisionResponse(BaseModel):
    """Decision resolution response."""
    id: str
    fragment_id: str
    decision_type: str
    decision_notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class EvidenceProgressResponse(BaseModel):
    """Evidence processing progress."""
    sources_count: int
    fragments_count: int
    pending_extraction: int
    pending_analysis: int
    pending_decisions: int
    integrated_count: int


class ExtractRequest(BaseModel):
    """Request to trigger extraction."""
    force: bool = Field(False, description="Re-extract even if already done")


# =============================================================================
# PREDICAMENT SCHEMAS (Coherence Monitoring)
# =============================================================================

class PredicamentType(str, Enum):
    """Types of predicaments detected by the coherence monitor."""
    THEORETICAL = "theoretical"
    EMPIRICAL = "empirical"
    CONCEPTUAL = "conceptual"
    PRAXIS = "praxis"


class PredicamentSeverity(str, Enum):
    """How critical is this predicament."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PredicamentStatus(str, Enum):
    """Lifecycle status of a predicament."""
    DETECTED = "detected"
    ANALYZING = "analyzing"
    RESOLVED = "resolved"
    DEFERRED = "deferred"


class PredicamentCreate(BaseModel):
    """Create a predicament (typically from coherence monitor)."""
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=10)
    predicament_type: PredicamentType
    severity: PredicamentSeverity = PredicamentSeverity.MEDIUM
    pole_a: Optional[str] = None
    pole_b: Optional[str] = None
    source_unit_ids: List[str] = []
    source_evidence_ids: List[str] = []


class PredicamentUpdate(BaseModel):
    """Update a predicament."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    severity: Optional[PredicamentSeverity] = None
    status: Optional[PredicamentStatus] = None
    pole_a: Optional[str] = None
    pole_b: Optional[str] = None
    resolution_notes: Optional[str] = None


class PredicamentSummary(BaseModel):
    """Predicament summary for list view."""
    id: str
    title: str
    predicament_type: PredicamentType
    severity: PredicamentSeverity
    status: PredicamentStatus
    source_unit_count: int = 0
    has_grid: bool = False
    detected_at: datetime

    class Config:
        from_attributes = True


class PredicamentResponse(BaseModel):
    """Full predicament response."""
    id: str
    project_id: str
    title: str
    description: str
    predicament_type: PredicamentType
    severity: PredicamentSeverity
    status: PredicamentStatus
    pole_a: Optional[str] = None
    pole_b: Optional[str] = None
    source_unit_ids: List[str] = []
    source_evidence_ids: List[str] = []
    generated_grid_id: Optional[str] = None
    resolution_notes: Optional[str] = None
    resulting_dialectic_id: Optional[str] = None
    detected_at: datetime
    resolved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PredicamentWithContext(BaseModel):
    """Predicament with related units and evidence."""
    predicament: PredicamentResponse
    source_units: List[UnitResponse] = []
    source_evidence: List[EvidenceFragmentResponse] = []
    generated_grid: Optional[GridResponse] = None


class CoherenceCheckRequest(BaseModel):
    """Request a coherence check."""
    deep_analysis: bool = Field(
        False,
        description="Use Opus 4.5 with extended thinking for deep analysis"
    )
    focus_unit_ids: List[str] = Field(
        [],
        description="Optional: Focus on specific units"
    )


class CoherenceCheckResponse(BaseModel):
    """Response from coherence check."""
    predicaments_found: List[PredicamentSummary]
    total_found: int
    new_detected: int
    analysis_depth: str  # "quick" or "deep"
    thinking_tokens_used: Optional[int] = None


class PredicamentResolveRequest(BaseModel):
    """Request to resolve a predicament into a dialectic."""
    resolution_approach: str = Field(
        ...,
        description="How the predicament was resolved"
    )
    dialectic_name: str = Field(
        ...,
        description="Name for the resulting dialectic"
    )
    resolution_notes: Optional[str] = None


class PredicamentResolveResponse(BaseModel):
    """Response from resolving a predicament."""
    predicament_id: str
    resulting_dialectic: UnitResponse
    message: str = "Predicament resolved and transformed into dialectic"


class MatrixRefinement(BaseModel):
    """Refinement instructions for regenerating a matrix."""
    row_refinement: Optional[str] = Field(
        None,
        description="Row axis refinement: more_granular, broader, axis_actors, axis_assumptions, etc."
    )
    row_custom: Optional[str] = Field(
        None,
        description="Custom description for rows when row_refinement is 'add_row' or 'custom_row'"
    )
    col_refinement: Optional[str] = Field(
        None,
        description="Column axis refinement: more_granular, broader, axis_capabilities, axis_poles, etc."
    )
    col_custom: Optional[str] = Field(
        None,
        description="Custom description for columns when col_refinement is 'add_col' or 'custom_col'"
    )
    custom_instruction: Optional[str] = Field(
        None,
        description="Free-form instruction to guide LLM analysis"
    )


class GenerateGridRequest(BaseModel):
    """Request to generate an analytical grid for a predicament."""
    grid_type: Optional[str] = Field(
        None,
        description="Optional: Force a specific grid type"
    )
    # Refinement options
    row_refinement: Optional[str] = Field(None, description="Row axis refinement")
    row_custom: Optional[str] = Field(None, description="Custom row description")
    col_refinement: Optional[str] = Field(None, description="Column axis refinement")
    col_custom: Optional[str] = Field(None, description="Custom column description")
    custom_instruction: Optional[str] = Field(None, description="Custom LLM instruction")


# =============================================================================
# CELL ACTION SCHEMAS
# =============================================================================

class CellActionType(str, Enum):
    """Available cell action types."""
    # Single cell actions
    WHAT_WOULD_IT_TAKE = "what_would_it_take"
    DEEP_ANALYSIS = "deep_analysis"
    GENERATE_ARGUMENTS = "generate_arguments"
    SCENARIO_EXPLORATION = "scenario_exploration"
    SURFACE_ASSUMPTIONS = "surface_assumptions"
    # Multi-cell actions
    FIND_CONNECTIONS = "find_connections"
    COALITION_DESIGN = "coalition_design"
    PRIORITIZE = "prioritize"
    SYNTHESIZE_CONCEPT = "synthesize_concept"
    DRAFT_CONTENT = "draft_content"


class CellInfo(BaseModel):
    """Information about a selected cell."""
    row_id: str = Field(..., description="Row identifier")
    col_id: str = Field(..., description="Column identifier")
    row_label: str = Field(..., description="Human-readable row label")
    col_label: str = Field(..., description="Human-readable column label")
    rating: str = Field(..., description="Cell rating: strong, moderate, weak, empty")
    content: Optional[str] = Field(None, description="Cell content/analysis")


class CellActionRequest(BaseModel):
    """Request to execute an action on selected cells."""
    action_type: CellActionType = Field(..., description="The action to execute")
    cells: List[CellInfo] = Field(..., min_length=1, description="Selected cells")
    custom_context: Optional[str] = Field(None, description="Additional context from user")


class CellActionResponse(BaseModel):
    """Response from executing a cell action."""
    action_type: str
    cells_analyzed: int
    result: Dict[str, Any] = Field(..., description="Structured result based on action type")
    thinking_summary: Optional[str] = Field(None, description="Summary of LLM thinking process")
    created_at: datetime = Field(default_factory=datetime.utcnow)


# =============================================================================
# DYNAMIC CELL ACTIONS - Context-specific action generation
# =============================================================================

class GeneratedAction(BaseModel):
    """A dynamically generated action for selected cells."""
    id: str = Field(..., description="Unique action identifier")
    label: str = Field(..., description="Short action name (3-5 words)")
    description: str = Field(..., description="What this action produces and why it's valuable")
    icon: str = Field(default="lightbulb", description="Bootstrap icon name")
    output_type: str = Field(default="analysis", description="Type of output: analysis, recommendations, comparison, etc.")


class GenerateCellActionsRequest(BaseModel):
    """Request to generate context-specific actions for selected cells."""
    cells: List[CellInfo] = Field(..., min_length=1, description="Selected cells to analyze")


class GenerateCellActionsResponse(BaseModel):
    """Response with generated actions for selected cells."""
    actions: List[GeneratedAction] = Field(default_factory=list)
    cells_count: int = Field(..., description="Number of cells analyzed")
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class ExecuteDynamicActionRequest(BaseModel):
    """Request to execute a dynamically generated action."""
    cells: List[CellInfo] = Field(..., min_length=1, description="Selected cells")
    action: GeneratedAction = Field(..., description="The action to execute")


class ExecuteDynamicActionResponse(BaseModel):
    """Response from executing a dynamic action."""
    action_executed: GeneratedAction
    cells_analyzed: int
    result: Dict[str, Any] = Field(..., description="Structured analysis result")
    thinking_summary: Optional[str] = Field(None, description="Summary of LLM thinking")
    executed_at: datetime = Field(default_factory=datetime.utcnow)


# =============================================================================
# PREDICAMENT NOTES - Saved insights from cell actions
# =============================================================================

class PredicamentNote(BaseModel):
    """A note saved from a cell action result."""
    id: str = Field(..., description="Unique note identifier")
    title: str = Field(..., description="Note title (from action label)")
    content: Dict[str, Any] = Field(..., description="The result content from the action")
    action: GeneratedAction = Field(..., description="The action that produced this note")
    cells: List[CellInfo] = Field(..., description="The cells that were analyzed")
    thinking_summary: Optional[str] = Field(None, description="LLM thinking summary")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SaveNoteRequest(BaseModel):
    """Request to save a cell action result as a note."""
    title: str = Field(..., description="Note title")
    content: Dict[str, Any] = Field(..., description="The result content")
    action: GeneratedAction = Field(..., description="The action that produced this")
    cells: List[CellInfo] = Field(..., description="The cells analyzed")
    thinking_summary: Optional[str] = Field(None, description="LLM thinking summary")


class SaveNoteResponse(BaseModel):
    """Response from saving a note."""
    note: PredicamentNote
    message: str = "Note saved successfully"


class NotesList(BaseModel):
    """List of notes for a predicament."""
    notes: List[PredicamentNote] = []
    count: int = 0


class SpawnDialecticFromNoteRequest(BaseModel):
    """Request to spawn a dialectic from a saved note."""
    # note_id is a path parameter, not in body
    dialectic_name: str = Field(..., description="Name for the new dialectic")
    definition: Optional[str] = Field(None, description="Optional definition override")
    pole_a: Optional[str] = Field(None, description="Thesis/Pole A")
    pole_b: Optional[str] = Field(None, description="Antithesis/Pole B")


class SpawnDialecticFromNoteResponse(BaseModel):
    """Response from spawning a dialectic."""
    dialectic: UnitResponse
    note_id: str
    message: str = "Dialectic created from note"


# Update forward references
ProjectResponse.model_rebuild()
