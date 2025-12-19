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

## Future Directions

As the Theory Service evolves, consider:
- Tracking blind spot resolution across sessions
- Visualizing blind spot patterns across concepts
- Connecting blind spots to dialectics when appropriate
- Using blind spot history to improve initial identification

