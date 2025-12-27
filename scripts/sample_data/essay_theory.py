"""
Sample Data: Academic Essay & Theory Building Strategy

A meta-project demonstrating how to use Strategizer to plan and develop
academic essays, theoretical arguments, and scholarly contributions.

This is particularly relevant as it mirrors the core use case of the
theory-service itself.
"""

from api.strategizer.models import (
    UnitType, UnitTier, AnalysisStatus, EvidenceSourceType, EvidenceRelationship
)


ESSAY_THEORY_PROJECT = {
    "name": "Academic Essay & Theory Building Strategy",
    "brief": """Developing a strategic framework for writing compelling academic essays
and building original theoretical contributions. This project explores how to craft
arguments that are both intellectually rigorous and persuasively effective, balancing
scholarly grounding with conceptual innovation.""",

    "domain": {
        "name": "Essay & Theory Development",
        "core_question": "How do we construct academic arguments that advance knowledge while remaining grounded in existing scholarship?",
        "success_looks_like": "Essays that make original contributions, engage productively with existing literature, anticipate objections, and move readers toward new understanding.",
        "vocabulary": {
            "thesis": "The central claim or argument that the essay defends",
            "warrant": "The logical connection between evidence and claim (Toulmin)",
            "dialectic": "The productive tension between opposing positions",
            "interlocutor": "The scholarly voices and positions being engaged",
            "contribution": "The novel insight or advancement the essay provides",
            "scaffolding": "The structural framework that guides reader comprehension",
            "move": "A rhetorical or argumentative step within the essay",
            "stakes": "Why the argument matters; what hinges on getting it right",
            "foreclosure": "Positions or interpretations that accepting a claim rules out",
            "grounding": "The evidential and theoretical foundation supporting claims",
        },
        "template_base": "ESSAY_THEORY",
    },

    "units": [
        # =====================================================================
        # CONCEPTS (5)
        # =====================================================================
        {
            "unit_type": UnitType.CONCEPT,
            "display_type": "Core Concept",
            "tier": UnitTier.DOMAIN,
            "name": "Thesis Architecture",
            "definition": "The structural design of a thesis statement that makes a specific, defensible, and significant claim while signaling the essay's contribution to ongoing scholarly conversation.",
            "content": {
                "key_insight": "A thesis is not just a claim but a position-taking within a field of existing positions",
                "components": ["Specificity", "Defensibility", "Significance", "Positionality"],
            },
            "grids": {
                "LOGICAL": {
                    "claim": "Effective thesis statements must simultaneously be specific enough to be falsifiable, broad enough to be significant, and positioned clearly against alternative views.",
                    "grounds": "Analysis of successful academic essays reveals that impactful theses explicitly locate themselves within existing debates rather than making claims in a vacuum.",
                    "warrant": "Scholarly contribution requires both novelty (saying something new) and relevance (engaging what has been said), which thesis architecture must encode.",
                    "backing": "Peer review consistently evaluates theses on originality, clarity of contribution, and awareness of the field.",
                    "qualifier": "The balance between specificity and significance varies by discipline and genre.",
                    "rebuttal": "Some argue that overly positioned theses become defensive rather than exploratory; however, even exploratory essays benefit from clear initial claims that can be revised.",
                },
                "ACTOR": {
                    "protagonist": "The scholar developing the thesis, seeking to make an original contribution",
                    "allies": "Mentors, peer reviewers, and scholarly communities that validate and refine claims",
                    "antagonists": "Competing interpretations, methodological skeptics, and the weight of existing literature",
                    "affected_parties": "Future scholars who will build on or respond to the thesis",
                    "gatekeepers": "Journal editors, dissertation committees, and disciplinary norms",
                },
                "TEMPORAL": {
                    "origin": "Initial intuition or puzzle that motivates inquiry",
                    "evolution": "Thesis refinement through research, writing, and feedback loops",
                    "current_state": "Working thesis that guides the draft",
                    "trajectory": "Final thesis that emerges through revision and sharpening",
                    "key_transitions": "Moving from descriptive to argumentative; from broad to precise; from defensive to generative",
                },
            },
        },
        {
            "unit_type": UnitType.CONCEPT,
            "display_type": "Core Concept",
            "tier": UnitTier.DOMAIN,
            "name": "Evidence Integration",
            "definition": "The strategic deployment of textual evidence, data, examples, and citations to support claims while maintaining argumentative momentum and authorial voice.",
            "content": {
                "key_insight": "Evidence doesn't speak for itself—it requires framing, analysis, and connection to the larger argument",
                "integration_moves": ["Introduce", "Present", "Analyze", "Connect"],
            },
            "grids": {
                "LOGICAL": {
                    "claim": "Evidence must be introduced, presented, analyzed, and explicitly connected to claims—the 'quote and move on' approach fails to demonstrate understanding or build argument.",
                    "grounds": "Readers cannot infer the relevance of evidence; they need the writer to articulate why this evidence matters for this claim.",
                    "warrant": "Argumentation requires explicit reasoning chains; evidence provides premises but warrants and conclusions must be supplied by the writer.",
                    "backing": "Writing pedagogy consistently emphasizes the ICE method (Introduce, Cite, Explain) or similar frameworks.",
                    "qualifier": "The depth of analysis varies by genre—a literature review may present more evidence with less analysis than a theoretical essay.",
                    "rebuttal": "Some claim extensive analysis makes essays verbose; however, concise analysis is still analysis.",
                },
                "ACTOR": {
                    "protagonist": "The writer deploying evidence strategically",
                    "allies": "Source authors whose work supports the argument",
                    "antagonists": "Counter-evidence, alternative interpretations of the same evidence",
                    "affected_parties": "Readers who need clear reasoning to follow the argument",
                    "gatekeepers": "Citation norms, disciplinary expectations about evidence types",
                },
                "TEMPORAL": {
                    "origin": "Research phase where evidence is gathered",
                    "evolution": "Drafting where evidence is placed and analyzed",
                    "current_state": "Revision where evidence-claim connections are tightened",
                    "trajectory": "Final version where every piece of evidence clearly advances the argument",
                },
            },
        },
        {
            "unit_type": UnitType.CONCEPT,
            "display_type": "Core Concept",
            "tier": UnitTier.DOMAIN,
            "name": "Scholarly Positioning",
            "definition": "The art of situating one's argument within existing scholarly conversations, identifying allies and interlocutors, and clarifying the nature of one's contribution.",
            "content": {
                "key_insight": "Every essay enters a conversation already in progress; positioning determines how that entry is received",
                "moves": ["Survey", "Align", "Differentiate", "Contribute"],
            },
            "grids": {
                "LOGICAL": {
                    "claim": "Scholarly contributions are evaluated not in isolation but relative to existing work; clear positioning is therefore essential for reception.",
                    "grounds": "Reviewers and readers assess novelty by comparing claims to the existing literature they know.",
                    "warrant": "Knowledge advances incrementally through dialogue; positioning shows awareness of and engagement with that dialogue.",
                    "backing": "The 'literature review' is a standard requirement precisely because positioning is expected.",
                    "qualifier": "Positioning can be implicit in short-form genres but must be explicit in longer scholarly work.",
                    "rebuttal": "Some argue that truly original work need not position itself; however, even paradigm-shifting work must explain what it's shifting from.",
                },
                "ACTOR": {
                    "protagonist": "The scholar seeking to join and advance a conversation",
                    "allies": "Prior scholars whose work provides foundation",
                    "antagonists": "Scholars whose views are being challenged or revised",
                    "affected_parties": "The scholarly community whose understanding may shift",
                    "gatekeepers": "Disciplinary canons and citation expectations",
                },
                "TEMPORAL": {
                    "origin": "Historical development of the conversation being entered",
                    "evolution": "How the writer's understanding of the field developed",
                    "current_state": "The present state of the debate",
                    "trajectory": "Where the writer's contribution aims to take the conversation",
                },
            },
        },
        {
            "unit_type": UnitType.CONCEPT,
            "display_type": "Core Concept",
            "tier": UnitTier.DOMAIN,
            "name": "Argumentative Momentum",
            "definition": "The forward movement of an essay that carries readers through the argument, building understanding and conviction progressively.",
            "content": {
                "key_insight": "Essays should feel like they're going somewhere, not just presenting information",
                "elements": ["Stakes", "Progression", "Transitions", "Payoff"],
            },
            "grids": {
                "LOGICAL": {
                    "claim": "Effective essays create a sense of intellectual journey where each section builds on the previous and prepares for the next.",
                    "grounds": "Reader engagement depends on understanding why each part matters and where the argument is heading.",
                    "warrant": "Humans process narratives better than lists; argumentative momentum creates a narrative arc for ideas.",
                    "backing": "Rhetorical theory from Aristotle onward emphasizes arrangement (taxis) as crucial to persuasion.",
                    "qualifier": "Different genres allow different pacing—a philosophical essay may move more slowly than a policy brief.",
                    "rebuttal": "Some modular or exploratory essays resist linear momentum; however, even these benefit from clear section purposes.",
                },
                "ACTOR": {
                    "protagonist": "The writer guiding readers through the argument",
                    "allies": "Clear transitions, signposting, and structural cues",
                    "antagonists": "Reader fatigue, confusion, and skepticism",
                    "affected_parties": "Readers whose understanding develops through the essay",
                },
                "TEMPORAL": {
                    "origin": "Opening hook that establishes stakes",
                    "evolution": "Body sections that build the case progressively",
                    "current_state": "Transitions that mark progress and preview what's next",
                    "trajectory": "Conclusion that delivers the promised payoff",
                },
            },
        },
        {
            "unit_type": UnitType.CONCEPT,
            "display_type": "Core Concept",
            "tier": UnitTier.DOMAIN,
            "name": "Counter-Argument Engagement",
            "definition": "The strategic anticipation and response to objections, alternative views, and potential misreadings that strengthens rather than weakens the main argument.",
            "content": {
                "key_insight": "Addressing objections shows intellectual honesty and actually strengthens the argument by demonstrating awareness of its limits",
                "strategies": ["Anticipate", "Acknowledge", "Respond", "Integrate"],
            },
            "grids": {
                "LOGICAL": {
                    "claim": "Engaging counter-arguments demonstrates intellectual rigor and preemptively addresses reader skepticism, making the main argument more persuasive.",
                    "grounds": "Readers often think of objections as they read; addressing these shows the writer has thought more deeply.",
                    "warrant": "Dialectical reasoning—thesis, antithesis, synthesis—produces more robust conclusions than one-sided advocacy.",
                    "backing": "Peer review explicitly asks whether authors have considered alternative explanations and objections.",
                    "qualifier": "Not every possible objection needs addressing—only those likely to occur to the intended audience.",
                    "rebuttal": "Some argue that raising objections gives them undue prominence; however, unaddressed objections linger in readers' minds regardless.",
                },
                "ACTOR": {
                    "protagonist": "The writer anticipating and responding to criticism",
                    "allies": "The strongest versions of opposing arguments (steelmanning)",
                    "antagonists": "Weak or strawman versions that don't genuinely challenge",
                    "affected_parties": "Skeptical readers who need their concerns addressed",
                },
                "TEMPORAL": {
                    "origin": "Initial awareness of the controversy or debate",
                    "evolution": "Deepening engagement with opposing views through research",
                    "current_state": "Strategic placement of counter-arguments in the essay",
                    "trajectory": "Synthesis that incorporates valid objections into a stronger position",
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
            "name": "Originality vs. Scholarly Grounding",
            "definition": "The productive tension between making novel claims and remaining accountable to existing scholarship.",
            "content": {
                "thesis": "Original contribution is the goal of academic writing",
                "antithesis": "Claims must be grounded in and validated by existing literature",
                "synthesis": "True originality emerges from deep engagement with tradition, not departure from it",
            },
            "grids": {
                "LOGICAL": {
                    "claim": "The best academic work is simultaneously deeply grounded in existing scholarship AND genuinely original in its contribution.",
                    "grounds": "Work that ignores scholarship is dismissed as naive; work that only synthesizes is dismissed as derivative.",
                    "warrant": "Knowledge advances through both continuity (building on) and discontinuity (breaking from) existing understanding.",
                    "backing": "Canonical works in every field exhibit this balance—deeply learned yet genuinely innovative.",
                    "qualifier": "Different genres weight this differently—a review essay emphasizes grounding, a theoretical intervention emphasizes novelty.",
                    "rebuttal": "Some claim true originality requires ignoring tradition; however, even revolutionary work defines itself against what it rejects.",
                },
                "ACTOR": {
                    "protagonist": "The scholar navigating between innovation and tradition",
                    "allies": "Mentors who model this balance; editors who appreciate both",
                    "antagonists": "Reviewers who emphasize one at the expense of the other",
                    "affected_parties": "The field that benefits from balanced contributions",
                },
                "TEMPORAL": {
                    "origin": "Graduate training that emphasizes literature mastery",
                    "evolution": "Developing voice through imitation and differentiation",
                    "current_state": "Finding the sweet spot for a particular project",
                    "trajectory": "Mature scholarship that wears learning lightly while innovating boldly",
                },
            },
        },
        {
            "unit_type": UnitType.DIALECTIC,
            "display_type": "Tension",
            "tier": UnitTier.DOMAIN,
            "name": "Depth vs. Breadth",
            "definition": "The tension between exploring topics deeply and covering sufficient scope for the argument.",
            "content": {
                "thesis": "Deep analysis of fewer points creates more convincing arguments",
                "antithesis": "Broad coverage demonstrates comprehensive understanding",
                "synthesis": "Strategic depth on key points within a broader framework",
            },
            "grids": {
                "LOGICAL": {
                    "claim": "Effective essays achieve depth at crucial moments while maintaining enough breadth to contextualize the contribution.",
                    "grounds": "Readers need both: depth to be convinced on key claims, breadth to understand significance.",
                    "warrant": "Attention and space are limited; strategic allocation maximizes argumentative impact.",
                    "backing": "Word limits force choices; successful authors learn to make these choices strategically.",
                    "qualifier": "Genre affects the balance—dissertations allow more breadth, articles require more depth on fewer points.",
                    "rebuttal": "Some argue for consistent depth throughout; however, this often produces verbose, unfocused writing.",
                },
                "ACTOR": {
                    "protagonist": "The writer allocating limited space and attention",
                    "allies": "Clear sense of the core argument that guides allocation",
                    "antagonists": "The temptation to include everything learned in research",
                    "affected_parties": "Readers whose engagement depends on appropriate pacing",
                },
                "TEMPORAL": {
                    "origin": "Broad research phase that gathers more than can be used",
                    "evolution": "Drafting that reveals what's truly essential",
                    "current_state": "Revision that cuts and expands strategically",
                    "trajectory": "Final version where every element earns its place",
                },
            },
        },
        {
            "unit_type": UnitType.DIALECTIC,
            "display_type": "Tension",
            "tier": UnitTier.DOMAIN,
            "name": "Persuasion vs. Inquiry",
            "definition": "The tension between writing to convince readers of a predetermined position and writing to genuinely explore a question.",
            "content": {
                "thesis": "Essays should persuade readers of the writer's position",
                "antithesis": "Essays should be genuine inquiries open to unexpected conclusions",
                "synthesis": "Honest inquiry leads to the most persuasive writing because readers trust the process",
            },
            "grids": {
                "LOGICAL": {
                    "claim": "The most persuasive academic writing emerges from genuine inquiry rather than advocacy for predetermined conclusions.",
                    "grounds": "Readers sense when writers are genuinely thinking vs. merely defending; the former creates trust.",
                    "warrant": "Academic credibility depends on intellectual honesty; performative inquiry undermines this.",
                    "backing": "The most influential academic works often began as genuine puzzles, not positions to defend.",
                    "qualifier": "Some genres (policy briefs, legal arguments) require more explicit advocacy.",
                    "rebuttal": "Some argue all writing is advocacy; however, the mode of advocacy matters for credibility.",
                },
                "ACTOR": {
                    "protagonist": "The writer balancing conviction and openness",
                    "allies": "Research processes that challenge initial assumptions",
                    "antagonists": "Confirmation bias, deadline pressure, ego investment in positions",
                    "affected_parties": "Readers who benefit from honest scholarship",
                },
                "TEMPORAL": {
                    "origin": "Initial puzzle or question that motivates research",
                    "evolution": "Research that may confirm, complicate, or overturn initial hunches",
                    "current_state": "Writing that reflects the actual journey of thought",
                    "trajectory": "Conclusions that feel earned rather than imposed",
                },
            },
        },

        # =====================================================================
        # ACTORS (4)
        # =====================================================================
        {
            "unit_type": UnitType.ACTOR,
            "display_type": "Stakeholder",
            "tier": UnitTier.DOMAIN,
            "name": "The Writer-Scholar",
            "definition": "The person developing and articulating the argument, navigating between their understanding and their expression.",
            "content": {
                "role": "Primary agent of knowledge production and communication",
                "challenges": ["Imposter syndrome", "Perfectionism", "Finding voice"],
                "resources": ["Training", "Feedback", "Models to emulate"],
            },
            "grids": {
                "LOGICAL": {
                    "claim": "The writer-scholar's development is central to essay quality; technical skills matter less than cultivated judgment.",
                    "grounds": "Writing cannot be reduced to following rules; it requires situation-specific choices.",
                    "warrant": "Expertise develops through practice, feedback, and reflection—not just instruction.",
                    "backing": "Successful academics describe their development as gradual cultivation of sensibility.",
                },
                "ACTOR": {
                    "protagonist": "The developing scholar",
                    "allies": "Mentors, writing groups, supportive peers",
                    "antagonists": "Inner critic, comparison to established scholars",
                    "affected_parties": "Future students and readers who benefit from their development",
                },
                "TEMPORAL": {
                    "origin": "Early training and formative intellectual experiences",
                    "evolution": "Gradual development of voice, judgment, and expertise",
                    "current_state": "Present stage of development with current projects",
                    "trajectory": "Continued growth toward scholarly maturity",
                },
            },
        },
        {
            "unit_type": UnitType.ACTOR,
            "display_type": "Stakeholder",
            "tier": UnitTier.DOMAIN,
            "name": "The Ideal Reader",
            "definition": "The imagined audience whose needs, knowledge, and expectations guide writing decisions.",
            "content": {
                "role": "The construct that guides accessibility and pitch decisions",
                "characteristics": ["Informed but not expert", "Sympathetic but critical", "Busy but engaged"],
            },
            "grids": {
                "LOGICAL": {
                    "claim": "Having a clear ideal reader in mind improves writing by providing a consistent standard for decisions about explanation, evidence, and tone.",
                    "grounds": "Writers who imagine 'everyone' as audience often produce unfocused, inconsistently pitched work.",
                    "warrant": "Communication is always addressed; knowing the addressee shapes effective rhetoric.",
                    "backing": "Professional writers consistently describe imagining specific readers while writing.",
                },
                "ACTOR": {
                    "protagonist": "The imagined reader guiding writing choices",
                    "allies": "Real readers who approximate the ideal (writing group members, friendly reviewers)",
                    "antagonists": "The temptation to write for oneself or for no one in particular",
                    "affected_parties": "Actual readers who benefit when writing is appropriately pitched",
                },
                "TEMPORAL": {
                    "origin": "Initial conception of who the essay is for",
                    "evolution": "Refinement through feedback and revision",
                    "current_state": "Working sense of reader that guides current draft",
                    "trajectory": "Final version calibrated to actual venue and readership",
                },
            },
        },
        {
            "unit_type": UnitType.ACTOR,
            "display_type": "Stakeholder",
            "tier": UnitTier.DOMAIN,
            "name": "Scholarly Interlocutors",
            "definition": "The existing authors and positions that the essay engages, builds on, or argues against.",
            "content": {
                "role": "The scholarly conversation the essay joins",
                "types": ["Allies whose work provides foundation", "Opponents whose views are challenged", "Pioneers who framed the questions"],
            },
            "grids": {
                "LOGICAL": {
                    "claim": "Scholarly writing is fundamentally dialogic; it succeeds by clearly engaging specific interlocutors rather than speaking into a void.",
                    "grounds": "Knowledge advances through conversation; new contributions must connect to existing ones.",
                    "warrant": "Readers understand claims partly through their relation to familiar positions.",
                    "backing": "Citation practices across disciplines formalize this dialogic expectation.",
                },
                "ACTOR": {
                    "protagonist": "Key scholars whose work is engaged",
                    "allies": "Those whose frameworks are adopted or extended",
                    "antagonists": "Those whose views are challenged (respectfully)",
                    "affected_parties": "The scholarly community witnessing the dialogue",
                },
                "TEMPORAL": {
                    "origin": "Historical development of the relevant conversation",
                    "evolution": "How the debate has developed and shifted",
                    "current_state": "Present state of the scholarly discussion",
                    "trajectory": "Where the writer's contribution aims to take it",
                },
            },
        },
        {
            "unit_type": UnitType.ACTOR,
            "display_type": "Stakeholder",
            "tier": UnitTier.DOMAIN,
            "name": "Gatekeepers & Evaluators",
            "definition": "The editors, reviewers, committees, and institutions that judge and validate scholarly work.",
            "content": {
                "role": "Quality control and validation of scholarly contribution",
                "types": ["Journal editors", "Peer reviewers", "Dissertation committees", "Hiring committees"],
            },
            "grids": {
                "LOGICAL": {
                    "claim": "Understanding gatekeeper expectations is practical wisdom, not selling out; it enables effective communication with evaluators.",
                    "grounds": "Gatekeepers are typically experts whose standards reflect disciplinary values.",
                    "warrant": "Effective rhetoric requires audience awareness; evaluators are a key audience.",
                    "backing": "Successful scholars learn to write for reviewers while maintaining intellectual integrity.",
                },
                "ACTOR": {
                    "protagonist": "The evaluators whose approval is sought",
                    "allies": "Mentors who understand and can explain expectations",
                    "antagonists": "Opaque or arbitrary standards; capricious reviewers",
                    "affected_parties": "Scholars whose careers depend on evaluation outcomes",
                },
                "TEMPORAL": {
                    "origin": "Historical development of peer review and credentialing",
                    "evolution": "Shifting standards and expectations over time",
                    "current_state": "Present norms and their controversies",
                    "trajectory": "Evolving practices (open review, post-publication review, etc.)",
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
            "source_name": "Academic Writing Workshop Notes",
            "source_content": "Notes from faculty writing workshop on thesis development and argumentation.",
            "fragments": [
                {
                    "content": "The best thesis statements do three things: they make a specific claim, they signal the type of argument being made, and they position the writer within a scholarly conversation.",
                    "source_location": "Workshop Day 1, Thesis Development",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Thesis Architecture",
                    "target_grid_slot": "claim",
                    "confidence": 0.95,
                },
                {
                    "content": "Many graduate students struggle with the 'so what?' question. They can describe their research but not articulate why it matters. Stakes must be established early.",
                    "source_location": "Workshop Day 2, Stakes and Significance",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Argumentative Momentum",
                    "target_grid_slot": "grounds",
                    "confidence": 0.88,
                },
                {
                    "content": "Quote dropping is the most common evidence integration problem. Students include quotes without introducing, analyzing, or connecting them to the argument.",
                    "source_location": "Workshop Day 3, Evidence",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Evidence Integration",
                    "target_grid_slot": "claim",
                    "confidence": 0.92,
                },
                {
                    "content": "The literature review isn't just about showing you've read things. It's about constructing the conversation your work enters and positioning yourself within it.",
                    "source_location": "Workshop Day 4, Positioning",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Scholarly Positioning",
                    "target_grid_slot": "warrant",
                    "confidence": 0.90,
                },
                {
                    "content": "Addressing counter-arguments early on can feel like weakening your position, but it actually strengthens it by showing you've thought through objections.",
                    "source_location": "Workshop Day 5, Counter-Arguments",
                    "status": AnalysisStatus.NEEDS_DECISION,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Counter-Argument Engagement",
                    "why_needs_decision": "This suggests placing counter-arguments early, but conventional wisdom often places them after establishing the main argument. Where should they go?",
                    "interpretations": [
                        {
                            "key": "early",
                            "title": "Address objections early in the essay",
                            "strategy": "Place counter-argument engagement in the introduction or early body paragraphs",
                            "rationale": "Preempts reader skepticism and clears the ground for the main argument",
                            "relationship_type": EvidenceRelationship.SUPPORTS,
                            "target_unit_name": "Counter-Argument Engagement",
                            "target_grid_slot": "claim",
                            "is_recommended": True,
                            "commitment_statement": "Essays should address major objections before fully developing the main argument",
                            "foreclosure_statements": ["Saving all counter-arguments for late in the essay", "Assuming readers will suspend skepticism"],
                        },
                        {
                            "key": "late",
                            "title": "Address objections after establishing the main argument",
                            "strategy": "Place counter-argument engagement in later body paragraphs",
                            "rationale": "Allows the reader to first understand what's being defended before seeing challenges",
                            "relationship_type": EvidenceRelationship.QUALIFIES,
                            "target_unit_name": "Counter-Argument Engagement",
                            "target_grid_slot": "qualifier",
                            "is_recommended": False,
                            "commitment_statement": "Counter-arguments work best when readers already understand the main claim",
                            "foreclosure_statements": ["Addressing objections before the reader knows what's at stake"],
                        },
                    ],
                },
            ],
        },
        {
            "source_type": EvidenceSourceType.MANUAL,
            "source_name": "Peer Review Feedback Patterns",
            "source_content": "Aggregated analysis of common peer review feedback themes.",
            "fragments": [
                {
                    "content": "Reviewer feedback most commonly cites: unclear contribution (34%), insufficient engagement with literature (28%), weak evidence-claim connections (22%), and structural issues (16%).",
                    "source_location": "Feedback Analysis, p. 12",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Scholarly Positioning",
                    "target_grid_slot": "backing",
                    "confidence": 0.94,
                },
                {
                    "content": "Successful revisions typically involve sharpening the thesis (not broadening it), cutting tangential material (not adding more evidence), and making the argumentative structure more explicit.",
                    "source_location": "Revision Patterns, p. 45",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Depth vs. Breadth",
                    "target_grid_slot": "backing",
                    "confidence": 0.91,
                },
                {
                    "content": "Papers rejected for 'lack of contribution' often contain substantial research but fail to articulate what new understanding they provide beyond synthesizing existing work.",
                    "source_location": "Rejection Analysis, p. 23",
                    "status": AnalysisStatus.NEEDS_DECISION,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Originality vs. Scholarly Grounding",
                    "why_needs_decision": "This highlights the importance of articulating contribution, but doesn't clarify whether the issue is typically the actual contribution or just its articulation.",
                    "interpretations": [
                        {
                            "key": "articulate",
                            "title": "The problem is usually articulation, not substance",
                            "strategy": "Focus on explicitly stating the contribution, even if it seems obvious",
                            "rationale": "Many papers have genuine contributions that authors assume are self-evident but aren't",
                            "relationship_type": EvidenceRelationship.EXTENDS,
                            "target_unit_name": "Originality vs. Scholarly Grounding",
                            "target_grid_slot": "claim",
                            "is_recommended": True,
                            "commitment_statement": "Contribution must be explicitly articulated, not left implicit",
                            "foreclosure_statements": ["Assuming readers will infer the contribution"],
                        },
                        {
                            "key": "substance",
                            "title": "The problem is often genuinely insufficient contribution",
                            "strategy": "Before writing, ensure there's a real contribution worth articulating",
                            "rationale": "Some papers genuinely only synthesize without adding new understanding",
                            "relationship_type": EvidenceRelationship.QUALIFIES,
                            "target_unit_name": "Originality vs. Scholarly Grounding",
                            "target_grid_slot": "rebuttal",
                            "is_recommended": False,
                            "commitment_statement": "Better articulation can't save a paper without genuine contribution",
                            "foreclosure_statements": ["Assuming articulation is always the bottleneck"],
                        },
                    ],
                },
                {
                    "content": "Reviewers consistently praise papers that 'acknowledge limitations honestly' and criticize those that 'oversell findings.' Intellectual humility correlates with favorable reviews.",
                    "source_location": "Positive Feedback Themes, p. 34",
                    "status": AnalysisStatus.ANALYZED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Persuasion vs. Inquiry",
                    "target_grid_slot": "backing",
                    "confidence": 0.87,
                },
                {
                    "content": "The most common structural feedback is 'I couldn't follow the argument'—not that the argument was wrong, but that its structure was unclear.",
                    "source_location": "Structure Feedback, p. 56",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Argumentative Momentum",
                    "target_grid_slot": "backing",
                    "confidence": 0.93,
                },
            ],
        },
        {
            "source_type": EvidenceSourceType.MANUAL,
            "source_name": "Successful Dissertation Analysis",
            "source_content": "Study of award-winning dissertations across humanities and social sciences.",
            "fragments": [
                {
                    "content": "Award-winning dissertations typically spent 40% more time on literature engagement than average dissertations, but this engagement was more focused—fewer sources, deeper analysis.",
                    "source_location": "Chapter 3: Literature Engagement",
                    "status": AnalysisStatus.INTEGRATED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Depth vs. Breadth",
                    "target_grid_slot": "grounds",
                    "confidence": 0.89,
                },
                {
                    "content": "The opening chapters of successful dissertations typically articulated the 'puzzle' or 'problem' before the thesis, creating intellectual stakes before proposing a solution.",
                    "source_location": "Chapter 2: Opening Strategies",
                    "status": AnalysisStatus.ANALYZED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Argumentative Momentum",
                    "target_grid_slot": "claim",
                    "confidence": 0.86,
                },
                {
                    "content": "Successful authors described their writing process as genuinely exploratory—they didn't know their conclusion when they started. This was evident in the final text's authentic engagement with complexity.",
                    "source_location": "Chapter 5: Process Analysis",
                    "status": AnalysisStatus.NEEDS_DECISION,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Persuasion vs. Inquiry",
                    "why_needs_decision": "This suggests genuine inquiry leads to better writing, but many successful scholars describe knowing their argument before writing. Is exploratory writing essential or just one valid approach?",
                    "interpretations": [
                        {
                            "key": "essential",
                            "title": "Genuine inquiry is essential to the best academic writing",
                            "strategy": "Begin writing before conclusions are fixed; let the writing process shape the argument",
                            "rationale": "The process of writing-as-thinking produces authentically complex engagement",
                            "relationship_type": EvidenceRelationship.SUPPORTS,
                            "target_unit_name": "Persuasion vs. Inquiry",
                            "target_grid_slot": "claim",
                            "is_recommended": True,
                            "commitment_statement": "The best academic writing emerges from genuine inquiry, not just articulation of predetermined conclusions",
                            "foreclosure_statements": ["Fully planning arguments before writing", "Treating writing as mere transcription of thought"],
                        },
                        {
                            "key": "optional",
                            "title": "Exploratory writing is one valid approach among several",
                            "strategy": "Match process to project—some work benefits from exploration, other from clear planning",
                            "rationale": "Different scholars and projects may require different processes",
                            "relationship_type": EvidenceRelationship.QUALIFIES,
                            "target_unit_name": "Persuasion vs. Inquiry",
                            "target_grid_slot": "qualifier",
                            "is_recommended": False,
                            "commitment_statement": "There is no single best writing process; exploratory writing is one valid option",
                            "foreclosure_statements": ["Prescribing exploratory writing for all projects"],
                        },
                    ],
                },
                {
                    "content": "Voice development—the sense of a distinctive authorial presence—was identified as a key differentiator. This wasn't about personality but about consistent intellectual perspective.",
                    "source_location": "Chapter 6: Voice and Style",
                    "status": AnalysisStatus.PENDING,
                    "relationship_type": EvidenceRelationship.NEW_INSIGHT,
                    "confidence": 0.75,
                },
                {
                    "content": "Committee members reported valuing 'intellectual courage'—the willingness to make strong claims and engage seriously with the strongest objections.",
                    "source_location": "Chapter 7: Committee Perspectives",
                    "status": AnalysisStatus.ANALYZED,
                    "relationship_type": EvidenceRelationship.SUPPORTS,
                    "target_unit_name": "Counter-Argument Engagement",
                    "target_grid_slot": "backing",
                    "confidence": 0.88,
                },
            ],
        },
    ],
}
