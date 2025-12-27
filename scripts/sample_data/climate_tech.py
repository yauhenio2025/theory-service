"""
Climate Tech Investment Strategy - Sample Project Data

A comprehensive sample project demonstrating:
- 6 concepts, 3 dialectics, 4 actors (13 units total)
- Full grid content for each unit (LOGICAL, ACTOR, TEMPORAL)
- 3 evidence sources with 20+ fragments
- Mix of INTEGRATED, NEEDS_DECISION, ANALYZED, and PENDING fragments
"""

from api.strategizer.models import (
    UnitType, UnitTier, UnitStatus, GridTier,
    EvidenceSourceType, ExtractionStatus, AnalysisStatus, EvidenceRelationship
)

CLIMATE_TECH_PROJECT = {
    "name": "Climate Tech Investment Strategy",
    "brief": """We are launching a $100M climate tech fund targeting breakthrough technologies
in carbon capture, green hydrogen, grid-scale storage, and sustainable materials. We want to
develop a framework for evaluating climate tech opportunities that balances financial returns
with climate impact. Key questions include: How do we assess deep tech defensibility? When
should we prioritize climate impact over returns? How do we navigate the tension between
long VC fund lifecycles and even longer deep tech timelines?""",

    "domain": {
        "name": "Climate Tech Venture Investment",
        "core_question": "Where should we deploy capital for maximum climate impact while achieving venture returns?",
        "success_looks_like": "A deployed fund with clear thesis on defensibility, impact measurement, and portfolio construction that attracts top climate founders",
        "vocabulary": {
            "concept": "Investment Thesis",
            "dialectic": "Strategic Trade-off",
            "actor": "Market Player"
        },
        "template_base": "investment"
    },

    "units": [
        # =====================================================================
        # CONCEPTS (6)
        # =====================================================================
        {
            "unit_type": UnitType.CONCEPT,
            "name": "Technical Defensibility",
            "definition": "The ability of a climate tech company to build durable competitive moats through patents, proprietary processes, and deep technical know-how that cannot be easily replicated.",
            "display_type": "Investment Thesis",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Deep tech companies with strong IP and process know-how can build durable competitive moats in climate tech",
                    "evidence": "Analysis of 50 climate tech exits shows patent portfolio correlates 0.72 with acquisition premium; Breakthrough Energy portfolio companies with 10+ patents see 3x higher follow-on rates",
                    "warrant": "In capital-intensive industries with long development cycles, replication barriers matter more than speed-to-market. Climate tech hardware requires specialized manufacturing that takes years to develop.",
                    "counter": "Open-source approaches and rapid iteration may outpace patent-protected innovation. Tesla open-sourced its patents yet maintained market leadership.",
                    "rebuttal": "While true for software-centric climate solutions, hardware-intensive climate tech (carbon capture, green hydrogen) requires capital that patents help attract. The Tesla case involves consumer products with brand moats, not industrial technology."
                },
                "ACTOR": {
                    "proponents": "Deep tech VCs (Lux Capital, DCVC, Breakthrough Energy), university tech transfer offices, national labs with licensing programs",
                    "opponents": "Open innovation advocates, some climate activists who prioritize speed of deployment over returns",
                    "regulators": "USPTO, DOE with tech transfer mandates, ARPA-E program office",
                    "beneficiaries": "Founders with PhDs and lab experience, universities with strong IP practices, patent attorneys",
                    "casualties": "Fast-follower startups that cannot afford long R&D cycles, developing countries that need technology transfer"
                },
                "TEMPORAL": {
                    "origins": "Emerged from biotech and semiconductor investment patterns in the 1980s-90s, adapted to cleantech 1.0 failures (2008-2012) that revealed importance of hard moats",
                    "current_state": "Increasing focus on defensibility as climate tech matures beyond subsidized markets; 2023 saw record patent filings in carbon capture and hydrogen",
                    "trajectory": "Will intensify as more capital chases fewer breakthrough opportunities; expect patent thickets and cross-licensing deals similar to semiconductor industry",
                    "inflection_points": "Major patent disputes (like solar IP wars), open-source breakthroughs, or regulatory mandates for technology sharing",
                    "end_states": "Either a well-functioning IP market enabling investment, or a tragedy of the anti-commons blocking deployment"
                }
            }
        },
        {
            "unit_type": UnitType.CONCEPT,
            "name": "Climate Impact Potential",
            "definition": "The potential for a technology to reduce gigatons of CO2 equivalent emissions at scale, considering both direct impact and system-level effects.",
            "display_type": "Investment Thesis",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Climate tech investments should be evaluated primarily on potential gigatons of CO2e reduction at scale, not just financial returns",
                    "evidence": "Project Drawdown ranks solutions by potential impact; top 10 solutions account for 60% of reduction potential. Climate investments in high-impact sectors show 40% higher LP interest.",
                    "warrant": "The purpose of a climate fund is climate impact; financial returns are necessary for sustainability but not sufficient for mission alignment",
                    "counter": "Impact measurement is imprecise and gameable; a profitable company can reinvest in more impact while an impactful but unprofitable company achieves nothing",
                    "rebuttal": "While measurement is imperfect, ignoring impact potential leads to greenwashing. We can use conservative estimates and focus on technologies with clear attribution."
                },
                "ACTOR": {
                    "proponents": "Impact-focused LPs (foundations, family offices), climate scientists on advisory boards, NGOs tracking corporate climate commitments",
                    "opponents": "Traditional VCs focused on pure returns, some founders who see impact metrics as burdensome",
                    "regulators": "SEC with climate disclosure rules, EU with taxonomy requirements, California's climate-related financial risk legislation",
                    "beneficiaries": "Companies with high-impact technologies that might not meet traditional VC hurdles, communities affected by climate change",
                    "casualties": "Companies with incremental improvements, investors who cannot measure or report impact"
                },
                "TEMPORAL": {
                    "origins": "Roots in ESG investing (1990s), accelerated by Paris Agreement (2015), and mainstreamed by net-zero commitments (2020+)",
                    "current_state": "Rapidly evolving impact measurement standards; tension between rigorous measurement and practical deployment",
                    "trajectory": "Expect convergence on standards, mandatory disclosure, and integration into mainstream valuation models",
                    "inflection_points": "Major greenwashing scandal, successful carbon market, or breakthrough in measurement technology",
                    "end_states": "Either impact becomes fully integrated into financial analysis, or remains a separate track for mission-driven capital"
                }
            }
        },
        {
            "unit_type": UnitType.CONCEPT,
            "name": "Path to Scale Economics",
            "definition": "The trajectory by which unit economics become viable at production scale, considering learning curves, manufacturing scale-ups, and market development.",
            "display_type": "Investment Thesis",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Climate tech investments should target technologies with clear learning curves that reach cost parity with fossil alternatives at scale",
                    "evidence": "Solar PV followed an 24% learning curve for 40 years; battery storage is on similar trajectory. Technologies without learning curve evidence have higher failure rates.",
                    "warrant": "Subsidy-dependent technologies are politically vulnerable; sustainable impact requires market competitiveness",
                    "counter": "Some technologies with high strategic value (long-duration storage, sustainable aviation fuel) may never reach cost parity but are still essential for net zero",
                    "rebuttal": "While some strategic technologies require ongoing support, a VC fund needs most investments to achieve unsubsidized viability within fund lifetime"
                },
                "ACTOR": {
                    "proponents": "Manufacturing-focused VCs, operations-focused founders, utilities planning procurement",
                    "opponents": "Research-focused scientists who see commercialization pressure as premature, policy advocates focused on deployment subsidies",
                    "regulators": "DOE loan program office, state clean energy standards setters, manufacturing incentive programs",
                    "beneficiaries": "First-mover manufacturers who ride the learning curve, countries building clean energy industrial bases",
                    "casualties": "Late entrants who compete against learned-out incumbents, stranded fossil assets"
                },
                "TEMPORAL": {
                    "origins": "Learning curve economics from Wright's Law (1936), applied to energy by Swanson (2006), now central to climate modeling",
                    "current_state": "Solar and onshore wind have achieved parity; offshore wind, storage, and hydrogen approaching; DAC and SAF still distant",
                    "trajectory": "Expect S-curve adoption as technologies cross parity thresholds; hydrogen likely next major transition",
                    "inflection_points": "Green hydrogen reaching $2/kg, solid-state batteries hitting 500 Wh/kg, DAC crossing $200/ton",
                    "end_states": "Either a clean energy economy with competitive alternatives in all sectors, or persistent gaps requiring permanent subsidy"
                }
            }
        },
        {
            "unit_type": UnitType.CONCEPT,
            "name": "Policy Tailwinds",
            "definition": "How government policy accelerates or enables technology adoption through mandates, incentives, procurement, and standard-setting.",
            "display_type": "Investment Thesis",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Climate tech investments should prioritize sectors with strong policy tailwinds that de-risk market development",
                    "evidence": "IRA allocated $369B to clean energy; EU Green Deal mobilizes similar scale. Solar deployment increased 10x after feed-in tariffs; EV adoption accelerated with tax credits.",
                    "warrant": "Policy creates guaranteed demand, reduces technology risk, and attracts follow-on capital in capital-intensive sectors",
                    "counter": "Policy is politically fragile; cleantech 1.0 collapsed when subsidies were cut. Over-reliance on policy creates stranded investment risk.",
                    "rebuttal": "Current policy is more durable (IRA structured as tax credits, not appropriations), and we can mitigate by investing in technologies approaching unsubsidized viability"
                },
                "ACTOR": {
                    "proponents": "Policy-aware VCs, government affairs teams at portfolio companies, clean energy industry associations",
                    "opponents": "Libertarian investors skeptical of government intervention, fossil fuel lobbies seeking to block climate policy",
                    "regulators": "EPA setting emissions standards, DOE running demonstration programs, state utility commissions",
                    "beneficiaries": "Technologies aligned with current policy priorities, domestic manufacturers benefiting from local content requirements",
                    "casualties": "Technologies not included in policy support, imported technologies excluded by local content rules"
                },
                "TEMPORAL": {
                    "origins": "Modern roots in 1970s energy crisis response, accelerated by 2009 stimulus, transformed by 2022 IRA",
                    "current_state": "Unprecedented policy support globally; US, EU, and China in industrial policy competition",
                    "trajectory": "Expect continued escalation as climate impacts intensify and green industrial competition accelerates",
                    "inflection_points": "2024/2028 US elections, next major climate disaster, breakthrough in carbon border adjustment implementation",
                    "end_states": "Either sustained global policy alignment enabling transition, or political backlash and policy whiplash"
                }
            }
        },
        {
            "unit_type": UnitType.CONCEPT,
            "name": "Market Timing Risk",
            "definition": "The gap between when a technology is technically ready and when the market is ready to adopt it at scale.",
            "display_type": "Investment Thesis",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Many climate tech failures result from technology-market timing mismatch rather than technology failure itself",
                    "evidence": "Cleantech 1.0 companies like Solyndra failed despite working technology because Chinese competition and low gas prices closed the market window. First-gen EV companies preceded market readiness by a decade.",
                    "warrant": "Venture returns require market timing; technologies that work but cannot find market fit within fund lifecycles are failures",
                    "counter": "Patient capital and longer fund structures can wait for market readiness; the climate crisis demands investment even in poorly-timed technologies",
                    "rebuttal": "While some patient capital exists, most VCs operate on 10-year fund cycles. We need both market-timed investments and policy advocacy to accelerate market readiness."
                },
                "ACTOR": {
                    "proponents": "Experienced cleantech 1.0 investors, market-savvy founders, industry analysts",
                    "opponents": "Mission-driven investors willing to accept timing risk, deep tech academics focused on breakthrough potential",
                    "regulators": "Industrial policy makers who can influence market timing through procurement and mandates",
                    "beneficiaries": "Well-timed entrants who capture market inflection points",
                    "casualties": "Pioneers who prove technology but exhaust capital before market readiness, investors in poorly-timed funds"
                },
                "TEMPORAL": {
                    "origins": "Learned painfully from cleantech 1.0 collapse (2008-2012), formalized in subsequent investment theses",
                    "current_state": "Current wave appears better timed with policy support, but still risks in hydrogen, DAC, and SAF",
                    "trajectory": "Expect continued iteration on timing frameworks, with more sophisticated market readiness assessment",
                    "inflection_points": "Major market windows opening (hydrogen offtake, carbon removal purchases), or closing (policy reversal, technology leap)",
                    "end_states": "Either refined timing frameworks improve success rates, or the field accepts higher failure rates as cost of climate urgency"
                }
            }
        },
        {
            "unit_type": UnitType.CONCEPT,
            "name": "Incumbent Disruption Potential",
            "definition": "How a technology threatens existing industry players and/or creates opportunities for partnership with them.",
            "display_type": "Investment Thesis",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Climate tech that partners with incumbents often scales faster than pure disruption plays",
                    "evidence": "Heliogen partnered with utilities; Carbon Engineering with Oxy. Pure disruptors like early EV companies faced distribution challenges until Tesla built its own network.",
                    "warrant": "Incumbents control infrastructure, distribution, and customer relationships essential for scale",
                    "counter": "Incumbent partnership can lead to capture and suppression of disruptive technology to protect existing business",
                    "rebuttal": "Partnership structure matters; licensing/offtake agreements preserve startup independence while accessing incumbent resources. The key is negotiating from strength."
                },
                "ACTOR": {
                    "proponents": "Strategics seeking energy transition positioning, corporate VC arms, founders with industry backgrounds",
                    "opponents": "Disruptive founders who see incumbents as the enemy, environmental advocates suspicious of fossil fuel partnerships",
                    "regulators": "Antitrust authorities monitoring acquisitions, industrial policy makers shaping competitive dynamics",
                    "beneficiaries": "Technologies that can sell to incumbents (CCUS, hydrogen), incumbents who successfully transition",
                    "casualties": "Pure-play disruptors who cannot access distribution, incumbents who fail to adapt"
                },
                "TEMPORAL": {
                    "origins": "Clayton Christensen disruption theory (1997) adapted to energy, tested by solar industry evolution",
                    "current_state": "Increasing incumbent engagement as net-zero commitments require technology solutions",
                    "trajectory": "Expect more strategic investment, joint ventures, and acquisitions as pressure mounts",
                    "inflection_points": "Major oil company spin-off of clean energy assets, antitrust action against incumbent acquisitions",
                    "end_states": "Either incumbents successfully transition (and dominate clean economy), or new entrants displace them"
                }
            }
        },

        # =====================================================================
        # DIALECTICS (3)
        # =====================================================================
        {
            "unit_type": UnitType.DIALECTIC,
            "name": "Climate Impact vs Financial Returns",
            "definition": "The core tension between maximizing emissions reduction and maximizing financial returns to LPs.",
            "display_type": "Strategic Trade-off",
            "tier": UnitTier.DOMAIN,
            "content": {
                "pole_a": "Climate Impact",
                "pole_b": "Financial Returns"
            },
            "grids": {
                "LOGICAL": {
                    "claim": "A climate fund can achieve both top-quartile returns AND meaningful climate impact, but must explicitly navigate trade-offs rather than pretending alignment",
                    "evidence": "Generation Investment Management and Breakthrough Energy have demonstrated strong returns and impact, but both acknowledge sector constraints and trade-offs",
                    "warrant": "Pretending perfect alignment leads to greenwashing; explicit trade-off frameworks enable honest decision-making",
                    "counter": "The best climate investments ARE the best financial investments because policy and market trends favor them",
                    "rebuttal": "While correlation is increasing, there are still cases where higher-impact investments have worse risk-adjusted returns. Honest frameworks help navigate these."
                },
                "TEMPORAL": {
                    "origins": "Emerged from 1990s ESG debates, sharpened by cleantech 1.0 failures that raised questions about returns, and impact investing movement's struggle with 'concessionary returns'",
                    "current_state": "Current consensus attempts to resolve tension by claiming alignment, but sophisticated practitioners acknowledge persistent trade-offs",
                    "trajectory": "Expect greater differentiation between impact-first and returns-first climate funds, with explicit positioning",
                    "inflection_points": "Major fund demonstrating superior returns through impact focus, or fund failure blamed on impact-over-returns bias",
                    "end_states": "Either market fully integrates climate risk/opportunity (resolving tension), or permanent segmentation between impact and financial capital"
                }
            }
        },
        {
            "unit_type": UnitType.DIALECTIC,
            "name": "Deep Tech Timeline vs VC Fund Lifecycle",
            "definition": "The tension between climate deep tech's 10-15 year development cycles and traditional VC's 7-10 year fund structures.",
            "display_type": "Strategic Trade-off",
            "tier": UnitTier.DOMAIN,
            "content": {
                "pole_a": "Deep Tech Timeline (10-15 years)",
                "pole_b": "VC Fund Lifecycle (7-10 years)"
            },
            "grids": {
                "LOGICAL": {
                    "claim": "VC fund structures are fundamentally misaligned with climate deep tech timelines, requiring either fund structure innovation or investment stage optimization",
                    "evidence": "FOAK projects in carbon capture and green hydrogen typically take 7-12 years from lab to commercial scale. Traditional VC funds have 10-year terms with 5-year investment periods.",
                    "warrant": "Investors cannot return capital if technologies haven't reached commercial milestones by fund end",
                    "counter": "Strategic exits and secondary markets can provide liquidity before full commercial deployment",
                    "rebuttal": "Strategic exits are viable but often value-destroying; secondary markets for deep tech are thin. The fundamental timeline mismatch remains."
                },
                "TEMPORAL": {
                    "origins": "Cleantech 1.0 revealed the mismatch; early funds extended terms or wrote off investments that hadn't commercialized",
                    "current_state": "New fund structures emerging (15-year funds, evergreen structures, project finance hybrids)",
                    "trajectory": "Expect continued innovation in fund structure and more explicit stage segmentation",
                    "inflection_points": "Major deep tech fund demonstrating returns with longer structure, or LP rejection of extended timelines",
                    "end_states": "Either new fund structures become standard for climate deep tech, or the sector relies primarily on non-VC capital"
                }
            }
        },
        {
            "unit_type": UnitType.DIALECTIC,
            "name": "First Mover vs Fast Follower",
            "definition": "Whether to invest in category-defining first movers or wait for fast followers who learn from pioneers' mistakes.",
            "display_type": "Strategic Trade-off",
            "tier": UnitTier.DOMAIN,
            "content": {
                "pole_a": "First Mover Advantage",
                "pole_b": "Fast Follower Learning"
            },
            "grids": {
                "LOGICAL": {
                    "claim": "In capital-intensive climate tech, fast followers often outperform first movers who bear technology and market development costs",
                    "evidence": "Chinese solar manufacturers overtook First Solar; Korean battery makers learned from Japanese pioneers. However, Tesla's first-mover EV position proved durable.",
                    "warrant": "First movers in hardware sectors face high capex risk and educate the market for followers",
                    "counter": "First movers can build customer relationships, manufacturing learning, and brand that followers cannot replicate",
                    "rebuttal": "Both patterns exist; the key is identifying which dynamics dominate in each sector. Patent-protected, relationship-intensive businesses favor first movers."
                },
                "TEMPORAL": {
                    "origins": "Classic strategy question, applied to cleantech after observing solar and wind industry evolution",
                    "current_state": "Current generation more cautious about first-mover investment, but policy tailwinds create first-mover windows",
                    "trajectory": "Expect more sophisticated timing frameworks that identify first-mover windows and fast-follower opportunities",
                    "inflection_points": "Policy changes that close first-mover windows, technology breakthroughs that reset competitive positions",
                    "end_states": "Either continued sector-by-sector variation, or pattern convergence as climate tech matures"
                }
            }
        },

        # =====================================================================
        # ACTORS (4)
        # =====================================================================
        {
            "unit_type": UnitType.ACTOR,
            "name": "DOE & National Labs",
            "definition": "The US Department of Energy and its network of national laboratories that conduct fundamental research, de-risk technologies, and provide loan guarantees for first-of-a-kind projects.",
            "display_type": "Market Player",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "DOE and national labs are essential for de-risking pre-commercial climate tech, enabling VC investment at earlier stages",
                    "evidence": "ARPA-E portfolio has generated $8B in follow-on private investment. LPO has supported numerous first-of-kind projects including Tesla Motors loan.",
                    "warrant": "Private capital cannot absorb full technology risk for frontier climate tech; public investment crowds in rather than crowds out private capital",
                    "counter": "Government involvement picks winners, distorts markets, and can create dependencies on continued support",
                    "rebuttal": "Well-designed programs (competitive selection, private co-investment requirements) avoid these pitfalls. The Tesla LPO loan was repaid early with interest."
                },
                "ACTOR": {
                    "proponents": "Climate tech ecosystem, university researchers, industrial policy advocates",
                    "opponents": "Small-government conservatives, fossil fuel lobbies, some libertarian VCs",
                    "regulators": "Congressional appropriators, OMB, GAO oversight",
                    "beneficiaries": "Startups spinning out lab technology, established companies accessing demonstration funding, regions hosting national labs",
                    "casualties": "Technologies not selected for support, private R&D crowded out in supported areas"
                },
                "TEMPORAL": {
                    "origins": "Manhattan Project and Cold War origins, expanded to energy after 1970s crises, climate focus accelerated under Obama",
                    "current_state": "Historic funding from IRA and BIL; rapid expansion of programs and authorities",
                    "trajectory": "Expect continued expansion regardless of administration, though program emphasis may shift",
                    "inflection_points": "2024 election, major program success or scandal, China competition escalation",
                    "end_states": "Either permanent industrial policy infrastructure, or retrenchment under future deregulatory pressure"
                }
            }
        },
        {
            "unit_type": UnitType.ACTOR,
            "name": "Oil & Gas Majors",
            "definition": "Large integrated oil and gas companies like ExxonMobil, Chevron, Shell, and BP that control vast infrastructure, capital, and talent potentially applicable to energy transition.",
            "display_type": "Market Player",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Oil majors are essential partners for scaling climate tech, despite legitimate concerns about greenwashing and capture",
                    "evidence": "Oxy's investment in Carbon Engineering, Chevron's investment in ChargerHelp, Shell's investment in nature-based solutions. Majors control 80% of industrial decarbonization infrastructure.",
                    "warrant": "Climate tech cannot scale without incumbent infrastructure, capital, and offtake agreements; engagement is preferable to confrontation",
                    "counter": "Major partnership is a Faustian bargain; they will use technology to extend fossil fuel extraction and suppress genuinely disruptive alternatives",
                    "rebuttal": "Partnership structure matters. Strategic minority investments, licensing, and offtake agreements can access resources while preserving startup independence. The alternative is slower deployment."
                },
                "ACTOR": {
                    "proponents": "Industry transition advocates, realist environmentalists, investor-led engagement initiatives like CA100+",
                    "opponents": "Divestment movement, environmental justice advocates, renewable purists",
                    "regulators": "SEC on climate disclosure, antitrust authorities on acquisitions, state AGs on climate fraud",
                    "beneficiaries": "Technologies aligned with oil major decarbonization pathways (CCUS, blue hydrogen, SAF)",
                    "casualties": "Pure disruption plays that threaten core oil business, communities harmed by continued extraction"
                },
                "TEMPORAL": {
                    "origins": "Majors began climate positioning in 2000s, accelerated by shareholder pressure and net-zero commitments post-2015",
                    "current_state": "Mixed signals: record profits reinvested in production, but growing transition investments. European majors ahead of US.",
                    "trajectory": "Expect continued divergence between US (doubling down on oil) and European (transitioning) majors",
                    "inflection_points": "Major stranded asset writedown, activist campaign success, government mandate for transition investment",
                    "end_states": "Either successful transition to diversified energy companies, or death spiral as clean energy disrupts core business"
                }
            }
        },
        {
            "unit_type": UnitType.ACTOR,
            "name": "Utilities",
            "definition": "Electric utilities that own and operate grid infrastructure, purchase power, and increasingly invest in distributed energy resources.",
            "display_type": "Market Player",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Utilities are becoming critical climate tech customers and investors as they face decarbonization mandates and grid modernization needs",
                    "evidence": "Utilities are largest buyers of grid storage, primary offtakers for utility-scale renewables, and increasingly investing in distributed resources through venture arms",
                    "warrant": "The electricity sector is 25% of emissions and the gateway to electrification of transport and buildings; utility procurement drives technology deployment",
                    "counter": "Utilities are inherently conservative, slow-moving, and captured by existing asset bases; they will resist disruptive technology",
                    "rebuttal": "While true historically, regulatory mandates and competitive pressure from distributed energy are forcing utility innovation. The key is targeting progressive utilities and regulators."
                },
                "ACTOR": {
                    "proponents": "Progressive utilities like NextEra, utility venture arms, grid modernization advocates",
                    "opponents": "Conservative utilities defending coal assets, rooftop solar competitors, energy democracy advocates",
                    "regulators": "State PUCs setting rate structures, FERC on wholesale markets, RTOs/ISOs operating grids",
                    "beneficiaries": "Grid storage, VPP, grid software companies that sell to utilities",
                    "casualties": "Distributed energy companies that compete with utilities, stranded utility assets"
                },
                "TEMPORAL": {
                    "origins": "Utilities were climate laggards through 2010s, began shifting as solar/wind economics improved and regulations tightened",
                    "current_state": "Rapid transformation in progressive states, resistance in conservative states; massive capital deployment needed for grid modernization",
                    "trajectory": "Expect continued acceleration as EV charging and building electrification create massive load growth requiring grid investment",
                    "inflection_points": "Major grid failure attributed to insufficient investment, successful utility business model reform, federal transmission policy",
                    "end_states": "Either reformed utilities as clean energy platforms, or continued fragmentation between utility and distributed energy models"
                }
            }
        },
        {
            "unit_type": UnitType.ACTOR,
            "name": "Strategic Corporate Investors",
            "definition": "Large corporations like Google, Amazon, Microsoft, and Salesforce making climate commitments that drive technology procurement and investment.",
            "display_type": "Market Player",
            "tier": UnitTier.DOMAIN,
            "grids": {
                "LOGICAL": {
                    "claim": "Corporate climate commitments are creating massive demand pull for climate tech, making strategics essential customers and investors",
                    "evidence": "Frontier carbon removal commitment ($925M), Microsoft's $1B Climate Innovation Fund, Google's 24/7 carbon-free energy goal driving storage innovation",
                    "warrant": "Corporate procurement can de-risk first-of-kind projects and provide patient offtake agreements that enable project financing",
                    "counter": "Corporate commitments are often greenwashing; voluntary action is insufficient without policy mandates",
                    "rebuttal": "While some commitments are weak, sophisticated corporate procurement (like Frontier's rigorous standards) can drive genuine innovation. The key is distinguishing credible from performative commitments."
                },
                "ACTOR": {
                    "proponents": "Corporate sustainability officers, climate-focused corporate VCs, ESG-motivated institutional investors",
                    "opponents": "Greenwashing watchdogs, mandatory regulation advocates, shareholder primacy traditionalists",
                    "regulators": "FTC on green claims, SEC on climate disclosure, international voluntary standards bodies",
                    "beneficiaries": "Technologies aligned with corporate decarbonization pathways (renewables, carbon removal, efficiency)",
                    "casualties": "Companies that cannot meet corporate procurement standards, competitors excluded from corporate VC networks"
                },
                "TEMPORAL": {
                    "origins": "Corporate sustainability began in 1990s as risk management, became strategic under net-zero pressure post-2015",
                    "current_state": "Rapid escalation of commitments, but execution gaps and credibility concerns; Frontier and similar initiatives raising the bar",
                    "trajectory": "Expect consolidation around high-integrity commitments, regulatory backstops for claims, and integration with mandatory disclosure",
                    "inflection_points": "Major greenwashing scandal, success of ambitious buyer coalitions, mandatory scope 3 disclosure",
                    "end_states": "Either corporate action becomes standard practice with strong accountability, or credibility collapse leads to regulation-only approach"
                }
            }
        }
    ],

    # =========================================================================
    # EVIDENCE SOURCES
    # =========================================================================
    "evidence_sources": [
        {
            "source_name": "BloombergNEF Climate Tech Report 2024",
            "source_type": EvidenceSourceType.MANUAL,
            "source_content": """Global climate tech investment reached $70B in 2023, with carbon capture
and green hydrogen seeing the largest YoY growth at 45% and 62% respectively. The report finds that
climate tech companies with strong patent portfolios command 30% higher valuations. First-of-a-kind
projects remain the hardest to finance, with an average 'valley of death' period of 7-12 years.
Policy tailwinds from IRA are reshaping investment geography, with US share of climate VC rising
from 40% to 52% YoY. Corporate buyers are increasingly important, with Fortune 500 climate procurement
growing 3x since 2020.""",
            "fragments": [
                {
                    "content": "Global climate tech investment reached $70B in 2023, with carbon capture and green hydrogen seeing the largest YoY growth at 45% and 62% respectively.",
                    "source_location": "Page 3, Executive Summary",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Climate Impact Potential",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 92
                },
                {
                    "content": "Climate tech companies with strong patent portfolios command 30% higher valuations than comparable companies without IP protection.",
                    "source_location": "Page 12, IP Analysis Section",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Technical Defensibility",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 88
                },
                {
                    "content": "First-of-a-kind (FOAK) climate tech projects face a 'valley of death' between pilot and commercial scale, with average timelines of 7-12 years from lab to market.",
                    "source_location": "Page 24, FOAK Analysis",
                    "status": AnalysisStatus.NEEDS_DECISION,
                    "confidence": 65,
                    "why_needs_decision": "This fragment could strengthen either the 'Deep Tech Timeline vs VC Fund Lifecycle' dialectic or the 'Market Timing Risk' concept - user needs to choose primary placement",
                    "interpretations": [
                        {
                            "key": "a",
                            "title": "Supports timeline-lifecycle dialectic",
                            "target_unit_name": "Deep Tech Timeline vs VC Fund Lifecycle",
                            "target_grid_slot": "LOGICAL.evidence",
                            "relationship_type": EvidenceRelationship.SUPPORTS,
                            "is_recommended": True,
                            "strategy": "Use as primary evidence for the structural misalignment between deep tech development and VC fund cycles",
                            "rationale": "The 7-12 year FOAK timeline directly demonstrates why traditional 10-year VC structures are problematic for deep tech investments",
                            "commitment_statement": "Accepting this placement commits you to emphasizing fund structure innovation as a key solution to climate tech investment challenges",
                            "foreclosure_statements": ["Alternative framing as primarily a market timing issue", "Emphasis on project finance rather than venture capital solutions"]
                        },
                        {
                            "key": "b",
                            "title": "Deepens market timing risk concept",
                            "target_unit_name": "Market Timing Risk",
                            "target_grid_slot": "LOGICAL.evidence",
                            "relationship_type": EvidenceRelationship.SUPPORTS,
                            "is_recommended": False,
                            "strategy": "Use to quantify the typical technology-market gap in climate deep tech",
                            "rationale": "The timeline data helps investors understand typical development periods for assessing market readiness alignment",
                            "commitment_statement": "Accepting this placement commits you to framing the problem as primarily about timing skill rather than structural capital constraints",
                            "foreclosure_statements": ["Emphasis on fund structure innovation", "Focus on patient capital as structural solution"]
                        }
                    ]
                },
                {
                    "content": "US share of climate VC rose from 40% to 52% YoY, driven primarily by IRA incentives and domestic content requirements.",
                    "source_location": "Page 36, Geographic Analysis",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Policy Tailwinds",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 85
                },
                {
                    "content": "Corporate climate procurement by Fortune 500 companies has grown 3x since 2020, with technology giants leading demand for carbon removal and 24/7 renewable matching.",
                    "source_location": "Page 42, Corporate Buyer Section",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Strategic Corporate Investors",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 90
                },
                {
                    "content": "Early-stage climate tech valuations declined 25% in 2023 while growth-stage valuations remained stable, suggesting investor preference for de-risked opportunities.",
                    "source_location": "Page 8, Valuation Trends",
                    "status": AnalysisStatus.ANALYZED,
                    "relationship_type": EvidenceRelationship.QUALIFIES,
                    "target_unit_name": "Technical Defensibility",
                    "target_grid_slot": "LOGICAL.counter",
                    "confidence": 70
                },
                {
                    "content": "The gap between announced corporate climate commitments and actual procurement contracts widened in 2023, with only 35% of commitments backed by binding agreements.",
                    "source_location": "Page 45, Commitment Tracking",
                    "status": AnalysisStatus.PENDING,
                    "confidence": 0
                }
            ]
        },
        {
            "source_name": "IEA Net Zero Pathway Analysis 2024",
            "source_type": EvidenceSourceType.MANUAL,
            "source_content": """The IEA's updated net zero pathway shows that achieving 1.5C requires
tripling renewable capacity by 2030 and a 6x increase in clean energy investment. Carbon capture
deployment must increase 100x from current levels. The analysis identifies four critical technology
gaps: long-duration storage, sustainable aviation fuel, green steel, and direct air capture.
Policy acceleration scenarios show that coordinated government action could accelerate technology
deployment by 5-10 years. The pathway emphasizes that first-mover countries in clean energy
manufacturing will capture persistent economic advantages.""",
            "fragments": [
                {
                    "content": "Carbon capture deployment must increase 100x from current levels to achieve net zero, from current 40 Mt/yr to 4,000+ Mt/yr by 2050.",
                    "source_location": "Chapter 2, Technology Pathways",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Climate Impact Potential",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 94
                },
                {
                    "content": "Policy acceleration scenarios show coordinated government action could accelerate technology deployment by 5-10 years compared to current trajectory.",
                    "source_location": "Chapter 4, Policy Scenarios",
                    "status": AnalysisStatus.NEEDS_DECISION,
                    "confidence": 72,
                    "why_needs_decision": "Could be used to support 'Policy Tailwinds' concept or to complicate 'Market Timing Risk' by suggesting policy can shift timing windows",
                    "interpretations": [
                        {
                            "key": "a",
                            "title": "Strengthens policy tailwinds",
                            "target_unit_name": "Policy Tailwinds",
                            "target_grid_slot": "LOGICAL.evidence",
                            "relationship_type": EvidenceRelationship.EXTENDS,
                            "is_recommended": True,
                            "strategy": "Use to quantify the magnitude of policy impact on technology deployment timelines",
                            "rationale": "The 5-10 year acceleration potential directly demonstrates policy leverage on climate tech deployment",
                            "commitment_statement": "Commits you to viewing policy as a primary accelerant that investors should track and factor into timing decisions",
                            "foreclosure_statements": ["Purely technology-focused investment approach", "Policy-agnostic investment thesis"]
                        },
                        {
                            "key": "b",
                            "title": "Adds nuance to timing risk",
                            "target_unit_name": "Market Timing Risk",
                            "target_grid_slot": "TEMPORAL.inflection_points",
                            "relationship_type": EvidenceRelationship.EXTENDS,
                            "is_recommended": False,
                            "strategy": "Use to identify policy changes as key timing inflection points",
                            "rationale": "Policy-driven timeline shifts are unpredictable but material, adding complexity to timing analysis",
                            "commitment_statement": "Commits you to incorporating policy scenarios into timing risk assessment",
                            "foreclosure_statements": ["Treating policy as stable background condition", "Purely technology-focused timing analysis"]
                        }
                    ]
                },
                {
                    "content": "First-mover countries in clean energy manufacturing will capture persistent economic advantages, with an estimated 10-year lead translating to 30% market share advantage.",
                    "source_location": "Chapter 5, Industrial Strategy",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "First Mover vs Fast Follower",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 78
                },
                {
                    "content": "Achieving net zero requires clean energy investment to increase from $1.8T currently to $4.5T annually by 2030, with the largest gaps in grid infrastructure and industrial decarbonization.",
                    "source_location": "Chapter 1, Investment Needs",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Utilities",
                    "target_grid_slot": "TEMPORAL.trajectory",
                    "confidence": 91
                },
                {
                    "content": "Four critical technology gaps remain for net zero: long-duration storage (100+ hours), sustainable aviation fuel at scale, near-zero emissions steel, and direct air capture below $100/ton.",
                    "source_location": "Chapter 3, Technology Gaps",
                    "status": AnalysisStatus.ANALYZED,
                    "relationship_type": EvidenceRelationship.EXTENDS,
                    "target_unit_name": "Path to Scale Economics",
                    "target_grid_slot": "TEMPORAL.current_state",
                    "confidence": 86
                },
                {
                    "content": "The learning curve for green hydrogen shows potential to reach $2/kg by 2030 in optimal locations, but requires 10x scale-up of electrolyzer manufacturing capacity.",
                    "source_location": "Chapter 2, Hydrogen Analysis",
                    "status": AnalysisStatus.PENDING,
                    "confidence": 0
                }
            ]
        },
        {
            "source_name": "Breakthrough Energy Ventures Portfolio Analysis",
            "source_type": EvidenceSourceType.MANUAL,
            "source_content": """Analysis of BEV's portfolio reveals key success patterns in climate tech
investing. Companies with founder-market fit (prior industry experience) show 2.5x higher success
rates. IP-protected business models correlate with higher valuations at exit. The analysis shows
that partnership with incumbents accelerates scale but requires careful governance. Portfolio
companies that accessed DOE funding showed faster technology development. The fund's 20-year
structure allows patience for deep tech timelines.""",
            "fragments": [
                {
                    "content": "BEV portfolio companies with founder-market fit (prior industry experience) show 2.5x higher success rates than first-time founders in the sector.",
                    "source_location": "Section 2, Founder Analysis",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Incumbent Disruption Potential",
                    "target_grid_slot": "ACTOR.proponents",
                    "confidence": 82
                },
                {
                    "content": "Portfolio companies that accessed DOE funding (ARPA-E, LPO, or lab partnerships) showed 40% faster technology development compared to purely privately-funded peers.",
                    "source_location": "Section 4, Public-Private Synergy",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "DOE & National Labs",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 88
                },
                {
                    "content": "BEV's 20-year fund structure has allowed patience for deep tech timelines, with no pressure for premature exits. Average holding period is projected at 12-15 years.",
                    "source_location": "Section 1, Fund Structure",
                    "status": AnalysisStatus.NEEDS_DECISION,
                    "confidence": 75,
                    "why_needs_decision": "Could support the dialectic on timeline misalignment (as evidence of solution) or could support DOE & National Labs (as evidence of patient capital models)",
                    "interpretations": [
                        {
                            "key": "a",
                            "title": "Solution to timeline dialectic",
                            "target_unit_name": "Deep Tech Timeline vs VC Fund Lifecycle",
                            "target_grid_slot": "TEMPORAL.current_state",
                            "relationship_type": EvidenceRelationship.EXTENDS,
                            "is_recommended": True,
                            "strategy": "Use as evidence that fund structure innovation can resolve the fundamental tension",
                            "rationale": "BEV's 20-year structure directly addresses the 10-15 year deep tech development timeline",
                            "commitment_statement": "Commits you to advocating for longer fund structures as a key enabler of climate deep tech investment",
                            "foreclosure_statements": ["Accepting short-term VC as only viable model", "Focus on project finance rather than venture innovation"]
                        },
                        {
                            "key": "b",
                            "title": "Complements public funding",
                            "target_unit_name": "DOE & National Labs",
                            "target_grid_slot": "LOGICAL.warrant",
                            "relationship_type": EvidenceRelationship.EXTENDS,
                            "is_recommended": False,
                            "strategy": "Use to show that patient private capital complements public R&D support",
                            "rationale": "Long-term VC and public funding together create a complete capital stack for deep tech",
                            "commitment_statement": "Commits you to viewing private and public patient capital as complementary rather than substitutes",
                            "foreclosure_statements": ["Emphasis on purely private capital solutions", "Skepticism of government role in innovation"]
                        },
                        {
                            "key": "c",
                            "title": "Unique philanthropic structure",
                            "target_unit_name": "Climate Impact vs Financial Returns",
                            "target_grid_slot": "LOGICAL.evidence",
                            "relationship_type": EvidenceRelationship.QUALIFIES,
                            "is_recommended": False,
                            "strategy": "Note that BEV's structure is enabled by philanthropic LP base, not replicable by traditional funds",
                            "rationale": "The 20-year structure works because BEV's LPs accept patient, concessionary returns",
                            "commitment_statement": "Commits you to acknowledging limits of commercial capital for longest-timeline investments",
                            "foreclosure_statements": ["Expectation that all climate funds can adopt long structures", "Pure market-based framing of climate investing"]
                        }
                    ]
                },
                {
                    "content": "Partnership with incumbents accelerated scale for 70% of portfolio companies, but required board governance provisions to prevent strategic capture.",
                    "source_location": "Section 3, Strategic Partnerships",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Oil & Gas Majors",
                    "target_grid_slot": "LOGICAL.rebuttal",
                    "confidence": 80
                },
                {
                    "content": "IP-protected business models in the BEV portfolio showed 45% higher valuations at follow-on rounds compared to similar companies without patent protection.",
                    "source_location": "Section 2, Valuation Analysis",
                    "status": AnalysisStatus.ANALYZED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Technical Defensibility",
                    "target_grid_slot": "LOGICAL.evidence",
                    "confidence": 84
                }
            ]
        }
    ]
}
