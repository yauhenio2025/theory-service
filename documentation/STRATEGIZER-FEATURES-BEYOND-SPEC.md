# Strategizer: Features Beyond Original Specification

**Date:** 2025-12-29
**Purpose:** Document all features implemented beyond the original STRATEGIZER-IMPLEMENTATION-SPEC.md and MVP plans

---

## Executive Summary

The Strategizer implementation significantly exceeded the original specification scope. While the MVP plan focused on **Phase 1 (Domain Bootstrapping + Basic Q&A)** with stubs for Phase 2-3, the actual implementation includes:

1. **Complete Phase 1** - Domain bootstrapping, unit management, Q&A dialogue ✅
2. **Complete Phase 2** - Evidence integration with confidence-based routing ✅
3. **Partial Phase 3** - Friction detection (evolved into Coherence Monitoring) ✅
4. **NEW: Theoretical Coherence Monitoring System** - Not in original spec
5. **NEW: Predicament Management** - Detection, analysis, resolution workflow
6. **NEW: Interactive Matrix Analysis** - Cell-based actions with AI menus
7. **NEW: Dialectic Generation from Notes** - Transform insights into units
8. **NEW: Extended Thinking Integration** - Opus 4.5 with deep analysis

---

## Original Specification Scope

### Phase 1 (MVP Target)
- Project creation with brief ✅
- Domain bootstrapping (LLM proposes structure) ✅
- Basic unit creation: Concepts, Dialectics, Actors ✅
- Simple Q&A to refine units ✅
- SQLite/PostgreSQL persistence ✅

### Phase 2 (Planned, not in MVP)
- PDF upload (single and batch)
- Fragment extraction from PDFs
- Fragment-to-unit matching
- Auto-integration for high-confidence matches
- Pending decisions queue

### Phase 3 (Planned, not in MVP)
- Friction detection across all unit types
- Friction surfacing with resolution options
- Unit evolution based on evidence
- Domain evolution

### Explicitly Out of Scope
- ~~Multi-grid analysis~~ (now implemented)
- ~~Epistemic status tracking~~ (now implemented via coherence)
- ~~External literature API~~ (still stubbed)
- ~~Multi-user/auth~~ (still not implemented)
- ~~Export functionality~~ (still not implemented)

---

## Features Implemented Beyond Specification

### 1. Theoretical Coherence Monitoring System (Entirely New)

**Not mentioned anywhere in original specs.** This is a complete subsystem for detecting and managing theoretical tensions in the framework.

#### 1.1 Two-Tier Coherence Analysis
```
Quick Scan (Sonnet)     → Fast detection of obvious tensions
Deep Analysis (Opus)    → Extended thinking with 10K token budget
```

**Endpoints:**
- `POST /projects/{id}/coherence/quick-scan`
- `POST /projects/{id}/coherence/deep-analysis`
- `GET /projects/{id}/coherence/stats`

**What It Does:**
- Analyzes entire framework for internal contradictions
- Detects four predicament types:
  - **Theoretical Tension** - Concepts don't cohere
  - **Empirical Gap** - Evidence missing or contradictory
  - **Conceptual Ambiguity** - Unclear boundaries/definitions
  - **Praxis Limitation** - Theory doesn't translate to action

#### 1.2 Predicament Detection & Lifecycle
```
DETECTED → ACKNOWLEDGED → UNDER_ANALYSIS → RESOLVED/DEFERRED
```

**Not in spec:** The concept of a "predicament" as a first-class entity that tracks theoretical tensions through a resolution workflow.

---

### 2. Predicament Grid Generation with LLM Refinement

**Spec mentioned grids only for units.** The implementation extends grids to predicaments with dynamic generation.

#### 2.1 Grid Generation for Predicaments
```python
POST /projects/{id}/predicaments/{id}/generate-grid

# Generates an analytical matrix tailored to the specific predicament
# with rows/columns derived from the tension's nature
```

