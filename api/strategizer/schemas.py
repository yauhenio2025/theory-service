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


# Update forward references
ProjectResponse.model_rebuild()
