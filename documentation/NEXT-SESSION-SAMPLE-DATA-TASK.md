# Next Session Task: Populate Strategizer Sample Projects

## Objective

Create 3-4 extensive sample projects across different domains with deep, realistic data to demonstrate the full Strategizer workflow. Each project should have:
- Bootstrapped domain with vocabulary
- 8-15 units (concepts, dialectics, actors)
- Multiple grids applied to each unit
- Evidence sources with extracted fragments
- Some pending decisions to resolve
- Some already-integrated evidence

This will let the user explore the UI and understand how all pieces fit together.

---

## Sample Project 1: Climate Tech Investment

**Domain:** Climate Tech Venture Investment
**Brief:** "We are launching a $100M climate tech fund targeting breakthrough technologies in carbon capture, green hydrogen, grid-scale storage, and sustainable materials. We want to develop a framework for evaluating climate tech opportunities that balances financial returns with climate impact."

### Units to Create

**Concepts (6):**
1. **Technical Defensibility** - Moats in deep tech (patents, know-how, process secrets)
2. **Climate Impact Potential** - Gigatons of CO2 equivalent reduction possible
3. **Path to Scale Economics** - When unit economics become viable at scale
4. **Policy Tailwinds** - How regulation accelerates or enables adoption
5. **Market Timing Risk** - Technology ready vs market ready gap
6. **Incumbent Disruption Potential** - Threat to or opportunity for legacy players

**Dialectics (3):**
1. **Climate Impact ↔ Financial Returns** - The core tension in impact investing
2. **Deep Tech Timeline ↔ VC Fund Lifecycle** - 10-year horizons vs 7-year funds
3. **First Mover ↔ Fast Follower** - Pioneering vs learning from others' mistakes

**Actors (4):**
1. **DOE & National Labs** - Government R&D and loan programs
2. **Oil & Gas Majors** - Incumbents with cash and infrastructure
3. **Utilities** - Grid operators and power purchasers
4. **Strategic Corporate Investors** - Google, Amazon, Microsoft climate commitments

### Grids to Apply

For each concept, apply:
- **LOGICAL** grid (claim, evidence, warrant, counter, rebuttal)
- **ACTOR** grid (proponents, opponents, regulators, beneficiaries, casualties)
- **TEMPORAL** grid (origins, current_state, trajectory, inflection_points)

For each dialectic, apply:
- **LOGICAL** grid
- **TEMPORAL** grid

### Evidence Sources (3)

1. **Source:** "BloombergNEF Climate Tech Report 2024"
   - Type: manual
   - Extract 8-10 fragments about market sizing, technology readiness

2. **Source:** "IEA Net Zero Pathway Analysis"
   - Type: url (mock as manual)
   - Extract 6-8 fragments about policy scenarios, technology adoption curves

3. **Source:** "Breakthrough Energy Ventures Portfolio Analysis"
   - Type: manual
   - Extract 5-6 fragments about what makes successful climate investments

### Fragment Status Distribution

- 40% INTEGRATED (high confidence, auto-applied)
- 30% NEEDS_DECISION (medium confidence, awaiting user choice)
- 20% ANALYZED (pending integration)
- 10% PENDING (not yet analyzed)

---

## Sample Project 2: Foundation Strategy (Moldova Media)

**Domain:** Foundation Media Strategy
**Brief:** "We are a foundation supporting independent media in Moldova, a small Eastern European country between Romania and Ukraine. We want to develop a strategic framework for understanding the media ecosystem, identifying where our grants can have the most impact, and building resilient information infrastructure."

### Units to Create

**Concepts (5):**
1. **Information Sovereignty** - A country's capacity to produce its own narratives
2. **Media Ecosystem Resilience** - Ability to withstand shocks and disinformation
3. **Revenue Diversification** - Moving beyond donor dependency
4. **Cross-Border Content Syndication** - Sharing content with Romanian partners
5. **Digital-First Transition** - Moving from TV/print to online audiences

**Dialectics (3):**
1. **Independence ↔ Sustainability** - Editorial independence vs commercial viability
2. **National Focus ↔ Diaspora Reach** - Serving domestic vs global Moldovan audience
3. **Quality ↔ Engagement** - In-depth journalism vs viral content

**Actors (4):**
1. **Oligarch-Owned Media** - Competitors with political backing
2. **European Funders** - EU, EED, other foundations
3. **Diaspora Communities** - Moldovans in Italy, Romania, Germany
4. **Government Regulators** - Broadcasting council, media laws

### Grids to Apply

