import { useState, useEffect } from 'react'
import AddEvidenceSource from './components/AddEvidenceSource'
import EvidenceDecisionView from './components/EvidenceDecisionView'

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

// Format item content - parse JSON-like strings and display nicely
function formatItemContent(content, itemType) {
  // Try to parse if it looks like a dict/object representation
  if (content.startsWith('{') && content.includes(':')) {
    try {
      // Convert Python-style dict to JSON
      const jsonStr = content
        .replace(/'/g, '"')
        .replace(/None/g, 'null')
        .replace(/True/g, 'true')
        .replace(/False/g, 'false')
      const parsed = JSON.parse(jsonStr)

      // Format based on what fields are present
      if (parsed.year && parsed.event) {
        return (
          <div>
            <strong>{parsed.year}</strong>: {parsed.event}
            {parsed.impact && <div style={{ color: '#666', marginTop: '0.25rem', fontSize: '0.85rem' }}>Impact: {parsed.impact}</div>}
          </div>
        )
      }
      if (parsed.from && parsed.to) {
        return <span>{parsed.from} → {parsed.to}</span>
      }
      if (parsed.statement) {
        return <span>{parsed.statement}</span>
      }
      // Generic object display
      return (
        <div>
          {Object.entries(parsed).map(([k, v]) => (
            <div key={k} style={{ marginBottom: '0.15rem' }}>
              <strong style={{ textTransform: 'capitalize' }}>{k.replace(/_/g, ' ')}</strong>: {String(v)}
            </div>
          ))}
        </div>
      )
    } catch (e) {
      // Not valid JSON, return as-is
    }
  }
  return content
}

// Group items by type for better organization
function groupItemsByType(items) {
  const groups = {}
  items?.forEach(item => {
    const type = item.item_type
    if (!groups[type]) groups[type] = []
    groups[type].push(item)
  })
  return groups
}

// Get a nice label for item types
function getItemTypeLabel(type) {
  const labels = {
    'conditions_of_possibility': 'Conditions of Possibility',
    'key_moments': 'Key Historical Moments',
    'forward_inference': 'Forward Inferences',
    'backward_inference': 'Backward Inferences',
    'lateral_inference': 'Lateral Inferences',
    'commitment': 'Commitments',
    'hard_commitment': 'Hard Commitments',
    'soft_commitment': 'Soft Commitments',
    'anomaly': 'Anomalies',
    'contradiction': 'Contradictions',
    'gray_zone': 'Gray Zones',
    'looping_effect': 'Looping Effects',
    'visibility': 'What Becomes Visible',
    'invisibility': 'What Becomes Invisible',
    'transformation': 'Transformation Vectors',
    'vocabulary_addition': 'Vocabulary Additions',
    'norm': 'Embedded Norms',
    'authority': 'Authority Relations',
    'assumption': 'Assumptions',
    'given': 'Taken-for-Granted',
  }
  return labels[type] || type.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
}

// Provenance badge component
function ProvenanceBadge({ item }) {
  const provType = item.provenance_type || item.created_via || 'wizard'
  const badgeStyles = {
    wizard: { bg: '#e3e8ee', text: '#5c6773', label: 'wizard' },
    evidence: { bg: '#e8f5e9', text: '#2e7d32', label: 'evidence' },
    evidence_auto_integrate: { bg: '#e8f5e9', text: '#2e7d32', label: 'auto' },
    evidence_decision: { bg: '#fff3e0', text: '#e65100', label: 'decision' },
    user_manual: { bg: '#e3f2fd', text: '#1565c0', label: 'manual' },
    initial_wizard: { bg: '#e3e8ee', text: '#5c6773', label: 'wizard' },
  }
  const style = badgeStyles[provType] || badgeStyles.wizard

  return (
    <span style={{
      backgroundColor: style.bg,
      color: style.text,
      padding: '0.15rem 0.4rem',
      borderRadius: '4px',
      fontSize: '0.7rem',
      fontWeight: 500,
      marginLeft: '0.5rem',
    }}>
      {style.label}
    </span>
  )
}

// Web Centrality badge
function CentralityBadge({ centrality }) {
  if (!centrality) return null
  const styles = {
    core: { bg: '#c62828', text: '#fff', label: 'Core' },
    high: { bg: '#e65100', text: '#fff', label: 'High' },
    medium: { bg: '#f9a825', text: '#000', label: 'Medium' },
    peripheral: { bg: '#9e9e9e', text: '#fff', label: 'Peripheral' },
  }
  const style = styles[centrality] || styles.medium
  return (
    <span style={{
      backgroundColor: style.bg,
      color: style.text,
      padding: '0.15rem 0.5rem',
      borderRadius: '4px',
      fontSize: '0.7rem',
      fontWeight: 500,
      marginLeft: '0.5rem',
    }}>
      {style.label}
    </span>
  )
}

// Reasoning Scaffold Display - The Quinean intermediate layer
function ReasoningScaffoldDisplay({ scaffold, itemContent }) {
  const [expanded, setExpanded] = useState(false)

  if (!scaffold) return null

  return (
    <div style={{ marginTop: '0.75rem' }}>
      <button
        onClick={() => setExpanded(!expanded)}
        style={{
          background: 'none',
          border: '1px solid #e0e0e0',
          borderRadius: '4px',
          padding: '0.35rem 0.75rem',
          cursor: 'pointer',
          fontSize: '0.8rem',
          color: '#666',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
        }}
      >
        <span style={{ fontSize: '1rem' }}>{expanded ? '▾' : '▸'}</span>
        Show Reasoning
      </button>

      {expanded && (
        <div style={{
          marginTop: '0.75rem',
          backgroundColor: '#f8f9fa',
          borderRadius: '8px',
          padding: '1rem',
          border: '1px solid #e0e0e0',
        }}>
          {/* Inference Type */}
          {scaffold.inference_type && (
            <div style={{ marginBottom: '1rem' }}>
              <div style={{ fontSize: '0.75rem', color: '#666', textTransform: 'uppercase', marginBottom: '0.25rem' }}>
                Inference Type
              </div>
              <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                <span style={{
                  backgroundColor: '#1565C0',
                  color: '#fff',
                  padding: '0.2rem 0.5rem',
                  borderRadius: '4px',
                  fontSize: '0.8rem',
                  fontWeight: 500,
                }}>
                  {scaffold.inference_type}
                </span>
                {scaffold.inference_rule && (
                  <span style={{ color: '#666', fontSize: '0.85rem' }}>
                    via {scaffold.inference_rule}
                  </span>
                )}
              </div>
            </div>
          )}

          {/* Premises */}
          {scaffold.premises?.length > 0 && (
            <div style={{ marginBottom: '1rem' }}>
              <div style={{ fontSize: '0.75rem', color: '#666', textTransform: 'uppercase', marginBottom: '0.5rem' }}>
                From Premises
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {scaffold.premises.map((premise, i) => (
                  <div key={i} style={{
                    backgroundColor: '#fff',
                    padding: '0.5rem 0.75rem',
                    borderRadius: '4px',
                    borderLeft: `3px solid ${premise.centrality === 'core' ? '#c62828' : premise.centrality === 'high' ? '#e65100' : '#9e9e9e'}`,
                  }}>
                    <div style={{ fontSize: '0.9rem', marginBottom: '0.25rem' }}>{premise.claim}</div>
                    <div style={{ display: 'flex', gap: '0.5rem', fontSize: '0.75rem', color: '#888' }}>
                      <span style={{
                        backgroundColor: '#e8e8e8',
                        padding: '0.1rem 0.4rem',
                        borderRadius: '3px',
                      }}>
                        {premise.claim_type}
                      </span>
                      <span style={{
                        backgroundColor: '#e8e8e8',
                        padding: '0.1rem 0.4rem',
                        borderRadius: '3px',
                      }}>
                        {premise.centrality}
                      </span>
                      <span style={{
                        backgroundColor: '#e8e8e8',
                        padding: '0.1rem 0.4rem',
                        borderRadius: '3px',
                      }}>
                        {premise.source}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Reasoning Trace */}
          {scaffold.reasoning_trace && (
            <div style={{ marginBottom: '1rem' }}>
              <div style={{ fontSize: '0.75rem', color: '#666', textTransform: 'uppercase', marginBottom: '0.25rem' }}>
                Reasoning Trace
              </div>
              <div style={{
                backgroundColor: '#fff',
                padding: '0.75rem',
                borderRadius: '4px',
                fontSize: '0.9rem',
                lineHeight: 1.5,
                fontStyle: 'italic',
                color: '#444',
              }}>
                {scaffold.reasoning_trace}
              </div>
            </div>
          )}

          {/* Source Context */}
          {(scaffold.source_passage || scaffold.derivation_trigger) && (
            <div style={{ marginBottom: '1rem' }}>
              <div style={{ fontSize: '0.75rem', color: '#666', textTransform: 'uppercase', marginBottom: '0.25rem' }}>
                Triggered By
              </div>
              <div style={{
                backgroundColor: '#e3f2fd',
                padding: '0.75rem',
                borderRadius: '4px',
              }}>
                {scaffold.derivation_trigger && (
                  <div style={{ fontSize: '0.8rem', color: '#1565C0', marginBottom: '0.25rem' }}>
                    Source: {scaffold.derivation_trigger}
                  </div>
                )}
                {scaffold.source_passage && (
                  <div style={{ fontSize: '0.85rem', fontStyle: 'italic' }}>
                    "{scaffold.source_passage}"
                  </div>
                )}
                {scaffold.source_location && (
                  <div style={{ fontSize: '0.75rem', color: '#666', marginTop: '0.25rem' }}>
                    Location: {scaffold.source_location}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Confidence Decomposition */}
          {(scaffold.premise_confidence || scaffold.inference_validity || scaffold.web_coherence) && (
            <div style={{ marginBottom: '1rem' }}>
              <div style={{ fontSize: '0.75rem', color: '#666', textTransform: 'uppercase', marginBottom: '0.5rem' }}>
                Confidence Decomposition
              </div>
              <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', marginBottom: '0.5rem' }}>
                {scaffold.premise_confidence && (
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '1.1rem', fontWeight: 'bold', color: '#2E7D32' }}>
                      {Math.round(scaffold.premise_confidence * 100)}%
                    </div>
                    <div style={{ fontSize: '0.7rem', color: '#666' }}>Premise</div>
                  </div>
                )}
                {scaffold.inference_validity && (
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '1.1rem', fontWeight: 'bold', color: '#1565C0' }}>
                      {Math.round(scaffold.inference_validity * 100)}%
                    </div>
                    <div style={{ fontSize: '0.7rem', color: '#666' }}>Inference</div>
                  </div>
                )}
                {scaffold.source_quality && (
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '1.1rem', fontWeight: 'bold', color: '#7B1FA2' }}>
                      {Math.round(scaffold.source_quality * 100)}%
                    </div>
                    <div style={{ fontSize: '0.7rem', color: '#666' }}>Source</div>
                  </div>
                )}
                {scaffold.web_coherence && (
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '1.1rem', fontWeight: 'bold', color: '#E65100' }}>
                      {Math.round(scaffold.web_coherence * 100)}%
                    </div>
                    <div style={{ fontSize: '0.7rem', color: '#666' }}>Coherence</div>
                  </div>
                )}
              </div>
              {scaffold.confidence_explanation && (
                <div style={{ fontSize: '0.85rem', color: '#555', fontStyle: 'italic' }}>
                  {scaffold.confidence_explanation}
                </div>
              )}
            </div>
          )}

          {/* Alternatives Rejected */}
          {scaffold.alternatives_rejected?.length > 0 && (
            <div style={{ marginBottom: '1rem' }}>
              <div style={{ fontSize: '0.75rem', color: '#666', textTransform: 'uppercase', marginBottom: '0.5rem' }}>
                Alternatives Considered
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {scaffold.alternatives_rejected.map((alt, i) => (
                  <div key={i} style={{
                    backgroundColor: '#ffebee',
                    padding: '0.5rem 0.75rem',
                    borderRadius: '4px',
                    borderLeft: '3px solid #c62828',
                  }}>
                    <div style={{ fontSize: '0.85rem', color: '#c62828', marginBottom: '0.25rem' }}>
                      ✗ {alt.inference}
                    </div>
                    <div style={{ fontSize: '0.8rem', color: '#666' }}>
                      Rejected: {alt.rejected_because}
                    </div>
                    {alt.plausibility && (
                      <div style={{ fontSize: '0.75rem', color: '#888', marginTop: '0.25rem' }}>
                        Plausibility: {Math.round(alt.plausibility * 100)}%
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Revisability Cost */}
          {scaffold.revisability_cost && (
            <div style={{ marginBottom: '1rem' }}>
              <div style={{ fontSize: '0.75rem', color: '#666', textTransform: 'uppercase', marginBottom: '0.25rem' }}>
                Revisability Cost (Quine)
              </div>
              <div style={{
                backgroundColor: '#fff3e0',
                padding: '0.75rem',
                borderRadius: '4px',
                fontSize: '0.85rem',
                color: '#e65100',
              }}>
                {scaffold.revisability_cost}
              </div>
            </div>
          )}

          {/* Dependent Claims */}
          {scaffold.dependent_claims?.length > 0 && (
            <div>
              <div style={{ fontSize: '0.75rem', color: '#666', textTransform: 'uppercase', marginBottom: '0.25rem' }}>
                Depends On
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem' }}>
                {scaffold.dependent_claims.map((claim, i) => (
                  <span key={i} style={{
                    backgroundColor: '#e8e8e8',
                    padding: '0.2rem 0.5rem',
                    borderRadius: '4px',
                    fontSize: '0.75rem',
                  }}>
                    {claim}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

// Evidence Dashboard component
function EvidenceDashboard({ conceptId, onOpenAddSource, onOpenDecisions }) {
  const [progress, setProgress] = useState(null)
  const [sources, setSources] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!conceptId) return
    loadData()
  }, [conceptId])

  const loadData = async () => {
    setLoading(true)
    try {
      const [progressData, sourcesData] = await Promise.all([
        api(`/concepts/${conceptId}/evidence/progress`),
        api(`/concepts/${conceptId}/evidence/sources`),
      ])
      setProgress(progressData)
      setSources(sourcesData)
    } catch (err) {
      console.error('Failed to load evidence data:', err)
    }
    setLoading(false)
  }

  if (loading) {
    return <div style={{ padding: '2rem', textAlign: 'center', color: '#666' }}>Loading evidence data...</div>
  }

  return (
    <div>
      {/* Progress Cards */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
        gap: '1rem',
        marginBottom: '1.5rem',
      }}>
        <div style={{ textAlign: 'center', padding: '1.25rem', backgroundColor: '#f8f9fa', borderRadius: '8px' }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#1565C0' }}>{progress?.total_sources || 0}</div>
          <div style={{ color: '#666', fontSize: '0.9rem' }}>Sources</div>
        </div>
        <div style={{ textAlign: 'center', padding: '1.25rem', backgroundColor: '#f8f9fa', borderRadius: '8px' }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#7B1FA2' }}>{progress?.total_fragments || 0}</div>
          <div style={{ color: '#666', fontSize: '0.9rem' }}>Extracts</div>
        </div>
        <div style={{ textAlign: 'center', padding: '1.25rem', backgroundColor: '#e8f5e9', borderRadius: '8px' }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#2E7D32' }}>{progress?.auto_integrated_count || 0}</div>
          <div style={{ color: '#666', fontSize: '0.9rem' }}>Auto-Integrated</div>
        </div>
        <div style={{ textAlign: 'center', padding: '1.25rem', backgroundColor: progress?.needs_decision_count > 0 ? '#fff3e0' : '#f8f9fa', borderRadius: '8px' }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: progress?.needs_decision_count > 0 ? '#E65100' : '#666' }}>
            {progress?.needs_decision_count || 0}
          </div>
          <div style={{ color: '#666', fontSize: '0.9rem' }}>Pending Decisions</div>
        </div>
      </div>

      {/* Action Buttons */}
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem', flexWrap: 'wrap' }}>
        <button
          onClick={onOpenAddSource}
          style={{
            padding: '0.75rem 1.5rem',
            borderRadius: '6px',
            border: 'none',
            backgroundColor: '#1565C0',
            color: '#fff',
            cursor: 'pointer',
            fontSize: '1rem',
            fontWeight: 500,
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
          }}
        >
          <span style={{ fontSize: '1.2rem' }}>+</span> Add Source
        </button>
        {progress?.needs_decision_count > 0 && (
          <button
            onClick={onOpenDecisions}
            style={{
              padding: '0.75rem 1.5rem',
              borderRadius: '6px',
              border: 'none',
              backgroundColor: '#E65100',
              color: '#fff',
              cursor: 'pointer',
              fontSize: '1rem',
              fontWeight: 500,
            }}
          >
            View Pending Decisions ({progress.needs_decision_count})
          </button>
        )}
      </div>

      {/* Sources List */}
      <div>
        <h3 style={{ marginBottom: '1rem' }}>Evidence Sources</h3>
        {sources.length === 0 ? (
          <div style={{
            padding: '2rem',
            textAlign: 'center',
            backgroundColor: '#f8f9fa',
            borderRadius: '8px',
            color: '#666',
          }}>
            No evidence sources yet. Add a source to begin evidence integration.
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {sources.map(source => (
              <div
                key={source.id}
                style={{
                  padding: '1rem',
                  backgroundColor: '#fff',
                  border: '1px solid #e8e8e8',
                  borderRadius: '8px',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <div>
                  <div style={{ fontWeight: 500, marginBottom: '0.25rem' }}>{source.source_name}</div>
                  <div style={{ fontSize: '0.85rem', color: '#666' }}>
                    <span style={{
                      backgroundColor: '#e3e8ee',
                      padding: '0.15rem 0.5rem',
                      borderRadius: '4px',
                      marginRight: '0.75rem',
                    }}>
                      {source.source_type}
                    </span>
                    {source.extracted_count} fragments extracted
                  </div>
                </div>
                <div style={{
                  padding: '0.35rem 0.75rem',
                  borderRadius: '20px',
                  fontSize: '0.8rem',
                  fontWeight: 500,
                  backgroundColor: source.extraction_status === 'completed' ? '#e8f5e9' :
                                   source.extraction_status === 'failed' ? '#ffebee' : '#fff3e0',
                  color: source.extraction_status === 'completed' ? '#2e7d32' :
                         source.extraction_status === 'failed' ? '#c62828' : '#e65100',
                }}>
                  {source.extraction_status}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

function OperationSection({ operation, analysis, colors }) {
  const [expanded, setExpanded] = useState(false)
  const groupedItems = groupItemsByType(analysis?.items)

  return (
    <div
      style={{
        backgroundColor: 'rgba(255,255,255,0.85)',
        borderRadius: '8px',
        marginBottom: '0.75rem',
        border: `1px solid ${colors.border}`,
        boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
      }}
    >
      <div
        onClick={() => setExpanded(!expanded)}
        style={{
          padding: '1rem 1.25rem',
          cursor: 'pointer',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start',
        }}
      >
        <div style={{ flex: 1 }}>
          <div style={{ fontWeight: 600, color: colors.text, marginBottom: '0.35rem', fontSize: '1.05rem' }}>
            {operation.name}
          </div>
          <div style={{ fontSize: '0.9rem', color: '#555', lineHeight: 1.4 }}>
            {operation.description}
          </div>
          {operation.influences?.length > 0 && (
            <div style={{ fontSize: '0.8rem', color: '#888', marginTop: '0.5rem' }}>
              <span style={{ opacity: 0.7 }}>Influences:</span> {operation.influences.map(i => i.short_name).join(', ')}
            </div>
          )}
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginLeft: '1rem' }}>
          {analysis && (
            <span style={{
              backgroundColor: colors.text,
              color: '#fff',
              padding: '0.35rem 0.75rem',
              borderRadius: '20px',
              fontSize: '0.8rem',
              fontWeight: 500,
            }}>
              {analysis.items?.length || 0} items
            </span>
          )}
          <span style={{ color: colors.text, fontSize: '1.2rem', fontWeight: 300 }}>{expanded ? '−' : '+'}</span>
        </div>
      </div>

      {expanded && analysis && (
        <div style={{ padding: '0 1.25rem 1.25rem', borderTop: `1px solid ${colors.border}` }}>
          {analysis.canonical_statement && (
            <div style={{
              backgroundColor: colors.bg,
              padding: '1rem 1.25rem',
              borderRadius: '6px',
              marginTop: '1rem',
              borderLeft: `4px solid ${colors.text}`,
            }}>
              <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: colors.text, marginBottom: '0.5rem', fontWeight: 600, letterSpacing: '0.5px' }}>
                Summary
              </div>
              <div style={{ fontSize: '0.95rem', lineHeight: 1.5, color: '#333' }}>
                {analysis.canonical_statement}
              </div>
            </div>
          )}

          {Object.keys(groupedItems).length > 0 && (
            <div style={{ marginTop: '1.25rem' }}>
              {Object.entries(groupedItems).map(([itemType, items]) => (
                <div key={itemType} style={{ marginBottom: '1.25rem' }}>
                  <div style={{
                    fontWeight: 600,
                    marginBottom: '0.75rem',
                    fontSize: '0.85rem',
                    color: colors.text,
                    textTransform: 'uppercase',
                    letterSpacing: '0.5px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                  }}>
                    {getItemTypeLabel(itemType)}
                    <span style={{
                      backgroundColor: colors.bg,
                      padding: '0.15rem 0.5rem',
                      borderRadius: '10px',
                      fontSize: '0.75rem',
                      fontWeight: 500,
                    }}>
                      {items.length}
                    </span>
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                    {items.map((item, idx) => (
                      <div
                        key={item.id || idx}
                        style={{
                          padding: '0.75rem 1rem',
                          backgroundColor: '#fff',
                          borderRadius: '6px',
                          border: '1px solid #e8e8e8',
                          fontSize: '0.9rem',
                          lineHeight: 1.5,
                        }}
                      >
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                          <div style={{ flex: 1 }}>{formatItemContent(item.content, item.item_type)}</div>
                          <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'flex-start' }}>
                            <CentralityBadge centrality={item.web_centrality} />
                            <ProvenanceBadge item={item} />
                          </div>
                        </div>
                        {(item.severity || item.strength || item.coherence_score != null) && (
                          <div style={{ marginTop: '0.5rem', display: 'flex', gap: '1rem', fontSize: '0.8rem', color: '#888', flexWrap: 'wrap' }}>
                            {item.severity && <span>Severity: <strong>{item.severity}</strong></span>}
                            {item.strength != null && <span>Strength: <strong>{Math.round(item.strength * 100)}%</strong></span>}
                            {item.coherence_score != null && <span>Coherence: <strong>{Math.round(item.coherence_score * 100)}%</strong></span>}
                            {item.observation_proximity != null && <span>Observation Proximity: <strong>{Math.round(item.observation_proximity * 100)}%</strong></span>}
                          </div>
                        )}
                        {item.reasoning_scaffold && (
                          <ReasoningScaffoldDisplay scaffold={item.reasoning_scaffold} itemContent={item.content} />
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}

          {operation.key_questions?.length > 0 && (
            <div style={{
              marginTop: '1.25rem',
              padding: '1rem',
              backgroundColor: '#f8f9fa',
              borderRadius: '6px',
            }}>
              <div style={{ fontWeight: 600, marginBottom: '0.75rem', fontSize: '0.8rem', color: '#666', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                Guiding Questions
              </div>
              <ul style={{ margin: 0, paddingLeft: '1.25rem', color: '#555', fontSize: '0.9rem', lineHeight: 1.6 }}>
                {operation.key_questions.map((q, i) => (
                  <li key={i} style={{ marginBottom: '0.35rem' }}>{q}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {expanded && !analysis && (
        <div style={{
          padding: '1.25rem',
          color: '#999',
          fontStyle: 'italic',
          borderTop: `1px solid ${colors.border}`,
          textAlign: 'center',
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
  const [activeTab, setActiveTab] = useState('analysis')
  const [showAddSource, setShowAddSource] = useState(false)
  const [showDecisions, setShowDecisions] = useState(false)
  const [evidenceKey, setEvidenceKey] = useState(0) // For forcing refresh

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

              {/* Tab Navigation */}
              <div style={{
                display: 'flex',
                borderBottom: '2px solid #e8e8e8',
                marginBottom: '1.5rem',
              }}>
                <button
                  onClick={() => setActiveTab('analysis')}
                  style={{
                    padding: '0.75rem 1.5rem',
                    border: 'none',
                    backgroundColor: 'transparent',
                    cursor: 'pointer',
                    fontSize: '1rem',
                    fontWeight: 500,
                    color: activeTab === 'analysis' ? '#1565C0' : '#666',
                    borderBottom: activeTab === 'analysis' ? '2px solid #1565C0' : '2px solid transparent',
                    marginBottom: '-2px',
                  }}
                >
                  Analysis
                </button>
                <button
                  onClick={() => setActiveTab('evidence')}
                  style={{
                    padding: '0.75rem 1.5rem',
                    border: 'none',
                    backgroundColor: 'transparent',
                    cursor: 'pointer',
                    fontSize: '1rem',
                    fontWeight: 500,
                    color: activeTab === 'evidence' ? '#1565C0' : '#666',
                    borderBottom: activeTab === 'evidence' ? '2px solid #1565C0' : '2px solid transparent',
                    marginBottom: '-2px',
                  }}
                >
                  Evidence
                </button>
              </div>

              {/* Analysis Tab Content */}
              {activeTab === 'analysis' && (
                <>
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

              {/* Evidence Tab Content */}
              {activeTab === 'evidence' && (
                <EvidenceDashboard
                  key={evidenceKey}
                  conceptId={selectedConcept}
                  onOpenAddSource={() => setShowAddSource(true)}
                  onOpenDecisions={() => setShowDecisions(true)}
                />
              )}
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

      {/* Modals */}
      {showAddSource && selectedConcept && (
        <AddEvidenceSource
          conceptId={selectedConcept}
          apiUrl={API_URL}
          onClose={() => setShowAddSource(false)}
          onSourceAdded={() => {
            setShowAddSource(false)
            setEvidenceKey(k => k + 1) // Refresh evidence dashboard
          }}
        />
      )}

      {showDecisions && selectedConcept && (
        <EvidenceDecisionView
          conceptId={selectedConcept}
          apiUrl={API_URL}
          onClose={() => setShowDecisions(false)}
          onDecisionMade={() => {
            setEvidenceKey(k => k + 1) // Refresh evidence dashboard
            // Also reload the concept analysis to show new provenance
            loadConceptAnalysis(selectedConcept)
          }}
        />
      )}
    </div>
  )
}

export default ConceptAnalysisViewer
