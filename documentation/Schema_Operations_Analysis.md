# Schema Operations Analysis

## Two Types of Operations

### INTERNAL OPERATIONS (Within Database)
- Analyze relationships between concepts already in DB
- Compute consistency metrics
- Find neighborhoods/bridges
- Validate internal coherence
- Can be scheduled or triggered on concept changes

### EXTERNAL OPERATIONS (From Outside)
- Evidence testing from essay-flow clusters
- LLM analysis of concept structure
- User/expert input
- Theory source extraction
- Triggered by new evidence or manual review

---

## Field-by-Field Analysis

### Legend
- 🔵 **INTERNAL** - Computed from DB analysis
- 🟠 **EXTERNAL** - From evidence/LLM/user input
- 🟢 **HYBRID** - Can be populated/updated by either
- ⚡ **Trigger**: What causes this to be filled/updated

---

## CORE: concepts table

| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| term | 🟠 EXTERNAL | Initial import from theory source | User/extraction |
| definition | 🟠 EXTERNAL | Initial import | User/extraction |
| category | 🟠 EXTERNAL | Initial import | User/extraction |
| source_id | 🟠 EXTERNAL | Initial import | Links to theory_sources |
| status | 🟢 HYBRID | Evidence challenge OR internal review | Can be updated by evidence |
| confidence | 🟢 HYBRID | Computed from challenges OR set manually | Aggregate of dimensional confidence |
| centrality | 🔵 INTERNAL | Recompute when web changes | Count inferences, measure connectivity |
| entrenchment_score | 🔵 INTERNAL | Recompute when web changes | How many concepts depend on this |
| health_status | 🟢 HYBRID | Evidence testing OR internal analysis | Based on challenges + evolution |
| birth_period | 🟠 EXTERNAL | Initial import | Historical research |
| birth_problem | 🟠 EXTERNAL | Initial import | Historical research |
| hierarchy_level | 🔵 INTERNAL | Computed from built_from relations | Count levels in hierarchy |
| bootstrap_status | 🟢 HYBRID | LLM analysis OR evidence testing | Complex assessment |
| core_cognition_derived | 🟠 EXTERNAL | LLM analysis | Cognitive science input |

---

## QUINEAN DIMENSION

### concept_inferences
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| concept_id | 🟠 EXTERNAL | Initial setup | FK |
| inference_type | 🟠 EXTERNAL | LLM analysis of concept | forward/backward/lateral/contradiction |
| inference_statement | 🟠 EXTERNAL | LLM analysis | The inference text |
| target_concept_id | 🔵 INTERNAL | DB lookup after inference created | Match statement to existing concept |
| strength | 🟢 HYBRID | LLM estimate, updated by evidence | Can be revised down |
| defeasible | 🟠 EXTERNAL | LLM analysis | Logical property |
| challenged_at | 🟠 EXTERNAL | Evidence testing | When evidence contradicts |

**Operations needed:**
- EXTERNAL: Initial LLM analysis to extract inferences
- INTERNAL: Match `target_concept_id` to existing concepts
- EXTERNAL: Evidence testing can challenge/weaken inferences

### concept_web_tensions
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| concept_id | 🟠 EXTERNAL | Initial setup | FK |
| tension_with_concept_id | 🔵 INTERNAL | DB analysis | Find concepts with contradicting inferences |
| tension_description | 🟢 HYBRID | LLM can describe, or computed | Describe the tension |
| resolution_cost | 🔵 INTERNAL | Computed from entrenchment | How costly to resolve |

**Operations needed:**
- INTERNAL: Scan for contradictions between concept inferences
- INTERNAL: Compute resolution costs from entrenchment scores

---

## SELLARSIAN DIMENSION

### concept_givenness (1:1)
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| is_myth_of_given | 🟠 EXTERNAL | LLM analysis | Philosophical assessment |
| should_be_inferred_from | 🟠 EXTERNAL | LLM analysis | What evidence should support |
| space_of_reasons_role | 🟠 EXTERNAL | LLM analysis | Role in justification |
| manifest_scientific_tension | 🟠 EXTERNAL | LLM analysis | Everyday vs scientific |

**Operations needed:**
- EXTERNAL: LLM philosophical analysis of concept

### concept_givenness_markers
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| marker_text | 🟠 EXTERNAL | LLM analysis OR corpus search | Language markers |
| example_usage | 🟠 EXTERNAL | Evidence clusters, literature | Real examples |
| confidence | 🟢 HYBRID | Initial estimate, revised by evidence | Can be challenged |

**Operations needed:**
- EXTERNAL: LLM analysis to find markers
- EXTERNAL: Corpus search in literature/evidence for examples

