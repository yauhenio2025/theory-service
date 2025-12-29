# Strategizer v2: Structure Discovery First

**Date:** 2025-12-29
**Status:** Design Proposal
**Core Insight:** Structure is never given - it must be discovered ASAP

---

## The Problem with Strategizer v1

The current system assumes structure exists and then:
1. Bootstraps a domain from a brief
2. Creates units within that domain
3. Detects tensions between units
4. Resolves tensions

**The sorcery:** We take the bootstrapped structure as given. But structure is NEVER given - it must be discovered. And speed of discovery matters because:

- Structure enables abductive gap-finding
- Gaps enable structure remaking
- This cycle IS the value proposition

---

## The Multi-Dimensional Space of User Needs

Users don't just exist in a "domain." They exist at the intersection of:

### Dimension 1: DOMAIN
What field/area is this in?
- Writing/Essays
- Foundation Strategy
- Investment Analysis
- Policy Development
- Brand Strategy
- Research Programs
- Personal Planning
- Organizational Design
- ...

### Dimension 2: ARTIFACT TYPE
What are you producing?

| Domain | Possible Artifact Types |
|--------|------------------------|
| Writing | Op-ed (800w), Long Essay (5K-30K), Book Chapter, Blog Post, Academic Paper |
| Foundation | Strategy Document, Grant Proposal, Theory of Change, Portfolio Review, Impact Assessment |
| Investment | Investment Memo, Due Diligence Report, Market Analysis, Portfolio Construction, Exit Analysis |
| Policy | Policy Brief, White Paper, Regulatory Analysis, Stakeholder Map, Implementation Plan |

**Key insight:** Same domain, DIFFERENT grids based on artifact type.

### Dimension 3: USER SITUATION
Where are you starting from?
- **Blank Slate:** No prior work, need to discover everything
- **Refining Existing:** Have materials, need to improve/extend
- **Pivoting:** Have structure but it's wrong, need to remake
- **Scaling:** Have working approach, need to systematize
- **Auditing:** Have completed work, need to verify/validate

### Dimension 4: SUPPORT TYPE
What kind of help do you need?
- **Structure Discovery:** What should the framework even look like?
- **Gap Identification:** What's missing from current structure?
- **Content Generation:** Fill in the structure with substance
- **Tension Resolution:** Resolve contradictions within structure
- **Validation:** Stress-test existing structure against challenges

---

## The META-GRID Concept

A META-GRID is not a grid FOR content - it's a grid ABOUT the project structure itself.

### META-GRID Dimensions

