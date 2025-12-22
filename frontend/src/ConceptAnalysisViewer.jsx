import { useState, useEffect } from 'react'

const API_URL = import.meta.env.VITE_API_URL || 'https://theory-api.onrender.com'

// API helper
async function api(endpoint) {
  const response = await fetch(`${API_URL}${endpoint}`, {
    headers: { 'Content-Type': 'application/json' },
  })
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }))
    throw new Error(error.detail || 'Request failed')
  }
  return response.json()
}

// Dimension color map matching the backend
const DIMENSION_COLORS = {
  positional: { bg: '#E3F2FD', text: '#1565C0', border: '#90CAF9' },
  genealogical: { bg: '#FFF3E0', text: '#E65100', border: '#FFCC80' },
  presuppositional: { bg: '#FCE4EC', text: '#AD1457', border: '#F48FB1' },
  commitment: { bg: '#F3E5F5', text: '#7B1FA2', border: '#CE93D8' },
  affordance: { bg: '#E8F5E9', text: '#2E7D32', border: '#A5D6A7' },
  normalization: { bg: '#FFEBEE', text: '#C62828', border: '#EF9A9A' },
  boundary: { bg: '#E0F7FA', text: '#00838F', border: '#80DEEA' },
  dynamic: { bg: '#FFF8E1', text: '#F57F17', border: '#FFE082' },
}

// Dimension icons/emojis
const DIMENSION_ICONS = {
  positional: '📍',
  genealogical: '🌳',
  presuppositional: '🔍',
  commitment: '🤝',
  affordance: '🚀',
  normalization: '⚖️',
  boundary: '🔲',
  dynamic: '🔄',
}

