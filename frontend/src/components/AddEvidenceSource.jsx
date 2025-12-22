import { useState } from 'react'

const SOURCE_TYPES = [
  { value: 'article', label: 'Academic Article' },
  { value: 'book', label: 'Book/Chapter' },
  { value: 'news', label: 'News Article' },
  { value: 'thinker_work', label: "Thinker's Work" },
  { value: 'url', label: 'Web URL' },
  { value: 'manual', label: 'Manual Entry' },
]

function AddEvidenceSource({ conceptId, onClose, onSourceAdded, apiUrl }) {
  const [formData, setFormData] = useState({
    source_type: 'article',
    source_name: '',
    source_url: '',
    source_date: '',
    source_content: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${apiUrl}/concepts/${conceptId}/evidence/sources`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          source_date: formData.source_date ? new Date(formData.source_date).toISOString() : null,
        }),
      })

      if (!response.ok) {
        const err = await response.json()
        throw new Error(err.detail || 'Failed to add source')
      }

      const newSource = await response.json()
      onSourceAdded(newSource)
      onClose()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

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
      <div className="modal-content" style={{
        backgroundColor: '#fff',
        borderRadius: '12px',
        width: '90%',
        maxWidth: '600px',
        maxHeight: '90vh',
        overflow: 'auto',
        boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
      }}>
        <div style={{
          padding: '1.5rem',
          borderBottom: '1px solid #e8e8e8',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}>
          <h2 style={{ margin: 0, fontSize: '1.25rem' }}>Add Evidence Source</h2>
          <button
            onClick={onClose}
            style={{
              background: 'none',
              border: 'none',
              fontSize: '1.5rem',
              cursor: 'pointer',
              color: '#666',
            }}
          >
            &times;
          </button>
        </div>

        <form onSubmit={handleSubmit} style={{ padding: '1.5rem' }}>
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

          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>
              Source Type
            </label>
            <select
              value={formData.source_type}
              onChange={(e) => setFormData({ ...formData, source_type: e.target.value })}
              style={{
                width: '100%',
                padding: '0.75rem',
                borderRadius: '6px',
                border: '1px solid #ddd',
                fontSize: '1rem',
              }}
            >
              {SOURCE_TYPES.map(t => (
                <option key={t.value} value={t.value}>{t.label}</option>
              ))}
            </select>
          </div>

          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>
              Source Name / Citation *
            </label>
            <input
              type="text"
              required
              value={formData.source_name}
              onChange={(e) => setFormData({ ...formData, source_name: e.target.value })}
              placeholder="e.g., Zuboff, S. (2019). The Age of Surveillance Capitalism"
              style={{
                width: '100%',
                padding: '0.75rem',
                borderRadius: '6px',
                border: '1px solid #ddd',
                fontSize: '1rem',
              }}
            />
          </div>

          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>
              URL (optional)
            </label>
            <input
              type="url"
              value={formData.source_url}
              onChange={(e) => setFormData({ ...formData, source_url: e.target.value })}
              placeholder="https://..."
              style={{
                width: '100%',
                padding: '0.75rem',
                borderRadius: '6px',
                border: '1px solid #ddd',
                fontSize: '1rem',
              }}
            />
          </div>

          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>
              Date (optional)
            </label>
            <input
              type="date"
              value={formData.source_date}
              onChange={(e) => setFormData({ ...formData, source_date: e.target.value })}
              style={{
                width: '100%',
                padding: '0.75rem',
                borderRadius: '6px',
                border: '1px solid #ddd',
                fontSize: '1rem',
              }}
            />
          </div>

          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>
              Content *
            </label>
            <textarea
              required
              value={formData.source_content}
              onChange={(e) => setFormData({ ...formData, source_content: e.target.value })}
              placeholder="Paste the relevant text, excerpts, or full article content here..."
              rows={10}
              style={{
                width: '100%',
                padding: '0.75rem',
                borderRadius: '6px',
                border: '1px solid #ddd',
                fontSize: '1rem',
                fontFamily: 'inherit',
                resize: 'vertical',
              }}
            />
            <div style={{ fontSize: '0.85rem', color: '#666', marginTop: '0.5rem' }}>
              The content will be analyzed to extract relevant claims and insights.
            </div>
          </div>

          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
            <button
              type="button"
              onClick={onClose}
              disabled={loading}
              style={{
                padding: '0.75rem 1.5rem',
                borderRadius: '6px',
                border: '1px solid #ddd',
                backgroundColor: '#fff',
                cursor: 'pointer',
                fontSize: '1rem',
              }}
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              style={{
                padding: '0.75rem 1.5rem',
                borderRadius: '6px',
                border: 'none',
                backgroundColor: '#1565C0',
                color: '#fff',
                cursor: loading ? 'not-allowed' : 'pointer',
                fontSize: '1rem',
                fontWeight: 500,
              }}
            >
              {loading ? 'Adding...' : 'Add & Extract Claims'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default AddEvidenceSource
