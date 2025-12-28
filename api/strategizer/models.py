"""
Strategizer SQLAlchemy Models

Database models for the Strategizer system:
- Projects: Strategic projects with briefs
- Domains: Bootstrapped domain structures
- Units: Concepts, Dialectics, Actors
- Grids: Analytical grids applied to units
- Dialogue: Q&A conversation history
"""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum as PyEnum

from sqlalchemy import (
    Column, String, Text, DateTime, Boolean, Integer,
    ForeignKey, JSON, Enum, Index
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


def generate_uuid() -> str:
    """Generate a UUID string for primary keys."""
    return str(uuid.uuid4())


# =============================================================================
# ENUMS
# =============================================================================

class UnitType(str, PyEnum):
    """Universal unit types."""
    CONCEPT = "concept"
    DIALECTIC = "dialectic"
    ACTOR = "actor"


class UnitTier(str, PyEnum):
    """Unit tier in the three-tier system."""
    UNIVERSAL = "universal"
    DOMAIN = "domain"
    EMERGENT = "emergent"


class UnitStatus(str, PyEnum):
    """Unit lifecycle status."""
    DRAFT = "draft"
    TESTED = "tested"
    CANONICAL = "canonical"


class GridTier(str, PyEnum):
    """Grid tier in the three-tier system."""
    REQUIRED = "required"
    FLEXIBLE = "flexible"
    WILDCARD = "wildcard"


class DialogueTurnType(str, PyEnum):
    """Types of dialogue turns."""
    USER_QUESTION = "user_question"
    SYSTEM_RESPONSE = "system_response"
    SUGGESTION = "suggestion"


class EvidenceSourceType(str, PyEnum):
    """Types of evidence sources."""
    PDF = "pdf"
    URL = "url"
    MANUAL = "manual"


class ExtractionStatus(str, PyEnum):
    """Status of evidence extraction from a source."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AnalysisStatus(str, PyEnum):
    """Status of fragment analysis."""
    PENDING = "PENDING"
    ANALYZED = "ANALYZED"
    NEEDS_DECISION = "NEEDS_DECISION"
    INTEGRATED = "INTEGRATED"
    REJECTED = "REJECTED"


class EvidenceRelationship(str, PyEnum):
    """How evidence relates to a grid slot."""
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    EXTENDS = "extends"
    QUALIFIES = "qualifies"
    NEW_INSIGHT = "new_insight"


# =============================================================================
# PROJECTS
# =============================================================================

class StrategizerProject(Base):
    """
    A strategic project containing a domain and units.
    """
    __tablename__ = "strategizer_projects"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    brief = Column(Text, nullable=False)  # Original project description

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    domain = relationship("StrategizerDomain", back_populates="project", uselist=False, cascade="all, delete-orphan")
    units = relationship("StrategizerUnit", back_populates="project", cascade="all, delete-orphan")
    dialogue_turns = relationship("StrategizerDialogueTurn", back_populates="project", cascade="all, delete-orphan")


# =============================================================================
# DOMAINS
# =============================================================================

class StrategizerDomain(Base):
    """
    A bootstrapped domain structure for a project.
    Created by LLM analysis of the project brief.
    """
    __tablename__ = "strategizer_domains"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("strategizer_projects.id", ondelete="CASCADE"), nullable=False, unique=True)

    name = Column(String(255), nullable=False)  # e.g., "Climate Tech Investment"
    core_question = Column(Text)  # e.g., "Where to deploy capital for max climate impact?"
    success_looks_like = Column(Text)  # Description of success

    # Vocabulary mapping: {"concept": "Thesis", "dialectic": "Trade-off", "actor": "Player"}
    vocabulary = Column(JSON, default=dict)

    # Which template this was cloned from (theory, foundation, brand, government, investment, or None)
    template_base = Column(String(50), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    project = relationship("StrategizerProject", back_populates="domain")
    seed_content = relationship("StrategizerSeedContent", back_populates="domain", cascade="all, delete-orphan")


class StrategizerSeedContent(Base):
    """
    Seed content proposed during domain bootstrapping.
    User can accept or reject each piece.
    """
    __tablename__ = "strategizer_seed_content"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    domain_id = Column(String(36), ForeignKey("strategizer_domains.id", ondelete="CASCADE"), nullable=False)

    content_type = Column(String(50), nullable=False)  # 'concept', 'dialectic', 'actor', 'grid'
    content = Column(JSON, nullable=False)  # The full seed content

    accepted = Column(Boolean, default=None)  # None = pending, True = accepted, False = rejected

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    domain = relationship("StrategizerDomain", back_populates="seed_content")


# =============================================================================
# UNITS
# =============================================================================

class StrategizerUnit(Base):
    """
    A strategic unit: Concept, Dialectic, or Actor.
    """
    __tablename__ = "strategizer_units"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("strategizer_projects.id", ondelete="CASCADE"), nullable=False)

    # Unit identity
    unit_type = Column(Enum(UnitType), nullable=False)
    display_type = Column(String(100))  # Domain-specific name (e.g., "Thesis", "Trade-off")
    tier = Column(Enum(UnitTier), default=UnitTier.DOMAIN)

    # Core content
    name = Column(String(255), nullable=False)
    definition = Column(Text)
    content = Column(JSON, default=dict)  # Type-specific content

    # Status
    status = Column(Enum(UnitStatus), default=UnitStatus.DRAFT)
    version = Column(Integer, default=1)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("StrategizerProject", back_populates="units")
    grids = relationship("StrategizerGridInstance", back_populates="unit", cascade="all, delete-orphan")

    # Indices
    __table_args__ = (
        Index("idx_strategizer_units_project", "project_id"),
        Index("idx_strategizer_units_type", "unit_type"),
    )


# =============================================================================
# GRIDS
# =============================================================================

class StrategizerGridInstance(Base):
    """
    A grid instance applied to a unit.
    Grids are analytical lenses with slots to fill.
    """
    __tablename__ = "strategizer_grid_instances"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    unit_id = Column(String(36), ForeignKey("strategizer_units.id", ondelete="CASCADE"), nullable=False)

    grid_type = Column(String(100), nullable=False)  # 'LOGICAL', 'ACTOR', 'TEMPORAL', etc.
    tier = Column(Enum(GridTier), default=GridTier.REQUIRED)

    # Slot content: {"slot_name": {"content": "...", "confidence": 0.8, ...}}
    slots = Column(JSON, default=dict)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    unit = relationship("StrategizerUnit", back_populates="grids")

    # Indices
    __table_args__ = (
        Index("idx_strategizer_grids_unit", "unit_id"),
    )


# =============================================================================
# DIALOGUE
# =============================================================================

class StrategizerDialogueTurn(Base):
    """
    A turn in the Q&A dialogue.
    """
    __tablename__ = "strategizer_dialogue_turns"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("strategizer_projects.id", ondelete="CASCADE"), nullable=False)
    unit_id = Column(String(36), ForeignKey("strategizer_units.id", ondelete="SET NULL"), nullable=True)

    # Dialogue content
    turn_type = Column(Enum(DialogueTurnType), nullable=False)
    content = Column(Text, nullable=False)
    context = Column(JSON, default=dict)  # Additional context

    # Actions
    actions_proposed = Column(JSON, default=list)  # What the system suggested
    actions_taken = Column(JSON, default=list)  # What was actually executed

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    project = relationship("StrategizerProject", back_populates="dialogue_turns")

    # Indices
    __table_args__ = (
        Index("idx_strategizer_dialogue_project", "project_id"),
    )


# =============================================================================
# EVIDENCE
# =============================================================================

class StrategizerEvidenceSource(Base):
    """
    An external source of evidence (PDF, URL, manual input).
    Evidence is extracted into fragments for analysis.
    """
    __tablename__ = "strategizer_evidence_sources"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("strategizer_projects.id", ondelete="CASCADE"), nullable=False)

    source_type = Column(Enum(EvidenceSourceType), nullable=False)
    source_name = Column(String(500), nullable=False)  # Filename, URL, or title
    source_url = Column(String(1000))
    source_content = Column(Text)  # Full text content

    extraction_status = Column(Enum(ExtractionStatus), default=ExtractionStatus.PENDING)
    extraction_error = Column(Text)
    extracted_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("StrategizerProject", backref="evidence_sources")
    fragments = relationship("StrategizerEvidenceFragment", back_populates="source", cascade="all, delete-orphan")

    # Indices
    __table_args__ = (
        Index("idx_strategizer_evidence_source_project", "project_id"),
    )


class StrategizerEvidenceFragment(Base):
    """
    An extracted claim/insight from an evidence source.
    Analyzed for relationship to grid slots.
    """
    __tablename__ = "strategizer_evidence_fragments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    source_id = Column(String(36), ForeignKey("strategizer_evidence_sources.id", ondelete="CASCADE"), nullable=False)

    content = Column(Text, nullable=False)  # The extracted claim/insight
    source_location = Column(String(200))  # Page, paragraph, etc.
    extraction_metadata = Column(JSON)  # Additional extraction info

    # Analysis results
    analysis_status = Column(Enum(AnalysisStatus), default=AnalysisStatus.PENDING)
    relationship_type = Column(Enum(EvidenceRelationship))
    target_unit_id = Column(String(36), ForeignKey("strategizer_units.id", ondelete="SET NULL"))
    target_grid_slot = Column(String(100))  # "GRID_TYPE.slot_name" format
    confidence = Column(Integer)  # 0-100 confidence score
    is_ambiguous = Column(Boolean, default=False)
    why_needs_decision = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    source = relationship("StrategizerEvidenceSource", back_populates="fragments")
    interpretations = relationship("StrategizerEvidenceInterpretation", back_populates="fragment", cascade="all, delete-orphan")

    # Indices
    __table_args__ = (
        Index("idx_strategizer_fragment_source", "source_id"),
        Index("idx_strategizer_fragment_status", "analysis_status"),
    )


class StrategizerEvidenceInterpretation(Base):
    """
    A possible interpretation of an ambiguous evidence fragment.
    When confidence is low, LLM proposes 2-4 interpretations for user choice.
    """
    __tablename__ = "strategizer_evidence_interpretations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    fragment_id = Column(String(36), ForeignKey("strategizer_evidence_fragments.id", ondelete="CASCADE"), nullable=False)

    interpretation_key = Column(String(10))  # 'a', 'b', 'c', 'd'
    title = Column(String(200), nullable=False)
    strategy = Column(Text)  # How this interpretation would integrate
    rationale = Column(Text)  # Why this interpretation makes sense

    # Target slot for this interpretation
    relationship_type = Column(Enum(EvidenceRelationship))
    target_unit_id = Column(String(36), ForeignKey("strategizer_units.id", ondelete="SET NULL"))
    target_grid_slot = Column(String(100))
    is_recommended = Column(Boolean, default=False)

    # Commitment/foreclosure analysis
    commitment_statement = Column(Text)  # What you're committing to if chosen
    foreclosure_statements = Column(JSON)  # What you're giving up if chosen

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    fragment = relationship("StrategizerEvidenceFragment", back_populates="interpretations")

    # Indices
    __table_args__ = (
        Index("idx_strategizer_interp_fragment", "fragment_id"),
    )


class StrategizerEvidenceDecision(Base):
    """
    A user decision on an ambiguous evidence fragment.
    Records which interpretation was chosen and why.
    """
    __tablename__ = "strategizer_evidence_decisions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    fragment_id = Column(String(36), ForeignKey("strategizer_evidence_fragments.id", ondelete="CASCADE"), nullable=False)
    interpretation_id = Column(String(36), ForeignKey("strategizer_evidence_interpretations.id", ondelete="SET NULL"))

    decision_type = Column(String(50), nullable=False)  # 'accept_interpretation', 'reject_all', 'manual_override'
    decision_notes = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Indices
    __table_args__ = (
        Index("idx_strategizer_decision_fragment", "fragment_id"),
    )


# =============================================================================
# PREDICAMENTS (Theoretical Coherence Monitoring)
# =============================================================================

class PredicamentType(str, PyEnum):
    """Types of predicaments detected by the coherence monitor."""
    THEORETICAL = "theoretical"  # Unresolved tensions in assumptions
    EMPIRICAL = "empirical"      # Gap between theory and observed reality
    CONCEPTUAL = "conceptual"    # Concept doesn't carve reality well
    PRAXIS = "praxis"            # Theory can't guide action


class PredicamentSeverity(str, PyEnum):
    """How critical is this predicament to address."""
    LOW = "low"           # Minor inconsistency, can ignore
    MEDIUM = "medium"     # Worth addressing when convenient
    HIGH = "high"         # Should address before finalizing framework
    CRITICAL = "critical" # Fundamental flaw requiring immediate attention


class PredicamentStatus(str, PyEnum):
    """Lifecycle status of a predicament."""
    DETECTED = "detected"    # Just found by coherence monitor
    ANALYZING = "analyzing"  # Has a generated grid, being worked on
    RESOLVED = "resolved"    # Transformed into a dialectic
    DEFERRED = "deferred"    # Acknowledged but not resolved now


class StrategizerPredicament(Base):
    """
    A detected tension, gap, or inconsistency in the theoretical framework.

    Predicaments are detected by the Coherence Monitor and represent:
    - THEORETICAL: Conflicts between concepts/assumptions
    - EMPIRICAL: Reality that theory can't explain
    - CONCEPTUAL: Categories that don't carve reality well
    - PRAXIS: Theory that can't guide action

    Resolution path: Predicament → Analytical Grid → Analysis → Dialectic → Learning
    """
    __tablename__ = "strategizer_predicaments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("strategizer_projects.id", ondelete="CASCADE"), nullable=False)

    # Predicament identity
    title = Column(String(255), nullable=False)  # e.g., "State vs. Lab Power Tension"
    description = Column(Text, nullable=False)   # Full description of the predicament
    predicament_type = Column(Enum(PredicamentType), nullable=False)
    severity = Column(Enum(PredicamentSeverity), default=PredicamentSeverity.MEDIUM)
    status = Column(Enum(PredicamentStatus), default=PredicamentStatus.DETECTED)

    # The two poles of tension (for dialectical predicaments)
    pole_a = Column(Text)  # First side of the tension
    pole_b = Column(Text)  # Second side of the tension

    # Source tracking: which units/evidence surfaced this predicament
    source_unit_ids = Column(JSON, default=list)     # List of unit IDs involved
    source_evidence_ids = Column(JSON, default=list) # List of fragment IDs that revealed this

    # Resolution
    generated_grid_id = Column(String(36), ForeignKey("strategizer_grid_instances.id", ondelete="SET NULL"))
    resolution_notes = Column(Text)  # How it was resolved / why deferred
    resulting_dialectic_id = Column(String(36), ForeignKey("strategizer_units.id", ondelete="SET NULL"))

    # Notes: insights saved from cell actions
    # Format: [{"id": "uuid", "title": "...", "content": {...}, "action": {...}, "cells": [...], "created_at": "..."}]
    notes = Column(JSON, default=list)

    # Timestamps
    detected_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("StrategizerProject", backref="predicaments")
    generated_grid = relationship("StrategizerGridInstance", foreign_keys=[generated_grid_id])
    resulting_dialectic = relationship("StrategizerUnit", foreign_keys=[resulting_dialectic_id])

    # Indices
    __table_args__ = (
        Index("idx_strategizer_predicament_project", "project_id"),
        Index("idx_strategizer_predicament_status", "status"),
        Index("idx_strategizer_predicament_type", "predicament_type"),
    )
