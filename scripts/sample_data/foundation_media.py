"""
Foundation Media Strategy (Moldova) - Sample Project Data

A comprehensive sample project for foundation/nonprofit strategic planning:
- 5 concepts, 3 dialectics, 4 actors (12 units total)
- Full grid content for each unit
- 2 evidence sources with 14 fragments
- Mix of statuses for demonstration
"""

from api.strategizer.models import (
    UnitType, UnitTier, UnitStatus, GridTier,
    EvidenceSourceType, ExtractionStatus, AnalysisStatus, EvidenceRelationship
)

FOUNDATION_MEDIA_PROJECT = {
    "name": "Moldova Independent Media Strategy",
    "brief": """We are a foundation supporting independent media in Moldova, a small Eastern
European country between Romania and Ukraine. The media landscape is fragmented, with many
outlets controlled by oligarchs or influenced by Russian disinformation. We want to develop
a strategic framework for understanding the media ecosystem, identifying where our grants
can have the most impact, and building resilient information infrastructure. Key questions:
How do we strengthen media sustainability without creating donor dependency? How do we reach
both domestic and diaspora audiences? How do we build resilience against information warfare?""",

    "domain": {
        "name": "Foundation Media Strategy",
        "core_question": "How can we build a resilient, independent media ecosystem in Moldova that serves democratic development?",
        "success_looks_like": "A media ecosystem with diverse, sustainable outlets that produce quality journalism, reach all audiences, and resist manipulation",
        "vocabulary": {
            "concept": "Strategic Lever",
            "dialectic": "Strategic Tension",
            "actor": "Ecosystem Player"
        },
        "template_base": "foundation"
    },

    "units": [
        # =====================================================================
        # CONCEPTS (5)
        # =====================================================================
        {
            "unit_type": UnitType.CONCEPT,
            "name": "Information Sovereignty",
            "definition": "A country's capacity to produce its own narratives and resist external information manipulation, particularly from hostile state actors.",
            "display_type": "Strategic Lever",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Moldova's democratic development requires building domestic capacity to produce trusted information that competes with Russian disinformation",
                    "evidence": "Surveys show 40% of Moldovans get news from Russian sources; TV news is dominated by 3 oligarch-controlled channels; independent outlets have 15% reach",
                    "warrant": "Democracy requires informed citizens; when external actors dominate the information space, democratic deliberation is compromised",
                    "counter": "Information sovereignty can become censorship; Moldova should focus on media literacy rather than trying to out-produce Russian content",
                    "rebuttal": "We're not advocating censorship, but capacity building. Media literacy and local content production are complementary, not alternatives."
                },
                "ACTOR": {
                    "proponents": "Pro-European government, Western donors, independent journalists, civil society",
                    "opponents": "Russian-aligned politicians, oligarch media owners, some who fear government control",
                    "regulators": "Broadcasting Council (captured), EU through association agreement, CoE monitoring",
                    "beneficiaries": "Independent media outlets, Moldovan citizens, democratic institutions",
                    "casualties": "Russian propaganda outlets, oligarch media empires, political actors relying on disinformation"
                },
                "TEMPORAL": {
                    "origins": "Became urgent after 2014 Ukraine crisis; Moldova recognized as target of Russian information operations",
                    "current_state": "New pro-European government since 2020 attempting reform; war in Ukraine intensified Russian disinformation; EU candidate status creates pressure for progress",
                    "trajectory": "Moving toward EU standards, but progress fragile; diaspora increasingly important audience",
                    "inflection_points": "2024 presidential election, potential gas crisis, EU accession progress",
                    "end_states": "Either robust domestic information ecosystem, or continued vulnerability to external manipulation"
                }
            }
        },
        {
            "unit_type": UnitType.CONCEPT,
            "name": "Media Ecosystem Resilience",
            "definition": "The ability of the media ecosystem as a whole to withstand shocks, adapt to change, and maintain core functions of informing citizens.",
            "display_type": "Strategic Lever",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Resilience requires diversity - multiple outlets across regions, languages, formats - not concentration of support in a few star performers",
                    "evidence": "When key outlet TV8 was taken off air in 2023, there was no equivalent replacement. Regional media is underdeveloped. Romanian-language news dominates while Russian-speakers are underserved.",
                    "warrant": "Concentrated ecosystems are fragile; diversity provides redundancy and reach into different communities",
                    "counter": "Spreading resources thin undermines quality; better to have few excellent outlets than many mediocre ones",
                    "rebuttal": "This isn't about quantity vs quality; it's about not having single points of failure. We need quality AND distribution."
                },
                "ACTOR": {
                    "proponents": "Regional media, minority language outlets, diversity advocates, decentralization supporters",
                    "opponents": "Star outlets that benefit from concentrated funding, efficiency-focused donors",
                    "regulators": "EU media pluralism standards, CoE diversity frameworks",
                    "beneficiaries": "Regional audiences, minority communities, new media entrants",
                    "casualties": "Outlets that compete for diversified funding, potential for lower individual grants"
                },
                "TEMPORAL": {
                    "origins": "Lesson learned from Eastern European media development showing fragility of concentrated investments",
                    "current_state": "Most donor funding goes to 4-5 Chisinau-based outlets; regional media severely underfunded",
                    "trajectory": "Growing recognition of need for diversification, but implementation lags",
                    "inflection_points": "Next major outlet closure, regional election stories that only local media covers, diaspora engagement success",
                    "end_states": "Either distributed resilient ecosystem, or continued dependence on few outlets that are vulnerable to capture or closure"
                }
            }
        },
        {
            "unit_type": UnitType.CONCEPT,
            "name": "Revenue Diversification",
            "definition": "Moving media outlets from donor dependency toward sustainable business models combining advertising, subscriptions, events, and strategic partnerships.",
            "display_type": "Strategic Lever",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Long-term media independence requires reducing donor dependency through multiple revenue streams, even if this means slower growth",
                    "evidence": "Average independent outlet gets 70% of revenue from donors. Advertising market is captured by oligarch media. Subscription models emerging but small. Events and training generate some revenue.",
                    "warrant": "Donor funding is volatile, creates dependency, and may not last forever; self-sustaining media is truly independent",
                    "counter": "In a small, poor market, commercial sustainability is a fantasy. Better to accept ongoing donor support than compromise journalism for revenue.",
                    "rebuttal": "This isn't about eliminating donors but reducing concentration. Even going from 70% to 50% donor revenue significantly increases resilience and independence."
                },
                "ACTOR": {
                    "proponents": "Business-minded media leaders, sustainability-focused donors, media development consultants",
                    "opponents": "Journalism purists concerned about commercial pressure, outlets comfortable with donor model",
                    "regulators": "Tax authorities, advertising regulators, donor compliance requirements",
                    "beneficiaries": "Outlets that develop business capacity, advertising industry (slightly), consultants",
                    "casualties": "Outlets that can't adapt, newsroom staff if cost-cutting required"
                },
                "TEMPORAL": {
                    "origins": "Global media sustainability movement, prompted by post-2008 donor fatigue and recognition of model fragility",
                    "current_state": "Lots of talk, limited progress. Successful micro-experiments with events and membership. Advertising limited by small market and oligarch capture.",
                    "trajectory": "Slow progress likely; major breakthroughs possible through collective advertising sales or platform revenue-sharing",
                    "inflection_points": "Successful membership model at scale, collective advertising initiative, major donor pulling out forcing adaptation",
                    "end_states": "Either diversified revenue across outlets, or permanent donor dependency with all its limitations"
                }
            }
        },
        {
            "unit_type": UnitType.CONCEPT,
            "name": "Cross-Border Content Syndication",
            "definition": "Sharing content across borders, particularly with Romania's media ecosystem, to expand reach and reduce duplication.",
            "display_type": "Strategic Lever",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Moldova should leverage cultural and linguistic ties to Romania by syndicating content, thereby reaching diaspora and reducing costs",
                    "evidence": "800K+ Moldovans in Romania and EU; Romanian media has larger budgets but covers Moldova poorly; TVR Moldova exists but is underfunded",
                    "warrant": "Shared language enables content sharing; diaspora remittances are 15% of GDP, indicating engaged diaspora; economies of scale favor larger Romanian market",
                    "counter": "Romanian media has different standards and audiences; Moldova needs authentic Moldovan voices, not Romanian imports",
                    "rebuttal": "Syndication doesn't mean replacement; it means Moldovan outlets reaching larger audiences and Romanian audiences getting Moldovan perspectives. Both preserve Moldovan voice."
                },
                "ACTOR": {
                    "proponents": "Pan-Romanian cultural advocates, diaspora organizations, efficiency-minded donors",
                    "opponents": "Moldovan nationalist media, outlets fearing competition, some Russophone media",
                    "regulators": "Broadcasting regulators in both countries, EU media cooperation frameworks",
                    "beneficiaries": "Diaspora audiences, Moldovan outlets gaining distribution, Romanian audiences interested in region",
                    "casualties": "Small outlets that can't compete with syndicated content, Moldovan identity purists"
                },
                "TEMPORAL": {
                    "origins": "Historical cultural ties; increased after 2000s EU integration of Romania and Moldova's European aspirations",
                    "current_state": "Some ad hoc sharing; Romanian TV available in Moldova; limited formal partnerships",
                    "trajectory": "Likely to increase with EU integration and war-driven interest in region",
                    "inflection_points": "Major syndication deal, policy enabling cross-border cooperation, diaspora funding initiative",
                    "end_states": "Either integrated Romanian-Moldovan media space, or continued separation with missed synergies"
                }
            }
        },
        {
            "unit_type": UnitType.CONCEPT,
            "name": "Digital-First Transition",
            "definition": "Shifting from legacy broadcast/print formats to digital platforms while retaining audience trust and developing new engagement models.",
            "display_type": "Strategic Lever",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Independent media's future is digital, where they can bypass oligarch-controlled broadcast infrastructure and reach young/diaspora audiences",
                    "evidence": "Under-35 audience is 70% digital; TV audience aging; Telegram/Facebook news groups growing; successful digital-first outlets like newsmaker.md exist",
                    "warrant": "Digital platforms reduce distribution costs, enable direct audience relationships, and aren't controlled by oligarchs",
                    "counter": "Older, rural, Russophone audiences prefer TV; digital platforms are also manipulation vectors; digital advertising doesn't cover costs",
                    "rebuttal": "Digital-first doesn't mean digital-only. We need hybrid strategies that prioritize digital while maintaining TV presence. The key is not being dependent on infrastructure others control."
                },
                "ACTOR": {
                    "proponents": "Young journalists, tech-savvy outlets, digital democracy advocates, platform companies",
                    "opponents": "Legacy media, older journalists, rural audiences, those concerned about digital divides",
                    "regulators": "Emerging digital content regulation, platform policies, EU Digital Services Act",
                    "beneficiaries": "Digital-first outlets, young audiences, diaspora, tech service providers",
                    "casualties": "Print media, some TV outlets, older journalists without digital skills"
                },
                "TEMPORAL": {
                    "origins": "Global digital transition accelerated in Moldova by COVID-19 and war in Ukraine driving online engagement",
                    "current_state": "Hybrid moment: digital growing but TV still dominant for politics; Telegram emerged as key news distribution",
                    "trajectory": "Accelerating toward digital, but uneven; TV may retain political importance",
                    "inflection_points": "Major outlet going digital-only, TV license controversy, platform policy change affecting distribution",
                    "end_states": "Either digital-dominant ecosystem with TV supplementary, or continued hybrid with ongoing infrastructure vulnerabilities"
                }
            }
        },

        # =====================================================================
        # DIALECTICS (3)
        # =====================================================================
        {
            "unit_type": UnitType.DIALECTIC,
            "name": "Independence vs Sustainability",
            "definition": "The tension between maintaining editorial independence and achieving financial sustainability.",
            "display_type": "Strategic Tension",
            "tier": UnitTier.DOMAIN,
            "content": {
                "pole_a": "Editorial Independence",
                "pole_b": "Financial Sustainability"
            },
            "grids": {
                "LOGICAL": {
                    "claim": "True independence requires financial sustainability, but the path to sustainability often compromises independence - this tension must be actively managed, not denied",
                    "evidence": "Donor-dependent outlets are beholden to donor priorities; ad-dependent outlets face commercial pressure; subscription models work for some but exclude audiences",
                    "warrant": "All funding sources create some dependency; the goal is diversification to avoid capture by any single interest",
                    "counter": "Some argue that pure journalism should be publicly funded like a utility; others argue donors are less compromising than commercial interests",
                    "rebuttal": "Public funding in Moldova risks political capture; donors may be less compromising short-term but create long-term dependency. No single solution; diversification is key."
                },
                "TEMPORAL": {
                    "origins": "Inherent tension in media, sharpened in Moldova by weak commercial market and politicized ownership",
                    "current_state": "Most outlets accept donor dependency as least-bad option; some experimenting with hybrid models",
                    "trajectory": "Growing pressure for sustainability, but commercial options remain limited",
                    "inflection_points": "Major donor policy shift, breakthrough business model, demonstration of sustainable outlet",
                    "end_states": "Either managed tension with diversified funding, or drift toward one pole or the other"
                }
            }
        },
        {
            "unit_type": UnitType.DIALECTIC,
            "name": "National Focus vs Diaspora Reach",
            "definition": "The tension between serving domestic Moldovan audiences and reaching the large diaspora in Romania and EU.",
            "display_type": "Strategic Tension",
            "tier": UnitTier.DOMAIN,
            "content": {
                "pole_a": "National/Domestic Focus",
                "pole_b": "Diaspora Reach"
            },
            "grids": {
                "LOGICAL": {
                    "claim": "Diaspora engagement is strategically valuable but must not divert resources from serving domestic audiences who face the most acute information needs",
                    "evidence": "Diaspora (1.2M) is comparable to domestic population; diaspora sends $1.5B remittances and votes in elections; but domestic audiences face oligarch media and disinformation directly",
                    "warrant": "Diaspora can provide funding, amplification, and political support; but the core mission is democratic development in Moldova, which requires reaching domestic citizens",
                    "counter": "Diaspora may be more engaged and willing to pay; focusing on diaspora might be more sustainable than fighting for scarce domestic attention",
                    "rebuttal": "Diaspora engagement should supplement, not replace, domestic focus. The goal is a complementary strategy that leverages diaspora resources for domestic impact."
                },
                "TEMPORAL": {
                    "origins": "Moldova's diaspora grew dramatically after 2000 as EU freedom of movement expanded; became politically significant with 2020 election",
                    "current_state": "Growing diaspora engagement, especially after 2020 election and 2022 war; but most outlets still focused domestically",
                    "trajectory": "Diaspora likely to become more important as population shrinks and diaspora voting power grows",
                    "inflection_points": "Diaspora-focused outlet launch, remittance-funded media initiative, diaspora voting threshold in elections",
                    "end_states": "Either integrated domestic-diaspora strategy, or continued separation with missed synergies"
                }
            }
        },
        {
            "unit_type": UnitType.DIALECTIC,
            "name": "Quality vs Engagement",
            "definition": "The tension between producing high-quality in-depth journalism and creating content that drives engagement on platforms.",
            "display_type": "Strategic Tension",
            "tier": UnitTier.DOMAIN,
            "content": {
                "pole_a": "Quality/Depth",
                "pole_b": "Engagement/Virality"
            },
            "grids": {
                "LOGICAL": {
                    "claim": "Sustainable independent media requires both quality journalism that builds credibility AND engaging content that drives reach - they are not mutually exclusive",
                    "evidence": "Pure quality outlets have limited reach; viral-focused content degrades trust. Successful hybrid examples exist (e.g., Ziarul de Garda investigations that go viral).",
                    "warrant": "Impact requires both reach and credibility; neither alone is sufficient for democratic development",
                    "counter": "The algorithm rewards sensationalism; competing on engagement means adopting oligarch media tactics",
                    "rebuttal": "Engagement doesn't require sensationalism. Compelling storytelling, visual journalism, and community engagement can drive reach while maintaining quality."
                },
                "TEMPORAL": {
                    "origins": "Tension intensified with social media and attention economy, sharpened by COVID-19 misinformation competition",
                    "current_state": "Most outlets struggle to balance; successful examples show it's possible but resource-intensive",
                    "trajectory": "Platform evolution will continue to shape this tension; AI may enable new approaches",
                    "inflection_points": "Viral quality journalism breakthrough, platform algorithm changes, new engagement models",
                    "end_states": "Either new synthesis of quality and engagement, or continued fragmentation between elite and mass media"
                }
            }
        },

        # =====================================================================
        # ACTORS (4)
        # =====================================================================
        {
            "unit_type": UnitType.ACTOR,
            "name": "Oligarch-Owned Media",
            "definition": "Media outlets controlled by politically-connected oligarchs, primarily used for political influence rather than journalism.",
            "display_type": "Ecosystem Player",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Oligarch media is the primary competitor for audience attention and the main vector for disinformation and political manipulation",
                    "evidence": "3 oligarch-controlled TV channels have 60% of audience; they amplify pro-Russian narratives; journalists are poorly paid but have largest megaphones",
                    "warrant": "Understanding competitor dynamics is essential; oligarch media defines the information environment independent media must navigate",
                    "counter": "Oligarch media is declining in influence; focusing on them gives them too much importance",
                    "rebuttal": "While influence may be declining among some demographics, they still dominate political discourse and older audiences. Ignoring them is not a viable strategy."
                },
                "ACTOR": {
                    "proponents": "Oligarchs themselves, aligned political parties, some employees dependent on jobs",
                    "opponents": "Independent media, civil society, pro-European government, Western donors",
                    "regulators": "Broadcasting Council (historically captured), new government attempts at reform, EU accession pressure",
                    "beneficiaries": "Oligarchs seeking political influence, pro-Russian political forces, some content creators with resources",
                    "casualties": "Democratic discourse, audience trust in media generally, independent competitors for audience"
                },
                "TEMPORAL": {
                    "origins": "Emerged in 1990s-2000s as business-political tool; consolidated under Plahotniuc era (2016-2019)",
                    "current_state": "Under pressure from new government but still dominant; some diversifying to digital",
                    "trajectory": "Likely slow decline as regulatory pressure increases and audiences shift digital",
                    "inflection_points": "Major oligarch prosecution, TV license revocation, ownership transparency law enforcement",
                    "end_states": "Either gradual decline to marginal influence, or adaptation that maintains political media capture"
                }
            }
        },
        {
            "unit_type": UnitType.ACTOR,
            "name": "European Funders",
            "definition": "European Union, European Endowment for Democracy, and other European foundations providing grants for independent media development.",
            "display_type": "Ecosystem Player",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "European funders are essential for independent media survival but must evolve from project-based to core support and sustainability assistance",
                    "evidence": "EED, EU, German foundations provide majority of independent media funding. Most is project-based with heavy reporting requirements. Little focus on business development.",
                    "warrant": "Funders shaped the current ecosystem; their evolution will shape future sustainability",
                    "counter": "Funders shouldn't subsidize media indefinitely; their role should be catalyst, not permanent patron",
                    "rebuttal": "We agree funders shouldn't be permanent patrons. But transition to sustainability requires different funding approaches than current project-based models."
                },
                "ACTOR": {
                    "proponents": "Independent media outlets, civil society, EU integration advocates",
                    "opponents": "Those viewing European influence as neocolonialism, sovereigntists, Russian-aligned politicians",
                    "regulators": "EU development policy, EED board, national development agencies, audit requirements",
                    "beneficiaries": "Funded outlets, media development consultants, EU foreign policy goals",
                    "casualties": "Outlets that don't fit funder priorities, local ownership of media development agenda"
                },
                "TEMPORAL": {
                    "origins": "Post-Cold War democracy promotion, intensified after 2000 with European Neighborhood Policy",
                    "current_state": "High funding availability post-Ukraine invasion; evolving toward sustainability and resilience focus",
                    "trajectory": "Likely continued high funding short-term; medium-term shift toward sustainability requirements",
                    "inflection_points": "EU policy review, major donor coordination initiative, breakthrough in sustainability models",
                    "end_states": "Either effective transition support to sustainable media, or endless dependency cycle"
                }
            }
        },
        {
            "unit_type": UnitType.ACTOR,
            "name": "Diaspora Communities",
            "definition": "Moldovan communities abroad, primarily in Romania, Italy, and Germany, who maintain cultural ties and political engagement.",
            "display_type": "Ecosystem Player",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Diaspora represents untapped resource for independent media through audience, funding, and political amplification",
                    "evidence": "1.2M diaspora (vs 2.6M domestic); $1.5B annual remittances; 300K voted in 2020 elections; active Facebook/Telegram communities; limited systematic engagement by media",
                    "warrant": "Diaspora has resources, interest, and lower capture risk than domestic audiences; but requires intentional engagement strategy",
                    "counter": "Diaspora is disconnected from daily Moldovan reality; their needs differ from domestic audiences; chasing diaspora money is distraction",
                    "rebuttal": "Diaspora stays connected precisely through media; serving their information needs can generate resources that support domestic journalism. Not either/or."
                },
                "ACTOR": {
                    "proponents": "Diaspora organizations, pan-European Moldovans, outlets already engaging diaspora",
                    "opponents": "Domestic-focused outlets seeing competition for attention, some suspicious of diaspora influence",
                    "regulators": "Diaspora voting regulations, EU media and immigration policy, remittance regulations",
                    "beneficiaries": "Outlets that successfully engage diaspora, diaspora civic organizations, Moldovan democracy",
                    "casualties": "Outlets that can't reach diaspora, domestic-only focus that misses diaspora resources"
                },
                "TEMPORAL": {
                    "origins": "Moldovan emigration grew post-2000; diaspora engagement intensified with 2020 election",
                    "current_state": "Growing diaspora media consumption and political engagement; limited systematic outlet strategies for diaspora",
                    "trajectory": "Diaspora likely to become more important as domestic population declines and diaspora political power grows",
                    "inflection_points": "Successful diaspora crowdfunding, diaspora-targeted outlet launch, diaspora voting rule changes",
                    "end_states": "Either integrated diaspora engagement strategy, or continued ad hoc approach missing opportunities"
                }
            }
        },
        {
            "unit_type": UnitType.ACTOR,
            "name": "Government Regulators",
            "definition": "The Broadcasting Council, Parliament, and other government bodies that regulate media through licensing, content rules, and ownership transparency.",
            "display_type": "Ecosystem Player",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Regulatory reform is essential for enabling independent media, but requires careful balance to avoid new forms of political control",
                    "evidence": "Broadcasting Council historically captured by oligarchs; new government attempting reform; ownership transparency laws weak; EU accession requires regulatory alignment",
                    "warrant": "Regulation shapes the competitive environment; bad regulation enabled oligarch capture, good regulation could level the playing field",
                    "counter": "Government regulation of media is inherently dangerous; Moldova should minimize regulation rather than reform it",
                    "rebuttal": "Minimizing regulation in Moldova meant oligarch self-regulation. Some regulation (ownership transparency, public interest obligations) can protect rather than threaten press freedom."
                },
                "ACTOR": {
                    "proponents": "Pro-European government, EU, media reform advocates, independent journalism advocates",
                    "opponents": "Oligarch media fearing new rules, libertarian media theorists, some who distrust any government media power",
                    "regulators": "Broadcasting Council, Parliament, Ministry of Culture, EU accession monitors",
                    "beneficiaries": "Independent media (if reforms work), audiences, democratic institutions",
                    "casualties": "Oligarch media if ownership transparency enforced, bad actors if content rules enforced"
                },
                "TEMPORAL": {
                    "origins": "Post-Soviet regulatory capture; European standards introduced through association agreement",
                    "current_state": "Reform window open with pro-European government; Broadcasting Council being reformed; ownership transparency legislation pending",
                    "trajectory": "Likely progress toward EU standards, but implementation is challenge; risk of reform reversal if government changes",
                    "inflection_points": "Key legislation passage, Broadcasting Council decision on oligarch licenses, EU accession negotiation chapter",
                    "end_states": "Either European-standard regulation enabling competition, or continued captured regulation protecting oligarchs"
                }
            }
        }
    ],

    # =========================================================================
    # EVIDENCE SOURCES
    # =========================================================================
    "evidence_sources": [
        {
            "source_name": "Moldova Media Landscape Assessment 2024",
            "source_type": EvidenceSourceType.MANUAL,
            "source_content": """Comprehensive assessment of Moldova's media ecosystem conducted for
European donors. Finds that 60% of TV audience consumes oligarch-controlled channels, while
independent outlets have 15% combined reach. Digital news consumption growing, with 70% of
under-35s primarily using online sources. Donor dependency remains at 70% for most independent
outlets. Regional media severely underfunded. Diaspora engagement growing but unsystematic.
Trust in media generally low, but higher for independent outlets among educated audiences.""",
            "fragments": [
                {
                    "content": "Oligarch-controlled television channels command 60% of total TV audience, with the three largest networks (controlled by Shor, Plahotniuc associates, and Voronin-aligned interests) dominating political coverage.",
                    "source_location": "Section 2.1, Market Structure",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Oligarch-Owned Media",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 92
                },
                {
                    "content": "Independent media outlets have a combined reach of 15% of the adult population, concentrated in Chisinau, among higher-educated demographics, and among those under 45.",
                    "source_location": "Section 2.3, Independent Media",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Information Sovereignty",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 88
                },
                {
                    "content": "Digital news consumption has grown 40% since 2020, with 70% of under-35 adults reporting online sources as their primary news channel. Telegram has emerged as the fastest-growing news distribution platform.",
                    "source_location": "Section 3.2, Digital Transition",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Digital-First Transition",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 90
                },
                {
                    "content": "Average donor dependency among independent outlets is 70%, with only 2 outlets achieving more than 40% revenue from non-donor sources. Advertising represents only 12% of independent media revenue due to market capture by oligarch outlets.",
                    "source_location": "Section 4.1, Financial Sustainability",
                    "status": AnalysisStatus.NEEDS_DECISION,
                    "confidence": 70,
                    "why_needs_decision": "This evidence could support 'Revenue Diversification' concept directly, or could strengthen the 'Independence vs Sustainability' dialectic by showing the severity of the tension",
                    "interpretations": [
                        {
                            "key": "a",
                            "title": "Supports revenue diversification case",
                            "target_unit_name": "Revenue Diversification",
                            "target_grid_slot": "LOGICAL.evidence",
                            "relationship_type": EvidenceRelationship.SUPPORTS,
                            "is_recommended": True,
                            "strategy": "Use as primary evidence for the need to diversify revenue streams",
                            "rationale": "The 70% donor dependency and 12% advertising share directly demonstrate the revenue concentration problem",
                            "commitment_statement": "Commits you to framing revenue diversification as a solvable operational challenge",
                            "foreclosure_statements": ["Framing donor dependency as acceptable steady state", "Arguing that commercial sustainability is impossible"]
                        },
                        {
                            "key": "b",
                            "title": "Deepens dialectic tension",
                            "target_unit_name": "Independence vs Sustainability",
                            "target_grid_slot": "LOGICAL.evidence",
                            "relationship_type": EvidenceRelationship.EXTENDS,
                            "is_recommended": False,
                            "strategy": "Use to quantify the severity of the independence-sustainability tension",
                            "rationale": "The data shows how constrained commercial options are, making the dialectic more acute",
                            "commitment_statement": "Commits you to treating the tension as structural rather than merely operational",
                            "foreclosure_statements": ["Simple business development solutions", "Optimistic timeline for commercial transition"]
                        }
                    ]
                },
                {
                    "content": "Regional media outside Chisinau is severely underfunded, with average regional outlet having 1/10th the budget of Chisinau-based peers. Only 3 regional outlets received international donor support in 2023.",
                    "source_location": "Section 2.5, Regional Media",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Media Ecosystem Resilience",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 85
                },
                {
                    "content": "Diaspora media consumption is growing, with estimated 400,000 Moldovans abroad regularly consuming Moldovan news online. However, systematic engagement strategies remain undeveloped.",
                    "source_location": "Section 3.4, Diaspora Audiences",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Diaspora Communities",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 78
                },
                {
                    "content": "Trust in media overall is low (28% trust media), but trust in independent outlets among their audiences is significantly higher (65%). The trust gap between independent and oligarch media has widened since 2020.",
                    "source_location": "Section 5.1, Audience Trust",
                    "status": AnalysisStatus.ANALYZED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Quality vs Engagement",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 82
                }
            ]
        },
        {
            "source_name": "EED Independent Media Support Evaluation",
            "source_type": EvidenceSourceType.MANUAL,
            "source_content": """Evaluation of European Endowment for Democracy's media support
program in Moldova. Finds that core support is more effective than project-based grants for
building institutional capacity. Sustainability initiatives have had limited success due to
market constraints. Content partnerships with Romanian media show promise. Regional distribution
of support needs improvement. Recommends shift toward sustainability-focused support with
longer grant cycles.""",
            "fragments": [
                {
                    "content": "Core institutional support showed significantly better outcomes than project-based grants, with outlets receiving core support 3x more likely to develop internal capacity and 2x more likely to retain talent.",
                    "source_location": "Finding 2.3, Grant Modalities",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "European Funders",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 86
                },
                {
                    "content": "Sustainability initiatives have had limited success, with only 2 of 15 supported outlets achieving meaningful progress toward commercial revenue. Key barriers include small market size, advertiser capture by oligarch media, and lack of business skills.",
                    "source_location": "Finding 3.1, Sustainability Challenges",
                    "status": AnalysisStatus.NEEDS_DECISION,
                    "confidence": 68,
                    "why_needs_decision": "Could be used to temper optimism about revenue diversification OR to support the case for business capacity building",
                    "interpretations": [
                        {
                            "key": "a",
                            "title": "Qualifies diversification optimism",
                            "target_unit_name": "Revenue Diversification",
                            "target_grid_slot": "LOGICAL.counter",
                            "relationship_type": EvidenceRelationship.QUALIFIES,
                            "is_recommended": True,
                            "strategy": "Use as evidence for the counter-argument that sustainability is difficult in Moldova's market",
                            "rationale": "The 2/15 success rate provides empirical grounding for skepticism about quick commercial transitions",
                            "commitment_statement": "Commits you to realistic expectations about sustainability timeline",
                            "foreclosure_statements": ["Over-promising commercial sustainability", "Suggesting donor exit within 5 years"]
                        },
                        {
                            "key": "b",
                            "title": "Supports capacity building need",
                            "target_unit_name": "European Funders",
                            "target_grid_slot": "LOGICAL.warrant",
                            "relationship_type": EvidenceRelationship.EXTENDS,
                            "is_recommended": False,
                            "strategy": "Use to argue for business skills development as part of funder support",
                            "rationale": "The 'lack of business skills' finding suggests capacity gaps that funders could address",
                            "commitment_statement": "Commits you to advocating for business development support from European funders",
                            "foreclosure_statements": ["Pure journalism focus in funder support", "Hands-off approach to outlet operations"]
                        }
                    ]
                },
                {
                    "content": "Content partnerships with Romanian media have shown promise, with 3 outlets achieving significant audience expansion through syndication. These partnerships also generated modest revenue through content licensing.",
                    "source_location": "Finding 4.2, Cross-Border Cooperation",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Cross-Border Content Syndication",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 80
                },
                {
                    "content": "Regional distribution of EED support is heavily weighted toward Chisinau: 85% of funding goes to capital-based outlets. This concentration may be limiting ecosystem resilience and excluding regional voices.",
                    "source_location": "Finding 5.1, Geographic Distribution",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.QUALIFIES,
                    "target_unit_name": "Media Ecosystem Resilience",
                    "target_grid_slot": "ACTOR.casualties",
                    "confidence": 84
                },
                {
                    "content": "Outlets with 3-year grant cycles showed significantly better strategic planning and staff retention than those with annual funding cycles. Recommendation is to move toward longer funding horizons with milestone-based reviews.",
                    "source_location": "Recommendation 2, Grant Duration",
                    "status": AnalysisStatus.ANALYZED,
                    "relationship_type": EvidenceRelationship.EXTENDS,
                    "target_unit_name": "Independence vs Sustainability",
                    "target_grid_slot": "TEMPORAL.trajectory",
                    "confidence": 76
                },
                {
                    "content": "Digital transition support has been underprioritized relative to its strategic importance. Only 15% of media support budget has gone to digital capacity building despite digital being the growth frontier.",
                    "source_location": "Finding 4.5, Digital Investment",
                    "status": AnalysisStatus.PENDING,
                    "confidence": 0
                },
                {
                    "content": "Coordination among European funders has improved but remains suboptimal. Overlapping support and gaps persist, with some outlets over-funded while strategic gaps remain unaddressed.",
                    "source_location": "Finding 6.1, Donor Coordination",
                    "status": AnalysisStatus.PENDING,
                    "confidence": 0
                }
            ]
        }
    ]
}
