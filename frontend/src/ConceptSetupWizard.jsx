import { useState, useEffect, useRef } from 'react'

/**
 * Enhanced Concept Setup Wizard - Staged Adaptive Questioning
 *
 * Uses Claude Opus 4.5 with extended thinking (32k budget) to:
 * 1. Stage 1: Genesis & Problem Space (predefined questions)
 * 2. Interim Analysis: Shows what we understand so far
 * 3. Stage 2: Differentiation (dynamically generated from Stage 1)
 * 4. Implications Preview: Shows what choices mean
 * 5. Stage 3: Grounding & Recognition
 * 6. Final Synthesis: Complete concept definition
 *
 * Features:
 * - Multiple choice with exclusivity groups
 * - Custom responses with categories (Alternative, Comment, Refinement)
 * - Mark as Dialectic for productive tensions
 * - Implications visualization
 */

const API_URL = import.meta.env.VITE_API_URL || 'https://theory-api.onrender.com'

// Enhanced wizard stages
const STAGES = {
  NOTES: 'notes',
  ANALYZING_NOTES: 'analyzing_notes',
  UNDERSTANDING_VALIDATION: 'understanding_validation',  // New: validate LLM's understanding
  DOCUMENT_UPLOAD: 'document_upload',  // Optional: upload supporting documents
  ANALYZING_DOCUMENT: 'analyzing_document',  // Analyzing uploaded document
  BLIND_SPOTS_CURATING: 'blind_spots_curating',  // Curator analyzing notes for blind spots
  BLIND_SPOTS_QUESTIONING: 'blind_spots_questioning',  // Dynamic questioning with sharpener
  STAGE1: 'stage1',
  ANALYZING_STAGE1: 'analyzing_stage1',
  INTERIM_ANALYSIS: 'interim_analysis',
  STAGE2: 'stage2',
  ANALYZING_STAGE2: 'analyzing_stage2',
  IMPLICATIONS_PREVIEW: 'implications_preview',
  STAGE3: 'stage3',
  GENEALOGY: 'genealogy',  // Intellectual genealogy: influences, ancestors, debates
  GENERATING_GENEALOGY: 'generating_genealogy',  // Generating genealogy hypotheses
  DEEP_COMMITMENTS: 'deep_commitments',  // Phase 1: Initial 9 philosophical dimensions questions
  ANALYZING_COMMITMENTS: 'analyzing_commitments',  // Generating Phase 1 questions
  GENERATING_PHASE2: 'generating_phase2',  // Generating Phase 2 follow-up questions
  DEEP_COMMITMENTS_PHASE2: 'deep_commitments_phase2',  // Phase 2: Targeted follow-ups
  GENERATING_PHASE3: 'generating_phase3',  // Generating Phase 3 synthesis questions
  DEEP_COMMITMENTS_PHASE3: 'deep_commitments_phase3',  // Phase 3: Final verification
  PROCESSING: 'processing',
  COMPLETE: 'complete'
}

// Stage navigation - defines the order and labels for breadcrumb navigation
// Only "checkpoint" stages are navigable (not analyzing/processing stages)
const STAGE_NAV = [
  { id: STAGES.NOTES, label: 'Start', shortLabel: '1', navigable: true },
  { id: STAGES.UNDERSTANDING_VALIDATION, label: 'Validate Understanding', shortLabel: '2', navigable: true },
  { id: STAGES.BLIND_SPOTS_QUESTIONING, label: 'Blind Spots', shortLabel: '3', navigable: true },
  { id: STAGES.DOCUMENT_UPLOAD, label: 'Documents', shortLabel: '4', navigable: true },
  { id: STAGES.INTERIM_ANALYSIS, label: 'Interim Review', shortLabel: '5', navigable: true },
  { id: STAGES.STAGE2, label: 'Differentiation', shortLabel: '6', navigable: true },
  { id: STAGES.IMPLICATIONS_PREVIEW, label: 'Implications', shortLabel: '7', navigable: true },
  { id: STAGES.STAGE3, label: 'Methodology', shortLabel: '8', navigable: true },
  { id: STAGES.GENEALOGY, label: 'Genealogy', shortLabel: '9', navigable: true },
  { id: STAGES.DEEP_COMMITMENTS, label: 'Philosophy P1', shortLabel: '10a', navigable: true },
  { id: STAGES.DEEP_COMMITMENTS_PHASE2, label: 'Philosophy P2', shortLabel: '10b', navigable: true },
  { id: STAGES.DEEP_COMMITMENTS_PHASE3, label: 'Philosophy P3', shortLabel: '10c', navigable: true },
  { id: STAGES.COMPLETE, label: 'Complete', shortLabel: '11', navigable: true }
]

// Map any stage to its nearest navigable checkpoint
const getNavCheckpoint = (stage) => {
  const checkpointMap = {
    [STAGES.NOTES]: STAGES.NOTES,
    [STAGES.ANALYZING_NOTES]: STAGES.NOTES,
    [STAGES.UNDERSTANDING_VALIDATION]: STAGES.UNDERSTANDING_VALIDATION,
    [STAGES.BLIND_SPOTS_CURATING]: STAGES.BLIND_SPOTS_QUESTIONING,
    [STAGES.BLIND_SPOTS_QUESTIONING]: STAGES.BLIND_SPOTS_QUESTIONING,
    [STAGES.DOCUMENT_UPLOAD]: STAGES.DOCUMENT_UPLOAD,
    [STAGES.ANALYZING_DOCUMENT]: STAGES.DOCUMENT_UPLOAD,
    [STAGES.STAGE1]: STAGES.DOCUMENT_UPLOAD,  // Stage 1 is now skipped, so map to doc upload
    [STAGES.ANALYZING_STAGE1]: STAGES.DOCUMENT_UPLOAD,
    [STAGES.INTERIM_ANALYSIS]: STAGES.INTERIM_ANALYSIS,
    [STAGES.STAGE2]: STAGES.STAGE2,
    [STAGES.ANALYZING_STAGE2]: STAGES.STAGE2,
    [STAGES.IMPLICATIONS_PREVIEW]: STAGES.IMPLICATIONS_PREVIEW,
    [STAGES.STAGE3]: STAGES.STAGE3,
    [STAGES.GENEALOGY]: STAGES.GENEALOGY,
    [STAGES.GENERATING_GENEALOGY]: STAGES.GENEALOGY,
    [STAGES.DEEP_COMMITMENTS]: STAGES.DEEP_COMMITMENTS,
    [STAGES.ANALYZING_COMMITMENTS]: STAGES.DEEP_COMMITMENTS,
    [STAGES.GENERATING_PHASE2]: STAGES.DEEP_COMMITMENTS_PHASE2,
    [STAGES.DEEP_COMMITMENTS_PHASE2]: STAGES.DEEP_COMMITMENTS_PHASE2,
    [STAGES.GENERATING_PHASE3]: STAGES.DEEP_COMMITMENTS_PHASE3,
    [STAGES.DEEP_COMMITMENTS_PHASE3]: STAGES.DEEP_COMMITMENTS_PHASE3,
    [STAGES.PROCESSING]: STAGES.DEEP_COMMITMENTS_PHASE3,
    [STAGES.COMPLETE]: STAGES.COMPLETE
  }
  return checkpointMap[stage] || stage
}

// Question types
const QUESTION_TYPES = {
  OPEN: 'open_ended',
  CHOICE: 'multiple_choice',
  MULTI: 'multi_select',
  SCALE: 'scale'
}

// Custom response categories (essay-flow pattern)
const CUSTOM_CATEGORIES = [
  { key: 'qualification', label: 'Qualification', description: 'Clarify or narrow the scope' },
  { key: 'addon', label: 'Add-on', description: 'Supplement the selected option' },
  { key: 'alternative', label: 'Alternative', description: 'Provide a different answer entirely' },
  { key: 'refinement', label: 'Refinement', description: 'Improve or refine an option' }
]

// 9 concept dimensions for impact topology
const CONCEPT_DIMENSIONS = [
  { id: 'genesis', label: 'Genesis', icon: '🌱' },
  { id: 'problem_space', label: 'Problem Space', icon: '🎯' },
  { id: 'definition', label: 'Definition', icon: '📖' },
  { id: 'differentiations', label: 'Differentiations', icon: '↔️' },
  { id: 'paradigmatic_cases', label: 'Cases', icon: '📋' },
  { id: 'recognition_markers', label: 'Recognition', icon: '👁️' },
  { id: 'core_claims', label: 'Claims', icon: '💡' },
  { id: 'falsification', label: 'Falsification', icon: '❌' },
  { id: 'dialectics', label: 'Dialectics', icon: '⚡' }
]

/**
 * Generate impact topology based on question and selected options
 * Maps how choices affect different concept dimensions
 */
function generateImpactTopology(question, selectedOptions, options) {
  if (!selectedOptions || selectedOptions.length === 0 || !question) return null

  // Get selected option objects
  const selectedOpts = options?.filter(o => selectedOptions.includes(o.value)) || []
  if (selectedOpts.length === 0) return null

  // Question-specific impact mappings
  const questionImpacts = {
    genesis_type: {
      theoretical_innovation: [
        { dimension: 'definition', effect: 'NEEDS', note: 'Strong theoretical grounding required' },
        { dimension: 'differentiations', effect: 'FOCUS', note: 'Must distinguish from existing frameworks' },
        { dimension: 'core_claims', effect: 'CENTER', note: 'Ontological claims become central' }
      ],
      empirical_discovery: [
        { dimension: 'paradigmatic_cases', effect: 'CENTER', note: 'Concrete examples become crucial' },
        { dimension: 'recognition_markers', effect: 'EXPAND', note: 'Need observable indicators' },
        { dimension: 'falsification', effect: 'EASIER', note: 'Empirical tests more direct' }
      ],
      synthetic_unification: [
        { dimension: 'differentiations', effect: 'COMPLEX', note: 'Must show what synthesis adds' },
        { dimension: 'problem_space', effect: 'BRIDGE', note: 'Gap between synthesized concepts' },
        { dimension: 'core_claims', effect: 'INTEGRATIVE', note: 'Claims span multiple domains' }
      ],
      paradigm_shift: [
        { dimension: 'definition', effect: 'RADICAL', note: 'Fundamentally new framing needed' },
        { dimension: 'genesis', effect: 'JUSTIFY', note: 'Must explain what it replaces' },
        { dimension: 'dialectics', effect: 'LIKELY', note: 'Old vs new paradigm tension' }
      ],
      normative_reframing: [
        { dimension: 'core_claims', effect: 'NORMATIVE', note: 'Evaluative criteria central' },
        { dimension: 'falsification', effect: 'VALUES', note: 'Tests involve value judgments' },
        { dimension: 'recognition_markers', effect: 'EVALUATIVE', note: 'Look for normative language' }
      ]
    },
    domain_scope: {
      domain_specific: [
        { dimension: 'paradigmatic_cases', effect: 'FOCUSED', note: 'Single domain examples' },
        { dimension: 'recognition_markers', effect: 'SPECIFIC', note: 'Domain-specific language' },
        { dimension: 'differentiations', effect: 'SHARPER', note: 'Clear boundaries within domain' }
      ],
      cross_domain: [
        { dimension: 'paradigmatic_cases', effect: 'DIVERSE', note: 'Need examples from each domain' },
        { dimension: 'definition', effect: 'ABSTRACT', note: 'Must work across contexts' },
        { dimension: 'falsification', effect: 'COMPLEX', note: 'Domain-specific tests needed' }
      ],
      meta_level: [
        { dimension: 'core_claims', effect: 'METHODOLOGICAL', note: 'Claims about how we think' },
        { dimension: 'recognition_markers', effect: 'REFLEXIVE', note: 'Look in analytical moves' },
        { dimension: 'paradigmatic_cases', effect: 'EXEMPLARY', note: 'Analytical examples needed' }
      ]
    }
  }

  // Get impacts for this question
  const questionId = question.id
  const impacts = []

  for (const opt of selectedOpts) {
    const optImpacts = questionImpacts[questionId]?.[opt.value]
    if (optImpacts) {
      impacts.push(...optImpacts)
    }
  }

  // If no specific impacts, generate generic ones based on option implications
  if (impacts.length === 0 && selectedOpts[0]?.implications) {
    impacts.push(
      { dimension: 'definition', effect: 'SHAPES', note: selectedOpts[0].implications },
      { dimension: 'differentiations', effect: 'AFFECTS', note: 'May change how we distinguish concept' }
    )
  }

  return impacts.length > 0 ? impacts : null
}

// =============================================================================
// TRANSFORMATION MODES (Sharpen/Generalize/Radicalize/Historicize/Deepen)
// =============================================================================
const TRANSFORM_MODES = [
  { id: 'sharpen', icon: '🎯', label: 'Sharpen', description: 'Make more specific and precise' },
  { id: 'generalize', icon: '🔭', label: 'Generalize', description: 'Make broader and more abstract' },
  { id: 'radicalize', icon: '🔥', label: 'Radicalize', description: 'Push to more provocative position' },
  { id: 'historicize', icon: '📜', label: 'Historicize', description: 'Ground in historical process' },
  { id: 'deepen', icon: '🔬', label: 'Deepen', description: 'Dig into underlying mechanisms' }
]

/**
 * RefineDropdown - Transformation mode selector (like essay-flow)
 */
