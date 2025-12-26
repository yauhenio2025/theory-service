# Theory Service Features Log

This document tracks major features introduced to the Theory Service application.

---

## 2025-12-26: User Experience Philosophy & Part 2 Grid Revision (Architectural Revision)

**Branch:** `main`

### Description
Major revision to STRATEGIZER-IMPLEMENTATION-SPEC.md Part 2 (Multi-Grid Analytical Layer). Aligned with flexible unit system from Part 1, and fundamentally reconceived the user experience around "attention-only-on-friction" philosophy. The system now operates as a background speculation engine where grids are applied and filled automatically, with users only engaged when genuine framework tensions require human judgment.

### The Core Philosophy

**User attention is a scarce, depletable resource.** The system should:
1. Process in background (LLM analysis, grid application, literature fetching)
2. Auto-integrate high-confidence content without user attention
3. Surface only genuine friction that requires value judgment
4. Provide multiple resolution paths with commitment/foreclosure articulation

### Key Changes

**1. New Section 2.0: User Experience Philosophy**
- The Speculative Engine concept — framework emergence from three sources
- Three Sources of Framework Enrichment (LLM analysis, user questions, literature)
- Attention Economics Principle (smooth vs friction operations)
- Friction-Gated Surfacing with resolution paths UI mockup
- What Grids Mean for Users (insights that surface, not forms to fill)

**2. Section 2.1 Revised**
- Updated from "5 unit types" to "Three-Tier Unit System"
- Added "NOT something users actively interact with"
- Emphasized grids operate in background, surfacing only on friction

**3. Section 2.2 Flexible Grids Revised**
- Reorganized from fixed unit types (CONCEPT, DIALECTIC, SCENARIO, ACTOR, INSTRUMENT) to Universal unit families (concept, tension, agent)
- Added "When Applied" column showing background vs surface logic
- Added Domain-Specific units table referencing Part 5 Domain Registry
- Added EmergentGridAssignment schema for Tier 3 units

**4. Section 2.5 GridSelector Completely Rewritten**
- Renamed to "Grid Selection Logic (Background, Automatic)"
- New `auto_apply_grids()` method that applies AND fills grids automatically
- `_get_universal_type()` maps any unit to Universal family
- `_apply_and_fill_grid()` fills from LLM analysis + literature
- `_detect_grid_friction()` finds conflicts requiring user attention
- Added "What Users See vs What Happens" diagram

**5. Section 2.7 Example Completely Rewritten**
- Changed from step-by-step user-driven approach to background processing
- New Investor domain example (Alibaba domestic pivot thesis)
- Shows: What User Does (paste notes) → What Happens in Background (6 units, 24 grids, 3 papers) → What User Sees (only 2 friction decisions)
- Two full UI mockups for friction-resolution decisions with commitment/foreclosure
- "OLD vs NEW APPROACH" comparison diagram
- Key stat: "Total active work: ~5 minutes"

### Principles Extracted (Added to tool-ideator knowledge base)

- `prn_attention_scarcity_economics` — Treat user attention as depletable resource
- `prn_fit_friction_detection_as_routing` — Fit/friction determines automation vs human judgment
- `prn_resolution_path_multiplicity` — Present multiple resolution paths, not single recommendations
- `prn_speculative_engine_architecture` — Build speculation engines, not just analytical frameworks

### Features Extracted (Added to tool-ideator knowledge base)

- `friction-gated-user-engagement-pattern` — System processes until friction detected, then surfaces
- `emergent-conceptual-straightjacket-development` — Frameworks emerge from LLM processing, not imposed upfront
- `multi-source-framework-enrichment` — Three sources: LLM, user questions, literature
- `smooth-operation-background-processing` — Categorize as smooth (auto) vs friction (surface)

### Files Modified
- `documentation/STRATEGIZER-IMPLEMENTATION-SPEC.md` (Part 2: ~500 lines added/revised)
  - Section 2.0: New "User Experience Philosophy" (~150 lines)
  - Section 2.1: Updated references to Three-Tier Unit System
  - Section 2.2: Reorganized grid taxonomy (~60 lines revised)
  - Section 2.5: Complete rewrite of GridSelector (~200 lines)
  - Section 2.7: Complete rewrite of example (~200 lines)

### Relationship to Prior Documents
- **Part 1 revision** — Part 2 now aligned with flexible unit system
- **strategy-workflow-enhancement-memo.md** — Essay-flow patterns (refactoring dashboard, pending decisions) now foundational to grid friction surfacing

---

## 2025-12-26: Three-Tier Unit System & LLM-Powered Evolution (Architectural Revision)

**Branch:** `main`

### Description
Major architectural revision to STRATEGIZER-IMPLEMENTATION-SPEC.md Part 1. Applied the same flexibility philosophy from the Three-Tier Grid System to the unit types themselves. If grids can be Required → Flexible → Wildcard, why should unit types be fixed at exactly 5? This revision introduces dynamic unit type evolution powered by background LLM friction detection.

### The Problem
The original spec defined 5 fixed unit types (Concept, Dialectic, Scenario, Actor, Instrument). But:
1. Different domains need different vocabularies ("Thesis" vs "Frame" vs "Position")
2. Some domains might need more/fewer/different unit types
3. Users discover new unit types through use that don't fit the taxonomy
4. The grids had three-tier flexibility, but units were rigid

### The Solution: Three-Tier Unit System

| Tier | Name | Count | Description |
|------|------|-------|-------------|
| **Tier 1** | Universal | 3 | Every domain needs these: Concept, Tension, Agent |
| **Tier 2** | Domain | 4-8 | Configured per domain, can be renamed/hidden/merged/split |
| **Tier 3** | Emergent | 0-N | Discovered through friction detection, promotable to Tier 2 |

### Key Innovations

**1. Universal Units with Domain Aliases**
```python
class ConceptUnit:
    unit_type: str  # "concept" — the universal type
    display_type: str  # "Thesis" — the domain alias
    extensions: dict[str, Any]  # Domain-specific extensions
```

A "Concept" unit in Theory domain displays as "Thesis", in Brand domain as "Position", in Government domain as "Policy Frame", in Foundation domain as "Play", and in Investor domain as "Investment Thesis".

**2. 5th Domain: Investor**
Added Investor domain (hedge fund/VC working with investment hypotheses):
- **Tier 1 Aliases:** Thesis, Signal Tension, Market Actor
- **Tier 2 Units:** Signal, Catalyst, Comparable, Risk Factor, Valuation Driver, Trade Structure
- Enables testing investment hypotheses against market phenomena

**3. Unit Type Refactoring Operations**
Seven operation types for unit type evolution:
- **RENAME:** Change display name (Actor → Player)
- **HIDE:** Suppress unused type from this project
- **MERGE:** Combine two types (Response + Measure → Intervention)
- **SPLIT:** Divide type into subspecies (Risk → Tail Risk + Basis Risk)
- **PROMOTE:** Elevate emergent type to Tier 2
- **CREATE:** Add entirely new Tier 2 type
- **DEMOTE:** Move Tier 2 back to emergent for reconsideration

**4. LLM-Powered Background Evolution**
Friction detection runs in background, detecting:
- **OTHER_OVERUSE:** "Other" selected >30% in type dropdowns
- **CONTENT_MISMATCH:** Unit content doesn't match type schema
- **NAME_EDITING:** Users repeatedly edit display names
- **OVERLAP_CONFUSION:** Units frequently cross-referenced between types
- **BIMODAL_DISTRIBUTION:** Type has two distinct usage patterns
- **DISUSE:** Type rarely or never used
- **FORCED_FIT:** Long comments explaining why type doesn't quite fit

**5. Confidence-Based Routing**
- High confidence (≥0.85) + non-destructive → auto-apply with notification
- Medium confidence (0.5-0.85) → pending decisions with user review
- Low confidence (<0.5) → logged for pattern accumulation

**6. "Users Don't Need to Know" Principle**
Most users won't even know about unit type evolution. The LLM handles it in background:
- Detects when unit types don't fit reality
- Proposes refactoring operations
- Routes through Pending Decisions for ambiguous cases
- System adapts to how users actually work

### Integration with Essay-Flow Patterns
| Essay-Flow Pattern | Strategizer Application |
|--------------------|------------------------|
| Refactoring Dashboard | Unit Type Refactoring Dashboard |
| Pending Decisions | Type Operation Decisions |
| Commitment/Foreclosure | "Merging commits you to..." / "You're passing on..." |
| Evidence Dual-Track | Auto-apply vs Pending for type operations |
| Skeleton Restructuring | Unit type restructuring suggestions |

