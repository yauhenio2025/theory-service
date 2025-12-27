"""
Sample Data: Geopolitics of AI Essay Project

A concrete essay project demonstrating how someone would use Strategizer
to develop an argument about the geopolitical implications of artificial
intelligence - with real concepts, actors, tensions, and evidence.

This represents actual essay work, not an abstract framework.
"""

from api.strategizer.models import (
    UnitType, UnitTier, AnalysisStatus, EvidenceSourceType, EvidenceRelationship
)


ESSAY_THEORY_PROJECT = {
    "name": "The Geopolitics of AI: Power, Sovereignty, and the New World Order",
    "brief": """An essay examining how artificial intelligence is reshaping global power
dynamics, national sovereignty, and international relations. The central argument explores
whether AI development is creating a new form of technological bipolarity between the US
and China, and what this means for middle powers, democratic governance, and the future
of international cooperation.""",

    "domain": {
        "name": "AI Geopolitics Analysis",
        "core_question": "How is AI reshaping the global balance of power, and what strategic choices should democratic nations make in response?",
        "success_looks_like": "A compelling essay that moves beyond simplistic 'AI race' narratives to reveal the complex interdependencies, strategic dilemmas, and normative choices facing nations in the AI era.",
        "vocabulary": {
            "compute sovereignty": "A nation's capacity to develop and deploy AI independent of foreign infrastructure",
            "techno-nationalism": "The fusion of technological development with nationalist political projects",
            "algorithmic colonialism": "The extension of power through AI systems that encode particular values and dependencies",
            "AI stack": "The full supply chain from chips to models to applications",
            "dual-use": "Technologies with both civilian and military applications",
            "decoupling": "The strategic separation of technology supply chains between rival powers",
            "middle power": "Nations that lack superpower status but have significant regional influence",
            "technological leapfrogging": "Bypassing intermediate stages of development through new technology adoption",
        },
        "template_base": "GEOPOLITICS_ESSAY",
    },

    "units": [
        # =====================================================================
        # CONCEPTS (5)
        # =====================================================================
        {
            "unit_type": UnitType.CONCEPT,
            "display_type": "Core Concept",
            "tier": UnitTier.DOMAIN,
            "name": "Compute Sovereignty",
            "definition": "The capacity of a nation to develop, train, and deploy AI systems using domestically controlled computational infrastructure, free from foreign dependencies or potential denial.",
            "content": {
                "key_insight": "Control over compute is becoming as strategically important as control over oil was in the 20th century",
                "indicators": ["Domestic chip fabrication", "Cloud infrastructure ownership", "Energy for data centers", "Talent retention"],
            },
            "grids": {
                "LOGICAL": {
                    "claim": "Compute sovereignty has become a core strategic imperative because AI capability depends on access to computational resources that can be denied through export controls, sanctions, or supply chain disruption.",
                    "grounds": "The US CHIPS Act, EU Chips Act, and China's semiconductor investments represent over $200B in state intervention. The October 2022 US export controls on advanced chips to China demonstrate compute denial as a strategic weapon.",
                    "warrant": "Nations that cannot guarantee access to advanced compute cannot guarantee AI capability, making them strategically dependent on those who can.",
                    "backing": "Historical precedent: energy dependence shaped 20th-century geopolitics. Compute is the new critical resource for 21st-century power.",
                    "qualifier": "Cloud computing and distributed training may partially mitigate the need for domestic fabrication, though this introduces different dependencies.",
                    "rebuttal": "Some argue that compute is a commodity that will eventually be available from multiple sources, but current chokepoints (ASML, TSMC) suggest otherwise.",
                },
                "ACTOR": {
                    "protagonist": "Nations seeking strategic autonomy in AI",
                    "allies": "Domestic chip makers, cloud providers, energy companies",
                    "antagonists": "Existing compute hegemons who benefit from dependency; market forces favoring concentration",
                    "affected_parties": "AI researchers dependent on foreign cloud; smaller nations priced out of compute race",
                    "gatekeepers": "ASML (lithography), TSMC (fabrication), Nvidia (GPUs), hyperscalers (cloud)",
                },
                "TEMPORAL": {
                    "origin": "2010s: Rising awareness of strategic tech dependencies",
                    "evolution": "2020-2022: COVID supply chain shocks; US-China tech decoupling",
                    "current_state": "2023-2024: Massive state investments in domestic capacity; export control regime tightening",
                    "trajectory": "2025-2030: Potential bifurcation into US-aligned and China-aligned compute ecosystems",
                    "key_transitions": "October 2022 US export controls marked the decisive shift from market-led to state-led compute allocation",
                },
            },
        },
        {
            "unit_type": UnitType.CONCEPT,
            "display_type": "Core Concept",
            "tier": UnitTier.DOMAIN,
            "name": "The AI Arms Race Narrative",
            "definition": "The framing of AI development as a zero-sum competition between nations where falling behind poses existential risks, justifying accelerated development and reduced safety constraints.",
            "content": {
                "key_insight": "The 'race' framing may be self-fulfilling, creating the very dynamics it claims to describe",
                "dangers": ["Reduced safety investment", "Undermined cooperation", "Militarization pressure", "Democratic oversight erosion"],
            },
            "grids": {
                "LOGICAL": {
                    "claim": "The 'AI arms race' narrative is partially manufactured by actors who benefit from it, but has become real through its effects on policy and investment decisions.",
                    "grounds": "Defense contractors, nationalist politicians, and some AI companies have incentives to promote race framing. But state investments now reflect race assumptions regardless of their origin.",
                    "warrant": "Social constructs become real through their consequences; the race narrative now shapes real resource allocation and strategic planning.",
                    "backing": "Similar dynamics occurred with the Cold War arms race, where threat inflation created real military buildups that validated the original threat assessments.",
                    "qualifier": "This doesn't mean there's no genuine competition—but the nature of that competition is shaped by how it's framed.",
                    "rebuttal": "Some argue the race is simply objective reality given China's stated AI ambitions, but this ignores how framing choices shape what counts as 'winning' or 'losing'.",
                },
                "ACTOR": {
                    "protagonist": "The narrative itself as a social force shaping behavior",
                    "allies": "Defense establishments, nationalist politicians, AI companies seeking military contracts",
                    "antagonists": "Arms control advocates, AI safety researchers, international cooperation proponents",
                    "affected_parties": "Publics who must live with the consequences; researchers pressured to compromise on safety",
                    "gatekeepers": "Media that amplifies or challenges the narrative; think tanks that provide legitimacy",
                },
                "TEMPORAL": {
                    "origin": "2017: China's 'New Generation AI Development Plan' triggers Western alarm",
                    "evolution": "2018-2021: Increasing framing of AI as national security issue",
                    "current_state": "2023-2024: Race narrative dominant in policy discourse, but counter-narratives emerging",
                    "trajectory": "Uncertain: Could intensify toward new Cold War or could shift toward managed competition",
                },
            },
        },
        {
            "unit_type": UnitType.CONCEPT,
            "display_type": "Core Concept",
            "tier": UnitTier.DOMAIN,
            "name": "Talent as Strategic Resource",
            "definition": "The recognition that AI capability depends critically on scarce human expertise, making talent acquisition and retention a core element of national AI strategy.",
            "content": {
                "key_insight": "Unlike compute, talent cannot be stockpiled—it must be continuously attracted, developed, and retained",
                "dynamics": ["Global competition for PhDs", "Brain drain patterns", "Diaspora networks", "Education pipeline"],
            },
            "grids": {
                "LOGICAL": {
                    "claim": "Talent concentration in a few locations (primarily US) creates both an advantage for those locations and a vulnerability for nations experiencing brain drain.",
                    "grounds": "Over 60% of top AI researchers work in the US, many foreign-born. China has invested heavily in talent return programs. Europe struggles with brain drain to US.",
                    "warrant": "AI breakthroughs require rare combinations of skills; talent cannot be quickly produced through investment alone.",
                    "backing": "The transformer architecture, diffusion models, and RLHF all emerged from small teams—talent density matters more than talent volume.",
                    "qualifier": "Remote work and distributed collaboration may partially change these dynamics.",
                    "rebuttal": "Some argue talent is fungible and will eventually be abundant, but frontier AI research remains extremely concentrated.",
                },
                "ACTOR": {
                    "protagonist": "Elite AI researchers and engineers as scarce strategic resource",
                    "allies": "Universities, research labs, immigration-friendly policies",
                    "antagonists": "Visa restrictions, nationalism, compensation gaps",
                    "affected_parties": "Developing nations losing talent; researchers navigating political pressures",
                    "gatekeepers": "Top universities (Stanford, MIT, Tsinghua, Cambridge); leading labs (DeepMind, OpenAI, Anthropic)",
                },
                "TEMPORAL": {
                    "origin": "2012: Deep learning breakthrough triggers talent demand spike",
                    "evolution": "2015-2020: Salary explosion; corporate poaching from academia",
                    "current_state": "2023-2024: Geopoliticized talent flows; visa restrictions; return programs",
                    "trajectory": "Competition intensifying but patterns unclear as remote work and new hubs emerge",
                },
            },
        },
        {
            "unit_type": UnitType.CONCEPT,
            "display_type": "Core Concept",
            "tier": UnitTier.DOMAIN,
            "name": "Algorithmic Colonialism",
            "definition": "The extension of power through AI systems that encode particular cultural values, create economic dependencies, and extract data from populations without meaningful consent or benefit-sharing.",
            "content": {
                "key_insight": "AI systems trained on particular data and optimized for particular users may not serve all populations equally—and may actively disadvantage some",
                "mechanisms": ["Training data bias", "Optimization for wealthy markets", "Data extraction without compensation", "Platform dependency"],
            },
            "grids": {
                "LOGICAL": {
                    "claim": "AI systems developed in the Global North and deployed globally risk reproducing colonial patterns of extraction, dependency, and cultural imposition.",
                    "grounds": "LLMs trained primarily on English underperform on other languages. Facial recognition shows racial bias. Recommendation systems optimize for advertisers, not users.",
                    "warrant": "Technology is not neutral; it encodes the values and serves the interests of those who create it.",
                    "backing": "Historical parallel: 'modernization' and 'development' discourses that universalized Western norms while extracting resources.",
                    "qualifier": "The analogy to colonialism can be overstated—there are important differences. But the structural dynamics merit attention.",
                    "rebuttal": "Critics argue this framing ignores agency and benefits of technology adoption; but adoption under dependency conditions isn't truly free choice.",
                },
                "ACTOR": {
                    "protagonist": "Global South nations and populations experiencing AI systems designed elsewhere",
                    "allies": "Postcolonial scholars, AI ethics researchers, digital rights organizations",
                    "antagonists": "Tech companies externalizing costs; Northern governments protecting their industries",
                    "affected_parties": "Content moderators in Kenya; gig workers in India; populations subject to facial recognition",
                    "gatekeepers": "Platform companies; international development institutions; standards bodies",
                },
                "TEMPORAL": {
                    "origin": "2010s: Platform colonization of emerging markets (Facebook, Google)",
                    "evolution": "2018-2022: Growing awareness of AI bias; Global South critique emerges",
                    "current_state": "2023-2024: Some pushback (data localization laws) but limited alternatives",
                    "trajectory": "Uncertain: Could see regional AI development or deepening dependency",
                },
            },
        },
        {
            "unit_type": UnitType.CONCEPT,
            "display_type": "Core Concept",
            "tier": UnitTier.DOMAIN,
            "name": "The Middle Power Dilemma",
            "definition": "The strategic challenge facing nations that cannot compete with US-China AI development but must navigate between the two powers while maintaining autonomy and democratic values.",
            "content": {
                "key_insight": "Middle powers face a three-way tension: strategic autonomy vs. economic integration vs. values alignment",
                "examples": ["EU", "UK", "Japan", "India", "Australia", "Canada", "South Korea"],
            },
            "grids": {
                "LOGICAL": {
                    "claim": "Middle powers cannot achieve full AI autonomy but can pursue 'strategic hedging'—diversifying dependencies and developing niche capabilities to maintain bargaining power.",
                    "grounds": "EU GDPR and AI Act represent regulatory power without frontier capability. Japan and Korea maintain specialized capabilities (robotics, semiconductors). India leverages talent and market size.",
                    "warrant": "In a bipolar tech world, middle powers that maintain options have more leverage than those locked into either bloc.",
                    "backing": "Cold War non-aligned movement showed middle powers can navigate between superpowers, though context differs.",
                    "qualifier": "The degree of hedging possible depends on specific circumstances—geography, existing dependencies, values commitments.",
                    "rebuttal": "Some argue middle powers must ultimately choose sides; but the tech ecosystem's interdependence creates space for hedging.",
                },
                "ACTOR": {
                    "protagonist": "Middle power governments navigating between blocs",
                    "allies": "Other middle powers (potential coalitions); domestic tech champions",
                    "antagonists": "Pressure from both superpowers to align; domestic actors with competing interests",
                    "affected_parties": "Citizens whose data governance depends on these choices; businesses affected by regulatory divergence",
                    "gatekeepers": "Trade negotiators; standards bodies; alliance structures",
                },
                "TEMPORAL": {
                    "origin": "2018-2020: Trade war makes non-alignment increasingly difficult",
                    "evolution": "2021-2023: Middle powers develop distinct strategies (EU regulation, Japanese specialization)",
                    "current_state": "2024: Strategies being tested as decoupling accelerates",
                    "trajectory": "Key question: Can middle powers maintain hedging as pressure to choose sides intensifies?",
                },
            },
        },

        # =====================================================================
        # DIALECTICS (3)
        # =====================================================================
        {
            "unit_type": UnitType.DIALECTIC,
            "display_type": "Tension",
            "tier": UnitTier.DOMAIN,
            "name": "Open Science vs. National Security",
            "definition": "The tension between the scientific norm of open publication and collaboration, and the national security imperative to control strategically significant AI capabilities.",
            "content": {
                "thesis": "Open science accelerates progress and prevents dangerous concentration of capability",
                "antithesis": "Some AI capabilities are too dangerous or strategically important to publish openly",
                "synthesis": "Structured access regimes that maintain research collaboration while preventing misuse",
            },
            "grids": {
                "LOGICAL": {
                    "claim": "The traditional scientific norm of openness is being challenged by AI's dual-use nature, creating a genuine dilemma without easy resolution.",
                    "grounds": "GPT-2 release debate (2019), AlphaFold open release vs. GPT-4 closed weights, growing classification of AI research.",
                    "warrant": "Both openness (preventing concentration, enabling safety research) and restriction (preventing misuse, maintaining advantage) serve legitimate values.",
                    "backing": "Nuclear physics precedent: Manhattan Project ended open nuclear research, with lasting consequences for the field and geopolitics.",
                    "qualifier": "The optimal regime likely varies by capability type—biosecurity risks differ from strategic risks.",
                    "rebuttal": "Open absolutists argue restriction doesn't work (knowledge spreads anyway); securitizers argue even temporary delay has value.",
                },
                "ACTOR": {
                    "protagonist": "The tension itself, forcing choices on all actors",
                    "allies": "Scientists valuing openness; security establishments valuing control",
                    "antagonists": "Those who deny the tension exists (on either side)",
                    "affected_parties": "Researchers whose careers depend on publication; publics affected by capability diffusion",
                },
                "TEMPORAL": {
                    "origin": "2018-2019: GPT-2 release debate surfaces the tension",
                    "evolution": "2020-2023: Gradual shift toward more closed development at frontier",
                    "current_state": "2024: Frontier labs largely closed; open-source community growing; regulation debated",
                    "trajectory": "Likely continued fragmentation: some research open, frontier increasingly restricted",
                },
            },
        },
        {
            "unit_type": UnitType.DIALECTIC,
            "display_type": "Tension",
            "tier": UnitTier.DOMAIN,
            "name": "Innovation Speed vs. Democratic Deliberation",
            "definition": "The tension between the rapid pace of AI development and the slow pace of democratic governance, raising questions about whether meaningful public input on transformative technology is possible.",
            "content": {
                "thesis": "Democratic legitimacy requires public deliberation on transformative technologies",
                "antithesis": "AI develops too fast for traditional democratic processes; delay means falling behind",
                "synthesis": "New governance mechanisms that enable meaningful input without stopping development",
            },
            "grids": {
                "LOGICAL": {
                    "claim": "Current AI development is proceeding faster than democratic institutions can deliberate, creating a legitimacy deficit even in democratic nations.",
                    "grounds": "ChatGPT went from launch to 100M users in 2 months. Major AI legislation (EU AI Act) takes years. Public understanding lags capability.",
                    "warrant": "Democratic governance requires informed consent; consent cannot be informed when technology changes faster than understanding.",
                    "backing": "Social media precedent: platforms transformed public discourse before societies understood the implications.",
                    "qualifier": "The 'innovation vs. deliberation' framing may itself be contestable—some innovations can wait.",
                    "rebuttal": "Techno-optimists argue markets aggregate preferences efficiently; but market choice ≠ democratic choice on collective impacts.",
                },
                "ACTOR": {
                    "protagonist": "Democratic publics whose future is being shaped",
                    "allies": "Deliberative democracy advocates; AI governance researchers; civil society",
                    "antagonists": "Move-fast ideology; lobbyists for minimal regulation; authoritarian competitors used to justify speed",
                    "affected_parties": "Everyone subject to AI systems they didn't choose",
                },
                "TEMPORAL": {
                    "origin": "2022-2023: ChatGPT makes AI governance urgency visible",
                    "evolution": "2023-2024: Rushed regulatory responses; executive orders; international summits",
                    "current_state": "Race between capability development and governance capacity-building",
                    "trajectory": "Critical juncture: Will governance catch up before transformative AI?",
                },
            },
        },
        {
            "unit_type": UnitType.DIALECTIC,
            "display_type": "Tension",
            "tier": UnitTier.DOMAIN,
            "name": "US-China Decoupling vs. Global Commons",
            "definition": "The tension between the logic of great power competition pushing toward technological separation, and the logic of global challenges requiring cooperation.",
            "content": {
                "thesis": "Strategic competition requires reducing dependencies on adversaries",
                "antithesis": "Global challenges (climate, pandemics, AI safety) require cooperation across blocs",
                "synthesis": "Managed competition with cooperation on existential risks—but is this stable?",
            },
            "grids": {
                "LOGICAL": {
                    "claim": "Complete US-China tech decoupling is economically costly and strategically dangerous, but managed interdependence is increasingly difficult to sustain.",
                    "grounds": "Semiconductor supply chains deeply intertwined. AI safety research benefits from global collaboration. But trust is low and declining.",
                    "warrant": "Neither full decoupling nor full integration is feasible; the question is where to draw lines.",
                    "backing": "Cold War precedent: even US-USSR maintained some cooperation (arms control, space). But current tech competition may be less amenable to compartmentalization.",
                    "qualifier": "Different domains may allow different degrees of cooperation—AI safety vs. AI military applications.",
                    "rebuttal": "Hawks argue any cooperation enables adversary capability; doves argue competition is manufactured. Both overstate their cases.",
                },
                "ACTOR": {
                    "protagonist": "The international system trying to manage great power competition",
                    "allies": "Multilateralists; AI safety community; business interests in continued trade",
                    "antagonists": "Security hawks on both sides; nationalists; those who profit from conflict",
                    "affected_parties": "Third countries forced to choose; global challenges that go unaddressed",
                },
                "TEMPORAL": {
                    "origin": "2018: Trade war begins tech decoupling",
                    "evolution": "2020-2022: COVID, chip controls accelerate separation",
                    "current_state": "2024: Selective decoupling in strategic tech; continued interdependence elsewhere",
                    "trajectory": "Key uncertainty: Will safety concerns create cooperation space, or will competition dynamics dominate?",
                },
            },
        },

        # =====================================================================
        # ACTORS (4)
        # =====================================================================
        {
            "unit_type": UnitType.ACTOR,
            "display_type": "Major Power",
            "tier": UnitTier.DOMAIN,
            "name": "United States",
            "definition": "The current AI hegemon, home to leading labs and talent, but facing challenges to its dominance and internal debates about AI governance.",
            "content": {
                "role": "Incumbent AI leader seeking to maintain advantage while managing risks",
                "key_tensions": ["Innovation vs. safety", "Openness vs. security", "Cooperation vs. competition"],
                "assets": ["Top labs (OpenAI, Anthropic, Google)", "Talent concentration", "Capital", "Chip design"],
            },
            "grids": {
                "LOGICAL": {
                    "claim": "US AI dominance is real but contingent—it depends on continued talent attraction, capital availability, and allied cooperation, all of which could erode.",
                    "grounds": "US leads on frontier models but faces TSMC dependency, talent visa restrictions, and allied frustration with ITAR controls.",
                    "warrant": "Hegemony requires not just current capability but the conditions for sustained advantage.",
                    "backing": "Historical hegemons (British Empire, Dutch Republic) lost position when conditions enabling dominance changed.",
                },
                "ACTOR": {
                    "protagonist": "US government and tech sector (partially aligned)",
                    "allies": "Five Eyes, NATO allies (conditionally), TSMC/Japan/Korea (for chips)",
                    "antagonists": "China (strategic competitor), domestic critics of tech power",
                    "affected_parties": "Global users of US AI systems; nations subject to US tech policy",
                },
                "TEMPORAL": {
                    "origin": "2012: Deep learning revolution begins in US labs",
                    "evolution": "2017-2022: US lead widens on foundation models",
                    "current_state": "2024: Clear lead but growing challenges and internal tensions",
                    "trajectory": "Attempting to lock in advantage through export controls and allied coordination",
                },
            },
        },
        {
            "unit_type": UnitType.ACTOR,
            "display_type": "Major Power",
            "tier": UnitTier.DOMAIN,
            "name": "China",
            "definition": "The primary challenger to US AI dominance, with massive state investment, large talent base, and distinct approach to AI governance prioritizing control and application.",
            "content": {
                "role": "Rising AI power seeking to overcome dependencies and develop alternative ecosystem",
                "key_tensions": ["Catching up vs. leapfrogging", "State control vs. innovation", "Self-reliance vs. integration"],
                "assets": ["State investment", "Large talent pool", "Data scale", "Manufacturing base"],
            },
            "grids": {
                "LOGICAL": {
                    "claim": "China has significant AI capabilities but faces structural disadvantages in frontier research that export controls are designed to exploit.",
                    "grounds": "Chinese labs trail on frontier LLMs; chip controls constrain compute access; talent ties to US are double-edged.",
                    "warrant": "Catching up is harder than leading because followers must overcome not just technical gaps but ecosystem advantages of leaders.",
                    "backing": "Soviet precedent: managed rough parity in some domains but never matched US innovation ecosystem.",
                    "qualifier": "China may leapfrog in specific applications (robotics, autonomous vehicles) even if trailing on frontier research.",
                },
                "ACTOR": {
                    "protagonist": "Chinese state and tech champions (Baidu, Alibaba, Tencent, ByteDance)",
                    "allies": "Belt and Road partners; nations seeking alternatives to US tech",
                    "antagonists": "US-led export control coalition; domestic constraints on private sector",
                    "affected_parties": "Chinese tech workers; nations in China's sphere of influence",
                },
                "TEMPORAL": {
                    "origin": "2017: 'New Generation AI Development Plan' signals strategic priority",
                    "evolution": "2018-2022: Rapid capability growth; then export control shock",
                    "current_state": "2024: Intense effort to develop domestic chip and model capability",
                    "trajectory": "Attempting to create self-sufficient AI ecosystem, with uncertain success",
                },
            },
        },
        {
            "unit_type": UnitType.ACTOR,
            "display_type": "Regulatory Power",
            "tier": UnitTier.DOMAIN,
            "name": "European Union",
            "definition": "A regulatory superpower without frontier AI capability, attempting to shape global AI development through standard-setting and values-based governance.",
            "content": {
                "role": "Normative power trying to influence AI development without leading it",
                "key_tensions": ["Regulation vs. innovation", "Autonomy vs. dependence", "Values vs. competitiveness"],
                "assets": ["Regulatory capacity", "Large market", "Democratic legitimacy", "Some specialized capabilities"],
            },
            "grids": {
                "LOGICAL": {
                    "claim": "The EU's regulatory approach represents a genuine third way between US market-led and China state-led models, but its effectiveness depends on market leverage it may be losing.",
                    "grounds": "AI Act is first comprehensive AI regulation. 'Brussels Effect' worked for GDPR. But EU has no frontier models and risks regulatory capture by US firms.",
                    "warrant": "Regulatory power depends on market access; if AI becomes critical infrastructure, nations may accept worse terms to get access.",
                    "backing": "GDPR shows EU can shape global standards, but tech companies have adapted to minimize impact.",
                },
                "ACTOR": {
                    "protagonist": "EU institutions and member states (imperfectly aligned)",
                    "allies": "Global South (on some issues); civil society; privacy advocates",
                    "antagonists": "Big Tech lobbying; US pressure; member states prioritizing competitiveness",
                    "affected_parties": "EU citizens; global users of AI systems shaped by EU regulation",
                },
                "TEMPORAL": {
                    "origin": "2018: GDPR establishes EU as digital regulation leader",
                    "evolution": "2019-2024: AI Act development",
                    "current_state": "2024: AI Act implemented; testing whether it helps or hinders EU AI development",
                    "trajectory": "Uncertain: Regulation may attract responsible AI, or may push AI development elsewhere",
                },
            },
        },
        {
            "unit_type": UnitType.ACTOR,
            "display_type": "Non-State Actor",
            "tier": UnitTier.DOMAIN,
            "name": "Frontier AI Labs",
            "definition": "The handful of organizations (OpenAI, Anthropic, Google DeepMind, Meta AI) actually building frontier AI systems, wielding enormous power with limited accountability.",
            "content": {
                "role": "De facto governors of AI development, making choices that affect everyone",
                "key_tensions": ["Commercial vs. safety", "Open vs. closed", "Speed vs. caution"],
                "assets": ["Technical capability", "Talent", "Capital", "Data", "Compute access"],
            },
            "grids": {
                "LOGICAL": {
                    "claim": "Frontier labs exercise quasi-governmental power over AI development with minimal democratic accountability, creating a legitimacy crisis as capabilities grow.",
                    "grounds": "A handful of labs decide what capabilities to develop, whether to release them, and what safety measures to implement. No democratic mandate for these choices.",
                    "warrant": "Power without accountability is illegitimate in democratic theory; frontier labs have power without accountability.",
                    "backing": "Historical parallel: private colonial companies (East India Company) exercised state-like power before being brought under government control.",
                    "qualifier": "Labs do face market and reputational constraints; the question is whether these are sufficient.",
                },
                "ACTOR": {
                    "protagonist": "Lab leadership making critical choices",
                    "allies": "Investors; AI researchers (partially); governments (conditionally)",
                    "antagonists": "AI safety critics; open source advocates; regulators; competitors",
                    "affected_parties": "Everyone affected by AI systems these labs create",
                },
                "TEMPORAL": {
                    "origin": "2015: OpenAI founded; DeepMind acquired",
                    "evolution": "2019-2023: Rapid capability gains; commercialization; scaling",
                    "current_state": "2024: Unprecedented power; growing scrutiny; some self-regulation",
                    "trajectory": "Key question: Will labs be brought under democratic governance, or will they remain quasi-autonomous?",
                },
            },
        },
    ],

    # =========================================================================
    # EVIDENCE SOURCES
    # =========================================================================
    "evidence_sources": [
        {
            "source_type": EvidenceSourceType.MANUAL,
            "source_name": "RAND Corporation: The Geopolitics of AI",
            "source_content": "A comprehensive analysis of how AI is reshaping international relations and great power competition.",
            "fragments": [
                {
                    "content": "Countries are increasingly viewing AI as a strategic technology akin to nuclear weapons in terms of its potential to shift the global balance of power.",
                    "source_location": "Executive Summary, p. 3",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "The AI Arms Race Narrative",
                    "target_grid_slot": "grounds",
                    "confidence": 0.92,
                },
                {
                    "content": "US export controls on advanced semiconductors to China represent the most significant technology denial policy since the Cold War COCOM regime.",
                    "source_location": "Chapter 3, p. 47",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Compute Sovereignty",
                    "target_grid_slot": "grounds",
                    "confidence": 0.95,
                },
                {
                    "content": "Middle powers face a trilemma: they cannot simultaneously maintain technological autonomy, deep economic integration with both superpowers, and strong values-based foreign policy.",
                    "source_location": "Chapter 5, p. 89",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "The Middle Power Dilemma",
                    "target_grid_slot": "claim",
                    "confidence": 0.88,
                },
                {
                    "content": "The concentration of AI talent in a few geographic clusters creates both opportunity and vulnerability—opportunity for those clusters, vulnerability for nations experiencing brain drain.",
                    "source_location": "Chapter 4, p. 72",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Talent as Strategic Resource",
                    "target_grid_slot": "claim",
                    "confidence": 0.90,
                },
            ],
        },
        {
            "source_type": EvidenceSourceType.MANUAL,
            "source_name": "Brookings: AI and Democratic Governance",
            "source_content": "Analysis of challenges AI poses for democratic institutions and potential responses.",
            "fragments": [
                {
                    "content": "The speed of AI development has outpaced the capacity of democratic institutions to deliberate, creating what we term a 'governance gap' that poses fundamental challenges to democratic legitimacy.",
                    "source_location": "Introduction, p. 8",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Innovation Speed vs. Democratic Deliberation",
                    "target_grid_slot": "claim",
                    "confidence": 0.93,
                },
                {
                    "content": "Frontier AI labs now make decisions affecting billions of people with less democratic oversight than the smallest municipal government.",
                    "source_location": "Chapter 2, p. 34",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Frontier AI Labs",
                    "target_grid_slot": "claim",
                    "confidence": 0.91,
                },
                {
                    "content": "The question is not whether AI development should be subject to democratic governance, but whether democratic governance can adapt quickly enough to be relevant.",
                    "source_location": "Chapter 4, p. 78",
                    "status": AnalysisStatus.NEEDS_DECISION,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Innovation Speed vs. Democratic Deliberation",
                    "why_needs_decision": "This frames democratic governance as needing to 'speed up' to match AI development. But should we instead ask whether AI development should 'slow down' to match democratic deliberation?",
                    "interpretations": [
                        {
                            "key": "speedup",
                            "title": "Democratic governance must speed up",
                            "strategy": "Focus on institutional reforms that enable faster deliberation",
                            "rationale": "AI development won't slow down, so governance must adapt",
                            "relationship_type": EvidenceRelationship.SUPPORTS,
                            "target_unit_name": "Innovation Speed vs. Democratic Deliberation",
                            "target_grid_slot": "claim",
                            "is_recommended": False,
                            "commitment_statement": "Democratic institutions must find ways to deliberate faster without sacrificing legitimacy",
                            "foreclosure_statements": ["Asking AI development to pause for governance"],
                        },
                        {
                            "key": "slowdown",
                            "title": "AI development should slow to match governance",
                            "strategy": "Advocate for development pauses or mandatory governance checkpoints",
                            "rationale": "Legitimacy matters more than speed; development without consent is illegitimate",
                            "relationship_type": EvidenceRelationship.CONTRADICTS,
                            "target_unit_name": "Innovation Speed vs. Democratic Deliberation",
                            "target_grid_slot": "rebuttal",
                            "is_recommended": True,
                            "commitment_statement": "AI development pace should be constrained by governance capacity, not the reverse",
                            "foreclosure_statements": ["Accepting that governance must simply adapt to whatever pace labs set"],
                        },
                    ],
                },
            ],
        },
        {
            "source_type": EvidenceSourceType.MANUAL,
            "source_name": "Foreign Affairs: The Coming AI Anarchy",
            "source_content": "Essay on how AI diffusion may destabilize the international order.",
            "fragments": [
                {
                    "content": "Unlike nuclear weapons, AI capabilities are dual-use by default and cannot be easily contained. Every commercial AI advance is potentially a military advance.",
                    "source_location": "Section: Why AI Is Different",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Open Science vs. National Security",
                    "target_grid_slot": "grounds",
                    "confidence": 0.87,
                },
                {
                    "content": "The US and China are pursuing incompatible visions of AI governance that cannot be reconciled through negotiation. Unlike arms control, there are no natural units to count or limits to verify.",
                    "source_location": "Section: The Cooperation Problem",
                    "status": AnalysisStatus.NEEDS_DECISION,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "US-China Decoupling vs. Global Commons",
                    "why_needs_decision": "The author is pessimistic about US-China AI cooperation. But is this pessimism warranted, or does it risk becoming self-fulfilling prophecy?",
                    "interpretations": [
                        {
                            "key": "pessimist",
                            "title": "Cooperation is genuinely impossible",
                            "strategy": "Accept bifurcation and focus on winning the competition",
                            "rationale": "Fundamental value differences preclude meaningful cooperation",
                            "relationship_type": EvidenceRelationship.SUPPORTS,
                            "target_unit_name": "US-China Decoupling vs. Global Commons",
                            "target_grid_slot": "claim",
                            "is_recommended": False,
                            "commitment_statement": "US-China AI cooperation is impossible given value divergence",
                            "foreclosure_statements": ["Pursuing cooperation on AI governance", "Treating China as potential partner on AI safety"],
                        },
                        {
                            "key": "optimist",
                            "title": "Limited cooperation remains possible and necessary",
                            "strategy": "Distinguish competition domains from cooperation domains",
                            "rationale": "Even Cold War rivals cooperated on existential risks; AI safety may enable similar cooperation",
                            "relationship_type": EvidenceRelationship.QUALIFIES,
                            "target_unit_name": "US-China Decoupling vs. Global Commons",
                            "target_grid_slot": "qualifier",
                            "is_recommended": True,
                            "commitment_statement": "Competition and cooperation can coexist in different domains",
                            "foreclosure_statements": ["Full decoupling as strategic necessity", "Treating all AI issues as zero-sum"],
                        },
                    ],
                },
                {
                    "content": "We are witnessing the emergence of 'techno-spheres of influence' where nations align themselves with either the US or Chinese technological ecosystem, with profound implications for data flows, standards, and values.",
                    "source_location": "Section: The New Iron Curtain",
                    "status": AnalysisStatus.ANALYZED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "The Middle Power Dilemma",
                    "target_grid_slot": "grounds",
                    "confidence": 0.85,
                },
            ],
        },
        {
            "source_type": EvidenceSourceType.MANUAL,
            "source_name": "Interview Notes: AI Policy Expert",
            "source_content": "Notes from interview with former NSC technology policy director.",
            "fragments": [
                {
                    "content": "The 'AI race' framing was consciously promoted by certain actors who benefited from it—defense contractors, nationalist politicians, and some AI companies seeking to justify reduced safety investment.",
                    "source_location": "Interview transcript, p. 12",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "The AI Arms Race Narrative",
                    "target_grid_slot": "grounds",
                    "confidence": 0.88,
                },
                {
                    "content": "The EU's AI Act may be remembered as either a historic achievement in technology governance or a cautionary tale of regulatory hubris. We won't know which for another decade.",
                    "source_location": "Interview transcript, p. 28",
                    "status": AnalysisStatus.PENDING,
                    "relationship_type": EvidenceRelationship.NEW_INSIGHT,
                    "confidence": 0.72,
                },
                {
                    "content": "The real story isn't US vs. China—it's that a handful of private labs, accountable to no one, are making decisions that will shape the 21st century. States are scrambling to catch up.",
                    "source_location": "Interview transcript, p. 45",
                    "status": AnalysisStatus.NEEDS_DECISION,
                    "relationship_type": EvidenceRelationship.EXTENDS,
                    "target_unit_name": "Frontier AI Labs",
                    "why_needs_decision": "This challenges the state-centric framing of AI geopolitics. Should the essay center state competition or lab power?",
                    "interpretations": [
                        {
                            "key": "states",
                            "title": "States remain the central actors",
                            "strategy": "Analyze lab power as delegated from states, ultimately subject to state control",
                            "rationale": "States can regulate labs; the question is whether they choose to",
                            "relationship_type": EvidenceRelationship.QUALIFIES,
                            "target_unit_name": "Frontier AI Labs",
                            "target_grid_slot": "qualifier",
                            "is_recommended": False,
                            "commitment_statement": "Lab power exists within state-structured systems and can be reclaimed",
                            "foreclosure_statements": ["Treating labs as autonomous from state power"],
                        },
                        {
                            "key": "labs",
                            "title": "Labs are the primary actors in AI geopolitics",
                            "strategy": "Reframe essay around lab power and state response",
                            "rationale": "Labs actually make the key decisions; states mostly react",
                            "relationship_type": EvidenceRelationship.EXTENDS,
                            "target_unit_name": "Frontier AI Labs",
                            "target_grid_slot": "claim",
                            "is_recommended": True,
                            "commitment_statement": "AI geopolitics is primarily about lab power, with states as context",
                            "foreclosure_statements": ["Traditional state-centric geopolitical framing"],
                        },
                    ],
                },
            ],
        },
    ],
}
