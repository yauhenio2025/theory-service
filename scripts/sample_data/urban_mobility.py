"""
Urban Mobility Policy - Sample Project Data

A comprehensive sample project for government/policy strategy:
- 5 concepts, 3 dialectics, 4 actors (12 units total)
- Full grid content for each unit
- 2 evidence sources with 12 fragments
- Mix of statuses for demonstration
"""

from api.strategizer.models import (
    UnitType, UnitTier, UnitStatus, GridTier,
    EvidenceSourceType, ExtractionStatus, AnalysisStatus, EvidenceRelationship
)

URBAN_MOBILITY_PROJECT = {
    "name": "Metropolitan Urban Mobility Strategy",
    "brief": """We are a city planning department developing a comprehensive urban mobility
strategy for a major metropolitan area (population 3 million). Our goals are to reduce car
dependency, improve public transit, enable micro-mobility, and prepare for autonomous vehicles.
The framework should help us navigate competing interests and long-term infrastructure
investments. Key questions: How do we balance accessibility for all residents with sustainability
goals? How do we manage the transition from car-centric infrastructure? How do we prepare for
technology disruption while making prudent investments?""",

    "domain": {
        "name": "Urban Mobility Policy",
        "core_question": "How can we create a sustainable, equitable, and efficient urban transportation system that serves all residents?",
        "success_looks_like": "A city where car ownership is optional, public transit is excellent, micro-mobility is safe, and streets serve people not just vehicles",
        "vocabulary": {
            "concept": "Policy Framework",
            "dialectic": "Policy Tension",
            "actor": "Stakeholder Group"
        },
        "template_base": "government"
    },

    "units": [
        # =====================================================================
        # CONCEPTS (5)
        # =====================================================================
        {
            "unit_type": UnitType.CONCEPT,
            "name": "15-Minute City",
            "definition": "An urban planning concept where all essential services are accessible within a 15-minute walk or bike ride from any residence.",
            "display_type": "Policy Framework",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Organizing the city around 15-minute accessibility fundamentally reduces mobility demand while improving quality of life",
                    "evidence": "Paris implementation reduced car trips by 22% in pilot arrondissements; Melbourne study shows 30% reduction in VMT where 15-minute criteria met; resident satisfaction higher in 15-minute neighborhoods",
                    "warrant": "The best trip is the one not taken; localization reduces system load while increasing convenience",
                    "counter": "15-minute city concept is elitist, ignores industrial/logistics needs, and is politically coded as anti-car",
                    "rebuttal": "Implementation can be inclusive if focused on underserved areas first. Industrial zones can be designated outside 15-minute residential areas. Framing as 'complete neighborhoods' avoids political coding."
                },
                "ACTOR": {
                    "proponents": "Urban planners, sustainability advocates, local businesses, residents who don't drive, public health advocates",
                    "opponents": "Suburban car owners, some disability advocates (if not designed inclusively), businesses dependent on regional draw, conspiracy theorists",
                    "regulators": "Zoning authorities, city council, state/regional transportation agencies",
                    "beneficiaries": "Non-drivers, local businesses, children and elderly, environment, public health",
                    "casualties": "Regional retailers, some car-dependent businesses, parking industry"
                },
                "TEMPORAL": {
                    "origins": "Concept articulated by Carlos Moreno (2016), implemented in Paris (2020), spread globally post-COVID",
                    "current_state": "Pilot programs in select neighborhoods; zoning reform underway; political controversy in some contexts",
                    "trajectory": "Likely to become mainstream planning principle, but implementation will be gradual and contested",
                    "inflection_points": "First major neighborhood completion, political backlash, pandemic-driven permanent behavior change",
                    "end_states": "Either foundational organizing principle for city, or niche concept limited to select neighborhoods"
                }
            }
        },
        {
            "unit_type": UnitType.CONCEPT,
            "name": "Modal Shift",
            "definition": "Moving trips from private cars to public transit, cycling, walking, and shared mobility.",
            "display_type": "Policy Framework",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Achieving sustainability and livability goals requires shifting 30% of car trips to other modes within 10 years",
                    "evidence": "Current mode share: 60% car, 20% transit, 15% walk, 5% bike. Peer cities have achieved 45% car share. Each percentage point shift saves X tons CO2 and $Y in infrastructure costs.",
                    "warrant": "The car-first paradigm is unsustainable spatially, environmentally, and economically; alternatives must become competitive",
                    "counter": "Modal shift penalizes car owners who have no alternatives; public transit is unsafe/unreliable; weather prevents cycling",
                    "rebuttal": "Shift should be enabled through better alternatives, not just restrictions. Safety and reliability are solvable. Weather is manageable with infrastructure (see Copenhagen, Amsterdam in winter)."
                },
                "ACTOR": {
                    "proponents": "Transit agencies, cycling advocates, environmental groups, urban core residents, public health advocates",
                    "opponents": "Suburban residents, auto industry, parking industry, some business groups, disability advocates (if transit is inaccessible)",
                    "regulators": "City transportation department, regional transit authority, state DOT, federal transit administration",
                    "beneficiaries": "Transit riders, cyclists, pedestrians, environment, urban livability, public health",
                    "casualties": "Car-dependent residents (in short term), parking industry, some car-oriented businesses"
                },
                "TEMPORAL": {
                    "origins": "Concept has long history; modern push began with 1970s oil crisis, revived with climate awareness",
                    "current_state": "Slow progress; COVID-19 disrupted transit ridership; bike infrastructure expanding; e-bikes changing dynamics",
                    "trajectory": "Likely acceleration as climate pressure mounts and alternatives improve; generational shift as young people drive less",
                    "inflection_points": "Major transit investment, gas price spike, congestion pricing implementation, e-bike tipping point",
                    "end_states": "Either fundamental transformation of mode share, or incremental improvement within car-dominant paradigm"
                }
            }
        },
        {
            "unit_type": UnitType.CONCEPT,
            "name": "Congestion Pricing",
            "definition": "Using price signals to manage road demand, typically by charging for entry to congested areas or for peak-hour travel.",
            "display_type": "Policy Framework",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Congestion pricing is the most efficient tool for managing road demand and funding transit alternatives",
                    "evidence": "London congestion charge reduced traffic 30% and raised £2.6B for transit; Stockholm referendum approved pricing after trial; Singapore's system has managed congestion for decades",
                    "warrant": "Roads are a scarce resource currently provided free at point of use; pricing corrects the market failure and funds alternatives",
                    "counter": "Congestion pricing is regressive, penalizing those who can't afford alternatives or live in underserved areas",
                    "rebuttal": "Equity concerns are valid but addressable through exemptions, rebates, and investment of revenues in underserved areas. Doing nothing also has equity impacts (pollution concentrated in poor areas)."
                },
                "ACTOR": {
                    "proponents": "Economists, some transit advocates, downtown businesses (eventually), environmental groups",
                    "opponents": "Suburban commuters, outer-borough residents, some businesses, politicians facing voter backlash",
                    "regulators": "City and state transportation departments, federal highway administration, courts (for legal challenges)",
                    "beneficiaries": "Urban residents (cleaner air, less congestion), transit riders (from reinvested revenue), economy (reduced congestion costs)",
                    "casualties": "Car commuters who pay more, businesses that lose car-dependent customers"
                },
                "TEMPORAL": {
                    "origins": "Theoretical concept since 1920s; implemented in Singapore (1975), London (2003), Stockholm (2007)",
                    "current_state": "Major cities studying; NYC approved but delayed; political resistance remains high; technology now enables sophisticated pricing",
                    "trajectory": "Likely to spread as congestion worsens and technology enables; but each city will be political battle",
                    "inflection_points": "NYC implementation (precedent for US), successful equity-focused design, autonomous vehicle disruption of model",
                    "end_states": "Either normalized tool across major cities, or perpetually proposed and rejected"
                }
            }
        },
        {
            "unit_type": UnitType.CONCEPT,
            "name": "Mobility as a Service (MaaS)",
            "definition": "Integrated multi-modal trip planning and payment that treats all transportation options as a seamless service.",
            "display_type": "Policy Framework",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "MaaS can make car ownership unnecessary for most trips by making alternatives seamless and competitive",
                    "evidence": "Helsinki Whim app users reduced car use 40%; LA Metro integration increased multi-modal trips 25%; subscription models show promise",
                    "warrant": "Friction between modes (separate apps, payment, planning) advantages car ownership; reducing friction levels playing field",
                    "counter": "MaaS benefits tech-savvy users; integration is technically difficult and politically contested; private operators resist integration",
                    "rebuttal": "Equity gaps in tech access are closing. Technical challenges are solvable (see EU examples). Regulation can require integration as condition of operating permits."
                },
                "ACTOR": {
                    "proponents": "Transit agencies, tech companies, mobility startups, younger residents, environmentalists",
                    "opponents": "Traditional transit unions (sometimes), private operators who benefit from fragmentation, car manufacturers",
                    "regulators": "Transit agencies, city transportation departments, state regulators, data privacy authorities",
                    "beneficiaries": "Multi-modal travelers, occasional users who don't want car ownership, tourists, transit agencies (ridership)",
                    "casualties": "Car ownership model, operators who lose to integration, those excluded by digital divide"
                },
                "TEMPORAL": {
                    "origins": "Concept emerged mid-2010s; Helsinki Whim (2016) pioneered; now spreading globally",
                    "current_state": "Pilot programs in many cities; full integration rare; business model still uncertain; pandemic disrupted progress",
                    "trajectory": "Likely continued growth but full vision remains elusive; may evolve differently than original conception",
                    "inflection_points": "Successful large-scale integration, major operator failure, autonomous vehicles changing equation",
                    "end_states": "Either seamless integrated mobility, or continued fragmented market with partial integration"
                }
            }
        },
        {
            "unit_type": UnitType.CONCEPT,
            "name": "Curb Space Allocation",
            "definition": "Managing the competing uses for street-level space including parking, transit, cycling, delivery, and outdoor commerce.",
            "display_type": "Policy Framework",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Curb space is the city's most valuable and contested real estate; active management is essential for mobility transformation",
                    "evidence": "One parking space generates $2K/year in meter revenue but $50K/year for outdoor dining; bike lanes generate 75% more retail spending per linear foot than car parking",
                    "warrant": "Curb space is finite; current allocation heavily favors free car storage over higher-value uses; reallocation drives modal shift",
                    "counter": "Removing parking destroys businesses; neighborhoods need parking for residents; delivery requires curb access",
                    "rebuttal": "Studies show bike lanes increase retail spending. Resident parking can be managed with permits. Delivery needs can be scheduled (off-peak zones). The question is BETTER allocation, not elimination."
                },
                "ACTOR": {
                    "proponents": "Urban designers, outdoor dining advocates, cycling advocates, transit agencies (for bus lanes)",
                    "opponents": "Some business owners, car-dependent residents, parking industry, delivery companies (if poorly implemented)",
                    "regulators": "City transportation, streets, and planning departments; business improvement districts",
                    "beneficiaries": "Pedestrians, cyclists, outdoor dining, transit speed, urban livability",
                    "casualties": "Free parking expectations, some car-dependent businesses initially"
                },
                "TEMPORAL": {
                    "origins": "Always contested; modern curb management emerged with tech (smart parking) and COVID-19 (outdoor dining)",
                    "current_state": "Increased experimentation post-COVID; outdoor dining normalization; bike lanes expanding; delivery pressure growing",
                    "trajectory": "Dynamic curb management likely to become standard; technology enables flex uses by time of day",
                    "inflection_points": "Successful street redesign, major delivery failure, permanent outdoor dining policy",
                    "end_states": "Either dynamic, optimized curb management, or continued car storage dominance with incremental change"
                }
            }
        },

        # =====================================================================
        # DIALECTICS (3)
        # =====================================================================
        {
            "unit_type": UnitType.DIALECTIC,
            "name": "Accessibility vs Sustainability",
            "definition": "The tension between serving all residents including those in car-dependent areas and reducing overall car dependence.",
            "display_type": "Policy Tension",
            "tier": UnitTier.DOMAIN,
            "content": {
                "pole_a": "Universal Accessibility",
                "pole_b": "Sustainability Goals"
            },
            "grids": {
                "LOGICAL": {
                    "claim": "Accessibility and sustainability are often framed as competing, but well-designed policy can advance both - with careful sequencing and equity focus",
                    "evidence": "Cities that invested in transit before congestion pricing saw higher acceptance; equity exemptions in London didn't undermine effectiveness; accessibility improves when streets have fewer cars",
                    "warrant": "False dichotomy often used to block change; real equity requires both access AND environmental improvement, which requires proactive design",
                    "counter": "In practice, sustainability often means restricting access (congestion pricing, parking removal) for those without alternatives",
                    "rebuttal": "This is a sequencing problem not a fundamental conflict. Invest in alternatives first, then implement restrictions with equity provisions. Doing nothing has worse equity outcomes."
                },
                "TEMPORAL": {
                    "origins": "Tension inherent but heightened by climate urgency and equity discourse",
                    "current_state": "Often used as excuse for inaction; some cities showing how to navigate",
                    "trajectory": "Climate pressure will force action; question is whether done equitably or not",
                    "inflection_points": "Major transit investment in underserved areas, congestion pricing with strong equity design, environmental justice lawsuit",
                    "end_states": "Either integrated approach that advances both, or perpetual conflict that blocks progress"
                }
            }
        },
        {
            "unit_type": UnitType.DIALECTIC,
            "name": "Speed vs Safety",
            "definition": "The tension between enabling fast travel and protecting pedestrians, cyclists, and other vulnerable road users.",
            "display_type": "Policy Tension",
            "tier": UnitTier.DOMAIN,
            "content": {
                "pole_a": "Traffic Flow/Speed",
                "pole_b": "Pedestrian/Cyclist Safety"
            },
            "grids": {
                "LOGICAL": {
                    "claim": "Safety must take priority; at urban speeds, each mph increase exponentially increases fatality risk for vulnerable users",
                    "evidence": "Pedestrian fatality risk increases from 10% at 20mph to 90% at 40mph; Vision Zero cities have reduced fatalities 50%+; throughput is often higher at lower speeds due to reduced crashes",
                    "warrant": "Every traffic death is a policy failure; roads must be designed for safety of most vulnerable users, not fastest",
                    "counter": "Slowing traffic increases congestion and travel time; some arterials must move traffic efficiently; emergency response needs speed",
                    "rebuttal": "Network should differentiate: slow streets in neighborhoods, faster arterials separated from pedestrians. Emergency response actually improves with fewer crashes. Congestion often caused by crashes that safety prevents."
                },
                "TEMPORAL": {
                    "origins": "20th century designed for cars; Vision Zero originated in Sweden (1997); spreading globally",
                    "current_state": "Vision Zero adopted rhetorically by many cities; implementation lagging; SUV proliferation increasing pedestrian deaths",
                    "trajectory": "Likely continued adoption with pressure from pedestrian/cyclist fatality trends",
                    "inflection_points": "Major pedestrian fatality incident, successful street redesign, automated enforcement at scale",
                    "end_states": "Either systemic safety transformation, or continued trading lives for speed"
                }
            }
        },
        {
            "unit_type": UnitType.DIALECTIC,
            "name": "Public Transit vs Shared Mobility",
            "definition": "The tension between investing in fixed-route public transit and enabling flexible shared mobility services.",
            "display_type": "Policy Tension",
            "tier": UnitTier.DOMAIN,
            "content": {
                "pole_a": "Fixed-Route Public Transit",
                "pole_b": "Flexible Shared Mobility"
            },
            "grids": {
                "LOGICAL": {
                    "claim": "Public transit and shared mobility are complementary, not competing - but require active integration and appropriate roles",
                    "evidence": "First/last mile services increase transit ridership 15-25%; Lyft/Uber initially grew transit (pre-pooling) then competed; microtransit fills gaps but can't replace trunk lines",
                    "warrant": "Fixed-route transit is efficient for high-demand corridors; shared mobility excels for first/last mile and low-density areas. Neither can do everything.",
                    "counter": "Shared mobility cannibalizes transit ridership; subsidizing Uber competes with buses; better to invest fully in transit",
                    "rebuttal": "Without first/last mile solutions, transit catchment is limited. The question is policy design: integrate and regulate shared mobility to complement, not compete."
                },
                "TEMPORAL": {
                    "origins": "Tension emerged with rideshare growth (2012+); microtransit experiments began 2015+",
                    "current_state": "Still experimenting with integration; microtransit results mixed; e-bikes changing equation",
                    "trajectory": "Autonomous vehicles will intensify this tension; need policy frameworks before technology forces hand",
                    "inflection_points": "Successful integration model, major rideshare policy change, autonomous vehicle deployment",
                    "end_states": "Either complementary ecosystem with clear roles, or fragmented competition that undermines both"
                }
            }
        },

        # =====================================================================
        # ACTORS (4)
        # =====================================================================
        {
            "unit_type": UnitType.ACTOR,
            "name": "Car Owners",
            "definition": "Residents who own and regularly use private vehicles, representing both a political constituency and a user group whose behavior must change.",
            "display_type": "Stakeholder Group",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Car owners are not a monolith; many would use alternatives if they were convenient, safe, and reliable - targeting 'captive drivers' is the strategy",
                    "evidence": "Surveys show 40% of car owners would consider giving up car if alternatives improved; 25% drive only because alternatives don't exist; true 'car lovers' are a minority",
                    "warrant": "Political framing as 'war on cars' creates false solidarity; actual policy should focus on making car-ownership optional, not punishing car use",
                    "counter": "Car owners vote; policies that threaten car convenience face strong opposition regardless of alternatives",
                    "rebuttal": "This is why sequencing matters: build alternatives, demonstrate benefits, create coalition of those who switched, THEN implement restrictions. The political coalition changes as mode share shifts."
                },
                "ACTOR": {
                    "proponents": "Auto industry, AAA, suburban municipalities, parking industry",
                    "opponents": "Transit and cycling advocates, urban environmentalists, anti-car urbanists",
                    "regulators": "City council (elected, responds to voters), state legislators (often from car-dependent suburbs)",
                    "beneficiaries": "Those who genuinely need cars (disabled, tradespeople, some parents), car industry",
                    "casualties": "Those stuck in traffic because system designed for cars, pedestrians/cyclists at risk"
                },
                "TEMPORAL": {
                    "origins": "Post-WWII suburban development created car dependence; political identity formed around car ownership",
                    "current_state": "Still politically powerful but weakening; younger generations driving less; urban residents increasingly frustrated with car dominance",
                    "trajectory": "Likely gradual shift as alternatives improve and generational change proceeds",
                    "inflection_points": "Gas price spike, major congestion event, successful car-free neighborhood, generational tipping point",
                    "end_states": "Either car ownership becomes optional luxury, or remains political identity that blocks change"
                }
            }
        },
        {
            "unit_type": UnitType.ACTOR,
            "name": "Transit Unions",
            "definition": "Labor unions representing transit workers, concerned about job security, working conditions, and automation threats.",
            "display_type": "Stakeholder Group",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Transit unions can be partners in transformation if their concerns about automation and job quality are addressed",
                    "evidence": "Union opposition has blocked some transit innovations; BUT unions supported service expansion and have expertise in operations; automation timeline is longer than feared",
                    "warrant": "Transit transformation requires worker buy-in for implementation; unions have legitimate concerns that can be addressed with good policy",
                    "counter": "Unions prioritize member interests over rider interests; work rules prevent efficiency; automation will make transit labor obsolete anyway",
                    "rebuttal": "Member and rider interests often align (better service, more jobs). Work rules can be reformed through negotiation. Automation will take decades; need workers for transition and oversight."
                },
                "ACTOR": {
                    "proponents": "Transit workers, labor movement, some progressives, transit agencies seeking stability",
                    "opponents": "Fiscal conservatives, tech companies pushing automation, some efficiency advocates",
                    "regulators": "National Labor Relations Board, state labor boards, transit agency management",
                    "beneficiaries": "Transit workers, riders (if service quality maintained), communities where transit workers live",
                    "casualties": "Potentially: workers if automation proceeds, riders if work rules block service improvements"
                },
                "TEMPORAL": {
                    "origins": "Transit unions formed early 20th century; battles over automation since 1970s",
                    "current_state": "Significant power in most cities; COVID-19 highlighted essential worker status; automation concerns growing",
                    "trajectory": "Continued influence but need to adapt to technology change; opportunity for labor-transit-climate coalition",
                    "inflection_points": "Major strike, successful partnership model, autonomous vehicle deployment, COVID-related workforce issues",
                    "end_states": "Either constructive partnership in transit transformation, or adversarial relationship that blocks progress"
                }
            }
        },
        {
            "unit_type": UnitType.ACTOR,
            "name": "Tech Platforms",
            "definition": "Companies like Uber, Lyft, Lime, and Bird that operate mobility services in the city.",
            "display_type": "Stakeholder Group",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Tech platforms can be valuable partners if properly regulated, but their profit incentives often conflict with public interest",
                    "evidence": "Platforms initially increased transit use, then cannibalized it; scooters provide first/last mile but create sidewalk conflicts; data sharing remains contested",
                    "warrant": "Private innovation can complement public transit; but without regulation, platforms optimize for profit not system efficiency",
                    "counter": "Platforms are competing with transit, not complementing it; their workers are exploited; their data practices are predatory",
                    "rebuttal": "These are regulatory failures, not inherent characteristics. Cities that require integration, data sharing, and labor standards get better outcomes. The choice is not platforms vs. no platforms; it's regulated vs. unregulated."
                },
                "ACTOR": {
                    "proponents": "Platform companies, some users (convenience), investors, gig economy advocates",
                    "opponents": "Taxi industry, some transit advocates, labor rights advocates, privacy advocates",
                    "regulators": "City transportation departments, public utilities commissions, state legislators",
                    "beneficiaries": "Users who value convenience, workers (partially - complex), areas underserved by transit",
                    "casualties": "Taxi industry, transit ridership (if unregulated), public space (if scooters poorly managed)"
                },
                "TEMPORAL": {
                    "origins": "Uber (2009), Lyft (2012), dockless bikes/scooters (2017+) - rapid emergence",
                    "current_state": "Established presence; regulatory frameworks still evolving; profitability uncertain; consolidation occurring",
                    "trajectory": "Likely continued presence but more regulated; autonomous vehicles will disrupt again",
                    "inflection_points": "Major regulatory action, platform bankruptcy, autonomous vehicle deployment, labor classification ruling",
                    "end_states": "Either integrated regulated partners, or continued adversarial relationship with regulatory cat-and-mouse"
                }
            }
        },
        {
            "unit_type": UnitType.ACTOR,
            "name": "Business Districts",
            "definition": "Commercial districts and their business improvement districts (BIDs) that have interests in customer access, delivery, and employee commuting.",
            "display_type": "Stakeholder Group",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Business districts can be powerful allies for mobility transformation if convinced that alternatives bring more customers than parking",
                    "evidence": "Studies show cyclists spend more per month at local retail than drivers; pedestrianization increases retail sales 30%+; congestion hurts delivery reliability",
                    "warrant": "Businesses care about customers and operations, not parking per se; if alternatives deliver customers and goods reliably, businesses will support them",
                    "counter": "Businesses depend on parking for customers; delivery requires curb access; employees can't commute without cars",
                    "rebuttal": "These are solvable: parking can be nearby not at-door; delivery can be scheduled/consolidated; employee commuting improves with transit. Success stories can be demonstrated."
                },
                "ACTOR": {
                    "proponents": "Forward-thinking BIDs, retail that benefits from foot traffic, restaurants (outdoor dining)",
                    "opponents": "Auto-oriented retail, parking lot owners, some suburban-style businesses in urban areas",
                    "regulators": "City economic development, BID governance, zoning authorities",
                    "beneficiaries": "Retail benefiting from pedestrian traffic, restaurants, office tenants with transit access",
                    "casualties": "Drive-through businesses, businesses dependent on cheap parking, suburban-style retail in urban areas"
                },
                "TEMPORAL": {
                    "origins": "BIDs emerged 1970s; business-mobility relationship contested throughout auto era",
                    "current_state": "COVID-19 shifted some businesses toward outdoor/pedestrian models; downtown recovery uncertain",
                    "trajectory": "Likely more business support for alternatives as evidence accumulates and generational change in business leadership",
                    "inflection_points": "Successful pedestrianization, downtown renaissance or decline, major retailer taking pro-transit stance",
                    "end_states": "Either business community as mobility transformation champion, or continued opposition to change"
                }
            }
        }
    ],

    # =========================================================================
    # EVIDENCE SOURCES
    # =========================================================================
    "evidence_sources": [
        {
            "source_name": "Urban Mobility Transformation Report 2024",
            "source_type": EvidenceSourceType.MANUAL,
            "source_content": """Comprehensive analysis of urban mobility trends across 50 major cities.
Key findings: cities with congestion pricing saw 25-30% reduction in car trips; bike mode share
doubled in cities with protected lane networks; 15-minute city pilots reduced VMT by 20%;
Vision Zero cities reduced pedestrian fatalities by 50%; MaaS adoption correlates with car ownership
reduction. Report also notes political challenges and equity concerns that must be addressed.""",
            "fragments": [
                {
                    "content": "Cities that implemented congestion pricing saw 25-30% reduction in car trips within the pricing zone, with London, Stockholm, and Singapore as primary examples.",
                    "source_location": "Chapter 3, Demand Management",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Congestion Pricing",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 92
                },
                {
                    "content": "Bike mode share doubled in cities that built comprehensive protected lane networks, from an average of 3% to 6% within 5 years of network completion.",
                    "source_location": "Chapter 4, Active Transportation",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Modal Shift",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 88
                },
                {
                    "content": "15-minute city pilot programs in Paris, Melbourne, and Barcelona reduced vehicle miles traveled by 15-22% in target neighborhoods, with highest reductions in areas with most complete local service provision.",
                    "source_location": "Chapter 2, Land Use Integration",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "15-Minute City",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 85
                },
                {
                    "content": "Cities implementing Vision Zero policies reduced pedestrian fatalities by 30-50%, with Oslo, Helsinki, and Tokyo approaching zero pedestrian deaths in urban cores.",
                    "source_location": "Chapter 5, Safety",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Speed vs Safety",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 90
                },
                {
                    "content": "MaaS adoption in Helsinki (Whim app) correlated with 15% reduction in car ownership among active users, though selection effects make causation difficult to establish.",
                    "source_location": "Chapter 6, Technology Integration",
                    "status": AnalysisStatus.NEEDS_DECISION,
                    "confidence": 70,
                    "why_needs_decision": "Evidence supports MaaS concept but with qualification about causation; could be used as evidence or as acknowledgment of uncertainty",
                    "interpretations": [
                        {
                            "key": "a",
                            "title": "Supports MaaS potential",
                            "target_unit_name": "Mobility as a Service (MaaS)",
                            "target_grid_slot": "LOGICAL.evidence",
                            "relationship_type": EvidenceRelationship.SUPPORTS,
                            "is_recommended": True,
                            "strategy": "Use as evidence while acknowledging correlation vs causation caveat",
                            "rationale": "Even with selection effects, the correlation is meaningful and aligns with theoretical mechanisms",
                            "commitment_statement": "Commits you to investing in MaaS while acknowledging evidence limitations",
                            "foreclosure_statements": ["Waiting for perfect evidence before MaaS investment", "Dismissing MaaS due to causation uncertainty"]
                        },
                        {
                            "key": "b",
                            "title": "Adds nuance to MaaS case",
                            "target_unit_name": "Mobility as a Service (MaaS)",
                            "target_grid_slot": "LOGICAL.counter",
                            "relationship_type": EvidenceRelationship.QUALIFIES,
                            "is_recommended": False,
                            "strategy": "Use to strengthen counter-argument about MaaS evidence gaps",
                            "rationale": "Honest acknowledgment of evidence limitations strengthens overall credibility",
                            "commitment_statement": "Commits you to epistemic humility about MaaS claims",
                            "foreclosure_statements": ["Overpromising MaaS benefits", "Ignoring implementation challenges"]
                        }
                    ]
                },
                {
                    "content": "Political opposition to congestion pricing remains high even in cities where implementation succeeded, with 55% initial opposition dropping to 30% only after 2+ years of operation.",
                    "source_location": "Chapter 7, Political Economy",
                    "status": AnalysisStatus.ANALYZED,
                    "relationship_type": EvidenceRelationship.EXTENDS,
                    "target_unit_name": "Car Owners",
                    "target_grid_slot": "TEMPORAL.trajectory",
                    "confidence": 82
                }
            ]
        },
        {
            "source_name": "Transit-Oriented Development Impact Study",
            "source_type": EvidenceSourceType.MANUAL,
            "source_content": """Analysis of transit-oriented development and its effects on mobility
patterns, property values, and urban form. Key findings: TOD reduces car ownership 20-40%;
property values increase 10-25% near quality transit; retail sales increase 30% after
pedestrianization; first/last mile services increase transit ridership 15-25%. Study also
identifies implementation challenges and equity concerns with displacement.""",
            "fragments": [
                {
                    "content": "Transit-oriented development reduces car ownership by 20-40% compared to auto-oriented development, with reductions concentrated among households with high transit access.",
                    "source_location": "Section 2, Car Ownership Impacts",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Modal Shift",
                    "target_grid_slot": "TEMPORAL.trajectory",
                    "confidence": 84
                },
                {
                    "content": "Retail sales increased 30% on average after pedestrianization of commercial streets, with restaurants and specialty retail seeing highest gains and destination retail seeing modest declines.",
                    "source_location": "Section 4, Commercial Impacts",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Business Districts",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 86
                },
                {
                    "content": "First/last mile services (shuttles, bikeshare, scooters) increased transit ridership by 15-25% at stations with previously poor pedestrian access.",
                    "source_location": "Section 3, Network Effects",
                    "status": AnalysisStatus.NEEDS_DECISION,
                    "confidence": 75,
                    "why_needs_decision": "Supports integration of shared mobility with transit, relevant to dialectic about transit vs shared mobility",
                    "interpretations": [
                        {
                            "key": "a",
                            "title": "Resolves transit/shared mobility tension",
                            "target_unit_name": "Public Transit vs Shared Mobility",
                            "target_grid_slot": "LOGICAL.evidence",
                            "relationship_type": EvidenceRelationship.SUPPORTS,
                            "is_recommended": True,
                            "strategy": "Use as primary evidence that shared mobility complements rather than competes with transit",
                            "rationale": "15-25% ridership increase directly demonstrates complementary relationship when properly integrated",
                            "commitment_statement": "Commits you to integration strategy rather than competition framing",
                            "foreclosure_statements": ["Treating shared mobility as transit competitor", "Restricting shared mobility near transit"]
                        },
                        {
                            "key": "b",
                            "title": "Supports MaaS integration",
                            "target_unit_name": "Mobility as a Service (MaaS)",
                            "target_grid_slot": "LOGICAL.evidence",
                            "relationship_type": EvidenceRelationship.EXTENDS,
                            "is_recommended": False,
                            "strategy": "Use to show MaaS integration benefits with concrete first/last mile example",
                            "rationale": "First/last mile integration is core MaaS use case; this validates the concept",
                            "commitment_statement": "Commits you to MaaS as integration layer for multi-modal trips",
                            "foreclosure_statements": ["Siloed mode planning", "Ignoring first/last mile problem"]
                        }
                    ]
                },
                {
                    "content": "Curb space reallocation from parking to bike lanes increased retail spending per linear foot by 75%, though initial business opposition was significant.",
                    "source_location": "Section 5, Curb Management",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Curb Space Allocation",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 80
                },
                {
                    "content": "Property values near high-quality transit increased 10-25%, but this premium often drove displacement of lower-income residents unless affordable housing protections were in place.",
                    "source_location": "Section 6, Equity Impacts",
                    "status": AnalysisStatus.ANALYZED,
                    "relationship_type": EvidenceRelationship.QUALIFIES,
                    "target_unit_name": "Accessibility vs Sustainability",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 78
                },
                {
                    "content": "Surveys of 'captive drivers' - those who drive only because alternatives are inadequate - show 40% would switch modes if transit travel time was within 25% of driving time.",
                    "source_location": "Section 7, Mode Choice",
                    "status": AnalysisStatus.PENDING,
                    "confidence": 0
                }
            ]
        }
    ]
}
