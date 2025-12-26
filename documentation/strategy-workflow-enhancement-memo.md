# Memo: Enhancing the Multi-Domain Strategizer with Essay-Flow Patterns

*December 26, 2025*

---

## Executive Summary

This memo proposes enhancements to the 4-domain strategizer framework (Theory/Essay, Foundation, Brand, Government) by transplanting battle-tested patterns from the essay-flow system. The core insight: **essay-flow has solved the problem of advancing complex intellectual work through stages while maintaining coherence, detecting gaps, and preserving optionality**. These same patterns can power strategic workflows across all four domains.

---

## Part 1: The Essay-Flow Architecture

### What Essay-Flow Already Solves

The essay-flow system (essay_flow_v3.py, ~19,000 lines) implements a 7-stage workflow for essay construction:

```
Stage 1: QUESTIONNAIRE
    ↓
Stage 2: STRATEGIC ITEMS V1 (initial generation)
    ↓
Stage 3: STAGED INTERROGATION (refinement questions)
    ↓
Stage 4: STRATEGIC ITEMS V2 (refined items)
    ↓
Stage 5: THROUGHLINES (cross-slot synthesis)
    ↓
Stage 6: STRATEGIC ITEMS V3 (throughline-aware revision)
    ↓
Stage 7: SKELETON REFINEMENT (final structure)
```

### Key Architectural Patterns

#### 1. Functional Slot Architecture
**Principle:** `prn_trajectory_over_identity` + `prn_genre_as_scaffold`

Essay-flow uses 8 fixed functional slots that define *what kinds of content* an essay needs:

| Slot | Function |
|------|----------|
| PHENOMENON | What you're examining |
| DEFINITION | How you're defining key terms |
| ILLUSTRATION | Concrete examples |
| HISTORY | Historical context |
| DIAGNOSIS | Root cause analysis |
| IMPLICATION | What follows from your analysis |
| INTERVENTION | What should be done |
| OBJECTION | Counter-arguments addressed |

**The key insight:** Slots are *functional positions*, not content. The same slot type appears in different sections with different content. This creates a scaffolded approach where the system knows *what it's missing* before it knows *what should fill the gap*.

#### 2. Strategic Items with Versioning
**Principle:** `prn_refinement_versioning` + `prn_upstream_regeneration_from_downstream`

Items progress through versions (V1 → V2 → V3) with explicit change tracking:

```json
{
  "item_id": "item_001",
  "version": 2,
  "status": "refined|merged|split|new|unchanged",
  "change_rationale": "why this changed from V1",
  "source_items": ["item_001_v1"],  // provenance
  "slot_type": "DIAGNOSIS",
  "content": "..."
}
```

This allows the system to track *how* understanding evolves, not just *what* the current understanding is.

#### 3. Staged Adaptive Interrogation
**Principle:** `prn_staged_adaptive_interrogation`

Each refinement stage asks questions *conditioned on* answers from previous stages:

```
STAGE N: Generate questions based on current state
     ↓
USER: Answers questions
     ↓
STAGE N+1: New questions incorporate N's answers
     ↓
...continues until saturation
```

The system tracks dependencies between questions and knows which answers unlocked which follow-ups.

#### 4. Throughline Generation (Cross-Slot Synthesis)
**Principle:** `prn_cross_slot_synthesis_scanning` + `prn_shared_scaffold_parallel_streams`

Throughlines are arguments that *span multiple slots*. The throughline factory:

1. Scans across all filled slots
2. Identifies potential connections
3. Generates "slot articulations" (how each slot contributes to the throughline)
4. Proposes "bridging strategies" (how to move between slots)
5. Surfaces "interrelation hints" (unexpected connections)

```json
{
  "throughline_id": "tl_001",
  "central_claim": "The core argument",
  "slot_articulations": {
    "PHENOMENON": "How the phenomenon section serves this throughline",
    "DIAGNOSIS": "How diagnosis section serves this throughline",
    ...
  },
  "bridging_strategies": [
    "How to transition from PHENOMENON to DIAGNOSIS"
  ],
  "interrelation_hints": [
    "Unexpected connection between HISTORY and IMPLICATION"
  ]
}
```

#### 5. Slot Saturation Detection
**Principle:** `prn_gap_aware_processing` + `prn_adaptive_termination`

The system detects when slots have "enough" content and when gaps remain:

- **Saturation signals:** Slot has multiple items, items have high confidence, no unresolved tensions
- **Gap signals:** Slot empty or sparse, items flagged low-confidence, unaddressed objections

This drives the "when to stop refining" decision.

#### 6. Evidence Integration Pipeline (Stage 8)
**Principle:** `prn_evidence_as_idea_vector` + `prn_confidence_based_routing`

The Evidence stage is one of essay-flow's most sophisticated features. External evidence (PDFs, articles, quotes) is analyzed for how it relates to the functional skeleton:

**Evidence Relationship Types (Idea Vectors):**
| Type | Function |
|------|----------|
| ILLUSTRATES | Concrete example that makes abstract vivid |
| DEEPENS | Adds nuance or complexity to existing claim |
| CHALLENGES | Contradicts a premise, requires revision |
| LIMITS | Establishes scope boundary |
| BRIDGES | Connects previously unlinked elements |
| INVERTS | Flips an assumed relationship |

**Dual-Track Processing:**
```
Evidence Fragment Analyzed
         │
         ├─── High Confidence (≥85%) + Non-conflicting
         │         │
         │         └─→ AUTO-INTEGRATED
         │              • Clusters created automatically
         │              • "Reject" option moves to manual review
         │              • Slot mappings shown (e.g., "5 slots across 2 throughlines")
         │              • Key datapoints extracted with timestamps
         │
         └─── Low Confidence OR Ambiguous OR Conflicting
                   │
                   └─→ PENDING DECISIONS
                        • Grouped into trend clusters
                        • Multiple resolution paths generated
                        • Requires human decision
```

**Skeleton Restructuring Suggestions:**
The system proactively suggests structural changes:
- **"new throughline" (strongly recommended)** — Evidence pattern doesn't fit existing throughlines
- **"gap detected" (recommended)** — Evidence reveals missing dimension
- **"reconsider" alert** — Auto-integrated evidence may undermine existing claim

