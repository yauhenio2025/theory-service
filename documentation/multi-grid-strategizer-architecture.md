# Multi-Grid Strategizer Architecture

*December 26, 2025*

---

## Executive Summary

This document proposes a **generative multi-grid architecture** for strategic thinking across domains. The core innovation: **there is no fixed grid**. Instead, multiple analytical grids are generated dynamically based on domain, genre, and project-specific needs. Each grid represents a different way of "slicing and dicing reality" — logical, temporal, functional, throughline-based, and more. A multi-agent system (Grid Generator, Gap Filler, Refactorer) orchestrates the creation, population, and refinement of these grids, ensuring robustness across all dimensions before execution.

---

## Part 1: The Multi-Grid Paradigm

### Why No Fixed Grid?

Previous approaches assumed a universal slot architecture:
- Essay-flow: PHENOMENON, DEFINITION, ILLUSTRATION, HISTORY, DIAGNOSIS, IMPLICATION, INTERVENTION, OBJECTION
- Foundation strategy: CONTEXT, DIAGNOSIS, THEORY_OF_CHANGE, INTERVENTION, EVIDENCE, RISK...

**The problem:** Different projects within the same domain may need radically different analytical structures. A policy brief needs different slices than a strategic plan. A brand launch needs different grids than a repositioning.

**The insight:** Grids themselves should be **emergent artifacts** based on:
1. Domain expectations (what grids are typically useful here?)
2. Genre conventions (what does this type of deliverable require?)
3. Project specifics (what does THIS particular project need?)

### The Three-Tier Grid System

Not all grids are created equal. We distinguish:

```
┌─────────────────────────────────────────────────────────────────┐
│                   THREE-TIER GRID SYSTEM                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TIER 1: REQUIRED GRIDS (Always present, non-negotiable)        │
│  ├─ LOGICAL — Every project needs sound argument structure      │
│  ├─ ACTOR — Every project has stakeholders whose positions      │
│  │          and responses matter                                │
│  └─ TEMPORAL — Everything unfolds in time with dependencies     │
│                                                                 │
│  These grids are ALWAYS instantiated. The Grid Generator        │
│  populates them from project brief; user cannot remove them.    │
│  They form the irreducible foundation of strategic analysis.    │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  TIER 2: FLEXIBLE GRIDS (From taxonomy, recommended)            │
│  ├─ Domain-typical grids suggested by Grid Generator            │
│  ├─ Examples: FUNCTIONAL, THROUGHLINE, SCENARIO, CAUSAL,        │
│  │           EVIDENTIAL, RESOURCE, NORMATIVE...                 │
│  └─ User can approve, reject, or defer                          │
│                                                                 │
│  These grids come from our learned taxonomy — patterns that     │
│  have proven useful across projects. Grid Generator recommends  │
│  based on domain + genre + brief signals.                       │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  TIER 3: WILDCARD GRIDS (LLM-proposed, emergent)                │
│  ├─ Novel grid types invented FOR THIS PROJECT                  │
│  ├─ Not from taxonomy — genuinely new analytical lenses         │
│  ├─ LLM explains: "This project needs a grid we don't have..."  │
│  └─ If validated, can be promoted to Tier 2 taxonomy            │
│                                                                 │
│  This is where genuine innovation happens. The LLM might see    │
│  a pattern in the project brief that doesn't fit any existing   │
│  grid type and propose something new.                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Why this matters:**

| Tier | Purpose | Example |
|------|---------|---------|
| **Required** | Ensures minimum analytical rigor | "You can't skip logical coherence check" |
| **Flexible** | Leverages accumulated wisdom | "Foundation projects usually need SCENARIO grids" |
| **Wildcard** | Enables project-specific insight | "This Moldova project needs a DIASPORA_INFLUENCE grid we've never used before" |

**The Wildcard Mechanism:**

When the Grid Generator analyzes a project brief, it can propose wildcard grids:

```
┌─────────────────────────────────────────────────────────────────┐
│  WILDCARD GRID PROPOSAL                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Grid Generator has identified a pattern not captured by        │
│  existing grid types:                                           │
│                                                                 │
│  PROPOSED: "DIASPORA_INFLUENCE" grid                            │
│                                                                 │
│  Rationale:                                                     │
│  "The project brief mentions Moldova's large diaspora (25% of   │
│   population abroad), remittance flows, and dual citizenship    │
│   patterns. This creates a unique analytical dimension not      │
│   captured by ACTOR (which focuses on domestic stakeholders)    │
│   or RESOURCE (which focuses on financial flows). A dedicated   │
│   DIASPORA_INFLUENCE grid would track:                          │
│   - Diaspora communities by location                            │
│   - Information channels (media consumption, social networks)   │
│   - Remittance patterns and economic influence                  │
│   - Political engagement (voting, advocacy)                     │
│   - Return migration dynamics"                                  │
│                                                                 │
│  Proposed Cell Types:                                           │
│  - COMMUNITY (diaspora population cluster)                      │
│  - CHANNEL (information/influence pathway)                      │
│  - FLOW (remittance or resource movement)                       │
│  - ENGAGEMENT (political participation mode)                    │
│                                                                 │
│  Proposed Relationships:                                        │
│  - INFLUENCES, FUNDS, INFORMS, MOBILIZES                        │
│                                                                 │
│  [Accept Grid] [Modify] [Reject] [Merge into ACTOR]            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Wildcard-to-Taxonomy Promotion:**

