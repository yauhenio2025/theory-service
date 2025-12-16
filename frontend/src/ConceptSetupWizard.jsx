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

// Custom response categories
const CUSTOM_CATEGORIES = {
  ALTERNATIVE: 'Alternative Answer',
  COMMENT: 'Comment',
  REFINEMENT: 'Refinement'
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
    dialecticNote: ''
  })

  // Analysis results
  const [interimAnalysis, setInterimAnalysis] = useState(null)
  const [implicationsPreview, setImplicationsPreview] = useState(null)
  const [dialectics, setDialectics] = useState([])

  // Thinking/processing state
  const [thinking, setThinking] = useState('')
  const [thinkingVisible, setThinkingVisible] = useState(true)
  const [currentPhase, setCurrentPhase] = useState(null)

  // Progress state
  const [progress, setProgress] = useState({ stage: 0, total: 8, label: 'Getting started' })
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
      dialecticNote: ''
    })
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
        dialecticNote: ''
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
        dialecticNote: ''
      })
    }
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

    setStage(STAGES.ANALYZING_STAGE1)
    setProgress({ stage: 1, total: 8, label: 'Analyzing your notes...' })

    await streamWizardRequest(
      '/concepts/wizard/stage1',
      { concept_name: conceptName, notes: notes, source_id: sourceId },
      {
        onThinking: (content) => {
          setThinkingContent(prev => prev + content)
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

          setProgress({ stage: 2, total: 8, label: 'Stage 1: Genesis & Problem Space' })
          setStage(STAGES.STAGE1)
          setThinkingContent('')
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
      dialectic_note: currentAnswer.dialecticNote || null
    }
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
        stage: stageNum + 1,
        total: 8,
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
    setProgress({ stage: 3, total: 8, label: 'Analyzing your answers...' })

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
            setProgress({ stage: 3, total: 8, label: 'Building interim understanding...' })
          } else if (phase === 'stage2_generation') {
            setProgress({ stage: 4, total: 8, label: 'Generating Stage 2 questions...' })
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
          setProgress({ stage: 4, total: 8, label: 'Review interim analysis' })
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
    setProgress({ stage: 5, total: 8, label: 'Stage 2: Differentiation & Clarification' })
    setStage(STAGES.STAGE2)
  }

  /**
   * Analyze Stage 2 answers and get implications preview
   */
  const analyzeStage2 = async (answers) => {
    setStage(STAGES.ANALYZING_STAGE2)
    setProgress({ stage: 5, total: 8, label: 'Analyzing differentiations...' })

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
          setProgress({ stage: 6, total: 8, label: 'Review implications' })
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
    setProgress({ stage: 7, total: 8, label: 'Stage 3: Grounding & Recognition' })
    setStage(STAGES.STAGE3)
  }

  /**
   * Final synthesis
   */
  const finalizeConceptWorkflow = async (stage3Answers) => {
    setStage(STAGES.PROCESSING)
    setProgress({ stage: 8, total: 8, label: 'Creating final concept definition...' })

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
          setProgress({ stage: 8, total: 8, label: 'Complete!' })
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
          {(stage === STAGES.ANALYZING_STAGE1 || stage === STAGES.ANALYZING_STAGE2 || stage === STAGES.PROCESSING) && (
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

                      return (
                        <div
                          key={idx}
                          className={`option-card ${isSelected ? 'selected' : ''} ${hasExclusivity ? 'exclusive' : ''}`}
                          onClick={() => toggleOption(opt, currentQuestion)}
                        >
                          <div className="option-selector">
                            {currentQuestion.type === QUESTION_TYPES.MULTI
                              ? (isSelected ? '☑' : '☐')
                              : (isSelected ? '●' : '○')
                            }
                          </div>
                          <div className="option-content">
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
                        </div>
                      )
                    })}
                  </div>
                )}

                {/* Custom response (write-in) */}
                {currentQuestion.allow_custom_response && currentQuestion.type !== QUESTION_TYPES.OPEN && (
                  <div className="custom-response-section">
                    <div className="custom-response-header">
                      <span>Add your own response:</span>
                      <div className="custom-categories">
                        {(currentQuestion.custom_response_categories || ['Alternative Answer', 'Comment', 'Refinement']).map(cat => (
                          <button
                            key={cat}
                            className={`category-btn ${currentAnswer.customCategory === cat ? 'active' : ''}`}
                            onClick={() => setCurrentAnswer(prev => ({
                              ...prev,
                              customCategory: prev.customCategory === cat ? null : cat
                            }))}
                          >
                            {cat}
                          </button>
                        ))}
                      </div>
                    </div>
                    {currentAnswer.customCategory && (
                      <textarea
                        value={currentAnswer.customResponse}
                        onChange={e => setCurrentAnswer(prev => ({ ...prev, customResponse: e.target.value }))}
                        placeholder={`Enter your ${currentAnswer.customCategory.toLowerCase()}...`}
                        rows={3}
                        className="wizard-textarea custom-textarea"
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
