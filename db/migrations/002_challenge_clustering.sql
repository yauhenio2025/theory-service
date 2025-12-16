-- Migration: Challenge Clustering and Emerging Theory Support
-- Date: 2024-12-16
-- Description: Adds tables for emerging concepts, emerging dialectics, and challenge clustering

-- ============================================================================
-- EMERGING CONCEPTS - Proposed new concepts from evidence
-- ============================================================================
CREATE TABLE IF NOT EXISTS emerging_concepts (
    id SERIAL PRIMARY KEY,
    source_project_id INTEGER NOT NULL,
    source_cluster_ids INTEGER[],           -- Can emerge from multiple clusters
    source_cluster_names TEXT[],

    proposed_name VARCHAR(300) NOT NULL,
    proposed_definition TEXT,
    emergence_rationale TEXT NOT NULL,
    evidence_strength VARCHAR(20),          -- strong, moderate, suggestive

    related_concept_ids INTEGER[],          -- Existing concepts this relates to
    differentiation_notes TEXT,             -- How it differs from existing

    confidence FLOAT DEFAULT 0.8,
    status VARCHAR(20) DEFAULT 'proposed',  -- proposed, clustering, accepted, rejected, promoted
    promoted_to_concept_id INTEGER REFERENCES concepts(id),

    cluster_group_id INTEGER,               -- For grouping similar proposals

    reviewer_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    reviewed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_emerging_concepts_project ON emerging_concepts(source_project_id);
CREATE INDEX IF NOT EXISTS idx_emerging_concepts_status ON emerging_concepts(status);
CREATE INDEX IF NOT EXISTS idx_emerging_concepts_cluster_group ON emerging_concepts(cluster_group_id);

-- ============================================================================
-- EMERGING DIALECTICS - Proposed new dialectics from evidence
-- ============================================================================
CREATE TABLE IF NOT EXISTS emerging_dialectics (
    id SERIAL PRIMARY KEY,
    source_project_id INTEGER NOT NULL,
    source_cluster_ids INTEGER[],
    source_cluster_names TEXT[],

    proposed_tension_a TEXT NOT NULL,
    proposed_tension_b TEXT NOT NULL,
    proposed_question TEXT,
    emergence_rationale TEXT NOT NULL,
    evidence_strength VARCHAR(20),

    related_dialectic_ids INTEGER[],
    differentiation_notes TEXT,

    confidence FLOAT DEFAULT 0.8,
    status VARCHAR(20) DEFAULT 'proposed',
    promoted_to_dialectic_id INTEGER REFERENCES dialectics(id),

    cluster_group_id INTEGER,

    reviewer_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    reviewed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_emerging_dialectics_project ON emerging_dialectics(source_project_id);
CREATE INDEX IF NOT EXISTS idx_emerging_dialectics_status ON emerging_dialectics(status);
CREATE INDEX IF NOT EXISTS idx_emerging_dialectics_cluster_group ON emerging_dialectics(cluster_group_id);

-- ============================================================================
-- CHALLENGE CLUSTERS - Groups of similar challenges for batch processing
-- ============================================================================
CREATE TABLE IF NOT EXISTS challenge_clusters (
    id SERIAL PRIMARY KEY,
    cluster_type VARCHAR(30) NOT NULL,      -- concept_impact, dialectic_impact, emerging_concept, emerging_dialectic

    -- LLM-generated cluster metadata
    cluster_summary TEXT,                   -- What unifies this cluster
    cluster_recommendation TEXT,            -- LLM's suggested action explanation
    recommended_action VARCHAR(30),         -- accept, reject, merge, refine, human_review

    -- Target entity (for impact clusters)
    target_concept_id INTEGER REFERENCES concepts(id),
    target_dialectic_id INTEGER REFERENCES dialectics(id),

    -- Cluster state
    status VARCHAR(20) DEFAULT 'pending',   -- pending, reviewing, resolved
    resolution_notes TEXT,
    member_count INTEGER DEFAULT 0,
    source_project_count INTEGER DEFAULT 0,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    resolved_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_challenge_clusters_type ON challenge_clusters(cluster_type);
CREATE INDEX IF NOT EXISTS idx_challenge_clusters_status ON challenge_clusters(status);
CREATE INDEX IF NOT EXISTS idx_challenge_clusters_target_concept ON challenge_clusters(target_concept_id);
CREATE INDEX IF NOT EXISTS idx_challenge_clusters_target_dialectic ON challenge_clusters(target_dialectic_id);

-- ============================================================================
-- CHALLENGE CLUSTER MEMBERS - Links challenges/emerging to clusters
-- ============================================================================
CREATE TABLE IF NOT EXISTS challenge_cluster_members (
    id SERIAL PRIMARY KEY,
    cluster_id INTEGER NOT NULL REFERENCES challenge_clusters(id) ON DELETE CASCADE,

    -- One of these will be set depending on cluster_type
    challenge_id INTEGER REFERENCES challenges(id) ON DELETE CASCADE,
    emerging_concept_id INTEGER REFERENCES emerging_concepts(id) ON DELETE CASCADE,
    emerging_dialectic_id INTEGER REFERENCES emerging_dialectics(id) ON DELETE CASCADE,

    similarity_score FLOAT,                 -- How similar to cluster centroid (0-1)
    created_at TIMESTAMPTZ DEFAULT NOW(),

    -- Ensure only one reference type per member
    CONSTRAINT single_reference CHECK (
        (challenge_id IS NOT NULL)::int +
        (emerging_concept_id IS NOT NULL)::int +
        (emerging_dialectic_id IS NOT NULL)::int = 1
    )
);

CREATE INDEX IF NOT EXISTS idx_cluster_members_cluster ON challenge_cluster_members(cluster_id);
CREATE INDEX IF NOT EXISTS idx_cluster_members_challenge ON challenge_cluster_members(challenge_id);
CREATE INDEX IF NOT EXISTS idx_cluster_members_emerging_concept ON challenge_cluster_members(emerging_concept_id);
CREATE INDEX IF NOT EXISTS idx_cluster_members_emerging_dialectic ON challenge_cluster_members(emerging_dialectic_id);

-- ============================================================================
-- ADD source_project_name TO CHALLENGES (if not exists)
-- ============================================================================
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'challenges' AND column_name = 'source_project_name'
    ) THEN
        ALTER TABLE challenges ADD COLUMN source_project_name VARCHAR(200);
    END IF;
END $$;

-- ============================================================================
-- ADD cluster_group_id TO CHALLENGES (for linking to clusters)
-- ============================================================================
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'challenges' AND column_name = 'cluster_group_id'
    ) THEN
        ALTER TABLE challenges ADD COLUMN cluster_group_id INTEGER;
    END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_challenges_cluster_group ON challenges(cluster_group_id);
