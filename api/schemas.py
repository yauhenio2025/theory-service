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


class EmergingStatus(str, Enum):
    PROPOSED = "proposed"
    CLUSTERING = "clustering"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    PROMOTED = "promoted"


class ClusterStatus(str, Enum):
    PENDING = "pending"
    REVIEWING = "reviewing"
    RESOLVED = "resolved"


class ClusterType(str, Enum):
    CONCEPT_IMPACT = "concept_impact"
    DIALECTIC_IMPACT = "dialectic_impact"
    EMERGING_CONCEPT = "emerging_concept"
    EMERGING_DIALECTIC = "emerging_dialectic"


class RecommendedAction(str, Enum):
    ACCEPT = "accept"
    REJECT = "reject"
    MERGE = "merge"
    REFINE = "refine"
    HUMAN_REVIEW = "human_review"


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
    source_project_name: Optional[str] = None
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
    source_project_name: Optional[str]
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


# =============================================================================
# EMERGING CONCEPT SCHEMAS
# =============================================================================

class EmergingConceptCreate(BaseModel):
    """Schema for submitting emerging concepts from essay-flow."""
    source_project_id: int
    source_project_name: Optional[str] = None
    source_cluster_ids: Optional[List[int]] = None
    source_cluster_names: Optional[List[str]] = None

    proposed_name: str = Field(..., min_length=1, max_length=300)
    proposed_definition: Optional[str] = None
    emergence_rationale: str = Field(..., min_length=1)
    evidence_strength: Optional[str] = None  # strong, moderate, suggestive

    related_concept_ids: Optional[List[int]] = None
    differentiation_notes: Optional[str] = None

    confidence: float = Field(default=0.8, ge=0.0, le=1.0)


class EmergingConceptUpdate(BaseModel):
    """Schema for updating emerging concepts."""
    proposed_name: Optional[str] = None
    proposed_definition: Optional[str] = None
    emergence_rationale: Optional[str] = None
    status: Optional[EmergingStatus] = None
    reviewer_notes: Optional[str] = None
    promoted_to_concept_id: Optional[int] = None


class EmergingConceptResponse(BaseModel):
    """Response schema for emerging concepts."""
    id: int
    source_project_id: int
    source_project_name: Optional[str]
    source_cluster_ids: Optional[List[int]]
    source_cluster_names: Optional[List[str]]

    proposed_name: str
    proposed_definition: Optional[str]
    emergence_rationale: str
    evidence_strength: Optional[str]

    related_concept_ids: Optional[List[int]]
    differentiation_notes: Optional[str]

    confidence: float
    status: EmergingStatus
    promoted_to_concept_id: Optional[int]
    cluster_group_id: Optional[int]

    reviewer_notes: Optional[str]
    created_at: datetime
    reviewed_at: Optional[datetime]

    # Related concept names for display
    related_concept_names: Optional[List[str]] = None

    class Config:
        from_attributes = True


# =============================================================================
# EMERGING DIALECTIC SCHEMAS
# =============================================================================

class EmergingDialecticCreate(BaseModel):
    """Schema for submitting emerging dialectics from essay-flow."""
    source_project_id: int
    source_project_name: Optional[str] = None
    source_cluster_ids: Optional[List[int]] = None
    source_cluster_names: Optional[List[str]] = None

    proposed_tension_a: str = Field(..., min_length=1)
    proposed_tension_b: str = Field(..., min_length=1)
    proposed_question: Optional[str] = None
    emergence_rationale: str = Field(..., min_length=1)
    evidence_strength: Optional[str] = None

    related_dialectic_ids: Optional[List[int]] = None
    differentiation_notes: Optional[str] = None

    confidence: float = Field(default=0.8, ge=0.0, le=1.0)


class EmergingDialecticUpdate(BaseModel):
    """Schema for updating emerging dialectics."""
    proposed_tension_a: Optional[str] = None
    proposed_tension_b: Optional[str] = None
    proposed_question: Optional[str] = None
    emergence_rationale: Optional[str] = None
    status: Optional[EmergingStatus] = None
    reviewer_notes: Optional[str] = None
    promoted_to_dialectic_id: Optional[int] = None