#### 7. Multi-Path Pending Decisions
**Principle:** `prn_possibility_as_foreclosure_warning` + `prn_commitment_articulation`

When evidence is ambiguous, the system generates multiple resolution paths:

```
┌─────────────────────────────────────────────────────────────────┐
│  TREND CLUSTER: "Public Sentiment Inversion"         86% conf  │
│  53 new │ 30 mod │ 0 del │ 11 clusters                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [🤖 AI pick] [A] Public Re... +2 -1 82%                       │
│               [B] Elite-Publ... +2 -1 84%                       │
│               [C] Labor Incom... +2 79%                        │
│               [D] Pre-Lock-In... -2 85%                        │
│                                                                 │
│  PATH A: "Public Resistance Constraint"                         │
│  → Infrastructure Succession: How AI Becomes New Foundation...  │
│                                                                 │
│  ┌─ PATH A COMMITS YOU TO: ─────────────────────────────────┐  │
│  │ "Infrastructure transition windows create temporal        │  │
│  │  asymmetries where public sentiment crystallizes before   │  │
│  │  deployment lock-in occurs..."                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─ A OVER B: YOU'RE PASSING ON: ───────────────────────────┐  │
│  │ "Hegemonic infrastructure operates through 'technological │  │
│  │  inevitability mythology'—the process by which..."        │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─ A OVER C: YOU'RE PASSING ON: ───────────────────────────┐  │
│  │ "Infrastructure transitions face structural brittleness   │  │
│  │  when their 'optimistic scenarios' require eliminating..."│  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Operations if A selected:                                      │
│  ├─ [ADD] COMPLICATION: Infrastructure transition windows...   │
│  ├─ [MOD] PHENOMENON: FROM: "Hegemonic infrastructure..."      │
│  │                    TO: "Hegemonic infrastructure..."        │
│  └─ [ADD] COMPLICATION: Technological incomprehensibility...   │
│                                                                 │
│                                     [Skip] [Accept]            │
└─────────────────────────────────────────────────────────────────┘
```

**Key Features:**
- **Trend Clustering:** Similar evidence fragments grouped for batch decisions
- **Path Metrics:** Each path shows +N additions, -N deletions, confidence %
- **AI Pick Indicator:** System recommendation highlighted
- **Commitment Statements:** What you're committing to by choosing this path
- **Foreclosure Statements:** What you're giving up relative to each alternative
- **Operation Preview:** Specific ADD/MOD/DEL changes shown per path

#### 8. Post-Evidence Tension Resolution (Follow-ups II)
**Principle:** `prn_tension_detection_after_integration` + `prn_commitment_tracking`

After evidence integration, a dedicated stage detects and resolves tensions:

```
┌─────────────────────────────────────────────────────────────────┐
│  Stage 9: Follow-ups II                                         │
│  "Last chance to refine functional skeleton before finalizing"  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Skeleton Completion Status                              49%    │
│  ════════════════════════════════════════════════════════      │
│                                                                 │
│  8 Tensions    5 Tensions     42 Slots      24 Slots           │
│  Detected      Resolved       Need Work     Complete           │
│                                                                 │
│  [Tension Resolution] [Slot Completion] [Skeleton Preview]      │
│                                                                 │
│  ┌─ Detected Tensions ──────────────────────────────────────┐  │
│  │                                                          │  │
│  │  ⚡ Contradiction                    [RESOLVED] [critical]│  │
│  │                                                          │  │
│  │  Sovereignty Theater vs Demonstrated Technical Capability │  │
│  │                                                          │  │
│  │  Throughline 48 (Sovereignty Theater) implies AI         │  │
│  │  independence is primarily ideological performance, but  │  │
│  │  substantial evidence shows China achieving genuine      │  │
│  │  technical alternatives: ASICs gaining market share      │  │
│  │  (17% to 55%), domestic chips 'comparable to' Nvidia's   │  │
│  │  restricted products...                                  │  │
│  │                                                          │  │
│  │  The skeleton needs to resolve whether sovereignty       │  │
│  │  claims are primarily performative OR substantive...     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Session Commitments                Quick Actions               │
│  ├─ ✓ Reframed throughline focus   ├─ [Detect Tensions]        │
│  │                                  ├─ [Assess Slot Quality]    │
│  │                                  ├─ [Refactoring Dashboard]  │
│  │                                  └─ [Proceed to Stage 10]    │
└─────────────────────────────────────────────────────────────────┘
```

**Tension Types:**
- **Contradiction:** Two elements make incompatible claims
- **Inconsistency:** Elements don't align but aren't directly opposed
- **Weak Content:** Slot has content but below quality threshold

**Session Commitments:** Tracks decisions made during the session for audit trail.

#### 9. Refactoring Dashboard
**Principle:** `prn_structural_operations_as_first_class` + `prn_seed_management`

A dedicated interface for structural changes to the skeleton:

