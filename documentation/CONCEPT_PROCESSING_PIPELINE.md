# Semi-Automated Concept Processing Pipeline

## Overview

This document describes the **processing pipeline** that takes user-provided knowledge about a novel concept and systematically populates the full schema through:

1. **User Knowledge Elicitation** (wizard)
2. **Recognition Marker Generation** (LLM-assisted)
3. **Document Staging** (user-guided)
4. **Targeted Instance Discovery** (LLM processing)
5. **Schema Population** (automated mapping)
6. **Gap Detection and Iteration** (continuous)

---

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         USER KNOWLEDGE PHASE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐               │
│   │   Wizard     │────▶│   Genesis    │────▶│  Recognition │               │
│   │   Q&A        │     │   Tables     │     │  Markers     │               │
│   └──────────────┘     └──────────────┘     └──────────────┘               │
│                                                     │                        │
│                              LLM generates additional markers from proxies   │
│                                                     ▼                        │
│                                            ┌──────────────┐                 │
│                                            │   Marker     │                 │
│                                            │   Bank       │                 │
│                                            └──────────────┘                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                              │
                                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DOCUMENT STAGING PHASE                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   User points to documents          System registers for processing          │
│                                                                              │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐               │
│   │  Document    │────▶│   Source     │────▶│  Processing  │               │
│   │  References  │     │   Pointers   │     │  Queue       │               │
│   └──────────────┘     └──────────────┘     └──────────────┘               │
│         │                                                                    │
│         │ User adds: relevance notes, expected instances, priority           │
│         ▼                                                                    │
│   ┌──────────────┐                                                          │
│   │  Section     │  (optional: focus on specific parts)                     │
│   │  Targeting   │                                                          │
│   └──────────────┘                                                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                              │
                                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DOCUMENT PROCESSING PHASE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐               │
│   │  Document    │────▶│  Chunking    │────▶│  Marker      │               │
│   │  Retrieval   │     │  & Sectioning│     │  Matching    │               │
│   └──────────────┘     └──────────────┘     └──────────────┘               │
│                                                     │                        │
│                                                     ▼                        │
│                                            ┌──────────────┐                 │
│                                            │   LLM        │                 │
│                                            │   Analysis   │                 │
│                                            └──────────────┘                 │
│                                                     │                        │
│                                                     ▼                        │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐               │
│   │  Instance    │◀────│  Confidence  │◀────│  Feature     │               │
│   │  Extraction  │     │  Scoring     │     │  Mapping     │               │
│   └──────────────┘     └──────────────┘     └──────────────┘               │
└─────────────────────────────────────────────────────────────────────────────┘
                                              │
                                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SCHEMA POPULATION PHASE                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Extracted instances map to schema tables                                   │
│                                                                              │
│   ┌────────────────────────────────────────────────────────────────┐        │
│   │                     INSTANCE DATA                               │        │
│   └────────────────────────────────────────────────────────────────┘        │
│              │                    │                    │                     │
│              ▼                    ▼                    ▼                     │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐               │
│   │  Quinean     │     │  Brandomian  │     │  Canguilhem  │               │
│   │  (web of     │     │  (inferential│     │  (vitality   │               │
│   │   belief)    │     │   relations) │     │   status)    │               │
│   └──────────────┘     └──────────────┘     └──────────────┘               │
│                                                                              │
│   source_type = 'evidence_testing'                                          │
│   source_reference = document citation                                       │
│   confidence = LLM confidence score                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                              │
                                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        GAP DETECTION & ITERATION                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐               │
│   │  Schema      │────▶│  Gap         │────▶│  User        │               │
│   │  Audit       │     │  Report      │     │  Prompt      │               │
│   └──────────────┘     └──────────────┘     └──────────────┘               │
│         │                                          │                        │
│         │                                          ▼                        │
│         │                                   ┌──────────────┐                │
│         │                                   │  Iterate     │                │
│         │                                   │  (more docs, │                │
│         │                                   │   more Q&A)  │                │
│         │                                   └──────────────┘                │
│         │                                          │                        │
│         └──────────────────────────────────────────┘                        │
│                              REPEAT UNTIL ADEQUATE                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: User Knowledge Elicitation

### Wizard Stages

| Stage | Focus | Key Outputs |
|-------|-------|-------------|
| 1 | Genesis & Identity | Name, definition, lineage, novelty claim |
| 2 | Problem Space | Gap description, failed alternatives, urgency |
| 3 | Differentiation | Contrasts with existing concepts |
| 4 | Cases & Domains | Paradigmatic examples, implicit domains, proxy terms |
| 5 | Foundational Claims | Core assertions, falsification conditions |
| 6 | Recognition Markers | Patterns for finding implicit instances |
| 7 | Source Documents | Documents queued for processing |