### concept_givenness_effects
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| effect_type | 🟠 EXTERNAL | LLM analysis | enables/blocks |
| effect_description | 🟠 EXTERNAL | LLM analysis | What is enabled/blocked |
| confidence | 🟢 HYBRID | Initial estimate, revised by evidence | Evidence can confirm/challenge |

**Operations needed:**
- EXTERNAL: LLM philosophical analysis
- EXTERNAL: Evidence testing can confirm/challenge effects

---

## BRANDOMIAN DIMENSION

### concept_commitments
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| commitment_type | 🟠 EXTERNAL | LLM analysis | commitment/entitlement/incompatibility |
| statement | 🟠 EXTERNAL | LLM analysis | The commitment text |
| is_honored | 🟠 EXTERNAL | Evidence testing | Does practice honor this? |
| violation_evidence | 🟠 EXTERNAL | Evidence clusters | Specific violations |
| inherited_from_concept_id | 🔵 INTERNAL | DB analysis | Check if commitment comes from parent |
| challenged_at | 🟠 EXTERNAL | Evidence testing | When challenged |

**Operations needed:**
- EXTERNAL: LLM analysis to extract commitments
- INTERNAL: Check inheritance from related concepts
- EXTERNAL: Evidence testing for violations

### concept_scorekeeping
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| score_event | 🟠 EXTERNAL | Evidence testing | What changed |
| commitment_id | 🔵 INTERNAL | FK lookup | Which commitment affected |
| score_change | 🟠 EXTERNAL | Evidence analysis | gained/lost/challenged |
| evidence_source | 🟠 EXTERNAL | Evidence cluster ref | What evidence triggered |

**Operations needed:**
- EXTERNAL: Log score changes from evidence testing

---

## DELEUZIAN DIMENSION (Revised)

### concept_components
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| component_name | 🟠 EXTERNAL | LLM analysis | What are the parts? |
| component_description | 🟠 EXTERNAL | LLM analysis | What each contributes |
| is_intensive | 🟠 EXTERNAL | LLM analysis | Philosophical property |
| order_index | 🟠 EXTERNAL | LLM analysis | Structure position |

**Operations needed:**
- EXTERNAL: LLM philosophical analysis to decompose concept

### concept_zones_of_indiscernibility
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| component_a_id | 🔵 INTERNAL | From components | FK |
| component_b_id | 🔵 INTERNAL | From components | FK |
| zone_description | 🟠 EXTERNAL | LLM analysis | What passes between |
| what_becomes_possible | 🟠 EXTERNAL | LLM analysis | What zone enables |

**Operations needed:**
- INTERNAL: Generate pairs from components
- EXTERNAL: LLM analysis of what happens in each zone

### concept_consistency
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| endoconsistency_description | 🟠 EXTERNAL | LLM analysis | How components hold |
| survey_point | 🟠 EXTERNAL | LLM analysis | Unifying point |
| consistency_strength | 🟢 HYBRID | LLM estimate, revised by evidence | Can weaken |

**Operations needed:**
- EXTERNAL: LLM philosophical analysis
- EXTERNAL: Evidence can challenge consistency

### concept_neighborhood
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| neighbor_concept_id | 🔵 INTERNAL | DB search | Find related concepts in DB |
| neighbor_description | 🟠 EXTERNAL | LLM if not in DB | Describe relation |
| relation_type | 🟢 HYBRID | LLM analysis OR computed | bridge/resonance/interference |
| neighborhood_order | 🔵 INTERNAL | Computed from relations | Distance in web |
| bridges_across_plane | 🔵 INTERNAL | Compare planes of concepts | Different plane_of_immanence? |

**Operations needed:**
- INTERNAL: Search DB for concepts with shared inferences/components
- INTERNAL: Compute neighborhood_order from web distance
- INTERNAL: Check if planes differ for bridge detection

### concept_plane_of_immanence
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| plane_name | 🟠 EXTERNAL | LLM/historical analysis | What plane? |
| what_plane_presupposes | 🟠 EXTERNAL | LLM analysis | Unthought assumptions |
| legitimate_problems | 🟠 EXTERNAL | LLM analysis | What can be asked |
| excluded_problems | 🟠 EXTERNAL | LLM analysis | What can't be asked |
| historical_emergence | 🟠 EXTERNAL | Historical research | When plane emerged |

**Operations needed:**
- EXTERNAL: LLM philosophical/historical analysis

### concept_personae
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| persona_name | 🟠 EXTERNAL | LLM analysis | Who thinks with this? |
| persona_description | 🟠 EXTERNAL | LLM analysis | What persona does |
| what_persona_enables | 🟠 EXTERNAL | LLM analysis | What thinking enabled |
| historical_origin | 🟠 EXTERNAL | Historical research | Where from |

