"""
Theory Service - Database Models
SQLAlchemy models for the Theory knowledge base.
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean,
    ForeignKey, Enum, Float, JSON, Table
)
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
    source_cluster_id = Column(Integer)  # evidence cluster that generated this
    source_cluster_name = Column(String(255))

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