### Files Modified
- `documentation/STRATEGIZER-IMPLEMENTATION-SPEC.md` (Part 1: ~500 lines added/revised)
  - Section 1.1: Updated Layer 4 diagram to show THREE-TIER UNIT SYSTEM
  - Section 1.2: Added 5th domain (Investor), domain unit vocabulary tables
  - Section 1.3: Complete rewrite as "Three-Tier Unit System" with subsections for Universal, Domain, and Emergent units
  - Section 1.4: New "Unit Type Refactoring Operations" section
  - Section 1.5: New "LLM-Powered Background Evolution" section with friction detection, pending decisions UI mockups
  - Section 1.6: Renumbered from old 1.4 "How Units Interact"

### Principles Embodied
- `prn_tiered_analytical_scaffolding` - Now applies to units, not just grids
- `prn_validated_emergence_promotion` - Emergent unit types prove themselves through use
- `prn_confidence_based_routing` - Auto-apply vs pending decisions based on confidence
- `prn_possibility_as_foreclosure_warning` - Show what each type operation forecloses
- `prn_friction_driven_generation` - New unit types emerge from detected friction

### Relationship to Prior Documents
- **STRATEGIZER-IMPLEMENTATION-SPEC.md** — This revision extends the core spec
- **strategy-workflow-enhancement-memo.md** — Essay-flow patterns (refactoring dashboard, pending decisions) now applied to unit type evolution

---

## 2025-12-26: Comprehensive Strategizer Implementation Specification

**Branch:** `main`

### Description
Created the authoritative implementation specification document (`STRATEGIZER-IMPLEMENTATION-SPEC.md`) — a ~3,500 line comprehensive guide that synthesizes all prior architecture work into a single buildable specification. This document can be handed to a new session to implement the system.

### Document Structure (5 Parts)

**Part 1: Core Architecture**
- 6-Layer system stack (Artifact → Units → Multi-Grid → Shackle → Generative → Doctrine)
- 4 Domains (Theory/Essay, Foundation, Brand, Government)
- 5 Core Units with full Python schemas:
  - ConceptUnit (crystallized meaning)
  - DialecticUnit (productive tensions with poles)
  - ScenarioUnit (Varsavsky-style value-laden futures)
  - ActorUnit (entities with agency and response models)
  - InstrumentUnit (available tools for action)
- Unit interaction diagram

**Part 2: Multi-Grid Analytical Layer**
- Three-Tier Grid System:
  - Tier 1 (Required): LOGICAL, ACTOR, TEMPORAL
  - Tier 2 (Flexible): Domain-specific taxonomic grids
  - Tier 3 (Wildcard): LLM-invented analytical lenses with promotion logic
- GridInstance, SlotContent, CrossReference schemas
- Grid operations (apply, fill, cross-reference, propose wildcard)
- GridSelector and MultiGridView classes
- Complete worked example (Dual Circulation concept)

**Part 3: Epistemic Infrastructure (Shackle)**
- SurpriseProfile (alternative to probability)
- FocusGain/FocusLoss (what actually matters for decisions)
- CrucialityAssessment (reversibility, repeatability, transformation)
- KaleidicTrigger (events that reframe everything)
- EpistemicStatus with assumptions and gap tracking
- Research Commissioning pipeline:
  - GapDetector → ResearchCommission → ResearchExecutor → ResearchIntegrator
- Complete worked example (Moldova Services Hub scenario)

**Part 4: Generative Process**
- 6-stage pipeline: FRICTION → DIAGNOSIS → COIN → TEST → ABSTRACT → PROMOTE
- FrictionDetector (5 trigger types)
- Diagnoser with 15+ DiagnosisType categories
- UnitCoiner with Hegelian sublation for false dialectics
- UnitTester (interlocutor, edge case, consistency, usefulness testing)
- Abstractor and PromotionEvaluator
- Interlocutor Modeling:
  - InterlocutorModel schema (commitments, moves, objections)
  - InterlocutorSimulator (rule-based, LLM, hybrid)
  - Example interlocutors for Theory, Foundation, Government domains

**Part 5: Domain Instantiations & Implementation**
- Domain instantiation pattern (vocabulary mapping, seed doctrine, custom grids)
- Theory/Essay domain (full seed concepts, dialectics, interlocutors, custom grids)
- Foundation Strategy domain (Plays, Strategic Tensions, Strategic Players)
- Brand Strategy domain (Positions, Brand Tensions, Market Actors)
- Government Planning domain (Policy Frames, Development Trade-offs, Development Actors)
- 8-Phase Implementation Roadmap (18 weeks)
- Database schema (6 tables with full SQL)
- API endpoints (21 endpoints across 6 resource types)
- Success criteria (MVP vs Full System)
- Quick Reference appendix

### Key Design Decisions

1. **Multi-Grid as Layer 3 Only** — Grids are analytical lenses within units, not the whole system
2. **Shackle is Orthogonal** — Epistemic infrastructure applies to ALL units, not a grid type
3. **Three-Tier Promotion** — Wildcards prove themselves through use before joining taxonomy
4. **Friction-Driven Generation** — New units emerge from detected gaps, not arbitrary creation
5. **Interlocutor Testing** — All new units stress-tested against simulated actor responses
6. **Research Integration** — Gap detection triggers commissioning with human review gate

### Files Created
- `documentation/STRATEGIZER-IMPLEMENTATION-SPEC.md` (~3,500 lines, 5 parts)

### Relationship to Prior Documents
- **ABSTRACT-STRATEGIZER-NOTES.md** — Original vision; this spec implements that vision
- **unified-strategizer-architecture.md** — Reconciliation document; superseded by this spec
- **multi-grid-strategizer-architecture.md** — Grid exploration; incorporated as Part 2

---

## 2025-12-26: Unified Strategizer Architecture (Reconciliation)

**Branch:** `main`

### Description
Created reconciliation document that corrects the over-scoping of multi-grid architecture by restoring the full vision from ABSTRACT-STRATEGIZER-NOTES.md. Key insight: **multi-grids are one layer of a larger system, not the whole system.**

### The Problem
The multi-grid exploration collapsed rich architectural distinctions:
- 5 distinct unit types → became "grid types"
- Varsavsky's Scenarios → demoted to "SCENARIO grid"
- Shackle's Epistemic Infrastructure → demoted to "grid enhancement"
- Generative Process → lost entirely
- Interlocutor Modeling → barely mentioned

### The Corrected Architecture

**6 Layers:**

| Layer | What It Is | Role |
|-------|------------|------|
| Layer 5 | **Artifact** | Essay, Strategy Doc, Brand Plan, Development Plan |
| Layer 4 | **5 Core Units** | Concept, Dialectic, Scenario, Actor, Instrument |
| Layer 3 | **Multi-Grid Analysis** | Analytical lenses WITHIN each unit type |
| Layer 2 | **Epistemic Infrastructure** | Shackle (surprise, cruciality, triggers) |
| Layer 1 | **Generative Process** | Friction → Coin → Test → Abstract → Promote |
| Layer 0 | **Stable Doctrine** | Accumulated validated units |

**5 Core Units (Not Grid Types):**

| Unit | What It Captures | Example |
|------|------------------|---------|
| **Concept** | Crystallized meaning | "Media Ecosystem Resilience" — a new play |
| **Dialectic** | Productive tension | "Visibility ↔ Protection" — must navigate, not resolve |
| **Scenario** | Value-laden future path (Varsavsky) | "Industrial Champion" vs "Services Leapfrog" |
| **Actor** | Entity with agency | IMF, civil society, competitors |
| **Instrument** | Available action | Grant, regulate, reposition, tax |

**Where Multi-Grid Actually Lives:**
- Layer 3 — analytical lenses WITHIN each unit type
- CONCEPT units get analyzed via LOGICAL, FUNCTIONAL, THROUGHLINE grids
- ACTOR units get analyzed via INTEREST, CAPABILITY, COALITION grids
- SCENARIO units get analyzed via TEMPORAL, TRADE-OFF, BRANCHING grids

**What Was Restored:**
1. Varsavsky's Scenarios as a distinct unit type (value-laden, internally coherent futures)
2. Shackle as orthogonal concern (applies to ALL units, not a grid type)
3. The Generative Process (friction-based workflow for creating new units)
4. Interlocutor Modeling (response simulation from harvested materials)
5. Research Commissioning (gap detection → AI research → integration)
6. The Hegelian Move (sublation of dialectics into higher-order concepts)

### Files Created
- `documentation/unified-strategizer-architecture.md` (~600 lines)

### Relationship to Prior Documents
- **ABSTRACT-STRATEGIZER-NOTES.md** — The authoritative vision; this document is the ground truth
- **multi-grid-strategizer-architecture.md** — Now scoped to Layer 3 only; should be renamed to `analytical-grid-layer-architecture.md`
- **strategy-workflow-enhancement-memo.md** — Slot architecture patterns remain useful, translatable to unit+grid structure

---