### Quality Gates

Before proceeding to document processing, require:

- [ ] Minimum 100-word definition
- [ ] At least 2 concept differentiations
- [ ] At least 1 paradigmatic case
- [ ] At least 1 implicit domain with proxy terms
- [ ] At least 3 recognition markers
- [ ] At least 1 queued source document

---

## Phase 2: Recognition Marker Generation

### User-Provided Markers

From wizard Stage 6:
- Linguistic patterns (argument structures, vocabulary)
- Structural patterns (relationships, dependencies)
- Situational patterns (crisis revelations, conflicts)

### LLM-Generated Markers

From proxy terms (Stage 4), generate additional search patterns:

```python
def generate_markers_from_proxies(proxy_terms, concept_definition):
    """
    LLM prompt to generate search patterns from proxy terms.
    """
    prompt = f"""
    CONCEPT: {concept_name}
    DEFINITION: {concept_definition}

    PROXY TERMS (terms used instead of concept name):
    {proxy_terms}

    Generate regex-compatible search patterns that would find passages
    discussing this concept using these proxy terms. Consider:
    1. Term combinations (term1 AND term2)
    2. Context words that often appear nearby
    3. Negation patterns (what the proxies are NOT)

    For each pattern, explain what it would catch and potential false positives.
    """
    return llm_call(prompt)
```

### Marker Bank Structure

```json
{
  "marker_id": "mk_001",
  "type": "argumentative",
  "description": "Arguments connecting technology to sovereignty loss",
  "patterns": [
    "(technology|tech) AND (dependency|dependence) AND (sovereignty|autonomy|control)",
    "(infrastructure) AND (foreign|external) AND (control|access)",
    "(supply chain) AND (vulnerability|risk) AND (strategic|critical)"
  ],
  "positive_indicators": [
    "connects tech choice to political capacity",
    "frames dependency as constraint on options"
  ],
  "negative_indicators": [
    "purely cost/efficiency framing",
    "temporary disruption without structural concern"
  ],
  "weight": 0.9,
  "source": "user_input"
}
```

---

## Phase 3: Document Staging

### Document Registration

When user points to a document:

```python
def register_document(concept_id, document_info, user_notes):
    """
    Stage document for later processing without immediate analysis.
    """
    return {
        "id": generate_id(),
        "concept_id": concept_id,
        "document_type": document_info["type"],  # academic, policy, news, etc.
        "reference": document_info["citation_or_url"],
        "title": document_info.get("title"),
        "author": document_info.get("author"),
        "date": document_info.get("date"),

        # User guidance for processing
        "relevance_note": user_notes["why_relevant"],
        "expected_instances": user_notes["what_to_find"],
        "specific_sections": user_notes.get("focus_sections"),
        "priority": user_notes.get("priority", 3),

        # Processing state
        "status": "queued",
        "queued_at": now(),
        "processing_results": None
    }
```

### Why Stage Before Processing?

1. **User Expertise**: User knows WHERE instances likely are
2. **Targeted Analysis**: Focus LLM attention on relevant sections
3. **Priority Management**: Process high-value documents first
4. **Context Accumulation**: Later documents benefit from earlier findings
5. **Cost Control**: Avoid processing irrelevant documents

---

## Phase 4: Document Processing

### Step 4.1: Document Retrieval

```python
def retrieve_document(source_pointer):
    """
    Fetch document content from reference.
    """
    if source_pointer.document_type == "url":
        content = fetch_url(source_pointer.reference)
    elif source_pointer.document_type == "pdf":
        content = extract_pdf(source_pointer.reference)
    elif source_pointer.document_type == "upload":
        content = read_upload(source_pointer.reference)

    return {
        "raw_content": content,
        "word_count": len(content.split()),
        "sections": extract_sections(content)  # If structured
    }
```

### Step 4.2: Chunking & Sectioning

```python
def prepare_for_analysis(document, source_pointer):
    """
    Break document into analyzable chunks.
    """
    # If user specified sections, prioritize those
    if source_pointer.specific_sections:
        chunks = extract_specified_sections(document, source_pointer.specific_sections)
    else:
        chunks = chunk_by_paragraphs(document, max_tokens=2000)

    return chunks
```

### Step 4.3: Marker-Based Filtering

