# Enriched Concept Schema - 9-Dimensional Analysis Framework

## Overview

This schema captures the deep structure of theoretical concepts based on 9 philosophical frameworks:
1. **Quinean** - Web of Belief (inferential connections, centrality)
2. **Sellarsian** - Inferential Roles (givenness, proper inference)
3. **Brandomian** - Social Practices (commitments, entitlements)
4. **Deleuzian** - Problems & Plane (what problems concept addresses)
5. **Bachelardian** - Obstacles (does concept block understanding?)
6. **Canguilhem** - Life History (birth, evolution, health status)
7. **Davidson** - Reasoning Styles (what style enables/requires)
8. **Blumenberg** - Metaphorology (root metaphors, conceptual work)
9. **Carey** - Bootstrapping (hierarchy level, what it's built from)

## Database Schema

### Core Concept Table (Extended)

```sql
-- Extended concept table with deep structure
ALTER TABLE concepts ADD COLUMN IF NOT EXISTS
    -- Basic metadata (existing)
    -- term, definition, category, status, confidence...

    -- 1. QUINEAN: Web Position
    centrality VARCHAR(20),  -- core, intermediate, peripheral
    web_coherence_impact TEXT,  -- how changing this affects other concepts

    -- 6. CANGUILHEM: Life History
    health_status VARCHAR(20),  -- healthy, strained, dying, being_born
    birth_period VARCHAR(100),  -- when concept emerged
    birth_problem TEXT,  -- what problem it was created to solve

    -- 9. CAREY: Hierarchy
    hierarchy_level INTEGER,  -- 0=primitive, 1=simple, 2=complex, 3+=bootstrapped
    bootstrap_status VARCHAR(20);  -- successful, partial, failed, attempted

-- 2. QUINEAN: Inferential Connections
CREATE TABLE IF NOT EXISTS concept_inferences (
    id SERIAL PRIMARY KEY,
    concept_id INTEGER REFERENCES concepts(id) ON DELETE CASCADE,

    inference_type VARCHAR(30) NOT NULL,  -- forward, backward, lateral, contradiction
    inference_statement TEXT NOT NULL,  -- "If X, then Y" or "X because Y"
    target_concept_id INTEGER REFERENCES concepts(id),  -- related concept if any
    strength FLOAT DEFAULT 0.8,  -- how strong is this inference

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. SELLARSIAN: Givenness Analysis
CREATE TABLE IF NOT EXISTS concept_givenness (
    id SERIAL PRIMARY KEY,
    concept_id INTEGER REFERENCES concepts(id) ON DELETE CASCADE,

    is_myth_of_given BOOLEAN DEFAULT FALSE,  -- is it falsely treated as foundational?
    givenness_markers TEXT[],  -- ["obviously", "naturally", "of course"]

    should_be_inferred_from TEXT,  -- what evidence/argument should support it
    theoretical_commitments_embedded TEXT[],  -- hidden assumptions

    what_givenness_enables TEXT,  -- what does treating as given allow
    what_givenness_blocks TEXT,  -- what questions become unaskable

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. BRANDOMIAN: Commitments & Entitlements
CREATE TABLE IF NOT EXISTS concept_commitments (
    id SERIAL PRIMARY KEY,
    concept_id INTEGER REFERENCES concepts(id) ON DELETE CASCADE,

    commitment_type VARCHAR(30) NOT NULL,  -- commitment, entitlement, incompatibility
    statement TEXT NOT NULL,  -- what you're committed to / entitled to

    is_honored BOOLEAN,  -- is this commitment actually honored in practice?
    violation_evidence TEXT,  -- if violated, where/how

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. DELEUZIAN: Problems & Plane
CREATE TABLE IF NOT EXISTS concept_problems (
    id SERIAL PRIMARY KEY,
    concept_id INTEGER REFERENCES concepts(id) ON DELETE CASCADE,

    problem_addressed TEXT NOT NULL,  -- what tension/problem does concept navigate
    tension_pole_a TEXT,  -- one side of tension
    tension_pole_b TEXT,  -- other side

    creative_responses TEXT[],  -- how concept helps navigate problem
    becomings_enabled TEXT[],  -- what transformations does concept enable
    becomings_blocked TEXT[],  -- what transformations does concept prevent

    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS concept_plane_assumptions (
    id SERIAL PRIMARY KEY,
    concept_id INTEGER REFERENCES concepts(id) ON DELETE CASCADE,

    assumption TEXT NOT NULL,  -- unquestioned background assumption
    makes_possible TEXT[],  -- what concepts/thinking this enables
    makes_impossible TEXT[],  -- what's foreclosed by this assumption

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. BACHELARDIAN: Obstacle Analysis
CREATE TABLE IF NOT EXISTS concept_obstacles (
    id SERIAL PRIMARY KEY,
    concept_id INTEGER REFERENCES concepts(id) ON DELETE CASCADE,

    is_obstacle BOOLEAN DEFAULT FALSE,  -- does this concept block understanding?
    obstacle_type VARCHAR(30),  -- experience, verbal, pragmatic, quantitative, substantialist

    what_it_blocks TEXT[],  -- what understanding/questions it prevents
    evidence_of_inadequacy TEXT[],  -- empirical challenges to concept
    why_persists TEXT,  -- ideological/class function

    rupture_would_enable TEXT,  -- what becomes thinkable after rupture
    rupture_trigger TEXT,  -- what would force abandonment

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. CANGUILHEM: Life History Details
CREATE TABLE IF NOT EXISTS concept_evolution (
    id SERIAL PRIMARY KEY,
    concept_id INTEGER REFERENCES concepts(id) ON DELETE CASCADE,

    period VARCHAR(100) NOT NULL,  -- time period of transformation
    transformation_description TEXT NOT NULL,
    problem_driving TEXT,  -- what problem drove this change
    who_transformed TEXT,  -- intellectual tradition, institution

    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS concept_normative_dimensions (
    id SERIAL PRIMARY KEY,
    concept_id INTEGER REFERENCES concepts(id) ON DELETE CASCADE,

    value_embedded TEXT NOT NULL,  -- what value is embedded
    whose_values TEXT,  -- whose interests does this serve
    what_excluded TEXT,  -- what's marked as "abnormal" or excluded

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8. DAVIDSON: Reasoning Style
CREATE TABLE IF NOT EXISTS concept_reasoning_styles (
    id SERIAL PRIMARY KEY,
    concept_id INTEGER REFERENCES concepts(id) ON DELETE CASCADE,

    style_required VARCHAR(100) NOT NULL,  -- financial, geopolitical, technical, etc.

    what_visible TEXT[],  -- what this style makes visible
    what_invisible TEXT[],  -- what's systematically hidden

    evidence_types_privileged TEXT[],  -- what counts as evidence in this style
    inference_patterns TEXT[],  -- characteristic reasoning moves

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 9. BLUMENBERG: Metaphorology
CREATE TABLE IF NOT EXISTS concept_metaphors (
    id SERIAL PRIMARY KEY,
    concept_id INTEGER REFERENCES concepts(id) ON DELETE CASCADE,

    root_metaphor TEXT NOT NULL,  -- e.g., "market as organism"
    source_domain TEXT,  -- where metaphor comes from

    what_metaphor_enables TEXT[],  -- what thinking it makes possible
    what_metaphor_hides TEXT[],  -- what it obscures

    resists_conceptualization BOOLEAN DEFAULT FALSE,  -- is this an absolute metaphor?
    why_resists TEXT,  -- why can't it be made precise

    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS concept_work_in_progress (
    id SERIAL PRIMARY KEY,
    concept_id INTEGER REFERENCES concepts(id) ON DELETE CASCADE,

    original_meaning TEXT,  -- what concept meant originally
    current_work TEXT NOT NULL,  -- what transformation is being attempted
    who_doing_work TEXT,  -- intellectual tradition, actors
    work_status VARCHAR(30),  -- succeeding, failing, ongoing

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 10. CAREY: Bootstrapping Details
CREATE TABLE IF NOT EXISTS concept_hierarchy (
    id SERIAL PRIMARY KEY,
    concept_id INTEGER REFERENCES concepts(id) ON DELETE CASCADE,

    built_from_concept_ids INTEGER[],  -- concepts this is bootstrapped from
    built_from_descriptions TEXT[],  -- how components combine

    combination_type VARCHAR(30),  -- simple_aggregation, interactive, qualitative_leap
    transparency VARCHAR(20),  -- high, medium, low (how visible are components)

    bootstrap_failure_reason TEXT,  -- if failed, why
    what_would_fix TEXT,  -- what would make bootstrap succeed

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for fast lookups
CREATE INDEX IF NOT EXISTS idx_concept_inferences_concept ON concept_inferences(concept_id);
CREATE INDEX IF NOT EXISTS idx_concept_inferences_type ON concept_inferences(inference_type);
CREATE INDEX IF NOT EXISTS idx_concept_commitments_concept ON concept_commitments(concept_id);
CREATE INDEX IF NOT EXISTS idx_concept_problems_concept ON concept_problems(concept_id);
CREATE INDEX IF NOT EXISTS idx_concept_obstacles_concept ON concept_obstacles(concept_id);
CREATE INDEX IF NOT EXISTS idx_concept_evolution_concept ON concept_evolution(concept_id);
CREATE INDEX IF NOT EXISTS idx_concept_metaphors_concept ON concept_metaphors(concept_id);
CREATE INDEX IF NOT EXISTS idx_concept_hierarchy_concept ON concept_hierarchy(concept_id);
```

## Challenge Impact Analysis

When a cluster impacts a concept, analyze across ALL 9 dimensions:

```sql
-- Enhanced challenge analysis table
CREATE TABLE IF NOT EXISTS challenge_dimensional_impact (
    id SERIAL PRIMARY KEY,
    challenge_id INTEGER REFERENCES challenges(id) ON DELETE CASCADE,
    concept_id INTEGER REFERENCES concepts(id) ON DELETE CASCADE,

    -- 1. QUINEAN: How does evidence affect inferential web?
    inferences_challenged TEXT[],  -- which inferences does evidence contradict
    centrality_impact VARCHAR(30),  -- does this move concept core→peripheral or vice versa
    web_tension_created TEXT,  -- what new tensions emerge

    -- 2. SELLARSIAN: Does evidence expose givenness myths?
    givenness_exposed BOOLEAN,  -- does evidence show concept falsely treated as given
    proper_inference_revealed TEXT,  -- what should concept actually be inferred from

    -- 3. BRANDOMIAN: Does evidence show commitment violations?
    commitments_violated TEXT[],  -- which commitments does evidence show broken
    entitlements_exceeded TEXT[],  -- claims beyond what evidence supports

    -- 4. DELEUZIAN: Does evidence reveal new problems?
    new_problems_revealed TEXT[],  -- what tensions does evidence expose
    lines_of_flight_opened TEXT[],  -- what escape routes become visible
    becomings_blocked_exposed TEXT[],  -- what transformations shown impossible

    -- 5. BACHELARDIAN: Does evidence show concept is obstacle?
    obstacle_evidence TEXT,  -- how does evidence show concept blocks understanding
    rupture_potential VARCHAR(20),  -- high, moderate, low

    -- 6. CANGUILHEM: How does evidence affect concept health?
    health_impact VARCHAR(20),  -- improving, worsening, neutral
    evolution_direction TEXT,  -- where is concept heading based on evidence

    -- 7. DAVIDSON: Does evidence require different reasoning style?
    style_inadequacy_revealed TEXT,  -- what style limitations does evidence expose
    new_style_needed TEXT,  -- what reasoning approach would work better

    -- 8. BLUMENBERG: Does evidence expose metaphor limitations?
    metaphor_strain_revealed TEXT,  -- how does evidence strain root metaphors
    conceptual_work_needed TEXT,  -- what transformation work is required

    -- 9. CAREY: Does evidence challenge bootstrap?
    hierarchy_impact TEXT,  -- does evidence show bootstrap failing
    rebuild_required BOOLEAN,  -- does concept need to be rebuilt from different primitives

    -- Summary
    overall_impact_severity VARCHAR(20),  -- minor, moderate, major, transformative
    recommended_response VARCHAR(30),  -- accept, refine, extend, rupture

    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Example: Analyzing "Technological Sovereignty"

```json
{
  "concept": "Technological Sovereignty",
  "definition": "A state's capacity to control its own technological development and infrastructure",

  "quinean_web": {
    "centrality": "intermediate",
    "forward_inferences": [
      "If tech sovereignty, then indigenous chip development possible",
      "If tech sovereignty, then reduced foreign dependency"
    ],
    "contradictions": ["Material dependency evidence", "Equipment imports"]
  },

  "sellarsian_givenness": {
    "is_myth_of_given": true,
    "givenness_markers": ["naturally", "clearly possible", "inevitable"],
    "should_be_inferred_from": "Analysis of actual material capacity, supply chains, knowledge dependencies",
    "what_givenness_blocks": "Questions about structural impossibility of sovereignty under current conditions"
  },

  "brandomian_commitments": {
    "commitments": [
      {"type": "commitment", "statement": "Autonomy achievable through investment", "honored": false},
      {"type": "entitlement", "statement": "Can claim sovereignty through rhetoric", "exceeded": true}
    ],
    "violations": "Claims sovereignty while evidence shows dependency"
  },

  "deleuzian_problems": {
    "problem_addressed": "How to claim autonomy while remaining dependent",
    "tension_poles": ["Political need for sovereignty rhetoric", "Material reality of dependency"],
    "becomings_blocked": "Genuine autonomy (requires system exit)",
    "becomings_enabled": "Performative sovereignty (claims without substance)"
  },

  "bachelardian_obstacle": {
    "is_obstacle": true,
    "obstacle_type": "verbal",
    "what_it_blocks": "Recognition of structural dependency, analysis of power asymmetries",
    "evidence_of_inadequacy": ["Gulf $2T but can't invest autonomously", "China depends on ASML"],
    "rupture_would_enable": "Honest analysis of dependency, new strategies"
  },

  "canguilhem_life": {
    "health_status": "strained",
    "birth_period": "2010s (US-China tech tensions)",
    "birth_problem": "How to mobilize resources for tech independence",
    "evolution": [
      {"period": "1648", "form": "Territorial sovereignty"},
      {"period": "1950s-70s", "form": "Economic sovereignty"},
      {"period": "2010s+", "form": "Technological sovereignty"}
    ],
    "trajectory": "Either dies (exposed as impossible) or transforms (sovereignty-within-subordination)"
  },

  "davidson_style": {
    "style_required": "geopolitical_realism",
    "makes_visible": ["State competition", "Strategic sectors", "National interest"],
    "makes_invisible": ["Class dynamics", "Capital interests", "Impossibility of autonomy"]
  },

  "blumenberg_metaphor": {
    "root_metaphor": "Sovereignty as territorial possession",
    "source_domain": "Territorial/military control",
    "what_enables": "Thinking tech can be 'owned' like territory",
    "what_hides": "Technology is networked, distributed, requires ongoing relationships",
    "resists_conceptualization": true,
    "why": "Territory and technology have fundamentally different autonomy conditions"
  },

  "carey_hierarchy": {
    "level": 3,
    "built_from": ["Sovereignty (state+territory+autonomy)", "Technology domain"],
    "bootstrap_status": "failed",
    "failure_reason": "Territorial sovereignty logic doesn't transfer to technology domain",
    "what_would_fix": "New concept: 'Strategic positioning' or 'Dependency management'"
  }
}
```

## Evidence Cluster Impact Analysis Template

When evidence impacts "Technological Sovereignty":

| Dimension | Question | Evidence Finding | Impact |
|-----------|----------|------------------|--------|
| **Quinean** | Does evidence contradict inferences? | Gulf has $2T but can't invest at Series B | Breaks "investment → autonomy" inference |
| **Sellarsian** | Does evidence expose givenness? | Shows sovereignty assumed not proven | Reveals myth of given |
| **Brandomian** | Are commitments violated? | Claims autonomy, evidence shows dependency | Major violation |
| **Deleuzian** | New problems revealed? | How to maintain legitimacy without capacity | Yes, new tension |
| **Bachelardian** | Evidence of obstacle? | Concept prevents seeing structural dependency | Yes, blocking |
| **Canguilhem** | Health impact? | Evidence shows concept failing | Worsening |
| **Davidson** | Style inadequacy? | Geopolitical frame misses class/capital | Yes |
| **Blumenberg** | Metaphor strained? | Territory metaphor breaking | Yes |
| **Carey** | Bootstrap failing? | Can't achieve Level 3 leap | Yes |

**Recommendation**: This concept requires **rupture** not refinement.

## Benefits of Enriched Schema

1. **Structured Analysis**: When cluster impacts concept, analyze systematically across 9 dimensions
2. **Deeper Insights**: Understand WHY concept is strained, not just THAT it's challenged
3. **Better Recommendations**: LLM can recommend accept/refine/rupture based on multi-dimensional analysis
4. **Conceptual Evolution**: Track how concepts change over time across all dimensions
5. **Cross-Concept Patterns**: Find concepts with similar structural issues
