/**
 * Strategizer JavaScript
 * Handles theme toggle, auto-save, AJAX operations, and UI interactions
 */

// =============================================================================
// THEME MANAGEMENT
// =============================================================================

function initTheme() {
    const savedTheme = localStorage.getItem('strategizer-theme') || 'light';
    document.documentElement.setAttribute('data-bs-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-bs-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-bs-theme', newTheme);
    localStorage.setItem('strategizer-theme', newTheme);
    updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
    const icon = document.getElementById('themeIcon');
    if (icon) {
        icon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
    }
}

// =============================================================================
// AUTO-SAVE
// =============================================================================

const AutoSave = {
    debounceTimer: null,
    debounceMs: 1000,
    indicator: null,

    init() {
        // Create indicator element
        this.indicator = document.createElement('div');
        this.indicator.className = 'autosave-indicator';
        this.indicator.innerHTML = '<i class="bi bi-cloud-arrow-up"></i> <span>Saved</span>';
        document.body.appendChild(this.indicator);
    },

    schedule(saveFunction) {
        if (this.debounceTimer) {
            clearTimeout(this.debounceTimer);
        }
        this.showSaving();
        this.debounceTimer = setTimeout(async () => {
            try {
                await saveFunction();
                this.showSaved();
            } catch (error) {
                this.showError(error);
            }
        }, this.debounceMs);
    },

    showSaving() {
        this.indicator.innerHTML = '<i class="bi bi-cloud-arrow-up"></i> <span>Saving...</span>';
        this.indicator.className = 'autosave-indicator saving';
    },

    showSaved() {
        this.indicator.innerHTML = '<i class="bi bi-check-circle"></i> <span>Saved</span>';
        this.indicator.className = 'autosave-indicator saved';
        setTimeout(() => {
            this.indicator.className = 'autosave-indicator';
        }, 2000);
    },

    showError(error) {
        this.indicator.innerHTML = '<i class="bi bi-exclamation-triangle"></i> <span>Error</span>';
        this.indicator.style.background = 'var(--st-danger)';
        console.error('AutoSave error:', error);
    }
};

// =============================================================================
// API HELPERS
// =============================================================================

const API = {
    baseUrl: '/api/strategizer',

    async request(method, path, data = null) {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        if (data) {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(`${this.baseUrl}${path}`, options);

        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
            throw new Error(error.detail || `HTTP ${response.status}`);
        }

        return response.json();
    },

    // Projects
    getProjects: () => API.request('GET', '/projects'),
    getProject: (id) => API.request('GET', `/projects/${id}`),
    createProject: (data) => API.request('POST', '/projects', data),
    updateProject: (id, data) => API.request('PUT', `/projects/${id}`, data),
    deleteProject: (id) => API.request('DELETE', `/projects/${id}`),

    // Units
    getUnits: (projectId) => API.request('GET', `/projects/${projectId}/units`),
    createUnit: (projectId, data) => API.request('POST', `/projects/${projectId}/units`, data),
    updateUnit: (projectId, unitId, data) => API.request('PUT', `/projects/${projectId}/units/${unitId}`, data),
    deleteUnit: (projectId, unitId) => API.request('DELETE', `/projects/${projectId}/units/${unitId}`),

    // Grids
    getGrids: (projectId, unitId) => API.request('GET', `/projects/${projectId}/units/${unitId}/grids`),
    createGrid: (projectId, unitId, data) => API.request('POST', `/projects/${projectId}/units/${unitId}/grids`, data),
    updateGrid: (projectId, unitId, gridId, data) => API.request('PUT', `/projects/${projectId}/units/${unitId}/grids/${gridId}`, data),
    updateSlot: (projectId, unitId, gridId, slot, data) => API.request('PUT', `/projects/${projectId}/units/${unitId}/grids/${gridId}/slots/${slot}`, data),

    // Evidence
    getProgress: (projectId) => API.request('GET', `/projects/${projectId}/evidence/progress`),
    getSources: (projectId) => API.request('GET', `/projects/${projectId}/evidence/sources`),
    addSource: (projectId, data) => API.request('POST', `/projects/${projectId}/evidence/sources`, data),
    extractSource: (projectId, sourceId) => API.request('POST', `/projects/${projectId}/evidence/sources/${sourceId}/extract`),
    getFragments: (projectId, status = null) => {
        const params = status ? `?status=${status}` : '';
        return API.request('GET', `/projects/${projectId}/evidence/fragments${params}`);
    },
    analyzeFragment: (projectId, fragmentId, data) => API.request('POST', `/projects/${projectId}/evidence/fragments/${fragmentId}/analyze`, data),
    getPendingDecision: (projectId) => API.request('GET', `/projects/${projectId}/evidence/decisions/pending`),
    resolveDecision: (projectId, fragmentId, data) => API.request('POST', `/projects/${projectId}/evidence/decisions/${fragmentId}/resolve`, data),

    // Domain
    bootstrap: (projectId, data) => API.request('POST', `/projects/${projectId}/bootstrap`, data)
};