## 2025-12-26: Multi-Grid Strategizer Architecture (Paradigm Shift)

**Branch:** `main`

### Description
Created a fundamentally new architecture document that shifts from fixed-slot to **generative multi-grid architecture**. The core innovation: there is no fixed grid. Instead, multiple analytical grids are generated dynamically based on domain, genre, and project-specific needs.

### Key Contributions

**1. The Multi-Grid Paradigm**
- No fixed slots - grids are emergent artifacts based on project needs
- Multiple simultaneous analytical lenses (logical, temporal, functional, etc.)
- Each grid has: cells, relationships, saturation criteria, health metrics

**2. Grid Type Taxonomy (10+ Types)**
| Type | Purpose |
|------|---------|
| LOGICAL | Map argument soundness |
| TEMPORAL | Map sequences and dependencies |
| FUNCTIONAL | Map rhetorical/functional roles |
| THROUGHLINE | Map argument threads |
| EVIDENTIAL | Map evidence relationships |
| ACTOR | Map stakeholder positions |
| SCENARIO | Map future possibilities |
| RESOURCE | Map resource flows |
| NORMATIVE | Map values and trade-offs |
| CAUSAL | Map causal mechanisms |

**3. Multi-Agent Architecture**
- **Grid Generator Agent:** Generates v0 of all grids from domain/genre/brief
- **Gap Filler Agent:** Populates grids via evidence, questions, option generation
- **Grid Refactorer Agent:** Proposes MERGE, SPLIT, NEW_GRID, CONSOLIDATE operations

**4. Grid Maturation Pipeline**
- Phase 1 (Foundation): ACTOR, CONTEXT, CONSTRAINT
- Phase 2 (Analytical): LOGICAL, CAUSAL, TEMPORAL - requires Phase 1 ≥70%
- Phase 3 (Strategic): SCENARIO, THEORY_OF_CHANGE - requires Phase 2 ≥70%
- Phase 4 (Synthesis): THROUGHLINE, NARRATIVE - requires Phase 3 ≥70%
- Phase 5 (Execution): EXECUTION_PLAN - requires Phase 4 ≥80%

**5. Grid Health Metrics**
Composite health = Saturation + Confidence + Coherence + Coverage + Tension count

**6. Gating Rules**
- Dependency Gating: Later grids READ-ONLY until foundational grids healthy
- Propagation Gating: Changes cascade through dependent grids
- Override with Acknowledgment: Users can override but must acknowledge

### Principles Extracted to tool-ideator (6 new principles)
- `prn_generative_analytical_structure` - Dynamic structure generation vs fixed
- `prn_multi_lens_analytical_coverage` - Multiple orthogonal analytical lenses
- `prn_maturation_gated_dependency` - Health thresholds gate dependent work
- `prn_function_specialized_agents` - Distinct agents for distinct cognitive functions
- `prn_cross_structure_tension_signaling` - Cross-grid tensions as valuable signals
- `prn_user_structural_agency` - User control over frame of analysis, not just content

### Features Extracted to tool-ideator (5 new features)
- `grid-type-taxonomy-as-lens-library`
- `multi-agent-function-decomposition`
- `phased-maturation-with-health-gating`
- `composite-health-metrics-with-override-acknowledgment`
- `grid-refactoring-operations-vocabulary`

### Files Created
- `documentation/multi-grid-strategizer-architecture.md` (~1100 lines)

---

## 2025-12-26: Three-Tier Grid System with Wildcard Mechanism (Refinement)

**Branch:** `main`

### Description
Refined the multi-grid architecture to distinguish between three tiers of analytical grids, balancing accumulated wisdom with emergent discovery.

### The Three Tiers

| Tier | Name | Description | Example |
|------|------|-------------|---------|
| **Tier 1** | Required | Always present, non-negotiable foundations | LOGICAL, ACTOR, TEMPORAL |
| **Tier 2** | Flexible | From learned taxonomy, recommended based on domain/genre | FUNCTIONAL, SCENARIO, CAUSAL, RESOURCE |
| **Tier 3** | Wildcard | LLM-invented for this specific project, genuinely novel | DIASPORA_INFLUENCE (Moldova example) |

### Key Mechanisms

**1. Required Grids (Tier 1)**
- LOGICAL: Every project needs sound argument structure
- ACTOR: Every project has stakeholders whose positions matter
- TEMPORAL: Everything unfolds in time with dependencies
- Cannot be removed by user; form irreducible foundation

**2. Flexible Grids (Tier 2)**
- Grid Generator recommends based on domain + genre + brief signals
- User can approve, reject, or defer
- Examples: FUNCTIONAL, THROUGHLINE, SCENARIO, CAUSAL, EVIDENTIAL, RESOURCE, NORMATIVE

**3. Wildcard Grids (Tier 3)**
- LLM proposes when it detects patterns not captured by existing grids
- Full proposal UI with rationale, cell types, relationship types
- User can Accept, Modify, Reject, or Merge into existing grid

**4. Wildcard-to-Taxonomy Promotion**
```python
def should_promote_to_taxonomy(self):
    return (
        self.usage_count >= 3 and
        len(self.projects_used_in) >= 2 and
        avg(self.user_ratings) >= 4.0
    )
```

### Principles Extracted to tool-ideator (3 new principles)
- `prn_tiered_analytical_scaffolding` - Required vs flexible vs emergent scaffolding
- `prn_emergent_analytical_lens_invention` - AI should invent novel lenses when needed
- `prn_validated_emergence_promotion` - Promote validated wildcards to taxonomy

### Features Extracted to tool-ideator (2 new features)
- `three-tier-grid-system` - The tiered approach to grid generation
- `wildcard-to-taxonomy-promotion` - Graduation mechanism for successful wildcards

### Files Modified
- `documentation/multi-grid-strategizer-architecture.md` - Added Part 1 Three-Tier System section

### Relationship to Prior Documents
This document **supersedes** the fixed-slot architecture in:
- `strategy-workflow-enhancement-memo.md` (slot architecture → grid architecture)
- `ABSTRACT-STRATEGIZER-NOTES.md` Part 6 (unified framework → multi-grid framework)

**Prior innovations retained** as grid types or grid enhancements:
- 12 philosophical signals → DIMENSIONAL grid
- Varsavsky development styles → STYLE grid
- Shackle uncertainty → SCENARIO grid enhancement
- Evidence integration → applies to all grids
- Refactoring dashboard → now grid-level operations

---

## 2025-12-26: Multi-Domain Strategizer Workflow Enhancement Memo (Major Expansion)

**Branch:** `main`

### Description
Created and substantially expanded comprehensive design memo for enhancing the 4-domain strategizer framework (Theory/Essay, Foundation, Brand, Government) by transplanting sophisticated patterns from the essay-flow system's Evidence and Follow-ups II stages.

### Key Contributions

**1. Full 11-Stage Workflow Architecture**
Documented the complete essay-flow 11-stage workflow and translated to strategizer:
- Stage 0: Doctrine Base → Stage 1: Project Brief → Stage 2: Seeds → Stage 3: Interrogation
- Stage 4: Emerging Structure → Stage 5: Throughlines → Stage 6: Functional Skeleton
- Stage 7: Refinement → **Stage 8: Evidence Integration** → **Stage 9: Post-Evidence Resolution**
- Stage 10: Final Artifact → Stage 11: Learning Capture

**2. Evidence Integration Pipeline (NEW - Critical)**
Documented essay-flow's sophisticated evidence handling:
- **Dual-track processing:** Auto-integration (≥85% confidence) vs Pending Decisions (ambiguous)
- **Idea vectors:** ILLUSTRATES, DEEPENS, CHALLENGES, LIMITS, BRIDGES, INVERTS
- **Skeleton restructuring suggestions:** "new throughline", "gap detected", "reconsider" alerts
- **Evidence Impact Assessment:** Auto-generated impact summaries

**3. Multi-Path Pending Decisions with Commitment/Foreclosure (NEW)**
- **Trend clustering:** Similar evidence grouped for batch decisions
- **A/B/C/D paths** with confidence scores and AI pick indicator
- **"PATH A COMMITS YOU TO:"** statements
- **"A OVER B: YOU'RE PASSING ON:"** foreclosure statements
- **Operation preview:** ADD/MOD/DEL changes shown before applying

**4. Post-Evidence Tension Resolution (NEW)**
- Tension detection: Contradictions, inconsistencies, weak content
- Slot completion metrics: "8 Tensions Detected, 5 Resolved, 42 Slots Need Work, 24 Complete"
- Session commitment tracking for audit trail
- Quick actions: Detect Tensions, Assess Slot Quality, Refactoring Dashboard

