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


# Update forward references
ProjectResponse.model_rebuild()
