# Data Genesis & Traceability Design

## The Problem You've Identified

Our current data structure has fields that appear without clear origin:
- **Premises** - where do they come from?
- **Alternatives Considered** - who generated these?
- **Reasoning Trace** - who wrote this?
- **Revisability Cost** - who determined this?

Everything needs to trace back to one of **three source pools**.

---

## The Three Source Pools

### Pool 1: WIZARD (User-Generated Seed)

The initial concept setup where the user provides foundational content.

**What the user provides:**
- Concept definition (their own words)
- Core claims they believe the concept entails
- Known contradictions/tensions
- Key thinkers they're aware of
- Disciplinary home
- Paradigm context

**Key insight:** The wizard doesn't populate everything. It establishes a **minimal scaffold** that evidence can then enrich, challenge, or validate.

### Pool 2: THEORETICAL (Academic/Thinker Sources)

Books, papers, essays by thinkers discussing related ideas.

**Characteristics:**
- May not mention "technological sovereignty" by name
- Discuss adjacent concepts (digital rights, data governance, etc.)
- Contain arguments, premises, conclusions
- Have named authors and citation info

**Examples:**
- Zuboff's "Surveillance Capitalism" (discusses data sovereignty implicitly)
- Floridi's work on digital ethics
- Policy papers on tech governance

### Pool 3: EMPIRICAL (Real-World Evidence)

News articles, think-tank reports, case studies.

**Characteristics:**
- Time-bound events (EU passes GDPR, US CHIPS Act)
- Named actors (companies, governments)
- Measurable outcomes
- Can confirm or complicate theoretical claims

**Examples:**
- "EU Digital Markets Act enters force" (news)
- Brookings report on semiconductor supply chains
- Case study of India's UPI system

---

## Data Flow: From Source to Stored Field

### PHASE 1: Wizard Seed

```
USER INPUT (Wizard)
    │
    ├── Q: "What is technological sovereignty?"
    │   └── A: "State control over critical digital infrastructure..."
    │       │
    │       └── CREATES: AnalysisItem
    │           - content: "State control over critical digital infrastructure..."
    │           - item_type: "core_definition"
    │           - provenance_type: "wizard"
    │           - wizard_session_id: 42
    │           - wizard_question_key: "concept_definition"
    │
    ├── Q: "What does this concept necessarily imply?"
    │   └── A: "States should invest in domestic chip manufacturing"
    │       │
    │       └── CREATES: AnalysisItem
    │           - content: "States should invest in domestic chip manufacturing"
    │           - item_type: "forward_inferences"
    │           - provenance_type: "wizard"
    │           - wizard_session_id: 42
    │           - wizard_question_key: "forward_implications"
    │
    └── Q: "What would contradict this concept?"
        └── A: "Complete free trade in all technology sectors"
            │
            └── CREATES: AnalysisItem
                - content: "Complete free trade in all technology sectors"
                - item_type: "contradictions"
                - provenance_type: "wizard"
                - wizard_session_id: 42
                - wizard_question_key: "contradictions"
```

**At this stage:**
- We have raw claims from the user
- NO reasoning scaffolds yet (no premises, no alternatives)
- NO relationships yet (no depends_on, supports)
- This is the SEED, not the full analysis

---

### PHASE 2: LLM Synthesis (Post-Wizard)

After wizard completion, an LLM analyzes the wizard inputs to generate:
- Reasoning scaffolds (premises, inference types)
- Suggested relationships between items
- Confidence scores