**5. Refactoring Dashboard (NEW)**
Full structural operations toolkit:
- **Operations:** SPLIT, MERGE, CLONE, REFRAME, BULK MOVE, CUT, + Create New
- **Seed management:** Orphan seeds, seed mappings, redistribution
- **Strategic Advisor:** AI recommendations for Overlaps, Gaps, Cleanup, Restructure

**6. Theory Testing (NEW)**
Testing throughlines/theories against evidence corpus with support/mixed/contradicted classification

**7. Domain-Specific Workflow Examples**
- **Foundation:** Moldova media strategy evidence integration with sustainability model revision
- **Brand:** Gucci heritage vs disruption tension resolution
- **Government:** Ghana planning office refactoring dashboard with doctrine restructuring

**8. Feature Transplant Priorities (Expanded)**
Now includes 30+ features in 5 priority tiers:
- Priority 0: Critical new capabilities (evidence dual-track, multi-path decisions, tension detection, refactoring dashboard)
- Priority 1: Core workflow features
- Priority 2: Quality enhancement
- Priority 3: Epistemic infrastructure
- Priority 4: Structural operations

### Files Modified
- `documentation/strategy-workflow-enhancement-memo.md` - Expanded from ~550 lines to ~1000+ lines

### Key Patterns Documented from Screenshots
Based on live essay-flow UI analysis:
1. Stage 8 Evidence with Auto-Integration Alerts and Skeleton Restructuring
2. Pending Decisions with trend clusters and multi-path selection
3. Commitment/Foreclosure articulation per path
4. Stage 9 Follow-ups II with tension resolution
5. Refactoring Dashboard with confirmed operations
6. Strategic Advisor modal for AI-powered recommendations

### Principles Embodied
- `prn_evidence_as_idea_vector` - Evidence classified by relationship type
- `prn_confidence_based_routing` - Dual-track based on confidence
- `prn_possibility_as_foreclosure_warning` - Show what each choice forecloses
- `prn_commitment_articulation` - Explicit commitment statements per path
- `prn_tension_detection_after_integration` - Post-evidence contradiction detection
- `prn_structural_operations_as_first_class` - Refactoring as first-class workflow
- `prn_session_commitment_tracking` - Audit trail of decisions

---

## 2025-12-25: Methodology Section Multiple-Choice with Escape Valve

**Commit:** `d630eb0`
**Branch:** `main`

### Description
Converted the methodology section (Stage 3) from requiring free-text typed answers to presenting pre-generated multiple-choice options with an "escape valve" for custom responses.

### The Problem
Stage 3 (Methodology/Grounding) previously required users to type long-form responses for questions about paradigmatic cases, recognition markers, core claims, and falsification conditions. This was:
1. High friction - requiring 100-150 character minimum typed responses
2. Cognitively demanding when the LLM already has rich context to infer likely answers
3. Inconsistent with the pattern established in other stages using multiple choice

### The Solution
Applied principles from the philosophy knowledge base to convert to a click-based interaction:

**Backend Changes (`api/concept_wizard.py`):**
- Modified `DYNAMIC_STAGE3_QUESTION_PROMPT` to generate multiple-choice questions
- LLM now generates 3-4 specific candidate answers based on accumulated context:
  - Notes summary
  - Stage 1 & 2 answers
  - Implications preview
  - Differentiation choices
- Each option has a label and detailed 2-3 sentence description
- Added `allow_custom_response: true` as escape valve

**Frontend Changes (`ConceptSetupWizard.jsx`):**
- Added `dynamicSectionUseCustom` state for tracking custom mode
- Added "None of these — write my own" option after multiple choice options
- Updated `hasDynamicAnswer()` to accept custom text input
- Updated `handleDynamicAnswerSubmit()` to handle custom responses with `is_custom` flag
- Updated `toggleDynamicOption()` to clear custom mode when selecting regular option

**CSS Changes (`index.css`):**
- Added styles for `.dynamic-custom-response` section
- Dashed border style for custom option
- Textarea styling for custom input area

### Principles Embodied
From the tool-ideator philosophy knowledge base:
- `prn_inferential_prepopulation` - System infers and prepopulates options based on accumulated context
- `prn_possibility_space` - Generate N structured options for user selection
- `prn_cognitive_load_transfer` - LLM does the heavy lifting, user validates/selects
- `multiple-choice-with-escape-valve-pattern` - Generate N options + "write your own" fallback
- `slot-completion-card-with-pre-generated-options` - Context-inferred completion options

### User Experience
Users now can:
1. Read 3-4 specific, context-aware options for each methodology question
2. Click to select the best-fitting option
3. OR click "None of these — write my own" and type custom answer
4. Add optional comment/qualification to any answer

This reduces typical Stage 3 completion time from ~5-7 minutes of typing to ~1-2 minutes of reading and clicking.

---

## 2025-12-22: 12-Dimensional Wizard Expansion (Kuhn, Foucault, Pragmatists)

**Commit:** `932864b`
**Branch:** `main`

### Description
Expanded the concept wizard from 9 to 12 dimensional signals by adding Kuhnian, Foucauldian, and Pragmatist philosophical traditions.

### New Dimensional Signals

| Signal | Key Extractions | Maps to Dimension |
|--------|----------------|-------------------|
| **kuhnian** | paradigm_position, exemplars, incommensurabilities, disciplinary_matrix | BOUNDARY |
| **foucauldian** | power_knowledge_nexus, governmentality_mode, subjectification_effects, discourse_formation | NORMALIZATION |
| **pragmatist** | cash_value, practical_consequences, performative_effects, habit_formations | AFFORDANCE |

### Key Concepts Extracted

**Kuhnian:**
- Paradigm position (normal_science → anomaly → crisis → revolutionary)
- Exemplars (paradigmatic cases that define proper use)
- Incommensurabilities (frameworks that cannot translate)
- Disciplinary matrix (shared symbolic generalizations, models, values)

**Foucauldian:**
- Power-knowledge nexus (what power enables what knowledge)
- Governmentality modes (discipline/security/sovereign/pastoral/neoliberal)
- Subjectification effects (what subjects the concept produces)
- Discourse formation (what statements become possible/impossible)

**Pragmatist:**
- Cash value (meaning in experiential terms)
- Practical consequences (what difference accepting this makes)
- Performative effects (what using the concept DOES)
- Habit formations (patterns of action enabled/blocked)

### Key Files
- `api/concept_wizard.py`: Updated all 4 prompt templates with new signals
- `api/wizard_to_schema_bridge.py`: Added processing for new signals

---

## 2025-12-22: Wizard to 8D Schema Bridge

**Commit:** `c106ead`
**Branch:** `main`

### Description
Created a bridge system that converts concept wizard outputs (hypothesis_cards, genealogy_cards, dimensional_signals, etc.) into the structured 8D concept analysis schema (AnalyzedConcept, ConceptAnalysis, AnalysisItem with provenance tracking).

### The Problem
The concept wizard and 8D schema were completely disconnected:
1. Wizard creates `Concept` records (from models.py)
2. 8D analysis uses `AnalyzedConcept` → `ConceptAnalysis` → `AnalysisItem` (from concept_analysis_models.py)
3. No automatic population of the 8D schema from wizard outputs
4. All the rich data (hypothesis_cards, genealogy_cards, dimensional_signals) was essentially lost

### The Solution

#### 1. New Bridge Module (`wizard_to_schema_bridge.py`)
Maps wizard outputs to 8D schema:
- `hypothesis_cards` → AnalysisItems in appropriate dimensions (thesis→POSITIONAL, assumption→PRESUPPOSITIONAL, etc.)
- `genealogy_cards` → GENEALOGICAL dimension items with thinker lineage
- `differentiation_cards` → POSITIONAL dimension incompatibility items
- `dimensional_signals` → Per-dimension items (quinean→inferences, sellarsian→assumptions, brandomian→commitments, etc.)
- Stage answers → Appropriate dimension items (core_definition, problem_addressed, etc.)
- `epistemic_blind_spots` → PRESUPPOSITIONAL dimension items marked for resolution

#### 2. Provenance Tracking
All items created via wizard bridge get:
- `provenance_type = WIZARD`
- `created_via = 'initial_wizard'`
- `provenance_source_id` = wizard session ID
- Full ItemReasoningScaffold with source excerpts

#### 3. Wizard Save Integration
Updated the `/concepts/wizard/save` endpoint to:
- Create legacy Concept record (backward compatible)
- Also call the bridge to populate 8D schema
- Return bridge results in response

#### 4. Retroactive Bridge Endpoint
Added `/concepts/{id}/evidence/bridge-wizard` for:
- Retroactively populating 8D schema for existing concepts
- Re-processing wizard outputs after schema updates
- Testing the bridge logic

### Key Files
- `api/wizard_to_schema_bridge.py` (NEW): Core bridge logic
- `api/concept_wizard.py`: Updated save_concept to call bridge
- `api/concept_evidence_router.py`: Added bridge-wizard endpoint