#### 2.2 Grid Refinement Parameters (Not in Spec)
Users can refine the generated matrix with:
- **Row/Column Granularity** - "More granular rows" / "Broader columns"
- **Axis Manipulation** - Add/remove/rename rows/columns
- **Custom Dimensions** - Add entirely new analytical axes
- **Free-Form Instructions** - Natural language refinement requests

**Example:**
```json
{
  "refinement_params": {
    "row_adjustment": "more_granular",
    "column_adjustment": "add_column",
    "new_column_name": "Coalition Potential",
    "instructions": "Focus on policy implementation barriers"
  }
}
```

---

### 3. Interactive Matrix Cell Actions (Entirely New)

**The spec described grids as data structures. The implementation makes them interactive.**

#### 3.1 Click-to-Action Matrix Intersections
Users can click on any cell intersection in a predicament matrix to trigger AI-powered analysis.

**Single-Cell Actions:**
| Action | Description |
|--------|-------------|
| `what_would_it_take` | Explore conditions for this cell to resolve |
| `deep_dive` | Extended thinking analysis of this intersection |
| `generate_arguments` | Create arguments for/against positions |
| `scenario_exploration` | Project future states from this point |
| `surface_assumptions` | Identify hidden assumptions at this intersection |

**Multi-Cell Actions:**
| Action | Description |
|--------|-------------|
| `find_connections` | Discover hidden relationships between cells |
| `coalition_design` | Design coalitions across actor cells |
| `prioritize` | Rank selected cells by urgency/impact |
| `synthesize_concept` | Create new concept from multiple insights |
| `draft_content` | Generate prose synthesizing selections |

#### 3.2 Dynamic Action Generation
```python
POST /projects/{id}/predicaments/{id}/generate-actions

# LLM generates context-specific actions based on:
# - The specific predicament's nature
# - The selected cell(s) and their content
# - The overall project context
# - What would help resolve the tension
```

**Not in spec:** Actions are generated dynamically per-context, not a fixed menu.

---

### 4. Predicament Notes System (Entirely New)

**A workflow for capturing insights from matrix analysis and transforming them into framework elements.**

#### 4.1 Save Insights as Notes
```python
POST /projects/{id}/predicaments/{id}/notes
{
  "insight_type": "observation|question|hypothesis|resolution_path",
  "content": "The insight text",
  "action_context": {
    "action_type": "deep_dive",
    "cell_row": "Government Actors",
    "cell_col": "Short-term Barriers",
    "thinking_summary": "Extended thinking output..."
  }
}
```

#### 4.2 Notes Retain Action Context
Each note preserves:
- The cell(s) it came from
- The action that generated it
- The LLM's thinking summary
- Timestamp and order

---

### 5. Dialectic Spawning from Notes (Entirely New)

**Transform accumulated insights into new framework elements.**

```python
POST /projects/{id}/predicaments/{id}/notes/{note_id}/spawn-dialectic
```

**What It Does:**
1. Takes the note's insight content
2. Analyzes it for dialectical structure
3. Generates:
   - Pole A (name, description, conditions favoring)
   - Pole B (name, description, conditions favoring)
   - Synthesis paths
   - Navigation strategies
4. Creates a new DialecticUnit in the project
5. Links it back to the source predicament

**Example Output:**
```yaml
dialectic:
  name: "Urgency ↔ Thoroughness"
  pole_a:
    name: "Urgency"
    description: "Need for immediate action given crisis conditions"
    when_prioritize: "When window of opportunity is closing"
  pole_b:
    name: "Thoroughness"
    description: "Need for comprehensive stakeholder buy-in"
    when_prioritize: "When long-term coalition stability matters"
  synthesis_paths:
    - "Staged implementation with early wins and later consolidation"
  provenance:
    source_predicament: "Climate Policy Tradeoffs"
    source_note_id: "uuid..."
```

---

### 6. Extended Thinking Integration (Not in Spec)

**The spec mentioned Claude API. The implementation uses Opus 4.5 with extended thinking for complex analysis.**

