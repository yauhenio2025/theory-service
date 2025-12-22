"""
Wizard to 8D Schema Bridge

Converts wizard outputs (hypothesis_cards, genealogy_cards, dimensional_signals, etc.)
into the structured 8D concept analysis schema (AnalyzedConcept, ConceptAnalysis, AnalysisItem).

This bridges the gap between:
- concept_wizard.py: Generates rich structured data via LLM conversations
- concept_analysis_models.py: Stores analysis in normalized 8D schema

Population Flow:
1. Wizard generates structured outputs (cards, signals, answers)
2. This bridge parses and maps to appropriate dimensions/operations
3. Creates AnalyzedConcept + ConceptAnalysis + AnalysisItem records
4. Sets provenance_type=WIZARD, created_via='initial_wizard'
5. Later: Evidence enrichment adds more items with provenance_type=EVIDENCE
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .concept_analysis_models import (
    AnalyzedConcept, ConceptAnalysis, AnalysisItem, ItemReasoningScaffold,
    ItemRelationship, AnalyticalOperation, AnalyticalDimension,
    DimensionType, ProvenanceType, ItemRelationType, RelationshipSource,
    WebCentrality, InferenceType, SourceType
)

logger = logging.getLogger(__name__)


# =====================================================================
# MAPPING CONFIGURATION
# =====================================================================

# Map wizard hypothesis card types to dimensions and item types
HYPOTHESIS_TYPE_TO_DIMENSION = {
    "thesis": (DimensionType.POSITIONAL, "forward_inference"),
    "assumption": (DimensionType.PRESUPPOSITIONAL, "hidden_assumption"),
    "tension": (DimensionType.DYNAMIC, "tension"),
    "methodological": (DimensionType.AFFORDANCE, "reasoning_style"),
    "normative": (DimensionType.NORMALIZATION, "embedded_norm"),
}

# Map dimensional signals to dimensions
SIGNAL_TO_DIMENSION = {
    "quinean": DimensionType.POSITIONAL,
    "sellarsian": DimensionType.PRESUPPOSITIONAL,
    "brandomian": DimensionType.COMMITMENT,
    "deleuzian": DimensionType.DYNAMIC,
    "bachelardian": DimensionType.GENEALOGICAL,
    "canguilhem": DimensionType.NORMALIZATION,
    "davidson": DimensionType.AFFORDANCE,
    "blumenberg": DimensionType.GENEALOGICAL,
    "carey": DimensionType.GENEALOGICAL,
}

# Map wizard stage answers to dimensions/operations
STAGE_ANSWER_MAPPINGS = {
    "core_definition": (DimensionType.POSITIONAL, "core_definition", "forward_inference"),
    "problem_addressed": (DimensionType.POSITIONAL, "problem_gap", "forward_inference"),
    "paradigmatic_case": (DimensionType.BOUNDARY, "paradigmatic_case", "gray_zone"),
    "recognition_markers": (DimensionType.AFFORDANCE, "recognition_pattern", "visibility_effect"),
    "core_claim": (DimensionType.COMMITMENT, "core_commitment", "commitment"),
    "falsification_condition": (DimensionType.BOUNDARY, "falsification", "anomaly"),
    "implicit_domain": (DimensionType.AFFORDANCE, "implicit_domain", "vocabulary_addition"),
}

# Confidence mapping from wizard levels to float
CONFIDENCE_MAP = {
    "high": 0.9,
    "medium": 0.7,
    "low": 0.5,
}


# =====================================================================
# HELPER FUNCTIONS
# =====================================================================

async def get_or_create_operation(
    db: AsyncSession,
    dimension_type: DimensionType,
    operation_name: str
) -> Optional[AnalyticalOperation]:
    """Get an operation by dimension and name, or return None if not found."""
    # First get the dimension
    dim_result = await db.execute(
        select(AnalyticalDimension).where(AnalyticalDimension.dimension_type == dimension_type)
    )
    dimension = dim_result.scalar_one_or_none()

    if not dimension:
        logger.warning(f"Dimension {dimension_type} not found in database")
        return None

    # Then find an operation in that dimension
    op_result = await db.execute(
        select(AnalyticalOperation).where(
            AnalyticalOperation.dimension_id == dimension.id
        ).limit(1)  # Get any operation in this dimension for now
    )
    operation = op_result.scalar_one_or_none()

    return operation


def map_confidence(wizard_confidence: str) -> float:
    """Convert wizard confidence strings to floats."""
    if isinstance(wizard_confidence, (int, float)):
        return float(wizard_confidence)
    return CONFIDENCE_MAP.get(str(wizard_confidence).lower(), 0.7)


def extract_source_passage(card: Dict[str, Any]) -> Optional[str]:
    """Extract source passage from card's source_excerpts."""
    excerpts = card.get("source_excerpts", [])
    if excerpts and isinstance(excerpts, list):
        return " | ".join([e for e in excerpts if e])
    return None


