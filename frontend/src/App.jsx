import { useState, useEffect, useCallback } from 'react'
import './index.css'
import ConceptSetupWizard from './ConceptSetupWizard'

const API_URL = import.meta.env.VITE_API_URL || 'https://theory-api.onrender.com'

// API helper
async function api(endpoint, options = {}) {
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  })
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }))
    throw new Error(error.detail || 'Request failed')
  }
  if (response.status === 204) return null
  return response.json()
}

// Toast notifications
function Toast({ message, type, onClose }) {
  useEffect(() => {
    const timer = setTimeout(onClose, 3000)
    return () => clearTimeout(timer)
  }, [onClose])

  return <div className={`toast ${type}`}>{message}</div>
}

function ToastContainer({ toasts, removeToast }) {
  return (
    <div className="toast-container">
      {toasts.map(t => (
        <Toast key={t.id} message={t.message} type={t.type} onClose={() => removeToast(t.id)} />
      ))}
    </div>
  )
}

// Modal component
function Modal({ title, onClose, children }) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{title}</h2>
          <button className="modal-close" onClick={onClose}>&times;</button>
        </div>
        <div className="modal-body">{children}</div>
      </div>
    </div>
  )
}

// Tags input component
function TagsInput({ value = [], onChange, placeholder }) {
  const [input, setInput] = useState('')

  const addTag = () => {
    if (input.trim() && !value.includes(input.trim())) {
      onChange([...value, input.trim()])
      setInput('')
    }
  }

  const removeTag = (tag) => {
    onChange(value.filter(t => t !== tag))
  }

  return (
    <div className="tags-input">
      {value.map(tag => (
        <span key={tag} className="tag">
          {tag}
          <button onClick={() => removeTag(tag)}>&times;</button>
        </span>
      ))}
      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && (e.preventDefault(), addTag())}
        onBlur={addTag}
        placeholder={value.length === 0 ? placeholder : ''}
      />
    </div>
  )
}

