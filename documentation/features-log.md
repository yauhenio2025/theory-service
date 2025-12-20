# Theory Service Features Log

This document tracks major features introduced to the Theory Service application.

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