```python
def apply_marker_filters(chunks, markers):
    """
    Pre-filter chunks using recognition markers before LLM analysis.
    """
    candidate_chunks = []

    for chunk in chunks:
        for marker in markers:
            for pattern in marker.patterns:
                if regex_match(pattern, chunk.text):
                    candidate_chunks.append({
                        "chunk": chunk,
                        "triggered_marker": marker,
                        "match_context": extract_context(chunk, pattern)
                    })
                    break

    return candidate_chunks
```

### Step 4.4: LLM Analysis

```python
def analyze_chunk_for_concept(chunk, concept, markers, differentiations):
    """
    Deep LLM analysis of candidate chunk.
    """
    prompt = f"""
    CONCEPT: {concept.name}
    DEFINITION: {concept.definition}

    RECOGNITION MARKERS THAT TRIGGERED THIS ANALYSIS:
    {chunk.triggered_marker.description}

    WHAT THIS CONCEPT IS NOT (avoid these confusions):
    {format_differentiations(differentiations)}

    PARADIGMATIC CASE FOR REFERENCE:
    {concept.paradigmatic_case.summary}

    TEXT TO ANALYZE:
    {chunk.text}

    TASKS:
    1. Does this passage exhibit the concept "{concept.name}"?
       - Explicitly (uses the term or equivalent)?
       - Implicitly (exhibits the phenomenon without naming it)?
       - Neither (false positive from marker match)?

    2. If yes, extract:
       - The specific quote(s) exhibiting the concept
       - Which features of the concept are demonstrated
       - The confidence level (high/medium/low)
       - Any claims or evidence that could populate the schema

    3. If no, explain why this is a false positive.

    4. Note any near-misses or related phenomena.

    OUTPUT (JSON):
    {{
      "exhibits_concept": true/false,
      "usage_type": "explicit" | "implicit" | "neither",
      "confidence": "high" | "medium" | "low",
      "confidence_score": 0.0-1.0,
      "quotes": [
        {{
          "text": "...",
          "start_position": N,
          "features_exhibited": ["feature1", "feature2"],
          "analysis": "Why this exhibits the concept..."
        }}
      ],
      "extracted_claims": [
        {{
          "claim_type": "causal" | "normative" | "descriptive",
          "claim_content": "...",
          "supporting_evidence": "..."
        }}
      ],
      "false_positive_reason": "...",  // If not exhibiting
      "near_misses": ["..."],
      "suggested_marker_refinements": ["..."]
    }}
    """
    return llm_call(prompt, response_format="json")
```

### Step 4.5: Instance Extraction

```python
def extract_instances(analysis_results, document, concept):
    """
    Convert LLM analysis to structured instances.
    """
    instances = []

    for result in analysis_results:
        if result.exhibits_concept:
            for quote in result.quotes:
                instance = {
                    "concept_id": concept.id,
                    "source_document_id": document.id,
                    "quote_text": quote.text,
                    "usage_type": result.usage_type,
                    "features_exhibited": quote.features_exhibited,
                    "analysis_notes": quote.analysis,
                    "confidence": result.confidence_score,
                    "source_type": "evidence_testing",
                    "source_reference": f"{document.citation}, p.{estimate_page(quote)}",
                    "created_at": now()
                }
                instances.append(instance)

    return instances
```

---

## Phase 5: Schema Population

### Mapping Instances to Schema Tables

Each extracted instance can populate multiple schema tables:

```python
def map_to_schema(instance, concept):
    """
    Determine which schema tables this instance can populate.
    """
    mappings = []

    # Quinean: Web of Belief
    if "belief_connection" in instance.features_exhibited:
        mappings.append({
            "table": "concept_belief_web",
            "data": {
                "concept_id": concept.id,
                "connected_belief": extract_belief(instance),
                "connection_type": classify_connection(instance),
                "source_type": "evidence_testing",
                "source_reference": instance.source_reference,
                "confidence": instance.confidence
            }
        })

    # Brandomian: Inferential Relations
    if "inference" in instance.features_exhibited:
        mappings.append({
            "table": "concept_inference_relations",
            "data": {
                "concept_id": concept.id,
                "premise_or_conclusion": extract_inference(instance),
                "relation_type": "material_inference",
                "source_type": "evidence_testing",
                "source_reference": instance.source_reference,
                "confidence": instance.confidence
            }
        })

    # Canguilhem: Vitality/Health
    if "normative_assessment" in instance.features_exhibited:
        mappings.append({
            "table": "concept_vitality_indicators",
            "data": {
                "concept_id": concept.id,
                "indicator_type": "external_assessment",
                "indicator_value": extract_assessment(instance),
                "source_type": "evidence_testing",
                "source_reference": instance.source_reference,
                "confidence": instance.confidence
            }
        })

    # Add to evidence tracking regardless
    mappings.append({
        "table": "concept_evidence",
        "data": {
            "concept_id": concept.id,
            "evidence_type": instance.usage_type,
            "quote": instance.quote_text,
            "analysis": instance.analysis_notes,
            "features": instance.features_exhibited,
            "source_type": "evidence_testing",
            "source_reference": instance.source_reference,
            "confidence": instance.confidence
        }
    })

    return mappings
```