// =============================================================================
// TOAST NOTIFICATIONS
// =============================================================================

const Toast = {
    container: null,

    init() {
        this.container = document.createElement('div');
        this.container.className = 'toast-container';
        document.body.appendChild(this.container);
    },

    show(message, type = 'info') {
        const icons = {
            success: 'check-circle-fill',
            error: 'exclamation-triangle-fill',
            warning: 'exclamation-circle-fill',
            info: 'info-circle-fill'
        };
        const bgColors = {
            success: 'bg-success',
            error: 'bg-danger',
            warning: 'bg-warning',
            info: 'bg-primary'
        };

        const toast = document.createElement('div');
        toast.className = `toast show ${bgColors[type]} text-white`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="toast-body d-flex align-items-center">
                <i class="bi bi-${icons[type]} me-2"></i>
                <span>${message}</span>
                <button type="button" class="btn-close btn-close-white ms-auto" onclick="this.parentElement.parentElement.remove()"></button>
            </div>
        `;

        this.container.appendChild(toast);

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    },

    success: (msg) => Toast.show(msg, 'success'),
    error: (msg) => Toast.show(msg, 'error'),
    warning: (msg) => Toast.show(msg, 'warning'),
    info: (msg) => Toast.show(msg, 'info')
};

// =============================================================================
// UI HELPERS
// =============================================================================

function showLoading(element) {
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>';
    element.style.position = 'relative';
    element.appendChild(overlay);
    return overlay;
}

function hideLoading(overlay) {
    if (overlay) {
        overlay.remove();
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function getUnitTypeBadge(unitType) {
    const badges = {
        concept: '<span class="badge badge-concept">Concept</span>',
        dialectic: '<span class="badge badge-dialectic">Dialectic</span>',
        actor: '<span class="badge badge-actor">Actor</span>'
    };
    return badges[unitType] || `<span class="badge bg-secondary">${unitType}</span>`;
}

function getStatusBadge(status) {
    const badges = {
        PENDING: '<span class="badge badge-pending">Pending</span>',
        ANALYZED: '<span class="badge bg-info">Analyzed</span>',
        NEEDS_DECISION: '<span class="badge badge-needs-decision">Needs Decision</span>',
        INTEGRATED: '<span class="badge badge-integrated">Integrated</span>',
        REJECTED: '<span class="badge bg-secondary">Rejected</span>'
    };
    return badges[status] || `<span class="badge bg-secondary">${status}</span>`;
}

function getConfidenceClass(confidence) {
    if (confidence >= 0.85) return 'confidence-high';
    if (confidence >= 0.60) return 'confidence-medium';
    return 'confidence-low';
}

// =============================================================================
// MODALS
// =============================================================================

function showConfirmModal(title, message, onConfirm) {
    const modal = new bootstrap.Modal(document.getElementById('confirmModal') || createConfirmModal());
    document.getElementById('confirmModalTitle').textContent = title;
    document.getElementById('confirmModalBody').textContent = message;
    document.getElementById('confirmModalBtn').onclick = () => {
        modal.hide();
        onConfirm();
    };
    modal.show();
}

function createConfirmModal() {
    const modalHtml = `
        <div class="modal fade" id="confirmModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="confirmModalTitle">Confirm</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body" id="confirmModalBody"></div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" id="confirmModalBtn">Confirm</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    return document.getElementById('confirmModal');
}

// =============================================================================
// INITIALIZATION
// =============================================================================

document.addEventListener('DOMContentLoaded', () => {
    // Initialize theme
    initTheme();

    // Theme toggle button
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }

    // Initialize components
    AutoSave.init();
    Toast.init();

    // Initialize page-specific functionality
    if (typeof initPage === 'function') {
        initPage();
    }
});
