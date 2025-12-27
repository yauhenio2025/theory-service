# Strategizer MVP Implementation Plan

**Created:** 2025-12-27
**Scope:** Phase 1 - Domain Bootstrapping + Basic Q&A
**Tech Stack:** FastAPI, SQLite, Claude API, Vanilla JS frontend

---

## Executive Summary

This plan implements Phase 1 of the Strategizer MVP: a domain-agnostic strategic thinking tool where users:
1. Create a project with a brief description
2. Bootstrap a domain (LLM proposes structure from brief)
3. Build strategic units (Concepts, Dialectics, Actors) through Q&A dialogue
4. Persist everything in SQLite

**Core Philosophy:**
- Python gathers data → LLM makes judgments → Python executes decisions
- Users only see things requiring their judgment (attention-only-on-friction)
- LLM-first design: No hardcoded thresholds, holistic assessment

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                 │
│  Vanilla JS + HTML Templates (Jinja2)                           │
│  - Project Setup Page                                            │
│  - Domain Bootstrap UI                                           │
│  - Unit Management (Concepts, Dialectics, Actors)               │
│  - Q&A Dialogue Interface                                        │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP/JSON
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND                               │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────┐ │
│  │ routers/         │  │ services/        │  │ prompts/       │ │
│  │  - projects.py   │  │  - bootstrap.py  │  │  - domain.py   │ │
│  │  - units.py      │  │  - dialogue.py   │  │  - units.py    │ │
│  │  - dialogue.py   │  │  - unit_ops.py   │  │  - qa.py       │ │
│  └──────────────────┘  └──────────────────┘  └────────────────┘ │
│  ┌──────────────────┐  ┌──────────────────┐                     │
│  │ models/          │  │ llm/             │                     │
│  │  - schemas.py    │  │  - claude.py     │                     │
│  │  - database.py   │  │  - streaming.py  │                     │
│  └──────────────────┘  └──────────────────┘                     │
└───────────────────────────┬─────────────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
    ┌──────────────┐               ┌──────────────┐
    │   SQLite     │               │  Claude API  │
    │  Database    │               │  (Anthropic) │
    └──────────────┘               └──────────────┘
```

---

## File Structure

```
strategizer/
├── main.py                    # FastAPI app entry point
├── config.py                  # Configuration (API keys, paths)
├── database.py                # SQLAlchemy setup + models
├── start                      # Universal start script
│
├── routers/
│   ├── __init__.py
│   ├── projects.py            # Project CRUD + bootstrap
│   ├── units.py               # Unit CRUD
│   └── dialogue.py            # Q&A endpoints
│
├── services/
│   ├── __init__.py
│   ├── bootstrap.py           # Domain bootstrapping logic
│   ├── dialogue.py            # Q&A dialogue service
│   └── unit_ops.py            # Unit operations
│
├── llm/
│   ├── __init__.py
│   ├── claude.py              # Claude API client wrapper
│   └── prompts/
│       ├── __init__.py
│       ├── domain_bootstrap.py
│       ├── unit_creation.py
│       └── qa_dialogue.py
│
├── models/
│   ├── __init__.py
│   └── schemas.py             # Pydantic models
│
├── templates/
│   ├── base.html
│   ├── index.html             # Project list
│   ├── project.html           # Main project view
│   └── components/
│       ├── domain_bootstrap.html
│       ├── unit_card.html
│       └── qa_panel.html
│
├── static/
│   ├── css/
│   │   └── main.css
│   └── js/
│       ├── app.js
│       ├── bootstrap.js
│       ├── units.js
│       └── dialogue.js
│
└── tests/
    ├── __init__.py
    ├── test_bootstrap.py
    ├── test_units.py
    └── test_dialogue.py
```

---

## Database Schema

```sql
-- Projects table
CREATE TABLE projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    brief TEXT NOT NULL,  -- Original project description
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Domains table (bootstrapped from brief)
CREATE TABLE domains (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    core_question TEXT,  -- "Where to deploy capital for max climate impact?"
    vocabulary JSON,     -- {"concept": "Thesis", "tension": "Trade-off", ...}
    template_base TEXT,  -- Which template cloned from (theory, foundation, etc)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(project_id)   -- One domain per project
);

