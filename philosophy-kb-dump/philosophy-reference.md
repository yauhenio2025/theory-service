# Philosophy Knowledge Base Reference

*Exported: 2025-12-26 11:05:03*

**159 principles** | **239 features** | **70 groundings**

---

# Principles

## Design

### `prn_approval_initiation_agency_bifurcation`

**User agency should be explicitly designed into distinct modes—reactive approval (evaluating and signing off on system-proposed changes) versus proactive initiation (articulating reasons for user-perceived needed changes)—with interface affordances, cognitive demands, and information requirements matched to each mode.
**

*Rationale:* These modes have different cognitive requirements: approval requires evaluation of presented options while initiation requires generation of justification. Conflating them creates interfaces that either demand unnecessary articulation for simple approvals or provide insufficient scaffolding for interpretive reframing.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `sign-off-vs-articulation-interface-bifurcation` - Sign-Off vs Articulation Interface Bifurcation


### `prn_asymmetric_choice_architecture`

**When presenting "choose A over B, C, D" decisions, structure information asymmetrically:  the selected option receives commitment framing (what you're choosing, why), while each  rejected alternative receives foreclosure framing (what specific value this alternative  offered that you're now passing on)—not as equal comparands but as commitment-plus-cost.
**

*Rationale:* This architectural pattern helps users understand choices as commitments with specific  costs rather than as selections from equivalent options. It supports more informed  decision-making by making opportunity costs concrete and option-specific.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `resolution-path-virtualization-panel` - Resolution Path Virtualization Panel
- `per-alternative-foreclosure-articulation` - Per-Alternative Foreclosure Articulation
- `commitment-plus-foreclosure-panel` - Commitment-Plus-Foreclosure Panel


### `prn_automated_staleness_detection`

**Systems with interdependent structures should include monitoring mechanisms that automatically detect when upstream changes have rendered downstream elements stale, surfacing inconsistency through alerts before users encounter drift organically, because manual coherence monitoring fails as system complexity increases.
**

*Rationale:* This principle separates DETECTION of staleness from REMEDIATION of staleness. Many systems handle remediation but leave detection to users. Automated detection shifts the burden from user vigilance to system monitoring, enabling humans to focus on resolution rather than identification.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `dynamic-coherence-as-system-property` - Dynamic Coherence as System Property
- `staleness-detection-monitor-pattern` - Staleness Detection Monitor Pattern


### `prn_background_pregeneration_illusion`

**Systems should pre-generate computationally expensive content in the background while users are occupied with other tasks, creating an illusion of instant, spontaneous response when the content is requested.**

*Rationale:* Users experience friction when they must wait for generation. By anticipating what content they'll need next and generating it during natural interaction pauses (reading, thinking, answering), systems can present pre-computed results instantly. This transforms perceived latency into perceived responsiveness without changing actual computation time. The key insight is that 'user occupied time' is free computation budget - the system should exploit parallelism between user cognition and machine computation.

*Tags:* ux, latency, background-generation, anticipation, illusion, parallelism

**Embodied by features:**
- `answer-options-pre-generation` - Answer Options Pre-Generation


### `prn_cognitive_task_matched_presentation`

**Match information presentation format to the cognitive task it supports—comparison requires parallel structure, evaluation requires hierarchical structure, exploration requires expandable structure—because format shapes cognitive efficiency.**

*Rationale:* **Evidence from source:** The demoted principle describes formatting for scanability and comparison, suggesting task-specific presentation.

**Why this matters:** The same information presented differently enables or inhibits different cognitive operations. Format is not neutral.

**Structural kinship:** prn_decision_interface_modality_matching, prn_detail_deferral_with_accessibility, prn_visual_state_legibility

**Embodied by features:**
- `sign-off-vs-articulation-interface-bifurcation` - Sign-Off vs Articulation Interface Bifurcation
- `pre-allocated-slot-interleaving` - Pre-Allocated Slot Interleaving
- `cognitive-task-to-scaffolding-modality-matching` - Cognitive Task to Scaffolding Modality Matching
  *specializes*
- `feat_structured_decision_presentation` - Structured Decision Presentation
  *Created by refactoring engine*


### `prn_confirmation_resolution_separation`

**Separate the act of confirming that an uncertainty exists and merits attention from 
the act of resolving it, because confirmation is a lower-commitment cognitive operation 
that preserves user agency and prevents defensive closure.
**

*Rationale:* When LLM systems detect gaps or tensions in user thinking, the natural response is 
to ask users to fix them. This conflates two distinct acts. Users can productively 
confirm "yes, this is genuinely uncertain" without having an answer. Systems that 
demand resolution lose the signal value of confirmed-but-unresolved uncertainties 
and trigger defensive closure.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `confirm-then-route-interrogation-pattern` - Confirm-Then-Route Interrogation Pattern
- `agency-preserving-response-options` - Agency-Preserving Response Options
- `confirm-explore-articulate-flow` - Confirm-Explore-Articulate Flow


### `prn_consumer_optimized_representation`

**Design information representations optimized for their primary consumer's cognitive architecture—whether human visual processing, algorithmic parsing, or hybrid interpretation—rather than assuming universal readability.**

*Rationale:* **Evidence from source:** The demoted principle explicitly optimizes for LLM consumption, suggesting a general pattern of consumer-driven design.

**Why this matters:** Different consumers (humans, algorithms, hybrid systems) have fundamentally different processing capabilities and constraints. Optimizing for the wrong consumer creates friction.

**Structural kinship:** prn_machine_legible_affordances, prn_explicit_capability_declaration, prn_context_driven_generation

**Embodied by features:**
- `feat_llm_optimized_data_structures` - LLM-Optimized Data Structures
  *Created by refactoring engine*


### `prn_context_driven_generation`

**When generation costs are low, adapt outputs to specific contexts and data rather than forcing contexts to fit generic templates—personalization should be the default, not the exception, with systems generating bespoke artifacts tailored to actual use conditions.**

*Rationale:* **Evidence from source:** Merged from prn_generative_personalization (personalization default), prn_context_specific_adaptation (context adaptation), and prn_bespoke_contextual (bespoke artifacts).

**Why this matters:** Generic templates force users to adapt to system constraints. When generation is cheap, systems should adapt to users instead.

**Structural kinship:** prn_late_binding_specialization, prn_user_centered_design, prn_resource_proportionality


### `prn_data_as_program`

**Treat data as executable specification—when data structures are sufficiently rich and systems sufficiently generic, data can define behavior without explicit programming, collapsing the distinction between configuration and code.**

*Rationale:* **Evidence from source:** The demoted principle describes context functioning as configuration, suggesting data-driven behavior.

**Why this matters:** Traditional separation of code and data creates artificial boundaries. Rich data structures can encode behavioral specifications.

**Structural kinship:** prn_machine_legible_affordances, prn_explicit_capability_declaration, prn_late_binding_semantic_labels

**Embodied by features:**
- `feat_context_driven_system_specialization` - Context-Driven System Specialization
  *Created by refactoring engine*


### `prn_deficit_neutral_uncertainty_framing`

**Present detected conceptual incompleteness as natural developmental material rather 
than as flaws requiring correction, because deficit-framed feedback triggers 
defensiveness that inhibits collaborative development.
**

*Rationale:* Concept development tools must present feedback about incompleteness in a way that 
invites engagement rather than defense. The same information ("you haven't fully 
worked out X") can be framed as "your thinking is flawed" or "here's fertile 
territory to explore"—the frame determines whether users lean in or push back.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `agency-preserving-response-options` - Agency-Preserving Response Options


### `prn_dual_consumer_structure_design`

**Intermediate representational structures should be designed to simultaneously  serve the producing system (improving its reasoning quality through structured  externalization requirements) AND the consuming humans (enabling audit,  verification, and iterative improvement of the system).
**

*Rationale:* Separating "structures for LLM processing" from "structures for human audit"  creates maintenance burden and misalignment. Dual-consumer design unifies these,  making the same structure serve both improvement and accountability.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `bidirectional-improvement-loop-architecture` - Bidirectional Improvement Loop Architecture


### `prn_fixed_foundation`

**Not everything should be fluid and customizable—certain elements must remain fixed and stable to provide reference points, because understanding and navigation require stable ground from which to perceive variation.**

*Rationale:* Total flexibility is paralyzing. Without constraints, there's no basis for
meaningful variation. A jazz musician improvises within the structure of
chord changes; without that structure, it's just noise.

Fixed elements provide:
- Cognitive anchors for users
- Evaluation criteria for outputs
- Consistent foundations across variations
- Limits that force creative solutions

The key is choosing WHAT to fix. Fix the process structure, not the content.
Fix the evaluation criteria, not the outputs. Fix the interaction patterns,
not the specific interfaces.


*Tags:* constraints, flexibility, grounding, architecture

**Embodied by features:**
- `eternal-ephemeral-extraction-dichotomy` - Eternal-Ephemeral Extraction Dichotomy
- `ai-indispensability-declaration` - AI Indispensability Declaration
  *LLM role declared as fixed architectural constraint*
- `family-strategies-system` - Family Strategies System
  *Strategies form a stable repertoire of approaches*
- `effectors-system` - Effectors System
  *Effectors form a fixed registry—stable ground for flexible strategies*
- `fixed-and-flexible-categories` - Fixed and Flexible Categories
  *Direct manifestation of keeping certain elements rigid while others flex*


### `prn_graceful_partial_completion_validity`

**Design systems to produce valid, usable outputs from any degree of partial completion,  treating full completion as optimal but not required, because user abandonment, time  constraints, or early satisfaction should not invalidate accumulated work.
**

*Rationale:* LLM-guided workflows often assume users will complete all steps. Designing for partial  completion changes how downstream prompts must be written (they must handle variable  input richness), how user experience is framed (no "incomplete" shame), and how systems  are architected (no hard dependencies on full completion).


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `continuation-vs-completion-binary-control` - Continuation vs Completion Binary Control
- `variable-ceiling-valid-at-any-point-workflow` - Variable-Ceiling Valid-At-Any-Point Workflow


### `prn_granular_quality_legibility`

**Quality assessments should be localized to individual structural elements with visible status indicators, transforming vague holistic 'needs improvement' judgments into specific actionable targets.**

*Rationale:* Holistic quality judgments paralyze users because they don't know where to start. Per-element quality indicators transform overwhelming revision tasks into sequences of localized improvements, and help users prioritize which elements need attention.

*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `hierarchical-detail-explanation-trade-off-navigation` - Hierarchical Detail-Explanation Trade-off Navigation


### `prn_inferential_prepopulation`

**When structural slots are underfilled, systems should proactively infer plausible content from surrounding context and present multiple variations for user selection or amendment, shifting cognitive burden from generation to evaluation.**

*Rationale:* Users often can recognize good content more easily than generate it. By inferring plausible completions and offering them as options, systems convert difficult generation tasks into easier selection/validation tasks while still allowing user override.

*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `slot-completion-card-with-pre-generated-options` - Slot Completion Card with Pre-generated Options


### `prn_input_qualification_for_context`

**When users provide free-form input alongside structured selections, systems should ask them to qualify what type of input they're providing to help downstream processing understand the intent.**

*Rationale:* Unqualified free-form input is ambiguous - it could be elaborating on selections, providing alternatives, or commenting on the process. By asking users to classify their input (elaboration, alternative, meta-comment), systems gain valuable context that helps LLMs or other processors interpret the input correctly. This small friction yields significant downstream quality improvement.

*Tags:* ux, disambiguation, input-classification, llm-context


### `prn_intent_formation_state_bifurcation`

**Systems gathering complex intent should bifurcate into distinct pathways based on user's  intent-formation state—direct expression for users with formed intent versus guided discovery  for users with unformed intent—because forcing all users through a single flow either  frustrates those who know what they want or overwhelms those who need scaffolding.
**

*Rationale:* LLM-powered systems often default to one interaction mode (usually free-form prompting).  Recognizing that users arrive in different epistemic states regarding their OWN intent  enables designing pathways optimized for each state, dramatically improving user experience  and output quality for users who don't yet know what they want.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `input-modality-election-modal` - Input Modality Election Modal


### `prn_interaction_time_as_computation_budget`

**Treat user interaction time (answering questions, making decisions, reading content)  as a computation budget for parallel background processing, using the time users spend  engaged with current content to pre-generate or refine upcoming content.
**

*Rationale:* Most LLM system designs treat generation as blocking. Recognizing that user interaction  time provides a natural parallelization opportunity changes architecture toward async  patterns where the system is always "thinking ahead" during user engagement periods.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `answer-options-pre-generation` - Answer Options Pre-Generation
- `dynamic-queue-injection-pattern` - Dynamic Queue Injection Pattern


### `prn_interactive_cognition`

**Thinking is enhanced by environments that provide immediate, substantive feedback—tools that enable rapid hypothesis testing and dynamic response accelerate understanding more than static recording tools.**

*Rationale:* Writing has historically been coextensive with thinking—we "think on paper."
But this romanticizes a particular modality as if it were essential to thought.
Thinking can happen in many contexts.

AI-mediated environments offer new possibilities: interfaces that solicit
explicit and implicit feedback, systems that help build and test models of
reality, real-time application through simulation. These may actually produce
*more* opportunities for thinking than sitting in a café with a laptop.

"We are trying to build a much better thinking environment than Microsoft Word."


**Embodied by features:**
- `feat_ai_thinking_environments` - AI Thinking Environments
  *Created by refactoring engine*
- `ui-llm-complementarity-architecture` - UI-LLM Complementarity Architecture
  *Re-linked from deprecated principle during refactoring*
- `plain-language-direction-with-llm-classification` - Plain Language Direction with LLM Classification
  *Re-linked from deprecated principle during refactoring*
- `user-term-engagement-interface` - User Term Engagement Interface
  *Re-linked from deprecated principle during refactoring*


### `prn_meta_structural_revisability`

**Systems should distinguish between filling structural positions and defining what positions exist, with both levels explicitly designed as revisable rather than treating structure as fixed scaffolding for variable content.
**

*Rationale:* Most LLM systems treat templates/schemas as fixed infrastructure that content fills. Recognizing that structure itself should be revisable prevents premature structural commitment and enables organic evolution of organizational frameworks as understanding deepens.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `multi-level-operation-vocabulary` - Multi-Level Operation Vocabulary
- `two-level-architecture-pattern` - Two-Level Architecture Pattern


### `prn_multi_layer_synchronization_obligation`

**Systems with interconnected structural layers (throughlines → concepts → dialectics)  require synchronized remediation across all layers when any layer undergoes transformation,  because layer interdependencies mean single-layer changes create cross-layer inconsistencies.
**

*Rationale:* Without explicit multi-layer awareness, LLMs will complete transformations at the requested  layer while leaving dependent layers inconsistent. The obligation to synchronize must be  built into the operation specification, not left to inference.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `dynamic-coherence-as-system-property` - Dynamic Coherence as System Property
- `cascading-remediation-protocol` - Cascading Remediation Protocol


### `prn_multi_level_advisory_scope`

**Advisory systems should be empowered to recommend changes across multiple abstraction levels simultaneously, with operation vocabularies defined for each level rather than restricting advice to a single operational plane.
**

*Rationale:* If advisory systems can only recommend content changes, users must independently recognize when structural revision is needed. Multi-level advisory scope ensures the system can surface structural inadequacy alongside content issues, preventing users from endlessly refining content within a fundamentally misfit structure.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `multi-level-operation-vocabulary` - Multi-Level Operation Vocabulary


### `prn_optimistic_execution`

**When action confidence is high and reversal cost is low, execute optimistically rather than blocking on approval—bias toward action with easy undo rather than inaction with explicit permission, because interruption cost exceeds correction cost.**

*Rationale:* **Evidence from source:** The demoted principle describes proceeding with action rather than blocking, suggesting an optimistic execution pattern.

**Why this matters:** Constant approval requests create cognitive overhead and interrupt flow. Optimistic execution with undo preserves momentum.

**Structural kinship:** prn_cognitive_division_of_labor, prn_activity_state_gated_automation, prn_human_authority_gate

**Embodied by features:**
- `feat_optimistic_automation_with_undo` - Optimistic Automation with Undo
  *Created by refactoring engine*


### `prn_rich_multiple_choice_structure`

**Multiple choice interfaces should distinguish between mutually exclusive options (single-select) and combinable options (multi-select), always include write-in capability with intent clarification, and push users toward richer self-expression.**

*Rationale:* Simple radio-button multiple choice artificially constrains expression. Real thought often involves combinations, qualifications, and novel perspectives. By structuring questions with both exclusive options (forcing trade-off thinking) and non-exclusive options (allowing synthesis), plus always-available write-in with clarified intent (elaboration vs new answer vs meta-comment), we get richer data and push users to think harder about what they actually mean.

*Tags:* multiple-choice, user-input, intent-clarification, rich-expression


### `prn_temporal_category_dispersion`

**When presenting items from multiple categories across a session, distribute items from  the same category across the temporal span rather than clustering them sequentially,  because dispersion prevents category fatigue, enables cross-category comparison, and  maintains cognitive freshness.
**

*Rationale:* Without explicit dispersion, LLMs generating multi-category content tend to cluster by  category (completing one before starting another). Instructing temporal dispersion  produces better user experiences and more balanced cognitive engagement across the  full category taxonomy.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `pre-allocated-slot-interleaving` - Pre-Allocated Slot Interleaving


### `prn_tradeoff_versus_property_comparison`

**Decision interfaces should distinguish between property-comparison (side-by-side grids  showing features across options) and trade-off-comparison (what you commit to by choosing  one option plus what you specifically forgo from each alternative), because these serve  different cognitive tasks and conflating them produces interfaces that serve neither well.
**

*Rationale:* LLMs often default to generating comparison grids because they're a familiar format, but  many decision contexts require trade-off presentation. Recognizing this distinction helps  prompt engineers request the right format and helps LLMs generate more useful decision support.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `per-alternative-foreclosure-articulation` - Per-Alternative Foreclosure Articulation


### `prn_transformation_context_for_impact_assessment`

**When assessing the impact of structural changes on related elements, provide both the transformation history (what merged, split, created, retired) and the current state of affected elements, because impact assessment requires understanding the transition, not just the before or after state.
**

*Rationale:* Systems often track only current state, losing transformation history. This principle identifies transformation type as semantically significant—a merge has different implications than a split, even if both result in a single element. Preserving this information enables richer impact assessment.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `transformation-state-context-bundle` - Transformation-State Context Bundle


### `prn_transformation_invalidates_references`

**When structural elements are merged, split, or retired, all references TO those elements  (roles, states, relationships) become structurally invalid and require explicit reconstruction,  because references encode positions relative to structures that no longer exist in their  original form.
**

*Rationale:* LLMs performing structural refactoring will focus on the elements being changed and overlook  dependent elements that reference them. Making reference invalidation explicit prevents  orphaned relationships and semantic drift in interconnected systems.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `relationship-invalidation-audit-pattern` - Relationship Invalidation Audit Pattern


### `prn_trigger_source_typology`

**System actions should be categorized by their trigger source—context-triggered (arising from external structural evolution requiring reactive adaptation) versus interpretation-triggered (arising from internal reframing requiring proactive user initiation)—because these categories demand fundamentally different automation levels, user agency patterns, and interface affordances.
**

*Rationale:* Recognizing trigger source as a first-class design dimension prevents conflating automated and user-initiated workflows. It guides interface design, automation levels, and cognitive load distribution. A system that treats all changes uniformly will either over-automate interpretive decisions or under-automate structural propagation.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `context-interpretation-trigger-router` - Context-Interpretation Trigger Router


### `prn_user_controlled_refinement_depth`

**Iterative refinement processes should give users explicit control over when to stop refining  and generate output, because optimal refinement depth varies by user, context, and task— some users need three rounds of questioning, others need ten, and forcing uniform depth  either truncates useful exploration or imposes unnecessary friction.
**

*Rationale:* Many LLM interaction patterns impose fixed-depth processing (one round of clarification,  predetermined number of questions). This principle recognizes that complex intent elicitation  is inherently variable-depth and systems should treat depth as a user parameter rather than  a system constant.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `continuation-vs-completion-binary-control` - Continuation vs Completion Binary Control


## Epistemology

### `prn_abstraction_independence`

**When extracting knowledge across abstraction levels, run independent discovery passes at each level before synthesis; grounding-first approaches bias toward the concrete and miss regulative principles that guide design without direct manifestation.**

*Rationale:* This principle emerged from designing philosophy extraction workflows. The naive approach
extracts macro principles only when they can be traced to meso-level features and code
groundings. This creates systematic blind spots:

**The Embodiment Bias**: If we require principles to be "expressible" in concrete form,
we miss:
- Regulative principles (guide decisions but don't manifest directly)
- Structural principles (govern relationships, not implementations)
- Negative principles (what NOT to do has no positive code signature)
- Meta-principles (about the process itself, not the product)

**The Solution**: Run parallel independent extraction passes:
1. Grounded pass: Find principles visible in code/features
2. Abstract pass: Find principles from description alone, ignoring expressibility
3. Synthesis: Deduplicate, keeping anything from (2) not captured by (1)

This ensures the concrete doesn't over-constrain the abstract.


*Tags:* extraction, multi-level-analysis, bias-prevention

**Embodied by features:**
- `two-level-architecture-pattern` - Two-Level Architecture Pattern
- `logical-rhetorical-linkage-tracking` - Logical-Rhetorical Linkage Tracking


### `prn_constraints_as_crystallization`

**Constraints function as crystallization mechanisms that make visible the difference between theoretical freedom and practical agency—they don't merely limit but reveal which possibilities were always illusory and which remain genuinely available.**

*Rationale:* **Evidence from source:** Split from prn_constraint_narrowing_as_progre to isolate the epistemic/revelatory function of constraints.

**Why this matters:** Constraints are often viewed negatively as limitations. Reframing them as revelation mechanisms changes how we approach problem-solving.

**Structural kinship:** prn_constraint_as_strategy, prn_epistemic_friction, prn_bounded_rationality


### `prn_distinction_surfacing_through_choice`

**Multiple-choice questions serve not merely to gather preferences but to surface distinctions  the user may not have considered, making visible the decision space that exists within what  appeared to be a single intention—the options themselves are epistemic interventions.
**

*Rationale:* This reframes multiple-choice interfaces from mere efficiency tools (faster than typing)  to epistemic scaffolding (reveal hidden decision dimensions). LLM-generated options can  deliberately span the possibility space to ensure users confront choices they didn't  know they were making.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `llm-dual-role-question-answer-processing` - LLM Dual Role Question-Answer Processing


### `prn_epistemic_ontological_distinction`

**Systems processing conceptual content should distinguish between ontological  underdetermination (the object itself is genuinely open, in tension, or in process)  and epistemic underdetermination (limitations in our current grasp, positioning,  or path to the concept), because conflating them misattributes knowledge gaps  to the object or genuine dialectical openness to mere ignorance.
**

*Rationale:* Without this distinction, systems conflate two fundamentally different situations:  (1) genuine dialectical complexity that should be preserved as productive incompletion,  and (2) analytical insufficiency that can be remediated through better questioning.  Treating epistemic gaps as ontological openness wastes opportunity for clarification;  treating ontological openness as epistemic gaps destroys valuable tension.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `seven-category-epistemic-gap-framework` - Seven-Category Epistemic Gap Framework


### `prn_holistic_semantic_judgment`

**Semantic assessment tasks require holistic judgment over complete situational context rather than decomposed scoring of individual factors, because meaning emerges from relationships between elements that piecemeal evaluation cannot capture.
**

*Rationale:* Decomposition is a default engineering strategy, but semantic judgment resists it. Recognizing when holistic assessment is required prevents designs that break semantic tasks into tractable sub-problems, only to find the reassembled result misses the point entirely.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `semantic-territory-shift-detection` - Semantic Territory Shift Detection
- `algorithmic-proxy-recognition-heuristic` - Algorithmic Proxy Recognition Heuristic


### `prn_intellectual_profile`

**Build explicit intellectual profiles—representations of theoretical interests, preferences, and positions—early in the process, because the stronger this profile, the more effective pattern-matching and collaboration with LLMs becomes.**

*Rationale:* For LLMs to help with pattern matching, they need to know what patterns
you're looking for. This requires an explicit representation of your
intellectual interests, theoretical positions, and aesthetic preferences.

Building this profile used to be slow—it emerged implicitly over years of
writing. Now, with customized interfaces that cross-pollinate your thinking
with others' and solicit explicit review of generated connections, the
profile can be built much faster.

The richer the profile, the more effectively LLMs can suggest relevant
connections, filter irrelevant material, and generate aligned outputs.


*Tags:* profile-building, preferences, collaboration, pattern-matching

**Embodied by features:**
- `theory-answer-multiplication` - Theory-Answer Multiplication
  *supports*
- `research-mode-pre-selection` - Research Mode Pre-Selection
  *Early mode selection builds the intellectual profile that enables subsequent pattern-matching*
- `human-in-loop-proposal-review` - Human-in-Loop Proposal Review
  *Feedback learning builds model of reviewer preferences*


### `prn_particularity_recovery`

**Abstractions derived from compressed representations must be returned to the particular—understanding advances not by moving from specific to general and stopping, but by using the general as an instrument for re-encountering the specific with new eyes.**

*Rationale:* Every synthesis sacrifices particularity for surveyability; every abstraction purchases scope at the cost of texture. This is not a flaw to avoid but a dialectical necessity to complete. The provisional schema, however crude, accomplishes what unaided attention cannot: it transforms an undifferentiated mass into a structured field of inquiry. Yet the schema remains hollow until it confronts the resistance of individual instances—the friction, exception, and surplus meaning that compression necessarily effaced. Knowledge deepens not through abstraction alone but through the return journey: the general illuminating what the particular contains, the particular revealing what the general overlooked.


*Tags:* dialectics, abstraction, particularity, hermeneutic-circle

**Embodied by features:**
- `concretization-stage` - Concretization Stage
  *enables*


### `prn_perspective_as_structure`

**Intellectual perspectives can be formalized as structured schemas that encode their assumptions, values, and reasoning patterns—making implicit worldviews explicit and operationalizable.**

*Rationale:* Knowledge production doesn't happen in a vacuum—it occurs in a domain of
competing frameworks. Marxism focuses on class struggle; Foucauldianism
on power-knowledge dynamics; each paradigm has its research questions
and interpretive lenses.

Normally, theories get tested through social feedback from colleagues.
But thinkers may hesitate to share for fear of critique. By embedding
paradigms as schemas in tools, we can subject developing theories to
structured critique from multiple perspectives simultaneously—creating
productive intellectual friction without the social costs.


**Embodied by features:**
- `feat_paradigm_schema_embodiment` - Paradigm Schema Embodiment
  *Created by refactoring engine*
- `genre-archetype-function-mapping` - Genre Archetype Function Mapping
  *Re-linked from deprecated principle during refactoring*
- `multi-strategy-research-slicing` - Multi-Strategy Research Slicing
  *Re-linked from deprecated principle during refactoring*


### `prn_provisional_type_presentation`

**Structural categories and slot types should be presented to users as "plausible but revisable" rather than definitive, making the provisional nature of structural choices explicit in how they are surfaced.
**

*Rationale:* How structure is presented shapes user willingness to revise it. Structures presented as definitive create anchoring effects; structures presented as provisional invite collaborative refinement. The framing itself is an intervention in user cognition about structural flexibility.


*Tags:* auto-extracted, from-prompt


### `prn_reasoning_justification_externalization`

**LLM outputs should include not just conclusions but the specific justification  for each inferential step—why this particular instance was selected, from what  context it was triggered, and what alternatives were implicitly rejected—making  the reasoning pathway itself a structured, queryable artifact.
**

*Rationale:* Without externalized justification, LLM reasoning is a black box that cannot  be audited, debugged, or systematically improved. Forcing justification  externalization creates feedback loops for both prompt refinement and LLM  reasoning quality.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `inference-provenance-capture-pattern` - Inference Provenance Capture Pattern


### `prn_substantive_over_meta_description`

**Decision support content must present actual proposed content, specific text, and  concrete examples rather than meta-descriptions ("more comprehensive"), statistical  summaries ("✓ More seeds"), or categorical labels ("Engages: X"), because genuine  evaluation requires the material itself, not descriptions of the material.
**

*Rationale:* LLMs often generate meta-level summaries when asked to compare options, but users making  real decisions need the concrete material. This principle guides prompt engineering toward  requesting actual content rather than accepting summary abstractions.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `substantive-preview-materialization` - Substantive Preview Materialization


### `prn_synthesis_first_bootstrap`

**Bootstrap schemas and typologies from synthesized materials first, then enrich through systematic re-engagement with source texts—synthesis provides the provisional scaffold, original data provides the substantive refinement.**

*Rationale:* The cost structure of LLM operations inverts traditional scholarship: generating initial abstractions from summaries is now cheap, allowing us to produce workable ontologies rapidly. These provisional schemas then serve as structured lenses for re-examining original materials, transforming vague intuitions into rigorous typologies through iterative enrichment rather than upfront exhaustive analysis.


*Tags:* bootstrapping, synthesis, iterative-refinement

**Embodied by features:**
- `genre-archetype-function-mapping` - Genre Archetype Function Mapping


### `prn_uncertainty_typology_richness`

**Categorize detected uncertainty with sufficient typological richness to capture 
qualitatively different phenomena, because overly narrow categories force 
misclassification and trigger inappropriate handling.
**

*Rationale:* LLM systems detecting "problems" in user input tend to lump all issues together. 
But a gap (missing information), a tension (productive dialectic), and an open 
question (genuine uncertainty) require different handling. Rich typology enables 
appropriate routing: fill gaps, preserve tensions, explore questions.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `seven-category-epistemic-gap-framework` - Seven-Category Epistemic Gap Framework
- `three-way-uncertainty-typology` - Three-Way Uncertainty Typology


## Extracted

### `prn_activity_state_gated_automation`

**Automated system behaviors should be gated by detected user activity state, triggering only during quiescent periods rather than interrupting active exploration, because automation during active work creates chaotic interference while automation during rest feels assistive.**

*Rationale:* **Evidence from source:** auto-navigation has to be smarter - if we are still moving our mouse or clicking on multiple selections we should not auto-navigate. this should happen ONLY if we are rest for some time... right now, it's too chaotic

**Why this matters:** Automation that doesn't respect user activity state creates frustrating interference—the system "helps" precisely when the user is actively trying to do something themselves. Temporal sensitivity to user state is essential for automation that feels assistive rather than adversarial.

**Structural kinship:** ['prn_dual_mode_operation (both concern human vs automated control)', 'prn_human_authority_gate (both preserve human agency over consequential actions)', 'prn_adaptive_termination (both involve systems detecting state changes to adjust behavior)']

**Embodied by features:**
- `cascaded-generation-triggers` - Cascaded Generation Triggers
  *variant_of*
- `quiescence-triggered-automation` - Quiescence-Triggered Automation
  *embodies*


### `prn_arbitrary_insertion_architecture`

**Design systems with validated insertion points throughout the workflow rather than fixed input stages, allowing contextual content to be introduced wherever it becomes relevant rather than only at designated entry points.**

*Rationale:* **Evidence from source:** The prompt describes inserting 'news articles even before we generate any through-lines or even before we generate any strategic items, just to enhance the context' and emphasizes that 'there may be some inputs—like news articles and some additional context—that we might want to insert at any point.'

**Why this matters:** Most LLM workflows assume inputs arrive at the start. Real knowledge work discovers relevant context mid-process. Systems that support arbitrary insertion must design prompts that gracefully incorporate new context into ongoing reasoning, not just process initial inputs. This requires prompts that treat context as accumulating rather than fixed.

**Structural kinship:** prn_forward_staged_data_harvesting (information timing), prn_context_completeness (complete situational context)

**Embodied by features:**
- `arbitrary-point-content-injection` - Arbitrary-Point Content Injection
  *embodies*


### `prn_archeological_pattern_mining`

**[DEPRECATED] Treat accumulated work as archeological data to analyze for patterns. Functionality covered by prn_cybernetic_self_correction (process as analyzable data) and prn_dialectical_knowledge_production (patterns emerge through iteration).**

*Rationale:* **Evidence from source:** in my earlier projects i've accumulated a lot of prompts... for analysis with the view of understanding whether my previous techniques/methodology point to distinct engines/bundles/media

**Why this matters:** Past work embodies tacit knowledge that wasn't explicitly articulated. Mining it with fresh analytical frameworks can recover implicit patterns and methodologies.

**Structural kinship:** prn_synthesis_first_bootstrap, prn_theory_grounded_extraction


### `prn_assumption_dependency_management`

**Complex interrogation structures should track dependencies between questions and avoid building new questions on unverified assumptions from prior questions—validate foundations before stacking.**

*Rationale:* **Evidence from source:** than stack 10 questions on top of assumptions we haven't probed

**Why this matters:** In multi-question flows, later questions often implicitly assume answers to earlier ones. If those assumptions are wrong, the entire downstream inquiry becomes irrelevant or misleading. This principle demands explicit management of assumption dependencies.

**Structural kinship:** prn_front_load_decisions, prn_logical_coherence, prn_cascade_containment

**Embodied by features:**
- `confirm-then-route-interrogation-pattern` - Confirm-Then-Route Interrogation Pattern
- `assumption-grounded-question-sequencing` - Assumption-Grounded Question Sequencing
  *embodies*


### `prn_bidirectional_modification_symmetry`

**When two elements need reconciliation, treat modification of either element as equally valid options; do not privilege one element's stability over the other without explicit justification.**

*Rationale:* **Evidence from source:** The prompt consistently mentions 'modifying either principles or relationships or both' and 'tweaked one or both elements' - refusing to assume that one category (principles vs features) has inherent priority in modification decisions.

**Why this matters:** Prevents hidden biases in knowledge curation. LLMs given asymmetric instructions might always modify the 'lower-level' element. Symmetry ensures genuine options are surfaced for human decision.

**Structural kinship:** prn_optionality_preservation, prn_deferred_commitment

**Embodied by features:**
- `bidirectional-reformulation-options` - Bidirectional Reformulation Options
  *embodies*


### `prn_bidirectional_process_content_evolution`

**Process structure and content outputs should evolve bidirectionally - the process determines what content is gathered, while accumulated content/results should trigger proposals for process restructuring.**

*Rationale:* **Evidence from source:** Author notes 'LLMs might propose adjustment to the flow as we get results' and emphasizes that this dynamic relationship should be explicit - the process isn't just executed but is itself a subject of evolution based on what emerges.

**Why this matters:** Fixed processes cannot adapt when early results reveal that planned stages are unnecessary or that missing stages are needed. Bidirectional evolution allows the system to become smarter about its own operation as it accumulates evidence about what works.

**Structural kinship:** prn_runtime_strategy_adaptation, prn_schema_data_co_evolution, prn_upstream_regeneration_from_downstream

**Embodied by features:**
- `result-triggered-process-restructuring` - Result-Triggered Process Restructuring
  *embodies*


### `prn_cognitive_task_matched_presentation`

**Match information presentation format to the cognitive task it supports—comparison requires parallel structure, evaluation requires hierarchical structure, exploration requires expandable structure—because format shapes cognitive efficiency.**

*Rationale:* **Evidence from source:** The demoted principle describes formatting for scanability and comparison, suggesting task-specific presentation.

**Why this matters:** The same information presented differently enables or inhibits different cognitive operations. Format is not neutral.

**Structural kinship:** prn_decision_interface_modality_matching, prn_detail_deferral_with_accessibility, prn_visual_state_legibility

**Embodied by features:**
- `sign-off-vs-articulation-interface-bifurcation` - Sign-Off vs Articulation Interface Bifurcation
- `pre-allocated-slot-interleaving` - Pre-Allocated Slot Interleaving
- `cognitive-task-to-scaffolding-modality-matching` - Cognitive Task to Scaffolding Modality Matching
  *specializes*
- `feat_structured_decision_presentation` - Structured Decision Presentation
  *Created by refactoring engine*


### `prn_conflict_triage`

**Distinguish routine conflicts (resolvable through aggregation) from substantive tensions (requiring explicit examination) and route accordingly.**

*Rationale:* This principle was discovered through philosophical archaeology of a tool brief.
It represents tacit design knowledge that was implicitly operating but not yet formalized.

**Evidence from source:** The commentary asks when to 'handle reconciliation internally vs. delegating to Cross-Advisor,' suggesting conflicts have different characters requiring different handling.

**Structural kinship:** Related to prn_epistemic_friction (conflict as signal) and prn_cross_model_examination (explicit comparison), but specifically about classification and routing of conflicts rather than just acknowledging their value.


*Tags:* brief-derived

**Embodied by features:**
- `fit-based-evidence-bifurcation` - Fit-Based Evidence Bifurcation
  *embodies*


### `prn_constraint_as_strategy`

**Constraints should drive strategy rather than merely limit execution—explicit resource boundaries enable intelligent allocation and prevent waste on low-value paths.**

*Rationale:* Discovered through philosophical archaeology. Evidence: The brief emphasizes: "There are constraints. We can spend only so many days, so  many queries, and so many hundreds of dollars on a research project. So we have to  strategize." Also: "There is a budget for Phase 1, and the objective is to discover  truly novel authors..." And: "we might switch, pivot, and go for another strategy—or  just launch another Card with a different strategy, even prematurely."

Structural kinship: ['prn_chunking', 'prn_cybernetic_correction']


**Embodied by features:**
- `feat_budget_front_loading` - Budget Front-Loading
  *Created by refactoring engine*
- `cost-explained-processing-choice` - Cost-Explained Processing Choice
  *Re-linked from deprecated principle during refactoring*


### `prn_constraints_as_crystallization`

**Constraints function as crystallization mechanisms that make visible the difference between theoretical freedom and practical agency—they don't merely limit but reveal which possibilities were always illusory and which remain genuinely available.**

*Rationale:* **Evidence from source:** Split from prn_constraint_narrowing_as_progre to isolate the epistemic/revelatory function of constraints.

**Why this matters:** Constraints are often viewed negatively as limitations. Reframing them as revelation mechanisms changes how we approach problem-solving.

**Structural kinship:** prn_constraint_as_strategy, prn_epistemic_friction, prn_bounded_rationality


### `prn_consumer_optimized_representation`

**Design information representations optimized for their primary consumer's cognitive architecture—whether human visual processing, algorithmic parsing, or hybrid interpretation—rather than assuming universal readability.**

*Rationale:* **Evidence from source:** The demoted principle explicitly optimizes for LLM consumption, suggesting a general pattern of consumer-driven design.

**Why this matters:** Different consumers (humans, algorithms, hybrid systems) have fundamentally different processing capabilities and constraints. Optimizing for the wrong consumer creates friction.

**Structural kinship:** prn_machine_legible_affordances, prn_explicit_capability_declaration, prn_context_driven_generation

**Embodied by features:**
- `feat_llm_optimized_data_structures` - LLM-Optimized Data Structures
  *Created by refactoring engine*


### `prn_context_driven_generation`

**When generation costs are low, adapt outputs to specific contexts and data rather than forcing contexts to fit generic templates—personalization should be the default, not the exception, with systems generating bespoke artifacts tailored to actual use conditions.**

*Rationale:* **Evidence from source:** Merged from prn_generative_personalization (personalization default), prn_context_specific_adaptation (context adaptation), and prn_bespoke_contextual (bespoke artifacts).

**Why this matters:** Generic templates force users to adapt to system constraints. When generation is cheap, systems should adapt to users instead.

**Structural kinship:** prn_late_binding_specialization, prn_user_centered_design, prn_resource_proportionality


### `prn_contextual_extraction_superiority`

**Extraction performed with knowledge of downstream use-context produces superior results to the same extraction performed before context is available, even when this requires processing to occur later in the pipeline.**

*Rationale:* **Evidence from source:** The explicit contrast: 'contextually enhanced extraction of context at a slightly later stage' is preferable to 'a-contextual extraction of context at an early stage' - naming a-contextual processing as specifically inferior.

**Why this matters:** This principle inverts common engineering intuitions about pre-computation; it suggests that for LLM-based systems, just-in-time processing with full context beats cached/pre-computed processing that lacks context.

**Structural kinship:** prn_late_binding_semantic_labels (defer binding until context available), prn_execution_readiness_criteria (explicit criteria before delegation)

**Embodied by features:**
- `full-context-semantic-assessment-pattern` - Full-Context Semantic Assessment Pattern
- `conversation-guided-extraction-targeting` - Conversation-Guided Extraction Targeting
  *embodies*
- `document-collection-staging-without-processing` - Document Collection Staging Without Processing
  *embodies*


### `prn_continuous_background_synthesis`

**Run synthesis operations continuously as a background process throughout data collection rather than deferring synthesis to a distinct final phase, allowing the evolving synthesis state to inform and constrain data gathering at every step.**

*Rationale:* **Evidence from source:** The instruction to 'try to make sense of the weight issue early on and keep refining it throughout the user's answers' treats synthesis not as a terminal operation but as an ongoing parallel process that runs continuously alongside data collection.

**Why this matters:** Deferred synthesis creates a disconnect between data gathering and output generation - systems collect data without knowing whether it will actually resolve synthesis requirements. Continuous synthesis makes collection-synthesis coupling tight enough to detect and correct problems in real-time.

**Structural kinship:** prn_iterative_theory_data_dialectic, prn_serial_global_processing, prn_runtime_strategy_adaptation

**Embodied by features:**
- `dynamic-queue-injection-pattern` - Dynamic Queue Injection Pattern
- `parallel-state-companion-track` - Parallel State Companion Track
- `continuous-background-weight-refinement` - Continuous Background Weight Refinement
  *embodies*


### `prn_contrastive_context_enrichment`

**When providing context to LLMs about user choices or system states, include not just what is but what could have been—the rejected alternatives, unchosen paths, and available-but-unused options—because meaning emerges from contrast.**

*Rationale:* **Evidence from source:** The explicit reasoning that knowing "what we did not choose while choosing what we did choose" provides "detail/depth" for modeling behavior implicitly invokes a contrastive theory of meaning—choices are defined relationally against their alternatives.

**Why this matters:** LLMs interpret user choices more accurately when they understand the choice set, not just the outcome. "User selected option A" means something different depending on whether B was also available or whether A was the only option. Contrastive context enables more precise modeling of user preferences and intent.

**Structural kinship:** ['prn_comprehensive_context (both advocate for richer context provision)', 'prn_lens_dependent_extraction (both recognize that framing affects interpretation)', 'prn_possibility_space (both value preserving awareness of alternatives)']

**Embodied by features:**
- `transformation-state-context-bundle` - Transformation-State Context Bundle
- `distinctiveness-guard-provision` - Distinctiveness Guard Provision
- `refactoring-context-package-assembly` - Refactoring Context Package Assembly
- `commitment-plus-foreclosure-panel` - Commitment-Plus-Foreclosure Panel
- `explicit-criterion-threading-between-llm-calls` - Explicit Criterion Threading Between LLM Calls
  *supports*
- *(+3 more)*


### `prn_criteria_grounded_advisory`

**When requesting advisory output from LLMs, explicitly enumerate the criteria by which the decision should be made, giving the model clear grounds for reasoning rather than leaving it to infer what matters.
**

*Rationale:* **Evidence from source:** The prompt specifies asking "which would better serve our need for abstraction, modularity, comprehensiveness, etc?"—naming the specific criteria by which the choice should be evaluated rather than asking for general advice.


**Why this matters:** Without explicit criteria, LLMs may advise based on inferred or default criteria that don't match the user's actual decision framework. Explicit criteria focus the advisory reasoning and make the basis for recommendations transparent and contestable.


**Structural kinship:** prn_comprehensive_context, prn_theory_grounded_extraction

**Embodied by features:**
- `multi-level-operation-vocabulary` - Multi-Level Operation Vocabulary
- `criteria-enumeration-in-advisory-prompts` - Criteria Enumeration in Advisory Prompts
  *embodies*
- `choice-architecture-constraint` - Choice Architecture Constraint
  *enables*


### `prn_cross_slot_synthesis_scanning`

**Systems should include explicit mechanisms ("factories") that scan across different functional categories to identify potential higher-level connections, rather than relying on ad-hoc or implicit synthesis.**

*Rationale:* **Evidence from source:** we should have some kind of a through-line factory which will scan our functional outline as it exists across all of the slots, and it will try to find larger, more abstract connective tissues that are rhetorical and argumentative.

**Why this matters:** Through-lines and meta-patterns don't emerge automatically from local work—they require explicit cross-cutting analysis. Without a dedicated scanning mechanism, connections between distant parts of an argument remain invisible, and the system produces fragmented rather than unified outputs.

**Structural kinship:** prn_controlled_propagation, prn_gap_aware_processing, prn_framework_expansion_reanalysis

**Embodied by features:**
- `batch-then-synthesize-pattern` - Batch-Then-Synthesize Pattern
  *enables*
- `slot-level-synthesis-abstraction` - Slot-Level Synthesis Abstraction
  *embodies*
- `through-line-factory-pattern` - Through-line Factory Pattern
  *embodies*


### `prn_decision_interface_modality_matching`

**Pre-generated decision support content should be presented through interface affordances (modals, sidebars, collapsibles) that match the cognitive task—comparison requires parallel visibility, exploration requires expandability.**

*Rationale:* **Evidence from source:** The instruction to 'stick it into a modal, sidebar, or something similar' reveals awareness that generated content must be architecturally positioned to support the decision task, not just dumped into the main flow.

**Why this matters:** LLM-generated content for decision support fails when presentation architecture doesn't match decision structure. Recognizing that different decision types require different spatial arrangements improves interface design for AI-assisted choices.

**Structural kinship:** prn_format_for_decision_support, prn_detail_deferral_with_accessibility, prn_visual_state_legibility

**Embodied by features:**
- `decision-support-container-matching` - Decision Support Container Matching
  *embodies*


### `prn_decision_space_propagation`

**When users make selections through an interface, downstream LLM processing should receive not just the selections themselves but the full decision space (available options, chosen options, rejected options) to enable richer modeling of user intent and preferences.**

*Rationale:* **Evidence from source:** The user's key insight that 'knowing what we did not choose while choosing what we did choose enhances the LLM's ability to model our behavior/expectations' goes beyond mere capture—it's about propagating the full decision context as input to subsequent LLM operations. The phrasing 'down the chain/path' suggests awareness of a processing pipeline where this information has value.

**Why this matters:** LLMs model user preferences more accurately when they can see what was rejected alongside what was chosen—this mirrors how preference learning works in RLHF. Systems that only pass forward positive selections lose the contrastive signal that helps LLMs calibrate their understanding of what the user actually wants versus what was merely acceptable.

**Structural kinship:** ['prn_negative_selection_capture (specialization for LLM consumption)', 'prn_contrastive_context_enrichment (operational mechanism)', 'prn_comprehensive_context (domain-specific instance)']

**Embodied by features:**
- `decision-context-bundle` - Decision Context Bundle
  *embodies*


### `prn_default_recommendation_elicitation`

**When seeking LLM advice on choices between generated options, explicitly request a recommended default rather than neutral analysis, because humans conserve cognitive resources by evaluating recommendations rather than weighing unranked options.
**

*Rationale:* **Evidence from source:** "Formulate it in such a way that the LLM would propose a default and we won't have to think about it ourselves"—the explicit design goal is eliciting a recommendation, not just surfacing considerations.


**Why this matters:** LLMs often default to presenting balanced analysis rather than making recommendations, but humans often need recommendations they can accept or override rather than analyses they must synthesize. Explicitly requesting a default changes the output mode from "here are considerations" to "here is what I'd do."


**Structural kinship:** prn_cognitive_load_transfer, prn_format_for_decision_support

**Embodied by features:**
- `recommendation-mode-request` - Recommendation Mode Request
  *embodies*


### `prn_detail_deferral_with_accessibility`

**Pre-generate detailed content (narrative text, full language) but present structural summaries by default (bulletpoints, logic descriptions, transition names), keeping detail collapsed but accessible, so users can maintain big-picture focus while preserving access to instantiation.**

*Rationale:* **Evidence from source:** The prompt requests 'bulletpoint like structure and hide the narrative text but make it easy to unpack/view,' 'focus on big dynamics, not language (even though pre-generate language to give us a feel for it),' and 'include initially collapsed text but focus on the logic of the transition.'

**Why this matters:** Detailed language is necessary for final output but distracting during structural decision-making. This principle enables systems to satisfy both needs: generate detail for completeness but present structure for clarity, letting users control their zoom level.

**Structural kinship:** prn_format_for_decision_support (formatting for evaluation), prn_function_form_phase_separation (separating structure from presentation), prn_intermediary_curation (curating before presenting)

**Embodied by features:**
- `collapsible-detail-architecture` - Collapsible Detail Architecture
  *Implements collapsed-by-default detail with expand-on-demand access*


### `prn_dialogue_emergent_relevance`

**User-LLM conversation itself generates the targeting criteria for what's relevant in source materials, making dialogue a discovery mechanism rather than merely an output channel.**

*Rationale:* **Evidence from source:** The phrase 'the nature of the convo between user the LLM will help us understand what exactly to look for in those documents' treats conversation as generating relevance criteria that couldn't be specified upfront.

**Why this matters:** Recognizing that conversation produces relevance criteria suggests system architectures where document retrieval/extraction systems listen to dialogue state rather than operating on fixed pre-queries.

**Structural kinship:** prn_staged_adaptive_interrogation (questions emerge from prior answers), prn_dialectical_refinement (understanding emerges through cycles)

**Embodied by features:**
- `llm-dual-role-question-answer-processing` - LLM Dual Role Question-Answer Processing
- `dual-channel-progressive-specialization` - Dual-Channel Progressive Specialization
  *embodies*
- `just-in-time-profile-construction` - Just-In-Time Profile Construction
  *supports*
- `conversation-guided-extraction-targeting` - Conversation-Guided Extraction Targeting
  *embodies*


### `prn_domain_transcendent_abstraction`

**Abstract process structures away from any specific domain instantiation so the same operational logic serves multiple domains (journalism, academia, policy) through different parameterization rather than different architectures.**

*Rationale:* **Evidence from source:** The prompt describes the need to move from 'essay flow tool' to 'generic tool' and lists multiple target domains: 'academic article or writing an essay... news piece... foundation... policy reports, reports from grantees.' It explicitly states 'efforts must transcend that and penetrate other institutions.'

**Why this matters:** When prompts are domain-specific, each new domain requires new prompt engineering. Domain-transcendent design means prompts operate on abstract roles (source material, analytical frame, output format) that get instantiated differently per domain. This dramatically reduces prompt proliferation and enables systematic domain transfer.

**Structural kinship:** prn_abstraction_independence (independent abstraction passes), prn_domain_archetypes (categorical templates per domain)

**Embodied by features:**
- `domain-agnostic-initial-architecture` - Domain-Agnostic Initial Architecture
  *embodies*
- `domain-portable-process-architecture` - Domain-Portable Process Architecture
  *embodies*


### `prn_downstream_aware_generation`

**Prompts that generate initial outputs should explicitly encode how those outputs will be processed, transformed, and synthesized in subsequent stages, because generation optimized for immediate coherence often produces outputs poorly suited for downstream operations.**

*Rationale:* **Evidence from source:** The user states "we have to incorporate all these future uses into the prompt that generates initial throughlines" and suggests rewinding to "regenerate throughlines with these future uses in mind"—explicitly arguing that upstream generation must be designed with downstream processing in view.

**Why this matters:** LLM outputs are often well-formed in isolation but structurally incompatible with subsequent processing steps; designing prompts with the full pipeline in mind produces outputs that flow smoothly through multi-stage systems.

**Structural kinship:** prn_capability_addition_cascade_analysis, prn_front_load_decisions

**Embodied by features:**
- `quality-gated-phase-transition` - Quality-Gated Phase Transition
- `stage-contingent-question-calibration` - Stage-Contingent Question Calibration
  *enables*
- `preemptive-output-structure-anticipation` - Preemptive Output Structure Anticipation
  *implements*
- `logical-rhetorical-translation-prerequisites` - Logical-Rhetorical Translation Prerequisites
  *embodies*
- `stage-bridging-extraction-strategy` - Stage-Bridging Extraction Strategy
  *embodies*
- *(+2 more)*


### `prn_dual_outline_constraint`

**Writing requires satisfying both logical validity and rhetorical effectiveness; systems should track both dimensions and their mutual requirements.**

*Rationale:* This principle was discovered through features-first extraction.

**Evidence from brief:** The insistence on 'translation of logical to rhetorical arguments' and that 'materials would be shared across two outlines—serving as evidence, transition, hooks, or rhetorical functions.'

**Structural kinship:** prn_abstraction_independence, prn_logical_coherence

**Why novel:** 

*Tags:* brief-derived, features-first

**Embodied by features:**
- `logical-rhetorical-translation-prerequisites` - Logical-Rhetorical Translation Prerequisites
  *embodies*
- `logical-rhetorical-linkage-tracking` - Logical-Rhetorical Linkage Tracking
- `genre-archetype-function-mapping` - Genre Archetype Function Mapping


### `prn_dynamic_elicitation_injection`

**When anticipated outputs reveal information gaps, strategically inject targeted questions into the interaction flow at opportune moments rather than adhering to predetermined question sequences, treating the question flow itself as dynamically optimizable based on model needs.**

*Rationale:* **Evidence from source:** The phrase 'strategically insert a question or two which will help us make sense of the weights EVEN BEFORE we generated the weightlines' explicitly proposes injecting questions that weren't part of the original flow, driven by the needs of anticipated downstream processing.

**Why this matters:** Fixed question sequences cannot anticipate all information needed for novel output configurations. Dynamic injection allows systems to fill specific gaps identified by anticipatory models, converting passive questionnaires into active information-hunting instruments.

**Structural kinship:** prn_staged_adaptive_interrogation, prn_proactive_insufficiency_signaling, prn_runtime_strategy_adaptation

**Embodied by features:**
- `dynamic-queue-injection-pattern` - Dynamic Queue Injection Pattern
- `non-predetermined-stage-sequencing` - Non-Predetermined Stage Sequencing
  *extends*
- `weight-gap-targeted-question-insertion` - Weight-Gap Targeted Question Insertion
  *embodies*


### `prn_embodied_decision_substrate`

**Consequential choices require pre-generation of sufficient concrete material that decision-makers can develop an 'embodied feel' for each option rather than evaluating abstractly described alternatives.**

*Rationale:* **Evidence from source:** The phrase 'full embodied feel for what choosing each of the readings would involve' and the request to 'generate enough mock data to make this happen' indicate that abstract description is insufficient—tangible instantiation is required for proper decision-making.

**Why this matters:** LLMs can cheaply generate concrete instantiations, but prompts often ask only for descriptions of options. Recognizing that decisions require experiential substrate rather than propositional summaries shifts how we structure choice-presenting interfaces.

**Structural kinship:** prn_option_impact_preview, prn_abstract_concrete_progressive, prn_practical_discovery_over_theoretical

**Embodied by features:**
- `substantive-preview-materialization` - Substantive Preview Materialization
- `provisional-formulation-as-knowledge-probe` - Provisional Formulation as Knowledge Probe
  *extends*
- `embodied-decision-substrate-generation` - Embodied Decision Substrate Generation
  *embodies*


### `prn_emergent_choice`

**Genuine choices are not given at the start but emerge through analytical work; systems should track this emergence rather than forcing premature selection.**

*Rationale:* This principle was discovered through features-first extraction.

**Evidence from brief:** The explicit principle that 'We don't have choices - we create them by analyzing corpora for materials.'

**Structural kinship:** prn_abductive_logic, prn_process_as_data

**Why novel:** 

*Tags:* brief-derived, features-first

**Embodied by features:**
- `diagnostic-disambiguation-flow` - Diagnostic Disambiguation Flow
- `reasoning-chain-display` - Reasoning Chain Display
- `choice-creation-through-analysis-cycles` - Choice Creation Through Analysis Cycles
- `cross-pollination-proposition-generation` - Cross-Pollination Proposition Generation


### `prn_event_driven_refinement`

**Knowledge structures should evolve in response to events (new data, external changes, scheduled reviews) rather than only through explicit invocation; systems that can be triggered maintain freshness that imperative-only systems cannot.**

*Rationale:* This principle was discovered through philosophical archaeology of a tool brief.
It represents tacit design knowledge that was implicitly operating but not yet formalized.

**Evidence from source:** The brief specifies five distinct trigger points: "Post-synthesis: After initial schema generation completes. New specimen added: An excellent new example is added to a genre's corpus. Cross-genre trigger: Another genre's schema was refined... Scheduled refinement: Periodic re-engagement to catch drift or staleness. Manual invocation." This event-driven architecture pattern reflects a commitment to schemas as living, responsive artifacts.


**Structural kinship:** ['prn_cybernetic_correction (events as correction triggers)', 'prn_abductive_logic (new data triggers theory refinement)']


*Tags:* brief-derived

**Embodied by features:**
- `staleness-detection-monitor-pattern` - Staleness Detection Monitor Pattern
- `task-driven-pipeline-composition` - Task-Driven Pipeline Composition
  *relates_to*
- `stray-element-as-workflow-trigger` - Stray Element as Workflow Trigger
  *embodies*
- `eternal-ephemeral-extraction-dichotomy` - Eternal-Ephemeral Extraction Dichotomy


### `prn_expansion_constraint_rhythm`

**Progress emerges through rhythmic alternation between expansion and constraint—expand the solution space to exhaustion, then narrow through constraints to reveal what's actually viable, with each cycle illuminating which possibilities were illusory and which remain tractable.**

*Rationale:* **Evidence from source:** Split from prn_constraint_narrowing_as_progre to isolate the rhythmic alternation pattern from the crystallization function.

**Why this matters:** Problem-solving often stalls when stuck in either pure expansion (overwhelm) or pure constraint (premature closure). Explicit rhythm enables sustainable progress.

**Structural kinship:** prn_iterative_theory_data_dialectic, prn_divergent_convergent_cycles, prn_cybernetic_feedback


### `prn_explicit_process_externalization`

**The workflow itself should be an explicit, versioned, user-adjustable data structure that LLMs propose, humans modify, and all processing stages can query - making process design a first-class collaborative artifact rather than implicit system architecture.**

*Rationale:* **Evidence from source:** Author states 'we would probably generate it early on,' 'have an LLM propose that after some initial questions and the user can adjust/modify,' 'keep track of versioning,' and 'the more we are explicit about this flexible dynamism, the better results we'll get.'

**Why this matters:** When process structure is implicit (hardcoded in system design), users cannot meaningfully participate in process design and LLMs cannot reason about or propose process improvements. Externalizing process as queryable data enables both human agency and LLM-driven optimization of the workflow itself.

**Structural kinship:** prn_data_as_program, prn_refinement_versioning, prn_human_authority_gate

**Embodied by features:**
- `cognitive-scaffolding-for-intellectual-navigation` - Cognitive Scaffolding for Intellectual Navigation
- `collaborative-process-design-with-versioning` - Collaborative Process Design with Versioning
  *embodies*


### `prn_extensibility_as_design_criterion`

**When discovering patterns for system design, explicitly optimize for ease of future extension rather than just current completeness, treating "easy to add X later" as a first-class requirement.**

*Rationale:* **Evidence from source:** i want it to be super-easy for us to add things like that once the system is operational so we need to set it up correctly... our overall concern is building a highly modular/configurable system that will be easy to modify/expand in the future

**Why this matters:** This shifts pattern identification from "what exists" to "what structure would make adding new types easy" - a meta-level concern that should shape how categories are discovered and structured.

**Structural kinship:** prn_provisional_structures, prn_schema_data_co_evolution

**Embodied by features:**
- `type-generic-element-processing` - Type-Generic Element Processing
  *embodies*
- `schema-introspective-question-generation` - Schema-Introspective Question Generation
  *supports*


### `prn_externalized_imagination_infrastructure`

**AI systems should function as external cognitive infrastructure that enables imagination and conceptual exploration beyond what working memory and internal visualization can support, making thinkable what cannot be held 'in the head'.**

*Rationale:* **Evidence from source:** The prompt explicitly states the goal is 'the most sophisticated cognitive/imagination support possible' and identifies the limitation as 'users have trouble conceptualizing in their head - when they think unabetted - or on paper when they just write'

**Why this matters:** Reframes LLM systems from question-answering tools to imagination prosthetics - this changes what we build from interfaces that capture answers to environments that enable thinking users couldn't otherwise do

**Structural kinship:** prn_interactive_cognition, prn_possibility_space_architecture

**Embodied by features:**
- `cognitive-scaffolding-for-intellectual-navigation` - Cognitive Scaffolding for Intellectual Navigation
- `cognitive-task-to-scaffolding-modality-matching` - Cognitive Task to Scaffolding Modality Matching
  *embodies*
- `choice-impact-topology-rendering` - Choice-Impact Topology Rendering
  *embodies*
- `provisional-formulation-as-knowledge-probe` - Provisional Formulation as Knowledge Probe
  *embodies*


### `prn_extrapolative_inference_request`

**Ask LLMs not only to analyze what patterns exist in data, but to extrapolate what complementary structures should exist based on discovered patterns - inferring from engines to appropriate media, from problems to solutions.**

*Rationale:* **Evidence from source:** ask to extrapolate and get the LLM to think about what kind of media - a textual memo? a table? a blend of the two? a particular ***KIND*** of gemini visualization? - would be useful in rendering the particular slant

**Why this matters:** This leverages LLMs' strength in pattern completion and analogy - moving from discovered analytical structures to appropriate presentation forms that the author hasn't yet imagined.

**Structural kinship:** prn_downstream_aware_generation, prn_domain_archetypes

**Embodied by features:**
- `trinity-classification-framework` - Trinity Classification Framework
  *enables*


### `prn_formalization_as_education`

**When systems translate user intentions from plain language to formal specifications, exposing the translation back to users develops their expertise and expands their conceptual vocabulary.**

*Rationale:* **Evidence from source:** The prompt states users 'express it once' in plain language, then the system shows them formal terms 'so that they develop their imagination and their skill.' The explicit goal is 'walking them through the complexity of the process and immersing them in it' to 'expand their imagination to the point where they would be asking completely novel questions.'

**Why this matters:** This reframes system formalization as a pedagogical opportunity rather than just a translation step. LLM systems that expose their interpretive work to users can serve as teaching tools, not just execution tools—users learn the formal vocabulary that makes them more effective prompt engineers and system collaborators.

**Structural kinship:** prn_tacit_to_explicit, prn_emergence_through_iterative_re

**Embodied by features:**
- `bidirectional-improvement-loop-architecture` - Bidirectional Improvement Loop Architecture
- `reasoning-chain-display` - Reasoning Chain Display
- `translation-map-display` - Translation Map Display
- `expert-transparency-mode` - Expert Transparency Mode
  *supports*
- `plain-language-registry-extension-pipeline` - Plain-Language Registry Extension Pipeline
  *embodies*


### `prn_forward_staged_data_harvesting`

**At each processing stage, extract not only what that stage requires but also data that will serve downstream stages, even when users don't recognize its future relevance, packaging future-oriented extraction within current-stage work.**

*Rationale:* **Evidence from source:** The author says: 'There are surely things we can extract from the user that the user doesn't even know about that, while packaged as functional skeleton work, would actually help us greatly when it comes to doing the rhetorical outline strategy'

**Why this matters:** Users only understand what's relevant to their current task; systems that harvest information for future stages during current-stage work avoid costly backtracking and redundant questioning

**Structural kinship:** prn_downstream_aware_generation, prn_structured_elicitation, prn_early_consequential_decisions

**Embodied by features:**
- `uncertainty-to-question-pipeline` - Uncertainty-to-Question Pipeline
- `first-input-throughline-projection` - First-Input Throughline Projection
  *extends*
- `arbitrary-point-content-injection` - Arbitrary-Point Content Injection
  *relates_to*
- `cascaded-generation-triggers` - Cascaded Generation Triggers
  *embodies*
- `stage-bridging-extraction-strategy` - Stage-Bridging Extraction Strategy
  *embodies*


### `prn_friction_focused_attention_allocation`

**Direct human cognitive effort preferentially toward items that create structural tension or conflict with existing frameworks, treating harmonious integrations as background operations that merit notification but not active attention.**

*Rationale:* **Evidence from source:** The phrase 'the core of the action is on dealing with those that cause friction/conflict' explicitly prioritizes human attention toward conflict cases rather than spreading it across all items equally.

**Why this matters:** LLM systems often demand uniform attention across all outputs; this principle enables intelligent attention allocation by making 'structural fit with existing knowledge' the primary routing criterion, allowing humans to invest cognitive effort where it generates maximum value.

**Structural kinship:** prn_cognitive_division_of_labor, prn_conflict_triage, prn_resource_proportionality

**Embodied by features:**
- `friction-prioritized-attention-allocation` - Friction-Prioritized Attention Allocation
  *embodies*


### `prn_generation_evaluation_separation`

**When LLMs both generate options and advise on selection, these functions should be separated into distinct calls rather than conflated in a single prompt, because generation benefits from expansive creativity while evaluation benefits from constrained comparative reasoning.
**

*Rationale:* **Evidence from source:** The prompt explicitly specifies "first API call to generate values; second API call to ask for advice on how to choose between them"—treating these as fundamentally different cognitive operations requiring different prompting contexts.


**Why this matters:** Conflating generation and evaluation in a single call produces outputs that self-censor during generation or fail to seriously evaluate during selection. Separation allows each call to be optimized for its specific epistemic function, improving both option richness and advice quality.


**Structural kinship:** prn_function_form_phase_separation, prn_chunking

**Embodied by features:**
- `two-stage-generation-advice-pattern` - Two-Stage Generation-Advice Pattern
  *embodies*


### `prn_genre_as_scaffold`

**Genre conventions encode successful patterns of argumentation; making them explicit as functional typologies provides scaffolding for both extraction and composition.**

*Rationale:* This principle was discovered through features-first extraction.

**Evidence from brief:** The emphasis on building 'thorough typology of each genre's logical functions—the archetypes logically, not just rhetorically' and using these to guide what's needed.

**Structural kinship:** prn_paradigm_embodiment, prn_fixed_foundation

**Why novel:** 

*Tags:* brief-derived, features-first

**Embodied by features:**
- `invisible-foundation-pattern` - Invisible Foundation Pattern
- `genre-mediated-template-derivation` - Genre-Mediated Template Derivation
- `genre-indexed-requirement-templates` - Genre-Indexed Requirement Templates
  *embodies*
- `functional-slot-architecture` - Functional Slot Architecture
  *supports*
- `critical-question-prioritization` - Critical Question Prioritization
- *(+3 more)*


### `prn_graduated_intervention_intensity`

**When seeking to resolve system inconsistencies or gaps, attempt minimal interventions first (no changes) before escalating to moderate interventions (single-element changes) and finally maximal interventions (multi-element changes).**

*Rationale:* **Evidence from source:** Step 2 seeks 'direct hits/relationships that we can make without any modifications' before Step 3 proposes 'ways of modifying either principles or relationships or both' - a clear graduation from zero-modification to one-element to both-element changes.

**Why this matters:** Prevents over-engineering by LLMs. Without explicit graduation, LLMs tend toward elaborate solutions. This principle ensures simpler connections are discovered before complex reconciliations are attempted.

**Structural kinship:** prn_resource_proportionality, prn_deferred_commitment

**Embodied by features:**
- `zero-modification-first-assessment` - Zero-Modification-First Assessment
  *embodies*


### `prn_human_authority_gate`

**Consequential modifications to persistent structures require explicit human approval; systems propose, humans dispose. This is not merely compensation for LLM limits but a design commitment to human authority.**

*Rationale:* This principle was discovered through philosophical archaeology of a tool brief.
It represents tacit design knowledge that was implicitly operating but not yet formalized.

**Evidence from source:** The brief repeatedly emphasizes human approval as non-negotiable: "Human review is essential: The tool generates proposals; humans make final decisions." This is listed as both an assumption and a scope constraint ("Fully autonomous schema modification" is explicitly out of scope). The distinction from prn_compensate_llm_limits is that this isn't about capability compensation—it's about authority allocation. Even a perfect LLM should not autonomously modify schemas.


**Structural kinship:** ["prn_compensate_llm_limits (related but distinct—that's about capability, this is about authority)", 'prn_cybernetic_correction (human review as a specific correction mechanism)']


*Tags:* brief-derived

**Embodied by features:**
- `sign-off-vs-articulation-interface-bifurcation` - Sign-Off vs Articulation Interface Bifurcation
- `agency-preserving-response-options` - Agency-Preserving Response Options
- `result-triggered-process-restructuring` - Result-Triggered Process Restructuring
  *constrains*
- `correction-then-commit-gating` - Correction-Then-Commit Gating
  *supports*
- `granular-post-hoc-override-controls` - Granular Post-Hoc Override Controls
  *implements*
- *(+5 more)*


### `prn_impact_topology_materialization`

**Make visible the full network topology of how conceptual choices propagate through an argument or system - not just listing impacts but rendering the structure of dependency and implication that users cannot maintain mentally.**

*Rationale:* **Evidence from source:** Specific reference to 'analysis of impact of defining a concept this way rather than that way, with possible impact/implications on the rest of the argument' - emphasis on what users 'have trouble conceptualizing in their head'

**Why this matters:** Arguments and conceptual systems have complex interdependencies; making these visible enables strategic conceptual decisions rather than ad-hoc choices that create unforeseen inconsistencies

**Structural kinship:** prn_option_impact_preview, prn_change_impact_propagation, prn_possibility_as_foreclosure_warning

**Embodied by features:**
- `choice-impact-topology-rendering` - Choice-Impact Topology Rendering
  *embodies*


### `prn_interpretive_cascade_instantiation`

**When interpretive choices cascade through interconnected structures, instantiate the full downstream revision requirements for each option rather than abstractly describing propagation effects.**

*Rationale:* **Evidence from source:** The prompt requests showing 'what kind of revisions to the parts of the throughline would be needed, depending on which of the sub-options for integrating each reading we go with'—not a description of propagation but actual instantiated revisions.

**Why this matters:** Abstract statements like 'this would require updating X' fail to convey the true cost of changes. Actually generating the revised versions makes costs concrete and comparable, enabling informed selection among interpretive options.

**Structural kinship:** prn_bounded_propagation, prn_capability_addition_cascade_analysis, prn_downstream_aware_generation

**Embodied by features:**
- `resolution-path-virtualization-panel` - Resolution Path Virtualization Panel
- `sub-option-dependent-revision-branching` - Sub-Option Dependent Revision Branching
  *extends*
- `interpretive-choice-cascade-pre-computation` - Interpretive Choice Cascade Pre-Computation
  *embodies*


### `prn_inter_stage_criterion_propagation`

**When multiple LLM invocations collaborate across a multi-stage process, the variables, criteria, and constraints that govern each stage's behavior should be explicitly passed as structured data between stages rather than left implicit or re-derived.**

*Rationale:* **Evidence from source:** Author emphasizes 'the passing of variables/criteria among LLMs' and connects explicit process awareness to 'not only ask the right questions but restructure the process accordingly' - suggesting that criteria propagation is the mechanism by which process-awareness operates.

**Why this matters:** Without explicit criterion propagation, each LLM invocation must infer constraints from context or operate with incomplete information. Explicit propagation creates a coordinated 'nervous system' across the pipeline where upstream decisions properly constrain downstream behavior.

**Structural kinship:** prn_provenance_preservation, prn_decision_space_propagation, prn_contrastive_context_enrichment

**Embodied by features:**
- `answer-accumulating-question-batches` - Answer-Accumulating Question Batches
- `explicit-criterion-threading-between-llm-calls` - Explicit Criterion Threading Between LLM Calls
  *embodies*


### `prn_irrelevance_tolerance_instruction`

**When processing noisy data sources, explicitly instruct LLMs that not all input data will be relevant and that filtering is expected, preventing forced pattern-matching where genuine relevance is absent.**

*Rationale:* **Evidence from source:** clarify in the prompt to the api that some of the data it will be accessing won't be relevant to the task at hand at all - this is a registry of my old prompts, i didn't clear it specifically

**Why this matters:** LLMs tend toward finding patterns and relevance even in noise; explicitly licensing irrelevance recognition prevents hallucinated connections and overfitting to random structure.

**Structural kinship:** prn_wildcard_inclusion_for_complet, prn_content_based_routing

**Embodied by features:**
- `noise-aware-prompt-framing` - Noise-Aware Prompt Framing
  *embodies*


### `prn_late_binding_semantic_labels`

**Establish structural relationships and logical roles early in processing pipelines, but defer binding semantic labels (names, titles, descriptions) until content is fully assembled and context is maximally available.**

*Rationale:* **Evidence from source:** The prompt explicitly states: 'we'll think abstractly in earlier stages - we'll understand that there are logical/structural connections between elements... but we'll name them only at the pre-rendering stage to make sure their names are most adequate to the content.'

**Why this matters:** LLMs generate better labels when they have full context. Early naming forces commitment before understanding is complete, resulting in generic or misaligned labels like 'Level 0: Root Categories' instead of content-appropriate descriptions.

**Structural kinship:** prn_deferred_commitment, prn_abstract_concrete_progressive_

**Embodied by features:**
- `abstract-structural-placeholder-pattern` - Abstract Structural Placeholder Pattern
  *embodies*
- `concretization-stage` - Concretization Stage
  *embodies*


### `prn_logical_coherence`

**System modifications should preserve logical coherence by tracking dependencies and re-evaluating proposals in light of accepted changes.**

*Rationale:* This principle was discovered through philosophical archaeology of a tool brief.
It represents tacit design knowledge that was implicitly operating but not yet formalized.

**Evidence from source:** The commentary identifies that 'accepting proposal A changes the context for proposal B' and asks how to handle this. This suggests proposals exist in a logical space where coherence matters.

**Structural kinship:** Related to prn_cybernetic_correction (re-evaluation as feedback) but specifically about maintaining structural integrity of the artifact being modified. Also shares concern with prn_chunking about granularity vs. coherence tradeoffs.


*Tags:* brief-derived

**Embodied by features:**
- `cascading-remediation-protocol` - Cascading Remediation Protocol
- `assumption-grounded-question-sequencing` - Assumption-Grounded Question Sequencing
  *enables*
- `mutual-exclusivity-mapping` - Mutual Exclusivity Mapping
  *supports*
- `edit-impact-tracking` - Edit Impact Tracking
- `versioned-questionnaire-regeneration-pipeline` - Versioned Questionnaire Regeneration Pipeline


### `prn_machine_legible_affordances`

**System capabilities should be discoverable and composable by automated agents, not just humans—machine-readable declarations of what's possible enable programmatic reasoning about action spaces.**

*Rationale:* Discovered through philosophical archaeology. Evidence: The brief describes: "LLMs can evaluate the results and draw on our repertoire of  actions defined in our Registry of Effectors, our Registry of Family Strategies,  and our Registry of AI Operations." Later: "There must be a much tighter schema for  how these Family Strategies work, how we populate them, and how we expose them to  the LLMs so they can pick which combination to run."

Structural kinship: ['prn_llm_first_creative', 'prn_compensate_llm_limits']


**Embodied by features:**
- `feat_llm_readable_capability_registry` - LLM-Readable Capability Registry
  *Created by refactoring engine*
- `role-based-fact-mobilization-on-demand` - Role-Based Fact Mobilization On-Demand
  *Re-linked from deprecated principle during refactoring*


### `prn_multimodal_cognitive_scaffolding`

**Different cognitive tasks (imagining possibilities, tracing implications, articulating beliefs, comparing options) require different scaffolding modalities - questions, visualizations, path-diagrams, and interfaces are all tools in a repertoire that must be matched to cognitive task type.**

*Rationale:* **Evidence from source:** Explicit statement that 'questions are one way to do it but interfaces, visualizations of paths that can be taken, and the implications thereof, etc - all of that is part and parcel of our repertoire too' - and 'questions are like crutches - but so is the UI/interface'

**Why this matters:** Treating questioning as the only elicitation modality misses that thinking involves spatial reasoning, comparison, path-tracing - modalities that text questions alone cannot scaffold

**Structural kinship:** prn_cognitive_task_matched_presentation, prn_decision_interface_modality_matching

**Embodied by features:**
- `input-modality-election-modal` - Input Modality Election Modal
- `cognitive-task-to-scaffolding-modality-matching` - Cognitive Task to Scaffolding Modality Matching
  *embodies*


### `prn_negative_selection_capture`

**What users explicitly reject or pass over during selection processes provides informationally rich context that should be captured and propagated alongside positive selections, because choices are defined as much by what was not chosen as by what was.**

*Rationale:* **Evidence from source:** do we pass on some summary or full info of the clusters we did not select down the chain/path? we should because it's informative knowledge - knowing what we did not choose while choosing what we did choose enhances the LLM's ability to model our behavior/expectations with a bit more detail/depth

**Why this matters:** Most systems only track positive selections, losing the contrastive information that gives choices meaning. When LLMs receive only what was chosen without knowing the alternatives, they lose critical context for understanding user intent. Rejected options reveal the boundary conditions of user preferences—what they explicitly didn't want among viable alternatives.

**Structural kinship:** ['prn_process_as_data (both treat non-output artifacts as valuable)', 'prn_comprehensive_context (both argue for providing seemingly non-essential information)', 'prn_intellectual_profile (both aim to build richer user models)']

**Embodied by features:**
- `uncertainty-to-question-pipeline` - Uncertainty-to-Question Pipeline
- `per-alternative-foreclosure-articulation` - Per-Alternative Foreclosure Articulation
- `hierarchical-sharpen-triggers` - Hierarchical Sharpen Triggers
  *embodies*
- `decision-context-bundle` - Decision Context Bundle
  *enables*


### `prn_optimistic_execution`

**When action confidence is high and reversal cost is low, execute optimistically rather than blocking on approval—bias toward action with easy undo rather than inaction with explicit permission, because interruption cost exceeds correction cost.**

*Rationale:* **Evidence from source:** The demoted principle describes proceeding with action rather than blocking, suggesting an optimistic execution pattern.

**Why this matters:** Constant approval requests create cognitive overhead and interrupt flow. Optimistic execution with undo preserves momentum.

**Structural kinship:** prn_cognitive_division_of_labor, prn_activity_state_gated_automation, prn_human_authority_gate

**Embodied by features:**
- `feat_optimistic_automation_with_undo` - Optimistic Automation with Undo
  *Created by refactoring engine*


### `prn_option_impact_preview`

**When presenting modification options to users, pre-compute and display their potential impacts on interconnected system elements, transforming selection from local evaluation to system-aware decision-making.**

*Rationale:* **Evidence from source:** The prompt states that 'whatever virtual options are given would need to trigger stress tests of other parts/throughlines' - options should not be evaluated in isolation but with their cascading effects made visible.

**Why this matters:** LLM-generated options often appear locally optimal but have non-obvious system-wide effects. Pre-computing these effects prevents users from accepting changes that create downstream incoherence.

**Structural kinship:** prn_bounded_propagation, prn_capability_addition_cascade_analysis, prn_possibility_as_foreclosure_warning

**Embodied by features:**
- `resolution-path-virtualization-panel` - Resolution Path Virtualization Panel
- `choice-impact-topology-rendering` - Choice-Impact Topology Rendering
  *specializes*
- `interpretive-choice-cascade-pre-computation` - Interpretive Choice Cascade Pre-Computation
  *embodies*
- `propagation-triggered-stress-testing` - Propagation-Triggered Stress Testing
  *embodies*


### `prn_possibility_as_foreclosure_warning`

**Present multiple possibilities not merely as options for selection but as warnings about what commitment to any option would foreclose, making the cost of premature commitment visible through the alternatives it eliminates.**

*Rationale:* **Evidence from source:** we want to present the user with embodied possibilities of straightjacketing/pigeonholing their argument early on, to precisely avoid not having considered better options

**Why this matters:** Traditional option presentation emphasizes what you get by choosing. This principle emphasizes what you lose. When users see that choosing throughline A eliminates throughlines B and C, they make more informed commitments. The alternatives serve an epistemic function even if never selected.

**Structural kinship:** prn_contrastive_context_enrichment, prn_negative_selection_capture, prn_front_load_decisions

**Embodied by features:**
- `conditions-of-possibility-interrogation` - Conditions of Possibility Interrogation
- `commitment-plus-foreclosure-panel` - Commitment-Plus-Foreclosure Panel
- `choice-impact-topology-rendering` - Choice-Impact Topology Rendering
  *extends*
- `mutual-exclusivity-mapping` - Mutual Exclusivity Mapping
  *embodies*


### `prn_possibility_space_architecture`

**Systems should pre-generate branching possibility spaces at multiple levels of abstraction, transforming user experience from sequential generation into navigation of pre-populated virtualities that can be selectively actualized.**

*Rationale:* **Evidence from source:** The prompt repeatedly uses 'possibilities spaces,' 'virtualities,' describes wanting to 'create possibilities/virtualities, some of them concrete... some of them concrete/abstract,' and insists on pre-generating options at every level rather than generating on selection.

**Why this matters:** When LLM generation is cheap, the interaction paradigm shifts from 'generate what I ask for' to 'show me the landscape of what's possible.' This enables discovery of options users wouldn't have known to request and makes the decision space tangible rather than abstract.

**Structural kinship:** prn_pre_curation_with_option_prese (pre-curated alternatives), prn_possibility_as_foreclosure_warning (possibilities as decision context), prn_divergence_as_signal (multiple valid outputs)

**Embodied by features:**
- `slot-completion-card-with-pre-generated-options` - Slot Completion Card with Pre-generated Options
- `sub-option-dependent-revision-branching` - Sub-Option Dependent Revision Branching
  *embodies*
- `cascaded-generation-triggers` - Cascaded Generation Triggers
  *Pre-generates branching possibility spaces for navigation*
- `in-slot-option-swapping` - In-Slot Option Swapping
  *Allows navigation within pre-populated option spaces*


### `prn_practical_discovery_over_theoretical`

**When facing complex process design questions, generate early-stage outputs to learn from rather than attempting to theorize the perfect approach, because observing actual system behavior shortens learning cycles more effectively than abstract reasoning.**

*Rationale:* **Evidence from source:** The author explicitly states: 'So instead of solving this question theoretically, we'll actually solve it in practice—that would be the idea, and that would probably shorten the learning cycle and get us where we need to be much faster.'

**Why this matters:** LLM system designers often over-invest in upfront theoretical design when cheap generation allows empirical discovery; recognizing this accelerates development by treating generated outputs as experimental data rather than final products

**Structural kinship:** prn_dialectical_refinement, prn_process_as_data

**Embodied by features:**
- `synthetic-data-ui-scaffolding` - Synthetic-Data UI Scaffolding
- `bidirectional-stage-learning-loop` - Bidirectional Stage Learning Loop
  *embodies*


### `prn_precision_forcing_interrogation`

**Refinement stages should contain questions specifically designed to force precision on vague or underdetermined elements, treating imprecision as a targetable property that questioning can address.**

*Rationale:* **Evidence from source:** The prompt specifies questions that 'will force us to be a bit more precise about concepts and dialectics' - the questioning is not just exploratory but has the explicit goal of tightening precision on theoretical elements

**Why this matters:** LLM-generated questions often explore broadly; questions explicitly designed to force precision produce tighter, more operationalizable outputs rather than expansive but vague elaborations

**Structural kinship:** prn_staged_adaptive_interrogation, prn_dynamic_elicitation_injection, prn_gap_aware_processing

**Embodied by features:**
- `diagnostic-disambiguation-flow` - Diagnostic Disambiguation Flow
- `precision-forcing-refinement-questions` - Precision-Forcing Refinement Questions
  *embodies*


### `prn_proactive_insufficiency_signaling`

**LLMs should recognize when they have identified possibilities but lack sufficient data to evaluate or complete them, explicitly signaling this insufficiency and generating targeted follow-up questions rather than producing incomplete outputs or hallucinating completeness.**

*Rationale:* **Evidence from source:** perhaps the LLM will say: look here I spot some possibilities in terms of throughlines/slots but I don't have enough data... so I have to ask you a bunch of follow-up questions to see if it's feasible

**Why this matters:** LLMs typically generate outputs regardless of input sufficiency, masking gaps with confident-sounding completions. This principle makes data insufficiency a first-class system state that triggers explicit questioning rather than degraded output quality. It transforms the LLM from an oracle into a diagnostic partner.

**Structural kinship:** prn_anthropologist_role, prn_emergence_through_iterative_re, prn_gap_aware_processing

**Embodied by features:**
- `weight-gap-targeted-question-insertion` - Weight-Gap Targeted Question Insertion
  *implements*
- `llm-driven-diagnostic-questioning` - LLM-Driven Diagnostic Questioning
  *embodies*


### `prn_process_parameterized_questioning`

**Questions at any processing stage should be explicitly parameterized by the current process plan, with question types, granularity, and focus determined by which other stages exist or have been removed from the workflow.**

*Rationale:* **Evidence from source:** The author states that if Evidence stage exists, Refinement should ask for 'typologies of examples/event patterns'; if Evidence stage 'has been nuked in flow design,' then Refinement should 'force the user to think of specific examples' - showing that question content is a function of process structure.

**Why this matters:** Without explicit process-awareness, each stage operates with implicit assumptions about what comes before/after, leading to redundant questions, missing information, or inappropriately-scoped inquiries. Making process structure an explicit input to question generation enables truly coordinated multi-stage workflows.

**Structural kinship:** prn_downstream_aware_generation, prn_stage_appropriate_question_types

**Embodied by features:**
- `explicit-criterion-threading-between-llm-calls` - Explicit Criterion Threading Between LLM Calls
  *enables*
- `stage-contingent-question-calibration` - Stage-Contingent Question Calibration
  *embodies*


### `prn_productive_incompletion`

**Not all questions should be resolved—some should be deliberately converted to retained "problematiques" that become structural features of the output, providing narrative tension and marking areas of genuine dialectical openness.**

*Rationale:* **Evidence from source:** we would convert them from questions to problematiques; these will be the kind of elements and areas and domains that we will keep open throughout the essay... it's very important for us to be able to retain that possibility because this will... this is what will provide some kind of narrative tension inside the argument.

**Why this matters:** LLM systems often treat all gaps as defects to be filled. This principle recognizes that intellectual work sometimes requires preserving uncertainty as a feature rather than a bug—marking genuine dialectics rather than papering over them with false resolution. Outputs become richer and more honest.

**Structural kinship:** prn_optionality_preservation, prn_deferred_commitment, prn_closure_matches_problem

**Embodied by features:**
- `three-way-uncertainty-typology` - Three-Way Uncertainty Typology
- `question-to-problematique-conversion` - Question-to-Problematique Conversion
  *embodies*


### `prn_productive_relationship_filtering`

**Not all possible relationships between new data and existing frameworks merit exploration; systems should help identify which relationships would be 'productive' to pursue based on current project needs rather than exhaustively cataloging all connections.**

*Rationale:* **Evidence from source:** The prompt asks to 'understand what kinds of relationships are possible and what kinds would be productive for us to experiment and play with' - distinguishing possible from productive, implying a filtering function.

**Why this matters:** LLMs can identify many relationships but not all are worth pursuing. Helping users focus on productive relationships prevents exhausting attention on low-value connections while missing high-value ones.

**Structural kinship:** prn_resource_proportionality, prn_function_based_on_demand_retri, prn_relevance_latency_tradeoff

**Embodied by features:**
- `productivity-filtered-relationship-exploration` - Productivity-Filtered Relationship Exploration
  *embodies*


### `prn_provisional_articulation_as_catalyst`

**System-generated provisional conclusions, formulations, and intermediate articulations serve as catalysts for extracting tacit user knowledge - the act of seeing an imperfect formulation crystallizes the user's ability to articulate what they actually think.**

*Rationale:* **Evidence from source:** Explicit instruction: 'if you think that outputting some temporary conclusions/answers/formulations for stage 1 will help you extract better answers in stage 2, do not hesitate' - treating provisional outputs as elicitation tools rather than final products

**Why this matters:** Users often know more than they can articulate on demand; seeing provisional framings activates recognition-based knowledge that generation-based questioning cannot reach

**Structural kinship:** prn_embodied_decision_substrate, prn_forward_staged_data_harvesting

**Embodied by features:**
- `slot-completion-card-with-pre-generated-options` - Slot Completion Card with Pre-generated Options
- `non-predetermined-stage-sequencing` - Non-Predetermined Stage Sequencing
  *supports*
- `provisional-formulation-as-knowledge-probe` - Provisional Formulation as Knowledge Probe
  *embodies*


### `prn_reasoning_resource_maximization`

**For tasks requiring strategic reasoning and dynamic adaptation, allocate maximum available computational resources (token limits, reasoning modes, context windows) rather than economizing, because reasoning quality scales with resource availability.**

*Rationale:* **Evidence from source:** Explicit instruction: 'opus 4.5 64 max tokens, 32k tokens reasoning mode' and 'shouldn't spare any resources to unleash LLM's reasoning power.' This is not proportional allocation but maximum allocation for reasoning-heavy work.

**Why this matters:** Many practitioners default to minimizing token usage for cost efficiency, but this principle recognizes that strategic reasoning tasks have qualitatively different resource requirements where economizing degrades output quality non-linearly.

**Structural kinship:** prn_resource_proportionality (inverts the proportionality logic for certain task types), prn_relevance_latency_tradeoff (accepts costs for quality)

**Embodied by features:**
- `maximum-resource-allocation-for-strategic-reasonin` - Maximum Resource Allocation for Strategic Reasoning
  *embodies*


### `prn_refinement_versioning`

**Track and display version numbers on elements that have been regenerated/sharpened, making the history of iterative refinement visible and distinguishing fresh generation from progressively improved elements.**

*Rationale:* **Evidence from source:** The prompt explicitly requests 'add a little version somewhere to display (e.g. v1, v2) - to flag that we have already sharpened some of these elements in earlier gos.'

**Why this matters:** Without version visibility, users lose track of which elements have been refined and which are still raw generations. This creates confusion about where attention has been invested and where further refinement might be valuable.

**Structural kinship:** prn_process_as_data (process as informative data), prn_provenance_preservation (maintaining traceable connections), prn_visual_state_legibility (encoding state visually)

**Embodied by features:**
- `collaborative-process-design-with-versioning` - Collaborative Process Design with Versioning
  *applies*
- `hierarchical-sharpen-triggers` - Hierarchical Sharpen Triggers
  *Tracks version numbers through iterative sharpen cycles*


### `prn_reformulation_before_rejection`

**When elements fail to connect within a knowledge system, explore whether reformulation of one or both elements enables connection before accepting disconnection as legitimate.**

*Rationale:* **Evidence from source:** The prompt explicitly requests 'bridge reformulations that, if only tweaked one or both elements we are trying to match, would result in us establishing a link' - treating disconnection as potentially a formulation problem rather than an ontological fact.

**Why this matters:** LLMs excel at semantic reformulation. This principle transforms apparent knowledge gaps into reformulation opportunities, leveraging LLM paraphrasing capability to increase knowledge graph connectivity.

**Structural kinship:** prn_schema_as_hypothesis, prn_epistemic_friction


### `prn_regeneration_over_retrofitting`

**When foundational assumptions or requirements change, regenerate from earlier pipeline stages rather than attempting to retrofit new requirements onto existing outputs, because LLM generation is cheap while manual integration of incompatible structures is expensive.**

*Rationale:* **Evidence from source:** The user concludes "perhaps we should rewind and regenerate throughlines with these future uses in mind" rather than suggesting modifications to existing throughlines—they prefer clean regeneration over patching.

**Why this matters:** The instinct to preserve existing work often leads to awkward patches and structural compromises; LLM abundance makes regeneration cheap, and clean regeneration typically produces more coherent outputs than retrofitted modifications.

**Structural kinship:** prn_cybernetic_correction, prn_provisional_adaptive_structures

**Embodied by features:**
- `hierarchical-sharpen-triggers` - Hierarchical Sharpen Triggers
  *embodies*


### `prn_relationship_type_taxonomy`

**When integrating source materials with theoretical frameworks, explicitly categorize the type of relationship (illustration, nuance-discovery, challenge, extension) because different relationship types require different processing pathways and have different implications for framework evolution.**

*Rationale:* **Evidence from source:** The prompt enumerates distinct relationship types: 'illustration of the main dynamic,' 'illustration of the previously undetected nuance/sub-dynamic,' 'challenges to the logic of the argument' - implying these categories matter for how material is processed and used.

**Why this matters:** LLMs can process source material more effectively when given an explicit typology of how material might relate to existing structures, enabling targeted extraction and appropriate handling rather than generic summarization.

**Structural kinship:** prn_content_based_routing, prn_domain_archetypes

**Embodied by features:**
- `source-framework-relationship-classification` - Source-Framework Relationship Classification
  *embodies*


### `prn_relevance_latency_tradeoff`

**When additional processing time significantly improves output relevance or personalization, accept latency rather than prioritizing speed—users will wait for responses that demonstrably incorporate their context over immediate generic responses.**

*Rationale:* **Evidence from source:** better to have users waiting for 30 seconds while they expect a new batch of questions but to make questions super-relevant and build off one another/clarified assumptions - than stack 10 questions on top of assumptions we haven't probed

**Why this matters:** Challenges the default engineering assumption that faster is always better. Recognizes that users distinguish between "waiting because system is slow" and "waiting because system is thinking about my specific situation"—the latter builds trust and delivers value.

**Structural kinship:** prn_resource_proportionality, prn_bespoke_contextual


### `prn_runtime_strategy_adaptation`

**Systems should continuously re-evaluate strategic approach based on accumulated results and emerging context, rather than committing to fixed execution plans—strategy and execution should be interleaved, not sequential.**

*Rationale:* **Evidence from source:** The demoted principle describes ongoing re-evaluation during execution, suggesting a general pattern beyond LLMs.

**Why this matters:** Pre-planned strategies cannot account for information revealed during execution. Rigid plans waste resources on paths that prove unproductive.

**Structural kinship:** prn_cybernetic_feedback, prn_strategic_nondeterminism, prn_event_driven_refinement

**Embodied by features:**
- `result-triggered-process-restructuring` - Result-Triggered Process Restructuring
  *embodies*
- `feat_llm_continuous_strategy_adaptation` - LLM Continuous Strategy Adaptation
  *Created by refactoring engine*


### `prn_schema_reflexive_generation`

**LLM prompts that operate on structured systems should introspect on the current schema to dynamically generate appropriate processing for each structural element type, rather than hardcoding responses for known elements.**

*Rationale:* **Evidence from source:** The requirement that refinement be 'structure-aware' means the system must inspect what elements exist (concepts, dialectics, propositions, future unknowns) and generate questions accordingly, not rely on predetermined question sets for predetermined elements

**Why this matters:** LLM systems that hardcode prompts for specific structural elements become brittle when schemas evolve; systems that generate prompts by reflecting on current schema remain robust through schema changes without prompt rewriting

**Structural kinship:** prn_process_parameterized_questioning, prn_data_as_program, prn_context_driven_generation

**Embodied by features:**
- `schema-introspective-question-generation` - Schema-Introspective Question Generation
  *embodies*


### `prn_serial_global_processing`

**When processing items sequentially, maintain active global system context and evaluate each item's potential systemic effects rather than treating each processing unit as isolated, because valuable integration opportunities and coherence threats only become visible at the system level.**

*Rationale:* **Evidence from source:** The prompt describes going through PDFs 'one by one' while simultaneously requiring awareness of 'how a tweak in one throughline will affect the other throughlines' and being 'on the lookout for propagation effects' - serial processing with systemic consciousness.

**Why this matters:** LLMs processing items sequentially often lose global context. Explicitly maintaining system awareness during serial processing prevents locally sensible but globally incoherent integrations.

**Structural kinship:** prn_downstream_aware_generation, prn_context_completeness, prn_shared_scaffold_parallel_streams

**Embodied by features:**
- `serial-processing-with-global-throughline-awarenes` - Serial Processing with Global Throughline Awareness
  *embodies*


### `prn_shared_scaffold_parallel_streams`

**When multiple independent work streams must eventually merge, they should share a common structural scaffold that creates natural alignment points, enabling synthesis operations at each scaffold level rather than requiring post-hoc reconciliation.**

*Rationale:* **Evidence from source:** The prompt describes how throughlines share a "unified slot structure" with "slots shared between the overall skeleton of the whole essay AND of the given throughline"—the same functional slots (IMPLICATIONS, INTERVENTIONS) appear in both individual throughlines and the unified essay structure.

**Why this matters:** Without shared scaffolding, merging independent streams requires expensive structural alignment; shared scaffolds make synthesis a matter of content reconciliation within pre-aligned structures rather than simultaneous structural and content negotiation.

**Structural kinship:** prn_cross_slot_synthesis_scanning, prn_cascading_virtuality

**Embodied by features:**
- `throughline-factory-pattern` - Throughline Factory Pattern
  *embodies*


### `prn_stage_appropriate_question_types`

**Different processing stages require qualitatively different types of questions—structural stages need categorical and logical questions while later stages need flow, narrative, and rhetorical questions—and prompts should adapt question types to stage characteristics.**

*Rationale:* **Evidence from source:** The author distinguishes: 'in the rhetorical outline, we can still do kind of questions with multiple answers, like we did in the functional skeleton, but they would be much more about flow, narrative, argumentation. How is it that we want to make that argument?'

**Why this matters:** Using logical questions at rhetorical stages (or vice versa) produces mismatched outputs; recognizing stage-question alignment improves elicitation effectiveness

**Structural kinship:** prn_staged_processing, prn_function_form_phase_separation

**Embodied by features:**
- `stage-contingent-question-calibration` - Stage-Contingent Question Calibration
  *specializes*


### `prn_staged_adaptive_interrogation`

**Complex interrogation should proceed in sequential stages where each stage's questions are generated based on answers from prior stages, allowing the inquiry to progressively narrow and deepen rather than scattering attention across unvalidated assumptions.**

*Rationale:* **Evidence from source:** first ask a batch of three questions... get users' answers... then we generate a second batch based on those answers and pending strategic items... then we generate the final third batch of questions, incorporating everything from the previous two

**Why this matters:** Prevents the common failure mode of asking all questions upfront, which either overwhelms users or builds on unverified assumptions. Each stage validates foundations before building further, creating a more reliable epistemic structure.

**Structural kinship:** prn_abductive_logic, prn_emergence_through_iterative_re, prn_abstraction_level_sequencing

**Embodied by features:**
- `answer-accumulating-question-batches` - Answer-Accumulating Question Batches
- `curator-sharpener-two-stage-architecture` - Curator-Sharpener Two-Stage Architecture
- `uncertainty-to-question-pipeline` - Uncertainty-to-Question Pipeline
- `confirm-explore-articulate-flow` - Confirm-Explore-Articulate Flow
- `diagnostic-disambiguation-flow` - Diagnostic Disambiguation Flow
- *(+4 more)*


### `prn_staging_processing_separation`

**Distinguish between making resources accessible to a system (staging) and extracting structured content from them (processing); resources should be staged early for availability but processed late when context clarifies extraction requirements.**

*Rationale:* **Evidence from source:** The prompt describes wanting to 'point the tool to some folders with docs' (staging) while 'build up a profile' should happen in a way that's contextually relevant (processing) - treating these as separable operations with different timing requirements.

**Why this matters:** This principle enables system designs where document corpuses are connected but dormant until activated by specific needs, avoiding both the cost of comprehensive pre-processing and the latency of just-in-time document discovery.

**Structural kinship:** prn_function_based_on_demand_retri (mobilize selectively), prn_arbitrary_insertion_architecture (content introduced when relevant)

**Embodied by features:**
- `just-in-time-profile-construction` - Just-In-Time Profile Construction
  *embodies*
- `document-collection-staging-without-processing` - Document Collection Staging Without Processing
  *embodies*


### `prn_structural_fit_assessment_phase`

**Before integrating new content into existing frameworks, explicitly assess the degree of structural fit between the content and target slots, using fit assessment as a routing decision rather than attempting integration first.**

*Rationale:* **Evidence from source:** The prompt's logic assumes a prior determination of which evidence 'naturally fits into supporting the stuff in the slots' versus which 'causes friction'—implying an explicit fit assessment phase before integration attempts.

**Why this matters:** Without explicit fit assessment, systems either over-consult humans (asking about everything) or create downstream cleanup work (integrating first, then discovering conflicts). Pre-integration fit assessment enables intelligent routing and reduces both consultation fatigue and error correction.

**Structural kinship:** prn_execution_readiness_criteria, prn_conflict_triage, prn_staged_processing

**Embodied by features:**
- `fit-based-evidence-bifurcation` - Fit-Based Evidence Bifurcation
  *embodies*


### `prn_structured_integration`

**Approved insights should flow into persistent structures through defined integration pathways rather than accumulating as unstructured additions.**

*Rationale:* This principle was discovered through features-first extraction.

**Evidence from brief:** The explicit enumeration of integration options: 'folding into existing argument, a higher unit of analysis (claim), or generating entirely new argument.'

**Structural kinship:** prn_controlled_propagation, prn_chunking

**Why novel:** 

*Tags:* brief-derived, features-first

**Embodied by features:**
- `provenance-attached-writing-context` - Provenance-Attached Writing Context
- `food-for-thought-integration-pathways` - Food for Thought Integration Pathways


### `prn_substance_instance_tiering`

**Separate archetypal types (substances) from their concrete exemplifications (instances) in a two-tier selection process, requiring users to commit to the abstract category before seeing concrete options, because premature exposure to instances biases toward surface appeal over structural fit.**

*Rationale:* **Evidence from source:** The prompt explicitly separates 'substance' from 'implementation,' requires 'three substances × three instances,' and insists users must 'see substances first and only then choose what instances.' Even openings should have 'archetypal openings - substance - and then fill in the particular examples.'

**Why this matters:** Users often select based on surface linguistic appeal rather than structural appropriateness. Forcing engagement with the abstract archetype first ensures the structural role is understood before concrete instantiation can seduce with attractive but potentially ill-fitted language.

**Structural kinship:** prn_abstract_concrete_progressive_ (dialectic between abstract and concrete), prn_emergent_choice (choices emerge through process), prn_function_form_phase_separation (separating structural from presentational)

**Embodied by features:**
- `substance-instance-matrices` - Substance × Instance Matrices
  *Direct implementation of two-tier substance/instance selection pattern*


### `prn_theory_grounded_extraction`

**User inputs gain multiplicative generative power when processed through an existing theoretical framework; the theory enables inference, cross-pollination, and gap-filling that raw inputs alone cannot provide.**

*Rationale:* **Evidence from source:** a single answer to a question in the initial questionnaire might not mean much, but once it's operationalized within our broader theoretical project, it becomes much more generative... strategic items that we extract, they would not just be grounded in our answers to the questions, they would also be grounded in our theory.

**Why this matters:** Many LLM workflows treat each user input in isolation, missing the compounding effects of connecting inputs to persistent theoretical frameworks. A theory base acts as a lens that reveals implications invisible to framework-free processing, turning sparse inputs into rich outputs.

**Structural kinship:** prn_comprehensive_context, prn_intellectual_profile, prn_cross_pollination_as_generativ

**Embodied by features:**
- `refactoring-context-package-assembly` - Refactoring Context Package Assembly
- `theory-answer-multiplication` - Theory-Answer Multiplication
  *embodies*


### `prn_type_polymorphic_processing`

**Design LLM processing mechanisms to operate on structural element categories (types) rather than specific instances, enabling automatic inclusion of new instances within existing types without mechanism modification.**

*Rationale:* **Evidence from source:** The prompt distinguishes between the current specific elements ('propositions, concepts, dialectics') and the general principle that 'different structural elements' may be added, requiring the refinement to work at the type level not the instance level

**Why this matters:** When LLM prompts enumerate specific items rather than operating on item types, every schema addition requires prompt updates; type-level operations scale automatically with schema growth

**Structural kinship:** prn_domain_transcendent_abstraction, prn_substance_instance_tiering, prn_extensibility_as_design_criterion

**Embodied by features:**
- `type-generic-element-processing` - Type-Generic Element Processing
  *embodies*


### `prn_upstream_regeneration_from_downstream`

**When users make refinements at lower/later/more-concrete levels of a hierarchy, they should be able to regenerate upstream/earlier/more-abstract elements to make them more bespoke to those downstream choices, enabling bidirectional influence rather than purely top-down determination.**

*Rationale:* **Evidence from source:** The prompt explicitly describes going back to 'regenerate those elements to make them more precise/bespoke based on the choices/refinements we made further down below' and 'regenerate transitions upward' after choosing implementation details - this is not just forward propagation but backward regeneration.

**Why this matters:** Most LLM workflows are purely top-down: generate abstract → refine to concrete → output. This principle recognizes that concrete choices reveal what the abstract SHOULD have been, and cheap regeneration enables iterative coherence that manual editing cannot achieve.

**Structural kinship:** prn_bounded_propagation (bounded change propagation), prn_regeneration_over_retrofitting (regeneration approach), prn_dialectical_refinement (iterative framework-data interaction)

**Embodied by features:**
- `hierarchical-sharpen-triggers` - Hierarchical Sharpen Triggers
  *Enables downstream refinements to trigger upstream regeneration*


### `prn_user_archetype_grounding`

**Frame system design analysis around a specific user archetype and their characteristic questions, providing a north star that distinguishes relevant patterns from interesting-but-irrelevant ones.**

*Rationale:* **Evidence from source:** our guiding question is this: we are targeting researchers who want to make quick sense of the collections of articles without having to read individual pieces. so we need to find ways to make this helpful for them

**Why this matters:** Without an explicit user archetype, pattern identification drifts toward what's structurally interesting rather than what's functionally useful. The user question provides evaluative grounding.

**Structural kinship:** prn_function_based_on_demand_retri, prn_context_completeness

**Embodied by features:**
- `user-question-driven-pattern-discovery` - User-Question-Driven Pattern Discovery
  *embodies*


### `prn_verification_easier_than_generation`

**LLMs are more reliable at verifying whether outputs match inputs than at generating correct outputs initially, because verification is a constrained comparison task while generation requires unconstrained production.**

*Rationale:* **Evidence from source:** The proposal assumes a second LLM checking fields against inputs will catch errors the generating model made, implying verification is a fundamentally more tractable task than generation for LLMs.

**Why this matters:** This principle justifies architectural patterns where cheap verification layers can dramatically improve reliability of expensive generation steps, changing cost-benefit calculations for LLM pipeline design.

**Structural kinship:** prn_generation_evaluation_separation, prn_adversarial_multi_perspective_refinement

**Embodied by features:**
- `input-grounded-field-comparison` - Input-Grounded Field Comparison
  *supports*
- `secondary-llm-verification-layer` - Secondary LLM Verification Layer
  *embodies*


### `prn_visual_state_legibility`

**Interactive interfaces must encode system states (active/inactive, selected/unselected, available/unavailable) through sufficient visual contrast that state is immediately perceivable without cognitive effort.**

*Rationale:* **Evidence from source:** The user's complaint that 'Questions tabs are too pale - the inactive ones are barely visible' diagnoses a failure of visual state encoding. The issue isn't aesthetic preference but functional: users cannot perceive the decision landscape when visual differentiation is insufficient.

**Why this matters:** When users interact with systems to provide input for LLM processing, unclear visual state creates cognitive overhead that degrades decision quality. Users making selections under conditions of visual ambiguity provide noisier signals than those working with clear interfaces.

**Structural kinship:** ['prn_bespoke_contextual (interface design dimension)', 'prn_formalization_as_education (making system state explicit)']

**Embodied by features:**
- `granular-post-hoc-override-controls` - Granular Post-Hoc Override Controls
  *supports*
- `in-slot-option-swapping` - In-Slot Option Swapping
  *embodies*
- `streaming-progress-visibility` - Streaming Progress Visibility
  *embodies*
- `multi-level-possibility-mapping-interface` - Multi-Level Possibility Mapping Interface
  *supports*
- `state-contrast-audit` - State Contrast Audit
  *embodies*


## Governance

### `prn_change_impact_propagation`

**Changes must propagate through interconnected systems to maintain coherence—local modifications create inconsistencies that must be resolved through propagation to dependent elements, because systems with internal contradictions are unstable.**

*Rationale:* **Evidence from source:** Split from prn_bounded_propagation, which conflated two distinct concerns: the necessity of propagation for coherence, and the necessity of bounds to prevent cascades.

**Why this matters:** This captures the completeness side: without propagation, local changes create global inconsistencies. A database update that doesn't propagate to dependent views leaves the system in contradiction.

**Structural kinship:** Related to prn_propagation_bounds (the containment counterpart), prn_provisional_frameworks (coherent evolution), prn_cybernetic_self_correction (systems maintaining consistency).

**Embodied by features:**
- `transformation-state-context-bundle` - Transformation-State Context Bundle
- `dynamic-coherence-as-system-property` - Dynamic Coherence as System Property
- `staleness-detection-monitor-pattern` - Staleness Detection Monitor Pattern
- `cascading-remediation-protocol` - Cascading Remediation Protocol
- `relationship-invalidation-audit-pattern` - Relationship Invalidation Audit Pattern
- *(+1 more)*


## Meta

### `prn_interactive_cognition`

**Thinking is enhanced by environments that provide immediate, substantive feedback—tools that enable rapid hypothesis testing and dynamic response accelerate understanding more than static recording tools.**

*Rationale:* Writing has historically been coextensive with thinking—we "think on paper."
But this romanticizes a particular modality as if it were essential to thought.
Thinking can happen in many contexts.

AI-mediated environments offer new possibilities: interfaces that solicit
explicit and implicit feedback, systems that help build and test models of
reality, real-time application through simulation. These may actually produce
*more* opportunities for thinking than sitting in a café with a laptop.

"We are trying to build a much better thinking environment than Microsoft Word."


**Embodied by features:**
- `feat_ai_thinking_environments` - AI Thinking Environments
  *Created by refactoring engine*
- `ui-llm-complementarity-architecture` - UI-LLM Complementarity Architecture
  *Re-linked from deprecated principle during refactoring*
- `plain-language-direction-with-llm-classification` - Plain Language Direction with LLM Classification
  *Re-linked from deprecated principle during refactoring*
- `user-term-engagement-interface` - User Term Engagement Interface
  *Re-linked from deprecated principle during refactoring*


## Methodology

### `prn_abstraction_independence`

**When extracting knowledge across abstraction levels, run independent discovery passes at each level before synthesis; grounding-first approaches bias toward the concrete and miss regulative principles that guide design without direct manifestation.**

*Rationale:* This principle emerged from designing philosophy extraction workflows. The naive approach
extracts macro principles only when they can be traced to meso-level features and code
groundings. This creates systematic blind spots:

**The Embodiment Bias**: If we require principles to be "expressible" in concrete form,
we miss:
- Regulative principles (guide decisions but don't manifest directly)
- Structural principles (govern relationships, not implementations)
- Negative principles (what NOT to do has no positive code signature)
- Meta-principles (about the process itself, not the product)

**The Solution**: Run parallel independent extraction passes:
1. Grounded pass: Find principles visible in code/features
2. Abstract pass: Find principles from description alone, ignoring expressibility
3. Synthesis: Deduplicate, keeping anything from (2) not captured by (1)

This ensures the concrete doesn't over-constrain the abstract.


*Tags:* extraction, multi-level-analysis, bias-prevention

**Embodied by features:**
- `two-level-architecture-pattern` - Two-Level Architecture Pattern
- `logical-rhetorical-linkage-tracking` - Logical-Rhetorical Linkage Tracking


### `prn_activity_state_gated_automation`

**Automated system behaviors should be gated by detected user activity state, triggering only during quiescent periods rather than interrupting active exploration, because automation during active work creates chaotic interference while automation during rest feels assistive.**

*Rationale:* **Evidence from source:** auto-navigation has to be smarter - if we are still moving our mouse or clicking on multiple selections we should not auto-navigate. this should happen ONLY if we are rest for some time... right now, it's too chaotic

**Why this matters:** Automation that doesn't respect user activity state creates frustrating interference—the system "helps" precisely when the user is actively trying to do something themselves. Temporal sensitivity to user state is essential for automation that feels assistive rather than adversarial.

**Structural kinship:** ['prn_dual_mode_operation (both concern human vs automated control)', 'prn_human_authority_gate (both preserve human agency over consequential actions)', 'prn_adaptive_termination (both involve systems detecting state changes to adjust behavior)']

**Embodied by features:**
- `cascaded-generation-triggers` - Cascaded Generation Triggers
  *variant_of*
- `quiescence-triggered-automation` - Quiescence-Triggered Automation
  *embodies*


### `prn_arbitrary_insertion_architecture`

**Design systems with validated insertion points throughout the workflow rather than fixed input stages, allowing contextual content to be introduced wherever it becomes relevant rather than only at designated entry points.**

*Rationale:* **Evidence from source:** The prompt describes inserting 'news articles even before we generate any through-lines or even before we generate any strategic items, just to enhance the context' and emphasizes that 'there may be some inputs—like news articles and some additional context—that we might want to insert at any point.'

**Why this matters:** Most LLM workflows assume inputs arrive at the start. Real knowledge work discovers relevant context mid-process. Systems that support arbitrary insertion must design prompts that gracefully incorporate new context into ongoing reasoning, not just process initial inputs. This requires prompts that treat context as accumulating rather than fixed.

**Structural kinship:** prn_forward_staged_data_harvesting (information timing), prn_context_completeness (complete situational context)

**Embodied by features:**
- `arbitrary-point-content-injection` - Arbitrary-Point Content Injection
  *embodies*


### `prn_archeological_pattern_mining`

**[DEPRECATED] Treat accumulated work as archeological data to analyze for patterns. Functionality covered by prn_cybernetic_self_correction (process as analyzable data) and prn_dialectical_knowledge_production (patterns emerge through iteration).**

*Rationale:* **Evidence from source:** in my earlier projects i've accumulated a lot of prompts... for analysis with the view of understanding whether my previous techniques/methodology point to distinct engines/bundles/media

**Why this matters:** Past work embodies tacit knowledge that wasn't explicitly articulated. Mining it with fresh analytical frameworks can recover implicit patterns and methodologies.

**Structural kinship:** prn_synthesis_first_bootstrap, prn_theory_grounded_extraction


### `prn_articulation_over_resolution_questioning`

**Generate follow-up questions that help users articulate their uncertainties more 
clearly rather than questions designed to force resolution, because premature 
resolution forecloses productive conceptual development.
**

*Rationale:* Standard LLM patterns aim to resolve user uncertainty. But in concept development, 
the goal is often to help users understand what they're uncertain about more 
precisely—not to eliminate the uncertainty. Questions that clarify the shape of 
uncertainty are more valuable than questions that demand premature answers.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `confirm-explore-articulate-flow` - Confirm-Explore-Articulate Flow


### `prn_assumption_dependency_management`

**Complex interrogation structures should track dependencies between questions and avoid building new questions on unverified assumptions from prior questions—validate foundations before stacking.**

*Rationale:* **Evidence from source:** than stack 10 questions on top of assumptions we haven't probed

**Why this matters:** In multi-question flows, later questions often implicitly assume answers to earlier ones. If those assumptions are wrong, the entire downstream inquiry becomes irrelevant or misleading. This principle demands explicit management of assumption dependencies.

**Structural kinship:** prn_front_load_decisions, prn_logical_coherence, prn_cascade_containment

**Embodied by features:**
- `confirm-then-route-interrogation-pattern` - Confirm-Then-Route Interrogation Pattern
- `assumption-grounded-question-sequencing` - Assumption-Grounded Question Sequencing
  *embodies*


### `prn_bidirectional_modification_symmetry`

**When two elements need reconciliation, treat modification of either element as equally valid options; do not privilege one element's stability over the other without explicit justification.**

*Rationale:* **Evidence from source:** The prompt consistently mentions 'modifying either principles or relationships or both' and 'tweaked one or both elements' - refusing to assume that one category (principles vs features) has inherent priority in modification decisions.

**Why this matters:** Prevents hidden biases in knowledge curation. LLMs given asymmetric instructions might always modify the 'lower-level' element. Symmetry ensures genuine options are surfaced for human decision.

**Structural kinship:** prn_optionality_preservation, prn_deferred_commitment

**Embodied by features:**
- `bidirectional-reformulation-options` - Bidirectional Reformulation Options
  *embodies*


### `prn_bidirectional_process_content_evolution`

**Process structure and content outputs should evolve bidirectionally - the process determines what content is gathered, while accumulated content/results should trigger proposals for process restructuring.**

*Rationale:* **Evidence from source:** Author notes 'LLMs might propose adjustment to the flow as we get results' and emphasizes that this dynamic relationship should be explicit - the process isn't just executed but is itself a subject of evolution based on what emerges.

**Why this matters:** Fixed processes cannot adapt when early results reveal that planned stages are unnecessary or that missing stages are needed. Bidirectional evolution allows the system to become smarter about its own operation as it accumulates evidence about what works.

**Structural kinship:** prn_runtime_strategy_adaptation, prn_schema_data_co_evolution, prn_upstream_regeneration_from_downstream

**Embodied by features:**
- `result-triggered-process-restructuring` - Result-Triggered Process Restructuring
  *embodies*


### `prn_conflict_triage`

**Distinguish routine conflicts (resolvable through aggregation) from substantive tensions (requiring explicit examination) and route accordingly.**

*Rationale:* This principle was discovered through philosophical archaeology of a tool brief.
It represents tacit design knowledge that was implicitly operating but not yet formalized.

**Evidence from source:** The commentary asks when to 'handle reconciliation internally vs. delegating to Cross-Advisor,' suggesting conflicts have different characters requiring different handling.

**Structural kinship:** Related to prn_epistemic_friction (conflict as signal) and prn_cross_model_examination (explicit comparison), but specifically about classification and routing of conflicts rather than just acknowledging their value.


*Tags:* brief-derived

**Embodied by features:**
- `fit-based-evidence-bifurcation` - Fit-Based Evidence Bifurcation
  *embodies*


### `prn_constraint_as_strategy`

**Constraints should drive strategy rather than merely limit execution—explicit resource boundaries enable intelligent allocation and prevent waste on low-value paths.**

*Rationale:* Discovered through philosophical archaeology. Evidence: The brief emphasizes: "There are constraints. We can spend only so many days, so  many queries, and so many hundreds of dollars on a research project. So we have to  strategize." Also: "There is a budget for Phase 1, and the objective is to discover  truly novel authors..." And: "we might switch, pivot, and go for another strategy—or  just launch another Card with a different strategy, even prematurely."

Structural kinship: ['prn_chunking', 'prn_cybernetic_correction']


**Embodied by features:**
- `feat_budget_front_loading` - Budget Front-Loading
  *Created by refactoring engine*
- `cost-explained-processing-choice` - Cost-Explained Processing Choice
  *Re-linked from deprecated principle during refactoring*


### `prn_contextual_extraction_superiority`

**Extraction performed with knowledge of downstream use-context produces superior results to the same extraction performed before context is available, even when this requires processing to occur later in the pipeline.**

*Rationale:* **Evidence from source:** The explicit contrast: 'contextually enhanced extraction of context at a slightly later stage' is preferable to 'a-contextual extraction of context at an early stage' - naming a-contextual processing as specifically inferior.

**Why this matters:** This principle inverts common engineering intuitions about pre-computation; it suggests that for LLM-based systems, just-in-time processing with full context beats cached/pre-computed processing that lacks context.

**Structural kinship:** prn_late_binding_semantic_labels (defer binding until context available), prn_execution_readiness_criteria (explicit criteria before delegation)

**Embodied by features:**
- `full-context-semantic-assessment-pattern` - Full-Context Semantic Assessment Pattern
- `conversation-guided-extraction-targeting` - Conversation-Guided Extraction Targeting
  *embodies*
- `document-collection-staging-without-processing` - Document Collection Staging Without Processing
  *embodies*


### `prn_continuous_background_synthesis`

**Run synthesis operations continuously as a background process throughout data collection rather than deferring synthesis to a distinct final phase, allowing the evolving synthesis state to inform and constrain data gathering at every step.**

*Rationale:* **Evidence from source:** The instruction to 'try to make sense of the weight issue early on and keep refining it throughout the user's answers' treats synthesis not as a terminal operation but as an ongoing parallel process that runs continuously alongside data collection.

**Why this matters:** Deferred synthesis creates a disconnect between data gathering and output generation - systems collect data without knowing whether it will actually resolve synthesis requirements. Continuous synthesis makes collection-synthesis coupling tight enough to detect and correct problems in real-time.

**Structural kinship:** prn_iterative_theory_data_dialectic, prn_serial_global_processing, prn_runtime_strategy_adaptation

**Embodied by features:**
- `dynamic-queue-injection-pattern` - Dynamic Queue Injection Pattern
- `parallel-state-companion-track` - Parallel State Companion Track
- `continuous-background-weight-refinement` - Continuous Background Weight Refinement
  *embodies*


### `prn_contrastive_context_enrichment`

**When providing context to LLMs about user choices or system states, include not just what is but what could have been—the rejected alternatives, unchosen paths, and available-but-unused options—because meaning emerges from contrast.**

*Rationale:* **Evidence from source:** The explicit reasoning that knowing "what we did not choose while choosing what we did choose" provides "detail/depth" for modeling behavior implicitly invokes a contrastive theory of meaning—choices are defined relationally against their alternatives.

**Why this matters:** LLMs interpret user choices more accurately when they understand the choice set, not just the outcome. "User selected option A" means something different depending on whether B was also available or whether A was the only option. Contrastive context enables more precise modeling of user preferences and intent.

**Structural kinship:** ['prn_comprehensive_context (both advocate for richer context provision)', 'prn_lens_dependent_extraction (both recognize that framing affects interpretation)', 'prn_possibility_space (both value preserving awareness of alternatives)']

**Embodied by features:**
- `transformation-state-context-bundle` - Transformation-State Context Bundle
- `distinctiveness-guard-provision` - Distinctiveness Guard Provision
- `refactoring-context-package-assembly` - Refactoring Context Package Assembly
- `commitment-plus-foreclosure-panel` - Commitment-Plus-Foreclosure Panel
- `explicit-criterion-threading-between-llm-calls` - Explicit Criterion Threading Between LLM Calls
  *supports*
- *(+3 more)*


### `prn_criteria_grounded_advisory`

**When requesting advisory output from LLMs, explicitly enumerate the criteria by which the decision should be made, giving the model clear grounds for reasoning rather than leaving it to infer what matters.
**

*Rationale:* **Evidence from source:** The prompt specifies asking "which would better serve our need for abstraction, modularity, comprehensiveness, etc?"—naming the specific criteria by which the choice should be evaluated rather than asking for general advice.


**Why this matters:** Without explicit criteria, LLMs may advise based on inferred or default criteria that don't match the user's actual decision framework. Explicit criteria focus the advisory reasoning and make the basis for recommendations transparent and contestable.


**Structural kinship:** prn_comprehensive_context, prn_theory_grounded_extraction

**Embodied by features:**
- `multi-level-operation-vocabulary` - Multi-Level Operation Vocabulary
- `criteria-enumeration-in-advisory-prompts` - Criteria Enumeration in Advisory Prompts
  *embodies*
- `choice-architecture-constraint` - Choice Architecture Constraint
  *enables*


### `prn_cross_slot_synthesis_scanning`

**Systems should include explicit mechanisms ("factories") that scan across different functional categories to identify potential higher-level connections, rather than relying on ad-hoc or implicit synthesis.**

*Rationale:* **Evidence from source:** we should have some kind of a through-line factory which will scan our functional outline as it exists across all of the slots, and it will try to find larger, more abstract connective tissues that are rhetorical and argumentative.

**Why this matters:** Through-lines and meta-patterns don't emerge automatically from local work—they require explicit cross-cutting analysis. Without a dedicated scanning mechanism, connections between distant parts of an argument remain invisible, and the system produces fragmented rather than unified outputs.

**Structural kinship:** prn_controlled_propagation, prn_gap_aware_processing, prn_framework_expansion_reanalysis

**Embodied by features:**
- `batch-then-synthesize-pattern` - Batch-Then-Synthesize Pattern
  *enables*
- `slot-level-synthesis-abstraction` - Slot-Level Synthesis Abstraction
  *embodies*
- `through-line-factory-pattern` - Through-line Factory Pattern
  *embodies*


### `prn_decision_interface_modality_matching`

**Pre-generated decision support content should be presented through interface affordances (modals, sidebars, collapsibles) that match the cognitive task—comparison requires parallel visibility, exploration requires expandability.**

*Rationale:* **Evidence from source:** The instruction to 'stick it into a modal, sidebar, or something similar' reveals awareness that generated content must be architecturally positioned to support the decision task, not just dumped into the main flow.

**Why this matters:** LLM-generated content for decision support fails when presentation architecture doesn't match decision structure. Recognizing that different decision types require different spatial arrangements improves interface design for AI-assisted choices.

**Structural kinship:** prn_format_for_decision_support, prn_detail_deferral_with_accessibility, prn_visual_state_legibility

**Embodied by features:**
- `decision-support-container-matching` - Decision Support Container Matching
  *embodies*


### `prn_decision_space_propagation`

**When users make selections through an interface, downstream LLM processing should receive not just the selections themselves but the full decision space (available options, chosen options, rejected options) to enable richer modeling of user intent and preferences.**

*Rationale:* **Evidence from source:** The user's key insight that 'knowing what we did not choose while choosing what we did choose enhances the LLM's ability to model our behavior/expectations' goes beyond mere capture—it's about propagating the full decision context as input to subsequent LLM operations. The phrasing 'down the chain/path' suggests awareness of a processing pipeline where this information has value.

**Why this matters:** LLMs model user preferences more accurately when they can see what was rejected alongside what was chosen—this mirrors how preference learning works in RLHF. Systems that only pass forward positive selections lose the contrastive signal that helps LLMs calibrate their understanding of what the user actually wants versus what was merely acceptable.

**Structural kinship:** ['prn_negative_selection_capture (specialization for LLM consumption)', 'prn_contrastive_context_enrichment (operational mechanism)', 'prn_comprehensive_context (domain-specific instance)']

**Embodied by features:**
- `decision-context-bundle` - Decision Context Bundle
  *embodies*


### `prn_default_recommendation_elicitation`

**When seeking LLM advice on choices between generated options, explicitly request a recommended default rather than neutral analysis, because humans conserve cognitive resources by evaluating recommendations rather than weighing unranked options.
**

*Rationale:* **Evidence from source:** "Formulate it in such a way that the LLM would propose a default and we won't have to think about it ourselves"—the explicit design goal is eliciting a recommendation, not just surfacing considerations.


**Why this matters:** LLMs often default to presenting balanced analysis rather than making recommendations, but humans often need recommendations they can accept or override rather than analyses they must synthesize. Explicitly requesting a default changes the output mode from "here are considerations" to "here is what I'd do."


**Structural kinship:** prn_cognitive_load_transfer, prn_format_for_decision_support

**Embodied by features:**
- `recommendation-mode-request` - Recommendation Mode Request
  *embodies*


### `prn_detail_deferral_with_accessibility`

**Pre-generate detailed content (narrative text, full language) but present structural summaries by default (bulletpoints, logic descriptions, transition names), keeping detail collapsed but accessible, so users can maintain big-picture focus while preserving access to instantiation.**

*Rationale:* **Evidence from source:** The prompt requests 'bulletpoint like structure and hide the narrative text but make it easy to unpack/view,' 'focus on big dynamics, not language (even though pre-generate language to give us a feel for it),' and 'include initially collapsed text but focus on the logic of the transition.'

**Why this matters:** Detailed language is necessary for final output but distracting during structural decision-making. This principle enables systems to satisfy both needs: generate detail for completeness but present structure for clarity, letting users control their zoom level.

**Structural kinship:** prn_format_for_decision_support (formatting for evaluation), prn_function_form_phase_separation (separating structure from presentation), prn_intermediary_curation (curating before presenting)

**Embodied by features:**
- `collapsible-detail-architecture` - Collapsible Detail Architecture
  *Implements collapsed-by-default detail with expand-on-demand access*


### `prn_dialogue_emergent_relevance`

**User-LLM conversation itself generates the targeting criteria for what's relevant in source materials, making dialogue a discovery mechanism rather than merely an output channel.**

*Rationale:* **Evidence from source:** The phrase 'the nature of the convo between user the LLM will help us understand what exactly to look for in those documents' treats conversation as generating relevance criteria that couldn't be specified upfront.

**Why this matters:** Recognizing that conversation produces relevance criteria suggests system architectures where document retrieval/extraction systems listen to dialogue state rather than operating on fixed pre-queries.

**Structural kinship:** prn_staged_adaptive_interrogation (questions emerge from prior answers), prn_dialectical_refinement (understanding emerges through cycles)

**Embodied by features:**
- `llm-dual-role-question-answer-processing` - LLM Dual Role Question-Answer Processing
- `dual-channel-progressive-specialization` - Dual-Channel Progressive Specialization
  *embodies*
- `just-in-time-profile-construction` - Just-In-Time Profile Construction
  *supports*
- `conversation-guided-extraction-targeting` - Conversation-Guided Extraction Targeting
  *embodies*


### `prn_domain_transcendent_abstraction`

**Abstract process structures away from any specific domain instantiation so the same operational logic serves multiple domains (journalism, academia, policy) through different parameterization rather than different architectures.**

*Rationale:* **Evidence from source:** The prompt describes the need to move from 'essay flow tool' to 'generic tool' and lists multiple target domains: 'academic article or writing an essay... news piece... foundation... policy reports, reports from grantees.' It explicitly states 'efforts must transcend that and penetrate other institutions.'

**Why this matters:** When prompts are domain-specific, each new domain requires new prompt engineering. Domain-transcendent design means prompts operate on abstract roles (source material, analytical frame, output format) that get instantiated differently per domain. This dramatically reduces prompt proliferation and enables systematic domain transfer.

**Structural kinship:** prn_abstraction_independence (independent abstraction passes), prn_domain_archetypes (categorical templates per domain)

**Embodied by features:**
- `domain-agnostic-initial-architecture` - Domain-Agnostic Initial Architecture
  *embodies*
- `domain-portable-process-architecture` - Domain-Portable Process Architecture
  *embodies*


### `prn_downstream_aware_generation`

**Prompts that generate initial outputs should explicitly encode how those outputs will be processed, transformed, and synthesized in subsequent stages, because generation optimized for immediate coherence often produces outputs poorly suited for downstream operations.**

*Rationale:* **Evidence from source:** The user states "we have to incorporate all these future uses into the prompt that generates initial throughlines" and suggests rewinding to "regenerate throughlines with these future uses in mind"—explicitly arguing that upstream generation must be designed with downstream processing in view.

**Why this matters:** LLM outputs are often well-formed in isolation but structurally incompatible with subsequent processing steps; designing prompts with the full pipeline in mind produces outputs that flow smoothly through multi-stage systems.

**Structural kinship:** prn_capability_addition_cascade_analysis, prn_front_load_decisions

**Embodied by features:**
- `quality-gated-phase-transition` - Quality-Gated Phase Transition
- `stage-contingent-question-calibration` - Stage-Contingent Question Calibration
  *enables*
- `preemptive-output-structure-anticipation` - Preemptive Output Structure Anticipation
  *implements*
- `logical-rhetorical-translation-prerequisites` - Logical-Rhetorical Translation Prerequisites
  *embodies*
- `stage-bridging-extraction-strategy` - Stage-Bridging Extraction Strategy
  *embodies*
- *(+2 more)*


### `prn_dual_outline_constraint`

**Writing requires satisfying both logical validity and rhetorical effectiveness; systems should track both dimensions and their mutual requirements.**

*Rationale:* This principle was discovered through features-first extraction.

**Evidence from brief:** The insistence on 'translation of logical to rhetorical arguments' and that 'materials would be shared across two outlines—serving as evidence, transition, hooks, or rhetorical functions.'

**Structural kinship:** prn_abstraction_independence, prn_logical_coherence

**Why novel:** 

*Tags:* brief-derived, features-first

**Embodied by features:**
- `logical-rhetorical-translation-prerequisites` - Logical-Rhetorical Translation Prerequisites
  *embodies*
- `logical-rhetorical-linkage-tracking` - Logical-Rhetorical Linkage Tracking
- `genre-archetype-function-mapping` - Genre Archetype Function Mapping


### `prn_dynamic_elicitation_injection`

**When anticipated outputs reveal information gaps, strategically inject targeted questions into the interaction flow at opportune moments rather than adhering to predetermined question sequences, treating the question flow itself as dynamically optimizable based on model needs.**

*Rationale:* **Evidence from source:** The phrase 'strategically insert a question or two which will help us make sense of the weights EVEN BEFORE we generated the weightlines' explicitly proposes injecting questions that weren't part of the original flow, driven by the needs of anticipated downstream processing.

**Why this matters:** Fixed question sequences cannot anticipate all information needed for novel output configurations. Dynamic injection allows systems to fill specific gaps identified by anticipatory models, converting passive questionnaires into active information-hunting instruments.

**Structural kinship:** prn_staged_adaptive_interrogation, prn_proactive_insufficiency_signaling, prn_runtime_strategy_adaptation

**Embodied by features:**
- `dynamic-queue-injection-pattern` - Dynamic Queue Injection Pattern
- `non-predetermined-stage-sequencing` - Non-Predetermined Stage Sequencing
  *extends*
- `weight-gap-targeted-question-insertion` - Weight-Gap Targeted Question Insertion
  *embodies*


### `prn_early_gap_modeling_for_progressive_clarification`

**Model gaps in your understanding of the user's intent or concept early in the interaction, so that subsequent questions can be strategically designed to progressively fill those gaps.**

*Rationale:* Without an explicit model of what's unclear, question generation becomes generic or scattershot. By identifying specific gaps early - what aspects of the user's thinking are underdeveloped, ambiguous, or unspecified - the system can generate targeted questions that systematically reduce uncertainty. This transforms questioning from interrogation into collaborative sense-making, where each question visibly addresses a known gap rather than fishing for information.

*Tags:* gap-modeling, progressive-clarification, question-generation, uncertainty-reduction, concept-development

**Embodied by features:**
- `uncertainty-to-question-pipeline` - Uncertainty-to-Question Pipeline
  *This feature IS the implementation of the principle - it creates a direct pipeline from identified/confirmed uncertainties to targeted question generation, ensuring questions fill specific gaps rather than asking generic follow-ups.*
- `confirm-explore-articulate-flow` - Confirm-Explore-Articulate Flow
  *The flow starts with LLM identifying gaps/tensions/questions from user notes - this IS the early gap modeling step. User confirmation then validates which gaps are real, and Stage 2 questions directly target those confirmed gaps.*
- `three-way-uncertainty-typology` - Three-Way Uncertainty Typology
  *The typology (gaps, tensions, questions) provides the vocabulary for modeling different TYPES of gaps, enabling more nuanced subsequent questioning - e.g., questions that help articulate a tension differ from questions that fill an information gap.*


### `prn_embodied_decision_substrate`

**Consequential choices require pre-generation of sufficient concrete material that decision-makers can develop an 'embodied feel' for each option rather than evaluating abstractly described alternatives.**

*Rationale:* **Evidence from source:** The phrase 'full embodied feel for what choosing each of the readings would involve' and the request to 'generate enough mock data to make this happen' indicate that abstract description is insufficient—tangible instantiation is required for proper decision-making.

**Why this matters:** LLMs can cheaply generate concrete instantiations, but prompts often ask only for descriptions of options. Recognizing that decisions require experiential substrate rather than propositional summaries shifts how we structure choice-presenting interfaces.

**Structural kinship:** prn_option_impact_preview, prn_abstract_concrete_progressive, prn_practical_discovery_over_theoretical

**Embodied by features:**
- `substantive-preview-materialization` - Substantive Preview Materialization
- `provisional-formulation-as-knowledge-probe` - Provisional Formulation as Knowledge Probe
  *extends*
- `embodied-decision-substrate-generation` - Embodied Decision Substrate Generation
  *embodies*


### `prn_emergent_choice`

**Genuine choices are not given at the start but emerge through analytical work; systems should track this emergence rather than forcing premature selection.**

*Rationale:* This principle was discovered through features-first extraction.

**Evidence from brief:** The explicit principle that 'We don't have choices - we create them by analyzing corpora for materials.'

**Structural kinship:** prn_abductive_logic, prn_process_as_data

**Why novel:** 

*Tags:* brief-derived, features-first

**Embodied by features:**
- `diagnostic-disambiguation-flow` - Diagnostic Disambiguation Flow
- `reasoning-chain-display` - Reasoning Chain Display
- `choice-creation-through-analysis-cycles` - Choice Creation Through Analysis Cycles
- `cross-pollination-proposition-generation` - Cross-Pollination Proposition Generation


### `prn_epistemic_grounding_before_thesis_generation`

**Gather information about the user's epistemic position and blind spots before generating theses or hypotheses, so that generated content addresses their actual theoretical concerns rather than generic possibilities.**

*Rationale:* Users arrive at concept articulation with tacit theoretical agendas - presuppositions, paradigm dependencies, and unconfronted challenges they may not have explicitly surfaced. By exploring these blind spots BEFORE generating hypotheses, the system can produce theses that are targeted to what the user actually cares about rather than what might generically apply to their topic. This prevents the frustrating experience of reviewing generic hypotheses that miss the user's real concerns.

*Tags:* theory-service, wizard-flow, hypothesis-generation, blind-spots, user-intent

**Embodied by features:**
- `blind-spots-before-hypotheses-flow` - Blind Spots Before Hypotheses Flow


### `prn_event_driven_refinement`

**Knowledge structures should evolve in response to events (new data, external changes, scheduled reviews) rather than only through explicit invocation; systems that can be triggered maintain freshness that imperative-only systems cannot.**

*Rationale:* This principle was discovered through philosophical archaeology of a tool brief.
It represents tacit design knowledge that was implicitly operating but not yet formalized.

**Evidence from source:** The brief specifies five distinct trigger points: "Post-synthesis: After initial schema generation completes. New specimen added: An excellent new example is added to a genre's corpus. Cross-genre trigger: Another genre's schema was refined... Scheduled refinement: Periodic re-engagement to catch drift or staleness. Manual invocation." This event-driven architecture pattern reflects a commitment to schemas as living, responsive artifacts.


**Structural kinship:** ['prn_cybernetic_correction (events as correction triggers)', 'prn_abductive_logic (new data triggers theory refinement)']


*Tags:* brief-derived

**Embodied by features:**
- `staleness-detection-monitor-pattern` - Staleness Detection Monitor Pattern
- `task-driven-pipeline-composition` - Task-Driven Pipeline Composition
  *relates_to*
- `stray-element-as-workflow-trigger` - Stray Element as Workflow Trigger
  *embodies*
- `eternal-ephemeral-extraction-dichotomy` - Eternal-Ephemeral Extraction Dichotomy


### `prn_expansion_constraint_rhythm`

**Progress emerges through rhythmic alternation between expansion and constraint—expand the solution space to exhaustion, then narrow through constraints to reveal what's actually viable, with each cycle illuminating which possibilities were illusory and which remain tractable.**

*Rationale:* **Evidence from source:** Split from prn_constraint_narrowing_as_progre to isolate the rhythmic alternation pattern from the crystallization function.

**Why this matters:** Problem-solving often stalls when stuck in either pure expansion (overwhelm) or pure constraint (premature closure). Explicit rhythm enables sustainable progress.

**Structural kinship:** prn_iterative_theory_data_dialectic, prn_divergent_convergent_cycles, prn_cybernetic_feedback


### `prn_explicit_process_externalization`

**The workflow itself should be an explicit, versioned, user-adjustable data structure that LLMs propose, humans modify, and all processing stages can query - making process design a first-class collaborative artifact rather than implicit system architecture.**

*Rationale:* **Evidence from source:** Author states 'we would probably generate it early on,' 'have an LLM propose that after some initial questions and the user can adjust/modify,' 'keep track of versioning,' and 'the more we are explicit about this flexible dynamism, the better results we'll get.'

**Why this matters:** When process structure is implicit (hardcoded in system design), users cannot meaningfully participate in process design and LLMs cannot reason about or propose process improvements. Externalizing process as queryable data enables both human agency and LLM-driven optimization of the workflow itself.

**Structural kinship:** prn_data_as_program, prn_refinement_versioning, prn_human_authority_gate

**Embodied by features:**
- `cognitive-scaffolding-for-intellectual-navigation` - Cognitive Scaffolding for Intellectual Navigation
- `collaborative-process-design-with-versioning` - Collaborative Process Design with Versioning
  *embodies*


### `prn_extensibility_as_design_criterion`

**When discovering patterns for system design, explicitly optimize for ease of future extension rather than just current completeness, treating "easy to add X later" as a first-class requirement.**

*Rationale:* **Evidence from source:** i want it to be super-easy for us to add things like that once the system is operational so we need to set it up correctly... our overall concern is building a highly modular/configurable system that will be easy to modify/expand in the future

**Why this matters:** This shifts pattern identification from "what exists" to "what structure would make adding new types easy" - a meta-level concern that should shape how categories are discovered and structured.

**Structural kinship:** prn_provisional_structures, prn_schema_data_co_evolution

**Embodied by features:**
- `type-generic-element-processing` - Type-Generic Element Processing
  *embodies*
- `schema-introspective-question-generation` - Schema-Introspective Question Generation
  *supports*


### `prn_externalized_imagination_infrastructure`

**AI systems should function as external cognitive infrastructure that enables imagination and conceptual exploration beyond what working memory and internal visualization can support, making thinkable what cannot be held 'in the head'.**

*Rationale:* **Evidence from source:** The prompt explicitly states the goal is 'the most sophisticated cognitive/imagination support possible' and identifies the limitation as 'users have trouble conceptualizing in their head - when they think unabetted - or on paper when they just write'

**Why this matters:** Reframes LLM systems from question-answering tools to imagination prosthetics - this changes what we build from interfaces that capture answers to environments that enable thinking users couldn't otherwise do

**Structural kinship:** prn_interactive_cognition, prn_possibility_space_architecture

**Embodied by features:**
- `cognitive-scaffolding-for-intellectual-navigation` - Cognitive Scaffolding for Intellectual Navigation
- `cognitive-task-to-scaffolding-modality-matching` - Cognitive Task to Scaffolding Modality Matching
  *embodies*
- `choice-impact-topology-rendering` - Choice-Impact Topology Rendering
  *embodies*
- `provisional-formulation-as-knowledge-probe` - Provisional Formulation as Knowledge Probe
  *embodies*


### `prn_extrapolative_inference_request`

**Ask LLMs not only to analyze what patterns exist in data, but to extrapolate what complementary structures should exist based on discovered patterns - inferring from engines to appropriate media, from problems to solutions.**

*Rationale:* **Evidence from source:** ask to extrapolate and get the LLM to think about what kind of media - a textual memo? a table? a blend of the two? a particular ***KIND*** of gemini visualization? - would be useful in rendering the particular slant

**Why this matters:** This leverages LLMs' strength in pattern completion and analogy - moving from discovered analytical structures to appropriate presentation forms that the author hasn't yet imagined.

**Structural kinship:** prn_downstream_aware_generation, prn_domain_archetypes

**Embodied by features:**
- `trinity-classification-framework` - Trinity Classification Framework
  *enables*


### `prn_fixed_foundation`

**Not everything should be fluid and customizable—certain elements must remain fixed and stable to provide reference points, because understanding and navigation require stable ground from which to perceive variation.**

*Rationale:* Total flexibility is paralyzing. Without constraints, there's no basis for
meaningful variation. A jazz musician improvises within the structure of
chord changes; without that structure, it's just noise.

Fixed elements provide:
- Cognitive anchors for users
- Evaluation criteria for outputs
- Consistent foundations across variations
- Limits that force creative solutions

The key is choosing WHAT to fix. Fix the process structure, not the content.
Fix the evaluation criteria, not the outputs. Fix the interaction patterns,
not the specific interfaces.


*Tags:* constraints, flexibility, grounding, architecture

**Embodied by features:**
- `eternal-ephemeral-extraction-dichotomy` - Eternal-Ephemeral Extraction Dichotomy
- `ai-indispensability-declaration` - AI Indispensability Declaration
  *LLM role declared as fixed architectural constraint*
- `family-strategies-system` - Family Strategies System
  *Strategies form a stable repertoire of approaches*
- `effectors-system` - Effectors System
  *Effectors form a fixed registry—stable ground for flexible strategies*
- `fixed-and-flexible-categories` - Fixed and Flexible Categories
  *Direct manifestation of keeping certain elements rigid while others flex*


### `prn_formalization_as_education`

**When systems translate user intentions from plain language to formal specifications, exposing the translation back to users develops their expertise and expands their conceptual vocabulary.**

*Rationale:* **Evidence from source:** The prompt states users 'express it once' in plain language, then the system shows them formal terms 'so that they develop their imagination and their skill.' The explicit goal is 'walking them through the complexity of the process and immersing them in it' to 'expand their imagination to the point where they would be asking completely novel questions.'

**Why this matters:** This reframes system formalization as a pedagogical opportunity rather than just a translation step. LLM systems that expose their interpretive work to users can serve as teaching tools, not just execution tools—users learn the formal vocabulary that makes them more effective prompt engineers and system collaborators.

**Structural kinship:** prn_tacit_to_explicit, prn_emergence_through_iterative_re

**Embodied by features:**
- `bidirectional-improvement-loop-architecture` - Bidirectional Improvement Loop Architecture
- `reasoning-chain-display` - Reasoning Chain Display
- `translation-map-display` - Translation Map Display
- `expert-transparency-mode` - Expert Transparency Mode
  *supports*
- `plain-language-registry-extension-pipeline` - Plain-Language Registry Extension Pipeline
  *embodies*


### `prn_forward_staged_data_harvesting`

**At each processing stage, extract not only what that stage requires but also data that will serve downstream stages, even when users don't recognize its future relevance, packaging future-oriented extraction within current-stage work.**

*Rationale:* **Evidence from source:** The author says: 'There are surely things we can extract from the user that the user doesn't even know about that, while packaged as functional skeleton work, would actually help us greatly when it comes to doing the rhetorical outline strategy'

**Why this matters:** Users only understand what's relevant to their current task; systems that harvest information for future stages during current-stage work avoid costly backtracking and redundant questioning

**Structural kinship:** prn_downstream_aware_generation, prn_structured_elicitation, prn_early_consequential_decisions

**Embodied by features:**
- `uncertainty-to-question-pipeline` - Uncertainty-to-Question Pipeline
- `first-input-throughline-projection` - First-Input Throughline Projection
  *extends*
- `arbitrary-point-content-injection` - Arbitrary-Point Content Injection
  *relates_to*
- `cascaded-generation-triggers` - Cascaded Generation Triggers
  *embodies*
- `stage-bridging-extraction-strategy` - Stage-Bridging Extraction Strategy
  *embodies*


### `prn_friction_focused_attention_allocation`

**Direct human cognitive effort preferentially toward items that create structural tension or conflict with existing frameworks, treating harmonious integrations as background operations that merit notification but not active attention.**

*Rationale:* **Evidence from source:** The phrase 'the core of the action is on dealing with those that cause friction/conflict' explicitly prioritizes human attention toward conflict cases rather than spreading it across all items equally.

**Why this matters:** LLM systems often demand uniform attention across all outputs; this principle enables intelligent attention allocation by making 'structural fit with existing knowledge' the primary routing criterion, allowing humans to invest cognitive effort where it generates maximum value.

**Structural kinship:** prn_cognitive_division_of_labor, prn_conflict_triage, prn_resource_proportionality

**Embodied by features:**
- `friction-prioritized-attention-allocation` - Friction-Prioritized Attention Allocation
  *embodies*


### `prn_generation_evaluation_separation`

**When LLMs both generate options and advise on selection, these functions should be separated into distinct calls rather than conflated in a single prompt, because generation benefits from expansive creativity while evaluation benefits from constrained comparative reasoning.
**

*Rationale:* **Evidence from source:** The prompt explicitly specifies "first API call to generate values; second API call to ask for advice on how to choose between them"—treating these as fundamentally different cognitive operations requiring different prompting contexts.


**Why this matters:** Conflating generation and evaluation in a single call produces outputs that self-censor during generation or fail to seriously evaluate during selection. Separation allows each call to be optimized for its specific epistemic function, improving both option richness and advice quality.


**Structural kinship:** prn_function_form_phase_separation, prn_chunking

**Embodied by features:**
- `two-stage-generation-advice-pattern` - Two-Stage Generation-Advice Pattern
  *embodies*


### `prn_genre_as_scaffold`

**Genre conventions encode successful patterns of argumentation; making them explicit as functional typologies provides scaffolding for both extraction and composition.**

*Rationale:* This principle was discovered through features-first extraction.

**Evidence from brief:** The emphasis on building 'thorough typology of each genre's logical functions—the archetypes logically, not just rhetorically' and using these to guide what's needed.

**Structural kinship:** prn_paradigm_embodiment, prn_fixed_foundation

**Why novel:** 

*Tags:* brief-derived, features-first

**Embodied by features:**
- `invisible-foundation-pattern` - Invisible Foundation Pattern
- `genre-mediated-template-derivation` - Genre-Mediated Template Derivation
- `genre-indexed-requirement-templates` - Genre-Indexed Requirement Templates
  *embodies*
- `functional-slot-architecture` - Functional Slot Architecture
  *supports*
- `critical-question-prioritization` - Critical Question Prioritization
- *(+3 more)*


### `prn_graduated_intervention_intensity`

**When seeking to resolve system inconsistencies or gaps, attempt minimal interventions first (no changes) before escalating to moderate interventions (single-element changes) and finally maximal interventions (multi-element changes).**

*Rationale:* **Evidence from source:** Step 2 seeks 'direct hits/relationships that we can make without any modifications' before Step 3 proposes 'ways of modifying either principles or relationships or both' - a clear graduation from zero-modification to one-element to both-element changes.

**Why this matters:** Prevents over-engineering by LLMs. Without explicit graduation, LLMs tend toward elaborate solutions. This principle ensures simpler connections are discovered before complex reconciliations are attempted.

**Structural kinship:** prn_resource_proportionality, prn_deferred_commitment

**Embodied by features:**
- `zero-modification-first-assessment` - Zero-Modification-First Assessment
  *embodies*


### `prn_human_authority_gate`

**Consequential modifications to persistent structures require explicit human approval; systems propose, humans dispose. This is not merely compensation for LLM limits but a design commitment to human authority.**

*Rationale:* This principle was discovered through philosophical archaeology of a tool brief.
It represents tacit design knowledge that was implicitly operating but not yet formalized.

**Evidence from source:** The brief repeatedly emphasizes human approval as non-negotiable: "Human review is essential: The tool generates proposals; humans make final decisions." This is listed as both an assumption and a scope constraint ("Fully autonomous schema modification" is explicitly out of scope). The distinction from prn_compensate_llm_limits is that this isn't about capability compensation—it's about authority allocation. Even a perfect LLM should not autonomously modify schemas.


**Structural kinship:** ["prn_compensate_llm_limits (related but distinct—that's about capability, this is about authority)", 'prn_cybernetic_correction (human review as a specific correction mechanism)']


*Tags:* brief-derived

**Embodied by features:**
- `sign-off-vs-articulation-interface-bifurcation` - Sign-Off vs Articulation Interface Bifurcation
- `agency-preserving-response-options` - Agency-Preserving Response Options
- `result-triggered-process-restructuring` - Result-Triggered Process Restructuring
  *constrains*
- `correction-then-commit-gating` - Correction-Then-Commit Gating
  *supports*
- `granular-post-hoc-override-controls` - Granular Post-Hoc Override Controls
  *implements*
- *(+5 more)*


### `prn_impact_topology_materialization`

**Make visible the full network topology of how conceptual choices propagate through an argument or system - not just listing impacts but rendering the structure of dependency and implication that users cannot maintain mentally.**

*Rationale:* **Evidence from source:** Specific reference to 'analysis of impact of defining a concept this way rather than that way, with possible impact/implications on the rest of the argument' - emphasis on what users 'have trouble conceptualizing in their head'

**Why this matters:** Arguments and conceptual systems have complex interdependencies; making these visible enables strategic conceptual decisions rather than ad-hoc choices that create unforeseen inconsistencies

**Structural kinship:** prn_option_impact_preview, prn_change_impact_propagation, prn_possibility_as_foreclosure_warning

**Embodied by features:**
- `choice-impact-topology-rendering` - Choice-Impact Topology Rendering
  *embodies*


### `prn_intellectual_profile`

**Build explicit intellectual profiles—representations of theoretical interests, preferences, and positions—early in the process, because the stronger this profile, the more effective pattern-matching and collaboration with LLMs becomes.**

*Rationale:* For LLMs to help with pattern matching, they need to know what patterns
you're looking for. This requires an explicit representation of your
intellectual interests, theoretical positions, and aesthetic preferences.

Building this profile used to be slow—it emerged implicitly over years of
writing. Now, with customized interfaces that cross-pollinate your thinking
with others' and solicit explicit review of generated connections, the
profile can be built much faster.

The richer the profile, the more effectively LLMs can suggest relevant
connections, filter irrelevant material, and generate aligned outputs.


*Tags:* profile-building, preferences, collaboration, pattern-matching

**Embodied by features:**
- `theory-answer-multiplication` - Theory-Answer Multiplication
  *supports*
- `research-mode-pre-selection` - Research Mode Pre-Selection
  *Early mode selection builds the intellectual profile that enables subsequent pattern-matching*
- `human-in-loop-proposal-review` - Human-in-Loop Proposal Review
  *Feedback learning builds model of reviewer preferences*


### `prn_interpretive_cascade_instantiation`

**When interpretive choices cascade through interconnected structures, instantiate the full downstream revision requirements for each option rather than abstractly describing propagation effects.**

*Rationale:* **Evidence from source:** The prompt requests showing 'what kind of revisions to the parts of the throughline would be needed, depending on which of the sub-options for integrating each reading we go with'—not a description of propagation but actual instantiated revisions.

**Why this matters:** Abstract statements like 'this would require updating X' fail to convey the true cost of changes. Actually generating the revised versions makes costs concrete and comparable, enabling informed selection among interpretive options.

**Structural kinship:** prn_bounded_propagation, prn_capability_addition_cascade_analysis, prn_downstream_aware_generation

**Embodied by features:**
- `resolution-path-virtualization-panel` - Resolution Path Virtualization Panel
- `sub-option-dependent-revision-branching` - Sub-Option Dependent Revision Branching
  *extends*
- `interpretive-choice-cascade-pre-computation` - Interpretive Choice Cascade Pre-Computation
  *embodies*


### `prn_inter_stage_criterion_propagation`

**When multiple LLM invocations collaborate across a multi-stage process, the variables, criteria, and constraints that govern each stage's behavior should be explicitly passed as structured data between stages rather than left implicit or re-derived.**

*Rationale:* **Evidence from source:** Author emphasizes 'the passing of variables/criteria among LLMs' and connects explicit process awareness to 'not only ask the right questions but restructure the process accordingly' - suggesting that criteria propagation is the mechanism by which process-awareness operates.

**Why this matters:** Without explicit criterion propagation, each LLM invocation must infer constraints from context or operate with incomplete information. Explicit propagation creates a coordinated 'nervous system' across the pipeline where upstream decisions properly constrain downstream behavior.

**Structural kinship:** prn_provenance_preservation, prn_decision_space_propagation, prn_contrastive_context_enrichment

**Embodied by features:**
- `answer-accumulating-question-batches` - Answer-Accumulating Question Batches
- `explicit-criterion-threading-between-llm-calls` - Explicit Criterion Threading Between LLM Calls
  *embodies*


### `prn_irrelevance_tolerance_instruction`

**When processing noisy data sources, explicitly instruct LLMs that not all input data will be relevant and that filtering is expected, preventing forced pattern-matching where genuine relevance is absent.**

*Rationale:* **Evidence from source:** clarify in the prompt to the api that some of the data it will be accessing won't be relevant to the task at hand at all - this is a registry of my old prompts, i didn't clear it specifically

**Why this matters:** LLMs tend toward finding patterns and relevance even in noise; explicitly licensing irrelevance recognition prevents hallucinated connections and overfitting to random structure.

**Structural kinship:** prn_wildcard_inclusion_for_complet, prn_content_based_routing

**Embodied by features:**
- `noise-aware-prompt-framing` - Noise-Aware Prompt Framing
  *embodies*


### `prn_late_binding_semantic_labels`

**Establish structural relationships and logical roles early in processing pipelines, but defer binding semantic labels (names, titles, descriptions) until content is fully assembled and context is maximally available.**

*Rationale:* **Evidence from source:** The prompt explicitly states: 'we'll think abstractly in earlier stages - we'll understand that there are logical/structural connections between elements... but we'll name them only at the pre-rendering stage to make sure their names are most adequate to the content.'

**Why this matters:** LLMs generate better labels when they have full context. Early naming forces commitment before understanding is complete, resulting in generic or misaligned labels like 'Level 0: Root Categories' instead of content-appropriate descriptions.

**Structural kinship:** prn_deferred_commitment, prn_abstract_concrete_progressive_

**Embodied by features:**
- `abstract-structural-placeholder-pattern` - Abstract Structural Placeholder Pattern
  *embodies*
- `concretization-stage` - Concretization Stage
  *embodies*


### `prn_latent_expertise_derivation`

**Expert knowledge (best practices, domain conventions) should guide the derivation of user-facing structures without the derivation process or expert knowledge itself being directly surfaced to users.
**

*Rationale:* This pattern enables expert knowledge to shape outputs without overwhelming users with the full complexity of domain conventions. LLMs can internalize best practices and produce appropriately-shaped structures without users needing to specify or even understand those practices.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `invisible-foundation-pattern` - Invisible Foundation Pattern
- `genre-mediated-template-derivation` - Genre-Mediated Template Derivation


### `prn_logical_coherence`

**System modifications should preserve logical coherence by tracking dependencies and re-evaluating proposals in light of accepted changes.**

*Rationale:* This principle was discovered through philosophical archaeology of a tool brief.
It represents tacit design knowledge that was implicitly operating but not yet formalized.

**Evidence from source:** The commentary identifies that 'accepting proposal A changes the context for proposal B' and asks how to handle this. This suggests proposals exist in a logical space where coherence matters.

**Structural kinship:** Related to prn_cybernetic_correction (re-evaluation as feedback) but specifically about maintaining structural integrity of the artifact being modified. Also shares concern with prn_chunking about granularity vs. coherence tradeoffs.


*Tags:* brief-derived

**Embodied by features:**
- `cascading-remediation-protocol` - Cascading Remediation Protocol
- `assumption-grounded-question-sequencing` - Assumption-Grounded Question Sequencing
  *enables*
- `mutual-exclusivity-mapping` - Mutual Exclusivity Mapping
  *supports*
- `edit-impact-tracking` - Edit Impact Tracking
- `versioned-questionnaire-regeneration-pipeline` - Versioned Questionnaire Regeneration Pipeline


### `prn_machine_legible_affordances`

**System capabilities should be discoverable and composable by automated agents, not just humans—machine-readable declarations of what's possible enable programmatic reasoning about action spaces.**

*Rationale:* Discovered through philosophical archaeology. Evidence: The brief describes: "LLMs can evaluate the results and draw on our repertoire of  actions defined in our Registry of Effectors, our Registry of Family Strategies,  and our Registry of AI Operations." Later: "There must be a much tighter schema for  how these Family Strategies work, how we populate them, and how we expose them to  the LLMs so they can pick which combination to run."

Structural kinship: ['prn_llm_first_creative', 'prn_compensate_llm_limits']


**Embodied by features:**
- `feat_llm_readable_capability_registry` - LLM-Readable Capability Registry
  *Created by refactoring engine*
- `role-based-fact-mobilization-on-demand` - Role-Based Fact Mobilization On-Demand
  *Re-linked from deprecated principle during refactoring*


### `prn_multimodal_cognitive_scaffolding`

**Different cognitive tasks (imagining possibilities, tracing implications, articulating beliefs, comparing options) require different scaffolding modalities - questions, visualizations, path-diagrams, and interfaces are all tools in a repertoire that must be matched to cognitive task type.**

*Rationale:* **Evidence from source:** Explicit statement that 'questions are one way to do it but interfaces, visualizations of paths that can be taken, and the implications thereof, etc - all of that is part and parcel of our repertoire too' - and 'questions are like crutches - but so is the UI/interface'

**Why this matters:** Treating questioning as the only elicitation modality misses that thinking involves spatial reasoning, comparison, path-tracing - modalities that text questions alone cannot scaffold

**Structural kinship:** prn_cognitive_task_matched_presentation, prn_decision_interface_modality_matching

**Embodied by features:**
- `input-modality-election-modal` - Input Modality Election Modal
- `cognitive-task-to-scaffolding-modality-matching` - Cognitive Task to Scaffolding Modality Matching
  *embodies*


### `prn_negative_selection_capture`

**What users explicitly reject or pass over during selection processes provides informationally rich context that should be captured and propagated alongside positive selections, because choices are defined as much by what was not chosen as by what was.**

*Rationale:* **Evidence from source:** do we pass on some summary or full info of the clusters we did not select down the chain/path? we should because it's informative knowledge - knowing what we did not choose while choosing what we did choose enhances the LLM's ability to model our behavior/expectations with a bit more detail/depth

**Why this matters:** Most systems only track positive selections, losing the contrastive information that gives choices meaning. When LLMs receive only what was chosen without knowing the alternatives, they lose critical context for understanding user intent. Rejected options reveal the boundary conditions of user preferences—what they explicitly didn't want among viable alternatives.

**Structural kinship:** ['prn_process_as_data (both treat non-output artifacts as valuable)', 'prn_comprehensive_context (both argue for providing seemingly non-essential information)', 'prn_intellectual_profile (both aim to build richer user models)']

**Embodied by features:**
- `uncertainty-to-question-pipeline` - Uncertainty-to-Question Pipeline
- `per-alternative-foreclosure-articulation` - Per-Alternative Foreclosure Articulation
- `hierarchical-sharpen-triggers` - Hierarchical Sharpen Triggers
  *embodies*
- `decision-context-bundle` - Decision Context Bundle
  *enables*


### `prn_option_impact_preview`

**When presenting modification options to users, pre-compute and display their potential impacts on interconnected system elements, transforming selection from local evaluation to system-aware decision-making.**

*Rationale:* **Evidence from source:** The prompt states that 'whatever virtual options are given would need to trigger stress tests of other parts/throughlines' - options should not be evaluated in isolation but with their cascading effects made visible.

**Why this matters:** LLM-generated options often appear locally optimal but have non-obvious system-wide effects. Pre-computing these effects prevents users from accepting changes that create downstream incoherence.

**Structural kinship:** prn_bounded_propagation, prn_capability_addition_cascade_analysis, prn_possibility_as_foreclosure_warning

**Embodied by features:**
- `resolution-path-virtualization-panel` - Resolution Path Virtualization Panel
- `choice-impact-topology-rendering` - Choice-Impact Topology Rendering
  *specializes*
- `interpretive-choice-cascade-pre-computation` - Interpretive Choice Cascade Pre-Computation
  *embodies*
- `propagation-triggered-stress-testing` - Propagation-Triggered Stress Testing
  *embodies*


### `prn_particularity_recovery`

**Abstractions derived from compressed representations must be returned to the particular—understanding advances not by moving from specific to general and stopping, but by using the general as an instrument for re-encountering the specific with new eyes.**

*Rationale:* Every synthesis sacrifices particularity for surveyability; every abstraction purchases scope at the cost of texture. This is not a flaw to avoid but a dialectical necessity to complete. The provisional schema, however crude, accomplishes what unaided attention cannot: it transforms an undifferentiated mass into a structured field of inquiry. Yet the schema remains hollow until it confronts the resistance of individual instances—the friction, exception, and surplus meaning that compression necessarily effaced. Knowledge deepens not through abstraction alone but through the return journey: the general illuminating what the particular contains, the particular revealing what the general overlooked.


*Tags:* dialectics, abstraction, particularity, hermeneutic-circle

**Embodied by features:**
- `concretization-stage` - Concretization Stage
  *enables*


### `prn_perspective_as_structure`

**Intellectual perspectives can be formalized as structured schemas that encode their assumptions, values, and reasoning patterns—making implicit worldviews explicit and operationalizable.**

*Rationale:* Knowledge production doesn't happen in a vacuum—it occurs in a domain of
competing frameworks. Marxism focuses on class struggle; Foucauldianism
on power-knowledge dynamics; each paradigm has its research questions
and interpretive lenses.

Normally, theories get tested through social feedback from colleagues.
But thinkers may hesitate to share for fear of critique. By embedding
paradigms as schemas in tools, we can subject developing theories to
structured critique from multiple perspectives simultaneously—creating
productive intellectual friction without the social costs.


**Embodied by features:**
- `feat_paradigm_schema_embodiment` - Paradigm Schema Embodiment
  *Created by refactoring engine*
- `genre-archetype-function-mapping` - Genre Archetype Function Mapping
  *Re-linked from deprecated principle during refactoring*
- `multi-strategy-research-slicing` - Multi-Strategy Research Slicing
  *Re-linked from deprecated principle during refactoring*


### `prn_possibility_as_foreclosure_warning`

**Present multiple possibilities not merely as options for selection but as warnings about what commitment to any option would foreclose, making the cost of premature commitment visible through the alternatives it eliminates.**

*Rationale:* **Evidence from source:** we want to present the user with embodied possibilities of straightjacketing/pigeonholing their argument early on, to precisely avoid not having considered better options

**Why this matters:** Traditional option presentation emphasizes what you get by choosing. This principle emphasizes what you lose. When users see that choosing throughline A eliminates throughlines B and C, they make more informed commitments. The alternatives serve an epistemic function even if never selected.

**Structural kinship:** prn_contrastive_context_enrichment, prn_negative_selection_capture, prn_front_load_decisions

**Embodied by features:**
- `conditions-of-possibility-interrogation` - Conditions of Possibility Interrogation
- `commitment-plus-foreclosure-panel` - Commitment-Plus-Foreclosure Panel
- `choice-impact-topology-rendering` - Choice-Impact Topology Rendering
  *extends*
- `mutual-exclusivity-mapping` - Mutual Exclusivity Mapping
  *embodies*


### `prn_possibility_space_architecture`

**Systems should pre-generate branching possibility spaces at multiple levels of abstraction, transforming user experience from sequential generation into navigation of pre-populated virtualities that can be selectively actualized.**

*Rationale:* **Evidence from source:** The prompt repeatedly uses 'possibilities spaces,' 'virtualities,' describes wanting to 'create possibilities/virtualities, some of them concrete... some of them concrete/abstract,' and insists on pre-generating options at every level rather than generating on selection.

**Why this matters:** When LLM generation is cheap, the interaction paradigm shifts from 'generate what I ask for' to 'show me the landscape of what's possible.' This enables discovery of options users wouldn't have known to request and makes the decision space tangible rather than abstract.

**Structural kinship:** prn_pre_curation_with_option_prese (pre-curated alternatives), prn_possibility_as_foreclosure_warning (possibilities as decision context), prn_divergence_as_signal (multiple valid outputs)

**Embodied by features:**
- `slot-completion-card-with-pre-generated-options` - Slot Completion Card with Pre-generated Options
- `sub-option-dependent-revision-branching` - Sub-Option Dependent Revision Branching
  *embodies*
- `cascaded-generation-triggers` - Cascaded Generation Triggers
  *Pre-generates branching possibility spaces for navigation*
- `in-slot-option-swapping` - In-Slot Option Swapping
  *Allows navigation within pre-populated option spaces*


### `prn_practical_discovery_over_theoretical`

**When facing complex process design questions, generate early-stage outputs to learn from rather than attempting to theorize the perfect approach, because observing actual system behavior shortens learning cycles more effectively than abstract reasoning.**

*Rationale:* **Evidence from source:** The author explicitly states: 'So instead of solving this question theoretically, we'll actually solve it in practice—that would be the idea, and that would probably shorten the learning cycle and get us where we need to be much faster.'

**Why this matters:** LLM system designers often over-invest in upfront theoretical design when cheap generation allows empirical discovery; recognizing this accelerates development by treating generated outputs as experimental data rather than final products

**Structural kinship:** prn_dialectical_refinement, prn_process_as_data

**Embodied by features:**
- `synthetic-data-ui-scaffolding` - Synthetic-Data UI Scaffolding
- `bidirectional-stage-learning-loop` - Bidirectional Stage Learning Loop
  *embodies*


### `prn_precision_forcing_interrogation`

**Refinement stages should contain questions specifically designed to force precision on vague or underdetermined elements, treating imprecision as a targetable property that questioning can address.**

*Rationale:* **Evidence from source:** The prompt specifies questions that 'will force us to be a bit more precise about concepts and dialectics' - the questioning is not just exploratory but has the explicit goal of tightening precision on theoretical elements

**Why this matters:** LLM-generated questions often explore broadly; questions explicitly designed to force precision produce tighter, more operationalizable outputs rather than expansive but vague elaborations

**Structural kinship:** prn_staged_adaptive_interrogation, prn_dynamic_elicitation_injection, prn_gap_aware_processing

**Embodied by features:**
- `diagnostic-disambiguation-flow` - Diagnostic Disambiguation Flow
- `precision-forcing-refinement-questions` - Precision-Forcing Refinement Questions
  *embodies*


### `prn_presupposition_surfacing_obligation`

**Guided workflows should actively externalize user presuppositions—the tacit theoretical  commitments, paradigmatic assumptions, and epistemic positioning that users bring but  do not spontaneously articulate—treating prior-surfacing as a required operation rather  than an optional refinement.
**

*Rationale:* Users cannot evaluate their own conceptual work without awareness of the presuppositions  structuring it. LLMs can generate questions and provisional articulations that surface  these priors, but only if the system treats surfacing as obligatory infrastructure  rather than optional enrichment.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `conditions-of-possibility-interrogation` - Conditions of Possibility Interrogation


### `prn_proactive_insufficiency_signaling`

**LLMs should recognize when they have identified possibilities but lack sufficient data to evaluate or complete them, explicitly signaling this insufficiency and generating targeted follow-up questions rather than producing incomplete outputs or hallucinating completeness.**

*Rationale:* **Evidence from source:** perhaps the LLM will say: look here I spot some possibilities in terms of throughlines/slots but I don't have enough data... so I have to ask you a bunch of follow-up questions to see if it's feasible

**Why this matters:** LLMs typically generate outputs regardless of input sufficiency, masking gaps with confident-sounding completions. This principle makes data insufficiency a first-class system state that triggers explicit questioning rather than degraded output quality. It transforms the LLM from an oracle into a diagnostic partner.

**Structural kinship:** prn_anthropologist_role, prn_emergence_through_iterative_re, prn_gap_aware_processing

**Embodied by features:**
- `weight-gap-targeted-question-insertion` - Weight-Gap Targeted Question Insertion
  *implements*
- `llm-driven-diagnostic-questioning` - LLM-Driven Diagnostic Questioning
  *embodies*


### `prn_process_parameterized_questioning`

**Questions at any processing stage should be explicitly parameterized by the current process plan, with question types, granularity, and focus determined by which other stages exist or have been removed from the workflow.**

*Rationale:* **Evidence from source:** The author states that if Evidence stage exists, Refinement should ask for 'typologies of examples/event patterns'; if Evidence stage 'has been nuked in flow design,' then Refinement should 'force the user to think of specific examples' - showing that question content is a function of process structure.

**Why this matters:** Without explicit process-awareness, each stage operates with implicit assumptions about what comes before/after, leading to redundant questions, missing information, or inappropriately-scoped inquiries. Making process structure an explicit input to question generation enables truly coordinated multi-stage workflows.

**Structural kinship:** prn_downstream_aware_generation, prn_stage_appropriate_question_types

**Embodied by features:**
- `explicit-criterion-threading-between-llm-calls` - Explicit Criterion Threading Between LLM Calls
  *enables*
- `stage-contingent-question-calibration` - Stage-Contingent Question Calibration
  *embodies*


### `prn_productive_incompletion`

**Not all questions should be resolved—some should be deliberately converted to retained "problematiques" that become structural features of the output, providing narrative tension and marking areas of genuine dialectical openness.**

*Rationale:* **Evidence from source:** we would convert them from questions to problematiques; these will be the kind of elements and areas and domains that we will keep open throughout the essay... it's very important for us to be able to retain that possibility because this will... this is what will provide some kind of narrative tension inside the argument.

**Why this matters:** LLM systems often treat all gaps as defects to be filled. This principle recognizes that intellectual work sometimes requires preserving uncertainty as a feature rather than a bug—marking genuine dialectics rather than papering over them with false resolution. Outputs become richer and more honest.

**Structural kinship:** prn_optionality_preservation, prn_deferred_commitment, prn_closure_matches_problem

**Embodied by features:**
- `three-way-uncertainty-typology` - Three-Way Uncertainty Typology
- `question-to-problematique-conversion` - Question-to-Problematique Conversion
  *embodies*


### `prn_productive_relationship_filtering`

**Not all possible relationships between new data and existing frameworks merit exploration; systems should help identify which relationships would be 'productive' to pursue based on current project needs rather than exhaustively cataloging all connections.**

*Rationale:* **Evidence from source:** The prompt asks to 'understand what kinds of relationships are possible and what kinds would be productive for us to experiment and play with' - distinguishing possible from productive, implying a filtering function.

**Why this matters:** LLMs can identify many relationships but not all are worth pursuing. Helping users focus on productive relationships prevents exhausting attention on low-value connections while missing high-value ones.

**Structural kinship:** prn_resource_proportionality, prn_function_based_on_demand_retri, prn_relevance_latency_tradeoff

**Embodied by features:**
- `productivity-filtered-relationship-exploration` - Productivity-Filtered Relationship Exploration
  *embodies*


### `prn_provisional_articulation_as_catalyst`

**System-generated provisional conclusions, formulations, and intermediate articulations serve as catalysts for extracting tacit user knowledge - the act of seeing an imperfect formulation crystallizes the user's ability to articulate what they actually think.**

*Rationale:* **Evidence from source:** Explicit instruction: 'if you think that outputting some temporary conclusions/answers/formulations for stage 1 will help you extract better answers in stage 2, do not hesitate' - treating provisional outputs as elicitation tools rather than final products

**Why this matters:** Users often know more than they can articulate on demand; seeing provisional framings activates recognition-based knowledge that generation-based questioning cannot reach

**Structural kinship:** prn_embodied_decision_substrate, prn_forward_staged_data_harvesting

**Embodied by features:**
- `slot-completion-card-with-pre-generated-options` - Slot Completion Card with Pre-generated Options
- `non-predetermined-stage-sequencing` - Non-Predetermined Stage Sequencing
  *supports*
- `provisional-formulation-as-knowledge-probe` - Provisional Formulation as Knowledge Probe
  *embodies*


### `prn_reasoning_resource_maximization`

**For tasks requiring strategic reasoning and dynamic adaptation, allocate maximum available computational resources (token limits, reasoning modes, context windows) rather than economizing, because reasoning quality scales with resource availability.**

*Rationale:* **Evidence from source:** Explicit instruction: 'opus 4.5 64 max tokens, 32k tokens reasoning mode' and 'shouldn't spare any resources to unleash LLM's reasoning power.' This is not proportional allocation but maximum allocation for reasoning-heavy work.

**Why this matters:** Many practitioners default to minimizing token usage for cost efficiency, but this principle recognizes that strategic reasoning tasks have qualitatively different resource requirements where economizing degrades output quality non-linearly.

**Structural kinship:** prn_resource_proportionality (inverts the proportionality logic for certain task types), prn_relevance_latency_tradeoff (accepts costs for quality)

**Embodied by features:**
- `maximum-resource-allocation-for-strategic-reasonin` - Maximum Resource Allocation for Strategic Reasoning
  *embodies*


### `prn_refinement_versioning`

**Track and display version numbers on elements that have been regenerated/sharpened, making the history of iterative refinement visible and distinguishing fresh generation from progressively improved elements.**

*Rationale:* **Evidence from source:** The prompt explicitly requests 'add a little version somewhere to display (e.g. v1, v2) - to flag that we have already sharpened some of these elements in earlier gos.'

**Why this matters:** Without version visibility, users lose track of which elements have been refined and which are still raw generations. This creates confusion about where attention has been invested and where further refinement might be valuable.

**Structural kinship:** prn_process_as_data (process as informative data), prn_provenance_preservation (maintaining traceable connections), prn_visual_state_legibility (encoding state visually)

**Embodied by features:**
- `collaborative-process-design-with-versioning` - Collaborative Process Design with Versioning
  *applies*
- `hierarchical-sharpen-triggers` - Hierarchical Sharpen Triggers
  *Tracks version numbers through iterative sharpen cycles*


### `prn_reformulation_before_rejection`

**When elements fail to connect within a knowledge system, explore whether reformulation of one or both elements enables connection before accepting disconnection as legitimate.**

*Rationale:* **Evidence from source:** The prompt explicitly requests 'bridge reformulations that, if only tweaked one or both elements we are trying to match, would result in us establishing a link' - treating disconnection as potentially a formulation problem rather than an ontological fact.

**Why this matters:** LLMs excel at semantic reformulation. This principle transforms apparent knowledge gaps into reformulation opportunities, leveraging LLM paraphrasing capability to increase knowledge graph connectivity.

**Structural kinship:** prn_schema_as_hypothesis, prn_epistemic_friction


### `prn_regeneration_over_retrofitting`

**When foundational assumptions or requirements change, regenerate from earlier pipeline stages rather than attempting to retrofit new requirements onto existing outputs, because LLM generation is cheap while manual integration of incompatible structures is expensive.**

*Rationale:* **Evidence from source:** The user concludes "perhaps we should rewind and regenerate throughlines with these future uses in mind" rather than suggesting modifications to existing throughlines—they prefer clean regeneration over patching.

**Why this matters:** The instinct to preserve existing work often leads to awkward patches and structural compromises; LLM abundance makes regeneration cheap, and clean regeneration typically produces more coherent outputs than retrofitted modifications.

**Structural kinship:** prn_cybernetic_correction, prn_provisional_adaptive_structures

**Embodied by features:**
- `hierarchical-sharpen-triggers` - Hierarchical Sharpen Triggers
  *embodies*


### `prn_relationship_type_taxonomy`

**When integrating source materials with theoretical frameworks, explicitly categorize the type of relationship (illustration, nuance-discovery, challenge, extension) because different relationship types require different processing pathways and have different implications for framework evolution.**

*Rationale:* **Evidence from source:** The prompt enumerates distinct relationship types: 'illustration of the main dynamic,' 'illustration of the previously undetected nuance/sub-dynamic,' 'challenges to the logic of the argument' - implying these categories matter for how material is processed and used.

**Why this matters:** LLMs can process source material more effectively when given an explicit typology of how material might relate to existing structures, enabling targeted extraction and appropriate handling rather than generic summarization.

**Structural kinship:** prn_content_based_routing, prn_domain_archetypes

**Embodied by features:**
- `source-framework-relationship-classification` - Source-Framework Relationship Classification
  *embodies*


### `prn_relevance_latency_tradeoff`

**When additional processing time significantly improves output relevance or personalization, accept latency rather than prioritizing speed—users will wait for responses that demonstrably incorporate their context over immediate generic responses.**

*Rationale:* **Evidence from source:** better to have users waiting for 30 seconds while they expect a new batch of questions but to make questions super-relevant and build off one another/clarified assumptions - than stack 10 questions on top of assumptions we haven't probed

**Why this matters:** Challenges the default engineering assumption that faster is always better. Recognizes that users distinguish between "waiting because system is slow" and "waiting because system is thinking about my specific situation"—the latter builds trust and delivers value.

**Structural kinship:** prn_resource_proportionality, prn_bespoke_contextual


### `prn_schema_reflexive_generation`

**LLM prompts that operate on structured systems should introspect on the current schema to dynamically generate appropriate processing for each structural element type, rather than hardcoding responses for known elements.**

*Rationale:* **Evidence from source:** The requirement that refinement be 'structure-aware' means the system must inspect what elements exist (concepts, dialectics, propositions, future unknowns) and generate questions accordingly, not rely on predetermined question sets for predetermined elements

**Why this matters:** LLM systems that hardcode prompts for specific structural elements become brittle when schemas evolve; systems that generate prompts by reflecting on current schema remain robust through schema changes without prompt rewriting

**Structural kinship:** prn_process_parameterized_questioning, prn_data_as_program, prn_context_driven_generation

**Embodied by features:**
- `schema-introspective-question-generation` - Schema-Introspective Question Generation
  *embodies*


### `prn_semantic_over_algorithmic_for_meaning`

**When assessing semantic relationships, conceptual overlap, meaning shifts, or interpretive adequacy, prefer LLM semantic interpretation with rich context over algorithmic calculation with weights and thresholds, because numeric proxies cannot capture the nuances of meaning that emerge from conceptual relationships.
**

*Rationale:* Engineers default to algorithmic solutions because they're deterministic and testable. This principle provides clear guidance on when to override that default: if the task involves assessing meaning, conceptual coherence, or semantic relationships, algorithmic approaches are categorically insufficient regardless of how sophisticated the weighting scheme. This prevents wasted effort on inherently inadequate solutions.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `algorithmic-proxy-recognition-heuristic` - Algorithmic Proxy Recognition Heuristic
- `full-context-semantic-assessment-pattern` - Full-Context Semantic Assessment Pattern


### `prn_serial_global_processing`

**When processing items sequentially, maintain active global system context and evaluate each item's potential systemic effects rather than treating each processing unit as isolated, because valuable integration opportunities and coherence threats only become visible at the system level.**

*Rationale:* **Evidence from source:** The prompt describes going through PDFs 'one by one' while simultaneously requiring awareness of 'how a tweak in one throughline will affect the other throughlines' and being 'on the lookout for propagation effects' - serial processing with systemic consciousness.

**Why this matters:** LLMs processing items sequentially often lose global context. Explicitly maintaining system awareness during serial processing prevents locally sensible but globally incoherent integrations.

**Structural kinship:** prn_downstream_aware_generation, prn_context_completeness, prn_shared_scaffold_parallel_streams

**Embodied by features:**
- `serial-processing-with-global-throughline-awarenes` - Serial Processing with Global Throughline Awareness
  *embodies*


### `prn_shared_scaffold_parallel_streams`

**When multiple independent work streams must eventually merge, they should share a common structural scaffold that creates natural alignment points, enabling synthesis operations at each scaffold level rather than requiring post-hoc reconciliation.**

*Rationale:* **Evidence from source:** The prompt describes how throughlines share a "unified slot structure" with "slots shared between the overall skeleton of the whole essay AND of the given throughline"—the same functional slots (IMPLICATIONS, INTERVENTIONS) appear in both individual throughlines and the unified essay structure.

**Why this matters:** Without shared scaffolding, merging independent streams requires expensive structural alignment; shared scaffolds make synthesis a matter of content reconciliation within pre-aligned structures rather than simultaneous structural and content negotiation.

**Structural kinship:** prn_cross_slot_synthesis_scanning, prn_cascading_virtuality

**Embodied by features:**
- `throughline-factory-pattern` - Throughline Factory Pattern
  *embodies*


### `prn_sibling_context_for_distinctiveness`

**When synthesizing or modifying elements within a collection, provide explicit context  about unchanged sibling elements to prevent semantic overlap and maintain distinctiveness  across the set.
**

*Rationale:* LLMs generating content in isolation will naturally gravitate toward central tendencies,  creating overlap with sibling elements. Distinctiveness must be explicitly engineered  through contextual constraint rather than assumed from task framing.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `semantic-territory-shift-detection` - Semantic Territory Shift Detection
- `distinctiveness-guard-provision` - Distinctiveness Guard Provision
- `refactoring-context-package-assembly` - Refactoring Context Package Assembly


### `prn_stage_appropriate_question_types`

**Different processing stages require qualitatively different types of questions—structural stages need categorical and logical questions while later stages need flow, narrative, and rhetorical questions—and prompts should adapt question types to stage characteristics.**

*Rationale:* **Evidence from source:** The author distinguishes: 'in the rhetorical outline, we can still do kind of questions with multiple answers, like we did in the functional skeleton, but they would be much more about flow, narrative, argumentation. How is it that we want to make that argument?'

**Why this matters:** Using logical questions at rhetorical stages (or vice versa) produces mismatched outputs; recognizing stage-question alignment improves elicitation effectiveness

**Structural kinship:** prn_staged_processing, prn_function_form_phase_separation

**Embodied by features:**
- `stage-contingent-question-calibration` - Stage-Contingent Question Calibration
  *specializes*


### `prn_staged_adaptive_interrogation`

**Complex interrogation should proceed in sequential stages where each stage's questions are generated based on answers from prior stages, allowing the inquiry to progressively narrow and deepen rather than scattering attention across unvalidated assumptions.**

*Rationale:* **Evidence from source:** first ask a batch of three questions... get users' answers... then we generate a second batch based on those answers and pending strategic items... then we generate the final third batch of questions, incorporating everything from the previous two

**Why this matters:** Prevents the common failure mode of asking all questions upfront, which either overwhelms users or builds on unverified assumptions. Each stage validates foundations before building further, creating a more reliable epistemic structure.

**Structural kinship:** prn_abductive_logic, prn_emergence_through_iterative_re, prn_abstraction_level_sequencing

**Embodied by features:**
- `answer-accumulating-question-batches` - Answer-Accumulating Question Batches
- `curator-sharpener-two-stage-architecture` - Curator-Sharpener Two-Stage Architecture
- `uncertainty-to-question-pipeline` - Uncertainty-to-Question Pipeline
- `confirm-explore-articulate-flow` - Confirm-Explore-Articulate Flow
- `diagnostic-disambiguation-flow` - Diagnostic Disambiguation Flow
- *(+4 more)*


### `prn_staging_processing_separation`

**Distinguish between making resources accessible to a system (staging) and extracting structured content from them (processing); resources should be staged early for availability but processed late when context clarifies extraction requirements.**

*Rationale:* **Evidence from source:** The prompt describes wanting to 'point the tool to some folders with docs' (staging) while 'build up a profile' should happen in a way that's contextually relevant (processing) - treating these as separable operations with different timing requirements.

**Why this matters:** This principle enables system designs where document corpuses are connected but dormant until activated by specific needs, avoiding both the cost of comprehensive pre-processing and the latency of just-in-time document discovery.

**Structural kinship:** prn_function_based_on_demand_retri (mobilize selectively), prn_arbitrary_insertion_architecture (content introduced when relevant)

**Embodied by features:**
- `just-in-time-profile-construction` - Just-In-Time Profile Construction
  *embodies*
- `document-collection-staging-without-processing` - Document Collection Staging Without Processing
  *embodies*


### `prn_strategic_structure_before_tactical_content`

**Allocate structural positions and emphasis weights before generating the specific  content that fills those positions, separating the strategic decision of what to  emphasize from the tactical decision of how to instantiate that emphasis.
**

*Rationale:* When LLMs make strategic and tactical decisions simultaneously, they often optimize  locally (generating good individual items) at the expense of global balance (appropriate  emphasis across categories). Separating these decisions into distinct passes produces  better-balanced outputs.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `pre-allocated-slot-interleaving` - Pre-Allocated Slot Interleaving
- `curator-sharpener-two-stage-architecture` - Curator-Sharpener Two-Stage Architecture


### `prn_structural_fit_assessment_phase`

**Before integrating new content into existing frameworks, explicitly assess the degree of structural fit between the content and target slots, using fit assessment as a routing decision rather than attempting integration first.**

*Rationale:* **Evidence from source:** The prompt's logic assumes a prior determination of which evidence 'naturally fits into supporting the stuff in the slots' versus which 'causes friction'—implying an explicit fit assessment phase before integration attempts.

**Why this matters:** Without explicit fit assessment, systems either over-consult humans (asking about everything) or create downstream cleanup work (integrating first, then discovering conflicts). Pre-integration fit assessment enables intelligent routing and reduces both consultation fatigue and error correction.

**Structural kinship:** prn_execution_readiness_criteria, prn_conflict_triage, prn_staged_processing

**Embodied by features:**
- `fit-based-evidence-bifurcation` - Fit-Based Evidence Bifurcation
  *embodies*


### `prn_structured_integration`

**Approved insights should flow into persistent structures through defined integration pathways rather than accumulating as unstructured additions.**

*Rationale:* This principle was discovered through features-first extraction.

**Evidence from brief:** The explicit enumeration of integration options: 'folding into existing argument, a higher unit of analysis (claim), or generating entirely new argument.'

**Structural kinship:** prn_controlled_propagation, prn_chunking

**Why novel:** 

*Tags:* brief-derived, features-first

**Embodied by features:**
- `provenance-attached-writing-context` - Provenance-Attached Writing Context
- `food-for-thought-integration-pathways` - Food for Thought Integration Pathways


### `prn_substance_instance_tiering`

**Separate archetypal types (substances) from their concrete exemplifications (instances) in a two-tier selection process, requiring users to commit to the abstract category before seeing concrete options, because premature exposure to instances biases toward surface appeal over structural fit.**

*Rationale:* **Evidence from source:** The prompt explicitly separates 'substance' from 'implementation,' requires 'three substances × three instances,' and insists users must 'see substances first and only then choose what instances.' Even openings should have 'archetypal openings - substance - and then fill in the particular examples.'

**Why this matters:** Users often select based on surface linguistic appeal rather than structural appropriateness. Forcing engagement with the abstract archetype first ensures the structural role is understood before concrete instantiation can seduce with attractive but potentially ill-fitted language.

**Structural kinship:** prn_abstract_concrete_progressive_ (dialectic between abstract and concrete), prn_emergent_choice (choices emerge through process), prn_function_form_phase_separation (separating structural from presentational)

**Embodied by features:**
- `substance-instance-matrices` - Substance × Instance Matrices
  *Direct implementation of two-tier substance/instance selection pattern*


### `prn_synthesis_first_bootstrap`

**Bootstrap schemas and typologies from synthesized materials first, then enrich through systematic re-engagement with source texts—synthesis provides the provisional scaffold, original data provides the substantive refinement.**

*Rationale:* The cost structure of LLM operations inverts traditional scholarship: generating initial abstractions from summaries is now cheap, allowing us to produce workable ontologies rapidly. These provisional schemas then serve as structured lenses for re-examining original materials, transforming vague intuitions into rigorous typologies through iterative enrichment rather than upfront exhaustive analysis.


*Tags:* bootstrapping, synthesis, iterative-refinement

**Embodied by features:**
- `genre-archetype-function-mapping` - Genre Archetype Function Mapping


### `prn_theory_grounded_extraction`

**User inputs gain multiplicative generative power when processed through an existing theoretical framework; the theory enables inference, cross-pollination, and gap-filling that raw inputs alone cannot provide.**

*Rationale:* **Evidence from source:** a single answer to a question in the initial questionnaire might not mean much, but once it's operationalized within our broader theoretical project, it becomes much more generative... strategic items that we extract, they would not just be grounded in our answers to the questions, they would also be grounded in our theory.

**Why this matters:** Many LLM workflows treat each user input in isolation, missing the compounding effects of connecting inputs to persistent theoretical frameworks. A theory base acts as a lens that reveals implications invisible to framework-free processing, turning sparse inputs into rich outputs.

**Structural kinship:** prn_comprehensive_context, prn_intellectual_profile, prn_cross_pollination_as_generativ

**Embodied by features:**
- `refactoring-context-package-assembly` - Refactoring Context Package Assembly
- `theory-answer-multiplication` - Theory-Answer Multiplication
  *embodies*


### `prn_type_polymorphic_processing`

**Design LLM processing mechanisms to operate on structural element categories (types) rather than specific instances, enabling automatic inclusion of new instances within existing types without mechanism modification.**

*Rationale:* **Evidence from source:** The prompt distinguishes between the current specific elements ('propositions, concepts, dialectics') and the general principle that 'different structural elements' may be added, requiring the refinement to work at the type level not the instance level

**Why this matters:** When LLM prompts enumerate specific items rather than operating on item types, every schema addition requires prompt updates; type-level operations scale automatically with schema growth

**Structural kinship:** prn_domain_transcendent_abstraction, prn_substance_instance_tiering, prn_extensibility_as_design_criterion

**Embodied by features:**
- `type-generic-element-processing` - Type-Generic Element Processing
  *embodies*


### `prn_upstream_regeneration_from_downstream`

**When users make refinements at lower/later/more-concrete levels of a hierarchy, they should be able to regenerate upstream/earlier/more-abstract elements to make them more bespoke to those downstream choices, enabling bidirectional influence rather than purely top-down determination.**

*Rationale:* **Evidence from source:** The prompt explicitly describes going back to 'regenerate those elements to make them more precise/bespoke based on the choices/refinements we made further down below' and 'regenerate transitions upward' after choosing implementation details - this is not just forward propagation but backward regeneration.

**Why this matters:** Most LLM workflows are purely top-down: generate abstract → refine to concrete → output. This principle recognizes that concrete choices reveal what the abstract SHOULD have been, and cheap regeneration enables iterative coherence that manual editing cannot achieve.

**Structural kinship:** prn_bounded_propagation (bounded change propagation), prn_regeneration_over_retrofitting (regeneration approach), prn_dialectical_refinement (iterative framework-data interaction)

**Embodied by features:**
- `hierarchical-sharpen-triggers` - Hierarchical Sharpen Triggers
  *Enables downstream refinements to trigger upstream regeneration*


### `prn_user_archetype_grounding`

**Frame system design analysis around a specific user archetype and their characteristic questions, providing a north star that distinguishes relevant patterns from interesting-but-irrelevant ones.**

*Rationale:* **Evidence from source:** our guiding question is this: we are targeting researchers who want to make quick sense of the collections of articles without having to read individual pieces. so we need to find ways to make this helpful for them

**Why this matters:** Without an explicit user archetype, pattern identification drifts toward what's structurally interesting rather than what's functionally useful. The user question provides evaluative grounding.

**Structural kinship:** prn_function_based_on_demand_retri, prn_context_completeness

**Embodied by features:**
- `user-question-driven-pattern-discovery` - User-Question-Driven Pattern Discovery
  *embodies*


### `prn_verification_easier_than_generation`

**LLMs are more reliable at verifying whether outputs match inputs than at generating correct outputs initially, because verification is a constrained comparison task while generation requires unconstrained production.**

*Rationale:* **Evidence from source:** The proposal assumes a second LLM checking fields against inputs will catch errors the generating model made, implying verification is a fundamentally more tractable task than generation for LLMs.

**Why this matters:** This principle justifies architectural patterns where cheap verification layers can dramatically improve reliability of expensive generation steps, changing cost-benefit calculations for LLM pipeline design.

**Structural kinship:** prn_generation_evaluation_separation, prn_adversarial_multi_perspective_refinement

**Embodied by features:**
- `input-grounded-field-comparison` - Input-Grounded Field Comparison
  *supports*
- `secondary-llm-verification-layer` - Secondary LLM Verification Layer
  *embodies*


### `prn_visibility_as_quality_forcing`

**Requiring systems to make their reasoning visible and explicable functions not  merely as an audit mechanism but as an active quality-improvement forcing  function, because the act of structuring reasoning for external legibility  improves the reasoning itself.
**

*Rationale:* This reframes visibility requirements from overhead (necessary for compliance)  to investment (directly improving output quality). Systems designed with this  understanding will treat reasoning externalization as a feature, not a cost.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `hierarchical-detail-explanation-trade-off-navigation` - Hierarchical Detail-Explanation Trade-off Navigation


### `prn_visual_state_legibility`

**Interactive interfaces must encode system states (active/inactive, selected/unselected, available/unavailable) through sufficient visual contrast that state is immediately perceivable without cognitive effort.**

*Rationale:* **Evidence from source:** The user's complaint that 'Questions tabs are too pale - the inactive ones are barely visible' diagnoses a failure of visual state encoding. The issue isn't aesthetic preference but functional: users cannot perceive the decision landscape when visual differentiation is insufficient.

**Why this matters:** When users interact with systems to provide input for LLM processing, unclear visual state creates cognitive overhead that degrades decision quality. Users making selections under conditions of visual ambiguity provide noisier signals than those working with clear interfaces.

**Structural kinship:** ['prn_bespoke_contextual (interface design dimension)', 'prn_formalization_as_education (making system state explicit)']

**Embodied by features:**
- `granular-post-hoc-override-controls` - Granular Post-Hoc Override Controls
  *supports*
- `in-slot-option-swapping` - In-Slot Option Swapping
  *embodies*
- `streaming-progress-visibility` - Streaming Progress Visibility
  *embodies*
- `multi-level-possibility-mapping-interface` - Multi-Level Possibility Mapping Interface
  *supports*
- `state-contrast-audit` - State Contrast Audit
  *embodies*


## Process

### `prn_early_issue_confirmation_for_routing`

**Surface potential issues (gaps, ambiguities, uncertainties) early in workflows  and seek user confirmation of their validity before structuring downstream  interrogation, because unconfirmed issues cannot reliably guide question design  while confirmed issues provide stable routing criteria.
**

*Rationale:* Structuring interrogation around unconfirmed issues wastes cognitive effort on  false positives and misses genuine gaps. User confirmation transforms speculative  gap-detection into validated constraints that can legitimately shape the rest  of the workflow.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `curator-sharpener-two-stage-architecture` - Curator-Sharpener Two-Stage Architecture
- `confirm-then-route-interrogation-pattern` - Confirm-Then-Route Interrogation Pattern


### `prn_execution_readiness_criteria`

**Consequential actions should be preceded by verification stages that complete before commitment, treating provisional outputs as hypotheses requiring validation rather than facts requiring execution—because the cost of correction after commitment typically exceeds the cost of verification before commitment.**

*Rationale:* **Evidence from source:** Abduced from prn_correction_before_commitment, which mandated 'verification and correction stages that complete before any changes are committed'—a general pattern about sequencing verification before consequence.

**Why this matters:** This captures the economic logic: verification is cheaper than remediation. It's not specific to LLMs—it applies to any system where actions have consequences and errors are costly to reverse.

**Structural kinship:** Related to prn_human_authority_gate (approval before action), prn_provisional_frameworks (outputs as hypotheses), prn_staged_decomposition (sequential stages).

**Embodied by features:**
- `relationship-invalidation-audit-pattern` - Relationship Invalidation Audit Pattern
- `quality-gated-phase-transition` - Quality-Gated Phase Transition
- `prn_human_authority_gate` - LLM Verification Gate
  *Created by refactoring engine*


### `prn_parallel_epistemic_state_tracking`

**Epistemic gaps, uncertainties, and unresolved positioning should be tracked as  persistent, evolving state throughout a guided workflow—accompanying the user  as a parallel information stream that updates and accumulates rather than being  identified once and forgotten.
**

*Rationale:* Epistemic gaps evolve—some get resolved through subsequent work, new ones emerge,  confirmed gaps shape questioning. Without persistent tracking, the system loses  the ability to adapt interrogation strategy based on accumulated epistemic state  and cannot show users how their understanding has evolved.


*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `parallel-state-companion-track` - Parallel State Companion Track


### `prn_pipeline_completion_gate`

**Before major workflow phase transitions, establish explicit completion checkpoints that force gap-filling and tension resolution, because pipeline transitions amplify upstream incompleteness and downstream stages cannot compensate for structural deficiencies inherited from earlier phases.**

*Rationale:* Recognizing natural 'phase transition boundaries' in LLM pipelines helps architects design appropriate completion-forcing mechanisms at those junctures rather than assuming gradual refinement can always compensate for early gaps.

*Tags:* auto-extracted, from-prompt

**Embodied by features:**
- `quality-gated-phase-transition` - Quality-Gated Phase Transition


### `prn_resource_proportionality`

**Match resource expenditure to task requirements by allocating expensive, high-capability resources to tasks requiring their full capacity while using cheaper, constrained resources for tasks within their capability envelope—because uniform resource allocation wastes capacity on simple tasks and starves complex tasks.**

*Rationale:* **Evidence from source:** Abduced from prn_economic_model_tiering, which described matching model cost/capability to task demands ('cheaper/faster models for constrained tasks', 'expensive models for unconstrained generation').

**Why this matters:** This is the general principle of capability-cost matching: don't use a sledgehammer to crack a nut, don't use a nutcracker on a boulder. It applies beyond LLMs to any resource allocation problem.

**Structural kinship:** Related to prn_capability_based_allocation (match tasks to capabilities), prn_staged_decomposition (different stages have different requirements), prn_front_load_consequential_decisions (allocate attention to high-consequence items).

*Tags:* brief-derived

**Embodied by features:**
- `prn_economic_model_tiering` - LLM Model Tiering
  *Created by refactoring engine*
- `cross-model-economic-verification` - Cross-Model Economic Verification
  *embodies*
- `maximum-resource-allocation-for-strategic-reasonin` - Maximum Resource Allocation for Strategic Reasoning
  *supports*
- `friction-prioritized-attention-allocation` - Friction-Prioritized Attention Allocation
  *supports*
- `productivity-filtered-relationship-exploration` - Productivity-Filtered Relationship Exploration
  *supports*
- *(+2 more)*


### `prn_runtime_strategy_adaptation`

**Systems should continuously re-evaluate strategic approach based on accumulated results and emerging context, rather than committing to fixed execution plans—strategy and execution should be interleaved, not sequential.**

*Rationale:* **Evidence from source:** The demoted principle describes ongoing re-evaluation during execution, suggesting a general pattern beyond LLMs.

**Why this matters:** Pre-planned strategies cannot account for information revealed during execution. Rigid plans waste resources on paths that prove unproductive.

**Structural kinship:** prn_cybernetic_feedback, prn_strategic_nondeterminism, prn_event_driven_refinement

**Embodied by features:**
- `result-triggered-process-restructuring` - Result-Triggered Process Restructuring
  *embodies*
- `feat_llm_continuous_strategy_adaptation` - LLM Continuous Strategy Adaptation
  *Created by refactoring engine*


## Proposed

### `prn_data_as_program`

**Treat data as executable specification—when data structures are sufficiently rich and systems sufficiently generic, data can define behavior without explicit programming, collapsing the distinction between configuration and code.**

*Rationale:* **Evidence from source:** The demoted principle describes context functioning as configuration, suggesting data-driven behavior.

**Why this matters:** Traditional separation of code and data creates artificial boundaries. Rich data structures can encode behavioral specifications.

**Structural kinship:** prn_machine_legible_affordances, prn_explicit_capability_declaration, prn_late_binding_semantic_labels

**Embodied by features:**
- `feat_context_driven_system_specialization` - Context-Driven System Specialization
  *Created by refactoring engine*


### `prn_execution_readiness_criteria`

**Consequential actions should be preceded by verification stages that complete before commitment, treating provisional outputs as hypotheses requiring validation rather than facts requiring execution—because the cost of correction after commitment typically exceeds the cost of verification before commitment.**

*Rationale:* **Evidence from source:** Abduced from prn_correction_before_commitment, which mandated 'verification and correction stages that complete before any changes are committed'—a general pattern about sequencing verification before consequence.

**Why this matters:** This captures the economic logic: verification is cheaper than remediation. It's not specific to LLMs—it applies to any system where actions have consequences and errors are costly to reverse.

**Structural kinship:** Related to prn_human_authority_gate (approval before action), prn_provisional_frameworks (outputs as hypotheses), prn_staged_decomposition (sequential stages).

**Embodied by features:**
- `relationship-invalidation-audit-pattern` - Relationship Invalidation Audit Pattern
- `quality-gated-phase-transition` - Quality-Gated Phase Transition
- `prn_human_authority_gate` - LLM Verification Gate
  *Created by refactoring engine*


### `prn_resource_proportionality`

**Match resource expenditure to task requirements by allocating expensive, high-capability resources to tasks requiring their full capacity while using cheaper, constrained resources for tasks within their capability envelope—because uniform resource allocation wastes capacity on simple tasks and starves complex tasks.**

*Rationale:* **Evidence from source:** Abduced from prn_economic_model_tiering, which described matching model cost/capability to task demands ('cheaper/faster models for constrained tasks', 'expensive models for unconstrained generation').

**Why this matters:** This is the general principle of capability-cost matching: don't use a sledgehammer to crack a nut, don't use a nutcracker on a boulder. It applies beyond LLMs to any resource allocation problem.

**Structural kinship:** Related to prn_capability_based_allocation (match tasks to capabilities), prn_staged_decomposition (different stages have different requirements), prn_front_load_consequential_decisions (allocate attention to high-consequence items).

*Tags:* brief-derived

**Embodied by features:**
- `prn_economic_model_tiering` - LLM Model Tiering
  *Created by refactoring engine*
- `cross-model-economic-verification` - Cross-Model Economic Verification
  *embodies*
- `maximum-resource-allocation-for-strategic-reasonin` - Maximum Resource Allocation for Strategic Reasoning
  *supports*
- `friction-prioritized-attention-allocation` - Friction-Prioritized Attention Allocation
  *supports*
- `productivity-filtered-relationship-exploration` - Productivity-Filtered Relationship Exploration
  *supports*
- *(+2 more)*


## Split

### `prn_change_impact_propagation`

**Changes must propagate through interconnected systems to maintain coherence—local modifications create inconsistencies that must be resolved through propagation to dependent elements, because systems with internal contradictions are unstable.**

*Rationale:* **Evidence from source:** Split from prn_bounded_propagation, which conflated two distinct concerns: the necessity of propagation for coherence, and the necessity of bounds to prevent cascades.

**Why this matters:** This captures the completeness side: without propagation, local changes create global inconsistencies. A database update that doesn't propagate to dependent views leaves the system in contradiction.

**Structural kinship:** Related to prn_propagation_bounds (the containment counterpart), prn_provisional_frameworks (coherent evolution), prn_cybernetic_self_correction (systems maintaining consistency).

**Embodied by features:**
- `transformation-state-context-bundle` - Transformation-State Context Bundle
- `dynamic-coherence-as-system-property` - Dynamic Coherence as System Property
- `staleness-detection-monitor-pattern` - Staleness Detection Monitor Pattern
- `cascading-remediation-protocol` - Cascading Remediation Protocol
- `relationship-invalidation-audit-pattern` - Relationship Invalidation Audit Pattern
- *(+1 more)*


## Uncategorized

### `prn_benchmark_driven_best_practice`

**Analyze exemplary instances to derive patterns that define expectations and guide gap identification**

**Embodied by features:**
- `invisible-foundation-pattern` - Invisible Foundation Pattern
- `genre-mediated-template-derivation` - Genre-Mediated Template Derivation
- `rhetorical-gap-taxonomy` - Rhetorical Gap Taxonomy
  *embodies*
- `genre-indexed-requirement-templates` - Genre-Indexed Requirement Templates
  *enables*


### `prn_closure_matches_problem`

**Match output closure to problem structure: deliver complete answers for well-bounded queries, but generate productive constraints and generative provocations for ambiguous, multi-interpretable problems where premature conclusion forecloses exploration.**

*Rationale:* Different problem types demand different tool behaviors. Closed problems (factual, deterministic, convergent) benefit from definitive resolution. Open problems (interpretive, generative, hermeneutic) benefit from catalytic outputs that expand the solution space rather than collapse it. The tool's role shifts based on problem topology: oracle for clarity, mirror for complexity.

**Embodied by features:**
- `variable-ceiling-valid-at-any-point-workflow` - Variable-Ceiling Valid-At-Any-Point Workflow


### `prn_content_based_routing`

**Different types of content should be routed through different processing pathways based on their epistemic characteristics—match processing intensity and human involvement to content type, with evaluative content requiring human judgment and factual content enabling automated curation.**

**Embodied by features:**
- `context-interpretation-trigger-router` - Context-Interpretation Trigger Router
- `three-way-uncertainty-typology` - Three-Way Uncertainty Typology
- `fit-based-evidence-bifurcation` - Fit-Based Evidence Bifurcation
  *implements*
- `source-framework-relationship-classification` - Source-Framework Relationship Classification
  *supports*


### `prn_cross_pollination_as_generativ`

**Generate new understanding by systematically representing interactions between one's current framework and external source materials**

**Embodied by features:**
- `theory-answer-multiplication` - Theory-Answer Multiplication
  *enables*


### `prn_domain_archetypes`

**Every domain should have categorical templates (archetypes) that provide structure for understanding individual instances; these templates encode expectations.**

**Embodied by features:**
- `rhetorical-gap-taxonomy` - Rhetorical Gap Taxonomy
  *embodies*
- `genre-indexed-requirement-templates` - Genre-Indexed Requirement Templates
  *supports*


### `prn_dual_mode_operation`

**Provide both fully automated and human-supervised modes, allowing progressive delegation as trust in automated processes increases**

**Embodied by features:**
- `context-interpretation-trigger-router` - Context-Interpretation Trigger Router
- `silent-integration-with-disclosure` - Silent Integration with Disclosure
  *supports*
- `cost-explained-processing-choice` - Cost-Explained Processing Choice
  *embodies*


### `prn_early_consequential_decisions`

**In systems with path dependencies, elicit the most consequential information first—including resource budgets, strategic constraints, and critical parameters—because early decisions constrain the entire possibility space of downstream outcomes.**

**Embodied by features:**
- `collaborative-process-design-with-versioning` - Collaborative Process Design with Versioning
  *enables*


### `prn_eternal_ephemeral_dimension_se`

**Systems should distinguish between permanent, context-independent elements and project-specific, version-dependent elements**


### `prn_explicit_capability_declaration`

**Make system capabilities explicitly queryable through structured declarations rather than leaving them implicit in code, enabling both human and automated agents to discover and compose available actions.**


### `prn_flexibility_through_stability`

**Stability in some system elements enables flexibility in others—only from firm ground can we understand what becomes flexible and what becomes personalized, because contrast requires a stable reference frame.**


### `prn_framework_expansion_reanalysis`

**When categorical frameworks expand, use this as a trigger to re-analyze existing data under the expanded framework, not just to classify new data.**


### `prn_function_based_on_demand_retri`

**Extract comprehensively but mobilize selectively based on which function needs to be fulfilled at the moment of use**

**Embodied by features:**
- `just-in-time-profile-construction` - Just-In-Time Profile Construction
  *supports*
- `user-question-driven-pattern-discovery` - User-Question-Driven Pattern Discovery
  *supports*


### `prn_gap_aware_processing`

**Systems should identify what is missing relative to benchmarks and direct extraction efforts toward dimensions that are underrepresented**

**Embodied by features:**
- `rhetorical-gap-taxonomy` - Rhetorical Gap Taxonomy
  *embodies*
- `through-line-factory-pattern` - Through-line Factory Pattern
  *enables*
- `slot-saturation-detection` - Slot Saturation Detection
- `stray-element-as-workflow-trigger` - Stray Element as Workflow Trigger
  *supports*


### `prn_intermediary_curation`

**Interpose processing layers between raw extraction and human attention; curating, clustering, and grouping should be performed by intermediary agents.**


### `prn_pre_curation_with_option_prese`

**Prepare multiple curated streams aligned with anticipated functions so users can choose among pre-organized alternatives rather than curating everything individually**

**Embodied by features:**
- `substance-instance-matrices` - Substance × Instance Matrices
  *embodies*


### `prn_provenance_preservation`

**Maintain traceable connections from synthesized outputs back to source materials to enable verification and contextual enrichment**

**Embodied by features:**
- `inference-provenance-capture-pattern` - Inference Provenance Capture Pattern
- `input-grounded-field-comparison` - Input-Grounded Field Comparison
  *supports*
- `context-limit-splitting-strategy` - Context-Limit Splitting Strategy
  *enables*
- `carryover-relationship-annotation` - Carryover Relationship Annotation
  *embodies*


### `prn_retroactive_schema_refinement`

**Schemas should be living documents that retroactively reshape prior extractions; as understanding improves, historical data should be re-interpreted under the improved framework.**


### `prn_schema_data_co_evolution`

**Organizational schemas should evolve as new knowledge is incorporated, and existing data should be reclassified under improved schemas rather than remaining frozen**

**Embodied by features:**
- `two-level-architecture-pattern` - Two-Level Architecture Pattern


### `prn_strategic_nondeterminism`

**Introduce controlled non-determinism at decision points where creative interpretation or multiple valid solutions exist, rather than forcing deterministic resolution of inherently ambiguous problems.**


### `prn_synthetic_data_for_best_practi`

**Generate hypothetical examples to establish benchmarks when empirical experimentation is impractical**

**Embodied by features:**
- `synthetic-data-ui-scaffolding` - Synthetic-Data UI Scaffolding
- `embodied-decision-substrate-generation` - Embodied Decision Substrate Generation
  *embodies*


### `prn_trajectory_over_identity`

**Prioritize direction and trajectory over specific instances; the role something plays matters more than its individual identity.**

**Embodied by features:**
- `functional-slot-architecture` - Functional Slot Architecture
  *supports*


### `prn_trigger_based_schema_revision`

**New inputs should trigger evaluation of whether existing organizational structures need abstraction, merging, or expansion**


### `prn_wildcard_inclusion_for_complet`

**Include open-ended, unscripted queries alongside structured ones to capture insights that fall outside predefined categories**

**Embodied by features:**
- `noise-aware-prompt-framing` - Noise-Aware Prompt Framing
  *supports*
- `multiple-choice-with-escape-valve-pattern` - Multiple-Choice with Escape Valve Pattern
  *embodies*


---

# Features

## Project: GS HARVESTER

### `ai-indispensability-declaration` - AI Indispensability Declaration

The system explicitly declares that AI is 'completely indispensable' and that future redesigns must preserve LLM composition, execution, and evaluation of queries.

*Description:* The commentary makes an explicit architectural commitment: AI enables the restructuring of processes to ask high-impact questions early, and LLMs are essential for formulating, executing, and monitoring queries. Any redesign must preserve this fundamental role.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_llm_first_creative` - Explicit declaration that LLMs are primary rather than supplementary
- `prn_fixed_foundation` - LLM role declared as fixed architectural constraint


### `exhaustive-effector-audit` - Exhaustive Effector Audit

The system requires periodic audits to ensure all technical capabilities of Google Scholar are captured in the Effector registry.

*Description:* The commentary identifies that current Effectors are not exhaustive—capabilities like law review filtering or site-specific searches are unused. This implies a design commitment to systematically auditing available technical capabilities and ensuring the registry captures them all.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_possibility_space` - Audits ensure the full possibility space of technical capabilities is available
- `prn_compensate_llm_limits` - Expanding Effectors increases non-LLM resources available for compensation


### `direct-registry-modification-pipeline` - Direct Registry Modification Pipeline

The envisioned system shortens the path from meta-learning suggestions to registry modifications, enabling feedback to directly restructure operational schemas.

*Description:* The commentary describes a desired architecture where suggestions from meta-learning can be clustered by AI, reviewed by users (accept/reject/refine), and translated directly into registry modifications by LLMs. The goal is to eliminate intermediary steps between insight and implementation.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_hegelian_abstraction` - Human work shifts to abstract review while LLMs handle implementation
- `prn_cybernetic_correction` - Direct modification enables faster correction cycles


### `exclusion-based-discovery` - Exclusion-Based Discovery

The system uses exclude operators to filter out known entities (authors, sources) in order to surface genuinely novel material.

*Description:* A key tactical pattern is using exclusion to enable discovery—by explicitly excluding known authors and sources, searches can surface novel material that would otherwise be buried beneath landmark results. This combines with date filtering to target recent work by unknown authors.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_epistemic_friction` - Deliberately creating conditions for unfamiliar material to surface
- `prn_compensate_llm_limits` - Using exclusion to compensate for LLM's tendency to know only landmarks


### `meta-learning-module` - Meta-Learning Module

A learning module analyzes LLM responses to think through what new strategies or Effector combinations would be possible, feeding improvements back into the system.

*Description:* The system includes a meta-learning component that analyzes feedback from operations to suggest improvements. While Effectors themselves are fixed, the ways they combine with strategies is not. The module aims to identify patterns in results that suggest new tactical combinations or registry refinements.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_abductive_logic` - Using operational data to refine system theory
- `prn_cybernetic_correction` - System-level self-reflection and adjustment

**Code locations (3):**
- `backend/agents/learning-phase-orchestrator.js:LearningPhaseOrchestrator` (lines 0-0)
- `backend/agents/venn-execution-strategy.js:VennExecutionStrategy` (lines 0-0)
- `backend/agents/reflection-generator.js:ReflectionGeneratorAgent` (lines 0-0)


### `llm-batch-ranking` - LLM Batch Ranking

Final ranking of harvested papers occurs in batches (up to 150-200) through LLM evaluation, selecting top results across all clusters.

*Description:* The final phase involves LLM-based ranking of large batches of papers—potentially 150-200 at a time. Papers are evaluated for relevance to the research goal, with a selection process that narrows to a final set (e.g., 200 pieces) across all clusters. This leverages LLM capacity for rapid relevance assessment.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_chunking` - Batch-based ranking as chunked evaluation process
- `prn_llm_first_creative` - Using LLM judgment for relevance evaluation

**Code locations (2):**
- `backend/rank-all-433-streaming.js:loadPreRankingCheckpoint` (lines 0-0)
- `backend/rank-all-433-streaming.js:rankAllWithStreaming` (lines 0-0)


### `trans-cluster-operations` - Trans-Cluster Operations

Operations that span across all clusters after individual cluster execution, enabling system-wide analysis and citation harvesting for top results.

*Description:* After all clusters complete their four phases, the system performs operations across the entire result set—finding the most promising works across all clusters and doing deep citation work on them. This enables insights that only emerge from seeing results holistically rather than cluster-by-cluster.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_hegelian_abstraction` - Moving from individual clusters to holistic view represents abstraction level shift
- `prn_process_determinism` - Trans-cluster operations are a defined phase building on cluster outputs

**Code locations (1):**
- `generate-viewer.js:generateViewer` (lines 0-0)


### `family-strategies-system` - Family Strategies System

Content and semantics-based search techniques—ways of combining semantic units like thinkers with concepts—that represent cultivated research best practices.

*Description:* Family Strategies are distinct from Effectors in being semantic rather than technical. They describe 'techniques and best practices' for combining semantic units in queries—pairing thinker names with concept names, for instance. They represent accumulated research craft knowledge encoded into reusable patterns.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_fixed_foundation` - Strategies form a stable repertoire of approaches
- `prn_tacit_to_explicit` - Cultivated craft knowledge rendered explicit as named strategies

**Code locations (4):**
- `test-v2-production.js:testMode` (lines 0-0)
- `test-v2-frontend-backend-contract.js:validateComponentContracts` (lines 0-0)
- `test-v2-frontend-backend-contract.js:validateFamilyNames` (lines 0-0)
- *(+1 more)*


### `effectors-system` - Effectors System

Procedural operators that leverage Google Scholar's technical capabilities—date exclusion, parameter filtering, source restriction, exclude operators—to optimize search mechanics.

*Description:* Effectors are defined as 'procedural and operational' mechanisms that exploit the technical capabilities of Google Scholar's query system. They include date restrictions, exclude operators, source filtering, and other mechanical optimizations. They are distinct from semantic strategies and form a fixed registry that LLMs can draw upon.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_compensate_llm_limits` - Technical operations provide non-LLM resources to fill knowledge gaps
- `prn_fixed_foundation` - Effectors form a fixed registry—stable ground for flexible strategies

**Code locations (1):**
- `backend/rank-all-433-streaming.js:prepareResearchContext` (lines 0-0)


### `mid-card-evaluation-and-pivot` - Mid-Card Evaluation and Pivot

At the midpoint of a Card's budget, the system evaluates whether results are satisfactory and can pivot to alternative strategies if not.

*Description:* The system includes explicit checkpoints for mid-course evaluation. If half the budget is spent and results are disappointing, the system can switch strategies, launch a different Card, or abandon the current approach. This includes 'abandoned query checks' to decide whether to use partial results or redo queries.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_process_determinism` - Evaluation points are deterministic even if outcomes are not
- `prn_cybernetic_correction` - Explicit checkpoint for course correction based on performance

**Code locations (3):**
- `backend/test-integration-pagination-effectors.js:runIntegrationTests` (lines 0-0)
- `backend/test-pagination-effectors.js:testCase4_NoFalsePositives` (lines 0-0)
- `backend/test-pagination-effectors.js:testCase1_DomainDriftDetection` (lines 0-0)


### `real-time-query-evaluation-and-correction` - Real-Time Query Evaluation and Correction

LLMs evaluate query results in real-time and draw on registries of possible actions to formulate improved subsequent queries.

*Description:* After each query executes, the system evaluates results and decides how to improve the next query. LLMs can draw on a Registry of Effectors, Family Strategies, and AI Operations to formulate adjustments. This enables flexible strategies that course-correct based on actual results rather than predetermined paths.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_cybernetic_correction` - Direct implementation of self-checking and course correction at every stage
- `prn_abductive_logic` - Using data from queries to refine subsequent query formulation
- `prn_llm_first_creative` - LLM evaluation enables non-deterministic adaptation


### `cards-as-tactical-units` - Cards as Tactical Units

Within the discovery phase, Cards function as 'sub-sub-strategies' with individual budgets, specific search tactics, and evaluation checkpoints.

*Description:* Cards represent the finest granularity of strategic decomposition—individual tactical approaches within the discovery phase. Each Card has a budget allocation, a specific search strategy (e.g., 'get authors from last five years using key terms in title'), and is subject to query-level evaluation. Cards can be abandoned mid-execution if results are disappointing.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_chunking` - Cards are the smallest discrete chunks of the search process
- `prn_cybernetic_correction` - Card-level granularity enables fine-grained course correction

**Code locations (8):**
- `backend/test-pagination-effectors.js:testCase5_EffectorPerformance` (lines 0-0)
- `backend/test-pagination-effectors.js:testCase3_PhaseSpecificThresholds` (lines 0-0)
- `backend/test-pagination-effectors.js:testCase2_MinimumResultsThreshold` (lines 0-0)
- *(+5 more)*


### `anti-recency-discovery-phase` - Anti-Recency Discovery Phase

Phase 1 deliberately fights LLM memory limitations through exclusion-based searches that target recent work missing from training data.

*Description:* The discovery phase has an explicit goal of finding authors, sources, and vocabulary from the last five years that are likely missing from LLM memory due to training cutoffs. It uses exclusion operators to remove known authors while filtering to recent dates, creating a deliberate strategy to surface novel recent work.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_abductive_logic` - Discovery phase gathers new data to refine the knowledge base
- `prn_compensate_llm_limits` - Direct manifestation of actively compensating for LLM cutoff limitations

**Code locations (3):**
- `test-v2-frontend-backend-contract.js:validateModifierRegistry` (lines 0-0)
- `test-v2-frontend-backend-contract.js:validateDateFiltering` (lines 0-0)
- `backend/scholar-year-filter-working.js:searchScholarWithYearFilter` (lines 0-0)


### `llm-memory-extraction-phase` - LLM Memory Extraction Phase

Phase 0 pulls landmark texts, authors, publications, and terms from LLM memory to establish a baseline of known knowledge before seeking novelty.

*Description:* Before active searching, the system extracts what the LLM already 'knows' about the field—landmark works, key figures, important publications. This establishes a baseline that enables the subsequent discovery phase to identify truly novel material by excluding known landmarks.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_compensate_llm_limits` - Extracting memory creates the baseline needed to compensate for cutoff dates
- `prn_llm_first_creative` - Using LLM knowledge generation before external searches


### `four-phase-cluster-execution` - Four-Phase Cluster Execution

Each cluster executes through four distinct phases: Remembering (Phase 0), Discovery (Phase 1), Execution (Phase 2), and Citations (Phase 3).

*Description:* The system structures cluster execution as a four-phase process: first pulling landmarks from LLM memory, then actively discovering recent work not in that memory, then executing large-scale searches with all gathered terms, and finally looking up citations for promising results. This creates a systematic flow from knowledge baseline through expansion to depth.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_process_determinism` - Phases chain together building on each other's work
- `prn_chunking` - Breaking execution into defined phases with distinct purposes

**Code locations (3):**
- `load-from-checkpoints.js:loadFromCheckpoints` (lines 0-0)
- `test-v2-week2-e2e.js:runE2ETest` (lines 0-0)
- `test-v2-frontend-backend-contract.js:validateProgressState` (lines 0-0)


### `user-term-engagement-interface` - User Term Engagement Interface

Users can edit, add, delete, and tinker with terms and clusters before execution begins, enabling substantive engagement with the search strategy.

*Description:* Before execution, users are presented with generated strategies, clusters, and terms that they can modify. They can delete unwanted elements, add new ones, exclude publications or authors, and add terms in other languages. The system is designed to encourage early engagement because quality depends on initial term accuracy.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_thinking_environments` - Interface designed to solicit feedback and enable refinement
- `prn_anthropologist_role` - Structured interface helps externalize tacit knowledge about relevant terms
- `prn_interactive_cognition` - Re-linked from deprecated principle during refactoring


### `fixed-and-flexible-categories` - Fixed and Flexible Categories

The system maintains both universal categories (Concepts, Thinkers) and field-specific flexible categories (Events, Battles, Party Congresses) that adapt to the research domain.

*Description:* Within term categories, some elements are fixed across all research contexts—like Concepts and Thinkers—while others are generated based on the specific field being researched. This creates a scaffold that is partly stable and partly adaptive to the domain's particular taxonomic logic.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_fixed_foundation` - Direct manifestation of keeping certain elements rigid while others flex
- `prn_generative_personalization` - Re-linked from deprecated principle during refactoring
- `prn_bespoke_contextual` - Flexible categories enable domain-appropriate customization

**Code locations (2):**
- `shared/validation/validate-family.js:validateFamilyDefinition` (lines 0-0)
- `shared/validation/validate-family.js:checkFamilyApplicability` (lines 0-0)


### `hierarchical-strategy-structure` - Hierarchical Strategy Structure

Research execution is organized hierarchically: Strategies contain Clusters (sub-strategies), which contain categorized terms including Concepts, Thinkers, and field-specific elements.

*Description:* The system organizes research through multiple nested levels: strategies at the top, clusters as sub-strategies within them, and various categories of terms within clusters. This creates a clear hierarchy from broad approach down to specific search elements, enabling both strategic overview and granular control.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_chunking` - Breaking down the research process into nested smaller chunks
- `prn_hegelian_abstraction` - Multiple levels of abstraction from concrete terms to abstract strategies

**Code locations (2):**
- `backend/rerank-session.js:rerankSession` (lines 0-0)
- `test-trans-cluster-from-checkpoints.js:testTransClusterFromCheckpoints` (lines 0-0)


### `multi-strategy-research-slicing` - Multi-Strategy Research Slicing

The system presents multiple strategic approaches to 'slice the research cake'—chronological, analogical, conceptual, or eclectic—acknowledging that research admits many valid entry points.

*Description:* Rather than imposing a single research methodology, the system pre-generates what seem like the most likely strategies and entry points, presenting them to users. This reflects recognition that research projects can be approached through different lenses and that the choice of lens should be explicit rather than assumed.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_paradigm_embodiment` - Different strategies embody different paradigmatic orientations to research
- `prn_perspective_as_structure` - Re-linked from deprecated principle during refactoring
- `prn_possibility_space` - Presenting multiple strategic options rather than forcing single approach

**Code locations (1):**
- `backend/agents/clustering-agent.js:ClusteringAgent` (lines 0-0)


### `llm-generated-dynamic-questions` - LLM-Generated Dynamic Questions

Follow-up questions are generated by LLMs based on research mode and user answers, creating highly customized interrogation.

*Description:* After the initial mode selection, the system generates 5-6 follow-up questions determined by LLM prompts that depend on both the chosen research mode and previous answers. These questions are pre-generated in real-time, though the commentary notes potential for even more dynamic generation where questions are formulated while users answer previous ones.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_bespoke_contextual` - Questions are personalized to the specific research context
- `prn_llm_first_creative` - Using LLM non-determinism for creative question generation rather than fixed algorithmic questioning
- `prn_anthropologist_role` - LLM-generated questions operationalize the anthropologist function of guided elicitation
- `prn_generative_personalization` - Re-linked from deprecated principle during refactoring


### `front-loaded-critical-questioning` - Front-Loaded Critical Questioning

The system prioritizes getting the most important information first, recognizing that early answers create path dependencies for all subsequent interactions.

*Description:* The system is designed to ask 'big questions first' because knowing critical information early enables proper structuring of all follow-up questions. This acknowledges that there are path dependencies—what users answer early determines what questions make sense later.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_front_load_decisions` - Created by refactoring engine
- `prn_chunking` - Breaking down into stages where early chunks inform later ones
- `prn_process_determinism` - Chaining processes where early outputs structure later inputs


### `research-mode-pre-selection` - Research Mode Pre-Selection

Users must choose their research mode at the beginning, forcing them to confront what they're truly seeking before any queries begin.

*Description:* The system requires users to select a research mode upfront, pre-structuring choices to help users grasp their ideal output. This forces early commitment that enables highly customized subsequent questioning. The modes include options like single-query focus or Venn diagram overlapping disciplines.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_intellectual_profile` - Early mode selection builds the intellectual profile that enables subsequent pattern-matching
- `prn_tacit_to_explicit` - Renders implicit research goals explicit before committing to queries
- `prn_anthropologist_role` - Structured process to help users externalize tacit knowledge about what they actually want

**Code locations (2):**
- `test-v2-frontend-backend-contract.js:validateModeIDAlignment` (lines 0-0)
- `test-v2-frontend-backend-contract.js:validateModeIDs` (lines 0-0)


## Project: asc

### `cascading-remediation-protocol` - Cascading Remediation Protocol

Ordered sequence for addressing multi-layer synchronization after structural transformations.


*Description:* After structural transformation at one layer, execute remediation in dependency order:  (1) identify all layers with dependencies on the transformed layer; (2) for each dependent  layer, identify specific elements requiring remediation; (3) determine remediation type  (remake, update, retire) for each element; (4) execute remediations in order from most  dependent to least dependent, ensuring downstream elements are stable before upstream  elements reference them. This prevents orphaned references and circular invalidation.


*Confidence:* 82% | *Status:* draft

**Embodies principles:**
- `prn_change_impact_propagation`
- `prn_logical_coherence`
- `prn_multi_layer_synchronization_obligation`


### `distinctiveness-guard-provision` - Distinctiveness Guard Provision

Providing existing sibling content as "negative examples" to constrain generation toward distinctiveness.


*Description:* When generating or modifying content that must be distinct from existing siblings, explicitly  provide those siblings not as models to follow but as semantic territory to avoid. Frame the  constraint positively ("be maximally distinct from...") rather than negatively ("don't duplicate...")  to guide the LLM toward productive differentiation rather than anxious avoidance.


*Confidence:* 85% | *Status:* draft

**Embodies principles:**
- `prn_contrastive_context_enrichment`
- `prn_sibling_context_for_distinctiveness`


### `relationship-invalidation-audit-pattern` - Relationship Invalidation Audit Pattern

Explicit enumeration of all relationships invalidated by structural transformation before execution.


*Description:* Before completing any structural transformation, perform an explicit audit that identifies all  elements pointing TO the elements being transformed. For each identified relationship, determine  whether it (a) becomes invalid and requires reconstruction, (b) requires updating to point to  transformed successors, or (c) should be retired entirely. This audit converts implicit cascading  effects into explicit remediation tasks.


*Confidence:* 87% | *Status:* draft

**Embodies principles:**
- `prn_change_impact_propagation`
- `prn_execution_readiness_criteria`
- `prn_transformation_invalidates_references`


### `refactoring-context-package-assembly` - Refactoring Context Package Assembly

A structured technique for assembling complete context before any structural transformation operation.


*Description:* Before instructing an LLM to perform structural refactoring (merge, split, demote), assemble  a context package containing three mandatory components: (1) sibling elements that will remain  unchanged, framed as distinctiveness constraints; (2) the theoretical foundation (vocabulary,  tensions, established concepts) that must be preserved and extended; (3) dependent elements  whose relationships to the transformed elements will require remediation. This package ensures  the LLM has the full context needed for coherent synthesis.


*Confidence:* 90% | *Status:* draft

**Embodies principles:**
- `prn_theory_grounded_extraction`
- `prn_sibling_context_for_distinctiveness`
- `prn_contrastive_context_enrichment`


### `diagnostic-disambiguation-flow` - Diagnostic Disambiguation Flow

When multiple interpretations of user intent or content are viable, use targeted diagnostic questions to narrow ambiguity before committing to resolution paths.

*Description:* Rather than choosing an interpretation implicitly or presenting all possibilities equally, route detected ambiguities through diagnostic questions specifically designed to disambiguate. The questions surface the decision point to users and elicit the information needed to select the appropriate resolution path. This prevents systems from silently resolving ambiguity in ways that don't match user intent.

*Confidence:* 84% | *Status:* draft

**Embodies principles:**
- `prn_precision_forcing_interrogation`
- `prn_emergent_choice`
- `prn_staged_adaptive_interrogation`


### `quality-gated-phase-transition` - Quality-Gated Phase Transition

Establish minimum quality thresholds at phase boundaries that must be satisfied before workflow proceeds to the next major stage.

*Description:* At natural workflow phase transitions (e.g., from structural to rhetorical stages), implement completion gates that assess element-level quality, surface deficiencies, and force remediation attempts. The gate doesn't block proceeding entirely but ensures the system has made its best effort to complete upstream structures, with explicit user acknowledgment of any remaining gaps. This prevents downstream stages from inheriting avoidable structural deficiencies.

*Confidence:* 87% | *Status:* draft

**Embodies principles:**
- `prn_execution_readiness_criteria`
- `prn_downstream_aware_generation`
- `prn_pipeline_completion_gate`


### `slot-completion-card-with-pre-generated-options` - Slot Completion Card with Pre-generated Options

For weak or empty structural slots, display quality status and offer multiple context-inferred completion options for user selection or amendment.

*Description:* Each structural element is assessed for quality (Empty | Weak | Adequate | Strong). For elements below threshold, the system pre-generates multiple completion options by inferring from surrounding context. These appear as selectable cards showing the proposed content, allowing users to select the best fit, modify a selected option, or provide their own content. This pattern preserves user authority while reducing generative burden.

*Confidence:* 92% | *Status:* draft

**Embodies principles:**
- `prn_inferential_prepopulation`
- `prn_provisional_articulation_as_catalyst`
- `prn_possibility_space_architecture`


### `resolution-path-virtualization-panel` - Resolution Path Virtualization Panel

Pre-compute multiple resolution paths for detected tensions, each displayed with commitment framing, foreclosure panels, and live skeleton diffs.

*Description:* When conflicts are detected between evidence and existing structure, the system generates 2-4 resolution paths. Each path is rendered with: (1) commitment panel showing what this path affirms, (2) foreclosure panels showing what each alternative offered that you're passing on, (3) skeleton diff viewer showing current state vs. path-applied state. Users select from pre-virtualized resolutions rather than constructing resolutions themselves.

*Confidence:* 90% | *Status:* draft

**Embodies principles:**
- `prn_option_impact_preview`
- `prn_interpretive_cascade_instantiation`
- `prn_asymmetric_choice_architecture`


### `per-alternative-foreclosure-articulation` - Per-Alternative Foreclosure Articulation

For each rejected alternative, explicitly articulate its unique value proposition that  the user is foregoing.


*Description:* Don't just list alternatives as "not chosen"—for each of B, C, D, generate a specific  statement of what that alternative offered that A does not. This requires understanding  each alternative's distinctive contribution, not just how it differs on shared dimensions.  The output should answer "What specifically would B have given me that I'm now not getting?"


*Confidence:* 88% | *Status:* draft

**Embodies principles:**
- `prn_negative_selection_capture`
- `prn_asymmetric_choice_architecture`
- `prn_tradeoff_versus_property_comparison`


### `substantive-preview-materialization` - Substantive Preview Materialization

Surface actual proposed content (text, changes, additions) rather than descriptions or  summaries of what would change.


*Description:* When displaying options that represent potential changes (adding a seed, modifying a  throughline, integrating evidence), show the actual text/content that would result rather  than meta-descriptions. "The proposed seed: '[actual text]'" beats "✓ Adds a new seed."  Users evaluate the thing itself, not claims about the thing.


*Confidence:* 90% | *Status:* draft

**Embodies principles:**
- `prn_embodied_decision_substrate`
- `prn_substantive_over_meta_description`


### `synthetic-data-ui-scaffolding` - Synthetic-Data UI Scaffolding

Use plausible synthetic data to design and validate UI patterns before populating with  real data.


*Description:* Separate UI structural decisions from data accuracy concerns by having LLMs generate  "reasonable" placeholder data that illustrates the intended format. The UI is evaluated  for whether it supports the cognitive task correctly; data is then regenerated from  real sources once the structure is validated. This accelerates iteration on information  architecture.


*Confidence:* 85% | *Status:* draft

**Embodies principles:**
- `prn_synthetic_data_for_best_practi`
- `prn_practical_discovery_over_theoretical`


### `commitment-plus-foreclosure-panel` - Commitment-Plus-Foreclosure Panel

A UI pattern that displays the selected option's value proposition alongside explicit  per-alternative foreclosure costs.


*Description:* Rather than a symmetric comparison grid, this pattern structures decision support as:  (1) What you're committing to by choosing A [with substantive content], followed by  (2) separate sections for each of B, C, D showing "By passing on [X], you forgo [specific  value X uniquely offered]." Each foreclosed alternative gets its own substantive  explanation of what it would have provided that A doesn't.


*Confidence:* 89% | *Status:* draft

**Embodies principles:**
- `prn_possibility_as_foreclosure_warning`
- `prn_contrastive_context_enrichment`
- `prn_asymmetric_choice_architecture`


## Project: concrete-abstractor

### `human-in-loop-proposal-review` - Human-in-Loop Proposal Review

LLM generates refinement proposals; humans make final decisions on schema modifications.

*Description:* The system analyzes schema-source mismatches and generates specific proposals (split types, merge types, new dimensions, etc.) but does not autonomously modify the schema. Instead, it presents proposals for rapid human review with approve/reject/modify options. Early decisions influence subsequent proposals through feedback learning.


*Confidence:* 90% | *Status:* draft

**Embodies principles:**
- `prn_llm_first_creative` - LLM handles interpretive work, not categorical authority
- `prn_compensate_llm_limits` - LLM proposes, human decides, database stores
- `prn_intellectual_profile` - Feedback learning builds model of reviewer preferences


### `cross-genre-cascade-management` - Cross-Genre Cascade Management

Handle cascading refinements when one genre's schema changes affect other genres' schemas.

*Description:* When this tool refines a genre's schema, it may trigger re-evaluation of other genres that share abstractions or dimensions. The system needs to manage these cascades to prevent infinite loops while maintaining full dynamism—allowing legitimate propagation of insights across genres without runaway recursion.


*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_epistemic_friction` - Cross-genre friction reveals shared inadequacies
- `prn_cybernetic_correction` - Cascades are system-level feedback propagation


### `cost-aware-processing-strategy` - Cost-Aware Processing Strategy

Balance thoroughness of refinement with practical cost constraints through tiered processing and sampling.

*Description:* Full iterative refinement across large corpora using premium LLMs could be expensive. The system should support tiered processing (cheaper models for initial passes, premium models for refinement) and intelligent sampling strategies to maximize insight per dollar spent.


*Confidence:* 80% | *Status:* draft

**Embodies principles:**
- `prn_chunking` - Chunking enables selective high-investment processing
- `prn_compensate_llm_limits` - Different models for different tasks based on capability needs


### `convergence-detection` - Convergence Detection

Determine when iterative refinement has reached diminishing returns and should terminate.

*Description:* The system needs mechanisms to detect when the schema has stabilized—when additional passes through source material produce few or no refinement proposals, or when proposals become increasingly minor. This could involve schema stability metrics, proposal frequency tracking, or human judgment about when to stop.


*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_chunking` - Convergence is measured at chunk boundaries
- `prn_cybernetic_correction` - Meta-level feedback about the process itself


### `reconciliation-handoff-protocol` - Reconciliation Handoff Protocol

Determine when conflicting proposals should be handled internally versus delegated to Cross-Advisor tool.

*Description:* When multiple source files produce conflicting refinement proposals, the system needs logic for deciding whether to reconcile internally (e.g., through confidence scoring or majority voting) or escalate to the Cross-Advisor tool for explicit reconciliation of divergent perspectives.


*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_divergence_as_signal` - Re-linked from deprecated principle during refactoring
- `prn_compensate_llm_limits` - Escalation compensates for single-model limitations
- `prn_epistemic_friction` - Genuine conflicts are epistemically valuable friction
- `prn_cross_model_examination` - Cross-Advisor leverages model diversity for reconciliation


### `trigger-based-invocation` - Trigger-Based Invocation

Automatically initiate schema refinement when specific events occur across the system.

*Description:* The tool can be triggered by multiple events: post-synthesis completion, new specimen added to corpus, another genre's schema modified (cross-genre trigger), scheduled periodic refinement, or manual invocation. This enables dynamic schema evolution in response to system changes.


*Confidence:* 85% | *Status:* draft

**Embodies principles:**
- `prn_abductive_logic` - New data triggers theory revision
- `prn_cybernetic_correction` - Triggers are environmental feedback signals


### `spiral-development-mechanism` - Spiral Development Mechanism

Schema interrogates concrete, concrete reshapes schema, refined schema reveals new aspects previously invisible.

*Description:* Not merely adding examples to a schema, but a genuine spiral: the schema provides a lens for examining sources, sources reveal schema inadequacies, the refined schema enables seeing new patterns in the same sources. Each complete cycle produces a schema that is both more abstract (more universal) and more concrete (more determinate).


*Confidence:* 90% | *Status:* draft

**Embodies principles:**
- `prn_epistemic_friction` - Each turn of the spiral requires confrontation with resistance
- `prn_abductive_logic` - The spiral IS the theory-data movement made concrete


### `schema-versioning-evolution-tracking` - Schema Versioning and Evolution Tracking

Maintain version control or diff-based tracking of how schemas change through refinement iterations.

*Description:* As schemas evolve through multiple refinement passes, the system should track what changed, when, and why. This enables rollback, comparison of schema versions, understanding of schema development trajectory, and auditing of refinement decisions.


*Confidence:* 85% | *Status:* draft

**Embodies principles:**
- `prn_tacit_to_explicit` - Version history makes evolution trajectory explicit
- `prn_chunking` - Each version is a chunk in the evolution timeline


### `resistance-based-refinement` - Resistance-Based Refinement

Use the schema's failure to categorize source material as the generative signal for improvement.

*Description:* The tool specifically looks for where the schema fails to account for what's in the text—where reality resists categorization. These points of failure become the basis for refinement proposals. The friction between abstract schema and concrete instance is not a bug but the primary mechanism of improvement.


*Confidence:* 90% | *Status:* draft

**Embodies principles:**
- `prn_abductive_logic` - Data resistance triggers theory revision
- `prn_epistemic_friction` - Friction between schema and source is the generative mechanism


### `proposal-interdependency-management` - Proposal Interdependency Management

Handle cases where accepting one refinement proposal changes the context for evaluating other proposals.

*Description:* When multiple proposals are generated from the same analysis pass, they may interact—accepting one proposal might make another irrelevant, contradictory, or more/less important. The system needs to either batch proposals with dependency analysis or present them sequentially with re-evaluation after each decision.


*Confidence:* 70% | *Status:* draft

**Embodies principles:**
- `prn_cybernetic_correction` - Re-evaluation after each decision is a correction mechanism
- `prn_chunking` - Dependency tracking adds complexity to chunked processing


### `iterative-schema-enrichment` - Iterative Schema Enrichment

Systematically refine provisional schemas by confronting them with source material through multiple passes.

*Description:* Takes skeletal schemas generated from synthesis and enriches them through iterative re-engagement with original sources. Each iteration identifies where the schema succeeds or fails to capture reality, generates refinement proposals, and updates the schema based on human-approved changes. The process continues until convergence or human termination.


*Confidence:* 95% | *Status:* draft

**Embodies principles:**
- `prn_cybernetic_correction` - Feedback at every iteration drives improvement
- `prn_chunking` - Each pass is a bounded, inspectable step
- `prn_abductive_logic` - The entire refinement cycle IS the theory-data spiral


## Project: cross-advisor

### `probabilistic-regularity-assumption` - Probabilistic Regularity Assumption

The system assumes LLM responses follow probabilistic patterns that, while non-deterministic, are predictable enough to enable systematic cross-learning.

*Description:* The design rests on the assumption that even though LLM outputs are non-deterministic, they exhibit sufficient regularity and pattern that exposing one model to another's reasoning provides genuine learning value. The system treats LLM behavior as probabilistically structured rather than random.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_llm_first_creative` - Acknowledges non-determinism while still finding value in LLM outputs
- `prn_process_determinism` - Justifies building deterministic processes around non-deterministic content

**Code locations (1):**
- `backend/operations/context_builder.py:ContextBuilder.build_context` (lines 0-0)


### `accelerated-domain-modeling` - Accelerated Domain Modeling

The system rapidly builds a model of the problem domain in each LLM's context by exposing it to multiple solution trajectories and critique patterns.

*Description:* Rather than having each model slowly discover domain patterns through its own trial and error, the system accelerates learning by showing each model how multiple approaches play out simultaneously. This compressed exposure to the 'possibility space' of solutions and their failure modes rapidly builds domain understanding.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_possibility_space` - Explores multiple solution trajectories to map the domain
- `prn_abductive_logic` - Builds domain understanding through exposure to multiple data points

**Code locations (2):**
- `backend/demo_operations.py:demo_initial_broadcast` (lines 0-0)
- `backend/app.py:update_context_visibility` (lines 0-0)


### `stress-tested-robust-output` - Stress-Tested Robust Output

The final output has been subjected to multiple rounds of critique, defense, and cross-examination, making it more robust than single-model generation.

*Description:* The system's ultimate goal is producing outputs that have survived extensive scrutiny from multiple perspectives. By the time a solution emerges, it has been challenged, defended, revised, and evaluated through multiple lenses, making it more likely to withstand real-world implementation challenges.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_cybernetic_correction` - Multiple correction cycles improve output quality
- `prn_divergence_as_signal` - Re-linked from deprecated principle during refactoring
- `prn_cross_model_examination` - Cross-examination is the mechanism for stress-testing
- `prn_epistemic_friction` - Friction through critique produces more robust outputs


### `collaborative-implementation-planning` - Collaborative Implementation Planning

After selecting the winning solution, all three models collaborate to determine the specific implementation approach.

*Description:* Once evaluation identifies the best solution, the system doesn't simply execute that model's implementation plan. Instead, all three models contribute to figuring out how to implement the winning proposal, potentially combining insights from different models' implementation strategies.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_divergence_as_signal` - Re-linked from deprecated principle during refactoring
- `prn_chunking` - Separates solution selection from implementation as distinct chunks
- `prn_cross_model_examination` - Continues to leverage multiple model perspectives even after selection

**Code locations (1):**
- `backend/app.py:op_full_cross_review` (lines 0-0)


### `blind-parallel-evaluation` - Blind Parallel Evaluation

An independent evaluation process where all three models rank the best shots without knowing which model produced which solution.

*Description:* After best shots are formulated, all three models participate in evaluating the solutions, but the system conceals authorship to prevent bias. Each model ranks solutions based on merit alone, and these parallel evaluations determine the winning approach.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_epistemic_friction` - Different evaluation perspectives create productive friction in judgment
- `prn_cross_model_examination` - Uses multiple models to evaluate outputs from multiple perspectives
- `prn_divergence_as_signal` - Re-linked from deprecated principle during refactoring

**Code locations (3):**
- `backend/app.py:op_post_rank_cross_review` (lines 0-0)
- `backend/app.py:op_ranking_adjudication` (lines 0-0)
- `backend/app.py:op_full_ranking` (lines 0-0)


### `best-shot-formulation` - Best Shot Formulation

After multiple revision rounds, each model produces its final, best solution incorporating all learning from the process.

*Description:* Following the iterative critique and observation cycles, each model synthesizes everything it has learned—its own revisions, critiques received, and observations of peer approaches—into a single 'best shot' solution. This represents the culmination of the learning process.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_process_determinism` - Defines a clear culmination point in the process flow
- `prn_abductive_logic` - Synthesizes learning from iterative refinement into final output

**Code locations (3):**
- `backend/orchestrator.py:get_operation_description` (lines 0-0)
- `backend/app.py:op_produce_deliverable` (lines 0-0)
- `backend/app.py:op_best_shot` (lines 0-0)


### `iterative-revision-rounds` - Iterative Revision Rounds

The system supports multiple rounds of solution refinement, with user-configurable workflow depth and dependencies.

*Description:* Users can design workflows with varying numbers of revision cycles, where each round builds on previous critiques and observations. The system provides flexibility in how many rounds to run while maintaining certain dependencies like ranking steps that must occur after solution generation.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_abductive_logic` - Iterative refinement spirals toward better understanding
- `prn_cybernetic_correction` - Multiple rounds enable course correction at each stage
- `prn_chunking` - Breaks the process into explicit stages with defined insertion points
- `prn_process_determinism` - Creates deterministic process structure while allowing non-deterministic content

**Code locations (6):**
- `backend/app.py:create_workflow_profile` (lines 0-0)
- `backend/workflow_executor.py:run_workflow` (lines 0-0)
- `backend/models.py:WorkflowStepResult` (lines 0-0)
- *(+3 more)*


### `meta-exposure-to-peer-work` - Meta-Exposure to Peer Work

Each model sees not only critiques of its own work but also how other models solved the problem and what critiques they received.

*Description:* Beyond receiving direct feedback, each model observes the complete problem-solving and critique cycles of the other models. Claude sees GPT's solution and the critiques GPT received, and Gemini's solution and its critiques. This creates a meta-level learning environment where models learn from observing peer performance and peer mistakes.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_abductive_logic` - Multiple solution trajectories provide data for refining domain understanding
- `prn_cross_model_examination` - Extends cross-examination to include observation of peer processes
- `prn_divergence_as_signal` - Re-linked from deprecated principle during refactoring

**Code locations (1):**
- `backend/app.py:get_context_visibility` (lines 0-0)


### `selective-critique-integration` - Selective Critique Integration

Models are instructed to discern and selectively accept or reject feedback rather than blindly incorporating all suggestions.

*Description:* After receiving critiques, each model must actively evaluate the feedback and decide whether to defend its original approach or accept modifications. The system explicitly instructs models to 'discern, not just blindly accept everything,' treating them as agents with judgment rather than passive recipients of correction.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_epistemic_friction` - The resistance and selective acceptance creates productive friction
- `prn_cybernetic_correction` - Models self-correct through judgment rather than mechanical acceptance


### `multi-model-cross-examination` - Multi-Model Cross-Examination

Three different LLM models (Claude, Gemini, GPT) simultaneously solve the same problem and critique each other's solutions.

*Description:* Each model generates its own solution to the user's problem, then receives critiques from the other two models. This creates a triangulated approach where no single model's perspective dominates. The system orchestrates parallel problem-solving followed by structured mutual critique.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_possibility_space` - Generates multiple solution approaches to explore the problem space
- `prn_divergence_as_signal` - Re-linked from deprecated principle during refactoring
- `prn_epistemic_friction` - Creates productive conflict between different model perspectives
- `prn_cross_model_examination` - Directly implements cross-model examination as the core mechanism

**Code locations (2):**
- `backend/orchestrator.py:evaluate_conversation_state` (lines 0-0)
- `backend/workflow_executor.py:WorkflowExecutor` (lines 0-0)


## Project: dictation-features

### `provenance-attached-writing-context` - Provenance-Attached Writing Context

Food for thought items carry provenance tracking that attaches as context during the writing stage.

*Description:* The system tracks where each food for thought item originated and how it was integrated into the outline. During writing execution, this provenance attaches as context, enabling the generation to draw on the original sources and reasoning that led to each element. This creates traceability from final prose back to corpus origins.

*Confidence:* 84% | *Status:* draft

**Embodies principles:**
- `prn_bespoke_contextual`
- `prn_structured_integration`
- `prn_generative_personalization` - Re-linked from deprecated principle during refactoring
- `prn_process_as_data`


### `abundance-carrying-with-deferred-closure` - Abundance Carrying with Deferred Closure

For factual information, the system maintains multiple possibilities throughout the process, deferring selection until writing.

*Description:* Rather than closing prematurely on which facts to use, the system carries abundance—maintaining multiple possibilities for factual information until the end. Selection happens based on the role facts play at writing time. Users focus on the vector (direction and function) rather than particularities. This contrasts with evaluative claims that do require earlier commitment.

*Confidence:* 87% | *Status:* draft

**Embodies principles:**
- `prn_adaptive_termination`
- `prn_epistemic_weight_routing`
- `prn_deferred_selection`
- `prn_optionality_preservation`
- `prn_possibility_space`


### `plain-language-direction-with-llm-classification` - Plain Language Direction with LLM Classification

Users express intentions in natural language while LLMs handle classification into logical outline structures and pattern-matching.

*Description:* Instead of requiring users to classify how claims fit the logical outline, users describe broader directions in plain language. LLMs perform the classification, pattern-matching what facts or claims are needed to fulfill stated functions. Users say 'I would like to illustrate this' and the system surfaces what's available, or coaching indicates 'There are gaps your outline that best exemplars would normally feature.'

*Confidence:* 88% | *Status:* draft

**Embodies principles:**
- `prn_hegelian_abstraction`
- `prn_genre_as_scaffold`
- `prn_thinking_environments`
- `prn_anthropologist_role`
- `prn_interactive_cognition` - Re-linked from deprecated principle during refactoring


### `choice-creation-through-analysis-cycles` - Choice Creation Through Analysis Cycles

The system recognizes that clean choices don't exist at the start but emerge through extraction, re-analysis, and understanding implications.

*Description:* Rather than presuming available material choices from the start, the system manages the gradual emergence of choices through work cycles. Initially there are no clean choices—they are created by analyzing corpora for materials, organizing by genre function expectations, and reviewing fit with both genre best practices and the central argument. Only at the end of the cycle do genuine choices become available.

*Confidence:* 89% | *Status:* draft

**Embodies principles:**
- `prn_schema_as_hypothesis`
- `prn_emergent_choice`
- `prn_abductive_logic`


### `pre-curated-cluster-streams-with-bundle-selection` - Pre-Curated Cluster Streams with Bundle Selection

Curatorial agents pre-curate multiple streams of fact clusters, allowing users to select at the bundle level rather than evaluating individual items.

*Description:* Based on best practices and functional requirements, curatorial agents pre-curate three (or more) streams of clustered facts. Users choose among these curated bundles rather than individually reviewing all items. This enables steering by 'direction of travel' within broader teleology—the rest can be fetched and curated later, even during writing.

*Confidence:* 88% | *Status:* draft

**Embodies principles:**
- `prn_front_load_decisions`
- `prn_epistemic_weight_routing`
- `prn_optionality_preservation`
- `prn_possibility_space`
- `prn_hegelian_abstraction`
- `prn_deferred_selection`


### `logical-rhetorical-linkage-tracking` - Logical-Rhetorical Linkage Tracking

The system maintains explicit links between logical propositions and rhetorical requirements, tracking gaps and triggering targeted extraction.

*Description:* For every genre archetype, the system maps what rhetorical propositions require what logical propositions. This creates a benchmark linking logical and rhetorical outlines. The system tracks what's amiss—where rhetorical needs lack logical support—and pushes for targeted extraction to fill gaps. Materials may serve different functions across the two outlines (evidence, transition, hooks).

*Confidence:* 86% | *Status:* draft

**Embodies principles:**
- `prn_genre_as_scaffold`
- `prn_abstraction_independence`
- `prn_dual_outline_constraint`
- `prn_cybernetic_correction`


### `food-for-thought-integration-pathways` - Food for Thought Integration Pathways

Approved propositions integrate into the outline through explicit pathways: fold into existing argument, elevate to claim, or generate new branch.

*Description:* When a user approves a food for thought item, the system facilitates choosing an integration pathway: folding it into an existing argument (enrichment), using it to generate a higher unit of analysis (claim), or creating an entirely new argument branch (expansion). LLMs facilitate this choice by presenting options appropriate to the proposition's nature.

*Confidence:* 87% | *Status:* draft

**Embodies principles:**
- `prn_llm_first_creative`
- `prn_structured_integration`
- `prn_controlled_propagation`


### `cross-pollination-proposition-generation` - Cross-Pollination Proposition Generation

The system generates propositions as discrete units of cross-pollination between user hypothesis and corpus content.

*Description:* Cross-pollination occurs between the user's current argument/thesis and corpus materials, generating 'propositions' (food for thought) as individual reviewable units. Each proposition pre-generates a potential path for the argument. Users review whether propositions advance their argument in depth (deepening existing claims) or breadth (expanding into new territory).

*Confidence:* 91% | *Status:* draft

**Embodies principles:**
- `prn_emergent_choice`
- `prn_deferred_selection`
- `prn_tacit_to_explicit`
- `prn_chunking`
- `prn_epistemic_friction`


### `role-based-fact-mobilization-on-demand` - Role-Based Fact Mobilization On-Demand

Facts are extracted comprehensively but mobilized on-demand based on the functional role they need to fulfill.

*Description:* Rather than pre-selecting facts during curation, the system extracts all available facts and determines which to mobilize based on declared function. The function defines what's needed: 'To illustrate ideas, how life shaped ideas, or introduce someone unknown? Depending on function, the facts we extract will differ.' Even at writing stage, additional facts can be fetched for anecdotes.

*Confidence:* 89% | *Status:* draft

**Embodies principles:**
- `prn_possibility_space`
- `prn_optionality_preservation`
- `prn_deferred_selection`
- `prn_compensate_llm_limits`
- `prn_registry_exposed_to_llm`
- `prn_machine_legible_affordances` - Re-linked from deprecated principle during refactoring


### `genre-archetype-function-mapping` - Genre Archetype Function Mapping

Each genre archetype has a defined typology of logical functions and rhetorical expectations that guide extraction and review.

*Description:* For each genre (intellectual profile, ideas essay, etc.), the system maintains a breakdown of expected functions and logical clusters. Review happens based on function ('This looks like a good element for our contextualization function'). A Perry Anderson piece requires certain rhetorical propositions which require certain logical propositions—this mapping guides what to extract and identifies gaps.

*Confidence:* 88% | *Status:* draft

**Embodies principles:**
- `prn_genre_as_scaffold`
- `prn_synthesis_first_bootstrap`
- `prn_paradigm_embodiment`
- `prn_perspective_as_structure` - Re-linked from deprecated principle during refactoring
- `prn_dual_outline_constraint`


### `tiered-material-classification-with-differential-review` - Tiered Material Classification with Differential Review

Materials are classified into ideational claims requiring human review versus factual data delegated to LLM curation.

*Description:* The system separates 'critical, evaluative, provocative, contrarian units of food for thought from cross-pollination' that require careful human review from 'factual claims from corpora' that can be delegated to curatorial agents for clustering and grouping. Ideational claims shape the logical outline directly; factual data is mobilized on-demand based on functional requirements without individual review.

*Confidence:* 91% | *Status:* draft

**Embodies principles:**
- `prn_resource_proportionality`
- `prn_hegelian_abstraction`
- `prn_epistemic_weight_routing`
- `prn_human_authority_gate`


### `versioned-questionnaire-regeneration-pipeline` - Versioned Questionnaire Regeneration Pipeline

Each outline version generates new questionnaires, with explicit tracking of which previous answers to revise, retain, or retire.

*Description:* When upgrading from Version N to Version N+1 of an outline, the system sends all previous questionnaire answers alongside both outline versions to generate new questions and answers. It explicitly identifies which existing answers remain valid, which need revision, and which are no longer relevant. By Version 5, the accumulated corpus contains all current answers plus version-specific refinements.

*Confidence:* 90% | *Status:* draft

**Embodies principles:**
- `prn_process_as_data`
- `prn_logical_coherence`
- `prn_cascade_containment`
- `prn_lens_dependent_extraction`
- `prn_extraction_permanence_tiers`


### `eternal-ephemeral-extraction-dichotomy` - Eternal-Ephemeral Extraction Dichotomy

Corpus analysis separates fixed questions asked of all inputs from project-specific questions that evolve with outline versions.

*Description:* The system maintains two extraction dimensions: eternal (fixed questions about main argument, concepts, dialectical tensions—shared across projects and extracted once to persist indefinitely) and ephemeral (project- and outline-version-specific questions that regenerate as the outline evolves). When upgrading outline versions, the ephemeral questionnaire regenerates while eternal answers provide stable context.

*Confidence:* 93% | *Status:* draft

**Embodies principles:**
- `prn_fixed_foundation`
- `prn_lens_dependent_extraction`
- `prn_extraction_permanence_tiers`
- `prn_event_driven_refinement`


### `outline-version-dependent-corpus-interrogation` - Outline-Version-Dependent Corpus Interrogation

The same corpora produces different food for thought based on the current version of the logical and functional outline.

*Description:* As users refine their logical and functional outline from Version 1 to Version N, the system regenerates 'food for thought' by re-interrogating the same corpora with evolved questions. The outline acts as a lens that determines what becomes visible and extractable from source materials. Version 1 may surface certain cross-pollinations while Version 5 reveals entirely different propositions from identical inputs.

*Confidence:* 92% | *Status:* draft

**Embodies principles:**
- `prn_living_artifacts`
- `prn_abductive_logic`
- `prn_co_evolution`
- `prn_lens_dependent_extraction`
- `prn_extraction_permanence_tiers`


## Project: essay-flow

### `multi-level-operation-vocabulary` - Multi-Level Operation Vocabulary

Define distinct operation types for each architectural level, enabling advisors and users to articulate changes at the appropriate abstraction.


*Description:* Rather than having a single set of modification operations, define vocabularies appropriate to each level: content operations (split/merge/clone/reframe for throughlines), meta-operations (add/remove/redefine slot types). Advisory systems should be able to invoke operations from any level, and recommendations should specify which level they target. This makes the level distinction operationally meaningful rather than merely conceptual.


*Confidence:* 86% | *Status:* draft

**Embodies principles:**
- `prn_criteria_grounded_advisory`
- `prn_meta_structural_revisability`
- `prn_multi_level_advisory_scope`


### `invisible-foundation-pattern` - Invisible Foundation Pattern

Have expert knowledge shape user-facing outputs through derivation processes that remain invisible to users.


*Description:* Expert knowledge (best practices, domain conventions, quality criteria) operates as a derivation layer that shapes what users see without itself being surfaced. Users interact with derived structures—which are informed by expertise—rather than needing to understand or specify the underlying expert knowledge. The expertise is operationalized rather than communicated.


*Confidence:* 84% | *Status:* draft

**Embodies principles:**
- `prn_latent_expertise_derivation`
- `prn_genre_as_scaffold`
- `prn_benchmark_driven_best_practice`


### `genre-mediated-template-derivation` - Genre-Mediated Template Derivation

Use genre/domain best practices as an intermediary derivation layer between generic templates and situation-specific structures.


*Description:* Instead of applying universal templates directly or asking users to specify structure ad-hoc, introduce an intermediary derivation step: (1) identify the genre/domain, (2) retrieve or generate best practices for that genre, (3) map those best practices onto structural slots. This creates genre-appropriate starting structures without hardcoding genre-specific templates.


*Confidence:* 88% | *Status:* draft

**Embodies principles:**
- `prn_latent_expertise_derivation`
- `prn_benchmark_driven_best_practice`
- `prn_genre_as_scaffold`


### `two-level-architecture-pattern` - Two-Level Architecture Pattern

Separate content-filling operations from structure-defining operations as distinct architectural levels with independent modification capabilities.


*Description:* Rather than treating templates as fixed containers that content fills, design systems with explicit separation between "what fills slots" (content level) and "what slots exist" (meta level). Each level has its own operation vocabulary: content-level operations (split, merge, clone, reframe) and meta-level operations (add slot type, remove slot type, redefine slot semantics). Both levels should be modifiable during the same workflow.


*Confidence:* 90% | *Status:* draft

**Embodies principles:**
- `prn_abstraction_independence`
- `prn_schema_data_co_evolution`
- `prn_meta_structural_revisability`


### `llm-dual-role-question-answer-processing` - LLM Dual Role Question-Answer Processing

The same LLM generates the questions AND interprets accumulated answers to generate output.

*Description:* Rather than separating question generation from answer interpretation, use a single LLM  context that both generates contextually-appropriate questions and synthesizes the  accumulated answers into the final output. The LLM "knows what it asked" and therefore  can interpret answers with full awareness of what distinctions each question was designed  to surface. This creates tighter coupling between elicitation and interpretation.


*Confidence:* 82% | *Status:* draft

**Embodies principles:**
- `prn_dialogue_emergent_relevance`
- `prn_distinction_surfacing_through_choice`


### `continuation-vs-completion-binary-control` - Continuation vs Completion Binary Control

Offer users explicit "go deeper" vs "generate now" choice after each refinement cycle.

*Description:* After each question batch, present two clear options: "Next Questions" (continue refining,  go deeper into specification) and "Generate [Output]" (use accumulated answers to produce  output now). This makes refinement depth a user-controlled variable rather than a  system-determined constant. Users self-select their stopping point based on whether they  feel sufficiently specified.


*Confidence:* 88% | *Status:* implemented

**Embodies principles:**
- `prn_graceful_partial_completion_validity`
- `prn_user_controlled_refinement_depth`

**Code locations (1):**
- `/home/evgeny/projects/asc/web/templates/essay_flow/refactoring_dashboard.html:requestMoreQuestions` (lines 3138-3203)


### `answer-accumulating-question-batches` - Answer-Accumulating Question Batches

Question batches where each batch incorporates all accumulated answers from prior batches.

*Description:* Generate questions in small batches (3-4) rather than all at once. After each batch, the LLM  receives the full context of all prior answers and uses this to generate more refined,  targeted questions. This creates a narrowing funnel where early questions establish broad  parameters and later questions refine specific details. The accumulated answer context  enables increasingly precise questioning.


*Confidence:* 92% | *Status:* implemented

**Embodies principles:**
- `prn_inter_stage_criterion_propagation`
- `prn_staged_adaptive_interrogation`

**Code locations (1):**
- `/home/evgeny/projects/asc/web/routes/essay_flow_v3.py:generate_reframe_questions` (lines 13887-14025)


### `input-modality-election-modal` - Input Modality Election Modal

A modal offering users explicit choice between free-form expression and structured guided input.

*Description:* Present users with a binary choice at the start of complex intent-gathering: "I'll describe it"  routes to a text input field for direct expression, while "Guide me through it" initiates a  structured questioning flow. This acknowledges that users arrive with different degrees of  intent formation and routes them to appropriately matched interaction modes.


*Confidence:* 90% | *Status:* implemented

**Embodies principles:**
- `prn_multimodal_cognitive_scaffolding`
- `prn_intent_formation_state_bifurcation`

**Code locations (1):**
- `/home/evgeny/projects/asc/web/templates/essay_flow/refactoring_dashboard.html:initiateReframe` (lines 2910-2937)


### `semantic-territory-shift-detection` - Semantic Territory Shift Detection

Ask LLMs to assess whether conceptual boundaries have shifted in ways that affect elements not directly modified.


*Description:* After structural changes, prompt an LLM to reason about "semantic territory"—the conceptual space each remaining element occupies. Has a merge changed what a surviving element means by altering its contrasts? Has a split created overlap where distinctiveness existed? Has a retirement left orphaned content that should migrate? This framing enables the LLM to assess indirect semantic effects that algorithmic approaches miss.


*Confidence:* 80% | *Status:* draft

**Embodies principles:**
- `prn_sibling_context_for_distinctiveness`
- `prn_holistic_semantic_judgment`


### `transformation-state-context-bundle` - Transformation-State Context Bundle

Package transformation history (what changed and how) alongside current state when requesting impact assessment from an LLM.


*Description:* When structural changes occur (merges, splits, creations, retirements), construct a context bundle containing: (1) transformation events with their types, (2) the prior state of affected elements, (3) the current state of remaining elements, and (4) the relationships between transformed and remaining elements. This bundle enables the LLM to reason about whether transformations have affected the semantic territory of elements that weren't directly changed.


*Confidence:* 85% | *Status:* draft

**Embodies principles:**
- `prn_transformation_context_for_impact_assessment`
- `prn_contrastive_context_enrichment`
- `prn_change_impact_propagation`


### `algorithmic-proxy-recognition-heuristic` - Algorithmic Proxy Recognition Heuristic

Recognize numeric weights, thresholds, and scoring formulas for semantic tasks as signals that the design should be refactored toward LLM judgment.


*Description:* When reviewing system designs, flag any component that uses numeric weights, base_weights, thresholds, or scoring formulas to assess semantic properties (coherence, staleness, relevance, adequacy). These are "algorithmic proxies" that approximate what LLMs can assess directly. Refactor by identifying what context the algorithm was trying to encode numerically, then provide that context to an LLM in natural language.


*Confidence:* 85% | *Status:* draft

**Embodies principles:**
- `prn_holistic_semantic_judgment`
- `prn_semantic_over_algorithmic_for_meaning`


### `full-context-semantic-assessment-pattern` - Full-Context Semantic Assessment Pattern

Present complete situational context to an LLM for holistic semantic judgment rather than calculating scores through algorithmic decomposition.


*Description:* When a system needs to assess semantic relationships, replace weight-based calculation with context-rich LLM prompting. Package all relevant information—what changed, what remains, how elements relate, what categories of transformation occurred—into a single context window. Ask the LLM to reason about semantic impact rather than computing it. This pattern trades algorithmic determinism for semantic sensitivity.


*Confidence:* 90% | *Status:* implemented

**Embodies principles:**
- `prn_semantic_over_algorithmic_for_meaning`
- `prn_contextual_extraction_superiority`

**Code locations (1):**
- `/home/evgeny/projects/asc/web/services/staleness_service.py:build_staleness_assessment_prompt` (lines 158-285)


### `dynamic-coherence-as-system-property` - Dynamic Coherence as System Property

Treat structural coherence as an emergent, continuously-maintained property rather than a static state achieved at design time.

*Description:* Design the system architecture around the assumption that coherence between structural layers is inherently unstable and requires ongoing maintenance. This means building in: (1) continuous monitoring for coherence violations, (2) proposal generation for coherence restoration, (3) user approval gates before coherence changes execute, and (4) version tracking to understand coherence evolution over time. The phrase "we want everything to be dynamic" encodes this stance.


*Confidence:* 82% | *Status:* draft

**Embodies principles:**
- `prn_multi_layer_synchronization_obligation`
- `prn_automated_staleness_detection`
- `prn_change_impact_propagation`


### `sign-off-vs-articulation-interface-bifurcation` - Sign-Off vs Articulation Interface Bifurcation

Design distinct interface modes for reactive approval (minimal user input) versus proactive reframing (guided articulation required).

*Description:* Create two interface pathways for the same underlying operation (e.g., throughline reframing). The approval pathway presents pre-computed proposals with accept/reject/modify affordances, optimized for quick evaluation. The articulation pathway provides scaffolding for users to state their interpretive reason for change before the system can propose solutions. The cognitive load, information display, and interaction patterns differ substantially between modes.


*Confidence:* 84% | *Status:* draft

**Embodies principles:**
- `prn_human_authority_gate`
- `prn_cognitive_task_matched_presentation`
- `prn_approval_initiation_agency_bifurcation`


### `staleness-detection-monitor-pattern` - Staleness Detection Monitor Pattern

Background process that tracks interdependency relationships and surfaces alerts when upstream changes create downstream inconsistency.

*Description:* Implement a monitoring layer that maintains a dependency graph between structural elements (e.g., outline → throughlines). When any element undergoes significant modification, the monitor traverses dependencies to identify potentially stale downstream elements, generates staleness alerts with specific change context, and queues these for user attention. The key is separating detection (automated) from remediation (human-gated).


*Confidence:* 90% | *Status:* draft

**Embodies principles:**
- `prn_change_impact_propagation`
- `prn_event_driven_refinement`
- `prn_automated_staleness_detection`


### `context-interpretation-trigger-router` - Context-Interpretation Trigger Router

Route system changes through different pathways based on whether they originate from structural context changes or user interpretation changes.

*Description:* Implement a classification layer that identifies the source of any change request: structural/contextual triggers (outline modified, sections merged) route to an automated proposal pathway requiring only sign-off, while interpretive triggers (user decides meaning has shifted) route to a guided articulation pathway that elicits the user's reframing rationale. Each pathway has distinct interface affordances and information requirements.


*Confidence:* 87% | *Status:* draft

**Embodies principles:**
- `prn_content_based_routing`
- `prn_dual_mode_operation`
- `prn_trigger_source_typology`


### `edit-impact-tracking` - Edit Impact Tracking

Shows ripple effects when editing a slot, displaying affected throughlines, strategic items, and rhetorical sections.

*Description:* When a user edits a functional slot, displays a cascade impact preview showing: affected throughlines that span this slot, linked strategic items, rhetorical sections that draw from this slot. Offers options to update all downstream references, park affected items for manual review, or proceed without cascade. Prevents unintended inconsistencies from isolated edits.

*Confidence:* 85% | *Status:* draft

**Embodies principles:**
- `prn_logical_coherence`
- `prn_cascade_containment`
- `prn_controlled_propagation`

**Code locations (3):**
- `/home/evgeny/projects/asc/web/templates/essay_flow/main.html:editSlot` (lines 3064-3137)
- `/home/evgeny/projects/asc/web/routes/essay_flow.py:get_edit_impact` (lines 3046-3057)
- `/home/evgeny/projects/asc/gcis/db.py:get_slot_edit_impact` (lines 12181-12268)


### `reasoning-chain-display` - Reasoning Chain Display

Shows the analytical reasoning that led to each suggested option, not just the options themselves.

*Description:* When presenting thesis options or slot suggestions, displays HOW each emerged from the user's material. Shows which passages supported the inference, what analytical moves were made (synthesis of contradictions, contrarian reframing, etc.), and confidence levels with justification. Users understand the analytical work that produced options rather than receiving them as unexplained alternatives.

*Confidence:* 85% | *Status:* draft

**Embodies principles:**
- `prn_emergent_choice`
- `prn_formalization_as_education`

**Code locations (1):**
- `/home/evgeny/projects/asc/web/templates/essay_flow/main.html:thesis-options-rendering` (lines 3995-4012)


### `critical-question-prioritization` - Critical Question Prioritization

Dynamically reorders questionnaire questions to front-load the most consequential ones based on genre.

*Description:* The entry questionnaire reorders itself based on what's most consequential for the selected genre. For Book Review, thesis and phenomenon come first. For Political Analysis, diagnosis might lead. Questions are marked with priority indicators (★) and users see an explanation of why certain questions come first ("Questions 1-2 determine all downstream answers"). Ensures path-dependent decisions are made early.

*Confidence:* 85% | *Status:* draft

**Embodies principles:**
- `prn_front_load_decisions`
- `prn_genre_as_scaffold`

**Code locations (3):**
- `/home/evgeny/projects/asc/migrations/058_critical_question_prioritization.sql:migration-058` (lines 1-61)
- `/home/evgeny/projects/asc/web/templates/essay_flow/main.html:renderCurrentQuestion` (lines 3750-3765)
- `/home/evgeny/projects/asc/gcis/db.py:get_entry_questionnaire_questions` (lines 11688-11701)


### `slot-saturation-detection` - Slot Saturation Detection

Tracks material density per functional slot and suggests when users have enough content to move to the next phase.

*Description:* Adds a "Coverage Meter" that monitors how much material has been collected for each functional slot. Shows saturation percentages, flags underdeveloped slots, and actively suggests when the user should stop collecting and start structuring. Provides contextual guidance like "You have strong diagnostic material but weak implications - consider adding consequences before moving to rhetorical sequencing."

*Confidence:* 90% | *Status:* draft

**Embodies principles:**
- `prn_gap_aware_processing`
- `prn_adaptive_termination`

**Code locations (1):**
- `/home/evgeny/projects/asc/web/templates/essay_flow/main.html:saturation-summary-panel` (lines 907-942)


### `translation-map-display` - Translation Map Display

Shows users how their raw notes mapped to functional slots during analysis, making structural translation visible and educational.

*Description:* When Notes Import analyzes user text, displays a "Translation Map" panel showing the mapping between original text passages and the functional slots they were assigned to, along with confidence scores. Users see exactly WHY their notes became specific slots (PHENOMENON, DIAGNOSIS, etc.), learning the essay structure through use. This transforms the analysis from a black box into a teaching moment.

*Confidence:* 90% | *Status:* draft

**Embodies principles:**
- `prn_formalization_as_education`
- `prn_tacit_to_explicit`

**Code locations (3):**
- `/home/evgeny/projects/asc/web/templates/essay_flow/main.html:toggleTranslationMap` (lines 4202-4212)
- `/home/evgeny/projects/asc/web/templates/essay_flow/main.html:renderNotesResults` (lines 3951-3981)
- `/home/evgeny/projects/asc/web/routes/essay_flow.py:analyze_notes` (lines 2592-2628)


## Project: prompt-extraction

### `non-predetermined-stage-sequencing` - Non-Predetermined Stage Sequencing

Generate later elicitation stages only after processing earlier responses, preventing the predetermined feel of pre-scripted interrogation.

*Description:* Generate later elicitation stages only after processing earlier responses, preventing the predetermined feel of pre-scripted interrogation.

Rather than presenting a fixed question sequence, the system generates stage 2 questions only after stage 1 is answered, allowing the inquiry trajectory to genuinely respond to user input. This maintains the feeling that the process is exploring rather than administering a survey, supporting authentic knowledge extraction.

**When to use:** When extracting complex or partially-formed user knowledge; when premature question exposure would anchor or constrain responses; when the value lies in probing rather than surveying.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_provisional_articulation_as_catalyst` - supports
- `prn_dynamic_elicitation_injection` - extends
- `prn_staged_adaptive_interrogation` - embodies


### `cognitive-task-to-scaffolding-modality-matching` - Cognitive Task to Scaffolding Modality Matching

Deploy questions, visualizations, path-diagrams, and interfaces as distinct tools matched to specific cognitive support needs.

*Description:* Deploy questions, visualizations, path-diagrams, and interfaces as distinct tools matched to specific cognitive support needs.

Different cognitive operations—imagining possibilities, tracing implications, articulating beliefs—require different external supports. The system treats questions as one modality among many, selecting or combining visualizations, interactive interfaces, and path diagrams based on what the cognitive task actually requires rather than defaulting to verbal interrogation.

**When to use:** When verbal questions hit diminishing returns; when users need to 'see' rather than 'answer'; when the cognitive task is spatial (path exploration) rather than propositional (assertion).

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_externalized_imagination_infrastructure` - embodies
- `prn_cognitive_task_matched_presentation` - specializes
- `prn_multimodal_cognitive_scaffolding` - embodies


### `choice-impact-topology-rendering` - Choice-Impact Topology Rendering

Visualize the network of downstream implications when a conceptual choice is made one way versus another.

*Description:* Visualize the network of downstream implications when a conceptual choice is made one way versus another.

When users face definitional or conceptual decisions, the system renders visible the propagation topology—showing how defining concept X one way affects arguments Y and Z, versus defining it differently. This makes conceptual interdependencies navigable rather than requiring users to hold complex implication chains mentally.

**When to use:** When conceptual definitions have cascading effects on argument structure; when users need to understand trade-offs between formulation choices; when the 'cost' of a decision is its downstream constraints.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_externalized_imagination_infrastructure` - embodies
- `prn_possibility_as_foreclosure_warning` - extends
- `prn_option_impact_preview` - specializes
- `prn_impact_topology_materialization` - embodies


### `provisional-formulation-as-knowledge-probe` - Provisional Formulation as Knowledge Probe

Output tentative conclusions and articulations mid-process to catalyze user's ability to express tacit knowledge.

*Description:* Output tentative conclusions and articulations mid-process to catalyze user's ability to express tacit knowledge.

Rather than only asking questions, the system generates provisional answers, formulations, or conclusions at intermediate stages. These imperfect articulations serve as stimuli that help users recognize and correct toward what they actually think—extracting knowledge they 'may know but may not have yet articulated.'

**When to use:** When users possess relevant knowledge but struggle to articulate it directly; when questions alone fail to surface tacit understanding; when seeing a 'wrong' answer helps clarify the 'right' one.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_externalized_imagination_infrastructure` - embodies
- `prn_embodied_decision_substrate` - extends
- `prn_provisional_articulation_as_catalyst` - embodies


### `type-generic-element-processing` - Type-Generic Element Processing

Processing mechanisms operate on categories of structural elements rather than hardcoded specific element types, enabling automatic coverage of future additions.

*Description:* Processing mechanisms operate on categories of structural elements rather than hardcoded specific element types, enabling automatic coverage of future additions.

Rather than building separate refinement logic for 'concepts', 'dialectics', and 'propositions' individually, the system treats these as instances of 'theoretical structural elements' and processes them polymorphically. When new element types are added to the theory package, they automatically receive appropriate refinement processing without code changes.

**When to use:** When designing systems that must handle evolving schemas where new structural element types may be introduced over time.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_extensibility_as_design_criterion` - embodies
- `prn_type_polymorphic_processing` - embodies


### `precision-forcing-refinement-questions` - Precision-Forcing Refinement Questions

Refinement stages include questions specifically designed to force users or LLMs toward greater precision on vague theoretical elements.

*Description:* Refinement stages include questions specifically designed to force users or LLMs toward greater precision on vague theoretical elements.

Questions in the refinement phase are crafted to target imprecision as a specific property, demanding more exact specification of concepts and dialectics. This treats vagueness not as an inevitable state but as something that targeted questioning can systematically address and reduce.

**When to use:** When theoretical elements like concepts or dialectics have been generated but remain underdetermined and need sharpening before downstream use.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_precision_forcing_interrogation` - embodies
- `prn_staged_adaptive_interrogation` - supports


### `schema-introspective-question-generation` - Schema-Introspective Question Generation

Refinement questions are generated by introspecting what structural element types currently exist in the theory package rather than using a fixed question set.

*Description:* Refinement questions are generated by introspecting what structural element types currently exist in the theory package rather than using a fixed question set.

The refinement stage examines the current schema to discover what theoretical elements are present (propositions, concepts, dialectics, etc.) and generates appropriate refinement questions for each element type. This allows the questioning to adapt automatically when new structural elements are added to the theory package.

**When to use:** When building refinement or interrogation stages that need to remain valid as the underlying data schema evolves with new element types.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_extensibility_as_design_criterion` - supports
- `prn_schema_reflexive_generation` - embodies


### `explicit-criterion-threading-between-llm-calls` - Explicit Criterion Threading Between LLM Calls

Pass variables, criteria, and constraints as explicit structured data between collaborating LLM invocations.

*Description:* Pass variables, criteria, and constraints as explicit structured data between collaborating LLM invocations.

When multiple LLMs work across a multi-stage process, make the handoff of governing criteria explicit rather than implicit. Each stage should receive and can query the current process plan, relevant constraints, and evaluation criteria as structured data. This enables both asking the right questions and knowing when/how to propose restructuring.

**When to use:** Apply whenever orchestrating multiple LLM calls that need to maintain coherence with each other and with an evolving process plan, especially in agentic or pipeline architectures.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_inter_stage_criterion_propagation` - embodies
- `prn_contrastive_context_enrichment` - supports
- `prn_process_parameterized_questioning` - enables


### `result-triggered-process-restructuring` - Result-Triggered Process Restructuring

Enable LLMs to propose modifications to the workflow structure based on accumulated results.

*Description:* Enable LLMs to propose modifications to the workflow structure based on accumulated results.

As processing proceeds and results accumulate, LLMs should be able to propose adjustments to the workflow itself—not just the content. This creates a feedback loop where content outcomes inform process evolution, making the system dynamically adaptive rather than following a fixed plan regardless of what emerges.

**When to use:** Apply in extended multi-stage workflows where early results may reveal that the planned process is suboptimal, and where the cost of continuing a misaligned process exceeds the cost of restructuring.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_bidirectional_process_content_evolution` - embodies
- `prn_human_authority_gate` - constrains
- `prn_runtime_strategy_adaptation` - embodies


### `collaborative-process-design-with-versioning` - Collaborative Process Design with Versioning

Introduce an early stage where LLMs propose a workflow, users adjust it, and version changes are tracked.

*Description:* Introduce an early stage where LLMs propose a workflow, users adjust it, and version changes are tracked.

Add an explicit process-design phase where, after initial questions, an LLM generates a proposed workflow/flow structure. Users can modify this proposal, and all versions of the process design are tracked. This makes the workflow itself a first-class artifact that both parties shape rather than a hidden system constraint.

**When to use:** Apply when building multi-stage systems where users should have agency over process structure, particularly when different users may need different workflow configurations.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_refinement_versioning` - applies
- `prn_early_consequential_decisions` - enables
- `prn_explicit_process_externalization` - embodies


### `stage-contingent-question-calibration` - Stage-Contingent Question Calibration

Adjust question types based on which processing stages exist or have been removed from the workflow.

*Description:* Adjust question types based on which processing stages exist or have been removed from the workflow.

When formulating questions at any stage, explicitly check the current process plan to determine question granularity. If downstream stages exist for gathering specific evidence, ask for typologies and patterns; if those stages have been removed, ask for specific examples directly. This prevents asking the wrong type of question for the available process structure.

**When to use:** Apply when designing question-generation prompts for any stage that feeds into optional or configurable downstream stages, especially refinement or elicitation phases.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_process_parameterized_questioning` - embodies
- `prn_downstream_aware_generation` - enables
- `prn_stage_appropriate_question_types` - specializes


### `preemptive-output-structure-anticipation` - Preemptive Output Structure Anticipation

Work backward from anticipated final output structures to identify what information must be elicited, treating output requirements as constraints on input gathering.

*Description:* Work backward from anticipated final output structures to identify what information must be elicited, treating output requirements as constraints on input gathering.

The system explicitly reasons about what throughlines might exist and what weight distributions they would require, using this anticipation to identify gaps in current knowledge. This transforms the elicitation process from forward-flowing data gathering into bidirectional reasoning where anticipated outputs constrain and guide the questions asked.

**When to use:** Use when final outputs have structural requirements (like weighted throughlines) that depend on information not naturally surfaced by standard elicitation, requiring deliberate backward reasoning from output needs to input requirements.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_anticipatory_model_instantiation` - embodies
- `prn_downstream_aware_generation` - implements


### `continuous-background-weight-refinement` - Continuous Background Weight Refinement

Maintain and progressively refine weight hypotheses throughout all user interactions rather than computing weights only at a designated stage.

*Description:* Maintain and progressively refine weight hypotheses throughout all user interactions rather than computing weights only at a designated stage.

Instead of treating weight determination as a discrete phase that occurs after data collection, the system runs weight inference as a continuous background process. Each new user answer updates the provisional weight distribution, with the model becoming progressively more accurate and revealing which aspects remain underdetermined.

**When to use:** Apply in workflows where multiple independent dimensions must be weighted relative to each other and where user responses provide indirect evidence about relative importance across the entire interaction.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_continuous_background_synthesis` - embodies
- `prn_iterative_theory_data_dialectic` - extends
- `prn_continuous_strategic_reasoning` - Created by refactoring engine


### `weight-gap-targeted-question-insertion` - Weight-Gap Targeted Question Insertion

Strategically inject questions into the elicitation flow specifically designed to resolve weight distribution ambiguities revealed by anticipatory models.

*Description:* Strategically inject questions into the elicitation flow specifically designed to resolve weight distribution ambiguities revealed by anticipatory models.

When the provisional throughline model reveals that weight distribution cannot be determined from existing data, the system inserts targeted questions at opportune moments rather than following a fixed question sequence. These questions are designed specifically to disambiguate weight assignments before formal weight generation occurs.

**When to use:** Use when anticipated outputs require parametric decisions (like weights, priorities, or distributions) that cannot be reliably inferred from standard elicitation questions alone.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_dynamic_elicitation_injection` - embodies
- `prn_proactive_insufficiency_signaling` - implements


### `first-input-throughline-projection` - First-Input Throughline Projection

Instruct LLMs to begin constructing provisional models of final outputs immediately upon receiving the first user input.

*Description:* Instruct LLMs to begin constructing provisional models of final outputs immediately upon receiving the first user input.

Rather than waiting until all user data is collected, the system prompts the LLM to start anticipating what throughlines might emerge from the very first answer. This creates an evolving hypothesis about final structures that gets refined with each subsequent input, transforming passive data collection into active model-building.

**When to use:** Apply when designing multi-step elicitation flows where the final output structure depends on synthesizing information across all steps, and where early anticipation can reveal what additional information is needed.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_forward_staged_data_harvesting` - extends
- `prn_anticipatory_model_instantiation` - embodies


### `correction-then-commit-gating` - Correction-Then-Commit Gating

Parse verification suggestions into corrections, apply them to outputs, and only then execute consequential operations.

*Description:* Parse verification suggestions into corrections, apply them to outputs, and only then execute consequential operations.

The verification layer produces correction suggestions rather than direct fixes. These suggestions are parsed, applied to modify the original outputs, and the corrected version is what gets committed to downstream processes. This creates a gate where no refactoring or permanent changes occur until validation passes.

**When to use:** When outputs drive automated refactoring, code changes, or other irreversible operations where pre-commitment correction is cheaper than post-commitment rollback.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_cybernetic_feedback` - embodies
- `prn_human_authority_gate` - supports
- `prn_correction_before_commitment` - embodies


### `input-grounded-field-comparison` - Input-Grounded Field Comparison

Structure verification prompts to explicitly compare output fields against original input fields as ground truth.

*Description:* Structure verification prompts to explicitly compare output fields against original input fields as ground truth.

Frame the verification task as checking whether each output field correctly derives from or matches corresponding input data. The verifier receives both inputs and outputs, with instructions to identify any fields that don't properly reflect the source inputs. This anchors validation in concrete comparison rather than abstract quality assessment.

**When to use:** When outputs contain structured fields that should faithfully represent input data, and hallucination risk manifests as field-level fabrication or distortion.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_provenance_preservation` - supports
- `prn_verification_easier_than_generation` - supports
- `prn_input_anchored_validation` - embodies


### `cross-model-economic-verification` - Cross-Model Economic Verification

Assign verification tasks to cheaper/faster models than the primary generation model.

*Description:* Assign verification tasks to cheaper/faster models than the primary generation model.

Use an economical model (e.g., Haiku 4.5) to verify outputs from a more capable but expensive model (e.g., Sonnet). Verification is a constrained comparison task that doesn't require the full reasoning capacity of premium models, making this economically efficient without sacrificing quality.

**When to use:** When pipeline includes multiple LLM stages and cost optimization matters, particularly for verification stages that can tolerate reduced capability.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_resource_proportionality` - embodies
- `prn_economic_model_tiering` - embodies
- `prn_cognitive_division_of_labor` - supports


### `secondary-llm-verification-layer` - Secondary LLM Verification Layer

Interpose a dedicated LLM pass specifically for validating outputs before they trigger downstream actions.

*Description:* Interpose a dedicated LLM pass specifically for validating outputs before they trigger downstream actions.

After primary generation, route outputs through a second LLM instance tasked solely with verification rather than generation. This verification layer compares outputs against inputs to identify mismatches, hallucinations, or drift. The separated concerns allow verification-optimized prompting distinct from generation-optimized prompting.

**When to use:** When LLM outputs will trigger consequential changes (refactoring, database updates, API calls) where hallucinations would cause harm that's expensive to reverse.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_phase_separated_processing` - embodies
- `prn_verification_easier_than_generation` - embodies
- `prn_correction_before_commitment` - embodies


### `dynamic-strategic-course-correction` - Dynamic Strategic Course-Correction

LLMs should continuously re-strategize based on accumulated user answers and contextual pointers.

*Description:* LLMs should continuously re-strategize based on accumulated user answers and contextual pointers.

Rather than executing predetermined pipelines, the system should 'strategize on the fly and course-correct based on user answers, pointers to more contextual docs.' Each new input triggers re-evaluation of approach, making strategy an ongoing activity interleaved with execution.

**When to use:** When user engagement reveals information that should reshape the overall approach, not just immediate outputs

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_continuous_strategic_reasoning` - embodies
- `prn_cybernetic_feedback` - supports
- `prn_runtime_pipeline_orchestration` - supports


### `maximum-resource-allocation-for-strategic-reasonin` - Maximum Resource Allocation for Strategic Reasoning

Explicitly allocate highest available computational resources when tasks require strategic adaptation.

*Description:* Explicitly allocate highest available computational resources when tasks require strategic adaptation.

When strategic reasoning, course-correction, and on-the-fly adaptation are required, configure LLMs with maximum token limits and reasoning modes rather than economizing. The instruction 'shouldn't spare any resources' treats reasoning quality as the paramount concern over efficiency.

**When to use:** When tasks require dynamic strategy formulation rather than routine processing, especially when user context is evolving

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_reasoning_resource_maximization` - embodies
- `prn_resource_proportionality` - supports


### `dual-channel-progressive-specialization` - Dual-Channel Progressive Specialization

Configure systems through both pre-loaded contextual documents and emergent user dialogue responses.

*Description:* Configure systems through both pre-loaded contextual documents and emergent user dialogue responses.

Customization depth increases through two complementary channels: a contextual docs folder provides initial domain grounding, while user responses during conversation add deeper, more specific configuration. The combination produces specialization neither channel could achieve alone.

**When to use:** When building adaptive systems that need both baseline domain knowledge and real-time personalization

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_context_as_configuration` - embodies
- `prn_staged_adaptive_interrogation` - supports
- `prn_dialogue_emergent_relevance` - embodies


### `domain-agnostic-initial-architecture` - Domain-Agnostic Initial Architecture

Design systems to start without domain commitment, becoming specialized only through runtime inputs.

*Description:* Design systems to start without domain commitment, becoming specialized only through runtime inputs.

The framework begins as a generic structure not configured for any specific use case (foundation, VC, essay writing). Domain specificity emerges entirely from contextual documents and user interactions rather than initial design choices. This enables the same core architecture to serve radically different purposes.

**When to use:** When building systems that must serve multiple domains or when the specific domain won't be known until runtime

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_context_as_configuration` - embodies
- `prn_domain_transcendent_abstraction` - embodies


### `just-in-time-profile-construction` - Just-In-Time Profile Construction

Build structured entity profiles (e.g., philanthropy profiles) only after sufficient conversational context exists to determine useful structure.

*Description:* Build structured entity profiles (e.g., philanthropy profiles) only after sufficient conversational context exists to determine useful structure.

Defer the construction of structured profiles from document collections until dialogue has established what aspects matter for downstream tool functions. This ensures profiles are built in a way that serves actual use rather than speculative completeness, with structure emerging from demonstrated need rather than anticipated need.

**When to use:** When creating entity profiles that must serve varied downstream functions, and optimal profile structure depends on how the profile will be used.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_function_based_on_demand_retri` - supports
- `prn_staging_processing_separation` - embodies
- `prn_dialogue_emergent_relevance` - supports


### `conversation-guided-extraction-targeting` - Conversation-Guided Extraction Targeting

Use the dynamics of user-LLM dialogue to discover what aspects of staged documents are actually relevant to extract.

*Description:* Use the dynamics of user-LLM dialogue to discover what aspects of staged documents are actually relevant to extract.

Rather than pre-determining extraction schemas, allow the evolving conversation between user and LLM to generate extraction criteria. The dialogue itself becomes a discovery mechanism that reveals what the user actually needs from the document collection, making extraction more targeted and valuable.

**When to use:** When document collections are large and varied, and relevance cannot be determined without understanding user intent through interaction.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_contextual_extraction_superiority` - embodies
- `prn_dialogue_emergent_relevance` - embodies
- `prn_dialectical_refinement` - supports


### `document-collection-staging-without-processing` - Document Collection Staging Without Processing

Register document folders with the system for availability without triggering immediate extraction or structuring.

*Description:* Register document folders with the system for availability without triggering immediate extraction or structuring.

Point the tool to folders containing relevant documents (e.g., philanthropy materials) to make them accessible for later use, but do not perform upfront extraction or transformation. This separates resource availability from resource processing, allowing documents to be staged early while extraction criteria are determined later through use.

**When to use:** When building tools that need access to external document collections but where relevance criteria are not yet clear at setup time.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_staging_processing_separation` - embodies
- `prn_contextual_extraction_superiority` - embodies


### `domain-portable-process-architecture` - Domain-Portable Process Architecture

Abstracting process structures so the same operational modules serve journalism, academia, policy work, and other domains through parameterization rather than separate implementations.

*Description:* Abstracting process structures so the same operational modules serve journalism, academia, policy work, and other domains through parameterization rather than separate implementations.

The core processing modules (generating through-lines, strategic items, semantic clustering) are designed domain-agnostically, with domain-specific behavior emerging from the input materials and configured parameters rather than hard-coded domain logic. This requires identifying the truly universal operations across domains and making domain-specific aspects configurable rather than structural.

**When to use:** When building tools intended to serve multiple institutional contexts (newsrooms, foundations, academic institutions) and when the underlying cognitive operations are similar despite surface differences in outputs.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_domain_transcendent_abstraction` - embodies
- `prn_context_as_configuration` - Created by refactoring engine
- `prn_generative_personalization` - relates_to
- `prn_context_specific_adaptation` - supports


### `arbitrary-point-content-injection` - Arbitrary-Point Content Injection

Enabling contextual inputs like articles, reports, or additional data to be inserted at any point in the workflow rather than only at designated input stages.

*Description:* Enabling contextual inputs like articles, reports, or additional data to be inserted at any point in the workflow rather than only at designated input stages.

The system supports inserting enrichment materials (news articles, policy reports, academic papers, grantee reports) before, during, or after core processing stages. This allows context to enhance processing at the moment it becomes most relevant—whether for initial framing, mid-process semantic clustering, or late-stage validation. Input architecture is designed for permeability rather than gatekeeping.

**When to use:** When the relevance of supplementary materials depends on what has been generated so far, and when users may discover useful context mid-process that should inform subsequent operations.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_arbitrary_insertion_architecture` - embodies
- `prn_forward_staged_data_harvesting` - relates_to


### `task-driven-pipeline-composition` - Task-Driven Pipeline Composition

Assembling the sequence and quantity of processing stages dynamically based on task requirements and emerging results rather than fixed templates.

*Description:* Assembling the sequence and quantity of processing stages dynamically based on task requirements and emerging results rather than fixed templates.

Rather than prescribing a fixed flow, the system determines which operations to run and in what order based on the specific task, user inputs, and intermediate results. This includes responding to user interaction during processing and adjusting the remaining pipeline accordingly. The distinction shifts from predetermined outcome to predetermined operational repertoire.

**When to use:** When different tasks require fundamentally different processing patterns even within the same domain, and when user feedback during processing should influence subsequent steps.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_event_driven_refinement` - relates_to
- `prn_cybernetic_feedback` - supports
- `prn_runtime_pipeline_orchestration` - embodies


### `position-agnostic-module-definition` - Position-Agnostic Module Definition

Designing operational modules that function identically regardless of where they appear in a processing sequence.

*Description:* Designing operational modules that function identically regardless of where they appear in a processing sequence.

Modules are built to be self-contained units that can be invoked early (before generating through-lines), late (after strategy elucidation), or multiple times throughout a workflow. Each module operates on current state without assumptions about prior steps, enabling arbitrary sequencing. This requires explicit input/output contracts rather than implicit positional dependencies.

**When to use:** When building flexible workflows where the optimal order of operations varies by task, user preference, or emerging results, and where the same operation may need to run multiple times at different stages.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_composable_process_primitives` - embodies
- `prn_staged_processing` - extends


### `friction-prioritized-attention-allocation` - Friction-Prioritized Attention Allocation

Direct the core user action toward items causing structural conflict, treating harmonious integrations as resolved background operations.

*Description:* Direct the core user action toward items causing structural conflict, treating harmonious integrations as resolved background operations.

Explicitly design the interaction flow so that friction-causing evidence commands primary attention and cognitive effort. Seamlessly integrated items are acknowledged but don't compete for attention. This inverts the common pattern of reviewing everything equally by making conflict the attention attractor.

**When to use:** When processing mixed content streams where some items require human judgment and others don't; when trying to optimize human cognitive allocation across heterogeneous processing needs.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_cognitive_division_of_labor` - implements
- `prn_resource_proportionality` - supports
- `prn_friction_focused_attention_allocation` - embodies


### `granular-post-hoc-override-controls` - Granular Post-Hoc Override Controls

Present auto-integrated items with check/uncheck toggles enabling selective acceptance or rejection after automatic action.

*Description:* Present auto-integrated items with check/uncheck toggles enabling selective acceptance or rejection after automatic action.

Rather than blocking on pre-approval or acting without recourse, provide interface controls that let users review and selectively override automatic decisions. Each integrated item becomes checkable/uncheckable, converting binary approve-all or reject-all into granular item-level control exercised after integration.

**When to use:** When automatic actions need human oversight but shouldn't require exhaustive pre-approval; when users need efficient ways to correct edge cases without reviewing every item.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_human_authority_gate` - implements
- `prn_visual_state_legibility` - supports
- `prn_act_notify_override_pattern` - embodies


### `silent-integration-with-disclosure` - Silent Integration with Disclosure

Automatically integrate naturally-fitting evidence while proactively informing users what was done and offering preview.

*Description:* Automatically integrate naturally-fitting evidence while proactively informing users what was done and offering preview.

For evidence that passes structural fit assessment without conflict, proceed with integration without blocking for approval. Simultaneously notify users of what was integrated and provide preview capability so they understand system actions. This treats non-conflicting integration as the default while maintaining transparency.

**When to use:** When handling high-confidence, low-risk content additions where requiring pre-approval would create unnecessary friction without adding value.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_cognitive_division_of_labor` - implements
- `prn_dual_mode_operation` - supports
- `prn_act_notify_override_pattern` - embodies


### `fit-based-evidence-bifurcation` - Fit-Based Evidence Bifurcation

Route evidence to different processing pathways based on whether it harmonizes with or conflicts against existing structural slots.

*Description:* Route evidence to different processing pathways based on whether it harmonizes with or conflicts against existing structural slots.

Before attempting integration, assess each piece of evidence against target slots in the functional skeleton to determine structural compatibility. Evidence that naturally fits proceeds to automatic integration, while evidence causing friction routes to human-attention workflows. This assessment becomes the primary routing decision point.

**When to use:** When integrating heterogeneous content into structured frameworks where some items will fit naturally and others will require reconciliation or modification.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_conflict_triage` - embodies
- `prn_content_based_routing` - implements
- `prn_structural_fit_assessment_phase` - embodies


### `sub-option-dependent-revision-branching` - Sub-Option Dependent Revision Branching

Map revision requirements that vary based on which sub-options users select within each major interpretive choice.

*Description:* Map revision requirements that vary based on which sub-options users select within each major interpretive choice.

Beyond showing impacts of top-level choices, pre-generate how different sub-options for integrating each reading create different revision patterns. This reveals the decision space as a branching tree where sub-choices within each interpretation have their own distinct cascading effects.

**When to use:** When interpretive choices have nested sub-options and users need to understand how combinations of choices interact to determine final revision requirements

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_possibility_space_architecture` - embodies
- `prn_interpretive_cascade_instantiation` - extends


### `decision-support-container-matching` - Decision Support Container Matching

Select interface affordances (modals, sidebars, collapsibles) that match the cognitive requirements of the decision task.

*Description:* Select interface affordances (modals, sidebars, collapsibles) that match the cognitive requirements of the decision task.

Pre-generated decision support content should be presented through interface patterns chosen specifically for the cognitive task at hand. Comparison tasks need parallel visibility; exploration needs expandability. The container choice shapes how effectively users can process the pre-computed options.

**When to use:** When implementing UI for presenting multiple pre-generated interpretive paths or integration options requiring user selection

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_format_for_decision_support` - extends
- `prn_decision_interface_modality_matching` - embodies


### `embodied-decision-substrate-generation` - Embodied Decision Substrate Generation

Generate sufficient mock/sample data to populate decision interfaces so users can develop felt intuition rather than abstract evaluation.

*Description:* Generate sufficient mock/sample data to populate decision interfaces so users can develop felt intuition rather than abstract evaluation.

Rather than describing options abstractly, generate enough concrete mock data to fill out decision support interfaces. This enables users to develop an 'embodied feel' for what each choice entails through interaction with substantive content rather than evaluating descriptions of content.

**When to use:** When designing decision points where abstract descriptions would be insufficient for users to appreciate the full weight of each option

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_synthetic_data_for_best_practi` - embodies
- `prn_embodied_decision_substrate` - embodies


### `interpretive-choice-cascade-pre-computation` - Interpretive Choice Cascade Pre-Computation

Pre-generate the full set of downstream revisions required by each competing interpretation before presenting options to users.

*Description:* Pre-generate the full set of downstream revisions required by each competing interpretation before presenting options to users.

When users face competing interpretations of data or readings, the system pre-computes what revisions would be needed to interconnected elements (like throughline parts) for each option. This makes the full implications of each choice visible upfront rather than discovered after commitment.

**When to use:** When integrating empirical data into structured outlines where multiple valid interpretations exist and each would propagate differently through the structure

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_option_impact_preview` - embodies
- `prn_interpretive_cascade_instantiation` - embodies


### `productivity-filtered-relationship-exploration` - Productivity-Filtered Relationship Exploration

Distinguish relationships that are 'productive to experiment with' from exhaustive cataloging of all possible connections.

*Description:* Distinguish relationships that are 'productive to experiment with' from exhaustive cataloging of all possible connections.

Not every relationship between source material and framework merits exploration. The system should help identify which relationships would be productive to pursue—those that might enrich, twist, or refine throughlines—based on current project needs rather than presenting all possible connections equally.

**When to use:** When surfacing potential connections between sources and theoretical frameworks, to prevent overwhelm and focus experimentation.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_resource_proportionality` - supports
- `prn_productive_relationship_filtering` - embodies


### `serial-processing-with-global-throughline-awarenes` - Serial Processing with Global Throughline Awareness

Process source documents sequentially while maintaining active awareness of the entire throughline ecosystem.

*Description:* Process source documents sequentially while maintaining active awareness of the entire throughline ecosystem.

When going through sources one by one, maintain the full context of all throughlines being developed so that each source's potential contributions can be evaluated against the whole system. This prevents isolated extraction and enables recognition of cross-throughline implications during per-document processing.

**When to use:** During systematic review of source materials for a multi-threaded intellectual project.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_context_completeness` - supports
- `prn_serial_global_processing` - embodies


### `propagation-triggered-stress-testing` - Propagation-Triggered Stress Testing

Automatically trigger stress tests of interconnected system elements when modification options are surfaced.

*Description:* Automatically trigger stress tests of interconnected system elements when modification options are surfaced.

When presenting virtual options for modifying one throughline, the system should automatically trigger stress tests showing how that modification would propagate to other throughlines. This transforms local editing decisions into system-aware choices by making cross-element effects visible before commitment.

**When to use:** When users are considering modifications to any element within an interconnected argument system.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_bounded_propagation` - supports
- `prn_option_impact_preview` - embodies


### `source-framework-relationship-classification` - Source-Framework Relationship Classification

Explicitly categorize each source material's relationship type to the theoretical framework before processing.

*Description:* Explicitly categorize each source material's relationship type to the theoretical framework before processing.

When integrating external sources (PDFs, articles) with developing arguments, first classify what kind of relationship the source has: illustration of main dynamic, discovery of previously undetected nuance/sub-dynamic, challenge to existing logic, etc. Different relationship types then route to different processing pathways with distinct implications for framework evolution.

**When to use:** When processing batches of source materials against established theoretical throughlines, before extracting or integrating content.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_content_based_routing` - supports
- `prn_relationship_type_taxonomy` - embodies


### `cascaded-generation-triggers` - Cascaded Generation Triggers

Trigger generation of dependent elements immediately after generating the elements they depend on.

*Description:* Trigger generation of dependent elements immediately after generating the elements they depend on.

When one element is generated, immediately trigger generation of elements that logically follow or connect to it - generate transitions after generating the elements they transition between, generate implementations after generating substances. This pre-populates the possibility space before users need to navigate it, reducing wait time during exploration.

**When to use:** Any workflow where elements have logical dependencies and generation is cheap enough to speculate - document structures where sections connect, UI flows where screens link, arguments where premises lead to conclusions.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_activity_state_gated_automation` - variant_of
- `prn_possibility_space_architecture` - Pre-generates branching possibility spaces for navigation
- `prn_forward_staged_data_harvesting` - embodies


### `substance-instance-matrices` - Substance × Instance Matrices

Generate N instances per M substance types, creating a selectable matrix of possibilities.

*Description:* Generate N instances per M substance types, creating a selectable matrix of possibilities.

For each archetypal type (substance), generate a fixed number of concrete instantiations (instances), creating an M×N matrix where users first select substance (choosing which archetype fits their purpose) then select instance (choosing which specific manifestation of that archetype they prefer). All cells are pre-generated and regeneratable.

**When to use:** When presenting alternative approaches that vary along two dimensions: the abstract strategy (how to argue) and the concrete execution (what specific language to use). Examples: argument types × specific arguments, transition logics × transition phrasings.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_abstract_concrete_progressive_` - supports
- `prn_substance_instance_tiering` - Direct implementation of two-tier substance/instance selection pattern
- `prn_pre_curation_with_option_prese` - embodies


### `collapsible-detail-architecture` - Collapsible Detail Architecture

Default to structural/logical summaries with expandable detailed content underneath.

*Description:* Default to structural/logical summaries with expandable detailed content underneath.

Present each element with a two-layer structure: a visible structural summary (bulletpoints, logic description, archetypal name) and a collapsed detailed layer (full narrative text, specific language). Users can expand any element to see detail without leaving the structural overview. This preserves big-picture navigation while making concrete instantiation accessible.

**When to use:** When users need to make structural decisions across many elements before attending to surface-level detail - essay structure, argument organization, narrative planning.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_format_for_decision_support` - embodies
- `prn_detail_deferral_with_accessibility` - Implements collapsed-by-default detail with expand-on-demand access
- `prn_function_form_phase_separation` - supports


### `hierarchical-sharpen-triggers` - Hierarchical Sharpen Triggers

Regeneration buttons that incorporate all downstream selections and rejections into the regeneration context.

*Description:* Regeneration buttons that incorporate all downstream selections and rejections into the regeneration context.

Each element has a 'sharpen' action that regenerates it using enriched context from all user choices made at downstream levels. The sharpening call includes not just what was selected but what was rejected, enabling the LLM to understand the full decision space and generate options more precisely aligned with emerging user preferences.

**When to use:** Any system where earlier/abstract elements can be made more appropriate after later/concrete elements have been specified - outlines after content is drafted, introductions after conclusions are written, connectors after both endpoints are defined.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_regeneration_over_retrofitting` - embodies
- `prn_contrastive_context_enrichment` - embodies
- `prn_upstream_regeneration_from_downstream` - Enables downstream refinements to trigger upstream regeneration
- `prn_refinement_versioning` - Tracks version numbers through iterative sharpen cycles
- `prn_negative_selection_capture` - embodies


### `in-slot-option-swapping` - In-Slot Option Swapping

Multiple options occupy the same visual position, with selection swapping content in place rather than stacking alternatives.

*Description:* Multiple options occupy the same visual position, with selection swapping content in place rather than stacking alternatives.

When presenting multiple possibilities for an element (e.g., transition options between arguments), alternatives should swap into the same visual slot rather than appearing as a vertical stack. Clicking 'transition #2' replaces 'transition #1' in the same position, maintaining spatial relationships and making comparison feel like trying on alternatives rather than surveying a list.

**When to use:** When presenting alternative options for any element that has a fixed position in a larger structure (transitions, connectors, opening variations), particularly when spatial context matters for evaluating fit.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_format_for_decision_support` - supports
- `prn_possibility_space_architecture` - Allows navigation within pre-populated option spaces
- `prn_visual_state_legibility` - embodies


### `logical-rhetorical-translation-prerequisites` - Logical-Rhetorical Translation Prerequisites

Identify features that make logical arguments more amenable to rhetorical transformation.

*Description:* Identify features that make logical arguments more amenable to rhetorical transformation.

Before attempting to translate logical structures into rhetorical presentations, analyze which logical argument forms translate more naturally to effective rhetoric. Some logical arguments may need polishing to acquire features that make rhetorical transformation smoother—this is not rhetorical work but logical work that enables better rhetorical outcomes.

**When to use:** When preparing structured arguments for audience-facing presentation, when evaluating whether outlines are ready for prose generation

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_function_form_phase_separation` - embodies
- `prn_downstream_aware_generation` - embodies
- `prn_dual_outline_constraint` - embodies


### `bidirectional-stage-learning-loop` - Bidirectional Stage Learning Loop

Generate outputs at later stages to learn what's needed at earlier stages, then iterate.

*Description:* Generate outputs at later stages to learn what's needed at earlier stages, then iterate.

Rather than perfecting each stage before advancing, generate provisional outputs at later stages to reveal what's missing or underdeveloped at earlier stages. Use the experience of producing version 1 of a later-stage output to understand what refinements are needed at prior stages. This creates a learning cycle where stage interdependencies are discovered empirically rather than theorized abstractly.

**When to use:** When process design is uncertain, when stage interdependencies are unclear, or when theoretical analysis of stage requirements is proving unproductive

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_process_as_data` - embodies
- `prn_practical_discovery_over_theoretical` - embodies
- `prn_dialectical_refinement` - embodies


### `rhetorical-gap-taxonomy` - Rhetorical Gap Taxonomy

Maintain an explicit classification of what might be missing for effective rhetorical presentation.

*Description:* Maintain an explicit classification of what might be missing for effective rhetorical presentation.

When transitioning from structural to presentational concerns, systematically check against a taxonomy of rhetorical elements: opening hooks, illustrative examples, clarifying metaphors, narrative landmarks/flagposts, structural interventions (chapters/parts), closing statements (rhetorical questions, calls to action). This taxonomy provides structured gap identification rather than ad-hoc noticing.

**When to use:** When preparing content for rhetorical presentation, evaluating whether structural outlines are ready for execution, or assessing writing completeness

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_domain_archetypes` - embodies
- `prn_benchmark_driven_best_practice` - embodies
- `prn_gap_aware_processing` - embodies


### `comprehensive-execution-brief` - Comprehensive Execution Brief

Create a self-contained document that enables a zero-context LLM to execute complex tasks.

*Description:* Create a self-contained document that enables a zero-context LLM to execute complex tasks.

When delegating to a new LLM session, produce a brief that contains: complete background context, explicit task specifications, success criteria, permitted interventions, constraints, and the rationale for decisions. The goal is immersion sufficient that the executing LLM can handle edge cases intelligently without consultation. This is not mere instruction but knowledge transfer that enables autonomous execution.

**When to use:** When work must span multiple LLM sessions, when delegating to automated pipelines, or when human-designed plans must be machine-executed

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_context_completeness` - embodies
- `prn_context_immersion_for_execution` - embodies
- `prn_cross_session_context_handoff` - embodies


### `stage-bridging-extraction-strategy` - Stage-Bridging Extraction Strategy

Systematically identify what can be extracted at the current stage that will serve subsequent stages.

*Description:* Systematically identify what can be extracted at the current stage that will serve subsequent stages.

At each processing stage, explicitly analyze what information could be gathered that would enable better performance at the next stage. Package this extraction within current-stage work so users contribute without recognizing the forward-looking purpose. This creates a pipeline where each stage actively prepares for its successor rather than operating in isolation.

**When to use:** When designing multi-stage processing pipelines, especially where user input is required at multiple stages and backtracking is costly

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_structured_elicitation` - embodies
- `prn_forward_staged_data_harvesting` - embodies
- `prn_downstream_aware_generation` - embodies


### `user-question-driven-pattern-discovery` - User-Question-Driven Pattern Discovery

Ground pattern discovery in the specific questions target users would ask.

*Description:* Ground pattern discovery in the specific questions target users would ask.

The prompt frames the entire analysis around "researchers who want to make quick sense of collections of articles" and their characteristic needs. This provides evaluative criteria for which patterns matter and which are merely interesting - does discovering this help researchers or not?

**When to use:** When analyzing for system design and the ultimate measure of success is user value rather than analytical completeness.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_user_archetype_grounding` - embodies
- `prn_function_based_on_demand_retri` - supports


### `noise-aware-prompt-framing` - Noise-Aware Prompt Framing

When providing noisy data to LLMs, explicitly frame expectations about relevance and filtering.

*Description:* When providing noisy data to LLMs, explicitly frame expectations about relevance and filtering.

The instruction to clarify that "some of the data... won't be relevant" preemptively calibrates LLM behavior. This prevents the model from either forcing relevance onto irrelevant data or becoming confused about why certain content is included.

**When to use:** Any task where input data is not curated specifically for the analysis, including historical data, legacy systems, or comprehensive archives that contain mixed-relevance content.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_irrelevance_tolerance_instruction` - embodies
- `prn_wildcard_inclusion_for_complet` - supports


### `trinity-classification-framework` - Trinity Classification Framework

Structure analytical exploration around a multi-dimensional classification scheme that captures complementary aspects.

*Description:* Structure analytical exploration around a multi-dimensional classification scheme that captures complementary aspects.

The engines/bundles/media trinity provides three lenses for classifying the same phenomena - processing logic (engines), organizational grouping (bundles), and output rendering (media). This multi-dimensional approach prevents premature collapse into a single classification axis.

**When to use:** When exploring patterns in complex domains where phenomena have multiple aspects that may require different treatment - what something is, how it's grouped, and how it's presented.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_extrapolative_inference_request` - enables
- `prn_provisional_structures` - embodies


### `streaming-progress-visibility` - Streaming Progress Visibility

For long-running LLM operations, use streaming with visual progress indicators to maintain operational visibility.

*Description:* For long-running LLM operations, use streaming with visual progress indicators to maintain operational visibility.

The mention of "streaming, dots, etc" indicates a pattern of maintaining visible progress for extended API calls. This prevents the "black box" effect where users don't know if processing is stalled or progressing, enabling informed intervention.

**When to use:** Any batch or long-running LLM operation where human monitoring is expected and where early termination or intervention may be necessary.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_visual_state_legibility` - embodies
- `prn_human_authority_gate` - enables


### `context-limit-splitting-strategy` - Context-Limit Splitting Strategy

When source materials exceed context limits, split them strategically into multiple processing units.

*Description:* When source materials exceed context limits, split them strategically into multiple processing units.

Rather than truncating or summarizing oversized inputs, the approach proactively identifies files that may exceed token limits and splits them into multiple units that each receive full-fidelity processing. "We might need to split the largest of them into two if it's more than one million tokens."

**When to use:** When working with large documents or datasets that may exceed model context windows, especially when fidelity of analysis matters more than processing efficiency.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_staged_processing` - supports
- `prn_provenance_preservation` - enables


### `batch-then-synthesize-pattern` - Batch-Then-Synthesize Pattern

Process multiple items individually with intermediate artifacts, then perform cross-item synthesis.

*Description:* Process multiple items individually with intermediate artifacts, then perform cross-item synthesis.

Each file is processed independently, generating an analysis_[x].json artifact that captures findings. Only after all individual processing completes does the system perform a reconciliation synthesis across all artifacts. This creates clean separation between exploration and integration.

**When to use:** When analyzing multiple documents or data sources for emergent patterns, especially when individual items may exceed what can be meaningfully processed together, or when intermediate artifacts enable progressive refinement.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_cross_slot_synthesis_scanning` - enables
- `prn_staged_processing` - embodies


### `future-use-injection` - Future-Use Injection

Explicitly inject downstream processing requirements into upstream generation prompts.

*Description:* Explicitly inject downstream processing requirements into upstream generation prompts.

This technique involves documenting all downstream operations that will be performed on generated outputs, then incorporating those requirements directly into the generation prompt. For example, if throughlines will be synthesized across shared slots, the throughline generation prompt explicitly states this requirement so the LLM can structure outputs to facilitate that synthesis.

**When to use:** When designing multi-stage LLM pipelines where outputs from earlier stages feed into later processing. Critical when later stages have structural requirements that early-stage outputs must satisfy.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_capability_addition_cascade_analysis` - supports
- `prn_downstream_aware_generation` - embodies


### `bridging-strategy-elicitation` - Bridging Strategy Elicitation

Explicitly request LLMs to generate strategies for connecting disparate elements rather than asking them to simply connect those elements.

*Description:* Explicitly request LLMs to generate strategies for connecting disparate elements rather than asking them to simply connect those elements.

Instead of asking "combine these throughlines," ask "what bridging strategies could make these throughlines click together?" This meta-level query produces actionable techniques rather than a single merged output, giving users strategic options and making the reconciliation logic explicit. The strategies themselves become artifacts that can be evaluated, selected, and reused.

**When to use:** When integrating elements that have meaningful tensions or divergences—not simple aggregation cases but genuine synthesis challenges where the mode of integration matters.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_cognitive_load_transfer` - embodies
- `prn_possibility_space` - supports


### `slot-level-synthesis-abstraction` - Slot-Level Synthesis Abstraction

Generate abstract synthesis by reconciling content from multiple sources at each structural slot rather than attempting holistic integration.

*Description:* Generate abstract synthesis by reconciling content from multiple sources at each structural slot rather than attempting holistic integration.

Rather than synthesizing entire documents or arguments at once, this technique processes each functional slot (e.g., IMPLICATIONS) independently across all source streams. For each slot, the LLM identifies shared points, reconciles tensions, and produces a unified abstraction. This produces synthesis that respects the structural logic of the domain while managing the cognitive complexity of integration.

**When to use:** When merging multiple documents, arguments, or analyses that share common structural slots. Especially useful when sources have natural alignment through shared templates but divergent content within those templates.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_cross_slot_synthesis_scanning` - embodies
- `prn_chunking` - embodies


### `throughline-factory-pattern` - Throughline Factory Pattern

A structured approach to generating multiple parallel argument streams that share common functional slots and are designed for eventual convergence.

*Description:* A structured approach to generating multiple parallel argument streams that share common functional slots and are designed for eventual convergence.

The pattern involves generating multiple independent "throughlines" (argument threads) that each populate the same structural skeleton. Each throughline has its own content for shared slots (IMPLICATIONS, INTERVENTIONS, etc.), but the slot structure is common across all throughlines. This shared structure enables systematic synthesis at each slot level when throughlines are merged.

**When to use:** When building systems that generate multiple parallel options (arguments, designs, analyses) that must eventually be synthesized rather than simply selected between. Particularly valuable when the synthesis should preserve elements from multiple streams rather than choosing one winner.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_shared_scaffold_parallel_streams` - embodies
- `prn_downstream_aware_generation` - enables
- `prn_cascading_virtuality` - embodies


### `recommendation-mode-request` - Recommendation Mode Request

Explicitly request that the LLM propose a default recommendation rather than presenting balanced analysis.


*Description:* Explicitly request that the LLM propose a default recommendation rather than presenting balanced analysis.


The prompt design goal is that the LLM "would propose a default and we won't have to think about it ourselves." This represents a specific output mode— recommendation rather than analysis—that must be explicitly requested because LLMs often default to presenting balanced considerations. Framing expectations around "propose a default" shifts the output from neutral to advisory.


**When to use:** Apply when the human role is to approve, override, or refine rather than to synthesize from scratch. Particularly valuable for routine decisions where cognitive effort should be minimized but human authority preserved.


*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_human_authority_gate` - supports
- `prn_cognitive_load_transfer` - enables
- `prn_default_recommendation_elicitation` - embodies


### `criteria-enumeration-in-advisory-prompts` - Criteria Enumeration in Advisory Prompts

Explicitly name the evaluation criteria when requesting decision advice from LLMs.


*Description:* Explicitly name the evaluation criteria when requesting decision advice from LLMs.


The prompt specifies asking "which would better serve our need for abstraction, modularity, comprehensiveness"—naming the criteria rather than asking for general advice. This technique makes the grounds for recommendation explicit, ensures the LLM reasons about what actually matters, and makes recommendations auditable against stated criteria.


**When to use:** Apply whenever requesting comparative evaluation or decision advice, especially when the relevant criteria are domain-specific or non-obvious. Critical when recommendations will influence downstream processing or persistent structures.


*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_comprehensive_context` - supports
- `prn_criteria_grounded_advisory` - embodies
- `prn_context_completeness` - Re-linked from deprecated principle during refactoring


### `choice-architecture-constraint` - Choice Architecture Constraint

Frame advisory requests by explicitly stating the choice architecture ("if the choice is between X and Y") to bound the response space.


*Description:* Frame advisory requests by explicitly stating the choice architecture ("if the choice is between X and Y") to bound the response space.


Rather than asking open-ended "what should I do?" questions, the prompt frames the decision as "if the choice is between linking it to this existing principle or creating a new one." This constrains the LLM's advisory space to the actual options under consideration, preventing tangential advice about options not on the table.


**When to use:** Apply when the decision space is already known and the need is for comparative evaluation rather than option discovery. Particularly useful when prior processing has already established what the viable options are.


*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_criteria_grounded_advisory` - enables
- `prn_format_for_decision_support` - supports


### `two-stage-generation-advice-pattern` - Two-Stage Generation-Advice Pattern

Separate option generation from selection advice into distinct, sequential API calls.


*Description:* Separate option generation from selection advice into distinct, sequential API calls.


The first API call focuses purely on generating the possibility space—in this case, identifying which existing principles could serve as parents for a demoted feature, plus surfacing the option of creating new principles. The second API call takes this generated space as input and provides advisory output on selection. This separation allows each call to be optimized for its function.


**When to use:** Apply when a workflow requires both creative option generation and evaluative selection guidance, particularly when the evaluation criteria are complex enough to benefit from dedicated reasoning rather than post-hoc filtering.


*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_chunking` - embodies
- `prn_generation_evaluation_separation` - embodies
- `prn_deferred_selection` - enables


### `assumption-grounded-question-sequencing` - Assumption-Grounded Question Sequencing

Sequence questions so that later questions only build on verified earlier answers.

*Description:* Sequence questions so that later questions only build on verified earlier answers.

Map the dependency structure of questions—which questions assume answers to other questions. Sequence interrogation so that assumption-generating questions come before assumption-dependent questions, and generate later questions only after earlier dependencies are resolved. Never stack questions on unverified foundations.

**When to use:** Multi-stage elicitation where questions have logical dependencies—diagnostic workflows, requirements refinement, philosophical inquiry, essay premise development.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_assumption_dependency_management` - embodies
- `prn_front_load_decisions` - supports
- `prn_logical_coherence` - enables


### `llm-deputized-exploration-pattern` - LLM-Deputized Exploration Pattern

Delegate possibility space exploration to LLM, reserve human attention for selection.

*Description:* Delegate possibility space exploration to LLM, reserve human attention for selection.

Rather than asking users to generate options or articulate positions from scratch, have the LLM exhaustively enumerate the possibility space based on context, then present these as options for human evaluation. This exploits the asymmetry between LLM generation costs (cheap) and human generation costs (expensive/fatiguing).

**When to use:** Any scenario where users "know it when they see it" better than they can generate it from scratch—design preference elicitation, problem framing, strategic option development, assumption mapping.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_cognitive_load_transfer` - embodies
- `prn_possibility_space` - embodies
- `prn_anthropologist_role` - enables


### `progressive-batch-interrogation-pattern` - Progressive Batch Interrogation Pattern

Present questions in small batches, adapting subsequent batches based on answers.

*Description:* Present questions in small batches, adapting subsequent batches based on answers.

Instead of presenting all questions upfront, divide interrogation into stages (e.g., 3 batches of 3 questions). Each batch generates based on prior answers plus remaining strategic objectives. The final batch synthesizes everything from earlier stages. Accept latency between batches as the cost of relevance.

**When to use:** Complex elicitation scenarios where later questions should depend on earlier answers—onboarding flows, diagnostic interviews, requirements gathering, assumption refinement for creative work.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_emergence_through_iterative_re` - supports
- `prn_chunking` - embodies
- `prn_staged_adaptive_interrogation` - embodies


### `multiple-choice-with-escape-valve-pattern` - Multiple-Choice with Escape Valve Pattern

Generate N structured options plus one open-ended "add your own" option.

*Description:* Generate N structured options plus one open-ended "add your own" option.

Pre-generate sophisticated multiple choice answers (e.g., 5) that represent the LLM's best mapping of the possibility space, then add a final option for user-generated alternatives. This captures 80% of cases efficiently while preserving 100% coverage through the escape valve. Allow multiple selections to reflect that preferences aren't always mutually exclusive.

**When to use:** Any user input solicitation where the domain is bounded enough for meaningful option generation but open enough that surprises are possible—preference elicitation, assumption probing, configuration selection, feedback collection.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_possibility_space` - embodies
- `prn_wildcard_inclusion_for_complet` - embodies
- `prn_cognitive_load_transfer` - enables


### `genre-indexed-requirement-templates` - Genre-Indexed Requirement Templates

Use genre conventions to pre-specify what functional elements and through-lines a piece needs, guiding the elicitation process.

*Description:* Use genre conventions to pre-specify what functional elements and through-lines a piece needs, guiding the elicitation process.

For each genre (essay, analysis, proposal, etc.), the system maintains a template of expected functional slots and common through-line patterns. This allows the system to "coach and force and nudge the user into thinking about dimensions that they need to think through" by knowing in advance what building blocks are typically required.

**When to use:** Apply when the output genre is known and has conventional structural expectations that can scaffold the elicitation and composition process.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_genre_as_scaffold` - embodies
- `prn_benchmark_driven_best_practice` - enables
- `prn_domain_archetypes` - supports


### `phase-readiness-gates` - Phase Readiness Gates

Transitions between processing phases require explicit verification that prior phases have achieved sufficient completion.

*Description:* Transitions between processing phases require explicit verification that prior phases have achieved sufficient completion.

The system tracks "readiness" for phase transitions—e.g., rhetorical outlining is gated until the functional outline reaches sufficient completeness. Gates can be surfaced to users as prompts ("We need X more elements before we can identify through-lines") and can be overridden with user acknowledgment of the limitations this introduces.

**When to use:** Apply in multi-phase workflows where later phases depend on the outputs of earlier phases and premature transition would produce hollow results.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_abstraction_level_sequencing` - embodies
- `prn_chunking` - supports


### `theory-answer-multiplication` - Theory-Answer Multiplication

User inputs are systematically combined with a persistent theoretical framework to generate strategic items that neither could produce alone.

*Description:* User inputs are systematically combined with a persistent theoretical framework to generate strategic items that neither could produce alone.

Rather than processing user answers in isolation, the system routes them through an existing theoretical base extracted from the user's prior work. This enables inference, reveals implications, surfaces connections, and generates follow-up questions that wouldn't emerge from the answers alone. Strategic items are tagged with both their input origin and theoretical grounding.

**When to use:** Apply when users have an existing body of work or theoretical commitments that should inform the interpretation of new inputs.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_cross_pollination_as_generativ` - enables
- `prn_theory_grounded_extraction` - embodies
- `prn_intellectual_profile` - supports


### `through-line-factory-pattern` - Through-line Factory Pattern

An explicit scanning mechanism that identifies potential higher-level connections across disparate functional elements.

*Description:* An explicit scanning mechanism that identifies potential higher-level connections across disparate functional elements.

A dedicated processing component that takes a populated functional outline and systematically scans for patterns that could constitute through-lines—abstract connective tissues linking different parts of an argument (e.g., diagnosis to prescription, phenomena to implications). The factory both proposes candidate through-lines and identifies what elements are missing to complete them.

**When to use:** Apply after functional elements are sufficiently populated, as a distinct phase that bridges component-level and synthesis-level work.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_gap_aware_processing` - enables
- `prn_cross_slot_synthesis_scanning` - embodies


### `question-to-problematique-conversion` - Question-to-Problematique Conversion

A mechanism to convert unanswered questions into deliberately preserved dialectical tensions rather than treating them as blockers.

*Description:* A mechanism to convert unanswered questions into deliberately preserved dialectical tensions rather than treating them as blockers.

When users cannot answer follow-up questions, the system offers to convert them to "problematiques"—marked open questions that become structural features of the output. These are tracked separately from gaps-to-be-filled, and can be surfaced in the final argument as acknowledged uncertainties or dialectical tensions.

**When to use:** Apply when building knowledge structures where some uncertainty is legitimate and should be preserved in the output, rather than hidden or artificially resolved.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_productive_incompletion` - embodies
- `prn_optionality_preservation` - supports


### `mutual-exclusivity-mapping` - Mutual Exclusivity Mapping

Explicitly identify and display which possibilities are mutually exclusive versus composable.

*Description:* Explicitly identify and display which possibilities are mutually exclusive versus composable.

When generating multiple possibilities, analyze and mark which options can coexist (can be combined into the same throughline/configuration) versus which are mutually exclusive (choosing one eliminates others). This transforms a flat list of options into a structured possibility space with explicit constraints.

**When to use:** When presenting options that have logical relationships with each other—some compatible, some incompatible—and users need to understand these relationships to make informed choices.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_logical_coherence` - supports
- `prn_contrastive_context_enrichment` - supports
- `prn_possibility_as_foreclosure_warning` - embodies


### `ui-llm-complementarity-architecture` - UI-LLM Complementarity Architecture

Design UI and LLM as complementary systems with distinct roles in managing possibility space.

*Description:* Design UI and LLM as complementary systems with distinct roles in managing possibility space.

Structure the system so that UI handles presentation, selection, and state management while LLM handles generation, questioning, and possibility analysis. Both are "allies" working toward the same goal of surfacing and exploring options. UI makes possibilities navigable; LLM makes possibilities visible. Neither alone is sufficient.

**When to use:** When building AI-augmented tools where users need to both explore generated options and make consequential selections among them.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_format_for_decision_support` - supports
- `prn_interactive_cognition` - Re-linked from deprecated principle during refactoring
- `prn_human_authority_gate` - supports
- `prn_thinking_environments` - embodies


### `functional-slot-architecture` - Functional Slot Architecture

Define argument structure through named functional positions rather than content-based or positional descriptions.

*Description:* Define argument structure through named functional positions rather than content-based or positional descriptions.

Decompose arguments (or other complex artifacts) into functional slots like "diagnosis," "implication," "intervention" where each slot is defined by what it DOES in the argument rather than what it contains or where it appears. Content can then be assigned to slots based on functional fit, and the same content might serve different functions in different configurations.

**When to use:** When building systems for argument construction, essay writing, or any structured composition where the role of elements matters more than their position or identity.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_trajectory_over_identity` - supports
- `prn_genre_as_scaffold` - supports
- `prn_function_form_phase_separation` - embodies


### `llm-driven-diagnostic-questioning` - LLM-Driven Diagnostic Questioning

LLM identifies what it can see, what's uncertain, and what questions would resolve uncertainty.

*Description:* LLM identifies what it can see, what's uncertain, and what questions would resolve uncertainty.

Rather than generating complete outputs or asking generic questions, the LLM analyzes its current understanding, identifies specific gaps or decision points where user input would materially change outputs, and generates targeted questions. The questions are diagnostically motivated—each question has a clear function in the possibility space.

**When to use:** When user input is incomplete or ambiguous and the LLM can identify specific information that would disambiguate between competing possibilities.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_anthropologist_role` - embodies
- `prn_emergence_through_iterative_re` - supports
- `prn_proactive_insufficiency_signaling` - embodies


### `multi-level-possibility-mapping-interface` - Multi-Level Possibility Mapping Interface

Generate and display possibilities at multiple abstraction levels with explicit mapping between levels.

*Description:* Generate and display possibilities at multiple abstraction levels with explicit mapping between levels.

Create a UI pattern where possibilities exist at distinct abstraction layers (e.g., strategic items → throughlines → slots), and the interface explicitly shows how possibilities at one level combine to produce possibilities at the next. Users can explore combinations and see which upstream choices generate which downstream option spaces.

**When to use:** When building systems for complex artifacts (arguments, designs, plans) that have hierarchical structure where decisions at higher levels constrain options at lower levels.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_visual_state_legibility` - supports
- `prn_cascading_virtuality` - embodies
- `prn_possibility_space` - embodies


### `state-contrast-audit` - State Contrast Audit

Verify that all interactive states have sufficient visual differentiation.

*Description:* Verify that all interactive states have sufficient visual differentiation.

Systematically enumerate the visual states an interface element can inhabit (active/inactive, selected/unselected, hovered, disabled) and verify that each pair of states has sufficient contrast to be instantly distinguishable. Flag state pairs that rely on subtle differences (slight opacity changes, minor color shifts) as legibility risks requiring remediation.

**When to use:** Interface design review, accessibility auditing, any system where users make selections that will inform downstream LLM processing.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_visual_state_legibility` - embodies


### `decision-support-formatting` - Decision-Support Formatting

Transform LLM outputs requiring user selection into visually structured, scannable formats.

*Description:* Transform LLM outputs requiring user selection into visually structured, scannable formats.

When LLM outputs will be presented for human evaluation/selection, apply formatting transforms that prioritize comparison: convert prose lists to bulleted items, separate options with visual boundaries, group related items, ensure consistent structure across alternatives. This is a distinct formatting mode from 'reading comprehension' presentation.

**When to use:** Any interface where users must choose among LLM-generated options—cluster selection, alternative generation, recommendation surfaces, classification review.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_generative_personalization` - Re-linked from deprecated principle during refactoring
- `prn_bespoke_contextual` - supports
- `prn_format_for_decision_support` - embodies


### `decision-context-bundle` - Decision Context Bundle

Package selections with their decision context for downstream LLM consumption.

*Description:* Package selections with their decision context for downstream LLM consumption.

When users make selections, construct a structured bundle containing: (1) what options were available, (2) what was selected, (3) what was explicitly viewed but not selected, (4) optionally, the sequence of interaction. Pass this bundle to downstream LLM processing stages rather than just the selection results. Format enables LLM to reason about user preferences contrastively.

**When to use:** Multi-stage workflows where early human selections inform later LLM processing—wizard interfaces, iterative refinement flows, preference elicitation systems.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_decision_space_propagation` - embodies
- `prn_contrastive_context_enrichment` - supports
- `prn_negative_selection_capture` - enables


### `quiescence-triggered-automation` - Quiescence-Triggered Automation

Gate automated actions on detected user inactivity rather than immediate event response.

*Description:* Gate automated actions on detected user inactivity rather than immediate event response.

Monitor user activity signals (mouse movement, clicking patterns, scroll behavior) and only trigger automated behaviors (navigation, suggestions, updates) when the user has been quiescent for a threshold period. This transforms automation from chaotic interruption into assistive suggestion that respects the user's exploration rhythm.

**When to use:** Any interface where automated suggestions or navigation could interrupt active user exploration—auto-complete, smart navigation, recommendation surfaces, contextual help.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_activity_state_gated_automation` - embodies


### `cost-explained-processing-choice` - Cost-Explained Processing Choice

Presenting users with processing strategy choices alongside explicit cost implications.

*Description:* Presenting users with processing strategy choices alongside explicit cost implications.

When offering users the choice between pre-extraction (batch processing all types upfront) and on-demand extraction (processing as needed), the system 'explains clearly' the cost implications of each approach. This pattern makes resource tradeoffs visible and gives users informed agency over computational expenditure rather than hiding costs or making unilateral decisions.

**When to use:** When systems offer multiple processing strategies with different resource profiles, especially in LLM-based systems where token costs vary significantly based on approach.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_dual_mode_operation` - embodies
- `prn_constraint_as_strategy` - Re-linked from deprecated principle during refactoring
- `prn_budget_driven_strategy` - supports


### `expert-transparency-mode` - Expert Transparency Mode

An optional detailed view that exposes internal processing logic for users developing expertise.

*Description:* An optional detailed view that exposes internal processing logic for users developing expertise.

For 'expert users, or users who are about to become experts,' the system provides a way to 'go and look inside the hood, but in an accessible way.' This view shows what each visualization mode extracts, how elements pass to the curator, and how different modes affect processing. The feature serves both transparency and pedagogical goals—building user mental models of previously black-box processes.

**When to use:** When building systems with pedagogical goals where users should progressively understand system internals, or when transparency is valued for trust-building with sophisticated users.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_tacit_to_explicit` - embodies
- `prn_formalization_as_education` - supports


### `plain-language-registry-extension-pipeline` - Plain-Language Registry Extension Pipeline

A multi-stage process enabling users to add new capability types through plain-language descriptions that get progressively formalized.

*Description:* A multi-stage process enabling users to add new capability types through plain-language descriptions that get progressively formalized.

Users describe desired new visualization types in plain language. An LLM analyzes and formalizes the description. Users review the formalization, learning from the translation. Upon approval, another LLM creates the proper registry entry. The system then analyzes implications for extraction, curation, and rendering stages. This pipeline democratizes system extension while maintaining structural integrity.

**When to use:** When building extensible systems where non-technical users should be able to add new processing modes or capability types without direct code modification.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_human_authority_gate` - embodies
- `prn_formalization_as_education` - embodies
- `prn_capability_addition_cascade_analysis` - enables


### `vision-model-output-verification-stage` - Vision-Model Output Verification Stage

An optional post-rendering verification step that sends generated visuals to vision-capable LLMs to confirm specification adherence.

*Description:* An optional post-rendering verification step that sends generated visuals to vision-capable LLMs to confirm specification adherence.

After diagrams or visualizations are rendered, the system can optionally send them to vision-capable models (Claude, Gemini) to verify that all specified elements are present and correctly represented. This creates a quality assurance loop that catches rendering failures and specification drift. The feature is positioned as trust-enhancing and user-optional.

**When to use:** When generating visual outputs where correctness is important and the generation process may introduce errors or omissions not detectable by the generating system alone.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_cybernetic_correction` - supports
- `prn_multimodal_output_verification` - embodies


### `extract-curate-render-pipeline` - Extract-Curate-Render Pipeline

A three-stage processing architecture for transforming text into visualizations with distinct LLM roles at each stage.

*Description:* A three-stage processing architecture for transforming text into visualizations with distinct LLM roles at each stage.

The workflow separates extraction (pulling elements from source texts), curation (preparing and organizing extracted elements for rendering), and rendering (generating final visual outputs). Each stage has dedicated prompts and processing logic, with outputs from each stage feeding the next. This separation enables stage-specific optimization and debugging.

**When to use:** When building systems that transform unstructured input into structured visual outputs, especially when the transformation requires multiple interpretive steps that benefit from different prompting strategies.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_chunking` - embodies
- `prn_process_determinism` - supports


### `context-complete-session-briefing` - Context-Complete Session Briefing

Generate comprehensive handoff documents that contain all context needed for contextually isolated future sessions.

*Description:* Generate comprehensive handoff documents that contain all context needed for contextually isolated future sessions.

When work must continue in a session that 'won't have any context apart from what you give it,' generate a complete briefing that explains: the task, the existing artifacts (prompts, pipelines), the methodology, the specific problem being addressed, and the desired approach. The briefing should enable a fresh session to continue work without information loss.

**When to use:** Apply when complex multi-session work involves LLMs that lack persistent memory, especially when continuing sessions may use different models or occur after significant time gaps.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_context_completeness` - Re-linked from deprecated principle during refactoring
- `prn_cross_session_context_handoff` - embodies
- `prn_comprehensive_context` - supports


### `abstract-structural-placeholder-pattern` - Abstract Structural Placeholder Pattern

Maintain generic structural placeholders throughout intermediate processing, reserving meaningful labels for final stages.

*Description:* Maintain generic structural placeholders throughout intermediate processing, reserving meaningful labels for final stages.

Use placeholders like 'Level 0', 'Root Category', 'Sub-Category' throughout extraction and curation, explicitly acknowledging these are structural roles rather than content descriptions. This pattern prevents premature concretization while maintaining clear structural relationships. The 'robotic legend' is a feature of intermediate artifacts, not a bug—it signals where concretization is still needed.

**When to use:** Apply when building visualization or document pipelines where structural relationships are determined before content fully crystallizes. Placeholders make explicit what remains to be concretized.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_abstract_concrete_progressive_` - enables
- `prn_late_binding_semantic_labels` - embodies


### `multi-stage-suggestion-collection-with-late-reconc` - Multi-Stage Suggestion Collection with Late Reconciliation

Collect naming/labeling suggestions across multiple early stages, then reconcile them in a dedicated later stage.

*Description:* Collect naming/labeling suggestions across multiple early stages, then reconcile them in a dedicated later stage.

Rather than making naming decisions at each stage, extraction and curation stages generate suggestions for concrete labels. These suggestions accumulate and are passed to a reconciliation stage that 'will look at them and reconcile or choose its own.' This pattern separates suggestion generation from decision-making, enabling each stage to contribute observations without bearing commitment burden.

**When to use:** Apply when multiple processing stages have partial visibility into what good labels/names might be, but none has complete context. The reconciliation stage can weigh suggestions against each other and against the fully assembled content.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_deferred_commitment` - embodies
- `prn_optionality_preservation` - supports


### `concretization-stage` - Concretization Stage

A dedicated pre-rendering stage that transforms abstract structural categories into content-appropriate concrete labels.

*Description:* A dedicated pre-rendering stage that transforms abstract structural categories into content-appropriate concrete labels.

After curation establishes logical structure and before rendering produces visual output, a concretization stage examines the actual content of extractions and determines appropriate semantic labels. This stage bridges abstract frameworks with particular content, replacing generic placeholders like 'Root Category' with meaningful names derived from the actual material.

**When to use:** Apply when pipelines use abstract structural roles (parent/child, root/leaf, category/subcategory) that must eventually be presented to users with meaningful labels. Especially valuable when the same structural role may need different names depending on content.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_late_binding_semantic_labels` - embodies
- `prn_particularity_recovery` - enables


### `carryover-relationship-annotation` - Carryover Relationship Annotation

Explicitly track which relationships are inherited versus directly established.

*Description:* Explicitly track which relationships are inherited versus directly established.

When relationships propagate through connection chains (e.g., groundings → features → principles), annotate inherited relationships distinctly from direct relationships. This preserves provenance and enables reasoning about relationship strength and directness.

**When to use:** Complex knowledge graphs with transitive relationships, provenance-sensitive systems, contexts where relationship strength matters.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_controlled_propagation` - supports
- `prn_provenance_preservation` - embodies


### `stray-element-as-workflow-trigger` - Stray Element as Workflow Trigger

Use the presence of disconnected elements as an automatic trigger for reconciliation workflows.

*Description:* Use the presence of disconnected elements as an automatic trigger for reconciliation workflows.

Rather than waiting for users to notice gaps, systematically identify elements lacking expected connections and use their existence to initiate structured reconciliation processes. The 'stray' status becomes a first-class trigger event, not just a passive state.

**When to use:** Knowledge graph maintenance, continuous integration of knowledge systems, any system where connectivity is a quality metric.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_event_driven_refinement` - embodies
- `prn_gap_aware_processing` - supports


### `zero-modification-first-assessment` - Zero-Modification-First Assessment

Assess whether elements can connect without changes before proposing any modifications.

*Description:* Assess whether elements can connect without changes before proposing any modifications.

Before triggering reformulation logic, explicitly check whether the elements can be legitimately connected in their current form. This separates 'discovery of existing but unrecognized relationships' from 'creation of new relationships through reformulation' - two conceptually distinct operations.

**When to use:** Knowledge management systems, relationship discovery tools, any context where you want to distinguish finding versus creating connections.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_resource_proportionality` - supports
- `prn_graduated_intervention_intensity` - embodies


### `bidirectional-reformulation-options` - Bidirectional Reformulation Options

Present modification options for either or both elements when proposing relationship-enabling changes.

*Description:* Present modification options for either or both elements when proposing relationship-enabling changes.

When an LLM proposes reformulations to enable relationships, it generates separate options: modify element A only, modify element B only, or modify both. This prevents hidden bias toward modifying one element type and gives users genuine choice about where conceptual change should occur.

**When to use:** Knowledge graph curation, ontology alignment, schema reconciliation - any context where disconnected elements might be reconnected through semantic modification.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_bidirectional_modification_symmetry` - embodies
- `prn_optionality_preservation` - supports


### `staged-integration-workflow` - Staged Integration Workflow

A multi-phase workflow moving from discovery through assessment to proposal to acceptance to integration, with clear gates between phases.


*Description:* A multi-phase workflow moving from discovery through assessment to proposal to acceptance to integration, with clear gates between phases.


The workflow explicitly sequences: (1) identification of candidates, (2) LLM assessment of direct compatibility, (3) LLM proposal of modifications for incompatible pairs, (4) user review and acceptance, (5) integration of accepted changes. Each phase has distinct inputs, outputs, and actors (system, LLM, human). The phases create natural breakpoints where users can pause, review, or abandon without corrupting system state.


**When to use:** Apply when building any human-AI collaborative workflow where actions have persistent effects on shared data structures. The pattern prevents cascading errors by ensuring human checkpoints before state changes, while still leveraging LLM capability for discovery and proposal generation.


*Confidence:* 75% | *Status:* draft


### `reformulation-suggestion-pipeline` - Reformulation Suggestion Pipeline

A workflow where an LLM proposes element modifications that would enable previously impossible relationships, presented for human review and selective acceptance.


*Description:* A workflow where an LLM proposes element modifications that would enable previously impossible relationships, presented for human review and selective acceptance.


When direct relationship matching fails, the system enters a reformulation mode where the LLM generates specific suggestions for how to modify the wording, scope, or framing of elements such that they become compatible. These suggestions are presented as options ("producing options for reconciliation") that preserve user agency. The pipeline separates generation (LLM) from selection (human), maintaining human authority over knowledge structure changes.


**When to use:** Apply when knowledge structures have rigidity that prevents relationship formation, but the underlying concepts could be compatible with different articulation. Useful in collaborative knowledge building where different contributors may have expressed related ideas in incompatible framings.


*Confidence:* 75% | *Status:* draft


### `llm-mediated-relationship-proposal` - LLM-Mediated Relationship Proposal

Using an LLM to assess potential relationships between elements and propose connections with varying degrees of modification required.


*Description:* Using an LLM to assess potential relationships between elements and propose connections with varying degrees of modification required.


The LLM receives two sets of disconnected elements and performs two types of analysis: (1) "direct hits" where relationships can be established without modifying either element, and (2) "bridge proposals" where the LLM suggests modifications to one or both elements that would enable a valid relationship. The LLM acts as a semantic similarity engine with creative reformulation capability, not just a classifier.


**When to use:** Apply when building systems that need to discover implicit relationships in knowledge structures, particularly when the relationship criteria involve semantic compatibility rather than exact matching. Effective when human time for manual relationship discovery is limited but the knowledge structure benefits from denser connections.


*Confidence:* 75% | *Status:* draft


### `review-accept-integrate-flow` - Review-Accept-Integrate Flow

Present system proposals for human review with direct pathways to integration upon acceptance.

*Description:* Present system proposals for human review with direct pathways to integration upon acceptance.

Structure the UI so that LLM-generated proposals (direct matches or reformulations) are presented for explicit human review. Acceptance triggers automatic integration into the knowledge base. Rejection returns to proposal generation or terminates. This pattern maintains human authority while minimizing friction for approved changes.

**When to use:** Apply whenever system proposals would modify persistent knowledge structures. Essential for maintaining trust in automated systems while enabling efficient knowledge base evolution.

*Confidence:* 75% | *Status:* draft


### `reformulation-option-generation` - Reformulation Option Generation

Generate modified versions of elements specifically designed to enable new relationships.

*Description:* Generate modified versions of elements specifically designed to enable new relationships.

When elements don't naturally connect, prompt the LLM to produce reformulated versions—of one or both elements—that would create valid pairings. Present these as options with clear indication of what changed and why. This makes the LLM a collaborator in knowledge base improvement, not just a classifier.

**When to use:** Apply after direct matching has been attempted and failed. Use when element definitions are provisional and the goal is knowledge base coherence rather than preserving original formulations.

*Confidence:* 75% | *Status:* draft


### `llm-mediated-relationship-assessment` - LLM-Mediated Relationship Assessment

Use an LLM to evaluate whether disconnected elements could or should be connected.

*Description:* Use an LLM to evaluate whether disconnected elements could or should be connected.

Position the LLM as an intelligent assessor between orphaned elements and potential relationships. The LLM evaluates semantic compatibility, identifies near-matches, and distinguishes between 'no valid connection' and 'connection possible with modification.' This leverages LLM comprehension without ceding decision authority.

**When to use:** Apply when orphan elements are identified and human review of all possible pairings would be prohibitively expensive. The LLM pre-filters and prioritizes human attention.

*Confidence:* 75% | *Status:* draft


### `stray-element-discovery` - Stray Element Discovery

Systematically identify elements lacking expected connections within a knowledge graph.

*Description:* Systematically identify elements lacking expected connections within a knowledge graph.

Query the knowledge base to surface elements that exist in isolation—lacking connections to complementary element types. This transforms implicit gaps into explicit work items, making invisible incompleteness visible and actionable.

**When to use:** Apply during knowledge base maintenance cycles, when preparing for relationship enrichment work, or when auditing knowledge structure integrity.

*Confidence:* 75% | *Status:* draft


### `cascading-relationship-inheritance` - Cascading Relationship Inheritance

When elements link, their existing relationships propagate to connected elements.

*Description:* When elements link, their existing relationships propagate to connected elements.

The prompt notes that "any groundings relationships that features have  will carry on to the principles linked to features." This is a pattern  where establishing a new relationship causes existing relationships of  one element to propagate to the newly connected element. It treats  relationship creation as a trigger for inheritance propagation rather  than an isolated event.


**When to use:** Apply when knowledge elements exist in a typed relationship network where  certain relationship types should transitively propagate across new  connections, enabling efficient knowledge enrichment through linking.


*Confidence:* 75% | *Status:* draft


### `user-gated-integration-pattern` - User-Gated Integration Pattern

Staging proposed changes for review before committing to persistent structures.

*Description:* Staging proposed changes for review before committing to persistent structures.

A workflow pattern where system-generated modifications are staged in a  review space rather than directly applied. Users see proposed changes  alongside their implications, can accept/reject/modify individual proposals,  and only approved changes propagate to the knowledge base. This maintains  human authority while leveraging automated proposal generation.


**When to use:** Apply when automated systems generate modifications to persistent knowledge  structures, and when the cost of incorrect modifications exceeds the cost  of human review. Essential for knowledge bases where coherence and  authority matter.


*Confidence:* 75% | *Status:* draft


### `reformulation-as-reconciliation` - Reformulation-as-Reconciliation

Using LLM to suggest how elements could be rephrased to enable new relationships.

*Description:* Using LLM to suggest how elements could be rephrased to enable new relationships.

A technique where, instead of only matching elements as they exist, an  LLM proposes how elements could be reformulated to create valid  relationships. The LLM examines the semantic distance between elements  and suggests minimal modifications that would make connection meaningful.  Crucially, it generates multiple reformulation options rather than a  single recommendation.


**When to use:** Apply when knowledge elements are close enough to relate but their current  formulations create friction, and when preserving the underlying meaning  while enabling connection is more valuable than maintaining exact wording.


*Confidence:* 75% | *Status:* draft


### `multi-tier-matching-pipeline` - Multi-Tier Matching Pipeline

Graduated approach from direct matching to modified matching to user acceptance.

*Description:* Graduated approach from direct matching to modified matching to user acceptance.

A processing pipeline that attempts matches at multiple tiers of intervention:  first seeking direct connections with no modifications, then proposing  single-element modifications, then bilateral modifications, and finally  presenting all viable options for user selection. Each tier represents  increased intervention surface and is attempted only if prior tiers  prove insufficient.


**When to use:** Apply when reconciling knowledge elements where exact matches are preferred  but near-matches are acceptable with modification, and where the cost of  modification should be proportional to matching difficulty.


*Confidence:* 75% | *Status:* draft


### `stray-element-detection` - Stray Element Detection

Programmatically identify elements that lack required relationship connections.

*Description:* Programmatically identify elements that lack required relationship connections.

A pattern for finding "orphaned" elements in knowledge graphs—elements  that should have relationships but don't. In this case, principles without  feature connections and features without principle connections. The  detection is structural (graph traversal) rather than semantic, identifying  absence through query rather than judgment.


**When to use:** Apply when building knowledge management systems where relationships between  element types are expected but not enforced, and you want to surface gaps  for remediation rather than letting them silently accumulate.


*Confidence:* 75% | *Status:* draft


## Project: refactoring

### `prn_meta_content_suppression` - LLM Meta-Commentary Filter

Filter LLM meta-commentary from end-user outputs, removing self-referential commentary about the generation process that represents internal processing artifacts.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_meta_content_suppression` - Created by refactoring engine


### `prn_multimodal_output_verification` - LLM Multimodal Verification

Cross-modal LLM verification of generated outputs, sending outputs to models that can perceive that modality and confirm alignment with specifications.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_input_anchored_validation` - Created by refactoring engine


### `prn_input_anchored_validation` - LLM Input Fidelity Check

LLM output validation by comparison to input ground truth, explicitly checking that outputs remain faithful to inputs rather than evaluating outputs in isolation.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_correction_before_commitment` - Created by refactoring engine


### `prn_economic_model_tiering` - LLM Model Tiering

Cost-optimized LLM model selection by pipeline stage, using cheaper/faster models for constrained tasks while reserving expensive models for unconstrained generation.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_resource_proportionality` - Created by refactoring engine


### `prn_human_authority_gate` - LLM Verification Gate

Verification gates between LLM generation and system commitment, interposing verification and correction stages that complete before any changes are committed.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_execution_readiness_criteria` - Created by refactoring engine


### `prn_anticipatory_model_instantiation` - LLM Anticipatory Model Construction

LLMs construct provisional output models from first inputs to guide data collection, building anticipatory models from earliest data points to identify information gaps.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_schema_as_hypothesis` - Created by refactoring engine


### `feat_structured_decision_presentation` - Structured Decision Presentation

When LLM outputs require human evaluation or selection, format for scanability and comparison through structured visual hierarchy (bullets, line breaks, grouping) over compact prose.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_cognitive_task_matched_presentation` - Created by refactoring engine


### `feat_optimistic_automation_with_undo` - Optimistic Automation with Undo

For high-confidence, low-stakes automated actions, proceed with the action while proactively notifying users and providing easy override mechanisms.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_optimistic_execution` - Created by refactoring engine


### `feat_llm_capability_impact_analysis` - LLM Capability Impact Analysis

When users propose new system capabilities, LLMs should analyze how additions cascade through processing stages and automatically identify required adjustments.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_change_impact_propagation` - Created by refactoring engine


### `feat_context_driven_system_specialization` - Context-Driven System Specialization

Design systems where contextual content (documents, user responses, examples) functions as runtime configuration that transforms generic systems into domain-specific tools.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_data_as_program` - Created by refactoring engine


### `feat_llm_continuous_strategy_adaptation` - LLM Continuous Strategy Adaptation

LLM systems should engage in ongoing strategic reasoning that re-evaluates approach and course-corrects based on accumulated context, rather than executing pre-planned pipelines.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_runtime_strategy_adaptation` - Created by refactoring engine


### `feat_llm_optimized_data_structures` - LLM-Optimized Data Structures

Design data structures anticipating that LLMs will be the primary consumers, optimizing for machine parsing and reasoning rather than human readability.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_consumer_optimized_representation` - Created by refactoring engine


### `feat_ai_thinking_environments` - AI Thinking Environments

AI-mediated contexts can produce superior thinking environments compared to traditional tools by enabling real-time theory testing, virtualization, simulation, and dynamic feedback that traditional writing tools cannot provide.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_interactive_cognition` - Created by refactoring engine


### `feat_meta_learning_capability_evolution` - Meta-Learning Capability Evolution

Systems should include meta-learning components that analyze operational feedback and propose modifications to their own capability registries, shortening the path from insight to implementation.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_self_modifying_systems` - Created by refactoring engine


### `feat_comprehensive_llm_context` - Comprehensive LLM Context

Provide comprehensive context to LLMs, even if not immediately relevant to the specific task, because understanding emerges from relationships between elements rather than isolated facts.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_context_completeness` - Created by refactoring engine


### `feat_llm_readable_capability_registry` - LLM-Readable Capability Registry

System capabilities should be explicitly registered in structured schemas that LLMs can read, select from, and combine—making the system's action space legible to AI reasoning.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_machine_legible_affordances` - Created by refactoring engine


### `feat_paradigm_schema_embodiment` - Paradigm Schema Embodiment

Embody coherent paradigms, epistemes, and ideologies as structured schemas within the system, enabling theories to be subjected to rigorous multi-perspectival critique from various intellectual vantage points.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_perspective_as_structure` - Created by refactoring engine


### `feat_multi_model_cross_examination` - Multi-Model Cross-Examination

Use multiple LLM models to cross-examine each other's outputs and observe how they respond differently to similar tasks—their divergence reveals insights and accelerates understanding of the problem domain.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_adversarial_multi_perspective_refinement` - Created by refactoring engine
- `prn_divergence_as_signal` - Created by refactoring engine


### `feat_llm_dynamic_personalization` - LLM Dynamic Personalization

Use LLMs to generate both content and design elements dynamically, creating bespoke outputs personalized to specific data and context rather than forcing contexts into generic templates.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_context_as_configuration` - Created by refactoring engine
- `prn_generative_personalization` - Created by refactoring engine


### `feat_budget_front_loading` - Budget Front-Loading

Elicit explicit resource budgets (time, queries, cost) as first-class inputs at the beginning of workflows, using them to drive strategic choices rather than treating them as afterthoughts that truncate execution.

*Confidence:* 75% | *Status:* draft

**Embodies principles:**
- `prn_front_load_decisions` - Created by refactoring engine
- `prn_constraint_as_strategy` - Created by refactoring engine


## Project: test

### `new-feature-test-123` - New Feature Test 123

Testing ID gen

*Description:* Testing ID gen

Should work now

*Confidence:* 75% | *Status:* draft


### `feat_test_feature_abc_041816` - Test Feature ABC

A test feature

*Description:* For testing

*Confidence:* 75% | *Status:* draft


## Project: theory-service

### `cognitive-scaffolding-for-intellectual-navigation` - Cognitive Scaffolding for Intellectual Navigation

Building external structures ("crutches") that enable both humans and AI  to navigate complex conceptual terrain beyond unassisted capacity.


*Description:* Recognize that complex intellectual work exceeds the cognitive capacity of  both humans (working memory limits) and LLMs (context coherence limits).  Design external scaffolding structures—visible intermediate representations,  explicit connection maps, justification fields—that function as shared  cognitive infrastructure enabling navigation of complexity that neither  party could manage internally.


*Confidence:* 85% | *Status:* draft

**Embodies principles:**
- `prn_explicit_process_externalization`
- `prn_externalized_imagination_infrastructure`


### `bidirectional-improvement-loop-architecture` - Bidirectional Improvement Loop Architecture

Intermediate structures that create feedback loops for both LLM reasoning  improvement and human system improvement.


*Description:* Design intermediate representational layers (fields, metadata, scaffolds)  that serve two improvement loops: (1) the structure itself forces the LLM  into better reasoning by requiring explicit justification and source  attribution, and (2) the populated structure gives humans visibility into  LLM reasoning that enables prompt refinement and system improvement. The  same structure serves both loops simultaneously.


*Confidence:* 87% | *Status:* draft

**Embodies principles:**
- `prn_formalization_as_education`
- `prn_dual_consumer_structure_design`


### `hierarchical-detail-explanation-trade-off-navigation` - Hierarchical Detail-Explanation Trade-off Navigation

Explicit acceptance of structural complexity (sub-levels, sub-hierarchies)  as the necessary cost of explanatory richness.


*Description:* When facing the choice between flat/simple structure with opaque reasoning  versus deep/complex structure with transparent reasoning, deliberately choose  depth. The cost of navigating additional hierarchy is outweighed by the value  of inspectable, auditable, improvable reasoning. Design interfaces to make  hierarchy navigation tractable rather than avoiding hierarchy.


*Confidence:* 82% | *Status:* draft

**Embodies principles:**
- `prn_visibility_as_quality_forcing`
- `prn_granular_quality_legibility`


### `inference-provenance-capture-pattern` - Inference Provenance Capture Pattern

Structured capture of each inferential step including conclusion, triggering  source, selection justification, and implicit alternatives.


*Description:* For each inference or connection the LLM makes (forward inference, contradiction  detection, conceptual link), capture: (a) the inference itself, (b) the specific  source context that triggered it, (c) why this instance was selected over  alternatives, and (d) what the alternative inferences could have been. This  creates a multi-layered record that enables both verification and improvement.


*Confidence:* 90% | *Status:* draft

**Embodies principles:**
- `prn_provenance_preservation`
- `prn_reasoning_justification_externalization`


### `blind-spots-before-hypotheses-flow` - Blind Spots Before Hypotheses Flow

Reorders wizard flow to explore epistemic blind spots BEFORE generating hypothesis cards, so theses are informed by user's revealed theoretical agenda.

*Description:* The Concept Setup Wizard now follows a new flow where notes analysis extracts blind spots but NOT hypothesis cards. Users then explore these blind spots through the curator/sharpener questioning system. Only after they've answered blind spots questions does the system generate hypothesis, genealogy, and differentiation cards - informed by what the user revealed they care about through their answers. This produces more targeted, relevant hypotheses that address the user's actual theoretical concerns rather than generic possibilities.

*Confidence:* 80% | *Status:* draft

**Embodies principles:**
- `prn_epistemic_grounding_before_thesis_generation`


### `answer-options-pre-generation` - Answer Options Pre-Generation

Pre-generates multiple choice answer options in the background while user answers previous questions

*Description:* Implements background pre-generation of answer options during blind spots questioning. After curator completes, immediately generates options for first 2 slots. After each answer submission, generates options for next 3 upcoming slots. Uses a cache (preGeneratedOptionsCache) to store pre-generated options by slot index. When user clicks 'Help me articulate', checks cache first for instant response. If cache hit, user sees options immediately; if cache miss, generates synchronously. This exploits the time users spend reading/answering questions as free computation budget.

*Confidence:* 90% | *Status:* implemented

**Embodies principles:**
- `prn_interaction_time_as_computation_budget`
- `prn_background_pregeneration_illusion`

**Code locations (1):**
- `/home/evgeny/projects/theory-service/frontend/src/ConceptSetupWizard.jsx:preGenerateOptionsForSlot` (lines 1184-1231)


### `pre-allocated-slot-interleaving` - Pre-Allocated Slot Interleaving

Assign items from multiple categories to specific positions using an interleaving  pattern before generating item content, ensuring temporal dispersion.


*Description:* The slot allocation map "{misreading_risk: [4, 9, 14], presupposition: [1, 5], ...}"  demonstrates pre-allocation with built-in interleaving. Rather than filling slots 1-3  with category A then 4-6 with category B, positions are pre-assigned to ensure same- category items are spread across the session. This is structural interleaving - the  dispersion is guaranteed by the allocation map before any content is generated.


*Confidence:* 85% | *Status:* draft

**Embodies principles:**
- `prn_strategic_structure_before_tactical_content`
- `prn_cognitive_task_matched_presentation`
- `prn_temporal_category_dispersion`


### `variable-ceiling-valid-at-any-point-workflow` - Variable-Ceiling Valid-At-Any-Point Workflow

Workflows with a defined maximum scope where any amount of partial completion produces  valid downstream input, with progress indicators that reflect variable completion.


*Description:* The system has "up to 16 slots" but explicitly validates outputs from "Even 3 out of 16  answers." Users "can skip/terminate at any point." The progress indicator shows "X of Y  answered where Y can change." This creates a workflow where the ceiling is known (16  maximum) but the floor is zero, and any point between is legitimate. Downstream processing  must be designed to work with variable input richness rather than requiring complete data.


*Confidence:* 89% | *Status:* draft

**Embodies principles:**
- `prn_closure_matches_problem`
- `prn_graceful_partial_completion_validity`


### `dynamic-queue-injection-pattern` - Dynamic Queue Injection Pattern

Background generation process watches for triggers, generates content, and injects it  into a shared queue that the frontend polls or subscribes to via SSE.


*Description:* The Sharpener runs continuously, watching for new answers. When triggered, it generates  new questions and injects them into specific queue positions. The frontend polls or  uses Server-Sent Events to receive newly available questions. This decouples generation  timing from presentation timing - users see questions "as they become available" rather  than waiting for batch generation. The queue structure (with pre-allocated slot positions)  enables questions to appear in the right order even when generated out of order.


*Confidence:* 88% | *Status:* draft

**Embodies principles:**
- `prn_interaction_time_as_computation_budget`
- `prn_continuous_background_synthesis`
- `prn_dynamic_elicitation_injection`


### `curator-sharpener-two-stage-architecture` - Curator-Sharpener Two-Stage Architecture

Separate strategic analysis (what to emphasize) from tactical generation (specific  content), with the first stage producing routing metadata consumed by the second.


*Description:* The Curator stage runs once at initialization, analyzing input against a taxonomy and  producing an allocation map (which categories, how many slots each, at which positions).  The Sharpener stage runs continuously, consuming this map plus accumulated user responses  to generate specific content for each allocated slot. This separation allows strategic  decisions to be made with full input context while tactical decisions incorporate  evolving response context.


*Confidence:* 91% | *Status:* draft

**Embodies principles:**
- `prn_early_issue_confirmation_for_routing`
- `prn_staged_adaptive_interrogation`
- `prn_strategic_structure_before_tactical_content`


### `parallel-state-companion-track` - Parallel State Companion Track

A design pattern where a specific dimension of process state (epistemic gaps,  tensions, decisions) is tracked as a persistent companion alongside main workflow  state.


*Description:* Rather than embedding state within workflow stages or treating it as transient,  certain dimensions are elevated to companion status—visible throughout the workflow,  updated continuously, and available for reference at any point. The prompt compares  this to "how concepts/dialectics tracking works," suggesting an existing pattern  being extended to new content.


*Confidence:* 82% | *Status:* draft

**Embodies principles:**
- `prn_parallel_epistemic_state_tracking`
- `prn_continuous_background_synthesis`


### `conditions-of-possibility-interrogation` - Conditions of Possibility Interrogation

A specific questioning technique that asks what enables a way of thinking and what  it simultaneously occludes or forecloses.


*Description:* Rather than simply asking "what does this concept mean?" or "is this concept valid?",  this technique asks: "What makes this way of thinking possible? What historical,  paradigmatic, or structural conditions enable it? And what does thinking this way  make difficult to see or consider?" This surfaces the constitutive outside of any  conceptual framework.


*Confidence:* 88% | *Status:* draft

**Embodies principles:**
- `prn_possibility_as_foreclosure_warning`
- `prn_presupposition_surfacing_obligation`


### `confirm-then-route-interrogation-pattern` - Confirm-Then-Route Interrogation Pattern

A two-phase pattern where identified issues are first confirmed by users before  being used to structure subsequent questioning.


*Description:* Rather than immediately acting on detected gaps or uncertainties, the system first  presents them to users for confirmation ("are these real issues?"). Only confirmed  issues then become routing criteria for downstream interrogation design. This prevents  building question structures on false assumptions while converting user confirmation  into legitimate constraint.


*Confidence:* 85% | *Status:* draft

**Embodies principles:**
- `prn_confirmation_resolution_separation`
- `prn_assumption_dependency_management`
- `prn_early_issue_confirmation_for_routing`


### `seven-category-epistemic-gap-framework` - Seven-Category Epistemic Gap Framework

A structured typology for categorizing different kinds of epistemic underdetermination  in conceptual work.


*Description:* The framework distinguishes: (1) Ambiguities - contested meaning, (2) Likely misreadings -  predictable misunderstandings, (3) Gray areas - boundary cases, (4) Paradigm-dependent  conclusions - episteme-relative readings, (5) Presupposition clarification - implicit  priors, (6) Structural weaknesses - inherent limitations, (7) Conditions of possibility -  enabling/occluding conditions. Each category implies different remediation strategies  and downstream handling.


*Confidence:* 90% | *Status:* draft

**Embodies principles:**
- `prn_uncertainty_typology_richness`
- `prn_epistemic_ontological_distinction`


### `uncertainty-to-question-pipeline` - Uncertainty-to-Question Pipeline

Use user-confirmed uncertainties as structured input for generating targeted 
follow-up questions, creating a direct mapping from identified gaps to exploration.


*Description:* Rather than generating generic follow-up questions, use the specific gaps, tensions, 
and open questions that users confirmed as relevant to parameterize question generation. 
This creates focused exploration that directly addresses what users acknowledged as 
genuinely uncertain, rather than scattershot questioning that may not serve actual 
user needs. The confirmation stage acts as a targeting mechanism.


*Confidence:* 86% | *Status:* draft

**Embodies principles:**
- `prn_staged_adaptive_interrogation`
- `prn_early_gap_modeling_for_progressive_clarification` - This feature IS the implementation of the principle - it creates a direct pipeline from identified/confirmed uncertainties to targeted question generation, ensuring questions fill specific gaps rather than asking generic follow-ups.
- `prn_negative_selection_capture`
- `prn_forward_staged_data_harvesting`


### `agency-preserving-response-options` - Agency-Preserving Response Options

Design response options that invite exploration ("Yes, explore this") rather than 
demanding action ("Approve") or binary judgment ("Accept/Reject").


*Description:* UI language shapes the cognitive task users think they're performing. "Approve/Reject" 
frames the task as judgment and demands resolution stance. "Yes, explore this / Yes + 
add context / Not relevant" frames the task as collaborative exploration and preserves 
user agency over what happens next. The language signals that confirming an uncertainty 
doesn't commit the user to resolving it.


*Confidence:* 88% | *Status:* draft

**Embodies principles:**
- `prn_deficit_neutral_uncertainty_framing`
- `prn_human_authority_gate`
- `prn_confirmation_resolution_separation`


### `confirm-explore-articulate-flow` - Confirm-Explore-Articulate Flow

Structure concept development as: LLM identifies → User confirms relevance → 
Confirmed items generate exploration questions → Questions clarify rather than resolve.


*Description:* This interaction pattern separates distinct cognitive operations across stages. 
First, the LLM proposes candidate uncertainties. Second, users perform lightweight 
confirmation (not resolution) of which are relevant. Third, confirmed items become 
inputs to question generation. Fourth, questions help articulate the shape of 
uncertainty rather than demanding answers. Each stage has different cognitive 
demands and different UI affordances.


*Confidence:* 92% | *Status:* draft

**Embodies principles:**
- `prn_articulation_over_resolution_questioning`
- `prn_confirmation_resolution_separation`
- `prn_early_gap_modeling_for_progressive_clarification` - The flow starts with LLM identifying gaps/tensions/questions from user notes - this IS the early gap modeling step. User confirmation then validates which gaps are real, and Stage 2 questions directly target those confirmed gaps.
- `prn_staged_adaptive_interrogation`


### `three-way-uncertainty-typology` - Three-Way Uncertainty Typology

Classify conceptual underdevelopment into Gaps (incomplete areas), Tensions 
(productive dialectics), and Open Questions (explorable uncertainties).


*Description:* This typology provides structural vocabulary for different types of incompleteness 
in user thinking. Gaps are areas where understanding is simply missing—they need 
filling. Tensions are oppositions inherent to the concept that may be productive 
to preserve—they need navigation, not resolution. Open Questions are uncertainties 
where exploration would be valuable—they need articulation. Each type maps to 
different downstream handling.


*Confidence:* 90% | *Status:* draft

**Embodies principles:**
- `prn_content_based_routing`
- `prn_early_gap_modeling_for_progressive_clarification` - The typology (gaps, tensions, questions) provides the vocabulary for modeling different TYPES of gaps, enabling more nuanced subsequent questioning - e.g., questions that help articulate a tension differ from questions that fill an information gap.
- `prn_productive_incompletion`
- `prn_uncertainty_typology_richness`


