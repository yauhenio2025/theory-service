# Theory Service Features Log

This document tracks major features introduced to the Theory Service application.

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