```
WIZARD OUTPUTS → LLM SYNTHESIS PROMPT → ENRICHED DATA

Prompt:
"Given these wizard-provided claims about 'Technological Sovereignty':
- Definition: {definition}
- Forward implications: {implications}
- Contradictions: {contradictions}

For the implication 'States should invest in domestic chip manufacturing':
1. What PREMISES does this inference depend on?
2. What TYPE of inference is this (deductive, material, abductive...)?
3. What ALTERNATIVES could one infer instead, and why were they not chosen?
4. How CENTRAL is this claim to the concept's web of belief?"

LLM Response:
{
  "premises": [
    {
      "claim": "Technological sovereignty requires autonomous capacity...",
      "genesis": {
        "type": "derived_from_wizard",
        "source_item_id": 123,  // The definition item
        "derivation": "Extracted from user's definition"
      }
    },
    {
      "claim": "Semiconductors are foundational to all digital technology",
      "genesis": {
        "type": "llm_background_knowledge",
        "confidence": 0.95,
        "verifiable_via": "empirical_sources"
      }
    }
  ],
  "inference_type": "material",
  "alternatives_rejected": [
    {
      "inference": "States should rely on allied nations for chips",
      "rejected_because": "Conflicts with sovereignty emphasis on autonomy",
      "genesis": {
        "type": "llm_generated_alternative",
        "reasoning": "Common alternative in IR literature"
      }
    }
  ]
}
```

**Key insight:** The LLM synthesis has TWO types of genesis:
1. **Derived from wizard** - extracted/inferred from user input
2. **LLM background knowledge** - the LLM's training data (should be flagged for verification)

---

### PHASE 3: Evidence Integration (Theoretical Sources)

User uploads a paper or book excerpt. System extracts relevant content.

```
THEORETICAL SOURCE: Zuboff, "Surveillance Capitalism" (2019)
    │
    ├── EXTRACTION PROMPT:
    │   "Given this text and the concept 'Technological Sovereignty',
    │    extract claims that relate to this concept."
    │
    └── EXTRACTED FRAGMENTS:
        │
        ├── Fragment 1: "Data is the new raw material of capitalism"
        │   │
        │   └── RELATIONSHIP ANALYSIS:
        │       "This SUPPORTS the premise that technology isn't politically neutral"
        │       │
        │       └── CREATES: ItemRelationship
        │           - source_item_id: [new item for Zuboff quote]
        │           - target_item_id: [existing "technology not neutral" item]
        │           - relationship_type: SUPPORTS
        │           - discovered_via: EVIDENCE_EXTRACTED
        │           - evidence_fragment_id: 456
        │           │
        │           └── GENESIS:
        │               - source_type: "theoretical"
        │               - source_name: "Zuboff, Surveillance Capitalism"
        │               - source_page: "Ch. 3, p. 67"
        │               - extraction_method: "llm_extraction"
        │               - extraction_prompt_version: "v2.1"
        │
        └── Fragment 2: "Behavioral prediction markets..."
            │
            └── CREATES NEW ITEM (if novel insight):
                - content: "Sovereignty concerns extend to behavioral data markets"
                - item_type: "forward_inferences"
                - provenance_type: "evidence"
                - evidence_source_id: [Zuboff source record]
                - evidence_fragment_id: 457
```

---

### PHASE 4: Evidence Integration (Empirical Sources)

User uploads a news article. System extracts real-world instances.

```
EMPIRICAL SOURCE: "EU Passes Digital Markets Act" (Reuters, 2022)
    │
    ├── EXTRACTION PROMPT:
    │   "Given this news article and the concept 'Technological Sovereignty',
    │    identify:
    │    1. Real-world events that INSTANTIATE the concept
    │    2. Events that CHALLENGE theoretical claims
    │    3. Events that provide BOUNDARY CONDITIONS"
    │
    └── EXTRACTED FRAGMENTS:
        │
        └── Fragment: "EU requires interoperability for messaging platforms"
            │
            ├── RELATIONSHIP: SUPPORTS "States can impose tech requirements"
            │
            └── CREATES: AnalysisItem (paradigmatic case)
                - content: {
                    "case": "EU Digital Markets Act",
                    "what_happened": "Required interoperability for messaging",
                    "why_paradigmatic": "Demonstrates state capacity to regulate tech giants"
                  }
                - item_type: "paradigmatic_cases"
                - provenance_type: "evidence"
                - evidence_source_id: [Reuters source record]
                │
                └── GENESIS:
                    - source_type: "empirical"
                    - source_name: "Reuters"
                    - source_url: "https://..."
                    - source_date: "2022-07-05"
                    - actors: ["EU", "Meta", "Apple"]
                    - extraction_confidence: 0.9
```

