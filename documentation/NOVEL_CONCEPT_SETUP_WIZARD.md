# Novel Concept Setup Wizard

## Overview

This document describes the design of the **Concept Setup Wizard** - a structured knowledge elicitation system for introducing novel concepts that don't exist in public discourse.

### The Problem

When introducing a novel concept:
- LLMs have no training data about it
- Cannot find examples in documents
- Will try to assimilate it to familiar concepts (collapsing distinctions)
- Will hallucinate connections that don't exist

### The Solution

A **staged adaptive wizard** that:
1. Extracts user knowledge through structured Q&A
2. Populates the Genesis dimension tables
3. Creates recognition markers for document search
4. Enables targeted LLM analysis of source documents
5. Signals gaps and requests additional user input

---

## Philosophical Foundations

### Design Principles (from tool-ideator knowledge base)

| Principle ID | Name | Application |
|-------------|------|-------------|
| `prn_staged_adaptive_interrogation` | Staged Adaptive Interrogation | Questions build on previous answers; later stages adapt |
| `prn_theory_grounded_extraction` | Theory-Grounded Extraction | User inputs gain power through theoretical framing |
| `prn_proactive_insufficiency_signaling` | Proactive Insufficiency Signaling | LLM explicitly signals when it lacks data |
| `prn_precision_forcing_interrogation` | Precision-Forcing Interrogation | Questions designed to force definitional precision |
| `prn_forward_staged_data_harvesting` | Forward-Staged Data Harvesting | Capture data for later pipeline stages |
| `prn_embodied_decision_substrate` | Embodied Decision Substrate | Concrete material for decisions, not abstractions |
| `prn_formalization_as_education` | Formalization as Education | Process of answering builds user's own understanding |

### Feature Patterns

| Feature | Application |
|---------|-------------|
| `progressive-batch-interrogation-pattern` | Questions in meaningful batches, not all at once |
| `multiple-choice-with-escape-valve-pattern` | MC options + "Other" for unexpected answers |
| `llm-driven-diagnostic-questioning` | LLM generates follow-up questions based on gaps |
| `conversation-guided-extraction-targeting` | Conversation history guides what to extract next |
| `document-collection-staging-without-processing` | Register docs now, process later with context |

---

## Wizard Stages

### Stage 1: Genesis and Identity

**Goal:** Capture the origin story and basic identity of the concept.

**Questions:**
1. **Genesis Type** (MC): How would you characterize the origin of this concept?
   - Theoretical innovation
   - Empirical discovery
   - Synthetic unification
   - Paradigm shift
   - Other (elaborate)

2. **Concept Name** (Open): What is the name of your concept?

3. **Core Definition** (Open): In one paragraph, provide your working definition.

4. **Theoretical Lineage** (Open): What intellectual traditions does this build on?

**Populates:** `concept_genesis`, `concepts` tables

---

### Stage 2: Problem Space

**Goal:** Articulate WHY this concept needs to exist.

**Questions:**
1. **Gap Description** (Open): What problem or gap in understanding does this concept address?

2. **Failed Alternatives** (Open): What existing concepts have you tried? Why are they inadequate?

3. **Problem Domains** (Multi-select): Where is this gap most felt?
   - Academic research
   - Policy analysis
   - Industry practice
   - Public discourse
   - Other

4. **Urgency** (Open): Why address this now?

**Populates:** `concept_problem_space` table

---

### Stage 3: Differentiation

**Goal:** Define concept boundaries by contrast with similar concepts.

**Questions:**
1. **Most Confused With** (Open): What existing concept is this MOST likely to be confused with?

2. **Confusion Consequence** (Open): Why is this confusion problematic? What understanding is lost?

3. **Additional Contrasts** (Repeatable): List other concepts to differentiate from.
   - Concept name
   - Type of confusion (subset, superset, synonym, false opposition)
   - Key distinction

**Populates:** `concept_differentiation` table

**LLM Assistance:** After user input, LLM can suggest additional potential confusions based on the definition.

---

### Stage 4: Implicit Domains and Paradigmatic Cases

**Goal:** Map where the concept operates without being named, and provide exemplary instances.

**Questions:**
1. **Paradigmatic Case** (Open): What is the single best example that captures the essence?

2. **Why Paradigmatic** (Open): What makes this example exemplary?