#### 6.1 Where Extended Thinking is Used
| Feature | Thinking Budget |
|---------|----------------|
| Deep Coherence Analysis | 10,000 tokens |
| Cell Deep Dive Actions | 8,000 tokens |
| Dialectic Generation | 6,000 tokens |
| Dynamic Action Generation | 4,000 tokens |

#### 6.2 Streaming for Long Operations
```python
# Uses client.messages.stream() for extended thinking
# Prevents timeout on operations that can take 30+ seconds
# Returns thinking summaries alongside content
```

---

### 7. Evidence Integration (Phase 2 Implemented Early)

**The spec planned this for Phase 2, but it's fully implemented.**

#### 7.1 Confidence-Based Routing
```
≥0.85 confidence  →  Auto-integrate to grid slot
0.60-0.84         →  Needs user confirmation
<0.60             →  Generate multiple interpretation options
```

#### 7.2 Interpretation Generation with Commitment/Foreclosure
```json
{
  "interpretations": [
    {
      "key": "a",
      "title": "Supports dialectic tension",
      "commitment": "You're committing to this evidence challenging your thesis",
      "foreclosure": "You're passing on using this as supporting evidence",
      "target_unit": "Climate Impact ↔ Financial Returns",
      "is_recommended": true
    }
  ]
}
```

---

### 8. Background Coherence Checks (Not in Spec)

**Coherence monitoring runs automatically in background.**

Triggered on:
- Unit creation
- Unit updates
- Grid slot modifications

Uses quick Sonnet-based scans to detect obvious tensions without blocking user flow.

---

### 9. Grid System Extensions

#### 9.1 Grid Auto-Application
```python
POST /projects/{id}/units/{unit_id}/grids/auto-apply

# Automatically applies appropriate grids based on unit type
# Concepts get: LOGICAL, ACTOR, TEMPORAL, GENEALOGICAL, FUNCTIONAL
# Dialectics get: LOGICAL, ACTOR, TEMPORAL, SYNTHESIS, CONTEXTUAL
# Actors get: LOGICAL, ACTOR, TEMPORAL, INFLUENCE, COALITION
```

#### 9.2 Grid Friction Detection (LLM-Powered)
```python
POST /projects/{id}/grids/detect-friction

# Scans all grids across all units for:
# - Contradictions between slots
# - Gaps in critical slots
# - Inconsistencies across units
```

---

### 10. Complete Web UI (Beyond Minimal Spec)

**The spec sketched text mockups. The implementation is a full web application.**

| Page | Features |
|------|----------|
| `/ui/` | Project list with create modal, domain summaries |
| `/ui/projects/{id}` | 3-column workspace (units by type, overview, stats) |
| `/ui/projects/{id}/units/{id}` | Full unit editing with grid accordion |
| `/ui/projects/{id}/evidence` | Sources, fragments, extraction triggers |
| `/ui/projects/{id}/decisions` | Pending decisions with interpretation review |
| `/ui/projects/{id}/coherence` | Predicament dashboard with quick/deep scan triggers |
| `/ui/projects/{id}/predicaments/{id}` | Interactive matrix with cell actions, notes, dialectic spawning |

---

## Feature Comparison Matrix

| Feature | In Original Spec | Actually Implemented |
|---------|------------------|---------------------|
| Project CRUD | ✅ Phase 1 | ✅ |
| Domain Bootstrapping | ✅ Phase 1 | ✅ |
| Unit Management | ✅ Phase 1 | ✅ |
| Q&A Dialogue | ✅ Phase 1 | ✅ |
| Grid Instances | ✅ Phase 1 (basic) | ✅ Enhanced |
| Evidence Upload | ❌ Phase 2 | ✅ |
| Fragment Extraction | ❌ Phase 2 | ✅ |
| Confidence Routing | ❌ Phase 2 | ✅ |
| Pending Decisions | ❌ Phase 2 | ✅ |
| Friction Detection | ❌ Phase 3 | ✅ (as Coherence) |
| Unit Evolution | ❌ Phase 3 | ✅ (via Dialectic Spawning) |
| **Coherence Monitoring** | ❌ Not mentioned | ✅ NEW |
| **Predicament System** | ❌ Not mentioned | ✅ NEW |
| **Matrix Cell Actions** | ❌ Not mentioned | ✅ NEW |
| **Notes System** | ❌ Not mentioned | ✅ NEW |
| **Dialectic Spawning** | ❌ Not mentioned | ✅ NEW |
| **Extended Thinking** | ❌ Not mentioned | ✅ NEW |
| **Grid Refinement** | ❌ Not mentioned | ✅ NEW |
| **Dynamic Actions** | ❌ Not mentioned | ✅ NEW |
| **Background Checks** | ❌ Not mentioned | ✅ NEW |

