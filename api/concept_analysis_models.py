"""
Operation-Indexed Concept Analysis Models

This schema organizes concept analysis by ANALYTICAL OPERATION rather than by thinker.
Each dimension groups related operations; thinkers become metadata references.
"""

from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean, DateTime,
    ForeignKey, Enum, JSON, Table, UniqueConstraint
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()


# ==================== ENUMS ====================

class DimensionType(str, enum.Enum):
    """The 8 analytical dimensions."""
    POSITIONAL = "positional"
    GENEALOGICAL = "genealogical"
    PRESUPPOSITIONAL = "presuppositional"
    COMMITMENT = "commitment"
    AFFORDANCE = "affordance"
    NORMALIZATION = "normalization"
    BOUNDARY = "boundary"
    DYNAMIC = "dynamic"


class OutputType(str, enum.Enum):
    """Types of analytical output."""
    INFERENCE_MAP = "inference_map"
    PARADIGM_ASSESSMENT = "paradigm_assessment"
    DISCOURSE_MAP = "discourse_map"
    CENTRALITY_SCORE = "centrality_score"
    BOOTSTRAP_TREE = "bootstrap_tree"
    EMERGENCE_NARRATIVE = "emergence_narrative"
    RUPTURE_ASSESSMENT = "rupture_assessment"
    METAPHOR_ANALYSIS = "metaphor_analysis"
    PREDECESSOR_LIST = "predecessor_list"
    GIVENNESS_LIST = "givenness_list"
    ASSUMPTION_INVENTORY = "assumption_inventory"
    OBSTACLE_ASSESSMENT = "obstacle_assessment"
    TENSION_ANALYSIS = "tension_analysis"
    COMMITMENT_LIST = "commitment_list"
    NORMATIVE_ENTAILMENTS = "normative_entailments"
    INCOMPATIBILITY_MAP = "incompatibility_map"
    ENTITLEMENT_LIST = "entitlement_list"
    TRANSFORMATION_VECTORS = "transformation_vectors"
    PRACTICAL_EFFECTS = "practical_effects"
    VISIBILITY_MAP = "visibility_map"
    VOCABULARY_ADDITIONS = "vocabulary_additions"
    INQUIRY_STRUCTURE = "inquiry_structure"
    EMBEDDED_NORMS = "embedded_norms"
    PATHOLOGICAL_BOUNDARIES = "pathological_boundaries"
    NATURALIZED_POWER = "naturalized_power"
    AUTHORITY_MAP = "authority_map"
    GOVERNMENTALITY_ANALYSIS = "governmentality_analysis"
    TRUTH_REGIME = "truth_regime"
    ANOMALY_LIST = "anomaly_list"
    CONTRADICTION_MAP = "contradiction_map"
    INCOMMENSURABILITY_ASSESSMENT = "incommensurability_assessment"
    GRAY_ZONES = "gray_zones"
    CRISIS_INDICATORS = "crisis_indicators"
    LOOPING_EFFECTS = "looping_effects"
    HABIT_INVENTORY = "habit_inventory"
    REVISION_CONDITIONS = "revision_conditions"
    KIND_CREATION = "kind_creation"
    MATRIX_EVOLUTION = "matrix_evolution"


class SourceType(str, enum.Enum):
    """Source of an analysis entry."""
    USER_AUTHORED = "user_authored"
    LLM_GENERATED = "llm_generated"
    IMPORTED = "imported"
    SYNTHESIZED = "synthesized"


# ==================== JUNCTION TABLES ====================

# Many-to-many: Operation <-> Theoretical Influence
operation_influences = Table(
    'ca_operation_influences',
    Base.metadata,
    Column('operation_id', Integer, ForeignKey('ca_analytical_operations.id'), primary_key=True),
    Column('influence_id', Integer, ForeignKey('ca_theoretical_influences.id'), primary_key=True),
    Column('contribution_note', Text),  # How this thinker contributes to this operation
)


# ==================== CORE SCHEMA TABLES ====================

class AnalyticalDimension(Base):
    """
    The 8 analytical dimensions - top-level categories.
    These are mostly static/reference data.
    """
    __tablename__ = 'ca_analytical_dimensions'

    id = Column(Integer, primary_key=True)
    dimension_type = Column(Enum(DimensionType), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    core_question = Column(Text, nullable=False)
    description = Column(Text)
    color_scheme = Column(String(20))  # CSS color for UI
    icon = Column(String(50))  # Icon identifier
    sequence_order = Column(Integer, default=0)

    # Relationships
    operations = relationship("AnalyticalOperation", back_populates="dimension")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class TheoreticalInfluence(Base):
    """
    Thinkers who inform the analytical operations.
    Reference data - linked to operations via junction table.
    """
    __tablename__ = 'ca_theoretical_influences'

    id = Column(Integer, primary_key=True)
    short_name = Column(String(50), unique=True, nullable=False)  # e.g., "Quine"
    full_name = Column(String(200), nullable=False)  # e.g., "Willard Van Orman Quine"
    years = Column(String(50))  # e.g., "1908-2000"
    key_works = Column(JSON)  # List of key works
    core_insight = Column(Text)
    wikipedia_url = Column(String(500))

    # Relationships
    operations = relationship(
        "AnalyticalOperation",
        secondary=operation_influences,
        back_populates="influences"
    )

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class AnalyticalOperation(Base):
    """
    Specific analytical operations within dimensions.
    These define WHAT you do to analyze a concept.
    """
    __tablename__ = 'ca_analytical_operations'

    id = Column(Integer, primary_key=True)
    dimension_id = Column(Integer, ForeignKey('ca_analytical_dimensions.id'), nullable=False)

    name = Column(String(100), nullable=False)
    description = Column(Text)
    key_questions = Column(JSON)  # List of guiding questions
    output_type = Column(Enum(OutputType))
    example_prompt = Column(Text)  # Example prompt for LLM
    sequence_order = Column(Integer, default=0)

    # Relationships
    dimension = relationship("AnalyticalDimension", back_populates="operations")
    influences = relationship(
        "TheoreticalInfluence",
        secondary=operation_influences,
        back_populates="operations"
    )
    analyses = relationship("ConceptAnalysis", back_populates="operation")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('dimension_id', 'name', name='uq_dimension_operation'),
    )