```
┌─────────────────────────────────────────────────────────────────┐
│  Refactoring Dashboard                                          │
│  "Manage structural changes to throughlines"                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  14 Confirmed     0 Pending      43 Seeds       5 Throughlines │
│  Operations       /Previewing    Affected                       │
│                                                                 │
│  Functional Skeleton [21 slots]                            ▼   │
│                                                                 │
│  [+ Create New] [Split] [Merge] [Clone] [Reframe]              │
│  [Bulk Move Seeds] [Orphan Seeds] [Strategic Advisor]           │
│                                                                 │
│  ┌─ Refactoring Operations ─────────────────────────────────┐  │
│  │                                                          │  │
│  │  [REFRAME] Sovereignty Theater: How Elites...  confirmed │  │
│  │  [REFRAME] Infrastructure Succession: How AI... confirmed │  │
│  │  [SPLIT]   Hegemonic Complexity T... → 28 seeds  confirmed│  │
│  │  [REFRAME] The Complexity Trap: How AI...       confirmed │  │
│  │  [CUT]     Deleted throughline: Clone Test      confirmed │  │
│  │  [BULK MOVE] 6 seeds: Hegemonic → Petrodollar   confirmed │  │
│  │  [MERGE]   Into: Infrastructure Succession...   confirmed │  │
│  │  [SPLIT]   The Material Ceiling... → 15 seeds   confirmed │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─ Current Seed Mappings ──────────────────────────────────┐  │
│  │  Sovereignty Theater: How Elites...      20 seeds    ✕   │  │
│  │  The Elite Bargain: Collaborative...     21 seeds    ✕   │  │
│  │  Infrastructure Succession: How...       18 seeds    ✕   │  │
│  │  Complexity Lock-In: How Techni...       12 seeds    ✕   │  │
│  │  Weaponization Brittleness: How...       18 seeds    ✕   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**Refactoring Operations:**
| Operation | Description |
|-----------|-------------|
| **SPLIT** | Divide one throughline into multiple, redistributing seeds |
| **MERGE** | Combine throughlines, consolidating seeds |
| **CLONE** | Duplicate a throughline for experimental variation |
| **REFRAME** | Change the framing without changing the seeds |
| **BULK MOVE** | Move multiple seeds from one throughline to another |
| **CUT** | Delete a throughline (seeds become orphaned) |
| **+ Create New** | Add a throughline from scratch |

**Seed Management:**
- Seeds are the atomic content units mapped to throughlines
- **Orphan Seeds:** Seeds not mapped to any throughline (need rehoming)
- **Seed Mappings Panel:** Shows distribution across throughlines

**Strategic Advisor Modal:**
AI-powered analysis with focus areas:
- **Overlaps:** Throughlines covering same ground
- **Gaps:** Missing coverage areas
- **Cleanup:** Redundant or weak elements
- **Restructure:** Major architectural improvements

---

## Part 2: Transplanting to the Strategizer

### The Translation Table

| Essay-Flow Construct | Theory Domain | Foundation Domain | Brand Domain | Government Domain |
|---------------------|---------------|-------------------|--------------|-------------------|
| **Functional Slots** | Essay sections (Phenomenon, Diagnosis, etc.) | Strategy sections (Context, Theory of Change, etc.) | Strategy sections (Brand Position, etc.) | Plan sections (Context, Objectives, etc.) |
| **Strategic Items / Seeds** | Arguments, claims, evidence | Plays, interventions, evidence | Positions, initiatives, evidence | Policies, programs, evidence |
| **Throughlines** | Thesis lines | Theories of change | Brand narratives | Development doctrines |
| **Evidence Integration** | Academic sources, primary texts | Field reports, grantee data, news | Consumer research, market data | Statistics, comparable cases, expert analysis |
| **Pending Decisions** | "Which interpretation of this source?" | "Which theory of change does this support?" | "Which brand position does this validate?" | "Which policy mechanism does this suggest?" |
| **Tension Detection** | "These claims contradict" | "This intervention conflicts with that assumption" | "This position undermines that narrative" | "This instrument conflicts with that objective" |
| **Refactoring** | Split/merge thesis lines | Split/merge theories of change | Split/merge brand narratives | Split/merge policy frameworks |

### NEW: Evidence-to-Strategy Translation

The Evidence stage is particularly powerful for strategic domains:

| Essay-Flow Evidence Pattern | Foundation Strategy | Brand Strategy | Government Planning |
|-----------------------------|---------------------|----------------|---------------------|
| **Auto-Integration (high confidence)** | Grantee report confirms theory of change | Consumer survey validates positioning | Policy evaluation confirms instrument effectiveness |
| **Pending Decision (ambiguous)** | Evidence supports multiple theories of change | Consumer insight could support different positions | Data suggests multiple policy paths |
| **New Throughline Suggested** | Evidence pattern doesn't fit existing strategies | Consumer behavior suggests new market segment | Data reveals unaddressed development dimension |
| **Gap Detected** | Evidence reveals blind spot in strategy | Consumer research shows missing brand attribute | Statistics reveal unaddressed population segment |
| **Contradiction Detected** | Grantee outcomes contradict assumptions | Consumer behavior contradicts brand promise | Policy outcomes contradict stated objectives |

### NEW: Refactoring Operations Translation

| Refactoring Operation | Foundation Strategy | Brand Strategy | Government Planning |
|-----------------------|---------------------|----------------|---------------------|
| **SPLIT** | Split one theory of change into multiple targeted strategies | Split one brand narrative into segment-specific stories | Split one policy into targeted instruments |
| **MERGE** | Consolidate overlapping interventions | Merge redundant brand messages | Consolidate fragmented policies |
| **REFRAME** | Adjust framing without changing interventions | Reposition without changing product | Reframe objectives without changing instruments |
| **BULK MOVE** | Move plays from one strategy to another | Move initiatives between brand pillars | Move programs between policy areas |
| **CLONE** | Test alternative theory of change | A/B test brand narratives | Pilot alternative policy approaches |
| **CUT** | Sunset ineffective strategy | Retire brand message | Discontinue policy |
| **Orphan Seeds** | Plays not assigned to any strategy | Initiatives without clear brand home | Programs not aligned with any objective |

### Proposed: Universal Slot Architecture for Strategic Domains

Based on essay-flow's slot pattern, here are proposed functional slots for each domain:

#### Foundation Strategy Slots

| Slot | Function | Essay-Flow Analog |
|------|----------|-------------------|
| CONTEXT | Operating environment | PHENOMENON |
| DIAGNOSIS | Problem analysis | DIAGNOSIS |
| THEORY_OF_CHANGE | Causal mechanism | IMPLICATION |
| INTERVENTION | What we'll do | INTERVENTION |
| EVIDENCE | Support for claims | ILLUSTRATION |
| RISK | What could go wrong | OBJECTION |
| ACTOR_POSITION | Key player stances | (new) |
| EXIT_CONDITION | When/how to stop | (new) |

#### Brand Strategy Slots

| Slot | Function | Essay-Flow Analog |
|------|----------|-------------------|
| MARKET_CONTEXT | Competitive landscape | PHENOMENON |
| BRAND_DIAGNOSIS | Brand's current position | DIAGNOSIS |
| POSITIONING | Where we'll compete | DEFINITION |
| NARRATIVE | Story we tell | (maps to throughline) |
| EVIDENCE | Consumer insights, data | ILLUSTRATION |
| COMPETITIVE_RESPONSE | How rivals will react | OBJECTION |
| IMPLEMENTATION | Tactical execution | INTERVENTION |

#### Government Planning Slots

| Slot | Function | Essay-Flow Analog |
|------|----------|-------------------|
| CONTEXT | National/regional situation | PHENOMENON |
| DEVELOPMENT_DIAGNOSIS | Root causes of current state | DIAGNOSIS |
| DEVELOPMENT_STYLE | Overall approach (Varsavsky) | DEFINITION |
| OBJECTIVE | What we're trying to achieve | IMPLICATION |
| INSTRUMENT | Policy tools to deploy | INTERVENTION |
| EVIDENCE | Data, comparable cases | ILLUSTRATION |
| ACTOR_RESPONSE | How key actors will react | OBJECTION |
| SEQUENCING | Order of implementation | (new) |
| MONITORING | How we'll know if it's working | (new) |

---

## Part 3: The Staged Workflow Pattern

### The Full 11-Stage Architecture (Based on Essay-Flow)

Essay-flow uses an 11-stage workflow. Here's the complete pattern:

```
┌─────────────────────────────────────────────────────────────────┐
│          ESSAY-FLOW: COMPLETE 11-STAGE WORKFLOW                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Stage 0: THEORY BASE                                           │
│  └─ Establish philosophical framework, load doctrine            │
│                                                                 │
│  Stage 1: QUESTIONS                                             │
│  └─ Initial questionnaire, gather project parameters            │
│                                                                 │
│  Stage 2: SEEDS                                                 │
│  └─ Generate initial content units (arguments, claims)          │
│                                                                 │
│  Stage 3: FOLLOW-UPS (First Round)                              │
│  └─ Staged interrogation, refine seeds based on answers         │
│                                                                 │
│  Stage 4: EMERGING THEORY                                       │
│  └─ Synthesize patterns from seeds into proto-throughlines      │
│                                                                 │
│  Stage 5: THROUGHLINES                                          │
│  └─ Generate cross-slot throughlines with slot articulations    │
│                                                                 │
│  Stage 6: FUNCTIONAL SKELETON                                   │
│  └─ Map seeds to slots, assess coverage, identify gaps          │
│                                                                 │
│  Stage 7: REFINEMENT                                            │
│  └─ Fill gaps, strengthen weak slots, improve coherence         │
│                                                                 │
│  Stage 8: EVIDENCE ⭐ (Critical new capability)                 │
│  ├─ Upload external evidence (PDFs, articles, quotes)           │
│  ├─ Auto-integration for high-confidence evidence               │
│  ├─ Pending decisions for ambiguous evidence                    │
│  ├─ Batch processing for large evidence sets                    │
│  ├─ Theory testing against evidence (69 tests in example)       │
│  └─ Skeleton restructuring suggestions                          │
│                                                                 │
│  Stage 9: FOLLOW-UPS II ⭐ (Post-evidence)                      │
│  ├─ Tension detection (contradictions, inconsistencies)         │
│  ├─ Slot completion assessment                                  │
│  ├─ Refactoring dashboard access                                │
│  └─ Session commitment tracking                                 │
│                                                                 │
│  Stage 10: SKELETON V2                                          │
│  └─ Final structure after evidence integration and refactoring  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### General Pattern (All Domains) — Enhanced

