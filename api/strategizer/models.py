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