# ==================== CONCEPT TABLES ====================

class AnalyzedConcept(Base):
    """
    A concept being analyzed through the 8-dimensional framework.
    """
    __tablename__ = 'ca_analyzed_concepts'

    id = Column(Integer, primary_key=True)
    term = Column(String(200), nullable=False)
    definition = Column(Text)
    author = Column(String(200))  # Who created/uses this concept
    source_work = Column(String(500))
    year = Column(Integer)

    # Metadata
    is_user_concept = Column(Boolean, default=True)  # User's own vs. external
    paradigm = Column(String(200))
    disciplinary_home = Column(String(200))

    # Relationships
    analyses = relationship("ConceptAnalysis", back_populates="concept")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class ConceptAnalysis(Base):
    """
    The actual analysis - one per concept per operation.
    This is where the substantive content lives.
    """
    __tablename__ = 'ca_concept_analyses'

    id = Column(Integer, primary_key=True)
    concept_id = Column(Integer, ForeignKey('ca_analyzed_concepts.id'), nullable=False)
    operation_id = Column(Integer, ForeignKey('ca_analytical_operations.id'), nullable=False)

    # Core content
    canonical_statement = Column(Text)  # One-sentence summary
    analysis_data = Column(JSON)  # Structured analysis content

    # Metadata
    version = Column(String(20), default="1.0")
    confidence = Column(Float, default=0.8)
    source_type = Column(Enum(SourceType), default=SourceType.LLM_GENERATED)
    notes = Column(Text)

    # Relationships
    concept = relationship("AnalyzedConcept", back_populates="analyses")
    operation = relationship("AnalyticalOperation", back_populates="analyses")
    history = relationship("ConceptAnalysisHistory", back_populates="analysis")
    items = relationship("AnalysisItem", back_populates="analysis")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('concept_id', 'operation_id', name='uq_concept_operation'),
    )


class ConceptAnalysisHistory(Base):
    """
    Version history for analyses - tracks changes over time.
    """
    __tablename__ = 'ca_concept_analysis_history'

    id = Column(Integer, primary_key=True)
    analysis_id = Column(Integer, ForeignKey('ca_concept_analyses.id'), nullable=False)

    version = Column(String(20), nullable=False)
    canonical_statement = Column(Text)
    analysis_data = Column(JSON)
    confidence = Column(Float)
    change_type = Column(String(50))  # e.g., "revision", "correction", "expansion"
    change_notes = Column(Text)
    changed_by = Column(String(100))

    # Relationship
    analysis = relationship("ConceptAnalysis", back_populates="history")

    created_at = Column(DateTime, server_default=func.now())


# ==================== STRUCTURED ANALYSIS ITEMS ====================
# These tables store the individual items that make up an analysis
# (e.g., individual inferences, individual commitments, etc.)

class AnalysisItem(Base):
    """
    Individual items within an analysis.
    Normalized storage for things like:
    - Individual inferences
    - Individual commitments
    - Individual anomalies
    - etc.
    """
    __tablename__ = 'ca_analysis_items'

    id = Column(Integer, primary_key=True)
    analysis_id = Column(Integer, ForeignKey('ca_concept_analyses.id'), nullable=False)

    item_type = Column(String(50), nullable=False)  # e.g., "forward_inference", "commitment", "anomaly"
    content = Column(Text, nullable=False)  # Main content

    # Common optional fields
    strength = Column(Float)  # 0-1 strength/confidence
    severity = Column(String(20))  # e.g., "hard", "soft", "high", "low"
    subtype = Column(String(50))  # Additional categorization

    # Rich extra data as JSON for type-specific fields
    extra_data = Column(JSON)

    sequence_order = Column(Integer, default=0)

    # Relationship
    analysis = relationship("ConceptAnalysis", back_populates="items")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


# ==================== HELPER FUNCTIONS ====================

def get_dimension_color(dimension_type: DimensionType) -> str:
    """Return CSS color for a dimension."""
    colors = {
        DimensionType.POSITIONAL: '#E3F2FD',       # Blue
        DimensionType.GENEALOGICAL: '#FFF3E0',     # Orange
        DimensionType.PRESUPPOSITIONAL: '#FCE4EC', # Pink
        DimensionType.COMMITMENT: '#F3E5F5',       # Purple
        DimensionType.AFFORDANCE: '#E8F5E9',       # Green
        DimensionType.NORMALIZATION: '#FFEBEE',    # Red
        DimensionType.BOUNDARY: '#E0F7FA',         # Cyan
        DimensionType.DYNAMIC: '#FFF8E1',          # Amber
    }
    return colors.get(dimension_type, '#FFFFFF')
