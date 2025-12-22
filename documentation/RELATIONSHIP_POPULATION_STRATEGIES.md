# Item Relationship Population Strategies

This document describes how inter-item relationships (DEPENDS_ON, SUPPORTS, CONTRADICTS, etc.) are populated in the concept analysis system. The goal is to ensure these relationships are never "dummy data" but are actively generated through multiple real-world pathways.

## Overview

Item relationships form a knowledge web connecting claims, inferences, and insights within a concept analysis. Each relationship has:
- **source_item_id**: The originating item
- **target_item_id**: The related item
- **relationship_type**: The semantic nature of the connection
- **discovered_via**: How the relationship was identified (provenance)
- **confidence**: How certain we are about the relationship
- **explanation**: Why this relationship holds

## Relationship Types

| Type | Description | Example |
|------|-------------|---------|
| `depends_on` | Source assumes or requires target | "Semiconductor investment" depends on "national ownership requirements" |
| `supports` | Source provides backing for target | "States have legitimate interests" supports "domestic investment" |
| `contradicts` | Source logically opposes target | "Free trade absolutism" contradicts "investment requirements" |
| `tension_with` | Source creates friction with target (not outright contradiction) | "Efficiency focus" in tension with "sovereignty goals" |
| `enables` | Source makes target possible | "R&D funding" enables "tech independence" |
| `supersedes` | Source replaces or updates target | "New definition" supersedes "old definition" |
| `specializes` | Source is a specific instance of target | "Chip sovereignty" specializes "tech sovereignty" |
| `generalizes` | Source is a broader category of target | "Digital rights" generalizes "data sovereignty" |

## Population Strategies

### 1. Wizard-Generated Relationships

**Source**: `RelationshipSource.WIZARD_GENERATED`

During the initial concept setup wizard, relationships are inferred from the structural connections implied by user input:

#### Implementation Approach
```python
# In concept_setup_wizard.py or similar

async def infer_wizard_relationships(concept_id: int, items: List[AnalysisItem]):
    """
    Infer relationships between items based on wizard input patterns.

    Examples:
    - Forward inferences DEPEND ON backward inferences (transcendental conditions)
    - Contradictions CONTRADICT forward inferences and assumptions
    - Paradigmatic cases SUPPORT theoretical claims
    """
    relationships = []

    # Group items by type
    forward_infs = [i for i in items if i.item_type == 'forward_inferences']
    backward_infs = [i for i in items if i.item_type == 'backward_inferences']
    contradictions = [i for i in items if i.item_type == 'contradictions']

    # Forward inferences often depend on backward inferences (transcendental conditions)
    for fwd in forward_infs:
        for bwd in backward_infs:
            if semantic_similarity(fwd.content, bwd.content) > 0.6:
                relationships.append(ItemRelationship(
                    source_item_id=fwd.id,
                    target_item_id=bwd.id,
                    relationship_type=ItemRelationType.DEPENDS_ON,
                    discovered_via=RelationshipSource.WIZARD_GENERATED,
                    confidence=0.75,
                    explanation=f"Inferred: forward inference depends on transcendental condition"
                ))

    # Contradictions contradict related forward inferences
    for contra in contradictions:
        for fwd in forward_infs:
            if semantic_similarity(contra.content, fwd.content) > 0.5:
                relationships.append(ItemRelationship(
                    source_item_id=contra.id,
                    target_item_id=fwd.id,
                    relationship_type=ItemRelationType.CONTRADICTS,
                    discovered_via=RelationshipSource.WIZARD_GENERATED,
                    confidence=0.8,
                    explanation=f"Contradiction opposes inference"
                ))

    return relationships
```

#### When Triggered
- After wizard completion, run relationship inference
- Can be re-run to refresh relationships based on updated items

### 2. Evidence-Extracted Relationships

**Source**: `RelationshipSource.EVIDENCE_EXTRACTED`

When processing external sources (articles, papers, news), extract relationships between the new evidence and existing items:

