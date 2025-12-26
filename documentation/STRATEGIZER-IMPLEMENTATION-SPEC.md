# Strategizer Implementation Specification

*Comprehensive Implementation Guide — December 2025*

---

## Document Purpose

This is the **authoritative implementation specification** for building the Multi-Domain Strategizer. It synthesizes:
- The 5-unit strategic framework
- Multi-grid analytical architecture (properly scoped)
- Shackle-inspired epistemic infrastructure
- Varsavsky-inspired scenario modeling
- The generative knowledge creation process
- Cross-domain application patterns

**Target:** Hand this document to an implementation session and build the system.

---

# PART 1: CORE ARCHITECTURE

## 1.1 The Full System Stack

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         STRATEGIZER ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ LAYER 5: ARTIFACT                                                      │ │
│  │ The deliverable being built                                            │ │
│  │ • Essay/Book (Theory)                                                  │ │
│  │ • Strategy Document (Foundation)                                       │ │
│  │ • Brand Strategy (Brand)                                               │ │
│  │ • Development Plan (Government)                                        │ │
│  │ • Investment Thesis (Investor)                                         │ │
│  │                                                                        │ │
│  │ Structure: SPINE (thesis/ToC) → PILLARS (sections) → BLOCKS (content)  │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    ↑                                         │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ LAYER 4: THREE-TIER UNIT SYSTEM                                        │ │
│  │ Strategic objects that populate the artifact                           │ │
│  │                                                                        │ │
│  │  TIER 1 (Universal): ┌─────────┐ ┌─────────┐ ┌─────────┐              │ │
│  │  Always present       │ CONCEPT │ │ TENSION │ │  AGENT  │              │ │
│  │                       └─────────┘ └─────────┘ └─────────┘              │ │
│  │                                                                        │ │
│  │  TIER 2 (Domain): Configured per domain — can be renamed, added       │ │
│  │  • Theory: Interlocutor, Framework, Move, Trope                       │ │
│  │  • Foundation: Theory of Change, Grantee Profile, Lever, Exit         │ │
│  │  • Brand: Touchpoint, Campaign, Asset, Moment                         │ │
│  │  • Government: Constraint, Mandate, Path, Instrument                  │ │
│  │  • Investor: Thesis, Signal, Catalyst, Risk Factor, Comparable        │ │
│  │                                                                        │ │
│  │  TIER 3 (Emergent): Discovered through use, promotable to Domain tier │ │
│  │  • LLM detects friction → proposes new unit type → user confirms      │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    ↑                                         │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ LAYER 3: MULTI-GRID ANALYTICAL STRUCTURE                               │ │
│  │ How we decompose/analyze WITHIN each unit type                         │ │
│  │                                                                        │ │
│  │ Same Three-Tier System applies to grids:                               │ │
│  │ • Required grids (LOGICAL, ACTOR, TEMPORAL)                           │ │
│  │ • Flexible grids (domain-specific taxonomy)                           │ │
│  │ • Wildcard grids (LLM-invented, promotable)                           │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    ↑                                         │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ LAYER 2: EPISTEMIC INFRASTRUCTURE (Shackle)                            │ │
│  │ Orthogonal concern — applies to ALL units                              │ │
│  │                                                                        │ │
│  │ • Surprise Profile (potential_surprise, focus_gain/loss)               │ │
│  │ • Cruciality Assessment (reversibility, repeatability, learning)       │ │
│  │ • Kaleidic Triggers (events that reframe everything)                   │ │
│  │ • Epistemic Status (evidence, confidence, assumptions, gaps)           │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    ↑                                         │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ LAYER 1: GENERATIVE INFRASTRUCTURE + BACKGROUND EVOLUTION              │ │
│  │ How units AND unit types get created and refined                       │ │
│  │                                                                        │ │
│  │ FRICTION → DIAGNOSIS → COIN → TEST → ABSTRACT → PROMOTE                │ │
│  │                                                                        │ │
│  │ + LLM-Powered Background Evolution:                                    │ │
│  │   • Unit Type Friction Detection (types don't fit reality)             │ │
│  │   • Refactoring Dashboard (RENAME, MERGE, SPLIT, PROMOTE, HIDE)        │ │
│  │   • Pending Decisions (multi-path with commitment/foreclosure)         │ │
│  │   • Auto-apply or human review based on confidence                     │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    ↑                                         │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ LAYER 0: STABLE DOCTRINE                                               │ │
│  │ Accumulated, validated units per domain                                │ │
│  │                                                                        │ │
│  │ • Theory Doctrine: Concepts, Dialectics, Interlocutors                 │ │
│  │ • Foundation Doctrine: Plays, Strategic Tensions, Actor Models         │ │
│  │ • Brand Doctrine: Positions, Brand Tensions, Market Actor Models       │ │
│  │ • Government Doctrine: Policy Frames, Trade-offs, Development Actors   │ │
│  │ • Investor Doctrine: Theses, Risk Patterns, Catalyst Models            │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 1.2 The 5 Domains

The system serves five strategic domains with parallel but flexible structures:

| Domain | Practitioner | Artifact | Core Challenge |
|--------|--------------|----------|----------------|
| **Theory/Essay** | Scholar, writer | Essay, book, article | Articulate novel concepts; position in debates |
| **Foundation** | Philanthropic strategist | Strategy document | Design effective interventions; navigate actors |
| **Brand** | Brand strategist | Brand strategy | Position in market; navigate tensions |
| **Government** | Development planner | Development plan | Choose development path; coordinate actors |
| **Investor** | Hedge fund/VC analyst | Investment thesis | Test hypotheses against phenomena; allocate capital |

### Default Domain Unit Vocabulary

Each domain starts with a default vocabulary that can evolve through use:

| Universal | Theory | Foundation | Brand | Government | Investor |
|-----------|--------|------------|-------|------------|----------|
| **Concept** | Concept | Play | Position | Policy Frame | Thesis |
| **Tension** | Dialectic | Strategic Tension | Brand Tension | Trade-off | Risk-Reward |
| **Agent** | Interlocutor | Strategic Player | Market Actor | Dev. Actor | Market Force |

### Domain-Specific Unit Types (Tier 2)

| Domain | Additional Unit Types |
|--------|----------------------|
| **Theory** | Framework, Move, Trope, Lineage |
| **Foundation** | Theory of Change, Grantee Profile, Lever, Exit Condition |
| **Brand** | Touchpoint, Campaign, Asset, Moment, Segment |
| **Government** | Constraint, Mandate, Path, Instrument, Sequence |
| **Investor** | Signal, Catalyst, Comparable, Risk Factor, Position Size |

**Key Insight:** These are DEFAULTS, not fixed. The system detects when:
- A unit type is unused (hide it)
- Users keep creating "Other" (need new type)
- Two types are being used interchangeably (merge them)
- One type is doing too much work (split it)

---

## 1.3 The Three-Tier Unit System

The unit system mirrors the grid system: **Universal → Domain → Emergent**. This provides stability where needed while allowing evolution where reality demands it.

### 1.3.1 Why Three Tiers?

**The Problem with Fixed Units:**
If we declare "every domain has exactly 5 units: Concept, Dialectic, Scenario, Actor, Instrument" — we're committing the same error we avoided with grids. We'd be imposing a priori categories rather than letting them emerge from use.

**The Solution:**
```
TIER 1 (Universal):  3 units every domain genuinely needs
                     Cannot be removed, can be renamed (aliased)

TIER 2 (Domain):     4-8 units configured per domain
                     Can be renamed, hidden, merged, split
                     Start with defaults, evolve through use

TIER 3 (Emergent):   Discovered through friction detection
                     LLM proposes → user confirms → promoted to Tier 2
```

### 1.3.2 Tier 1: Universal Units

These three units are genuinely universal — every strategic domain requires them:

#### UNIVERSAL UNIT 1: CONCEPT

**Definition:** A named, reusable way of carving up reality. Crystallized meaning that enables seeing and acting.

**Domain Aliases:**
| Domain | Alias | Examples |
|--------|-------|----------|
| Theory | Concept | "Technological Sovereignty," "Comprador Dependency" |
| Foundation | Play | "Media Ecosystem Resilience," "Institution-First" |
| Brand | Position | "Restrained Intensity," "Heritage Through Novelty" |
| Government | Policy Frame | "Regional Manufacturing Hub," "Green Industrial" |
| Investor | Thesis | "AI Infrastructure Moat," "Regulatory Arbitrage" |

**Base Schema (all domains extend this):**
```python
class ConceptUnit:
    # Identity
    id: str
    name: str
    domain: Domain
    unit_type: str  # "concept" — the universal type
    display_type: str  # "Thesis" — the domain alias

    # Core content (universal)
    definition: str
    what_it_enables: list[str]
    what_it_forecloses: list[str]
    conditions_of_application: list[str]

    # Relations (universal)
    compatible_with: list[str]
    incompatible_with: list[str]
    enables: list[str]

    # Status
    status: UnitStatus
    epistemic_status: EpistemicStatus

    # Domain-specific extensions stored here
    extensions: dict[str, Any]
```

**Domain Extensions:**
```python
# Theory domain adds:
extensions = {
    "derived_from": ["prior", "concepts"],
    "breaks_from": ["rejected", "concepts"],
    "thinkers_lineage": [ThinkerReference(...)]
}

# Investor domain adds:
extensions = {
    "time_horizon": "18-36 months",
    "conviction_level": "high",
    "position_size_guidance": "5-8% of portfolio",
    "key_metrics": ["GPU utilization", "inference cost"]
}
```

**Generative Trigger:**
> "None of our existing [Concepts/Plays/Theses] carve reality correctly. We need to name something new."

---

#### UNIVERSAL UNIT 2: TENSION

**Definition:** A named trade-off that must be navigated, not resolved. Productive opposition that drives strategic work.

**Domain Aliases:**
| Domain | Alias | Examples |
|--------|-------|----------|
| Theory | Dialectic | "Rigor ↔ Accessibility" |
| Foundation | Strategic Tension | "Visibility ↔ Protection" |
| Brand | Brand Tension | "Heritage ↔ Novelty" |
| Government | Trade-off | "Growth ↔ Equity" |
| Investor | Risk-Reward | "Growth ↔ Profitability" |

**Base Schema:**
```python
class TensionUnit:
    id: str
    name: str  # "pole_a ↔ pole_b" format
    domain: Domain
    unit_type: str  # "tension"
    display_type: str  # Domain alias

    # The poles (universal)
    pole_a: Pole
    pole_b: Pole

    # Current position (universal)
    weight_toward_a: float  # 0.0 to 1.0
    position_rationale: str

    # Dynamics (universal)
    what_pushes_toward_a: list[str]
    what_pushes_toward_b: list[str]
    navigation_strategies: list[str]

    # Resolution
    status: TensionStatus  # ACTIVE | SUBLATED | DEPRECATED
    sublated_into: str | None
    sublation_insight: str | None

    epistemic_status: EpistemicStatus
    extensions: dict[str, Any]

class Pole:
    name: str
    description: str
    what_it_prioritizes: list[str]
    what_it_sacrifices: list[str]
    extreme_form: str
```

**Hegelian Move:** Sublation — a higher-order insight dissolves the apparent dichotomy.

---

#### UNIVERSAL UNIT 3: AGENT

**Definition:** An entity with agency whose responses shape outcomes. Active players who constrain and enable.

**Domain Aliases:**
| Domain | Alias | Examples |
|--------|-------|----------|
| Theory | Interlocutor | "Marxist tradition," "Postcolonial critics" |
| Foundation | Strategic Player | "EU," "Government," "Opposition" |
| Brand | Market Actor | "Hermès," "LVMH," "Core customers" |
| Government | Development Actor | "IMF," "China," "Diaspora" |
| Investor | Market Force | "Fed," "Competitors," "Regulators" |

**Base Schema:**
```python
class AgentUnit:
    id: str
    name: str
    domain: Domain
    unit_type: str  # "agent"
    display_type: str  # Domain alias
    agent_type: AgentType  # ALLY | OPPONENT | TARGET | REGULATOR | etc.

    # Profile (universal)
    interests: list[str]
    capabilities: list[str]
    constraints: list[str]
    power_sources: list[str]

    # Behavioral model (universal)
    characteristic_moves: list[str]
    blind_spots: list[str]
    triggers: list[str]

    # Relationship (universal)
    relationship_to_us: Relationship
    coalition_potential: str
    veto_power: bool

    # Response modeling
    response_model: ResponseModel
    scenario_responses: dict[str, ScenarioResponse]

    epistemic_status: EpistemicStatus
    extensions: dict[str, Any]
```

---

### 1.3.3 Tier 2: Domain-Specific Units

These units are **configured per domain** — they start with defaults but can be:
- **Renamed** (alias changes, underlying type preserved)
- **Hidden** (not shown in UI but data preserved)
- **Merged** (two types become one)
- **Split** (one type becomes two)

#### THEORY DOMAIN: Tier 2 Units

| Unit Type | Description | Schema Extension |
|-----------|-------------|------------------|
| **Framework** | A systematic approach to analysis | `stages`, `key_moves`, `outputs` |
| **Move** | A rhetorical/argumentative action | `move_type`, `effect`, `risks` |
| **Trope** | A recurring pattern or figure | `instances`, `variations`, `risks` |
| **Lineage** | An intellectual tradition | `key_figures`, `core_texts`, `positions` |

#### FOUNDATION DOMAIN: Tier 2 Units

| Unit Type | Description | Schema Extension |
|-----------|-------------|------------------|
| **Theory of Change** | Causal mechanism for impact | `inputs`, `mechanisms`, `outcomes`, `assumptions` |
| **Grantee Profile** | Type of organization to fund | `characteristics`, `capacity_requirements` |
| **Lever** | Point of intervention | `leverage_point`, `required_resources` |
| **Exit Condition** | When/how to exit | `success_criteria`, `timeline`, `handoff` |

#### BRAND DOMAIN: Tier 2 Units

| Unit Type | Description | Schema Extension |
|-----------|-------------|------------------|
| **Touchpoint** | Interaction moment | `channel`, `experience_requirements` |
| **Campaign** | Coordinated effort | `objectives`, `channels`, `duration` |
| **Asset** | Owned/earned/paid media | `asset_type`, `ownership`, `refresh_cycle` |
| **Moment** | Cultural/temporal opportunity | `timing`, `relevance`, `response_window` |
| **Segment** | Customer group | `demographics`, `psychographics`, `value` |

#### GOVERNMENT DOMAIN: Tier 2 Units

| Unit Type | Description | Schema Extension |
|-----------|-------------|------------------|
| **Constraint** | What limits action | `constraint_type`, `severity`, `workarounds` |
| **Mandate** | What's required | `source`, `compliance_requirements` |
| **Path** | Varsavsky-style development scenario | `phases`, `value_commitments`, `winners`, `losers` |
| **Instrument** | Policy tool | `mechanism`, `resource_requirements`, `effects` |
| **Sequence** | Order of implementation | `dependencies`, `parallel_tracks` |

#### INVESTOR DOMAIN: Tier 2 Units

| Unit Type | Description | Schema Extension |
|-----------|-------------|------------------|
| **Signal** | Indicator of thesis playing out | `metric`, `threshold`, `lead_time` |
| **Catalyst** | Trigger for value realization | `event_type`, `timing`, `probability` |
| **Comparable** | Analogous situation | `similarity_dimensions`, `outcome`, `lessons` |
| **Risk Factor** | What could go wrong | `risk_type`, `mitigation`, `hedging` |
| **Position Size** | Allocation guidance | `conviction_level`, `sizing_logic`, `constraints` |

---

### 1.3.4 Tier 3: Emergent Units

Emergent units are discovered through **friction detection** — when existing types don't fit reality.

**Schema:**
```python
class EmergentUnitType:
    id: str
    proposed_name: str  # "Cautionary Tale"
    domain: Domain
    extends_universal: str  # "concept" — what base type it extends

    # Justification
    why_needed: str  # "Existing concepts don't capture..."
    friction_source: FrictionSource  # Which friction events led to this
    example_instances: list[str]  # Concrete examples

    # Distinctiveness
    distinctiveness_score: float
    similar_to: list[str]  # Existing types it resembles
    key_differentiators: list[str]  # What makes it distinct

    # Usage tracking
    usage_count: int
    projects_using: list[str]

    # Promotion
    status: EmergentStatus  # PROPOSED | TESTING | PROMOTED | REJECTED
    promoted_at: datetime | None
    promoted_to_tier: int | None  # 2 if promoted

    # Schema
    proposed_schema: dict  # Additional fields this type needs
```

**Promotion Criteria:**
```python
def should_promote_unit_type(proposal: EmergentUnitType) -> bool:
    return (
        proposal.usage_count >= 5 and
        proposal.distinctiveness_score > 0.7 and
        len(proposal.projects_using) >= 2 and
        not subsumable_by_existing(proposal)
    )
```

**Examples of Emergent Types:**
- **Theory:** "Cautionary Tale" — examples that warn rather than inspire
- **Foundation:** "Veto Player" — actor who can block but not create
- **Brand:** "Anti-Persona" — who we explicitly don't serve
- **Government:** "Implementation Bottleneck" — capacity constraint
- **Investor:** "Valuation Anchor" — comparable that sets expectations

---

## 1.4 Unit Type Refactoring Operations

Just as essay-flow has a Refactoring Dashboard for throughlines (SPLIT, MERGE, CLONE, REFRAME), the Strategizer has refactoring operations for **unit types themselves**.

### 1.4.1 The Operations

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    UNIT TYPE REFACTORING OPERATIONS                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  RENAME    Change the display name without changing underlying type          │
│            "Dialectic" → "Productive Tension" (alias, same schema)          │
│                                                                              │
│  HIDE      Remove from UI without deleting data                              │
│            "Trope" hidden in this project (unused but preserved)            │
│                                                                              │
│  MERGE     Combine two types that are being used interchangeably            │
│            "Signal" + "Indicator" → "Signal" (migrate all instances)        │
│                                                                              │
│  SPLIT     Divide one type that's doing too much work                        │
│            "Actor" → "Ally" + "Opponent" + "Regulator"                       │
│                                                                              │
│  PROMOTE   Move emergent type to Tier 2 (domain-specific)                    │
│            "Valuation Anchor" (Tier 3) → (Tier 2)                           │
│                                                                              │
│  CREATE    LLM proposes entirely new type based on friction                  │
│            Friction detected → "Cautionary Tale" proposed                    │
│                                                                              │
│  DEMOTE    Move unused Tier 2 type to "available but hidden"                 │
│            "Trope" demoted after 6 months of no use                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.4.2 Refactoring Dashboard for Unit Types

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Unit Type Refactoring Dashboard                                             │
│  Investor Domain — Q1 2025 Project                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  3 Confirmed      2 Pending       47 Units         8 Active Types           │
│  Operations       /Previewing     Affected                                   │
│                                                                              │
│  Active Unit Types [8]                                                   ▼   │
│                                                                              │
│  [+ Create New] [Rename] [Merge] [Split] [Hide] [Promote Emergent]          │
│                                                                              │
│  ┌─ Recent Operations ─────────────────────────────────────────────────────┐│
│  │                                                                         ││
│  │  [RENAME] "Risk-Reward" → "Core Tension"                     confirmed ││
│  │           Rationale: "Risk-Reward" too narrow for all tensions         ││
│  │                                                                         ││
│  │  [MERGE] "Signal" + "Leading Indicator" → "Signal"           confirmed ││
│  │          12 instances migrated                                          ││
│  │                                                                         ││
│  │  [PROMOTE] "Valuation Anchor" (emergent → Tier 2)            confirmed ││
│  │            Used 8 times across 3 projects                               ││
│  │                                                                         ││
│  │  [PENDING] [SPLIT] "Market Force" → "Macro Force" + "Micro Force"      ││
│  │            LLM detected: some forces are economy-wide,                  ││
│  │            others are company-specific                                  ││
│  │            [Preview] [Accept] [Reject]                                  ││
│  │                                                                         ││
│  │  [PENDING] [CREATE] New type: "Regime Change"                          ││
│  │            Friction: Users creating "Concepts" for political shifts    ││
│  │            that aren't really investment theses                         ││
│  │            [Preview Schema] [Accept] [Reject]                           ││
│  │                                                                         ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─ Current Type Usage ────────────────────────────────────────────────────┐│
│  │  Thesis (Concept)              14 instances    ✓                        ││
│  │  Core Tension (Tension)         8 instances    ✓                        ││
│  │  Market Force (Agent)          11 instances    ✓                        ││
│  │  Signal                        18 instances    ✓                        ││
│  │  Catalyst                       9 instances    ✓                        ││
│  │  Comparable                     7 instances    ✓                        ││
│  │  Risk Factor                   12 instances    ✓                        ││
│  │  Valuation Anchor               8 instances    ★ newly promoted         ││
│  │                                                                         ││
│  │  ⚠️ Unused types: Position Size (0), Lineage (0)                       ││
│  │  💡 Suggestion: Hide unused types?                                      ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.4.3 Schema for Unit Type Operations

```python
class UnitTypeOperation:
    id: str
    operation_type: OperationType  # RENAME | HIDE | MERGE | SPLIT | PROMOTE | CREATE | DEMOTE
    domain: Domain
    timestamp: datetime

    # What's being changed
    source_types: list[str]  # Type IDs being operated on
    target_types: list[str]  # Resulting type IDs

    # Justification
    rationale: str
    friction_source: FrictionEvent | None  # What triggered this
    confidence: float

    # Impact
    affected_units: list[str]  # Unit IDs that will be affected
    migration_plan: dict  # How to migrate instances

    # Status
    status: OperationStatus  # PROPOSED | PENDING | CONFIRMED | APPLIED | REJECTED

class OperationType(Enum):
    RENAME = "rename"
    HIDE = "hide"
    MERGE = "merge"
    SPLIT = "split"
    PROMOTE = "promote"
    CREATE = "create"
    DEMOTE = "demote"
```

---

## 1.5 LLM-Powered Background Evolution

The critical insight from essay-flow: **flexibility should be emergent through use, not upfront configuration**. Users don't need to configure unit types manually — the LLM detects when reality doesn't fit the current schema and proposes changes.

### 1.5.0 The LLM-First Principle

**CRITICAL DESIGN PRINCIPLE:** This system is LLM-first, not Python-first.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LLM-FIRST vs PYTHON-FIRST                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PYTHON-FIRST (What We DON'T Do)                                            │
│  ─────────────────────────────────                                          │
│  • Hardcoded thresholds: if other_ratio > 0.20                              │
│  • Numeric cutoffs: if confidence >= 0.85                                   │
│  • Rule-based pattern matching: if usage_count >= 5                         │
│  • Boolean logic for judgment calls                                         │
│                                                                              │
│  Problem: Thresholds are arbitrary. 0.20 vs 0.19? 5 vs 4? These encode     │
│  human judgment in the wrong place — hardcoded where it should be contextual│
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────── │
│                                                                              │
│  LLM-FIRST (What We Do)                                                      │
│  ─────────────────────────                                                   │
│  • LLM assessment: "Does this pattern suggest we need a new unit type?"     │
│  • LLM judgment: "Is this change significant enough to surface to user?"    │
│  • LLM holistic evaluation: "Has this type proven useful enough to promote?"│
│  • Contextual reasoning over mechanical rules                               │
│                                                                              │
│  Benefit: LLMs can weigh multiple factors, understand context, and make    │
│  nuanced judgments that rigid thresholds cannot.                            │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────── │
│                                                                              │
│  WHEN TO USE PYTHON                                                          │
│  ────────────────────                                                        │
│  • Data retrieval and aggregation (gather evidence for LLM)                 │
│  • Storage and persistence (save LLM decisions)                             │
│  • Orchestration (coordinate LLM calls)                                     │
│  • Mechanical operations (no judgment involved)                             │
│                                                                              │
│  Python gathers data → LLM makes judgments → Python executes decisions      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.5.1 The Background Evolution Loop

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LLM-POWERED BACKGROUND EVOLUTION                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ 1. FRICTION DETECTION (Continuous, Background)                          ││
│  │                                                                         ││
│  │ LLM monitors for signals that current types don't fit reality:          ││
│  │                                                                         ││
│  │ • "Other" type usage > 20% in any category                              ││
│  │ • Description/content mismatch with type definition                     ││
│  │ • Users editing type names in free-text fields                          ││
│  │ • Two types with >80% field overlap being used differently              ││
│  │ • One type with bimodal content distribution (should split?)            ││
│  │ • Type unused for 6+ months (should hide?)                              ││
│  │                                                                         ││
│  └────────────────────────────────────┬────────────────────────────────────┘│
│                                       │                                      │
│                                       ▼                                      │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ 2. DIAGNOSIS + PROPOSAL GENERATION                                       ││
│  │                                                                         ││
│  │ When friction detected, LLM generates:                                   ││
│  │                                                                         ││
│  │ • Diagnosis: What's not working and why                                 ││
│  │ • Proposed operation: MERGE, SPLIT, RENAME, CREATE, HIDE                ││
│  │ • Migration plan: How existing instances would be affected              ││
│  │ • Confidence score: How certain is this the right fix                   ││
│  │ • Commitment statement: "This commits you to..."                        ││
│  │ • Foreclosure statement: "This means passing on..."                     ││
│  │                                                                         ││
│  └────────────────────────────────────┬────────────────────────────────────┘│
│                                       │                                      │
│                                       ▼                                      │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ 3. ROUTING (LLM-Assessed, Not Threshold-Based)                          ││
│  │                                                                         ││
│  │  The LLM holistically evaluates each proposal and recommends routing:   ││
│  │                                                                         ││
│  │  AUTO-APPLY route:                                                      ││
│  │  ────────────────────────────────────────────────────────               ││
│  │  LLM determines: "This is a clear improvement with minimal disruption.  ││
│  │  User would likely accept. Safe to apply with undo option."             ││
│  │  → Notification: "Renamed 'Risk-Reward' to 'Core Tension'"              ││
│  │                                                                         ││
│  │  PENDING DECISION route:                                                ││
│  │  ────────────────────────────────────────────────────────               ││
│  │  LLM determines: "This involves meaningful trade-offs or affects work   ││
│  │  user cares about. Requires human judgment."                            ││
│  │  → Multi-path UI with commitment/foreclosure articulation               ││
│  │                                                                         ││
│  │  SUGGESTION route:                                                      ││
│  │  ────────────────────────────────────────────────────────               ││
│  │  LLM determines: "This might help but I'm uncertain. Worth mentioning   ││
│  │  but not worth interrupting workflow."                                  ││
│  │  → "LLM noticed you might benefit from..."                              ││
│  │                                                                         ││
│  │  NOTE: No hardcoded thresholds (≥85%, <60%). LLM reasons contextually. ││
│  │                                                                         ││
│  └────────────────────────────────────┬────────────────────────────────────┘│
│                                       │                                      │
│                                       ▼                                      │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ 4. LEARNING CAPTURE                                                      ││
│  │                                                                         ││
│  │ When user confirms/rejects proposals:                                   ││
│  │                                                                         ││
│  │ • Store decision + context as training examples for LLM prompts         ││
│  │ • Record domain-specific patterns ("Investor domain splits more")       ││
│  │ • Cross-project learning ("If Project A did this, suggest to B")        ││
│  │ • Calibrate LLM judgment based on user feedback                         ││
│  │ • Build corpus of accepted/rejected proposals for future context        ││
│  │                                                                         ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.5.2 Friction Detection Signals

```python
class FrictionSignal:
    signal_type: FrictionType
    severity: float  # 0.0 to 1.0
    evidence: list[str]  # Specific instances
    affected_type: str
    domain: Domain
    detected_at: datetime

class FrictionType(Enum):
    OTHER_OVERUSE = "other_overuse"           # Too many "Other" selections
    CONTENT_MISMATCH = "content_mismatch"     # Content doesn't match type
    NAME_EDITING = "name_editing"             # Users editing type names
    OVERLAP_CONFUSION = "overlap_confusion"   # Two types used interchangeably
    BIMODAL_DISTRIBUTION = "bimodal"          # One type doing two jobs
    DISUSE = "disuse"                         # Type not used
    FORCED_FIT = "forced_fit"                 # Content clearly doesn't belong

class FrictionDetector:
    """
    LLM-FIRST friction detection.

    Python gathers evidence → LLM judges whether friction exists.
    No hardcoded thresholds like "other_ratio > 0.20".
    """

    async def scan_project(self, project: Project, llm: LLM) -> list[FrictionSignal]:
        # PYTHON: Gather all evidence
        evidence_package = await self._gather_evidence(project)

        # LLM: Holistic assessment of whether friction exists
        prompt = f"""
        Analyze this project's unit type usage for signs of friction —
        places where the current type system doesn't fit reality.

        PROJECT EVIDENCE:
        {evidence_package.to_yaml()}

        EXISTING UNIT TYPES:
        {project.domain_config.unit_types}

        Consider these friction patterns:
        1. "Other" overuse — Are users putting things in "Other" that deserve their own type?
        2. Content-type mismatch — Does content inside types not match type definitions?
        3. Name editing — Are users overriding type names in free-text?
        4. Overlap confusion — Are two types being used interchangeably?
        5. Bimodal distribution — Is one type doing two different jobs?
        6. Disuse — Are any types never used?
        7. Forced fit — Is content clearly shoehorned into wrong types?

        For each friction you detect, provide:
        - signal_type: Which pattern
        - severity: How important is this (LOW, MEDIUM, HIGH, CRITICAL)
        - evidence: Specific examples from the project
        - affected_type: Which type is affected
        - rationale: Why you believe this is friction

        Return as YAML list. Return empty list if no friction detected.
        """

        response = await llm.generate(prompt)
        friction_signals = parse_friction_signals(response)

        return friction_signals

    async def _gather_evidence(self, project: Project) -> EvidencePackage:
        """
        PYTHON: Mechanical data gathering — no judgment.
        """
        return EvidencePackage(
            other_count=await self.count_other_instances(project),
            total_count=await self.count_all_instances(project),
            type_distribution=await self.get_type_distribution(project),
            sample_content_per_type=await self.sample_content(project, n=5),
            user_edits=await self.get_user_type_name_edits(project),
            unused_types=await self.find_unused_types(project),
            last_activity_per_type=await self.get_last_activity(project)
        )
```

### 1.5.3 Pending Decisions UI for Type Operations

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PENDING DECISION: Unit Type Restructuring                                   │
│                                                                              │
│  FRICTION DETECTED: "Market Force" appears to be doing two different jobs   │
│                                                                              │
│  Evidence:                                                                   │
│  • 11 instances total                                                        │
│  • 6 instances describe economy-wide forces (Fed, inflation, rates)         │
│  • 5 instances describe company-specific forces (competitors, management)   │
│  • Content clustering shows clear separation (0.87 silhouette score)        │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  [AI pick] [A] SPLIT into "Macro Force" + "Micro Force"        82% conf     │
│            [B] Keep as is, add sub-type field                  71% conf     │
│            [C] Create filtering tags instead                   65% conf     │
│                                                                              │
│  ┌─ PATH A COMMITS YOU TO: ────────────────────────────────────────────────┐│
│  │ Two distinct unit types with different analytical implications.          ││
│  │ Macro forces get TEMPORAL grid by default; Micro forces get ACTOR grid. ││
│  │ 11 instances will be migrated (6 → Macro, 5 → Micro).                   ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─ A OVER B: YOU'RE PASSING ON: ──────────────────────────────────────────┐│
│  │ Keeping a single type with optional sub-categorization.                  ││
│  │ Would require adding "force_scope: macro|micro" field.                  ││
│  │ Simpler migration but less analytical clarity.                           ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  Operations if A selected:                                                   │
│  ├─ [CREATE] New type: "Macro Force" (inherits from Agent)                  │
│  ├─ [CREATE] New type: "Micro Force" (inherits from Agent)                  │
│  ├─ [MIGRATE] 6 instances → "Macro Force"                                   │
│  ├─ [MIGRATE] 5 instances → "Micro Force"                                   │
│  └─ [HIDE] Original "Market Force" type                                     │
│                                                                              │
│                                            [Skip for now] [Accept A]         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.5.4 Integration with Essay-Flow Patterns

The Strategizer's background evolution directly mirrors essay-flow's patterns:

| Essay-Flow Pattern | Strategizer Equivalent |
|--------------------|------------------------|
| Evidence dual-track processing | Type operation routing (auto-apply vs. pending) |
| Multi-path pending decisions | Type restructuring proposals with A/B/C paths |
| Commitment/foreclosure articulation | "Path A commits you to..." / "You're passing on..." |
| Skeleton restructuring suggestions | Type restructuring suggestions |
| Refactoring dashboard | Unit Type Refactoring Dashboard |
| Strategic Advisor | LLM analysis for overlaps, gaps, cleanup |
| Session commitment tracking | Type operation audit trail |
| Theory testing | Type-content fit analysis |

### 1.5.5 The "Users Don't Need to Know" Principle

Most users will never see the type refactoring infrastructure. Instead:

1. **They just work** — creating units, filling content
2. **System adapts silently** — auto-applied changes with subtle notifications
3. **Only complex decisions surface** — high-impact changes require input
4. **Learning is captured** — future projects benefit from past decisions

This is the essay-flow philosophy applied to the meta-level: **the schema itself evolves through use**.

---

## 1.6 How Units Interact

```
                    ┌─────────────────────────────┐
                    │         SCENARIOS           │
                    │    (possible futures)       │
                    │                             │
                    │  Each scenario embeds:      │
                    │  • Value commitments        │
                    │  • Trade-off resolutions    │
                    │  • Branching points         │
                    └──────────────┬──────────────┘
                                   │
                                   │ Scenarios bundle concepts,
                                   │ resolve dialectics,
                                   │ and sequence instruments
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
              ▼                    ▼                    ▼
     ┌────────────────┐   ┌────────────────┐   ┌────────────────┐
     │    CONCEPTS    │   │   DIALECTICS   │   │  INSTRUMENTS   │
     │ (how we frame) │◄──│ (tensions to   │──►│ (what we can   │
     │                │   │  navigate)     │   │  do)           │
     │ Concepts shape │   │                │   │                │
     │ what we see    │   │ Dialectics     │   │ Instruments    │
     │                │   │ constrain      │   │ determine      │
     │                │   │ choices        │   │ reachability   │
     └────────┬───────┘   └────────────────┘   └───────┬────────┘
              │                                        │
              │           ┌────────────────┐           │
              └──────────►│    ACTORS      │◄──────────┘
                          │ (who responds) │
                          │                │
                          │ Actors respond │
                          │ to instruments;│
                          │ their responses│
                          │ determine which│
                          │ scenario       │
                          │ actually       │
                          │ unfolds        │
                          └────────────────┘
```

**The Dynamics:**

1. **Concepts** frame how we see the situation — they shape which scenarios seem possible and which seem absurd

2. **Dialectics** reveal tensions that must be navigated — they constrain scenario choice (each scenario implicitly resolves some dialectics)

3. **Scenarios** are coherent paths through time — they bundle concepts, resolve dialectics (by weighting one pole), and sequence instruments

4. **Instruments** are how we act — they shape which scenarios are reachable given our resources and constraints

5. **Actors** respond to our instruments — their responses determine which scenario actually unfolds (vs. which we intended)

---

*End of Part 1. Part 2 covers the Multi-Grid Analytical Layer.*

---

# PART 2: MULTI-GRID ANALYTICAL LAYER

## 2.0 User Experience Philosophy: Attention-Only-On-Friction

**The core insight:** User attention is a scarce, depletable resource. The system should consume it only when human judgment is actually required.

### 2.0.1 The Speculative Engine

The user comes to this software with a **project** — something they're trying to think through. Our goal is to help them develop a **speculative engine**: a generative framework that enables hypothesis formation and possibility exploration for their specific situation.

This "conceptual straightjacket" (in a good sense — like scientific paradigms that enable rather than constrain) emerges from **three sources**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    THREE SOURCES OF FRAMEWORK ENRICHMENT                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ 1. LLM ANALYSIS                                                          ││
│  │                                                                         ││
│  │    As user works, LLM continuously:                                     ││
│  │    • Develops conceptual structure from project materials               ││
│  │    • Applies grids to emerging units                                    ││
│  │    • Detects patterns, tensions, gaps                                   ││
│  │    • Proposes unit types, grid types, relationships                     ││
│  │                                                                         ││
│  │    All this happens in BACKGROUND — user doesn't need to know.          ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ 2. LLM-GENERATED QUESTIONS TO USER                                       ││
│  │                                                                         ││
│  │    When LLM can't resolve something itself:                             ││
│  │    • Ambiguities requiring value judgment                               ││
│  │    • Framework choices with tradeoffs                                   ││
│  │    • Empirical uncertainties needing user knowledge                     ││
│  │                                                                         ││
│  │    Questions are FRICTION-GATED — only asked when necessary.            ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ 3. EXTERNAL LITERATURE FETCHING                                          ││
│  │                                                                         ││
│  │    System proactively fetches:                                          ││
│  │    • Scholarly papers relevant to project domain                        ││
│  │    • Empirical data that could inform units                             ││
│  │    • Competing frameworks for comparison                                ││
│  │                                                                         ││
│  │    Integration is AUTOMATIC if high-confidence fit.                     ││
│  │    User only sees when something CHALLENGES the framework.              ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.0.2 The Attention Economics Principle

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ATTENTION ALLOCATION LOGIC                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  SMOOTH OPERATIONS (No User Attention Required)                              │
│  ──────────────────────────────────────────────────                          │
│  • Theory application to new domain                                          │
│  • Evidence accumulation that confirms framework                             │
│  • Grid filling with high-confidence content                                 │
│  • Unit creation that fits existing taxonomy                                 │
│  • Cross-references between compatible units                                 │
│  • Literature that deepens existing understanding                            │
│                                                                              │
│  → These happen in BACKGROUND. User may not even know.                       │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────── │
│                                                                              │
│  FRICTION OPERATIONS (User Attention Required)                               │
│  ──────────────────────────────────────────────────                          │
│  • New content that CHALLENGES existing framework                            │
│  • Evidence that CONTRADICTS established units                               │
│  • Grid slots that produce CONFLICTING analyses                              │
│  • Unit types that DON'T FIT the current taxonomy                            │
│  • Literature that suggests ALTERNATIVE frameworks                           │
│  • Tradeoffs that require VALUE JUDGMENT                                     │
│                                                                              │
│  → These SURFACE to user with multiple resolution paths.                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.0.3 Friction-Gated Surfacing

When friction is detected, the system doesn't just alert — it **provides resolution paths**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ⚠️  Framework Tension Detected                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  The new evidence about [X] doesn't fit your current framework:             │
│                                                                              │
│  • Your framework says: [current thesis]                                     │
│  • The evidence suggests: [challenging finding]                             │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────── │
│                                                                              │
│  Resolution Paths:                                                           │
│                                                                              │
│  [A] Revise your framework to accommodate this                     ★ AI pick │
│      COMMITS YOU TO: Broader scope, less precision                          │
│      YOU'RE PASSING ON: The simpler, more focused original thesis           │
│                                                                              │
│  [B] Treat this as an exception to the rule                                 │
│      COMMITS YOU TO: Acknowledging boundary conditions                      │
│      YOU'RE PASSING ON: The universality of your framework                  │
│                                                                              │
│  [C] Reject this evidence as methodologically flawed                        │
│      COMMITS YOU TO: Defending your methodology choice                      │
│      YOU'RE PASSING ON: This potential source of insight                    │
│                                                                              │
│  [D] Split into two sub-frameworks for different conditions                 │
│      COMMITS YOU TO: More complexity, conditional claims                    │
│      YOU'RE PASSING ON: Unified explanatory simplicity                      │
│                                                                              │
│                                            [Choose Path] [Defer for Later]  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.0.4 What This Means for Grids

Grids are **not** something users actively "apply" and "fill". Instead:

1. **LLM applies grids in background** as units are created
2. **LLM fills slots** from available materials
3. **Gaps are detected** and either:
   - Auto-resolved via literature fetching
   - Surfaced as questions if user knowledge required
4. **Contradictions are detected** across grids and surfaced as friction
5. **New grid types are proposed** when existing ones don't fit

The user experiences grids as **insights that surface** rather than **forms to fill**.

---

## 2.1 What Multi-Grid IS (and ISN'T)

**Multi-Grid is Layer 3** — an analytical infrastructure that operates WITHIN each unit type. It provides structured ways to decompose, analyze, and cross-reference units.

### What Multi-Grid IS:
- **Analytical lenses** for examining units from different angles
- **Slot systems** that organize content within units
- **Cross-referencing** across dimension values
- **A vocabulary** for structured thinking

### What Multi-Grid IS NOT:
- ❌ NOT a replacement for the Three-Tier Unit System
- ❌ NOT where domain-specific units live (those are Layer 4)
- ❌ NOT the whole system — just Layer 3
- ❌ NOT something users actively interact with (that's background LLM work)
- ❌ NOT mandatory for all units (some units don't need grid analysis)

**The key insight:** Each UNIT (whether Universal, Domain, or Emergent) can be analyzed through MULTIPLE GRID TYPES. Grids are lenses that operate in background, surfacing only when they detect friction.

---

## 2.2 The Three-Tier Grid System

Not all grids are equal. Some provide essential structure, others offer taxonomic richness, others emerge from LLM insight.

### TIER 1: Required Grids (Always Present)

These core analytical dimensions apply across all unit types:

| Grid | Slots | What It Does |
|------|-------|--------------|
| **LOGICAL** | Claim, Evidence, Warrant, Counter, Rebuttal | Argumentation structure — any unit making claims |
| **ACTOR** | Interests, Capabilities, Constraints, Coalition | Actor mapping — any unit involving agency |
| **TEMPORAL** | Past, Present, Future, Horizon | Time structure — any unit with temporal development |

Every unit can be analyzed through at least one Required Grid. They're the baseline.

### TIER 2: Flexible Grids (Taxonomic)

Pre-defined grids from domain expertise. Selected based on **Universal unit tier** and context. Since Domain and Emergent units extend Universal types, they inherit these grid applicabilities.

**For CONCEPT-family units** (includes domain aliases like Thesis, Play, Position, Frame, Investment Thesis):
| Grid | Slots | When Applied |
|------|-------|--------------|
| **ETYMOLOGICAL** | Origin, Evolution, Current, Drift | Background — understanding concept history |
| **FUNCTIONAL** | What_Enables, What_Forecloses, Conditions | Auto — core to concept definition |
| **GENEALOGICAL** | Precursors, Breaks_From, Leads_To | Background — tracing intellectual lineage |
| **COMPARATIVE** | Similar_Concepts, Key_Differentiators, Hybrid_Potential | Auto — surfaces when similar concepts detected |
| **DEFINITIONAL** | Core_Claim, Boundary_Conditions, Edge_Cases | Auto — core to concept identity |

**For TENSION-family units** (includes domain aliases like Dialectic, Trade-off, Signal Tension):
| Grid | Slots | When Applied |
|------|-------|--------------|
| **POLE** | Pole_A, Pole_B, Extreme_A, Extreme_B | Auto — core to tension structure |
| **NAVIGATION** | Current_Position, Push_Toward_A, Push_Toward_B, Strategies | Surfaces when decision needed |
| **SUBLATION** | Insight, Higher_Order_Concept, Dissolved_By | Surfaces when resolution detected |
| **POLITICAL** | Who_Benefits_From_A, Who_Benefits_From_B, Mediators | Background — actor implications |

**For AGENT-family units** (includes domain aliases like Actor, Player, Market Force, Stakeholder):
| Grid | Slots | When Applied |
|------|-------|--------------|
| **INTEREST** | Wants, Fears, Core_Commitments, Deal_Breakers | Auto — core to agent modeling |
| **CAPABILITY** | Resources, Allies, Veto_Power, Constraints | Auto — understanding what agent can do |
| **BEHAVIORAL** | Typical_Moves, Blind_Spots, Triggers | Background — predicting responses |
| **COALITION** | Alignment_Potential, Opposition_Potential, Conditions | Surfaces when coalition analysis needed |
| **RESPONSE** | To_Change_A, To_Change_B, Under_Pressure | Auto — how agent responds to scenarios |

**For Domain-Specific units** (Tier 2 units like Scenario, Instrument, Signal, Catalyst):

These are configured per-domain in the Domain Registry (see Part 5). Examples:

| Domain | Unit Type | Applicable Grids |
|--------|-----------|------------------|
| Theory | Trope | GENEALOGICAL, FUNCTIONAL, RHETORICAL |
| Theory | Development Style | VALUE, SEQUENCE, ACTOR |
| Foundation | Initiative | RESOURCE, PATH, MECHANISM |
| Brand | Touchpoint | FUNCTIONAL, TEMPORAL, EXPERIENTIAL |
| Government | Policy Instrument | MECHANISM, RESOURCE, POLITICAL |
| Investor | Signal | TEMPORAL, EVIDENTIAL, CONFIDENCE |
| Investor | Catalyst | SEQUENCE, PROBABILITY, ACTOR |

**For Emergent units** (Tier 3):

When a new unit type is proposed, the LLM also proposes applicable grids:

```python
class EmergentGridAssignment:
    unit_type: str  # "Cautionary Tale"
    proposed_grids: list[str]  # ["GENEALOGICAL", "RHETORICAL", "AFFECTIVE"]
    rationale: str  # "Cautionary tales need origin story, rhetorical function, emotional impact"
```

### TIER 3: Wildcard Grids (LLM-Invented)

When material doesn't fit Required or Flexible grids, the LLM can propose new analytical lenses:

```python
class WildcardGrid:
    # Identity
    id: str  # e.g., "GRID_WC_20241226_001"
    name: str  # e.g., "LEGITIMACY"
    invented_by: str  # "claude-3-opus" / "gpt-4" / etc.

    # Specification
    slots: list[str]  # The dimension values
    description: str  # What this grid reveals
    what_it_sees: str  # What becomes visible through this lens
    what_it_misses: str  # Blind spots of this lens

    # Status
    status: WildcardStatus  # PROPOSED | VALIDATED | PROMOTED | REJECTED
    uses_count: int  # How often applied
    usefulness_ratings: list[float]  # 1-5 ratings per use

    # Promotion tracking
    promoted_at: datetime | None
    promoted_to_tier: int | None  # 2 = Flexible taxonomy
    rejection_reason: str | None
```

**Promotion Logic (LLM-First):**

```python
async def evaluate_wildcard_promotion(grid: WildcardGrid, llm: LLM) -> PromotionDecision:
    """
    LLM-FIRST: When should a wildcard become part of the Flexible taxonomy?

    No hardcoded thresholds (uses_count < 3, avg >= 4.0, etc.).
    LLM holistically evaluates the grid's usefulness and fit.
    """

    # PYTHON: Gather evidence about grid's performance
    evidence = GridEvaluationEvidence(
        uses_count=grid.uses_count,
        usefulness_ratings=grid.usefulness_ratings,
        sample_applications=await get_sample_grid_applications(grid.id, n=5),
        user_feedback=await get_user_feedback(grid.id),
        similar_existing_grids=await find_similar_grids(grid.name, grid.slots),
        domains_used_in=await get_domains_where_used(grid.id)
    )

    # LLM: Holistic promotion decision
    prompt = f"""
    Evaluate whether this wildcard grid should be promoted to the Flexible taxonomy.

    GRID DETAILS:
    Name: {grid.name}
    Slots: {grid.slots}
    What it sees: {grid.what_it_sees}
    What it misses: {grid.what_it_misses}

    USAGE EVIDENCE:
    {evidence.to_yaml()}

    Consider:
    1. Is this grid genuinely useful? (Not just used, but providing insight)
    2. Is it distinct from existing grids? (Not duplicating LOGICAL, ACTOR, etc.)
    3. Is it generalizable? (Useful beyond the specific project that spawned it)
    4. Are the slots well-defined and coherent?
    5. Would promoting it add value to the taxonomy?

    Decide:
    - PROMOTE_TO_FLEXIBLE: This grid earned its place in the standard toolkit
    - KEEP_AS_WILDCARD: Useful but too specialized or needs more evidence
    - DEPRECATE: Not providing enough value, retire it
    - TOO_EARLY: Insufficient evidence to judge (needs more applications)

    Provide decision and detailed rationale.
    """

    response = await llm.generate(prompt)
    return parse_promotion_decision(response)
```

---

## 2.3 Grid Instantiation Schema

When a grid is APPLIED to a unit, it creates a GridInstance:

```python
class GridInstance:
    # Identity
    id: str
    grid_type: str  # e.g., "LOGICAL", "ACTOR", "WC_LEGITIMACY"
    tier: int  # 1, 2, or 3
    unit_id: str  # The unit this instance analyzes

    # Content
    filled_slots: dict[str, SlotContent]  # slot_name → content

    # Metadata
    created_at: datetime
    created_by: str  # "user" | "llm" | "system"
    last_modified: datetime

    # Quality
    completeness: float  # 0-1, % slots filled
    confidence: float  # 0-1, how confident in accuracy
    saturation_flags: dict[str, bool]  # Which slots are "done"

class SlotContent:
    value: str | list[str]  # The content
    evidence: list[str]  # Sources/justification
    needs_research: bool  # Gap detected?
    confidence: float  # 0-1

    # For comparative slots
    cross_references: list[CrossReference]

class CrossReference:
    target_unit_id: str
    relationship: str  # "similar_to", "opposes", "enables", etc.
    note: str
```

---

## 2.4 Grid Operations

### Operation 1: Apply Grid (LLM-First Compatibility)

```python
async def apply_grid(unit: Unit, grid_type: str, llm: LLM) -> GridInstance:
    """
    LLM-FIRST: Create a new grid instance for a unit.

    Grid compatibility is NOT just type-matching. LLM assesses whether
    this grid makes sense for this particular unit's content.
    """

    if grid_type in TIER_1_GRIDS:
        grid_def = get_tier_1_grid(grid_type)
        # Tier 1 always allowed
    elif grid_type in TIER_2_GRIDS:
        grid_def = get_tier_2_grid(grid_type)
        # LLM assesses compatibility instead of type-matching
        compatibility = await llm.assess_grid_compatibility(
            unit_content=unit.content,
            unit_type=unit.unit_type,
            grid_definition=grid_def
        )
        if not compatibility.is_compatible:
            raise IncompatibleGridError(
                f"{grid_type} may not fit this unit: {compatibility.reason}"
            )
    else:
        # Must be wildcard
        grid_def = get_or_create_wildcard(grid_type)

    # Create instance with empty slots
    instance = GridInstance(
        id=generate_id(),
        grid_type=grid_type,
        tier=grid_def.tier,
        unit_id=unit.id,
        filled_slots={slot: SlotContent(value="", evidence=[], needs_research=False, confidence=0.0)
                      for slot in grid_def.slots}
    )

    return instance
```

### Operation 2: Fill Slot (LLM-First Saturation)

```python
async def fill_slot(
    instance: GridInstance,
    slot_name: str,
    content: SlotContent,
    llm: LLM
) -> GridInstance:
    """
    LLM-FIRST: Fill a slot in a grid instance.

    Saturation is NOT a threshold (confidence >= 0.8, evidence >= 2).
    LLM assesses whether this slot is "done" based on content quality.
    """

    instance.filled_slots[slot_name] = content
    instance.last_modified = now()

    # Calculate completeness (mechanical - OK for Python)
    filled = sum(1 for s in instance.filled_slots.values() if s.value)
    instance.completeness = filled / len(instance.filled_slots)

    # LLM-FIRST: Assess saturation (judgment call - needs LLM)
    saturation = await llm.assess_slot_saturation(
        slot_name=slot_name,
        slot_content=content.value,
        slot_evidence=content.evidence,
        grid_type=instance.grid_type,
        unit_context=await get_unit(instance.unit_id)
    )
    instance.saturation_flags[slot_name] = saturation.is_saturated
    if saturation.needs_more:
        content.needs_research = True
        content.research_hint = saturation.what_is_missing

    # Detect gaps
    if content.needs_research:
        emit_event(GapDetected(
            unit_id=instance.unit_id,
            slot=slot_name,
            reason=saturation.what_is_missing if hasattr(saturation, 'what_is_missing') else None
        ))

    return instance
```

### Operation 3: Cross-Reference

```python
def add_cross_reference(
    source_instance: GridInstance,
    source_slot: str,
    target_unit_id: str,
    relationship: str,
    note: str
) -> GridInstance:
    """
    Create a cross-reference from one unit's slot to another unit.

    This is how we build the knowledge graph.
    """

    ref = CrossReference(
        target_unit_id=target_unit_id,
        relationship=relationship,
        note=note
    )

    source_instance.filled_slots[source_slot].cross_references.append(ref)

    return source_instance
```

### Operation 4: Propose Wildcard Grid

```python
def propose_wildcard_grid(
    material: str,  # The content we're trying to analyze
    existing_grids: list[str],  # Already applied to this unit
    llm: LLM
) -> WildcardGrid:
    """
    Ask LLM to invent a new analytical lens.
    """

    prompt = f"""
    The following material doesn't fit neatly into these existing grids: {existing_grids}

    Material:
    {material}

    Propose a new analytical grid. Specify:
    1. A name for this grid (single word or short phrase)
    2. 3-6 slot names that would structure analysis through this lens
    3. What this lens reveals that existing lenses miss
    4. What this lens might miss or distort

    Format as JSON:
    {{
        "name": "...",
        "slots": ["...", "...", ...],
        "what_it_sees": "...",
        "what_it_misses": "..."
    }}
    """

    response = llm.generate(prompt)
    grid_spec = parse_json(response)

    return WildcardGrid(
        id=f"GRID_WC_{datetime.now().strftime('%Y%m%d')}_{uuid4()[:8]}",
        name=grid_spec["name"],
        invented_by=llm.model_id,
        slots=grid_spec["slots"],
        description=f"Invented to analyze: {material[:100]}...",
        what_it_sees=grid_spec["what_it_sees"],
        what_it_misses=grid_spec["what_it_misses"],
        status=WildcardStatus.PROPOSED,
        uses_count=0,
        usefulness_ratings=[]
    )
```

---

## 2.5 Grid Selection Logic (Background, Automatic)

Grid selection happens **in background** — the LLM applies grids automatically based on unit type and content. The user only sees grids when friction is detected.

```python
class GridSelector:
    """
    Background grid selection based on Three-Tier Unit System.

    The user doesn't interact with this directly — it runs as part of
    the background framework enrichment process.
    """

    # Universal unit families → default grids
    UNIVERSAL_GRIDS = {
        "concept": ["LOGICAL", "FUNCTIONAL", "DEFINITIONAL", "COMPARATIVE"],
        "tension": ["POLE", "NAVIGATION", "POLITICAL", "TEMPORAL"],
        "agent": ["INTEREST", "CAPABILITY", "BEHAVIORAL", "RESPONSE"]
    }

    async def auto_apply_grids(
        self,
        unit: Unit,
        context: AnalysisContext
    ) -> list[GridInstance]:
        """
        Automatically apply appropriate grids to a unit.
        Called in BACKGROUND when units are created/updated.

        Returns filled grid instances — user doesn't see this unless friction.
        """

        instances = []

        # 1. Determine the universal family this unit belongs to
        universal_type = self._get_universal_type(unit)

        # 2. Apply Required Tier 1 grids
        for grid in TIER_1_GRIDS:
            instance = await self._apply_and_fill_grid(unit, grid, context)
            instances.append(instance)

        # 3. Apply Flexible Tier 2 grids based on universal family
        family_grids = self.UNIVERSAL_GRIDS.get(universal_type, [])
        for grid in family_grids:
            instance = await self._apply_and_fill_grid(unit, grid, context)
            instances.append(instance)

        # 4. Check for domain-specific grids
        domain_grids = await self._get_domain_grids(unit.domain, unit.unit_type)
        for grid in domain_grids:
            instance = await self._apply_and_fill_grid(unit, grid, context)
            instances.append(instance)

        # 5. Consider wildcard grids from similar units
        relevant_wildcards = await self._find_relevant_wildcards(unit, context)
        for wc in relevant_wildcards[:2]:  # Max 2 wildcards
            instance = await self._apply_and_fill_grid(unit, wc.name, context)
            instances.append(instance)

        # 6. Detect friction across all grids
        friction = await self._detect_grid_friction(instances)
        if friction:
            await self._surface_friction_to_user(friction, instances)

        return instances

    def _get_universal_type(self, unit: Unit) -> str:
        """
        Map any unit to its Universal family.

        - Thesis, Play, Position, Frame, Investment Thesis → "concept"
        - Dialectic, Trade-off, Signal Tension → "tension"
        - Actor, Player, Market Force, Stakeholder → "agent"
        - Domain-specific units → check their 'extends_universal' field
        """

        # Universal units map directly
        if unit.unit_type in ["concept", "tension", "agent"]:
            return unit.unit_type

        # Domain units have extends_universal field
        if hasattr(unit, 'extends_universal'):
            return unit.extends_universal

        # Fallback: LLM inference
        return self._infer_universal_type(unit)

    async def _apply_and_fill_grid(
        self,
        unit: Unit,
        grid_type: str,
        context: AnalysisContext
    ) -> GridInstance:
        """
        Apply a grid AND fill it from available materials.

        This is the key difference from old approach:
        - Old: Create empty grid, wait for user to fill
        - New: Create grid AND fill it from LLM analysis + literature
        """

        instance = apply_grid(unit, grid_type)

        # LLM fills slots from:
        # 1. Unit content
        # 2. Project materials
        # 3. Fetched literature
        # 4. Cross-references to other units

        filled = await self.llm.fill_grid_slots(
            grid_instance=instance,
            unit=unit,
            project_materials=context.materials,
            literature=context.relevant_literature
        )

        return filled

    async def _detect_grid_friction(
        self,
        instances: list[GridInstance],
        llm: LLM
    ) -> list[GridFriction]:
        """
        LLM-FIRST: Look for conflicts across grids that require user attention.

        No hardcoded confidence thresholds (< 0.6).
        LLM holistically assesses whether any friction warrants user attention.
        """

        # PYTHON: Gather evidence about all grid instances
        evidence = GridFrictionEvidence(
            instances=[{
                "grid_type": inst.grid_type,
                "filled_slots": {
                    slot: {
                        "value_summary": content.value[:200] if content.value else None,
                        "source": content.source,
                        "confidence_signal": content.confidence  # Signal, not threshold
                    }
                    for slot, content in inst.filled_slots.items()
                }
            } for inst in instances]
        )

        # LLM: Holistic friction detection
        prompt = f"""
        Analyze these grid instances for friction that warrants user attention.

        Grid Evidence:
        {evidence.to_json()}

        Look for:
        1. Cross-grid contradictions (e.g., one grid says X, another implies not-X)
        2. Slots where the content seems uncertain, vague, or potentially wrong
        3. Missing connections between grids that should reference each other
        4. Slots filled with content that doesn't quite fit the slot's purpose

        For each friction point, explain:
        - What the friction is
        - Why it matters to the user
        - Whether it truly requires user attention or can be resolved automatically

        Return structured friction analysis.
        """

        response = await llm.generate(prompt)
        return parse_grid_friction(response)
```

### What Users See vs What Happens

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     GRID PROCESSING: VISIBLE vs HIDDEN                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  HIDDEN (Background)                                                         │
│  ────────────────────────                                                    │
│  • Grids automatically applied to new units                                  │
│  • Slots filled from LLM analysis                                            │
│  • Literature fetched and integrated                                         │
│  • Cross-references discovered                                               │
│  • Completeness tracked                                                      │
│  • All of this: NO USER ATTENTION                                            │
│                                                                              │
│  VISIBLE (Surfaced on Friction)                                              │
│  ────────────────────────────────                                            │
│  • "New evidence challenges your framework"                                  │
│  • "These two analyses contradict each other"                                │
│  • "This slot has low confidence — can you clarify?"                         │
│  • "Literature suggests alternative framework"                               │
│  • Resolution paths with commitment/foreclosure                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2.6 Multi-Grid Views

A unit can have multiple grids applied. The system needs to synthesize them:

```python
class MultiGridView:
    """
    A view of a unit through all its applied grids.
    """

    unit_id: str
    unit_type: str

    # All grid instances for this unit
    grid_instances: list[GridInstance]

    # Synthesized view
    def get_complete_picture(self) -> UnitAnalysis:
        """
        Combine all grids into a unified view.
        """
        return UnitAnalysis(
            unit_id=self.unit_id,
            grids_applied=[gi.grid_type for gi in self.grid_instances],
            overall_completeness=self._average_completeness(),
            gaps_identified=self._collect_gaps(),
            cross_references=self._collect_cross_refs(),
            insights_by_grid={
                gi.grid_type: self._summarize_grid(gi)
                for gi in self.grid_instances
            }
        )

    def find_contradictions(self) -> list[Contradiction]:
        """
        Look for inconsistencies across grids.

        Example: LOGICAL grid says "well-supported"
                 but GENEALOGICAL grid shows "breaks from established tradition"
        """
        contradictions = []

        for i, grid_a in enumerate(self.grid_instances):
            for grid_b in self.grid_instances[i+1:]:
                # Check for conflicting claims
                conflicts = self._detect_conflicts(grid_a, grid_b)
                contradictions.extend(conflicts)

        return contradictions

    def suggest_additional_grids(self) -> list[str]:
        """
        Based on what's filled, suggest additional grids.

        Example: If ACTOR grid shows powerful coalition potential,
                 suggest COALITION grid for deeper analysis.
        """
        suggestions = []
        applied = {gi.grid_type for gi in self.grid_instances}

        # Pattern matching on filled content
        for gi in self.grid_instances:
            if gi.grid_type == "ACTOR" and "coalition" in str(gi.filled_slots).lower():
                if "COALITION" not in applied:
                    suggestions.append("COALITION")

            if gi.grid_type == "VALUE" and "trade" in str(gi.filled_slots).lower():
                if "DIALECTIC" not in applied:
                    suggestions.append("Might benefit from POLE/NAVIGATION analysis")

        return suggestions
```

---

## 2.7 Grid-Unit Integration Example: The User's Actual Experience

Let's trace what the user ACTUALLY SEES vs what happens in background:

**Scenario:** User is working on an investment hypothesis project (Investor domain). They've pasted some notes about a company.

### What the User Does

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Project: [Chinese Tech Platform Analysis]                                   │
│  Domain: Investor                                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  [User pastes notes about Alibaba's "Dual Circulation" strategy]            │
│                                                                              │
│  "Alibaba is repositioning toward domestic consumption. Management says     │
│   they're less focused on international expansion. The Singles Day GMV      │
│   growth is slowing but domestic consumption patterns are shifting..."      │
│                                                                              │
│                                                        [Save and Continue]  │
└─────────────────────────────────────────────────────────────────────────────┘
```

The user clicks "Save and Continue" — and that's all they do. They might go get coffee.

### What Happens in Background (User Doesn't See)

```python
# 1. LLM ANALYZES NOTES → PROPOSES UNITS
async def process_user_notes(notes: str, project: Project):
    # LLM extracts potential units
    proposed_units = await llm.extract_units_from_notes(
        notes=notes,
        domain=project.domain,  # Investor
        existing_units=project.units
    )

    # Returns:
    # - Investment Thesis: "Alibaba domestic pivot thesis"
    # - Signal: "Singles Day GMV deceleration"
    # - Signal: "Management rhetoric shift"
    # - Catalyst: "Regulatory pressure easing"
    # - Agent: "Chinese middle-class consumer"
    # - Tension: "Growth vs. profitability"

# 2. FOR EACH UNIT → AUTO-APPLY AND FILL GRIDS
for unit in proposed_units:
    grids = await grid_selector.auto_apply_grids(unit, context)

    # Example for the "Alibaba domestic pivot" thesis:
    # - LOGICAL grid: Claim, Evidence, Warrant filled from notes
    # - FUNCTIONAL grid: What_Enables, What_Forecloses filled
    # - COMPARATIVE grid: Similar_Concepts found ("JD domestic focus", "Meituan local services")
    # - TEMPORAL grid: Past, Present, Future trajectory mapped

# 3. LITERATURE FETCH → AUTO-INTEGRATE
relevant_papers = await fetch_literature(
    queries=["China dual circulation strategy", "Alibaba domestic market", "Chinese consumer spending trends"],
    max_results=10
)

for paper in relevant_papers:
    # LLM-FIRST: LLM decides whether to auto-integrate or queue for user
    # No hardcoded threshold (>= 0.85). LLM reasons about fit holistically.
    fit_decision = await llm.analyze_fit(
        paper,
        project.framework,
        instruction="""
        Analyze whether this paper should be auto-integrated or reviewed by user.
        Consider: Does it clearly support, clearly challenge, or ambiguously relate?
        Auto-integrate only when the fit is unambiguous and non-controversial.
        """
    )

    if fit_decision.auto_integrate:
        await auto_integrate_evidence(paper, project)
    else:
        await queue_pending_decision(paper, fit_decision, project)

# 4. DETECT FRICTION ACROSS ALL GRIDS
friction = await detect_project_friction(project)

# Found friction:
# - COMPARATIVE grid shows similar concept "Import Substitution" but that
#   has negative historical connotations → needs user decision
# - Literature paper challenges the thesis by showing consumer debt levels
#   are rising faster than incomes → framework tension detected
```

### What the User Sees (Only the Friction)

When the user comes back from getting coffee:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Project: Chinese Tech Platform Analysis          ⚠️ 2 items need attention │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ✓ 6 units identified from your notes                                       │
│  ✓ 24 grids applied and filled                                              │
│  ✓ 3 relevant papers integrated automatically                               │
│  ⚠️ 2 items need your input                                                 │
│                                                                              │
│                                          [View Emerging Framework] [Review]  │
└─────────────────────────────────────────────────────────────────────────────┘
```

If they click "Review":

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ⚠️  Decision 1 of 2                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  The COMPARATIVE grid found that "Alibaba domestic pivot" is similar to:    │
│                                                                              │
│  • Import Substitution Industrialization (1960s development model)          │
│                                                                              │
│  However, this comparison has problematic connotations (ISI is now seen     │
│  as a failed strategy in development economics).                            │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────── │
│                                                                              │
│  How should we handle this comparison?                                       │
│                                                                              │
│  [A] Keep the comparison — the similarity is instructive despite connotation│
│      COMMITS YOU TO: Addressing "but ISI failed" objection in your thesis   │
│      YOU'RE PASSING ON: Cleaner framing without historical baggage          │
│                                                                              │
│  [B] Remove comparison — find different analogies                  ★ AI pick │
│      COMMITS YOU TO: Finding fresh comparisons (may take research)          │
│      YOU'RE PASSING ON: The genuine insight that domestic focus has risks   │
│                                                                              │
│  [C] Reframe as "lessons learned" — what's different this time              │
│      COMMITS YOU TO: Articulating why Alibaba avoids ISI's failures         │
│      YOU'RE PASSING ON: Simple narrative; adds complexity                   │
│                                                                              │
│                                            [Choose Path] [Defer for Later]  │
└─────────────────────────────────────────────────────────────────────────────┘
```

And:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ⚠️  Decision 2 of 2                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  📄 New evidence challenges your framework:                                  │
│                                                                              │
│  Paper: "Chinese Household Debt and Consumption Patterns 2020-2024"         │
│  Source: NBER Working Paper                                                  │
│                                                                              │
│  Key finding: Consumer debt-to-income ratios rising faster than incomes.    │
│  This challenges your thesis that "domestic consumption can sustain growth" │
│                                                                              │
│  Your framework says: Alibaba's domestic pivot is sustainable               │
│  The evidence suggests: Consumption growth may be debt-financed, not real   │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────── │
│                                                                              │
│  [A] Revise thesis to include this risk factor                     ★ AI pick │
│      COMMITS YOU TO: More nuanced "conditional on debt sustainability"      │
│      → LLM will add new Risk Factor unit: "Consumer debt accumulation"      │
│                                                                              │
│  [B] Treat as short-term noise — thesis remains valid long-term             │
│      COMMITS YOU TO: Defending why debt is temporary phenomenon             │
│      → LLM will add this as Counter in LOGICAL grid with your defense       │
│                                                                              │
│  [C] This evidence is too important — need to fundamentally rethink         │
│      COMMITS YOU TO: Major framework revision                               │
│      → LLM will surface all units affected and propose restructuring        │
│                                                                              │
│                                            [Choose Path] [Defer for Later]  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### What the User Experienced

1. Pasted notes
2. Got coffee
3. Came back to find 6 units identified, 24 grids filled, 3 papers integrated
4. Made 2 decisions about genuine tensions
5. Done

**Total active work: ~5 minutes**

**What would have taken hours in traditional approach: 0 minutes** (background processing)

### The Key Difference

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        OLD vs NEW APPROACH                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  OLD: User fills slots                                                       │
│  ────────────────────────                                                    │
│  1. User creates unit                                                        │
│  2. User applies grid                                                        │
│  3. User fills each slot manually                                            │
│  4. User repeats for each grid                                               │
│  5. User notices gaps themselves                                             │
│  6. User searches for literature                                             │
│  7. User integrates findings                                                 │
│                                                                              │
│  → Hours of work, high friction, user does all cognitive labor               │
│                                                                              │
│  NEW: LLM fills, user resolves friction                                      │
│  ──────────────────────────────────────────                                  │
│  1. User provides materials                                                  │
│  2. [BACKGROUND] Units extracted, grids applied, slots filled                │
│  3. [BACKGROUND] Literature fetched and high-fit content integrated         │
│  4. [BACKGROUND] Friction detected                                           │
│  5. User resolves 2-3 genuine tensions with multiple resolution paths        │
│                                                                              │
│  → Minutes of active work, low friction, user provides judgment only         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

*End of Part 2. Part 3 covers Shackle's Epistemic Infrastructure and Research Commissioning.*

---

# PART 3: EPISTEMIC INFRASTRUCTURE (SHACKLE)

## 3.1 Why Shackle Matters

G.L.S. Shackle (1903-1992) was an economist who rejected probabilistic approaches to uncertainty. His insight: **radical uncertainty cannot be tamed by probability distributions.**

In strategic planning, this means:
- We can't assign probabilities to scenarios
- The future is shaped by decisions that haven't been made yet
- New possibilities emerge that were previously inconceivable
- **Crucial decisions** are different from routine ones — they change the decision-maker and the world

**Why this matters for the Strategizer:**

Traditional planning tools pretend uncertainty can be quantified. Shackle forces us to acknowledge:
1. Some things are genuinely unknown (not just "uncertain")
2. Our actions change the landscape of what's possible
3. Major decisions are path-dependent and largely irreversible
4. "Surprise" is the proper metric, not probability

---

## 3.2 Core Shacklean Concepts

### Concept 1: Potential Surprise

**Instead of:** "What's the probability of X?"
**Ask:** "How surprised would I be if X happened?"

```python
class SurpriseProfile:
    """
    Shackle's alternative to probability distributions.

    For any scenario/outcome, we assess:
    - How surprised would we be if it happened?
    - How surprised would we be if it DIDN'T happen?

    This avoids the false precision of probability.
    """

    # Surprise at occurrence
    potential_surprise: SurpriseLevel  # IMPOSSIBLE | SURPRISING | CONCEIVABLE | UNSURPRISING | EXPECTED

    # Surprise at non-occurrence
    surprise_at_absence: SurpriseLevel

    # What this combination means
    interpretation: str

    # Evidence supporting this assessment
    evidence: list[str]

class SurpriseLevel(Enum):
    IMPOSSIBLE = "Would violate known laws/constraints"
    SURPRISING = "Would require unusual circumstances"
    CONCEIVABLE = "Neither surprising nor expected"
    UNSURPRISING = "Fits with current trajectory"
    EXPECTED = "Would be surprising if it DIDN'T happen"
```

**Example Application:**

```python
# For a SCENARIO: "Moldova joins EU by 2030"
moldova_eu_scenario.surprise_profile = SurpriseProfile(
    potential_surprise=SurpriseLevel.CONCEIVABLE,
    surprise_at_absence=SurpriseLevel.UNSURPRISING,
    interpretation="Could happen but wouldn't be surprised if it doesn't. EU expansion dynamics uncertain.",
    evidence=[
        "Georgia precedent unclear",
        "Ukraine war could accelerate or block",
        "Transnistria unresolved"
    ]
)
```

### Concept 2: Focus Gain and Focus Loss

Shackle's insight: **Not all scenarios matter equally for decision-making.**

- **Focus Gain:** The best outcome that's conceivable — what pulls us toward this option
- **Focus Loss:** The worst outcome that's conceivable — what makes us hesitate

```python
class FocusOutcomes:
    """
    The scenarios that ACTUALLY matter for decision-making.

    We don't weigh all scenarios equally. We focus on:
    - The best case that's not ridiculous (focus gain)
    - The worst case that's not ridiculous (focus loss)

    These focus points determine whether we act.
    """

    focus_gain: FocusPoint
    focus_loss: FocusPoint

    # How these combine into decision-relevant assessment
    decision_relevance: str

class FocusPoint:
    scenario_id: str
    description: str
    potential_surprise: SurpriseLevel  # Must be CONCEIVABLE or better
    payoff_description: str  # What's at stake
    conditions_for_realization: list[str]
```

**Example:**

```python
# For an INSTRUMENT: "Aggressive SEZ policy for Moldova"
aggressive_sez.focus_outcomes = FocusOutcomes(
    focus_gain=FocusPoint(
        scenario_id="SEZ_SUCCESS",
        description="SEZs attract significant FDI, create manufacturing cluster",
        potential_surprise=SurpriseLevel.CONCEIVABLE,
        payoff_description="Moldova becomes regional manufacturing hub",
        conditions_for_realization=["EU access maintained", "Skilled labor available", "Infrastructure investment follows"]
    ),
    focus_loss=FocusPoint(
        scenario_id="SEZ_FAILURE",
        description="SEZs become white elephants, fiscal drain",
        potential_surprise=SurpriseLevel.CONCEIVABLE,
        payoff_description="Wasted resources, political fallout, delayed alternatives",
        conditions_for_realization=["Global FDI downturn", "Competitor countries more attractive", "Infrastructure bottlenecks"]
    ),
    decision_relevance="The gain is attractive but not overwhelmingly so. The loss is recoverable. Moderate risk profile."
)
```

### Concept 3: Cruciality

**Crucial decisions** are fundamentally different from routine choices:

- They change the decision-maker (you learn, you commit, you're now "the person who did X")
- They change the world (path dependencies, precedents, signals)
- They're largely irreversible
- They don't repeat — you can't "try again with different conditions"

```python
class CrucialityAssessment:
    """
    How crucial is this decision/scenario/instrument?

    Shackle's insight: Crucial decisions cannot be approached
    with expected-value thinking because:
    1. They don't repeat (no law of large numbers)
    2. They change the world (no stable distribution)
    3. They change the decider (learning effects)
    """

    # Reversibility
    reversibility: Reversibility  # FULLY | PARTIALLY | BARELY | IRREVERSIBLE

    # Repeatability
    is_repeatable: bool  # Can we try again?
    similar_decisions_history: list[str]  # Past analogues

    # Transformation effects
    changes_us: list[str]  # How this changes the decision-maker
    changes_world: list[str]  # How this changes the landscape

    # Precedent effects
    precedent_set: str  # What precedent does this establish?
    signals_sent: list[str]  # What does this communicate to actors?

    # Overall cruciality
    cruciality_level: CrucialityLevel  # ROUTINE | SIGNIFICANT | CRUCIAL | EPOCHAL
    cruciality_rationale: str

class CrucialityLevel(Enum):
    ROUTINE = "Repeatable, reversible, limited stakes"
    SIGNIFICANT = "Some path dependency, notable but manageable"
    CRUCIAL = "Major commitment, limited reversibility, shapes future options"
    EPOCHAL = "Defines era, irreversible, transforms actor identity"
```

**Example:**

```python
# For a SCENARIO: "Ghana pivots to full technological sovereignty"
tech_sovereignty_scenario.cruciality = CrucialityAssessment(
    reversibility=Reversibility.BARELY,
    is_repeatable=False,
    similar_decisions_history=["South Korea 1960s", "India software 1990s", "China semiconductors 2020s"],

    changes_us=[
        "Ghana becomes 'the country that bet on sovereignty'",
        "Political capital committed to this path",
        "New institutional capabilities required"
    ],
    changes_world=[
        "Signals Africa can pursue alternative to dependency",
        "Changes FDI expectations for region",
        "Creates precedent for other small states"
    ],

    precedent_set="Small developing country can pursue industrial policy despite WTO constraints",
    signals_sent=["Not aligned with pure market liberalization", "Open to China/alternative partnerships"],

    cruciality_level=CrucialityLevel.CRUCIAL,
    cruciality_rationale="Commits significant resources, shapes regional expectations, limited do-over options"
)
```

### Concept 4: Kaleidic Triggers

Shackle's most radical insight: **The future isn't "out there" waiting to be discovered — it's made by decisions.**

A **kaleidic shift** is when someone's decision reframes the entire landscape:
- New possibilities suddenly conceivable
- Old certainties now questionable
- The "rules of the game" change

```python
class KaleidicTrigger:
    """
    Events or decisions that would fundamentally reframe the landscape.

    Named after Shackle's "kaleidic" metaphor: like a kaleidoscope,
    one turn and the whole pattern changes.
    """

    # Identity
    id: str
    name: str

    # What triggers it
    triggering_conditions: list[str]
    likelihood_description: str  # Not a probability — qualitative

    # Effects
    what_becomes_possible: list[str]  # New options opened
    what_becomes_impossible: list[str]  # Options closed
    what_gets_reframed: list[str]  # Changed meaning

    # Actor effects
    actors_empowered: list[str]
    actors_disempowered: list[str]

    # Temporal
    warning_signs: list[str]  # How we'd see it coming
    response_window: str  # How long to adjust after trigger

class KaleidicRegistry:
    """
    Maintain a registry of kaleidic triggers per domain/project.
    """

    triggers: list[KaleidicTrigger]

    def check_for_triggers(self, current_events: list[Event]) -> list[TriggeredAlert]:
        """
        Compare current events against registered triggers.
        """
        alerts = []
        for event in current_events:
            for trigger in self.triggers:
                if self._matches_condition(event, trigger.triggering_conditions):
                    alerts.append(TriggeredAlert(trigger=trigger, event=event))
        return alerts
```

**Example Triggers:**

```python
# Theory domain
theory_triggers = [
    KaleidicTrigger(
        id="KUHN_SHIFT",
        name="Paradigm Shift in Field",
        triggering_conditions=["Major journal publishes paradigm-breaking article", "Leading scholars switch allegiance"],
        what_becomes_possible=["Previously marginal positions now central", "New funding streams"],
        what_becomes_impossible=["Previous orthodoxy hard to publish"],
        what_gets_reframed=["History of field rewritten", "Who counts as important"]
    )
]

# Government domain
govt_triggers = [
    KaleidicTrigger(
        id="REGIME_CHANGE_NEIGHBOR",
        name="Political transition in key neighbor",
        triggering_conditions=["Election/coup in neighboring country", "New government with different orientation"],
        what_becomes_possible=["New trade agreements", "Different alliance structures"],
        what_becomes_impossible=["Continuation of current arrangements"],
        actors_empowered=["Opposition aligned with new neighbor regime"],
        warning_signs=["Polling data", "Opposition rhetoric shifts", "Diplomatic signals"]
    )
]
```

---

## 3.3 Shackle in the Architecture

Shackle's epistemic infrastructure is **ORTHOGONAL** to the unit system and grid system. It applies everywhere:

```
                    ┌─────────────────────────────────────────┐
                    │       SHACKLE LAYER (ORTHOGONAL)        │
                    │                                          │
                    │  Applies to:                             │
                    │  • Every SCENARIO unit                   │
                    │  • Every ACTOR model (uncertainty about  │
                    │    their responses)                      │
                    │  • Every INSTRUMENT (uncertainty about   │
                    │    effects)                              │
                    │  • Every CONCEPT (epistemic status)      │
                    │  • Every DIALECTIC (where resolution     │
                    │    stands)                               │
                    │                                          │
                    │  Provides:                               │
                    │  • Surprise profiles                     │
                    │  • Focus outcomes                        │
                    │  • Cruciality assessments               │
                    │  • Kaleidic triggers                    │
                    │                                          │
                    └─────────────────────────────────────────┘
                                        │
          ┌─────────────────────────────┼─────────────────────────────┐
          ▼                             ▼                             ▼
    ┌───────────┐               ┌───────────────┐              ┌───────────────┐
    │  CONCEPTS │               │   SCENARIOS   │              │  INSTRUMENTS  │
    │           │               │               │              │               │
    │ epistemic │               │ surprise_     │              │ cruciality    │
    │ _status   │               │ profile       │              │ _assessment   │
    │           │               │ focus_        │              │               │
    │           │               │ outcomes      │              │ focus_        │
    │           │               │ kaleidic_     │              │ outcomes      │
    │           │               │ triggers      │              │               │
    └───────────┘               └───────────────┘              └───────────────┘
```

**Integration with EpistemicStatus:**

Every unit carries an EpistemicStatus that reflects Shacklean thinking:

```python
class EpistemicStatus:
    """
    What do we know about this unit? How confident are we?
    """

    # Evidence quality
    evidence_type: EvidenceType  # EMPIRICAL | THEORETICAL | ANALOGICAL | INTUITIVE | SPECULATIVE
    evidence_sources: list[str]
    evidence_quality: float  # 0-1

    # Confidence (NOT probability)
    confidence: float  # 0-1, subjective assessment
    confidence_rationale: str

    # Gaps
    known_unknowns: list[str]  # What we know we don't know
    suspected_unknowns: list[str]  # What we suspect we're missing
    blind_spots: list[str]  # What we might be systematically missing

    # Assumptions
    critical_assumptions: list[Assumption]

    # Review status
    last_review: datetime
    needs_review: bool
    review_trigger: str | None

class Assumption:
    statement: str
    confidence: float
    what_if_wrong: str  # Impact if assumption fails
    test_conditions: list[str]  # How we'd know it's wrong
```

---

## 3.4 Research Commissioning

When the system detects gaps in epistemic status or needs_research flags, it can commission research:

### Gap Detection

```python
class GapDetector:
    """
    LLM-FIRST: Identify epistemic gaps that need research.

    No hardcoded thresholds (confidence < 0.6) or rule-based priority.
    LLM holistically assesses what gaps exist and how urgent they are.
    """

    async def scan_for_gaps(self, unit: Unit, llm: LLM) -> list[ResearchGap]:
        # PYTHON: Gather all evidence about the unit's epistemic state
        evidence = GapDetectionEvidence(
            unit_id=unit.id,
            unit_type=unit.type,
            unit_content_summary=unit.content[:500] if unit.content else None,
            epistemic_status={
                "known_unknowns": unit.epistemic_status.known_unknowns,
                "suspected_unknowns": unit.epistemic_status.suspected_unknowns,
                "blind_spots": unit.epistemic_status.blind_spots,
                "evidence_type": unit.epistemic_status.evidence_type,
                "evidence_quality": unit.epistemic_status.evidence_quality,
                "confidence": unit.epistemic_status.confidence,
                "confidence_rationale": unit.epistemic_status.confidence_rationale
            },
            grid_slots=[{
                "grid_type": gi.grid_type,
                "slot_name": slot_name,
                "has_content": bool(slot_content.value),
                "needs_research_flag": slot_content.needs_research,
                "confidence_signal": slot_content.confidence
            } for gi in unit.grid_instances
              for slot_name, slot_content in gi.filled_slots.items()],
            assumptions=[{
                "statement": a.statement,
                "confidence_signal": a.confidence,
                "what_if_wrong": a.what_if_wrong,
                "test_conditions": a.test_conditions,
                "has_test_data": self._has_test_data(a)
            } for a in unit.epistemic_status.critical_assumptions]
        )

        # LLM: Holistic gap detection and prioritization
        prompt = f"""
        Analyze this unit's epistemic state to identify research gaps.

        Unit Evidence:
        {evidence.to_json()}

        For each gap you identify:
        1. What is the gap? (known unknown, slot needing research, untested assumption)
        2. How critical is this gap to the unit's usefulness?
        3. What would happen if we proceed without filling this gap?
        4. How urgent is addressing it? (Consider: stakes, dependencies, cost of delay)

        Prioritize holistically - not by thresholds but by reasoning about:
        - What makes this unit actionable or not
        - What risks are we taking with incomplete knowledge
        - What the user would want to know

        Return structured gap analysis with priorities.
        """

        response = await llm.generate(prompt)
        return parse_research_gaps(response)
```

### Research Commission Generation

```python
class ResearchCommission:
    """
    A commissioned research task to fill an epistemic gap.
    """

    # Identity
    id: str
    created_at: datetime

    # What we need
    gap: ResearchGap
    research_question: str
    scope: str  # What to cover
    constraints: list[str]  # What NOT to cover

    # How to do it
    suggested_sources: list[str]
    methodology: str

    # Output specification
    output_format: OutputFormat
    integration_target: str  # Which unit/slot this fills

    # Status
    status: CommissionStatus  # PENDING | IN_PROGRESS | COMPLETED | FAILED
    assigned_to: str | None  # "web_search" | "llm_deep_dive" | "human"

class ResearchExecutor:
    """
    LLM-FIRST: Execute research commissions.

    LLM assesses confidence in findings holistically, not via rule-based scoring.
    """

    async def execute(self, commission: ResearchCommission, llm: LLM) -> ResearchResult:
        """
        Execute a research commission.

        Steps:
        1. Formulate search/research strategy
        2. Execute (web search, LLM analysis, or both)
        3. Synthesize findings
        4. LLM assesses confidence in findings
        5. Return result for human review
        """

        if commission.assigned_to == "web_search":
            raw_findings = await self.web_search(commission.research_question)
        elif commission.assigned_to == "llm_deep_dive":
            raw_findings = await self.llm_analyze(commission.research_question, commission.scope)
        else:
            # Hybrid
            search_results = await self.web_search(commission.research_question)
            raw_findings = await self.llm_synthesize(search_results, commission.scope)

        # Format for target
        formatted = self.format_for_integration(raw_findings, commission.integration_target)

        # LLM-FIRST: Assess confidence holistically
        confidence_assessment = await llm.generate(f"""
        Assess confidence in these research findings:

        Research Question: {commission.research_question}
        Findings: {formatted[:2000]}
        Sources: {raw_findings.sources}

        Consider:
        1. Source quality and credibility
        2. Consistency across sources
        3. How directly the findings answer the question
        4. What's still uncertain or contested
        5. Recency and relevance of sources

        Return a confidence assessment with rationale.
        """)

        return ResearchResult(
            commission_id=commission.id,
            findings=formatted,
            sources=raw_findings.sources,
            confidence_assessment=parse_confidence_assessment(confidence_assessment),
            needs_human_review=True  # Always require human review
        )
```

### Research Integration

```python
class ResearchIntegrator:
    """
    Integrate research results into units.
    """

    def integrate(self, result: ResearchResult, commission: ResearchCommission) -> IntegrationResult:
        """
        Integrate research findings into the target unit/slot.

        Human review required before committing.
        """

        unit = get_unit(commission.gap.unit_id)

        if commission.gap.gap_type == GapType.SLOT_GAP:
            # Update specific grid slot
            grid_type, slot_name = commission.gap.grid_context
            grid_instance = get_grid_instance(unit.id, grid_type)

            # Propose update
            proposed_update = SlotContent(
                value=result.findings,
                evidence=result.sources,
                needs_research=False,  # Gap now filled
                confidence=result.confidence
            )

            return IntegrationResult(
                type="SLOT_UPDATE",
                target=(grid_type, slot_name),
                proposed_value=proposed_update,
                requires_approval=True
            )

        elif commission.gap.gap_type == GapType.KNOWN_UNKNOWN:
            # Update epistemic status
            new_knowledge = result.findings
            return IntegrationResult(
                type="EPISTEMIC_UPDATE",
                target=("epistemic_status", "known_unknowns"),
                proposed_value=f"RESOLVED: {commission.gap.description} → {new_knowledge}",
                requires_approval=True
            )
```

---

## 3.5 Shackle in Practice: Complete Example

Let's trace Shackle infrastructure for a Government domain scenario:

**Scenario:** "Moldova Services Hub Strategy"

```python
# 1. Create the scenario unit
moldova_services = ScenarioUnit(
    id="GOVT_SCENARIO_MOLDOVA_SERVICES",
    name="Moldova Services Hub Strategy",
    domain=Domain.GOVERNMENT,
    description="Transform Moldova into regional IT/services hub, leveraging EU access and language skills",
    internal_logic="Low labor costs + EU proximity + Russian/Romanian bilingualism = services arbitrage",
    value_commitments=["Human capital investment", "EU integration", "Services over manufacturing"]
)

# 2. Attach Surprise Profile
moldova_services.surprise_profile = SurpriseProfile(
    potential_surprise=SurpriseLevel.UNSURPRISING,  # Fits current trajectory
    surprise_at_absence=SurpriseLevel.CONCEIVABLE,  # Wouldn't be shocked if fails
    interpretation="This is a plausible continuation of current direction, but success is not assured",
    evidence=[
        "IT sector already growing 15% annually",
        "Several successful outsourcing firms",
        "Brain drain continues despite growth"
    ]
)

# 3. Attach Focus Outcomes
moldova_services.focus_outcomes = FocusOutcomes(
    focus_gain=FocusPoint(
        scenario_id="SERVICES_BREAKOUT",
        description="Moldova becomes 'Eastern European Ireland' for services",
        potential_surprise=SurpriseLevel.SURPRISING,  # Ambitious but conceivable
        payoff_description="20,000+ high-wage IT jobs, GDP per capita doubles",
        conditions_for_realization=[
            "EU visa liberalization maintained",
            "Romanian speakers attracted back",
            "Major contracts with Western firms"
        ]
    ),
    focus_loss=FocusPoint(
        scenario_id="SERVICES_STAGNATION",
        description="Growth plateaus, Moldova remains low-wage margin player",
        potential_surprise=SurpriseLevel.UNSURPRISING,  # This is the default
        payoff_description="Continued brain drain, missed opportunity window",
        conditions_for_realization=[
            "Competitor countries offer better deals",
            "Remote work normalizes, location less important",
            "Skilled workers continue emigrating"
        ]
    ),
    decision_relevance="The gain requires unusual conditions; the loss is the default. Needs active intervention to move toward gain."
)

# 4. Attach Cruciality Assessment
moldova_services.cruciality = CrucialityAssessment(
    reversibility=Reversibility.PARTIALLY,
    is_repeatable=True,  # Can adjust strategy
    similar_decisions_history=["Estonia e-governance", "Ireland IDA", "Philippines BPO"],

    changes_us=[
        "Commits human capital investment budget",
        "Signals priority to international investors",
        "Education system reoriented"
    ],
    changes_world=[
        "Sets expectation for similar small states",
        "Competitor response likely (Ukraine, Romania)"
    ],

    precedent_set="Small post-Soviet state can compete on quality, not just cost",
    signals_sent=["Open for business", "Betting on EU integration"],

    cruciality_level=CrucialityLevel.SIGNIFICANT,
    cruciality_rationale="Major commitment but course corrections possible. Not existential."
)

# 5. Register Kaleidic Triggers
moldova_services.kaleidic_triggers = [
    KaleidicTrigger(
        id="UKRAINE_RESOLUTION",
        name="Ukraine War Resolution",
        triggering_conditions=["Ceasefire", "Reconstruction begins"],
        what_becomes_possible=[
            "Ukraine becomes massive competitor for IT talent",
            "Regional reconstruction creates demand",
            "Western investment flood to region"
        ],
        what_becomes_impossible=[
            "Moldova as unique EU-adjacent option",
            "Security premium for Moldova stability"
        ],
        warning_signs=["Peace negotiations", "Western reconstruction pledges"],
        response_window="6-12 months to reposition"
    ),
    KaleidicTrigger(
        id="TRANSNISTRIA_RESOLUTION",
        name="Transnistria Status Change",
        triggering_conditions=["Moldova regains control", "Or: Russia annexes"],
        what_becomes_possible=[
            "If resolved: Full territorial integrity, expanded labor pool",
            "If lost: EU integration accelerates as compensation"
        ],
        what_becomes_impossible=[
            "Current ambiguous status quo"
        ],
        warning_signs=["Russian troop movements", "Diplomatic initiatives", "Local governance changes"],
        response_window="Weeks in crisis, months in resolution"
    )
]

# 6. Epistemic Status with Shacklean honesty
moldova_services.epistemic_status = EpistemicStatus(
    evidence_type=EvidenceType.ANALOGICAL,
    evidence_sources=["Estonia case study", "Ireland IDA analysis", "Moldova IT sector data"],
    evidence_quality=0.6,

    confidence=0.5,
    confidence_rationale="Model is plausible but conditions differ; Moldova is poorer, smaller, more peripheral",

    known_unknowns=[
        "Will EU maintain visa liberalization?",
        "Can brain drain be reversed?",
        "What's competitor response time?"
    ],
    suspected_unknowns=[
        "AI impact on outsourcing demand",
        "Generational attitudes to return migration"
    ],
    blind_spots=[
        "May be overestimating language advantage",
        "May be underestimating infrastructure needs"
    ],

    critical_assumptions=[
        Assumption(
            statement="EU market access will continue",
            confidence=0.7,
            what_if_wrong="Strategy fails entirely",
            test_conditions=["EU political shifts", "Trade policy changes"]
        ),
        Assumption(
            statement="IT demand will grow for at least 10 years",
            confidence=0.6,
            what_if_wrong="Window of opportunity closes",
            test_conditions=["AI automation trends", "Global outsourcing patterns"]
        )
    ]
)
```

---

*End of Part 3. Part 4 covers the Generative Process and Interlocutor Modeling.*

---

# PART 4: GENERATIVE PROCESS

## 4.1 The Knowledge Creation Pipeline

The Strategizer doesn't just organize existing knowledge — it generates new strategic understanding. This happens through a structured process:

```
FRICTION → DIAGNOSIS → COIN → TEST → ABSTRACT → PROMOTE
```

Each stage produces outputs that feed into the next:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        GENERATIVE PROCESS PIPELINE                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │ FRICTION │ →  │ DIAGNOSIS│ →  │   COIN   │ →  │   TEST   │ →  │ ABSTRACT │ │
│  │          │    │          │    │          │    │          │    │          │ │
│  │ Something│    │ Name the │    │ Create   │    │ Stress   │    │ Extract  │ │
│  │ doesn't  │    │ type of  │    │ new unit │    │ test the │    │ what     │ │
│  │ fit      │    │ gap      │    │ to fill  │    │ new unit │    │ transfers│ │
│  │          │    │          │    │ the gap  │    │          │    │          │ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│                                                                         │      │
│                                                                         ▼      │
│                                                               ┌──────────────┐ │
│                                                               │   PROMOTE    │ │
│                                                               │              │ │
│                                                               │ Add to stable│ │
│                                                               │ doctrine     │ │
│                                                               │              │ │
│                                                               └──────────────┘ │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4.2 Stage 1: FRICTION

### What It Is

Friction is when the current conceptual apparatus doesn't fit the material. Something resists categorization. The existing grids leave orphaned content. The scenarios don't feel right.

### Triggers

```python
class FrictionDetector:
    """
    LLM-FIRST: Detect when the system is encountering friction.

    No hardcoded severities (MEDIUM, HIGH). LLM holistically assesses
    what friction exists and how severe it is based on context.
    """

    async def detect_friction(self, context: AnalysisContext, llm: LLM) -> list[FrictionEvent]:
        # PYTHON: Gather all potential friction signals
        evidence = FrictionEvidence(
            orphan_content=self._find_orphan_content(context),
            forced_fits=self._find_forced_fits(context),
            contradictions=self._find_contradictions(context),
            repeated_workarounds=self._find_repeated_workarounds(context),
            interlocutor_surprises=self._find_interlocutor_surprises(context),
            context_summary={
                "project_type": context.project.domain,
                "active_grids": [g.grid_type for g in context.active_grids],
                "recent_units": [u.type for u in context.recent_units[-10:]]
            }
        )

        # LLM: Holistic friction detection and severity assessment
        prompt = f"""
        Analyze this context for conceptual friction that needs attention.

        Evidence Package:
        {evidence.to_json()}

        For each friction signal:
        1. Is this genuine friction or just normal variance?
        2. How severe is it? Consider:
           - Does it block progress?
           - Does it indicate a fundamental conceptual gap?
           - Is it a local annoyance or a systemic problem?
        3. What makes this friction worth surfacing to the user?

        Not every mismatch is friction. Only flag things where:
        - The conceptual apparatus genuinely doesn't fit the material
        - There's a pattern suggesting missing abstraction
        - The user would benefit from knowing about this

        Return structured friction analysis with holistic severity reasoning.
        """

        response = await llm.generate(prompt)
        return parse_friction_events(response)
```

### Output

Friction events feed into diagnosis:

```python
class FrictionEvent:
    id: str
    type: FrictionType
    description: str
    severity: Severity
    context: AnalysisContext
    timestamp: datetime

    # What triggered it
    trigger_content: str
    trigger_location: str  # Which unit/grid/slot

    # Status
    status: FrictionStatus  # DETECTED | DIAGNOSING | RESOLVED | DEFERRED
```

---

## 4.3 Stage 2: DIAGNOSIS

### What It Is

Diagnosis names the TYPE of gap. It's not enough to know something doesn't fit — we need to know what KIND of thing is missing.

### Diagnostic Categories

```python
class GapDiagnosis:
    """
    What type of knowledge is missing?
    """

    friction_id: str
    diagnosis_type: DiagnosisType
    recommended_action: str
    confidence: float

class DiagnosisType(Enum):
    # Conceptual gaps
    MISSING_CONCEPT = "We lack a concept to name this phenomenon"
    WRONG_CONCEPT = "We're using the wrong concept; need a different one"
    VAGUE_CONCEPT = "Concept exists but is too vague; needs refinement"

    # Dialectic gaps
    MISSING_DIALECTIC = "There's an unrecognized tension here"
    FALSE_DIALECTIC = "What looks like a trade-off can actually be dissolved"
    MISWEIGHTED_DIALECTIC = "The balance is wrong; need to reweight"

    # Scenario gaps
    MISSING_SCENARIO = "A coherent future path is unrecognized"
    IMPOSSIBLE_SCENARIO = "Current scenario is actually blocked"
    HYBRID_NEEDED = "Need to combine elements of multiple scenarios"

    # Actor gaps
    MISSING_ACTOR = "A relevant actor is unmodeled"
    WRONG_MODEL = "Actor model doesn't predict actual behavior"
    COALITION_SHIFT = "Actor alignments have changed"

    # Instrument gaps
    MISSING_INSTRUMENT = "No available tool addresses this problem"
    INEFFECTIVE_INSTRUMENT = "The tool doesn't work as expected"
    COMBINATION_NEEDED = "Need to combine instruments in new way"

    # Structural gaps
    MISSING_GRID = "No existing grid captures this analytical dimension"
    CROSS_REFERENCE_NEEDED = "Units need to be linked that aren't"
    LEVEL_MISMATCH = "Operating at wrong level of abstraction"
```

### Diagnostic Process

```python
class Diagnoser:
    """
    Diagnose friction events to determine what's needed.
    """

    def diagnose(self, friction: FrictionEvent, llm: LLM) -> GapDiagnosis:
        """
        Use LLM to diagnose the type of gap.
        """

        prompt = f"""
        The following friction has been detected:

        Type: {friction.type}
        Description: {friction.description}
        Context: {friction.context.summarize()}

        Diagnose what type of knowledge gap this represents.

        Choose from:
        - MISSING_CONCEPT: We need a new concept
        - WRONG_CONCEPT: We're using the wrong concept
        - MISSING_DIALECTIC: There's an unrecognized tension
        - FALSE_DIALECTIC: Apparent trade-off can be dissolved
        - MISSING_SCENARIO: A coherent future path is unrecognized
        - MISSING_ACTOR: A relevant actor is unmodeled
        - WRONG_MODEL: Actor model doesn't predict behavior
        - MISSING_INSTRUMENT: No tool addresses this
        - MISSING_GRID: Need new analytical dimension
        - OTHER: Explain

        Provide:
        1. Diagnosis type
        2. Explanation of why this diagnosis
        3. Recommended action
        4. Confidence (0-1)
        """

        response = llm.generate(prompt)
        return parse_diagnosis(response)
```

---

## 4.4 Stage 3: COIN

### What It Is

"Coin" means creating a new unit to fill the diagnosed gap. Like minting a new coin, we're adding to the currency of thought.

### Coining Process

```python
class UnitCoiner:
    """
    Create new units to fill diagnosed gaps.
    """

    def coin(self, diagnosis: GapDiagnosis, context: AnalysisContext, llm: LLM) -> Unit:
        """
        Generate a new unit based on the diagnosis.
        """

        if diagnosis.diagnosis_type in [DiagnosisType.MISSING_CONCEPT, DiagnosisType.WRONG_CONCEPT]:
            return self._coin_concept(diagnosis, context, llm)
        elif diagnosis.diagnosis_type in [DiagnosisType.MISSING_DIALECTIC, DiagnosisType.FALSE_DIALECTIC]:
            return self._coin_dialectic(diagnosis, context, llm)
        elif diagnosis.diagnosis_type == DiagnosisType.MISSING_SCENARIO:
            return self._coin_scenario(diagnosis, context, llm)
        elif diagnosis.diagnosis_type in [DiagnosisType.MISSING_ACTOR, DiagnosisType.WRONG_MODEL]:
            return self._coin_actor(diagnosis, context, llm)
        elif diagnosis.diagnosis_type == DiagnosisType.MISSING_GRID:
            return self._coin_wildcard_grid(diagnosis, context, llm)
        else:
            raise UnsupportedDiagnosisError(diagnosis.diagnosis_type)

    def _coin_concept(self, diagnosis: GapDiagnosis, context: AnalysisContext, llm: LLM) -> ConceptUnit:
        """
        Generate a new concept.
        """

        prompt = f"""
        We need a new concept. Here's the gap:

        {diagnosis.description}

        Context:
        {context.summarize()}

        Create a new concept that fills this gap. Provide:

        1. Name (evocative but precise)
        2. Definition (one paragraph)
        3. What it enables (what becomes visible/possible)
        4. What it forecloses (what becomes invisible/impossible)
        5. Conditions of application (when to use this concept)
        6. What it breaks from (prior concepts it rejects)
        7. What it builds on (prior concepts it extends)

        Format as YAML.
        """

        response = llm.generate(prompt)
        concept_spec = parse_yaml(response)

        return ConceptUnit(
            id=generate_id("CONCEPT"),
            name=concept_spec["name"],
            domain=context.domain,
            definition=concept_spec["definition"],
            what_it_enables=concept_spec["what_it_enables"],
            what_it_forecloses=concept_spec["what_it_forecloses"],
            conditions_of_application=concept_spec["conditions_of_application"],
            breaks_from=concept_spec.get("breaks_from", []),
            derived_from=concept_spec.get("builds_on", []),
            status=UnitStatus.DRAFT,
            created_from_friction=diagnosis.friction_id
        )
```

### Hegelian Sublation

When the diagnosis is FALSE_DIALECTIC, we coin a higher-order concept that dissolves the apparent tension:

```python
def _coin_sublation(self, diagnosis: GapDiagnosis, dialectic: DialecticUnit, llm: LLM) -> ConceptUnit:
    """
    Create a concept that sublates (dissolves) a false dialectic.
    """

    prompt = f"""
    The following dialectic appears to be a false dichotomy:

    {dialectic.name}
    Pole A: {dialectic.pole_a.description}
    Pole B: {dialectic.pole_b.description}

    Why it's false:
    {diagnosis.description}

    Create a higher-order concept that:
    1. Shows why the dichotomy was false
    2. Preserves what was valuable in both poles
    3. Reveals a new way of seeing that transcends the opposition

    This is Hegelian sublation (Aufhebung):
    - Negate the opposition
    - Preserve what was true in each pole
    - Elevate to a higher synthesis

    Provide the sublating concept with full specification.
    """

    response = llm.generate(prompt)
    concept_spec = parse_yaml(response)

    # Create the sublating concept
    sublating_concept = ConceptUnit(
        id=generate_id("CONCEPT"),
        name=concept_spec["name"],
        domain=dialectic.domain,
        definition=concept_spec["definition"],
        what_it_enables=concept_spec["what_it_enables"],
        what_it_forecloses=concept_spec["what_it_forecloses"],
        derived_from=[dialectic.pole_a.name, dialectic.pole_b.name],
        status=UnitStatus.DRAFT,
        sublation_of=dialectic.id
    )

    # Update the dialectic
    dialectic.status = DialecticStatus.SUBLATED
    dialectic.sublated_into = sublating_concept.id
    dialectic.sublation_insight = concept_spec.get("sublation_insight", "")

    return sublating_concept
```

---

## 4.5 Stage 4: TEST

### What It Is

New units must be stress-tested before promotion. We test against:
1. **Interlocutors** — What would critics say?
2. **Edge cases** — Does it hold at the margins?
3. **Internal consistency** — Does it contradict other units?
4. **Usefulness** — Does it actually help?

### Testing Process

```python
class UnitTester:
    """
    LLM-FIRST: Stress test newly coined units.

    No hardcoded thresholds (score >= 0.6, >= 0.4) or rule-based severity.
    LLM holistically evaluates whether the unit passes each test dimension.
    """

    async def test(self, unit: Unit, context: AnalysisContext, llm: LLM) -> TestResult:
        """
        Run all tests on a unit via LLM holistic evaluation.
        """

        # PYTHON: Gather all test evidence
        test_evidence = TestEvidence(
            unit={
                "id": unit.id,
                "type": unit.type,
                "content": unit.content[:1000] if unit.content else None,
                "epistemic_status": unit.epistemic_status.to_dict()
            },
            interlocutors=[{
                "id": i.id,
                "perspective": i.perspective,
                "known_objections": i.known_objections
            } for i in context.get_relevant_interlocutors(unit)],
            edge_cases=self._generate_edge_cases(unit),
            related_units=[{
                "id": u.id,
                "type": u.type,
                "summary": u.content[:200] if u.content else None
            } for u in context.all_units[:20]],  # Sample for context
            usage_context={
                "project_domain": context.project.domain,
                "how_used": self._get_usage_examples(unit)
            }
        )

        # LLM: Holistic test evaluation
        prompt = f"""
        Evaluate this unit across four test dimensions:

        Unit and Context:
        {test_evidence.to_json()}

        Test Dimensions:

        1. INTERLOCUTOR TEST: How would the listed critics respond?
           - Would they find obvious flaws?
           - Are there objections the unit can't handle?
           - Rate not by threshold, but by: "Would this embarrass us?"

        2. EDGE CASE TEST: Does the concept hold at its margins?
           - Consider the edge cases listed
           - Are there definitional problems at the boundaries?
           - Rate by: "Does this remain coherent under stress?"

        3. CONSISTENCY TEST: Does it contradict other units?
           - Look at the related units
           - Any logical conflicts?
           - Rate by: "Can these coexist in the same framework?"

        4. USEFULNESS TEST: Does it actually help thinking?
           - Given the usage context
           - Does this concept earn its place?
           - Rate by: "Would removing this make the analysis worse?"

        For each dimension:
        - Provide reasoning, not just pass/fail
        - Assess severity of any issues holistically
        - Consider: would this issue block promotion or just need noting?

        Return structured test results with overall recommendation.
        """

        response = await llm.generate(prompt)
        return parse_test_result(response)
```

---

## 4.6 Stage 5: ABSTRACT

### What It Is

Before promotion, we extract what's generalizable. A unit created for one project might have broader applicability.

### Abstraction Process

```python
class Abstractor:
    """
    Extract generalizable elements from project-specific units.
    """

    def abstract(self, unit: Unit, source_context: AnalysisContext) -> AbstractedUnit:
        """
        Generalize a unit for potential cross-project use.
        """

        # Identify project-specific elements
        specific_elements = self._identify_specific_elements(unit, source_context)

        # Identify generalizable elements
        general_elements = self._identify_general_elements(unit)

        # Generate abstracted version
        abstracted = self._create_abstracted_version(unit, general_elements)

        # Document what was project-specific
        abstracted.project_specific_notes = specific_elements
        abstracted.conditions_for_transfer = self._identify_transfer_conditions(unit)

        return abstracted

    def _identify_transfer_conditions(self, unit: Unit) -> list[str]:
        """
        Under what conditions would this unit apply to other projects?
        """

        if isinstance(unit, ConceptUnit):
            # What domain characteristics are required?
            return [
                f"Domain has: {condition}"
                for condition in unit.conditions_of_application
            ]
        elif isinstance(unit, ScenarioUnit):
            # What structural conditions are required?
            return unit.phases[0].success_indicators if unit.phases else []
        # ... etc for other unit types
```

---

## 4.7 Stage 6: PROMOTE

### What It Is

Validated, abstracted units join the stable doctrine. They become available for future projects.

### Promotion Criteria

```python
class PromotionEvaluator:
    """
    LLM-FIRST: Determine if a unit should be promoted to doctrine.

    No hardcoded thresholds (confidence < 0.5) or rule-based rejection.
    LLM holistically evaluates whether the unit deserves promotion.
    """

    async def evaluate(
        self,
        unit: Unit,
        test_results: TestResult,
        abstracted: AbstractedUnit,
        llm: LLM
    ) -> PromotionDecision:
        """
        LLM-FIRST: Should this unit be promoted to stable doctrine?
        """

        # PYTHON: Gather all evaluation evidence
        evidence = PromotionEvidence(
            unit={
                "id": unit.id,
                "type": unit.type,
                "content_summary": unit.content[:500] if unit.content else None
            },
            test_results=test_results.to_dict(),
            abstraction={
                "conditions_for_transfer": abstracted.conditions_for_transfer,
                "project_specific_notes": abstracted.project_specific_notes,
                "general_elements": abstracted.general_elements
            },
            epistemic_status=abstracted.epistemic_status.to_dict(),
            similar_in_doctrine=[{
                "id": s.id,
                "summary": s.content[:200] if s.content else None,
                "similarity_reason": self._explain_similarity(abstracted, s)
            } for s in self._find_similar_in_doctrine(abstracted)]
        )

        # LLM: Holistic promotion evaluation
        prompt = f"""
        Evaluate whether this unit should be promoted to stable doctrine.

        Evidence:
        {evidence.to_json()}

        Consider:

        1. TEST QUALITY: Did it pass testing? Are the test results convincing?
           - Not just "did it pass" but "should we trust those passes?"

        2. TRANSFERABILITY: Can this be used in other projects?
           - Are the transfer conditions clear and meaningful?
           - Or is this too project-specific?

        3. UNIQUENESS: Does this add something new to doctrine?
           - Look at similar existing doctrine
           - Does this differentiate enough to warrant separate entry?
           - Or should it be merged with existing?

        4. EPISTEMIC QUALITY: How confident are we in this?
           - Not a threshold check, but: "Would we stake decisions on this?"
           - Is the evidence base strong enough for doctrine status?

        For each dimension, reason about quality holistically.

        Return:
        - approved: boolean
        - reasoning: Why or why not
        - if approved: recommended_placement, recommended_tags
        - if not approved: what would need to change
        """

        response = await llm.generate(prompt)
        return parse_promotion_decision(response)

    def promote(self, unit: Unit, decision: PromotionDecision) -> None:
        """
        Add unit to doctrine.
        """

        unit.status = UnitStatus.PROMOTED
        unit.promoted_at = datetime.now()
        unit.doctrine_placement = decision.recommended_placement

        # Add to doctrine store
        doctrine_store.add(unit)

        # Create cross-references
        self._link_to_related_doctrine(unit)

        # Notify
        emit_event(UnitPromoted(unit_id=unit.id, placement=decision.recommended_placement))
```

---

## 4.8 Interlocutor Modeling

### What It Is

Interlocutors are the ACTOR units for the Theory domain — intellectual positions that respond to arguments. For other domains, we call them Strategic Players, Market Actors, or Development Actors.

The key insight: **We model their likely responses and use this to stress-test our work.**

### Interlocutor Schema

```python
class InterlocutorModel:
    """
    A model of an intellectual position or actor that will respond to our work.
    """

    # Identity
    id: str
    name: str  # "The Marxist Tradition", "LVMH", "The IMF"
    domain: Domain

    # Core commitments
    core_commitments: list[str]  # What they believe
    methodological_preferences: list[str]  # How they like to argue
    valued_outcomes: list[str]  # What they want

    # Response patterns
    characteristic_moves: list[ResponsePattern]  # How they typically respond
    predictable_objections: list[Objection]  # What they always object to
    trigger_topics: list[str]  # Topics that provoke strong response

    # Simulation
    simulation_type: SimulationType  # RULE_BASED | LLM | HYBRID
    llm_persona_prompt: str | None  # For LLM simulation
    calibration_data: list[CalibrationExample]  # Past responses for validation

class ResponsePattern:
    trigger: str  # What provokes this response
    pattern: str  # The typical response structure
    examples: list[str]  # Historical examples

class Objection:
    topic: str
    objection_type: ObjectionType  # METHODOLOGICAL | EMPIRICAL | NORMATIVE | RHETORICAL
    typical_form: str  # How the objection is usually phrased
    our_response: str | None  # How we've responded in past
```

### Response Simulation

```python
class InterlocutorSimulator:
    """
    Simulate interlocutor responses to our work.
    """

    def simulate_response(
        self,
        interlocutor: InterlocutorModel,
        content: str,  # Our argument/proposal/position
        context: str
    ) -> SimulatedResponse:
        """
        Generate a simulated response from this interlocutor.
        """

        if interlocutor.simulation_type == SimulationType.RULE_BASED:
            return self._rule_based_response(interlocutor, content)

        elif interlocutor.simulation_type == SimulationType.LLM:
            prompt = f"""
            You are simulating the response of: {interlocutor.name}

            Their core commitments:
            {interlocutor.core_commitments}

            Their methodological preferences:
            {interlocutor.methodological_preferences}

            Topics that trigger strong responses:
            {interlocutor.trigger_topics}

            Here is the content they are responding to:
            ---
            {content}
            ---

            Context: {context}

            Provide their likely response. Be authentic to their perspective.
            Include:
            1. Their immediate reaction
            2. Their main objections (if any)
            3. What they would find valuable (if anything)
            4. How they would position their own view in response

            Format as YAML:
            reaction: ...
            objections: [...]
            valuable_elements: [...]
            counter_position: ...
            """

            response = self.llm.generate(prompt)
            return parse_simulated_response(response)

        else:  # HYBRID
            rule_response = self._rule_based_response(interlocutor, content)
            llm_response = self._llm_response(interlocutor, content, context)
            return self._merge_responses(rule_response, llm_response)
```

### Using Interlocutor Responses

```python
class InterlocutorIntegrator:
    """
    LLM-FIRST: Use interlocutor responses to improve our work.

    No rule-based severity checks (if severity == HIGH).
    LLM holistically evaluates which objections warrant action.
    """

    async def process_responses(
        self,
        unit: Unit,
        responses: list[SimulatedResponse],
        llm: LLM
    ) -> InterlocutorAnalysis:
        """
        LLM-FIRST: Analyze what we learned from simulated responses.
        """

        # PYTHON: Gather all response evidence
        evidence = InterlocutorEvidence(
            unit={
                "id": unit.id,
                "type": unit.type,
                "content_summary": unit.content[:500] if unit.content else None
            },
            responses=[{
                "interlocutor_id": r.interlocutor_id,
                "interlocutor_perspective": r.perspective,
                "objections": [{
                    "description": o.description,
                    "target": o.target,
                    "severity_signal": o.severity  # Signal, not threshold
                } for o in r.objections],
                "insights": r.insights,
                "would_accept": r.would_accept,
                "conditions_for_acceptance": r.conditions_for_acceptance
            } for r in responses]
        )

        # LLM: Holistic analysis of interlocutor feedback
        prompt = f"""
        Analyze these simulated interlocutor responses to improve the unit.

        Evidence:
        {evidence.to_json()}

        Determine:

        1. COMMON OBJECTIONS: What do multiple interlocutors object to?
           - Which objections are serious enough to require revision?
           - Not by severity enum, but by: "Would this objection embarrass us?"

        2. UNIQUE INSIGHTS: What did we learn from specific interlocutors?
           - What perspectives did they bring that we missed?
           - What would strengthen our work?

        3. BLIND SPOTS: What are we systematically missing?
           - What are interlocutors seeing that we're not?
           - What assumptions are we making that they question?

        4. RECOMMENDATIONS: What should we do?
           - Which objections require revision vs acknowledgment vs dismissal?
           - What blind spots should we add to epistemic status?
           - Reason about each recommendation holistically.

        Return structured interlocutor analysis with prioritized recommendations.
        """

        response = await llm.generate(prompt)
        return parse_interlocutor_analysis(response)
```

### Interlocutor Examples by Domain

**Theory Domain:**
```python
marxist_tradition = InterlocutorModel(
    id="INTERLOCUTOR_MARXIST",
    name="The Marxist Tradition",
    domain=Domain.THEORY,
    core_commitments=[
        "Material conditions determine consciousness",
        "Class conflict is fundamental",
        "Capitalism creates its own contradictions"
    ],
    methodological_preferences=[
        "Historical materialism",
        "Dialectical analysis",
        "Critique of ideology"
    ],
    predictable_objections=[
        Objection(
            topic="Any theory ignoring class",
            objection_type=ObjectionType.METHODOLOGICAL,
            typical_form="This analysis lacks class perspective..."
        ),
        Objection(
            topic="Market solutions",
            objection_type=ObjectionType.NORMATIVE,
            typical_form="This naturalizes capitalist relations..."
        )
    ]
)
```

**Foundation Domain:**
```python
effective_altruism = InterlocutorModel(
    id="ACTOR_EA",
    name="Effective Altruism Community",
    domain=Domain.FOUNDATION,
    core_commitments=[
        "Maximize expected impact",
        "Evidence-based giving",
        "Cause prioritization matters"
    ],
    predictable_objections=[
        Objection(
            topic="Any intervention without RCT evidence",
            objection_type=ObjectionType.EMPIRICAL,
            typical_form="What's the evidence base for this intervention?"
        ),
        Objection(
            topic="Systemic change approaches",
            objection_type=ObjectionType.METHODOLOGICAL,
            typical_form="How do you measure counterfactual impact?"
        )
    ]
)
```

**Government Domain:**
```python
imf_perspective = InterlocutorModel(
    id="ACTOR_IMF",
    name="IMF Perspective",
    domain=Domain.GOVERNMENT,
    core_commitments=[
        "Macroeconomic stability",
        "Market-based mechanisms",
        "Fiscal discipline"
    ],
    predictable_objections=[
        Objection(
            topic="Industrial policy",
            objection_type=ObjectionType.METHODOLOGICAL,
            typical_form="How does this avoid picking winners?"
        ),
        Objection(
            topic="Deficit spending",
            objection_type=ObjectionType.NORMATIVE,
            typical_form="What's the debt sustainability outlook?"
        )
    ]
)
```

---

*End of Part 4. Part 5 covers Domain Instantiations and Implementation Roadmap.*

---

# PART 5: DOMAIN INSTANTIATIONS & IMPLEMENTATION

## 5.1 Domain Instantiation Patterns

Each domain (Theory, Foundation, Brand, Government) shares the same architecture but with different vocabulary, examples, and emphases.

### The Instantiation Template

```python
class DomainInstantiation:
    """
    How to adapt the system for a specific domain.
    """

    domain: Domain
    name: str  # "Theory/Essay", "Foundation Strategy", etc.

    # Vocabulary mapping
    unit_vocabulary: dict[UnitType, str]  # e.g., CONCEPT → "Play" for Foundation

    # Default grids per unit type
    default_grids: dict[UnitType, list[str]]

    # Starter doctrine
    seed_concepts: list[ConceptUnit]
    seed_dialectics: list[DialecticUnit]
    seed_interlocutors: list[ActorUnit]

    # Example scenarios
    example_scenarios: list[ScenarioUnit]

    # Domain-specific extensions
    custom_grids: list[GridDefinition]  # Domain-specific flexible grids
    custom_enums: dict[str, list[str]]  # Domain-specific enum values
```

---

## 5.2 Theory/Essay Domain

**Purpose:** Build academic essays, books, articles. Navigate intellectual debates. Position novel concepts.

### Vocabulary

| Generic | Theory Domain |
|---------|---------------|
| Concept | **Concept** |
| Dialectic | **Dialectic** |
| Scenario | **Framework Evolution** |
| Actor | **Interlocutor** |
| Instrument | **Analytical Operation** |

### Seed Doctrine

```python
THEORY_SEED_CONCEPTS = [
    ConceptUnit(
        id="THEORY_CONCEPT_PARADIGM",
        name="Paradigm",
        domain=Domain.THEORY,
        definition="A shared set of assumptions, methods, and exemplars that define normal science within a discipline",
        what_it_enables=["Recognition of revolutionary vs. normal science", "Understanding of incommensurability"],
        what_it_forecloses=["Cumulative view of scientific progress"],
        thinkers_lineage=[ThinkerReference(name="Thomas Kuhn", work="Structure of Scientific Revolutions")]
    ),
    ConceptUnit(
        id="THEORY_CONCEPT_GENEALOGY",
        name="Genealogy",
        domain=Domain.THEORY,
        definition="Historical analysis that traces contingent origins rather than essential development",
        what_it_enables=["Denaturalization of current arrangements", "Visibility of power in knowledge"],
        what_it_forecloses=["Progress narratives", "Teleological histories"],
        thinkers_lineage=[ThinkerReference(name="Michel Foucault", work="Discipline and Punish")]
    )
]

THEORY_SEED_DIALECTICS = [
    DialecticUnit(
        id="THEORY_DIALECTIC_RIGOR_ACCESS",
        name="Rigor ↔ Accessibility",
        domain=Domain.THEORY,
        pole_a=Pole(name="Rigor", description="Technical precision, careful qualifications, exact terminology"),
        pole_b=Pole(name="Accessibility", description="Broad readability, simpler prose, public engagement"),
        navigation_strategies=[
            "Layer the text (technical core + accessible framing)",
            "Define terms on first use",
            "Use concrete examples before abstract formulation"
        ]
    ),
    DialecticUnit(
        id="THEORY_DIALECTIC_SPECIFIC_GENERAL",
        name="Specificity ↔ Generalizability",
        domain=Domain.THEORY,
        pole_a=Pole(name="Specificity", description="Rich case detail, contextual particularity"),
        pole_b=Pole(name="Generalizability", description="Abstract principles, cross-case patterns"),
        navigation_strategies=[
            "Move from case to theory to application",
            "Explicit scope conditions",
            "Use 'strategic essentialism' deliberately"
        ]
    )
]

THEORY_SEED_INTERLOCUTORS = [
    ActorUnit(
        id="THEORY_ACTOR_POSITIVIST",
        name="Positivist Tradition",
        domain=Domain.THEORY,
        core_commitments=["Value neutrality", "Empirical verification", "Generalization"],
        predictable_objections=[
            Objection(topic="Normative claims", typical_form="But isn't this just ideology disguised as analysis?"),
            Objection(topic="Case studies", typical_form="N=1, how do you generalize?")
        ]
    ),
    ActorUnit(
        id="THEORY_ACTOR_POSTCOLONIAL",
        name="Postcolonial Critique",
        domain=Domain.THEORY,
        core_commitments=["Center marginalized voices", "Critique Eurocentrism", "Material effects of knowledge"],
        predictable_objections=[
            Objection(topic="Western theory", typical_form="Whose knowledge is being centered here?"),
            Objection(topic="Universal claims", typical_form="This universalism masks particular interests")
        ]
    )
]
```

### Theory-Specific Grids

```python
THEORY_CUSTOM_GRIDS = [
    GridDefinition(
        name="INTELLECTUAL_POSITION",
        slots=["Lineage", "Key_Claims", "Methods", "Exemplars", "Opponents"],
        applicable_to=[UnitType.CONCEPT],
        description="Situate concepts within intellectual traditions"
    ),
    GridDefinition(
        name="ARGUMENTATIVE",
        slots=["Thesis", "Antithesis", "Synthesis", "Sublation_Candidate"],
        applicable_to=[UnitType.DIALECTIC],
        description="Track Hegelian movement of ideas"
    )
]
```

---

## 5.3 Foundation Strategy Domain

**Purpose:** Design philanthropic strategies. Navigate actor landscapes. Sequence interventions.

### Vocabulary

| Generic | Foundation Domain |
|---------|-------------------|
| Concept | **Play** |
| Dialectic | **Strategic Tension** |
| Scenario | **Intervention Pathway** |
| Actor | **Strategic Player** |
| Instrument | **Intervention Type** |

### Seed Doctrine

```python
FOUNDATION_SEED_CONCEPTS = [
    ConceptUnit(
        id="FOUNDATION_CONCEPT_LEVERAGE",
        name="Philanthropic Leverage",
        domain=Domain.FOUNDATION,
        definition="The ratio of systemic change to philanthropic dollars spent",
        what_it_enables=["Comparison across interventions", "Focus on catalytic vs. direct funding"],
        what_it_forecloses=["Pure service delivery mentality"]
    ),
    ConceptUnit(
        id="FOUNDATION_CONCEPT_ECOSYSTEM",
        name="Ecosystem Resilience",
        domain=Domain.FOUNDATION,
        definition="The capacity of an intervention space to maintain function under stress",
        what_it_enables=["Funding diversity of approaches", "Supporting connective tissue"],
        what_it_forecloses=["Single-organization bets", "Monopoly grantmaking"]
    )
]

FOUNDATION_SEED_DIALECTICS = [
    DialecticUnit(
        id="FOUNDATION_DIALECTIC_VISIBILITY_PROTECTION",
        name="Visibility ↔ Protection",
        domain=Domain.FOUNDATION,
        pole_a=Pole(name="Visibility", description="Public profile, advocacy, naming and shaming"),
        pole_b=Pole(name="Protection", description="Low profile, security, operational security"),
        navigation_strategies=[
            "Different grantees for different roles",
            "Phased approach (build capacity quietly, then go public)",
            "Rapid response funds for when visibility becomes necessary"
        ]
    )
]

FOUNDATION_SEED_ACTORS = [
    ActorUnit(
        id="FOUNDATION_ACTOR_HOST_GOVT",
        name="Host Government",
        domain=Domain.FOUNDATION,
        actor_type=ActorType.REGULATOR,
        interests=["Maintain sovereignty", "Access to resources", "Domestic legitimacy"],
        characteristic_moves=["Registration requirements", "Funding restrictions", "NGO laws"],
        triggers=["Foreign interference narrative", "Election cycles", "Regime criticism"]
    ),
    ActorUnit(
        id="FOUNDATION_ACTOR_LOCAL_CSO",
        name="Local Civil Society",
        domain=Domain.FOUNDATION,
        actor_type=ActorType.ALLY,
        interests=["Sustainability", "Autonomy", "Legitimacy"],
        characteristic_moves=["Coalition building", "Community mobilization", "Translation work"],
        constraints=["Funding dependency", "State pressure", "Capacity limits"]
    )
]
```

### Foundation-Specific Grids

```python
FOUNDATION_CUSTOM_GRIDS = [
    GridDefinition(
        name="THEORY_OF_CHANGE",
        slots=["Inputs", "Activities", "Outputs", "Outcomes", "Impact", "Assumptions"],
        applicable_to=[UnitType.SCENARIO],
        description="Standard ToC framework for intervention pathways"
    ),
    GridDefinition(
        name="EXIT_STRATEGY",
        slots=["Success_Conditions", "Handoff_Plan", "Sustainability_Indicators", "Failure_Conditions"],
        applicable_to=[UnitType.SCENARIO, UnitType.INSTRUMENT],
        description="Plan for foundation exit from intervention"
    ),
    GridDefinition(
        name="RISK_REGISTER",
        slots=["Risk", "Likelihood", "Impact", "Mitigation", "Owner"],
        applicable_to=[UnitType.SCENARIO, UnitType.INSTRUMENT],
        description="Track operational and strategic risks"
    )
]
```

---

## 5.4 Brand Strategy Domain

**Purpose:** Position brands in market. Navigate brand tensions. Design brand trajectories.

### Vocabulary

| Generic | Brand Domain |
|---------|--------------|
| Concept | **Position** |
| Dialectic | **Brand Tension** |
| Scenario | **Brand Trajectory** |
| Actor | **Market Actor** |
| Instrument | **Strategic Move** |

### Seed Doctrine

```python
BRAND_SEED_CONCEPTS = [
    ConceptUnit(
        id="BRAND_CONCEPT_RESTRAINED_INTENSITY",
        name="Restrained Intensity",
        domain=Domain.BRAND,
        definition="Maximum expressive power delivered through minimal means",
        what_it_enables=["Gucci-like maximalism without excess", "Drama through constraint"],
        what_it_forecloses=["Quiet minimalism", "Loud maximalism"],
        examples=["Bottega Veneta's intrecciato", "Japanese architecture"]
    ),
    ConceptUnit(
        id="BRAND_CONCEPT_HERITAGE_INNOVATION",
        name="Heritage Through Novelty",
        domain=Domain.BRAND,
        definition="Expressing tradition not through repetition but through creative reinterpretation",
        what_it_enables=["Relevance without abandoning roots", "Evolution as continuity"],
        what_it_forecloses=["Pure archival revivals", "Rootless trend-chasing"]
    )
]

BRAND_SEED_DIALECTICS = [
    DialecticUnit(
        id="BRAND_DIALECTIC_HERITAGE_NOVELTY",
        name="Heritage ↔ Novelty",
        domain=Domain.BRAND,
        pole_a=Pole(name="Heritage", description="Brand history, archives, signature codes"),
        pole_b=Pole(name="Novelty", description="Fresh designs, new directions, surprise"),
        navigation_strategies=[
            "Reinterpret signature codes, don't just repeat",
            "New techniques on classic forms",
            "Alternate seasons of more/less heritage"
        ]
    ),
    DialecticUnit(
        id="BRAND_DIALECTIC_EXCLUSIVITY_ACCESS",
        name="Exclusivity ↔ Accessibility",
        domain=Domain.BRAND,
        pole_a=Pole(name="Exclusivity", description="Limited availability, high price, barrier to entry"),
        pole_b=Pole(name="Accessibility", description="Broader reach, entry price points, visibility"),
        navigation_strategies=[
            "Tiered product architecture",
            "Exclusive experiences, accessible products",
            "Geographic/temporal exclusivity"
        ]
    )
]

BRAND_SEED_ACTORS = [
    ActorUnit(
        id="BRAND_ACTOR_HERMES",
        name="Hermès",
        domain=Domain.BRAND,
        actor_type=ActorType.COMPETITOR,
        interests=["Protect ultra-luxury position", "Craft narrative", "Family control"],
        characteristic_moves=["Ignore competitors", "Double down on waitlists", "Never discount"],
        blind_spots=["Digital natives", "Resale market"]
    ),
    ActorUnit(
        id="BRAND_ACTOR_CORE_CUSTOMER",
        name="Core Customer Base",
        domain=Domain.BRAND,
        actor_type=ActorType.CONSTITUENCY,
        interests=["Status signaling", "Quality assurance", "Identity expression"],
        triggers=["Brand dilution", "Visible discounting", "Demographic shift"]
    )
]
```

---

## 5.5 Government Planning Domain

**Purpose:** Design development strategies. Navigate trade-offs. Coordinate actors.

### Vocabulary

| Generic | Government Domain |
|---------|-------------------|
| Concept | **Policy Frame** |
| Dialectic | **Development Trade-off** |
| Scenario | **Development Style** |
| Actor | **Development Actor** |
| Instrument | **Policy Instrument** |

### Seed Doctrine

```python
GOVERNMENT_SEED_CONCEPTS = [
    ConceptUnit(
        id="GOVT_CONCEPT_TECH_SOVEREIGNTY",
        name="Technological Sovereignty",
        domain=Domain.GOVERNMENT,
        definition="Capacity to develop, maintain, and regulate technology domestically",
        what_it_enables=["Strategic autonomy", "Industrial upgrading", "Security in key sectors"],
        what_it_forecloses=["Pure comparative advantage", "Full integration into global supply chains"],
        examples=["EU digital sovereignty", "China's semiconductor policy", "India's UPI"]
    ),
    ConceptUnit(
        id="GOVT_CONCEPT_LEAPFROG",
        name="Developmental Leapfrogging",
        domain=Domain.GOVERNMENT,
        definition="Skipping intermediate stages of development by adopting latest technologies/models",
        what_it_enables=["Rapid modernization", "Avoiding legacy lock-in"],
        what_it_forecloses=["Gradual capability building", "Learning-by-doing in intermediate tech"],
        examples=["Mobile banking in Africa", "Estonia's e-governance"]
    )
]

GOVERNMENT_SEED_DIALECTICS = [
    DialecticUnit(
        id="GOVT_DIALECTIC_GROWTH_EQUITY",
        name="Growth ↔ Equity",
        domain=Domain.GOVERNMENT,
        pole_a=Pole(name="Growth", description="GDP expansion, investment attraction, productivity"),
        pole_b=Pole(name="Equity", description="Distribution, inclusion, poverty reduction"),
        navigation_strategies=[
            "Redistributive taxation after growth",
            "Inclusive growth targeting",
            "Geographic equity through industrial policy"
        ]
    ),
    DialecticUnit(
        id="GOVT_DIALECTIC_SOVEREIGNTY_INTEGRATION",
        name="Sovereignty ↔ Integration",
        domain=Domain.GOVERNMENT,
        pole_a=Pole(name="Sovereignty", description="Policy autonomy, self-reliance, national control"),
        pole_b=Pole(name="Integration", description="Trade openness, FDI, global supply chains"),
        navigation_strategies=[
            "Strategic sectors vs. open sectors",
            "Conditional integration (local content requirements)",
            "Regional integration as middle path"
        ]
    )
]

GOVERNMENT_SEED_SCENARIOS = [
    ScenarioUnit(
        id="GOVT_SCENARIO_INDUSTRIAL_CHAMPION",
        name="Industrial Champion Path (Korea Model)",
        domain=Domain.GOVERNMENT,
        description="State-directed industrial policy creating national champions in targeted sectors",
        value_commitments=["Export orientation", "Technological upgrading", "State capacity"],
        who_benefits=["Large firms", "Skilled workers", "Urban centers"],
        who_loses=["SMEs initially", "Rural areas", "Consumer welfare short-term"],
        time_horizon=TimeHorizon.LONG,
        phases=[
            ScenarioPhase(name="Protection", time_range="Years 1-5", key_actions=["Tariffs", "Subsidies"]),
            ScenarioPhase(name="Export Push", time_range="Years 5-15", key_actions=["FDI attraction", "Technology transfer"]),
            ScenarioPhase(name="Upgrading", time_range="Years 15-30", key_actions=["R&D investment", "Liberalization"])
        ]
    )
]

GOVERNMENT_SEED_ACTORS = [
    ActorUnit(
        id="GOVT_ACTOR_IMF",
        name="IMF",
        domain=Domain.GOVERNMENT,
        actor_type=ActorType.REGULATOR,
        interests=["Macroeconomic stability", "Market liberalization", "Debt sustainability"],
        characteristic_moves=["Conditionality", "Surveillance", "Technical assistance"],
        triggers=["Balance of payments crisis", "Debt accumulation", "Currency volatility"]
    ),
    ActorUnit(
        id="GOVT_ACTOR_DOMESTIC_FIRMS",
        name="Domestic Private Sector",
        domain=Domain.GOVERNMENT,
        actor_type=ActorType.ALLY,
        interests=["Protection from competition", "Access to finance", "Infrastructure"],
        characteristic_moves=["Lobbying", "Coalition building", "Exit threat"],
        constraints=["Capital access", "Technology gaps", "Scale limitations"]
    )
]
```

---

## 5.6 Implementation Roadmap

### Phase 1: Core Data Model (Week 1-2)

**Goal:** Implement the unit types and basic persistence.

```python
# File: models/units.py
# Implement:
# - ConceptUnit, DialecticUnit, ScenarioUnit, ActorUnit, InstrumentUnit
# - EpistemicStatus, SurpriseProfile, CrucialityAssessment
# - Base relationships and cross-references

# File: models/grids.py
# Implement:
# - GridDefinition, GridInstance, SlotContent
# - Tier classification (Required, Flexible, Wildcard)

# File: persistence/store.py
# Implement:
# - SQLite/PostgreSQL storage for units
# - JSON serialization for complex nested structures
# - Query interfaces for unit retrieval
```

**Deliverable:** Can create, store, and retrieve all 5 unit types with basic grids.

### Phase 2: Grid System (Week 3-4)

**Goal:** Implement the Three-Tier Grid System.

```python
# File: grids/tier_1.py
# Implement:
# - LOGICAL, ACTOR, TEMPORAL grids
# - Automatic applicability to all unit types

# File: grids/tier_2.py
# Implement:
# - All Flexible grids organized by unit type
# - Applicability checking logic

# File: grids/tier_3.py
# Implement:
# - WildcardGrid creation from LLM
# - Promotion logic (uses_count, ratings)
# - Validation and rejection

# File: grids/operations.py
# Implement:
# - apply_grid(), fill_slot(), add_cross_reference()
# - GridSelector for recommending applicable grids
# - MultiGridView for synthesizing across grids
```

**Deliverable:** Can apply multiple grids to units, fill slots, create cross-references.

### Phase 3: Epistemic Infrastructure (Week 5-6)

**Goal:** Implement Shackle's framework.

```python
# File: epistemic/surprise.py
# Implement:
# - SurpriseProfile, SurpriseLevel
# - FocusOutcomes, FocusPoint

# File: epistemic/cruciality.py
# Implement:
# - CrucialityAssessment
# - Reversibility, CrucialityLevel

# File: epistemic/kaleidic.py
# Implement:
# - KaleidicTrigger, KaleidicRegistry
# - Trigger matching and alerting

# File: epistemic/status.py
# Implement:
# - EpistemicStatus with all fields
# - Assumption tracking
# - Gap detection
```

**Deliverable:** All units carry epistemic metadata; kaleidic triggers can be registered and matched.

### Phase 4: Generative Process (Week 7-9)

**Goal:** Implement the FRICTION → PROMOTE pipeline.

```python
# File: generative/friction.py
# Implement:
# - FrictionDetector with all trigger types
# - FrictionEvent logging

# File: generative/diagnosis.py
# Implement:
# - Diagnoser with LLM integration
# - All DiagnosisType handling

# File: generative/coin.py
# Implement:
# - UnitCoiner for each unit type
# - Hegelian sublation for dialectics

# File: generative/test.py
# Implement:
# - UnitTester with interlocutor simulation
# - Edge case generation
# - Consistency checking

# File: generative/promote.py
# Implement:
# - Abstractor for generalization
# - PromotionEvaluator with all criteria
# - Doctrine store integration
```

**Deliverable:** Complete generative pipeline from friction detection through doctrine promotion.

### Phase 5: Research Commissioning (Week 10)

**Goal:** Implement gap detection and research integration.

```python
# File: research/gaps.py
# Implement:
# - GapDetector scanning all units
# - Priority assessment

# File: research/commission.py
# Implement:
# - ResearchCommission generation
# - ResearchExecutor with web search + LLM

# File: research/integrate.py
# Implement:
# - ResearchIntegrator for slot updates
# - Human review workflow
```

**Deliverable:** System can detect gaps, commission research, and integrate findings.

### Phase 6: Interlocutor Modeling (Week 11-12)

**Goal:** Implement actor/interlocutor simulation.

```python
# File: actors/model.py
# Implement:
# - InterlocutorModel with full schema
# - ResponsePattern, Objection

# File: actors/simulate.py
# Implement:
# - InterlocutorSimulator (rule-based, LLM, hybrid)
# - Response generation prompts

# File: actors/integrate.py
# Implement:
# - InterlocutorIntegrator
# - Objection categorization
# - Blind spot discovery
```

**Deliverable:** Can simulate interlocutor responses and integrate feedback.

### Phase 7: Domain Instantiation (Week 13-14)

**Goal:** Set up the four domains with seed doctrine.

```python
# File: domains/theory.py
# File: domains/foundation.py
# File: domains/brand.py
# File: domains/government.py

# Each implements:
# - DomainInstantiation configuration
# - Seed concepts, dialectics, actors
# - Custom grids
# - Example scenarios
```

**Deliverable:** All four domains configured with starter doctrine.

### Phase 8: Web Interface (Week 15-18)

**Goal:** Build a Flask/React interface for the system.

```
Features:
1. Project management (create, list, open projects)
2. Unit browser (view all units by type, search, filter)
3. Unit editor (create/edit units with grid support)
4. Grid workspace (apply grids, fill slots, cross-reference)
5. Doctrine browser (view stable doctrine, promote units)
6. Generative dashboard (view friction events, diagnoses, pending promotions)
7. Research queue (view commissioned research, review results)
8. Interlocutor panel (run simulations, review responses)
```

---

## 5.7 Database Schema Overview

```sql
-- Core units
CREATE TABLE units (
    id TEXT PRIMARY KEY,
    unit_type TEXT NOT NULL,  -- CONCEPT, DIALECTIC, SCENARIO, ACTOR, INSTRUMENT
    domain TEXT NOT NULL,
    name TEXT NOT NULL,
    data JSON NOT NULL,  -- Full unit data
    status TEXT NOT NULL,  -- DRAFT, VALIDATED, PROMOTED, DEPRECATED
    created_at TIMESTAMP,
    promoted_at TIMESTAMP,
    project_id TEXT
);

-- Grid instances
CREATE TABLE grid_instances (
    id TEXT PRIMARY KEY,
    unit_id TEXT NOT NULL REFERENCES units(id),
    grid_type TEXT NOT NULL,
    tier INTEGER NOT NULL,
    filled_slots JSON NOT NULL,
    created_at TIMESTAMP,
    completeness FLOAT
);

-- Cross-references
CREATE TABLE cross_references (
    id TEXT PRIMARY KEY,
    source_unit_id TEXT NOT NULL REFERENCES units(id),
    target_unit_id TEXT NOT NULL REFERENCES units(id),
    relationship TEXT NOT NULL,
    note TEXT,
    created_at TIMESTAMP
);

-- Wildcard grids (tier 3)
CREATE TABLE wildcard_grids (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    slots JSON NOT NULL,
    description TEXT,
    invented_by TEXT,
    status TEXT,  -- PROPOSED, VALIDATED, PROMOTED, REJECTED
    uses_count INTEGER DEFAULT 0,
    usefulness_ratings JSON
);

-- Friction events
CREATE TABLE friction_events (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    description TEXT NOT NULL,
    severity TEXT NOT NULL,
    trigger_content TEXT,
    trigger_location TEXT,
    status TEXT,  -- DETECTED, DIAGNOSING, RESOLVED, DEFERRED
    diagnosis_id TEXT,
    created_at TIMESTAMP
);

-- Research commissions
CREATE TABLE research_commissions (
    id TEXT PRIMARY KEY,
    gap_description TEXT NOT NULL,
    research_question TEXT NOT NULL,
    status TEXT,  -- PENDING, IN_PROGRESS, COMPLETED, FAILED
    result JSON,
    created_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Kaleidic triggers
CREATE TABLE kaleidic_triggers (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    domain TEXT NOT NULL,
    triggering_conditions JSON NOT NULL,
    effects JSON NOT NULL,
    warning_signs JSON,
    active BOOLEAN DEFAULT TRUE
);
```

---

## 5.8 API Endpoints

```python
# Units
POST   /api/units                    # Create unit
GET    /api/units                    # List units (with filters)
GET    /api/units/{id}               # Get unit
PUT    /api/units/{id}               # Update unit
DELETE /api/units/{id}               # Delete unit
POST   /api/units/{id}/promote       # Promote to doctrine

# Grids
POST   /api/units/{id}/grids         # Apply grid to unit
GET    /api/units/{id}/grids         # List grids on unit
PUT    /api/units/{id}/grids/{grid}  # Update grid instance
POST   /api/grids/propose            # Propose wildcard grid

# Cross-references
POST   /api/cross-references         # Create cross-reference
GET    /api/units/{id}/references    # Get references for unit

# Generative
GET    /api/friction                 # List friction events
POST   /api/friction/{id}/diagnose   # Diagnose friction
POST   /api/friction/{id}/coin       # Coin new unit
POST   /api/units/{id}/test          # Test unit

# Research
POST   /api/research/commission      # Commission research
GET    /api/research/pending         # List pending research
POST   /api/research/{id}/integrate  # Integrate research result

# Interlocutors
GET    /api/interlocutors            # List interlocutor models
POST   /api/simulate                 # Simulate interlocutor response

# Kaleidic
GET    /api/kaleidic/triggers        # List triggers
POST   /api/kaleidic/check           # Check for triggered events
```

---

## 5.9 Success Criteria

### Minimum Viable Product (MVP)

1. ✅ Create and store all 5 unit types
2. ✅ Apply Required and Flexible grids
3. ✅ Fill slots and create cross-references
4. ✅ Basic epistemic status tracking
5. ✅ Web interface for browsing/editing units
6. ✅ Single domain (Theory) fully instantiated

### Full System

1. ✅ All four domains instantiated with seed doctrine
2. ✅ Wildcard grid creation and promotion
3. ✅ Full Shackle epistemic infrastructure
4. ✅ Complete generative pipeline (FRICTION → PROMOTE)
5. ✅ Research commissioning and integration
6. ✅ Interlocutor simulation
7. ✅ Kaleidic trigger monitoring
8. ✅ Multi-project support
9. ✅ Doctrine versioning and rollback

---

# APPENDIX: Quick Reference

## The 6-Layer Stack

```
Layer 5: ARTIFACT (what we're building)
Layer 4: 5 UNITS (Concept, Dialectic, Scenario, Actor, Instrument)
Layer 3: MULTI-GRID (analytical lenses within units)
Layer 2: SHACKLE (epistemic infrastructure — orthogonal)
Layer 1: GENERATIVE (how new units are created)
Layer 0: DOCTRINE (stable, validated units)
```

## The 5 Core Units

| Unit | What It Is | Example (Theory) | Example (Government) |
|------|------------|------------------|---------------------|
| Concept | Named way of carving reality | "Paradigm" | "Technological Sovereignty" |
| Dialectic | Trade-off to navigate | "Rigor ↔ Accessibility" | "Growth ↔ Equity" |
| Scenario | Coherent future path | "Framework Evolution" | "Industrial Champion Path" |
| Actor | Entity with agency | "Marxist Tradition" | "IMF" |
| Instrument | Tool for action | "Genealogical Critique" | "Tax Incentive" |

## The Three-Tier Grid System

| Tier | Name | Source | Examples |
|------|------|--------|----------|
| 1 | Required | Core architecture | LOGICAL, ACTOR, TEMPORAL |
| 2 | Flexible | Domain taxonomy | FUNCTIONAL, POLE, MECHANISM |
| 3 | Wildcard | LLM-invented | GEOPOLITICAL_POSITIONING |

## Shackle Concepts

- **Potential Surprise:** How surprised would we be?
- **Focus Gain/Loss:** Best/worst conceivable outcomes
- **Cruciality:** How irreversible and transformative?
- **Kaleidic Trigger:** Events that reframe everything

## Generative Pipeline

```
FRICTION → DIAGNOSIS → COIN → TEST → ABSTRACT → PROMOTE
```

---

*End of STRATEGIZER-IMPLEMENTATION-SPEC.md*

*Version 1.0 — December 2025*