### Mapping Details

| Wizard Output | Dimension | Item Type |
|--------------|-----------|-----------|
| hypothesis_cards (thesis) | POSITIONAL | forward_inference |
| hypothesis_cards (assumption) | PRESUPPOSITIONAL | hidden_assumption |
| hypothesis_cards (tension) | DYNAMIC | tension |
| hypothesis_cards (normative) | NORMALIZATION | embedded_norm |
| genealogy_cards | GENEALOGICAL | theoretical_lineage |
| differentiation_cards | POSITIONAL | incompatibility |
| dimensional_signals.quinean | POSITIONAL | forward_inference |
| dimensional_signals.sellarsian | PRESUPPOSITIONAL | hidden_assumption |
| dimensional_signals.brandomian | COMMITMENT | commitment |
| dimensional_signals.deleuzian | DYNAMIC | tension |
| dimensional_signals.bachelardian | GENEALOGICAL | epistemological_break |
| dimensional_signals.canguilhem | NORMALIZATION | embedded_norm |
| dimensional_signals.davidson | AFFORDANCE | reasoning_style |
| dimensional_signals.blumenberg | GENEALOGICAL | root_metaphor |
| dimensional_signals.carey | GENEALOGICAL | component_concept |
| epistemic_blind_spots | PRESUPPOSITIONAL | epistemic_blind_spot |

### Principles Applied
- `prn_provenance_transparency`: Every item traces to wizard origin
- `prn_evidence_driven_concept_refinement`: Wizard seeds concept, evidence enriches it
- `prn_data_genesis_traceability`: Every field tracks its source

---

## 2025-12-22: Item-to-Item Relationship System

**Commit:** `a21074a`
**Branch:** `main`

### Description
Added proper item-to-item relationships with foreign keys, replacing the previous JSON text arrays in reasoning scaffolds. This enables building a real knowledge web where items can reference each other with typed relationships like DEPENDS_ON, SUPPORTS, CONTRADICTS, etc.

### The Problem
The previous `dependent_claims` field in ItemReasoningScaffold was just a JSON array of text strings with no actual links to other items. This meant:
1. No way to navigate to dependent items
2. No way to update relationships when items change
3. No provenance tracking (how was this relationship discovered?)
4. No real-world population strategy

### The Solution

#### 1. ItemRelationship Junction Table
New model with proper foreign keys:
- `source_item_id` / `target_item_id`: Links to AnalysisItem
- `relationship_type`: Enum with 8 types (depends_on, supports, contradicts, tension_with, enables, supersedes, specializes, generalizes)
- `discovered_via`: Provenance tracking (wizard_generated, evidence_extracted, llm_inferred, user_curated, system_detected)
- `confidence`: Float 0-1
- `explanation`: Why this relationship holds
- `evidence_fragment_id`: Optional link to evidence source

#### 2. Bidirectional Relationships
Items track both outgoing and incoming relationships:
- `outgoing_relationships`: What this item relates to
- `incoming_relationships`: What relates to this item

#### 3. Frontend Display
Updated ReasoningScaffoldDisplay component to:
- Show relationships grouped by type with color-coded icons
- Display direction (outgoing/incoming) with badges
- Show provenance source and confidence
- Make items clickable to navigate and highlight

#### 4. Population Strategies Documentation
Created comprehensive documentation covering 5 population strategies:
1. **Wizard-Generated**: Inferred from structural patterns during initial setup
2. **Evidence-Extracted**: When processing external sources (articles, papers, news)
3. **LLM-Inferred**: Batch inference across all items
4. **User-Curated**: Manual relationship creation
5. **System-Detected**: Automatic detection from content references

### Key Files
- `api/concept_analysis_models.py`: ItemRelationType, RelationshipSource enums, ItemRelationship model
- `api/concept_analysis_router.py`: Updated to return relationships with items
- `scripts/seed_concept_analysis.py`: Sample relationships for testing
- `frontend/src/ConceptAnalysisViewer.jsx`: Updated ReasoningScaffoldDisplay component
- `documentation/RELATIONSHIP_POPULATION_STRATEGIES.md`: Comprehensive strategy guide

### Principles Applied
- `prn_provenance_transparency`: Every relationship tracks how it was discovered
- `prn_evidence_driven_concept_refinement`: Multiple pathways to populate relationships from real-world sources

---

## 2025-12-22: Quinean Intermediate Reasoning Layer

**Commit:** `0b9d040`
**Branch:** `main`

### Description
Added a rich intermediate reasoning layer to AnalysisItem, inspired by Quine's web of belief model. This layer captures the full derivation chain, confidence decomposition, alternatives rejected, and revisability cost for each analytical item - enabling both better LLM reasoning and human audit of the inference process.

### The Problem
Analysis items (like forward inferences) displayed only a strength percentage (e.g., "90%") without explaining:
1. WHY the LLM picked this particular inference
2. What PREMISES supported it and how central each is to the web of belief
3. What SOURCE/CONTEXT triggered the derivation
4. What ALTERNATIVES were considered and rejected
5. What the COST would be of revising this belief

### The Solution

#### 1. Quinean Fields on AnalysisItem
Added new fields to capture web-of-belief positioning:
- `web_centrality`: CORE | HIGH | MEDIUM | PERIPHERAL (how central to belief web)
- `observation_proximity`: Float 0-1 (how close to empirical grounding)
- `coherence_score`: Float 0-1 (how well integrated with other beliefs)

#### 2. ItemReasoningScaffold Model
New model with ~20 fields for full reasoning capture:

**Inference Type & Rule:**
- `inference_type`: DEDUCTIVE | MATERIAL | DEFAULT | ABDUCTIVE | ANALOGICAL | TRANSCENDENTAL
- `inference_rule`: Name of the rule applied (e.g., "material_implication", "condition_of_possibility")

**Derivation Chain:**
- `premises`: JSON list of premises with claim, claim_type, centrality, source
- `reasoning_trace`: Full natural language explanation of the inference

**Source Provenance:**
- `derivation_trigger`: What triggered this (concept_definition, prior_inference, external_source, user_notes)
- `source_passage`: The relevant source text
- `source_location`: Where in the source

**Alternatives & Rejection:**
- `alternatives_rejected`: JSON list of {inference, rejected_because, plausibility}

**Confidence Decomposition:**
- `premise_confidence`: Confidence in premises (0-1)
- `inference_validity`: Validity of inference step (0-1)
- `source_quality`: Quality of source (0-1)
- `web_coherence`: Coherence with belief web (0-1)
- `confidence_explanation`: Why these confidence levels

**Quinean Revisability:**
- `revisability_cost`: What would need to change if this were revised
- `dependent_claims`: What other claims depend on this

#### 3. Frontend ReasoningScaffoldDisplay Component
Rich expandable display showing:
- Inference type badge (e.g., "MATERIAL inference via material_implication")
- Premises with centrality color-coding (core=red, high=orange, medium=yellow, peripheral=green)
- Full reasoning trace
- Source context section
- Confidence decomposition (4 visual bars)
- Alternatives rejected with plausibility scores
- Quinean revisability cost
- Dependent claims

### Philosophical Grounding

**Quine's Web of Belief:**
- Beliefs form an interconnected network, not isolated atoms
- Central beliefs (logic, math) are highly resistant to revision
- Peripheral beliefs (specific observations) are easily revisable
- Revision in one area ripples through connected beliefs
- "No statement is immune to revision" but some have higher costs

**Inference Types Captured:**
- **Deductive**: Logically necessary (A→B, A, therefore B)
- **Material**: Domain-specific rules (semiconductors foundational → invest in fabs)
- **Default**: Defeasible reasoning (birds fly, unless penguin)
- **Abductive**: Inference to best explanation
- **Analogical**: Similar cases, similar treatment
- **Transcendental**: Conditions of possibility

### API Changes
Updated `/concept-analysis/concepts/{id}/dimension/{dim}` to return:
- `web_centrality`, `observation_proximity`, `coherence_score` on items
- Full `reasoning_scaffold` object when present

### Files Modified
- `api/concept_analysis_models.py`: Added WebCentrality, InferenceType enums, ItemReasoningScaffold model, Quinean fields to AnalysisItem
- `api/concept_analysis_router.py`: Updated endpoints to return reasoning scaffold data
- `scripts/seed_concept_analysis.py`: Added REASONING_SCAFFOLDS with 4 sample items
- `frontend/src/ConceptAnalysisViewer.jsx`: Added CentralityBadge and ReasoningScaffoldDisplay components

### Principles Embodied
- `prn_reasoning_justification_externalization`: Make LLM reasoning visible, not hidden
- `prn_dual_consumer_structure_design`: Structure serves both LLM cognition and human audit
- `prn_visibility_as_quality_forcing`: Visibility forces quality improvement in prompts

