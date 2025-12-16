import { useState, useEffect, useRef, useCallback } from 'react'

/**
 * ConceptSetupWizard - Adaptive wizard for novel concept creation
 *
 * Uses Claude Opus 4.5 with extended thinking (32k budget) to:
 * 1. Analyze user's initial notes (optional)
 * 2. Generate adaptive follow-up questions
 * 3. Build the concept's Genesis dimension data
 * 4. Show thinking process in real-time
 */

const API_URL = import.meta.env.VITE_API_URL || 'https://theory-api.onrender.com'

// Wizard stages
const STAGES = {
  NOTES: 'notes',           // Optional initial notes dump
  ANALYZING: 'analyzing',   // LLM analyzing notes
  QUESTIONS: 'questions',   // Adaptive Q&A
  PROCESSING: 'processing', // Final processing
  COMPLETE: 'complete'      // Done
}

// Question types
const QUESTION_TYPES = {
  OPEN: 'open_ended',
  CHOICE: 'multiple_choice',
  MULTI: 'multi_select',
  SCALE: 'scale'
}

export default function ConceptSetupWizard({ sourceId, onComplete, onCancel }) {
  // Wizard state
  const [stage, setStage] = useState(STAGES.NOTES)
  const [notes, setNotes] = useState('')
  const [conceptName, setConceptName] = useState('')

  // Q&A state
  const [questions, setQuestions] = useState([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [answers, setAnswers] = useState({})
  const [currentAnswer, setCurrentAnswer] = useState('')
  const [selectedOptions, setSelectedOptions] = useState([])

  // Thinking state
  const [thinking, setThinking] = useState('')
  const [thinkingVisible, setThinkingVisible] = useState(true)
  const [responseText, setResponseText] = useState('')

  // Progress state
  const [progress, setProgress] = useState({ stage: 0, total: 6, label: 'Getting started' })
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

  /**
   * Stream response from wizard API
   * Handles both thinking blocks and text responses
   */
  const streamWizardRequest = async (endpoint, body, onThinking, onText, onComplete) => {
    setLoading(true)
    setError(null)
    setThinking('')
    setResponseText('')

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

        // Process SSE events
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            if (data === '[DONE]') continue

            try {
              const event = JSON.parse(data)

              if (event.type === 'thinking') {
                setThinking(prev => prev + event.content)
                onThinking?.(event.content)
              } else if (event.type === 'text') {
                setResponseText(prev => prev + event.content)
                onText?.(event.content)
              } else if (event.type === 'complete') {
                onComplete?.(event.data)
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
    }
  }

  /**
   * Start wizard - either from notes or skip to questions
   */
  const startFromNotes = async () => {
    if (!conceptName.trim()) {
      setError('Please enter a concept name')
      return
    }

    setStage(STAGES.ANALYZING)
    setProgress({ stage: 1, total: 6, label: 'Analyzing your notes...' })

    await streamWizardRequest(
      '/concepts/wizard/analyze-notes',
      {
        concept_name: conceptName,
        notes: notes.trim() || null,
        source_id: sourceId
      },
      null, // onThinking
      null, // onText
      (data) => {
        // Notes analyzed, questions generated
        setQuestions(data.questions || [])
        setProgress({ stage: 2, total: 6, label: 'Ready to ask questions' })
        setStage(STAGES.QUESTIONS)
      }
    )
  }

  /**
   * Skip notes and start with default questions
   */
  const skipNotes = async () => {
    if (!conceptName.trim()) {
      setError('Please enter a concept name')
      return
    }

    setStage(STAGES.ANALYZING)
    setProgress({ stage: 1, total: 6, label: 'Preparing questions...' })

    await streamWizardRequest(
      '/concepts/wizard/start',
      {
        concept_name: conceptName,
        source_id: sourceId
      },
      null,
      null,
      (data) => {
        setQuestions(data.questions || [])
        setProgress({ stage: 2, total: 6, label: 'Ready to ask questions' })
        setStage(STAGES.QUESTIONS)
      }
    )
  }

  /**
   * Submit answer to current question
   */
  const submitAnswer = async () => {
    const currentQ = questions[currentQuestionIndex]
    if (!currentQ) return

    // Validate answer
    let answer
    if (currentQ.type === QUESTION_TYPES.CHOICE) {
      answer = selectedOptions[0]
    } else if (currentQ.type === QUESTION_TYPES.MULTI) {
      answer = selectedOptions
    } else {
      answer = currentAnswer.trim()
    }

    if (!answer || (Array.isArray(answer) && answer.length === 0)) {
      if (currentQ.required !== false) {
        setError('Please provide an answer')
        return
      }
    }

    // Store answer
    const newAnswers = {
      ...answers,
      [currentQ.id]: answer
    }
    setAnswers(newAnswers)

    // Reset input
    setCurrentAnswer('')
    setSelectedOptions([])
    setError(null)

    // Check if we should generate follow-up questions or move to next
    if (currentQuestionIndex < questions.length - 1) {
      // Still have questions
      setCurrentQuestionIndex(currentQuestionIndex + 1)
      setProgress({
        stage: 2 + Math.floor((currentQuestionIndex + 1) / questions.length * 2),
        total: 6,
        label: `Question ${currentQuestionIndex + 2} of ${questions.length}`
      })
    } else {
      // All questions answered - check for follow-ups or finalize
      setStage(STAGES.PROCESSING)
      setProgress({ stage: 5, total: 6, label: 'Processing your concept...' })

      await streamWizardRequest(
        '/concepts/wizard/process',
        {
          concept_name: conceptName,
          notes: notes.trim() || null,
          answers: newAnswers,
          source_id: sourceId
        },
        null,
        null,
        (data) => {
          if (data.more_questions) {
            // LLM wants to ask follow-up questions
            setQuestions(prev => [...prev, ...data.questions])
            setStage(STAGES.QUESTIONS)
            setProgress({
              stage: 4,
              total: 6,
              label: `Follow-up question ${currentQuestionIndex + 2}`
            })
          } else {
            // Complete
            setConceptData(data.concept)
            setProgress({ stage: 6, total: 6, label: 'Complete!' })
            setStage(STAGES.COMPLETE)
          }
        }
      )
    }
  }

  /**
   * Handle option selection for choice questions
   */
  const toggleOption = (option, isMulti) => {
    if (isMulti) {
      setSelectedOptions(prev =>
        prev.includes(option)
          ? prev.filter(o => o !== option)
          : [...prev, option]
      )
    } else {
      setSelectedOptions([option])
    }
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

  return (
    <div className="wizard-overlay">
      <div className="wizard-container">
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
                  The wizard will help you articulate it through structured questions.
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
                  placeholder="Paste any notes, ideas, or draft definitions you have about this concept. The AI will analyze these and generate tailored follow-up questions..."
                  className="wizard-textarea"
                  rows={10}
                />
                <span className="help-text">
                  If you have existing notes, paste them here. The AI will analyze them
                  and ask more targeted questions. You can also skip this step.
                </span>
              </div>

              <div className="wizard-actions">
                <button className="btn btn-secondary" onClick={onCancel}>
                  Cancel
                </button>
                <button
                  className="btn btn-secondary"
                  onClick={skipNotes}
                  disabled={!conceptName.trim()}
                >
                  Skip Notes
                </button>
                <button
                  className="btn btn-primary"
                  onClick={startFromNotes}
                  disabled={!conceptName.trim()}
                >
                  {notes.trim() ? 'Analyze Notes & Continue' : 'Start Wizard'}
                </button>
              </div>
            </div>
          )}

          {/* STAGE: Analyzing */}
          {stage === STAGES.ANALYZING && (
            <div className="wizard-stage">
              <div className="stage-header">
                <h3>Analyzing...</h3>
                <p>
                  Claude is analyzing your input and preparing questions tailored to
                  help articulate "{conceptName}".
                </p>
              </div>

              <div className="thinking-panel">
                <div className="thinking-header">
                  <span className="thinking-indicator">
                    <span className="pulse"></span>
                    Thinking...
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

              {responseText && (
                <div className="response-preview">
                  {responseText}
                </div>
              )}
            </div>
          )}

          {/* STAGE: Questions - Debug fallback */}
          {stage === STAGES.QUESTIONS && !currentQuestion && (
            <div className="wizard-stage">
              <div className="wizard-error">
                No questions loaded. Questions array length: {questions.length}.
                Current index: {currentQuestionIndex}.
                {questions.length > 0 && (
                  <pre style={{fontSize: '10px', maxHeight: '200px', overflow: 'auto'}}>
                    {JSON.stringify(questions[0], null, 2)}
                  </pre>
                )}
              </div>
            </div>
          )}

          {/* STAGE: Questions */}
          {stage === STAGES.QUESTIONS && currentQuestion && (
            <div className="wizard-stage">
              <div className="question-counter">
                Question {currentQuestionIndex + 1} of {questions.length}
              </div>

              <div className="question-card">
                <div className="question-header">
                  <span className="question-stage-badge">
                    Stage {currentQuestion.stage || 1}
                  </span>
                  {currentQuestion.rationale && (
                    <span className="question-rationale" title={currentQuestion.rationale}>
                      Why this question?
                    </span>
                  )}
                </div>

                <h3 className="question-text">{currentQuestion.text}</h3>

                {currentQuestion.help && (
                  <p className="question-help">{currentQuestion.help}</p>
                )}

                {/* Open-ended answer */}
                {currentQuestion.type === QUESTION_TYPES.OPEN && (
                  <div className="answer-input">
                    <textarea
                      value={currentAnswer}
                      onChange={e => setCurrentAnswer(e.target.value)}
                      placeholder={currentQuestion.placeholder || 'Type your answer...'}
                      rows={currentQuestion.rows || 4}
                      className="wizard-textarea"
                    />
                    {currentQuestion.min_length && (
                      <div className="char-count">
                        {currentAnswer.length} / {currentQuestion.min_length} min characters
                      </div>
                    )}
                  </div>
                )}

                {/* Multiple choice */}
                {currentQuestion.type === QUESTION_TYPES.CHOICE && (
                  <div className="answer-options">
                    {currentQuestion.options?.map((opt, idx) => (
                      <div
                        key={idx}
                        className={`option-card ${selectedOptions.includes(opt.value) ? 'selected' : ''}`}
                        onClick={() => toggleOption(opt.value, false)}
                      >
                        <div className="option-radio">
                          {selectedOptions.includes(opt.value) ? '●' : '○'}
                        </div>
                        <div className="option-content">
                          <div className="option-label">{opt.label}</div>
                          {opt.description && (
                            <div className="option-description">{opt.description}</div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {/* Multi-select */}
                {currentQuestion.type === QUESTION_TYPES.MULTI && (
                  <div className="answer-options">
                    {currentQuestion.options?.map((opt, idx) => (
                      <div
                        key={idx}
                        className={`option-card ${selectedOptions.includes(opt.value) ? 'selected' : ''}`}
                        onClick={() => toggleOption(opt.value, true)}
                      >
                        <div className="option-checkbox">
                          {selectedOptions.includes(opt.value) ? '☑' : '☐'}
                        </div>
                        <div className="option-content">
                          <div className="option-label">{opt.label}</div>
                          {opt.description && (
                            <div className="option-description">{opt.description}</div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {/* Scale */}
                {currentQuestion.type === QUESTION_TYPES.SCALE && (
                  <div className="answer-scale">
                    <input
                      type="range"
                      min={currentQuestion.min || 1}
                      max={currentQuestion.max || 5}
                      value={currentAnswer || currentQuestion.min || 1}
                      onChange={e => setCurrentAnswer(e.target.value)}
                      className="wizard-slider"
                    />
                    <div className="scale-labels">
                      <span>{currentQuestion.min_label || 'Low'}</span>
                      <span className="scale-value">{currentAnswer || currentQuestion.min || 1}</span>
                      <span>{currentQuestion.max_label || 'High'}</span>
                    </div>
                  </div>
                )}

                {currentQuestion.example && (
                  <div className="question-example">
                    <strong>Example:</strong> {currentQuestion.example}
                  </div>
                )}
              </div>

              {/* Previous answers summary */}
              {Object.keys(answers).length > 0 && (
                <div className="answers-summary">
                  <button
                    className="summary-toggle"
                    onClick={() => {
                      const el = document.querySelector('.answers-list')
                      if (el) el.classList.toggle('collapsed')
                    }}
                  >
                    Previous answers ({Object.keys(answers).length})
                  </button>
                  <div className="answers-list collapsed">
                    {questions.slice(0, currentQuestionIndex).map((q, idx) => (
                      <div key={q.id} className="answer-preview">
                        <strong>Q{idx + 1}:</strong> {String(answers[q.id]).slice(0, 100)}...
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="wizard-actions">
                <button className="btn btn-secondary" onClick={onCancel}>
                  Cancel
                </button>
                {currentQuestionIndex > 0 && (
                  <button
                    className="btn btn-secondary"
                    onClick={() => setCurrentQuestionIndex(currentQuestionIndex - 1)}
                  >
                    Back
                  </button>
                )}
                <button
                  className="btn btn-primary"
                  onClick={submitAnswer}
                  disabled={loading}
                >
                  {currentQuestionIndex < questions.length - 1 ? 'Next' : 'Finish'}
                </button>
              </div>
            </div>
          )}

          {/* STAGE: Processing */}
          {stage === STAGES.PROCESSING && (
            <div className="wizard-stage">
              <div className="stage-header">
                <h3>Processing Your Concept</h3>
                <p>
                  Claude is synthesizing your answers into a comprehensive concept definition
                  for "{conceptName}".
                </p>
              </div>

              <div className="thinking-panel">
                <div className="thinking-header">
                  <span className="thinking-indicator">
                    <span className="pulse"></span>
                    Building concept...
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
                    {thinking || 'Synthesizing your responses...'}
                  </div>
                )}
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
                      <div>
                        <span className="preview-label">Lineage:</span>
                        <span>{conceptData.genesis.lineage}</span>
                      </div>
                    </div>
                  </div>
                )}

                {conceptData.problem_space && (
                  <div className="preview-section">
                    <h4>Problem Space</h4>
                    <p className="preview-value">{conceptData.problem_space.gap}</p>
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

                {conceptData.paradigmatic_case && (
                  <div className="preview-section">
                    <h4>Paradigmatic Case</h4>
                    <p className="preview-value">{conceptData.paradigmatic_case.name}</p>
                    <p className="preview-secondary">{conceptData.paradigmatic_case.why}</p>
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

                {conceptData.core_claims?.length > 0 && (
                  <div className="preview-section">
                    <h4>Core Claims</h4>
                    <ul className="preview-list">
                      {conceptData.core_claims.map((c, i) => (
                        <li key={i}>
                          <span className="claim-type">[{c.type}]</span> {c.statement}
                        </li>
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
