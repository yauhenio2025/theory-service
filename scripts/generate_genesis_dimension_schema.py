#!/usr/bin/env python3
"""
Genesis Dimension Schema Generator

This script generates the schema extension for novel concept creation -
concepts that don't exist in public discourse but are implied/operational
in various domains.

The Genesis dimension is NOT tied to a single philosopher but synthesizes:
- Bachelard's concept of epistemic rupture (new concepts break with old)
- Canguilhem's normativity (concepts create new standards)
- Hacking's making up people (concepts can create new categories)
- Blumenberg's metaphorology (foundational metaphors shape thought)

Key Design Principles (from tool-ideator knowledge base):
- prn_staged_adaptive_interrogation: Questions build on previous answers
- prn_theory_grounded_extraction: Inputs gain power through theoretical framing
- prn_proactive_insufficiency_signaling: LLM signals when it lacks data
- prn_precision_forcing_interrogation: Questions force definitional precision
- prn_forward_staged_data_harvesting: Extract data for future pipeline stages
- prn_embodied_decision_substrate: Concrete material for decisions
- prn_formalization_as_education: Expose translation to build user expertise
"""

import pandas as pd
from datetime import datetime
import os

# Output directory
OUTPUT_DIR = "/home/evgeny/projects/theory-service/documentation"