function RefineDropdown({ card, cardType, onTransform, isTransforming }) {
  const [open, setOpen] = useState(false)
  const [selectedMode, setSelectedMode] = useState('sharpen')
  const [guidance, setGuidance] = useState('')

  const handleTransform = () => {
    onTransform(card.id, cardType, selectedMode, guidance)
    setOpen(false)
    setGuidance('')
  }

  return (
    <div className="refine-dropdown">
      <button
        className="refine-dropdown-trigger"
        onClick={() => setOpen(!open)}
        disabled={isTransforming}
      >
        {isTransforming ? 'Transforming...' : 'Refine ▾'}
      </button>
      {open && (
        <div className="refine-dropdown-content">
          <div className="refine-modes">
            {TRANSFORM_MODES.map(mode => (
              <span
                key={mode.id}
                className={`refine-option ${selectedMode === mode.id ? 'selected' : ''}`}
                onClick={() => setSelectedMode(mode.id)}
                title={mode.description}
              >
                {mode.icon} {mode.label}
              </span>
            ))}
          </div>
          <div className="refine-input-row">
            <input
              type="text"
              placeholder="Optional guidance..."
              value={guidance}
              onChange={(e) => setGuidance(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleTransform()}
            />
            <button onClick={handleTransform} className="refine-submit">
              →
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

/**
 * HypothesisCard - Card for displaying and interacting with hypothesis/genealogy/differentiation cards
 */
function HypothesisCard({ card, cardType, onApprove, onReject, onTransform, isTransforming }) {
  // Get display content based on card type
  const getContent = () => {
    switch (cardType) {
      case 'hypothesis':
        return card.content
      case 'genealogy':
        return `${card.thinker}: ${card.connection}`
      case 'differentiation':
        return `NOT ${card.contrasted_with}: ${card.difference}`
      default:
        return card.content
    }
  }

  const getTypeLabel = () => {
    switch (cardType) {
      case 'hypothesis':
        return card.type || 'thesis'
      case 'genealogy':
        return card.tradition || 'influence'
      case 'differentiation':
        return 'differentiation'
      default:
        return 'claim'
    }
  }

  const statusClass = card.status === 'approved' ? 'approved' : card.status === 'rejected' ? 'rejected' : ''

  return (
    <div className={`hypothesis-card ${statusClass}`}>
      <div className="card-header">
        <span className={`card-type ${card.type || ''}`}>{getTypeLabel()}</span>
      </div>

      <div className="card-content">
        {getContent()}
      </div>

      {card.rationale && (
        <div className="card-rationale">
          <strong>Why:</strong> {card.rationale}
        </div>
      )}

      {card.source_excerpts && card.source_excerpts.length > 0 && (
        <div className="card-excerpts">
          <strong>From your notes:</strong>
          {card.source_excerpts.slice(0, 2).map((excerpt, i) => (
            <blockquote key={i}>"{excerpt}"</blockquote>
          ))}
        </div>
      )}

      {card.transformation_history && card.transformation_history.length > 0 && (
        <div className="card-history">
          <small>
            Transformed {card.transformation_history.length}x (last: {card.transformation_history[card.transformation_history.length - 1].mode})
          </small>
        </div>
      )}

      <div className="card-actions">
        <button
          className={`card-action approve ${card.status === 'approved' ? 'active' : ''}`}
          onClick={() => onApprove(card.id, cardType)}
          disabled={isTransforming}
        >
          ✓
        </button>
        <button
          className={`card-action reject ${card.status === 'rejected' ? 'active' : ''}`}
          onClick={() => onReject(card.id, cardType)}
          disabled={isTransforming}
        >
          ✗
        </button>
        <RefineDropdown
          card={card}
          cardType={cardType}
          onTransform={onTransform}
          isTransforming={isTransforming}
        />
      </div>
    </div>
  )
}

export default function ConceptSetupWizard({ sourceId, onComplete, onCancel }) {
  // Wizard state
  const [stage, setStage] = useState(STAGES.NOTES)
  const [notes, setNotes] = useState('')
  const [conceptName, setConceptName] = useState('')

  // Stage-specific data
  const [stageData, setStageData] = useState({
    stage1: { questions: [], answers: [] },
    stage2: { questions: [], answers: [] },
    stage3: { questions: [], answers: [] }
  })

  // Current stage Q&A
  const [questions, setQuestions] = useState([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)

  // Enhanced answer state
  const [currentAnswer, setCurrentAnswer] = useState({
    selectedOptions: [],
    textAnswer: '',
    customResponse: '',
    customCategory: null,
    isDialectic: false,
    dialecticPoleA: '',
    dialecticPoleB: '',
    dialecticNote: '',
    optionComments: {}  // { optionValue: comment }
  })

  // Option comment expansion state
  const [expandedComments, setExpandedComments] = useState({})

  // Analysis results
  const [interimAnalysis, setInterimAnalysis] = useState(null)
  const [implicationsPreview, setImplicationsPreview] = useState(null)
  const [dialectics, setDialectics] = useState([])

  // Understanding validation state (Phase 2)
  const [notesUnderstanding, setNotesUnderstanding] = useState(null)
  const [understandingRating, setUnderstandingRating] = useState(0)  // 1-5 stars
  const [understandingCorrection, setUnderstandingCorrection] = useState('')
  const [isRegenerating, setIsRegenerating] = useState(false)

  // Granular feedback state for key insights
  const [insightFeedback, setInsightFeedback] = useState({})  // { index: { status: 'approved'|'rejected', comment: '' } }
  const [expandedInsightComment, setExpandedInsightComment] = useState({})  // { index: true/false }

  // Granular feedback state for tensions
  const [tensionFeedback, setTensionFeedback] = useState({})  // { index: { status: 'approved'|'approved_with_comment'|'rejected', comment: '' } }
  const [expandedTensionComment, setExpandedTensionComment] = useState({})  // { index: true/false }
  const [isGeneratingTensions, setIsGeneratingTensions] = useState(false)

  // Genealogy state - intellectual origins and influences
  const [userInfluences, setUserInfluences] = useState([])  // User-added influences not detected
  const [genealogyAnswers, setGenealogyAnswers] = useState({})  // Answers to probing questions
  const [expandedGenealogy, setExpandedGenealogy] = useState(true)  // Show/hide genealogy section

  // Generated examples state (Phase 4 - synthetic case studies)
  const [generatedCases, setGeneratedCases] = useState([])
  const [caseRatings, setCaseRatings] = useState({})  // { case_id: 'good' | 'partial' | 'not_fit' }
  const [caseComments, setCaseComments] = useState({})  // { case_id: 'comment...' }
  const [generatedMarkers, setGeneratedMarkers] = useState([])
  const [markerRatings, setMarkerRatings] = useState({})
  const [markerComments, setMarkerComments] = useState({})
  const [isGeneratingExamples, setIsGeneratingExamples] = useState(false)

  // Thinking/processing state
  const [thinking, setThinking] = useState('')
  const [thinkingVisible, setThinkingVisible] = useState(true)
  const [currentPhase, setCurrentPhase] = useState(null)

  // Progress state (9 stages total with understanding validation)
  const [progress, setProgress] = useState({ stage: 0, total: 9, label: 'Getting started' })
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  // Final concept data
  const [conceptData, setConceptData] = useState(null)

  // Editable draft state for 9-dimension final page
  const [editableDraft, setEditableDraft] = useState({
    genesis: { type: '', lineage: '', break_from: '' },
    problem_space: { gap: '', failed_alternatives: '' },
    definition: '',
    differentiations: [],
    paradigmatic_cases: [],
    recognition_markers: [],
    core_claims: { ontological: '', causal: '' },
    falsification_conditions: [],
    dialectics: []
  })
  const [editingSection, setEditingSection] = useState(null)
  const [sectionFeedback, setSectionFeedback] = useState({})
  const [isRegeneratingSections, setIsRegeneratingSections] = useState({})

  // Document upload state
  const [uploadedDocuments, setUploadedDocuments] = useState([])  // [{name, size, analysis}]
  const [selectedFile, setSelectedFile] = useState(null)
  const [isUploadingDocument, setIsUploadingDocument] = useState(false)
  const [documentAnalysisProgress, setDocumentAnalysisProgress] = useState(null)
  const [dimensionalExtraction, setDimensionalExtraction] = useState(null)  // Combined 9-dim data from docs

  // Deep Commitments state (9 philosophical dimensions) - Phase 1
  const [deepCommitmentQuestions, setDeepCommitmentQuestions] = useState([])
  const [deepCommitmentAnswers, setDeepCommitmentAnswers] = useState({})  // {question_id: {selected, comment}}
  const [currentCommitmentIndex, setCurrentCommitmentIndex] = useState(0)
  const [isGeneratingCommitments, setIsGeneratingCommitments] = useState(false)

  // Phase 2: Follow-up questions based on Phase 1 answers
  const [phase2Questions, setPhase2Questions] = useState([])
  const [phase2Answers, setPhase2Answers] = useState({})
  const [currentPhase2Index, setCurrentPhase2Index] = useState(0)
  const [isGeneratingPhase2, setIsGeneratingPhase2] = useState(false)

  // Phase 3: Final verification/synthesis questions
  const [phase3Questions, setPhase3Questions] = useState([])
  const [phase3Answers, setPhase3Answers] = useState({})
  const [currentPhase3Index, setCurrentPhase3Index] = useState(0)
  const [isGeneratingPhase3, setIsGeneratingPhase3] = useState(false)

  // Card-based review state (new flow: hypothesis, genealogy, differentiation cards)
  const [hypothesisCards, setHypothesisCards] = useState([])  // From notes analysis
  const [genealogyCards, setGenealogyCards] = useState([])
  const [differentiationCards, setDifferentiationCards] = useState([])
  const [dimensionalSignals, setDimensionalSignals] = useState({})  // 9-dim signals from notes
  const [isTransformingCard, setIsTransformingCard] = useState(null)  // card_id being transformed
  const [cardReviewStage, setCardReviewStage] = useState('hypothesis')  // hypothesis, genealogy, differentiation

  // Generated options state (for open-ended questions)
  const [generatedOptions, setGeneratedOptions] = useState([])  // Options generated from notes/context
  const [selectedGeneratedOptions, setSelectedGeneratedOptions] = useState([])  // Multi-select: array of selected option IDs
  const [generatedOptionsComment, setGeneratedOptionsComment] = useState('')  // User comment on selections
  const [isGeneratingOptions, setIsGeneratingOptions] = useState(false)
  const [transformingOptionId, setTransformingOptionId] = useState(null)  // Option being transformed
  const [hasAutoGeneratedForQuestion, setHasAutoGeneratedForQuestion] = useState(null)  // Track auto-generation per question

  // Intellectual Genealogy state (Stage 8)
  const [genealogyHypotheses, setGenealogyHypotheses] = useState([])  // Generated genealogy hypotheses
  const [userAddedInfluences, setUserAddedInfluences] = useState([])  // User-added influences
  const [isGeneratingGenealogy, setIsGeneratingGenealogy] = useState(false)
  const [newInfluenceInput, setNewInfluenceInput] = useState({ name: '', type: 'thinker', connection: '' })

  // Curator-Sharpener Blind Spots Questioning state
  const [blindSpotsQueue, setBlindSpotsQueue] = useState({
    slots: [],
    currentIndex: 0,
    sharpenerPending: [],
    completedCount: 0,
    skippedCount: 0
  })
  const [curatorAllocation, setCuratorAllocation] = useState(null)
  const [currentBlindSpotAnswer, setCurrentBlindSpotAnswer] = useState('')
  const [answerOptions, setAnswerOptions] = useState(null)  // Generated multiple choice options
  const [selectedOptionIds, setSelectedOptionIds] = useState([])  // Track multi-select
  const [writeInAddition, setWriteInAddition] = useState('')  // Additional write-in text
  const [isGeneratingOptions, setIsGeneratingOptions] = useState(false)
  const [isCurating, setIsCurating] = useState(false)
  const [isSharpening, setIsSharpening] = useState(false)
  const [blindSpotsQuality, setBlindSpotsQuality] = useState(null)

  // Session persistence state
  const [hasSavedSession, setHasSavedSession] = useState(false)
  const [savedSessionInfo, setSavedSessionInfo] = useState(null)

  // Server session state
  const [serverSessions, setServerSessions] = useState([])
  const [currentSessionKey, setCurrentSessionKey] = useState(null)
  const [isLoadingServerSessions, setIsLoadingServerSessions] = useState(false)
  const [serverSessionError, setServerSessionError] = useState(null)

  // Refs
  const thinkingRef = useRef(null)
  const abortControllerRef = useRef(null)
  const serverSaveTimeoutRef = useRef(null)

  // =========================================================================
  // SESSION PERSISTENCE - Save/Restore wizard state (localStorage + server)
  // =========================================================================
  const STORAGE_KEY = `concept_wizard_session_${sourceId || 'default'}`

  // Fetch server sessions on mount
  useEffect(() => {
    fetchServerSessions()
  }, [])

  // Fetch sessions from server
  const fetchServerSessions = async () => {
    setIsLoadingServerSessions(true)
    setServerSessionError(null)
    try {
      const response = await fetch(`${API_URL}/concepts/wizard/sessions?status=active`)
      if (response.ok) {
        const sessions = await response.json()
        setServerSessions(sessions)
      } else {
        console.error('Failed to fetch server sessions:', response.status)
      }
    } catch (e) {
      console.error('Error fetching server sessions:', e)
      setServerSessionError('Could not connect to server')
    } finally {
      setIsLoadingServerSessions(false)
    }
  }

  // Save session to server (debounced)
  const saveToServer = async (sessionData) => {
    if (!currentSessionKey && !sessionData.conceptName) return

    try {
      const response = await fetch(`${API_URL}/concepts/wizard/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_key: currentSessionKey || undefined,
          concept_name: sessionData.conceptName,
          session_state: sessionData,
          stage: sessionData.stage,
          source_id: sourceId || null
        })
      })

      if (response.ok) {
        const saved = await response.json()
        if (!currentSessionKey) {
          setCurrentSessionKey(saved.session_key)
        }
        return saved
      }
    } catch (e) {
      console.error('Error saving session to server:', e)
    }
    return null
  }

  // Check for saved session on mount (localStorage fallback)
  useEffect(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY)
      if (saved) {
        const parsed = JSON.parse(saved)
        if (parsed.conceptName && parsed.stage !== STAGES.NOTES) {
          setHasSavedSession(true)
          setSavedSessionInfo({
            conceptName: parsed.conceptName,
            stage: parsed.stage,
            savedAt: parsed.savedAt
          })
        }
      }
    } catch (e) {
      console.error('Error checking saved session:', e)
    }
  }, [])

  // Save session state on significant changes
  useEffect(() => {
    // Don't save if we're at the beginning or if no concept name
    if (stage === STAGES.NOTES || !conceptName) return

    const sessionData = {
      stage,
      conceptName,
      notes,
      stageData,
      notesUnderstanding,
      hypothesisCards,
      differentiationCards,
      tensionFeedback,
      uploadedDocuments,
      dimensionalExtraction,
      questions,
      currentQuestionIndex,
      interimAnalysis,
      blindSpotsQueue,
      curatorAllocation,
      savedAt: new Date().toISOString()
    }

    // Save to localStorage immediately
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(sessionData))
    } catch (e) {
      console.error('Error saving session to localStorage:', e)
    }

    // Save to server (debounced - 3 seconds)
    if (serverSaveTimeoutRef.current) {
      clearTimeout(serverSaveTimeoutRef.current)
    }
    serverSaveTimeoutRef.current = setTimeout(() => {
      saveToServer(sessionData)
    }, 3000)

    return () => {
      if (serverSaveTimeoutRef.current) {
        clearTimeout(serverSaveTimeoutRef.current)
      }
    }
  }, [stage, conceptName, notes, stageData, notesUnderstanding, hypothesisCards, differentiationCards, tensionFeedback, uploadedDocuments, dimensionalExtraction, questions, currentQuestionIndex, interimAnalysis, blindSpotsQueue, curatorAllocation])

  // Restore from localStorage
  const restoreSession = () => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY)
      if (saved) {
        const parsed = JSON.parse(saved)
        applySessionData(parsed)
        setHasSavedSession(false)
        setSavedSessionInfo(null)
      }
    } catch (e) {
      console.error('Error restoring session:', e)
      clearSavedSession()
    }
  }

  // Restore from server session
  const restoreServerSession = async (sessionKey) => {
    try {
      const response = await fetch(`${API_URL}/concepts/wizard/sessions/${sessionKey}`)
      if (response.ok) {
        const session = await response.json()
        applySessionData(session.session_state)
        setCurrentSessionKey(session.session_key)
      } else {
        setError('Failed to load session from server')
      }
    } catch (e) {
      console.error('Error restoring server session:', e)
      setError('Could not connect to server')
    }
  }

  // Apply session data to state (shared between local and server restore)
  const applySessionData = (parsed) => {
    console.log('[Session Restore] Restoring stage:', parsed.stage, 'blindSpotsQueue:', parsed.blindSpotsQueue)
    setStage(parsed.stage)
    setConceptName(parsed.conceptName)
    setNotes(parsed.notes || '')
    setStageData(parsed.stageData || { stage1: { questions: [], answers: [] }, stage2: { questions: [], answers: [] }, stage3: { questions: [], answers: [] } })
    setNotesUnderstanding(parsed.notesUnderstanding || null)
    setHypothesisCards(parsed.hypothesisCards || [])
    setDifferentiationCards(parsed.differentiationCards || [])
    setTensionFeedback(parsed.tensionFeedback || {})
    setUploadedDocuments(parsed.uploadedDocuments || [])
    setDimensionalExtraction(parsed.dimensionalExtraction || null)
    setQuestions(parsed.questions || [])
    setCurrentQuestionIndex(parsed.currentQuestionIndex || 0)
    setInterimAnalysis(parsed.interimAnalysis || null)
    // Restore blind spots questioning state (normalize in case of snake_case from old sessions)
    if (parsed.blindSpotsQueue) {
      const queue = parsed.blindSpotsQueue
      setBlindSpotsQueue({
        slots: queue.slots || [],
        currentIndex: queue.current_index ?? queue.currentIndex ?? 0,
        sharpenerPending: queue.sharpener_pending || queue.sharpenerPending || [],
        completedCount: queue.completed_count ?? queue.completedCount ?? 0,
        skippedCount: queue.skipped_count ?? queue.skippedCount ?? 0
      })
    }
    if (parsed.curatorAllocation) {
      setCuratorAllocation(parsed.curatorAllocation)
    }
  }

  // Delete server session
  const deleteServerSession = async (sessionKey) => {
    try {
      const response = await fetch(`${API_URL}/concepts/wizard/sessions/${sessionKey}`, {
        method: 'DELETE'
      })
      if (response.ok) {
        setServerSessions(prev => prev.filter(s => s.session_key !== sessionKey))
      }
    } catch (e) {
      console.error('Error deleting server session:', e)
    }
  }

  // Clear saved session
  const clearSavedSession = () => {
    try {
      localStorage.removeItem(STORAGE_KEY)
      setHasSavedSession(false)
      setSavedSessionInfo(null)
    } catch (e) {
      console.error('Error clearing session:', e)
    }
  }

  // Manual save checkpoint (saves to both localStorage and server)
  const saveCheckpoint = async () => {
    if (!conceptName || stage === STAGES.NOTES) return

    const sessionData = {
      stage,
      conceptName,
      notes,
      stageData,
      notesUnderstanding,
      hypothesisCards,
      differentiationCards,
      tensionFeedback,
      uploadedDocuments,
      dimensionalExtraction,
      questions,
      currentQuestionIndex,
      interimAnalysis,
      blindSpotsQueue,
      curatorAllocation,
      savedAt: new Date().toISOString(),
      isManualCheckpoint: true
    }

    // Save to localStorage
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(sessionData))
    } catch (e) {
      console.error('Error saving checkpoint to localStorage:', e)
    }

    // Save to server immediately (not debounced for manual saves)
    const originalLabel = progress.label
    setProgress(prev => ({ ...prev, label: 'Saving to server...' }))

    const saved = await saveToServer(sessionData)

    if (saved) {
      setProgress(prev => ({ ...prev, label: '✓ Saved to server!' }))
    } else {
      setProgress(prev => ({ ...prev, label: '✓ Saved locally (server unavailable)' }))
    }
    setTimeout(() => setProgress(prev => ({ ...prev, label: originalLabel })), 2000)
  }

  // Navigate to a specific stage
  const navigateToStage = (targetStage) => {
    // Don't allow navigation to analyzing/processing stages
    const navItem = STAGE_NAV.find(n => n.id === targetStage)
    if (!navItem || !navItem.navigable) return

    // Don't navigate if already at this stage
    if (getNavCheckpoint(stage) === targetStage) return

    // Allow navigation
    setStage(targetStage)
    setError(null)
    setThinking('')
  }

  // Get the previous navigable stage for back button
  const getPreviousStage = () => {
    const currentCheckpoint = getNavCheckpoint(stage)
    const currentIndex = STAGE_NAV.findIndex(n => n.id === currentCheckpoint)
    if (currentIndex <= 0) return null
    return STAGE_NAV[currentIndex - 1].id
  }

  // Go back to previous stage
  const goBack = () => {
    const prevStage = getPreviousStage()
    if (prevStage) {
      navigateToStage(prevStage)
    }
  }

  // Auto-scroll thinking panel
  useEffect(() => {
    if (thinkingRef.current) {
      thinkingRef.current.scrollTop = thinkingRef.current.scrollHeight
    }
  }, [thinking])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
      }
    }
  }, [])

  // Load prefilled answer when question changes (for Stage 1 preprocessing)
  useEffect(() => {
    if (questions.length > 0 && currentQuestionIndex >= 0 && currentQuestionIndex < questions.length) {
      const currentQ = questions[currentQuestionIndex]
      if (currentQ?.prefilled?.value) {
        loadPrefilledAnswer(currentQ)
      }
    }
  }, [questions, currentQuestionIndex])

  // Reset answer state when moving to new question
  const resetCurrentAnswer = () => {
    setCurrentAnswer({
      selectedOptions: [],
      textAnswer: '',
      customResponse: '',
      customCategory: null,
      isDialectic: false,
      dialecticPoleA: '',
      dialecticPoleB: '',
      dialecticNote: '',
      optionComments: {}
    })
    setExpandedComments({})
  }

  // Load prefilled answer for current question if available
  const loadPrefilledAnswer = (question) => {
    if (!question?.prefilled?.value) {
      resetCurrentAnswer()
      return
    }

    const prefill = question.prefilled
    const value = prefill.value

    if (question.type === 'open_ended') {
      setCurrentAnswer({
        selectedOptions: [],
        textAnswer: value || '',
        customResponse: '',
        customCategory: null,
        isDialectic: false,
        dialecticPoleA: '',
        dialecticPoleB: '',
        dialecticNote: '',
        optionComments: {}
      })
    } else {
      // multiple_choice or multi_select
      const options = Array.isArray(value) ? value : [value]
      setCurrentAnswer({
        selectedOptions: options,
        textAnswer: '',
        customResponse: '',
        customCategory: null,
        isDialectic: false,
        dialecticPoleA: '',
        dialecticPoleB: '',
        dialecticNote: '',
        optionComments: {}
      })
    }
    setExpandedComments({})
  }

  /**
   * Stream response from wizard API with enhanced event handling
   */
  const streamWizardRequest = async (endpoint, body, handlers = {}) => {
    setLoading(true)
    setError(null)
    setThinking('')
    setCurrentPhase(null)

    abortControllerRef.current = new AbortController()

    try {
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        signal: abortControllerRef.current.signal
      })

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Request failed' }))
        // Handle FastAPI validation errors which return detail as an array
        const detail = error.detail
        let errorMessage = 'Request failed'
        if (typeof detail === 'string') {
          errorMessage = detail
        } else if (Array.isArray(detail)) {
          errorMessage = detail.map(d => d.msg || d.message || JSON.stringify(d)).join('; ')
        } else if (detail?.msg || detail?.message) {
          errorMessage = detail.msg || detail.message
        }
        throw new Error(errorMessage)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            if (data === '[DONE]') continue

            try {
              const event = JSON.parse(data)

              if (event.type === 'phase') {
                setCurrentPhase(event.phase)
                handlers.onPhase?.(event.phase)
              } else if (event.type === 'thinking') {
                // Only call handler - don't also set state here, as handler does that
                handlers.onThinking?.(event.content)
              } else if (event.type === 'text') {
                handlers.onText?.(event.content)
              } else if (event.type === 'interim_complete') {
                setInterimAnalysis(event.data)
                handlers.onInterimComplete?.(event.data)
              } else if (event.type === 'complete') {
                handlers.onComplete?.(event.data)
              } else if (event.type === 'curator_complete') {
                handlers.onCuratorComplete?.(event.data)
              } else if (event.type === 'sharpener_complete') {
                handlers.onSharpenerComplete?.(event.data)
              } else if (event.type === 'sharpener_started') {
                handlers.onSharpenerStarted?.(event.data)
              } else if (event.type === 'error') {
                const errMsg = typeof event.message === 'string'
                  ? event.message
                  : (event.message?.detail || event.message?.error || JSON.stringify(event.message))
                throw new Error(errMsg)
              }
            } catch (e) {
              if (e.message !== 'Unexpected end of JSON input') {
                console.error('Parse error:', e)
              }
            }
          }
        }
      }
    } catch (err) {
      if (err.name !== 'AbortError') {
        const errorMsg = typeof err === 'string' ? err : (err?.message || JSON.stringify(err))
        setError(errorMsg)
        console.error('Stream error:', err)
      }
    } finally {
      setLoading(false)
      setCurrentPhase(null)
    }
  }

  // =========================================================================
  // CURATOR-SHARPENER BLIND SPOTS QUESTIONING
  // =========================================================================

  /**
   * Helper to normalize snake_case queue from backend to camelCase for frontend
   */
  const normalizeQueueState = (queue) => ({
    slots: queue?.slots || [],
    currentIndex: queue?.current_index ?? queue?.currentIndex ?? 0,
    sharpenerPending: queue?.sharpener_pending || queue?.sharpenerPending || [],
    completedCount: queue?.completed_count ?? queue?.completedCount ?? 0,
    skippedCount: queue?.skipped_count ?? queue?.skippedCount ?? 0
  })

  /**
   * Start the Curator service to analyze notes and allocate blind spot questions
   */
  const startCurator = async () => {
    console.log('[Curator] Starting curator service...')
    console.log('[Curator] conceptName:', conceptName, 'notes length:', notes?.length, 'sessionKey:', currentSessionKey)
    setStage(STAGES.BLIND_SPOTS_CURATING)
    setIsCurating(true)
    setProgress({ stage: 3, total: 11, label: 'Analyzing blind spots...' })

    await streamWizardRequest(
      '/concepts/wizard/curate-blind-spots',
      {
        concept_name: conceptName,
        notes: notes,
        notes_understanding: notesUnderstanding,
        session_id: currentSessionKey
      },
      {
        onThinking: (content) => {
          setThinking(prev => prev + content)
        },
        onCuratorComplete: (data) => {
          console.log('[Curator] Complete! Received allocation:', data.curator_allocation?.total_slots, 'slots')
          console.log('[Curator] Queue:', data.blind_spots_queue?.slots?.length, 'questions')
          console.log('[Curator] First slot:', data.blind_spots_queue?.slots?.[0])
          setCuratorAllocation(data.curator_allocation)
          // Normalize snake_case from backend to camelCase for frontend
          setBlindSpotsQueue(normalizeQueueState(data.blind_spots_queue))
          setStage(STAGES.BLIND_SPOTS_QUESTIONING)
          setIsCurating(false)
        }
      }
    )
  }

  /**
   * Submit an answer to a blind spot question
   */
  const submitBlindSpotAnswer = async (skip = false) => {
    const currentSlot = blindSpotsQueue.slots[blindSpotsQueue.currentIndex]
    if (!currentSlot) return

    // Build the answer: use combined options + write-in if using options mode,
    // otherwise use the regular textarea answer
    let finalAnswer = ''
    if (!skip) {
      if (answerOptions && (selectedOptionIds.length > 0 || writeInAddition.trim())) {
        finalAnswer = buildCombinedAnswer()
      } else {
        finalAnswer = currentBlindSpotAnswer
      }
    }

    try {
      const response = await fetch(`${API_URL}/concepts/wizard/submit-blind-spot-answer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: currentSessionKey,
          slot_id: currentSlot.slot_id,
          answer: finalAnswer,
          skip: skip
        })
      })

      if (!response.ok) throw new Error('Failed to submit answer')
      const data = await response.json()

      // Update local queue state (normalize snake_case to camelCase)
      setBlindSpotsQueue(normalizeQueueState(data.queue_state))
      setCurrentBlindSpotAnswer('')
      setAnswerOptions(null)  // Clear options for next question
      setSelectedOptionIds([])  // Clear multi-select
      setWriteInAddition('')  // Clear write-in

      // Check if complete
      if (data.is_complete) {
        setBlindSpotsQuality(data.quality)
        setStage(STAGES.DOCUMENT_UPLOAD)
        return
      }

      // Trigger sharpener if recommended
      if (data.should_sharpen && data.sharpener_context) {
        triggerSharpener(data.sharpener_context)
      }
    } catch (err) {
      setError(err.message)
    }
  }

  /**
   * Generate multiple choice answer options for the current question
   * Implements prn_intent_formation_state_bifurcation - guided discovery for unformed intent
   */
  const generateAnswerOptions = async () => {
    const currentSlot = blindSpotsQueue.slots[blindSpotsQueue.currentIndex]
    if (!currentSlot) return

    setIsGeneratingOptions(true)
    setAnswerOptions(null)

    try {
      // Gather previous answers for context
      const previousAnswers = blindSpotsQueue.slots
        .filter(s => s.status === 'answered' && s.answer)
        .map(s => ({ question: s.question, answer: s.answer }))

      const response = await fetch(`${API_URL}/concepts/wizard/generate-answer-options`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: currentSlot.question,
          category: currentSlot.category,
          concept_name: conceptName,
          notes_context: notes,
          previous_answers: previousAnswers
        })
      })

      if (!response.ok) throw new Error('Failed to generate options')
      const data = await response.json()

      setAnswerOptions(data)
    } catch (err) {
      console.error('Error generating answer options:', err)
      setError('Failed to generate answer options. Try writing your own answer.')
    } finally {
      setIsGeneratingOptions(false)
    }
  }

  /**
   * Toggle selection of an answer option
   * Handles both mutually exclusive (single select) and non-exclusive (multi-select) modes
   */
  const toggleAnswerOption = (option) => {
    const isMutuallyExclusive = answerOptions?.mutually_exclusive ?? true

    if (isMutuallyExclusive) {
      // Single select mode - replace selection
      if (selectedOptionIds.includes(option.id)) {
        setSelectedOptionIds([])
      } else {
        setSelectedOptionIds([option.id])
      }
    } else {
      // Multi-select mode - toggle in array
      setSelectedOptionIds(prev =>
        prev.includes(option.id)
          ? prev.filter(id => id !== option.id)
          : [...prev, option.id]
      )
    }
  }

  /**
   * Build combined answer from selected options + write-in
   */
  const buildCombinedAnswer = () => {
    const parts = []

    // Add selected option texts
    if (answerOptions && selectedOptionIds.length > 0) {
      const selectedTexts = answerOptions.options
        .filter(opt => selectedOptionIds.includes(opt.id))
        .map(opt => opt.text)
      parts.push(...selectedTexts)
    }

    // Add write-in if present
    if (writeInAddition.trim()) {
      parts.push(writeInAddition.trim())
    }

    return parts.join('\n\n')
  }

  /**
   * Check if we have a valid answer (from options or write-in or both)
   */
  const hasValidAnswer = () => {
    return selectedOptionIds.length > 0 || writeInAddition.trim() || currentBlindSpotAnswer.trim()
  }

  /**
   * Trigger the Sharpener service to generate a follow-up question
   * Runs in background while user answers other questions
   */
  const triggerSharpener = async (context) => {
    setIsSharpening(true)

    // Add to pending list
    setBlindSpotsQueue(prev => ({
      ...prev,
      sharpenerPending: [...prev.sharpenerPending, context.slot_id]
    }))

    await streamWizardRequest(
      '/concepts/wizard/sharpen-question',
      {
        session_id: currentSessionKey,
        slot_id: context.slot_id,
        answer: context.answer,
        concept_name: conceptName,
        notes_context: notes
      },
      {
        onSharpenerComplete: (data) => {
          // Insert new slot into queue
          setBlindSpotsQueue(prev => {
            const newSlots = [...prev.slots]
            newSlots.splice(data.insert_position, 0, data.new_slot)
            return {
              ...prev,
              slots: newSlots,
              sharpenerPending: prev.sharpenerPending.filter(id => id !== context.slot_id)
            }
          })
          setIsSharpening(false)
        }
      }
    )
  }

  /**
   * Finish blind spots questioning early
   */
  const finishBlindSpotsEarly = async () => {
    try {
      const response = await fetch(`${API_URL}/concepts/wizard/finish-blind-spots`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: currentSessionKey })
      })

      if (!response.ok) throw new Error('Failed to finish')
      const data = await response.json()

      setBlindSpotsQuality(data.quality)
      setStage(STAGES.DOCUMENT_UPLOAD)
    } catch (err) {
      setError(err.message)
    }
  }

  /**
   * Get the current blind spot question slot
   */
  const getCurrentBlindSpotSlot = () => {
    return blindSpotsQueue.slots[blindSpotsQueue.currentIndex] || null
  }

  /**
   * Start the staged wizard flow
   */
  const startWizard = async () => {
    if (!conceptName.trim()) {
      setError('Please enter a concept name')
      return
    }

    setStage(STAGES.ANALYZING_NOTES)
    setProgress({ stage: 1, total: 9, label: 'Analyzing your notes...' })

    await streamWizardRequest(
      '/concepts/wizard/stage1',
      { concept_name: conceptName, notes: notes, source_id: sourceId },
      {
        onThinking: (content) => {
          setThinking(prev => prev + content)
        },
        onComplete: (data) => {
          // Store questions and analysis for later use
          setQuestions(data.questions || [])
          // Support both new (gaps_tensions_questions) and old (potential_tensions) field names
          const gapsTensionsQuestions = data.gaps_tensions_questions || data.potential_tensions || []
          setStageData(prev => ({
            ...prev,
            stage1: {
              ...prev.stage1,
              questions: data.questions || [],
              notesAnalysis: data.notes_analysis || null,
              gapsTensionsQuestions: gapsTensionsQuestions
            }
          }))

          // Pre-populate answers from prefilled values
          const prefilledAnswers = []
          for (const q of (data.questions || [])) {
            if (q.prefilled && q.prefilled.value) {
              prefilledAnswers.push({
                question_id: q.id,
                selected_options: Array.isArray(q.prefilled.value) ? q.prefilled.value :
                                  (q.type === 'multiple_choice' || q.type === 'multi_select') ? [q.prefilled.value] : null,
                text_answer: q.type === 'open_ended' ? q.prefilled.value : null,
                prefilled_confidence: q.prefilled.confidence,
                prefilled_reasoning: q.prefilled.reasoning
              })
            }
          }
          if (prefilledAnswers.length > 0) {
            setStageData(prev => ({
              ...prev,
              stage1: { ...prev.stage1, prefilledAnswers }
            }))
          }

          // Build understanding object for validation
          const understanding = {
            summary: data.notes_analysis?.summary || 'Unable to extract summary from your notes.',
            preliminaryDefinition: data.notes_analysis?.preliminary_definition || null,
            keyInsights: data.notes_analysis?.key_insights || [],
            gapsTensionsQuestions: gapsTensionsQuestions,
            // Genealogy - intellectual origins and influences
            genealogy: data.genealogy || {
              detected_influences: [],
              emergence_context: {},
              needs_probing: []
            },
            // 9-dimensional signals extracted from notes
            dimensionalSignals: data.dimensional_signals || null,
            prefilledCount: prefilledAnswers.length,
            totalQuestions: (data.questions || []).length,
            confidenceLevels: prefilledAnswers.reduce((acc, p) => {
              const conf = p.prefilled_confidence || 'low'
              acc[conf] = (acc[conf] || 0) + 1
              return acc
            }, {})
          }
          setNotesUnderstanding(understanding)

          // Store dimensional signals in dimensional extraction state
          if (data.dimensional_signals) {
            setDimensionalExtraction(prev => ({
              ...prev,
              ...data.dimensional_signals,
              source: 'notes_preprocessing'
            }))
            setDimensionalSignals(data.dimensional_signals)
          }

          // Store new card-based data from notes analysis
          if (data.hypothesis_cards && data.hypothesis_cards.length > 0) {
            setHypothesisCards(data.hypothesis_cards)
          }
          if (data.genealogy_cards && data.genealogy_cards.length > 0) {
            setGenealogyCards(data.genealogy_cards)
          }
          if (data.differentiation_cards && data.differentiation_cards.length > 0) {
            setDifferentiationCards(data.differentiation_cards)
          }

          // Go to understanding validation instead of directly to Stage 1
          setProgress({ stage: 2, total: 9, label: 'Validate my understanding' })
          setStage(STAGES.UNDERSTANDING_VALIDATION)
          setThinking('')
        }
      }
    )
  }

  /**
   * Accept understanding and proceed to Stage 1
   * If user provided granular feedback, refine pre-fills first
   */
  const acceptUnderstandingAndContinue = async () => {
    // Check if user provided any granular feedback
    const hasInsightFeedback = Object.keys(insightFeedback).length > 0
    const hasTensionFeedback = Object.keys(tensionFeedback).length > 0
    const hasGenealogyAnswers = Object.keys(genealogyAnswers).length > 0
    const hasUserInfluences = userInfluences.length > 0

    if (hasInsightFeedback || hasTensionFeedback || hasGenealogyAnswers || hasUserInfluences) {
      // User provided granular feedback - refine pre-fills before continuing
      setStage(STAGES.ANALYZING_NOTES)
      setProgress({ stage: 2, total: 9, label: 'Refining understanding with your feedback...' })
      setThinking('')

      await streamWizardRequest(
        '/concepts/wizard/refine-with-feedback',
        {
          concept_name: conceptName,
          notes: notes,
          original_understanding: {
            summary: notesUnderstanding.summary,
            preliminaryDefinition: notesUnderstanding.preliminaryDefinition,
            key_insights: notesUnderstanding.keyInsights,
            gapsTensionsQuestions: notesUnderstanding.gapsTensionsQuestions,
            genealogy: notesUnderstanding.genealogy
          },
          insight_feedback: insightFeedback,
          tension_feedback: tensionFeedback,
          // Genealogy user input
          genealogy_answers: genealogyAnswers,
          user_influences: userInfluences,
          original_questions: questions,
          source_id: sourceId
        },
        {
          onThinking: (content) => {
            setThinking(prev => prev + content)
          },
          onComplete: (data) => {
            // Update questions with refined pre-fills
            setQuestions(data.refined_questions || questions)

            // Update the notes analysis shown in Stage 1
            setStageData(prev => ({
              ...prev,
              stage1: {
                ...prev.stage1,
                questions: data.refined_questions || questions,
                notesAnalysis: data.refined_understanding || prev.stage1.notesAnalysis,
                approvedTensions: data.approved_tensions || [],
                validationNote: data.validation_note
              }
            }))

            // Clear feedback state for next time
            setInsightFeedback({})
            setTensionFeedback({})
            setExpandedInsightComment({})
            setExpandedTensionComment({})
            // Clear genealogy feedback state
            setGenealogyAnswers({})
            setUserInfluences([])

            // Now proceed to Stage 1
            setProgress({ stage: 3, total: 9, label: 'Stage 1: Genesis & Problem Space' })
            setStage(STAGES.STAGE1)
            setCurrentQuestionIndex(0)
            setThinking('')
          }
        }
      )
    } else {
      // No granular feedback - proceed directly
      setProgress({ stage: 3, total: 9, label: 'Stage 1: Genesis & Problem Space' })
      setStage(STAGES.STAGE1)
      setCurrentQuestionIndex(0)
    }
  }

  /**
   * Generate synthetic case studies
   */
  const generateCaseStudies = async () => {
    setIsGeneratingExamples(true)
    setError(null)
    setThinking('')

    // Build concept definition from interim analysis
    const definition = interimAnalysis?.understanding_summary ||
      stageData.stage1?.notesAnalysis?.preliminary_definition ||
      ''

    // Build context from answers
    const context = [
      ...stageData.stage1.answers.map(a => `${a.question_id}: ${a.text_answer || a.selected_options?.join(', ')}`),
      ...stageData.stage2.answers.map(a => `${a.question_id}: ${a.text_answer || a.selected_options?.join(', ')}`)
    ].join('\n')

    await streamWizardRequest(
      '/concepts/wizard/generate-case-studies',
      {
        concept_name: conceptName,
        concept_definition: definition,
        context: context
      },
      {
        onThinking: (content) => {
          setThinking(prev => prev + content)
        },
        onComplete: (data) => {
          setGeneratedCases(data.generated_cases || [])
          setIsGeneratingExamples(false)
          setThinking('')
        }
      }
    )
  }

  /**
   * Generate recognition markers
   */
  const generateRecognitionMarkers = async () => {
    setIsGeneratingExamples(true)
    setError(null)
    setThinking('')

    // Build concept definition from interim analysis
    const definition = interimAnalysis?.understanding_summary ||
      stageData.stage1?.notesAnalysis?.preliminary_definition ||
      ''

    // Get approved cases
    const approvedCases = generatedCases.filter(c =>
      caseRatings[c.id] === 'good' || caseRatings[c.id] === 'partial'
    )

    await streamWizardRequest(
      '/concepts/wizard/generate-recognition-markers',
      {
        concept_name: conceptName,
        concept_definition: definition,
        paradigmatic_cases: approvedCases
      },
      {
        onThinking: (content) => {
          setThinking(prev => prev + content)
        },
        onComplete: (data) => {
          setGeneratedMarkers(data.generated_markers || [])
          setIsGeneratingExamples(false)
          setThinking('')
        }
      }
    )
  }

  /**
   * Rate a generated case
   */
  const rateCaseStudy = (caseId, rating) => {
    setCaseRatings(prev => ({ ...prev, [caseId]: rating }))
  }

  /**
   * Update comment on a case
   */
  const updateCaseComment = (caseId, comment) => {
    setCaseComments(prev => ({ ...prev, [caseId]: comment }))
  }

  /**
   * Rate a recognition marker
   */
  const rateMarker = (markerId, rating) => {
    setMarkerRatings(prev => ({ ...prev, [markerId]: rating }))
  }

  /**
   * Update comment on a marker
   */
  const updateMarkerComment = (markerId, comment) => {
    setMarkerComments(prev => ({ ...prev, [markerId]: comment }))
  }

  /**
   * Regenerate understanding with user feedback
   */
  const regenerateUnderstanding = async () => {
    if (!understandingCorrection.trim()) {
      setError('Please provide corrections or clarifications to regenerate')
      return
    }

    setIsRegenerating(true)
    setError(null)
    setThinking('')
    setStage(STAGES.ANALYZING_NOTES)
    setProgress({ stage: 1, total: 9, label: 'Re-analyzing with your feedback...' })

    await streamWizardRequest(
      '/concepts/wizard/regenerate-understanding',
      {
        concept_name: conceptName,
        notes: notes,
        previous_understanding: notesUnderstanding,
        user_rating: 3,  // Default to neutral rating since we removed the UI
        user_correction: understandingCorrection,
        source_id: sourceId
      },
      {
        onThinking: (content) => {
          setThinking(prev => prev + content)
        },
        onComplete: (data) => {
          setQuestions(data.questions || [])
          // Support both new (gaps_tensions_questions) and old (potential_tensions) field names
          const gapsTensionsQuestionsRegen = data.gaps_tensions_questions || data.potential_tensions || []
          setStageData(prev => ({
            ...prev,
            stage1: {
              ...prev.stage1,
              questions: data.questions || [],
              notesAnalysis: data.notes_analysis || null,
              gapsTensionsQuestions: gapsTensionsQuestionsRegen
            }
          }))

          // Update prefilled answers
          const prefilledAnswers = []
          for (const q of (data.questions || [])) {
            if (q.prefilled && q.prefilled.value) {
              prefilledAnswers.push({
                question_id: q.id,
                selected_options: Array.isArray(q.prefilled.value) ? q.prefilled.value :
                                  (q.type === 'multiple_choice' || q.type === 'multi_select') ? [q.prefilled.value] : null,
                text_answer: q.type === 'open_ended' ? q.prefilled.value : null,
                prefilled_confidence: q.prefilled.confidence,
                prefilled_reasoning: q.prefilled.reasoning
              })
            }
          }

          // Update understanding
          const understanding = {
            summary: data.notes_analysis?.summary || 'Unable to extract summary.',
            preliminaryDefinition: data.notes_analysis?.preliminary_definition || null,
            keyInsights: data.notes_analysis?.key_insights || [],
            gapsTensionsQuestions: gapsTensionsQuestionsRegen,
            // Preserve or update genealogy from regeneration
            genealogy: data.genealogy || notesUnderstanding?.genealogy || {
              detected_influences: [],
              emergence_context: {},
              needs_probing: []
            },
            prefilledCount: prefilledAnswers.length,
            totalQuestions: (data.questions || []).length,
            confidenceLevels: prefilledAnswers.reduce((acc, p) => {
              const conf = p.prefilled_confidence || 'low'
              acc[conf] = (acc[conf] || 0) + 1
              return acc
            }, {}),
            regeneratedFromFeedback: true
          }
          setNotesUnderstanding(understanding)

          // Reset correction for next round
          setUnderstandingCorrection('')
          setIsRegenerating(false)

          setProgress({ stage: 2, total: 9, label: 'Validate my understanding' })
          setStage(STAGES.UNDERSTANDING_VALIDATION)
          setThinking('')
        }
      }
    )
  }

  /**
   * Set feedback for a specific key insight
   */
  const setInsightStatus = (index, status) => {
    setInsightFeedback(prev => ({
      ...prev,
      [index]: { ...prev[index], status }
    }))
  }

  /**
   * Set comment for a specific key insight
   */
  const setInsightComment = (index, comment) => {
    setInsightFeedback(prev => ({
      ...prev,
      [index]: { ...prev[index], comment }
    }))
  }

  /**
   * Toggle insight comment expansion
   */
  const toggleInsightComment = (index) => {
    setExpandedInsightComment(prev => ({
      ...prev,
      [index]: !prev[index]
    }))
  }

  /**
   * Set feedback for a specific tension
   */
  const setTensionStatus = (index, status) => {
    setTensionFeedback(prev => ({
      ...prev,
      [index]: { ...prev[index], status }
    }))
  }

  /**
   * Set comment for a specific tension
   */
  const setTensionComment = (index, comment) => {
    setTensionFeedback(prev => ({
      ...prev,
      [index]: { ...prev[index], comment }
    }))
  }

  /**
   * Regenerate a specific insight with feedback
   */
  const regenerateInsight = async (index) => {
    const insight = notesUnderstanding.keyInsights[index]
    const feedback = insightFeedback[index]

    if (!feedback?.comment?.trim()) {
      setError('Please add a comment explaining how to improve this insight')
      return
    }

    setIsRegenerating(true)
    setThinking('')

    await streamWizardRequest(
      '/concepts/wizard/regenerate-insight',
      {
        concept_name: conceptName,
        notes: notes,
        insight_index: index,
        current_insight: insight,
        feedback: feedback.comment,
        all_insights: notesUnderstanding.keyInsights
      },
      {
        onThinking: (content) => {
          setThinking(prev => prev + content)
        },
        onComplete: (data) => {
          // Update the specific insight
          const newInsights = [...notesUnderstanding.keyInsights]
          newInsights[index] = data.regenerated_insight
          setNotesUnderstanding(prev => ({
            ...prev,
            keyInsights: newInsights
          }))
          // Clear feedback for this insight
          setInsightFeedback(prev => {
            const updated = { ...prev }
            delete updated[index]
            return updated
          })
          setExpandedInsightComment(prev => ({ ...prev, [index]: false }))
          setIsRegenerating(false)
          setThinking('')
        }
      }
    )
  }

  /**
   * Generate additional tensions based on current understanding
   */
  const generateMoreTensions = async () => {
    setIsGeneratingTensions(true)
    setThinking('')

    // Get approved tensions to avoid duplicates
    const approvedTensions = notesUnderstanding.gapsTensionsQuestions
      .filter((_, i) => tensionFeedback[i]?.status === 'approved' || tensionFeedback[i]?.status === 'approved_with_comment')

    await streamWizardRequest(
      '/concepts/wizard/generate-tensions',
      {
        concept_name: conceptName,
        notes: notes,
        existing_tensions: notesUnderstanding.gapsTensionsQuestions,
        approved_tensions: approvedTensions,
        notes_analysis: notesUnderstanding
      },
      {
        onThinking: (content) => {
          setThinking(prev => prev + content)
        },
        onComplete: (data) => {
          // Append new tensions to existing ones
          const newTensions = data.generated_tensions || []
          setNotesUnderstanding(prev => ({
            ...prev,
            gapsTensionsQuestions: [...prev.gapsTensionsQuestions, ...newTensions]
          }))
          setIsGeneratingTensions(false)
          setThinking('')
        }
      }
    )
  }

  /**
   * Regenerate a specific tension using the comment as context
   */
  const regenerateTension = async (index) => {
    const tension = notesUnderstanding.gapsTensionsQuestions[index]
    const feedback = tensionFeedback[index]

    if (!feedback?.comment?.trim()) {
      setError('Please add a comment explaining how to improve this tension')
      return
    }

    setIsGeneratingTensions(true)
    setThinking('')

    const tensionText = typeof tension === 'string'
      ? tension
      : (tension.description || tension.tension || JSON.stringify(tension))

    await streamWizardRequest(
      '/concepts/wizard/regenerate-tension',
      {
        concept_name: conceptName,
        notes: notes,
        tension_index: index,
        current_tension: tensionText,
        feedback: feedback.comment,
        all_tensions: notesUnderstanding.gapsTensionsQuestions.map(t =>
          typeof t === 'string' ? t : (t.description || t.tension || JSON.stringify(t))
        )
      },
      {
        onThinking: (content) => {
          setThinking(prev => prev + content)
        },
        onComplete: (data) => {
          // Update the specific tension
          const newTensions = [...notesUnderstanding.gapsTensionsQuestions]
          newTensions[index] = data.regenerated_tension
          setNotesUnderstanding(prev => ({
            ...prev,
            gapsTensionsQuestions: newTensions
          }))
          // Clear feedback for this tension
          setTensionFeedback(prev => {
            const updated = { ...prev }
            delete updated[index]
            return updated
          })
          setExpandedTensionComment(prev => ({ ...prev, [index]: false }))
          setIsGeneratingTensions(false)
          setThinking('')
        }
      }
    )
  }

  // ==========================================================================
  // CARD TRANSFORMATION FUNCTIONS (Sharpen/Generalize/Radicalize/Historicize/Deepen)
  // ==========================================================================

  /**
   * Transform a card using one of the 5 transformation modes
   */
  const transformCard = async (cardId, cardType, mode, guidance = '') => {
    // Find the card to transform
    let card, setCards
    switch (cardType) {
      case 'hypothesis':
        card = hypothesisCards.find(c => c.id === cardId)
        setCards = setHypothesisCards
        break
      case 'genealogy':
        card = genealogyCards.find(c => c.id === cardId)
        setCards = setGenealogyCards
        break
      case 'differentiation':
        card = differentiationCards.find(c => c.id === cardId)
        setCards = setDifferentiationCards
        break
      default:
        console.error('Unknown card type:', cardType)
        return
    }

    if (!card) {
      console.error('Card not found:', cardId)
      return
    }

    setIsTransformingCard(cardId)
    setThinking('')

    await streamWizardRequest(
      '/concepts/wizard/transform-card',
      {
        card_id: cardId,
        card_type: cardType,
        card_content: card.content || card.connection || card.difference,
        mode: mode,
        guidance: guidance,
        notes_context: notes.slice(0, 2000),  // Truncate for context
        concept_name: conceptName
      },
      {
        onThinking: (content) => {
          setThinking(prev => prev + content)
        },
        onComplete: (data) => {
          // Update the card with transformed content
          setCards(prevCards => prevCards.map(c => {
            if (c.id === cardId) {
              const historyEntry = {
                mode,
                guidance,
                original: c.content || c.connection || c.difference,
                result: data.transformed_content,
                timestamp: new Date().toISOString()
              }
              return {
                ...c,
                content: data.transformed_content,
                connection: cardType === 'genealogy' ? data.transformed_content : c.connection,
                difference: cardType === 'differentiation' ? data.transformed_content : c.difference,
                transformation_history: [...(c.transformation_history || []), historyEntry]
              }
            }
            return c
          }))
          setIsTransformingCard(null)
          setThinking('')
        }
      }
    )
  }

  /**
   * Approve a card (mark as approved)
   */
  const approveCard = (cardId, cardType) => {
    const updateCardStatus = (prevCards) => prevCards.map(c =>
      c.id === cardId ? { ...c, status: 'approved' } : c
    )

    switch (cardType) {
      case 'hypothesis':
        setHypothesisCards(updateCardStatus)
        break
      case 'genealogy':
        setGenealogyCards(updateCardStatus)
        break
      case 'differentiation':
        setDifferentiationCards(updateCardStatus)
        break
    }
  }

  /**
   * Reject a card (mark as rejected)
   */
  const rejectCard = (cardId, cardType) => {
    const updateCardStatus = (prevCards) => prevCards.map(c =>
      c.id === cardId ? { ...c, status: 'rejected' } : c
    )

    switch (cardType) {
      case 'hypothesis':
        setHypothesisCards(updateCardStatus)
        break
      case 'genealogy':
        setGenealogyCards(updateCardStatus)
        break
      case 'differentiation':
        setDifferentiationCards(updateCardStatus)
        break
    }
  }

  /**
   * Accept all pending cards of a given type
   */
  const acceptAllCards = (cardType) => {
    const acceptAll = (prevCards) => prevCards.map(c =>
      c.status === 'pending' ? { ...c, status: 'approved' } : c
    )

    switch (cardType) {
      case 'hypothesis':
        setHypothesisCards(acceptAll)
        break
      case 'differentiation':
        setDifferentiationCards(acceptAll)
        break
      case 'all':
        setHypothesisCards(acceptAll)
        setDifferentiationCards(acceptAll)
        break
    }
  }

  // ==========================================================================
  // GENERATE OPTIONS FOR OPEN-ENDED QUESTIONS
  // ==========================================================================

  /**
   * Generate answer options for an open-ended question based on notes and context
   */
  const generateOptionsForQuestion = async (question) => {
    setIsGeneratingOptions(true)
    setGeneratedOptions([])
    setSelectedGeneratedOption(null)

    // Collect previous answers for context
    const previousAnswers = []
    for (const stage of ['stage1', 'stage2', 'stage3']) {
      if (stageData[stage]?.answers) {
        for (const ans of stageData[stage].answers) {
          previousAnswers.push({
            question_id: ans.question_id,
            question: ans.question || ans.question_id,
            answer: ans.text_answer || ans.selected_options?.join(', ') || ''
          })
        }
      }
    }

    try {
      const response = await fetch(`${API_URL}/concepts/wizard/generate-options`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          concept_name: conceptName,
          question_id: question.id,
          question_text: question.text,
          notes: notes,
          hypothesis_cards: hypothesisCards,
          differentiation_cards: differentiationCards,
          previous_answers: previousAnswers,
          notes_understanding: notesUnderstanding
        })
      })

      if (!response.ok) {
        throw new Error('Failed to generate options')
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            if (data === '[DONE]') continue

            try {
              const event = JSON.parse(data)
              if (event.type === 'options') {
                setGeneratedOptions(event.data || [])
              } else if (event.type === 'error') {
                const errMsg = typeof event.message === 'string'
                  ? event.message
                  : (event.message?.detail || JSON.stringify(event.message))
                setError(errMsg)
              }
            } catch (e) {
              // Ignore parse errors for partial data
            }
          }
        }
      }
    } catch (e) {
      console.error('Error generating options:', e)
      setError('Failed to generate options: ' + (e?.message || 'Unknown error'))
    } finally {
      setIsGeneratingOptions(false)
    }
  }

  /**
   * Toggle selection of a generated option (multi-select)
   */
  const selectGeneratedOption = (option) => {
    setSelectedGeneratedOptions(prev => {
      const isSelected = prev.includes(option.id)
      let newSelections
      if (isSelected) {
        // Deselect
        newSelections = prev.filter(id => id !== option.id)
      } else {
        // Add to selection
        newSelections = [...prev, option.id]
      }

      // Update text answer with all selected options
      const selectedContents = newSelections
        .map(id => generatedOptions.find(o => o.id === id)?.content)
        .filter(Boolean)
      setCurrentAnswer(prevAnswer => ({
        ...prevAnswer,
        textAnswer: selectedContents.join('\n\n---\n\n'),
        // Store the structured selections
        selectedGeneratedOptions: newSelections.map(id => {
          const opt = generatedOptions.find(o => o.id === id)
          return { id: opt?.id, content: opt?.content }
        })
      }))

      return newSelections
    })
  }

  /**
   * Transform a generated option using one of the 5 modes
   */
  const transformGeneratedOption = async (optionId, mode, guidance = '') => {
    const option = generatedOptions.find(o => o.id === optionId)
    if (!option) return

    setTransformingOptionId(optionId)

    try {
      const response = await fetch(`${API_URL}/concepts/wizard/transform-card`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          card_id: optionId,
          card_type: 'option',
          card_content: option.content,
          mode: mode,
          guidance: guidance,
          notes_context: notes?.slice(0, 2000),
          concept_name: conceptName
        })
      })

      if (!response.ok) {
        throw new Error('Failed to transform option')
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''
      let transformedContent = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            if (data === '[DONE]') continue

            try {
              const event = JSON.parse(data)
              if (event.type === 'text') {
                transformedContent += event.content
              } else if (event.type === 'complete') {
                transformedContent = event.data.transformed_content
              }
            } catch (e) {
              // Ignore parse errors
            }
          }
        }
      }

      // Update the option with transformed content
      if (transformedContent) {
        setGeneratedOptions(prev => prev.map(o => {
          if (o.id === optionId) {
            return {
              ...o,
              content: transformedContent,
              transformation_history: [...(o.transformation_history || []), { mode, original: option.content }]
            }
          }
          return o
        }))

        // Update text answer if this option was among the selected options
        if (selectedGeneratedOptions.includes(optionId)) {
          // Rebuild the combined text answer with the transformed content
          setCurrentAnswer(prev => {
            const selectedContents = selectedGeneratedOptions
              .map(id => {
                if (id === optionId) return transformedContent
                return generatedOptions.find(o => o.id === id)?.content
              })
              .filter(Boolean)
            return {
              ...prev,
              textAnswer: selectedContents.join('\n\n---\n\n'),
              selectedGeneratedOptions: prev.selectedGeneratedOptions?.map(opt =>
                opt.id === optionId ? { ...opt, content: transformedContent } : opt
              )
            }
          })
        }
      }
    } catch (e) {
      console.error('Error transforming option:', e)
      setError('Failed to transform option: ' + (e?.message || 'Unknown error'))
    } finally {
      setTransformingOptionId(null)
    }
  }

  // Clear generated options and auto-generate for OPEN questions
  useEffect(() => {
    // Clear previous options
    setGeneratedOptions([])
    setSelectedGeneratedOptions([])
    setGeneratedOptionsComment('')
    setHasAutoGeneratedForQuestion(null)

    // Auto-generate options for OPEN type questions
    const currentQ = questions[currentQuestionIndex]
    if (currentQ && currentQ.type === QUESTION_TYPES.OPEN &&
        (stage === STAGES.STAGE1 || stage === STAGES.STAGE2 || stage === STAGES.STAGE3)) {
      // Auto-generate after a small delay to let the UI settle
      const timer = setTimeout(() => {
        if (hasAutoGeneratedForQuestion !== currentQ.id) {
          setHasAutoGeneratedForQuestion(currentQ.id)
          generateOptionsForQuestion(currentQ)
        }
      }, 300)
      return () => clearTimeout(timer)
    }
  }, [currentQuestionIndex, questions, stage])

  // ==========================================================================
  // INTELLECTUAL GENEALOGY
  // ==========================================================================

  /**
   * Generate intellectual genealogy hypotheses based on all previous responses
   */
  const generateGenealogy = async () => {
    setIsGeneratingGenealogy(true)
    setGenealogyHypotheses([])
    setThinking('')

    try {
      const response = await fetch(`${API_URL}/concepts/wizard/generate-genealogy`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          concept_name: conceptName,
          notes: notes,
          hypothesis_cards: hypothesisCards,
          differentiation_cards: differentiationCards,
          stage1_answers: stageData.stage1?.answers || [],
          stage2_answers: stageData.stage2?.answers || [],
          stage3_answers: stageData.stage3?.answers || [],
          notes_understanding: notesUnderstanding
        })
      })

      if (!response.ok) {
        throw new Error('Failed to generate genealogy')
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            if (data === '[DONE]') continue

            try {
              const event = JSON.parse(data)
              if (event.type === 'genealogy') {
                // Add status: 'pending' to each hypothesis
                const hypothesesWithStatus = (event.data || []).map(h => ({
                  ...h,
                  status: 'pending'
                }))
                setGenealogyHypotheses(hypothesesWithStatus)
              } else if (event.type === 'status') {
                setThinking(event.message)
              } else if (event.type === 'error') {
                const errMsg = typeof event.message === 'string'
                  ? event.message
                  : (event.message?.detail || JSON.stringify(event.message))
                setError(errMsg)
              }
            } catch (e) {
              // Ignore parse errors
            }
          }
        }
      }
    } catch (e) {
      console.error('Error generating genealogy:', e)
      setError('Failed to generate genealogy: ' + (e?.message || 'Unknown error'))
    } finally {
      setIsGeneratingGenealogy(false)
      setThinking('')
    }
  }

  /**
   * Approve/reject a genealogy hypothesis
   */
  const updateGenealogyStatus = (hypothesisId, status) => {
    setGenealogyHypotheses(prev => prev.map(h =>
      h.id === hypothesisId ? { ...h, status } : h
    ))
  }

  /**
   * Add a user-specified influence
   */
  const addUserInfluence = () => {
    if (!newInfluenceInput.name.trim()) return

    const newInfluence = {
      id: `user_${Date.now()}`,
      type: newInfluenceInput.type,
      name: newInfluenceInput.name.trim(),
      connection: newInfluenceInput.connection.trim(),
      confidence: 'user_added',
      status: 'approved',
      is_user_added: true
    }

    setUserAddedInfluences(prev => [...prev, newInfluence])
    setNewInfluenceInput({ name: '', type: 'thinker', connection: '' })
  }

  /**
   * Remove a user-added influence
   */
  const removeUserInfluence = (influenceId) => {
    setUserAddedInfluences(prev => prev.filter(i => i.id !== influenceId))
  }

  /**
   * Proceed from genealogy to deep commitments
   */
  const proceedFromGenealogy = async () => {
    // Collect approved genealogy (both generated and user-added)
    const approvedGenealogy = [
      ...genealogyHypotheses.filter(h => h.status === 'approved'),
      ...userAddedInfluences
    ]

    // Store in stage data
    setStageData(prev => ({
      ...prev,
      genealogy: approvedGenealogy
    }))

    // Generate deep commitment questions (will transition to DEEP_COMMITMENTS when done)
    await generateDeepCommitments()
  }

  /**
   * Handle document file selection
   */
  const handleFileSelect = (event) => {
    const file = event.target.files[0]
    if (file) {
      // Validate file type
      const validTypes = ['application/pdf', 'text/plain', 'text/markdown']
      const validExtensions = ['.pdf', '.txt', '.md', '.markdown']
      const hasValidExt = validExtensions.some(ext => file.name.toLowerCase().endsWith(ext))

      if (!validTypes.includes(file.type) && !hasValidExt) {
        setError('Please upload a PDF, TXT, or Markdown file')
        return
      }

      // Validate file size (max 50MB)
      if (file.size > 50 * 1024 * 1024) {
        setError('File too large. Maximum size is 50MB.')
        return
      }

      setSelectedFile(file)
      setError(null)
    }
  }

  /**
   * Upload and analyze a document using Sonnet 4.5 with 1M token context
   */
  const uploadAndAnalyzeDocument = async () => {
    if (!selectedFile) {
      setError('Please select a file first')
      return
    }

    setIsUploadingDocument(true)
    setError(null)
    setThinking('')
    setDocumentAnalysisProgress('Starting analysis...')

    try {
      const formData = new FormData()
      formData.append('file', selectedFile)
      formData.append('concept_name', conceptName)
      formData.append('existing_context', JSON.stringify({
        notes_summary: notesUnderstanding?.summary || notes,
        genealogy: notesUnderstanding?.genealogy || {},
        preliminary_definition: notesUnderstanding?.preliminaryDefinition || '',
        previous_extractions: dimensionalExtraction
      }))

      const response = await fetch(`${API_URL}/concepts/wizard/analyze-document`, {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`)
      }

      // Handle SSE stream
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''
      let fullText = ''
      let extractedData = null

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            if (data === '[DONE]') continue

            try {
              const parsed = JSON.parse(data)
              if (parsed.type === 'status') {
                setDocumentAnalysisProgress(parsed.message)
              } else if (parsed.type === 'text') {
                fullText += parsed.content
                setThinking(prev => prev + parsed.content)
              } else if (parsed.type === 'complete') {
                extractedData = parsed.data
              } else if (parsed.type === 'error') {
                throw new Error(parsed.message)
              }
            } catch (e) {
              if (e.message.includes('Upload failed')) throw e
            }
          }
        }
      }

      // Store the extracted dimensional data
      if (extractedData) {
        // Merge with existing extractions
        setDimensionalExtraction(prev => {
          if (!prev) return extractedData
          // Merge arrays, prefer newer data
          return {
            quinean: { ...prev.quinean, ...extractedData.quinean },
            sellarsian: { ...prev.sellarsian, ...extractedData.sellarsian },
            brandomian: { ...prev.brandomian, ...extractedData.brandomian },
            deleuzian: { ...prev.deleuzian, ...extractedData.deleuzian },
            bachelardian: { ...prev.bachelardian, ...extractedData.bachelardian },
            canguilhem: { ...prev.canguilhem, ...extractedData.canguilhem },
            davidson: { ...prev.davidson, ...extractedData.davidson },
            blumenberg: { ...prev.blumenberg, ...extractedData.blumenberg },
            carey: { ...prev.carey, ...extractedData.carey },
            document_summary: extractedData.document_summary,
            key_excerpts: [...(prev.key_excerpts || []), ...(extractedData.key_excerpts || [])]
          }
        })

        // Record the uploaded document
        setUploadedDocuments(prev => [...prev, {
          name: selectedFile.name,
          size: selectedFile.size,
          uploadedAt: new Date().toISOString(),
          summary: extractedData.document_summary || 'Analysis complete'
        }])
      }

      setSelectedFile(null)
      setDocumentAnalysisProgress(null)
      setThinking('')

    } catch (error) {
      const errorMsg = typeof error === 'string' ? error : (error?.message || JSON.stringify(error))
      setError(errorMsg)
    } finally {
      setIsUploadingDocument(false)
    }
  }

  /**
   * Convert approved hypothesis cards to Stage 1 "answers" format
   * This allows us to skip Stage 1 generic questions when cards are validated
   */
  const convertCardsToAnswers = () => {
    const answers = []

    // Convert approved hypothesis cards to answers
    hypothesisCards
      .filter(c => c.status === 'approved')
      .forEach(card => {
        answers.push({
          question_id: `hypothesis_${card.id}`,
          text_answer: card.content,
          card_type: card.type || 'thesis',
          source: 'validated_card'
        })
      })

    // Convert approved differentiation cards to answers
    differentiationCards
      .filter(c => c.status === 'approved')
      .forEach(card => {
        answers.push({
          question_id: `differentiation_${card.id}`,
          text_answer: `NOT ${card.contrasted_with}: ${card.difference}`,
          card_type: 'differentiation',
          source: 'validated_card'
        })
      })

    return answers
  }

  /**
   * Proceed with validated cards - skip Stage 1 generic questions
   */
  const proceedWithValidatedCards = async () => {
    // Check if we have any approved cards
    const approvedHypotheses = hypothesisCards.filter(c => c.status === 'approved')
    const approvedDifferentiations = differentiationCards.filter(c => c.status === 'approved')

    if (approvedHypotheses.length === 0 && approvedDifferentiations.length === 0) {
      // No cards approved - fall back to Stage 1 questions
      setProgress({ stage: 3, total: 11, label: 'Stage 1: Genesis & Problem Space' })
      setStage(STAGES.STAGE1)
      setCurrentQuestionIndex(0)
      return
    }

    // Convert approved cards to answers format
    const cardAnswers = convertCardsToAnswers()

    // Store as Stage 1 answers and proceed to analysis
    setStageData(prev => ({
      ...prev,
      stage1: {
        ...prev.stage1,
        answers: cardAnswers,
        skippedGenericQuestions: true
      }
    }))

    // Go directly to Stage 1 analysis (which generates Stage 2)
    await analyzeStage1(cardAnswers)
  }

  /**
   * Skip document upload and continue with validated cards
   */
  const skipDocumentUpload = () => {
    proceedWithValidatedCards()
  }

  /**
   * Continue from document upload with validated cards
   */
  const continueFromDocumentUpload = () => {
    proceedWithValidatedCards()
  }

  /**
   * Generate Deep Commitment questions (all 9 philosophical dimensions)
   * Called after Stage 3 when enough context has accumulated
   */
  const generateDeepCommitments = async () => {
    setIsGeneratingCommitments(true)
    setStage(STAGES.ANALYZING_COMMITMENTS)
    setProgress({ stage: 9, total: 11, label: 'Generating philosophical dimension questions...' })
    setThinking('')
    setError(null)

    try {
      const response = await fetch(`${API_URL}/concepts/wizard/generate-deep-commitments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          concept_name: conceptName,
          notes_summary: notesUnderstanding?.summary || notes,
          genealogy: notesUnderstanding?.genealogy || {},
          user_approved_genealogy: stageData.genealogy || genealogyHypotheses.filter(h => h.status === 'approved'),
          stage1_answers: stageData.stage1?.answers || [],
          stage2_answers: stageData.stage2?.answers || [],
          dimensional_extraction: dimensionalExtraction
        })
      })

      if (!response.ok) {
        throw new Error(`Request failed: ${response.statusText}`)
      }

      // Handle SSE stream
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''
      let questionsData = null

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            if (data === '[DONE]') continue

            try {
              const parsed = JSON.parse(data)
              if (parsed.type === 'thinking') {
                setThinking(prev => prev + parsed.content)
              } else if (parsed.type === 'text') {
                setThinking(prev => prev + parsed.content)
              } else if (parsed.type === 'complete') {
                questionsData = parsed.data
              } else if (parsed.type === 'error') {
                throw new Error(parsed.message)
              }
            } catch (e) {
              if (e.message.includes('Request failed')) throw e
            }
          }
        }
      }

      if (questionsData?.deep_commitment_questions) {
        setDeepCommitmentQuestions(questionsData.deep_commitment_questions)
        setCurrentCommitmentIndex(0)
        setProgress({ stage: 9, total: 11, label: 'Deep Commitments: Philosophical Dimensions' })
        setStage(STAGES.DEEP_COMMITMENTS)
      } else {
        // No questions generated, skip to finalization
        setProgress({ stage: 10, total: 11, label: 'Final synthesis...' })
        setStage(STAGES.PROCESSING)
      }

    } catch (error) {
      const errorMsg = typeof error === 'string' ? error : (error?.message || JSON.stringify(error))
      setError(errorMsg)
      setStage(STAGES.STAGE3)  // Go back to Stage 3 on error
    } finally {
      setIsGeneratingCommitments(false)
      setThinking('')
    }
  }

  /**
   * Answer a deep commitment question
   */
  const answerCommitmentQuestion = (questionId, selected, comment = '') => {
    setDeepCommitmentAnswers(prev => ({
      ...prev,
      [questionId]: { selected, comment }
    }))
  }

  /**
   * Move to next commitment question (Phase 1) or go to Phase 2
   */
  const nextCommitmentQuestion = () => {
    if (currentCommitmentIndex < deepCommitmentQuestions.length - 1) {
      setCurrentCommitmentIndex(prev => prev + 1)
    } else {
      // Done with Phase 1 - generate Phase 2 questions
      generatePhase2Questions()
    }
  }

  /**
   * Move to previous commitment question (Phase 1)
   */
  const prevCommitmentQuestion = () => {
    if (currentCommitmentIndex > 0) {
      setCurrentCommitmentIndex(prev => prev - 1)
    }
  }

  /**
   * Generate Phase 2 follow-up questions based on Phase 1 answers
   */
  const generatePhase2Questions = async () => {
    setIsGeneratingPhase2(true)
    setStage(STAGES.GENERATING_PHASE2)
    setProgress({ stage: 10, total: 13, label: 'Generating targeted follow-up questions...' })
    setThinking('')

    try {
      const response = await fetch(`${API_URL}/concepts/wizard/generate-phase2-questions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          concept_name: conceptName,
          notes_summary: notesUnderstanding?.summary || notes,
          phase1_questions: deepCommitmentQuestions,
          phase1_answers: deepCommitmentAnswers,
          stage1_answers: stageData.stage1?.answers || [],
          stage2_answers: stageData.stage2?.answers || [],
          stage3_answers: stageData.stage3?.answers || [],
          genealogy: stageData.genealogy || genealogyHypotheses.filter(h => h.status === 'approved'),
          dimensional_extraction: dimensionalExtraction
        })
      })

      if (!response.ok) {
        throw new Error(`Request failed: ${response.statusText}`)
      }

      // Handle SSE stream
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''
      let questionsData = null

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            if (data === '[DONE]') continue

            try {
              const parsed = JSON.parse(data)
              if (parsed.type === 'thinking') {
                setThinking(prev => prev + parsed.content)
              } else if (parsed.type === 'complete') {
                questionsData = parsed.data
              } else if (parsed.type === 'error') {
                throw new Error(parsed.message)
              }
            } catch (e) {
              if (e.message.includes('Request failed')) throw e
            }
          }
        }
      }

      if (questionsData?.questions && questionsData.questions.length > 0) {
        setPhase2Questions(questionsData.questions)
        setCurrentPhase2Index(0)
        setProgress({ stage: 10, total: 13, label: 'Phase 2: Targeted Follow-ups' })
        setStage(STAGES.DEEP_COMMITMENTS_PHASE2)
      } else {
        // No Phase 2 questions generated, go to Phase 3
        generatePhase3Questions()
      }

    } catch (error) {
      const errorMsg = typeof error === 'string' ? error : (error?.message || JSON.stringify(error))
      setError(errorMsg)
      setStage(STAGES.DEEP_COMMITMENTS)  // Go back to Phase 1 on error
    } finally {
      setIsGeneratingPhase2(false)
      setThinking('')
    }
  }

  /**
   * Answer a Phase 2 question
   */
  const answerPhase2Question = (questionId, selected, comment = '') => {
    setPhase2Answers(prev => ({
      ...prev,
      [questionId]: { selected, comment }
    }))
  }

  /**
   * Move to next Phase 2 question or go to Phase 3
   */
  const nextPhase2Question = () => {
    if (currentPhase2Index < phase2Questions.length - 1) {
      setCurrentPhase2Index(prev => prev + 1)
    } else {
      // Done with Phase 2 - generate Phase 3 questions
      generatePhase3Questions()
    }
  }

  /**
   * Move to previous Phase 2 question
   */
  const prevPhase2Question = () => {
    if (currentPhase2Index > 0) {
      setCurrentPhase2Index(prev => prev - 1)
    }
  }

  /**
   * Generate Phase 3 synthesis/verification questions
   */
  const generatePhase3Questions = async () => {
    setIsGeneratingPhase3(true)
    setStage(STAGES.GENERATING_PHASE3)
    setProgress({ stage: 11, total: 13, label: 'Generating final synthesis questions...' })
    setThinking('')

    try {
      const response = await fetch(`${API_URL}/concepts/wizard/generate-phase3-questions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          concept_name: conceptName,
          notes_summary: notesUnderstanding?.summary || notes,
          phase1_questions: deepCommitmentQuestions,
          phase1_answers: deepCommitmentAnswers,
          phase2_questions: phase2Questions,
          phase2_answers: phase2Answers,
          stage1_answers: stageData.stage1?.answers || [],
          stage2_answers: stageData.stage2?.answers || [],
          stage3_answers: stageData.stage3?.answers || [],
          genealogy: stageData.genealogy || genealogyHypotheses.filter(h => h.status === 'approved'),
          dimensional_extraction: dimensionalExtraction
        })
      })

      if (!response.ok) {
        throw new Error(`Request failed: ${response.statusText}`)
      }

      // Handle SSE stream
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''
      let questionsData = null

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            if (data === '[DONE]') continue

            try {
              const parsed = JSON.parse(data)
              if (parsed.type === 'thinking') {
                setThinking(prev => prev + parsed.content)
              } else if (parsed.type === 'complete') {
                questionsData = parsed.data
              } else if (parsed.type === 'error') {
                throw new Error(parsed.message)
              }
            } catch (e) {
              if (e.message.includes('Request failed')) throw e
            }
          }
        }
      }

      if (questionsData?.questions && questionsData.questions.length > 0) {
        setPhase3Questions(questionsData.questions)
        setCurrentPhase3Index(0)
        setProgress({ stage: 11, total: 13, label: 'Phase 3: Final Synthesis' })
        setStage(STAGES.DEEP_COMMITMENTS_PHASE3)
      } else {
        // No Phase 3 questions generated, proceed to finalization
        finalizeWithCommitments()
      }

    } catch (error) {
      const errorMsg = typeof error === 'string' ? error : (error?.message || JSON.stringify(error))
      setError(errorMsg)
      setStage(STAGES.DEEP_COMMITMENTS_PHASE2)  // Go back to Phase 2 on error
    } finally {
      setIsGeneratingPhase3(false)
      setThinking('')
    }
  }

  /**
   * Answer a Phase 3 question
   */
  const answerPhase3Question = (questionId, selected, comment = '') => {
    setPhase3Answers(prev => ({
      ...prev,
      [questionId]: { selected, comment }
    }))
  }

  /**
   * Move to next Phase 3 question or finalize
   */
  const nextPhase3Question = () => {
    if (currentPhase3Index < phase3Questions.length - 1) {
      setCurrentPhase3Index(prev => prev + 1)
    } else {
      // Done with all phases - finalize
      finalizeWithCommitments()
    }
  }

  /**
   * Move to previous Phase 3 question
   */
  const prevPhase3Question = () => {
    if (currentPhase3Index > 0) {
      setCurrentPhase3Index(prev => prev - 1)
    }
  }

  /**
   * Finalize concept including all philosophical commitment answers
   */
  const finalizeWithCommitments = async () => {
    setStage(STAGES.PROCESSING)
    setProgress({ stage: 12, total: 13, label: 'Final synthesis with all dimensions...' })
    // Pass all answers to finalization
    await finalizeConceptWorkflowWithCommitments(stageData.stage3?.answers || [])
  }

  /**
   * Final synthesis with deep commitment answers included
   */
  const finalizeConceptWorkflowWithCommitments = async (stage3Answers) => {
    // Build validated cases from user ratings
    const validatedCases = generatedCases
      .filter(c => caseRatings[c.id] === 'good' || caseRatings[c.id] === 'partial')
      .map(c => ({
        ...c,
        rating: caseRatings[c.id],
        comment: caseComments[c.id] || ''
      }))

    // Build validated markers from user ratings
    const validatedMarkers = generatedMarkers
      .filter(m => markerRatings[m.id] === 'good' || markerRatings[m.id] === 'partial')
      .map(m => ({
        ...m,
        rating: markerRatings[m.id],
        comment: markerComments[m.id] || ''
      }))

    // Build approved tensions from understanding validation
    const approvedTensions = (notesUnderstanding?.gapsTensionsQuestions || [])
      .filter((_, i) => {
        const feedback = tensionFeedback[i]
        return feedback?.status === 'approved' || feedback?.status === 'approved_with_comment'
      })
      .map((tension, i) => {
        const feedback = tensionFeedback[i] || {}
        const tensionObj = typeof tension === 'string' ? { description: tension } : tension
        return {
          ...tensionObj,
          comment: feedback.comment || ''
        }
      })

    await streamWizardRequest(
      '/concepts/wizard/finalize',
      {
        concept_name: conceptName,
        notes: notes.trim() || null,
        all_answers: {
          stage1: stageData.stage1.answers,
          stage2: stageData.stage2.answers,
          stage3: stage3Answers,
          deep_commitments_phase1: deepCommitmentAnswers,
          deep_commitments_phase2: phase2Answers,
          deep_commitments_phase3: phase3Answers
        },
        interim_analysis: interimAnalysis,
        dialectics: dialectics,
        validated_cases: validatedCases.length > 0 ? validatedCases : null,
        validated_markers: validatedMarkers.length > 0 ? validatedMarkers : null,
        approved_tensions: approvedTensions.length > 0 ? approvedTensions : null,
        dimensional_extraction: dimensionalExtraction,  // Include document extraction data
        source_id: sourceId
      },
      {
        onThinking: (content) => {
          setThinking(prev => prev + content)
        },
        onComplete: (data) => {
          setConceptData(data.concept)
          // Populate editable draft from concept data, including validated data
          populateEditableDraft(data.concept, validatedCases, validatedMarkers, approvedTensions)
          setProgress({ stage: 13, total: 13, label: 'Complete!' })
          setStage(STAGES.COMPLETE)
        }
      }
    )
  }

  /**
   * Build AnswerWithMeta object from current answer state
   */
  const buildAnswerMeta = (questionId) => {
    // For case/marker questions, include the rated items
    let validatedCasesData = null
    let validatedMarkersData = null

    if (questionId === 'paradigmatic_case' || questionId?.includes('case')) {
      const rated = generatedCases.filter(c =>
        caseRatings[c.id] === 'good' || caseRatings[c.id] === 'partial'
      )
      if (rated.length > 0) {
        validatedCasesData = rated.map(c => ({
          ...c,
          rating: caseRatings[c.id],
          comment: caseComments[c.id] || null
        }))
      }
    }

    if (questionId === 'recognition_markers' || questionId?.includes('marker') || questionId?.includes('recognition')) {
      const rated = generatedMarkers.filter(m =>
        markerRatings[m.id] === 'good' || markerRatings[m.id] === 'partial'
      )
      if (rated.length > 0) {
        validatedMarkersData = rated.map(m => ({
          ...m,
          rating: markerRatings[m.id],
          comment: markerComments[m.id] || null
        }))
      }
    }

    return {
      question_id: questionId,
      selected_options: currentAnswer.selectedOptions.length > 0 ? currentAnswer.selectedOptions : null,
      text_answer: currentAnswer.textAnswer || null,
      custom_response: currentAnswer.customResponse || null,
      custom_response_category: currentAnswer.customCategory,
      is_dialectic: currentAnswer.isDialectic,
      dialectic_pole_a: currentAnswer.dialecticPoleA || null,
      dialectic_pole_b: currentAnswer.dialecticPoleB || null,
      dialectic_note: currentAnswer.dialecticNote || null,
      option_comments: Object.keys(currentAnswer.optionComments).length > 0 ? currentAnswer.optionComments : null,
      // Include validated cases/markers for Stage 3 questions
      validated_cases: validatedCasesData,
      validated_markers: validatedMarkersData
    }
  }

  /**
   * Toggle option comment expansion
   */
  const toggleOptionComment = (optionValue) => {
    setExpandedComments(prev => ({
      ...prev,
      [optionValue]: !prev[optionValue]
    }))
  }

  /**
   * Update option comment
   */
  const updateOptionComment = (optionValue, comment) => {
    setCurrentAnswer(prev => ({
      ...prev,
      optionComments: {
        ...prev.optionComments,
        [optionValue]: comment
      }
    }))
  }

  /**
   * Submit answer to current question
   */
  const submitAnswer = async () => {
    const currentQ = questions[currentQuestionIndex]
    if (!currentQ) return

    // Build the answer
    const answerMeta = buildAnswerMeta(currentQ.id)

    // Validate - need at least one of:
    // - selected options
    // - text answer
    // - custom response
    // - validated cases (for case questions)
    // - validated markers (for marker questions)
    const hasAnswer = (answerMeta.selected_options?.length > 0) ||
                      answerMeta.text_answer ||
                      answerMeta.custom_response ||
                      answerMeta.validated_cases?.length > 0 ||
                      answerMeta.validated_markers?.length > 0

    if (!hasAnswer && currentQ.required !== false) {
      setError('Please provide an answer (select options, rate generated items, or type your answer)')
      return
    }

    setError(null)

    // Track dialectics
    if (currentAnswer.isDialectic && currentAnswer.dialecticPoleA && currentAnswer.dialecticPoleB) {
      setDialectics(prev => [...prev, {
        description: `Tension in ${currentQ.id}`,
        pole_a: currentAnswer.dialecticPoleA,
        pole_b: currentAnswer.dialecticPoleB,
        marked_as_dialectic: true,
        user_note: currentAnswer.dialecticNote
      }])
    }

    // Determine which stage we're in and update appropriately
    const currentStageName = stage === STAGES.STAGE1 ? 'stage1' :
                            stage === STAGES.STAGE2 ? 'stage2' : 'stage3'

    setStageData(prev => ({
      ...prev,
      [currentStageName]: {
        ...prev[currentStageName],
        answers: [...prev[currentStageName].answers, answerMeta]
      }
    }))

    resetCurrentAnswer()

    // Move to next question or next stage
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
      const stageNum = stage === STAGES.STAGE1 ? 1 : stage === STAGES.STAGE2 ? 2 : 3
      setProgress({
        stage: stageNum + 2,  // +2 because of understanding validation stage
        total: 9,
        label: `Stage ${stageNum}: Question ${currentQuestionIndex + 2} of ${questions.length}`
      })
    } else {
      // Stage complete - move to analysis
      const answers = [...stageData[currentStageName].answers, answerMeta]

      if (stage === STAGES.STAGE1) {
        await analyzeStage1(answers)
      } else if (stage === STAGES.STAGE2) {
        await analyzeStage2(answers)
      } else if (stage === STAGES.STAGE3) {
        // Store Stage 3 answers, then go to Genealogy
        setStageData(prev => ({
          ...prev,
          stage3: { ...prev.stage3, answers: answers }
        }))
        // Go to Intellectual Genealogy stage (Stage 8)
        setStage(STAGES.GENEALOGY)
        setProgress({ stage: 8, total: 11, label: 'Intellectual Genealogy' })
      }
    }
  }

  /**
   * Analyze Stage 1 answers and get Stage 2 questions
   */
  const analyzeStage1 = async (answers) => {
    setStage(STAGES.ANALYZING_STAGE1)
    setProgress({ stage: 4, total: 9, label: 'Analyzing your answers...' })

    // Collect approved tensions from notes preprocessing (Validate Understanding stage)
    // These will be passed so the Interim Analysis can identify NEW tensions
    const approvedTensionsFromNotes = (notesUnderstanding?.gapsTensionsQuestions || [])
      .map((t, i) => {
        const feedback = tensionFeedback[i]
        if (feedback?.status === 'approved' || feedback?.status === 'approved_with_comment') {
          return typeof t === 'string' ? t : (t.description || t.pole_a + ' vs ' + t.pole_b)
        }
        return null
      })
      .filter(Boolean)

    await streamWizardRequest(
      '/concepts/wizard/analyze-stage1',
      {
        concept_name: conceptName,
        notes: notes.trim() || null,
        answers: answers,
        source_id: sourceId,
        approved_tensions_from_notes: approvedTensionsFromNotes.length > 0 ? approvedTensionsFromNotes : null
      },
      {
        onThinking: (content) => {
          setThinking(prev => prev + content)
        },
        onPhase: (phase) => {
          if (phase === 'interim_analysis') {
            setProgress({ stage: 4, total: 9, label: 'Building interim understanding...' })
          } else if (phase === 'stage2_generation') {
            setProgress({ stage: 5, total: 9, label: 'Generating Stage 2 questions...' })
          }
        },
        onInterimComplete: (interim) => {
          setInterimAnalysis(interim)
        },
        onComplete: (data) => {
          // Store Stage 1 final data
          setStageData(prev => ({
            ...prev,
            stage1: { ...prev.stage1, answers: answers }
          }))

          // Set up for interim display
          setInterimAnalysis(data.interim_analysis)

          // Prepare Stage 2 questions
          setStageData(prev => ({
            ...prev,
            stage2: { questions: data.questions || [], answers: [] }
          }))

          // Show interim analysis first
          setProgress({ stage: 5, total: 9, label: 'Review interim analysis' })
          setStage(STAGES.INTERIM_ANALYSIS)
        }
      }
    )
  }

  /**
   * Continue from interim analysis to Stage 2
   */
  const continueToStage2 = () => {
    setQuestions(stageData.stage2.questions)
    setCurrentQuestionIndex(0)
    resetCurrentAnswer()
    setProgress({ stage: 6, total: 9, label: 'Stage 2: Differentiation & Clarification' })
    setStage(STAGES.STAGE2)
  }

  /**
   * Analyze Stage 2 answers and get implications preview
   */
  const analyzeStage2 = async (answers) => {
    setStage(STAGES.ANALYZING_STAGE2)
    setProgress({ stage: 6, total: 9, label: 'Analyzing differentiations...' })

    await streamWizardRequest(
      '/concepts/wizard/analyze-stage2',
      {
        concept_name: conceptName,
        notes: notes.trim() || null,
        stage1_answers: stageData.stage1.answers,
        stage2_answers: answers,
        interim_analysis: interimAnalysis,
        source_id: sourceId
      },
      {
        onThinking: (content) => {
          setThinking(prev => prev + content)
        },
        onComplete: (data) => {
          // Store Stage 2 final data
          setStageData(prev => ({
            ...prev,
            stage2: { ...prev.stage2, answers: answers },
            stage3: { questions: data.questions || [], answers: [] }
          }))

          // Set implications preview
          setImplicationsPreview(data.implications_preview)

          // Show implications preview
          setProgress({ stage: 7, total: 9, label: 'Review implications' })
          setStage(STAGES.IMPLICATIONS_PREVIEW)
        }
      }
    )
  }

  /**
   * Continue from implications preview to Stage 3
   */
  const continueToStage3 = () => {
    setQuestions(stageData.stage3.questions)
    setCurrentQuestionIndex(0)
    resetCurrentAnswer()
    setProgress({ stage: 8, total: 9, label: 'Stage 3: Grounding & Recognition' })
    setStage(STAGES.STAGE3)
  }

  /**
   * Final synthesis
   */
  const finalizeConceptWorkflow = async (stage3Answers) => {
    setStage(STAGES.PROCESSING)
    setProgress({ stage: 9, total: 9, label: 'Creating final concept definition...' })

    // Build validated cases from user ratings
    const validatedCases = generatedCases
      .filter(c => caseRatings[c.id] === 'good' || caseRatings[c.id] === 'partial')
      .map(c => ({
        ...c,
        rating: caseRatings[c.id],
        comment: caseComments[c.id] || ''
      }))

    // Build validated markers from user ratings
    const validatedMarkers = generatedMarkers
      .filter(m => markerRatings[m.id] === 'good' || markerRatings[m.id] === 'partial')
      .map(m => ({
        ...m,
        rating: markerRatings[m.id],
        comment: markerComments[m.id] || ''
      }))

    // Build approved tensions from understanding validation
    const approvedTensions = (notesUnderstanding?.gapsTensionsQuestions || [])
      .filter((_, i) => {
        const feedback = tensionFeedback[i]
        return feedback?.status === 'approved' || feedback?.status === 'approved_with_comment'
      })
      .map((tension, i) => {
        const feedback = tensionFeedback[i] || {}
        const tensionObj = typeof tension === 'string' ? { description: tension } : tension
        return {
          ...tensionObj,
          comment: feedback.comment || ''
        }
      })

    await streamWizardRequest(
      '/concepts/wizard/finalize',
      {
        concept_name: conceptName,
        notes: notes.trim() || null,
        all_answers: {
          stage1: stageData.stage1.answers,
          stage2: stageData.stage2.answers,
          stage3: stage3Answers
        },
        interim_analysis: interimAnalysis,
        dialectics: dialectics,
        validated_cases: validatedCases.length > 0 ? validatedCases : null,
        validated_markers: validatedMarkers.length > 0 ? validatedMarkers : null,
        approved_tensions: approvedTensions.length > 0 ? approvedTensions : null,
        source_id: sourceId
      },
      {
        onThinking: (content) => {
          setThinking(prev => prev + content)
        },
        onComplete: (data) => {
          setConceptData(data.concept)
          // Populate editable draft from concept data, including validated data
          populateEditableDraft(data.concept, validatedCases, validatedMarkers, approvedTensions)
          setProgress({ stage: 9, total: 9, label: 'Complete!' })
          setStage(STAGES.COMPLETE)
        }
      }
    )
  }

  /**
   * Populate editable draft from concept data
   * Uses validated data as fallbacks if LLM response is empty or malformed
   */
  const populateEditableDraft = (concept, validatedCases = [], validatedMarkers = [], approvedTensions = []) => {
    console.log('[populateEditableDraft] Concept data:', concept)
    console.log('[populateEditableDraft] Validated cases:', validatedCases)
    console.log('[populateEditableDraft] Validated markers:', validatedMarkers)
    console.log('[populateEditableDraft] Approved tensions:', approvedTensions)

    // PARADIGMATIC CASES - handle various formats
    let cases = []
    // Try paradigmatic_cases (array) first
    if (Array.isArray(concept.paradigmatic_cases) && concept.paradigmatic_cases.length > 0) {
      cases = concept.paradigmatic_cases.map(c => ({
        title: c.title || c.name || '',
        description: c.description || '',
        relevance: c.relevance || c.why || ''
      }))
    }
    // Try singular paradigmatic_case (some schemas use this)
    else if (concept.paradigmatic_case && typeof concept.paradigmatic_case === 'object') {
      cases = [{
        title: concept.paradigmatic_case.name || concept.paradigmatic_case.title || '',
        description: concept.paradigmatic_case.description || '',
        relevance: concept.paradigmatic_case.why || ''
      }]
    }
    // Fall back to user-validated cases
    if (cases.length === 0 && validatedCases.length > 0) {
      console.log('[populateEditableDraft] Using validated cases as fallback')
      cases = validatedCases.map(c => ({
        title: c.title || c.name || '',
        description: c.description || '',
        relevance: c.relevance || ''
      }))
    }

    // RECOGNITION MARKERS - normalize to objects with description
    let markers = []
    if (Array.isArray(concept.recognition_markers) && concept.recognition_markers.length > 0) {
      markers = concept.recognition_markers.map(m => {
        if (typeof m === 'string') return { description: m }
        return { description: m.description || m.pattern || String(m) }
      })
    }
    // Fall back to user-validated markers
    if (markers.length === 0 && validatedMarkers.length > 0) {
      console.log('[populateEditableDraft] Using validated markers as fallback')
      markers = validatedMarkers.map(m => {
        if (typeof m === 'string') return { description: m }
        return { description: m.pattern || m.marker || m.description || String(m) }
      })
    }

    // DIALECTICS - combine LLM response, marked dialectics, and approved tensions
    let conceptDialectics = []
    if (Array.isArray(concept.dialectics) && concept.dialectics.length > 0) {
      conceptDialectics = concept.dialectics.map(d => ({
        pole_a: d.pole_a || '',
        pole_b: d.pole_b || '',
        description: d.description || '',
        note: d.note || ''
      }))
    }
    // If LLM didn't return dialectics, build from our sources
    if (conceptDialectics.length === 0) {
      // Add marked dialectics from question flow
      const fromMarked = dialectics.map(d => ({
        pole_a: d.pole_a || '',
        pole_b: d.pole_b || '',
        description: d.description || '',
        note: d.user_note || ''
      }))

      // Add approved tensions from understanding validation
      const fromApproved = approvedTensions.map(t => ({
        pole_a: t.pole_a || '',
        pole_b: t.pole_b || '',
        description: t.description || t.tension || (typeof t === 'string' ? t : ''),
        note: t.comment || ''
      }))

      conceptDialectics = [...fromMarked, ...fromApproved]
      if (conceptDialectics.length > 0) {
        console.log('[populateEditableDraft] Built dialectics from fallback sources:', conceptDialectics)
      }
    }

    // FALSIFICATION CONDITIONS
    let falsificationConditions = []
    if (Array.isArray(concept.falsification_conditions) && concept.falsification_conditions.length > 0) {
      falsificationConditions = concept.falsification_conditions
    }
    if (falsificationConditions.length === 0) {
      falsificationConditions = ['(No falsification conditions specified - click Edit to add)']
    }

    const draft = {
      genesis: concept.genesis || { type: '', lineage: '', break_from: '' },
      problem_space: concept.problem_space || { gap: '', failed_alternatives: '' },
      definition: concept.definition || '',
      differentiations: Array.isArray(concept.differentiations) ? concept.differentiations : [],
      paradigmatic_cases: cases,
      recognition_markers: markers,
      core_claims: concept.core_claims || { ontological: '', causal: '' },
      falsification_conditions: falsificationConditions,
      dialectics: conceptDialectics
    }

    console.log('[populateEditableDraft] Final draft:', draft)
    setEditableDraft(draft)
  }

  /**
   * Update a specific section of the editable draft
   */
  const updateDraftSection = (section, value) => {
    setEditableDraft(prev => ({
      ...prev,
      [section]: value
    }))
  }

  /**
   * Toggle editing mode for a section
   */
  const toggleEditSection = (section) => {
    setEditingSection(editingSection === section ? null : section)
  }

  /**
   * Regenerate a specific section with feedback
   */
  const regenerateSection = async (section) => {
    const feedback = sectionFeedback[section] || ''
    if (!feedback.trim()) return

    setIsRegeneratingSections(prev => ({ ...prev, [section]: true }))

    try {
      const response = await fetch(`${API_URL}/regenerate-section`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          concept_name: conceptName,
          section: section,
          current_value: editableDraft[section],
          feedback: feedback,
          full_context: {
            all_answers: stageData,
            interim_analysis: interimAnalysis,
            dialectics: dialectics
          },
          source_id: sourceId
        })
      })

      if (!response.ok) throw new Error('Regeneration failed')

      const data = await response.json()
      updateDraftSection(section, data.regenerated_value)
      setSectionFeedback(prev => ({ ...prev, [section]: '' }))
    } catch (err) {
      setError(`Failed to regenerate ${section}: ${err.message}`)
    } finally {
      setIsRegeneratingSections(prev => ({ ...prev, [section]: false }))
    }
  }

  /**
   * Handle option toggle with exclusivity groups
   */
  const toggleOption = (option, question) => {
    const isMulti = question.type === QUESTION_TYPES.MULTI
    const exclusivityGroup = option.exclusivity_group

    setCurrentAnswer(prev => {
      let newSelected = [...prev.selectedOptions]

      if (newSelected.includes(option.value)) {
        // Deselect
        newSelected = newSelected.filter(v => v !== option.value)
      } else {
        // Select
        if (!isMulti) {
          // Single select - clear others
          newSelected = [option.value]
        } else {
          // Multi select - handle exclusivity
          if (exclusivityGroup !== null && exclusivityGroup !== undefined) {
            // Remove other options in same exclusivity group
            const groupOptions = question.options
              .filter(o => o.exclusivity_group === exclusivityGroup)
              .map(o => o.value)
            newSelected = newSelected.filter(v => !groupOptions.includes(v))
          }
          newSelected.push(option.value)
        }
      }

      return { ...prev, selectedOptions: newSelected }
    })
  }

  /**
   * Save the completed concept - merges editableDraft with conceptData
   */
  const saveConceptAndClose = async () => {
    if (!conceptData) return

    // Merge editableDraft with conceptData to include user edits
    const finalConceptData = {
      ...conceptData,
      name: conceptData.name || conceptName,
      genesis: editableDraft.genesis,
      problem_space: editableDraft.problem_space,
      definition: editableDraft.definition,
      differentiations: editableDraft.differentiations,
      paradigmatic_cases: editableDraft.paradigmatic_cases,
      recognition_markers: editableDraft.recognition_markers,
      core_claims: editableDraft.core_claims,
      falsification_conditions: editableDraft.falsification_conditions,
      dialectics: editableDraft.dialectics
    }

    setLoading(true)
    try {
      const response = await fetch(`${API_URL}/concepts/wizard/save`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          concept_data: finalConceptData,
          source_id: sourceId
        })
      })

      if (!response.ok) {
        throw new Error('Failed to save concept')
      }

      const result = await response.json()
      onComplete?.(result.concept)
    } catch (err) {
      const errorMsg = typeof err === 'string' ? err : (err?.message || JSON.stringify(err))
      setError(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  // Current question
  const currentQuestion = questions[currentQuestionIndex]

  // Get stage number for display
  const getStageNumber = () => {
    if (stage === STAGES.STAGE1 || stage === STAGES.ANALYZING_STAGE1) return 1
    if (stage === STAGES.INTERIM_ANALYSIS || stage === STAGES.STAGE2 || stage === STAGES.ANALYZING_STAGE2) return 2
    if (stage === STAGES.IMPLICATIONS_PREVIEW || stage === STAGES.STAGE3) return 3
    return 0
  }

  return (
    <div className="wizard-overlay">
      <div className="wizard-container wizard-enhanced">
        {/* Header */}
        <div className="wizard-header">
          <div className="wizard-title">
            <h2>Novel Concept Setup Wizard</h2>
            <span className="wizard-subtitle">
              Powered by Claude Opus 4.5 with extended thinking
            </span>
          </div>
          <button className="wizard-close" onClick={onCancel}>&times;</button>
        </div>

        {/* Progress bar with save checkpoint */}
        <div className="wizard-progress">
          <div className="progress-bar-container">
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{ width: `${(progress.stage / progress.total) * 100}%` }}
              />
            </div>
            {stage !== STAGES.NOTES && conceptName && (
              <button
                className="save-checkpoint-btn"
                onClick={saveCheckpoint}
                title="Save checkpoint for later"
              >
                💾
              </button>
            )}
          </div>
          <div className="progress-label">{progress.label}</div>
        </div>

        {/* Stage navigation breadcrumb */}
        <div className="stage-nav-breadcrumb">
          {STAGE_NAV.map((navItem, index) => {
            const currentCheckpoint = getNavCheckpoint(stage)
            const currentIndex = STAGE_NAV.findIndex(n => n.id === currentCheckpoint)
            const isCurrent = navItem.id === currentCheckpoint
            const isCompleted = index < currentIndex
            const isClickable = navItem.navigable && isCompleted
            const isDisabled = index > currentIndex

            return (
              <div key={navItem.id} className="nav-item-wrapper">
                {index > 0 && <span className="nav-connector">›</span>}
                <button
                  className={`nav-stage-btn ${isCurrent ? 'current' : ''} ${isCompleted ? 'completed' : ''} ${isDisabled ? 'disabled' : ''}`}
                  onClick={() => isClickable && navigateToStage(navItem.id)}
                  disabled={isDisabled || isCurrent}
                  title={isClickable ? `Go back to ${navItem.label}` : navItem.label}
                >
                  <span className="nav-num">{navItem.shortLabel}</span>
                  <span className="nav-label">{navItem.label}</span>
                </button>
              </div>
            )
          })}
        </div>

        {/* Main content */}
        <div className="wizard-content">
          {/* Back button - appears when not on first stage */}
          {getPreviousStage() && !loading && (
            <button className="wizard-back-btn" onClick={goBack}>
              ← Back to {STAGE_NAV.find(n => n.id === getPreviousStage())?.label || 'Previous'}
            </button>
          )}

          {/* Error display */}
          {error && (
            <div className="wizard-error">
              {typeof error === 'string' ? error : (error?.message || JSON.stringify(error))}
              <button onClick={() => setError(null)}>&times;</button>
            </div>
          )}

          {/* STAGE: Notes Input */}
          {stage === STAGES.NOTES && (
            <div className="wizard-stage">
              {/* Server Sessions Banner */}
              {serverSessions.length > 0 && (
                <div className="server-sessions-banner">
                  <div className="server-sessions-header">
                    <strong>Continue a saved session</strong>
                    <span className="session-count">{serverSessions.length} active session{serverSessions.length !== 1 ? 's' : ''}</span>
                  </div>
                  <div className="server-sessions-list">
                    {serverSessions.slice(0, 3).map(session => (
                      <div key={session.session_key} className="server-session-item">
                        <div className="session-info">
                          <span className="session-concept">{session.concept_name}</span>
                          <span className="session-stage">{session.stage || 'In progress'}</span>
                          <span className="session-time">
                            Last updated: {new Date(session.updated_at).toLocaleString()}
                          </span>
                        </div>
                        <div className="session-actions">
                          <button
                            className="btn btn-primary btn-sm"
                            onClick={() => restoreServerSession(session.session_key)}
                          >
                            Resume
                          </button>
                          <button
                            className="btn btn-danger btn-sm"
                            onClick={() => deleteServerSession(session.session_key)}
                            title="Delete session"
                          >
                            &times;
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                  {serverSessions.length > 3 && (
                    <p className="more-sessions-hint">
                      + {serverSessions.length - 3} more session{serverSessions.length - 3 !== 1 ? 's' : ''} available
                    </p>
                  )}
                </div>
              )}

              {/* Local Resume Session Banner (fallback when server unavailable) */}
              {hasSavedSession && savedSessionInfo && !serverSessions.find(s => s.concept_name === savedSessionInfo.conceptName) && (
                <div className="resume-session-banner local-session">
                  <div className="resume-info">
                    <strong>Resume local session?</strong>
                    <p>
                      Found saved progress for "<em>{savedSessionInfo.conceptName}</em>"
                      {savedSessionInfo.savedAt && (
                        <span className="saved-time">
                          {' '}(saved {new Date(savedSessionInfo.savedAt).toLocaleString()})
                        </span>
                      )}
                    </p>
                  </div>
                  <div className="resume-actions">
                    <button className="btn btn-primary btn-sm" onClick={restoreSession}>
                      Resume Session
                    </button>
                    <button className="btn btn-secondary btn-sm" onClick={clearSavedSession}>
                      Start Fresh
                    </button>
                  </div>
                </div>
              )}

              <div className="stage-header">
                <h3>Introduce Your Concept</h3>
                <p>
                  You're introducing a concept that doesn't exist in public discourse yet.
                  The wizard will help you articulate it through staged questioning.
                </p>
              </div>

              <div className="form-group">
                <label>Concept Name *</label>
                <input
                  type="text"
                  value={conceptName}
                  onChange={e => setConceptName(e.target.value)}
                  placeholder="e.g., Technological Sovereignty"
                  className="wizard-input"
                />
                <span className="help-text">
                  Choose a name that captures the essence of your concept
                </span>
              </div>

              <div className="form-group">
                <label>Initial Notes (Optional)</label>
                <textarea
                  value={notes}
                  onChange={e => setNotes(e.target.value)}
                  placeholder="Paste any notes, ideas, or draft definitions you have about this concept..."
                  className="wizard-textarea"
                  rows={8}
                />
                <span className="help-text">
                  If you have existing notes, they'll help the AI ask better questions.
                </span>
              </div>

              <div className="wizard-actions">
                <button className="btn btn-secondary" onClick={onCancel}>
                  Cancel
                </button>
                <button
                  className="btn btn-primary"
                  onClick={startWizard}
                  disabled={!conceptName.trim()}
                >
                  Start Wizard
                </button>
              </div>
            </div>
          )}

          {/* STAGE: Analyzing (any analysis stage) */}
          {(stage === STAGES.ANALYZING_NOTES || stage === STAGES.ANALYZING_STAGE1 || stage === STAGES.ANALYZING_STAGE2 || stage === STAGES.ANALYZING_DOCUMENT || stage === STAGES.ANALYZING_COMMITMENTS || stage === STAGES.PROCESSING) && (
            <div className="wizard-stage">
              <div className="stage-header">
                <h3>
                  {stage === STAGES.PROCESSING ? 'Creating Final Concept...' : 'Analyzing...'}
                </h3>
                <p>
                  {currentPhase === 'interim_analysis' && 'Building understanding from your answers...'}
                  {currentPhase === 'stage2_generation' && 'Generating tailored follow-up questions...'}
                  {currentPhase === 'implications_preview' && 'Analyzing implications of your choices...'}
                  {currentPhase === 'generating_stage3' && 'Generating context-specific Stage 3 questions...'}
                  {currentPhase === 'final_synthesis' && 'Synthesizing complete concept definition...'}
                  {!currentPhase && 'Processing...'}
                </p>
              </div>

              <div className="thinking-panel">
                <div className="thinking-header">
                  <span className="thinking-indicator">
                    <span className="pulse"></span>
                    {currentPhase || 'Thinking'}...
                  </span>
                  <button
                    className="btn btn-sm btn-secondary"
                    onClick={() => setThinkingVisible(!thinkingVisible)}
                  >
                    {thinkingVisible ? 'Hide' : 'Show'} Thinking
                  </button>
                </div>
                {thinkingVisible && (
                  <div className="thinking-content" ref={thinkingRef}>
                    {thinking || 'Starting analysis...'}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* STAGE: Understanding Validation - User rates and corrects LLM's understanding */}
          {stage === STAGES.UNDERSTANDING_VALIDATION && notesUnderstanding && (
            <div className="wizard-stage">
              <div className="stage-header">
                <h3>Here's What I Understand From Your Notes</h3>
                <p>Please validate my understanding before we proceed. Rate how well I captured your concept and add any corrections.</p>
              </div>

              <div className="understanding-validation-panel">
                {/* Regeneration indicator */}
                {notesUnderstanding.regeneratedFromFeedback && (
                  <div className="regenerated-badge">
                    Re-analyzed with your feedback
                  </div>
                )}

                {/* Understanding Summary */}
                <div className="uv-section uv-summary">
                  <h4>My Summary of Your Concept</h4>
                  <p className="uv-summary-text">{notesUnderstanding.summary}</p>
                </div>

                {/* Preliminary Definition */}
                {notesUnderstanding.preliminaryDefinition && (
                  <div className="uv-section uv-definition">
                    <h4>Working Definition</h4>
                    <div className="uv-definition-text">
                      {notesUnderstanding.preliminaryDefinition}
                    </div>
                  </div>
                )}

              </div>

              {/* =========================================================== */}
              {/* HYPOTHESIS CARDS REVIEW SECTION (Card-Based Flow)           */}
              {/* =========================================================== */}
              {(hypothesisCards.length > 0 || differentiationCards.length > 0) && (
                <div className="cards-review-section">
                  <div className="cards-review-header">
                    <h3>Review Generated Claims</h3>
                    <p>These claims were extracted from your notes. Approve, reject, or transform each card.</p>

                    {/* Card stage tabs with Accept All buttons */}
                    <div className="card-stage-tabs-container">
                    <div className="card-stage-tabs">
                      <button
                        className={`card-stage-tab ${cardReviewStage === 'hypothesis' ? 'active' : ''}`}
                        onClick={() => setCardReviewStage('hypothesis')}
                      >
                        Hypotheses ({hypothesisCards.length})
                        {hypothesisCards.filter(c => c.status === 'approved').length > 0 && (
                          <span className="approved-count">
                            ✓{hypothesisCards.filter(c => c.status === 'approved').length}
                          </span>
                        )}
                      </button>
                      <button
                        className={`card-stage-tab ${cardReviewStage === 'differentiation' ? 'active' : ''}`}
                        onClick={() => setCardReviewStage('differentiation')}
                      >
                        Differentiations ({differentiationCards.length})
                        {differentiationCards.filter(c => c.status === 'approved').length > 0 && (
                          <span className="approved-count">
                            ✓{differentiationCards.filter(c => c.status === 'approved').length}
                          </span>
                        )}
                      </button>
                    </div>
                    <button
                      className="btn btn-sm btn-success accept-all-btn"
                      onClick={() => acceptAllCards('all')}
                      disabled={[...hypothesisCards, ...differentiationCards].filter(c => c.status === 'pending').length === 0}
                      title="Accept all pending hypotheses and differentiations"
                    >
                      ✓ Accept All ({[...hypothesisCards, ...differentiationCards].filter(c => c.status === 'pending').length})
                    </button>
                    </div>
                  </div>

                  {/* Hypothesis Cards */}
                  {cardReviewStage === 'hypothesis' && hypothesisCards.length > 0 && (
                    <div className="card-grid">
                      {hypothesisCards.map(card => (
                        <HypothesisCard
                          key={card.id}
                          card={card}
                          cardType="hypothesis"
                          onApprove={approveCard}
                          onReject={rejectCard}
                          onTransform={transformCard}
                          isTransforming={isTransformingCard === card.id}
                        />
                      ))}
                    </div>
                  )}

                  {/* Differentiation Cards */}
                  {cardReviewStage === 'differentiation' && differentiationCards.length > 0 && (
                    <div className="card-grid">
                      {differentiationCards.map(card => (
                        <HypothesisCard
                          key={card.id}
                          card={card}
                          cardType="differentiation"
                          onApprove={approveCard}
                          onReject={rejectCard}
                          onTransform={transformCard}
                          isTransforming={isTransformingCard === card.id}
                        />
                      ))}
                    </div>
                  )}

                  {/* Summary of reviewed cards */}
                  <div className="cards-review-summary">
                    <span>
                      Approved: {[...hypothesisCards, ...differentiationCards].filter(c => c.status === 'approved').length}
                    </span>
                    <span>
                      Rejected: {[...hypothesisCards, ...differentiationCards].filter(c => c.status === 'rejected').length}
                    </span>
                    <span>
                      Pending: {[...hypothesisCards, ...differentiationCards].filter(c => c.status === 'pending').length}
                    </span>
                  </div>
                </div>
              )}

              {/* Correction Input - at the very bottom */}
              <div className="uv-section uv-correction">
                <h4>Add Corrections or Clarifications</h4>
                <p className="uv-correction-help">
                  If I misunderstood something, please explain. This will improve the questions I ask.
                </p>
                <textarea
                  value={understandingCorrection}
                  onChange={e => setUnderstandingCorrection(e.target.value)}
                  placeholder="What did I get wrong? What's missing? What needs clarification?"
                  rows={4}
                  className="wizard-textarea uv-correction-textarea"
                />
              </div>

              <div className="wizard-actions">
                <button className="btn btn-secondary" onClick={onCancel}>
                  Cancel
                </button>
                <button
                  className="btn btn-secondary"
                  onClick={regenerateUnderstanding}
                  disabled={isRegenerating || !understandingCorrection.trim()}
                >
                  {isRegenerating ? 'Re-analyzing...' : 'Regenerate with Feedback'}
                </button>
                <button
                  className="btn btn-primary"
                  onClick={() => {
                    console.log('[UI] Button clicked: Accept & Continue to Blind Spots')
                    startCurator()
                  }}
                >
                  Accept & Continue to Blind Spots →
                </button>
              </div>
            </div>
          )}

          {/* STAGE: Blind Spots Curating */}
          {stage === STAGES.BLIND_SPOTS_CURATING && (
            <div className="wizard-stage blind-spots-curating">
              <div className="stage-header">
                <h3>🔍 Analyzing Your Epistemic Blind Spots...</h3>
                <p>The curator is examining your notes to identify areas where your positioning could be made more explicit.</p>
              </div>
              <div className="analyzing-animation">
                <div className="spinner-large" />
                <p className="analyzing-status">{currentPhase || 'Analyzing notes against 7 epistemic categories...'}</p>
              </div>
              {thinking && thinkingVisible && (
                <div className="thinking-panel">
                  <div className="thinking-header">
                    <span>Claude's Analysis</span>
                    <button onClick={() => setThinkingVisible(false)} className="btn-icon">×</button>
                  </div>
                  <pre className="thinking-content" ref={thinkingRef}>{thinking}</pre>
                </div>
              )}
            </div>
          )}

          {/* STAGE: Blind Spots Questioning */}
          {stage === STAGES.BLIND_SPOTS_QUESTIONING && (
            <div className="wizard-stage blind-spots-questioning">
              <div className="stage-header">
                <h3>🎯 Clarify Your Epistemic Positioning</h3>
                <p>Answer these questions to make your assumptions, boundaries, and commitments more explicit.</p>
              </div>

              {/* Check if queue is loaded */}
              {(!blindSpotsQueue.slots || blindSpotsQueue.slots.length === 0) ? (
                <div className="blind-spots-loading">
                  <p>Loading questions... If this persists, please go back and click "Accept & Continue to Blind Spots" again.</p>
                  <button
                    className="btn btn-secondary"
                    onClick={() => setStage(STAGES.UNDERSTANDING_VALIDATION)}
                  >
                    ← Back to Understanding
                  </button>
                </div>
              ) : (
                <>
              {/* Progress Bar */}
              <div className="blind-spots-progress">
                <div className="progress-bar">
                  <div
                    className="progress-fill"
                    style={{ width: `${(blindSpotsQueue.completedCount / blindSpotsQueue.slots.length) * 100}%` }}
                  />
                </div>
                <div className="progress-text">
                  {blindSpotsQueue.completedCount} of {blindSpotsQueue.slots.length} answered
                  {blindSpotsQueue.sharpenerPending?.length > 0 && (
                    <span className="sharpening-indicator">
                      (+{blindSpotsQueue.sharpenerPending.length} generating...)
                    </span>
                  )}
                </div>
              </div>

              {/* Current Question */}
              {(() => {
                const currentSlot = getCurrentBlindSpotSlot()
                if (!currentSlot) return null

                const categoryConfig = {
                  ambiguity: { icon: '🔀', label: 'Ambiguity', color: '#6366f1' },
                  presupposition: { icon: '🎯', label: 'Presupposition', color: '#f59e0b' },
                  paradigm_dependency: { icon: '🔭', label: 'Paradigm', color: '#8b5cf6' },
                  likely_misreading: { icon: '⚠️', label: 'Misreading Risk', color: '#ef4444' },
                  gray_zone: { icon: '🌫️', label: 'Gray Zone', color: '#6b7280' },
                  unfilled_slot: { icon: '📝', label: 'Unfilled', color: '#3b82f6' },
                  unconfronted_challenge: { icon: '❓', label: 'Challenge', color: '#ec4899' }
                }

                const config = categoryConfig[currentSlot.category] || categoryConfig.ambiguity

                return (
                  <div className={`blind-spot-question-card depth-${currentSlot.depth}`}>
                    <div className="question-header">
                      <span
                        className="category-badge"
                        style={{ backgroundColor: config.color }}
                      >
                        {config.icon} {config.label}
                      </span>
                      {currentSlot.depth > 1 && (
                        <span className="depth-badge">Follow-up (depth {currentSlot.depth})</span>
                      )}
                      {currentSlot.generated_by === 'sharpener' && (
                        <span className="sharpener-badge">✨ Sharpened</span>
                      )}
                    </div>

                    <p className="question-text">{currentSlot.question}</p>

                    {/* Help me articulate button - prn_intent_formation_state_bifurcation */}
                    <div className="articulation-help">
                      <button
                        className="btn btn-outline articulate-btn"
                        onClick={generateAnswerOptions}
                        disabled={isGeneratingOptions}
                      >
                        {isGeneratingOptions ? (
                          <>Generating options...</>
                        ) : (
                          <>💡 Help me articulate</>
                        )}
                      </button>
                      {!answerOptions && !isGeneratingOptions && (
                        <span className="articulate-hint">
                          Not sure how to answer? Get suggested options.
                        </span>
                      )}
                    </div>

                    {/* Generated answer options */}
                    {answerOptions && (
                      <div className="answer-options-container">
                        <div className="options-header">
                          <p className="options-guidance">{answerOptions.guidance}</p>
                          <span className={`select-mode-badge ${answerOptions.mutually_exclusive ? 'exclusive' : 'multi'}`}>
                            {answerOptions.mutually_exclusive ? '⚫ Pick one' : '✅ Select multiple'}
                          </span>
                        </div>
                        {answerOptions.exclusivity_reason && (
                          <p className="exclusivity-reason">{answerOptions.exclusivity_reason}</p>
                        )}
                        <div className="answer-options-grid">
                          {answerOptions.options.map((option) => (
                            <button
                              key={option.id}
                              className={`answer-option-card ${selectedOptionIds.includes(option.id) ? 'selected' : ''}`}
                              onClick={() => toggleAnswerOption(option)}
                            >
                              <div className="option-select-indicator">
                                {answerOptions.mutually_exclusive ? (
                                  <span className={`radio-indicator ${selectedOptionIds.includes(option.id) ? 'checked' : ''}`}>
                                    {selectedOptionIds.includes(option.id) ? '●' : '○'}
                                  </span>
                                ) : (
                                  <span className={`checkbox-indicator ${selectedOptionIds.includes(option.id) ? 'checked' : ''}`}>
                                    {selectedOptionIds.includes(option.id) ? '☑' : '☐'}
                                  </span>
                                )}
                              </div>
                              <div className="option-content">
                                <span className={`stance-badge stance-${option.stance}`}>
                                  {option.stance}
                                </span>
                                <p className="option-text">{option.text}</p>
                              </div>
                            </button>
                          ))}
                        </div>

                        {/* Write-in addition - always available */}
                        <div className="write-in-section">
                          <label className="write-in-label">
                            ✏️ Add your own thoughts {selectedOptionIds.length > 0 ? '(optional)' : ''}
                          </label>
                          <textarea
                            className="write-in-textarea"
                            placeholder="Write your own answer or add to the selected options..."
                            value={writeInAddition}
                            onChange={(e) => setWriteInAddition(e.target.value)}
                            rows={3}
                          />
                        </div>

                        <div className="options-footer">
                          <button
                            className="btn btn-text dismiss-options"
                            onClick={() => {
                              setAnswerOptions(null)
                              setSelectedOptionIds([])
                              setWriteInAddition('')
                            }}
                          >
                            Dismiss options
                          </button>
                          {(selectedOptionIds.length > 0 || writeInAddition.trim()) && (
                            <span className="selection-summary">
                              {selectedOptionIds.length} selected
                              {writeInAddition.trim() ? ' + write-in' : ''}
                            </span>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Regular textarea - only show when NOT using options mode */}
                    {!answerOptions && (
                      <textarea
                        className="blind-spot-answer"
                        placeholder="Your answer (2-3 sentences)..."
                        value={currentBlindSpotAnswer}
                        onChange={(e) => setCurrentBlindSpotAnswer(e.target.value)}
                        rows={4}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter' && e.metaKey && currentBlindSpotAnswer.trim()) {
                            submitBlindSpotAnswer(false)
                          }
                        }}
                      />
                    )}

                    <div className="question-actions">
                      <button
                        className="btn btn-secondary"
                        onClick={() => submitBlindSpotAnswer(true)}
                      >
                        Skip
                      </button>
                      <button
                        className="btn btn-primary"
                        onClick={() => submitBlindSpotAnswer(false)}
                        disabled={!hasValidAnswer()}
                      >
                        Answer (⌘↵)
                      </button>
                    </div>
                  </div>
                )
              })()}

              {/* Early Finish Option */}
              {blindSpotsQueue.completedCount >= 3 && (
                <div className="early-finish-section">
                  <p className="early-finish-hint">
                    You've answered {blindSpotsQueue.completedCount} questions.
                    {blindSpotsQueue.completedCount < 6
                      ? ' A few more would strengthen the analysis.'
                      : blindSpotsQueue.completedCount < 10
                        ? ' Good progress! Continue or finish when ready.'
                        : ' Excellent coverage!'}
                  </p>
                  <button
                    className="btn btn-outline"
                    onClick={finishBlindSpotsEarly}
                  >
                    Finish with Current Answers
                  </button>
                </div>
              )}

              {/* Allocation Rationale (collapsible) */}
              {curatorAllocation && (
                <details className="allocation-details">
                  <summary>Why these questions?</summary>
                  <p>{curatorAllocation.emphasis_rationale}</p>
                  <div className="category-weights">
                    {Object.entries(curatorAllocation.category_weights || {}).map(([cat, weight]) => (
                      <span key={cat} className="weight-tag">
                        {cat}: {Math.round(weight * 100)}%
                      </span>
                    ))}
                  </div>
                </details>
              )}
                </>
              )}
            </div>
          )}

          {/* STAGE: Document Upload (Optional) */}
          {stage === STAGES.DOCUMENT_UPLOAD && (
            <div className="wizard-stage">
              <div className="stage-header">
                <h3>📄 Upload Supporting Documents (Optional)</h3>
                <p>
                  Have longer documents (papers, drafts, notes) about your concept?
                  Upload them for deep analysis using Claude's 1M token context.
                </p>
              </div>

              <div className="document-upload-panel">
                {/* Already uploaded documents */}
                {uploadedDocuments.length > 0 && (
                  <div className="uploaded-docs-section">
                    <h4>✓ Analyzed Documents</h4>
                    <div className="uploaded-docs-list">
                      {uploadedDocuments.map((doc, i) => (
                        <div key={i} className="uploaded-doc-card">
                          <div className="doc-icon">📄</div>
                          <div className="doc-info">
                            <span className="doc-name">{doc.name}</span>
                            <span className="doc-size">{(doc.size / 1024).toFixed(1)} KB</span>
                          </div>
                          <div className="doc-summary">{doc.summary}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Upload new document */}
                <div className="upload-section">
                  <h4>📤 Upload Document</h4>
                  <p className="upload-help">
                    Supported: PDF, TXT, Markdown (max 50MB)
                  </p>

                  <div className="file-input-wrapper">
                    <input
                      type="file"
                      accept=".pdf,.txt,.md,.markdown"
                      onChange={handleFileSelect}
                      className="file-input"
                      id="doc-upload"
                    />
                    <label htmlFor="doc-upload" className="file-input-label">
                      {selectedFile ? selectedFile.name : 'Choose file...'}
                    </label>
                  </div>

                  {selectedFile && (
                    <div className="selected-file-info">
                      <span>Selected: {selectedFile.name}</span>
                      <span className="file-size">({(selectedFile.size / 1024).toFixed(1)} KB)</span>
                    </div>
                  )}

                  <button
                    className="btn btn-secondary"
                    onClick={uploadAndAnalyzeDocument}
                    disabled={!selectedFile || isUploadingDocument}
                  >
                    {isUploadingDocument ? 'Analyzing...' : 'Upload & Analyze'}
                  </button>

                  {isUploadingDocument && documentAnalysisProgress && (
                    <div className="upload-progress">
                      <span className="pulse"></span>
                      {documentAnalysisProgress}
                    </div>
                  )}
                </div>

                {/* Dimensional extraction preview */}
                {dimensionalExtraction && (
                  <div className="extraction-preview">
                    <h4>🔍 Extracted Dimensions</h4>
                    <div className="dimension-badges">
                      {dimensionalExtraction.quinean && <span className="dim-badge quinean">Quinean</span>}
                      {dimensionalExtraction.sellarsian && <span className="dim-badge sellarsian">Sellarsian</span>}
                      {dimensionalExtraction.brandomian && <span className="dim-badge brandomian">Brandomian</span>}
                      {dimensionalExtraction.deleuzian && <span className="dim-badge deleuzian">Deleuzian</span>}
                      {dimensionalExtraction.bachelardian && <span className="dim-badge bachelardian">Bachelardian</span>}
                      {dimensionalExtraction.canguilhem && <span className="dim-badge canguilhem">Canguilhem</span>}
                      {dimensionalExtraction.davidson && <span className="dim-badge davidson">Davidson</span>}
                      {dimensionalExtraction.blumenberg && <span className="dim-badge blumenberg">Blumenberg</span>}
                      {dimensionalExtraction.carey && <span className="dim-badge carey">Carey</span>}
                    </div>
                    <p className="extraction-note">
                      This context will inform the questions we ask later.
                    </p>
                  </div>
                )}

                {/* Thinking panel during analysis */}
                {isUploadingDocument && thinking && (
                  <div className="thinking-panel">
                    <div className="thinking-header">
                      <span className="thinking-indicator">
                        <span className="pulse"></span>
                        Analyzing document...
                      </span>
                    </div>
                    <div className="thinking-content" ref={thinkingRef}>
                      {thinking}
                    </div>
                  </div>
                )}
              </div>

              <div className="wizard-actions">
                <button className="btn btn-secondary" onClick={onCancel}>
                  Cancel
                </button>
                <button
                  className="btn btn-secondary"
                  onClick={skipDocumentUpload}
                >
                  Skip Documents
                </button>
                <button
                  className="btn btn-primary"
                  onClick={continueFromDocumentUpload}
                  disabled={isUploadingDocument}
                >
                  Continue to Stage 1 →
                </button>
              </div>
            </div>
          )}

          {/* STAGE: Analyzing Document */}
          {stage === STAGES.ANALYZING_DOCUMENT && (
            <div className="wizard-stage">
              <div className="stage-header">
                <h3>Analyzing Document...</h3>
                <p>Extracting 9 philosophical dimensions from your document.</p>
              </div>
              <div className="thinking-panel">
                <div className="thinking-header">
                  <span className="thinking-indicator">
                    <span className="pulse"></span>
                    {documentAnalysisProgress || 'Processing...'}
                  </span>
                </div>
                {thinking && (
                  <div className="thinking-content" ref={thinkingRef}>
                    {thinking}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* STAGE: Interim Analysis Display */}
          {stage === STAGES.INTERIM_ANALYSIS && interimAnalysis && (
            <div className="wizard-stage">
              <div className="stage-header">
                <h3>Here's What I Understand So Far</h3>
                <p>Review this interim analysis before we continue to Stage 2.</p>
              </div>

              <div className="interim-panel">
                <div className="interim-section">
                  <h4>Understanding Summary</h4>
                  <p className="interim-summary">{interimAnalysis.understanding_summary}</p>
                </div>

                {interimAnalysis.key_commitments?.length > 0 && (
                  <div className="interim-section">
                    <h4>Key Commitments You've Made</h4>
                    <div className="badge-list">
                      {interimAnalysis.key_commitments.map((c, i) => (
                        <span key={i} className="commitment-badge">{c}</span>
                      ))}
                    </div>
                  </div>
                )}

                {/* New blind spots discovered from Stage 1 answers (distinct from notes preprocessing) */}
                {(interimAnalysis.epistemic_blind_spots?.length > 0 || interimAnalysis.new_tensions_from_answers?.length > 0 || interimAnalysis.tensions_detected?.length > 0) && (
                  <div className="interim-section">
                    <h4>New Blind Spots from Your Answers</h4>
                    <p className="tensions-intro">
                      These epistemic gaps emerged from your Stage 1 responses—areas where your positioning could be made more explicit:
                    </p>
                    <div className="tensions-list blind-spots-list">
                      {(interimAnalysis.epistemic_blind_spots || interimAnalysis.new_tensions_from_answers || interimAnalysis.tensions_detected || []).map((bs, i) => {
                        // Category config for display
                        const category = bs.category || bs.type || 'ambiguity'
                        const categoryConfig = {
                          ambiguity: { icon: '🔀', label: 'Ambiguity', color: '#6366f1' },
                          presupposition: { icon: '🎯', label: 'Presupposition', color: '#f59e0b' },
                          paradigm_dependency: { icon: '🔭', label: 'Paradigm', color: '#8b5cf6' },
                          likely_misreading: { icon: '⚠️', label: 'Misreading Risk', color: '#ef4444' },
                          gray_zone: { icon: '🌫️', label: 'Gray Zone', color: '#6b7280' },
                          unfilled_slot: { icon: '📝', label: 'Unfilled', color: '#3b82f6' },
                          unconfronted_challenge: { icon: '❓', label: 'Challenge', color: '#ec4899' },
                          gap: { icon: '📝', label: 'Gap', color: '#3b82f6' },
                          tension: { icon: '⚡', label: 'Tension', color: '#f59e0b' },
                          question: { icon: '❓', label: 'Question', color: '#8b5cf6' }
                        }
                        const config = categoryConfig[category] || categoryConfig.ambiguity
                        const whatUnclear = bs.what_unclear || bs.pole_a
                        const whatWouldHelp = bs.what_would_help || bs.pole_b
                        return (
                          <div key={i} className="tension-card new-tension blind-spot-card">
                            <span className="tension-badge blind-spot-badge" style={{ backgroundColor: config.color }}>
                              {config.icon} {config.label}
                            </span>
                            <p className="tension-description">{bs.description}</p>
                            {whatUnclear && whatWouldHelp && (
                              <div className="tension-poles blind-spot-clarification">
                                <span className="pole what-unclear">{whatUnclear}</span>
                                <span className="vs">→</span>
                                <span className="pole what-would-help">{whatWouldHelp}</span>
                              </div>
                            )}
                            {bs.source && (
                              <div className="tension-source">
                                <span className="source-label">Source:</span> {bs.source}
                              </div>
                            )}
                          </div>
                        )
                      })}
                    </div>
                  </div>
                )}

                {interimAnalysis.gaps_identified?.length > 0 && (
                  <div className="interim-section">
                    <h4>Areas to Clarify in Stage 2</h4>
                    <ul className="gaps-list">
                      {interimAnalysis.gaps_identified.map((g, i) => (
                        <li key={i} className="gap-item">{g}</li>
                      ))}
                    </ul>
                  </div>
                )}

                <div className="interim-section">
                  <h4>Preliminary Definition</h4>
                  <div className="preliminary-def">
                    {interimAnalysis.preliminary_definition}
                  </div>
                </div>
              </div>

              <div className="wizard-actions">
                <button className="btn btn-secondary" onClick={onCancel}>
                  Cancel
                </button>
                <button className="btn btn-primary" onClick={continueToStage2}>
                  Continue to Stage 2
                </button>
              </div>
            </div>
          )}

          {/* STAGE: Implications Preview */}
          {stage === STAGES.IMPLICATIONS_PREVIEW && implicationsPreview && (
            <div className="wizard-stage">
              <div className="stage-header">
                <h3>Implications of Your Choices</h3>
                <p>Here's what your Stage 2 answers mean for the concept.</p>
              </div>

              <div className="implications-panel">
                <div className="implications-section">
                  <h4>Definitional Trajectory</h4>
                  <p className="trajectory">{implicationsPreview.definition_trajectory}</p>
                </div>

                {implicationsPreview.key_differentiations?.length > 0 && (
                  <div className="implications-section">
                    <h4>Key Differentiations</h4>
                    <div className="differentiations-list">
                      {implicationsPreview.key_differentiations.map((d, i) => (
                        <div key={i} className="differentiation-card">
                          <div className="diff-header">
                            <strong>vs {d.from_concept}</strong>
                          </div>
                          <p className="diff-distinction">{d.distinction}</p>
                          <p className="diff-consequence">
                            <em>This means:</em> {d.consequence}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {(implicationsPreview.areas_still_developing?.length > 0 || implicationsPreview.remaining_tensions?.length > 0) && (
                  <div className="implications-section">
                    <h4>Areas Still Developing</h4>
                    <ul className="tensions-remaining">
                      {(implicationsPreview.areas_still_developing || implicationsPreview.remaining_tensions || []).map((t, i) => (
                        <li key={i}>{typeof t === 'string' ? t : (t?.description || t?.pole_a + ' vs ' + t?.pole_b || JSON.stringify(t))}</li>
                      ))}
                    </ul>
                  </div>
                )}

                <div className="implications-section">
                  <h4>Focus for Stage 3</h4>
                  <p className="grounding-focus">{implicationsPreview.grounding_focus}</p>
                </div>
              </div>

              <div className="wizard-actions">
                <button className="btn btn-secondary" onClick={onCancel}>
                  Cancel
                </button>
                <button className="btn btn-primary" onClick={continueToStage3}>
                  Continue to Stage 3
                </button>
              </div>
            </div>
          )}

          {/* STAGE: Questions (Stage 1, 2, or 3) */}
          {(stage === STAGES.STAGE1 || stage === STAGES.STAGE2 || stage === STAGES.STAGE3) && currentQuestion && (
            <div className="wizard-stage">
              <div className="question-counter">
                Stage {getStageNumber()}: Question {currentQuestionIndex + 1} of {questions.length}
              </div>

              {/* Notes Analysis Panel - show once at start of Stage 1 */}
              {stage === STAGES.STAGE1 && currentQuestionIndex === 0 && stageData.stage1?.notesAnalysis && (
                <div className="notes-analysis-panel">
                  <div className="notes-analysis-header">
                    <h4>📝 From Your Notes</h4>
                    <span className="notes-analysis-subtitle">
                      {stageData.stage1.validationNote
                        ? 'Refined understanding based on your validation feedback:'
                        : 'I extracted the following understanding:'}
                    </span>
                  </div>

                  {/* Show validation note if feedback was incorporated */}
                  {stageData.stage1.validationNote && (
                    <div className="validation-note-badge">
                      Your feedback incorporated: {stageData.stage1.validationNote}
                    </div>
                  )}

                  <div className="notes-analysis-content">
                    <p className="notes-summary">{stageData.stage1.notesAnalysis.summary}</p>
                    {stageData.stage1.notesAnalysis.preliminary_definition && (
                      <div className="preliminary-def">
                        <strong>Working definition:</strong>
                        <p>{stageData.stage1.notesAnalysis.preliminary_definition}</p>
                      </div>
                    )}
                    {stageData.stage1.notesAnalysis.key_insights?.length > 0 && (
                      <div className="key-insights">
                        <strong>Key insights {stageData.stage1.validationNote ? '(approved)' : ''}:</strong>
                        <ul>
                          {stageData.stage1.notesAnalysis.key_insights.map((insight, i) => (
                            <li key={i}>{insight}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {stageData.stage1.approvedTensions?.length > 0 && (
                      <div className="approved-tensions">
                        <strong>Preserved tensions (dialectics):</strong>
                        <ul>
                          {stageData.stage1.approvedTensions.map((tension, i) => (
                            <li key={i}>{typeof tension === 'string' ? tension : (tension?.description || tension?.pole_a + ' vs ' + tension?.pole_b)}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                  <p className="notes-analysis-note">
                    {stageData.stage1.validationNote
                      ? 'Pre-filled answers below have been refined based on your validation. Please verify and adjust as needed.'
                      : "I've pre-filled answers below where I had enough information. Please verify and adjust as needed."}
                  </p>
                </div>
              )}

              <div className="question-card">
                <div className="question-header">
                  {currentQuestion.rationale && (
                    <span className="question-rationale" title={currentQuestion.rationale}>
                      Why this question?
                    </span>
                  )}
                  {/* Prefilled indicator */}
                  {currentQuestion.prefilled?.value && (
                    <span className={`prefilled-badge prefilled-${currentQuestion.prefilled.confidence}`}>
                      ✨ Pre-filled ({currentQuestion.prefilled.confidence} confidence)
                    </span>
                  )}
                </div>

                <h3 className="question-text">{currentQuestion.text}</h3>

                {currentQuestion.help && (
                  <p className="question-help">{currentQuestion.help}</p>
                )}

                {/* Show context references for dynamically generated questions */}
                {currentQuestion.context_references && currentQuestion.context_references.length > 0 && (
                  <div className="context-references">
                    <span className="context-label">References from earlier stages:</span>
                    <div className="context-tags">
                      {currentQuestion.context_references.map((ref, idx) => (
                        <span key={idx} className="context-tag">{ref}</span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Show prefilled reasoning */}
                {currentQuestion.prefilled?.reasoning && (
                  <div className="prefilled-reasoning">
                    <span className="reasoning-label">Based on your notes:</span> {currentQuestion.prefilled.reasoning}
                    {currentQuestion.prefilled.source_excerpt && (
                      <blockquote className="source-excerpt">"{currentQuestion.prefilled.source_excerpt}"</blockquote>
                    )}
                  </div>
                )}

                {/* Generated Examples Panel for Stage 3 - paradigmatic cases */}
                {stage === STAGES.STAGE3 && (currentQuestion.id === 'paradigmatic_case' || currentQuestion.id?.includes('case')) && (
                  <div className="generated-examples-panel">
                    <div className="gen-examples-header">
                      <h4>Generated Case Studies</h4>
                      <p>I've generated candidate paradigmatic cases. Rate each to help identify the best examples.</p>
                      <button
                        className="btn btn-sm btn-secondary"
                        onClick={generateCaseStudies}
                        disabled={isGeneratingExamples}
                      >
                        {isGeneratingExamples ? 'Generating...' : generatedCases.length > 0 ? 'Regenerate' : 'Generate Cases'}
                      </button>
                    </div>

                    {isGeneratingExamples && thinking && (
                      <div className="thinking-mini">
                        <span className="thinking-label">Thinking...</span>
                        <p className="thinking-preview">{thinking.slice(-200)}</p>
                      </div>
                    )}

                    {generatedCases.length > 0 && (
                      <div className="gen-examples-list">
                        {generatedCases.map((caseItem, idx) => (
                          <div key={caseItem.id || idx} className={`example-card rating-${caseRatings[caseItem.id] || 'none'}`}>
                            <div className="example-header">
                              <span className="example-domain">{caseItem.domain}</span>
                              <h5 className="example-title">{caseItem.title}</h5>
                            </div>
                            <p className="example-description">{caseItem.description}</p>
                            <p className="example-relevance"><strong>Relevance:</strong> {caseItem.relevance}</p>

                            <div className="example-rating">
                              <span className="rating-label">Rate this example:</span>
                              <div className="rating-buttons">
                                <button
                                  className={`rating-btn good ${caseRatings[caseItem.id] === 'good' ? 'active' : ''}`}
                                  onClick={() => rateCaseStudy(caseItem.id, 'good')}
                                >
                                  Good Example
                                </button>
                                <button
                                  className={`rating-btn partial ${caseRatings[caseItem.id] === 'partial' ? 'active' : ''}`}
                                  onClick={() => rateCaseStudy(caseItem.id, 'partial')}
                                >
                                  Partially Fits
                                </button>
                                <button
                                  className={`rating-btn not_fit ${caseRatings[caseItem.id] === 'not_fit' ? 'active' : ''}`}
                                  onClick={() => rateCaseStudy(caseItem.id, 'not_fit')}
                                >
                                  Doesn't Fit
                                </button>
                              </div>
                            </div>

                            <div className="example-comment">
                              <input
                                type="text"
                                placeholder="Add comment about this case..."
                                value={caseComments[caseItem.id] || ''}
                                onChange={(e) => updateCaseComment(caseItem.id, e.target.value)}
                              />
                            </div>
                          </div>
                        ))}
                      </div>
                    )}

                    {generatedCases.length === 0 && !isGeneratingExamples && (
                      <div className="gen-examples-empty">
                        <p>Click "Generate Cases" to get LLM-suggested paradigmatic cases based on your concept definition.</p>
                      </div>
                    )}
                  </div>
                )}

                {/* Generated Examples Panel for Stage 3 - recognition markers */}
                {stage === STAGES.STAGE3 && (currentQuestion.id === 'recognition_markers' || currentQuestion.id?.includes('marker') || currentQuestion.id?.includes('recognition')) && (
                  <div className="generated-examples-panel">
                    <div className="gen-examples-header">
                      <h4>Generated Recognition Markers</h4>
                      <p>I've identified patterns that might indicate your concept in text. Validate which are useful.</p>
                      <button
                        className="btn btn-sm btn-secondary"
                        onClick={generateRecognitionMarkers}
                        disabled={isGeneratingExamples}
                      >
                        {isGeneratingExamples ? 'Generating...' : generatedMarkers.length > 0 ? 'Regenerate' : 'Generate Markers'}
                      </button>
                    </div>

                    {isGeneratingExamples && thinking && (
                      <div className="thinking-mini">
                        <span className="thinking-label">Thinking...</span>
                        <p className="thinking-preview">{thinking.slice(-200)}</p>
                      </div>
                    )}

                    {generatedMarkers.length > 0 && (
                      <div className="gen-markers-list">
                        {generatedMarkers.map((marker, idx) => (
                          <div key={marker.id || idx} className={`marker-card rating-${markerRatings[marker.id] || 'none'}`}>
                            <div className="marker-header">
                              <span className={`reliability-badge ${marker.reliability}`}>{marker.reliability}</span>
                              <h5 className="marker-pattern">{marker.pattern}</h5>
                            </div>
                            <p className="marker-example"><strong>Example:</strong> "{marker.example}"</p>
                            {marker.notes && <p className="marker-notes">{marker.notes}</p>}

                            <div className="marker-rating">
                              <span className="rating-label">Is this marker useful?</span>
                              <div className="rating-buttons">
                                <button
                                  className={`rating-btn good ${markerRatings[marker.id] === 'good' ? 'active' : ''}`}
                                  onClick={() => rateMarker(marker.id, 'good')}
                                >
                                  Good Marker
                                </button>
                                <button
                                  className={`rating-btn partial ${markerRatings[marker.id] === 'partial' ? 'active' : ''}`}
                                  onClick={() => rateMarker(marker.id, 'partial')}
                                >
                                  Partial
                                </button>
                                <button
                                  className={`rating-btn not_fit ${markerRatings[marker.id] === 'not_fit' ? 'active' : ''}`}
                                  onClick={() => rateMarker(marker.id, 'not_fit')}
                                >
                                  Not Relevant
                                </button>
                              </div>
                            </div>

                            <div className="marker-comment">
                              <input
                                type="text"
                                placeholder="Add comment about this marker..."
                                value={markerComments[marker.id] || ''}
                                onChange={(e) => updateMarkerComment(marker.id, e.target.value)}
                              />
                            </div>
                          </div>
                        ))}
                      </div>
                    )}

                    {generatedMarkers.length === 0 && !isGeneratingExamples && (
                      <div className="gen-examples-empty">
                        <p>Click "Generate Markers" to get LLM-suggested recognition patterns based on your concept and approved cases.</p>
                      </div>
                    )}
                  </div>
                )}

                {/* Open-ended answer with Auto-Generated Options (Multi-Select) */}
                {/* For Stage 3 case/marker questions, only show if no cases/markers are rated */}
                {currentQuestion.type === QUESTION_TYPES.OPEN && (
                  <div className="answer-input open-ended-enhanced">
                    {/* For Stage 3 case/marker questions - show "optional" note if rated items exist */}
                    {stage === STAGES.STAGE3 && (
                      (currentQuestion.id === 'paradigmatic_case' || currentQuestion.id?.includes('case')) &&
                      generatedCases.some(c => caseRatings[c.id] === 'good' || caseRatings[c.id] === 'partial')
                    ) && (
                      <div className="rated-items-notice">
                        <span className="notice-check">✓</span>
                        <span>You've rated case studies above. The text field below is optional.</span>
                      </div>
                    )}
                    {stage === STAGES.STAGE3 && (
                      (currentQuestion.id === 'recognition_markers' || currentQuestion.id?.includes('marker') || currentQuestion.id?.includes('recognition')) &&
                      generatedMarkers.some(m => markerRatings[m.id] === 'good' || markerRatings[m.id] === 'partial')
                    ) && (
                      <div className="rated-items-notice">
                        <span className="notice-check">✓</span>
                        <span>You've rated recognition markers above. The text field below is optional.</span>
                      </div>
                    )}

                    {/* Loading state - shown prominently during auto-generation */}
                    {isGeneratingOptions && (
                      <div className="generating-options-loading prominent">
                        <span className="loading-spinner" />
                        <span>Generating answer options from your notes...</span>
                      </div>
                    )}

                    {/* Generated Options (Multi-Select) */}
                    {generatedOptions.length > 0 && (
                      <>
                        <div className="generated-options-header">
                          <span className="options-instruction">
                            Select all that apply (you can select multiple):
                          </span>
                          <button
                            type="button"
                            className="btn btn-sm btn-regenerate"
                            onClick={() => generateOptionsForQuestion(currentQuestion)}
                            disabled={isGeneratingOptions}
                          >
                            {isGeneratingOptions ? '⏳' : '🔄'} Regenerate
                          </button>
                        </div>
                        <div className="generated-options-list multi-select">
                          {generatedOptions.map((opt, idx) => {
                            const isSelected = selectedGeneratedOptions.includes(opt.id)
                            const isTransforming = transformingOptionId === opt.id

                            return (
                              <div
                                key={opt.id || idx}
                                className={`generated-option-card ${isSelected ? 'selected' : ''}`}
                              >
                                <div
                                  className="option-selector checkbox"
                                  onClick={() => selectGeneratedOption(opt)}
                                >
                                  {isSelected ? '☑' : '☐'}
                                </div>
                                <div className="option-content" onClick={() => selectGeneratedOption(opt)}>
                                  <div className="option-text">{opt.content}</div>
                                  {opt.rationale && (
                                    <div className="option-rationale">
                                      <em>Why: {opt.rationale}</em>
                                    </div>
                                  )}
                                  {opt.transformation_history?.length > 0 && (
                                    <div className="option-transformed-badge">
                                      Refined {opt.transformation_history.length}x
                                    </div>
                                  )}
                                </div>
                                {/* Transform dropdown for this option */}
                                <div className="option-transform">
                                  <RefineDropdown
                                    card={{ id: opt.id, content: opt.content }}
                                    cardType="option"
                                    onTransform={(cardId, cardType, mode, guidance) =>
                                      transformGeneratedOption(opt.id, mode, guidance)
                                    }
                                    isTransforming={isTransforming}
                                  />
                                </div>
                              </div>
                            )
                          })}
                        </div>

                        {/* Selection summary */}
                        {selectedGeneratedOptions.length > 0 && (
                          <div className="selection-summary">
                            <span className="selection-count">
                              {selectedGeneratedOptions.length} option{selectedGeneratedOptions.length !== 1 ? 's' : ''} selected
                            </span>
                          </div>
                        )}

                        {/* Comment field for additional context */}
                        <div className="generated-options-comment">
                          <label>
                            <span className="comment-label">Add comment or qualification (optional):</span>
                            <textarea
                              value={generatedOptionsComment}
                              onChange={e => {
                                setGeneratedOptionsComment(e.target.value)
                                setCurrentAnswer(prev => ({
                                  ...prev,
                                  generatedOptionsComment: e.target.value
                                }))
                              }}
                              placeholder="Any additional thoughts, qualifications, or context..."
                              rows={2}
                              className="wizard-textarea comment-textarea"
                            />
                          </label>
                        </div>

                        {/* Custom answer section - collapsed by default */}
                        <details className="custom-answer-section">
                          <summary>Or write your own answer</summary>
                          <textarea
                            value={currentAnswer.textAnswer}
                            onChange={e => {
                              setCurrentAnswer(prev => ({ ...prev, textAnswer: e.target.value }))
                              // Clear selections if user writes custom answer
                              if (e.target.value.trim() && selectedGeneratedOptions.length > 0) {
                                setSelectedGeneratedOptions([])
                              }
                            }}
                            placeholder="Type your own answer here..."
                            rows={currentQuestion.rows || 4}
                            className="wizard-textarea"
                          />
                        </details>
                      </>
                    )}

                    {/* Fallback: show textarea if no options generated and not loading */}
                    {generatedOptions.length === 0 && !isGeneratingOptions && (
                      <div className="fallback-textarea-section">
                        <p className="fallback-note">
                          Options are being generated... If this takes too long, you can type your answer below.
                        </p>
                        <textarea
                          value={currentAnswer.textAnswer}
                          onChange={e => setCurrentAnswer(prev => ({ ...prev, textAnswer: e.target.value }))}
                          placeholder={currentQuestion.placeholder || 'Type your answer...'}
                          rows={currentQuestion.rows || 4}
                          className="wizard-textarea"
                        />
                        <button
                          type="button"
                          className="btn btn-generate-options"
                          onClick={() => generateOptionsForQuestion(currentQuestion)}
                          disabled={isGeneratingOptions}
                        >
                          Generate Answer Options
                        </button>
                      </div>
                    )}
                  </div>
                )}

                {/* Multiple choice / Multi-select */}
                {(currentQuestion.type === QUESTION_TYPES.CHOICE || currentQuestion.type === QUESTION_TYPES.MULTI) && (
                  <div className="answer-options">
                    {currentQuestion.options?.map((opt, idx) => {
                      const isSelected = currentAnswer.selectedOptions.includes(opt.value)
                      const hasExclusivity = opt.exclusivity_group !== null && opt.exclusivity_group !== undefined
                      const isCommentExpanded = expandedComments[opt.value]
                      const hasComment = currentAnswer.optionComments[opt.value]

                      return (
                        <div
                          key={idx}
                          className={`option-card ${isSelected ? 'selected' : ''} ${hasExclusivity ? 'exclusive' : ''}`}
                        >
                          <div
                            className="option-selector"
                            onClick={() => toggleOption(opt, currentQuestion)}
                          >
                            {currentQuestion.type === QUESTION_TYPES.MULTI
                              ? (isSelected ? '☑' : '☐')
                              : (isSelected ? '●' : '○')
                            }
                          </div>
                          <div className="option-content" onClick={() => toggleOption(opt, currentQuestion)}>
                            <div className="option-label">{opt.label}</div>
                            {opt.description && (
                              <div className="option-description">{opt.description}</div>
                            )}
                            {/* Show implications when selected */}
                            {isSelected && opt.implications && (
                              <div className="option-implications">
                                <strong>Implications:</strong> {opt.implications}
                              </div>
                            )}
                          </div>
                          {/* Comment expand/collapse button */}
                          <button
                            type="button"
                            className="option-comment-toggle"
                            onClick={(e) => {
                              e.stopPropagation()
                              toggleOptionComment(opt.value)
                            }}
                          >
                            💬 {isCommentExpanded ? 'Hide' : (hasComment ? 'Edit' : 'Comment')}
                          </button>
                          {/* Comment input when expanded */}
                          {isCommentExpanded && (
                            <textarea
                              className="option-comment-input"
                              value={currentAnswer.optionComments[opt.value] || ''}
                              onChange={(e) => updateOptionComment(opt.value, e.target.value)}
                              onClick={(e) => e.stopPropagation()}
                              placeholder={`Comment on "${opt.label}"...`}
                              rows={2}
                            />
                          )}
                        </div>
                      )
                    })}
                  </div>
                )}

                {/* Impact Topology Panel - show when options are selected */}
                {(currentQuestion.type === QUESTION_TYPES.CHOICE || currentQuestion.type === QUESTION_TYPES.MULTI) &&
                  currentAnswer.selectedOptions.length > 0 && (
                  <div className="impact-topology-panel">
                    <div className="topology-header">
                      <span className="topology-icon">🔗</span>
                      <h4>How This Choice Affects Your Concept</h4>
                    </div>
                    {(() => {
                      const impacts = generateImpactTopology(
                        currentQuestion,
                        currentAnswer.selectedOptions,
                        currentQuestion.options
                      )
                      if (!impacts) return (
                        <p className="topology-empty">Select an option to see how it affects other dimensions of your concept.</p>
                      )
                      return (
                        <div className="topology-grid">
                          {impacts.map((impact, idx) => {
                            const dim = CONCEPT_DIMENSIONS.find(d => d.id === impact.dimension)
                            return (
                              <div key={idx} className={`topology-card effect-${impact.effect.toLowerCase()}`}>
                                <div className="topology-card-header">
                                  <span className="dim-icon">{dim?.icon || '📌'}</span>
                                  <span className="dim-name">{dim?.label || impact.dimension}</span>
                                  <span className="effect-badge">{impact.effect}</span>
                                </div>
                                <p className="topology-note">{impact.note}</p>
                              </div>
                            )
                          })}
                        </div>
                      )
                    })()}
                  </div>
                )}

                {/* Custom response (write-in) - essay-flow pattern */}
                {currentQuestion.allow_custom_response && currentQuestion.type !== QUESTION_TYPES.OPEN && (
                  <div className="mc-custom-wrapper">
                    <div className="mc-custom-header">
                      <span className="mc-custom-label">Add your own:</span>
                      {CUSTOM_CATEGORIES.map(cat => (
                        <button
                          key={cat.key}
                          type="button"
                          className={`mc-custom-category ${currentAnswer.customCategory === cat.key ? 'active' : ''}`}
                          data-cat={cat.key}
                          onClick={() => setCurrentAnswer(prev => ({
                            ...prev,
                            customCategory: prev.customCategory === cat.key ? null : cat.key
                          }))}
                          title={cat.description}
                        >
                          {cat.label}
                        </button>
                      ))}
                    </div>
                    {currentAnswer.customCategory && (
                      <textarea
                        value={currentAnswer.customResponse}
                        onChange={e => setCurrentAnswer(prev => ({ ...prev, customResponse: e.target.value }))}
                        placeholder={`Enter your ${CUSTOM_CATEGORIES.find(c => c.key === currentAnswer.customCategory)?.label.toLowerCase() || 'response'}...`}
                        rows={3}
                        className="mc-custom-textarea"
                      />
                    )}
                  </div>
                )}

                {/* Mark as Dialectic toggle */}
                {currentQuestion.allow_mark_dialectic && (
                  <div className="dialectic-section">
                    <label
                      className={`dialectic-toggle ${currentAnswer.isDialectic ? 'active' : ''}`}
                      onClick={() => setCurrentAnswer(prev => ({ ...prev, isDialectic: !prev.isDialectic }))}
                    >
                      <input
                        type="checkbox"
                        checked={currentAnswer.isDialectic}
                        onChange={() => {}}
                      />
                      <span className="dialectic-icon">⚡</span>
                      <span>Mark as Dialectic</span>
                      <span className="dialectic-hint">Keep this as a productive tension</span>
                    </label>

                    {currentAnswer.isDialectic && (
                      <div className="dialectic-details">
                        {currentQuestion.dialectic_hint && (
                          <p className="dialectic-hint-text">{currentQuestion.dialectic_hint}</p>
                        )}
                        <div className="dialectic-poles">
                          <input
                            type="text"
                            value={currentAnswer.dialecticPoleA}
                            onChange={e => setCurrentAnswer(prev => ({ ...prev, dialecticPoleA: e.target.value }))}
                            placeholder="Pole A (e.g., theoretical)"
                            className="wizard-input pole-input"
                          />
                          <span className="vs-label">vs</span>
                          <input
                            type="text"
                            value={currentAnswer.dialecticPoleB}
                            onChange={e => setCurrentAnswer(prev => ({ ...prev, dialecticPoleB: e.target.value }))}
                            placeholder="Pole B (e.g., empirical)"
                            className="wizard-input pole-input"
                          />
                        </div>
                        <textarea
                          value={currentAnswer.dialecticNote}
                          onChange={e => setCurrentAnswer(prev => ({ ...prev, dialecticNote: e.target.value }))}
                          placeholder="Why is this tension productive? (optional)"
                          rows={2}
                          className="wizard-textarea dialectic-note"
                        />
                      </div>
                    )}
                  </div>
                )}

                {currentQuestion.example && (
                  <div className="question-example">
                    <strong>Example:</strong> {currentQuestion.example}
                  </div>
                )}
              </div>

              <div className="wizard-actions">
                <button className="btn btn-secondary" onClick={onCancel}>
                  Cancel
                </button>
                {currentQuestionIndex > 0 && (
                  <button
                    className="btn btn-secondary"
                    onClick={() => {
                      setCurrentQuestionIndex(currentQuestionIndex - 1)
                      // TODO: restore previous answer
                      resetCurrentAnswer()
                    }}
                  >
                    Back
                  </button>
                )}
                <button
                  className="btn btn-primary"
                  onClick={submitAnswer}
                  disabled={loading}
                >
                  {currentQuestionIndex < questions.length - 1 ? 'Next' : 'Complete Stage'}
                </button>
              </div>
            </div>
          )}

          {/* No questions fallback */}
          {(stage === STAGES.STAGE1 || stage === STAGES.STAGE2 || stage === STAGES.STAGE3) && !currentQuestion && (
            <div className="wizard-stage">
              <div className="wizard-error">
                No questions loaded for this stage. Questions: {questions.length}, Index: {currentQuestionIndex}
              </div>
            </div>
          )}

          {/* STAGE: Intellectual Genealogy */}
          {(stage === STAGES.GENEALOGY || stage === STAGES.GENERATING_GENEALOGY) && (
            <div className="wizard-stage genealogy-stage">
              <div className="stage-header">
                <h3>📚 Intellectual Genealogy</h3>
                <p>
                  What thinkers, concepts, frameworks, and debates influenced your concept?
                  Based on everything you've told me, I'll hypothesize some intellectual lineages.
                </p>
              </div>

              {/* Generate button */}
              {genealogyHypotheses.length === 0 && !isGeneratingGenealogy && (
                <div className="genealogy-generate-section">
                  <button
                    className="btn btn-primary btn-generate-genealogy"
                    onClick={generateGenealogy}
                  >
                    🔍 Generate Genealogy Hypotheses
                  </button>
                  <p className="generate-hint">
                    I'll analyze your notes and all previous answers to identify likely influences,
                    conceptual ancestors, relevant debates, and failed alternatives.
                  </p>
                </div>
              )}

              {/* Loading state */}
              {isGeneratingGenealogy && (
                <div className="genealogy-loading">
                  <span className="loading-spinner" />
                  <span>{thinking || 'Analyzing your concept for intellectual genealogy...'}</span>
                </div>
              )}

              {/* Generated hypotheses */}
              {genealogyHypotheses.length > 0 && (
                <div className="genealogy-hypotheses">
                  <h4>Generated Hypotheses</h4>
                  <p className="section-hint">Approve influences that apply, reject those that don't.</p>

                  <div className="genealogy-cards">
                    {genealogyHypotheses.map((hyp, idx) => (
                      <div
                        key={hyp.id || idx}
                        className={`genealogy-card ${hyp.status}`}
                      >
                        <div className="genealogy-card-header">
                          <span className={`genealogy-type ${hyp.type}`}>{hyp.type}</span>
                          <span className={`genealogy-confidence ${hyp.confidence}`}>
                            {hyp.confidence === 'high' ? '●●●' : hyp.confidence === 'medium' ? '●●○' : '●○○'}
                          </span>
                        </div>

                        <div className="genealogy-name">{hyp.name}</div>

                        <div className="genealogy-connection">{hyp.connection}</div>

                        {hyp.source_evidence && (
                          <div className="genealogy-evidence">
                            <em>Evidence: {hyp.source_evidence}</em>
                          </div>
                        )}

                        {hyp.why_relevant && (
                          <div className="genealogy-relevance">
                            <strong>Why relevant:</strong> {hyp.why_relevant}
                          </div>
                        )}

                        <div className="genealogy-actions">
                          <button
                            className={`btn-action approve ${hyp.status === 'approved' ? 'active' : ''}`}
                            onClick={() => updateGenealogyStatus(hyp.id, 'approved')}
                          >
                            ✓ Approve
                          </button>
                          <button
                            className={`btn-action reject ${hyp.status === 'rejected' ? 'active' : ''}`}
                            onClick={() => updateGenealogyStatus(hyp.id, 'rejected')}
                          >
                            ✗ Reject
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* User-added influences */}
              {(genealogyHypotheses.length > 0 || userAddedInfluences.length > 0) && (
                <div className="user-influences-section">
                  <h4>Add Your Own Influences</h4>
                  <p className="section-hint">Add any influences the LLM missed.</p>

                  {/* User added list */}
                  {userAddedInfluences.length > 0 && (
                    <div className="user-influences-list">
                      {userAddedInfluences.map(inf => (
                        <div key={inf.id} className="user-influence-item">
                          <span className={`genealogy-type ${inf.type}`}>{inf.type}</span>
                          <span className="influence-name">{inf.name}</span>
                          {inf.connection && <span className="influence-connection">— {inf.connection}</span>}
                          <button
                            className="btn-remove"
                            onClick={() => removeUserInfluence(inf.id)}
                          >
                            ×
                          </button>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Add new influence form */}
                  <div className="add-influence-form">
                    <select
                      value={newInfluenceInput.type}
                      onChange={e => setNewInfluenceInput(prev => ({ ...prev, type: e.target.value }))}
                    >
                      <option value="thinker">Thinker</option>
                      <option value="concept">Concept</option>
                      <option value="framework">Framework</option>
                      <option value="debate">Debate</option>
                      <option value="failed_alternative">Failed Alternative</option>
                    </select>
                    <input
                      type="text"
                      placeholder="Name (e.g., Karl Polanyi, embeddedness)"
                      value={newInfluenceInput.name}
                      onChange={e => setNewInfluenceInput(prev => ({ ...prev, name: e.target.value }))}
                    />
                    <input
                      type="text"
                      placeholder="Connection (optional)"
                      value={newInfluenceInput.connection}
                      onChange={e => setNewInfluenceInput(prev => ({ ...prev, connection: e.target.value }))}
                    />
                    <button
                      className="btn btn-secondary"
                      onClick={addUserInfluence}
                      disabled={!newInfluenceInput.name.trim()}
                    >
                      + Add
                    </button>
                  </div>
                </div>
              )}

              {/* Continue button */}
              {genealogyHypotheses.length > 0 && (
                <div className="stage-actions">
                  <button
                    className="btn btn-primary"
                    onClick={proceedFromGenealogy}
                  >
                    Continue to Philosophical Dimensions →
                  </button>
                </div>
              )}
            </div>
          )}

          {/* STAGE: Analyzing Commitments */}
          {stage === STAGES.ANALYZING_COMMITMENTS && (
            <div className="wizard-stage">
              <div className="stage-header">
                <h3>Generating Philosophical Dimension Questions...</h3>
                <p>Preparing questions about all 9 philosophical dimensions based on your context.</p>
              </div>
              <div className="thinking-panel">
                <div className="thinking-header">
                  <span className="thinking-indicator">
                    <span className="pulse"></span>
                    Generating questions...
                  </span>
                </div>
                {thinking && (
                  <div className="thinking-content" ref={thinkingRef}>
                    {thinking}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* STAGE: Deep Commitments - 9 Philosophical Dimensions MC Questions */}
          {stage === STAGES.DEEP_COMMITMENTS && deepCommitmentQuestions.length > 0 && (
            <div className="wizard-stage deep-commitments-stage">
              <div className="stage-header">
                <h3>🔬 Deep Philosophical Commitments</h3>
                <p>
                  These questions probe the 9 philosophical dimensions of your concept.
                  Based on your context, I've generated specific options for each.
                </p>
              </div>

              <div className="commitment-progress">
                <div className="progress-bar">
                  <div
                    className="progress-fill"
                    style={{ width: `${((currentCommitmentIndex + 1) / deepCommitmentQuestions.length) * 100}%` }}
                  />
                </div>
                <span className="progress-text">
                  Question {currentCommitmentIndex + 1} of {deepCommitmentQuestions.length}
                </span>
              </div>

              {(() => {
                const currentQ = deepCommitmentQuestions[currentCommitmentIndex]
                if (!currentQ) return null

                const currentAnswer = deepCommitmentAnswers[currentQ.id] || {}

                return (
                  <div className="commitment-question-card">
                    <div className="question-dimension-badge" data-dimension={currentQ.dimension}>
                      {currentQ.dimension?.charAt(0).toUpperCase() + currentQ.dimension?.slice(1) || 'Dimension'}
                    </div>

                    <h4 className="commitment-question-text">{currentQ.question}</h4>

                    {currentQ.rationale && (
                      <p className="commitment-rationale">{currentQ.rationale}</p>
                    )}

                    <div className="commitment-options">
                      {currentQ.options?.map((opt, i) => (
                        <label
                          key={opt.value || i}
                          className={`commitment-option ${currentAnswer.selected === opt.value || (currentAnswer.selected?.includes?.(opt.value)) ? 'selected' : ''}`}
                        >
                          <input
                            type={currentQ.allow_multiple ? 'checkbox' : 'radio'}
                            name={`commitment_${currentQ.id}`}
                            value={opt.value}
                            checked={
                              currentQ.allow_multiple
                                ? currentAnswer.selected?.includes?.(opt.value)
                                : currentAnswer.selected === opt.value
                            }
                            onChange={(e) => {
                              if (currentQ.allow_multiple) {
                                const newSelected = currentAnswer.selected || []
                                if (e.target.checked) {
                                  answerCommitmentQuestion(currentQ.id, [...newSelected, opt.value], currentAnswer.comment)
                                } else {
                                  answerCommitmentQuestion(currentQ.id, newSelected.filter(v => v !== opt.value), currentAnswer.comment)
                                }
                              } else {
                                answerCommitmentQuestion(currentQ.id, opt.value, currentAnswer.comment)
                              }
                            }}
                          />
                          <span className="option-content">
                            <span className="option-label">{opt.label}</span>
                            {opt.description && <span className="option-desc">{opt.description}</span>}
                          </span>
                        </label>
                      ))}

                      {/* None of the above option */}
                      <label
                        className={`commitment-option none-option ${currentAnswer.selected === 'none' ? 'selected' : ''}`}
                      >
                        <input
                          type={currentQ.allow_multiple ? 'checkbox' : 'radio'}
                          name={`commitment_${currentQ.id}`}
                          value="none"
                          checked={currentAnswer.selected === 'none'}
                          onChange={() => answerCommitmentQuestion(currentQ.id, 'none', currentAnswer.comment)}
                        />
                        <span className="option-content">
                          <span className="option-label">None of these / Other</span>
                          <span className="option-desc">I'll add a comment below</span>
                        </span>
                      </label>
                    </div>

                    {/* Comment field */}
                    <div className="commitment-comment">
                      <label>Add a comment (optional)</label>
                      <textarea
                        placeholder="Elaborate, qualify, or provide an alternative..."
                        value={currentAnswer.comment || ''}
                        onChange={(e) => answerCommitmentQuestion(currentQ.id, currentAnswer.selected, e.target.value)}
                        rows={2}
                      />
                    </div>
                  </div>
                )
              })()}

              <div className="wizard-actions">
                <button
                  className="btn btn-secondary"
                  onClick={prevCommitmentQuestion}
                  disabled={currentCommitmentIndex === 0}
                >
                  ← Previous
                </button>
                <button
                  className="btn btn-primary"
                  onClick={nextCommitmentQuestion}
                >
                  {currentCommitmentIndex < deepCommitmentQuestions.length - 1 ? 'Next →' : 'Continue to Phase 2 →'}
                </button>
              </div>
            </div>
          )}

          {/* STAGE: Generating Phase 2 Questions */}
          {stage === STAGES.GENERATING_PHASE2 && (
            <div className="wizard-stage">
              <div className="stage-header">
                <h3>Generating Phase 2 Questions...</h3>
                <p>Analyzing your Phase 1 answers to generate targeted follow-up questions.</p>
              </div>
              <div className="thinking-panel">
                <div className="thinking-header">
                  <span className="thinking-indicator">
                    <span className="pulse"></span>
                    Generating targeted questions...
                  </span>
                </div>
                {thinking && (
                  <div className="thinking-content" ref={thinkingRef}>
                    {thinking}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* STAGE: Phase 2 - Targeted Follow-up Questions */}
          {stage === STAGES.DEEP_COMMITMENTS_PHASE2 && phase2Questions.length > 0 && (
            <div className="wizard-stage deep-commitments-stage phase2">
              <div className="stage-header">
                <h3>🎯 Phase 2: Targeted Follow-ups</h3>
                <p>
                  Based on your Phase 1 answers, here are sharper questions to fill gaps
                  and probe specific commitments.
                </p>
              </div>

              <div className="commitment-progress">
                <div className="progress-bar phase2">
                  <div
                    className="progress-fill"
                    style={{ width: `${((currentPhase2Index + 1) / phase2Questions.length) * 100}%` }}
                  />
                </div>
                <span className="progress-text">
                  Phase 2: Question {currentPhase2Index + 1} of {phase2Questions.length}
                </span>
              </div>

              {(() => {
                const currentQ = phase2Questions[currentPhase2Index]
                if (!currentQ) return null

                const currentAnswer = phase2Answers[currentQ.id] || {}

                return (
                  <div className="commitment-question-card phase2">
                    {currentQ.dimension && (
                      <div className="question-dimension-badge" data-dimension={currentQ.dimension}>
                        {currentQ.dimension?.charAt(0).toUpperCase() + currentQ.dimension?.slice(1)}
                      </div>
                    )}
                    {currentQ.follow_up_to && (
                      <div className="follow-up-context">
                        Following up on your answer: "{currentQ.follow_up_to}"
                      </div>
                    )}

                    <h4 className="commitment-question-text">{currentQ.question}</h4>

                    {currentQ.rationale && (
                      <p className="commitment-rationale">{currentQ.rationale}</p>
                    )}

                    <div className="commitment-options">
                      {currentQ.options?.map((opt, i) => (
                        <label
                          key={opt.value || i}
                          className={`commitment-option ${currentAnswer.selected === opt.value ? 'selected' : ''}`}
                        >
                          <input
                            type="radio"
                            name={`phase2_${currentQ.id}`}
                            value={opt.value}
                            checked={currentAnswer.selected === opt.value}
                            onChange={() => answerPhase2Question(currentQ.id, opt.value, currentAnswer.comment)}
                          />
                          <span className="option-content">
                            <span className="option-label">{opt.label}</span>
                            {opt.description && <span className="option-desc">{opt.description}</span>}
                          </span>
                        </label>
                      ))}

                      <label
                        className={`commitment-option none-option ${currentAnswer.selected === 'none' ? 'selected' : ''}`}
                      >
                        <input
                          type="radio"
                          name={`phase2_${currentQ.id}`}
                          value="none"
                          checked={currentAnswer.selected === 'none'}
                          onChange={() => answerPhase2Question(currentQ.id, 'none', currentAnswer.comment)}
                        />
                        <span className="option-content">
                          <span className="option-label">None of these / Other</span>
                          <span className="option-desc">I'll add a comment below</span>
                        </span>
                      </label>
                    </div>

                    <div className="commitment-comment">
                      <label>Add a comment (optional)</label>
                      <textarea
                        placeholder="Elaborate, qualify, or provide an alternative..."
                        value={currentAnswer.comment || ''}
                        onChange={(e) => answerPhase2Question(currentQ.id, currentAnswer.selected, e.target.value)}
                        rows={2}
                      />
                    </div>
                  </div>
                )
              })()}

              <div className="wizard-actions">
                <button
                  className="btn btn-secondary"
                  onClick={prevPhase2Question}
                  disabled={currentPhase2Index === 0}
                >
                  ← Previous
                </button>
                <button
                  className="btn btn-primary"
                  onClick={nextPhase2Question}
                >
                  {currentPhase2Index < phase2Questions.length - 1 ? 'Next →' : 'Continue to Phase 3 →'}
                </button>
              </div>
            </div>
          )}

          {/* STAGE: Generating Phase 3 Questions */}
          {stage === STAGES.GENERATING_PHASE3 && (
            <div className="wizard-stage">
              <div className="stage-header">
                <h3>Generating Phase 3 Questions...</h3>
                <p>Synthesizing final verification questions based on all your answers.</p>
              </div>
              <div className="thinking-panel">
                <div className="thinking-header">
                  <span className="thinking-indicator">
                    <span className="pulse"></span>
                    Generating synthesis questions...
                  </span>
                </div>
                {thinking && (
                  <div className="thinking-content" ref={thinkingRef}>
                    {thinking}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* STAGE: Phase 3 - Final Synthesis Questions */}
          {stage === STAGES.DEEP_COMMITMENTS_PHASE3 && phase3Questions.length > 0 && (
            <div className="wizard-stage deep-commitments-stage phase3">
              <div className="stage-header">
                <h3>🔮 Phase 3: Final Synthesis</h3>
                <p>
                  These final questions verify key commitments and resolve any remaining tensions.
                </p>
              </div>

              <div className="commitment-progress">
                <div className="progress-bar phase3">
                  <div
                    className="progress-fill"
                    style={{ width: `${((currentPhase3Index + 1) / phase3Questions.length) * 100}%` }}
                  />
                </div>
                <span className="progress-text">
                  Phase 3: Question {currentPhase3Index + 1} of {phase3Questions.length}
                </span>
              </div>

              {(() => {
                const currentQ = phase3Questions[currentPhase3Index]
                if (!currentQ) return null

                const currentAnswer = phase3Answers[currentQ.id] || {}

                return (
                  <div className="commitment-question-card phase3">
                    {currentQ.dimension && (
                      <div className="question-dimension-badge" data-dimension={currentQ.dimension}>
                        {currentQ.dimension?.charAt(0).toUpperCase() + currentQ.dimension?.slice(1)}
                      </div>
                    )}
                    {currentQ.synthesis_context && (
                      <div className="synthesis-context">
                        {currentQ.synthesis_context}
                      </div>
                    )}

                    <h4 className="commitment-question-text">{currentQ.question}</h4>

                    {currentQ.rationale && (
                      <p className="commitment-rationale">{currentQ.rationale}</p>
                    )}

                    <div className="commitment-options">
                      {currentQ.options?.map((opt, i) => (
                        <label
                          key={opt.value || i}
                          className={`commitment-option ${currentAnswer.selected === opt.value ? 'selected' : ''}`}
                        >
                          <input
                            type="radio"
                            name={`phase3_${currentQ.id}`}
                            value={opt.value}
                            checked={currentAnswer.selected === opt.value}
                            onChange={() => answerPhase3Question(currentQ.id, opt.value, currentAnswer.comment)}
                          />
                          <span className="option-content">
                            <span className="option-label">{opt.label}</span>
                            {opt.description && <span className="option-desc">{opt.description}</span>}
                          </span>
                        </label>
                      ))}

                      <label
                        className={`commitment-option none-option ${currentAnswer.selected === 'none' ? 'selected' : ''}`}
                      >
                        <input
                          type="radio"
                          name={`phase3_${currentQ.id}`}
                          value="none"
                          checked={currentAnswer.selected === 'none'}
                          onChange={() => answerPhase3Question(currentQ.id, 'none', currentAnswer.comment)}
                        />
                        <span className="option-content">
                          <span className="option-label">None of these / Other</span>
                          <span className="option-desc">I'll add a comment below</span>
                        </span>
                      </label>
                    </div>

                    <div className="commitment-comment">
                      <label>Add a comment (optional)</label>
                      <textarea
                        placeholder="Elaborate, qualify, or provide an alternative..."
                        value={currentAnswer.comment || ''}
                        onChange={(e) => answerPhase3Question(currentQ.id, currentAnswer.selected, e.target.value)}
                        rows={2}
                      />
                    </div>
                  </div>
                )
              })()}

              <div className="wizard-actions">
                <button
                  className="btn btn-secondary"
                  onClick={prevPhase3Question}
                  disabled={currentPhase3Index === 0}
                >
                  ← Previous
                </button>
                <button
                  className="btn btn-primary"
                  onClick={nextPhase3Question}
                >
                  {currentPhase3Index < phase3Questions.length - 1 ? 'Next →' : 'Finish & Create Concept'}
                </button>
              </div>
            </div>
          )}

          {/* STAGE: Complete - Editable 9-Dimension Draft */}
          {stage === STAGES.COMPLETE && conceptData && (
            <div className="wizard-stage">
              <div className="stage-header success">
                <h3>Concept Draft Created</h3>
                <p>Review and edit each dimension. Click any section to modify it directly.</p>
              </div>

              <div className="nine-dimension-draft">
                {/* 1. GENESIS */}
                <div className={`dimension-section ${editingSection === 'genesis' ? 'editing' : ''}`}>
                  <div className="dimension-header" onClick={() => toggleEditSection('genesis')}>
                    <span className="dimension-icon">🌱</span>
                    <h4>1. Genesis</h4>
                    <button className="edit-toggle">{editingSection === 'genesis' ? '✓ Done' : '✎ Edit'}</button>
                  </div>
                  {editingSection === 'genesis' ? (
                    <div className="dimension-edit">
                      <div className="edit-field">
                        <label>Type</label>
                        <input
                          type="text"
                          value={editableDraft.genesis?.type || ''}
                          onChange={(e) => updateDraftSection('genesis', { ...editableDraft.genesis, type: e.target.value })}
                          placeholder="e.g., Theoretical Innovation, Empirical Discovery"
                        />
                      </div>
                      <div className="edit-field">
                        <label>Lineage</label>
                        <input
                          type="text"
                          value={editableDraft.genesis?.lineage || ''}
                          onChange={(e) => updateDraftSection('genesis', { ...editableDraft.genesis, lineage: e.target.value })}
                          placeholder="Builds on what existing concepts/theories"
                        />
                      </div>
                      <div className="edit-field">
                        <label>Break From</label>
                        <input
                          type="text"
                          value={editableDraft.genesis?.break_from || ''}
                          onChange={(e) => updateDraftSection('genesis', { ...editableDraft.genesis, break_from: e.target.value })}
                          placeholder="What does this concept challenge or replace"
                        />
                      </div>
                      <div className="regenerate-section">
                        <textarea
                          placeholder="Feedback for regeneration (e.g., 'emphasize the theoretical innovation aspect')"
                          value={sectionFeedback.genesis || ''}
                          onChange={(e) => setSectionFeedback(prev => ({ ...prev, genesis: e.target.value }))}
                        />
                        <button
                          className="btn btn-sm btn-secondary"
                          onClick={() => regenerateSection('genesis')}
                          disabled={isRegeneratingSections.genesis || !sectionFeedback.genesis?.trim()}
                        >
                          {isRegeneratingSections.genesis ? 'Regenerating...' : 'Regenerate with Feedback'}
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div className="dimension-content">
                      <div className="genesis-item">
                        <span className="item-label">Type</span>
                        <span className="item-value">{editableDraft.genesis?.type || <em>Not specified</em>}</span>
                      </div>
                      <div className="genesis-item">
                        <span className="item-label">Lineage</span>
                        <span className="item-value">{editableDraft.genesis?.lineage || <em>Not specified</em>}</span>
                      </div>
                      {editableDraft.genesis?.break_from && (
                        <div className="genesis-item">
                          <span className="item-label">Break from</span>
                          <span className="item-value">{editableDraft.genesis.break_from}</span>
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {/* 2. PROBLEM SPACE */}
                <div className={`dimension-section ${editingSection === 'problem_space' ? 'editing' : ''}`}>
                  <div className="dimension-header" onClick={() => toggleEditSection('problem_space')}>
                    <span className="dimension-icon">🎯</span>
                    <h4>2. Problem Space</h4>
                    <button className="edit-toggle">{editingSection === 'problem_space' ? '✓ Done' : '✎ Edit'}</button>
                  </div>
                  {editingSection === 'problem_space' ? (
                    <div className="dimension-edit">
                      <div className="edit-field">
                        <label>Gap Addressed</label>
                        <textarea
                          value={editableDraft.problem_space?.gap || ''}
                          onChange={(e) => updateDraftSection('problem_space', { ...editableDraft.problem_space, gap: e.target.value })}
                          placeholder="What conceptual gap does this fill"
                          rows={3}
                        />
                      </div>
                      <div className="edit-field">
                        <label>Failed Alternatives</label>
                        <textarea
                          value={editableDraft.problem_space?.failed_alternatives || ''}
                          onChange={(e) => updateDraftSection('problem_space', { ...editableDraft.problem_space, failed_alternatives: e.target.value })}
                          placeholder="What concepts failed to capture this"
                          rows={3}
                        />
                      </div>
                      <div className="regenerate-section">
                        <textarea
                          placeholder="Feedback for regeneration..."
                          value={sectionFeedback.problem_space || ''}
                          onChange={(e) => setSectionFeedback(prev => ({ ...prev, problem_space: e.target.value }))}
                        />
                        <button
                          className="btn btn-sm btn-secondary"
                          onClick={() => regenerateSection('problem_space')}
                          disabled={isRegeneratingSections.problem_space || !sectionFeedback.problem_space?.trim()}
                        >
                          {isRegeneratingSections.problem_space ? 'Regenerating...' : 'Regenerate with Feedback'}
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div className="dimension-content">
                      <div className="problem-item">
                        <span className="item-label">Gap</span>
                        <span className="item-value">{editableDraft.problem_space?.gap || <em>Not specified</em>}</span>
                      </div>
                      {editableDraft.problem_space?.failed_alternatives && (
                        <div className="problem-item">
                          <span className="item-label">Failed alternatives</span>
                          <span className="item-value">{editableDraft.problem_space.failed_alternatives}</span>
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {/* 3. DEFINITION (Brandom-style) */}
                <div className={`dimension-section ${editingSection === 'definition' ? 'editing' : ''}`}>
                  <div className="dimension-header" onClick={() => toggleEditSection('definition')}>
                    <span className="dimension-icon">📖</span>
                    <h4>3. Definition</h4>
                    <button className="edit-toggle">{editingSection === 'definition' ? '✓ Done' : '✎ Edit'}</button>
                  </div>
                  {editingSection === 'definition' ? (
                    <div className="dimension-edit">
                      <div className="edit-field">
                        <label>Brandom-style Definition</label>
                        <textarea
                          value={editableDraft.definition || ''}
                          onChange={(e) => updateDraftSection('definition', e.target.value)}
                          placeholder="The inferential definition of the concept..."
                          rows={5}
                        />
                      </div>
                      <div className="regenerate-section">
                        <textarea
                          placeholder="Feedback for regeneration..."
                          value={sectionFeedback.definition || ''}
                          onChange={(e) => setSectionFeedback(prev => ({ ...prev, definition: e.target.value }))}
                        />
                        <button
                          className="btn btn-sm btn-secondary"
                          onClick={() => regenerateSection('definition')}
                          disabled={isRegeneratingSections.definition || !sectionFeedback.definition?.trim()}
                        >
                          {isRegeneratingSections.definition ? 'Regenerating...' : 'Regenerate with Feedback'}
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div className="dimension-content">
                      <p className="definition-text">{editableDraft.definition || <em>Definition not generated</em>}</p>
                    </div>
                  )}
                </div>

                {/* 4. DIFFERENTIATIONS */}
                <div className={`dimension-section ${editingSection === 'differentiations' ? 'editing' : ''}`}>
                  <div className="dimension-header" onClick={() => toggleEditSection('differentiations')}>
                    <span className="dimension-icon">↔️</span>
                    <h4>4. Differentiations</h4>
                    <button className="edit-toggle">{editingSection === 'differentiations' ? '✓ Done' : '✎ Edit'}</button>
                  </div>
                  {editingSection === 'differentiations' ? (
                    <div className="dimension-edit">
                      {(editableDraft.differentiations || []).map((diff, idx) => (
                        <div key={idx} className="list-edit-item">
                          <input
                            type="text"
                            placeholder="vs Concept"
                            value={diff.confused_with || ''}
                            onChange={(e) => {
                              const updated = [...editableDraft.differentiations]
                              updated[idx] = { ...updated[idx], confused_with: e.target.value }
                              updateDraftSection('differentiations', updated)
                            }}
                          />
                          <textarea
                            placeholder="How it differs"
                            value={diff.difference || ''}
                            onChange={(e) => {
                              const updated = [...editableDraft.differentiations]
                              updated[idx] = { ...updated[idx], difference: e.target.value }
                              updateDraftSection('differentiations', updated)
                            }}
                            rows={2}
                          />
                          <button
                            className="btn btn-sm btn-danger"
                            onClick={() => {
                              const updated = editableDraft.differentiations.filter((_, i) => i !== idx)
                              updateDraftSection('differentiations', updated)
                            }}
                          >×</button>
                        </div>
                      ))}
                      <button
                        className="btn btn-sm btn-secondary add-item-btn"
                        onClick={() => updateDraftSection('differentiations', [
                          ...(editableDraft.differentiations || []),
                          { confused_with: '', difference: '' }
                        ])}
                      >+ Add Differentiation</button>
                    </div>
                  ) : (
                    <div className="dimension-content">
                      {editableDraft.differentiations?.length > 0 ? (
                        <ul className="dimension-list differentiations">
                          {editableDraft.differentiations.map((d, i) => (
                            <li key={i}>
                              <strong>vs {d.confused_with}</strong>
                              <p style={{ margin: '0.5rem 0 0', color: '#8b949e' }}>{d.difference}</p>
                            </li>
                          ))}
                        </ul>
                      ) : <em>No differentiations specified</em>}
                    </div>
                  )}
                </div>

                {/* 5. PARADIGMATIC CASES */}
                <div className={`dimension-section ${editingSection === 'paradigmatic_cases' ? 'editing' : ''}`}>
                  <div className="dimension-header" onClick={() => toggleEditSection('paradigmatic_cases')}>
                    <span className="dimension-icon">📋</span>
                    <h4>5. Paradigmatic Cases</h4>
                    <button className="edit-toggle">{editingSection === 'paradigmatic_cases' ? '✓ Done' : '✎ Edit'}</button>
                  </div>
                  {editingSection === 'paradigmatic_cases' ? (
                    <div className="dimension-edit">
                      {(editableDraft.paradigmatic_cases || []).map((c, idx) => (
                        <div key={idx} className="list-edit-item">
                          <input
                            type="text"
                            placeholder="Case title"
                            value={c.title || c.name || ''}
                            onChange={(e) => {
                              const updated = [...editableDraft.paradigmatic_cases]
                              updated[idx] = { ...updated[idx], title: e.target.value }
                              updateDraftSection('paradigmatic_cases', updated)
                            }}
                          />
                          <textarea
                            placeholder="Case description"
                            value={c.description || ''}
                            onChange={(e) => {
                              const updated = [...editableDraft.paradigmatic_cases]
                              updated[idx] = { ...updated[idx], description: e.target.value }
                              updateDraftSection('paradigmatic_cases', updated)
                            }}
                            rows={2}
                          />
                          <button
                            className="btn btn-sm btn-danger"
                            onClick={() => {
                              const updated = editableDraft.paradigmatic_cases.filter((_, i) => i !== idx)
                              updateDraftSection('paradigmatic_cases', updated)
                            }}
                          >×</button>
                        </div>
                      ))}
                      <button
                        className="btn btn-sm btn-secondary add-item-btn"
                        onClick={() => updateDraftSection('paradigmatic_cases', [
                          ...(editableDraft.paradigmatic_cases || []),
                          { title: '', description: '' }
                        ])}
                      >+ Add Case</button>
                    </div>
                  ) : (
                    <div className="dimension-content">
                      {editableDraft.paradigmatic_cases?.length > 0 ? (
                        <ul className="dimension-list cases">
                          {editableDraft.paradigmatic_cases.map((c, i) => (
                            <li key={i}>
                              <strong>{c.title || c.name}</strong>
                              {c.description && <p style={{ margin: '0.5rem 0 0', color: '#8b949e' }}>{c.description}</p>}
                              {c.relevance && <p style={{ margin: '0.25rem 0 0', color: '#6e7681', fontSize: '0.85rem' }}><em>Relevance: {c.relevance}</em></p>}
                            </li>
                          ))}
                        </ul>
                      ) : <em>No paradigmatic cases specified</em>}
                    </div>
                  )}
                </div>

                {/* 6. RECOGNITION MARKERS */}
                <div className={`dimension-section ${editingSection === 'recognition_markers' ? 'editing' : ''}`}>
                  <div className="dimension-header" onClick={() => toggleEditSection('recognition_markers')}>
                    <span className="dimension-icon">👁️</span>
                    <h4>6. Recognition Markers</h4>
                    <button className="edit-toggle">{editingSection === 'recognition_markers' ? '✓ Done' : '✎ Edit'}</button>
                  </div>
                  {editingSection === 'recognition_markers' ? (
                    <div className="dimension-edit">
                      {(editableDraft.recognition_markers || []).map((m, idx) => (
                        <div key={idx} className="list-edit-item single">
                          <textarea
                            placeholder="Recognition marker pattern"
                            value={m.description || m.pattern || ''}
                            onChange={(e) => {
                              const updated = [...editableDraft.recognition_markers]
                              updated[idx] = { ...updated[idx], description: e.target.value }
                              updateDraftSection('recognition_markers', updated)
                            }}
                            rows={2}
                          />
                          <button
                            className="btn btn-sm btn-danger"
                            onClick={() => {
                              const updated = editableDraft.recognition_markers.filter((_, i) => i !== idx)
                              updateDraftSection('recognition_markers', updated)
                            }}
                          >×</button>
                        </div>
                      ))}
                      <button
                        className="btn btn-sm btn-secondary add-item-btn"
                        onClick={() => updateDraftSection('recognition_markers', [
                          ...(editableDraft.recognition_markers || []),
                          { description: '' }
                        ])}
                      >+ Add Marker</button>
                    </div>
                  ) : (
                    <div className="dimension-content">
                      {editableDraft.recognition_markers?.length > 0 ? (
                        <ul className="dimension-list markers">
                          {editableDraft.recognition_markers.map((m, i) => (
                            <li key={i}>{m.description || m.pattern}</li>
                          ))}
                        </ul>
                      ) : <em>No recognition markers specified</em>}
                    </div>
                  )}
                </div>

                {/* 7. CORE CLAIMS */}
                <div className={`dimension-section ${editingSection === 'core_claims' ? 'editing' : ''}`}>
                  <div className="dimension-header" onClick={() => toggleEditSection('core_claims')}>
                    <span className="dimension-icon">💡</span>
                    <h4>7. Core Claims</h4>
                    <button className="edit-toggle">{editingSection === 'core_claims' ? '✓ Done' : '✎ Edit'}</button>
                  </div>
                  {editingSection === 'core_claims' ? (
                    <div className="dimension-edit">
                      <div className="edit-field">
                        <label>Ontological Claim</label>
                        <textarea
                          value={editableDraft.core_claims?.ontological || ''}
                          onChange={(e) => updateDraftSection('core_claims', { ...editableDraft.core_claims, ontological: e.target.value })}
                          placeholder="What does this concept say exists or is real"
                          rows={3}
                        />
                      </div>
                      <div className="edit-field">
                        <label>Causal Claim</label>
                        <textarea
                          value={editableDraft.core_claims?.causal || ''}
                          onChange={(e) => updateDraftSection('core_claims', { ...editableDraft.core_claims, causal: e.target.value })}
                          placeholder="What causal relationships does this concept assert"
                          rows={3}
                        />
                      </div>
                      <div className="regenerate-section">
                        <textarea
                          placeholder="Feedback for regeneration..."
                          value={sectionFeedback.core_claims || ''}
                          onChange={(e) => setSectionFeedback(prev => ({ ...prev, core_claims: e.target.value }))}
                        />
                        <button
                          className="btn btn-sm btn-secondary"
                          onClick={() => regenerateSection('core_claims')}
                          disabled={isRegeneratingSections.core_claims || !sectionFeedback.core_claims?.trim()}
                        >
                          {isRegeneratingSections.core_claims ? 'Regenerating...' : 'Regenerate with Feedback'}
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div className="dimension-content">
                      <div className="core-claims-grid">
                        <div className="core-claim ontological">
                          <div className="claim-type">Ontological Claim</div>
                          <div className="claim-text">{editableDraft.core_claims?.ontological || <em>Not specified</em>}</div>
                        </div>
                        <div className="core-claim causal">
                          <div className="claim-type">Causal Claim</div>
                          <div className="claim-text">{editableDraft.core_claims?.causal || <em>Not specified</em>}</div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {/* 8. FALSIFICATION CONDITIONS */}
                <div className={`dimension-section ${editingSection === 'falsification_conditions' ? 'editing' : ''}`}>
                  <div className="dimension-header" onClick={() => toggleEditSection('falsification_conditions')}>
                    <span className="dimension-icon">❌</span>
                    <h4>8. Falsification Conditions</h4>
                    <button className="edit-toggle">{editingSection === 'falsification_conditions' ? '✓ Done' : '✎ Edit'}</button>
                  </div>
                  {editingSection === 'falsification_conditions' ? (
                    <div className="dimension-edit">
                      {(editableDraft.falsification_conditions || []).map((condition, idx) => (
                        <div key={idx} className="list-edit-item single">
                          <textarea
                            placeholder="What would falsify this concept"
                            value={typeof condition === 'string' ? condition : condition.condition || ''}
                            onChange={(e) => {
                              const updated = [...editableDraft.falsification_conditions]
                              updated[idx] = e.target.value
                              updateDraftSection('falsification_conditions', updated)
                            }}
                            rows={2}
                          />
                          <button
                            className="btn btn-sm btn-danger"
                            onClick={() => {
                              const updated = editableDraft.falsification_conditions.filter((_, i) => i !== idx)
                              updateDraftSection('falsification_conditions', updated)
                            }}
                          >×</button>
                        </div>
                      ))}
                      <button
                        className="btn btn-sm btn-secondary add-item-btn"
                        onClick={() => updateDraftSection('falsification_conditions', [
                          ...(editableDraft.falsification_conditions || []),
                          ''
                        ])}
                      >+ Add Condition</button>
                    </div>
                  ) : (
                    <div className="dimension-content">
                      {editableDraft.falsification_conditions?.length > 0 ? (
                        <ul className="dimension-list falsification">
                          {editableDraft.falsification_conditions.map((c, i) => (
                            <li key={i}>{typeof c === 'string' ? c : c.condition}</li>
                          ))}
                        </ul>
                      ) : <em>No falsification conditions specified</em>}
                    </div>
                  )}
                </div>

                {/* 9. DIALECTICS (Preserved Tensions) */}
                <div className={`dimension-section ${editingSection === 'dialectics' ? 'editing' : ''}`}>
                  <div className="dimension-header" onClick={() => toggleEditSection('dialectics')}>
                    <span className="dimension-icon">⚡</span>
                    <h4>9. Dialectics (Preserved Tensions)</h4>
                    <button className="edit-toggle">{editingSection === 'dialectics' ? '✓ Done' : '✎ Edit'}</button>
                  </div>
                  {editingSection === 'dialectics' ? (
                    <div className="dimension-edit">
                      {(editableDraft.dialectics || []).map((d, idx) => (
                        <div key={idx} className="dialectic-edit-item">
                          <input
                            type="text"
                            placeholder="Pole A"
                            value={d.pole_a || ''}
                            onChange={(e) => {
                              const updated = [...editableDraft.dialectics]
                              updated[idx] = { ...updated[idx], pole_a: e.target.value }
                              updateDraftSection('dialectics', updated)
                            }}
                          />
                          <span className="vs-label">vs</span>
                          <input
                            type="text"
                            placeholder="Pole B"
                            value={d.pole_b || ''}
                            onChange={(e) => {
                              const updated = [...editableDraft.dialectics]
                              updated[idx] = { ...updated[idx], pole_b: e.target.value }
                              updateDraftSection('dialectics', updated)
                            }}
                          />
                          <button
                            className="btn btn-sm btn-danger"
                            onClick={() => {
                              const updated = editableDraft.dialectics.filter((_, i) => i !== idx)
                              updateDraftSection('dialectics', updated)
                            }}
                          >×</button>
                        </div>
                      ))}
                      <button
                        className="btn btn-sm btn-secondary add-item-btn"
                        onClick={() => updateDraftSection('dialectics', [
                          ...(editableDraft.dialectics || []),
                          { pole_a: '', pole_b: '', note: '' }
                        ])}
                      >+ Add Dialectic</button>
                    </div>
                  ) : (
                    <div className="dimension-content">
                      {editableDraft.dialectics?.length > 0 ? (
                        <div className="dialectics-list">
                          {editableDraft.dialectics.map((d, i) => (
                            <div key={i} className="dialectic-item">
                              <span className="dialectic-badge">⚡</span>
                              <div className="tension-desc">
                                {d.description || 'Productive tension'}
                                {d.note && <span style={{ color: '#6e7681', marginLeft: '0.5rem', fontSize: '0.85rem' }}>({d.note})</span>}
                              </div>
                              {(d.pole_a || d.pole_b) && (
                                <div className="poles-display">
                                  <span className="pole">{d.pole_a || '?'}</span>
                                  <span className="vs">vs</span>
                                  <span className="pole">{d.pole_b || '?'}</span>
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      ) : <em>No dialectics preserved</em>}
                    </div>
                  )}
                </div>
              </div>

              <div className="wizard-actions final-actions">
                <button className="btn btn-secondary" onClick={onCancel}>
                  Discard
                </button>
                <button
                  className="btn btn-primary"
                  onClick={saveConceptAndClose}
                  disabled={loading}
                >
                  {loading ? 'Saving...' : 'Save Concept'}
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