3. **Implicit Domain** (Repeatable): Where do you see this concept operating without being named?
   - Domain name
   - Domain type (academic, policy, industry, media, everyday)
   - Proxy terms used instead
   - Why proxies are inadequate

**Populates:** `concept_paradigmatic_cases`, `concept_implicit_domains` tables

---

### Stage 5: Foundational Claims

**Goal:** Articulate the claims about reality that the concept makes.

**Questions:**
1. **Core Claim** (Open): What is the most fundamental claim your concept makes?

2. **Claim Type** (MC): What kind of claim is this?
   - Ontological (what exists)
   - Causal (what causes what)
   - Normative (what should be)
   - Methodological (how to investigate)

3. **Falsification Condition** (Open): What would prove this concept useless or wrong?

4. **Additional Claims** (Repeatable): Other claims the concept makes.

**Populates:** `concept_foundational_claims` table

---

### Stage 6: Recognition Markers

**Goal:** Create patterns for finding implicit instances in documents.

**Questions:**
1. **Recognition Pattern** (Open): How can we recognize an implicit instance in text that doesn't use the term?

2. **Linguistic Markers** (Open): What linguistic patterns indicate this concept is in play?

3. **Structural Markers** (Open): What structural features would an instance have?

4. **False Positive Risk** (Open): What might LOOK like this concept but isn't?

**Populates:** `concept_recognition_markers` table

---

### Stage 7: Source Documents

**Goal:** Queue documents for targeted analysis.

**Questions:**
1. **Document Reference** (Repeatable): Point to documents where you believe implicit instances exist.
   - Document type (academic paper, policy doc, news article, etc.)
   - Citation/URL
   - Relevance note
   - Expected instances
   - Specific sections to focus on
   - Priority (1-5)

**Populates:** `concept_source_pointers` table

---

## Adaptive Branching Logic

### Question Dependencies

```
genesis_type = "other"
  └─→ genesis_type_elaborate (follow-up)

most_confused_with = [any]
  └─→ LLM generates: "Based on your definition, you might also be confused with [X]. Should we add differentiation?"

implicit_domain added
  └─→ Generate suggested search patterns from proxy_terms
  └─→ Offer to add recognition markers for this domain

paradigmatic_case provided
  └─→ LLM extracts features from case
  └─→ "Your case exhibits these features: [list]. Are these central to the concept?"
```

### LLM-Driven Follow-ups

After each stage, LLM analyzes responses and may generate:
1. **Clarification questions:** "You mentioned X - can you elaborate?"
2. **Consistency checks:** "Earlier you said Y, but this seems to conflict with Z"
3. **Gap identification:** "I notice you haven't addressed [dimension]. Is this intentional?"
4. **Suggestion prompts:** "Based on your definition, consider also differentiating from [concept]"

---

## Proactive Insufficiency Signaling

### What It Is

The LLM explicitly signals when it doesn't have enough information to:
- Populate a schema field
- Find implicit instances
- Generate meaningful analysis

### Implementation

After wizard completion, LLM generates a **Gap Report**:

```markdown
## Schema Population Status

### Well-Populated (High Confidence)
- concept_genesis: 95% complete
- concept_differentiation: 3 contrasts defined
- concept_paradigmatic_cases: 1 detailed case

### Needs More Input (Medium Confidence)
- concept_implicit_domains: Only 2 domains mapped
  - SUGGESTION: Consider adding domains in [industry, media]
- concept_recognition_markers: 3 markers defined
  - SUGGESTION: Add markers for [situational, behavioral] types

### Cannot Populate Without Help (Low Confidence)
- concept_claims (normative): No normative claims defined
  - QUESTION: Does this concept have normative implications?
- concept_implicit_domains (everyday): No everyday domain
  - QUESTION: Do ordinary people encounter this phenomenon?

### Document Processing Blockers
- Cannot search for instances without:
  - [ ] At least 3 recognition markers
  - [ ] At least 1 proxy term per domain
  - [ ] At least 1 queued source document
```

---

## Document Processing Pipeline

### Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Source         │     │  Recognition     │     │  Extracted      │
│  Pointers       │────▶│  Markers         │────▶│  Instances      │
│  (staged docs)  │     │  (search patterns)│     │  (schema data)  │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

### Processing Steps

1. **Document Retrieval**
   - Fetch document from reference (URL, file, or manual upload)
   - Convert to processable format

2. **Targeted Search**
   - Use recognition markers to identify candidate passages
   - Focus on user-specified sections if provided
   - Apply proxy term searches