```
┌─────────────────────────────────────────────────────────────────┐
│              STRATEGIZER: 11-STAGE WORKFLOW                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  STAGE 0: DOCTRINE BASE                                         │
│  ├─ Load domain-specific doctrine (plays, positions, frames)    │
│  ├─ Load interlocutor models (theoretical schools + actors)     │
│  └─ Output: Doctrine inventory, interlocutor gallery            │
│                                                                 │
│  STAGE 1: PROJECT BRIEF                                         │
│  ├─ User provides: Context, constraints, objectives             │
│  ├─ System infers: Relevant doctrine, applicable interlocutors  │
│  └─ Output: Project parameters, doctrine subset                 │
│                                                                 │
│  STAGE 2: SEEDS (Initial Units)                                 │
│  ├─ Generate initial strategic items (plays, positions, etc.)   │
│  ├─ Assign confidence levels, flag assumptions                  │
│  └─ Output: V1 seeds (sparse, assumed, low-confidence)          │
│                                                                 │
│  STAGE 3: INTERROGATION (Follow-ups I)                          │
│  ├─ Questions generated from current state                      │
│  ├─ Questions conditioned on prior answers                      │
│  ├─ Sharpener injects deeper probes while user answers          │
│  └─ Output: V2 seeds (richer, validated, higher-confidence)     │
│                                                                 │
│  STAGE 4: EMERGING STRUCTURE                                    │
│  ├─ Detect patterns across seeds                                │
│  ├─ Generate proto-throughlines (theories of change, etc.)      │
│  ├─ Surface potential tensions early                            │
│  └─ Output: Emerging structure preview                          │
│                                                                 │
│  STAGE 5: THROUGHLINES / DOCTRINES                              │
│  ├─ Generate cross-slot throughlines                            │
│  ├─ Slot articulations (how each slot serves the throughline)   │
│  ├─ Bridging strategies between slots                           │
│  └─ Output: Throughlines with full articulation                 │
│                                                                 │
│  STAGE 6: FUNCTIONAL SKELETON                                   │
│  ├─ Map seeds to slots                                          │
│  ├─ Assess slot saturation                                      │
│  ├─ Identify gaps, weak slots, orphan seeds                     │
│  └─ Output: Skeleton with coverage assessment                   │
│                                                                 │
│  STAGE 7: REFINEMENT                                            │
│  ├─ Fill identified gaps                                        │
│  ├─ Strengthen weak slots                                       │
│  ├─ Improve cross-slot coherence                                │
│  └─ Output: Refined skeleton V1                                 │
│                                                                 │
│  STAGE 8: EVIDENCE INTEGRATION ⭐                               │
│  ├─ Upload: Reports, data, articles, expert input               │
│  ├─ Auto-integrate high-confidence evidence                     │
│  ├─ Route ambiguous evidence to pending decisions               │
│  ├─ Generate commitment/foreclosure for each path               │
│  ├─ Batch process related evidence clusters                     │
│  ├─ Test theories against evidence corpus                       │
│  ├─ Suggest skeleton restructuring (new throughlines, gaps)     │
│  └─ Output: Evidence-informed skeleton, pending decisions       │
│                                                                 │
│  STAGE 9: POST-EVIDENCE RESOLUTION ⭐                           │
│  ├─ Detect tensions (contradictions, inconsistencies)           │
│  ├─ Assess slot completion (% complete, slots need work)        │
│  ├─ Resolve tensions with commitment/foreclosure framing        │
│  ├─ Access refactoring dashboard for structural changes         │
│  ├─ Track session commitments for audit trail                   │
│  └─ Output: Tension-resolved skeleton                           │
│                                                                 │
│  STAGE 10: FINAL ARTIFACT                                       │
│  ├─ Compile into domain-specific format                         │
│  ├─ Final coherence check                                       │
│  ├─ Flag remaining uncertainties as research agenda             │
│  └─ Output: Strategy document / Plan / Brand guide              │
│                                                                 │
│  STAGE 11: LEARNING CAPTURE                                     │
│  ├─ Identify generalizable insights                             │
│  ├─ Candidate new doctrine units (plays, positions, frames)     │
│  ├─ Update interlocutor models with observed responses          │
│  └─ Output: Doctrine updates, enhanced interlocutor models      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Stage Transitions: Saturation-Based

Borrowing from essay-flow's slot saturation detection:

```
STAGE N → STAGE N+1 when:
  ∀ slot ∈ required_slots:
    slot.item_count ≥ minimum_threshold
    AND slot.avg_confidence ≥ confidence_threshold
    AND slot.unresolved_tensions == 0 OR user_accepted_tensions