#### Implementation Approach
```python
# LLM prompt for evidence relationship extraction

EVIDENCE_RELATIONSHIP_PROMPT = """
Given this new evidence fragment and the existing concept analysis items,
identify relationships between them.

NEW EVIDENCE:
{evidence_content}

EXISTING ITEMS:
{existing_items_json}

For each relationship found, provide:
1. source_item: The evidence fragment OR an existing item ID
2. target_item: An existing item ID OR the evidence fragment
3. relationship_type: One of (depends_on, supports, contradicts, tension_with, enables, supersedes, specializes, generalizes)
4. confidence: 0.0 to 1.0
5. explanation: Why this relationship holds

Return as JSON array.
"""

async def extract_evidence_relationships(
    evidence_fragment: ConceptEvidenceFragment,
    existing_items: List[AnalysisItem]
) -> List[ItemRelationship]:
    """Extract relationships when new evidence is added."""

    # Call LLM with structured output
    result = await llm.generate(
        EVIDENCE_RELATIONSHIP_PROMPT.format(
            evidence_content=evidence_fragment.content,
            existing_items_json=serialize_items(existing_items)
        ),
        response_format="json"
    )

    relationships = []
    for rel in result['relationships']:
        relationships.append(ItemRelationship(
            source_item_id=rel['source_item'],
            target_item_id=rel['target_item'],
            relationship_type=ItemRelationType(rel['relationship_type']),
            discovered_via=RelationshipSource.EVIDENCE_EXTRACTED,
            confidence=rel['confidence'],
            explanation=rel['explanation'],
            evidence_fragment_id=evidence_fragment.id
        ))

    return relationships
```

#### Evidence Sources
- Academic papers (via DOI or full text)
- News articles (via URL fetch)
- Thinker's works (Zuboff, Floridi, etc.)
- Policy documents
- Manual text input

### 3. LLM-Inferred Relationships

**Source**: `RelationshipSource.LLM_INFERRED`

Batch inference to discover relationships across all items in a concept analysis:

#### Implementation Approach
```python
BATCH_RELATIONSHIP_INFERENCE_PROMPT = """
Analyze all items in this concept analysis and identify relationships between them.

CONCEPT: {concept_name}
ITEMS:
{all_items_json}

Identify:
1. Logical dependencies (what assumes what)
2. Evidential support (what backs what)
3. Contradictions and tensions
4. Specialization/generalization hierarchies
5. Enabling relationships

For each relationship:
- source_id, target_id
- relationship_type
- confidence (be conservative - only high-confidence relationships)
- explanation

Return JSON array. Focus on non-obvious relationships that add analytical value.
"""

async def batch_infer_relationships(concept_id: int) -> List[ItemRelationship]:
    """Run batch inference across all concept items."""

    items = await get_all_items_for_concept(concept_id)

    result = await llm.generate(
        BATCH_RELATIONSHIP_INFERENCE_PROMPT.format(
            concept_name=concept.name,
            all_items_json=serialize_items(items)
        ),
        response_format="json"
    )

    relationships = []
    for rel in result['relationships']:
        # Only add high-confidence relationships
        if rel['confidence'] >= 0.7:
            relationships.append(ItemRelationship(
                source_item_id=rel['source_id'],
                target_item_id=rel['target_id'],
                relationship_type=ItemRelationType(rel['relationship_type']),
                discovered_via=RelationshipSource.LLM_INFERRED,
                confidence=rel['confidence'],
                explanation=rel['explanation']
            ))

    return relationships
```

#### Triggering Batch Inference
- Manual trigger via admin UI
- Scheduled job (e.g., after X new items added)
- After major evidence integration

### 4. User-Curated Relationships

**Source**: `RelationshipSource.USER_CURATED`

Manual relationship creation by the analyst:

#### UI Components Needed
```jsx
// AddRelationshipModal.jsx

function AddRelationshipModal({ sourceItem, allItems, onSave }) {
  const [targetItemId, setTargetItemId] = useState(null)
  const [relationshipType, setRelationshipType] = useState('supports')
  const [explanation, setExplanation] = useState('')

  return (
    <Modal>
      <h3>Link "{sourceItem.content.slice(0, 50)}..." to another item</h3>

      <Select
        label="Relationship Type"
        value={relationshipType}
        onChange={setRelationshipType}
        options={[
          { value: 'depends_on', label: 'Depends On' },
          { value: 'supports', label: 'Supports' },
          { value: 'contradicts', label: 'Contradicts' },
          { value: 'tension_with', label: 'In Tension With' },
          { value: 'enables', label: 'Enables' },
          { value: 'supersedes', label: 'Supersedes' },
          { value: 'specializes', label: 'Specializes' },
          { value: 'generalizes', label: 'Generalizes' },
        ]}
      />

      <SearchableSelect
        label="Target Item"
        items={allItems.filter(i => i.id !== sourceItem.id)}
        value={targetItemId}
        onChange={setTargetItemId}
        renderItem={(item) => `[${item.item_type}] ${item.content.slice(0, 60)}...`}
      />

      <TextArea
        label="Why does this relationship hold?"
        value={explanation}
        onChange={setExplanation}
      />

      <Button onClick={() => onSave({
        source_item_id: sourceItem.id,
        target_item_id: targetItemId,
        relationship_type: relationshipType,
        explanation,
        discovered_via: 'user_curated',
        confidence: 0.95  // High confidence for manual curation
      })}>
        Create Relationship
      </Button>
    </Modal>
  )
}
```