3. **LLM Analysis**
   - For each candidate passage:
     - Does this exhibit the concept? (confidence score)
     - Which features does it demonstrate?
     - Is it explicit or implicit usage?
     - Extract relevant claims/evidence

4. **Schema Population**
   - Map extracted data to appropriate tables
   - Set source_type = 'evidence_testing'
   - Link to source document

5. **Feedback Loop**
   - Report what was found
   - Signal if no instances found (may indicate poor markers)
   - Suggest marker refinements

### LLM Prompt for Document Analysis

```
You are analyzing a document for implicit instances of the concept "{concept_name}".

CONCEPT DEFINITION:
{core_definition}

RECOGNITION MARKERS:
{markers_list}

PROXY TERMS TO LOOK FOR:
{proxy_terms}

WHAT THIS CONCEPT IS NOT:
{differentiations}

DOCUMENT SECTION:
{document_text}

TASK:
1. Identify passages that exhibit this concept (explicitly or implicitly)
2. For each passage:
   - Quote the relevant text
   - Explain why it exhibits the concept
   - Rate confidence (high/medium/low)
   - Note which markers triggered identification
   - Extract any claims or evidence
3. Note any near-misses (passages that ALMOST exhibit the concept but don't)
4. If no instances found, explain why and suggest marker refinements

OUTPUT FORMAT:
{structured_json_schema}
```

---

## UI/UX Design Recommendations

### Wizard Interface

1. **Progress Indicator**: Show current stage and completion percentage

2. **Save and Resume**: Allow partial completion, save progress

3. **Question Batching**: Show 2-3 questions at a time, not entire stage

4. **Inline Help**: Each question has expandable help text and example

5. **LLM Assistant Panel**: Side panel showing:
   - Real-time suggestions
   - Consistency notes
   - Gap warnings

6. **Schema Preview**: Visual representation of schema being populated

### Post-Wizard Dashboard

1. **Schema Completeness Map**: Visual showing populated vs. empty areas

2. **Document Queue**: List of staged documents with processing status

3. **Instance Feed**: Stream of extracted instances as they're found

4. **Gap Alerts**: Prominent display of areas needing attention

5. **Refinement Suggestions**: LLM-generated suggestions for improvement

---

## Example Walkthrough: "Technological Sovereignty"

### Stage 1 Responses

**Q: How would you characterize the origin?**
A: Theoretical innovation

**Q: What is the name?**
A: Technological Sovereignty

**Q: Working definition?**
A: Technological sovereignty refers to the capacity of a political entity to exercise meaningful control over the technological systems upon which its economy, security, and social functioning depend...

**Q: Theoretical lineage?**
A: Builds on sovereignty theory (Bodin, Schmitt), technology studies (Winner, Feenberg), and critical infrastructure studies

### LLM Response (Post-Stage 1)

```
✓ Genesis captured: theoretical_innovation
✓ Definition: 156 words, references political entity, control, technological systems

SUGGESTIONS:
- Your definition mentions "political entity" - consider clarifying whether
  this applies to sub-national entities (states, cities) or only nation-states
- You reference sovereignty theory - should we add Foucault's
  governmentality as a contrast?

NEXT: Let's explore why existing concepts are inadequate (Stage 2)
```

### Stage 4 Responses

**Q: Single best example?**
A: The European 5G and Huawei dilemma. European nations faced decisions about allowing Huawei equipment in their 5G networks...

**Q: Implicit domain?**
A: Semiconductor Policy - discussions of "supply chain security," "strategic autonomy," "onshoring" all circle around technological sovereignty without naming it

### LLM Response (Post-Stage 4)

```
✓ Paradigmatic case: Huawei 5G dilemma
  - Features identified: infrastructure dependency, surveillance risk,
    forced choice, sovereignty-efficiency tradeoff

✓ Implicit domain: Semiconductor Policy
  - Proxy terms captured: supply chain security, strategic autonomy,
    onshoring, friend-shoring, de-risking

GENERATED RECOGNITION MARKERS:
Based on your proxy terms, I've created these search patterns:
1. (supply chain) AND (security OR resilience) AND (strategic OR autonomy)
2. (semiconductor OR chip) AND (dependency OR vulnerability)
3. (onshoring OR reshoring) AND (critical OR strategic)

Should I add these to the recognition markers table?

GAP ALERT:
- Only 1 implicit domain mapped
- Recommend adding: Cloud Computing, AI Development, Telecommunications
```