---

## Revised Data Model for Full Traceability

### 1. Genesis Record (New Model)

Every piece of content needs a genesis record:

```python
class ContentGenesis(Base):
    """
    Tracks the origin of any piece of content in the system.
    Attached to AnalysisItem, ItemRelationship, or ReasoningScaffold fields.
    """
    __tablename__ = 'ca_content_genesis'

    id = Column(Integer, primary_key=True)

    # What this genesis is for
    target_type = Column(Enum)  # 'analysis_item', 'relationship', 'scaffold_premise', etc.
    target_id = Column(Integer)  # FK to the target record
    target_field = Column(String)  # Which field, e.g., 'premises[0].claim'

    # Source Pool (one of three)
    source_pool = Column(Enum)  # 'wizard', 'theoretical', 'empirical'

    # If wizard:
    wizard_session_id = Column(Integer, ForeignKey('ca_wizard_sessions.id'))
    wizard_question_key = Column(String)
    user_input_verbatim = Column(Text)

    # If theoretical/empirical:
    evidence_source_id = Column(Integer, ForeignKey('ca_evidence_sources.id'))
    evidence_fragment_id = Column(Integer, ForeignKey('ca_evidence_fragments.id'))
    passage_text = Column(Text)
    passage_location = Column(String)  # page, timestamp, paragraph

    # If LLM-derived:
    derived_from_genesis_ids = Column(JSON)  # Array of genesis IDs this was derived from
    derivation_method = Column(String)  # 'extraction', 'synthesis', 'inference'
    derivation_prompt_hash = Column(String)  # Track which prompt version
    derivation_confidence = Column(Float)

    # Verification status
    needs_verification = Column(Boolean, default=False)  # True for LLM background knowledge
    verified_by_evidence_id = Column(Integer)  # If later verified by evidence

    created_at = Column(DateTime, server_default=func.now())
```

### 2. Enhanced Wizard Session Tracking

```python
class WizardSession(Base):
    """
    Tracks a concept wizard session for provenance.
    """
    __tablename__ = 'ca_wizard_sessions'

    id = Column(Integer, primary_key=True)
    concept_id = Column(Integer, ForeignKey('ca_analyzed_concepts.id'))

    started_at = Column(DateTime)
    completed_at = Column(DateTime)

    # Store all Q&A for audit
    questions_answered = Column(JSON)  # [{key, question_text, user_answer, timestamp}]

    # Synthesis metadata
    synthesis_model = Column(String)  # 'claude-sonnet-4-5-20250929'
    synthesis_prompt_version = Column(String)
    synthesis_completed_at = Column(DateTime)
```

### 3. Structured Premise with Genesis

Instead of storing premises as opaque JSON, store them with genesis:

```python
class ScaffoldPremise(Base):
    """
    Individual premise in a reasoning scaffold, with full traceability.
    """
    __tablename__ = 'ca_scaffold_premises'

    id = Column(Integer, primary_key=True)
    scaffold_id = Column(Integer, ForeignKey('ca_item_reasoning_scaffolds.id'))

    claim = Column(Text, nullable=False)
    claim_type = Column(Enum)  # 'definitional', 'empirical', 'normative'
    centrality = Column(Enum)  # 'core', 'high', 'medium', 'peripheral'

    # Genesis - where does this premise come from?
    genesis_id = Column(Integer, ForeignKey('ca_content_genesis.id'))

    sequence_order = Column(Integer)
```