def create_genesis_tables():
    """Create all Genesis dimension tables for novel concept setup."""

    tables = {}

    # ==========================================================================
    # TABLE 1: concept_genesis - The origin story of the concept
    # ==========================================================================
    tables['concept_genesis'] = {
        'description': """
CONCEPT GENESIS - Origin Story and Theoretical Lineage

This table captures WHERE the concept comes from and WHY it's being introduced.
For novel concepts, this is critical because LLMs have no training data about it.

Philosophy: Bachelard's epistemic rupture - new concepts break with existing frameworks.
The genesis must explain both what's being left behind AND what's being created.

Key Questions This Table Answers:
- Why does this concept need to exist?
- What intellectual tradition does it emerge from?
- What epistemic break does it represent?
- Who is introducing it and with what authority?
""",
        'columns': [
            'concept_id',
            'genesis_type',          # theoretical_innovation, empirical_discovery, synthetic_unification, paradigm_shift
            'originator_type',       # individual, collective, institutional, emergent
            'originator_description', # Who/what is introducing this concept
            'theoretical_lineage',   # What traditions does it build on
            'break_from',            # What it's breaking from (Bachelardian rupture)
            'break_rationale',       # Why the break is necessary
            'first_articulation_context', # Where/when first articulated
            'initial_problem_space', # What problem prompted its creation
            'claimed_novelty_type',  # terminological, conceptual, paradigmatic, methodological
            'novelty_justification', # Why it's genuinely new
            'source_type',           # user_input, collaborative_elaboration
            'source_reference',
            'confidence',
            'created_at',
            'updated_at'
        ],
        'data': [
            {
                'concept_id': 1,
                'genesis_type': 'theoretical_innovation',
                'originator_type': 'individual',
                'originator_description': 'The user/researcher introducing this concept into their theoretical framework',
                'theoretical_lineage': 'Builds on sovereignty theory (Bodin, Schmitt), technology studies (Winner, Feenberg), and critical infrastructure studies',
                'break_from': 'Traditional sovereignty as purely territorial/political; technology as neutral tool',
                'break_rationale': 'Existing frameworks cannot explain how technological dependencies create new forms of sovereignty loss that operate outside traditional political channels',
                'first_articulation_context': 'Research into critical infrastructure dependencies and digital colonialism',
                'initial_problem_space': 'How do nations lose effective control over their futures through technological lock-in without formal political subordination?',
                'claimed_novelty_type': 'conceptual',
                'novelty_justification': 'While "digital sovereignty" exists, "technological sovereignty" encompasses material, infrastructural, and epistemic dimensions beyond the digital',
                'source_type': 'user_input',
                'source_reference': 'Initial concept setup wizard',
                'confidence': 0.95,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
        ]
    }

    # ==========================================================================
    # TABLE 2: concept_problem_space - What gap this concept fills
    # ==========================================================================
    tables['concept_problem_space'] = {
        'description': """
CONCEPT PROBLEM SPACE - The Gap This Concept Fills

This table captures the ABSENCE that the concept addresses. For novel concepts,
articulating the problem space is often more important than the solution.

Philosophy: Canguilhem's normativity - concepts emerge to address vital problems.
A concept without a clear problem space is not genuinely needed.

Wizard Questions That Populate This:
- "What phenomenon cannot be adequately described with existing concepts?"
- "What question do you find yourself unable to answer with current vocabulary?"
- "What explanatory gap does this concept fill?"
""",
        'columns': [
            'id',
            'concept_id',
            'gap_type',              # descriptive, explanatory, normative, practical, methodological
            'gap_description',       # What's missing
            'failed_alternatives',   # What existing concepts have been tried
            'failure_diagnosis',     # Why alternatives fail
            'problem_domains',       # Where this gap is felt
            'stakeholder_impact',    # Who suffers from this conceptual gap
            'urgency_rationale',     # Why address this now
            'source_type',
            'source_reference',
            'confidence',
            'created_at'
        ],
        'data': [
            {
                'id': 1,
                'concept_id': 1,
                'gap_type': 'explanatory',
                'gap_description': 'Cannot explain how nations become dependent on foreign technology ecosystems without formal political agreements',
                'failed_alternatives': 'Digital sovereignty (too narrow), national security (too state-centric), economic dependency (misses epistemic dimension)',
                'failure_diagnosis': 'Each captures a fragment but misses the systemic, infrastructural, and normative totality',
                'problem_domains': 'International relations, technology policy, critical infrastructure, economic development',
                'stakeholder_impact': 'Policymakers lack vocabulary to articulate concerns; citizens cannot name their situation; researchers fragment the phenomenon',
                'urgency_rationale': 'Accelerating technological dependencies during AI transition make this gap increasingly costly',
                'source_type': 'user_input',
                'source_reference': 'Problem space wizard section',
                'confidence': 0.9,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 2,
                'concept_id': 1,
                'gap_type': 'normative',
                'gap_description': 'No framework for evaluating when technological dependencies become sovereignty-threatening vs. beneficial interdependence',
                'failed_alternatives': 'Protectionism (too crude), free trade (ignores power), techno-nationalism (too reactive)',
                'failure_diagnosis': 'Binary framings miss the gradient of sovereignty erosion and the possibility of strategic technological choices',
                'problem_domains': 'Policy evaluation, international negotiation, technology assessment',
                'stakeholder_impact': 'Decisions made on ad-hoc basis; inconsistent standards across domains',
                'urgency_rationale': 'Major technological choices being made now will lock in dependencies for decades',
                'source_type': 'user_input',
                'source_reference': 'Problem space wizard section',
                'confidence': 0.85,
                'created_at': datetime.now().isoformat()
            }
        ]
    }

    # ==========================================================================
    # TABLE 3: concept_differentiation - What the concept is NOT
    # ==========================================================================
    tables['concept_differentiation'] = {
        'description': """
CONCEPT DIFFERENTIATION - What This Concept Is NOT

CRITICAL for novel concepts: Since LLMs have no training data, they will try to
assimilate new concepts to familiar ones. This table prevents that collapse.

Philosophy: Sellars' contrast classes - meaning comes from systematic contrast.
A concept is defined as much by what it excludes as by what it includes.

Wizard Questions:
- "What existing concept might someone confuse this with?"
- "Why is this NOT just a variant of X?"
- "What would be lost if we just used term Y instead?"
""",
        'columns': [
            'id',
            'concept_id',
            'confused_with',         # What it might be mistaken for
            'confusion_type',        # synonym_collapse, subset_reduction, superset_expansion, false_opposition
            'differentiation_axis',  # What dimension distinguishes them
            'this_concept_position', # Where this concept stands on that axis
            'other_concept_position', # Where the other concept stands
            'what_would_be_lost',    # Consequences of the confusion
            'surface_similarity',    # Why confusion is tempting
            'deep_difference',       # The fundamental distinction
            'source_type',
            'source_reference',
            'confidence',
            'created_at'
        ],
        'data': [
            {
                'id': 1,
                'concept_id': 1,
                'confused_with': 'Digital Sovereignty',
                'confusion_type': 'subset_reduction',
                'differentiation_axis': 'Material scope',
                'this_concept_position': 'Encompasses physical infrastructure, supply chains, manufacturing, AND digital systems',
                'other_concept_position': 'Primarily concerns data, software, and digital services',
                'what_would_be_lost': 'Miss semiconductor dependencies, rare earth vulnerabilities, hardware backdoors, manufacturing capacity',
                'surface_similarity': 'Both concern technology and state control',
                'deep_difference': 'Technological sovereignty is fundamentally material and infrastructural, not just informational',
                'source_type': 'user_input',
                'source_reference': 'Differentiation wizard section',
                'confidence': 0.95,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 2,
                'concept_id': 1,
                'confused_with': 'Economic Nationalism',
                'confusion_type': 'false_opposition',
                'differentiation_axis': 'Normative stance',
                'this_concept_position': 'Analytical framework that can inform various policy positions',
                'other_concept_position': 'Policy program with specific political commitments',
                'what_would_be_lost': 'Analytical power; concept becomes politically charged; nuance collapses',
                'surface_similarity': 'Both concern national control over economic/technological assets',
                'deep_difference': 'Tech sovereignty is descriptive/analytical first; economic nationalism is prescriptive/political',
                'source_type': 'user_input',
                'source_reference': 'Differentiation wizard section',
                'confidence': 0.9,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 3,
                'concept_id': 1,
                'confused_with': 'National Security',
                'confusion_type': 'superset_expansion',
                'differentiation_axis': 'Specificity of concern',
                'this_concept_position': 'Specifically technological dependencies affecting capacity for self-determination',
                'other_concept_position': 'Broad concern with all threats to national safety and stability',
                'what_would_be_lost': 'The specific technological logic gets lost in general security discourse',
                'surface_similarity': 'Tech dependencies can be security threats',
                'deep_difference': 'Tech sovereignty focuses on structural capacity, not threat-response; includes positive dimension of capability-building',
                'source_type': 'user_input',
                'source_reference': 'Differentiation wizard section',
                'confidence': 0.85,
                'created_at': datetime.now().isoformat()
            }
        ]
    }

    # ==========================================================================
    # TABLE 4: concept_implicit_domains - Where operative without being named
    # ==========================================================================
    tables['concept_implicit_domains'] = {
        'description': """
CONCEPT IMPLICIT DOMAINS - Where This Concept Operates Without Being Named

For novel concepts, the claim is that the phenomenon EXISTS but lacks a name.
This table maps where to look for implicit instances.

Philosophy: Blumenberg's metaphorology - concepts can operate through metaphors
before explicit articulation. Hacking's looping effects - categories shape
what they categorize even before explicit recognition.

Wizard Questions:
- "In what domains do you see this phenomenon operating without explicit recognition?"
- "Where do people talk AROUND this concept without naming it?"
- "What proxy terms or euphemisms are used instead?"

This table is CRITICAL for the next phase: searching documents for implicit instances.
""",
        'columns': [
            'id',
            'concept_id',
            'domain_name',           # Field/area where concept operates implicitly
            'domain_type',           # academic, policy, industry, media, everyday
            'manifestation_pattern', # How it shows up in this domain
            'proxy_terms',           # What terms are used instead (JSON array)
            'proxy_term_limitations', # Why proxies are inadequate
            'domain_specific_form',  # How concept manifests uniquely here
            'key_actors',            # Who deals with this implicitly
            'observable_tensions',   # Conflicts that reveal the concept
            'document_types_to_search', # What sources to analyze
            'search_patterns',       # Keywords/patterns to find instances
            'source_type',
            'source_reference',
            'confidence',
            'created_at'
        ],
        'data': [
            {
                'id': 1,
                'concept_id': 1,
                'domain_name': 'Semiconductor Policy',
                'domain_type': 'policy',
                'manifestation_pattern': 'Debates about chip manufacturing capacity framed as "supply chain security" or "economic competitiveness"',
                'proxy_terms': '["supply chain resilience", "strategic autonomy", "onshoring", "friend-shoring", "de-risking"]',
                'proxy_term_limitations': 'Each captures one aspect; none articulates the sovereignty dimension explicitly',
                'domain_specific_form': 'Concerns about fab capacity, equipment dependencies, design tool monopolies',
                'key_actors': 'CHIPS Act policymakers, semiconductor executives, national security officials',
                'observable_tensions': 'Efficiency vs. resilience debates; market vs. strategic logic conflicts',
                'document_types_to_search': 'Congressional hearings, CHIPS Act documents, industry white papers, national security reviews',
                'search_patterns': '["chip shortage" AND (security OR autonomy), "semiconductor" AND (dependency OR vulnerability), "foundry" AND (strategic OR national)]',
                'source_type': 'user_input',
                'source_reference': 'Implicit domains wizard section',
                'confidence': 0.9,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 2,
                'concept_id': 1,
                'domain_name': 'Cloud Computing Procurement',
                'domain_type': 'industry',
                'manifestation_pattern': 'Concerns about vendor lock-in, data jurisdiction, foreign provider dependencies',
                'proxy_terms': '["vendor lock-in", "data sovereignty", "cloud sovereignty", "strategic cloud", "sovereign cloud"]',
                'proxy_term_limitations': '"Cloud sovereignty" is narrower; "vendor lock-in" is purely commercial framing',
                'domain_specific_form': 'Government cloud procurement debates, GAIA-X initiative, hyperscaler dependencies',
                'key_actors': 'CIOs, procurement officials, EU regulators, cloud providers',
                'observable_tensions': 'Cost efficiency vs. control; global scale vs. local autonomy',
                'document_types_to_search': 'EU cloud strategy documents, government procurement policies, GAIA-X white papers',
                'search_patterns': '["cloud" AND (sovereignty OR "strategic autonomy"), "hyperscaler" AND (dependency OR risk), "government cloud" AND (control OR independence)]',
                'source_type': 'user_input',
                'source_reference': 'Implicit domains wizard section',
                'confidence': 0.85,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 3,
                'concept_id': 1,
                'domain_name': 'AI Development Race',
                'domain_type': 'media',
                'manifestation_pattern': 'Framing of AI competition as geopolitical struggle, concerns about "falling behind"',
                'proxy_terms': '["AI race", "AI supremacy", "compute sovereignty", "AI nationalism", "strategic AI"]',
                'proxy_term_limitations': 'Race framing misses structural dependencies; "AI nationalism" is pejorative',
                'domain_specific_form': 'GPU access concerns, training data sovereignty, model dependency, talent flows',
                'key_actors': 'Tech journalists, AI researchers, policy think tanks, national AI strategies',
                'observable_tensions': 'Open science vs. strategic advantage; global talent vs. national capacity',
                'document_types_to_search': 'National AI strategies, tech journalism, AI policy reports, congressional AI hearings',
                'search_patterns': '["AI" AND (sovereignty OR "strategic autonomy" OR "national capacity"), "compute" AND (access OR dependency), "AI infrastructure" AND (control OR independence)]',
                'source_type': 'user_input',
                'source_reference': 'Implicit domains wizard section',
                'confidence': 0.8,
                'created_at': datetime.now().isoformat()
            }
        ]
    }

    # ==========================================================================
    # TABLE 5: concept_recognition_markers - How to identify implicit instances
    # ==========================================================================
    tables['concept_recognition_markers'] = {
        'description': """
CONCEPT RECOGNITION MARKERS - How to Identify Implicit Instances

For novel concepts, we need to train ourselves (and LLMs) to recognize instances
even when the concept isn't named. This table provides the recognition criteria.

Philosophy: Hacking's "making up people" - before a category is named,
we need criteria to recognize potential members of that category.

This table feeds into LLM prompts for document analysis:
"Look for passages that exhibit these markers even if the term X is not used."

Wizard Questions:
- "What are the telltale signs that someone is dealing with this phenomenon?"
- "What linguistic patterns indicate this concept is in play?"
- "What structural features would an instance have?"
""",
        'columns': [
            'id',
            'concept_id',
            'marker_type',           # linguistic, structural, behavioral, situational, argumentative
            'marker_description',    # What to look for
            'marker_pattern',        # Regex or search pattern if applicable
            'positive_indicator',    # What confirms presence
            'negative_indicator',    # What rules out presence
            'false_positive_risk',   # What might look like this but isn't
            'discrimination_guide',  # How to tell real from false positive
            'example_text',          # Example passage exhibiting this marker
            'weight',                # How strongly this indicates the concept
            'source_type',
            'source_reference',
            'confidence',
            'created_at'
        ],
        'data': [
            {
                'id': 1,
                'concept_id': 1,
                'marker_type': 'argumentative',
                'marker_description': 'Arguments that technology choices have political/sovereignty implications beyond economics',
                'marker_pattern': '(technological|tech|technology) AND (dependency|dependence|reliance) AND (strategic|sovereign|autonomy|independence|control)',
                'positive_indicator': 'Explicit connection between technological dependency and loss of political/strategic agency',
                'negative_indicator': 'Purely commercial framing (cost, efficiency, market share)',
                'false_positive_risk': 'General discussions of trade policy or economic protectionism',
                'discrimination_guide': 'Look for emphasis on CAPACITY and CONTROL rather than just economic benefit',
                'example_text': '"Our reliance on foreign chip fabrication means we cannot guarantee access to advanced semiconductors in a crisis—this is not just an economic issue but a question of national capacity for autonomous action."',
                'weight': 0.9,
                'source_type': 'user_input',
                'source_reference': 'Recognition markers wizard section',
                'confidence': 0.9,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 2,
                'concept_id': 1,
                'marker_type': 'structural',
                'marker_description': 'Description of technological lock-in that affects decision-making autonomy',
                'marker_pattern': '(lock-in|locked into|dependent on|reliant on) AND (cannot|unable|forced to|no choice)',
                'positive_indicator': 'Lock-in described as constraining strategic options, not just switching costs',
                'negative_indicator': 'Lock-in described purely in terms of migration costs or inconvenience',
                'false_positive_risk': 'Normal IT vendor lock-in discussions',
                'discrimination_guide': 'Key: does the lock-in affect FUNDAMENTAL capacity or just convenience?',
                'example_text': '"Having built our entire defense communication system on proprietary protocols from a single foreign vendor, we now find ourselves unable to even contemplate alternative security architectures."',
                'weight': 0.85,
                'source_type': 'user_input',
                'source_reference': 'Recognition markers wizard section',
                'confidence': 0.85,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 3,
                'concept_id': 1,
                'marker_type': 'situational',
                'marker_description': 'Crisis or near-crisis revealing hidden technological dependencies',
                'marker_pattern': '(crisis|shortage|supply chain|disruption) AND (revealed|exposed|showed|demonstrated) AND (dependency|vulnerability|reliance)',
                'positive_indicator': 'Crisis reveals that a technological dependency has strategic implications',
                'negative_indicator': 'Crisis is purely about temporary supply disruption with no strategic dimension',
                'false_positive_risk': 'General supply chain disruption reporting',
                'discrimination_guide': 'Key: does the crisis reveal STRUCTURAL dependency or just temporary shortage?',
                'example_text': '"The chip shortage revealed that our entire automotive industry—and with it, significant strategic manufacturing capacity—depends on decisions made by a handful of foreign foundries."',
                'weight': 0.8,
                'source_type': 'user_input',
                'source_reference': 'Recognition markers wizard section',
                'confidence': 0.85,
                'created_at': datetime.now().isoformat()
            }
        ]
    }

    # ==========================================================================
    # TABLE 6: concept_paradigmatic_cases - Exemplary instances
    # ==========================================================================
    tables['concept_paradigmatic_cases'] = {
        'description': """
CONCEPT PARADIGMATIC CASES - Exemplary Instances That Define the Concept

For novel concepts, paradigmatic cases serve as anchors for understanding.
These are the "if you want to understand X, look at Y" examples.

Philosophy: Kuhn's exemplars - scientific concepts are learned through
paradigmatic cases, not definitions. Wittgenstein's family resemblance -
concepts are defined by similarity to central cases.

Wizard Questions:
- "What's the clearest example of this concept in action?"
- "If you had to point to ONE case that captures the essence, what would it be?"
- "What historical or contemporary situation best illustrates this?"
""",
        'columns': [
            'id',
            'concept_id',
            'case_name',             # Brief label for the case
            'case_type',             # historical, contemporary, hypothetical, composite
            'full_description',      # Detailed description of the case
            'why_paradigmatic',      # What makes this exemplary
            'features_exhibited',    # Which concept features it shows (JSON array)
            'features_absent',       # Which features it doesn't show (limitations)
            'teaching_value',        # What understanding this case builds
            'controversy_notes',     # Any debates about this case
            'source_documents',      # References for this case
            'source_type',
            'source_reference',
            'confidence',
            'created_at'
        ],
        'data': [
            {
                'id': 1,
                'concept_id': 1,
                'case_name': 'European 5G and Huawei Dilemma',
                'case_type': 'contemporary',
                'full_description': 'European nations faced decisions about allowing Huawei equipment in 5G networks. The debate revealed that critical communication infrastructure would depend on a foreign power\'s technology, with implications for surveillance, maintenance access, and future upgrade paths. Nations found themselves choosing between economic efficiency (Huawei\'s lower costs) and technological autonomy.',
                'why_paradigmatic': 'Clear case where technological choice = sovereignty choice; involves infrastructure; reveals dependency that wasn\'t obvious; forced explicit discussion',
                'features_exhibited': '["infrastructure dependency", "surveillance vulnerability", "upgrade path lock-in", "supply chain risk", "forced explicit choice"]',
                'features_absent': '["manufacturing capacity dimension", "knowledge/IP dimension", "positive capability-building"]',
                'teaching_value': 'Shows how infrastructure choices become sovereignty choices; illustrates the hidden political dimension of technology procurement',
                'controversy_notes': 'Some argue this was primarily geopolitical (US pressure) rather than genuine sovereignty concern',
                'source_documents': 'EU 5G Toolbox, national security reviews (UK, Germany, France), US pressure campaign documentation',
                'source_type': 'user_input',
                'source_reference': 'Paradigmatic cases wizard section',
                'confidence': 0.95,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 2,
                'concept_id': 1,
                'case_name': 'Taiwan Semiconductor Manufacturing Dependency',
                'case_type': 'contemporary',
                'full_description': 'Global dependency on TSMC for advanced chip manufacturing means that a geopolitical crisis in the Taiwan Strait would immediately affect the technological capacity of virtually every advanced economy. No nation has been able to replicate TSMC\'s capabilities despite decades of investment.',
                'why_paradigmatic': 'Extreme concentration of critical capability; affects ALL advanced technology; reveals manufacturing capacity as sovereignty issue; ongoing crisis potential',
                'features_exhibited': '["manufacturing capacity gap", "single point of failure", "geopolitical vulnerability", "capability dependency", "long-term structural dependency"]',
                'features_absent': '["software/platform dependency", "data dependency", "everyday visibility to citizens"]',
                'teaching_value': 'Shows how material/manufacturing capacity creates sovereignty dependencies that cannot be quickly remedied',
                'controversy_notes': 'Some argue this is normal market specialization; others see it as dangerous strategic vulnerability',
                'source_documents': 'CHIPS Act debates, national semiconductor strategies, geopolitical analysis of Taiwan situation',
                'source_type': 'user_input',
                'source_reference': 'Paradigmatic cases wizard section',
                'confidence': 0.9,
                'created_at': datetime.now().isoformat()
            }
        ]
    }

    # ==========================================================================
    # TABLE 7: concept_user_elaborations - Q&A responses from setup wizard
    # ==========================================================================
    tables['concept_user_elaborations'] = {
        'description': """
CONCEPT USER ELABORATIONS - Captured Q&A Responses from Setup Wizard

This table stores ALL responses from the concept setup wizard - both
multiple choice selections and open-ended elaborations.

Design Principle (prn_staged_adaptive_interrogation): Questions build on
previous answers. Later questions adapt based on earlier responses.

Design Principle (prn_formalization_as_education): The process of answering
helps the user clarify their own thinking about the concept.

This is the RAW CAPTURE of user knowledge before LLM processing.
""",
        'columns': [
            'id',
            'concept_id',
            'wizard_stage',          # Which stage of the wizard (1-N)
            'question_id',           # Reference to the question asked
            'question_text',         # The actual question
            'question_type',         # multiple_choice, open_ended, scale, ranking, multi_select
            'options_presented',     # For MC questions, what options were shown (JSON)
            'selected_options',      # For MC, which were selected (JSON array)
            'open_response',         # For open-ended, the full response
            'confidence_self_report', # User's confidence in their answer (1-5)
            'elaboration_notes',     # Any additional notes user added
            'time_spent_seconds',    # How long user spent on this question
            'revision_history',      # If user revised answer (JSON array of previous)
            'source_type',           # Always 'user_input' for this table
            'created_at',
            'updated_at'
        ],
        'data': [
            {
                'id': 1,
                'concept_id': 1,
                'wizard_stage': 1,
                'question_id': 'genesis_type',
                'question_text': 'How would you characterize the origin of this concept?',
                'question_type': 'multiple_choice',
                'options_presented': '[{"value": "theoretical_innovation", "label": "A new theoretical framework or lens"}, {"value": "empirical_discovery", "label": "A pattern discovered through empirical observation"}, {"value": "synthetic_unification", "label": "A synthesis of previously separate ideas"}, {"value": "paradigm_shift", "label": "A fundamental reconceptualization"}, {"value": "other", "label": "Other (please elaborate)"}]',
                'selected_options': '["theoretical_innovation"]',
                'open_response': None,
                'confidence_self_report': 4,
                'elaboration_notes': 'It\'s primarily theoretical but grounded in observed patterns of technological dependency',
                'time_spent_seconds': 45,
                'revision_history': None,
                'source_type': 'user_input',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            },
            {
                'id': 2,
                'concept_id': 1,
                'wizard_stage': 2,
                'question_id': 'core_definition',
                'question_text': 'In one paragraph, provide your working definition of this concept.',
                'question_type': 'open_ended',
                'options_presented': None,
                'selected_options': None,
                'open_response': 'Technological sovereignty refers to the capacity of a political entity (typically a nation-state, but potentially a region or bloc) to exercise meaningful control over the technological systems upon which its economy, security, and social functioning depend. This includes not merely access to technologies but the capacity to understand, modify, maintain, and if necessary replace them. Full technological sovereignty implies capability across the stack: from materials and manufacturing to design and operation.',
                'confidence_self_report': 4,
                'elaboration_notes': None,
                'time_spent_seconds': 180,
                'revision_history': None,
                'source_type': 'user_input',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            },
            {
                'id': 3,
                'concept_id': 1,
                'wizard_stage': 3,
                'question_id': 'most_confused_with',
                'question_text': 'What existing concept is this MOST likely to be confused with, and why is that confusion problematic?',
                'question_type': 'open_ended',
                'options_presented': None,
                'selected_options': None,
                'open_response': 'Digital sovereignty. While related, digital sovereignty primarily concerns data, software, and online services. Technological sovereignty is broader—it includes the material infrastructure, manufacturing capacity, and physical supply chains that underpin digital systems. A nation could have strong digital sovereignty (data localization, domestic platforms) but weak technological sovereignty (dependent on foreign hardware, unable to manufacture chips).',
                'confidence_self_report': 5,
                'elaboration_notes': None,
                'time_spent_seconds': 120,
                'revision_history': None,
                'source_type': 'user_input',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
        ]
    }

    # ==========================================================================
    # TABLE 8: concept_source_pointers - Documents to search for implicit instances
    # ==========================================================================
    tables['concept_source_pointers'] = {
        'description': """
CONCEPT SOURCE POINTERS - Documents Queued for Implicit Instance Discovery

This table implements "document staging without processing" (from tool-ideator).
User can point to documents where they believe implicit instances exist,
WITHOUT requiring immediate full processing.

The document is registered with notes about WHAT TO LOOK FOR, enabling
later targeted extraction using the recognition markers.

Workflow:
1. User uploads or references document
2. User adds notes: "Look for discussions of X in section Y"
3. System queues for processing
4. LLM extracts using recognition markers
5. Extracted instances populate other schema tables

Design Principle (prn_forward_staged_data_harvesting): Capture document
references early, process systematically later.
""",
        'columns': [
            'id',
            'concept_id',
            'document_type',         # academic_paper, news_article, policy_document, book_chapter, interview, speech
            'document_reference',    # Citation, URL, or file path
            'document_title',
            'document_author',
            'document_date',
            'user_relevance_note',   # User's note on why this is relevant
            'expected_instances',    # What kind of implicit instances expected
            'specific_sections',     # Particular sections to focus on
            'search_patterns_to_use', # Which patterns from recognition_markers to apply
            'processing_status',     # queued, processing, completed, failed
            'processing_results',    # Summary of what was found (JSON)
            'extracted_instance_ids', # References to extracted instances
            'priority',              # User-assigned priority (1-5)
            'source_type',           # user_input
            'created_at',
            'queued_at',
            'processed_at'
        ],
        'data': [
            {
                'id': 1,
                'concept_id': 1,
                'document_type': 'policy_document',
                'document_reference': 'European Commission (2020). Shaping Europe\'s Digital Future. COM(2020) 67 final.',
                'document_title': 'Shaping Europe\'s Digital Future',
                'document_author': 'European Commission',
                'document_date': '2020-02-19',
                'user_relevance_note': 'Core EU digital strategy document. Should contain implicit tech sovereignty concerns framed as "strategic autonomy" and "digital sovereignty".',
                'expected_instances': 'Policy framings of technological dependency as sovereignty concern; strategic autonomy language',
                'specific_sections': 'Executive summary, Section on technology sovereignty, Section on strategic sectors',
                'search_patterns_to_use': '[1, 2, 3]',  # IDs from recognition_markers
                'processing_status': 'queued',
                'processing_results': None,
                'extracted_instance_ids': None,
                'priority': 5,
                'source_type': 'user_input',
                'created_at': datetime.now().isoformat(),
                'queued_at': datetime.now().isoformat(),
                'processed_at': None
            },
            {
                'id': 2,
                'concept_id': 1,
                'document_type': 'academic_paper',
                'document_reference': 'Edler, J., et al. (2020). Technology sovereignty. From demand to concept. Fraunhofer ISI Discussion Papers.',
                'document_title': 'Technology sovereignty. From demand to concept.',
                'document_author': 'Edler, J., et al.',
                'document_date': '2020',
                'user_relevance_note': 'One of few academic papers explicitly using "technology sovereignty" term. May define differently than our usage.',
                'expected_instances': 'Explicit definitions and framings to compare against; policy context',
                'specific_sections': 'Definition section, Policy recommendations',
                'search_patterns_to_use': '[1, 2]',
                'processing_status': 'queued',
                'processing_results': None,
                'extracted_instance_ids': None,
                'priority': 5,
                'source_type': 'user_input',
                'created_at': datetime.now().isoformat(),
                'queued_at': datetime.now().isoformat(),
                'processed_at': None
            }
        ]
    }

    # ==========================================================================
    # TABLE 9: concept_foundational_claims - Core assertions that define the concept
    # ==========================================================================
    tables['concept_foundational_claims'] = {
        'description': """
CONCEPT FOUNDATIONAL CLAIMS - Core Assertions That Define the Concept

For novel concepts, we need to capture the CLAIMS being made about reality.
These are not just definitions but assertions about how the world works.

Philosophy: Brandom's inferentialism - concepts are defined by inferential
role, i.e., what follows from applying them and what they follow from.

Wizard Questions:
- "What must be TRUE for this concept to be useful/valid?"
- "What are you CLAIMING about reality when you use this concept?"
- "What would have to be FALSE for this concept to be useless?"
""",
        'columns': [
            'id',
            'concept_id',
            'claim_type',            # ontological, causal, normative, methodological
            'claim_statement',       # The claim itself
            'claim_priority',        # How central is this claim (1-5)
            'if_false_consequence',  # What happens to concept if this is false
            'supporting_evidence',   # What supports this claim
            'potential_challenges',  # What might challenge this claim
            'related_claims',        # Other claims this connects to (JSON array of IDs)
            'testability_notes',     # How could this claim be tested
            'source_type',
            'source_reference',
            'confidence',
            'created_at'
        ],
        'data': [
            {
                'id': 1,
                'concept_id': 1,
                'claim_type': 'ontological',
                'claim_statement': 'Technological dependencies can constitute a form of sovereignty loss distinct from and not reducible to economic, political, or military dependencies.',
                'claim_priority': 5,
                'if_false_consequence': 'The concept collapses into existing categories (economic dependency, security threat); no need for new concept',
                'supporting_evidence': 'Cases where technological lock-in constrains decision-making even absent economic pressure or military threat (e.g., equipment standards path dependency)',
                'potential_challenges': 'Reductionist argument that tech dependency is always ultimately economic or security-based',
                'related_claims': '[2, 3]',
                'testability_notes': 'Find cases where tech dependency constrains without economic or security pressure; if none exist, claim is false',
                'source_type': 'user_input',
                'source_reference': 'Foundational claims wizard section',
                'confidence': 0.85,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 2,
                'concept_id': 1,
                'claim_type': 'causal',
                'claim_statement': 'Technological dependencies, once established, create path dependencies that constrain future choices in ways that are difficult to reverse.',
                'claim_priority': 4,
                'if_false_consequence': 'Tech dependencies become merely temporary inconveniences, not structural sovereignty concerns',
                'supporting_evidence': 'Infrastructure lock-in effects, network effects, training/skill dependencies, data format lock-in',
                'potential_challenges': 'Examples of successful technological transitions despite deep dependencies',
                'related_claims': '[1, 4]',
                'testability_notes': 'Measure how long and costly it is to exit deep technological dependencies; if exits are easy, claim is false',
                'source_type': 'user_input',
                'source_reference': 'Foundational claims wizard section',
                'confidence': 0.9,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 3,
                'concept_id': 1,
                'claim_type': 'normative',
                'claim_statement': 'Maintaining some threshold of technological sovereignty is a legitimate political goal for any polity that values self-determination.',
                'claim_priority': 4,
                'if_false_consequence': 'Concept loses normative force; becomes merely descriptive without action implications',
                'supporting_evidence': 'Arguments from democratic self-determination, precedents in other sovereignty domains',
                'potential_challenges': 'Cosmopolitan arguments against sovereignty as value; efficiency arguments for interdependence',
                'related_claims': '[1]',
                'testability_notes': 'Normative claims cannot be empirically tested but can be evaluated for coherence and implications',
                'source_type': 'user_input',
                'source_reference': 'Foundational claims wizard section',
                'confidence': 0.75,
                'created_at': datetime.now().isoformat()
            }
        ]
    }

    # ==========================================================================
    # TABLE 10: wizard_question_bank - All questions for concept setup wizard
    # ==========================================================================
    tables['wizard_question_bank'] = {
        'description': """
WIZARD QUESTION BANK - All Questions for Concept Setup Wizard

This table defines the questions used in the concept setup wizard.
Questions are organized by stage and can branch based on previous answers.

Design Principle (prn_staged_adaptive_interrogation): Questions adapt based
on previous answers. Early answers determine which later questions appear.

Design Principle (prn_precision_forcing_interrogation): Questions are
designed to force precision, not accept vague answers.

Question Types:
- multiple_choice: Select one from options (can include "Other")
- multi_select: Select multiple from options
- open_ended: Free text response
- scale: Numeric scale (e.g., 1-5 confidence)
- ranking: Order items by preference
- conditional: Only appears based on previous answers
""",
        'columns': [
            'id',
            'stage',                 # Which wizard stage (1-N)
            'question_id',           # Unique identifier
            'question_text',
            'question_type',
            'question_rationale',    # Why this question matters
            'options',               # For MC/multi-select (JSON)
            'scale_labels',          # For scale questions (JSON)
            'validation_rules',      # Requirements for valid answer (JSON)
            'min_length',            # For open-ended, minimum characters
            'max_length',            # For open-ended, maximum characters
            'depends_on',            # Question ID this depends on (JSON)
            'condition',             # Condition for showing (JSON)
            'help_text',             # Explanation shown to user
            'example_answer',        # Example of a good answer
            'follow_up_question_id', # Next question based on answer (JSON mapping)
            'populates_table',       # Which table this answer populates
            'populates_column',      # Which column this answer populates
            'is_required',
            'order_in_stage'
        ],
        'data': [
            {
                'id': 1,
                'stage': 1,
                'question_id': 'genesis_type',
                'question_text': 'How would you characterize the origin of this concept?',
                'question_type': 'multiple_choice',
                'question_rationale': 'Understanding origin type shapes how we approach validation and development',
                'options': '[{"value": "theoretical_innovation", "label": "A new theoretical framework or lens", "description": "You are proposing a new way of understanding something"}, {"value": "empirical_discovery", "label": "A pattern discovered through observation", "description": "You noticed something in the world that needs naming"}, {"value": "synthetic_unification", "label": "A synthesis of previously separate ideas", "description": "You are combining existing concepts in a new way"}, {"value": "paradigm_shift", "label": "A fundamental reconceptualization", "description": "You are challenging basic assumptions in a field"}, {"value": "other", "label": "Other (please elaborate)", "description": "None of the above quite fits"}]',
                'scale_labels': None,
                'validation_rules': '{"required": true}',
                'min_length': None,
                'max_length': None,
                'depends_on': None,
                'condition': None,
                'help_text': 'This helps us understand what kind of support and validation your concept needs.',
                'example_answer': None,
                'follow_up_question_id': '{"other": "genesis_type_elaborate"}',
                'populates_table': 'concept_genesis',
                'populates_column': 'genesis_type',
                'is_required': True,
                'order_in_stage': 1
            },
            {
                'id': 2,
                'stage': 1,
                'question_id': 'concept_name',
                'question_text': 'What is the name of your concept?',
                'question_type': 'open_ended',
                'question_rationale': 'The name is often loaded with meaning and sets expectations',
                'options': None,
                'scale_labels': None,
                'validation_rules': '{"required": true, "minLength": 2, "maxLength": 100}',
                'min_length': 2,
                'max_length': 100,
                'depends_on': None,
                'condition': None,
                'help_text': 'Choose a name that captures the essence while being distinct from existing terms.',
                'example_answer': 'Technological Sovereignty',
                'follow_up_question_id': None,
                'populates_table': 'concepts',
                'populates_column': 'name',
                'is_required': True,
                'order_in_stage': 2
            },
            {
                'id': 3,
                'stage': 1,
                'question_id': 'core_definition',
                'question_text': 'In one paragraph, provide your working definition of this concept.',
                'question_type': 'open_ended',
                'question_rationale': 'Forces initial precision; becomes anchor for later refinement',
                'options': None,
                'scale_labels': None,
                'validation_rules': '{"required": true, "minLength": 100, "maxLength": 1500}',
                'min_length': 100,
                'max_length': 1500,
                'depends_on': None,
                'condition': None,
                'help_text': 'This doesn\'t need to be perfect. We\'ll refine it throughout the process. Aim for clarity over comprehensiveness.',
                'example_answer': 'Technological sovereignty refers to the capacity of a political entity to exercise meaningful control over the technological systems upon which its economy, security, and social functioning depend...',
                'follow_up_question_id': None,
                'populates_table': 'concepts',
                'populates_column': 'definition',
                'is_required': True,
                'order_in_stage': 3
            },
            {
                'id': 4,
                'stage': 2,
                'question_id': 'problem_space',
                'question_text': 'What problem or gap in understanding does this concept address? Why do we need a new concept for this?',
                'question_type': 'open_ended',
                'question_rationale': 'Justifies concept\'s existence; clarifies its purpose',
                'options': None,
                'scale_labels': None,
                'validation_rules': '{"required": true, "minLength": 150, "maxLength": 2000}',
                'min_length': 150,
                'max_length': 2000,
                'depends_on': None,
                'condition': None,
                'help_text': 'A concept needs to DO something. What can we understand, explain, or do with this concept that we couldn\'t before?',
                'example_answer': 'Existing concepts like "digital sovereignty" or "economic nationalism" fail to capture the specific way that technological dependencies create structural constraints on political autonomy...',
                'follow_up_question_id': None,
                'populates_table': 'concept_problem_space',
                'populates_column': 'gap_description',
                'is_required': True,
                'order_in_stage': 1
            },
            {
                'id': 5,
                'stage': 2,
                'question_id': 'failed_alternatives',
                'question_text': 'What existing concepts have you tried using for this phenomenon? Why are they inadequate?',
                'question_type': 'open_ended',
                'question_rationale': 'Forces confrontation with existing vocabulary; strengthens differentiation',
                'options': None,
                'scale_labels': None,
                'validation_rules': '{"required": true, "minLength": 100, "maxLength": 1500}',
                'min_length': 100,
                'max_length': 1500,
                'depends_on': None,
                'condition': None,
                'help_text': 'List at least 2-3 existing concepts you considered and explain why each falls short.',
                'example_answer': 'Digital sovereignty: too narrow, focused on data/software. National security: too broad, loses technological specificity. Economic dependency: misses the epistemic and capability dimensions...',
                'follow_up_question_id': None,
                'populates_table': 'concept_problem_space',
                'populates_column': 'failed_alternatives',
                'is_required': True,
                'order_in_stage': 2
            },
            {
                'id': 6,
                'stage': 3,
                'question_id': 'most_confused_with',
                'question_text': 'What existing concept is this MOST likely to be confused with?',
                'question_type': 'open_ended',
                'question_rationale': 'Identifies primary differentiation target',
                'options': None,
                'scale_labels': None,
                'validation_rules': '{"required": true, "minLength": 50, "maxLength": 500}',
                'min_length': 50,
                'max_length': 500,
                'depends_on': None,
                'condition': None,
                'help_text': 'Pick ONE concept that poses the greatest confusion risk.',
                'example_answer': 'Digital sovereignty',
                'follow_up_question_id': None,
                'populates_table': 'concept_differentiation',
                'populates_column': 'confused_with',
                'is_required': True,
                'order_in_stage': 1
            },
            {
                'id': 7,
                'stage': 3,
                'question_id': 'confusion_consequence',
                'question_text': 'Why is this confusion problematic? What understanding is lost if someone treats your concept as equivalent to [previous answer]?',
                'question_type': 'open_ended',
                'question_rationale': 'Makes differentiation concrete and consequential',
                'options': None,
                'scale_labels': None,
                'validation_rules': '{"required": true, "minLength": 100, "maxLength": 1000}',
                'min_length': 100,
                'max_length': 1000,
                'depends_on': 'most_confused_with',
                'condition': '{"answered": true}',
                'help_text': 'Be specific about what analysis, insight, or action would be missed.',
                'example_answer': 'If technological sovereignty is reduced to digital sovereignty, we miss the material dimension: semiconductor manufacturing, rare earth supply chains, physical infrastructure dependencies...',
                'follow_up_question_id': None,
                'populates_table': 'concept_differentiation',
                'populates_column': 'what_would_be_lost',
                'is_required': True,
                'order_in_stage': 2
            },
            {
                'id': 8,
                'stage': 4,
                'question_id': 'paradigmatic_case',
                'question_text': 'What is the single best example that captures the essence of this concept? Describe it in detail.',
                'question_type': 'open_ended',
                'question_rationale': 'Paradigmatic cases are crucial for concept teaching and recognition',
                'options': None,
                'scale_labels': None,
                'validation_rules': '{"required": true, "minLength": 200, "maxLength": 2000}',
                'min_length': 200,
                'max_length': 2000,
                'depends_on': None,
                'condition': None,
                'help_text': 'Think: if you had to explain this concept to someone new and could only use ONE example, what would it be?',
                'example_answer': 'The European 5G and Huawei dilemma. European nations faced decisions about allowing Huawei equipment in their 5G networks...',
                'follow_up_question_id': None,
                'populates_table': 'concept_paradigmatic_cases',
                'populates_column': 'full_description',
                'is_required': True,
                'order_in_stage': 1
            },
            {
                'id': 9,
                'stage': 4,
                'question_id': 'implicit_domain',
                'question_text': 'In what domain do you see this concept operating WITHOUT being explicitly named? What proxy terms or euphemisms are used instead?',
                'question_type': 'open_ended',
                'question_rationale': 'Essential for document search and implicit instance discovery',
                'options': None,
                'scale_labels': None,
                'validation_rules': '{"required": true, "minLength": 150, "maxLength": 1500}',
                'min_length': 150,
                'max_length': 1500,
                'depends_on': None,
                'condition': None,
                'help_text': 'Where do people discuss this phenomenon without having the vocabulary? What words do they use instead?',
                'example_answer': 'Semiconductor policy: discussions of "supply chain security," "strategic autonomy," "onshoring," "friend-shoring" all circle around technological sovereignty without naming it...',
                'follow_up_question_id': None,
                'populates_table': 'concept_implicit_domains',
                'populates_column': 'manifestation_pattern',
                'is_required': True,
                'order_in_stage': 2
            },
            {
                'id': 10,
                'stage': 5,
                'question_id': 'core_claim',
                'question_text': 'What is the most fundamental claim about reality that your concept makes? What must be TRUE for this concept to be meaningful?',
                'question_type': 'open_ended',
                'question_rationale': 'Forces articulation of core commitment; enables testing',
                'options': None,
                'scale_labels': None,
                'validation_rules': '{"required": true, "minLength": 100, "maxLength": 1000}',
                'min_length': 100,
                'max_length': 1000,
                'depends_on': None,
                'condition': None,
                'help_text': 'A concept makes claims about how the world works. What\'s yours?',
                'example_answer': 'Technological dependencies can constitute a form of sovereignty loss that is distinct from and not reducible to economic, political, or military dependencies.',
                'follow_up_question_id': None,
                'populates_table': 'concept_foundational_claims',
                'populates_column': 'claim_statement',
                'is_required': True,
                'order_in_stage': 1
            },
            {
                'id': 11,
                'stage': 5,
                'question_id': 'falsification_condition',
                'question_text': 'What would prove this concept useless or wrong? What would have to be true for you to abandon it?',
                'question_type': 'open_ended',
                'question_rationale': 'Forces intellectual honesty; enables refutation',
                'options': None,
                'scale_labels': None,
                'validation_rules': '{"required": true, "minLength": 100, "maxLength": 1000}',
                'min_length': 100,
                'max_length': 1000,
                'depends_on': None,
                'condition': None,
                'help_text': 'Be honest about what would make you give up this concept. A concept that can\'t be wrong isn\'t saying anything.',
                'example_answer': 'If every case of apparent technological sovereignty loss could be fully explained by economic incentives or security threats without remainder, the concept adds nothing new...',
                'follow_up_question_id': None,
                'populates_table': 'concept_foundational_claims',
                'populates_column': 'if_false_consequence',
                'is_required': True,
                'order_in_stage': 2
            },
            {
                'id': 12,
                'stage': 6,
                'question_id': 'recognition_pattern',
                'question_text': 'How can we recognize an implicit instance of this concept in a text that doesn\'t use the term? What patterns should we look for?',
                'question_type': 'open_ended',
                'question_rationale': 'Essential for LLM-assisted document analysis',
                'options': None,
                'scale_labels': None,
                'validation_rules': '{"required": true, "minLength": 150, "maxLength": 1500}',
                'min_length': 150,
                'max_length': 1500,
                'depends_on': None,
                'condition': None,
                'help_text': 'Describe linguistic patterns, argument structures, or situational descriptions that indicate this concept is in play.',
                'example_answer': 'Look for: arguments that technology choices have political/sovereignty implications beyond economics; descriptions of lock-in that constrains strategic options; crisis revelations of hidden dependencies...',
                'follow_up_question_id': None,
                'populates_table': 'concept_recognition_markers',
                'populates_column': 'marker_description',
                'is_required': True,
                'order_in_stage': 1
            }
        ]
    }

    return tables


def generate_excel():
    """Generate Excel file with Genesis dimension schema."""

    tables = create_genesis_tables()

    output_path = os.path.join(OUTPUT_DIR, "Genesis_Dimension_Schema.xlsx")

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:

        # Overview sheet
        overview_data = {
            'Genesis Dimension Schema': [
                '',
                'PURPOSE: Schema extension for novel concept creation',
                '',
                'This dimension enables setup of concepts that:',
                '- Do not exist in public discourse yet',
                '- Are implied/operational in various domains without being named',
                '- Cannot be found by LLMs in their training data',
                '- Require structured knowledge elicitation from users',
                '',
                'PHILOSOPHICAL FOUNDATIONS:',
                '- Bachelard: Epistemic rupture - new concepts break with old',
                '- Canguilhem: Normativity - concepts address vital problems',
                '- Hacking: Making up people - categories create what they name',
                '- Blumenberg: Metaphorology - concepts operate through metaphors before explicit naming',
                '- Sellars: Contrast classes - meaning through systematic differentiation',
                '- Brandom: Inferentialism - concepts defined by inferential role',
                '',
                'DESIGN PRINCIPLES (from tool-ideator):',
                '- Staged adaptive interrogation: Questions build on previous answers',
                '- Proactive insufficiency signaling: LLM signals when data is lacking',
                '- Precision-forcing interrogation: Questions force definitional precision',
                '- Forward-staged data harvesting: Capture data for later processing',
                '- Document staging without processing: Register sources for targeted extraction',
                '',
                'TABLES IN THIS SCHEMA:',
            ]
        }

        # Add table list
        for table_name in tables.keys():
            overview_data['Genesis Dimension Schema'].append(f'  - {table_name}')

        overview_data['Genesis Dimension Schema'].extend([
            '',
            'WORKFLOW:',
            '1. User enters concept via setup wizard (questions from wizard_question_bank)',
            '2. Responses stored in concept_user_elaborations',
            '3. Responses auto-populate other tables',
            '4. User points to source documents (concept_source_pointers)',
            '5. LLM searches documents using recognition markers',
            '6. Found instances populate remaining schema tables',
            '7. LLM signals gaps via proactive insufficiency signaling',
            '8. Iterate until schema adequately populated',
        ])

        overview_df = pd.DataFrame(overview_data)
        overview_df.to_excel(writer, sheet_name='Overview', index=False)

        # Each table gets its own sheet
        for table_name, table_info in tables.items():
            # Description rows
            desc_lines = [line.strip() for line in table_info['description'].strip().split('\n') if line.strip()]

            # Column headers
            columns = table_info['columns']

            # Data
            data = table_info['data']

            # Create combined dataframe
            rows = []

            # Add description
            for line in desc_lines:
                row = {col: '' for col in columns}
                row[columns[0]] = line
                rows.append(row)

            # Add empty separator
            rows.append({col: '' for col in columns})

            # Add header row indicator
            header_indicator = {col: '--- COLUMN ---' for col in columns}
            header_indicator[columns[0]] = '=== DATA BELOW ==='
            rows.append(header_indicator)

            # Add actual headers
            rows.append({col: col for col in columns})

            # Add data
            for record in data:
                row = {col: record.get(col, '') for col in columns}
                rows.append(row)

            df = pd.DataFrame(rows)
            df.to_excel(writer, sheet_name=table_name[:31], index=False, header=False)

    print(f"Generated: {output_path}")
    print(f"Tables: {len(tables)}")
    return output_path


def generate_sql_migration():
    """Generate SQL migration for Genesis dimension tables."""

    sql = """-- Genesis Dimension Schema Migration
-- Enables setup of novel concepts not in public discourse
-- Generated: {timestamp}

-- =============================================================================
-- TABLE: concept_genesis
-- Origin story and theoretical lineage of the concept
-- =============================================================================
CREATE TABLE IF NOT EXISTS concept_genesis (
    id SERIAL PRIMARY KEY,
    concept_id INTEGER NOT NULL REFERENCES concepts(id),

    genesis_type VARCHAR(50) NOT NULL,  -- theoretical_innovation, empirical_discovery, synthetic_unification, paradigm_shift
    originator_type VARCHAR(50),        -- individual, collective, institutional, emergent
    originator_description TEXT,

    theoretical_lineage TEXT,           -- What traditions it builds on
    break_from TEXT,                    -- What it's breaking from (Bachelardian rupture)
    break_rationale TEXT,

    first_articulation_context TEXT,
    initial_problem_space TEXT,

    claimed_novelty_type VARCHAR(50),   -- terminological, conceptual, paradigmatic, methodological
    novelty_justification TEXT,

    source_type VARCHAR(30) DEFAULT 'user_input',
    source_reference TEXT,
    confidence FLOAT DEFAULT 0.8,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_concept_genesis_concept ON concept_genesis(concept_id);

-- =============================================================================
-- TABLE: concept_problem_space
-- The gap this concept fills
-- =============================================================================
CREATE TABLE IF NOT EXISTS concept_problem_space (
    id SERIAL PRIMARY KEY,
    concept_id INTEGER NOT NULL REFERENCES concepts(id),

    gap_type VARCHAR(50) NOT NULL,      -- descriptive, explanatory, normative, practical, methodological
    gap_description TEXT NOT NULL,
    failed_alternatives TEXT,
    failure_diagnosis TEXT,

    problem_domains TEXT,               -- Where this gap is felt
    stakeholder_impact TEXT,
    urgency_rationale TEXT,

    source_type VARCHAR(30) DEFAULT 'user_input',
    source_reference TEXT,
    confidence FLOAT DEFAULT 0.8,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_concept_problem_space_concept ON concept_problem_space(concept_id);

-- =============================================================================
-- TABLE: concept_differentiation
-- What the concept is NOT (critical for novel concepts)
-- =============================================================================
CREATE TABLE IF NOT EXISTS concept_differentiation (
    id SERIAL PRIMARY KEY,
    concept_id INTEGER NOT NULL REFERENCES concepts(id),

    confused_with VARCHAR(200) NOT NULL,  -- What it might be mistaken for
    confusion_type VARCHAR(50),           -- synonym_collapse, subset_reduction, superset_expansion, false_opposition

    differentiation_axis TEXT,
    this_concept_position TEXT,
    other_concept_position TEXT,

    what_would_be_lost TEXT,
    surface_similarity TEXT,
    deep_difference TEXT,

    source_type VARCHAR(30) DEFAULT 'user_input',
    source_reference TEXT,
    confidence FLOAT DEFAULT 0.8,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_concept_differentiation_concept ON concept_differentiation(concept_id);

-- =============================================================================
-- TABLE: concept_implicit_domains
-- Where the concept operates without being named
-- =============================================================================
CREATE TABLE IF NOT EXISTS concept_implicit_domains (
    id SERIAL PRIMARY KEY,
    concept_id INTEGER NOT NULL REFERENCES concepts(id),

    domain_name VARCHAR(200) NOT NULL,
    domain_type VARCHAR(50),            -- academic, policy, industry, media, everyday

    manifestation_pattern TEXT,
    proxy_terms JSONB,                  -- Terms used instead
    proxy_term_limitations TEXT,

    domain_specific_form TEXT,
    key_actors TEXT,
    observable_tensions TEXT,

    document_types_to_search TEXT,
    search_patterns JSONB,              -- Keywords/patterns to find instances

    source_type VARCHAR(30) DEFAULT 'user_input',
    source_reference TEXT,
    confidence FLOAT DEFAULT 0.8,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_concept_implicit_domains_concept ON concept_implicit_domains(concept_id);

-- =============================================================================
-- TABLE: concept_recognition_markers
-- How to identify implicit instances
-- =============================================================================
CREATE TABLE IF NOT EXISTS concept_recognition_markers (
    id SERIAL PRIMARY KEY,
    concept_id INTEGER NOT NULL REFERENCES concepts(id),

    marker_type VARCHAR(50) NOT NULL,   -- linguistic, structural, behavioral, situational, argumentative
    marker_description TEXT NOT NULL,
    marker_pattern TEXT,                -- Regex or search pattern

    positive_indicator TEXT,
    negative_indicator TEXT,
    false_positive_risk TEXT,
    discrimination_guide TEXT,

    example_text TEXT,
    weight FLOAT DEFAULT 0.8,

    source_type VARCHAR(30) DEFAULT 'user_input',
    source_reference TEXT,
    confidence FLOAT DEFAULT 0.8,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_concept_recognition_markers_concept ON concept_recognition_markers(concept_id);

-- =============================================================================
-- TABLE: concept_paradigmatic_cases
-- Exemplary instances that define the concept
-- =============================================================================
CREATE TABLE IF NOT EXISTS concept_paradigmatic_cases (
    id SERIAL PRIMARY KEY,
    concept_id INTEGER NOT NULL REFERENCES concepts(id),

    case_name VARCHAR(200) NOT NULL,
    case_type VARCHAR(50),              -- historical, contemporary, hypothetical, composite
    full_description TEXT NOT NULL,

    why_paradigmatic TEXT,
    features_exhibited JSONB,           -- Which concept features it shows
    features_absent TEXT,               -- Limitations

    teaching_value TEXT,
    controversy_notes TEXT,
    source_documents TEXT,

    source_type VARCHAR(30) DEFAULT 'user_input',
    source_reference TEXT,
    confidence FLOAT DEFAULT 0.8,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_concept_paradigmatic_cases_concept ON concept_paradigmatic_cases(concept_id);

-- =============================================================================
-- TABLE: concept_user_elaborations
-- Raw Q&A responses from setup wizard
-- =============================================================================
CREATE TABLE IF NOT EXISTS concept_user_elaborations (
    id SERIAL PRIMARY KEY,
    concept_id INTEGER NOT NULL REFERENCES concepts(id),

    wizard_stage INTEGER NOT NULL,
    question_id VARCHAR(100) NOT NULL,
    question_text TEXT,
    question_type VARCHAR(50),          -- multiple_choice, open_ended, scale, ranking, multi_select

    options_presented JSONB,
    selected_options JSONB,
    open_response TEXT,

    confidence_self_report INTEGER,     -- 1-5
    elaboration_notes TEXT,
    time_spent_seconds INTEGER,
    revision_history JSONB,

    source_type VARCHAR(30) DEFAULT 'user_input',

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_concept_user_elaborations_concept ON concept_user_elaborations(concept_id);
CREATE INDEX idx_concept_user_elaborations_stage ON concept_user_elaborations(wizard_stage);

-- =============================================================================
-- TABLE: concept_source_pointers
-- Documents queued for implicit instance discovery
-- =============================================================================
CREATE TABLE IF NOT EXISTS concept_source_pointers (
    id SERIAL PRIMARY KEY,
    concept_id INTEGER NOT NULL REFERENCES concepts(id),

    document_type VARCHAR(50),          -- academic_paper, news_article, policy_document, book_chapter, interview, speech
    document_reference TEXT NOT NULL,
    document_title TEXT,
    document_author TEXT,
    document_date DATE,

    user_relevance_note TEXT,
    expected_instances TEXT,
    specific_sections TEXT,
    search_patterns_to_use JSONB,       -- IDs from recognition_markers

    processing_status VARCHAR(30) DEFAULT 'queued',  -- queued, processing, completed, failed
    processing_results JSONB,
    extracted_instance_ids JSONB,

    priority INTEGER DEFAULT 3,         -- 1-5

    source_type VARCHAR(30) DEFAULT 'user_input',

    created_at TIMESTAMPTZ DEFAULT NOW(),
    queued_at TIMESTAMPTZ DEFAULT NOW(),
    processed_at TIMESTAMPTZ
);

CREATE INDEX idx_concept_source_pointers_concept ON concept_source_pointers(concept_id);
CREATE INDEX idx_concept_source_pointers_status ON concept_source_pointers(processing_status);

-- =============================================================================
-- TABLE: concept_foundational_claims
-- Core assertions that define the concept
-- =============================================================================
CREATE TABLE IF NOT EXISTS concept_foundational_claims (
    id SERIAL PRIMARY KEY,
    concept_id INTEGER NOT NULL REFERENCES concepts(id),

    claim_type VARCHAR(50) NOT NULL,    -- ontological, causal, normative, methodological
    claim_statement TEXT NOT NULL,
    claim_priority INTEGER DEFAULT 3,   -- 1-5

    if_false_consequence TEXT,
    supporting_evidence TEXT,
    potential_challenges TEXT,
    related_claims JSONB,               -- Other claim IDs
    testability_notes TEXT,

    source_type VARCHAR(30) DEFAULT 'user_input',
    source_reference TEXT,
    confidence FLOAT DEFAULT 0.8,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_concept_foundational_claims_concept ON concept_foundational_claims(concept_id);

-- =============================================================================
-- TABLE: wizard_question_bank
-- All questions for concept setup wizard
-- =============================================================================
CREATE TABLE IF NOT EXISTS wizard_question_bank (
    id SERIAL PRIMARY KEY,

    stage INTEGER NOT NULL,
    question_id VARCHAR(100) NOT NULL UNIQUE,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL,

    question_rationale TEXT,
    options JSONB,                      -- For MC/multi-select
    scale_labels JSONB,                 -- For scale questions

    validation_rules JSONB,
    min_length INTEGER,
    max_length INTEGER,

    depends_on VARCHAR(100),            -- Question ID this depends on
    condition JSONB,                    -- Condition for showing

    help_text TEXT,
    example_answer TEXT,
    follow_up_question_id JSONB,        -- Branching

    populates_table VARCHAR(100),
    populates_column VARCHAR(100),

    is_required BOOLEAN DEFAULT true,
    order_in_stage INTEGER DEFAULT 1
);

CREATE INDEX idx_wizard_question_bank_stage ON wizard_question_bank(stage);
CREATE INDEX idx_wizard_question_bank_question_id ON wizard_question_bank(question_id);

-- =============================================================================
-- Populate initial wizard questions
-- =============================================================================
INSERT INTO wizard_question_bank (stage, question_id, question_text, question_type, question_rationale, options, validation_rules, min_length, max_length, help_text, example_answer, populates_table, populates_column, is_required, order_in_stage)
VALUES
(1, 'genesis_type', 'How would you characterize the origin of this concept?', 'multiple_choice',
 'Understanding origin type shapes how we approach validation and development',
 '[{{"value": "theoretical_innovation", "label": "A new theoretical framework or lens"}}, {{"value": "empirical_discovery", "label": "A pattern discovered through observation"}}, {{"value": "synthetic_unification", "label": "A synthesis of previously separate ideas"}}, {{"value": "paradigm_shift", "label": "A fundamental reconceptualization"}}, {{"value": "other", "label": "Other (please elaborate)"}}]'::jsonb,
 '{{"required": true}}'::jsonb, NULL, NULL,
 'This helps us understand what kind of support and validation your concept needs.',
 NULL, 'concept_genesis', 'genesis_type', true, 1),

(1, 'concept_name', 'What is the name of your concept?', 'open_ended',
 'The name sets expectations and should be distinct from existing terms',
 NULL, '{{"required": true, "minLength": 2, "maxLength": 100}}'::jsonb, 2, 100,
 'Choose a name that captures the essence while being distinct from existing terms.',
 'Technological Sovereignty', 'concepts', 'name', true, 2),

(1, 'core_definition', 'In one paragraph, provide your working definition of this concept.', 'open_ended',
 'Forces initial precision; becomes anchor for later refinement',
 NULL, '{{"required": true, "minLength": 100, "maxLength": 1500}}'::jsonb, 100, 1500,
 'This doesn''t need to be perfect. We''ll refine it throughout the process.',
 'Technological sovereignty refers to the capacity of a political entity to exercise meaningful control over the technological systems upon which its economy, security, and social functioning depend...',
 'concepts', 'definition', true, 3),

(2, 'problem_space', 'What problem or gap in understanding does this concept address? Why do we need a new concept for this?', 'open_ended',
 'Justifies concept''s existence; clarifies its purpose',
 NULL, '{{"required": true, "minLength": 150, "maxLength": 2000}}'::jsonb, 150, 2000,
 'A concept needs to DO something. What can we understand, explain, or do with this concept that we couldn''t before?',
 'Existing concepts like "digital sovereignty" fail to capture the specific way that technological dependencies create structural constraints on political autonomy...',
 'concept_problem_space', 'gap_description', true, 1),

(3, 'most_confused_with', 'What existing concept is this MOST likely to be confused with?', 'open_ended',
 'Identifies primary differentiation target',
 NULL, '{{"required": true, "minLength": 50, "maxLength": 500}}'::jsonb, 50, 500,
 'Pick ONE concept that poses the greatest confusion risk.',
 'Digital sovereignty',
 'concept_differentiation', 'confused_with', true, 1),

(4, 'paradigmatic_case', 'What is the single best example that captures the essence of this concept? Describe it in detail.', 'open_ended',
 'Paradigmatic cases are crucial for concept teaching and recognition',
 NULL, '{{"required": true, "minLength": 200, "maxLength": 2000}}'::jsonb, 200, 2000,
 'Think: if you had to explain this concept to someone new and could only use ONE example, what would it be?',
 'The European 5G and Huawei dilemma...',
 'concept_paradigmatic_cases', 'full_description', true, 1),

(5, 'core_claim', 'What is the most fundamental claim about reality that your concept makes? What must be TRUE for this concept to be meaningful?', 'open_ended',
 'Forces articulation of core commitment; enables testing',
 NULL, '{{"required": true, "minLength": 100, "maxLength": 1000}}'::jsonb, 100, 1000,
 'A concept makes claims about how the world works. What''s yours?',
 'Technological dependencies can constitute a form of sovereignty loss distinct from economic, political, or military dependencies.',
 'concept_foundational_claims', 'claim_statement', true, 1),

(6, 'recognition_pattern', 'How can we recognize an implicit instance of this concept in a text that doesn''t use the term? What patterns should we look for?', 'open_ended',
 'Essential for LLM-assisted document analysis',
 NULL, '{{"required": true, "minLength": 150, "maxLength": 1500}}'::jsonb, 150, 1500,
 'Describe linguistic patterns, argument structures, or situational descriptions that indicate this concept is in play.',
 'Look for: arguments that technology choices have political/sovereignty implications beyond economics...',
 'concept_recognition_markers', 'marker_description', true, 1);

COMMIT;
""".format(timestamp=datetime.now().isoformat())

    migration_path = os.path.join(OUTPUT_DIR, "genesis_dimension_migration.sql")
    with open(migration_path, 'w') as f:
        f.write(sql)

    print(f"Generated: {migration_path}")
    return migration_path


if __name__ == '__main__':
    print("=" * 60)
    print("GENESIS DIMENSION SCHEMA GENERATOR")
    print("For Novel Concept Creation")
    print("=" * 60)
    print()

    # Generate Excel
    excel_path = generate_excel()
    print()

    # Generate SQL migration
    sql_path = generate_sql_migration()
    print()

    print("=" * 60)
    print("NEXT STEPS:")
    print("1. Review Excel schema: Genesis_Dimension_Schema.xlsx")
    print("2. Run SQL migration: genesis_dimension_migration.sql")
    print("3. Implement wizard UI using wizard_question_bank")
    print("4. Implement document processing pipeline")
    print("=" * 60)