### Document Processing Example

**Queued Document:** European Commission (2020). "Shaping Europe's Digital Future"

**Processing Output:**

```
FOUND 7 IMPLICIT INSTANCES

Instance 1 (Confidence: HIGH)
Page 12: "Europe must have the capacity to make its own choices, based on
its own values, respecting its own rules. This requires building Europe's
technological capacities in critical areas..."
- Marker triggered: strategic autonomy framing
- Features: capacity for choice, technology-values link, critical areas
- Implicit usage: says "technological capacities" not "technological sovereignty"

Instance 2 (Confidence: HIGH)
Page 18: "Strategic autonomy in technology is not about closing off Europe
but about ensuring we can compete fairly in global markets without
depending on others for critical technologies..."
- Marker triggered: explicit "strategic autonomy in technology"
- Features: competitive framing, dependency concern
- Near-explicit: very close to concept but doesn't use exact term

Instance 3 (Confidence: MEDIUM)
Page 24: "Data and AI are resources that should be built and used in Europe
in a way that is consistent with European values..."
- Marker triggered: European values + technology
- Features: sovereignty over data, value-alignment
- Caution: Could be just data sovereignty, not full tech sovereignty

[4 more instances...]

SUMMARY:
- 5 high-confidence instances
- 2 medium-confidence instances
- Document strongly exhibits concept without naming it
- Primary framing: "strategic autonomy" and "technological capacities"

SCHEMA UPDATES:
- Added 3 quotes to concept_evidence table
- Updated proxy_terms with "technological capacities"
- Added EU policy as explicit domain
```

---

## Technical Implementation Notes

### Database Schema

The wizard populates these tables (see `genesis_dimension_migration.sql`):

| Table | Populated By |
|-------|-------------|
| `concepts` | Stage 1 (name, definition) |
| `concept_genesis` | Stage 1 |
| `concept_problem_space` | Stage 2 |
| `concept_differentiation` | Stage 3 |
| `concept_paradigmatic_cases` | Stage 4 |
| `concept_implicit_domains` | Stage 4 |
| `concept_foundational_claims` | Stage 5 |
| `concept_recognition_markers` | Stage 6 |
| `concept_source_pointers` | Stage 7 |
| `concept_user_elaborations` | All stages (raw responses) |

### API Endpoints

```
POST   /concepts/wizard/start
       Start new wizard session, return session_id

POST   /concepts/wizard/{session_id}/stage/{stage}
       Submit stage responses, get LLM feedback

GET    /concepts/wizard/{session_id}/status
       Get current progress, gaps, suggestions

POST   /concepts/wizard/{session_id}/complete
       Finalize wizard, trigger gap report

POST   /concepts/{id}/documents/queue
       Add document to processing queue

POST   /concepts/{id}/documents/{doc_id}/process
       Trigger document processing

GET    /concepts/{id}/schema-status
       Get population completeness map
```

### LLM Integration Points

1. **Post-stage analysis**: After each stage submission
2. **Gap detection**: Continuous monitoring of schema completeness
3. **Marker generation**: Auto-generate from proxy terms
4. **Document processing**: Targeted instance extraction
5. **Follow-up generation**: Context-aware clarification questions

---

## Success Metrics

### Wizard Completion

- Average time to complete: Target 30-45 minutes
- Stage abandonment rate: Target < 20%
- Questions requiring clarification: Target < 30%

### Schema Population

- Minimum viable: 70% of Genesis tables populated
- Target: 90% population after wizard + 1 document
- Gap resolution rate: 80% of flagged gaps addressed

### Document Processing

- Instance precision: > 80% confirmed by user
- Instance recall: Find > 70% of instances human would find
- False positive rate: < 20%

---

## Future Enhancements

1. **Multi-user Concept Development**: Multiple users contribute to same concept
2. **Concept Versioning**: Track how concept evolves over time
3. **Cross-concept Analysis**: Identify relationships between concepts
4. **Training Data Generation**: Use populated schemas to train specialized models
5. **Community Validation**: Allow domain experts to validate instances

---

## Appendix: Question Bank Reference

See `wizard_question_bank` table in `genesis_dimension_migration.sql` for full question definitions including:
- Question IDs
- Validation rules
- Dependencies
- Table/column mappings
- Help text and examples