### 4. Structured Alternatives with Genesis

```python
class ScaffoldAlternative(Base):
    """
    Alternative inference that was considered and rejected.
    """
    __tablename__ = 'ca_scaffold_alternatives'

    id = Column(Integer, primary_key=True)
    scaffold_id = Column(Integer, ForeignKey('ca_item_reasoning_scaffolds.id'))

    inference = Column(Text, nullable=False)
    rejected_because = Column(Text)
    plausibility = Column(Float)

    # Genesis - who generated this alternative?
    genesis_id = Column(Integer, ForeignKey('ca_content_genesis.id'))
    # Typically: llm_synthesis during post-wizard processing
    # Or: evidence_extracted if a source proposed this alternative
```

---

## Field-by-Field Genesis Mapping

### ReasoningScaffold Fields

| Field | Genesis Source | How Populated |
|-------|----------------|---------------|
| `inference_type` | LLM_SYNTHESIS | LLM analyzes the claim and wizard context |
| `inference_rule` | LLM_SYNTHESIS | LLM determines the rule being applied |
| `premises[]` | MIXED | Some from wizard (extracted from definition), some from LLM background |
| `reasoning_trace` | LLM_SYNTHESIS | LLM writes explanation based on premises |
| `derivation_trigger` | WIZARD or EVIDENCE | What source passage triggered this inference |
| `source_passage` | WIZARD or EVIDENCE | Verbatim text that led to this |
| `source_location` | WIZARD or EVIDENCE | Page/question/URL |
| `alternatives_rejected[]` | LLM_SYNTHESIS | LLM generates plausible alternatives |
| `revisability_cost` | LLM_SYNTHESIS | LLM assesses based on web position |
| `premise_confidence` | LLM_SYNTHESIS + EVIDENCE | Can be updated when evidence confirms/challenges |
| `inference_validity` | LLM_SYNTHESIS | LLM's confidence in the inference move |

### AnalysisItem Fields

| Field | Genesis Source | How Populated |
|-------|----------------|---------------|
| `content` | WIZARD or EVIDENCE | Either user typed it or extracted from source |
| `item_type` | SYSTEM | Determined by wizard question or extraction target |
| `strength/severity` | LLM_SYNTHESIS | LLM assigns based on analysis |
| `web_centrality` | LLM_SYNTHESIS | LLM determines position in belief web |
| `observation_proximity` | LLM_SYNTHESIS + EVIDENCE | Higher if supported by empirical sources |
| `coherence_score` | SYSTEM | Computed from relationship graph |

### ItemRelationship Fields

| Field | Genesis Source | How Populated |
|-------|----------------|---------------|
| `relationship_type` | LLM_SYNTHESIS or EVIDENCE | LLM infers or extraction identifies |
| `confidence` | LLM_SYNTHESIS | LLM's confidence in the relationship |
| `explanation` | LLM_SYNTHESIS | LLM explains why relationship holds |
| `discovered_via` | SYSTEM | Tracks which pool/method found it |

---

## Implementation: The Three Pipelines

### Pipeline 1: Wizard → Items + Basic Scaffolds