Apply all three Tier 1 grids (LOGICAL, ACTOR, TEMPORAL) plus:
- **RESOURCE** grid for actors (funding sources, capabilities, constraints)
- **SCENARIO** grid for concepts (optimistic, pessimistic, transformative futures)

### Evidence Sources (2)

1. **Source:** "Moldova Media Landscape Assessment 2024"
   - 10+ fragments about audience habits, trust levels, funding patterns

2. **Source:** "EED Independent Media Support Evaluation"
   - 8+ fragments about what interventions work, sustainability challenges

---

## Sample Project 3: Brand Strategy (Luxury Fashion)

**Domain:** Luxury Brand Strategy
**Brief:** "We are advising a heritage European luxury fashion house on their strategy for the next decade. They face pressure from digital-native competitors, changing consumer values around sustainability, and the rise of Asian markets. We need a framework for navigating heritage vs innovation tensions."

### Units to Create

**Concepts (5):**
1. **Heritage Authenticity** - The brand's historical credibility and craft tradition
2. **Sustainable Luxury** - Reconciling excess with environmental responsibility
3. **Digital Clienteling** - Personal relationships at scale through technology
4. **Cultural Relevance** - Staying meaningful to new generations
5. **Price Architecture** - Entry points, core, and aspirational tiers

**Dialectics (3):**
1. **Heritage ↔ Innovation** - Classic codes vs contemporary expression
2. **Exclusivity ↔ Accessibility** - Scarcity value vs volume growth
3. **Global Consistency ↔ Local Resonance** - One brand vs cultural adaptation

**Actors (3):**
1. **LVMH/Kering** - Competing conglomerates with deep pockets
2. **Gen Z Consumers** - Value-driven, digital-native, sustainability-focused
3. **Chinese Middle Class** - Largest growth market with unique preferences

### Evidence Sources (2)

1. **Source:** "Bain Luxury Market Study 2024"
   - Fragments about market trends, consumer segments, channel shifts

2. **Source:** "McKinsey State of Fashion Report"
   - Fragments about sustainability, digital transformation, regional dynamics

---

## Sample Project 4: Government Planning (Urban Mobility)

**Domain:** Urban Mobility Policy
**Brief:** "We are a city planning department developing a comprehensive urban mobility strategy. We want to reduce car dependency, improve public transit, enable micro-mobility, and prepare for autonomous vehicles. The framework should help us navigate competing interests and long-term infrastructure investments."

### Units to Create

**Concepts (5):**
1. **15-Minute City** - All essential services within 15-minute walk/bike
2. **Modal Shift** - Moving trips from cars to transit/cycling/walking
3. **Congestion Pricing** - Using price signals to manage road demand
4. **Mobility as a Service (MaaS)** - Integrated multi-modal trip planning
5. **Curb Space Allocation** - Competing uses for street-level space

**Dialectics (3):**
1. **Accessibility ↔ Sustainability** - Serving all residents vs reducing emissions
2. **Speed ↔ Safety** - Fast travel vs pedestrian/cyclist safety
3. **Public Transit ↔ Shared Mobility** - Fixed routes vs flexible services

**Actors (4):**
1. **Car Owners** - Voters who resist reduced car access
2. **Transit Unions** - Workers concerned about automation
3. **Tech Platforms** - Uber, Lyft, e-scooter companies
4. **Business Districts** - Need for customer/delivery access

---

## Implementation Script Outline

Create a Python script `scripts/seed_strategizer_samples.py` that:

### 1. Project Creation Loop
```python
SAMPLE_PROJECTS = [
    {
        "name": "Climate Tech Investment Strategy",
        "brief": "...",
        "units": [...],
        "evidence_sources": [...],
        "evidence_fragments": [...],
    },
    # ... more projects
]

for project_data in SAMPLE_PROJECTS:
    # Create project
    project = await create_project(project_data)

    # Bootstrap domain
    domain = await bootstrap_domain(project.id)

    # Create units
    for unit_data in project_data["units"]:
        unit = await create_unit(project.id, unit_data)

        # Apply grids to each unit
        for grid_type in ["LOGICAL", "ACTOR", "TEMPORAL"]:
            await create_grid(unit.id, grid_type, slots={...})

    # Create evidence sources
    for source_data in project_data["evidence_sources"]:
        source = await create_source(project.id, source_data)

        # Create fragments with varied status
        for fragment_data in source_data["fragments"]:
            await create_fragment(source.id, fragment_data)

            # For NEEDS_DECISION fragments, create interpretations
            if fragment_data["status"] == "NEEDS_DECISION":
                await create_interpretations(fragment.id, [...])
```

### 2. Realistic Grid Content

For each unit, populate slots with domain-appropriate content:

