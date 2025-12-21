"""
Theory Service - Database Models
SQLAlchemy models for the Theory knowledge base.
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean,
    ForeignKey, Enum, Float, JSON, Table, CheckConstraint
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.sql import func
import enum


class Base(DeclarativeBase):
    pass


# =============================================================================
# ENUMS
# =============================================================================

class ConceptStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    CHALLENGED = "challenged"


class DialecticStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    RESOLVED = "resolved"
    DEPRECATED = "deprecated"


class ChallengeStatus(str, enum.Enum):
    PENDING = "pending"
    ACKNOWLEDGED = "acknowledged"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    INTEGRATED = "integrated"


class ChallengeType(str, enum.Enum):
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


class EmergingStatus(str, enum.Enum):
    """Status for emerging concepts and dialectics."""
    PROPOSED = "proposed"
    CLUSTERING = "clustering"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    PROMOTED = "promoted"


class ClusterStatus(str, enum.Enum):
    """Status for challenge clusters."""
    PENDING = "pending"
    REVIEWING = "reviewing"
    RESOLVED = "resolved"


class ClusterType(str, enum.Enum):
    """Type of challenge cluster."""
    CONCEPT_IMPACT = "concept_impact"
    DIALECTIC_IMPACT = "dialectic_impact"
    EMERGING_CONCEPT = "emerging_concept"
    EMERGING_DIALECTIC = "emerging_dialectic"


class RecommendedAction(str, enum.Enum):
    """LLM-recommended action for a cluster."""
    ACCEPT = "accept"
    REJECT = "reject"
    MERGE = "merge"
    REFINE = "refine"
    HUMAN_REVIEW = "human_review"


# =============================================================================
# THEORY SOURCES
# =============================================================================

class TheorySource(Base):
    """A source document that theory is extracted from (article, paper, book)."""
    __tablename__ = "theory_sources"

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    short_name = Column(String(100), index=True)  # Short identifier for filtering
    source_type = Column(String(50), default="article")  # article, paper, book, notes
    description = Column(Text)  # Brief description of this theory source
    author = Column(String(255))

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    concepts = relationship("Concept", back_populates="source")
    dialectics = relationship("Dialectic", back_populates="source")
    claims = relationship("Claim", back_populates="source")


# =============================================================================
# CORE MODELS
# =============================================================================

class Concept(Base):
    """Theoretical concept with definition and relationships."""
    __tablename__ = "concepts"

    id = Column(Integer, primary_key=True)
    term = Column(String(255), nullable=False, index=True)
    definition = Column(Text, nullable=False)
    category = Column(String(100))  # e.g., "hegemony", "technology", "sovereignty"

    # Source linkage
    source_id = Column(Integer, ForeignKey("theory_sources.id"), nullable=True)

    # Metadata
    status = Column(Enum(ConceptStatus), default=ConceptStatus.ACTIVE)
    confidence = Column(Float, default=1.0)  # How confident we are in this concept
    source_notes = Column(Text)  # Additional notes about origin

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    source = relationship("TheorySource", back_populates="concepts")
    challenges = relationship("Challenge", back_populates="concept", foreign_keys="Challenge.concept_id")
    refinements = relationship("Refinement", back_populates="concept")


class Dialectic(Base):
    """Dialectical tension between two positions."""
    __tablename__ = "dialectics"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, index=True)
    tension_a = Column(Text, nullable=False)  # First position
    tension_b = Column(Text, nullable=False)  # Counter position
    description = Column(Text)  # Context/question this dialectic addresses

    # Source linkage
    source_id = Column(Integer, ForeignKey("theory_sources.id"), nullable=True)

    # Current state
    status = Column(Enum(DialecticStatus), default=DialecticStatus.ACTIVE)
    weight_toward_a = Column(Float, default=0.5)  # 0.0 = fully B, 1.0 = fully A

    # Metadata
    category = Column(String(100))
    source_notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    source = relationship("TheorySource", back_populates="dialectics")
    challenges = relationship("Challenge", back_populates="dialectic", foreign_keys="Challenge.dialectic_id")


class Claim(Base):
    """Theoretical claim or thesis."""
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True)
    statement = Column(Text, nullable=False)
    elaboration = Column(Text)

    # Source linkage
    source_id = Column(Integer, ForeignKey("theory_sources.id"), nullable=True)

    # Classification
    claim_type = Column(String(50))  # "thesis", "hypothesis", "observation"
    category = Column(String(100))
    confidence = Column(Float, default=0.8)

    # Status
    is_active = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    source = relationship("TheorySource", back_populates="claims")
    challenges = relationship("Challenge", back_populates="claim", foreign_keys="Challenge.claim_id")


class Challenge(Base):
    """
    Challenge to theory from empirical evidence.
    Posted by essay-flow when evidence impacts theory.
    """
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True)

    # Source identification (from essay-flow)
    source_project_id = Column(Integer, nullable=False)  # essay-flow project ID
    source_project_name = Column(String(200))  # Project name for display
    source_cluster_id = Column(Integer)  # evidence cluster that generated this
    source_cluster_name = Column(String(255))

    # Clustering
    cluster_group_id = Column(Integer, ForeignKey("challenge_clusters.id"))

    # What's being challenged
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=True)
    dialectic_id = Column(Integer, ForeignKey("dialectics.id"), nullable=True)
    claim_id = Column(Integer, ForeignKey("claims.id"), nullable=True)

    # Challenge details
    challenge_type = Column(Enum(ChallengeType), nullable=False)
    impact_summary = Column(Text, nullable=False)
    trend_description = Column(Text)
    key_evidence = Column(Text)
    confidence = Column(Float, default=0.8)

    # For dialectics: which side does evidence support?
    weight_toward_a = Column(Float)  # 0.0 = supports B, 1.0 = supports A

    # Proposed changes
    proposed_refinement = Column(Text)
    refinement_rationale = Column(Text)
    proposed_synthesis = Column(Text)
    proposed_reframe = Column(Text)

    # Status tracking
    status = Column(Enum(ChallengeStatus), default=ChallengeStatus.PENDING)
    reviewer_notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    reviewed_at = Column(DateTime(timezone=True))

    # Relationships
    concept = relationship("Concept", back_populates="challenges", foreign_keys=[concept_id])
    dialectic = relationship("Dialectic", back_populates="challenges", foreign_keys=[dialectic_id])
    claim = relationship("Claim", back_populates="challenges", foreign_keys=[claim_id])


class Refinement(Base):
    """
    Accepted refinement to a concept.
    Created when a challenge is integrated.
    """
    __tablename__ = "refinements"

    id = Column(Integer, primary_key=True)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)

    # What changed
    previous_definition = Column(Text)
    new_definition = Column(Text)
    change_rationale = Column(Text)

    # Source
    source_challenge_id = Column(Integer, ForeignKey("challenges.id"))

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    concept = relationship("Concept", back_populates="refinements")


# =============================================================================
# EMERGING THEORY - Proposed new concepts/dialectics from evidence
# =============================================================================

class EmergingConcept(Base):
    """
    Proposed new concept from evidence analysis.
    Can be promoted to a full Concept after review.
    """
    __tablename__ = "emerging_concepts"

    id = Column(Integer, primary_key=True)

    # Source identification
    source_project_id = Column(Integer, nullable=False)
    source_project_name = Column(String(200))
    source_cluster_ids = Column(ARRAY(Integer))  # Can emerge from multiple clusters
    source_cluster_names = Column(ARRAY(Text))

    # Proposed concept details
    proposed_name = Column(String(300), nullable=False)
    proposed_definition = Column(Text)
    emergence_rationale = Column(Text, nullable=False)
    evidence_strength = Column(Text)  # strong, moderate, suggestive, or longer descriptions

    # Relationship to existing theory
    related_concept_ids = Column(ARRAY(Integer))  # Existing concepts this relates to
    differentiation_notes = Column(Text)  # How it differs from existing

    # Assessment
    confidence = Column(Float, default=0.8)
    status = Column(Enum(EmergingStatus), default=EmergingStatus.PROPOSED)
    promoted_to_concept_id = Column(Integer, ForeignKey("concepts.id"))

    # Clustering
    cluster_group_id = Column(Integer, ForeignKey("challenge_clusters.id"))

    # Review
    reviewer_notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True))

    # Relationships
    promoted_concept = relationship("Concept", foreign_keys=[promoted_to_concept_id])
    cluster = relationship("ChallengeCluster", back_populates="emerging_concepts")


class EmergingDialectic(Base):
    """
    Proposed new dialectic tension from evidence analysis.
    Can be promoted to a full Dialectic after review.
    """
    __tablename__ = "emerging_dialectics"

    id = Column(Integer, primary_key=True)

    # Source identification
    source_project_id = Column(Integer, nullable=False)
    source_project_name = Column(String(200))
    source_cluster_ids = Column(ARRAY(Integer))
    source_cluster_names = Column(ARRAY(Text))

    # Proposed dialectic details
    proposed_tension_a = Column(Text, nullable=False)
    proposed_tension_b = Column(Text, nullable=False)
    proposed_question = Column(Text)  # The question this dialectic addresses
    emergence_rationale = Column(Text, nullable=False)
    evidence_strength = Column(Text)

    # Relationship to existing theory
    related_dialectic_ids = Column(ARRAY(Integer))
    differentiation_notes = Column(Text)

    # Assessment
    confidence = Column(Float, default=0.8)
    status = Column(Enum(EmergingStatus), default=EmergingStatus.PROPOSED)
    promoted_to_dialectic_id = Column(Integer, ForeignKey("dialectics.id"))

    # Clustering
    cluster_group_id = Column(Integer, ForeignKey("challenge_clusters.id"))

    # Review
    reviewer_notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True))

    # Relationships
    promoted_dialectic = relationship("Dialectic", foreign_keys=[promoted_to_dialectic_id])
    cluster = relationship("ChallengeCluster", back_populates="emerging_dialectics")


# =============================================================================
# CHALLENGE CLUSTERING - Group similar challenges for batch processing
# =============================================================================

class ChallengeCluster(Base):
    """
    Group of similar challenges from multiple projects.
    Enables batch review and LLM-powered recommendations.
    """
    __tablename__ = "challenge_clusters"

    id = Column(Integer, primary_key=True)
    cluster_type = Column(Enum(ClusterType), nullable=False)

    # LLM-generated cluster metadata
    cluster_summary = Column(Text)  # What unifies this cluster
    cluster_recommendation = Column(Text)  # Explanation of recommended action
    recommended_action = Column(Enum(RecommendedAction))

    # Target entity (for impact clusters)
    target_concept_id = Column(Integer, ForeignKey("concepts.id"))
    target_dialectic_id = Column(Integer, ForeignKey("dialectics.id"))

    # Cluster state
    status = Column(Enum(ClusterStatus), default=ClusterStatus.PENDING)
    resolution_notes = Column(Text)
    member_count = Column(Integer, default=0)
    source_project_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True))

    # Relationships
    target_concept = relationship("Concept", foreign_keys=[target_concept_id])
    target_dialectic = relationship("Dialectic", foreign_keys=[target_dialectic_id])
    members = relationship("ChallengeClusterMember", back_populates="cluster", cascade="all, delete-orphan")
    emerging_concepts = relationship("EmergingConcept", back_populates="cluster")
    emerging_dialectics = relationship("EmergingDialectic", back_populates="cluster")


class ChallengeClusterMember(Base):
    """
    Links a challenge or emerging item to a cluster.
    """
    __tablename__ = "challenge_cluster_members"

    id = Column(Integer, primary_key=True)
    cluster_id = Column(Integer, ForeignKey("challenge_clusters.id", ondelete="CASCADE"), nullable=False)

    # One of these will be set depending on cluster_type
    challenge_id = Column(Integer, ForeignKey("challenges.id", ondelete="CASCADE"))
    emerging_concept_id = Column(Integer, ForeignKey("emerging_concepts.id", ondelete="CASCADE"))
    emerging_dialectic_id = Column(Integer, ForeignKey("emerging_dialectics.id", ondelete="CASCADE"))

    # Similarity score (0-1, how similar to cluster centroid)
    similarity_score = Column(Float)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Ensure only one reference type per member
    __table_args__ = (
        CheckConstraint(
            '(CASE WHEN challenge_id IS NOT NULL THEN 1 ELSE 0 END + '
            'CASE WHEN emerging_concept_id IS NOT NULL THEN 1 ELSE 0 END + '
            'CASE WHEN emerging_dialectic_id IS NOT NULL THEN 1 ELSE 0 END) = 1',
            name='single_reference'
        ),
    )

    # Relationships
    cluster = relationship("ChallengeCluster", back_populates="members")
    challenge = relationship("Challenge", foreign_keys=[challenge_id])
    emerging_concept = relationship("EmergingConcept", foreign_keys=[emerging_concept_id])
    emerging_dialectic = relationship("EmergingDialectic", foreign_keys=[emerging_dialectic_id])


# =============================================================================
# WIZARD SESSIONS - Cross-device session persistence
# =============================================================================

class WizardSessionStatus(str, enum.Enum):
    """Status for wizard sessions."""
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class WizardSession(Base):
    """
    Stores wizard session state for cross-device persistence.
    Allows users to start a concept on one device and continue on another.
    """
    __tablename__ = "wizard_sessions"

    id = Column(Integer, primary_key=True)

    # Session identification
    session_key = Column(String(64), unique=True, nullable=False, index=True)
    concept_name = Column(String(300), nullable=False)

    # Session state (JSON blob with all wizard state)
    session_state = Column(JSON, nullable=False)

    # Metadata
    stage = Column(String(50))
    source_id = Column(Integer, ForeignKey("theory_sources.id"))

    # Status
    status = Column(String(20), default="active")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_accessed_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    source = relationship("TheorySource", foreign_keys=[source_id])


# =============================================================================
# CONCEPT RELATIONSHIPS - Inter-concept relations with dimensional nuance
# =============================================================================

class RelationshipType(str, enum.Enum):
    """Primary relationship types between concepts."""
    RIVALS = "rivals"  # Competing for same theoretical space
    COMPLEMENTS = "complements"  # Work together, fill different gaps
    SUBSUMES = "subsumes"  # Broader frame containing the other
    SUBSUMED_BY = "subsumed_by"  # Contained by a broader frame
    RUPTURES = "ruptures"  # Explicitly breaks from (Bachelardian)
    RUPTURED_BY = "ruptured_by"  # Broken from by another
    SPECIALIZES = "specializes"  # Specific case of a more general concept
    GENERALIZES = "generalizes"  # Abstracts from another concept
    SHARES_PROBLEMATIC = "shares_problematic"  # Address same underlying problem
    HISTORICIZES = "historicizes"  # Places another in historical context
    HISTORICIZED_BY = "historicized_by"  # Placed in historical context by another
    APPROPRIATES = "appropriates"  # Takes elements while transforming meaning
    APPROPRIATED_BY = "appropriated_by"  # Elements taken by another
    RESPONDS_TO = "responds_to"  # Direct theoretical response
    RESPONDED_TO_BY = "responded_to_by"  # Received response from another
    SYNTHESIZES = "synthesizes"  # Combines elements from multiple concepts
    COMPONENT_OF = "component_of"  # Is a component in a synthesis


class ProblematicRelation(str, enum.Enum):
    """How concepts relate in terms of their underlying problematic (Deleuzian)."""
    SAME = "same"  # Address exactly the same problematic
    OVERLAPPING = "overlapping"  # Partial overlap in problem space
    NESTED = "nested"  # One problematic contains the other
    ADJACENT = "adjacent"  # Related but distinct problematics
    DIFFERENT = "different"  # Unrelated problematics


class WebProximity(str, enum.Enum):
    """How close concepts are in the web of beliefs (Quinean)."""
    CORE = "core"  # Central, tightly connected
    ADJACENT = "adjacent"  # One degree of separation
    PERIPHERAL = "peripheral"  # Loosely connected
    DISTANT = "distant"  # Far apart in belief web


class ExternalConcept(Base):
    """
    Reference to a concept from an external author/work.
    Allows relating our concepts to concepts from Zuboff, Srnicek, etc.
    """
    __tablename__ = "external_concepts"

    id = Column(Integer, primary_key=True)

    # Core identification
    term = Column(String(255), nullable=False, index=True)
    author = Column(String(255), index=True)  # "Zuboff", "Srnicek", etc.
    source_work = Column(String(500))  # "The Age of Surveillance Capitalism"
    year = Column(Integer)  # Year of publication

    # Our understanding of their concept
    brief_definition = Column(Text)
    extended_definition = Column(Text)  # Fuller explanation

    # Paradigm/school classification
    paradigm = Column(String(255))  # "surveillance studies", "platform capitalism"
    research_program = Column(String(255))  # Broader research tradition
    disciplinary_home = Column(String(255))  # "sociology", "political economy", etc.

    # Key claims (JSON array of strings)
    key_claims = Column(JSON)  # ["claim1", "claim2", ...]

    # Dimensional pre-analysis (can be extracted from documents)
    dimensional_analysis = Column(JSON)  # Pre-computed dimensional aspects

    # Source documents we extracted this from
    source_document_ids = Column(ARRAY(Integer))  # IDs of uploaded documents

    # Metadata
    confidence = Column(Float, default=0.8)  # How confident in our understanding
    notes = Column(Text)  # Additional notes

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    relationships_as_source = relationship(
        "ConceptRelationship",
        foreign_keys="ConceptRelationship.external_concept_id",
        back_populates="external_concept"
    )


class ConceptRelationship(Base):
    """
    Relationship between concepts (internal or external) with dimensional nuance.
    Captures how concepts from different research programs/paradigms relate.
    """
    __tablename__ = "concept_relationships"

    id = Column(Integer, primary_key=True)

    # Source concept (one of these must be set)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=True)
    external_concept_id = Column(Integer, ForeignKey("external_concepts.id"), nullable=True)

    # Target concept (one of these must be set)
    related_concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=True)
    related_external_concept_id = Column(Integer, ForeignKey("external_concepts.id"), nullable=True)

    # Primary relationship type
    relationship_type = Column(Enum(RelationshipType), nullable=False)

    # Relationship strength and directionality
    strength = Column(Float, default=0.8)  # How strong is this relationship (0-1)
    is_symmetric = Column(Boolean, default=False)  # Is the relationship bidirectional?

    # Brief description
    description = Column(Text)  # Human-readable explanation

    # ==========================================================================
    # DIMENSIONAL NUANCE (9 Philosophical Dimensions)
    # ==========================================================================

    # Sellarsian Dimension (The "Given" / Foundational Claims)
    sellarsian = Column(JSON)
    # Structure: {
    #   "shared_givens": ["what both take for granted"],
    #   "contested_givens": ["where one questions the other's foundations"],
    #   "givenness_conflict": "description of foundational disagreement"
    # }

    # Brandomian Dimension (Inferential Commitments)
    brandomian = Column(JSON)
    # Structure: {
    #   "shared_commitments": ["what using both commits you to"],
    #   "conflicting_commitments": ["where commitments clash"],
    #   "entitlement_transfer": true/false - does entitlement to one give entitlement to other?
    # }

    # Deleuzian Dimension (Problematics)
    deleuzian = Column(JSON)
    # Structure: {
    #   "problematic_relation": "same|overlapping|nested|adjacent|different",
    #   "shared_tension": "description of shared problem/tension",
    #   "divergent_responses": "how they respond differently to same problem"
    # }

    # Hacking Dimension (Reasoning Styles)
    hacking = Column(JSON)
    # Structure: {
    #   "shared_styles": ["historical", "structural", etc.],
    #   "style_conflict": "description of reasoning style incompatibility",
    #   "compatibility": "high|medium|low|incompatible"
    # }

    # Bachelardian Dimension (Rupture/Continuity)
    bachelardian = Column(JSON)
    # Structure: {
    #   "rupture_direction": "A→B" or "B→A" or null,
    #   "what_is_ruptured": "what framework/assumption is broken",
    #   "continuity_despite_rupture": "what remains continuous"
    # }

    # Quinean Dimension (Web of Beliefs)
    quinean = Column(JSON)
    # Structure: {
    #   "web_proximity": "core|adjacent|peripheral|distant",
    #   "shared_inferences": ["inference patterns in common"],
    #   "inferential_bridges": ["how to get from one to other"]
    # }

    # Carey Dimension (Conceptual Combination/Components)
    carey = Column(JSON)
    # Structure: {
    #   "shared_components": ["component concepts in common"],
    #   "compositional_relation": "overlapping|disjoint|nested|emergent",
    #   "combination_notes": "how they combine or fail to"
    # }

    # Blumenberg Dimension (Metaphorical Grounds)
    blumenberg = Column(JSON)
    # Structure: {
    #   "shared_metaphors": ["mining", "harvesting", etc.],
    #   "metaphor_conflict": "where metaphorical grounds clash",
    #   "root_metaphor_relation": "description"
    # }

    # Canguilhem Dimension (Norms/Values/Interests)
    canguilhem = Column(JSON)
    # Structure: {
    #   "shared_interests": ["whose interests both serve"],
    #   "interest_conflict": "where normative commitments clash",
    #   "normative_stance_relation": "aligned|divergent|opposed"
    # }

    # ==========================================================================
    # Metadata and Provenance
    # ==========================================================================

    # How was this relationship identified?
    source_type = Column(String(50))  # "manual", "llm_extracted", "document_analysis"
    source_document_id = Column(Integer)  # If extracted from a document

    # Confidence in this relationship
    confidence = Column(Float, default=0.8)

    # Notes
    notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Ensure valid source/target combinations
    __table_args__ = (
        CheckConstraint(
            '(CASE WHEN concept_id IS NOT NULL THEN 1 ELSE 0 END + '
            'CASE WHEN external_concept_id IS NOT NULL THEN 1 ELSE 0 END) = 1',
            name='single_source_concept'
        ),
        CheckConstraint(
            '(CASE WHEN related_concept_id IS NOT NULL THEN 1 ELSE 0 END + '
            'CASE WHEN related_external_concept_id IS NOT NULL THEN 1 ELSE 0 END) = 1',
            name='single_target_concept'
        ),
    )

    # Relationships
    concept = relationship("Concept", foreign_keys=[concept_id])
    external_concept = relationship("ExternalConcept", foreign_keys=[external_concept_id], back_populates="relationships_as_source")
    related_concept = relationship("Concept", foreign_keys=[related_concept_id])
    related_external_concept = relationship("ExternalConcept", foreign_keys=[related_external_concept_id])