function DimensionCard({ dimension, analyses, expanded, onToggle }) {
  const colors = DIMENSION_COLORS[dimension.dimension_type] || { bg: '#f5f5f5', text: '#333', border: '#ddd' }
  const icon = DIMENSION_ICONS[dimension.dimension_type] || '📊'
  const dimensionAnalyses = analyses || []

  return (
    <div
      className="dimension-card"
      style={{
        backgroundColor: colors.bg,
        borderLeft: `4px solid ${colors.border}`,
        marginBottom: '1rem',
        borderRadius: '8px',
        overflow: 'hidden',
      }}
    >
      <div
        className="dimension-header"
        onClick={onToggle}
        style={{
          padding: '1rem',
          cursor: 'pointer',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <div>
          <span style={{ fontSize: '1.5rem', marginRight: '0.5rem' }}>{icon}</span>
          <span style={{ fontWeight: 600, color: colors.text, fontSize: '1.1rem' }}>
            {dimension.name}
          </span>
          <span style={{ marginLeft: '0.75rem', color: '#666', fontSize: '0.9rem' }}>
            {dimensionAnalyses.length} analyses
          </span>
        </div>
        <span style={{ fontSize: '1.2rem', color: colors.text }}>
          {expanded ? '▼' : '▶'}
        </span>
      </div>

      {expanded && (
        <div style={{ padding: '0 1rem 1rem' }}>
          <div style={{ fontStyle: 'italic', color: '#666', marginBottom: '1rem', fontSize: '0.95rem' }}>
            {dimension.core_question}
          </div>

          {dimension.operations?.map(op => {
            const opAnalysis = dimensionAnalyses.find(a => a.operation_id === op.id)
            return (
              <OperationSection
                key={op.id}
                operation={op}
                analysis={opAnalysis}
                colors={colors}
              />
            )
          })}
        </div>
      )}
    </div>
  )
}

function OperationSection({ operation, analysis, colors }) {
  const [expanded, setExpanded] = useState(false)

  return (
    <div
      style={{
        backgroundColor: 'rgba(255,255,255,0.7)',
        borderRadius: '6px',
        marginBottom: '0.75rem',
        border: `1px solid ${colors.border}`,
      }}
    >
      <div
        onClick={() => setExpanded(!expanded)}
        style={{
          padding: '0.75rem 1rem',
          cursor: 'pointer',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start',
        }}
      >
        <div>
          <div style={{ fontWeight: 500, color: colors.text, marginBottom: '0.25rem' }}>
            {operation.name}
          </div>
          <div style={{ fontSize: '0.85rem', color: '#666' }}>
            {operation.description}
          </div>
          {operation.influences?.length > 0 && (
            <div style={{ fontSize: '0.8rem', color: '#888', marginTop: '0.25rem' }}>
              Influences: {operation.influences.map(i => i.short_name).join(', ')}
            </div>
          )}
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          {analysis && (
            <span style={{
              backgroundColor: colors.text,
              color: '#fff',
              padding: '0.2rem 0.5rem',
              borderRadius: '4px',
              fontSize: '0.75rem',
            }}>
              {analysis.items?.length || 0} items
            </span>
          )}
          <span style={{ color: colors.text }}>{expanded ? '−' : '+'}</span>
        </div>
      </div>

      {expanded && analysis && (
        <div style={{ padding: '0 1rem 1rem', borderTop: `1px solid ${colors.border}` }}>
          {analysis.canonical_statement && (
            <div style={{
              backgroundColor: 'rgba(0,0,0,0.03)',
              padding: '0.75rem',
              borderRadius: '4px',
              marginTop: '0.75rem',
              fontStyle: 'italic',
            }}>
              <strong>Summary:</strong> {analysis.canonical_statement}
            </div>
          )}

          {analysis.items?.length > 0 && (
            <div style={{ marginTop: '0.75rem' }}>
              <div style={{ fontWeight: 500, marginBottom: '0.5rem', fontSize: '0.9rem' }}>
                Analysis Items:
              </div>
              {analysis.items.map((item, idx) => (
                <div
                  key={item.id || idx}
                  style={{
                    padding: '0.5rem 0.75rem',
                    marginBottom: '0.5rem',
                    backgroundColor: '#fff',
                    borderRadius: '4px',
                    border: '1px solid #eee',
                  }}
                >
                  <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'flex-start' }}>
                    <span style={{
                      backgroundColor: colors.bg,
                      color: colors.text,
                      padding: '0.1rem 0.4rem',
                      borderRadius: '3px',
                      fontSize: '0.75rem',
                      fontWeight: 500,
                      flexShrink: 0,
                    }}>
                      {item.item_type.replace(/_/g, ' ')}
                    </span>
                    <span style={{ fontSize: '0.9rem' }}>{item.content}</span>
                  </div>
                  {item.severity && (
                    <div style={{ fontSize: '0.8rem', color: '#888', marginTop: '0.25rem' }}>
                      Severity: {item.severity}
                    </div>
                  )}
                  {item.strength !== null && item.strength !== undefined && (
                    <div style={{ fontSize: '0.8rem', color: '#888', marginTop: '0.25rem' }}>
                      Strength: {Math.round(item.strength * 100)}%
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {operation.key_questions?.length > 0 && (
            <div style={{ marginTop: '0.75rem' }}>
              <div style={{ fontWeight: 500, marginBottom: '0.5rem', fontSize: '0.9rem', color: '#666' }}>
                Key Questions:
              </div>
              <ul style={{ margin: 0, paddingLeft: '1.25rem', color: '#666', fontSize: '0.85rem' }}>
                {operation.key_questions.map((q, i) => (
                  <li key={i} style={{ marginBottom: '0.25rem' }}>{q}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {expanded && !analysis && (
        <div style={{
          padding: '1rem',
          color: '#999',
          fontStyle: 'italic',
          borderTop: `1px solid ${colors.border}`,
        }}>
          No analysis data for this operation yet.
        </div>
      )}
    </div>
  )
}

function SchemaOverview({ overview }) {
  return (
    <div style={{
      backgroundColor: '#f8f9fa',
      padding: '1.5rem',
      borderRadius: '8px',
      marginBottom: '1.5rem',
    }}>
      <h3 style={{ marginTop: 0, marginBottom: '1rem' }}>Schema Overview</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '1rem' }}>
        <div style={{ textAlign: 'center', padding: '1rem', backgroundColor: '#fff', borderRadius: '6px' }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#1565C0' }}>{overview.dimensions_count}</div>
          <div style={{ color: '#666', fontSize: '0.9rem' }}>Dimensions</div>
        </div>
        <div style={{ textAlign: 'center', padding: '1rem', backgroundColor: '#fff', borderRadius: '6px' }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#2E7D32' }}>{overview.operations_count}</div>
          <div style={{ color: '#666', fontSize: '0.9rem' }}>Operations</div>
        </div>
        <div style={{ textAlign: 'center', padding: '1rem', backgroundColor: '#fff', borderRadius: '6px' }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#7B1FA2' }}>{overview.influences_count}</div>
          <div style={{ color: '#666', fontSize: '0.9rem' }}>Influences</div>
        </div>
        <div style={{ textAlign: 'center', padding: '1rem', backgroundColor: '#fff', borderRadius: '6px' }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#E65100' }}>{overview.concepts_count}</div>
          <div style={{ color: '#666', fontSize: '0.9rem' }}>Concepts</div>
        </div>
        <div style={{ textAlign: 'center', padding: '1rem', backgroundColor: '#fff', borderRadius: '6px' }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#C62828' }}>{overview.analyses_count}</div>
          <div style={{ color: '#666', fontSize: '0.9rem' }}>Analyses</div>
        </div>
      </div>

      <div style={{ marginTop: '1.5rem' }}>
        <h4 style={{ marginBottom: '0.5rem' }}>Theoretical Influences</h4>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
          {overview.influences?.map(inf => (
            <span
              key={inf.short_name}
              style={{
                backgroundColor: '#e3e8ee',
                padding: '0.3rem 0.75rem',
                borderRadius: '20px',
                fontSize: '0.85rem',
              }}
              title={inf.full_name}
            >
              {inf.short_name}
            </span>
          ))}
        </div>
      </div>
    </div>
  )
}

function ConceptAnalysisViewer() {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [overview, setOverview] = useState(null)
  const [concepts, setConcepts] = useState([])
  const [selectedConcept, setSelectedConcept] = useState(null)
  const [fullAnalysis, setFullAnalysis] = useState(null)
  const [expandedDimensions, setExpandedDimensions] = useState({})

  // Load initial data
  useEffect(() => {
    const loadData = async () => {
      setLoading(true)
      try {
        const [overviewData, conceptsData] = await Promise.all([
          api('/concept-analysis/schema-overview'),
          api('/concept-analysis/concepts'),
        ])
        setOverview(overviewData)
        setConcepts(conceptsData)

        // Auto-select first concept if available
        if (conceptsData.length > 0) {
          loadConceptAnalysis(conceptsData[0].id)
        }
      } catch (err) {
        setError(err.message)
      }
      setLoading(false)
    }
    loadData()
  }, [])

  const loadConceptAnalysis = async (conceptId) => {
    try {
      const data = await api(`/concept-analysis/concepts/${conceptId}`)
      setFullAnalysis(data)
      setSelectedConcept(conceptId)
      // Expand first dimension by default
      if (data.dimensions?.length > 0) {
        setExpandedDimensions({ [data.dimensions[0].dimension_type]: true })
      }
    } catch (err) {
      setError(err.message)
    }
  }

  const toggleDimension = (dimType) => {
    setExpandedDimensions(prev => ({
      ...prev,
      [dimType]: !prev[dimType],
    }))
  }

  const expandAll = () => {
    const allExpanded = {}
    fullAnalysis?.dimensions?.forEach(d => {
      allExpanded[d.dimension_type] = true
    })
    setExpandedDimensions(allExpanded)
  }

  const collapseAll = () => {
    setExpandedDimensions({})
  }

  if (loading) {
    return <div className="loading">Loading Concept Analysis Framework...</div>
  }

  if (error) {
    return <div className="error-alert">Error: {error}</div>
  }

  return (
    <div className="content full-width">
      <div className="card">
        <div className="card-header">
          <h2>8-Dimensional Concept Analysis</h2>
          <div style={{ fontSize: '0.9rem', color: '#666' }}>
            Operation-indexed philosophical framework
          </div>
        </div>
        <div className="card-body">
          {overview && <SchemaOverview overview={overview} />}

          {/* Concept selector */}
          {concepts.length > 0 && (
            <div style={{ marginBottom: '1.5rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>
                Select Concept to Analyze:
              </label>
              <select
                value={selectedConcept || ''}
                onChange={(e) => loadConceptAnalysis(parseInt(e.target.value))}
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  fontSize: '1rem',
                  borderRadius: '6px',
                  border: '1px solid #ddd',
                }}
              >
                {concepts.map(c => (
                  <option key={c.id} value={c.id}>
                    {c.term} ({c.analysis_count} analyses)
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* Full analysis view */}
          {fullAnalysis && (
            <>
              {/* Concept header */}
              <div style={{
                backgroundColor: '#1a1a2e',
                color: '#fff',
                padding: '1.5rem',
                borderRadius: '8px',
                marginBottom: '1.5rem',
              }}>
                <h2 style={{ margin: 0, marginBottom: '0.75rem' }}>
                  {fullAnalysis.concept.term}
                </h2>
                <p style={{ margin: 0, opacity: 0.9, lineHeight: 1.6 }}>
                  {fullAnalysis.concept.definition}
                </p>
                <div style={{ marginTop: '1rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
                  {fullAnalysis.concept.paradigm && (
                    <span style={{ backgroundColor: 'rgba(255,255,255,0.2)', padding: '0.25rem 0.75rem', borderRadius: '4px', fontSize: '0.85rem' }}>
                      {fullAnalysis.concept.paradigm}
                    </span>
                  )}
                  {fullAnalysis.concept.disciplinary_home && (
                    <span style={{ backgroundColor: 'rgba(255,255,255,0.2)', padding: '0.25rem 0.75rem', borderRadius: '4px', fontSize: '0.85rem' }}>
                      {fullAnalysis.concept.disciplinary_home}
                    </span>
                  )}
                </div>
              </div>

              {/* Expand/Collapse buttons */}
              <div style={{ marginBottom: '1rem', display: 'flex', gap: '0.5rem' }}>
                <button className="btn btn-secondary btn-sm" onClick={expandAll}>
                  Expand All
                </button>
                <button className="btn btn-secondary btn-sm" onClick={collapseAll}>
                  Collapse All
                </button>
              </div>

              {/* Dimensions */}
              {fullAnalysis.dimensions?.map(dim => (
                <DimensionCard
                  key={dim.dimension_type}
                  dimension={dim}
                  analyses={fullAnalysis.analyses_by_dimension?.[dim.dimension_type]}
                  expanded={expandedDimensions[dim.dimension_type]}
                  onToggle={() => toggleDimension(dim.dimension_type)}
                />
              ))}
            </>
          )}

          {concepts.length === 0 && (
            <div className="empty-state">
              <h3>No concepts analyzed yet</h3>
              <p>Run the seed script to populate with Tech Sovereignty analysis</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ConceptAnalysisViewer