-- Seed content table (initial concepts, dialectics proposed by bootstrapping)
CREATE TABLE seed_content (
    id TEXT PRIMARY KEY,
    domain_id TEXT NOT NULL REFERENCES domains(id) ON DELETE CASCADE,
    content_type TEXT NOT NULL,  -- 'concept', 'dialectic', 'actor', 'grid'
    content JSON NOT NULL,       -- The full seed content
    accepted BOOLEAN DEFAULT FALSE,  -- User accepted this seed?
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Units table (Concepts, Dialectics, Actors)
CREATE TABLE units (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,

    -- Unit identity
    unit_type TEXT NOT NULL,     -- 'concept', 'dialectic', 'actor'
    display_type TEXT,           -- Domain-specific name (e.g., "Thesis", "Trade-off")
    tier TEXT DEFAULT 'domain',  -- 'universal', 'domain', 'emergent'

    -- Core content
    name TEXT NOT NULL,
    definition TEXT,
    content JSON,                -- Type-specific content

    -- Status
    status TEXT DEFAULT 'draft', -- 'draft', 'tested', 'canonical'
    version INTEGER DEFAULT 1,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Unit extensions for type-specific fields
CREATE TABLE unit_extensions (
    id TEXT PRIMARY KEY,
    unit_id TEXT NOT NULL REFERENCES units(id) ON DELETE CASCADE,
    extension_type TEXT NOT NULL,  -- 'dialectic_poles', 'actor_interests', etc.
    extension_data JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Grids applied to units
CREATE TABLE grid_instances (
    id TEXT PRIMARY KEY,
    unit_id TEXT NOT NULL REFERENCES units(id) ON DELETE CASCADE,
    grid_type TEXT NOT NULL,      -- 'LOGICAL', 'ACTOR', 'TEMPORAL', etc.
    tier TEXT DEFAULT 'required', -- 'required', 'flexible', 'wildcard'
    slots JSON,                   -- Filled slot content
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Q&A dialogue history
CREATE TABLE dialogue_turns (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    unit_id TEXT REFERENCES units(id) ON DELETE SET NULL,  -- Optional: related unit

    -- Dialogue content
    turn_type TEXT NOT NULL,      -- 'user_question', 'system_response', 'suggestion'
    content TEXT NOT NULL,
    context JSON,                 -- Additional context for the turn

    -- Actions taken
    actions_proposed JSON,        -- What the system suggested
    actions_taken JSON,           -- What was actually executed

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indices
CREATE INDEX idx_units_project ON units(project_id);
CREATE INDEX idx_units_type ON units(unit_type);
CREATE INDEX idx_grids_unit ON grid_instances(unit_id);
CREATE INDEX idx_dialogue_project ON dialogue_turns(project_id);
CREATE INDEX idx_seed_domain ON seed_content(domain_id);
```

---

## API Endpoints

### Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/projects` | Create project from brief |
| `GET` | `/api/projects` | List all projects |
| `GET` | `/api/projects/{id}` | Get project with domain & units |
| `PUT` | `/api/projects/{id}` | Update project |
| `DELETE` | `/api/projects/{id}` | Delete project |

### Domain Bootstrapping

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/projects/{id}/bootstrap` | Bootstrap domain from brief |
| `GET` | `/api/projects/{id}/domain` | Get domain details |
| `POST` | `/api/projects/{id}/domain/seeds/accept` | Accept seed content |
| `POST` | `/api/projects/{id}/domain/seeds/reject` | Reject seed content |

### Units

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/projects/{id}/units` | Create unit |
| `GET` | `/api/projects/{id}/units` | List units (with filters) |
| `GET` | `/api/projects/{id}/units/{unit_id}` | Get unit details |
| `PUT` | `/api/projects/{id}/units/{unit_id}` | Update unit |
| `DELETE` | `/api/projects/{id}/units/{unit_id}` | Delete unit |
| `POST` | `/api/projects/{id}/units/{unit_id}/refine` | LLM-assisted refinement |

### Q&A Dialogue

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/projects/{id}/ask` | Ask question, get response |
| `POST` | `/api/projects/{id}/suggest` | Get suggestions for next steps |
| `GET` | `/api/projects/{id}/dialogue` | Get dialogue history |

---

## Implementation Steps

### Step 1: Project Scaffolding
**Goal:** FastAPI app that runs, serves templates, connects to SQLite

**Tasks:**
1. Create directory structure
2. Set up FastAPI with Jinja2 templates
3. Configure SQLAlchemy async with SQLite
4. Create database models
5. Create start script with auto-reload
6. Add basic index page showing "Strategizer MVP"

**Files:**
- `main.py`, `config.py`, `database.py`
- `templates/base.html`, `templates/index.html`
- `static/css/main.css`
- `start`

### Step 2: Project CRUD
**Goal:** Create, list, view, delete projects

**Tasks:**
1. Define Pydantic models for Project
2. Implement project router
3. Create project list template
4. Create project detail template (empty for now)
5. Wire up frontend forms

**Files:**
- `models/schemas.py`
- `routers/projects.py`
- `templates/index.html` (project list)
- `templates/project.html` (project view)
- `static/js/app.js`

### Step 3: Claude API Integration
**Goal:** Working Claude client with streaming support

**Tasks:**
1. Create Claude client wrapper
2. Implement streaming support (for long ops)
3. Add error handling and retry logic
4. Create test endpoint to verify API works

**Files:**
- `llm/claude.py`
- `llm/__init__.py`

### Step 4: Domain Bootstrapping
**Goal:** LLM creates domain from project brief

**Tasks:**
1. Create domain bootstrap prompt
2. Implement DomainBootstrapper service
3. Create bootstrap endpoint
4. Parse LLM response into domain + seeds
5. Store domain and seed content
6. Create bootstrap UI (show proposed domain, seeds)
7. Implement accept/reject for seeds

**Prompt Design:**
```
Analyze the project brief and design a domain structure:

PROJECT BRIEF:
{brief}

Design a domain by answering:

1. DOMAIN IDENTITY
   - What should this domain be called?
   - What's the core strategic question?
   - What does "success" look like?

2. UNIT VOCABULARY
   Map universal types to domain-specific terms:
   - Concepts → What are core abstractions called?
   - Tensions → What are key trade-offs called?
   - Actors → Who are the key players?

3. INITIAL GRIDS
   What analytical dimensions matter? Suggest 2-4 grids.

4. SEED CONTENT
   Suggest 2-3 starter concepts and 1-2 key tensions.

5. TEMPLATE PROXIMITY
   Which template is closest? (theory, foundation, brand, government, investment)

Return structured YAML.
```

**Files:**
- `llm/prompts/domain_bootstrap.py`
- `services/bootstrap.py`
- `routers/projects.py` (add bootstrap endpoint)
- `templates/components/domain_bootstrap.html`
- `static/js/bootstrap.js`

### Step 5: Unit Management
**Goal:** Create and manage Concepts, Dialectics, Actors

**Tasks:**
1. Define Pydantic models for each unit type
2. Implement unit router with CRUD
3. Create unit creation forms (per type)
4. Create unit card display component
5. Create unit list view
6. Implement unit detail/edit view

**Unit Types:**

**ConceptUnit:**
```python
{
    "name": "Dual Circulation",
    "definition": "China's strategy of...",
    "what_it_enables": ["..."],
    "what_it_forecloses": ["..."],
    "conditions_of_application": ["..."]
}
```

**DialecticUnit:**
```python
{
    "name": "Efficiency ↔ Resilience",
    "pole_a": {"name": "Efficiency", "description": "..."},
    "pole_b": {"name": "Resilience", "description": "..."},
    "navigation_strategies": ["..."],
    "when_prioritize_a": "...",
    "when_prioritize_b": "..."
}
```

**ActorUnit:**
```python
{
    "name": "The IMF",
    "actor_type": "institution",  # institution, individual, collective
    "interests": ["..."],
    "capabilities": ["..."],
    "constraints": ["..."],
    "likely_responses": {"scenario_x": "..."}
}
```

**Files:**
- `models/schemas.py` (add unit models)
- `routers/units.py`
- `services/unit_ops.py`
- `templates/components/unit_card.html`
- `templates/components/unit_form.html`
- `static/js/units.js`

### Step 6: Q&A Dialogue
**Goal:** Ask questions, get framework-aware responses

**Tasks:**
1. Create Q&A prompt template
2. Implement dialogue service
3. Create dialogue endpoint
4. Create dialogue UI panel
5. Implement suggestion generation
6. Wire up actions (create unit, refine unit, etc.)

**Dialogue Prompt:**
```
You are a strategic thinking partner helping develop a framework.

CURRENT PROJECT:
{project_name}
{project_brief}

CURRENT DOMAIN:
{domain_name}: {core_question}

EXISTING FRAMEWORK:
Concepts: {concepts_summary}
Tensions: {tensions_summary}
Actors: {actors_summary}

USER QUESTION:
{user_question}

Respond as a thinking partner:
1. Answer the question using framework context
2. Suggest relevant actions:
   - "create_concept": {name, definition} if a new concept is implied
   - "create_tension": {name, pole_a, pole_b} if a tension is surfaced
   - "refine_unit": {unit_id, refinement} if existing unit should evolve
   - "suggest_question": {question} for productive follow-up

Return JSON with:
- response: Your thinking partner response
- suggested_actions: List of actions with parameters
```

**Files:**
- `llm/prompts/qa_dialogue.py`
- `services/dialogue.py`
- `routers/dialogue.py`
- `templates/components/qa_panel.html`
- `static/js/dialogue.js`

### Step 7: Polish & Integration
**Goal:** Smooth, integrated experience

**Tasks:**
1. Style the UI (clean, minimal)
2. Add loading states for LLM calls
3. Implement real-time updates
4. Add keyboard shortcuts
5. Create getting started guide
6. Write tests for core flows

**Files:**
- `static/css/main.css` (polish)
- `static/js/app.js` (loading states)
- `tests/test_*.py`

---

## LLM Prompt Templates

### Domain Bootstrap Prompt
```python
DOMAIN_BOOTSTRAP_PROMPT = """
A user is starting a new strategic project. Analyze the brief and
design a domain structure for the Strategizer system.

PROJECT BRIEF:
{brief}

Design a domain by answering:

1. DOMAIN IDENTITY
   - What should this domain be called?
   - What's the core strategic question this domain addresses?
   - What does "success" look like in this domain?

2. UNIT VOCABULARY
   Map the universal unit types to domain-specific terms:
   - Concepts → What are core abstractions called in this domain?
     (e.g., "Plays" in philanthropy, "Theses" in investing)
   - Tensions → What are the key trade-offs called?
     (e.g., "Trade-offs", "Strategic tensions", "Paradoxes")
   - Actors → Who are the key players?
     (e.g., "Stakeholders", "Interlocutors", "Market participants")

3. INITIAL GRIDS
   Beyond universal grids (LOGICAL, ACTOR, TEMPORAL), what analytical
   dimensions matter for this domain? Suggest 2-4 domain-specific grids
   with their slot structures.

4. SEED CONTENT
   Suggest 2-3 starter concepts and 1-2 key tensions that any project
   in this domain would likely need to grapple with.

5. TEMPLATE PROXIMITY
   Which existing domain template is closest?
   Options: theory, foundation, brand, government, investment
   If none are close, say "none - build from scratch"

Return your design as YAML with this structure:

```yaml
identity:
  name: "Domain Name"
  core_question: "The fundamental strategic question"
  success_looks_like: "Description of success"

vocabulary:
  concept: "Domain-specific term for concepts"
  tension: "Domain-specific term for tensions"
  actor: "Domain-specific term for actors"

grids:
  - name: "GRID_NAME"
    description: "What this grid captures"
    slots:
      - slot_name: "description"

seed_concepts:
  - name: "Concept Name"
    definition: "Brief definition"
    why_fundamental: "Why this is a starting point"

seed_tensions:
  - name: "Pole A ↔ Pole B"
    pole_a: "Description of pole A"
    pole_b: "Description of pole B"
    why_fundamental: "Why this tension matters"

template_proximity: "theory" | "foundation" | "brand" | "government" | "investment" | "none"
```
"""
```

### Unit Creation Prompt
```python
UNIT_CREATION_PROMPT = """
Help the user develop a {unit_type} for their strategic framework.

PROJECT CONTEXT:
{project_context}

DOMAIN: {domain_name}
The domain uses "{display_type}" instead of "{unit_type}".

USER INPUT:
{user_input}

Create a well-formed {display_type}:

{type_specific_instructions}

Return as YAML:

```yaml
name: "Name of the {display_type}"
definition: "Clear, actionable definition"
{type_specific_fields}
```
"""

CONCEPT_INSTRUCTIONS = """
For a Concept/Thesis/Frame:
- name: A memorable, precise name
- definition: What this concept captures (1-2 sentences)
- what_it_enables: What becomes visible/possible with this concept? (list)
- what_it_forecloses: What becomes invisible/impossible? (list)
- conditions_of_application: When does this concept apply? (list)
"""

DIALECTIC_INSTRUCTIONS = """
For a Tension/Trade-off/Paradox:
- name: "Pole A ↔ Pole B" format
- pole_a:
    name: Name of first pole
    description: What this pole represents
- pole_b:
    name: Name of second pole
    description: What this pole represents
- navigation_strategies: How to navigate this tension (list)
- when_prioritize_a: Conditions favoring pole A
- when_prioritize_b: Conditions favoring pole B
"""

ACTOR_INSTRUCTIONS = """
For an Actor/Stakeholder/Player:
- name: Name of the actor
- actor_type: institution | individual | collective | market_force
- interests: What they want (list)
- capabilities: What they can do (list)
- constraints: What limits them (list)
- likely_responses: How they'd respond to key scenarios (dict)
"""
```

### Q&A Dialogue Prompt
```python
QA_DIALOGUE_PROMPT = """
You are a strategic thinking partner. The user is building a strategic
framework and has a question.

PROJECT: {project_name}
BRIEF: {project_brief}

DOMAIN: {domain_name}
Core Question: {core_question}

CURRENT FRAMEWORK:

## {concept_display_type}s ({concept_count})
{concepts_summary}

## {tension_display_type}s ({tension_count})
{tensions_summary}

## {actor_display_type}s ({actor_count})
{actors_summary}

---

USER QUESTION:
{user_question}

---

Respond as a thinking partner:

1. ANSWER: Address their question using the framework context. Be specific,
   reference existing units when relevant.

2. IMPLICATIONS: What does this question reveal about the framework?
   Are there gaps, tensions, or new directions implied?

3. SUGGESTED ACTIONS: Propose specific actions (0-3):
   - create_concept: If a new concept is implied
   - create_tension: If a new tension is surfaced
   - create_actor: If a new actor is identified
   - refine_unit: If an existing unit should evolve
   - ask_followup: If a clarifying question would help

Return as JSON:
```json
{
    "response": "Your thinking partner response...",
    "implications": "What this reveals about the framework...",
    "suggested_actions": [
        {
            "action_type": "create_concept",
            "parameters": {
                "name": "Suggested Concept",
                "definition": "Brief definition",
                "rationale": "Why this belongs in the framework"
            }
        }
    ]
}
```

Focus on being generative and helpful, not just descriptive. Push the
user's thinking forward.
"""
```

---

## UI Mockups (Text-Based)

### Project List Page
```
┌─────────────────────────────────────────────────────────────────┐
│ STRATEGIZER                                              [Dark] │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Your Projects                                                   │
│  ─────────────                                                   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Climate Tech Investment Strategy                        │    │
│  │ How to deploy capital for maximum climate impact        │    │
│  │                                                         │    │
│  │ Domain: Investment    Units: 12    Last: 2h ago        │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Moldova Media Strategy                                   │    │
│  │ Building ecosystem resilience for independent media     │    │
│  │                                                         │    │
│  │ Domain: Foundation    Units: 8     Last: 1d ago        │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  [+ New Project]                                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### New Project Modal
```
┌─────────────────────────────────────────────────────────────────┐
│ Create New Project                                        [X]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Project Name                                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ AI Policy for African Union                               │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Project Brief                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Developing a framework for AI governance across the      │   │
│  │ African Union, balancing innovation enablement with      │   │
│  │ protection of citizens, considering:                      │   │
│  │ - Limited compute infrastructure                          │   │
│  │ - Need for technology transfer                            │   │
│  │ - Sovereignty concerns with foreign AI systems            │   │
│  │ - Employment effects in informal economy                  │   │
│  │ - ...                                                     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Describe your strategic challenge. The more context you        │
│  provide, the better the system can help bootstrap your         │
│  framework.                                                      │
│                                                                  │
│                               [Cancel]  [Create & Bootstrap →]  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Domain Bootstrap Review
```
┌─────────────────────────────────────────────────────────────────┐
│ ← AI Policy for African Union                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Domain Structure (Proposed)                                     │
│  ────────────────────────────                                    │
│                                                                  │
│  Name: Government AI Policy                                      │
│  Core Question: How to govern AI for development benefit        │
│                 while managing risks and sovereignty?            │
│                                                                  │
│  Vocabulary:                                                     │
│    Concepts → "Policy Frames"                                    │
│    Tensions → "Development Trade-offs"                           │
│    Actors   → "Stakeholders"                                     │
│                                                                  │
│  [Accept Domain] [Modify]                                        │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Suggested Seed Content                                          │
│  ──────────────────────                                          │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ ◉ Policy Frame: "Leapfrog Development"                 │     │
│  │   AI as tool to skip stages of industrial development  │     │
│  │                                                         │     │
│  │   [ ] Accept  [ ] Reject  [Edit]                       │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ ◉ Trade-off: "Innovation ↔ Protection"                 │     │
│  │   Enabling AI adoption vs protecting vulnerable groups │     │
│  │                                                         │     │
│  │   [ ] Accept  [ ] Reject  [Edit]                       │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│                                    [Skip Seeds] [Accept All →]  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Main Project View
```
┌─────────────────────────────────────────────────────────────────┐
│ ← AI Policy for African Union                    [Settings] [?] │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────┐  ┌─────────────────┐  │
│  │ Framework                             │  │ Q&A Dialogue    │  │
│  │                                       │  │                 │  │
│  │ Policy Frames (4)            [+ Add]  │  │ ┌─────────────┐ │  │
│  │ ┌──────────────────────────────────┐  │  │ │ Ask me      │ │  │
│  │ │ Leapfrog Development         [⋮] │  │  │ │ anything... │ │  │
│  │ │ AI as tool to skip stages...     │  │  │ └─────────────┘ │  │
│  │ └──────────────────────────────────┘  │  │     [Ask →]     │  │
│  │ ┌──────────────────────────────────┐  │  │                 │  │
│  │ │ Sovereignty First            [⋮] │  │  │ ─────────────── │  │
│  │ │ Control over AI systems...       │  │  │                 │  │
│  │ └──────────────────────────────────┘  │  │ Recent:         │  │
│  │ ┌──────────────────────────────────┐  │  │                 │  │
│  │ │ Inclusive Transition         [⋮] │  │  │ ▸ What actors   │  │
│  │ │ Managing employment effects...   │  │  │   should we     │  │
│  │ └──────────────────────────────────┘  │  │   consider?     │  │
│  │                                       │  │                 │  │
│  │ Trade-offs (2)               [+ Add]  │  │ ▸ How does the  │  │
│  │ ┌──────────────────────────────────┐  │  │   informal      │  │
│  │ │ Innovation ↔ Protection      [⋮] │  │  │   economy fit?  │  │
│  │ └──────────────────────────────────┘  │  │                 │  │
│  │                                       │  │ Suggestions:    │  │
│  │ Stakeholders (3)             [+ Add]  │  │ ▸ Add actor:    │  │
│  │ ┌──────────────────────────────────┐  │  │   "Big Tech"    │  │
│  │ │ AU Commission                [⋮] │  │  │ ▸ Explore the   │  │
│  │ └──────────────────────────────────┘  │  │   data access   │  │
│  │                                       │  │   question      │  │
│  └──────────────────────────────────────┘  └─────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Success Criteria

### MVP Complete When:

1. **Project lifecycle works:**
   - [ ] Can create project with brief
   - [ ] Can view project list
   - [ ] Can delete project

2. **Domain bootstrapping works:**
   - [ ] LLM generates domain from brief
   - [ ] User can review and accept domain
   - [ ] User can accept/reject seed content

3. **Unit management works:**
   - [ ] Can create Concept units
   - [ ] Can create Dialectic units
   - [ ] Can create Actor units
   - [ ] Can view unit list
   - [ ] Can edit units
   - [ ] Can delete units

4. **Q&A dialogue works:**
   - [ ] Can ask questions about framework
   - [ ] Responses are framework-aware
   - [ ] Suggested actions are actionable
   - [ ] Can execute suggested actions

5. **Data persists:**
   - [ ] Projects survive server restart
   - [ ] Units survive server restart
   - [ ] Dialogue history persists

---

## Out of Scope (Phase 1)

- Evidence/PDF upload (Phase 2)
- Fragment extraction (Phase 2)
- Friction detection (Phase 3)
- Multi-grid analysis (Phase 3)
- Epistemic status tracking (Phase 3)
- External literature API
- Multi-user / auth
- Export functionality
- Real-time collaboration

---

## Dependencies

```
# requirements.txt
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.0
aiosqlite>=0.19.0
pydantic>=2.5.0
jinja2>=3.1.0
anthropic>=0.7.0
python-multipart>=0.0.6
pyyaml>=6.0
httpx>=0.25.0
```

---

## Next Steps After Plan Approval

1. Create project scaffolding (Step 1)
2. Implement project CRUD (Step 2)
3. Integrate Claude API (Step 3)
4. Build domain bootstrapping (Step 4)
5. Implement unit management (Step 5)
6. Create Q&A dialogue (Step 6)
7. Polish and test (Step 7)

Estimated implementation: ~6-8 focused coding sessions.

Ready to begin?