```python
async def process_wizard_session(session_id: int):
    """
    After wizard completion:
    1. Create AnalysisItems from user answers
    2. Run LLM synthesis to generate scaffolds
    3. Create genesis records for everything
    """
    session = await get_wizard_session(session_id)

    # Step 1: Create items from wizard answers
    for qa in session.questions_answered:
        item = AnalysisItem(
            content=qa['user_answer'],
            item_type=QUESTION_TO_ITEM_TYPE[qa['key']],
            provenance_type='wizard',
        )
        db.add(item)

        # Create genesis record
        genesis = ContentGenesis(
            target_type='analysis_item',
            target_id=item.id,
            source_pool='wizard',
            wizard_session_id=session_id,
            wizard_question_key=qa['key'],
            user_input_verbatim=qa['user_answer'],
        )
        db.add(genesis)

    # Step 2: LLM synthesis for scaffolds
    synthesis_result = await llm.synthesize_scaffolds(
        definition=session.get_answer('definition'),
        implications=session.get_answers('implications'),
        contradictions=session.get_answers('contradictions'),
    )

    for item_synthesis in synthesis_result['items']:
        # Create scaffold
        scaffold = ItemReasoningScaffold(
            item_id=item_synthesis['item_id'],
            inference_type=item_synthesis['inference_type'],
            reasoning_trace=item_synthesis['reasoning_trace'],
            # ... other fields
        )
        db.add(scaffold)

        # Create premises with genesis
        for premise_data in item_synthesis['premises']:
            premise = ScaffoldPremise(
                scaffold_id=scaffold.id,
                claim=premise_data['claim'],
                claim_type=premise_data['claim_type'],
                centrality=premise_data['centrality'],
            )
            db.add(premise)

            # Genesis for this premise
            if premise_data['derived_from_wizard']:
                genesis = ContentGenesis(
                    target_type='scaffold_premise',
                    target_id=premise.id,
                    source_pool='wizard',
                    wizard_session_id=session_id,
                    wizard_question_key=premise_data['source_question'],
                    derivation_method='extraction',
                )
            else:
                genesis = ContentGenesis(
                    target_type='scaffold_premise',
                    target_id=premise.id,
                    source_pool='wizard',  # Still wizard, but LLM-inferred
                    derivation_method='llm_background_knowledge',
                    derivation_confidence=premise_data['confidence'],
                    needs_verification=True,  # Flag for later evidence verification
                )
            db.add(genesis)
```

### Pipeline 2: Theoretical Source → Evidence Fragments → Items/Relationships

```python
async def process_theoretical_source(source_id: int):
    """
    Extract claims from academic source and integrate.
    """
    source = await get_evidence_source(source_id)

    # Extract relevant fragments
    fragments = await llm.extract_relevant_fragments(
        source_text=source.content,
        concept_definition=concept.definition,
        existing_items=[...],
    )

    for fragment_data in fragments:
        fragment = ConceptEvidenceFragment(
            source_id=source_id,
            content=fragment_data['text'],
            source_location=fragment_data['location'],
        )
        db.add(fragment)

        # Analyze relationship to existing items
        for relationship in fragment_data['relationships']:
            if relationship['confidence'] > 0.85:
                # Auto-integrate
                item_rel = ItemRelationship(
                    source_item_id=create_or_find_item(fragment_data),
                    target_item_id=relationship['target_item_id'],
                    relationship_type=relationship['type'],
                    discovered_via='evidence_extracted',
                    evidence_fragment_id=fragment.id,
                    confidence=relationship['confidence'],
                    explanation=relationship['explanation'],
                )
                db.add(item_rel)

                # Genesis
                genesis = ContentGenesis(
                    target_type='relationship',
                    target_id=item_rel.id,
                    source_pool='theoretical',
                    evidence_source_id=source_id,
                    evidence_fragment_id=fragment.id,
                    passage_text=fragment_data['text'],
                    passage_location=fragment_data['location'],
                    derivation_method='extraction',
                    derivation_confidence=relationship['confidence'],
                )
                db.add(genesis)
            else:
                # Queue for decision
                fragment.analysis_status = 'needs_decision'
```

### Pipeline 3: Empirical Source → Paradigmatic Cases + Validation