class EmergingDialecticResponse(BaseModel):
    """Response schema for emerging dialectics."""
    id: int
    source_project_id: int
    source_project_name: Optional[str]
    source_cluster_ids: Optional[List[int]]
    source_cluster_names: Optional[List[str]]

    proposed_tension_a: str
    proposed_tension_b: str
    proposed_question: Optional[str]
    emergence_rationale: str
    evidence_strength: Optional[str]

    related_dialectic_ids: Optional[List[int]]
    differentiation_notes: Optional[str]

    confidence: float
    status: EmergingStatus
    promoted_to_dialectic_id: Optional[int]
    cluster_group_id: Optional[int]

    reviewer_notes: Optional[str]
    created_at: datetime
    reviewed_at: Optional[datetime]

    # Related dialectic names for display
    related_dialectic_names: Optional[List[str]] = None

    class Config:
        from_attributes = True


# =============================================================================
# CHALLENGE CLUSTER SCHEMAS
# =============================================================================

class ChallengeClusterMemberResponse(BaseModel):
    """Response schema for cluster members."""
    id: int
    cluster_id: int
    challenge_id: Optional[int]
    emerging_concept_id: Optional[int]
    emerging_dialectic_id: Optional[int]
    similarity_score: Optional[float]
    created_at: datetime

    # Expanded details based on member type
    challenge: Optional["ChallengeResponse"] = None
    emerging_concept: Optional[EmergingConceptResponse] = None
    emerging_dialectic: Optional[EmergingDialecticResponse] = None

    class Config:
        from_attributes = True


class ChallengeClusterResponse(BaseModel):
    """Response schema for challenge clusters."""
    id: int
    cluster_type: ClusterType
    cluster_summary: Optional[str]
    cluster_recommendation: Optional[str]
    recommended_action: Optional[RecommendedAction]

    target_concept_id: Optional[int]
    target_dialectic_id: Optional[int]

    status: ClusterStatus
    resolution_notes: Optional[str]
    member_count: int
    source_project_count: int

    created_at: datetime
    resolved_at: Optional[datetime]

    # Expanded target details
    target_concept_term: Optional[str] = None
    target_dialectic_name: Optional[str] = None

    # Members (optionally loaded)
    members: Optional[List[ChallengeClusterMemberResponse]] = None

    class Config:
        from_attributes = True


class ChallengeClusterResolve(BaseModel):
    """Schema for resolving a challenge cluster."""
    status: ClusterStatus
    resolution_notes: Optional[str] = None
    # Action to apply to all members
    member_action: Optional[str] = None  # accept, reject, individual


# =============================================================================
# CLUSTERING REQUEST/RESPONSE SCHEMAS
# =============================================================================

class ClusteringRequest(BaseModel):
    """Request to run LLM clustering on pending challenges."""
    cluster_types: Optional[List[ClusterType]] = None  # All types if None
    target_concept_ids: Optional[List[int]] = None  # Filter by target
    target_dialectic_ids: Optional[List[int]] = None


class ClusteringResponse(BaseModel):
    """Response from clustering operation."""
    clusters_created: int
    challenges_clustered: int
    emerging_concepts_clustered: int
    emerging_dialectics_clustered: int
    processing_time_seconds: float


# =============================================================================
# BULK EMERGING SCHEMAS
# =============================================================================

class BulkEmergingConceptCreate(BaseModel):
    """Batch create emerging concepts from essay-flow."""
    emerging_concepts: List[EmergingConceptCreate]


class BulkEmergingConceptResponse(BaseModel):
    """Response for batch emerging concept creation."""
    created_count: int
    emerging_concept_ids: List[int]


class BulkEmergingDialecticCreate(BaseModel):
    """Batch create emerging dialectics from essay-flow."""
    emerging_dialectics: List[EmergingDialecticCreate]


class BulkEmergingDialecticResponse(BaseModel):
    """Response for batch emerging dialectic creation."""
    created_count: int
    emerging_dialectic_ids: List[int]


# =============================================================================
# DASHBOARD/STATS SCHEMAS
# =============================================================================

class ChallengeDashboardStats(BaseModel):
    """Statistics for the challenge dashboard."""
    concept_impacts: int
    dialectic_impacts: int
    emerging_concepts: int
    emerging_dialectics: int

    pending_challenges: int
    pending_clusters: int
    resolved_this_week: int

    source_projects: List[dict]  # [{id, name, count}]