If a wildcard grid proves useful across multiple projects, it can be promoted to Tier 2:

```python
class WildcardGrid:
    def __init__(self, name, rationale, cell_types, relationship_types):
        self.name = name
        self.rationale = rationale
        self.cell_types = cell_types
        self.relationship_types = relationship_types
        self.usage_count = 0
        self.projects_used_in = []
        self.user_ratings = []

    def should_promote_to_taxonomy(self):
        """Promote to Tier 2 if consistently useful"""
        return (
            self.usage_count >= 3 and
            len(self.projects_used_in) >= 2 and
            avg(self.user_ratings) >= 4.0
        )
```

### What IS a Grid?

A grid is a **structured analytical lens** that:
- Decomposes the project into cells (units of analysis)
- Defines relationships between cells
- Has saturation criteria (when is it "done"?)
- Has validation criteria (when is it "healthy"?)
- Contributes to the final deliverable

```
┌─────────────────────────────────────────────────────────────────┐
│                        GRID SCHEMA                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  grid_id: "logical-argument-map"                                │
│  grid_type: LOGICAL                                             │
│  purpose: "Map the logical structure of the argument"           │
│                                                                 │
│  cells: [                                                       │
│    { id: "premise_1", type: "PREMISE", content: "...", ... },   │
│    { id: "premise_2", type: "PREMISE", content: "...", ... },   │
│    { id: "conclusion_1", type: "CONCLUSION", depends_on: [...] }│
│  ]                                                              │
│                                                                 │
│  relationships: [                                               │
│    { from: "premise_1", to: "conclusion_1", type: "SUPPORTS" }, │
│    { from: "premise_2", to: "conclusion_1", type: "SUPPORTS" }  │
│  ]                                                              │
│                                                                 │
│  saturation_criteria: {                                         │
│    min_premises_per_conclusion: 2,                              │
│    all_conclusions_supported: true,                             │
│    no_orphan_premises: true                                     │
│  }                                                              │
│                                                                 │
│  health_metrics: {                                              │
│    coverage: 0.85,                                              │
│    coherence: 0.92,                                             │
│    evidence_backing: 0.78                                       │
│  }                                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 2: Grid Type Taxonomy

### Core Grid Types

| Grid Type | Purpose | Cell Types | Relationship Types |
|-----------|---------|------------|-------------------|
| **LOGICAL** | Map argument soundness | Premise, Conclusion, Assumption, Warrant | SUPPORTS, UNDERMINES, QUALIFIES |
| **TEMPORAL** | Map sequences and dependencies | Event, Phase, Milestone, Trigger | PRECEDES, ENABLES, BLOCKS, CAUSES |
| **FUNCTIONAL** | Map rhetorical/functional roles | Phenomenon, Diagnosis, Intervention, Objection | EXPLAINS, ADDRESSES, PREEMPTS |
| **THROUGHLINE** | Map argument threads | Throughline, Slot Articulation, Bridge | SPANS, ARTICULATES, BRIDGES |
| **EVIDENTIAL** | Map evidence relationships | Claim, Evidence, Source | ILLUSTRATES, DEEPENS, CHALLENGES, LIMITS |
| **ACTOR** | Map stakeholder positions | Actor, Position, Interest, Capability | ALLIES_WITH, OPPOSES, ENABLES, CONSTRAINS |
| **SCENARIO** | Map future possibilities | Scenario, Assumption, Trigger, Outcome | LEADS_TO, REQUIRES, FORECLOSES |
| **RESOURCE** | Map resource flows | Resource, Source, Sink, Constraint | FLOWS_TO, CONSUMES, PRODUCES |
| **NORMATIVE** | Map values and trade-offs | Value, Principle, Trade-off, Priority | TRUMPS, BALANCES, CONFLICTS_WITH |
| **CAUSAL** | Map causal mechanisms | Cause, Effect, Mechanism, Condition | CAUSES, MEDIATES, MODERATES |

### Domain-Specific Grid Types

| Domain | Additional Grid Types |
|--------|----------------------|
| **Theory/Essay** | DIALECTICAL (thesis-antithesis-synthesis), GENEALOGICAL (conceptual lineage), DIMENSIONAL (12 philosophical signals) |
| **Foundation** | THEORY_OF_CHANGE (intervention logic), EXIT_CONDITIONS (sustainability criteria), LEARNING_AGENDA (what we'll discover) |
| **Brand** | POSITIONING (competitive space), NARRATIVE_ARC (brand story), SEGMENT (audience slices) |
| **Government** | INSTRUMENT (policy tools), COALITION (political alliances), CAPACITY (state capabilities), SEQUENCING (implementation order) |

### Varsavsky Integration: Style Grids

From Oscar Varsavsky's work on development styles, a special grid type:

```
┌─────────────────────────────────────────────────────────────────┐
│                     DEVELOPMENT STYLE GRID                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Dimensions (radar axes):                                       │
│  ├─ National Autonomy      ████████░░  8/10                    │
│  ├─ Popular Participation  ██████░░░░  6/10                    │
│  ├─ Egalitarianism         ███████░░░  7/10                    │
│  ├─ Economic Growth        ████░░░░░░  4/10                    │
│  ├─ Technical Modernization ██████░░░░  6/10                   │
│  └─ Cultural Preservation  █████████░  9/10                    │
│                                                                 │
│  Style Classification: "Autonomist-Preservationist"             │
│                                                                 │
│  Trade-off Relationships:                                       │
│  ├─ Autonomy ←→ Economic Growth (tension)                      │
│  ├─ Participation ←→ Technical Modernization (neutral)         │
│  └─ Egalitarianism ←→ Cultural Preservation (synergy)          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Shackle Integration: Uncertainty Grids