---

## Architectural Additions

### New Database Tables (Beyond Spec)
```sql
-- Coherence system tables (not in original schema)
strategizer_predicaments
  - type (theoretical/empirical/conceptual/praxis)
  - severity (critical/major/minor/informational)
  - status (detected/acknowledged/under_analysis/resolved/deferred)
  - generated_grid (JSON)
  - resolution_summary

strategizer_predicament_notes
  - insight_type
  - content
  - action_context (JSON)
  - spawned_dialectic_id
```

### New Router Files
```
api/strategizer/
├── router.py           # Original (expanded)
├── evidence_router.py  # Added for Phase 2
├── coherence_router.py # NEW - entire coherence subsystem
└── ui_router.py        # Full web UI (beyond spec mockups)
```

### New Service Files
```
api/strategizer/services/
├── llm.py              # Original (expanded)
├── evidence_llm.py     # Added for evidence
└── coherence_monitor.py # NEW - coherence analysis
```

### New Prompt Files
```
api/strategizer/prompts/
├── grid_prompts.py     # Original
├── evidence_prompts.py # Added
└── coherence_prompts.py # NEW - 500+ lines
```

---

## Usage Patterns Enabled (Not Anticipated in Spec)

### 1. Iterative Matrix Refinement
```
User creates predicament →
  Generates matrix →
    Clicks cells for analysis →
      Saves insights as notes →
        Spawns dialectic from note →
          Dialectic joins framework
```

### 2. Evidence-Driven Coherence Detection
```
Upload evidence →
  Extract fragments →
    Integrate to grids →
      Background coherence check →
        Predicament detected →
          User investigates with matrix
```

### 3. Deep Analysis Workflow
```
Quick scan detects tension →
  User triggers deep analysis (Opus + thinking) →
    Predicament created with rich context →
      Matrix generated with refinement options →
        Cell-by-cell exploration with AI
```

---

## Principles Embodied (Beyond Original)

| Principle | Implementation |
|-----------|----------------|
| `prn_extended_thinking_for_depth` | Deep analysis uses 10K thinking tokens |
| `prn_matrix_as_exploration_surface` | Predicament grids are interactive |
| `prn_insight_to_structure` | Notes can spawn new dialectics |
| `prn_background_vigilance` | Coherence checks run automatically |
| `prn_dynamic_action_generation` | Actions tailored to context |
| `prn_provenance_preservation` | Dialectics link to source notes |

---

## Summary

The Strategizer implementation represents a **2-3x scope expansion** beyond the original MVP specification:

1. **Phase 1** was fully implemented as planned
2. **Phase 2** (Evidence) was implemented ahead of schedule
3. **Phase 3** (Friction) evolved into a richer **Coherence Monitoring System**
4. **New capabilities** for interactive matrix analysis, note-taking, and dialectic generation were added
5. **Extended thinking** integration enables deeper AI analysis than originally conceived

The system has evolved from "a framework builder with Q&A" into "an interactive theoretical coherence laboratory with AI-powered exploration tools."

---

*Generated: 2025-12-29*
*Comparing: STRATEGIZER-IMPLEMENTATION-SPEC.md, STRATEGIZER-MVP-ADDENDUM.md, STRATEGIZER-MVP-IMPLEMENTATION-PLAN.md vs. actual implementation*