```python
async def process_empirical_source(source_id: int):
    """
    Extract real-world instances and validate theoretical claims.
    """
    source = await get_evidence_source(source_id)

    # Extract events/cases
    cases = await llm.extract_empirical_cases(
        source_text=source.content,
        concept_definition=concept.definition,
        theoretical_claims=[...],
    )

    for case_data in cases:
        # Create paradigmatic case item
        item = AnalysisItem(
            content=json.dumps(case_data['case']),
            item_type='paradigmatic_cases',
            provenance_type='evidence',
        )
        db.add(item)

        genesis = ContentGenesis(
            target_type='analysis_item',
            target_id=item.id,
            source_pool='empirical',
            evidence_source_id=source_id,
            passage_text=case_data['source_passage'],
            passage_location=case_data['location'],
        )
        db.add(genesis)

        # Check if this validates any LLM background claims
        for validation in case_data['validates_claims']:
            # Find the claim's genesis
            claim_genesis = await get_genesis_for_item(validation['item_id'])
            if claim_genesis.needs_verification:
                claim_genesis.verified_by_evidence_id = source_id
                claim_genesis.needs_verification = False
```

---

## UI Implications

### 1. Provenance Badges (Enhanced)

Currently we show "[wizard]" or "[evidence]". Enhance to be clickable:

```jsx
function ProvenanceBadge({ item }) {
  const [showDetails, setShowDetails] = useState(false)

  return (
    <>
      <span
        onClick={() => setShowDetails(true)}
        style={{ cursor: 'pointer', textDecoration: 'underline' }}
      >
        {item.provenance_type === 'wizard' && '📝 wizard'}
        {item.provenance_type === 'evidence' && '📚 ' + item.evidence_source_name}
        {item.provenance_type === 'llm_synthesis' && '🤖 synthesized'}
      </span>

      {showDetails && (
        <GenesisDetailModal
          genesisId={item.genesis_id}
          onClose={() => setShowDetails(false)}
        />
      )}
    </>
  )
}
```

### 2. Genesis Detail Modal

```jsx
function GenesisDetailModal({ genesisId }) {
  const genesis = useGenesis(genesisId)

  return (
    <Modal>
      <h3>Origin of this content</h3>

      {genesis.source_pool === 'wizard' && (
        <div>
          <strong>Source:</strong> Concept Wizard (Session #{genesis.wizard_session_id})
          <br/>
          <strong>Question:</strong> {QUESTION_LABELS[genesis.wizard_question_key]}
          <br/>
          <strong>Your answer:</strong> "{genesis.user_input_verbatim}"
          <br/>
          <strong>Date:</strong> {genesis.created_at}
        </div>
      )}

      {genesis.source_pool === 'theoretical' && (
        <div>
          <strong>Source:</strong> {genesis.evidence_source.name}
          <br/>
          <strong>Author:</strong> {genesis.evidence_source.author}
          <br/>
          <strong>Location:</strong> {genesis.passage_location}
          <br/>
          <strong>Passage:</strong> "{genesis.passage_text}"
        </div>
      )}

      {genesis.derivation_method === 'llm_background_knowledge' && (
        <div className="warning">
          ⚠️ This was inferred by the AI from its training data.
          {genesis.needs_verification && (
            <strong> Not yet verified by evidence.</strong>
          )}
          {genesis.verified_by_evidence_id && (
            <span> ✓ Verified by: {genesis.verification_source_name}</span>
          )}
        </div>
      )}
    </Modal>
  )
}
```

### 3. Premise Provenance in Scaffold Display

```jsx
{scaffold.premises?.map((premise, i) => (
  <div key={i} className="premise">
    <div>{premise.claim}</div>
    <ProvenanceBadge genesis={premise.genesis} />
    {premise.genesis.needs_verification && (
      <span className="unverified">⚠️ Unverified AI inference</span>
    )}
  </div>
))}
```

---

## Summary: What Changes

1. **Every piece of content gets a `genesis_id`** linking to ContentGenesis
2. **Wizard sessions are tracked** with all Q&A for audit
3. **LLM-inferred content is flagged** as `needs_verification`
4. **Evidence can "verify"** previously unverified inferences
5. **UI shows full provenance** with click-through to details
6. **Three clear pipelines** for the three source pools

This ensures you can always answer: "Where did this come from?"