```

This makes stage transitions *evidence-based* rather than arbitrary.

---

## Part 4: Feature Transplants from Philosophy KB

### Priority 0: Critical New Capabilities (from Evidence & Follow-ups II)

| Feature | Source | Strategizer Application |
|---------|--------|------------------------|
| `evidence-dual-track-processing` | essay-flow | Route high-confidence evidence to auto-integration, ambiguous to pending decisions |
| `multi-path-pending-decisions` | essay-flow | Generate A/B/C/D paths with commitment/foreclosure articulation for each |
| `trend-clustering` | essay-flow | Group similar evidence fragments for batch decisions |
| `skeleton-restructuring-suggestions` | essay-flow | Proactively suggest new throughlines, gaps, reconsiderations |
| `post-evidence-tension-detection` | essay-flow | Detect contradictions and inconsistencies after evidence integration |
| `refactoring-dashboard` | essay-flow | Split/Merge/Clone/Reframe/Bulk Move structural operations |
| `strategic-advisor` | essay-flow | AI recommendations for Overlaps, Gaps, Cleanup, Restructure |
| `session-commitment-tracking` | essay-flow | Track decisions made during session for audit trail |
| `seed-management` | essay-flow | Orphan seeds, seed mappings, redistribution across throughlines |
| `theory-testing` | essay-flow | Test throughlines/theories against evidence corpus |

### Priority 1: Core Workflow Features

| Feature | Source | Strategizer Application |
|---------|--------|------------------------|
| `slot-saturation-detection` | essay-flow | Detect when strategic sections are adequately developed |
| `throughline-factory-pattern` | essay-flow | Generate theories of change / brand narratives / development doctrines |
| `answer-accumulating-question-batches` | essay-flow | Questions that build on prior answers during interrogation |
| `staged-adaptive-interrogation` | essay-flow | Multi-round questioning that adapts to current state |
| `llm-driven-diagnostic-questioning` | essay-flow | Generate probing questions based on detected gaps |
| `slot-articulation-generation` | essay-flow | For each throughline, generate how each slot serves it |

### Priority 2: Quality Enhancement

| Feature | Source | Strategizer Application |
|---------|--------|------------------------|
| `transformation-state-context-bundle` | essay-flow | When items change, carry full context of what/why |
| `staleness-detection-monitor-pattern` | essay-flow | Detect when actor models or scenarios are outdated |
| `distinctiveness-guard-provision` | asc | Ensure strategic items remain distinct from each other |
| `resolution-path-virtualization-panel` | asc | Show multiple paths for resolving detected tensions |
| `per-alternative-foreclosure-articulation` | asc | For each option, show what it forecloses |
| `idea-vector-typing` | essay-flow | Classify evidence as ILLUSTRATES, DEEPENS, CHALLENGES, LIMITS, BRIDGES, INVERTS |
| `auto-integration-with-reject-option` | essay-flow | Auto-integrate high-confidence evidence with manual override |

### Priority 3: Epistemic Infrastructure

| Feature | Source | Strategizer Application |
|---------|--------|------------------------|
| `seven-category-epistemic-gap-framework` | theory-service | Rich typology for categorizing gaps |
| `uncertainty-to-question-pipeline` | theory-service | Convert detected uncertainties into researchable questions |
| `confirm-then-route-interrogation-pattern` | theory-service | Confirm gap exists, then route to appropriate resolution |
| `agency-preserving-response-options` | theory-service | Present gaps without deficit framing |
| `commitment-statement-generation` | essay-flow | "PATH A COMMITS YOU TO: ..." |
| `foreclosure-articulation` | essay-flow | "A OVER B: YOU'RE PASSING ON: ..." |
| `operation-preview` | essay-flow | Show ADD/MOD/DEL changes before applying |

### Priority 4: Structural Operations

| Feature | Source | Strategizer Application |
|---------|--------|------------------------|
| `throughline-split` | essay-flow | Divide one throughline into multiple, redistributing seeds |
| `throughline-merge` | essay-flow | Combine throughlines, consolidating seeds |
| `throughline-clone` | essay-flow | Duplicate for experimental variation |
| `throughline-reframe` | essay-flow | Change framing without changing seeds |
| `bulk-seed-move` | essay-flow | Move multiple seeds between throughlines |
| `orphan-seed-management` | essay-flow | Handle seeds not mapped to any throughline |

---

## Part 5: Principle Applications

### Core Principles for Staged Advancement

| Principle | Statement | Strategizer Application |
|-----------|-----------|------------------------|
| `prn_staged_adaptive_interrogation` | Complex interrogation should proceed in sequential stages where each stage's questions are informed by prior answers | The foundation of the multi-stage workflow |
| `prn_upstream_regeneration_from_downstream` | When users make refinements at lower/later/more-concrete levels of a hierarchy, propagate those changes upstream | Actor feedback should update scenarios; tactical changes should update theory of change |
| `prn_gap_aware_processing` | Systems should identify what is missing relative to benchmarks | Systematic gap detection against slot requirements |
| `prn_cross_slot_synthesis_scanning` | Systems should include explicit mechanisms that scan across different slots to generate synthetic insights | Throughline/doctrine generation across filled slots |
| `prn_embodied_decision_substrate` | Consequential choices require pre-generation of sufficient concrete material | Generate concrete options before asking for decisions |
| `prn_possibility_as_foreclosure_warning` | Present multiple possibilities not merely as options for selection but as warnings about what each forecloses | Every strategic choice shows what it closes off |

### Principles for Epistemic Quality

| Principle | Statement | Strategizer Application |
|-----------|-----------|------------------------|
| `prn_epistemic_grounding_before_thesis_generation` | Gather information about the user's epistemic position and blind spots before generating theses | Early-stage interrogation before scenario generation |
| `prn_proactive_insufficiency_signaling` | LLMs should recognize when they have identified possibilities but lack sufficient information | System alerts when generating from thin evidence |
| `prn_verification_easier_than_generation` | LLMs are more reliable at verifying whether outputs match inputs than at generating from scratch | Use LLMs to validate actor responses against harvested materials |
| `prn_contrastive_context_enrichment` | Include not just what was chosen but what alternatives were considered and rejected | Track rejected scenarios, dismissed concerns, foreclosed options |

### Principles for Generative Work

| Principle | Statement | Strategizer Application |
|-----------|-----------|------------------------|
| `prn_emergent_choice` | Genuine choices are not given at the start but emerge through analytical work | Scenarios and options emerge from filled slots, not imposed |
| `prn_productive_incompletion` | Not all questions should be resolved—some should be deliberately converted to research agenda | Some gaps become ongoing monitoring, not immediate research |
| `prn_reformulation_before_rejection` | When elements fail to connect, explore whether reformulation enables integration | Before discarding a play/position, try reformulating it |

---

## Part 6: Domain-Specific Enhancements

### Theory/Essay Domain

**Current essay-flow patterns remain primary.** Enhancements:

1. **Interlocutor panel during drafting** — Surface likely critiques from modeled schools before finalizing
2. **Epistemic status on claims** — Every claim carries confidence level and evidence quality
3. **Scenario-aware writing** — Consider multiple reception scenarios while drafting

### Foundation Domain

**New patterns needed:**

1. **Play-Slot Mapping**
   - Each play (strategic pattern) should specify which slots it addresses
   - E.g., "Media Ecosystem Resilience" → primarily addresses INTERVENTION and THEORY_OF_CHANGE slots

2. **Actor-Conditional Scenarios**
   - Scenarios should fork based on actor responses
   - Generate scenario trees, not just lists

3. **Exit Condition Engineering**
   - Explicit EXIT_CONDITION slot
   - Each intervention must specify conditions for: continue, pivot, exit

4. **Tension-to-Play Pipeline**
   - When new tensions are named, system suggests relevant plays
   - When no play fits, system surfaces as generative opportunity

### Brand Domain

**New patterns needed:**

1. **Position-Narrative Coherence Check**
   - Positions must be expressible as narrative
   - If narrative doesn't flow, position needs refinement

2. **Competitive Response Simulation**
   - Before finalizing position, simulate competitor responses
   - Update position based on likely counter-moves

3. **Consumer Segment Interlocutors**
   - Model core customers, aspirational customers, critics as interlocutors
   - Query them on proposed positions before finalizing

4. **Brand Tension Saturation**
   - Track which brand tensions are addressed in current strategy
   - Flag unaddressed tensions as gaps

### Government Domain

**New patterns needed:**

1. **Instrument-Actor Compatibility Matrix**
   - Which instruments work with which actors?
   - Pre-compute coalition implications of instrument choices

2. **Varsavsky-Style Scenario Visualization**
   - Radar charts showing trade-off positions
   - Visual comparison of development styles

3. **Implementation Capacity Slot**
   - Explicit assessment of state capacity for each instrument
   - Flag instruments that exceed capacity

4. **Sequencing Dependencies**
   - Some instruments must precede others
   - System validates instrument sequences

---

## Part 7: The Research Commissioning Flow

Borrowing from essay-flow's gap detection and the Shackle framework:

```
┌─────────────────────────────────────────────────────────────────┐
│                    RESEARCH COMMISSIONING FLOW                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. GAP DETECTION (Automatic, continuous)                       │
│  ├─ Scan all slots for: missing items, low confidence,         │
│  │   outdated evidence, untested assumptions                    │
│  ├─ Scan all actor models for: low confidence, outdated,       │
│  │   missing for key decisions                                  │
│  ├─ Scan all scenarios for: unsupported assumptions,           │
│  │   missing kaleidic triggers                                  │
│  └─ Output: Prioritized gap inventory                          │
│                                                                 │
│  2. QUERY GENERATION                                            │
│  ├─ Convert gaps to plain-language research queries             │
│  ├─ Tag queries by: urgency, type (literature, actor, context) │
│  └─ Output: Research agenda                                     │
│                                                                 │
│  3. RESEARCH EXECUTION                                          │
│  ├─ Send queries to AI Research Service                         │
│  ├─ Service returns: findings, sources, confidence, follow-ups  │
│  └─ Output: Research results                                    │
│                                                                 │
│  4. INTEGRATION                                                 │
│  ├─ Update relevant units with new information                  │
│  ├─ Recalculate confidence levels                               │
│  ├─ Surface emergent actors, tensions, scenarios                │
│  ├─ Flag contradictions with existing items                     │
│  └─ Output: Updated strategic items, new items                  │
│                                                                 │
│  5. RE-EVALUATION                                               │
│  ├─ Re-run gap detection                                        │
│  ├─ Check if critical gaps resolved                             │
│  ├─ If not: generate follow-up queries                          │
│  └─ Output: Updated research agenda or proceed signal           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 8: Implementation Priorities