**Rows: Structural Elements**
- Domain Identity (Is it clear what domain we're in?)
- Artifact Specification (Is the target artifact well-defined?)
- Core Question (Is the driving question articulated?)
- Key Units (Are the main concepts/tensions/actors identified?)
- Relationships (Are unit relationships mapped?)
- Evidence Base (Is there grounding material?)
- Gaps (Are known unknowns catalogued?)
- Success Criteria (Is "done" defined?)

**Columns: Status Assessment**
- Absent (Not yet addressed)
- Emerging (Partially formed)
- Stable (Well-established)
- Needs Revision (Exists but problematic)

### META-GRID as Compass

The META-GRID tells you:
1. **Where you are:** What structural elements exist
2. **What's missing:** Gaps in the structure
3. **What needs work:** Elements that exist but are problematic
4. **What's next:** Priority actions for structure development

```
┌────────────────────┬────────┬──────────┬────────┬───────────────┐
│ Structural Element │ Absent │ Emerging │ Stable │ Needs Revision│
├────────────────────┼────────┼──────────┼────────┼───────────────┤
│ Domain Identity    │        │          │   ✓    │               │
│ Artifact Spec      │        │    ✓     │        │               │
│ Core Question      │   ✓    │          │        │               │
│ Key Concepts       │        │    ✓     │        │               │
│ Key Tensions       │   ✓    │          │        │               │
│ Key Actors         │        │          │   ✓    │               │
│ Relationships      │   ✓    │          │        │               │
│ Evidence Base      │        │    ✓     │        │               │
│ Known Gaps         │        │          │        │      ✓        │
│ Success Criteria   │   ✓    │          │        │               │
└────────────────────┴────────┴──────────┴────────┴───────────────┘
```

This META-GRID is the FIRST thing we generate, and it drives all subsequent work.

---

## Rapid Structure Discovery Protocol

### Phase 0: Arrival Classification (30 seconds)

**Quick questions:**
1. What domain is this? (dropdown or detected from brief)
2. What are you producing? (artifact type selector)
3. Where are you starting from? (situation radio)
4. What do you need most? (support type radio)

**Output:** Need Classification Vector
```json
{
  "domain": "foundation_strategy",
  "artifact_type": "theory_of_change",
  "situation": "blank_slate",
  "support_type": "structure_discovery"
}
```

### Phase 1: Material Intake (1-5 minutes)

Based on situation:

| Situation | Intake Actions |
|-----------|----------------|
| Blank Slate | Brief description, reference materials, aspirations |
| Refining Existing | Upload current draft, identify pain points |
| Pivoting | Upload what exists, explain why it's wrong |
| Scaling | Upload working examples, articulate patterns |
| Auditing | Upload complete work, identify concerns |

### Phase 2: META-GRID Generation (30 seconds)

LLM analyzes intake materials and generates:
1. Initial META-GRID assessment
2. Priority gaps
3. Recommended next questions

### Phase 3: Targeted Interrogation (2-10 minutes)

**Adaptive questioning based on META-GRID gaps:**

For each "Absent" element:
- Ask discovery questions
- Offer multiple-choice scaffolds (leverage LLM training data)
- Accept uploads that might contain answers

For each "Emerging" element:
- Ask clarification questions
- Offer completion suggestions

For each "Needs Revision" element:
- Surface the problem
- Offer revision paths

### Phase 4: Structure Proposal (30 seconds)

Based on:
- Need Classification Vector
- Intake Materials
- Interrogation Answers
- Artifact-Type-Specific Best Practices

Generate:
1. **Proposed Grid Architecture** - What grids should exist?
2. **Proposed Unit Types** - What kinds of things will we track?
3. **Proposed Workflow** - What's the sequence of work?

### Phase 5: Structure Negotiation (1-5 minutes)

User reviews proposed structure:
- Accept as-is
- Modify specific elements
- Reject and re-interrogate

---

## Artifact-Type-Aware Grid Generation

### The Key Innovation

Different artifact types within the same domain require DIFFERENT grids.

**Example: Writing Domain**

| Artifact Type | Key Grids |
|---------------|-----------|
| Op-Ed (800w) | HOOK, ARGUMENT, COUNTER, CALL_TO_ACTION |
| Long Essay (30K) | THROUGHLINE, CHAPTER_STRUCTURE, EVIDENCE_MAP, VOICE |
| Academic Paper | LITERATURE_REVIEW, METHODOLOGY, FINDINGS, LIMITATIONS |
| Blog Post | HOOK, LISTICLE_OR_NARRATIVE, TAKEAWAY, CTA |

**Example: Foundation Strategy Domain**

| Artifact Type | Key Grids |
|---------------|-----------|
| Theory of Change | PROBLEM_SPACE, INTERVENTION_LOGIC, OUTCOME_CHAIN, ASSUMPTIONS |
| Grant Proposal | NEED_STATEMENT, APPROACH, CAPACITY, BUDGET_NARRATIVE |
| Portfolio Review | INVESTMENT_THESIS, PORTFOLIO_MAP, PERFORMANCE, GAPS |
| Exit Strategy | SUSTAINABILITY_PLAN, TRANSITION_TIMELINE, RISK_MITIGATION |

### LLM Training Data as Best Practice Repository

The LLM knows structural regularities:
- What sections are typical for each artifact type
- What analytical frameworks apply
- What common pitfalls exist
- What distinguishes good from mediocre examples

**We extract this through structured prompting:**

```
For a {artifact_type} in the {domain} domain:

1. What are the essential structural elements?
2. What analytical grids would help organize thinking?
3. What are the 3 most common failure modes?
4. What distinguishes excellent from mediocre examples?
5. What questions should we ask to discover the right structure?

Based on your training on examples of excellent {artifact_type} work...
```

---

## The Abductive Cycle

Once initial structure exists:

```
┌─────────────────────────────────────────────────────────────┐
│                    ABDUCTIVE CYCLE                           │
│                                                              │
│   STRUCTURE                                                  │
│      │                                                       │
│      ▼                                                       │
│   META-GRID AUDIT ──────► Reveals GAPS                      │
│      │                         │                             │
│      │                         ▼                             │
│      │                    Gap Analysis                       │
│      │                         │                             │
│      │                         ▼                             │
│      │              STRUCTURE MODIFICATION                   │
│      │                         │                             │
│      └─────────────────────────┘                             │
│                                                              │
│   This cycle runs continuously, not just at friction points │
└─────────────────────────────────────────────────────────────┘
```

### Cycle Triggers

1. **Scheduled Audits:** Every N content additions, re-run META-GRID
2. **User-Initiated:** "Audit my structure" button
3. **Anomaly Detection:** Content that doesn't fit existing grids
4. **Completion Milestones:** After each phase, verify structure still fits

---

## Implementation Options

### Option A: Enhance Strategizer v1

**Add to existing system:**
- New "Structure Discovery" phase before domain bootstrap
- META-GRID concept as project-level entity
- Multi-dimensional need routing at project creation
- Artifact-type selector driving grid recommendations

**Pros:** Preserves grid refinement, cell actions, notes, dialectic spawning
**Cons:** Existing architecture may constrain; "domain" concept is baked in

### Option B: New Project (Strategizer v2)

**Fresh implementation in `/home/evgeny/projects/strategizer-v2/`:**
- Structure discovery as the core loop
- META-GRID from the start
- Artifact-type-aware everything
- Import v1 innovations (grid refinement, cell actions) as modules

**Pros:** Clean architecture, no legacy constraints
**Cons:** Significant rebuild effort, risk losing innovations

### Option C: Hybrid Approach

**New "Structure Discovery" service that:**
- Runs before Strategizer v1
- Outputs a Structure Specification
- V1 system consumes that specification
- META-GRID lives in new service, content work in v1

**Pros:** Best of both worlds, incremental
**Cons:** Integration complexity, two systems to maintain

---

## Recommended: Option B with Import Strategy

### Rationale

1. **The core insight is architectural** - Structure discovery should be PRIMARY, not bolted on
2. **Clean slate enables** - No fighting existing assumptions
3. **Import strategy preserves** - Grid refinement, cell actions, notes, dialectic spawning can all be imported as modules
4. **Speed matters** - Fresh implementation might actually be faster than refactoring

### Import Strategy

From Strategizer v1, import as modules:
- Grid refinement parameters (axis manipulation, granularity)
- Cell action system (single/multi-cell actions)
- Predicament notes and dialectic spawning
- Extended thinking integration patterns
- Evidence confidence routing

### New in v2

- META-GRID as first-class entity
- Multi-dimensional need classification
- Artifact-type-aware grid generation
- Abductive audit cycling
- Structure proposal/negotiation flow

---

## Prototype Scope (MVP)

### Must Have
1. **Arrival Classification** - 4-dimension need vector
2. **META-GRID Generation** - Basic structural audit
3. **Structure Proposal** - Artifact-type-aware grid recommendations
4. **Basic Content Work** - Create units, fill grids
5. **Audit Trigger** - Manual "audit structure" action

### Nice to Have
1. Adaptive interrogation based on META-GRID gaps
2. Upload analysis for situation detection
3. Automatic audit scheduling
4. Structure modification suggestions

### Import Later
1. Grid refinement (from v1)
2. Cell actions (from v1)
3. Evidence integration (from v1)
4. Coherence monitoring (from v1)

---

## Next Steps

1. **Create `/home/evgeny/projects/strategizer-v2/`** - Fresh project folder
2. **Implement Arrival Classification** - Multi-dimensional need assessment
3. **Implement META-GRID** - Basic structural audit grid
4. **Implement Artifact-Type Grid Registry** - Known grids per artifact type
5. **Implement Structure Proposal** - LLM-driven structure recommendation
6. **Basic Content Work** - Simple unit/grid CRUD
7. **Test with real use case** - Foundation strategy or writing domain

---

## Appendix: Example Flow

### User: Foundation wanting Theory of Change

**Phase 0: Classification**
```
Domain: Foundation Strategy
Artifact: Theory of Change
Situation: Blank Slate
Support: Structure Discovery
```

**Phase 1: Intake**
```
User uploads:
- Rough notes about climate adaptation focus
- Existing mission statement
- List of current grantees
```

**Phase 2: META-GRID Generated**
```
Domain Identity: Stable (climate adaptation foundation)
Artifact Spec: Emerging (ToC, but scope unclear)
Core Question: Absent
Key Concepts: Emerging (climate, adaptation, resilience mentioned)
Key Tensions: Absent
Key Actors: Stable (grantees listed)
Relationships: Absent
Evidence Base: Emerging (some materials)
Known Gaps: Absent
Success Criteria: Absent
```

**Phase 3: Interrogation**

Q1: "Your materials mention climate adaptation but don't specify geography. Is this global, regional, or local focus?"
→ User: "Regional - Southeast Asia"

Q2: "A Theory of Change needs a core question. Which best captures your focus?"
- [ ] "How can philanthropic capital accelerate climate adaptation in SE Asia?"
- [ ] "What interventions most effectively build community resilience?"
- [ ] "How do we bridge the adaptation finance gap for vulnerable populations?"
- [ ] Write my own...
→ User selects option 2

Q3: "What tensions do you anticipate navigating?"
- [ ] Speed of deployment ↔ Depth of community engagement
- [ ] Scale of impact ↔ Attribution of outcomes
- [ ] Proven interventions ↔ Innovative approaches
- [ ] Donor expectations ↔ Grantee autonomy
→ User selects 1 and 3

**Phase 4: Structure Proposal**
```
Recommended Grid Architecture for Theory of Change:

TIER 1 (Required):
- PROBLEM_SPACE: The problem you're solving
- INTERVENTION_LOGIC: Your theory of how change happens
- OUTCOME_CHAIN: Short → Medium → Long term outcomes
- ASSUMPTIONS: What must be true for this to work

TIER 2 (Recommended for your focus):
- ACTOR_MAP: Who does what in your theory
- EVIDENCE_BASE: What supports your intervention logic
- RISK_REGISTER: What could derail the theory

TIER 3 (Optional):
- MEASUREMENT_FRAMEWORK: How you'll know it's working
- LEARNING_AGENDA: What you need to learn

Accept this structure? [Yes] [Modify] [Start Over]
```

**Phase 5: Structure Negotiation**
→ User: "Add a GEOGRAPHIC_CONTEXT grid for the SE Asia specifics"
→ System adds, user accepts

**Proceed to Content Work with discovered structure**

---

*This document proposes a fundamental rearchitecture. Implementation in new project folder recommended.*
