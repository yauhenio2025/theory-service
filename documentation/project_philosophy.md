# Theory Service Project Philosophy

This document captures how the Theory Service embodies philosophical principles from our knowledge base.

---

## Core Principles Embodied

### prn_epistemic_ontological_distinction
**"Systems processing conceptual content should distinguish between ontological underdetermination and epistemic underdetermination."**

The Theory Service explicitly separates:
- **Dialectics** (ontological) - Genuine tensions/openness in the object itself
- **Blind Spots** (epistemic) - Gaps in the user's grasp, positioning, or path to the concept

This prevents misattributing knowledge gaps to the object or genuine dialectical openness to mere ignorance.

**Implementation:** The Blind Spots section (formerly Gaps/Tensions) uses 7 epistemic categories while Dialectics remain tracked separately.

---

### prn_presupposition_surfacing_obligation
**"Guided workflows should actively externalize user presuppositions."**

The Concept Setup Wizard proactively identifies what users are treating as "given" through:
- Sellarsian givenness detection ("obviously", "naturally", "clearly")
- Deleuzian plane assumption analysis
- Presupposition category in Blind Spots

**Implementation:** NOTES_PREPROCESSING_PROMPT explicitly searches for givenness markers and generates presupposition-type blind spots.

---

### prn_parallel_epistemic_state_tracking
**"Epistemic gaps should be tracked as persistent, evolving state throughout a guided workflow."**

Blind spots accompany the user throughout the wizard journey:
- Identified during notes preprocessing
- Updated after Stage 1 answers (INTERIM_ANALYSIS)
- Addressed in Stage 2 questions
- Tracked alongside Dialectics as a parallel dimension

**Implementation:** `gapsTensionsQuestions` / `epistemic_blind_spots` state persists across wizard stages.

---

### prn_early_issue_confirmation_for_routing
**"Surface potential issues early and seek user confirmation before structuring downstream interrogation."**

The Validate Understanding stage:
1. Shows identified blind spots immediately after notes analysis
2. Allows user to confirm/reject/refine each one
3. Uses confirmed blind spots to structure Stage 2 questions

**Implementation:** User feedback on blind spots (`approved`, `approved_with_comment`, `rejected`, `regenerate`) routes subsequent questioning.

---

### prn_staged_adaptive_interrogation
**"Questions should build on previous answers."**

The wizard adapts based on:
- Which blind spots user confirmed as relevant
- User-marked dialectics during questioning
- Deep commitments revealed through 9-dimensional probing

**Implementation:** STAGE2_GENERATION_PROMPT references confirmed blind spots and key commitments.

---

### prn_articulation_over_resolution_questioning
**"Force users to articulate positions rather than just resolving them."**

Blind spots are framed as areas to EXPLORE, not problems to RESOLVE:
- "You don't need to resolve these now—just indicate if I've identified real blind spots"
- Stage 2 questions help articulate, not force premature closure

**Implementation:** Help text and prompts emphasize exploration over resolution.

---

## 9-Dimensional Framework as Epistemic Lens

Each of the 9 philosophical dimensions provides a different lens for identifying blind spots:

| Dimension | Blind Spot Category | What It Surfaces |
|-----------|---------------------|------------------|
| Sellarsian | Presupposition | Unexamined "givens" |
| Brandomian | Ambiguity, Likely Misreading | Perspectival content issues |
| Deleuzian | Presupposition | Plane assumptions |
| Hacking | Paradigm Dependency | Reasoning style limits |
| Bachelardian | Unconfronted Challenge | Epistemological obstacles |
| Quinean | Gray Zone | Web tensions, boundaries |
| Carey | Unfilled Slot | Placeholder structures |
| Blumenberg | Ambiguity | Metaphor-laden terms |
| Canguilhem | Gray Zone | Milieu boundaries |

---

### prn_graceful_partial_completion_validity
**"Systems should produce valid outputs from partial inputs - even 3 out of 16 answers is sufficient for meaningful analysis."**

The blind spots questioning system:
- Works with as few as 3 answers (though more is better)
- Assesses completion quality: insufficient (<3), minimal (3-5), adequate (6-9), comprehensive (10+)
- Allows early termination at any point with quality feedback

**Implementation:** `assess_completion_quality()` function and early finish button.

---

### prn_temporal_category_dispersion
**"When surfacing multiple categories of issues, distribute them temporally rather than clustering by type."**

The Curator service interleaves question categories across the session:
- Prevents user fatigue from repeated similar questions
- Allows reflection between questions on the same theme
- Uses round-robin algorithm for fair distribution

**Implementation:** `interleave_slots()` algorithm ensures questions like [ambiguity, presupposition, paradigm, ambiguity, gray_zone...] rather than [ambiguity, ambiguity, ambiguity, presupposition, presupposition...].

---

### prn_interaction_time_as_computation_budget
**"Use the time users spend on one task to generate content for subsequent tasks."**

The Sharpener service runs asynchronously while users answer questions:
- After each answer, triggers follow-up generation in background
- New questions appear 2-3 slots ahead (not immediately)
- Frontend shows "generating..." indicator for pending sharpener tasks

**Implementation:** `triggerSharpener()` runs in background, results injected via SSE events.

---

### prn_strategic_structure_before_tactical_content
**"Determine the strategic allocation and structure before generating tactical content."**

The two-stage system separates:
- **Curator (strategic)**: Analyzes notes, determines category weights, allocates slots, designs interleaved sequence
- **Sharpener (tactical)**: Generates specific follow-up questions based on actual answers

**Implementation:** Curator runs first with full notes context; Sharpener runs incrementally with answer context.

---

### prn_intent_formation_state_bifurcation
**"Systems gathering complex intent should bifurcate into distinct pathways based on user's intent-formation state—direct expression for users with formed intent versus guided discovery for users with unformed intent."**

Users arrive at blind spots questions with different levels of clarity:
- Some already know what they want to say → need **free text entry**
- Some discover their answer through options → need **multiple choice / guided options**

Forcing all users through a single flow either frustrates those who know what they want or overwhelms those who need scaffolding.

**Implementation:** "Help me articulate" button generates 4 stance-based options:
- LLM determines if options are mutually exclusive or can be combined
- Multi-select enabled when options are compatible (checkboxes)
- Single-select when options are contradictory (radio buttons)
- Write-in always available - users can add their own text alongside selections
- Final answer combines selected options + write-in for richer context

---

### prn_background_pregeneration_illusion
**"Systems should pre-generate computationally expensive content in the background while users are occupied with other tasks, creating an illusion of instant, spontaneous response."**

Users experience friction when they must wait for LLM generation. By anticipating what content they'll need next and generating it during natural interaction pauses (reading, thinking, answering), the system presents pre-computed results instantly.

Key insight: "User occupied time" is free computation budget - exploit parallelism between user cognition and machine computation.

**Implementation:** Answer options pre-generation:
- After curator completes: pre-generate options for first 2 questions
- After each answer: pre-generate options for next 3 upcoming questions
- Cache in `preGeneratedOptionsCache` keyed by slot index
- When "Help me articulate" clicked: check cache first → instant response if hit

---

## Future Directions

As the Theory Service evolves, consider:
- Tracking blind spot resolution across sessions
- Visualizing blind spot patterns across concepts
- Connecting blind spots to dialectics when appropriate
- Using blind spot history to improve initial identification