### Phase 1: Foundation (Months 1-2)

1. **Universal slot architecture** for all four domains
2. **Strategic item schema** with versioning and provenance
3. **Basic staged workflow** (Initial → Interrogation → Synthesis)
4. **Gap detection** against slot requirements

### Phase 2: Intelligence (Months 3-4)

5. **Throughline/doctrine generator** (cross-slot synthesis)
6. **Interlocutor modeling framework** (theoretical schools + strategic actors)
7. **Research commissioning pipeline**
8. **Staged interrogation** with question dependencies

### Phase 3: Sophistication (Months 5-6)

9. **Shackle framework integration** (surprise, cruciality, focus outcomes)
10. **Scenario trees** with actor-conditional branching
11. **Learning capture** and doctrine promotion
12. **Cross-domain borrowing** infrastructure

### Phase 4: Scale (Months 7+)

13. **Multi-project learning** (how Moldova informs Hungary)
14. **Interlocutor model training** from harvested materials
15. **Generative moment support** (coining new plays/positions/frames)
16. **Artifact format flexibility** (different output formats per domain)

---

## Part 9: Domain-Specific Evidence & Refactoring Workflows

### Foundation Strategy: Evidence Integration Example

**Scenario:** OSF Moldova strategy receives new grantee evaluation report