```python
CLIMATE_TECH_GRIDS = {
    "Technical Defensibility": {
        "LOGICAL": {
            "claim": "Deep tech companies with strong IP and process know-how can build durable competitive moats",
            "evidence": "Analysis of 50 climate tech exits shows patent portfolio correlates with acquisition premium",
            "warrant": "In capital-intensive industries, replication barriers matter more than speed",
            "counter": "Open-source approaches and rapid iteration may outpace patent-protected innovation",
            "rebuttal": "While true for software, hardware-intensive climate tech requires capital that patents help attract"
        },
        "ACTOR": {
            "proponents": "Deep tech VCs (Lux, DCVC), university tech transfer offices",
            "opponents": "Open innovation advocates, some climate activists",
            "regulators": "USPTO, DOE with tech transfer mandates",
            "beneficiaries": "Founders with PhDs and lab experience",
            "casualties": "Fast-follower startups that can't replicate"
        },
        "TEMPORAL": {
            "origins": "Emerged from biotech and semiconductor investment patterns",
            "current_state": "Increasing focus on defensibility as climate tech matures",
            "trajectory": "Will intensify as more capital chases fewer breakthrough opportunities",
            "inflection_points": "Major patent disputes, open-source breakthroughs, regulatory changes"
        }
    },
    # ... more units
}
```

### 3. Evidence Fragment Examples

```python
CLIMATE_EVIDENCE_FRAGMENTS = [
    {
        "content": "Global climate tech investment reached $70B in 2023, with carbon capture and green hydrogen seeing the largest YoY growth at 45% and 62% respectively.",
        "source_location": "BloombergNEF Report, Page 12",
        "analysis_status": "INTEGRATED",
        "relationship_type": "ILLUSTRATES",
        "target_unit": "Climate Impact Potential",
        "target_grid_slot": "LOGICAL.evidence",
        "confidence": 0.92
    },
    {
        "content": "First-of-a-kind (FOAK) climate tech projects face a 'valley of death' between pilot and commercial scale, with average timelines of 7-12 years from lab to market.",
        "source_location": "IEA Report, Chapter 3",
        "analysis_status": "NEEDS_DECISION",
        "confidence": 0.65,
        "why_needs_decision": "Could strengthen either 'Deep Tech Timeline ↔ VC Fund Lifecycle' dialectic or 'Market Timing Risk' concept",
        "interpretations": [
            {
                "key": "a",
                "title": "Supports dialectic tension",
                "target_unit": "Deep Tech Timeline ↔ VC Fund Lifecycle",
                "target_grid_slot": "LOGICAL.evidence",
                "is_recommended": True
            },
            {
                "key": "b",
                "title": "Deepens risk concept",
                "target_unit": "Market Timing Risk",
                "target_grid_slot": "LOGICAL.evidence",
                "is_recommended": False
            }
        ]
    },
    # ... more fragments
]
```

---

## Expected Outcomes

After running the seed script, you'll have:

1. **4 Projects** visible at `/api/strategizer/ui/`
2. **~25 Units** total across projects with populated grids
3. **~75 Grid Instances** (3 grids per unit on average)
4. **~40 Evidence Fragments** with varied statuses
5. **~10 Pending Decisions** to explore in the UI

This gives you a realistic feel for:
- How the 3-column workspace displays a populated project
- How grid slots get filled with evidence
- How pending decisions present interpretation options
- How the evidence-to-grid flow works end-to-end

---

## Files to Create

1. `scripts/seed_strategizer_samples.py` - Main seeding script
2. `scripts/sample_data/climate_tech.py` - Climate tech domain data
3. `scripts/sample_data/foundation_media.py` - Foundation strategy data
4. `scripts/sample_data/luxury_brand.py` - Brand strategy data
5. `scripts/sample_data/urban_mobility.py` - Government planning data

---

## Running the Script

```bash
# From project root
python scripts/seed_strategizer_samples.py

# Or with specific project
python scripts/seed_strategizer_samples.py --project climate_tech
```

---

## Notes for Implementation

1. **Use existing models** - All models are already in `api/strategizer/models.py`
2. **Use async properly** - The database is async, so use `async with get_db()` pattern
3. **Generate UUIDs** - Use `uuid.uuid4()` for IDs
4. **Realistic content** - The grid slot content should read like real strategic analysis
5. **Varied confidence** - Spread fragments across confidence ranges (0.4-0.95)
6. **Interpretation options** - Each NEEDS_DECISION fragment needs 2-4 interpretations with commitment/foreclosure statements

This documentation should enable a fresh session to implement comprehensive sample data.
