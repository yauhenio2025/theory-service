-- Migration: Wizard Sessions for Cross-Device Persistence
-- Date: 2024-12-17
-- Description: Adds table for storing wizard session state across devices

-- ============================================================================
-- WIZARD SESSIONS - Stores wizard session state for cross-device persistence
-- ============================================================================
CREATE TABLE IF NOT EXISTS wizard_sessions (
    id SERIAL PRIMARY KEY,

    -- Session identification
    session_key VARCHAR(64) UNIQUE NOT NULL,  -- UUID for accessing session
    concept_name VARCHAR(300) NOT NULL,

    -- Session state (JSON blob with all wizard state)
    session_state JSONB NOT NULL,

    -- Metadata
    stage VARCHAR(50),                        -- Current wizard stage
    source_id INTEGER REFERENCES theory_sources(id),

    -- Status tracking
    status VARCHAR(20) DEFAULT 'active',      -- active, completed, abandoned

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    last_accessed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_wizard_sessions_key ON wizard_sessions(session_key);
CREATE INDEX IF NOT EXISTS idx_wizard_sessions_concept ON wizard_sessions(concept_name);
CREATE INDEX IF NOT EXISTS idx_wizard_sessions_status ON wizard_sessions(status);
CREATE INDEX IF NOT EXISTS idx_wizard_sessions_updated ON wizard_sessions(updated_at DESC);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_wizard_session_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for auto-updating timestamp
DROP TRIGGER IF EXISTS wizard_sessions_update_timestamp ON wizard_sessions;
CREATE TRIGGER wizard_sessions_update_timestamp
    BEFORE UPDATE ON wizard_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_wizard_session_timestamp();
