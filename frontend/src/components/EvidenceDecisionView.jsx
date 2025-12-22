import { useState, useEffect } from 'react'

const RELATIONSHIP_COLORS = {
  illustrates: { bg: '#E8F5E9', text: '#2E7D32', label: 'Illustrates' },
  deepens: { bg: '#E3F2FD', text: '#1565C0', label: 'Deepens' },
  challenges: { bg: '#FFEBEE', text: '#C62828', label: 'Challenges' },
  limits: { bg: '#FFF3E0', text: '#E65100', label: 'Limits' },
  bridges: { bg: '#F3E5F5', text: '#7B1FA2', label: 'Bridges' },
  inverts: { bg: '#FCE4EC', text: '#AD1457', label: 'Inverts' },
}

function EvidenceDecisionView({ conceptId, onClose, onDecisionMade, apiUrl }) {
  const [decision, setDecision] = useState(null)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(null)
  const [selectedInterpretation, setSelectedInterpretation] = useState(null)
  const [currentIndex, setCurrentIndex] = useState(0)

  const loadDecision = async (index = 0) => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${apiUrl}/concepts/${conceptId}/evidence/decisions/pending?index=${index}`)
      if (!response.ok) {
        const err = await response.json()
        throw new Error(err.detail || 'Failed to load decision')
      }
      const data = await response.json()
      setDecision(data)
      setCurrentIndex(index)
      setSelectedInterpretation(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadDecision(0)
  }, [conceptId])

  const handleSubmit = async () => {
    if (!selectedInterpretation) return

    setSubmitting(true)
    setError(null)

    try {
      // Get all change IDs for the selected interpretation
      const interp = decision.interpretations.find(i => i.id === selectedInterpretation)
      const changeIds = interp?.structural_changes?.map(c => c.id) || []

      const response = await fetch(`${apiUrl}/concepts/${conceptId}/evidence/decisions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          interpretation_id: selectedInterpretation,
          accepted_change_ids: changeIds,
          rejected_change_ids: [],
        }),
      })

      if (!response.ok) {
        const err = await response.json()
        throw new Error(err.detail || 'Failed to submit decision')
      }

      onDecisionMade()

      // Load next decision or close if done
      if (decision.decision_index < decision.total_pending) {
        loadDecision(currentIndex)
      } else {
        onClose()
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  const handleSkip = async () => {
    setSubmitting(true)
    try {
      await fetch(`${apiUrl}/concepts/${conceptId}/evidence/decisions/${decision.fragment.id}/skip`, {
        method: 'POST',
      })

      if (decision.decision_index < decision.total_pending) {
        loadDecision(currentIndex)
      } else {
        onClose()
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return (
      <div className="modal-overlay" style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
      }}>
        <div style={{ backgroundColor: '#fff', padding: '2rem', borderRadius: '8px' }}>
          Loading pending decision...
        </div>
      </div>
    )
  }

  if (!decision) {
    return (
      <div className="modal-overlay" style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
      }}>
        <div style={{
          backgroundColor: '#fff',
          padding: '2rem',
          borderRadius: '12px',
          textAlign: 'center',
        }}>
          <h3>No Pending Decisions</h3>
          <p>All evidence has been processed.</p>
          <button
            onClick={onClose}
            style={{
              padding: '0.75rem 1.5rem',
              borderRadius: '6px',
              border: 'none',
              backgroundColor: '#1565C0',
              color: '#fff',
              cursor: 'pointer',
            }}
          >
            Close
          </button>
        </div>
      </div>
    )
  }

  const relColor = RELATIONSHIP_COLORS[decision.fragment.relationship_type] || { bg: '#f5f5f5', text: '#333', label: decision.fragment.relationship_type }

  return (
    <div className="modal-overlay" style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      padding: '1rem',
    }}>
      <div className="modal-content" style={{
        backgroundColor: '#fff',
        borderRadius: '12px',
        width: '100%',
        maxWidth: '800px',
        maxHeight: '90vh',
        overflow: 'auto',
        boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
      }}>
        {/* Header */}
        <div style={{
          padding: '1.25rem 1.5rem',
          borderBottom: '1px solid #e8e8e8',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          backgroundColor: '#f8f9fa',
        }}>
          <div>
            <h2 style={{ margin: 0, fontSize: '1.1rem' }}>
              Pending Decision {decision.decision_index} of {decision.total_pending}
            </h2>
          </div>
          <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
            <button
              onClick={() => loadDecision(Math.max(0, currentIndex - 1))}
              disabled={currentIndex === 0}
              style={{
                padding: '0.5rem 1rem',
                borderRadius: '6px',
                border: '1px solid #ddd',
                backgroundColor: '#fff',
                cursor: currentIndex === 0 ? 'not-allowed' : 'pointer',
                opacity: currentIndex === 0 ? 0.5 : 1,
              }}
            >
              Prev
            </button>
            <button
              onClick={() => loadDecision(currentIndex + 1)}
              disabled={decision.decision_index >= decision.total_pending}
              style={{
                padding: '0.5rem 1rem',
                borderRadius: '6px',
                border: '1px solid #ddd',
                backgroundColor: '#fff',
                cursor: decision.decision_index >= decision.total_pending ? 'not-allowed' : 'pointer',
                opacity: decision.decision_index >= decision.total_pending ? 0.5 : 1,
              }}
            >
              Next
            </button>
            <button
              onClick={onClose}
              style={{
                background: 'none',
                border: 'none',
                fontSize: '1.5rem',
                cursor: 'pointer',
                color: '#666',
                marginLeft: '0.5rem',
              }}
            >
              &times;
            </button>
          </div>
        </div>

        <div style={{ padding: '1.5rem' }}>
          {error && (
            <div style={{
              backgroundColor: '#fee',
              border: '1px solid #fcc',
              padding: '0.75rem',
              borderRadius: '6px',
              marginBottom: '1rem',
              color: '#c00',
            }}>
              {error}
            </div>
          )}

          {/* Evidence Fragment */}
          <div style={{
            backgroundColor: '#f5f5f5',
            padding: '1.25rem',
            borderRadius: '8px',
            marginBottom: '1rem',
            borderLeft: '4px solid #1565C0',
          }}>
            <div style={{ fontSize: '0.8rem', color: '#666', marginBottom: '0.5rem', textTransform: 'uppercase' }}>
              Evidence Fragment
            </div>
            <div style={{ fontSize: '1.1rem', lineHeight: 1.6, fontStyle: 'italic' }}>
              "{decision.fragment.content}"
            </div>
            <div style={{ marginTop: '0.75rem', fontSize: '0.9rem', color: '#666' }}>
              — {decision.fragment.source_name}
            </div>
          </div>

          {/* Relationship & Target */}
          <div style={{
            display: 'flex',
            gap: '1rem',
            marginBottom: '1rem',
            flexWrap: 'wrap',
          }}>
            <div style={{
              backgroundColor: relColor.bg,
              color: relColor.text,
              padding: '0.5rem 1rem',
              borderRadius: '6px',
              fontWeight: 500,
            }}>
              {relColor.label}
            </div>
            {decision.fragment.target_dimension_name && (
              <div style={{
                backgroundColor: '#e8e8e8',
                padding: '0.5rem 1rem',
                borderRadius: '6px',
              }}>
                {decision.fragment.target_dimension_name} &gt; {decision.fragment.target_operation_name}
              </div>
            )}
            <div style={{
              backgroundColor: '#fff3cd',
              padding: '0.5rem 1rem',
              borderRadius: '6px',
            }}>
              Confidence: {Math.round((decision.fragment.confidence || 0) * 100)}%
            </div>
          </div>

          {/* Why needs decision */}
          {decision.fragment.why_needs_decision && (
            <div style={{
              backgroundColor: '#fff8e1',
              padding: '1rem',
              borderRadius: '8px',
              marginBottom: '1.5rem',
              borderLeft: '4px solid #ffc107',
            }}>
              <div style={{ fontSize: '0.8rem', color: '#856404', marginBottom: '0.5rem', textTransform: 'uppercase', fontWeight: 600 }}>
                Why This Needs Your Input
              </div>
              <div style={{ lineHeight: 1.6 }}>
                {decision.fragment.why_needs_decision}
              </div>
            </div>
          )}

          {/* Interpretation Options */}
          <div style={{
            borderTop: '2px solid #e8e8e8',
            paddingTop: '1.5rem',
            marginTop: '1rem',
          }}>
            <h3 style={{ margin: '0 0 1rem 0', fontSize: '1rem', textTransform: 'uppercase', color: '#666' }}>
              Interpretation Options
            </h3>

            {decision.interpretations.map((interp, idx) => (
              <div
                key={interp.id}
                onClick={() => setSelectedInterpretation(interp.id)}
                style={{
                  border: selectedInterpretation === interp.id ? '2px solid #1565C0' : '1px solid #ddd',
                  borderRadius: '8px',
                  padding: '1rem',
                  marginBottom: '1rem',
                  cursor: 'pointer',
                  backgroundColor: selectedInterpretation === interp.id ? '#E3F2FD' : '#fff',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', marginBottom: '0.75rem' }}>
                  <input
                    type="radio"
                    checked={selectedInterpretation === interp.id}
                    onChange={() => setSelectedInterpretation(interp.id)}
                    style={{ marginRight: '0.75rem' }}
                  />
                  <span style={{ fontWeight: 600 }}>
                    Option {interp.interpretation_key?.toUpperCase() || String.fromCharCode(65 + idx)}: {interp.title}
                  </span>
                  {interp.is_recommended && (
                    <span style={{
                      marginLeft: '0.75rem',
                      backgroundColor: '#2E7D32',
                      color: '#fff',
                      padding: '0.2rem 0.5rem',
                      borderRadius: '4px',
                      fontSize: '0.75rem',
                    }}>
                      Recommended
                    </span>
                  )}
                </div>

                {interp.strategy && (
                  <div style={{ marginBottom: '0.75rem', color: '#555', lineHeight: 1.5 }}>
                    {interp.strategy}
                  </div>
                )}

                {/* Structural Changes */}
                {interp.structural_changes?.length > 0 && (
                  <div style={{
                    backgroundColor: '#f8f9fa',
                    padding: '0.75rem',
                    borderRadius: '6px',
                    marginTop: '0.75rem',
                  }}>
                    {interp.structural_changes.map((change, cIdx) => (
                      <div key={change.id || cIdx} style={{ marginBottom: cIdx < interp.structural_changes.length - 1 ? '0.75rem' : 0 }}>
                        <div style={{ fontSize: '0.8rem', color: '#666', marginBottom: '0.25rem' }}>
                          {change.change_type?.toUpperCase()} {change.target_operation_name && `→ ${change.target_operation_name}`}
                        </div>
                        {change.before_content && (
                          <div style={{
                            backgroundColor: '#ffebee',
                            padding: '0.5rem',
                            borderRadius: '4px',
                            marginBottom: '0.5rem',
                            fontSize: '0.9rem',
                          }}>
                            <strong>Before:</strong> {change.before_content}
                          </div>
                        )}
                        {change.after_content && (
                          <div style={{
                            backgroundColor: '#e8f5e9',
                            padding: '0.5rem',
                            borderRadius: '4px',
                            fontSize: '0.9rem',
                          }}>
                            <strong>After:</strong> {change.after_content}
                          </div>
                        )}

                        {/* Commitment & Foreclosure */}
                        {(change.commitment_statement || change.foreclosure_statements?.length > 0) && (
                          <div style={{ marginTop: '0.75rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
                            {change.commitment_statement && (
                              <div style={{ flex: 1, minWidth: '200px' }}>
                                <div style={{ fontSize: '0.75rem', color: '#2E7D32', marginBottom: '0.25rem', fontWeight: 600 }}>
                                  COMMIT
                                </div>
                                <div style={{ fontSize: '0.85rem', color: '#333' }}>
                                  {change.commitment_statement}
                                </div>
                              </div>
                            )}
                            {change.foreclosure_statements?.length > 0 && (
                              <div style={{ flex: 1, minWidth: '200px' }}>
                                <div style={{ fontSize: '0.75rem', color: '#C62828', marginBottom: '0.25rem', fontWeight: 600 }}>
                                  FORECLOSE
                                </div>
                                <ul style={{ margin: 0, paddingLeft: '1.25rem', fontSize: '0.85rem', color: '#333' }}>
                                  {change.foreclosure_statements.map((f, fIdx) => (
                                    <li key={fIdx}>{f}</li>
                                  ))}
                                </ul>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Action Buttons */}
          <div style={{
            display: 'flex',
            gap: '1rem',
            justifyContent: 'flex-end',
            marginTop: '1.5rem',
            paddingTop: '1rem',
            borderTop: '1px solid #e8e8e8',
          }}>
            <button
              onClick={handleSkip}
              disabled={submitting}
              style={{
                padding: '0.75rem 1.5rem',
                borderRadius: '6px',
                border: '1px solid #ddd',
                backgroundColor: '#fff',
                cursor: submitting ? 'not-allowed' : 'pointer',
                fontSize: '1rem',
              }}
            >
              Skip for Now
            </button>
            <button
              onClick={handleSubmit}
              disabled={!selectedInterpretation || submitting}
              style={{
                padding: '0.75rem 1.5rem',
                borderRadius: '6px',
                border: 'none',
                backgroundColor: selectedInterpretation ? '#1565C0' : '#ccc',
                color: '#fff',
                cursor: !selectedInterpretation || submitting ? 'not-allowed' : 'pointer',
                fontSize: '1rem',
                fontWeight: 500,
              }}
            >
              {submitting ? 'Applying...' : 'Apply Selected Option'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default EvidenceDecisionView