From GLS Shackle's work on uncertainty:

```
┌─────────────────────────────────────────────────────────────────┐
│                      SCENARIO UNCERTAINTY GRID                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Scenario: "Authoritarian Consolidation"                        │
│                                                                 │
│  Shackle Metrics:                                               │
│  ├─ Potential Surprise (disbelief): 0.3 (not very surprising)  │
│  ├─ Focus Gain (if good): N/A                                   │
│  ├─ Focus Loss (if bad): -8/10 (devastating)                   │
│  └─ Cruciality: HIGH (decision is non-reversible)              │
│                                                                 │
│  Kaleidic Triggers:                                             │
│  ├─ Election results (Q4 2025)                                 │
│  ├─ Constitutional court ruling (Q2 2025)                      │
│  └─ EU funding decision (Q3 2025)                              │
│                                                                 │
│  Epistemic Status:                                              │
│  ├─ Evidence quality: MODERATE                                  │
│  ├─ Key assumptions: 3 critical, 2 verified, 1 untested        │
│  └─ Research gaps: 2 identified, 1 commissioned                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 3: Multi-Agent Architecture

### Agent 1: Grid Generator

**Purpose:** Generate v0 of all relevant grids based on domain, genre, and project brief.

```
┌─────────────────────────────────────────────────────────────────┐
│                      GRID GENERATOR AGENT                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  INPUTS:                                                        │
│  ├─ domain: "foundation_strategy"                               │
│  ├─ genre: "country_strategy"                                   │
│  ├─ project_brief: "5-year strategy for Moldova media support"  │
│  └─ doctrine_library: [available plays, theories, frames...]   │
│                                                                 │
│  PROCESS:                                                       │
│  1. Query genre templates for typical grid requirements         │
│  2. Analyze project brief for domain-specific signals           │
│  3. Generate initial grid set with empty/sparse cells           │
│  4. Propose priority order for grid population                  │
│  5. Flag dependencies between grids                             │
│                                                                 │
│  OUTPUTS:                                                       │
│  ├─ initial_grids: [                                            │
│  │   { grid_type: "LOGICAL", priority: 1, cells: [...] },      │
│  │   { grid_type: "TEMPORAL", priority: 2, cells: [...] },     │
│  │   { grid_type: "ACTOR", priority: 1, cells: [...] },        │
│  │   { grid_type: "THEORY_OF_CHANGE", priority: 2, cells: [...]}│
│  │ ]                                                            │
│  ├─ grid_dependencies: [                                        │
│  │   { from: "ACTOR", to: "SCENARIO", reason: "actor positions  │
│  │     determine scenario plausibility" },                      │
│  │   { from: "LOGICAL", to: "THROUGHLINE", reason: "throughlines│
│  │     must be logically sound" }                               │
│  │ ]                                                            │
│  └─ suggested_population_sequence: [ACTOR, LOGICAL, TEMPORAL...]│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Grid Generator Prompting Strategy:**

```
You are the Grid Generator for a {domain} project in the {genre} genre.

PROJECT BRIEF:
{project_brief}

AVAILABLE GRID TYPES:
{grid_type_taxonomy}

GENRE EXPECTATIONS for {genre}:
{genre_template}

TASK:
1. Identify which grid types are essential for this project
2. Identify which grid types would be valuable but optional
3. For each essential grid, generate v0 structure with:
   - Cell types needed
   - Relationship types needed
   - Saturation criteria
   - Dependencies on other grids
4. Propose a population sequence that respects dependencies

OUTPUT FORMAT: {schema}
```

### Agent 2: Gap Filler

**Purpose:** Populate and validate grids through evidence, questions, and option generation.

```
┌─────────────────────────────────────────────────────────────────┐
│                       GAP FILLER AGENT                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  INPUTS:                                                        │
│  ├─ current_grids: [all grids with current state]               │
│  ├─ evidence_corpus: [all integrated evidence]                  │
│  └─ user_responses: [all prior Q&A]                             │
│                                                                 │
│  MODES:                                                         │
│                                                                 │
│  MODE A: EVIDENCE REQUIREMENT                                   │
│  ├─ Detect cells with low confidence or missing content         │
│  ├─ Formulate research queries for AI/API research agent        │
│  ├─ Route incoming evidence to relevant cells                   │
│  └─ Trigger auto-integration or pending decisions               │
│                                                                 │
│  MODE B: USER INTERROGATION                                     │
│  ├─ Detect cells that require user judgment (not researchable)  │
│  ├─ Formulate questions to clarify/fill gaps                    │
│  ├─ Accumulate answers and update grids                         │
│  └─ Track which answers filled which cells                      │
│                                                                 │
│  MODE C: OPTION GENERATION                                      │
│  ├─ For ambiguous cells, generate 3-5 options                   │
│  ├─ For each option, articulate:                                │
│  │   - Commitment statement (what you're committing to)         │
│  │   - Foreclosure statements (what each alternative gives up)  │
│  │   - Grid impact (what changes across all grids)              │
│  ├─ Present trade-off matrix                                    │
│  └─ After selection, propagate changes across grids             │
│                                                                 │
│  OUTPUTS:                                                       │
│  ├─ research_queries: [queries for research agent]              │
│  ├─ user_questions: [questions for user]                        │
│  ├─ option_sets: [options with commitment/foreclosure]          │
│  └─ updated_grids: [grids with new content/confidence]          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Gap Detection Logic:**

```python
def detect_gaps(grid):
    gaps = []

    # Empty cells
    for cell in grid.cells:
        if cell.content is None or cell.content == "":
            gaps.append(Gap(
                cell_id=cell.id,
                gap_type="EMPTY",
                fillable_by=["evidence", "user", "inference"]
            ))

    # Low confidence cells
    for cell in grid.cells:
        if cell.confidence < 0.6:
            gaps.append(Gap(
                cell_id=cell.id,
                gap_type="LOW_CONFIDENCE",
                fillable_by=["evidence", "user"]
            ))

    # Missing relationships
    for cell in grid.cells:
        if cell.type == "CONCLUSION" and len(cell.supporting_premises) < 2:
            gaps.append(Gap(
                cell_id=cell.id,
                gap_type="UNDERSUPPORTED",
                fillable_by=["evidence", "inference"]
            ))

    # Unaddressed tensions
    for tension in grid.detected_tensions:
        if tension.status != "RESOLVED":
            gaps.append(Gap(
                tension_id=tension.id,
                gap_type="UNRESOLVED_TENSION",
                fillable_by=["user_decision"]
            ))

    return prioritize_gaps(gaps)
```

### Agent 3: Grid Refactorer

**Purpose:** Propose structural changes to existing grids and generation of new grids.

```
┌─────────────────────────────────────────────────────────────────┐
│                     GRID REFACTORER AGENT                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  INPUTS:                                                        │
│  ├─ current_grids: [all grids with current state]               │
│  ├─ evidence_corpus: [all integrated evidence]                  │
│  ├─ user_patterns: [patterns in user responses]                 │
│  └─ grid_health_metrics: [saturation, coherence, coverage...]   │
│                                                                 │
│  DETECTION MODES:                                               │
│                                                                 │
│  MODE A: GRID SURGERY                                           │
│  ├─ Detect overlapping grids → suggest MERGE                    │
│  ├─ Detect overloaded grids → suggest SPLIT                     │
│  ├─ Detect misframed grids → suggest REFRAME                    │
│  ├─ Detect obsolete grids → suggest DEPRECATE                   │
│  └─ Detect orphan cells → suggest REHOME                        │
│                                                                 │
│  MODE B: NEW GRID PROPOSAL                                      │
│  ├─ Detect patterns not captured by existing grids              │
│  ├─ Detect evidence clusters without grid home                  │
│  ├─ Detect recurring user concerns without grid representation  │
│  └─ Propose new grid type with rationale                        │
│                                                                 │
│  MODE C: CROSS-GRID OPTIMIZATION                                │
│  ├─ Detect cells that appear in multiple grids                  │
│  ├─ Propose cell consolidation or linking                       │
│  ├─ Detect grid dependency violations                           │
│  └─ Propose dependency reordering                               │
│                                                                 │
│  OUTPUTS:                                                       │
│  ├─ refactoring_proposals: [                                    │
│  │   { operation: "SPLIT", grid: "ACTOR", reason: "..." },     │
│  │   { operation: "NEW_GRID", grid_type: "COALITION", ... }    │
│  │ ]                                                            │
│  └─ strategic_advisor_recommendations: [                        │
│  │   { category: "OVERLAPS", details: "..." },                 │
│  │   { category: "GAPS", details: "..." }                      │
│  │ ]                                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Refactoring Detection Heuristics:**

| Signal | Proposed Operation | Rationale |
|--------|-------------------|-----------|
| Two grids share >40% of cells | MERGE | Redundant analytical lenses |
| Grid has >30 cells | SPLIT | Overloaded lens, losing analytical power |
| Grid health <50% after 3 rounds | REFRAME or DEPRECATE | Lens isn't working for this project |
| Evidence cluster with no grid home | NEW_GRID | Reality has dimension we're not capturing |
| User keeps asking questions in one area | NEW_GRID | User sees dimension we haven't formalized |
| Cell appears in 3+ grids | CONSOLIDATE | Same content serving multiple purposes |

---

## Part 4: Grid Sequencing and Maturation

### The Maturation Pipeline

Not all grids can be worked on simultaneously. Some must mature before others can be populated.

```
┌─────────────────────────────────────────────────────────────────┐
│                    GRID MATURATION PIPELINE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PHASE 1: FOUNDATION GRIDS                                      │
│  ├─ ACTOR grid (who are the players?)                          │
│  ├─ CONTEXT grid (what's the situation?)                       │
│  └─ CONSTRAINT grid (what can't change?)                       │
│                                                                 │
│  PHASE 2: ANALYTICAL GRIDS                                      │
│  ├─ LOGICAL grid (what's the argument structure?)              │
│  ├─ CAUSAL grid (what causes what?)                            │
│  ├─ TEMPORAL grid (what's the sequence?)                       │
│  └─ Requires: Phase 1 grids at ≥70% health                     │
│                                                                 │
│  PHASE 3: STRATEGIC GRIDS                                       │
│  ├─ SCENARIO grid (what futures are possible?)                 │
│  ├─ THEORY_OF_CHANGE grid (how will we create change?)         │
│  ├─ INSTRUMENT grid (what tools will we use?)                  │
│  └─ Requires: Phase 2 grids at ≥70% health                     │
│                                                                 │
│  PHASE 4: SYNTHESIS GRIDS                                       │
│  ├─ THROUGHLINE grid (what are the core arguments?)            │
│  ├─ NARRATIVE grid (what's the story?)                         │
│  └─ Requires: Phase 3 grids at ≥70% health                     │
│                                                                 │
│  PHASE 5: EXECUTION GRIDS                                       │
│  ├─ EXECUTION_PLAN grid (what exactly will we do?)             │
│  ├─ MONITORING grid (how will we know it's working?)           │
│  └─ Requires: Phase 4 grids at ≥80% health                     │
│                                                                 │
│  ═══════════════════════════════════════════════════════       │
│  Grids in later phases accept contributions early but are       │
│  NOT fully editable until prior phase grids are healthy         │
│  ═══════════════════════════════════════════════════════       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Grid Health Metrics

```python
class GridHealth:
    def __init__(self, grid):
        self.grid = grid

    def calculate(self):
        return {
            "saturation": self.cell_saturation(),      # % cells filled
            "confidence": self.avg_confidence(),        # avg cell confidence
            "coherence": self.internal_coherence(),     # relationships valid
            "coverage": self.domain_coverage(),         # covers expected areas
            "tensions": self.unresolved_tension_count() # 0 = best
        }

    def overall_health(self):
        metrics = self.calculate()
        return (
            metrics["saturation"] * 0.25 +
            metrics["confidence"] * 0.25 +
            metrics["coherence"] * 0.25 +
            metrics["coverage"] * 0.15 +
            (1 - min(metrics["tensions"] / 10, 1)) * 0.10
        )

    def is_healthy(self, threshold=0.7):
        return self.overall_health() >= threshold
```

### Gating Rules

```
┌─────────────────────────────────────────────────────────────────┐
│                        GATING RULES                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  RULE 1: Dependency Gating                                      │
│  ├─ Grid B depends on Grid A                                    │
│  ├─ Grid B cells are READ-ONLY until Grid A health ≥ 70%       │
│  └─ User can VIEW Grid B but cannot COMMIT changes              │
│                                                                 │
│  RULE 2: Propagation Gating                                     │
│  ├─ Changes in Grid A may invalidate cells in dependent Grid B  │
│  ├─ When Grid A changes significantly, Grid B enters REVIEW     │
│  └─ Affected Grid B cells flagged for re-validation             │
│                                                                 │
│  RULE 3: Execution Gating                                       │
│  ├─ EXECUTION_PLAN grid requires ALL prior grids at ≥ 80%      │
│  ├─ Cannot "finalize" until this threshold met                  │
│  └─ System shows "not ready for execution" with gap analysis    │
│                                                                 │
│  RULE 4: Override with Acknowledgment                           │
│  ├─ User CAN override gating rules                              │
│  ├─ But must acknowledge "proceeding with unhealthy grid X"     │
│  └─ Acknowledgment logged in session commitments                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 5: The Innovation Stack

### Core Innovation: Dynamic Grid Generation

The fundamental shift:

| OLD APPROACH | NEW APPROACH |
|--------------|--------------|
| Fixed slots for all projects | Grids generated per project |
| One analytical lens | Multiple simultaneous lenses |
| Universal saturation criteria | Grid-specific health metrics |
| Linear stage progression | Dependency-based maturation |
| Fixed agents | Specialized agents per function |

### Integration with Prior Innovations

| Prior Innovation | Integration with Multi-Grid |
|-----------------|----------------------------|
| **12 Philosophical Signals** | Becomes DIMENSIONAL grid type with 12 axes |
| **Varsavsky Development Styles** | Becomes STYLE grid type with radar visualization |
| **Shackle Uncertainty** | Becomes SCENARIO grid enhancement with surprise/cruciality metrics |
| **Interlocutor Models** | Becomes ACTOR grid cells with response templates |
| **Evidence Integration** | Applies to ALL grids, routes evidence to appropriate cells |
| **Tension Detection** | Applies ACROSS grids, detects cross-grid tensions |
| **Refactoring Dashboard** | Now operates on GRIDS not just throughlines |
| **Commitment/Foreclosure** | Applies to grid-level decisions, not just cell decisions |

### The User Experience

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER JOURNEY (SIMPLIFIED)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. USER provides PROJECT BRIEF                                 │
│     "5-year media support strategy for Moldova"                 │
│                                                                 │
│  2. GRID GENERATOR proposes initial grid set                    │
│     "For this project, I recommend: ACTOR, CONTEXT, LOGICAL,    │
│      TEMPORAL, THEORY_OF_CHANGE, SCENARIO, EXECUTION_PLAN.      │
│      Shall I also add COALITION grid given political context?"  │
│                                                                 │
│  3. USER approves/modifies grid set                             │
│     "Yes to COALITION, and add a SUSTAINABILITY grid"           │
│                                                                 │
│  4. GAP FILLER begins population sequence                       │
│     Phase 1: "Let's start with ACTOR grid. Who are the key     │
│              players in Moldova's media landscape?"             │
│                                                                 │
│  5. USER responds to questions / reviews evidence               │
│     Questions + evidence fill grid cells                        │
│                                                                 │
│  6. System shows GRID HEALTH DASHBOARD                          │
│     "ACTOR: 85% | CONTEXT: 72% | LOGICAL: 45% (blocked)        │
│      LOGICAL grid now unlocked - Phase 2 ready"                 │
│                                                                 │
│  7. REFACTORER periodically suggests improvements               │
│     "Evidence suggests splitting ACTOR grid into DOMESTIC_ACTORS│
│      and INTERNATIONAL_ACTORS. Approve?"                        │
│                                                                 │
│  8. Process continues until EXECUTION_PLAN grid ready           │
│     "All grids healthy. Ready to generate strategy document."   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 6: Grid Visualization Patterns

### Grid Health Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│                    GRID HEALTH DASHBOARD                        │
│  Moldova Media Strategy                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PHASE 1 - FOUNDATION                                           │
│  ├─ ACTOR         ████████████████░░░░  85% ✓ healthy          │
│  ├─ CONTEXT       ██████████████░░░░░░  72% ✓ healthy          │
│  └─ CONSTRAINT    ████████████████████  100% ✓ complete        │
│                                                                 │
│  PHASE 2 - ANALYTICAL                                           │
│  ├─ LOGICAL       █████████░░░░░░░░░░░  45% → in progress      │
│  ├─ CAUSAL        ████████░░░░░░░░░░░░  40% → in progress      │
│  └─ TEMPORAL      ██████████████░░░░░░  68% → needs attention  │
│                                                                 │
│  PHASE 3 - STRATEGIC                    [LOCKED]               │
│  ├─ SCENARIO      ░░░░░░░░░░░░░░░░░░░░  0%  🔒 blocked         │
│  ├─ THEORY_OF_CHANGE ░░░░░░░░░░░░░░░░░  5%  🔒 blocked         │
│  └─ COALITION     ░░░░░░░░░░░░░░░░░░░░  0%  🔒 blocked         │
│                                                                 │
│  PHASE 4 - SYNTHESIS                    [LOCKED]               │
│  └─ THROUGHLINE   ░░░░░░░░░░░░░░░░░░░░  0%  🔒 blocked         │
│                                                                 │
│  PHASE 5 - EXECUTION                    [LOCKED]               │
│  └─ EXECUTION_PLAN ░░░░░░░░░░░░░░░░░░░  0%  🔒 blocked         │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  NEXT ACTIONS:                                                  │
│  1. Complete LOGICAL grid questions (5 remaining)               │
│  2. Review evidence batch for TEMPORAL grid (12 pending)        │
│  3. Resolve tension in CAUSAL grid: "media regulation timing"   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Individual Grid View

```
┌─────────────────────────────────────────────────────────────────┐
│  ACTOR GRID                                      Health: 85%    │
│  Moldova Media Strategy                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [Domestic Media] [International] [Government] [Civil Society]  │
│                                                                 │
│  ┌─ Domestic Media Actors ──────────────────────────────────┐  │
│  │                                                          │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │  │
│  │  │ TV8         │  │ Ziarul de   │  │ NewsMaker   │      │  │
│  │  │ Position:   │  │ Gardă       │  │ Position:   │      │  │
│  │  │ Independent │  │ Position:   │  │ Pro-EU      │      │  │
│  │  │ Capability: │  │ Investigative│ │ Capability: │      │  │
│  │  │ HIGH        │  │ Capability: │  │ MODERATE    │      │  │
│  │  │ Conf: 92%   │  │ HIGH        │  │ Conf: 78%   │      │  │
│  │  └─────────────┘  │ Conf: 95%   │  └─────────────┘      │  │
│  │                   └─────────────┘                        │  │
│  │                                                          │  │
│  │  Relationships:                                          │  │
│  │  TV8 ←──ALLIES_WITH──→ Ziarul de Gardă                  │  │
│  │  NewsMaker ←──COMPETES_WITH──→ TV8                      │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Gaps Detected:                                                 │
│  ⚠️ Russian-language media actors not mapped (3 cells empty)   │
│  ⚠️ Regional media representation low (2 cells, low confidence) │
│                                                                 │
│  [Add Actor] [Import from Evidence] [View Relationships]        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 7: Domain-Specific Grid Sets

### Theory/Essay Domain

**Default Grid Set:**
1. LOGICAL (argument structure)
2. EVIDENTIAL (supporting evidence)
3. GENEALOGICAL (conceptual lineage)
4. DIMENSIONAL (12 philosophical signals)
5. FUNCTIONAL (rhetorical roles)
6. THROUGHLINE (thesis threads)
7. DIALECTICAL (tensions and syntheses)

### Foundation Strategy Domain

**Default Grid Set:**
1. ACTOR (stakeholders)
2. CONTEXT (situation analysis)
3. THEORY_OF_CHANGE (intervention logic)
4. SCENARIO (future possibilities)
5. INSTRUMENT (tools and mechanisms)
6. TEMPORAL (sequencing)
7. RESOURCE (funding and capacity)
8. COALITION (alliances)
9. EXIT_CONDITION (sustainability)
10. LEARNING_AGENDA (what we'll discover)

### Brand Strategy Domain

**Default Grid Set:**
1. MARKET_CONTEXT (competitive landscape)
2. SEGMENT (audience slices)
3. POSITIONING (competitive space)
4. NARRATIVE_ARC (brand story)
5. ATTRIBUTE (brand characteristics)
6. TOUCHPOINT (interaction points)
7. COMPETITOR_RESPONSE (likely reactions)

### Government Planning Domain

**Default Grid Set:**
1. CONTEXT (national/regional situation)
2. ACTOR (political players)
3. STYLE (Varsavsky development style)
4. OBJECTIVE (goals hierarchy)
5. INSTRUMENT (policy tools)
6. CAPACITY (state capabilities)
7. COALITION (political alliances)
8. TEMPORAL (implementation sequence)
9. SCENARIO (future paths)
10. MONITORING (indicators and feedback)

---

## Part 8: Implementation Architecture

### Data Model

```python
class Grid:
    id: str
    project_id: str
    grid_type: GridType  # LOGICAL, TEMPORAL, ACTOR, etc.
    phase: int  # 1-5 maturation phase
    cells: List[Cell]
    relationships: List[Relationship]
    saturation_criteria: SaturationCriteria
    health_metrics: HealthMetrics
    dependencies: List[GridDependency]
    status: GridStatus  # LOCKED, IN_PROGRESS, HEALTHY, COMPLETE

class Cell:
    id: str
    grid_id: str
    cell_type: str  # grid-specific types
    content: Optional[str]
    confidence: float
    evidence_ids: List[str]
    created_by: str  # "user" | "inference" | "evidence"
    version: int

class Relationship:
    id: str
    from_cell_id: str
    to_cell_id: str
    relationship_type: str  # grid-specific types
    confidence: float
    bidirectional: bool

class GridDependency:
    from_grid_id: str
    to_grid_id: str
    dependency_type: str  # "blocks" | "informs" | "validates"
    health_threshold: float  # required health to unblock
```

### Agent Orchestration

```python
class GridOrchestrator:
    def __init__(self, project):
        self.project = project
        self.grid_generator = GridGeneratorAgent()
        self.gap_filler = GapFillerAgent()
        self.refactorer = GridRefactorerAgent()

    async def run_cycle(self):
        # 1. Check if new grids needed
        new_grid_proposals = await self.refactorer.detect_new_grid_needs(
            self.project.grids,
            self.project.evidence_corpus
        )

        # 2. Check for refactoring opportunities
        refactor_proposals = await self.refactorer.detect_refactoring_needs(
            self.project.grids
        )

        # 3. Present proposals to user (if any)
        if new_grid_proposals or refactor_proposals:
            await self.present_proposals(new_grid_proposals, refactor_proposals)

        # 4. Identify highest-priority gaps
        gaps = await self.gap_filler.detect_all_gaps(self.project.grids)
        prioritized = self.gap_filler.prioritize_gaps(gaps)

        # 5. Determine fill strategy for top gaps
        for gap in prioritized[:5]:
            fill_strategy = await self.gap_filler.determine_fill_strategy(gap)

            if fill_strategy.type == "EVIDENCE":
                await self.commission_research(fill_strategy.queries)
            elif fill_strategy.type == "USER_QUESTION":
                await self.present_question(fill_strategy.question)
            elif fill_strategy.type == "OPTION_GENERATION":
                await self.present_options(fill_strategy.options)

        # 6. Update health metrics
        for grid in self.project.grids:
            grid.health_metrics = GridHealth(grid).calculate()

        # 7. Check phase unlocks
        await self.check_phase_transitions()
```

---

## Part 9: Principles Extracted

### New Principles for Multi-Grid Architecture

| Principle ID | Statement |
|--------------|-----------|
| `prn_generative_grid_architecture` | Analytical structures (grids) should be generated dynamically based on domain, genre, and project-specific needs, not fixed a priori |
| `prn_multi_lens_reality_slicing` | Complex strategic problems benefit from simultaneous analysis through multiple analytical lenses (grids), each capturing different dimensions |
| `prn_grid_maturation_gating` | Later-phase grids (synthesis, execution) should be blocked until foundational grids reach health thresholds |
| `prn_cross_grid_tension_detection` | Tensions should be detected not just within grids but across grids, flagging when different lenses produce incompatible conclusions |
| `prn_grid_health_as_execution_prerequisite` | Execution/action should be gated by aggregate grid health, ensuring all analytical dimensions are robust |
| `prn_specialized_agent_per_function` | Grid generation, gap filling, and refactoring should be handled by specialized agents with distinct prompting strategies |
| `prn_grid_dependency_propagation` | Changes in foundational grids should trigger review of dependent grids, with affected cells flagged for re-validation |
| `prn_user_grid_agency` | Users should be able to propose new grids, reject suggested grids, and override gating rules (with acknowledgment) |

---

## Appendix A: Grid Type Definitions

[Detailed schemas for each grid type...]

## Appendix B: Prompting Templates

[Templates for Grid Generator, Gap Filler, Refactorer agents...]

## Appendix C: Relationship to Prior Documents

This document supersedes the fixed-slot architecture in:
- `strategy-workflow-enhancement-memo.md` (slot architecture → grid architecture)
- `ABSTRACT-STRATEGIZER-NOTES.md` Part 6 (unified framework → multi-grid framework)

Prior innovations retained:
- All 12 philosophical signals (as DIMENSIONAL grid)
- Varsavsky development styles (as STYLE grid)
- Shackle uncertainty (as SCENARIO grid enhancement)
- Evidence integration (applies to all grids)
- Tension detection (applies across grids)
- Refactoring dashboard (now grid-level, not just throughline-level)
- Commitment/foreclosure (applies to grid decisions)

---

*End of Document*