### 5. System-Detected Relationships

**Source**: `RelationshipSource.SYSTEM_DETECTED`

Automatic detection based on structural patterns:

#### Implementation Approach
```python
async def detect_structural_relationships(concept_id: int) -> List[ItemRelationship]:
    """Detect relationships from structural patterns."""

    relationships = []
    items = await get_all_items_for_concept(concept_id)

    # Pattern 1: Items in same operation that reference each other
    for item in items:
        for other in items:
            if item.id == other.id:
                continue

            # Check if item content mentions concepts from other item
            if content_references(item.content, other.content):
                relationships.append(ItemRelationship(
                    source_item_id=item.id,
                    target_item_id=other.id,
                    relationship_type=ItemRelationType.DEPENDS_ON,
                    discovered_via=RelationshipSource.SYSTEM_DETECTED,
                    confidence=0.6,
                    explanation="Content reference detected"
                ))

    # Pattern 2: Contradiction items vs forward inferences
    contradictions = [i for i in items if i.item_type == 'contradictions']
    forward_infs = [i for i in items if i.item_type == 'forward_inferences']

    for contra in contradictions:
        for fwd in forward_infs:
            # Use embedding similarity to find related pairs
            similarity = compute_embedding_similarity(contra.content, fwd.content)
            if similarity > 0.65:
                relationships.append(ItemRelationship(
                    source_item_id=contra.id,
                    target_item_id=fwd.id,
                    relationship_type=ItemRelationType.CONTRADICTS,
                    discovered_via=RelationshipSource.SYSTEM_DETECTED,
                    confidence=similarity,
                    explanation=f"Semantic similarity: {similarity:.2f}"
                ))

    return relationships
```

## API Endpoints for Relationship Management

```python
# In concept_relationship_router.py

@router.post("/concepts/{concept_id}/relationships")
async def create_relationship(
    concept_id: int,
    data: CreateRelationshipRequest,
    db: Session = Depends(get_db)
):
    """Manually create a relationship."""
    ...

@router.post("/concepts/{concept_id}/relationships/infer")
async def infer_relationships(
    concept_id: int,
    strategy: str = Query("batch"),  # wizard, evidence, batch, system
    db: Session = Depends(get_db)
):
    """Run relationship inference using specified strategy."""
    ...

@router.delete("/concepts/{concept_id}/relationships/{rel_id}")
async def delete_relationship(
    concept_id: int,
    rel_id: int,
    db: Session = Depends(get_db)
):
    """Delete a relationship (soft delete via is_active=False)."""
    ...

@router.get("/concepts/{concept_id}/relationships/graph")
async def get_relationship_graph(
    concept_id: int,
    db: Session = Depends(get_db)
):
    """Get all relationships as a graph structure for visualization."""
    ...
```

## Confidence Calibration

Different sources have different baseline confidence levels:

| Source | Default Confidence | Notes |
|--------|-------------------|-------|
| `user_curated` | 0.95 | User explicitly created - high confidence |
| `wizard_generated` | 0.75 | Inferred from structural patterns |
| `evidence_extracted` | 0.70-0.90 | Depends on evidence quality |
| `llm_inferred` | 0.60-0.85 | Depends on context clarity |
| `system_detected` | 0.50-0.70 | Pattern-based, needs verification |

## Deduplication

When multiple sources identify the same relationship, merge them:

```python
async def merge_duplicate_relationships(relationships: List[ItemRelationship]):
    """Merge relationships with same source/target/type."""

    seen = {}
    for rel in relationships:
        key = (rel.source_item_id, rel.target_item_id, rel.relationship_type)

        if key in seen:
            existing = seen[key]
            # Take higher confidence
            if rel.confidence > existing.confidence:
                existing.confidence = rel.confidence
                existing.explanation = rel.explanation
            # Track all discovery sources
            existing.discovery_sources.append(rel.discovered_via)
        else:
            seen[key] = rel

    return list(seen.values())
```

## Future Enhancements

1. **Relationship Visualization**: Graph view showing concept items as nodes and relationships as edges
2. **Conflict Detection**: Identify when new relationships contradict existing ones
3. **Relationship Suggestions**: "Did you mean to add this relationship?" prompts
4. **Bulk Operations**: Apply relationship patterns across similar concepts
5. **Export/Import**: Share relationship patterns between concepts
