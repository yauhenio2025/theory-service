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


class EvidenceSourceType(str, enum.Enum):
    """Types of evidence sources."""
    ARTICLE = "article"
    BOOK = "book"
    NEWS = "news"
    THINKER_WORK = "thinker_work"
    URL = "url"
    MANUAL = "manual"


class ExtractionStatus(str, enum.Enum):
    """Status of evidence extraction from a source."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AnalysisStatus(str, enum.Enum):
    """Status of fragment analysis."""
    PENDING = "pending"
    ANALYZED = "analyzed"
    NEEDS_DECISION = "needs_decision"
    RESOLVED = "resolved"
    AUTO_INTEGRATED = "auto_integrated"


class EvidenceRelationship(str, enum.Enum):
    """How evidence relates to existing analysis (Idea Vectors)."""
    ILLUSTRATES = "illustrates"  # Concrete example making abstract vivid
    DEEPENS = "deepens"          # Adds nuance or complexity
    CHALLENGES = "challenges"    # Contradicts premise, requires revision
    LIMITS = "limits"            # Establishes scope boundary
    BRIDGES = "bridges"          # Connects previously unlinked operations
    INVERTS = "inverts"          # Flips assumed relationship


class ChangeType(str, enum.Enum):
    """Types of structural changes from evidence."""
    REVISION = "revision"
    ADDITION = "addition"
    STRENGTHENING = "strengthening"
    SCOPE_LIMITATION = "scope_limitation"
    DELETION = "deletion"


class ProvenanceType(str, enum.Enum):
    """Origin type for analysis items."""
    WIZARD = "wizard"
    EVIDENCE = "evidence"
    USER_MANUAL = "user_manual"
    LLM_SYNTHESIS = "llm_synthesis"


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

class WebCentrality(str, enum.Enum):
    """Quinean web of belief position - how central vs peripheral."""
    CORE = "core"          # Foundational, revision requires massive restructuring
    HIGH = "high"          # Important, revision affects many connected beliefs
    MEDIUM = "medium"      # Moderate importance, some connections
    PERIPHERAL = "peripheral"  # Edge beliefs, easily revisable


class InferenceType(str, enum.Enum):
    """Type of inferential move."""
    DEDUCTIVE = "deductive"        # Logically necessary
    MATERIAL = "material"          # Content-based, norm-governed
    DEFAULT = "default"            # Defeasible, can be overridden
    ABDUCTIVE = "abductive"        # Inference to best explanation
    ANALOGICAL = "analogical"      # From similar cases
    TRANSCENDENTAL = "transcendental"  # Conditions of possibility


class ItemRelationType(str, enum.Enum):
    """Types of relationships between analysis items.

    These capture the inferential web structure - how items depend on,
    support, contradict, or create tension with each other.
    """
    DEPENDS_ON = "depends_on"        # This item requires that item to be true
    SUPPORTS = "supports"            # This item provides evidence for that item
    CONTRADICTS = "contradicts"      # Logical incompatibility
    TENSION_WITH = "tension_with"    # Not contradictory but creates pressure
    ENABLES = "enables"              # This item makes that item possible/meaningful
    SUPERSEDES = "supersedes"        # This item replaces/updates that item
    SPECIALIZES = "specializes"      # This is a more specific version of that
    GENERALIZES = "generalizes"      # This is a more general version of that


class RelationshipSource(str, enum.Enum):
    """How a relationship was discovered/created."""
    WIZARD_GENERATED = "wizard_generated"      # From concept wizard LLM
    EVIDENCE_EXTRACTED = "evidence_extracted"  # From evidence integration
    LLM_INFERRED = "llm_inferred"              # From batch relationship inference
    USER_CURATED = "user_curated"              # Manual user input
    SYSTEM_DETECTED = "system_detected"        # Auto-detected (e.g., text matching)


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

    # ========== QUINEAN WEB OF BELIEF FIELDS ==========
    # These fields capture the item's position in the inferential web
    web_centrality = Column(Enum(WebCentrality))  # Core → Peripheral
    observation_proximity = Column(Float)  # 0-1: how close to empirical grounding
    coherence_score = Column(Float)  # 0-1: how well it fits the web

    # Provenance fields - track where this item came from
    provenance_type = Column(Enum(ProvenanceType), default=ProvenanceType.WIZARD)
    provenance_source_id = Column(Integer)  # FK to evidence_fragment or wizard_session
    provenance_decision_id = Column(Integer)  # FK to evidence_decision if from resolution
    created_via = Column(String(50))  # 'initial_wizard', 'evidence_auto_integrate', 'evidence_decision', 'manual_edit'
    supersedes_item_id = Column(Integer, ForeignKey('ca_analysis_items.id'))  # If this replaced another item
    is_active = Column(Boolean, default=True)  # False if superseded by another item

    # Relationships
    analysis = relationship("ConceptAnalysis", back_populates="items")
    superseded_by = relationship("AnalysisItem", remote_side=[id], backref="supersedes")
    reasoning_scaffold = relationship("ItemReasoningScaffold", back_populates="item", uselist=False, cascade="all, delete-orphan")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class ItemReasoningScaffold(Base):
    """
    Quinean Intermediate Reasoning Layer.

    Captures the full reasoning scaffold for how an AnalysisItem was derived:
    - What premises it follows from
    - What inference type was used
    - Why this conclusion vs alternatives
    - What would need to change if revised (revisability cost)
    - Source context that triggered it

    This makes LLM reasoning visible, auditable, and improvable.
    """
    __tablename__ = 'ca_item_reasoning_scaffolds'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('ca_analysis_items.id'), nullable=False, unique=True)

    # ========== DERIVATION CHAIN ==========
    # The inferential pathway from premises to conclusion

    inference_type = Column(Enum(InferenceType))  # How the inference was made
    inference_rule = Column(String(100))  # Specific rule if applicable (modus_ponens, etc.)

    # Premises as structured JSON array:
    # [{
    #   "claim": "Tech sovereignty requires domestic capacity",
    #   "claim_type": "definitional|empirical|normative",
    #   "centrality": "core|high|medium|peripheral",
    #   "source": "concept_definition|user_notes|external"
    # }]
    premises = Column(JSON)

    # The reasoning trace - natural language explanation of the inferential move
    reasoning_trace = Column(Text)

    # ========== SOURCE CONTEXT ==========
    # What triggered this item - provenance with visibility

    derivation_trigger = Column(String(50))  # 'user_notes', 'external_article', 'concept_definition', 'prior_inference'
    source_passage = Column(Text)  # The specific text that triggered this
    source_location = Column(String(200))  # Where in the source (paragraph, page, section)

    # ========== ALTERNATIVES CONSIDERED ==========
    # What other inferences could have been drawn but weren't
    # [{
    #   "inference": "Private sector could handle this",
    #   "rejected_because": "Conflicts with sovereignty's state-role emphasis",
    #   "plausibility": 0.4
    # }]
    alternatives_rejected = Column(JSON)

    # ========== STRENGTH DECOMPOSITION ==========
    # Why the confidence score is what it is

    # Individual factors that compose the final strength
    premise_confidence = Column(Float)      # 0-1: confidence in the premises
    inference_validity = Column(Float)      # 0-1: strength of the inferential move
    source_quality = Column(Float)          # 0-1: quality/reliability of the source
    web_coherence = Column(Float)           # 0-1: how well it fits the belief web

    # Natural language explanation of confidence
    confidence_explanation = Column(Text)

    # ========== REVISABILITY / WHAT-IF ==========
    # Quinean: what would need to change if this were rejected

    revisability_cost = Column(Text)  # Natural language description
    # Claims that would need revision if this item were rejected
    # ["If rejected, must revise claim X", "Would require new explanation for Y"]
    dependent_claims = Column(JSON)

    # ========== WEB CONNECTIONS ==========
    # What this item connects to in the inferential web

    # IDs of other items this directly supports
    supports_items = Column(JSON)  # [item_id, item_id, ...]
    # IDs of other items this is supported by
    supported_by_items = Column(JSON)  # [item_id, item_id, ...]
    # IDs of items this is in tension with
    tension_with_items = Column(JSON)  # [item_id, item_id, ...]

    # Relationship
    item = relationship("AnalysisItem", back_populates="reasoning_scaffold")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


# ==================== ITEM RELATIONSHIPS ====================
# Proper item-to-item relationship tracking with provenance

class ItemRelationship(Base):
    """
    Tracks relationships between analysis items.

    This is the proper way to represent "depends on", "supports", etc.
    Each relationship has:
    - Source and target items
    - Relationship type (depends_on, supports, contradicts, etc.)
    - How it was discovered (wizard, evidence, LLM inference, manual)
    - Confidence and explanation

    Population strategies:
    1. WIZARD_GENERATED: When generating inferences, LLM identifies what
       premises/items the inference depends on
    2. EVIDENCE_EXTRACTED: When processing articles/papers, identify which
       existing items are affected
    3. LLM_INFERRED: Batch job that analyzes all items for relationships
    4. USER_CURATED: Manual user input through UI
    5. SYSTEM_DETECTED: Auto-detected via text similarity, semantic matching
    """
    __tablename__ = 'ca_item_relationships'

    id = Column(Integer, primary_key=True)

    # The item that has the relationship
    source_item_id = Column(Integer, ForeignKey('ca_analysis_items.id'), nullable=False)
    # The item it relates to
    target_item_id = Column(Integer, ForeignKey('ca_analysis_items.id'), nullable=False)

    # What type of relationship
    relationship_type = Column(Enum(ItemRelationType), nullable=False)

    # How was this relationship discovered
    discovered_via = Column(Enum(RelationshipSource), nullable=False)

    # Confidence in this relationship (0-1)
    confidence = Column(Float, default=0.8)

    # Natural language explanation of why this relationship holds
    explanation = Column(Text)

    # Optional: If from evidence, which fragment triggered it
    evidence_fragment_id = Column(Integer, ForeignKey('ca_evidence_fragments.id'), nullable=True)

    # Is this relationship still valid (can be invalidated without deletion)
    is_active = Column(Boolean, default=True)

    # Who/what created this
    created_by = Column(String(100))  # 'wizard', 'evidence_processor', 'user:email', etc.

    # Relationships
    source_item = relationship(
        "AnalysisItem",
        foreign_keys=[source_item_id],
        backref="outgoing_relationships"
    )
    target_item = relationship(
        "AnalysisItem",
        foreign_keys=[target_item_id],
        backref="incoming_relationships"
    )

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Prevent duplicate relationships
    __table_args__ = (
        UniqueConstraint('source_item_id', 'target_item_id', 'relationship_type',
                        name='uq_item_relationship'),
    )


# ==================== EVIDENCE INTEGRATION TABLES ====================
# These tables support evidence-driven concept refinement

class ConceptEvidenceSource(Base):
    """
    An external source of evidence (article, book, news, etc.).
    Evidence is extracted into fragments for analysis.
    """
    __tablename__ = 'ca_evidence_sources'

    id = Column(Integer, primary_key=True)
    concept_id = Column(Integer, ForeignKey('ca_analyzed_concepts.id'), nullable=False)

    source_type = Column(Enum(EvidenceSourceType), nullable=False)
    source_name = Column(String(500), nullable=False)  # "Zuboff, S. - Surveillance Capitalism"
    source_url = Column(String(1000))
    source_date = Column(DateTime)
    source_content = Column(Text)  # Full text or summary

    extraction_status = Column(Enum(ExtractionStatus), default=ExtractionStatus.PENDING)
    extraction_error = Column(Text)  # Error message if failed
    extracted_count = Column(Integer, default=0)  # Number of fragments extracted

    # Relationships
    concept = relationship("AnalyzedConcept", backref="evidence_sources")
    fragments = relationship("ConceptEvidenceFragment", back_populates="source", cascade="all, delete-orphan")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class ConceptEvidenceFragment(Base):
    """
    An extracted claim/insight from an evidence source.
    Analyzed for relationship to existing concept analysis.
    """
    __tablename__ = 'ca_evidence_fragments'

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey('ca_evidence_sources.id'), nullable=False)

    content = Column(Text, nullable=False)  # The extracted claim/insight
    source_location = Column(String(200))  # page, paragraph, timestamp
    extraction_metadata = Column(JSON)  # Additional extraction info (likely_dimension, extraction_note)

    # Analysis results
    analysis_status = Column(Enum(AnalysisStatus), default=AnalysisStatus.PENDING)
    relationship_type = Column(Enum(EvidenceRelationship))
    target_operation_id = Column(Integer, ForeignKey('ca_analytical_operations.id'))
    target_item_id = Column(Integer, ForeignKey('ca_analysis_items.id'))
    confidence = Column(Float)  # 0.0-1.0
    is_ambiguous = Column(Boolean, default=False)
    why_needs_decision = Column(Text)  # LLM explanation if ambiguous

    # Relationships
    source = relationship("ConceptEvidenceSource", back_populates="fragments")
    target_operation = relationship("AnalyticalOperation")
    target_item = relationship("AnalysisItem")
    interpretations = relationship("ConceptEvidenceInterpretation", back_populates="fragment", cascade="all, delete-orphan")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class ConceptEvidenceInterpretation(Base):
    """
    A possible interpretation of ambiguous evidence.
    Multiple interpretations allow user to choose how to integrate.
    """
    __tablename__ = 'ca_evidence_interpretations'

    id = Column(Integer, primary_key=True)
    fragment_id = Column(Integer, ForeignKey('ca_evidence_fragments.id'), nullable=False)
    interpretation_key = Column(String(10))  # 'a', 'b', 'c'

    title = Column(String(200), nullable=False)  # "Reading A: Revise the commitment"
    strategy = Column(Text)  # What this interpretation means
    rationale = Column(Text)  # Why this reading is valid

    relationship_type = Column(Enum(EvidenceRelationship))
    target_operation_id = Column(Integer, ForeignKey('ca_analytical_operations.id'))
    is_selected = Column(Boolean, default=False)
    is_recommended = Column(Boolean, default=False)
    recommendation_rationale = Column(Text)

    display_order = Column(Integer, default=0)

    # Relationships
    fragment = relationship("ConceptEvidenceFragment", back_populates="interpretations")
    target_operation = relationship("AnalyticalOperation")
    structural_changes = relationship("ConceptStructuralChange", back_populates="interpretation", cascade="all, delete-orphan")

    created_at = Column(DateTime, server_default=func.now())


class ConceptStructuralChange(Base):
    """
    A specific change to the concept analysis proposed by an interpretation.
    Includes before/after diff and commitment/foreclosure statements.
    """
    __tablename__ = 'ca_structural_changes'

    id = Column(Integer, primary_key=True)
    interpretation_id = Column(Integer, ForeignKey('ca_evidence_interpretations.id'), nullable=False)

    change_type = Column(Enum(ChangeType), nullable=False)
    target_operation_id = Column(Integer, ForeignKey('ca_analytical_operations.id'))
    target_item_id = Column(Integer, ForeignKey('ca_analysis_items.id'))

    before_content = Column(Text)  # Current state (null for additions)
    after_content = Column(Text)   # Proposed new state (null for deletions)

    commitment_statement = Column(Text)   # What you're committing to
    foreclosure_statements = Column(JSON) # What you're giving up (array of strings)

    display_order = Column(Integer, default=0)

    # Relationships
    interpretation = relationship("ConceptEvidenceInterpretation", back_populates="structural_changes")
    target_operation = relationship("AnalyticalOperation")
    target_item = relationship("AnalysisItem")

    created_at = Column(DateTime, server_default=func.now())


class ConceptEvidenceDecision(Base):
    """
    A user's decision on how to integrate ambiguous evidence.
    Links fragment to chosen interpretation and applied changes.
    """
    __tablename__ = 'ca_evidence_decisions'

    id = Column(Integer, primary_key=True)
    concept_id = Column(Integer, ForeignKey('ca_analyzed_concepts.id'), nullable=False)
    fragment_id = Column(Integer, ForeignKey('ca_evidence_fragments.id'), nullable=False)

    selected_interpretation_id = Column(Integer, ForeignKey('ca_evidence_interpretations.id'))
    accepted_change_ids = Column(JSON)   # Array of change IDs to apply
    rejected_change_ids = Column(JSON)   # Array of rejected changes
    skipped = Column(Boolean, default=False)  # If user skipped without deciding

    decision_notes = Column(Text)
    decided_by = Column(String(100))

    # Relationships
    concept = relationship("AnalyzedConcept", backref="evidence_decisions")
    fragment = relationship("ConceptEvidenceFragment", backref="decision")
    selected_interpretation = relationship("ConceptEvidenceInterpretation")

    decided_at = Column(DateTime, server_default=func.now())


class ConceptEvidenceProgress(Base):
    """
    Tracks overall evidence integration progress for a concept.
    Updated as sources are added and fragments are processed.
    """
    __tablename__ = 'ca_evidence_progress'

    id = Column(Integer, primary_key=True)
    concept_id = Column(Integer, ForeignKey('ca_analyzed_concepts.id'), nullable=False, unique=True)

    total_sources = Column(Integer, default=0)
    total_fragments = Column(Integer, default=0)
    auto_integrated_count = Column(Integer, default=0)
    needs_decision_count = Column(Integer, default=0)
    resolved_count = Column(Integer, default=0)
    skipped_count = Column(Integer, default=0)

    # Relationship
    concept = relationship("AnalyzedConcept", backref="evidence_progress")

    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())


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
