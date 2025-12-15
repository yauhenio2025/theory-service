-- Migration: Add Theory Sources support
-- Date: 2024-12-16
-- Description: Creates theory_sources table and adds source_id to concepts, dialectics, claims

-- Create theory_sources table if not exists
CREATE TABLE IF NOT EXISTS theory_sources (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    short_name VARCHAR(100),
    source_type VARCHAR(50) DEFAULT 'article',
    description TEXT,
    author VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_theory_sources_short_name ON theory_sources(short_name);

-- Add source_id to concepts (if column doesn't exist)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'concepts' AND column_name = 'source_id'
    ) THEN
        ALTER TABLE concepts ADD COLUMN source_id INTEGER REFERENCES theory_sources(id);
    END IF;
END $$;

-- Add source_id to dialectics (if column doesn't exist)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'dialectics' AND column_name = 'source_id'
    ) THEN
        ALTER TABLE dialectics ADD COLUMN source_id INTEGER REFERENCES theory_sources(id);
    END IF;
END $$;

-- Add source_id to claims (if column doesn't exist)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'claims' AND column_name = 'source_id'
    ) THEN
        ALTER TABLE claims ADD COLUMN source_id INTEGER REFERENCES theory_sources(id);
    END IF;
END $$;

-- Create indexes for source_id
CREATE INDEX IF NOT EXISTS idx_concepts_source_id ON concepts(source_id);
CREATE INDEX IF NOT EXISTS idx_dialectics_source_id ON dialectics(source_id);
CREATE INDEX IF NOT EXISTS idx_claims_source_id ON claims(source_id);
