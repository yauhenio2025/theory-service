# Theory Service Features Log

This document tracks major features introduced to the Theory Service application.

---

## 2025-12-21: Strengthened New Dimensions & IE Export Function

**Commit:** `pending`
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