```
┌─────────────────────────────────────────────────────────────────┐
│  EVIDENCE UPLOADED: "2024 Moldova Media Resilience Evaluation"  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Evidence Impact Assessment (Auto-generated):                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ ⚠️ New evidence complicates "Media Sustainability"        │  │
│  │ theory of change. Evaluation shows independent outlets    │  │
│  │ achieved audience growth (+40%) but revenue remained      │  │
│  │ dependent on donor funding (92% external). This suggests  │  │
│  │ need for revised theory or new throughline.               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Skeleton Restructuring Suggestions:                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ [new throughline - strongly recommended]                  │  │
│  │ "Audience-Revenue Decoupling: How Independent Media       │  │
│  │  Builds Influence Without Financial Independence"         │  │
│  │                                                           │  │
│  │ [gap detected - recommended]                              │  │
│  │ Exit condition slot is empty. Evaluation data should      │  │
│  │ inform when OSF considers intervention "successful        │  │
│  │ enough" to exit.                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Pending Decisions (3):                                         │
│                                                                 │
│  CLUSTER: "Sustainability Model Revision"                       │
│  ├─ [A] Audience-First Model      +3 -1 78%    [AI pick]       │
│  ├─ [B] Hybrid Revenue Model      +2 -2 71%                    │
│  ├─ [C] Strategic Donor Dependence +1 -1 65%                   │
│  └─ [D] Infrastructure Pivot      +4 -3 62%                    │
│                                                                 │
│  PATH A COMMITS YOU TO:                                         │
│  "Media impact measured by audience reach and trust, not       │
│  financial independence. Exit conditions redefined around      │
│  audience metrics rather than revenue sustainability."         │
│                                                                 │
│  A OVER B: YOU'RE PASSING ON:                                   │
│  "Mixed funding model where commercial revenue supplements     │
│  donor funding. Would require different grantee selection."    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Brand Strategy: Tension Resolution Example

**Scenario:** Consumer research reveals contradiction in Gucci positioning

```
┌─────────────────────────────────────────────────────────────────┐
│  Stage 9: Post-Evidence Resolution                              │
│  Gucci Brand Strategy - Q1 2025                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Skeleton Completion Status                              67%    │
│  ════════════════════════════════════════════════════════      │
│                                                                 │
│  3 Tensions    1 Tensions     12 Slots      8 Slots            │
│  Detected      Resolved       Need Work     Complete           │
│                                                                 │
│  ┌─ Detected Tension ───────────────────────────────────────┐  │
│  │                                                          │  │
│  │  ⚡ Contradiction                         [critical]     │  │
│  │                                                          │  │
│  │  "Heritage Authenticity" vs "Youth Disruption"           │  │
│  │                                                          │  │
│  │  Brand Narrative 2 ("Heritage Authenticity") emphasizes  │  │
│  │  continuity with Italian craftsmanship tradition. But    │  │
│  │  consumer research shows Gen-Z consumers (45% of sales)  │  │
│  │  attracted to brand precisely for "disruption" and       │  │
│  │  "rule-breaking." These framings pull in opposite        │  │
│  │  directions.                                             │  │
│  │                                                          │  │
│  │  Resolution Options:                                     │  │
│  │  ├─ [A] Reframe heritage as "disruption tradition"       │  │
│  │  ├─ [B] Segment narratives by audience                   │  │
│  │  ├─ [C] Elevate disruption, downplay heritage            │  │
│  │  └─ [D] Create dialectical brand tension                 │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Refactoring Dashboard Access: [Refactoring Dashboard]          │
│  • Consider REFRAME on "Heritage Authenticity" throughline     │
│  • Consider MERGE if segmented narratives overlap              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Government Planning: Refactoring Dashboard Example

**Scenario:** Ghana Planning Office restructuring development strategy