# =====================================================================
# CORE BRIDGE FUNCTIONS
# =====================================================================

async def bridge_wizard_to_schema(
    db: AsyncSession,
    concept_name: str,
    wizard_data: Dict[str, Any],
    wizard_session_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Main bridge function: Convert wizard outputs to 8D schema.

    Args:
        db: Database session
        concept_name: Name of the concept
        wizard_data: Full wizard output including:
            - notes_analysis: {summary, key_insights, preliminary_definition}
            - hypothesis_cards: List of hypothesis cards
            - genealogy_cards: List of genealogy cards
            - differentiation_cards: List of differentiation cards
            - dimensional_signals: Dict of per-dimension signals
            - stage answers (core_definition, problem_addressed, etc.)
        wizard_session_id: Optional ID of the wizard session for provenance

    Returns:
        Dict with created IDs and summary
    """
    result = {
        "analyzed_concept_id": None,
        "analyses_created": 0,
        "items_created": 0,
        "relationships_created": 0,
        "errors": [],
    }

    try:
        # 1. Create AnalyzedConcept
        notes_analysis = wizard_data.get("notes_analysis", {})
        definition = (
            wizard_data.get("core_definition") or
            notes_analysis.get("preliminary_definition") or
            wizard_data.get("definition", "")
        )

        analyzed_concept = AnalyzedConcept(
            term=concept_name,
            definition=definition,
            is_user_concept=True,
            disciplinary_home=notes_analysis.get("field"),
        )
        db.add(analyzed_concept)
        await db.flush()  # Get the ID
        result["analyzed_concept_id"] = analyzed_concept.id

        # Track created items for relationship inference
        created_items: List[AnalysisItem] = []

        # 2. Process hypothesis cards
        items = await process_hypothesis_cards(
            db, analyzed_concept.id,
            wizard_data.get("hypothesis_cards", []),
            wizard_session_id
        )
        created_items.extend(items)
        result["items_created"] += len(items)

        # 3. Process genealogy cards
        items = await process_genealogy_cards(
            db, analyzed_concept.id,
            wizard_data.get("genealogy_cards", []),
            wizard_session_id
        )
        created_items.extend(items)
        result["items_created"] += len(items)

        # 4. Process differentiation cards
        items = await process_differentiation_cards(
            db, analyzed_concept.id,
            wizard_data.get("differentiation_cards", []),
            wizard_session_id
        )
        created_items.extend(items)
        result["items_created"] += len(items)

        # 5. Process dimensional signals
        items = await process_dimensional_signals(
            db, analyzed_concept.id,
            wizard_data.get("dimensional_signals", {}),
            wizard_session_id
        )
        created_items.extend(items)
        result["items_created"] += len(items)

        # 6. Process stage answers (core_definition, problem_addressed, etc.)
        items = await process_stage_answers(
            db, analyzed_concept.id,
            wizard_data,
            wizard_session_id
        )
        created_items.extend(items)
        result["items_created"] += len(items)

        # 7. Process epistemic blind spots as items to revisit
        items = await process_epistemic_blind_spots(
            db, analyzed_concept.id,
            wizard_data.get("epistemic_blind_spots",
                          wizard_data.get("gaps_tensions_questions", [])),
            wizard_session_id
        )
        created_items.extend(items)
        result["items_created"] += len(items)

        # Count analyses created
        analysis_result = await db.execute(
            select(ConceptAnalysis).where(ConceptAnalysis.concept_id == analyzed_concept.id)
        )
        result["analyses_created"] = len(analysis_result.scalars().all())

        await db.commit()

    except Exception as e:
        logger.error(f"Error bridging wizard to schema: {e}", exc_info=True)
        result["errors"].append(str(e))
        await db.rollback()

    return result


async def get_or_create_analysis(
    db: AsyncSession,
    concept_id: int,
    dimension_type: DimensionType,
) -> Optional[ConceptAnalysis]:
    """Get or create a ConceptAnalysis record for the given concept and dimension."""
    # Get operation for this dimension
    operation = await get_or_create_operation(db, dimension_type, "default")

    if not operation:
        logger.warning(f"Could not find operation for dimension {dimension_type}")
        return None

    # Check if analysis exists
    result = await db.execute(
        select(ConceptAnalysis).where(
            ConceptAnalysis.concept_id == concept_id,
            ConceptAnalysis.operation_id == operation.id
        )
    )
    analysis = result.scalar_one_or_none()

    if not analysis:
        analysis = ConceptAnalysis(
            concept_id=concept_id,
            operation_id=operation.id,
            source_type=SourceType.LLM_GENERATED,
        )
        db.add(analysis)
        await db.flush()

    return analysis


# =====================================================================
# CARD PROCESSORS
# =====================================================================

async def process_hypothesis_cards(
    db: AsyncSession,
    concept_id: int,
    cards: List[Dict[str, Any]],
    wizard_session_id: Optional[int] = None
) -> List[AnalysisItem]:
    """Process wizard hypothesis cards into AnalysisItems."""
    items = []

    for card in cards:
        card_type = card.get("type", "thesis")
        mapping = HYPOTHESIS_TYPE_TO_DIMENSION.get(card_type, (DimensionType.POSITIONAL, "forward_inference"))
        dimension_type, item_type = mapping

        analysis = await get_or_create_analysis(db, concept_id, dimension_type)
        if not analysis:
            continue

        # Create the item
        item = AnalysisItem(
            analysis_id=analysis.id,
            item_type=item_type,
            content=card.get("content", ""),
            strength=map_confidence(card.get("confidence", "medium")),
            extra_data={
                "wizard_card_id": card.get("id"),
                "wizard_card_type": card_type,
                "source_excerpts": card.get("source_excerpts", []),
                "rationale": card.get("rationale"),
            },
            provenance_type=ProvenanceType.WIZARD,
            provenance_source_id=wizard_session_id,
            created_via="initial_wizard",
            is_active=True,
        )
        db.add(item)
        await db.flush()

        # Create reasoning scaffold
        scaffold = ItemReasoningScaffold(
            item_id=item.id,
            derivation_trigger="user_notes",
            source_passage=extract_source_passage(card),
            reasoning_trace=card.get("rationale"),
            premise_confidence=map_confidence(card.get("confidence", "medium")),
        )
        db.add(scaffold)

        items.append(item)

    return items


async def process_genealogy_cards(
    db: AsyncSession,
    concept_id: int,
    cards: List[Dict[str, Any]],
    wizard_session_id: Optional[int] = None
) -> List[AnalysisItem]:
    """Process wizard genealogy cards into AnalysisItems."""
    items = []

    analysis = await get_or_create_analysis(db, concept_id, DimensionType.GENEALOGICAL)
    if not analysis:
        return items

    for card in cards:
        # Create item for thinker influence
        content = f"{card.get('thinker', 'Unknown')} ({card.get('tradition', '')}): {card.get('connection', '')}"

        item = AnalysisItem(
            analysis_id=analysis.id,
            item_type="theoretical_lineage",
            content=content,
            strength=map_confidence(card.get("confidence", "medium")),
            extra_data={
                "wizard_card_id": card.get("id"),
                "thinker": card.get("thinker"),
                "tradition": card.get("tradition"),
                "connection": card.get("connection"),
                "why_relevant": card.get("why_relevant"),
                "source_excerpts": card.get("source_excerpts", []),
            },
            provenance_type=ProvenanceType.WIZARD,
            provenance_source_id=wizard_session_id,
            created_via="initial_wizard",
            is_active=True,
        )
        db.add(item)
        await db.flush()

        # Create reasoning scaffold
        scaffold = ItemReasoningScaffold(
            item_id=item.id,
            derivation_trigger="user_notes",
            source_passage=extract_source_passage(card),
            reasoning_trace=card.get("why_relevant"),
            inference_type=InferenceType.ABDUCTIVE,
        )
        db.add(scaffold)

        items.append(item)

    return items


async def process_differentiation_cards(
    db: AsyncSession,
    concept_id: int,
    cards: List[Dict[str, Any]],
    wizard_session_id: Optional[int] = None
) -> List[AnalysisItem]:
    """Process wizard differentiation cards into AnalysisItems."""
    items = []

    analysis = await get_or_create_analysis(db, concept_id, DimensionType.POSITIONAL)
    if not analysis:
        return items

    for card in cards:
        # Create incompatibility/differentiation item
        content = f"Not {card.get('contrasted_with', 'unknown')}: {card.get('difference', '')}"

        item = AnalysisItem(
            analysis_id=analysis.id,
            item_type="incompatibility",
            content=content,
            strength=map_confidence(card.get("confidence", "medium")),
            subtype="differentiation",
            extra_data={
                "wizard_card_id": card.get("id"),
                "your_concept": card.get("your_concept"),
                "contrasted_with": card.get("contrasted_with"),
                "thinker_associated": card.get("thinker_associated"),
                "difference": card.get("difference"),
                "source_excerpts": card.get("source_excerpts", []),
            },
            provenance_type=ProvenanceType.WIZARD,
            provenance_source_id=wizard_session_id,
            created_via="initial_wizard",
            is_active=True,
        )
        db.add(item)
        await db.flush()

        items.append(item)

    return items


async def process_dimensional_signals(
    db: AsyncSession,
    concept_id: int,
    signals: Dict[str, Any],
    wizard_session_id: Optional[int] = None
) -> List[AnalysisItem]:
    """Process wizard dimensional signals into AnalysisItems."""
    items = []

    for signal_name, signal_data in signals.items():
        if not signal_data or not isinstance(signal_data, dict):
            continue

        dimension_type = SIGNAL_TO_DIMENSION.get(signal_name)
        if not dimension_type:
            continue

        analysis = await get_or_create_analysis(db, concept_id, dimension_type)
        if not analysis:
            continue

        confidence = map_confidence(signal_data.get("confidence", "low"))

        # Create items based on signal type
        items.extend(await _process_signal_by_type(
            db, analysis.id, signal_name, signal_data,
            confidence, wizard_session_id
        ))

    return items


async def _process_signal_by_type(
    db: AsyncSession,
    analysis_id: int,
    signal_name: str,
    signal_data: Dict[str, Any],
    confidence: float,
    wizard_session_id: Optional[int]
) -> List[AnalysisItem]:
    """Process individual signal type into items."""
    items = []

    # Quinean signals
    if signal_name == "quinean":
        for inference in signal_data.get("inferences_detected", []):
            if inference:
                item = AnalysisItem(
                    analysis_id=analysis_id,
                    item_type="forward_inference",
                    content=inference,
                    strength=confidence,
                    web_centrality=WebCentrality(signal_data.get("centrality_hint", "medium").lower())
                        if signal_data.get("centrality_hint") in ["core", "high", "medium", "peripheral"]
                        else WebCentrality.MEDIUM,
                    provenance_type=ProvenanceType.WIZARD,
                    provenance_source_id=wizard_session_id,
                    created_via="initial_wizard",
                    is_active=True,
                )
                db.add(item)
                await db.flush()
                items.append(item)

    # Sellarsian signals (givenness)
    elif signal_name == "sellarsian":
        for assumption in signal_data.get("hidden_assumptions", []):
            if assumption:
                item = AnalysisItem(
                    analysis_id=analysis_id,
                    item_type="hidden_assumption",
                    content=assumption,
                    strength=confidence,
                    provenance_type=ProvenanceType.WIZARD,
                    provenance_source_id=wizard_session_id,
                    created_via="initial_wizard",
                    is_active=True,
                )
                db.add(item)
                await db.flush()
                items.append(item)

    # Brandomian signals (commitments)
    elif signal_name == "brandomian":
        for commitment in signal_data.get("implicit_commitments", []):
            if commitment:
                item = AnalysisItem(
                    analysis_id=analysis_id,
                    item_type="commitment",
                    content=commitment,
                    strength=confidence,
                    provenance_type=ProvenanceType.WIZARD,
                    provenance_source_id=wizard_session_id,
                    created_via="initial_wizard",
                    is_active=True,
                )
                db.add(item)
                await db.flush()
                items.append(item)

    # Deleuzian signals (transformations)
    elif signal_name == "deleuzian":
        problem = signal_data.get("problem_addressed")
        if problem:
            item = AnalysisItem(
                analysis_id=analysis_id,
                item_type="tension",
                content=problem,
                strength=confidence,
                extra_data={
                    "tension_poles": signal_data.get("tension_poles", []),
                    "becomings_enabled": signal_data.get("becomings_enabled", []),
                    "becomings_blocked": signal_data.get("becomings_blocked", []),
                },
                provenance_type=ProvenanceType.WIZARD,
                provenance_source_id=wizard_session_id,
                created_via="initial_wizard",
                is_active=True,
            )
            db.add(item)
            await db.flush()
            items.append(item)

    # Bachelardian signals (breaks)
    elif signal_name == "bachelardian":
        breaking_from = signal_data.get("breaking_from")
        if breaking_from:
            item = AnalysisItem(
                analysis_id=analysis_id,
                item_type="epistemological_break",
                content=f"Breaking from: {breaking_from}",
                strength=confidence,
                extra_data={
                    "why_inadequate": signal_data.get("why_inadequate"),
                    "obstacle_risk": signal_data.get("obstacle_risk"),
                },
                provenance_type=ProvenanceType.WIZARD,
                provenance_source_id=wizard_session_id,
                created_via="initial_wizard",
                is_active=True,
            )
            db.add(item)
            await db.flush()
            items.append(item)

    # Canguilhem signals (norms)
    elif signal_name == "canguilhem":
        for value in signal_data.get("values_embedded", []):
            if value:
                item = AnalysisItem(
                    analysis_id=analysis_id,
                    item_type="embedded_norm",
                    content=value,
                    strength=confidence,
                    extra_data={
                        "whose_interests": signal_data.get("whose_interests"),
                        "what_excluded": signal_data.get("what_excluded"),
                    },
                    provenance_type=ProvenanceType.WIZARD,
                    provenance_source_id=wizard_session_id,
                    created_via="initial_wizard",
                    is_active=True,
                )
                db.add(item)
                await db.flush()
                items.append(item)

    # Davidson signals (reasoning styles)
    elif signal_name == "davidson":
        style = signal_data.get("reasoning_style")
        if style:
            item = AnalysisItem(
                analysis_id=analysis_id,
                item_type="reasoning_style",
                content=f"Reasoning style: {style}",
                strength=confidence,
                extra_data={
                    "makes_visible": signal_data.get("makes_visible", []),
                    "makes_invisible": signal_data.get("makes_invisible", []),
                },
                provenance_type=ProvenanceType.WIZARD,
                provenance_source_id=wizard_session_id,
                created_via="initial_wizard",
                is_active=True,
            )
            db.add(item)
            await db.flush()
            items.append(item)

    # Blumenberg signals (metaphors)
    elif signal_name == "blumenberg":
        metaphor = signal_data.get("root_metaphor")
        if metaphor:
            item = AnalysisItem(
                analysis_id=analysis_id,
                item_type="root_metaphor",
                content=metaphor,
                strength=confidence,
                extra_data={
                    "source_domain": signal_data.get("source_domain"),
                    "metaphor_work": signal_data.get("metaphor_work"),
                },
                provenance_type=ProvenanceType.WIZARD,
                provenance_source_id=wizard_session_id,
                created_via="initial_wizard",
                is_active=True,
            )
            db.add(item)
            await db.flush()
            items.append(item)

    # Carey signals (component concepts)
    elif signal_name == "carey":
        for component in signal_data.get("component_concepts", []):
            if component:
                item = AnalysisItem(
                    analysis_id=analysis_id,
                    item_type="component_concept",
                    content=component,
                    strength=confidence,
                    extra_data={
                        "combination_type": signal_data.get("combination_type"),
                        "what_emerges": signal_data.get("what_emerges"),
                    },
                    provenance_type=ProvenanceType.WIZARD,
                    provenance_source_id=wizard_session_id,
                    created_via="initial_wizard",
                    is_active=True,
                )
                db.add(item)
                await db.flush()
                items.append(item)

    return items


async def process_stage_answers(
    db: AsyncSession,
    concept_id: int,
    wizard_data: Dict[str, Any],
    wizard_session_id: Optional[int] = None
) -> List[AnalysisItem]:
    """Process wizard stage answers into AnalysisItems."""
    items = []

    for answer_key, mapping in STAGE_ANSWER_MAPPINGS.items():
        value = wizard_data.get(answer_key)
        if not value:
            continue

        dimension_type, item_subtype, item_type = mapping
        analysis = await get_or_create_analysis(db, concept_id, dimension_type)
        if not analysis:
            continue

        # Handle dict values (like paradigmatic_case)
        if isinstance(value, dict):
            content = value.get("description") or value.get("statement") or str(value)
            extra = value
        else:
            content = str(value)
            extra = {"wizard_answer_key": answer_key}

        item = AnalysisItem(
            analysis_id=analysis.id,
            item_type=item_type,
            content=content,
            subtype=item_subtype,
            extra_data=extra,
            provenance_type=ProvenanceType.WIZARD,
            provenance_source_id=wizard_session_id,
            created_via="initial_wizard",
            is_active=True,
        )
        db.add(item)
        await db.flush()
        items.append(item)

    return items


async def process_epistemic_blind_spots(
    db: AsyncSession,
    concept_id: int,
    blind_spots: List[Dict[str, Any]],
    wizard_session_id: Optional[int] = None
) -> List[AnalysisItem]:
    """Process epistemic blind spots as items to revisit."""
    items = []

    # Blind spots go to PRESUPPOSITIONAL dimension as areas to clarify
    analysis = await get_or_create_analysis(db, concept_id, DimensionType.PRESUPPOSITIONAL)
    if not analysis:
        return items

    for spot in blind_spots:
        if not spot:
            continue

        category = spot.get("category", spot.get("type", "ambiguity"))
        description = spot.get("description", "")

        if not description:
            continue

        item = AnalysisItem(
            analysis_id=analysis.id,
            item_type="epistemic_blind_spot",
            content=description,
            subtype=category,
            extra_data={
                "what_unclear": spot.get("what_unclear", spot.get("pole_a")),
                "what_would_help": spot.get("what_would_help", spot.get("pole_b")),
                "source": spot.get("source"),
                "needs_resolution": True,
            },
            provenance_type=ProvenanceType.WIZARD,
            provenance_source_id=wizard_session_id,
            created_via="initial_wizard",
            is_active=True,
        )
        db.add(item)
        await db.flush()
        items.append(item)

    return items


# =====================================================================
# API ENDPOINT FOR BRIDGE
# =====================================================================

async def finalize_wizard_concept(
    db: AsyncSession,
    concept_name: str,
    wizard_output: Dict[str, Any],
    wizard_session_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Finalize a wizard concept by bridging to the 8D schema.

    This is called after the wizard completes to:
    1. Create AnalyzedConcept from wizard output
    2. Create all ConceptAnalysis and AnalysisItem records
    3. Set proper provenance tracking

    Args:
        db: Database session
        concept_name: The concept term
        wizard_output: Full wizard output dictionary
        wizard_session_id: Optional wizard session ID for provenance

    Returns:
        Summary of what was created
    """
    return await bridge_wizard_to_schema(
        db=db,
        concept_name=concept_name,
        wizard_data=wizard_output,
        wizard_session_id=wizard_session_id
    )
