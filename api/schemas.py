"""
Theory Service - Pydantic Schemas
Request/Response models for the API.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


# =============================================================================
# ENUMS (mirror SQLAlchemy enums for Pydantic)
# =============================================================================

class ConceptStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    CHALLENGED = "challenged"


class DialecticStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    RESOLVED = "resolved"
    DEPRECATED = "deprecated"


class ChallengeStatus(str, Enum):
    PENDING = "pending"
    ACKNOWLEDGED = "acknowledged"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    INTEGRATED = "integrated"


class ChallengeType(str, Enum):
    SUPPORTS = "supports"
    CHALLENGES = "challenges"
    REFINES = "refines"
    EXTENDS = "extends"
    LIMITS = "limits"
    RESOLVES_TOWARD_A = "resolves_toward_a"
    RESOLVES_TOWARD_B = "resolves_toward_b"
    DEEPENS = "deepens"
    REFRAMES = "reframes"
    SYNTHESIZES = "synthesizes"


# =============================================================================
# THEORY SOURCE SCHEMAS
# =============================================================================

class TheorySourceBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    short_name: Optional[str] = Field(None, max_length=100)
    source_type: Optional[str] = "article"
    description: Optional[str] = None
    author: Optional[str] = None


class TheorySourceCreate(TheorySourceBase):
    pass


class TheorySourceResponse(TheorySourceBase):
    id: int
    created_at: datetime
    concept_count: Optional[int] = 0
    dialectic_count: Optional[int] = 0
    claim_count: Optional[int] = 0

    class Config:
        from_attributes = True


# =============================================================================
# CONCEPT SCHEMAS
# =============================================================================

class ConceptBase(BaseModel):
    term: str = Field(..., min_length=1, max_length=255)
    definition: str = Field(..., min_length=1)
    category: Optional[str] = None
    source_notes: Optional[str] = None
    source_id: Optional[int] = None


class ConceptCreate(ConceptBase):
    pass


class ConceptUpdate(BaseModel):
    term: Optional[str] = None
    definition: Optional[str] = None
    category: Optional[str] = None
    status: Optional[ConceptStatus] = None
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    source_notes: Optional[str] = None
    source_id: Optional[int] = None


class ConceptResponse(ConceptBase):
    id: int
    status: ConceptStatus
    confidence: float
    created_at: datetime
    updated_at: datetime
    challenge_count: Optional[int] = 0
    source_title: Optional[str] = None  # Populated from source relationship

    class Config:
        from_attributes = True


# =============================================================================
# DIALECTIC SCHEMAS
# =============================================================================

class DialecticBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    tension_a: str = Field(..., min_length=1)
    tension_b: str = Field(..., min_length=1)
    description: Optional[str] = None
    category: Optional[str] = None
    source_id: Optional[int] = None


class DialecticCreate(DialecticBase):
    source_notes: Optional[str] = None


class DialecticUpdate(BaseModel):
    name: Optional[str] = None
    tension_a: Optional[str] = None
    tension_b: Optional[str] = None
    description: Optional[str] = None
    status: Optional[DialecticStatus] = None
    weight_toward_a: Optional[float] = Field(None, ge=0.0, le=1.0)
    category: Optional[str] = None
    source_id: Optional[int] = None


class DialecticResponse(DialecticBase):
    id: int
    status: DialecticStatus
    weight_toward_a: float
    source_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    challenge_count: Optional[int] = 0
    source_title: Optional[str] = None  # Populated from source relationship

    class Config:
        from_attributes = True


# =============================================================================
# CLAIM SCHEMAS
# =============================================================================

class ClaimBase(BaseModel):
    statement: str = Field(..., min_length=1)
    elaboration: Optional[str] = None
    claim_type: Optional[str] = None
    category: Optional[str] = None
    source_id: Optional[int] = None


class ClaimCreate(ClaimBase):
    pass


class ClaimUpdate(BaseModel):
    statement: Optional[str] = None
    elaboration: Optional[str] = None
    claim_type: Optional[str] = None
    category: Optional[str] = None
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    is_active: Optional[bool] = None
    source_id: Optional[int] = None


class ClaimResponse(ClaimBase):
    id: int
    confidence: float
    is_active: bool
    created_at: datetime
    updated_at: datetime
    source_title: Optional[str] = None  # Populated from source relationship

    class Config:
        from_attributes = True


# =============================================================================
# CHALLENGE SCHEMAS (for essay-flow integration)
# =============================================================================

class ChallengeCreate(BaseModel):
    """Schema for essay-flow to post challenges to theory."""
    source_project_id: int
    source_cluster_id: Optional[int] = None
    source_cluster_name: Optional[str] = None

    # What's being challenged (exactly one should be set)
    concept_id: Optional[int] = None
    dialectic_id: Optional[int] = None
    claim_id: Optional[int] = None

    # Challenge details
    challenge_type: ChallengeType
    impact_summary: str
    trend_description: Optional[str] = None
    key_evidence: Optional[str] = None
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)

    # For dialectics
    weight_toward_a: Optional[float] = Field(None, ge=0.0, le=1.0)

    # Proposed changes
    proposed_refinement: Optional[str] = None
    refinement_rationale: Optional[str] = None
    proposed_synthesis: Optional[str] = None
    proposed_reframe: Optional[str] = None


class ChallengeResponse(BaseModel):
    id: int
    source_project_id: int
    source_cluster_id: Optional[int]
    source_cluster_name: Optional[str]

    concept_id: Optional[int]
    dialectic_id: Optional[int]
    claim_id: Optional[int]

    challenge_type: ChallengeType
    impact_summary: str
    trend_description: Optional[str]
    key_evidence: Optional[str]
    confidence: float
    weight_toward_a: Optional[float]

    proposed_refinement: Optional[str]
    refinement_rationale: Optional[str]
    proposed_synthesis: Optional[str]
    proposed_reframe: Optional[str]

    status: ChallengeStatus
    reviewer_notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    reviewed_at: Optional[datetime]

    # Related entity names (for display)
    concept_term: Optional[str] = None
    dialectic_name: Optional[str] = None
    claim_statement: Optional[str] = None

    class Config:
        from_attributes = True


class ChallengeReview(BaseModel):
    """Schema for reviewing/updating challenge status."""
    status: ChallengeStatus
    reviewer_notes: Optional[str] = None


# =============================================================================
# BULK/SYNC SCHEMAS (for essay-flow to fetch all theory)
# =============================================================================

class TheorySyncResponse(BaseModel):
    """Complete theory state for essay-flow to sync."""
    sources: List[TheorySourceResponse]
    concepts: List[ConceptResponse]
    dialectics: List[DialecticResponse]
    claims: List[ClaimResponse]
    synced_at: datetime


class BulkChallengeCreate(BaseModel):
    """Batch create challenges from essay-flow."""
    challenges: List[ChallengeCreate]


class BulkChallengeResponse(BaseModel):
    """Response for batch challenge creation."""
    created_count: int
    challenge_ids: List[int]