```
┌─────────────────────────────────────────────────────────────────┐
│  Refactoring Dashboard                                          │
│  Ghana Development Strategy 2025-2030                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  8 Confirmed      2 Pending      67 Seeds       4 Doctrines    │
│  Operations       /Previewing    Affected                       │
│                                                                 │
│  Functional Skeleton [18 slots]                            ▼   │
│                                                                 │
│  [+ Create New] [Split] [Merge] [Clone] [Reframe]              │
│  [Bulk Move Seeds] [Orphan Seeds] [Strategic Advisor]           │
│                                                                 │
│  ┌─ Refactoring Operations ─────────────────────────────────┐  │
│  │                                                          │  │
│  │  [SPLIT] Industrial Policy → 23 seeds redistributed:     │  │
│  │          • "Digital Infrastructure First"  (12 seeds)    │  │
│  │          • "Traditional Industry Upgrade"  (11 seeds)    │  │
│  │                                                confirmed │  │
│  │                                                          │  │
│  │  [REFRAME] "Import Substitution" → "Strategic Autonomy"  │  │
│  │          Reframing without changing policy instruments   │  │
│  │                                                confirmed │  │
│  │                                                          │  │
│  │  [MERGE] "Agricultural Modernization" + "Food Security"  │  │
│  │          → "Integrated Food Systems"                     │  │
│  │                                                confirmed │  │
│  │                                                          │  │
│  │  [BULK MOVE] 8 seeds: "Export Promotion" →               │  │
│  │          "Regional Integration Doctrine"                 │  │
│  │                                                confirmed │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─ Current Seed Mappings ──────────────────────────────────┐  │
│  │  Digital Infrastructure First         12 seeds    ✕      │  │
│  │  Traditional Industry Upgrade         11 seeds    ✕      │  │
│  │  Integrated Food Systems              18 seeds    ✕      │  │
│  │  Strategic Autonomy                   14 seeds    ✕      │  │
│  │  Regional Integration Doctrine        12 seeds    ✕      │  │
│  │                                                          │  │
│  │  ⚠️ Orphan Seeds: 4 (need rehoming)                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─ Strategic Advisor ──────────────────────────────────────┐  │
│  │                                                          │  │
│  │  [Overlaps] [Gaps] [Cleanup] [Restructure]              │  │
│  │                                                          │  │
│  │  Recommended:                                            │  │
│  │  • GAP: No doctrine addresses climate adaptation        │  │
│  │  • OVERLAP: "Strategic Autonomy" and "Regional          │  │
│  │    Integration" share 6 similar seeds                    │  │
│  │  • CLEANUP: 4 orphan seeds from old "Export Promotion"  │  │
│  │    need explicit rehoming decision                       │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Theory Testing Across Domains

Essay-flow's "Theory Testing" (69 tests in example) can be adapted:

| Domain | What's Being Tested | Against What Evidence |
|--------|--------------------|-----------------------|
| **Theory/Essay** | Thesis claims | Academic sources, primary texts |
| **Foundation** | Theories of change | Grantee outcomes, evaluation reports, field data |
| **Brand** | Brand positioning claims | Consumer research, sales data, sentiment analysis |
| **Government** | Policy effectiveness assumptions | Statistics, pilot results, comparable cases |

**Theory Testing UI Pattern:**
```
┌─────────────────────────────────────────────────────────────────┐
│  Theory Testing                                    69 tests     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ✓ 42 claims supported by evidence                             │
│  ⚠️ 18 claims with mixed support (need attention)               │
│  ✗ 9 claims contradicted by evidence (critical)                │
│                                                                 │
│  Filter: [All] [Supported] [Mixed] [Contradicted]              │
│                                                                 │
│  ┌─ Contradicted Claims ────────────────────────────────────┐  │
│  │                                                          │  │
│  │  CLAIM: "Independent media outlets can achieve           │  │
│  │         financial sustainability within 5 years"         │  │
│  │                                                          │  │
│  │  EVIDENCE: 12 fragments from 3 sources                   │  │
│  │  • Evaluation 2024: 92% donor-dependent after 7 years   │  │
│  │  • Grantee report: Revenue down 15% YoY                  │  │
│  │  • Field visit notes: "No path to sustainability"        │  │
│  │                                                          │  │
│  │  CONFIDENCE: 87% claim is FALSE                          │  │
│  │                                                          │  │
│  │  [View Details] [Revise Claim] [Accept Contradiction]    │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 10: Open Questions for Further Development

1. **Slot customization**: Should users be able to add/remove slots, or are they fixed per domain?

2. **Cross-domain translation**: If a foundation learns a play, can it suggest analogous brand positions?

3. **Confidence calibration**: How do we validate that our confidence levels are accurate?

4. **Actor model updating**: When do actual responses update models? What's the feedback loop?

5. **Throughline competition**: When multiple throughlines are possible, how do we help choose?

6. **Research query prioritization**: When budget is limited, which gaps get researched first?

7. **Generative moment detection**: How does the system recognize when existing units don't fit?

8. **Doctrine versioning**: How do we track doctrine evolution over time?

---

## Appendix A: Essay-Flow Principles Most Relevant to Strategizer

These principles from the philosophy KB are most directly applicable:

```
prn_staged_adaptive_interrogation    → Multi-stage questioning
prn_upstream_regeneration_from_downstream → Bidirectional propagation
prn_gap_aware_processing            → Gap detection
prn_cross_slot_synthesis_scanning   → Throughline generation
prn_embodied_decision_substrate     → Concrete options before decisions
prn_possibility_as_foreclosure_warning → Show what choices foreclose
prn_epistemic_grounding_before_thesis_generation → Gather info before generating
prn_proactive_insufficiency_signaling → Flag when evidence is thin
prn_contrastive_context_enrichment  → Include rejected alternatives
prn_emergent_choice                 → Choices emerge from work
prn_productive_incompletion         → Some gaps become ongoing research
prn_reformulation_before_rejection  → Try reformulating before discarding
prn_friction_focused_attention_allocation → Focus human attention on friction
prn_change_impact_propagation       → Changes cascade through system
prn_automated_staleness_detection   → Detect outdated elements
prn_assumption_dependency_management → Track dependencies between assumptions
```

---

## Appendix B: Relationship to ABSTRACT-STRATEGIZER-NOTES.md

This memo builds on the 6-part framework documented in ABSTRACT-STRATEGIZER-NOTES.md:

| ABSTRACT-STRATEGIZER-NOTES Section | This Memo Enhancement |
|-----------------------------------|----------------------|
| **Part 1: Dimensional Mapping** | Translates dimensions to slot architecture |
| **Part 2: Generative Process** | Adds Stage 8 (Learning Capture) with doctrine promotion |
| **Part 3: Scenarios, Actors, Instruments** | Integrates as first-class slots within staged workflow |
| **Part 4: Ghana Example** | Template for Government Planning slot instantiation |
| **Part 5: Shackle & Epistemic** | Integrated into Stage 2 (Epistemic Grounding) and Stage 4 (Scenario Generation) |
| **Part 6: Unified Framework** | Now operationalized as 8-stage workflow with saturation-based transitions |

The key addition: **how to advance through stages** rather than just what the stages contain.

---

## Appendix C: Key Essay-Flow Code Patterns to Extract

From `essay_flow_v3.py`, these specific patterns should be extracted and generalized:

1. **`generate_stage_questions()`** — Generates questions conditioned on current state
2. **`detect_slot_saturation()`** — Checks if slots have enough content
3. **`generate_throughlines()`** — Cross-slot synthesis factory
4. **`version_item()`** — Creates new version with change tracking
5. **`propagate_downstream_changes()`** — Cascades changes through dependencies
6. **`detect_staleness()`** — Flags outdated items based on related changes

These can become shared infrastructure across all four domain implementations.

---

*End of Memo*
