import { useState, useEffect, useRef, useCallback } from 'react'

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
  STAGE1: 'stage1',
  ANALYZING_STAGE1: 'analyzing_stage1',
  INTERIM_ANALYSIS: 'interim_analysis',
  STAGE2: 'stage2',
  ANALYZING_STAGE2: 'analyzing_stage2',
  IMPLICATIONS_PREVIEW: 'implications_preview',
  STAGE3: 'stage3',
  PROCESSING: 'processing',
  COMPLETE: 'complete'
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

  // Refs
  const thinkingRef = useRef(null)
  const abortControllerRef = useRef(null)

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
        throw new Error(error.detail || 'Request failed')
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
                setThinking(prev => prev + event.content)
                handlers.onThinking?.(event.content)
              } else if (event.type === 'text') {
                handlers.onText?.(event.content)
              } else if (event.type === 'interim_complete') {
                setInterimAnalysis(event.data)
                handlers.onInterimComplete?.(event.data)
              } else if (event.type === 'complete') {
                handlers.onComplete?.(event.data)
              } else if (event.type === 'error') {
                throw new Error(event.message)
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
        setError(err.message)
        console.error('Stream error:', err)
      }
    } finally {
      setLoading(false)
      setCurrentPhase(null)
    }
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
          setStageData(prev => ({
            ...prev,
            stage1: {
              ...prev.stage1,
              questions: data.questions || [],
              notesAnalysis: data.notes_analysis || null,
              potentialTensions: data.potential_tensions || []
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
            potentialTensions: data.potential_tensions || [],
            prefilledCount: prefilledAnswers.length,
            totalQuestions: (data.questions || []).length,
            confidenceLevels: prefilledAnswers.reduce((acc, p) => {
              const conf = p.prefilled_confidence || 'low'
              acc[conf] = (acc[conf] || 0) + 1
              return acc
            }, {})
          }
          setNotesUnderstanding(understanding)

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
   */
  const acceptUnderstandingAndContinue = () => {
    setProgress({ stage: 3, total: 9, label: 'Stage 1: Genesis & Problem Space' })
    setStage(STAGES.STAGE1)
    setCurrentQuestionIndex(0)
  }

  /**
   * Regenerate understanding with user feedback
   */
  const regenerateUnderstanding = async () => {
    if (!understandingCorrection.trim() && understandingRating === 0) {
      setError('Please provide a rating or correction to regenerate')
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
        user_rating: understandingRating,
        user_correction: understandingCorrection,
        source_id: sourceId
      },
      {
        onThinking: (content) => {
          setThinking(prev => prev + content)
        },
        onComplete: (data) => {
          setQuestions(data.questions || [])
          setStageData(prev => ({
            ...prev,
            stage1: {
              ...prev.stage1,
              questions: data.questions || [],
              notesAnalysis: data.notes_analysis || null,
              potentialTensions: data.potential_tensions || []
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
            potentialTensions: data.potential_tensions || [],
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
   * Build AnswerWithMeta object from current answer state
   */
  const buildAnswerMeta = (questionId) => {
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
      option_comments: Object.keys(currentAnswer.optionComments).length > 0 ? currentAnswer.optionComments : null
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

    // Validate - need at least selected options OR text answer OR custom response
    const hasAnswer = (answerMeta.selected_options?.length > 0) ||
                      answerMeta.text_answer ||
                      answerMeta.custom_response

    if (!hasAnswer && currentQ.required !== false) {
      setError('Please provide an answer')
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
        await finalizeConceptWorkflow(answers)
      }
    }
  }

  /**
   * Analyze Stage 1 answers and get Stage 2 questions
   */
  const analyzeStage1 = async (answers) => {
    setStage(STAGES.ANALYZING_STAGE1)
    setProgress({ stage: 4, total: 9, label: 'Analyzing your answers...' })

    await streamWizardRequest(
      '/concepts/wizard/analyze-stage1',
      {
        concept_name: conceptName,
        notes: notes.trim() || null,
        answers: answers,
        source_id: sourceId
      },
      {
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
        source_id: sourceId
      },
      {
        onComplete: (data) => {
          setConceptData(data.concept)
          setProgress({ stage: 9, total: 9, label: 'Complete!' })
          setStage(STAGES.COMPLETE)
        }
      }
    )
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
   * Save the completed concept
   */
  const saveConceptAndClose = async () => {
    if (!conceptData) return

    setLoading(true)
    try {
      const response = await fetch(`${API_URL}/concepts/wizard/save`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          concept_data: conceptData,
          source_id: sourceId
        })
      })

      if (!response.ok) {
        throw new Error('Failed to save concept')
      }

      const result = await response.json()
      onComplete?.(result.concept)
    } catch (err) {
      setError(err.message)
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

        {/* Progress bar */}
        <div className="wizard-progress">
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${(progress.stage / progress.total) * 100}%` }}
            />
          </div>
          <div className="progress-label">{progress.label}</div>
        </div>

        {/* Stage indicators */}
        <div className="stage-indicators">
          <div className={`stage-indicator ${getStageNumber() >= 1 ? 'active' : ''} ${getStageNumber() > 1 ? 'complete' : ''}`}>
            <span className="indicator-num">1</span>
            <span className="indicator-label">Genesis</span>
          </div>
          <div className="stage-connector" />
          <div className={`stage-indicator ${getStageNumber() >= 2 ? 'active' : ''} ${getStageNumber() > 2 ? 'complete' : ''}`}>
            <span className="indicator-num">2</span>
            <span className="indicator-label">Differentiation</span>
          </div>
          <div className="stage-connector" />
          <div className={`stage-indicator ${getStageNumber() >= 3 ? 'active' : ''}`}>
            <span className="indicator-num">3</span>
            <span className="indicator-label">Grounding</span>
          </div>
        </div>

        {/* Main content */}
        <div className="wizard-content">
          {/* Error display */}
          {error && (
            <div className="wizard-error">
              {error}
              <button onClick={() => setError(null)}>&times;</button>
            </div>
          )}

          {/* STAGE: Notes Input */}
          {stage === STAGES.NOTES && (
            <div className="wizard-stage">
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
          {(stage === STAGES.ANALYZING_NOTES || stage === STAGES.ANALYZING_STAGE1 || stage === STAGES.ANALYZING_STAGE2 || stage === STAGES.PROCESSING) && (
            <div className="wizard-stage">
              <div className="stage-header">
                <h3>
                  {stage === STAGES.PROCESSING ? 'Creating Final Concept...' : 'Analyzing...'}
                </h3>
                <p>
                  {currentPhase === 'interim_analysis' && 'Building understanding from your answers...'}
                  {currentPhase === 'stage2_generation' && 'Generating tailored follow-up questions...'}
                  {currentPhase === 'implications_preview' && 'Analyzing implications of your choices...'}
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

                {/* Key Insights Extracted */}
                {notesUnderstanding.keyInsights?.length > 0 && (
                  <div className="uv-section uv-insights">
                    <h4>Key Insights Extracted</h4>
                    <ul className="uv-insights-list">
                      {notesUnderstanding.keyInsights.map((insight, i) => (
                        <li key={i}>{insight}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Potential Tensions */}
                {notesUnderstanding.potentialTensions?.length > 0 && (
                  <div className="uv-section uv-tensions">
                    <h4>Potential Tensions Detected</h4>
                    <div className="uv-tensions-list">
                      {notesUnderstanding.potentialTensions.map((tension, i) => (
                        <div key={i} className="uv-tension-item">
                          <span className="tension-icon">⚡</span>
                          {tension}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Confidence Indicators */}
                <div className="uv-section uv-confidence">
                  <h4>Pre-filled Confidence</h4>
                  <div className="uv-confidence-grid">
                    <div className="uv-confidence-item">
                      <span className="conf-label">Questions pre-filled:</span>
                      <span className="conf-value">{notesUnderstanding.prefilledCount} / {notesUnderstanding.totalQuestions}</span>
                    </div>
                    {notesUnderstanding.confidenceLevels && Object.entries(notesUnderstanding.confidenceLevels).map(([level, count]) => (
                      <div key={level} className={`uv-confidence-item conf-${level}`}>
                        <span className="conf-label">{level} confidence:</span>
                        <span className="conf-value">{count}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Rating Section */}
                <div className="uv-section uv-rating">
                  <h4>Rate My Understanding</h4>
                  <p className="uv-rating-help">How well did I capture your concept? (1 = poor, 5 = excellent)</p>
                  <div className="star-rating">
                    {[1, 2, 3, 4, 5].map(star => (
                      <button
                        key={star}
                        type="button"
                        className={`star-btn ${understandingRating >= star ? 'active' : ''}`}
                        onClick={() => setUnderstandingRating(star)}
                      >
                        {understandingRating >= star ? '★' : '☆'}
                      </button>
                    ))}
                    {understandingRating > 0 && (
                      <span className="rating-label">
                        {understandingRating === 1 && 'Poor - needs significant correction'}
                        {understandingRating === 2 && 'Fair - several things wrong'}
                        {understandingRating === 3 && 'Okay - some corrections needed'}
                        {understandingRating === 4 && 'Good - minor adjustments'}
                        {understandingRating === 5 && 'Excellent - captured it well'}
                      </span>
                    )}
                  </div>
                </div>

                {/* Correction Input */}
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
              </div>

              <div className="wizard-actions">
                <button className="btn btn-secondary" onClick={onCancel}>
                  Cancel
                </button>
                <button
                  className="btn btn-secondary"
                  onClick={regenerateUnderstanding}
                  disabled={isRegenerating || (!understandingCorrection.trim() && understandingRating === 0)}
                >
                  {isRegenerating ? 'Re-analyzing...' : 'Regenerate with Feedback'}
                </button>
                <button
                  className="btn btn-primary"
                  onClick={acceptUnderstandingAndContinue}
                >
                  Accept & Continue to Stage 1
                </button>
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

                {interimAnalysis.tensions_detected?.length > 0 && (
                  <div className="interim-section">
                    <h4>Tensions Detected</h4>
                    <div className="tensions-list">
                      {interimAnalysis.tensions_detected.map((t, i) => (
                        <div key={i} className="tension-card">
                          <span className="tension-badge">
                            {t.marked_as_dialectic ? '⚡ Dialectic' : 'Tension'}
                          </span>
                          <p>{t.description}</p>
                          <div className="tension-poles">
                            <span className="pole">{t.pole_a}</span>
                            <span className="vs">vs</span>
                            <span className="pole">{t.pole_b}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {interimAnalysis.gaps_identified?.length > 0 && (
                  <div className="interim-section">
                    <h4>Gaps to Explore in Stage 2</h4>
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

                {implicationsPreview.remaining_tensions?.length > 0 && (
                  <div className="implications-section">
                    <h4>Remaining Tensions</h4>
                    <ul className="tensions-remaining">
                      {implicationsPreview.remaining_tensions.map((t, i) => (
                        <li key={i}>{t}</li>
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
                    <span className="notes-analysis-subtitle">I extracted the following understanding:</span>
                  </div>
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
                        <strong>Key insights:</strong>
                        <ul>
                          {stageData.stage1.notesAnalysis.key_insights.map((insight, i) => (
                            <li key={i}>{insight}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                  <p className="notes-analysis-note">
                    I've pre-filled answers below where I had enough information. Please verify and adjust as needed.
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

                {/* Show prefilled reasoning */}
                {currentQuestion.prefilled?.reasoning && (
                  <div className="prefilled-reasoning">
                    <span className="reasoning-label">Based on your notes:</span> {currentQuestion.prefilled.reasoning}
                    {currentQuestion.prefilled.source_excerpt && (
                      <blockquote className="source-excerpt">"{currentQuestion.prefilled.source_excerpt}"</blockquote>
                    )}
                  </div>
                )}

                {/* Open-ended answer */}
                {currentQuestion.type === QUESTION_TYPES.OPEN && (
                  <div className="answer-input">
                    <textarea
                      value={currentAnswer.textAnswer}
                      onChange={e => setCurrentAnswer(prev => ({ ...prev, textAnswer: e.target.value }))}
                      placeholder={currentQuestion.placeholder || 'Type your answer...'}
                      rows={currentQuestion.rows || 4}
                      className="wizard-textarea"
                    />
                    {currentQuestion.min_length && (
                      <div className="char-count">
                        {currentAnswer.textAnswer.length} / {currentQuestion.min_length} min characters
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

          {/* STAGE: Complete */}
          {stage === STAGES.COMPLETE && conceptData && (
            <div className="wizard-stage">
              <div className="stage-header success">
                <h3>Concept Created Successfully!</h3>
                <p>Review the generated concept below and save it to your theory.</p>
              </div>

              <div className="concept-preview">
                <div className="preview-section">
                  <h4>Concept Name</h4>
                  <p className="preview-value large">{conceptData.name || conceptName}</p>
                </div>

                <div className="preview-section">
                  <h4>Definition</h4>
                  <p className="preview-value">{conceptData.definition}</p>
                </div>

                {conceptData.genesis && (
                  <div className="preview-section">
                    <h4>Genesis</h4>
                    <div className="preview-grid">
                      <div>
                        <span className="preview-label">Type:</span>
                        <span>{conceptData.genesis.type}</span>
                      </div>
                      {conceptData.genesis.lineage && (
                        <div>
                          <span className="preview-label">Lineage:</span>
                          <span>{conceptData.genesis.lineage}</span>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {conceptData.differentiations?.length > 0 && (
                  <div className="preview-section">
                    <h4>Differentiations</h4>
                    <ul className="preview-list">
                      {conceptData.differentiations.map((d, i) => (
                        <li key={i}>
                          <strong>vs {d.confused_with}:</strong> {d.difference}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {dialectics.length > 0 && (
                  <div className="preview-section">
                    <h4>Preserved Dialectics</h4>
                    <div className="dialectics-preserved">
                      {dialectics.map((d, i) => (
                        <div key={i} className="dialectic-preview">
                          <span className="dialectic-badge">⚡</span>
                          <span>{d.pole_a}</span>
                          <span className="vs">vs</span>
                          <span>{d.pole_b}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {conceptData.recognition_markers?.length > 0 && (
                  <div className="preview-section">
                    <h4>Recognition Markers</h4>
                    <ul className="preview-list">
                      {conceptData.recognition_markers.map((m, i) => (
                        <li key={i}>{m.description}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              <div className="wizard-actions">
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
