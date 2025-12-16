-- Genesis Dimension Schema Migration
-- Enables setup of novel concepts not in public discourse
-- Generated: 2025-12-16T14:06:38.662060

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
 '[{"value": "theoretical_innovation", "label": "A new theoretical framework or lens"}, {"value": "empirical_discovery", "label": "A pattern discovered through observation"}, {"value": "synthetic_unification", "label": "A synthesis of previously separate ideas"}, {"value": "paradigm_shift", "label": "A fundamental reconceptualization"}, {"value": "other", "label": "Other (please elaborate)"}]'::jsonb,
 '{"required": true}'::jsonb, NULL, NULL,
 'This helps us understand what kind of support and validation your concept needs.',
 NULL, 'concept_genesis', 'genesis_type', true, 1),

(1, 'concept_name', 'What is the name of your concept?', 'open_ended',
 'The name sets expectations and should be distinct from existing terms',
 NULL, '{"required": true, "minLength": 2, "maxLength": 100}'::jsonb, 2, 100,
 'Choose a name that captures the essence while being distinct from existing terms.',
 'Technological Sovereignty', 'concepts', 'name', true, 2),

(1, 'core_definition', 'In one paragraph, provide your working definition of this concept.', 'open_ended',
 'Forces initial precision; becomes anchor for later refinement',
 NULL, '{"required": true, "minLength": 100, "maxLength": 1500}'::jsonb, 100, 1500,
 'This doesn''t need to be perfect. We''ll refine it throughout the process.',
 'Technological sovereignty refers to the capacity of a political entity to exercise meaningful control over the technological systems upon which its economy, security, and social functioning depend...',
 'concepts', 'definition', true, 3),

(2, 'problem_space', 'What problem or gap in understanding does this concept address? Why do we need a new concept for this?', 'open_ended',
 'Justifies concept''s existence; clarifies its purpose',
 NULL, '{"required": true, "minLength": 150, "maxLength": 2000}'::jsonb, 150, 2000,
 'A concept needs to DO something. What can we understand, explain, or do with this concept that we couldn''t before?',
 'Existing concepts like "digital sovereignty" fail to capture the specific way that technological dependencies create structural constraints on political autonomy...',
 'concept_problem_space', 'gap_description', true, 1),

(3, 'most_confused_with', 'What existing concept is this MOST likely to be confused with?', 'open_ended',
 'Identifies primary differentiation target',
 NULL, '{"required": true, "minLength": 50, "maxLength": 500}'::jsonb, 50, 500,
 'Pick ONE concept that poses the greatest confusion risk.',
 'Digital sovereignty',
 'concept_differentiation', 'confused_with', true, 1),

(4, 'paradigmatic_case', 'What is the single best example that captures the essence of this concept? Describe it in detail.', 'open_ended',
 'Paradigmatic cases are crucial for concept teaching and recognition',
 NULL, '{"required": true, "minLength": 200, "maxLength": 2000}'::jsonb, 200, 2000,
 'Think: if you had to explain this concept to someone new and could only use ONE example, what would it be?',
 'The European 5G and Huawei dilemma...',
 'concept_paradigmatic_cases', 'full_description', true, 1),

(5, 'core_claim', 'What is the most fundamental claim about reality that your concept makes? What must be TRUE for this concept to be meaningful?', 'open_ended',
 'Forces articulation of core commitment; enables testing',
 NULL, '{"required": true, "minLength": 100, "maxLength": 1000}'::jsonb, 100, 1000,
 'A concept makes claims about how the world works. What''s yours?',
 'Technological dependencies can constitute a form of sovereignty loss distinct from economic, political, or military dependencies.',
 'concept_foundational_claims', 'claim_statement', true, 1),

(6, 'recognition_pattern', 'How can we recognize an implicit instance of this concept in a text that doesn''t use the term? What patterns should we look for?', 'open_ended',
 'Essential for LLM-assisted document analysis',
 NULL, '{"required": true, "minLength": 150, "maxLength": 1500}'::jsonb, 150, 1500,
 'Describe linguistic patterns, argument structures, or situational descriptions that indicate this concept is in play.',
 'Look for: arguments that technology choices have political/sovereignty implications beyond economics...',
 'concept_recognition_markers', 'marker_description', true, 1);

COMMIT;