---

## 2025-12-22: Evidence Integration & Conflict Resolution System

**Commit:** `1808950`
**Branch:** `main`

### Description
Expanded the 8D concept analysis system to support evidence integration from external sources (articles, journalism, thinker's works) with provenance tracking, auto-integration for high-confidence insights, and a rich decision UI for ambiguous cases.

### The Problem
Concepts are not static - they evolve as new evidence is encountered. The previous system treated the initial wizard analysis as final, with no mechanism to:
1. Integrate insights from external sources (articles, books, news)
2. Track the provenance of each analytical element
3. Route ambiguous evidence through user decision-making
4. Articulate commitment/foreclosure tradeoffs for each interpretation

### The Solution

#### 1. Provenance Tracking
Added provenance fields to `AnalysisItem` model:
- `provenance_type`: wizard, evidence, user_manual, llm_synthesis
- `provenance_source_id`: Links to evidence fragment or wizard session
- `provenance_decision_id`: Links to evidence decision if from resolution
- `created_via`: initial_wizard, evidence_auto_integrate, evidence_decision, manual_edit
- `supersedes_item_id`: For items that replace previous versions

#### 2. Evidence Source Management
New models for tracking external sources:
- `ConceptEvidenceSource`: Articles, books, URLs with extraction status
- `ConceptEvidenceFragment`: Extracted claims with relationship analysis
- `ConceptEvidenceInterpretation`: Multiple valid readings for ambiguous evidence
- `ConceptStructuralChange`: Proposed changes with commitment/foreclosure statements
- `ConceptEvidenceDecision`: User choices and applied changes
- `ConceptEvidenceProgress`: Progress tracking for UI

#### 3. Relationship Types (Idea Vectors)
Six types adapted from ASC project patterns:
- **ILLUSTRATES**: Concrete example making abstract vivid
- **DEEPENS**: Adds nuance or complexity
- **CHALLENGES**: Contradicts premise, requires revision
- **LIMITS**: Establishes scope boundary
- **BRIDGES**: Connects previously unlinked operations
- **INVERTS**: Flips assumed relationship

#### 4. Auto-Integration vs Pending Decisions
- Confidence ≥ 0.85 + non-conflicting → auto-integrated
- Confidence < 0.85 OR ambiguous → routes to pending decisions UI

#### 5. Rich Decision UI
Pending decisions view shows:
- Evidence fragment with source citation
- Relationship type and confidence
- Why this needs user input
- 2-4 interpretation options with:
  - Structural changes (before/after)
  - Commitment statements (what you're committing to)
  - Foreclosure statements (what options you're giving up)

#### 6. API Endpoints
New router at `/concepts/{id}/evidence/`:
- `POST /sources` - Add evidence source
- `GET /sources` - List sources with status
- `GET /fragments` - List fragments by status
- `GET /decisions/pending` - Get next pending decision
- `POST /decisions` - Submit decision and apply changes
- `GET /progress` - Progress statistics

#### 7. LLM Prompts
Created comprehensive prompts for:
- Evidence extraction from sources
- Relationship analysis against existing schema
- Interpretation generation for ambiguous cases
- Commitment/foreclosure articulation
- Batch synthesis for multiple fragments

#### 8. Frontend Components
- **EvidenceDashboard**: Progress cards, sources list, action buttons
- **AddEvidenceSource**: Modal for adding new sources
- **EvidenceDecisionView**: Rich decision UI with interpretation options
- **ProvenanceBadge**: Shows origin of each analysis item
- **Tab Navigation**: Switch between Analysis and Evidence views

### Files Created/Modified
- `api/concept_analysis_models.py` - 6 new enums, 7 new models, provenance fields
- `api/concept_evidence_router.py` - New router with all endpoints
- `api/concept_evidence_prompts.py` - LLM prompts for evidence processing
- `api/main.py` - Router registration
- `frontend/src/ConceptAnalysisViewer.jsx` - Tab UI, EvidenceDashboard, ProvenanceBadge
- `frontend/src/components/AddEvidenceSource.jsx` - Source upload modal
- `frontend/src/components/EvidenceDecisionView.jsx` - Decision UI

### Principles Embodied
- `prn_provenance_transparency` - Every element traces back to its origin
- `prn_evidence_driven_concept_refinement` - Concepts evolve through evidence encounters
- `prn_commitment_foreclosure_articulation` - Decisions show what you gain and lose
- `prn_graceful_partial_completion_validity` - Works with partial evidence integration

---

## 2025-12-22: Operation-Indexed 8D Concept Analysis Framework

**Commit:** `e6d8dac`
**Branch:** `main`

### Description
Implemented a new operation-indexed concept analysis framework that reorganizes the philosophical dimensions by analytical operation rather than by thinker. This approach grounds dimensions in what they actually DO analytically, with thinkers as metadata references.

### The Problem
The previous 12-dimension schema was organized by thinker (Quinean, Sellarsian, Kuhnian, etc.). While useful for attribution, this organization:
1. Made it harder to see what analytical work each dimension performs
2. Created redundancy where different thinkers contributed similar operations
3. Made the schema less modular and harder to extend

### The Solution

#### 1. Reorganized into 8 Analytical Dimensions
Each dimension is defined by its core analytical question:
- **Positional Analysis**: Where does this concept SIT in various networks?
- **Genealogical Analysis**: Where does this concept COME FROM?
- **Presuppositional Analysis**: What does this concept TAKE FOR GRANTED?
- **Commitment Analysis**: What does accepting this concept COMMIT YOU TO?
- **Affordance Analysis**: What does this concept ENABLE or BLOCK?
- **Normalization Analysis**: What does this concept NORMALIZE?
- **Boundary Analysis**: What are the LIMITS of this concept?
- **Dynamic Analysis**: How does this concept CHANGE over time?

#### 2. 38 Analytical Operations
Each dimension contains 4-6 specific operations (e.g., Inferential Mapping, Paradigm Positioning, Givenness Excavation, etc.)

#### 3. 14 Theoretical Influences as Metadata
Thinkers (Quine, Kuhn, Foucault, Sellars, Brandom, etc.) are now linked to operations they inform via a junction table.

#### 4. SQLAlchemy Models
Created comprehensive async SQLAlchemy models:
- `AnalyticalDimension` - The 8 dimensions
- `AnalyticalOperation` - The 38 operations
- `TheoreticalInfluence` - The 14 thinkers
- `AnalyzedConcept` - Concepts being analyzed
- `ConceptAnalysis` - Analysis per concept per operation
- `AnalysisItem` - Individual items within analyses

#### 5. FastAPI Router
New `/concept-analysis/` endpoints:
- `GET /dimensions` - List all dimensions with operations
- `GET /operations` - List all operations
- `GET /influences` - List all theoretical influences
- `GET /concepts` - List analyzed concepts
- `GET /concepts/{id}` - Full analysis across all dimensions
- `GET /schema-overview` - High-level statistics

#### 6. React UI Component
Created `ConceptAnalysisViewer.jsx` with:
- Schema overview with statistics
- Concept selector
- Expandable dimension cards with color coding
- Nested operation sections showing analysis items
- Expand/collapse all functionality

#### 7. Complete Tech Sovereignty Analysis
Seeded database with comprehensive analysis of "Technological Sovereignty" across all 38 operations, generating 159 individual analysis items.

### Files Created/Modified
- `api/concept_analysis_models.py` - SQLAlchemy models
- `api/concept_analysis_router.py` - FastAPI router
- `scripts/seed_concept_analysis.py` - Database seeder
- `frontend/src/ConceptAnalysisViewer.jsx` - React component
- `frontend/src/App.jsx` - Added 8D Analysis tab

### Principles Embodied
- `prn_operation_grounding` - Dimensions are defined by analytical operations, not attribution
- `prn_modular_extensibility` - Schema can grow as new operations are discovered
- `prn_metadata_separation` - Thinkers inform operations but don't organize the schema

---

## 2025-12-21: Strengthened New Dimensions & IE Export Function

**Commit:** `8e09dee`
**Branch:** `main`

### Description
Strengthened the 3 new philosophical dimensions (Kuhnian, Pragmatist, Foucauldian) with additional analytical depth, added cross-cutting canonical statement tables, and created an export function for Intelligence Engine integration.

### The Problem
The 3 new dimensions added in the previous commit had basic table structures but lacked the full analytical depth of the original 9 dimensions. Additionally, there was no way to export concept analyses for use in the Intelligence Engine (IE).

### The Solution

#### 1. Strengthened Kuhnian Dimension
Added new tables and questions for:
- **Incommensurability mapping**: How concept relates to rival paradigms, translation issues
- **Crisis indicators**: What would trigger paradigm crisis, anomaly accumulation thresholds
- **Disciplinary matrix**: Shared commitments, values, and exemplars

#### 2. Strengthened Pragmatist Dimension
Added new tables and questions for:
- **Habits of action**: What habits and dispositions using the concept cultivates
- **Vocabulary games** (Rorty): What new things can be SAID with this concept
- **Inquiry process** (Dewey): How concept structures problem-solving

#### 3. Strengthened Foucauldian Dimension
Added new tables and questions for:
- **Discursive formations**: Rules of formation for statements
- **Regimes of truth**: What counts as true, who speaks with authority
- **Archaeology**: How concept emerged, discursive conditions of possibility

#### 4. Cross-Cutting Tables
- **concept_canonical_statements**: One canonical statement per dimension per concept
- **concept_export_metadata**: Metadata for IE export readiness

#### 5. IE Export Function
New endpoint `GET /export/{session_key}` that exports concepts in IE-compatible format including:
- Core identity (term, definition, author)
- Canonical statements for each of 12 dimensions
- Approved posits
- Blind spots exploration results
- External concept relationships
- Completeness score and export readiness indicator

### Implementation
- Updated `GENERATE_DEEP_COMMITMENTS_PROMPT` with strengthening concepts
- Added 7 new tables across 3 dimensions in spreadsheet generator
- Added `CROSS_CUTTING_TABLES` dictionary with canonical statements and export metadata
- Added `ConceptExportRequest/Response` models
- Added `export_concept_for_ie()` endpoint
- Updated spreadsheet generator to include cross-cutting tables sheet

### Principles Embodied
- `prn_dimensional_completeness_for_complex_programs` - All dimensions now have comparable analytical depth
- `prn_export_compatibility_with_ie` - Concept Wizard outputs are now IE-compatible

---

## 2025-12-21: Extended to 12-Dimension Philosophical Framework

**Commit:** `7b80e9c`
**Branch:** `main`

### Description
Extended the 9-dimension philosophical framework to 12 dimensions by adding Kuhnian, Pragmatist, and Foucauldian dimensions. This provides more comprehensive coverage for analyzing complex research programs.

### The Problem
The original 9 dimensions (Sellarsian, Brandomian, Deleuzian, Hacking, Bachelardian, Quinean, Carey, Blumenberg, Canguilhem) were excellent for conceptual analysis but missed three important axes:
- **Paradigm structure** (Kuhn) - What paradigm does the concept belong to? What counts as an anomaly?
- **Performative consequences** (Pragmatist) - What does USING the concept enable? What practical difference does it make?
- **Power-knowledge relations** (Foucault) - What power relations does it naturalize? What does it make governable?

### The Solution
Added 3 new dimensions to both the posit typology and the deep commitments questioning:

| Type | Description | Dimension |
|------|-------------|-----------|
| `paradigmatic` | How concept relates to paradigm structure | Kuhnian |
| `performative` | What using this concept DOES/enables | Pragmatist |
| `power_relational` | Power relations it naturalizes/contests | Foucauldian |

### Implementation
- Extended `PosItType` enum from 9 to 12 types
- Added metadata for new types (indigo, teal, rose colors)
- Updated `INFORMED_HYPOTHESIS_GENERATION_PROMPT` with new types and examples
- Updated `GENERATE_DEEP_COMMITMENTS_PROMPT` with 3 new dimension sections and example questions
- Added coverage validation to ensure posits span all 12 dimensions
- Added CSS for new posit colors

### Principles Embodied
- `prn_dimensional_completeness_for_complex_programs` - Complex research programs require analysis across all major philosophical axes
- Systematic extension of framework to handle paradigm membership, practical effects, and power dynamics

---

## 2025-12-21: 9-Dimension Grounded Posit Typology

**Commit:** `a417264`
**Branch:** `main`

### Description
Replaced ad-hoc "hypothesis" types (thesis, assumption, tension, methodological, normative) with a formal typology grounded in the 9-dimensional philosophical framework.

### The Problem
The previous card types were functional but ad-hoc:
- **thesis** - core argument
- **assumption** - implicit premise
- **tension** - internal conflict
- **methodological** - how to study
- **normative** - what should be

This mixed content type, epistemic status, structural features, and functional types without systematic grounding in our philosophical dimensions.

### The Solution
A 9-dimension grounded typology where each posit type maps to a specific philosophical dimension:

| Type | Description | Dimension |
|------|-------------|-----------|
| `definitional` | What the concept IS | Sellarsian |
| `inferential` | What follows from it | Brandomian |
| `incompatibility` | What it rules out | Brandomian |
| `genealogical` | Where it comes from | Carey/Blumenberg |
| `transformational` | What change it enables | Deleuzian |
| `epistemological_break` | What discontinuity it marks | Bachelardian |
| `methodological` | How to study/apply | Hacking |
| `normative` | Evaluative claims | Canguilhem |
| `positional` | Where it sits in belief web | Quinean |

### Implementation
- `PosItType` enum with all 9 types
- `POSIT_TYPE_METADATA` with labels, colors, dimensions
- Updated `INFORMED_HYPOTHESIS_GENERATION_PROMPT` with type examples
- New `GET /posit-types` endpoint for frontend
- Cards now show type label and dimension badge
- 9 distinct color schemes for posit types

### Terminology Change
"Hypotheses" renamed to "Posits" (preliminary claims) - more accurate since these aren't testable predictions but detected claims the user can approve/reject.

### Principles Embodied
- 9-dimensional framework now applies to claim categorization, not just concept analysis
- Systematic grounding of typology in philosophical dimensions

---

## 2025-12-21: Concept Relationships Schema

**Commit:** `38243a3`
**Branch:** `main`

### Description
Comprehensive schema for tracking relationships between internal concepts (ones we define) and external concepts from other authors/paradigms. Enables nuanced philosophical comparison across the 9-dimensional framework.

### The Problem
When developing concepts like "Organic Capitalism," we need to relate them to existing concepts from other thinkers (Zuboff's "Surveillance Capitalism," Srnicek's "Platform Capitalism"). Without structured relationships, these comparisons live only in prose - making them hard to query, visualize, or reason about systematically.

### The Solution
Two new database models with full CRUD API:

**ExternalConcept Model:**
- `term`, `author`, `source_work`, `year`
- `brief_definition`, `extended_definition`
- `paradigm`, `research_program`, `disciplinary_home`
- `key_claims` (JSON), `dimensional_analysis` (JSON)

**ConceptRelationship Model:**
- Source concept (internal OR external)
- Target concept (internal OR external)
- `relationship_type`: rivals, complements, subsumes, ruptures, specializes, shares_problematic, historicizes, appropriates, responds_to, synthesizes, instantiates, problematizes, extends
- 9 dimensional JSON columns for philosophical nuance:
  - `sellarsian`: manifest_vs_scientific (who, what), commitment_structure
  - `brandomian`: inferential_role_difference, material_incompatibility, normative_status_contrast
  - `deleuzian`: deterritorialization_vector, plane_of_consistency, becoming_direction
  - `hacking`: problematic_relation (same_problematic, adjacent, rival), web_proximity (near, far)
  - `bachelardian`: epistemological_break_assessment, obstacle_relation
  - `quinean`: centrality_difference (core vs peripheral), revisability_contrast
  - `carey`: core_domain_sharing, feature_inheritance, transformation_type
  - `blumenberg`: metaphor_inheritance, absolutism_relation, reoccupation_assessment
  - `canguilhem`: norm_relation, pathological_boundary_difference

### New Endpoints
- `GET/POST /concept-relationships/external-concepts`
- `GET/PATCH/DELETE /concept-relationships/external-concepts/{id}`
- `GET/POST /concept-relationships/relationships`
- `GET/PATCH/DELETE /concept-relationships/relationships/{id}`
- `GET /concept-relationships/concepts/{id}/relationships`
- `GET /concept-relationships/relationships/by-type/{type}`

### Database Migration
Run `POST /admin/migrate` to create the `external_concepts` and `concept_relationships` tables.

### Principles Embodied
- 9-dimensional concept analysis applied to inter-concept relationships
- Structured representation of philosophical dialogue across paradigms

---

## 2025-12-20: Blind Spots Before Hypotheses Flow

**Commit:** `3f17dd5` (initial), `3c257e3` (curator call fix)
**Branch:** `main`

### Description
Major wizard flow reordering: Epistemic blind spots questioning now happens BEFORE hypothesis generation. This allows the system to generate theses informed by the user's revealed theoretical agenda rather than generic possibilities.

### The Problem
Previously, hypothesis cards were generated during initial notes analysis, before the user had a chance to explore their blind spots. This meant theses were based solely on what was in the notes, missing the user's actual theoretical concerns that only emerge through the blind spots questioning process.

### The Solution
Reorder the wizard flow:
1. **Before:** Notes → Hypotheses → Blind Spots → ...
2. **After:** Notes → Blind Spots → Informed Hypotheses → ...

New flow:
1. Notes analysis extracts blind spots but NOT hypothesis cards
2. User explores blind spots through curator/sharpener questioning
3. After blind spots completion, system generates hypothesis/genealogy/differentiation cards **informed by** user's answers
4. User reviews the informed hypotheses in validate-understanding stage

### Implementation

**Backend:**
- `INITIAL_ANALYSIS_PROMPT` - New prompt for stage1 that generates blind spots but not cards
- `INFORMED_HYPOTHESIS_GENERATION_PROMPT` - New prompt that uses blind spots answers to generate targeted cards
- `POST /generate-informed-hypotheses` - New endpoint called after blind spots completion

**Frontend:**
- New `GENERATING_HYPOTHESES` stage
- Stage navigation reordered: Blind Spots → Validate Hypotheses
- `generateInformedHypotheses()` function wires up the new endpoint
- Both `finishBlindSpotsEarly` and `submitBlindSpotAnswer` completion now trigger hypothesis generation

### Principles Embodied
- `prn_epistemic_grounding_before_thesis_generation` - Gather epistemic position before generating theses

---

## 2025-12-20: Write-In Type Qualification Dropdown

**Commit:** `d92dcbd`
**Branch:** `main`

### Description
When users provide write-in text alongside selected options, a dropdown appears asking them to qualify what type of input they're providing.

### The Problem
When users write in their own text, the LLM doesn't know how to interpret it:
- Is it elaborating on selected answers?
- Is it a completely different alternative?
- Is it commentary on the question itself?

### The Solution
Add a dropdown that appears when write-in text is detected:
- "Elaboration on my selected answer(s)"
- "A new alternative answer"
- "A comment on this question itself"

The combined answer now includes labeled sections:
- `[Selected from options]:` for chosen multi-choice items
- `[Elaboration/Alternative/Comment]:` for write-in based on type

### Implementation
- `writeInType` state tracks selected type
- Dropdown appears conditionally when `writeInAddition.trim()` is truthy
- `buildCombinedAnswer()` includes type labels in the output

### Principles Embodied
- `prn_input_qualification_for_context` - Help LLM understand input intent
- Inspired by essay-flow's Guided Reframing modal

---

## 2025-12-20: Background Pre-Generation of Answer Options

**Commit:** `e7568c5`
**Branch:** `main`

### Description
Pre-generates multiple choice answer options in the background while users are occupied with other tasks, creating an illusion of instant response.

### The Problem
LLM calls take several seconds. When user clicks "Help me articulate", they must wait for generation. This friction discourages use of the guided discovery path.

### The Solution
Exploit "user occupied time" as free computation budget:
- After curator completes: immediately pre-generate options for first 2 questions
- After each answer: pre-generate options for next 3 upcoming questions
- When user clicks "Help me articulate": check cache first → instant response if pre-generated

### Implementation
- `preGeneratedOptionsCache` state: `{slotIndex: optionsData}`
- `preGeneratingSlots` state: Set of currently-generating slot indices
- `preGenerateOptionsForSlot(slotIndex, queueSnapshot)` - Background generation
- `triggerPreGeneration(startIndex, count, queueData)` - Trigger batch pre-generation

### Principles Embodied
- `prn_background_pregeneration_illusion` - Pre-generate while user is occupied
- `prn_interaction_time_as_computation_budget` - Use wait time for generation

---

## 2025-12-20: Dual Response Mode for Blind Spots Questioning

**Commit:** `257374a` (initial), updated with multi-select
**Branch:** `main`

### Description
Added "Help me articulate" feature that offers users a choice between free text entry and LLM-generated multiple choice options. Implements `prn_intent_formation_state_bifurcation` principle.

### The Problem
Users arrive at blind spots questions with different levels of intent clarity:
- Some know what they want to say → need free text entry
- Some need scaffolding to discover their position → need guided options

Forcing all users through a single flow frustrates both groups.

### The Solution
- "Help me articulate" button generates 4 stance-based answer options
- Each option represents a different epistemic stance: assertive, exploratory, qualified, provocative
- **Multi-select support**: LLM determines if options are mutually exclusive
  - If NOT mutually exclusive: checkboxes allow selecting multiple options
  - If mutually exclusive: radio buttons allow only one selection
- **Write-in always available**: Users can add their own text alongside any selected options
- **Combined answers**: Final submission merges selected options + write-in for richer context

### New Endpoint
- `POST /concepts/wizard/generate-answer-options` - Generates 4 stance-based answer options

### New Models
- `GenerateAnswerOptionsRequest` - Request with question context
- `AnswerOption` - Individual option with id, text, stance
- `GenerateAnswerOptionsResponse` - Response with options, guidance, mutually_exclusive flag, exclusivity_reason

### Frontend
- "Help me articulate" button with loading state
- 2x2 grid of selectable option cards with checkboxes/radio indicators
- Select mode badge ("Pick one" vs "Select multiple")
- Stance badges (assertive, exploratory, qualified, provocative)
- Write-in textarea always visible below options
- Selection summary showing count + write-in status
- Dismiss options button

### Principles Embodied
- `prn_intent_formation_state_bifurcation` - Bifurcate pathways based on user's intent-formation state

---

## 2025-12-19: Curator-Sharpener Two-Stage Questioning System

**Commit:** `69c2382`
**Branch:** `main`

### Description
Implemented a dynamic two-stage questioning system for blind spots exploration:
- **Curator Service**: Analyzes notes against 7-category epistemic registry, allocates question slots (max 16), determines emphasis, generates interleaved question sequence
- **Sharpener Service**: Runs asynchronously while user answers questions, generates deeper follow-ups based on answers, dynamically injects new questions into the queue

### Key Features
- **Temporal Category Dispersion**: Questions interleaved across categories (not clustered) to prevent fatigue
- **Graceful Partial Completion**: Even 3/16 answers is valid - system works with what it gets
- **Interaction Time as Computation Budget**: Uses answer time to generate deeper follow-ups
- **Dynamic Queue Injection**: Sharpened questions inserted 2-3 slots ahead for variety

### New Models
- `BlindSpotSlot` - Individual question slot with depth tracking (1-3)
- `CuratorAllocation` - Curator's analysis and allocation plan
- `BlindSpotsQueue` - Full queue with dynamic updates and sharpener pending tracking

### New Endpoints
- `POST /concepts/wizard/curate-blind-spots` - Curator service
- `POST /concepts/wizard/sharpen-question` - Sharpener service (SSE streaming)
- `POST /concepts/wizard/submit-blind-spot-answer` - Answer submission
- `POST /concepts/wizard/finish-blind-spots` - Early termination

### Frontend
- Progress bar with sharpening indicator animation
- Question card with category badges and depth indicators
- Early finish option after minimum 3 answers
- Allocation rationale disclosure panel

### Principles Embodied
- `prn_graceful_partial_completion_validity` - System works with partial inputs
- `prn_temporal_category_dispersion` - Questions spread across categories
- `prn_strategic_structure_before_tactical_content` - Curator decides allocation before Sharpener generates
- `prn_interaction_time_as_computation_budget` - Uses wait time for generation

---

## 2025-12-19: Epistemic Blind Spots Refactoring

**Commit:** `b6784bd`
**Branch:** `main`

### Description
Replaced the "Gaps, Tensions & Open Questions" section in the Concept Setup Wizard with "Blind Spots" - a more precise epistemic framing.

### Key Changes
- **New EpistemicBlindSpot model** with 7 categories derived from 9-dimensional analysis:
  - `ambiguity` - Terms/phrases with multiple valid readings
  - `presupposition` - What's treated as "given" without justification
  - `paradigm_dependency` - Where different epistemes produce different conclusions
  - `likely_misreading` - Common ways concept could be misunderstood
  - `gray_zone` - Boundary cases where application is uncertain
  - `unfilled_slot` - Placeholder structures awaiting elaboration
  - `unconfronted_challenge` - Objections not yet addressed

- **Frontend UI** with category badges, icons, and color coding
- **Updated prompts** for NOTES_PREPROCESSING, GENERATE_BLIND_SPOTS, INTERIM_ANALYSIS

### Rationale
Distinguishes between:
- **Ontological underdetermination** (dialectics) - the object itself is open/in process
- **Epistemic underdetermination** (blind spots) - user's positioning not yet explicit

This helps users articulate their priors, confront structural weaknesses, and grasp conditions of possibility for their thinking.

---

## 2025-12-19: Light/Dark Theme Support

**Commit:** `546aeeb`
**Branch:** `main`

### Description
Added support for light and dark themes with light mode as default.

---

## Previous Features

*(Add earlier features here as they are documented)*