### Source Type Tracking

All schema entries track their origin:

| source_type | Meaning |
|-------------|---------|
| `user_input` | Direct from wizard Q&A |
| `llm_analysis` | LLM generated from user input |
| `evidence_testing` | Extracted from document analysis |
| `internal_compute` | Derived from other schema data |
| `import` | Imported from external source |

---

## Phase 6: Gap Detection & Iteration

### Schema Audit

```python
def audit_schema_completeness(concept):
    """
    Assess which parts of schema are well-populated vs. empty.
    """
    tables = get_all_schema_tables()

    report = {
        "well_populated": [],    # >70% fields filled, multiple entries
        "partially_filled": [],  # Some data but gaps
        "empty": [],             # No data
        "user_action_needed": [] # Cannot be auto-populated
    }

    for table in tables:
        entries = query_table(table, concept_id=concept.id)
        fill_rate = calculate_fill_rate(entries, table.required_fields)

        if fill_rate > 0.7 and len(entries) > 0:
            report["well_populated"].append({
                "table": table.name,
                "entries": len(entries),
                "fill_rate": fill_rate
            })
        elif fill_rate > 0.3 or len(entries) > 0:
            report["partially_filled"].append({
                "table": table.name,
                "entries": len(entries),
                "fill_rate": fill_rate,
                "missing_fields": get_missing_fields(entries, table)
            })
        else:
            if table.requires_user_input:
                report["user_action_needed"].append({
                    "table": table.name,
                    "reason": table.user_input_reason
                })
            else:
                report["empty"].append({
                    "table": table.name,
                    "suggested_sources": table.suggested_data_sources
                })

    return report
```

### Proactive Insufficiency Signaling

```python
def generate_gap_report(concept, audit_report):
    """
    Generate actionable gap report for user.
    """
    prompt = f"""
    CONCEPT: {concept.name}

    SCHEMA AUDIT RESULTS:
    {format_audit(audit_report)}

    DOCUMENTS PROCESSED: {count_processed_documents(concept)}
    DOCUMENTS QUEUED: {count_queued_documents(concept)}

    TASKS:
    1. Identify the most critical gaps (what's blocking deeper understanding)
    2. Suggest specific actions to fill each gap:
       - Additional wizard questions to ask user
       - Types of documents to search
       - Specific search patterns to try
    3. Prioritize: what should user do NEXT?
    4. Estimate: how much more input is needed for "adequate" coverage?

    Be specific and actionable. Don't just say "more data needed" - say exactly
    what kind of data and where it might be found.
    """

    return llm_call(prompt)
```

### Example Gap Report

```markdown
## Schema Status: Technological Sovereignty

### Summary
- **Overall Population**: 62%
- **Documents Processed**: 3/7 queued
- **Instances Extracted**: 23

### Critical Gaps

#### 1. Normative Dimension (Priority: HIGH)
**Gap**: No data in `concept_normative_status` table.
**Why Critical**: Without normative grounding, concept is purely descriptive.
**Action Required**:
- User wizard question: "What ought to be done about technological sovereignty?"
- Search for: prescriptive policy statements, "should" language in tech policy

#### 2. Opposition/Resistance (Priority: HIGH)
**Gap**: No entries in `concept_challenges` table.
**Why Critical**: Concept appears uncontested, which is suspicious for a political concept.
**Action Required**:
- User wizard question: "Who would disagree with this concept? What would they say?"
- Search for: critiques of tech protectionism, arguments for interdependence

#### 3. Hacking Dimension (Priority: MEDIUM)
**Gap**: `concept_institutional_grounding` has only 1 entry.
**Why Critical**: Concept seems to float free of institutions.
**Action Required**:
- Search queued policy documents for institutional actors
- Add domain: "Government ministries dealing with tech policy"

### Suggested Next Actions

1. **Answer 2 wizard questions** (10 min):
   - Normative stance question
   - Opposition/resistance question

2. **Process queued documents** (30 min):
   - European Commission 2020 (HIGH priority, contains policy prescriptions)
   - Edler et al. 2020 (academic definition, may have critiques)

3. **Add 1 new document** targeting opposition:
   - Search for: "technology interdependence benefits" OR "against tech nationalism"

### Estimated to Adequate Coverage
- Current: 62%
- After suggested actions: ~80%
- Full coverage estimate: 2 more document processing cycles
```

