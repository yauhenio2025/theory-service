# Strategizer MVP Implementation Addendum

This addendum captures context from the design sessions that produced STRATEGIZER-IMPLEMENTATION-SPEC.md. A fresh session building the implementation plan should read this alongside the main spec and features-log.md.

---

## 1. What We're Building

An LLM-powered strategic thinking tool that helps users:
1. **Bootstrap a domain** from a project brief (any domain, not just the 5 examples)
2. **Build strategic frameworks** through Q&A dialogue
3. **Integrate evidence** (academic articles, news, reports) into the emerging framework
4. **Detect and resolve friction** when evidence challenges the framework

The system should feel like a thinking partner, not a form to fill out.

---

## 2. Reference Implementation: Essay Flow Evidence Stage

The essay-flow app at `/home/evgeny/projects/asc/` demonstrates how evidence integration should work. Key patterns to adopt:

### Evidence Upload Flow
- **Add Source / Batch Add Sources** — Upload PDFs (academic articles, news, reports)
- **Process All Pending** — Extract fragments from uploaded PDFs
- **Fragment Management** — Each PDF becomes multiple fragments (quotes, claims, data points)

### Evidence Integration Tabs
| Tab | Purpose |
|-----|---------|
| Sources & Fragments | Raw uploaded PDFs and their extracted fragments |
| Auto-Integrated | High-confidence matches auto-assigned to framework slots |
| Pending Decisions | Ambiguous fragments that need user judgment |
| Batch Processing | Process multiple fragments at once |
| Skeleton Preview | See how evidence affects the emerging framework |
| Theory Testing | Test framework claims against evidence |

### Key UX Pattern: Auto-Integration Alerts
When new evidence complicates or challenges the framework:
- **Evidence Impact Assessment** — Summary of how new evidence affects existing framework
- **Auto-Integration Alerts** — Specific conflicts that need attention
- **Skeleton Restructuring Suggestions** — Recommendations for framework changes

This is the "friction surfacing" pattern from the spec — users only see things that require their judgment.

---

## 3. MVP Scope

### Phase 1: Domain Bootstrapping + Basic Q&A

**Must Have:**
- Project creation with brief description
- Domain bootstrapping (LLM proposes domain structure from brief)
- Basic unit creation: Concepts, Dialectics, Actors
- Simple Q&A to refine units
- Persistence (SQLite)

**Stub:**
- External literature API (no automatic fetching yet)

### Phase 2: Evidence Integration

**Must Have:**
- PDF upload (single and batch)
- Fragment extraction from PDFs (via LLM)
- Fragment-to-unit matching (which unit does this evidence relate to?)
- Auto-integration for high-confidence matches
- Pending decisions queue for ambiguous evidence
- Basic friction detection (evidence contradicts existing unit)

**Stub:**
- External API integration (manual upload only)

### Phase 3: Friction & Evolution

**Must Have:**
- Friction detection across all unit types
- Friction surfacing with resolution options
- Unit evolution (refine concepts based on evidence)
- Domain evolution (add new unit types, grids as patterns emerge)

---

## 4. Core Design Principles (From Spec)

### LLM-First Philosophy

```
Python gathers data → LLM makes judgments → Python executes decisions
```

**DO:**
- Pass evidence packages to LLM for holistic assessment
- Ask LLM meaningful questions ("Does this evidence challenge the concept?")
- Store LLM decisions as training examples for learning

**DON'T:**
- Hardcode thresholds (no `if confidence > 0.85`)
- Use rule-based pattern matching for conceptual decisions
- Make LLM check arbitrary numeric cutoffs

### Attention-Only-On-Friction UX

```
Users should only see things that require their judgment
```

- **Smooth operations** — Happen in background, no user attention needed
- **Friction operations** — Surface to user with context + resolution options
- **Never ask** — What could be auto-decided
- **Always ask** — When values/commitments are at stake

### Three-Tier Unit System

| Tier | What | Examples | Mutability |
|------|------|----------|------------|
| Universal | Core abstractions any domain needs | Concept, Tension, Agent | Fixed |
| Domain | Domain-specific vocabulary | Thesis (investing), Play (philanthropy) | Evolves slowly |
| Emergent | Project-specific units | Whatever the project needs | Highly mutable |

### Three-Tier Grid System

| Tier | What | Examples |
|------|------|----------|
| Required | Every unit of type X gets these | Identity, Relations |
| Flexible | Domain suggests, user can modify | Methodology (for concepts) |
| Wildcard | User/LLM discovers during work | Whatever emerges |

---

## 5. Key Data Structures

### Project
```python
class Project:
    id: str
    name: str
    brief: str  # Original project description
    domain: DomainInstantiation  # Bootstrapped or cloned domain
    units: list[Unit]
    grids: list[GridInstance]
    evidence_sources: list[EvidenceSource]
    fragments: list[Fragment]
    friction_events: list[FrictionEvent]
```

### Unit (Abstract)
```python
class Unit:
    id: str
    type: str  # concept, dialectic, actor, etc.
    tier: Tier  # UNIVERSAL, DOMAIN, EMERGENT
    name: str
    definition: str
    status: UnitStatus  # DRAFT, TESTED, CANONICAL
    grids: list[GridInstance]
    evidence_links: list[EvidenceLink]
    version: int
```

