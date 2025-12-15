import { useState, useEffect, useCallback } from 'react'
import './index.css'

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
              <button className="btn btn-primary btn-sm" onClick={() => { setEditingItem(null); setShowConceptForm(true) }}>
                + New Concept
              </button>
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

      {/* CHALLENGES TAB */}
      {activeTab === 'challenges' && (
        <div className="content full-width">
          <div className="card">
            <div className="card-header">
              <h2>Challenges from Evidence</h2>
              <span className="list-item-meta">{pendingChallenges.length} pending review</span>
            </div>
            <div className="card-body">
              {challenges.length === 0 ? (
                <div className="empty-state">
                  <h3>No challenges yet</h3>
                  <p>Challenges from essay-flow will appear here when evidence contradicts or extends theory</p>
                </div>
              ) : (
                challenges.map(ch => (
                  <div key={ch.id} className={`card challenge-card ${ch.status}`}>
                    <div className="card-body">
                      <div className="challenge-meta">
                        <div>
                          <span className={`status ${ch.status}`}>{ch.status.replace('_', ' ')}</span>
                          <span> • {ch.challenge_type.replace('_', ' ')}</span>
                          {ch.concept_term && <span> • Concept: <strong>{ch.concept_term}</strong></span>}
                          {ch.dialectic_name && <span> • Dialectic: <strong>{ch.dialectic_name}</strong></span>}
                        </div>
                        <span>Project #{ch.source_project_id}</span>
                      </div>
                      <div className="challenge-evidence">
                        <strong>Evidence:</strong> {ch.evidence_summary}
                      </div>
                      {ch.proposed_refinement && (
                        <div className="detail-section">
                          <h4>Proposed Refinement</h4>
                          <div className="detail-content">{ch.proposed_refinement}</div>
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
                      {ch.reviewer_notes && (
                        <div className="detail-section" style={{ marginTop: '1rem' }}>
                          <h4>Reviewer Notes</h4>
                          <div className="detail-content">{ch.reviewer_notes}</div>
                        </div>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
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

      <ToastContainer toasts={toasts} removeToast={removeToast} />
    </div>
  )
}

export default App