**Operations needed:**
- EXTERNAL: LLM philosophical analysis

### concept_problems
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| problem_statement | 🟠 EXTERNAL | LLM analysis | What problem addressed |
| problem_type | 🟠 EXTERNAL | LLM classification | political/epistemological/etc |
| triggering_event | 🟠 EXTERNAL | Historical/current events | What made problem pressing |
| how_concept_responds | 🟠 EXTERNAL | LLM analysis | How concept addresses |
| problem_transformed_to | 🟢 HYBRID | LLM analysis OR evidence | How problem changes |

**Operations needed:**
- EXTERNAL: LLM philosophical/historical analysis
- EXTERNAL: Evidence can show problem transformation

---

## BACHELARDIAN DIMENSION

### concept_obstacles
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| is_obstacle | 🟢 HYBRID | LLM analysis, confirmed by evidence | Does it block? |
| obstacle_type | 🟠 EXTERNAL | LLM classification | Type of obstacle |
| why_persists | 🟠 EXTERNAL | LLM analysis | Ideological function |
| rupture_would_enable | 🟠 EXTERNAL | LLM analysis | What rupture allows |
| rupture_trigger | 🟠 EXTERNAL | LLM analysis | What would cause rupture |
| psychoanalytic_function | 🟠 EXTERNAL | LLM analysis | Unconscious need |
| epistemological_profile | 🟠 EXTERNAL | LLM analysis | Progress scale position |

**Operations needed:**
- EXTERNAL: LLM philosophical analysis
- EXTERNAL: Evidence can confirm/strengthen obstacle assessment

### concept_obstacle_blocks
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| blocked_understanding | 🟠 EXTERNAL | LLM analysis | What's blocked |
| confidence | 🟢 HYBRID | LLM estimate, evidence confirms | Evidence can confirm |

### concept_inadequacy_evidence
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| evidence_description | 🟠 EXTERNAL | Evidence clusters | Empirical challenge |
| source_cluster_id | 🟠 EXTERNAL | Essay-flow reference | Where evidence came from |
| confidence | 🟠 EXTERNAL | Evidence analysis | How strong |

**Operations needed:**
- EXTERNAL: Evidence testing populates this table

---

## CANGUILHEM DIMENSION

### concept_evolution
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| period | 🟠 EXTERNAL | Historical research | When |
| transformation_description | 🟠 EXTERNAL | Historical research | What changed |
| problem_driving | 🟠 EXTERNAL | Historical research | Why |
| who_transformed | 🟠 EXTERNAL | Historical research | Who |
| predecessor_concept_id | 🔵 INTERNAL | DB lookup | Link to earlier form |

**Operations needed:**
- EXTERNAL: Historical research/LLM analysis
- INTERNAL: Match predecessor to existing concepts

### concept_normative_dimensions
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| value_embedded | 🟠 EXTERNAL | LLM analysis | What value |
| whose_values | 🟠 EXTERNAL | LLM analysis | Who benefits |
| what_excluded | 🟠 EXTERNAL | LLM analysis | What's abnormalized |
| normal_vs_normative | 🟠 EXTERNAL | LLM analysis | Type |

### concept_vitality_indicators
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| indicator_type | 🟢 HYBRID | Evidence OR internal metrics | Type of health sign |
| indicator_description | 🟠 EXTERNAL | Evidence/observation | What shows health |
| observed_at | 🟠 EXTERNAL | When observed | Timestamp |

**Operations needed:**
- EXTERNAL: Evidence testing can add vitality indicators
- INTERNAL: Aggregate from challenges, compute health trends

---

## DAVIDSON/HACKING DIMENSION

### concept_reasoning_styles
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| style_name | 🟠 EXTERNAL | LLM analysis | What style |
| style_emerged | 🟠 EXTERNAL | Historical research | When |
| objects_created | 🟠 EXTERNAL | LLM analysis | What style creates |

### concept_style_visibility
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| visibility_type | 🟠 EXTERNAL | LLM analysis | visible/invisible |
| what_affected | 🟠 EXTERNAL | LLM analysis | What's visible/invisible |
| confidence | 🟢 HYBRID | LLM estimate, evidence confirms | Can be tested |

### concept_style_evidence
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| evidence_status | 🟠 EXTERNAL | LLM analysis | privileged/marginalized |
| evidence_type | 🟠 EXTERNAL | LLM analysis | What type |

### concept_style_inferences
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| inference_pattern | 🟠 EXTERNAL | LLM analysis | Characteristic move |

