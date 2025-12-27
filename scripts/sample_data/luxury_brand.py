"""
Luxury Brand Strategy - Sample Project Data

A comprehensive sample project for brand/marketing strategy:
- 5 concepts, 3 dialectics, 3 actors (11 units total)
- Full grid content for each unit
- 2 evidence sources with 12 fragments
- Mix of statuses for demonstration
"""

from api.strategizer.models import (
    UnitType, UnitTier, UnitStatus, GridTier,
    EvidenceSourceType, ExtractionStatus, AnalysisStatus, EvidenceRelationship
)

LUXURY_BRAND_PROJECT = {
    "name": "Heritage Luxury Fashion House Strategy",
    "brief": """We are advising a heritage European luxury fashion house with 150 years of history
on their strategy for the next decade. The brand is known for exceptional craftsmanship and
timeless designs, but faces pressure from digital-native competitors, changing consumer
values around sustainability, and the rise of Asian markets. We need a strategic framework
for navigating tensions between heritage and innovation, exclusivity and growth, global
consistency and local relevance. Key questions: How do we modernize without losing authenticity?
How do we grow in Asia while maintaining brand equity? How do we address sustainability
without undermining luxury positioning?""",

    "domain": {
        "name": "Luxury Brand Strategy",
        "core_question": "How can a heritage luxury brand modernize for new audiences while preserving the authenticity and exclusivity that defines its value?",
        "success_looks_like": "A rejuvenated brand that resonates with Gen Z and Asian consumers while maintaining premium positioning and heritage credibility",
        "vocabulary": {
            "concept": "Brand Pillar",
            "dialectic": "Brand Tension",
            "actor": "Market Force"
        },
        "template_base": "brand"
    },

    "units": [
        # =====================================================================
        # CONCEPTS (5)
        # =====================================================================
        {
            "unit_type": UnitType.CONCEPT,
            "name": "Heritage Authenticity",
            "definition": "The brand's historical credibility and craft tradition that provides differentiation and justifies premium pricing.",
            "display_type": "Brand Pillar",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Heritage authenticity is the brand's most valuable and defensible asset, requiring careful stewardship while enabling evolution",
                    "evidence": "Brand valuation premium of 40% vs. contemporary competitors; archive comprises 150 years of designs; artisan workshops employ 200+ craftspeople trained in traditional techniques",
                    "warrant": "In luxury, authenticity cannot be manufactured or bought; it can only be inherited and maintained. This creates an insurmountable barrier to entry.",
                    "counter": "Heritage can become a constraint, preventing necessary innovation; younger consumers may not value history",
                    "rebuttal": "Heritage need not constrain if positioned as a source of authority for innovation. Research shows Gen Z values craft authenticity even more than Millennials."
                },
                "ACTOR": {
                    "proponents": "Long-tenured employees, heritage purists, certain Asian collectors, brand historians",
                    "opponents": "Innovation advocates, some Gen Z consumers, fast-fashion competitors who dismiss heritage as irrelevant",
                    "regulators": "Luxury industry associations, cultural heritage authorities, trademark protections",
                    "beneficiaries": "The brand itself, craftspeople, consumers seeking genuine luxury, collectors",
                    "casualties": "Competitors without heritage, consumers seeking novelty over tradition"
                },
                "TEMPORAL": {
                    "origins": "Founded in 1874; key heritage moments include royal appointments (1920s), Hollywood golden age (1950s), first Asian flagship (1995)",
                    "current_state": "Heritage positioning strong but underutilized in marketing; archive digitization incomplete; craftsperson workforce aging",
                    "trajectory": "Must invest in heritage transmission to next generation of craftspeople while making heritage accessible to digital audiences",
                    "inflection_points": "Death of last founder-era craftsperson, archive exhibition, heritage-inspired viral collection",
                    "end_states": "Either living heritage continuously renewed, or museum piece that loses contemporary relevance"
                }
            }
        },
        {
            "unit_type": UnitType.CONCEPT,
            "name": "Sustainable Luxury",
            "definition": "Reconciling luxury's traditional association with excess and exclusivity with growing consumer and regulatory demands for environmental responsibility.",
            "display_type": "Brand Pillar",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Sustainability is becoming a prerequisite for luxury positioning, not a trade-off against it; durability and craft are inherently sustainable",
                    "evidence": "72% of Gen Z luxury consumers say sustainability influences purchases; EU regulations will require product passports by 2027; resale market growing 25% annually",
                    "warrant": "True luxury has always been about lasting value; disposability is antithetical to luxury. Sustainability aligns with heritage craft values.",
                    "counter": "Sustainability requirements raise costs and constrain design; consumers want newness, not just durability; 'sustainable luxury' is an oxymoron",
                    "rebuttal": "Luxury already commands premiums that can absorb sustainability costs. Durability IS newness when positioned as investment. The contradiction is only for mass luxury, not true craftsmanship."
                },
                "ACTOR": {
                    "proponents": "Sustainability-focused consumers, EU regulators, ESG-focused investors, Stella McCartney-like innovators",
                    "opponents": "Traditional luxury purists, suppliers resistant to change, some shareholders focused on short-term margins",
                    "regulators": "EU Circular Economy Action Plan, French duty of vigilance law, California Transparency Act",
                    "beneficiaries": "Environment, consumers seeking guilt-free luxury, brands that lead on sustainability",
                    "casualties": "Brands that greenwash, suppliers unable to meet standards, fast fashion disguised as luxury"
                },
                "TEMPORAL": {
                    "origins": "Emerged post-2015 Paris Agreement; accelerated by pandemic reflection and Gen Z influence",
                    "current_state": "Most luxury brands have commitments but implementation gaps; greenwashing concerns; leaders pulling ahead",
                    "trajectory": "Regulation will force laggards; leaders will gain structural advantage; transparency becoming norm",
                    "inflection_points": "EU product passport requirements, major brand's carbon-neutral achievement, supply chain scandal",
                    "end_states": "Either sustainability as table stakes with leaders differentiated, or continued skepticism and regulation driving compliance only"
                }
            }
        },
        {
            "unit_type": UnitType.CONCEPT,
            "name": "Digital Clienteling",
            "definition": "Building personal relationships at scale through technology, combining digital reach with the intimate service traditionally offered to top clients.",
            "display_type": "Brand Pillar",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Digital enables extending clienteling beyond top 1% to top 20% of customers, dramatically expanding high-touch relationships",
                    "evidence": "Top 1% of customers drive 25% of revenue; next 19% have potential but receive generic treatment. Pilots of digital clienteling show 3x conversion and 2x frequency.",
                    "warrant": "Luxury has always been about relationships; digital is simply a new channel for relationship-building",
                    "counter": "Digital is antithetical to luxury's exclusive, intimate experience; technology feels cold and generic",
                    "rebuttal": "Digital clienteling done right enhances rather than replaces human connection. The concierge uses data to be more attentive, not less personal."
                },
                "ACTOR": {
                    "proponents": "Digital-native luxury consumers, tech-savvy sales associates, CRM technology vendors, data-driven marketers",
                    "opponents": "Traditional sales associates, privacy-conscious consumers, luxury purists who see tech as incompatible",
                    "regulators": "GDPR, data privacy regulators, platform policies",
                    "beneficiaries": "Mid-tier customers who get better service, sales associates with better tools, brand revenue",
                    "casualties": "Those who value anonymity, competitors slow to adopt, associates unable to adapt"
                },
                "TEMPORAL": {
                    "origins": "Emerged from general retail tech adoption; accelerated by COVID-19 when stores closed",
                    "current_state": "Pilots underway; data infrastructure still being built; associates being trained; Asia leading adoption",
                    "trajectory": "Will become standard within 5 years; differentiation will shift to quality of implementation",
                    "inflection_points": "Successful scale of pilot program, competitor breakthrough, major privacy incident",
                    "end_states": "Either seamlessly integrated digital-physical clienteling, or technology that creates distance rather than connection"
                }
            }
        },
        {
            "unit_type": UnitType.CONCEPT,
            "name": "Cultural Relevance",
            "definition": "Staying meaningful to new generations and cultures while maintaining brand identity.",
            "display_type": "Brand Pillar",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Cultural relevance requires engaging with contemporary conversations while maintaining distance from fleeting trends",
                    "evidence": "Successful collaborations (like Dior x Travis Scott) drove 30% youth awareness increase; brand mentions in music/film correlate with sales; BUT trend-chasing damages long-term equity",
                    "warrant": "Luxury brands are cultural institutions; withdrawal from culture risks irrelevance, while trend-chasing risks trivialization",
                    "counter": "Engagement with popular culture dilutes luxury positioning; the brand should maintain aristocratic distance",
                    "rebuttal": "Historical evidence shows luxury brands have always engaged with culture of their time; aristocratic distance is itself a pose. The question is HOW to engage, not whether."
                },
                "ACTOR": {
                    "proponents": "Creative directors, cultural consultants, younger brand teams, celebrity partners",
                    "opponents": "Heritage purists, some long-time customers, those who see collaboration as dilution",
                    "regulators": "Trademark law, cultural appropriation critics, social media audiences",
                    "beneficiaries": "Young consumers discovering the brand, cultural partners, brand relevance metrics",
                    "casualties": "Those who preferred exclusivity, brand coherence if poorly executed"
                },
                "TEMPORAL": {
                    "origins": "Luxury-culture relationships date to Renaissance patronage; modern collaborations began in 1990s",
                    "current_state": "All major brands engaging; collaboration fatigue emerging; authenticity becoming differentiator",
                    "trajectory": "Moving from collaborations to deeper cultural embeddedness; need to be more selective and meaningful",
                    "inflection_points": "Successful cultural activation that defines the moment, failed collaboration that damages equity, shift in cultural conversation",
                    "end_states": "Either brand as cultural institution with enduring relevance, or irrelevant museum piece"
                }
            }
        },
        {
            "unit_type": UnitType.CONCEPT,
            "name": "Price Architecture",
            "definition": "The structure of entry-level, core, and aspirational product tiers that balances accessibility with exclusivity.",
            "display_type": "Brand Pillar",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Price architecture must provide entry points for new customers without diluting the exclusivity of core and aspirational tiers",
                    "evidence": "Brands with well-designed entry tiers convert 20% to core products within 3 years; poorly managed entry tiers cannibalize core and damage equity (Coach case study)",
                    "warrant": "Entry products are recruiting tools, not margin centers; they must provide genuine brand experience without full access",
                    "counter": "Entry-level products commoditize the brand and attract wrong customers; better to maintain high entry bar",
                    "rebuttal": "High entry bars work for ultra-exclusive brands; for broader luxury, the question is designing entry that builds toward core, not substitutes for it"
                },
                "ACTOR": {
                    "proponents": "Commercial teams seeking growth, new customers seeking access, entry-product designers",
                    "opponents": "Brand purists, top customers who value exclusivity, premium product teams",
                    "regulators": "Pricing regulations (some markets), brand governance processes",
                    "beneficiaries": "Aspiring customers, brand revenue, factories with steady orders",
                    "casualties": "Brand equity if poorly managed, premium product teams if cannibalized"
                },
                "TEMPORAL": {
                    "origins": "Diffusion lines emerged in 1980s; bridge pricing in 1990s; current era is more nuanced",
                    "current_state": "Most luxury brands have entry tiers but struggling to manage them; pressure to grow through accessibility",
                    "trajectory": "Moving toward experiences and services as entry points rather than just products",
                    "inflection_points": "Successful entry-to-core conversion program, entry product scandal, competitor's innovative entry strategy",
                    "end_states": "Either well-managed architecture that fuels growth, or premium dilution through poorly managed accessibility"
                }
            }
        },

        # =====================================================================
        # DIALECTICS (3)
        # =====================================================================
        {
            "unit_type": UnitType.DIALECTIC,
            "name": "Heritage vs Innovation",
            "definition": "The tension between preserving classic brand codes and evolving for new audiences and contexts.",
            "display_type": "Brand Tension",
            "tier": UnitTier.DOMAIN,
            "content": {
                "pole_a": "Heritage Preservation",
                "pole_b": "Contemporary Innovation"
            },
            "grids": {
                "LOGICAL": {
                    "claim": "The best luxury brands treat heritage as a vocabulary for innovation, not a constraint against it",
                    "evidence": "Chanel's classic codes reinterpreted each season; Gucci's successful reinvention while keeping core codes; Burberry's overemphasis on check as cautionary tale",
                    "warrant": "Heritage provides the grammar; innovation provides the sentences. Both are necessary for ongoing cultural conversation.",
                    "counter": "Some argue heritage should be preserved unchanged as sacred; others say it's just old and should be abandoned",
                    "rebuttal": "Both extremes fail: pure preservation becomes museum, pure innovation loses differentiation. The skill is in synthesis."
                },
                "TEMPORAL": {
                    "origins": "Eternal tension in luxury, but sharpened by pace of digital culture and Gen Z expectations",
                    "current_state": "Current creative direction leans heavily on heritage; question is whether to push more innovation",
                    "trajectory": "Likely cycle between heritage and innovation emphasis; key is maintaining coherent brand grammar through cycles",
                    "inflection_points": "Creative director change, breakthrough product that redefines the balance, market shift toward or away from heritage",
                    "end_states": "Either mastery of heritage-innovation synthesis, or veering to one extreme and losing the other's benefits"
                }
            }
        },
        {
            "unit_type": UnitType.DIALECTIC,
            "name": "Exclusivity vs Accessibility",
            "definition": "The tension between scarcity-driven value and volume-driven growth.",
            "display_type": "Brand Tension",
            "tier": UnitTier.DOMAIN,
            "content": {
                "pole_a": "Scarcity/Exclusivity",
                "pole_b": "Volume/Accessibility"
            },
            "grids": {
                "LOGICAL": {
                    "claim": "Exclusivity and accessibility can coexist if managed across carefully designed tiers and channels",
                    "evidence": "Hermes maintains extreme scarcity at top while growing overall revenue; LVMH manages portfolio across accessibility spectrum; single-tier brands struggle with this tension",
                    "warrant": "The key is preventing accessibility from diluting exclusivity through clear tier separation and brand governance",
                    "counter": "Any accessibility undermines true luxury; alternatively, exclusivity is elitism that should be abandoned",
                    "rebuttal": "Tier management allows serving different segments without contamination. The question is execution, not principle."
                },
                "TEMPORAL": {
                    "origins": "Luxury historically exclusive; accessibility debate intensified with global expansion in 1990s-2000s",
                    "current_state": "Brand in middle of spectrum; pressure to grow (accessibility) while protecting equity (exclusivity)",
                    "trajectory": "Digital will push toward more accessibility; scarcity will need to be actively managed and perhaps performed",
                    "inflection_points": "Launch of more accessible line, pullback on distribution, competitor's exclusivity failure",
                    "end_states": "Either managed coexistence across tiers, or drift to one pole with loss of the other's benefits"
                }
            }
        },
        {
            "unit_type": UnitType.DIALECTIC,
            "name": "Global Consistency vs Local Resonance",
            "definition": "The tension between maintaining one global brand identity and adapting to local cultural contexts.",
            "display_type": "Brand Tension",
            "tier": UnitTier.DOMAIN,
            "content": {
                "pole_a": "Global Consistency",
                "pole_b": "Local Resonance"
            },
            "grids": {
                "LOGICAL": {
                    "claim": "Global luxury brands can and must adapt to local cultures while maintaining core identity - this is cultural fluency, not dilution",
                    "evidence": "Dior's Chinese New Year collections increase China sales 20% without damaging Western perception; rigid global approach loses to locally-adapted competitors",
                    "warrant": "Luxury has always crossed cultures through adaptation; the skill is knowing what adapts (expression) vs. what stays constant (essence)",
                    "counter": "Local adaptation risks creating multiple brands that don't cohere; better to maintain strict global consistency",
                    "rebuttal": "Strict consistency risks being tone-deaf and losing relevance in key markets. The question is what level of adaptation at what tier of the brand."
                },
                "TEMPORAL": {
                    "origins": "Tension emerged with global expansion; intensified with rise of China market since 2010",
                    "current_state": "Current approach is cautious global consistency; likely underweighting local resonance especially in China",
                    "trajectory": "Local adaptation likely to increase as China, Middle East become more important; global consistency increasingly challenged",
                    "inflection_points": "Successful local campaign that sets new standard, cultural misstep that damages the brand, competitor breakthrough in local resonance",
                    "end_states": "Either cultural fluency that maintains global identity while resonating locally, or one-size-fits-all that loses cultural relevance"
                }
            }
        },

        # =====================================================================
        # ACTORS (3)
        # =====================================================================
        {
            "unit_type": UnitType.ACTOR,
            "name": "LVMH/Kering Conglomerates",
            "definition": "The dominant luxury conglomerates that set industry standards, attract talent, and have deep pockets for investment and acquisition.",
            "display_type": "Market Force",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Conglomerate competition requires us to be strategically clear about where we can win and where we need to be 'good enough'",
                    "evidence": "LVMH and Kering have 10x our resources; they can outspend on celebrity, media, stores. But independent brands maintain price premium and perceived authenticity.",
                    "warrant": "We cannot compete on conglomerate terms; we must compete on independence, heritage depth, and craft authenticity",
                    "counter": "Independence is weakness, not strength; we should seek acquisition or partnership with a conglomerate",
                    "rebuttal": "Acquisition would access resources but sacrifice authenticity premium. Partnership models that preserve independence may be worth exploring."
                },
                "ACTOR": {
                    "proponents": "The conglomerates themselves, investment bankers, some employees seeking bigger platform",
                    "opponents": "Independent brand advocates, family owners, consumers who value independence",
                    "regulators": "Competition authorities, luxury industry associations",
                    "beneficiaries": "Conglomerate shareholders, acquired brand teams (sometimes), consumers seeking consistent experience",
                    "casualties": "Acquired brands that lose identity, independents that can't compete, market diversity"
                },
                "TEMPORAL": {
                    "origins": "LVMH formed 1987; Kering luxury pivot 2000s; consolidation accelerated since 2010",
                    "current_state": "Duopoly dominates top tier; independents surviving but under pressure; Chanel uniquely positioned",
                    "trajectory": "Continued consolidation likely; independents will need to band together or find niches",
                    "inflection_points": "Major acquisition attempt, new conglomerate entrant, antitrust action, independent coalition forming",
                    "end_states": "Either maintained independence with clear positioning, or acquisition/partnership, or gradual marginalization"
                }
            }
        },
        {
            "unit_type": UnitType.ACTOR,
            "name": "Gen Z Consumers",
            "definition": "Digital-native consumers born after 1997 who will be the primary luxury audience of the next decades.",
            "display_type": "Market Force",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Gen Z is fundamentally reshaping luxury expectations around authenticity, sustainability, and digital experience",
                    "evidence": "Gen Z will be 40% of luxury market by 2035; they research extensively online before purchase; authenticity and sustainability are purchase drivers; they expect digital-first experience",
                    "warrant": "Brands that don't resonate with Gen Z now won't be relevant in 10 years; they are training ground for future customers",
                    "counter": "Gen Z has limited purchasing power; better to focus on wealthy Millennials and Gen X; Gen Z may 'grow out of' current values",
                    "rebuttal": "Gen Z may have limited power now, but they are future top customers. Their values are reshaping the market regardless of their spend. Betting against them is risky."
                },
                "ACTOR": {
                    "proponents": "Youth culture advocates, digital teams, sustainability teams, Gen Z employees",
                    "opponents": "Those focused on current high spenders, heritage purists, those skeptical of youth culture",
                    "regulators": "Youth marketing regulations, social media platform policies, sustainability disclosure requirements",
                    "beneficiaries": "Brands that successfully capture Gen Z, platforms favored by Gen Z, sustainability-focused suppliers",
                    "casualties": "Brands that miss the generational shift, traditional media, unsustainable practices"
                },
                "TEMPORAL": {
                    "origins": "Gen Z emerged as consumer force around 2015; influence accelerated through social media and COVID-19",
                    "current_state": "Brands experimenting with Gen Z engagement; mixed results; some authenticity backlash",
                    "trajectory": "Gen Z influence will only grow as purchasing power increases; need to build relationships now",
                    "inflection_points": "Successful Gen Z-focused campaign, Gen Z backlash against inauthenticity, Gen Z cultural moment that aligns with brand",
                    "end_states": "Either brand achieves genuine Gen Z relevance, or becomes 'your parents' brand'"
                }
            }
        },
        {
            "unit_type": UnitType.ACTOR,
            "name": "Chinese Middle Class",
            "definition": "The rapidly growing Chinese middle and upper-middle class that represents the largest growth market for luxury.",
            "display_type": "Market Force",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "China is the essential growth market for luxury, but requires genuine cultural understanding rather than superficial localization",
                    "evidence": "Chinese consumers are 35% of global luxury sales; growing at 12% annually; increasingly sophisticated; travel less post-COVID so domestic purchase important",
                    "warrant": "No global luxury brand can ignore China; but misunderstanding Chinese consumers has destroyed brands",
                    "counter": "China dependence is risky given geopolitics; better to diversify across markets",
                    "rebuttal": "Diversification is wise but doesn't change that China is essential. Risk mitigation means understanding and navigating, not avoiding."
                },
                "ACTOR": {
                    "proponents": "Growth-focused leadership, Asia teams, Chinese employees and partners",
                    "opponents": "Those concerned about China dependence, cultural conservatives uncomfortable with adaptation",
                    "regulators": "Chinese government (trade, content), EU/US geopolitics, customs authorities",
                    "beneficiaries": "Brands that succeed in China, Chinese consumers, Chinese creative talent",
                    "casualties": "Brands that fail in China, cultural missteps, brand coherence if adaptation is poor"
                },
                "TEMPORAL": {
                    "origins": "Chinese luxury growth began 2000s; accelerated 2010s; became dominant 2020s",
                    "current_state": "COVID-19 slowed travel-related consumption; domestic China market now critical; cultural sophistication rising",
                    "trajectory": "Will remain or become largest market; cultural expectations will only increase; local competitors emerging",
                    "inflection_points": "Major brand success or failure in China, geopolitical escalation, Chinese luxury brand emergence",
                    "end_states": "Either deep China success with cultural fluency, or marginalization in the largest market"
                }
            }
        }
    ],

    # =========================================================================
    # EVIDENCE SOURCES
    # =========================================================================
    "evidence_sources": [
        {
            "source_name": "Bain Luxury Market Study 2024",
            "source_type": EvidenceSourceType.MANUAL,
            "source_content": """Annual analysis of the global luxury market. Key findings include:
Chinese consumers represent 35% of luxury purchases globally. Gen Z will be 40% of the market
by 2035. Sustainability is becoming a purchase driver, with 72% of Gen Z saying it influences
their choices. The resale market is growing 25% annually. Digital now influences 85% of luxury
purchases. Heritage brands maintain a 40% valuation premium over contemporary competitors.""",
            "fragments": [
                {
                    "content": "Chinese consumers represent 35% of global luxury purchases, with the domestic China market growing faster (18%) than Chinese travel retail (declined 5%) post-COVID.",
                    "source_location": "Chapter 3, Market Geography",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Chinese Middle Class",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 94
                },
                {
                    "content": "Gen Z will represent 40% of luxury purchases by 2035, with the cohort already shaping brand preferences and marketing strategies despite limited current purchasing power.",
                    "source_location": "Chapter 4, Demographic Shifts",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Gen Z Consumers",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 88
                },
                {
                    "content": "72% of Gen Z luxury consumers report that sustainability influences their purchase decisions, compared to 52% of Millennials and 35% of Gen X.",
                    "source_location": "Chapter 5, Values and Purchasing",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Sustainable Luxury",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 86
                },
                {
                    "content": "The luxury resale market is growing 25% annually, with authenticated pre-owned now representing 10% of luxury spending. Many consumers enter the brand through resale before purchasing new.",
                    "source_location": "Chapter 6, Resale and Circularity",
                    "status": AnalysisStatus.NEEDS_DECISION,
                    "confidence": 68,
                    "why_needs_decision": "Could support Sustainable Luxury (circularity angle) OR Price Architecture (entry point strategy)",
                    "interpretations": [
                        {
                            "key": "a",
                            "title": "Supports sustainability positioning",
                            "target_unit_name": "Sustainable Luxury",
                            "target_grid_slot": "TEMPORAL.current_state",
                            "relationship_type": EvidenceRelationship.EXTENDS,
                            "is_recommended": False,
                            "strategy": "Use to show consumer demand for circular luxury models",
                            "rationale": "Resale growth demonstrates consumer appetite for extending product lifecycles",
                            "commitment_statement": "Commits you to engaging with resale as part of sustainability strategy",
                            "foreclosure_statements": ["Treating resale as threat to be fought", "Ignoring circularity in sustainability strategy"]
                        },
                        {
                            "key": "b",
                            "title": "Supports entry-point strategy",
                            "target_unit_name": "Price Architecture",
                            "target_grid_slot": "LOGICAL.evidence",
                            "relationship_type": EvidenceRelationship.EXTENDS,
                            "is_recommended": True,
                            "strategy": "Use to show resale as an entry point that converts to new purchases",
                            "rationale": "If consumers enter through resale and move to new, it's another tier in price architecture",
                            "commitment_statement": "Commits you to viewing authenticated resale as recruitment channel",
                            "foreclosure_statements": ["Fighting resale market", "Treating resale as pure cannibalization"]
                        }
                    ]
                },
                {
                    "content": "Heritage brands maintain a 40% valuation premium over contemporary competitors, with brand age correlating positively with price premium up to 150 years.",
                    "source_location": "Chapter 2, Brand Valuations",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Heritage Authenticity",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 90
                },
                {
                    "content": "LVMH and Kering together control 45% of the luxury fashion market, with independent brands seeing market share decline of 2% annually since 2018.",
                    "source_location": "Chapter 7, Competitive Landscape",
                    "status": AnalysisStatus.ANALYZED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "LVMH/Kering Conglomerates",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 82
                }
            ]
        },
        {
            "source_name": "McKinsey State of Fashion Report 2024",
            "source_type": EvidenceSourceType.MANUAL,
            "source_content": """Analysis of fashion industry trends including luxury segment. Covers
digital transformation, sustainability challenges, regional dynamics, and consumer behavior shifts.
Notes that successful cultural collaborations increased brand awareness by 30% among youth.
Digital clienteling pilots show 3x higher conversion rates. Supply chain transparency becoming
mandatory requirement in EU. Asia-Pacific will be 50% of luxury growth in next 5 years.""",
            "fragments": [
                {
                    "content": "Successful cultural collaborations (Dior x Travis Scott, LV x Supreme) increased brand awareness among under-25 consumers by 30%, though long-term equity impact varies by execution quality.",
                    "source_location": "Trend 4, Cultural Relevance",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Cultural Relevance",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 84
                },
                {
                    "content": "Digital clienteling pilots among luxury brands show 3x higher conversion rates and 2x higher frequency of purchase compared to generic digital marketing. ROI varies by implementation quality.",
                    "source_location": "Trend 2, Digital Excellence",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Digital Clienteling",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 80
                },
                {
                    "content": "EU Digital Product Passport requirements will mandate supply chain transparency by 2027, affecting how luxury brands communicate sustainability credentials and enabling secondary market authentication.",
                    "source_location": "Regulatory Update, Sustainability",
                    "status": AnalysisStatus.NEEDS_DECISION,
                    "confidence": 72,
                    "why_needs_decision": "Could support Sustainable Luxury (regulatory driver) OR Heritage Authenticity (authentication value)",
                    "interpretations": [
                        {
                            "key": "a",
                            "title": "Regulatory driver for sustainability",
                            "target_unit_name": "Sustainable Luxury",
                            "target_grid_slot": "ACTOR.regulators",
                            "relationship_type": EvidenceRelationship.SUPPORTS,
                            "is_recommended": True,
                            "strategy": "Use to show regulatory momentum requiring sustainability action",
                            "rationale": "Product passport mandates make sustainability compliance non-optional",
                            "commitment_statement": "Commits you to viewing sustainability as regulatory requirement not just choice",
                            "foreclosure_statements": ["Treating sustainability as optional PR initiative", "Delaying sustainability investment"]
                        },
                        {
                            "key": "b",
                            "title": "Authentication protects heritage",
                            "target_unit_name": "Heritage Authenticity",
                            "target_grid_slot": "TEMPORAL.trajectory",
                            "relationship_type": EvidenceRelationship.EXTENDS,
                            "is_recommended": False,
                            "strategy": "Use to show how product passports will enable authentication that protects heritage value",
                            "rationale": "Digital authentication can fight counterfeits and prove provenance, reinforcing heritage claims",
                            "commitment_statement": "Commits you to leveraging digital for heritage authentication",
                            "foreclosure_statements": ["Treating digital as separate from heritage strategy", "Missing authentication opportunity"]
                        }
                    ]
                },
                {
                    "content": "Asia-Pacific will account for 50% of luxury market growth in the next 5 years, with mainland China, Japan, and South Korea being primary drivers. However, brands must navigate increased local competition.",
                    "source_location": "Regional Analysis, APAC",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.EXTENDS,
                    "target_unit_name": "Global Consistency vs Local Resonance",
                    "target_grid_slot": "TEMPORAL.trajectory",
                    "confidence": 88
                },
                {
                    "content": "Consumer research shows that 65% of luxury purchasers conduct online research before store visits, but 78% prefer final purchase in physical stores - highlighting need for seamless omnichannel experience.",
                    "source_location": "Consumer Insights, Omnichannel",
                    "status": AnalysisStatus.ANALYZED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Digital Clienteling",
                    "target_grid_slot": "LOGICAL.warrant",
                    "confidence": 76
                },
                {
                    "content": "Chinese consumers show increasing preference for local luxury brands in certain categories, with domestic brands capturing 15% of luxury skincare market. This trend could extend to fashion if local quality improves.",
                    "source_location": "Regional Analysis, China Deep Dive",
                    "status": AnalysisStatus.PENDING,
                    "confidence": 0
                }
            ]
        }
    ]
}