---

## Processing Triggers

### Automatic Processing

1. **On wizard completion**: Generate initial markers, queue first document
2. **On document upload**: Add to queue with default priority
3. **On schedule**: Process next queued document every N hours
4. **On gap report**: Prioritize documents that could fill identified gaps

### Manual Triggers

1. **User clicks "Process Now"**: Immediate processing of specific document
2. **User requests "Fill Gaps"**: LLM-guided targeted search
3. **User adds markers**: Re-process documents with new markers

---

## Cost Management

### LLM Call Optimization

1. **Pre-filtering**: Use regex markers before LLM analysis
2. **Chunking**: Analyze only relevant sections, not full documents
3. **Caching**: Cache marker matches and analysis results
4. **Batching**: Process multiple documents in single LLM call where possible

### Estimated Costs (Claude Sonnet)

| Operation | Est. Tokens | Est. Cost |
|-----------|-------------|-----------|
| Wizard LLM assistance (per stage) | 2K input, 1K output | ~$0.02 |
| Marker generation from proxies | 1K input, 500 output | ~$0.01 |
| Document chunk analysis (per chunk) | 3K input, 1K output | ~$0.03 |
| Gap report generation | 5K input, 2K output | ~$0.05 |

**Typical full concept setup**: ~$0.50-2.00 depending on document count

---

## Success Criteria

### Minimum Viable Concept

- [ ] Genesis tables: 100% populated from wizard
- [ ] Differentiation: At least 2 contrasts
- [ ] At least 1 document processed
- [ ] At least 5 instances extracted
- [ ] Gap report generated

### Well-Developed Concept

- [ ] 80%+ schema population
- [ ] 3+ documents processed
- [ ] 20+ instances extracted
- [ ] Instances span 5+ schema tables
- [ ] User has addressed all HIGH priority gaps
- [ ] Recognition markers refined based on false positives

### Research-Ready Concept

- [ ] 95%+ schema population
- [ ] 10+ documents processed
- [ ] 50+ instances with confidence scores
- [ ] Opposition/challenges documented
- [ ] Normative and institutional dimensions filled
- [ ] Version history tracked
- [ ] External validation obtained

---

## Appendix: LLM Prompts

### A1: Marker Generation Prompt

```
CONCEPT: {name}
DEFINITION: {definition}
PROXY TERMS: {proxy_terms}

Generate 5-10 search patterns (regex-compatible) that would find passages
discussing this concept using proxy terms. For each pattern:
1. The pattern itself
2. What it's designed to catch
3. Potential false positive risk
4. Suggested weight (0.0-1.0)
```

### A2: Document Analysis Prompt

```
CONCEPT: {name}
DEFINITION: {definition}
NOT TO BE CONFUSED WITH: {differentiations}
RECOGNITION MARKERS: {markers}

DOCUMENT EXCERPT:
{text}

Does this excerpt exhibit the concept? If yes, extract:
- Specific quotes
- Features demonstrated
- Confidence level
- Schema-mappable claims

If no, explain why marker match was false positive.
```

### A3: Gap Report Prompt

```
CONCEPT: {name}
SCHEMA AUDIT: {audit_results}
DOCUMENTS PROCESSED: {doc_count}
INSTANCES EXTRACTED: {instance_count}

Identify critical gaps and provide specific, actionable recommendations for:
1. User questions to ask
2. Document types to search
3. Search patterns to try
4. Priority ordering

Be concrete: "search for critiques of tech nationalism in trade policy journals"
not just "find opposing views"
```

---

## Implementation Status

| Component | Status | Location |
|-----------|--------|----------|
| Schema (Genesis dimension) | COMPLETE | `genesis_dimension_migration.sql` |
| Wizard Question Bank | COMPLETE | `wizard_question_bank` table |
| Document Processing | DESIGNED | This document |
| API Endpoints | DESIGNED | This document |
| UI Components | PENDING | - |
| LLM Integration | PENDING | - |