---

## BLUMENBERG DIMENSION

### concept_metaphors
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| root_metaphor | 🟠 EXTERNAL | LLM analysis | The metaphor |
| source_domain | 🟠 EXTERNAL | LLM analysis | Where from |
| is_absolute | 🟠 EXTERNAL | LLM analysis | Can't be conceptualized? |
| nonconceptuality_aspect | 🟠 EXTERNAL | LLM analysis | What resists |

### concept_metaphor_effects
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| effect_type | 🟠 EXTERNAL | LLM analysis | enables/hides |
| effect_description | 🟠 EXTERNAL | LLM analysis | What |
| confidence | 🟢 HYBRID | LLM estimate, evidence tests | Can be revised |

### concept_metakinetics
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| period | 🟠 EXTERNAL | Historical research | When |
| transformation | 🟠 EXTERNAL | Historical research | How meaning shifted |

### concept_work_in_progress
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| original_meaning | 🟠 EXTERNAL | Historical research | Original |
| current_work | 🟠 EXTERNAL | LLM/observation | Current transformation |
| who_doing_work | 🟠 EXTERNAL | Research | Who |
| work_status | 🟢 HYBRID | Observation, evidence | succeeding/failing |

---

## CAREY DIMENSION

### concept_hierarchy
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| combination_type | 🟠 EXTERNAL | LLM analysis | How combined |
| transparency | 🟠 EXTERNAL | LLM analysis | How visible |
| bootstrap_failure_reason | 🟢 HYBRID | LLM analysis OR evidence | Why failed |
| what_would_fix | 🟠 EXTERNAL | LLM analysis | Remedy |
| incommensurable_with | 🟠 EXTERNAL | LLM analysis | Can't be reduced to |

### concept_built_from
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| component_concept_id | 🔵 INTERNAL | DB lookup | If component in DB |
| component_description | 🟠 EXTERNAL | LLM analysis | Description |
| component_level | 🔵 INTERNAL | Computed | Hierarchy level |
| how_combined | 🟠 EXTERNAL | LLM analysis | Combination method |

**Operations needed:**
- EXTERNAL: LLM analysis to identify building blocks
- INTERNAL: Match to existing concepts, compute levels

### concept_mapping_process
| Field | Source | Trigger | Notes |
|-------|--------|---------|-------|
| mapping_type | 🟠 EXTERNAL | Cognitive analysis | fast/extended |
| mapping_description | 🟠 EXTERNAL | LLM/cognitive analysis | How acquired |
| executive_function_needed | 🟠 EXTERNAL | LLM/cognitive analysis | Cognitive effort |

---

## Summary: Operation Types

### INTERNAL OPERATIONS (can be scheduled/automated)

1. **Compute centrality** - Count inferences, measure connectivity
2. **Compute entrenchment** - How many concepts depend on this
3. **Find neighborhoods** - Match concepts by shared inferences/components
4. **Detect tensions** - Find contradicting inferences between concepts
5. **Compute hierarchy levels** - Count levels in built_from relations
6. **Match to existing concepts** - Find target_concept_id, neighbor_concept_id, etc.
7. **Check plane bridges** - Compare plane_of_immanence across neighbors
8. **Aggregate health** - Compute vitality from challenges, indicators

### EXTERNAL OPERATIONS (triggered by events)

1. **Initial concept extraction** - From theory sources (LLM)
2. **Philosophical analysis** - Decompose concept across 9 dimensions (LLM)
3. **Evidence testing** - Check evidence clusters against concept claims
4. **Challenge processing** - Update confidence, add violations, log score changes
5. **Historical research** - Fill evolution, metakinetics, emergence periods
6. **User/expert input** - Manual corrections and additions

### TRIGGERS

| Trigger | Operations |
|---------|------------|
| **New concept added** | Run full philosophical analysis (LLM), compute initial centrality/entrenchment |
| **Concept modified** | Recompute centrality for neighbors, check tensions |
| **Evidence cluster received** | Run evidence testing, update confidences, add inadequacy_evidence |
| **Scheduled job** | Recompute all internal metrics, health aggregation |
| **Manual review** | Expert corrections, status updates |

---

## Schema Enhancement: Add Source Tracking

Every table should have:

```sql
-- Who/what populated this row
source_type VARCHAR(20),  -- 'llm_analysis', 'evidence_testing', 'internal_compute', 'user_input', 'import'
source_reference TEXT,    -- LLM model, cluster_id, user_id, etc.
```

This allows:
- Tracking provenance of every claim
- Knowing what can be recomputed vs. what needs external input
- Understanding which evidence challenged which claim