### Evidence Source & Fragment
```python
class EvidenceSource:
    id: str
    filename: str
    source_type: str  # pdf, url, manual
    content: str  # Full text
    metadata: dict  # Title, author, date, etc.
    fragments: list[Fragment]

class Fragment:
    id: str
    source_id: str
    content: str  # The extracted quote/claim/data
    fragment_type: str  # quote, claim, data, methodology
    relevance_assessment: dict  # Which units it might relate to
    integration_status: str  # PENDING, AUTO_INTEGRATED, NEEDS_DECISION, RESOLVED
    integration_decision: Optional[IntegrationDecision]
```

### Friction Event
```python
class FrictionEvent:
    id: str
    type: FrictionType  # CONTRADICTION, GAP, AMBIGUITY, TENSION
    severity: str  # LLM-assessed, not hardcoded
    description: str
    affected_units: list[str]
    triggering_evidence: Optional[str]
    resolution_options: list[ResolutionOption]
    status: str  # DETECTED, SURFACED, RESOLVED, DEFERRED
```

---

## 6. Key API Endpoints

### Project Management
```
POST   /api/projects                 # Create project from brief
GET    /api/projects/<id>            # Get project with all data
PUT    /api/projects/<id>            # Update project
```

### Domain & Units
```
POST   /api/projects/<id>/bootstrap  # Bootstrap domain from brief
POST   /api/projects/<id>/units      # Create unit
PUT    /api/projects/<id>/units/<id> # Update unit
GET    /api/projects/<id>/units      # List units
```

### Evidence
```
POST   /api/projects/<id>/evidence/upload     # Upload PDF(s)
POST   /api/projects/<id>/evidence/process    # Extract fragments
GET    /api/projects/<id>/evidence/pending    # Get pending decisions
POST   /api/projects/<id>/evidence/integrate  # Integrate fragment
POST   /api/projects/<id>/evidence/batch      # Batch process
```

### Friction
```
GET    /api/projects/<id>/friction           # Get current friction events
POST   /api/projects/<id>/friction/<id>/resolve  # Resolve friction
```

### Q&A / Dialogue
```
POST   /api/projects/<id>/ask    # Ask question, get framework-aware response
POST   /api/projects/<id>/suggest # Get suggestions for next steps
```

---

## 7. UI Structure (Based on Essay Flow)

### Main Navigation (Stages or Tabs)
1. **Project Setup** — Brief, domain selection/bootstrapping
2. **Core Framework** — Units (concepts, dialectics, actors)
3. **Evidence** — Upload, fragments, integration
4. **Friction** — Detected issues, resolution options
5. **Preview** — Current framework state

### Evidence Stage (Modeled on Essay Flow)

**Top Section:**
- Evidence Impact Assessment (when new evidence uploaded)
- Auto-Integration Alerts
- Skeleton Restructuring Suggestions

**Tab Bar:**
- Sources & Fragments
- Auto-Integrated (N)
- Pending Decisions (N)
- Batch Processing
- Framework Preview
- Testing

**Evidence Sources Panel:**
- List of uploaded PDFs
- "Add Source" / "Batch Add Sources" buttons
- "Process All Pending" button
- Status indicators (PENDING, COMPLETED)

**Stats Bar:**
- Total Fragments
- Auto-Assigned
- Need Decision
- Resolved

---

## 8. LLM Integration Points

### Domain Bootstrapping
**Input:** Project brief
**Output:** MinimalViableDomain (name, vocabulary, seed concepts, suggested grids)

### Fragment Extraction
**Input:** PDF content
**Output:** List of fragments with type classification

### Fragment Relevance Assessment
**Input:** Fragment + existing units
**Output:** Relevance scores + suggested integration targets

### Friction Detection
**Input:** New evidence + current framework state
**Output:** FrictionEvents with severity and resolution options

### Unit Refinement
**Input:** Current unit + refinement request/evidence
**Output:** Updated unit specification

### Dialogue Response
**Input:** User question + framework context
**Output:** Framework-aware response + suggested actions

---

## 9. Technical Stack (Suggested)

- **Backend:** Flask (consistent with essay-flow)
- **Database:** SQLite (simple, file-based)
- **LLM:** Claude API (Anthropic SDK)
- **PDF Processing:** PyPDF2 or pdfplumber for text extraction
- **Frontend:** Vanilla JS + HTML templates (or lightweight framework)

---

## 10. What NOT to Build in MVP

- External literature API integration (stub only)
- Multi-user / authentication
- Real-time collaboration
- Export functionality
- Complex visualizations
- Performance optimization
- Comprehensive error handling

Focus on the core loop: **Project → Domain → Units → Evidence → Friction → Evolution**

---

## 11. Success Criteria for MVP

1. **Can bootstrap a domain** from any project brief
2. **Can create and refine units** through Q&A
3. **Can upload PDFs** and extract fragments
4. **Can auto-integrate** high-confidence fragments
5. **Can surface friction** when evidence challenges framework
6. **Can resolve friction** with user input
7. **Framework evolves** based on evidence and user decisions

The MVP is successful if a user can:
- Start with a strategic question in any domain
- Build an initial framework through dialogue
- Upload relevant evidence
- See how evidence affects the framework
- Resolve conflicts and ambiguities
- End up with a more robust framework than they started with