// Concept Form
function ConceptForm({ concept, onSave, onCancel }) {
  const [form, setForm] = useState(concept || {
    term: '',
    definition: '',
    category: '',
    status: 'draft',
    source_thinkers: [],
    related_concepts: []
  })
  const [saving, setSaving] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    try {
      await onSave(form)
    } finally {
      setSaving(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label>Term *</label>
        <input
          value={form.term}
          onChange={e => setForm({...form, term: e.target.value})}
          required
        />
      </div>
      <div className="form-group">
        <label>Definition *</label>
        <textarea
          value={form.definition}
          onChange={e => setForm({...form, definition: e.target.value})}
          required
        />
      </div>
      <div className="form-row">
        <div className="form-group">
          <label>Category</label>
          <input
            value={form.category || ''}
            onChange={e => setForm({...form, category: e.target.value})}
            placeholder="e.g., epistemology, technology"
          />
        </div>
        <div className="form-group">
          <label>Status</label>
          <select value={form.status} onChange={e => setForm({...form, status: e.target.value})}>
            <option value="draft">Draft</option>
            <option value="active">Active</option>
            <option value="challenged">Challenged</option>
            <option value="revised">Revised</option>
            <option value="deprecated">Deprecated</option>
          </select>
        </div>
      </div>
      <div className="form-group">
        <label>Source Thinkers</label>
        <TagsInput
          value={form.source_thinkers}
          onChange={v => setForm({...form, source_thinkers: v})}
          placeholder="Add thinkers (press Enter)"
        />
      </div>
      <div className="form-actions">
        <button type="submit" className="btn btn-primary" disabled={saving}>
          {saving ? 'Saving...' : (concept ? 'Update' : 'Create')}
        </button>
        <button type="button" className="btn btn-secondary" onClick={onCancel}>Cancel</button>
      </div>
    </form>
  )
}

// Dialectic Form
function DialecticForm({ dialectic, onSave, onCancel }) {
  const [form, setForm] = useState(dialectic || {
    name: '',
    description: '',
    tension_a: '',
    tension_b: '',
    category: '',
    status: 'draft',
    resolution_notes: ''
  })
  const [saving, setSaving] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    try {
      await onSave(form)
    } finally {
      setSaving(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label>Name *</label>
        <input
          value={form.name}
          onChange={e => setForm({...form, name: e.target.value})}
          required
          placeholder="e.g., Efficiency vs. Democracy"
        />
      </div>
      <div className="form-group">
        <label>Description *</label>
        <textarea
          value={form.description}
          onChange={e => setForm({...form, description: e.target.value})}
          required
        />
      </div>
      <div className="form-row">
        <div className="form-group">
          <label>Tension A *</label>
          <input
            value={form.tension_a}
            onChange={e => setForm({...form, tension_a: e.target.value})}
            required
            placeholder="First pole of the tension"
          />
        </div>
        <div className="form-group">
          <label>Tension B *</label>
          <input
            value={form.tension_b}
            onChange={e => setForm({...form, tension_b: e.target.value})}
            required
            placeholder="Second pole of the tension"
          />
        </div>
      </div>
      <div className="form-row">
        <div className="form-group">
          <label>Category</label>
          <input
            value={form.category || ''}
            onChange={e => setForm({...form, category: e.target.value})}
          />
        </div>
        <div className="form-group">
          <label>Status</label>
          <select value={form.status} onChange={e => setForm({...form, status: e.target.value})}>
            <option value="draft">Draft</option>
            <option value="active">Active</option>
            <option value="resolved">Resolved</option>
            <option value="superseded">Superseded</option>
          </select>
        </div>
      </div>
      {form.status === 'resolved' && (
        <div className="form-group">
          <label>Resolution Notes</label>
          <textarea
            value={form.resolution_notes || ''}
            onChange={e => setForm({...form, resolution_notes: e.target.value})}
            placeholder="How was this tension resolved?"
          />
        </div>
      )}
      <div className="form-actions">
        <button type="submit" className="btn btn-primary" disabled={saving}>
          {saving ? 'Saving...' : (dialectic ? 'Update' : 'Create')}
        </button>
        <button type="button" className="btn btn-secondary" onClick={onCancel}>Cancel</button>
      </div>
    </form>
  )
}

// Claim Form
function ClaimForm({ claim, onSave, onCancel }) {
  const [form, setForm] = useState(claim || {
    statement: '',
    evidence_summary: '',
    category: '',
    is_active: true,
    confidence_level: 0.7,
    source_thinkers: [],
    related_concepts: [],
    related_dialectics: []
  })
  const [saving, setSaving] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    try {
      await onSave(form)
    } finally {
      setSaving(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label>Statement *</label>
        <textarea
          value={form.statement}
          onChange={e => setForm({...form, statement: e.target.value})}
          required
          placeholder="The claim we hold to be true..."
        />
      </div>
      <div className="form-group">
        <label>Evidence Summary</label>
        <textarea
          value={form.evidence_summary || ''}
          onChange={e => setForm({...form, evidence_summary: e.target.value})}
          placeholder="What evidence supports this claim?"
        />
      </div>
      <div className="form-row">
        <div className="form-group">
          <label>Category</label>
          <input
            value={form.category || ''}
            onChange={e => setForm({...form, category: e.target.value})}
          />
        </div>
        <div className="form-group">
          <label>Confidence Level</label>
          <input
            type="number"
            min="0"
            max="1"
            step="0.1"
            value={form.confidence_level || 0.7}
            onChange={e => setForm({...form, confidence_level: parseFloat(e.target.value)})}
          />
        </div>
      </div>
      <div className="form-group">
        <label>Source Thinkers</label>
        <TagsInput
          value={form.source_thinkers}
          onChange={v => setForm({...form, source_thinkers: v})}
          placeholder="Add thinkers (press Enter)"
        />
      </div>
      <div className="form-group">
        <label>
          <input
            type="checkbox"
            checked={form.is_active}
            onChange={e => setForm({...form, is_active: e.target.checked})}
          />
          {' '}Active Claim
        </label>
      </div>
      <div className="form-actions">
        <button type="submit" className="btn btn-primary" disabled={saving}>
          {saving ? 'Saving...' : (claim ? 'Update' : 'Create')}
        </button>
        <button type="button" className="btn btn-secondary" onClick={onCancel}>Cancel</button>
      </div>
    </form>
  )
}

// Challenge Dashboard Component
function ChallengeDashboard({ challenges, reviewChallenge, addToast, onRefresh }) {
  const [dashboardStats, setDashboardStats] = useState(null)
  const [emergingConcepts, setEmergingConcepts] = useState([])
  const [emergingDialectics, setEmergingDialectics] = useState([])
  const [clusters, setClusters] = useState([])
  const [subTab, setSubTab] = useState('overview')
  const [loading, setLoading] = useState(true)
  const [clustering, setClustering] = useState(false)

  // Load dashboard data
  useEffect(() => {
    const loadDashboardData = async () => {
      setLoading(true)
      try {
        const [statsData, ecData, edData, clusterData] = await Promise.all([
          api('/challenges/dashboard'),
          api('/emerging-concepts'),
          api('/emerging-dialectics'),
          api('/challenge-clusters')
        ])
        setDashboardStats(statsData)
        setEmergingConcepts(ecData)
        setEmergingDialectics(edData)
        setClusters(clusterData)
      } catch (err) {
        console.error('Failed to load dashboard:', err)
      }
      setLoading(false)
    }
    loadDashboardData()
  }, [])

  const runClustering = async () => {
    setClustering(true)
    try {
      const result = await api('/challenges/cluster', { method: 'POST', body: JSON.stringify({}) })
      addToast(`Clustering complete: ${result.clusters_created} clusters created`)
      // Refresh data
      const [clusterData, statsData] = await Promise.all([
        api('/challenge-clusters'),
        api('/challenges/dashboard')
      ])
      setClusters(clusterData)
      setDashboardStats(statsData)
      onRefresh()
    } catch (err) {
      addToast(err.message, 'error')
    }
    setClustering(false)
  }

  const resolveCluster = async (clusterId, action, notes = '') => {
    try {
      await api(`/challenge-clusters/${clusterId}`, {
        method: 'PATCH',
        body: JSON.stringify({
          status: 'resolved',
          resolution_notes: notes,
          member_action: action
        })
      })
      addToast(`Cluster resolved: ${action}`)
      // Refresh
      const clusterData = await api('/challenge-clusters')
      setClusters(clusterData)
      onRefresh()
    } catch (err) {
      addToast(err.message, 'error')
    }
  }

  const updateEmergingConcept = async (id, status) => {
    try {
      await api(`/emerging-concepts/${id}`, {
        method: 'PATCH',
        body: JSON.stringify({ status })
      })
      addToast(`Emerging concept ${status}`)
      const ecData = await api('/emerging-concepts')
      setEmergingConcepts(ecData)
    } catch (err) {
      addToast(err.message, 'error')
    }
  }

  const updateEmergingDialectic = async (id, status) => {
    try {
      await api(`/emerging-dialectics/${id}`, {
        method: 'PATCH',
        body: JSON.stringify({ status })
      })
      addToast(`Emerging dialectic ${status}`)
      const edData = await api('/emerging-dialectics')
      setEmergingDialectics(edData)
    } catch (err) {
      addToast(err.message, 'error')
    }
  }

  const conceptChallenges = challenges.filter(c => c.concept_id)
  const dialecticChallenges = challenges.filter(c => c.dialectic_id)
  const pendingClusters = clusters.filter(c => c.status === 'pending')

  if (loading) {
    return <div className="content full-width"><div className="loading">Loading challenge dashboard...</div></div>
  }

  return (
    <div className="content full-width">
      {/* Stats Overview */}
      {dashboardStats && (
        <div className="dashboard-stats">
          <div className="stat-card" onClick={() => setSubTab('concept-impacts')}>
            <div className="stat-number">{dashboardStats.concept_impacts}</div>
            <div className="stat-label">Concept Impacts</div>
          </div>
          <div className="stat-card" onClick={() => setSubTab('dialectic-impacts')}>
            <div className="stat-number">{dashboardStats.dialectic_impacts}</div>
            <div className="stat-label">Dialectic Impacts</div>
          </div>
          <div className="stat-card" onClick={() => setSubTab('emerging-concepts')}>
            <div className="stat-number">{dashboardStats.emerging_concepts}</div>
            <div className="stat-label">Emerging Concepts</div>
          </div>
          <div className="stat-card" onClick={() => setSubTab('emerging-dialectics')}>
            <div className="stat-number">{dashboardStats.emerging_dialectics}</div>
            <div className="stat-label">Emerging Dialectics</div>
          </div>
          <div className="stat-card highlight" onClick={() => setSubTab('clusters')} title="Groups of similar challenges for batch review">
            <div className="stat-number">{pendingClusters.length}</div>
            <div className="stat-label">Pending Clusters</div>
          </div>
        </div>
      )}

      {/* Sub-tabs */}
      <div className="sub-tabs">
        <button className={`sub-tab ${subTab === 'overview' ? 'active' : ''}`} onClick={() => setSubTab('overview')}>
          Overview
        </button>
        <button className={`sub-tab ${subTab === 'concept-impacts' ? 'active' : ''}`} onClick={() => setSubTab('concept-impacts')}>
          Concept Impacts ({conceptChallenges.length})
        </button>
        <button className={`sub-tab ${subTab === 'dialectic-impacts' ? 'active' : ''}`} onClick={() => setSubTab('dialectic-impacts')}>
          Dialectic Impacts ({dialecticChallenges.length})
        </button>
        <button className={`sub-tab ${subTab === 'emerging-concepts' ? 'active' : ''}`} onClick={() => setSubTab('emerging-concepts')}>
          Emerging Concepts ({emergingConcepts.length})
        </button>
        <button className={`sub-tab ${subTab === 'emerging-dialectics' ? 'active' : ''}`} onClick={() => setSubTab('emerging-dialectics')}>
          Emerging Dialectics ({emergingDialectics.length})
        </button>
        <button className={`sub-tab ${subTab === 'clusters' ? 'active' : ''}`} onClick={() => setSubTab('clusters')}>
          Clusters ({clusters.length})
        </button>
      </div>

      {/* Overview */}
      {subTab === 'overview' && (
        <div className="card">
          <div className="card-header">
            <h2>Challenge Reconciliation Dashboard</h2>
            <button
              className="btn btn-primary"
              onClick={runClustering}
              disabled={clustering}
            >
              {clustering ? 'Clustering...' : 'Run LLM Clustering'}
            </button>
          </div>
          <div className="card-body">
            <p>This dashboard helps reconcile theory challenges from multiple essay-flow projects.</p>

            {dashboardStats?.source_projects?.length > 0 && (
              <div className="detail-section">
                <h4>Evidence Source Projects</h4>
                <p style={{ fontSize: '0.85rem', color: '#666', marginBottom: '0.5rem' }}>
                  These are essay-flow projects where evidence was analyzed. Projects marked [MOCK] contain synthetic test data.
                </p>
                <div className="project-list">
                  {dashboardStats.source_projects.map(p => (
                    <div key={p.id} className={`project-badge ${p.name?.includes('[MOCK]') ? 'mock' : ''}`}>
                      {p.name} ({p.count} challenges)
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="detail-section">
              <h4>What are Clusters?</h4>
              <p style={{ marginBottom: '1rem' }}>
                Clusters group <strong>similar challenges</strong> together for batch review. For example, if 3 different evidence clusters
                all say "the Digital Sovereignty concept needs refinement", they get grouped into one cluster. The LLM analyzes them
                and recommends whether to accept, reject, or review individually.
              </p>
            </div>

            <div className="detail-section">
              <h4>Source Attribution</h4>
              <p style={{ marginBottom: '1rem' }}>
                <strong>Evidence Project</strong> (shown on challenges): Where the evidence was analyzed (e.g., "Morozov Socialism After AI" essay).<br/>
                <strong>Theory Source</strong> (in Concepts/Dialectics tabs): Where the theoretical concepts originated (e.g., "Morozov Theory Guide").
              </p>
            </div>

            <div className="detail-section">
              <h4>Workflow</h4>
              <ol className="workflow-steps">
                <li>Evidence from essay-flow generates challenges to theory</li>
                <li>Multiple projects may challenge the same concepts differently</li>
                <li>Click "Run LLM Clustering" to group similar challenges</li>
                <li>Review clusters and batch accept/reject</li>
                <li>Emerging concepts can be promoted to the theory base</li>
              </ol>
            </div>
          </div>
        </div>
      )}

      {/* Concept Impacts */}
      {subTab === 'concept-impacts' && (
        <div className="card">
          <div className="card-header">
            <h2>Concept Impacts</h2>
          </div>
          <div className="card-body">
            {conceptChallenges.length === 0 ? (
              <div className="empty-state">
                <h3>No concept impacts</h3>
                <p>Challenges to concepts will appear here</p>
              </div>
            ) : (
              conceptChallenges.map(ch => (
                <div key={ch.id} className={`card challenge-card ${ch.status}`}>
                  <div className="card-body">
                    <div className="challenge-meta">
                      <div>
                        <span className={`status ${ch.status}`}>{ch.status}</span>
                        <span className="impact-type"> {ch.challenge_type?.replace('_', ' ')}</span>
                        <span> → <strong>{ch.concept_term}</strong></span>
                      </div>
                      <span className="project-source">{ch.source_project_name || `Project #${ch.source_project_id}`}</span>
                    </div>
                    {ch.source_cluster_name && (
                      <div className="cluster-source">From cluster: {ch.source_cluster_name}</div>
                    )}
                    <div className="challenge-summary">{ch.impact_summary}</div>
                    {ch.proposed_refinement && (
                      <div className="proposed-change">
                        <strong>Proposed Refinement:</strong> {ch.proposed_refinement}
                      </div>
                    )}
                    {ch.status === 'pending' && (
                      <div className="challenge-actions">
                        <button className="btn btn-success btn-sm" onClick={() => reviewChallenge(ch.id, 'integrated')}>
                          Integrate
                        </button>
                        <button className="btn btn-secondary btn-sm" onClick={() => reviewChallenge(ch.id, 'accepted')}>
                          Accept
                        </button>
                        <button className="btn btn-danger btn-sm" onClick={() => reviewChallenge(ch.id, 'rejected')}>
                          Reject
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* Dialectic Impacts */}
      {subTab === 'dialectic-impacts' && (
        <div className="card">
          <div className="card-header">
            <h2>Dialectic Impacts</h2>
          </div>
          <div className="card-body">
            {dialecticChallenges.length === 0 ? (
              <div className="empty-state">
                <h3>No dialectic impacts</h3>
                <p>Challenges to dialectics will appear here</p>
              </div>
            ) : (
              dialecticChallenges.map(ch => (
                <div key={ch.id} className={`card challenge-card ${ch.status}`}>
                  <div className="card-body">
                    <div className="challenge-meta">
                      <div>
                        <span className={`status ${ch.status}`}>{ch.status}</span>
                        <span className="impact-type"> {ch.challenge_type?.replace('_', ' ')}</span>
                        <span> → <strong>{ch.dialectic_name}</strong></span>
                      </div>
                      <span className="project-source">{ch.source_project_name || `Project #${ch.source_project_id}`}</span>
                    </div>
                    {ch.weight_toward_a !== null && (
                      <div className="weight-indicator">
                        Weight toward A: {Math.round(ch.weight_toward_a * 100)}%
                        <div className="weight-bar">
                          <div className="weight-fill" style={{ width: `${ch.weight_toward_a * 100}%` }} />
                        </div>
                      </div>
                    )}
                    <div className="challenge-summary">{ch.impact_summary}</div>
                    {ch.proposed_synthesis && (
                      <div className="proposed-change">
                        <strong>Proposed Synthesis:</strong> {ch.proposed_synthesis}
                      </div>
                    )}
                    {ch.status === 'pending' && (
                      <div className="challenge-actions">
                        <button className="btn btn-success btn-sm" onClick={() => reviewChallenge(ch.id, 'accepted')}>
                          Accept
                        </button>
                        <button className="btn btn-danger btn-sm" onClick={() => reviewChallenge(ch.id, 'rejected')}>
                          Reject
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* Emerging Concepts */}
      {subTab === 'emerging-concepts' && (
        <div className="card">
          <div className="card-header">
            <h2>Emerging Concepts</h2>
            <span className="list-item-meta">New concepts proposed from evidence</span>
          </div>
          <div className="card-body">
            {emergingConcepts.length === 0 ? (
              <div className="empty-state">
                <h3>No emerging concepts</h3>
                <p>New concept proposals from evidence will appear here</p>
              </div>
            ) : (
              emergingConcepts.map(ec => (
                <div key={ec.id} className={`card emerging-card ${ec.status} ${ec.source_project_name?.includes('[MOCK]') ? 'mock-data' : ''}`}>
                  <div className="card-body">
                    <div className="emerging-header">
                      <h3>{ec.proposed_name}</h3>
                      <span className={`status ${ec.status}`}>{ec.status}</span>
                    </div>
                    <div className="emerging-meta">
                      <span className={ec.source_project_name?.includes('[MOCK]') ? 'mock-badge' : ''}>
                        {ec.source_project_name || `Project #${ec.source_project_id}`}
                      </span>
                      {ec.evidence_strength && <span> • Strength: {ec.evidence_strength}</span>}
                      <span> • Confidence: {Math.round((ec.confidence || 0.8) * 100)}%</span>
                    </div>
                    {ec.proposed_definition && (
                      <div className="emerging-definition">{ec.proposed_definition}</div>
                    )}
                    <div className="emerging-rationale">
                      <strong>Rationale:</strong> {ec.emergence_rationale}
                    </div>
                    {ec.source_cluster_names?.length > 0 && (
                      <div className="source-clusters">
                        <strong>Source clusters:</strong> {ec.source_cluster_names.join(', ')}
                      </div>
                    )}
                    {ec.status === 'proposed' && (
                      <div className="challenge-actions">
                        <button className="btn btn-success btn-sm" onClick={() => updateEmergingConcept(ec.id, 'promoted')}>
                          Promote to Concept
                        </button>
                        <button className="btn btn-secondary btn-sm" onClick={() => updateEmergingConcept(ec.id, 'accepted')}>
                          Accept
                        </button>
                        <button className="btn btn-danger btn-sm" onClick={() => updateEmergingConcept(ec.id, 'rejected')}>
                          Reject
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* Emerging Dialectics */}
      {subTab === 'emerging-dialectics' && (
        <div className="card">
          <div className="card-header">
            <h2>Emerging Dialectics</h2>
            <span className="list-item-meta">New tensions proposed from evidence</span>
          </div>
          <div className="card-body">
            {emergingDialectics.length === 0 ? (
              <div className="empty-state">
                <h3>No emerging dialectics</h3>
                <p>New dialectic proposals from evidence will appear here</p>
              </div>
            ) : (
              emergingDialectics.map(ed => (
                <div key={ed.id} className={`card emerging-card ${ed.status}`}>
                  <div className="card-body">
                    <div className="emerging-header">
                      <span className={`status ${ed.status}`}>{ed.status}</span>
                    </div>
                    <div className="emerging-meta">
                      <span>{ed.source_project_name || `Project #${ed.source_project_id}`}</span>
                      {ed.evidence_strength && <span> • Strength: {ed.evidence_strength}</span>}
                    </div>
                    <div className="tension emerging-tension">
                      <div className="tension-side a">
                        <div className="tension-label">Tension A</div>
                        <div className="tension-text">{ed.proposed_tension_a}</div>
                      </div>
                      <div className="tension-vs">vs</div>
                      <div className="tension-side b">
                        <div className="tension-label">Tension B</div>
                        <div className="tension-text">{ed.proposed_tension_b}</div>
                      </div>
                    </div>
                    {ed.proposed_question && (
                      <div className="emerging-question">
                        <strong>Question:</strong> {ed.proposed_question}
                      </div>
                    )}
                    <div className="emerging-rationale">
                      <strong>Rationale:</strong> {ed.emergence_rationale}
                    </div>
                    {ed.status === 'proposed' && (
                      <div className="challenge-actions">
                        <button className="btn btn-success btn-sm" onClick={() => updateEmergingDialectic(ed.id, 'promoted')}>
                          Promote to Dialectic
                        </button>
                        <button className="btn btn-secondary btn-sm" onClick={() => updateEmergingDialectic(ed.id, 'accepted')}>
                          Accept
                        </button>
                        <button className="btn btn-danger btn-sm" onClick={() => updateEmergingDialectic(ed.id, 'rejected')}>
                          Reject
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* Clusters */}
      {subTab === 'clusters' && (
        <div className="card">
          <div className="card-header">
            <h2>Challenge Clusters</h2>
            <button
              className="btn btn-primary"
              onClick={runClustering}
              disabled={clustering}
            >
              {clustering ? 'Running...' : 'Re-run Clustering'}
            </button>
          </div>
          <div className="card-body">
            <div style={{ background: '#f0f9ff', padding: '1rem', borderRadius: '8px', marginBottom: '1.5rem', fontSize: '0.9rem' }}>
              <strong>What are clusters?</strong> When multiple evidence sources make similar observations about a concept or dialectic,
              they get grouped into a cluster. The LLM analyzes each cluster and recommends an action: <strong>accept</strong> (strong consensus),
              <strong> reject</strong> (weak or contradicted), or <strong>human_review</strong> (complex case needing manual review).
            </div>
            {clusters.length === 0 ? (
              <div className="empty-state">
                <h3>No clusters yet</h3>
                <p>Run LLM clustering to group similar challenges</p>
              </div>
            ) : (
              clusters.map(cluster => (
                <div key={cluster.id} className={`card cluster-card ${cluster.status}`}>
                  <div className="card-body">
                    <div className="cluster-header">
                      <div>
                        <span className={`status ${cluster.status}`}>{cluster.status}</span>
                        <span className="cluster-type"> {cluster.cluster_type?.replace('_', ' ')}</span>
                        {cluster.target_concept_term && <span> → {cluster.target_concept_term}</span>}
                        {cluster.target_dialectic_name && <span> → {cluster.target_dialectic_name}</span>}
                      </div>
                      <div className="cluster-meta">
                        {cluster.member_count} members • {cluster.source_project_count} projects
                      </div>
                    </div>
                    {cluster.cluster_summary && (
                      <div className="cluster-summary">{cluster.cluster_summary}</div>
                    )}
                    {cluster.recommended_action && (
                      <div className={`cluster-recommendation ${cluster.recommended_action}`}>
                        <strong>LLM Recommendation:</strong> {cluster.recommended_action.replace('_', ' ')}
                        {cluster.cluster_recommendation && ` - ${cluster.cluster_recommendation}`}
                      </div>
                    )}
                    {cluster.status === 'pending' && (
                      <div className="challenge-actions">
                        <button className="btn btn-success btn-sm" onClick={() => resolveCluster(cluster.id, 'accept')}>
                          Accept All
                        </button>
                        <button className="btn btn-danger btn-sm" onClick={() => resolveCluster(cluster.id, 'reject')}>
                          Reject All
                        </button>
                        <button className="btn btn-secondary btn-sm" onClick={() => resolveCluster(cluster.id, 'individual')}>
                          Review Individually
                        </button>
                      </div>
                    )}
                    {cluster.resolution_notes && (
                      <div className="resolution-notes">
                        <strong>Resolution:</strong> {cluster.resolution_notes}
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  )
}

// Main App
function App() {
  const [activeTab, setActiveTab] = useState('concepts')
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [toasts, setToasts] = useState([])

  // Data states
  const [sources, setSources] = useState([])
  const [concepts, setConcepts] = useState([])
  const [dialectics, setDialectics] = useState([])
  const [claims, setClaims] = useState([])
  const [challenges, setChallenges] = useState([])

  // Selection states
  const [selectedConcept, setSelectedConcept] = useState(null)
  const [selectedDialectic, setSelectedDialectic] = useState(null)
  const [selectedClaim, setSelectedClaim] = useState(null)

  // Modal states
  const [showConceptForm, setShowConceptForm] = useState(false)
  const [showDialecticForm, setShowDialecticForm] = useState(false)
  const [showClaimForm, setShowClaimForm] = useState(false)
  const [showConceptWizard, setShowConceptWizard] = useState(false)
  const [editingItem, setEditingItem] = useState(null)

  // Filters
  const [sourceFilter, setSourceFilter] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [searchQuery, setSearchQuery] = useState('')

  // Toast helpers
  const addToast = (message, type = 'success') => {
    const id = Date.now()
    setToasts(t => [...t, { id, message, type }])
  }
  const removeToast = (id) => setToasts(t => t.filter(toast => toast.id !== id))

  // Load data
  const loadSources = useCallback(async () => {
    try {
      const data = await api('/sources')
      setSources(data)
    } catch (err) {
      console.error('Failed to load sources:', err)
    }
  }, [])

  const loadStats = useCallback(async () => {
    try {
      const data = await api('/stats')
      setStats(data)
    } catch (err) {
      console.error('Failed to load stats:', err)
    }
  }, [])

  const loadConcepts = useCallback(async () => {
    try {
      const params = new URLSearchParams()
      if (sourceFilter) params.set('source_id', sourceFilter)
      if (statusFilter) params.set('status', statusFilter)
      if (searchQuery) params.set('search', searchQuery)
      const data = await api(`/concepts?${params}`)
      setConcepts(data)
    } catch (err) {
      setError(err.message)
    }
  }, [sourceFilter, statusFilter, searchQuery])

  const loadDialectics = useCallback(async () => {
    try {
      const params = new URLSearchParams()
      if (sourceFilter) params.set('source_id', sourceFilter)
      if (statusFilter) params.set('status', statusFilter)
      const data = await api(`/dialectics?${params}`)
      setDialectics(data)
    } catch (err) {
      setError(err.message)
    }
  }, [sourceFilter, statusFilter])

  const loadClaims = useCallback(async () => {
    try {
      const params = new URLSearchParams()
      if (sourceFilter) params.set('source_id', sourceFilter)
      params.set('active_only', 'false')
      const data = await api(`/claims?${params}`)
      setClaims(data)
    } catch (err) {
      setError(err.message)
    }
  }, [sourceFilter])

  const loadChallenges = useCallback(async () => {
    try {
      const data = await api('/challenges?limit=100')
      setChallenges(data)
    } catch (err) {
      setError(err.message)
    }
  }, [])

  useEffect(() => {
    const loadAll = async () => {
      setLoading(true)
      setError(null)
      await Promise.all([loadSources(), loadStats(), loadConcepts(), loadDialectics(), loadClaims(), loadChallenges()])
      setLoading(false)
    }
    loadAll()
  }, [loadSources, loadStats, loadConcepts, loadDialectics, loadClaims, loadChallenges])

  // CRUD operations
  const saveConcept = async (data) => {
    try {
      if (editingItem) {
        await api(`/concepts/${editingItem.id}`, { method: 'PATCH', body: JSON.stringify(data) })
        addToast('Concept updated')
      } else {
        await api('/concepts', { method: 'POST', body: JSON.stringify(data) })
        addToast('Concept created')
      }
      setShowConceptForm(false)
      setEditingItem(null)
      loadConcepts()
      loadStats()
    } catch (err) {
      addToast(err.message, 'error')
    }
  }

  const deleteConcept = async (id) => {
    if (!confirm('Delete this concept?')) return
    try {
      await api(`/concepts/${id}`, { method: 'DELETE' })
      addToast('Concept deleted')
      setSelectedConcept(null)
      loadConcepts()
      loadStats()
    } catch (err) {
      addToast(err.message, 'error')
    }
  }

  const saveDialectic = async (data) => {
    try {
      if (editingItem) {
        await api(`/dialectics/${editingItem.id}`, { method: 'PATCH', body: JSON.stringify(data) })
        addToast('Dialectic updated')
      } else {
        await api('/dialectics', { method: 'POST', body: JSON.stringify(data) })
        addToast('Dialectic created')
      }
      setShowDialecticForm(false)
      setEditingItem(null)
      loadDialectics()
      loadStats()
    } catch (err) {
      addToast(err.message, 'error')
    }
  }

  const saveClaim = async (data) => {
    try {
      if (editingItem) {
        await api(`/claims/${editingItem.id}`, { method: 'PATCH', body: JSON.stringify(data) })
        addToast('Claim updated')
      } else {
        await api('/claims', { method: 'POST', body: JSON.stringify(data) })
        addToast('Claim created')
      }
      setShowClaimForm(false)
      setEditingItem(null)
      loadClaims()
      loadStats()
    } catch (err) {
      addToast(err.message, 'error')
    }
  }

  const reviewChallenge = async (id, status, notes = '') => {
    try {
      await api(`/challenges/${id}/review`, {
        method: 'PATCH',
        body: JSON.stringify({ status, reviewer_notes: notes })
      })
      addToast(`Challenge ${status}`)
      loadChallenges()
      loadConcepts()
      loadStats()
    } catch (err) {
      addToast(err.message, 'error')
    }
  }

  const pendingChallenges = challenges.filter(c => c.status === 'pending')

  if (loading) {
    return (
      <div className="app">
        <div className="loading">Loading Theory Service...</div>
      </div>
    )
  }

  return (
    <div className="app">
      <header>
        <h1>Theory Service</h1>
        {stats && (
          <div className="stats">
            <div className="stat">
              <span>Concepts:</span>
              <span className="stat-value">{stats.concepts}</span>
            </div>
            <div className="stat">
              <span>Dialectics:</span>
              <span className="stat-value">{stats.dialectics}</span>
            </div>
            <div className="stat">
              <span>Claims:</span>
              <span className="stat-value">{stats.claims}</span>
            </div>
            <div className="stat">
              <span>Pending:</span>
              <span className="stat-value">{stats.pending_challenges}</span>
            </div>
          </div>
        )}
        {sources.length > 0 && (
          <div className="source-filter">
            <label>Source:</label>
            <select
              className="source-select"
              value={sourceFilter}
              onChange={e => setSourceFilter(e.target.value)}
            >
              <option value="">All Sources</option>
              {sources.map(s => (
                <option key={s.id} value={s.id}>
                  {s.short_name || s.title} ({s.concept_count + s.dialectic_count + s.claim_count})
                </option>
              ))}
            </select>
          </div>
        )}
      </header>

      {error && <div className="error-alert">{error}</div>}

      <div className="tabs">
        <button className={`tab ${activeTab === 'concepts' ? 'active' : ''}`} onClick={() => setActiveTab('concepts')}>
          Concepts<span className="badge">{concepts.length}</span>
        </button>
        <button className={`tab ${activeTab === 'dialectics' ? 'active' : ''}`} onClick={() => setActiveTab('dialectics')}>
          Dialectics<span className="badge">{dialectics.length}</span>
        </button>
        <button className={`tab ${activeTab === 'claims' ? 'active' : ''}`} onClick={() => setActiveTab('claims')}>
          Claims<span className="badge">{claims.length}</span>
        </button>
        <button className={`tab ${activeTab === 'challenges' ? 'active' : ''}`} onClick={() => setActiveTab('challenges')}>
          Challenges<span className="badge">{pendingChallenges.length}</span>
        </button>
      </div>

      {/* CONCEPTS TAB */}
      {activeTab === 'concepts' && (
        <div className="content">
          <div className="card">
            <div className="card-header">
              <h2>Concepts</h2>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button className="btn btn-secondary btn-sm" onClick={() => setShowConceptWizard(true)}>
                  + Novel Concept Wizard
                </button>
                <button className="btn btn-primary btn-sm" onClick={() => { setEditingItem(null); setShowConceptForm(true) }}>
                  + New Concept
                </button>
              </div>
            </div>
            <div className="toolbar" style={{ padding: '1rem 1.25rem 0' }}>
              <input
                className="search-input"
                placeholder="Search concepts..."
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
              />
              <select className="filter-select" value={statusFilter} onChange={e => setStatusFilter(e.target.value)}>
                <option value="">All Statuses</option>
                <option value="draft">Draft</option>
                <option value="active">Active</option>
                <option value="challenged">Challenged</option>
                <option value="revised">Revised</option>
                <option value="deprecated">Deprecated</option>
              </select>
            </div>
            <div className="list">
              {concepts.length === 0 ? (
                <div className="empty-state">
                  <h3>No concepts yet</h3>
                  <p>Create your first theoretical concept</p>
                </div>
              ) : (
                concepts.map(c => (
                  <div
                    key={c.id}
                    className={`list-item ${selectedConcept?.id === c.id ? 'selected' : ''}`}
                    onClick={() => setSelectedConcept(c)}
                  >
                    <div className="list-item-header">
                      <span className="list-item-title">
                        {c.term}
                        {c.source_title && !sourceFilter && <span className="source-badge">{c.source_title.split(':')[0]}</span>}
                      </span>
                      <span className={`status ${c.status}`}>{c.status}</span>
                    </div>
                    <div className="list-item-meta">
                      {c.category && <span>{c.category}</span>}
                      {c.challenge_count > 0 && <span> • {c.challenge_count} challenges</span>}
                    </div>
                    <div className="list-item-preview">{c.definition}</div>
                  </div>
                ))
              )}
            </div>
          </div>

          {selectedConcept && (
            <div className="card">
              <div className="card-body">
                <div className="detail-header">
                  <h3>{selectedConcept.term}</h3>
                  <span className={`status ${selectedConcept.status}`}>{selectedConcept.status}</span>
                  <div className="detail-actions">
                    <button className="btn btn-secondary btn-sm" onClick={() => { setEditingItem(selectedConcept); setShowConceptForm(true) }}>
                      Edit
                    </button>
                    <button className="btn btn-danger btn-sm" onClick={() => deleteConcept(selectedConcept.id)}>
                      Delete
                    </button>
                  </div>
                </div>
                <div className="detail-section">
                  <h4>Definition</h4>
                  <div className="detail-content">{selectedConcept.definition}</div>
                </div>
                {selectedConcept.category && (
                  <div className="detail-section">
                    <h4>Category</h4>
                    <div className="detail-content">{selectedConcept.category}</div>
                  </div>
                )}
                {selectedConcept.source_title && (
                  <div className="detail-section">
                    <h4>Source</h4>
                    <div className="detail-content">{selectedConcept.source_title}</div>
                  </div>
                )}
                {selectedConcept.source_thinkers?.length > 0 && (
                  <div className="detail-section">
                    <h4>Source Thinkers</h4>
                    <div className="detail-content">{selectedConcept.source_thinkers.join(', ')}</div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {/* DIALECTICS TAB */}
      {activeTab === 'dialectics' && (
        <div className="content">
          <div className="card">
            <div className="card-header">
              <h2>Dialectics</h2>
              <button className="btn btn-primary btn-sm" onClick={() => { setEditingItem(null); setShowDialecticForm(true) }}>
                + New Dialectic
              </button>
            </div>
            <div className="toolbar" style={{ padding: '1rem 1.25rem 0' }}>
              <select className="filter-select" value={statusFilter} onChange={e => setStatusFilter(e.target.value)}>
                <option value="">All Statuses</option>
                <option value="draft">Draft</option>
                <option value="active">Active</option>
                <option value="resolved">Resolved</option>
                <option value="superseded">Superseded</option>
              </select>
            </div>
            <div className="list">
              {dialectics.length === 0 ? (
                <div className="empty-state">
                  <h3>No dialectics yet</h3>
                  <p>Create your first theoretical tension</p>
                </div>
              ) : (
                dialectics.map(d => (
                  <div
                    key={d.id}
                    className={`list-item ${selectedDialectic?.id === d.id ? 'selected' : ''}`}
                    onClick={() => setSelectedDialectic(d)}
                  >
                    <div className="list-item-header">
                      <span className="list-item-title">
                        {d.name}
                        {d.source_title && !sourceFilter && <span className="source-badge">{d.source_title.split(':')[0]}</span>}
                      </span>
                      <span className={`status ${d.status}`}>{d.status}</span>
                    </div>
                    <div className="list-item-meta">
                      {d.tension_a} vs {d.tension_b}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {selectedDialectic && (
            <div className="card">
              <div className="card-body">
                <div className="detail-header">
                  <h3>{selectedDialectic.name}</h3>
                  <span className={`status ${selectedDialectic.status}`}>{selectedDialectic.status}</span>
                  <div className="detail-actions">
                    <button className="btn btn-secondary btn-sm" onClick={() => { setEditingItem(selectedDialectic); setShowDialecticForm(true) }}>
                      Edit
                    </button>
                  </div>
                </div>
                <div className="tension">
                  <div className="tension-side a">
                    <div className="tension-label">Tension A</div>
                    <div className="tension-text">{selectedDialectic.tension_a}</div>
                  </div>
                  <div className="tension-vs">vs</div>
                  <div className="tension-side b">
                    <div className="tension-label">Tension B</div>
                    <div className="tension-text">{selectedDialectic.tension_b}</div>
                  </div>
                </div>
                <div className="detail-section">
                  <h4>Description</h4>
                  <div className="detail-content">{selectedDialectic.description}</div>
                </div>
                {selectedDialectic.source_title && (
                  <div className="detail-section">
                    <h4>Source</h4>
                    <div className="detail-content">{selectedDialectic.source_title}</div>
                  </div>
                )}
                {selectedDialectic.resolution_notes && (
                  <div className="detail-section">
                    <h4>Resolution Notes</h4>
                    <div className="detail-content">{selectedDialectic.resolution_notes}</div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {/* CLAIMS TAB */}
      {activeTab === 'claims' && (
        <div className="content">
          <div className="card">
            <div className="card-header">
              <h2>Claims</h2>
              <button className="btn btn-primary btn-sm" onClick={() => { setEditingItem(null); setShowClaimForm(true) }}>
                + New Claim
              </button>
            </div>
            <div className="list">
              {claims.length === 0 ? (
                <div className="empty-state">
                  <h3>No claims yet</h3>
                  <p>Create your first theoretical claim</p>
                </div>
              ) : (
                claims.map(c => (
                  <div
                    key={c.id}
                    className={`list-item ${selectedClaim?.id === c.id ? 'selected' : ''}`}
                    onClick={() => setSelectedClaim(c)}
                  >
                    <div className="list-item-header">
                      <span className="list-item-title">
                        {c.statement.slice(0, 70)}{c.statement.length > 70 ? '...' : ''}
                        {c.source_title && !sourceFilter && <span className="source-badge">{c.source_title.split(':')[0]}</span>}
                      </span>
                      <span className={`status ${c.is_active ? 'active' : 'deprecated'}`}>
                        {c.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </div>
                    <div className="list-item-meta">
                      {c.category && <span>{c.category}</span>}
                      {c.confidence && <span> • Confidence: {Math.round(c.confidence * 100)}%</span>}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {selectedClaim && (
            <div className="card">
              <div className="card-body">
                <div className="detail-header">
                  <h3>Claim Details</h3>
                  <span className={`status ${selectedClaim.is_active ? 'active' : 'deprecated'}`}>
                    {selectedClaim.is_active ? 'Active' : 'Inactive'}
                  </span>
                  <div className="detail-actions">
                    <button className="btn btn-secondary btn-sm" onClick={() => { setEditingItem(selectedClaim); setShowClaimForm(true) }}>
                      Edit
                    </button>
                  </div>
                </div>
                <div className="detail-section">
                  <h4>Statement</h4>
                  <div className="detail-content">{selectedClaim.statement}</div>
                </div>
                {selectedClaim.evidence_summary && (
                  <div className="detail-section">
                    <h4>Evidence Summary</h4>
                    <div className="detail-content">{selectedClaim.evidence_summary}</div>
                  </div>
                )}
                {selectedClaim.source_title && (
                  <div className="detail-section">
                    <h4>Source</h4>
                    <div className="detail-content">{selectedClaim.source_title}</div>
                  </div>
                )}
                {selectedClaim.source_thinkers?.length > 0 && (
                  <div className="detail-section">
                    <h4>Source Thinkers</h4>
                    <div className="detail-content">{selectedClaim.source_thinkers.join(', ')}</div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {/* CHALLENGES DASHBOARD TAB */}
      {activeTab === 'challenges' && (
        <ChallengeDashboard
          challenges={challenges}
          reviewChallenge={reviewChallenge}
          addToast={addToast}
          onRefresh={() => { loadChallenges(); loadStats(); }}
        />
      )}

      {/* MODALS */}
      {showConceptForm && (
        <Modal title={editingItem ? 'Edit Concept' : 'New Concept'} onClose={() => { setShowConceptForm(false); setEditingItem(null) }}>
          <ConceptForm concept={editingItem} onSave={saveConcept} onCancel={() => { setShowConceptForm(false); setEditingItem(null) }} />
        </Modal>
      )}

      {showDialecticForm && (
        <Modal title={editingItem ? 'Edit Dialectic' : 'New Dialectic'} onClose={() => { setShowDialecticForm(false); setEditingItem(null) }}>
          <DialecticForm dialectic={editingItem} onSave={saveDialectic} onCancel={() => { setShowDialecticForm(false); setEditingItem(null) }} />
        </Modal>
      )}

      {showClaimForm && (
        <Modal title={editingItem ? 'Edit Claim' : 'New Claim'} onClose={() => { setShowClaimForm(false); setEditingItem(null) }}>
          <ClaimForm claim={editingItem} onSave={saveClaim} onCancel={() => { setShowClaimForm(false); setEditingItem(null) }} />
        </Modal>
      )}

      {/* Concept Setup Wizard */}
      {showConceptWizard && (
        <ConceptSetupWizard
          sourceId={sourceFilter ? parseInt(sourceFilter) : null}
          onComplete={(concept) => {
            setShowConceptWizard(false)
            loadConcepts()
            loadStats()
            addToast(`Created concept: ${concept.term}`)
          }}
          onCancel={() => setShowConceptWizard(false)}
        />
      )}

      <ToastContainer toasts={toasts} removeToast={removeToast} />
    </div>
  )
}

export default App
