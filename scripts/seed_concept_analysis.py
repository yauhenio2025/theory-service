"""
Seed script for Operation-Indexed Concept Analysis

Creates tables and populates with:
1. The 8 analytical dimensions
2. All 38 analytical operations
3. The 14 theoretical influences
4. Complete Tech Sovereignty analysis
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.concept_analysis_models import (
    Base, AnalyticalDimension, TheoreticalInfluence, AnalyticalOperation,
    AnalyzedConcept, ConceptAnalysis, AnalysisItem, ItemReasoningScaffold,
    DimensionType, OutputType, SourceType, WebCentrality, InferenceType,
    operation_influences
)

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/theory_db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)


# ==================== DIMENSION DATA ====================

DIMENSIONS = [
    {
        'dimension_type': DimensionType.POSITIONAL,
        'name': 'Positional Analysis',
        'core_question': 'Where does this concept SIT in various networks?',
        'description': "Analyzes the concept's position in belief webs, paradigms, and discursive formations. Maps its relational structure.",
        'color_scheme': '#E3F2FD',
        'sequence_order': 1,
    },
    {
        'dimension_type': DimensionType.GENEALOGICAL,
        'name': 'Genealogical Analysis',
        'core_question': 'Where does this concept COME FROM?',
        'description': 'Traces the historical emergence, conceptual predecessors, and conditions of possibility for the concept.',
        'color_scheme': '#FFF3E0',
        'sequence_order': 2,
    },
    {
        'dimension_type': DimensionType.PRESUPPOSITIONAL,
        'name': 'Presuppositional Analysis',
        'core_question': 'What does this concept TAKE FOR GRANTED?',
        'description': 'Excavates hidden assumptions, unexamined givens, and background commitments embedded in the concept.',
        'color_scheme': '#FCE4EC',
        'sequence_order': 3,
    },
    {
        'dimension_type': DimensionType.COMMITMENT,
        'name': 'Commitment Analysis',
        'core_question': 'What does accepting this concept COMMIT YOU TO?',
        'description': 'Maps the inferential, normative, and practical commitments that follow from adopting the concept.',
        'color_scheme': '#F3E5F5',
        'sequence_order': 4,
    },
    {
        'dimension_type': DimensionType.AFFORDANCE,
        'name': 'Affordance Analysis',
        'core_question': 'What does this concept ENABLE or BLOCK?',
        'description': 'Maps what becomes possible or impossible, visible or invisible, sayable or unsayable through this concept.',
        'color_scheme': '#E8F5E9',
        'sequence_order': 5,
    },
    {
        'dimension_type': DimensionType.NORMALIZATION,
        'name': 'Normalization Analysis',
        'core_question': 'What does this concept NORMALIZE or make invisible?',
        'description': 'Exposes the norms, power relations, and governmentality embedded in and enabled by the concept.',
        'color_scheme': '#FFEBEE',
        'sequence_order': 6,
    },
    {
        'dimension_type': DimensionType.BOUNDARY,
        'name': 'Boundary Analysis',
        'core_question': 'What are the LIMITS of this concept?',
        'description': "Maps anomalies, contradictions, incommensurabilities, and edge cases that test the concept's boundaries.",
        'color_scheme': '#E0F7FA',
        'sequence_order': 7,
    },
    {
        'dimension_type': DimensionType.DYNAMIC,
        'name': 'Dynamic Analysis',
        'core_question': 'How does this concept CHANGE over time?',
        'description': 'Analyzes how the concept evolves, creates feedback loops, and shapes its own conditions.',
        'color_scheme': '#FFF8E1',
        'sequence_order': 8,
    },
]


# ==================== THEORETICAL INFLUENCES ====================

INFLUENCES = [
    {
        'short_name': 'Quine',
        'full_name': 'Willard Van Orman Quine',
        'years': '1908-2000',
        'key_works': ['Two Dogmas of Empiricism (1951)', 'Word and Object (1960)'],
        'core_insight': 'Beliefs face evidence as a corporate body; no belief is immune to revision; knowledge forms an interconnected web.',
    },
    {
        'short_name': 'Kuhn',
        'full_name': 'Thomas Kuhn',
        'years': '1922-1996',
        'key_works': ['The Structure of Scientific Revolutions (1962)'],
        'core_insight': 'Science operates within paradigms; normal science solves puzzles within paradigms; anomalies accumulate until paradigm shifts occur.',
    },
    {
        'short_name': 'Foucault',
        'full_name': 'Michel Foucault',
        'years': '1926-1984',
        'key_works': ['Discipline and Punish (1975)', 'History of Sexuality Vol. 1 (1976)', 'The Archaeology of Knowledge (1969)'],
        'core_insight': 'Knowledge and power are intertwined; discourse determines what can be said; concepts make phenomena governable.',
    },
    {
        'short_name': 'Sellars',
        'full_name': 'Wilfrid Sellars',
        'years': '1912-1989',
        'key_works': ['Empiricism and the Philosophy of Mind (1956)'],
        'core_insight': 'Nothing is epistemically "given"; all knowledge requires conceptual mediation; the manifest and scientific images may conflict.',
    },
    {
        'short_name': 'Brandom',
        'full_name': 'Robert Brandom',
        'years': '1950-',
        'key_works': ['Making It Explicit (1994)', 'Articulating Reasons (2000)'],
        'core_insight': 'Concepts are defined by their inferential role; assertion involves undertaking commitments and entitlements.',
    },
    {
        'short_name': 'Deleuze',
        'full_name': 'Gilles Deleuze',
        'years': '1925-1995',
        'key_works': ['Difference and Repetition (1968)', 'A Thousand Plateaus (1980, with Guattari)'],
        'core_insight': 'Concepts enable transformation and becoming; philosophy creates concepts that open new possibilities.',
    },
    {
        'short_name': 'Bachelard',
        'full_name': 'Gaston Bachelard',
        'years': '1884-1962',
        'key_works': ['The Formation of the Scientific Mind (1938)', 'The Philosophy of No (1940)'],
        'core_insight': 'Scientific progress involves epistemological ruptures; prior concepts can become obstacles to knowledge.',
    },
    {
        'short_name': 'Blumenberg',
        'full_name': 'Hans Blumenberg',
        'years': '1920-1996',
        'key_works': ['Paradigms for a Metaphorology (1960)', 'The Legitimacy of the Modern Age (1966)'],
        'core_insight': 'Absolute metaphors structure thought before explicit concepts; they reveal and conceal simultaneously.',
    },
    {
        'short_name': 'Carey',
        'full_name': 'Susan Carey',
        'years': '1942-',
        'key_works': ['The Origin of Concepts (2009)', 'Conceptual Change in Childhood (1985)'],
        'core_insight': 'Complex concepts bootstrap from simpler ones through developmental processes; conceptual change can be revolutionary.',
    },
    {
        'short_name': 'Canguilhem',
        'full_name': 'Georges Canguilhem',
        'years': '1904-1995',
        'key_works': ['The Normal and the Pathological (1943/1966)'],
        'core_insight': 'Norms are not discovered but created; the normal/pathological distinction is value-laden and historically contingent.',
    },
    {
        'short_name': 'Hacking',
        'full_name': 'Ian Hacking',
        'years': '1936-2023',
        'key_works': ['The Social Construction of What? (1999)', 'Historical Ontology (2002)'],
        'core_insight': 'Classification of people creates "looping effects"; interactive kinds change because they are classified.',
    },
    {
        'short_name': 'James',
        'full_name': 'William James',
        'years': '1842-1910',
        'key_works': ['Pragmatism (1907)', 'The Meaning of Truth (1909)'],
        'core_insight': 'The meaning of a concept lies in its practical consequences; truth is what works.',
    },
    {
        'short_name': 'Dewey',
        'full_name': 'John Dewey',
        'years': '1859-1952',
        'key_works': ['Experience and Nature (1925)', 'Logic: The Theory of Inquiry (1938)'],
        'core_insight': 'Inquiry is problem-solving; concepts are tools; habits structure thought and action.',
    },
    {
        'short_name': 'Rorty',
        'full_name': 'Richard Rorty',
        'years': '1931-2007',
        'key_works': ['Philosophy and the Mirror of Nature (1979)', 'Contingency, Irony, and Solidarity (1989)'],
        'core_insight': 'Progress comes through vocabulary change; new ways of speaking open new possibilities.',
    },
]


# ==================== OPERATIONS BY DIMENSION ====================

OPERATIONS = {
    DimensionType.POSITIONAL: [
        {
            'name': 'Inferential Mapping',
            'description': 'What follows from this concept? What contradicts it? What does it connect to?',
            'output_type': OutputType.INFERENCE_MAP,
            'influences': ['Quine'],
            'key_questions': [
                'What beliefs must you hold if you accept this concept?',
                'What does accepting this concept rule out?',
                'What lateral connections does it have to adjacent concepts?'
            ],
        },
        {
            'name': 'Paradigm Positioning',
            'description': 'Which paradigm does this belong to? Is it normal science or revolutionary?',
            'output_type': OutputType.PARADIGM_ASSESSMENT,
            'influences': ['Kuhn'],
            'key_questions': [
                'What paradigm does this concept operate within?',
                'What are the exemplary instances?',
                'Is this concept extending or challenging the paradigm?'
            ],
        },
        {
            'name': 'Discursive Positioning',
            'description': 'What statements does this concept make possible or impossible?',
            'output_type': OutputType.DISCOURSE_MAP,
            'influences': ['Foucault'],
            'key_questions': [
                "What can be said using this concept that couldn't be said before?",
                'What statements does it foreclose?',
                'What subject positions does it create?'
            ],
        },
        {
            'name': 'Web Centrality Assessment',
            'description': 'How central or peripheral is this concept? What is the cost of revision?',
            'output_type': OutputType.CENTRALITY_SCORE,
            'influences': ['Quine'],
            'key_questions': [
                'How many other beliefs depend on this concept?',
                'What would have to change if this concept were abandoned?',
                'Is this core or peripheral to your framework?'
            ],
        },
    ],
    DimensionType.GENEALOGICAL: [
        {
            'name': 'Conceptual Bootstrapping',
            'description': 'What simpler concepts combine to produce this more complex one?',
            'output_type': OutputType.BOOTSTRAP_TREE,
            'influences': ['Carey'],
            'key_questions': [
                'What simpler concepts is this built from?',
                'What emergent properties arise from their combination?',
                'What conceptual development was required?'
            ],
        },
        {
            'name': 'Historical Emergence',
            'description': 'What historical/discursive conditions made this concept possible?',
            'output_type': OutputType.EMERGENCE_NARRATIVE,
            'influences': ['Foucault'],
            'key_questions': [
                'What had to be in place for this concept to emerge?',
                'What historical moment does it belong to?',
                'What institutions or practices enabled it?'
            ],
        },
        {
            'name': 'Rupture Detection',
            'description': 'Does this concept mark an epistemological break? What does it break from?',
            'output_type': OutputType.RUPTURE_ASSESSMENT,
            'influences': ['Bachelard'],
            'key_questions': [
                'Does this concept represent a break from previous thinking?',
                'What older concept or framework does it supersede?',
                'What made the break possible or necessary?'
            ],
        },
        {
            'name': 'Metaphorical Archaeology',
            'description': 'What root metaphors structure this concept? What do they reveal/conceal?',
            'output_type': OutputType.METAPHOR_ANALYSIS,
            'influences': ['Blumenberg'],
            'key_questions': [
                'What is the governing metaphor?',
                'What does this metaphor make visible?',
                'What does it hide or distort?'
            ],
        },
        {
            'name': 'Predecessor Mapping',
            'description': 'What concepts did this replace or displace?',
            'output_type': OutputType.PREDECESSOR_LIST,
            'influences': ['Foucault', 'Bachelard'],
            'key_questions': [
                'What was being said before this concept existed?',
                'What concepts did it make obsolete?',
                'What problems did predecessors fail to solve?'
            ],
        },
    ],
    DimensionType.PRESUPPOSITIONAL: [
        {
            'name': 'Givenness Detection',
            'description': 'What does this concept treat as self-evident that actually requires justification?',
            'output_type': OutputType.GIVENNESS_LIST,
            'influences': ['Sellars'],
            'key_questions': [
                'What does this concept treat as obvious?',
                'What would someone demand justification for?',
                'What epistemic work is being smuggled in?'
            ],
        },
        {
            'name': 'Assumption Excavation',
            'description': 'What hidden background beliefs are required for this concept to work?',
            'output_type': OutputType.ASSUMPTION_INVENTORY,
            'influences': ['Sellars'],
            'key_questions': [
                'What must be true for this concept to make sense?',
                'What worldview does it presuppose?',
                'What empirical claims does it smuggle in?'
            ],
        },
        {
            'name': 'Obstacle Detection',
            'description': 'Does this concept itself block understanding of something deeper?',
            'output_type': OutputType.OBSTACLE_ASSESSMENT,
            'influences': ['Bachelard'],
            'key_questions': [
                'Does using this concept prevent seeing something important?',
                'What epistemological obstacles does it create?',
                'What would you understand better without it?'
            ],
        },
        {
            'name': 'Manifest/Scientific Tension',
            'description': 'Is there tension between everyday and theoretical understandings?',
            'output_type': OutputType.TENSION_ANALYSIS,
            'influences': ['Sellars'],
            'key_questions': [
                'How does common sense view this differently from theory?',
                'What folk concepts does this technical concept challenge?',
                'Where do intuitions mislead?'
            ],
        },
    ],
    DimensionType.COMMITMENT: [
        {
            'name': 'Inferential Commitment Mapping',
            'description': 'What other beliefs must you accept if you accept this?',
            'output_type': OutputType.COMMITMENT_LIST,
            'influences': ['Brandom'],
            'key_questions': [
                'If you assert this, what else must you be prepared to assert?',
                'What claims become unjustifiable if you hold this?',
                'What inferential moves does this license?'
            ],
        },
        {
            'name': 'Normative Entailment Tracking',
            'description': 'What values, norms, or obligations follow from this concept?',
            'output_type': OutputType.NORMATIVE_ENTAILMENTS,
            'influences': ['Brandom'],
            'key_questions': [
                'What should you value if you accept this concept?',
                'What actions become obligatory or forbidden?',
                'What normative stance does it encode?'
            ],
        },
        {
            'name': 'Incompatibility Detection',
            'description': 'What concepts or positions are materially incompatible with this one?',
            'output_type': OutputType.INCOMPATIBILITY_MAP,
            'influences': ['Brandom', 'Quine'],
            'key_questions': [
                'What can you NOT believe if you believe this?',
                'What positions does this rule out?',
                'Where are the hard incompatibilities vs. soft tensions?'
            ],
        },
        {
            'name': 'Entitlement Tracking',
            'description': 'What are you ENTITLED to claim if you accept this concept?',
            'output_type': OutputType.ENTITLEMENT_LIST,
            'influences': ['Brandom'],
            'key_questions': [
                'What further claims does this justify?',
                'What moves in the space of reasons does it enable?',
                'What authority does it confer?'
            ],
        },
    ],
    DimensionType.AFFORDANCE: [
        {
            'name': 'Transformation Mapping',
            'description': 'What changes, becomings, or movements does this concept enable?',
            'output_type': OutputType.TRANSFORMATION_VECTORS,
            'influences': ['Deleuze'],
            'key_questions': [
                'What transformations does this concept make thinkable?',
                'What lines of flight does it open?',
                'What becomings does it enable?'
            ],
        },
        {
            'name': 'Practical Effect Tracking',
            'description': 'What actions, interventions, or practices does this enable?',
            'output_type': OutputType.PRACTICAL_EFFECTS,
            'influences': ['James', 'Dewey'],
            'key_questions': [
                'What can you DO with this concept?',
                'What practical difference does it make?',
                'What interventions does it enable?'
            ],
        },
        {
            'name': 'Visibility Mapping',
            'description': 'What does this concept make visible vs. invisible?',
            'output_type': OutputType.VISIBILITY_MAP,
            'influences': ['Hacking', 'Foucault'],
            'key_questions': [
                'What phenomena does this concept bring into focus?',
                'What does it make harder to see?',
                'What does naming this create?'
            ],
        },
        {
            'name': 'Vocabulary Extension',
            'description': 'What new things can you SAY with this concept?',
            'output_type': OutputType.VOCABULARY_ADDITIONS,
            'influences': ['Rorty'],
            'key_questions': [
                'What conversations does this concept open?',
                'What was unsayable before this concept existed?',
                'What new descriptions does it enable?'
            ],
        },
        {
            'name': 'Inquiry Structuring',
            'description': 'How does this concept structure problem-solving and research?',
            'output_type': OutputType.INQUIRY_STRUCTURE,
            'influences': ['Dewey'],
            'key_questions': [
                'What does this concept make into a "problem"?',
                'What does it treat as "solved"?',
                'How does it organize inquiry?'
            ],
        },
    ],
    DimensionType.NORMALIZATION: [
        {
            'name': 'Norm Embedding Detection',
            'description': 'What norms are baked into this concept?',
            'output_type': OutputType.EMBEDDED_NORMS,
            'influences': ['Canguilhem'],
            'key_questions': [
                'What does this concept treat as normal/healthy/proper?',
                'What values are built into it?',
                'What standards does it encode?'
            ],
        },
        {
            'name': 'Pathological Boundary Mapping',
            'description': 'What does this concept mark as deviant, abnormal, or pathological?',
            'output_type': OutputType.PATHOLOGICAL_BOUNDARIES,
            'influences': ['Canguilhem'],
            'key_questions': [
                'What does this concept exclude as abnormal?',
                'What gets pathologized?',
                'Where is the normal/pathological boundary drawn?'
            ],
        },
        {
            'name': 'Power Relation Naturalization',
            'description': 'What power relations does this concept make seem natural or inevitable?',
            'output_type': OutputType.NATURALIZED_POWER,
            'influences': ['Foucault'],
            'key_questions': [
                'What power arrangements does this concept make invisible?',
                'Whose interests does it serve while appearing neutral?',
                'What domination does it naturalize?'
            ],
        },
        {
            'name': 'Authority Legitimization',
            'description': 'Whose expertise or authority does this concept validate?',
            'output_type': OutputType.AUTHORITY_MAP,
            'influences': ['Foucault'],
            'key_questions': [
                'Who gets to speak authoritatively about this?',
                'What credentials does it require?',
                'Whose knowledge counts?'
            ],
        },
        {
            'name': 'Governmentality Mapping',
            'description': 'What populations or phenomena does this concept make manageable?',
            'output_type': OutputType.GOVERNMENTALITY_ANALYSIS,
            'influences': ['Foucault'],
            'key_questions': [
                'What does this concept make governable?',
                'What techniques of management does it enable?',
                'How does it render things calculable?'
            ],
        },
        {
            'name': 'Truth Regime Analysis',
            'description': 'What counts as true within the framework this concept establishes?',
            'output_type': OutputType.TRUTH_REGIME,
            'influences': ['Foucault'],
            'key_questions': [
                'What counts as evidence within this framework?',
                'What would falsify claims made with this concept?',
                'Who arbitrates truth here?'
            ],
        },
    ],
    DimensionType.BOUNDARY: [
        {
            'name': 'Anomaly Detection',
            'description': 'What cases can this concept not handle?',
            'output_type': OutputType.ANOMALY_LIST,
            'influences': ['Kuhn'],
            'key_questions': [
                'What phenomena does this concept fail to explain?',
                'What are the stubborn counterexamples?',
                'Where does it break down?'
            ],
        },
        {
            'name': 'Contradiction Mapping',
            'description': 'What does this concept logically rule out?',
            'output_type': OutputType.CONTRADICTION_MAP,
            'influences': ['Quine', 'Brandom'],
            'key_questions': [
                'What is strictly incompatible with this concept?',
                'What would constitute a logical contradiction?',
                'Where are the hard boundaries?'
            ],
        },
        {
            'name': 'Incommensurability Analysis',
            'description': 'Can this concept be translated into rival frameworks?',
            'output_type': OutputType.INCOMMENSURABILITY_ASSESSMENT,
            'influences': ['Kuhn'],
            'key_questions': [
                'What rival frameworks exist?',
                'Can this concept be expressed in their terms?',
                'Where is translation impossible?'
            ],
        },
        {
            'name': 'Gray Zone Identification',
            'description': 'What are the boundary cases where application is uncertain?',
            'output_type': OutputType.GRAY_ZONES,
            'influences': ['Hacking'],
            'key_questions': [
                'What cases are neither clearly in nor out?',
                'Where do experts disagree about application?',
                'What makes boundary cases hard?'
            ],
        },
        {
            'name': 'Crisis Indicator Tracking',
            'description': 'What would force abandonment of this concept?',
            'output_type': OutputType.CRISIS_INDICATORS,
            'influences': ['Kuhn'],
            'key_questions': [
                'What accumulation of anomalies would be fatal?',
                'What discovery would make this concept untenable?',
                'How close are we to crisis?'
            ],
        },
    ],
    DimensionType.DYNAMIC: [
        {
            'name': 'Looping Effect Detection',
            'description': 'Does naming this change the thing named?',
            'output_type': OutputType.LOOPING_EFFECTS,
            'influences': ['Hacking'],
            'key_questions': [
                'Do the things classified by this concept change because of being classified?',
                'Is there awareness of being categorized?',
                'How does classification feed back?'
            ],
        },
        {
            'name': 'Habit Formation Tracking',
            'description': 'What habits of thought and practice does using this concept cultivate?',
            'output_type': OutputType.HABIT_INVENTORY,
            'influences': ['Dewey'],
            'key_questions': [
                'What ways of thinking does this concept train?',
                'What dispositions does repeated use create?',
                'What becomes automatic?'
            ],
        },
        {
            'name': 'Revision Condition Mapping',
            'description': 'Under what conditions would this concept need revision?',
            'output_type': OutputType.REVISION_CONDITIONS,
            'influences': ['Quine', 'Kuhn'],
            'key_questions': [
                'What new evidence would force modification?',
                'How revisable is this concept?',
                'What would a revised version look like?'
            ],
        },
        {
            'name': 'Kind-Making Analysis',
            'description': 'Does this concept create new categories of being?',
            'output_type': OutputType.KIND_CREATION,
            'influences': ['Hacking'],
            'key_questions': [
                'Does this concept bring a new kind of thing into existence?',
                "What didn't exist (as a kind) before this concept?",
                'Is this an interactive kind?'
            ],
        },
        {
            'name': 'Disciplinary Matrix Evolution',
            'description': 'How do shared practices around this concept shift over time?',
            'output_type': OutputType.MATRIX_EVOLUTION,
            'influences': ['Kuhn'],
            'key_questions': [
                'How has expert consensus shifted?',
                'What exemplars have changed?',
                'How has the community using this concept evolved?'
            ],
        },
    ],
}


# ==================== TECH SOVEREIGNTY ANALYSIS DATA ====================
# (Importing from the spreadsheet generator for consistency)

from scripts.generate_operation_indexed_spreadsheet import TECH_SOV_ANALYSIS


# ==================== QUINEAN REASONING SCAFFOLDS ====================
# Sample reasoning scaffolds for forward inferences in Inferential Mapping

REASONING_SCAFFOLDS = {
    # Key: (item_type, content_fragment) -> scaffold data
    ('forward_inferences', 'States should invest in domestic semiconductor manufacturing'): {
        'inference_type': InferenceType.MATERIAL,
        'inference_rule': 'material_implication',
        'premises': [
            {
                'claim': 'Technological sovereignty requires autonomous capacity for technology development',
                'claim_type': 'definitional',
                'centrality': 'core',
                'source': 'concept_definition'
            },
            {
                'claim': 'Semiconductors are foundational to all digital technology',
                'claim_type': 'empirical',
                'centrality': 'high',
                'source': 'domain_knowledge'
            },
            {
                'claim': 'Dependency on foreign semiconductor supply creates strategic vulnerability',
                'claim_type': 'empirical',
                'centrality': 'medium',
                'source': 'user_notes'
            }
        ],
        'reasoning_trace': 'Given the definitional link between sovereignty and autonomous capacity, combined with the empirical fact that semiconductors underpin all digital systems, it follows materially that states pursuing tech sovereignty must develop domestic chip manufacturing. The 2021-2023 chip shortage demonstrated the strategic vulnerability of import dependency.',
        'derivation_trigger': 'concept_definition',
        'source_passage': 'Technological sovereignty entails the capacity for indigenous technology development',
        'source_location': 'concept definition + domain knowledge',
        'alternatives_rejected': [
            {
                'inference': 'States should rely on allied nations for semiconductor supply',
                'rejected_because': 'Conflicts with sovereignty framing emphasis on autonomous capacity; allied dependencies can shift',
                'plausibility': 0.4
            },
            {
                'inference': 'Private sector investment alone can secure semiconductor supply',
                'rejected_because': 'Historical evidence shows market failures in strategic sectors; chip fabs require state-level capital',
                'plausibility': 0.3
            }
        ],
        'premise_confidence': 0.95,
        'inference_validity': 0.9,
        'source_quality': 0.9,
        'web_coherence': 0.92,
        'confidence_explanation': 'High strength (90%) due to: (1) tight definitional link between sovereignty and autonomous capacity, (2) empirical evidence from chip shortage demonstrating vulnerability, (3) strong coherence with industrial policy frameworks that are central to sovereignty discourse.',
        'revisability_cost': 'Rejecting this would require either: (a) weakening the definition of sovereignty to not require autonomous capacity, or (b) arguing semiconductors are not foundational to digital tech - both highly costly revisions.',
        'dependent_claims': [
            'Tech sovereignty requires industrial policy',
            'Strategic sectors deserve public investment',
            'Import dependency creates vulnerability'
        ],
        'web_centrality': WebCentrality.PERIPHERAL,
        'observation_proximity': 0.75,
    },
    ('forward_inferences', 'Critical infrastructure must have national ownership requirements'): {
        'inference_type': InferenceType.MATERIAL,
        'inference_rule': 'material_implication',
        'premises': [
            {
                'claim': 'Critical infrastructure is essential for national functioning',
                'claim_type': 'definitional',
                'centrality': 'high',
                'source': 'domain_knowledge'
            },
            {
                'claim': 'Foreign ownership of critical infrastructure enables external leverage',
                'claim_type': 'empirical',
                'centrality': 'medium',
                'source': 'geopolitical_analysis'
            }
        ],
        'reasoning_trace': 'If critical infrastructure is essential AND foreign ownership creates external leverage, then sovereignty (understood as freedom from external control) requires national ownership. This follows from the core sovereignty commitment to self-determination.',
        'derivation_trigger': 'prior_inference',
        'source_passage': 'Sovereignty implies freedom from external coercion',
        'source_location': 'sovereignty theory',
        'alternatives_rejected': [
            {
                'inference': 'Regulatory oversight is sufficient for foreign-owned infrastructure',
                'rejected_because': 'Regulation can be circumvented; ownership provides fundamental control',
                'plausibility': 0.5
            }
        ],
        'premise_confidence': 0.9,
        'inference_validity': 0.85,
        'source_quality': 0.85,
        'web_coherence': 0.88,
        'confidence_explanation': 'Strong inference (85%) but slightly lower than semiconductor case because: ownership requirements are more contested politically; some sovereignty advocates accept regulatory alternatives.',
        'revisability_cost': 'Would require distinguishing types of infrastructure or arguing regulation is sufficient for sovereignty.',
        'dependent_claims': [
            'States should screen foreign investment in strategic sectors',
            'National security review of tech acquisitions is justified'
        ],
        'web_centrality': WebCentrality.MEDIUM,
        'observation_proximity': 0.6,
    },
    ('backward_inferences', 'States have legitimate interests in technological capacity'): {
        'inference_type': InferenceType.TRANSCENDENTAL,
        'inference_rule': 'condition_of_possibility',
        'premises': [
            {
                'claim': 'Technological sovereignty is a valid political goal',
                'claim_type': 'normative',
                'centrality': 'core',
                'source': 'concept_definition'
            }
        ],
        'reasoning_trace': 'This is a transcendental inference: for tech sovereignty to be a valid goal AT ALL, states must have legitimate interests in technological capacity. If states had no such interests, sovereignty talk would be category error. This is a condition of possibility for the entire discourse.',
        'derivation_trigger': 'concept_definition',
        'source_passage': 'The concept of technological sovereignty presupposes state interest legitimacy',
        'source_location': 'conceptual analysis',
        'alternatives_rejected': [
            {
                'inference': 'Only individuals have legitimate tech interests; state interests are illegitimate aggregations',
                'rejected_because': 'Would dissolve the entire concept; libertarian framing incompatible with sovereignty',
                'plausibility': 0.2
            }
        ],
        'premise_confidence': 0.98,
        'inference_validity': 0.95,
        'source_quality': 0.9,
        'web_coherence': 0.95,
        'confidence_explanation': 'Very high (95%) because this is nearly analytic - it follows from the very possibility of sovereignty discourse. Rejecting it would dissolve the concept entirely.',
        'revisability_cost': 'Cannot reject this while maintaining any version of tech sovereignty. This is a load-bearing assumption.',
        'dependent_claims': [
            'All forward inferences from tech sovereignty',
            'The legitimacy of industrial policy',
            'State intervention in tech markets'
        ],
        'web_centrality': WebCentrality.CORE,
        'observation_proximity': 0.3,
    },
    ('contradictions', 'Complete free trade in all technology sectors'): {
        'inference_type': InferenceType.DEDUCTIVE,
        'inference_rule': 'material_incompatibility',
        'premises': [
            {
                'claim': 'Tech sovereignty requires capacity for autonomous tech development',
                'claim_type': 'definitional',
                'centrality': 'core',
                'source': 'concept_definition'
            },
            {
                'claim': 'Complete free trade precludes protective industrial policy',
                'claim_type': 'definitional',
                'centrality': 'high',
                'source': 'economic_theory'
            }
        ],
        'reasoning_trace': 'This is a hard contradiction: tech sovereignty REQUIRES industrial policy to build autonomous capacity, but complete free trade FORBIDS industrial policy. They cannot both be true. One must choose between the sovereignty framework and the pure free trade framework.',
        'derivation_trigger': 'concept_definition',
        'source_passage': 'Sovereignty requires autonomous capacity; free trade forbids protection',
        'source_location': 'conceptual analysis',
        'alternatives_rejected': [],
        'premise_confidence': 0.95,
        'inference_validity': 0.98,
        'source_quality': 0.9,
        'web_coherence': 0.95,
        'confidence_explanation': 'Near-deductive incompatibility. Both positions are clearly defined and their requirements are logically opposed.',
        'revisability_cost': 'This contradiction cannot be resolved without fundamentally redefining either sovereignty or free trade.',
        'dependent_claims': [
            'Tech sovereignty critique of WTO frameworks',
            'Justification for strategic industry exceptions'
        ],
        'web_centrality': WebCentrality.HIGH,
        'observation_proximity': 0.5,
    },
}


def create_reasoning_scaffold(session, item, item_content):
    """Create a reasoning scaffold for an analysis item if sample data exists."""
    key = (item.item_type, item_content)
    if key not in REASONING_SCAFFOLDS:
        return None

    scaffold_data = REASONING_SCAFFOLDS[key]

    scaffold = ItemReasoningScaffold(
        item_id=item.id,
        inference_type=scaffold_data.get('inference_type'),
        inference_rule=scaffold_data.get('inference_rule'),
        premises=scaffold_data.get('premises'),
        reasoning_trace=scaffold_data.get('reasoning_trace'),
        derivation_trigger=scaffold_data.get('derivation_trigger'),
        source_passage=scaffold_data.get('source_passage'),
        source_location=scaffold_data.get('source_location'),
        alternatives_rejected=scaffold_data.get('alternatives_rejected'),
        premise_confidence=scaffold_data.get('premise_confidence'),
        inference_validity=scaffold_data.get('inference_validity'),
        source_quality=scaffold_data.get('source_quality'),
        web_coherence=scaffold_data.get('web_coherence'),
        confidence_explanation=scaffold_data.get('confidence_explanation'),
        revisability_cost=scaffold_data.get('revisability_cost'),
        dependent_claims=scaffold_data.get('dependent_claims'),
    )
    session.add(scaffold)

    # Also update the item's Quinean fields
    if 'web_centrality' in scaffold_data:
        item.web_centrality = scaffold_data['web_centrality']
    if 'observation_proximity' in scaffold_data:
        item.observation_proximity = scaffold_data['observation_proximity']

    return scaffold


def seed_database():
    """Main seeding function."""
    # Create tables
    print("Creating tables...")
    Base.metadata.create_all(engine)

    session = Session()

    try:
        # Check if already seeded
        existing = session.query(AnalyticalDimension).first()
        if existing:
            print("Database already seeded. Clearing and re-seeding...")
            # Clear existing data in reverse dependency order
            session.query(ItemReasoningScaffold).delete()  # Delete scaffolds first (FK to items)
            session.query(AnalysisItem).delete()
            session.query(ConceptAnalysis).delete()
            session.query(AnalyzedConcept).delete()
            session.execute(operation_influences.delete())
            session.query(AnalyticalOperation).delete()
            session.query(TheoreticalInfluence).delete()
            session.query(AnalyticalDimension).delete()
            session.commit()

        # 1. Create dimensions
        print("Creating dimensions...")
        dimension_map = {}
        for dim_data in DIMENSIONS:
            dim = AnalyticalDimension(**dim_data)
            session.add(dim)
            session.flush()
            dimension_map[dim_data['dimension_type']] = dim

        # 2. Create theoretical influences
        print("Creating theoretical influences...")
        influence_map = {}
        for inf_data in INFLUENCES:
            inf = TheoreticalInfluence(**inf_data)
            session.add(inf)
            session.flush()
            influence_map[inf_data['short_name']] = inf

        # 3. Create operations and link to influences
        print("Creating operations...")
        operation_map = {}  # (dimension_type, op_name) -> operation
        for dim_type, ops in OPERATIONS.items():
            dimension = dimension_map[dim_type]
            for i, op_data in enumerate(ops):
                influences = op_data.pop('influences')
                op = AnalyticalOperation(
                    dimension_id=dimension.id,
                    sequence_order=i,
                    **op_data
                )
                session.add(op)
                session.flush()

                # Link influences
                for inf_name in influences:
                    if inf_name in influence_map:
                        stmt = operation_influences.insert().values(
                            operation_id=op.id,
                            influence_id=influence_map[inf_name].id
                        )
                        session.execute(stmt)

                operation_map[(dim_type, op_data['name'])] = op

        # 4. Create Tech Sovereignty concept
        print("Creating Tech Sovereignty concept...")
        tech_sov = AnalyzedConcept(
            term='Technological Sovereignty',
            definition='The capacity of a state or political entity to control, develop, and govern critical technologies within its jurisdiction, reducing dependency on foreign actors for essential technological capabilities.',
            author='Policy discourse',
            is_user_concept=True,
            paradigm='Strategic Autonomy / Post-Neoliberal Statecraft',
            disciplinary_home='Political Science / International Relations / Technology Policy'
        )
        session.add(tech_sov)
        session.flush()

        # 5. Create analyses for Tech Sovereignty
        print("Creating analyses...")
        dim_type_names = {
            '1. Positional Analysis': DimensionType.POSITIONAL,
            '2. Genealogical Analysis': DimensionType.GENEALOGICAL,
            '3. Presuppositional Analysis': DimensionType.PRESUPPOSITIONAL,
            '4. Commitment Analysis': DimensionType.COMMITMENT,
            '5. Affordance Analysis': DimensionType.AFFORDANCE,
            '6. Normalization Analysis': DimensionType.NORMALIZATION,
            '7. Boundary Analysis': DimensionType.BOUNDARY,
            '8. Dynamic Analysis': DimensionType.DYNAMIC,
        }

        for dim_name, dim_analyses in TECH_SOV_ANALYSIS.items():
            dim_type = dim_type_names.get(dim_name)
            if not dim_type:
                continue

            for op_name, op_analysis in dim_analyses.items():
                op = operation_map.get((dim_type, op_name))
                if not op:
                    print(f"  Warning: Operation not found: {op_name}")
                    continue

                # Create analysis
                analysis = ConceptAnalysis(
                    concept_id=tech_sov.id,
                    operation_id=op.id,
                    canonical_statement=op_analysis.get('canonical_statement', ''),
                    analysis_data=op_analysis.get('analysis', {}),
                    version=op_analysis.get('version', '1.0'),
                    confidence=op_analysis.get('confidence', 0.8),
                    source_type=SourceType.LLM_GENERATED,
                )
                session.add(analysis)
                session.flush()

                # Create individual items from analysis_data
                analysis_content = op_analysis.get('analysis', {})
                for key, items in analysis_content.items():
                    if isinstance(items, list):
                        for i, item in enumerate(items):
                            if isinstance(item, dict):
                                # Extract main content
                                content_keys = ['statement', 'commitment', 'norm', 'anomaly',
                                               'condition', 'metaphor', 'concept', 'action',
                                               'phrase', 'habit', 'kind', 'position',
                                               'phenomenon', 'relation', 'indicator',
                                               'classification', 'what_governed', 'claim_type']
                                content = None
                                for ck in content_keys:
                                    if ck in item:
                                        content = item[ck]
                                        break
                                if not content:
                                    content = str(item)[:500]

                                analysis_item = AnalysisItem(
                                    analysis_id=analysis.id,
                                    item_type=key,
                                    content=content,
                                    strength=item.get('strength'),
                                    severity=item.get('severity', item.get('seriousness')),
                                    extra_data=item,
                                    sequence_order=i,
                                )
                                session.add(analysis_item)
                                session.flush()  # Get the item ID

                                # Create reasoning scaffold if sample data exists
                                create_reasoning_scaffold(session, analysis_item, content)

        session.commit()
        print("Database seeded successfully!")

        # Print summary
        print("\n=== SUMMARY ===")
        print(f"Dimensions: {session.query(AnalyticalDimension).count()}")
        print(f"Operations: {session.query(AnalyticalOperation).count()}")
        print(f"Theoretical Influences: {session.query(TheoreticalInfluence).count()}")
        print(f"Concepts: {session.query(AnalyzedConcept).count()}")
        print(f"Analyses: {session.query(ConceptAnalysis).count()}")
        print(f"Analysis Items: {session.query(AnalysisItem).count()}")
        print(f"Reasoning Scaffolds: {session.query(ItemReasoningScaffold).count()}")

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        raise
    finally:
        session.close()


if __name__ == '__main__':
    seed_database()
