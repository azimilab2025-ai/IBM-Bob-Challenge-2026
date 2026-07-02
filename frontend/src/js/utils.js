/**
 * utils.js — Shared UI utilities
 * DOM helpers, formatting, toast notifications, modal management.
 */

/* ── Formatting ── */
const fmt = {
  currency: (v) => v == null ? '—' : `$${Number(v).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
  number:   (v) => v == null ? '—' : Number(v).toLocaleString('en-US'),
  decimal:  (v, d = 1) => v == null ? '—' : Number(v).toFixed(d),
  date:     (v) => v ? new Date(v).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' }) : '—',
  datetime: (v) => v ? new Date(v).toLocaleString('en-US', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }) : '—',
  percent:  (v) => v == null ? '—' : `${Number(v).toFixed(1)}%`,
};

/* ── Badge helper ── */
function badge(value, extra = '') {
  const cls = String(value).toLowerCase().replace(/\s+/g, '_');
  return `<span class="badge badge-${cls} ${extra}">${value ?? '—'}</span>`;
}

/* ── Toast notifications ── */
const toast = (() => {
  let container;
  function _getContainer() {
    if (!container) {
      container = document.createElement('div');
      container.style.cssText = 'position:fixed;bottom:20px;right:20px;z-index:9999;display:flex;flex-direction:column;gap:8px;';
      document.body.appendChild(container);
    }
    return container;
  }

  function show(message, type = 'info', duration = 3500) {
    const colors = { success: '#16a34a', danger: '#dc2626', warning: '#d97706', info: '#3b82d4' };
    const el = document.createElement('div');
    el.style.cssText = `
      background:${colors[type] || colors.info};color:#fff;padding:10px 16px;
      border-radius:6px;font-size:0.86rem;max-width:340px;line-height:1.5;
      box-shadow:0 4px 12px rgba(0,0,0,.15);
    `;
    el.textContent = message;
    _getContainer().appendChild(el);
    setTimeout(() => el.remove(), duration);
  }

  return {
    success: (msg) => show(msg, 'success'),
    error:   (msg) => show(msg, 'danger'),
    warning: (msg) => show(msg, 'warning'),
    info:    (msg) => show(msg, 'info'),
  };
})();

/* ── Modal helpers ── */
function openModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.remove('hidden');
}
function closeModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.add('hidden');
}

/* ── Sidebar active link ── */
function markActiveNav() {
  const page = location.pathname.split('/').pop();
  document.querySelectorAll('.nav-item').forEach(el => {
    const href = el.getAttribute('href') || '';
    if (href.includes(page)) el.classList.add('active');
    else el.classList.remove('active');
  });
}

/* ── Render user info in top-bar ── */
function renderUserBar() {
  const user = auth.getUser();
  const nameEl = document.getElementById('user-name');
  const roleEl = document.getElementById('user-role');
  if (nameEl && user) nameEl.textContent = user.full_name;
  if (roleEl && user) roleEl.textContent = user.role.replace(/_/g, ' ');
}

/* ── Loading state ── */
function setLoading(el, loading) {
  if (!el) return;
  if (loading) {
    el.disabled = true;
    el._originalText = el.innerHTML;
    el.innerHTML = '<span class="loading-spinner"></span>';
  } else {
    el.disabled = false;
    if (el._originalText) el.innerHTML = el._originalText;
  }
}

/* ── Empty state ── */
function emptyState(message = 'No data found') {
  return `<div class="empty-state"><div class="empty-state-icon">□</div><div class="empty-state-text">${message}</div></div>`;
}

/* ── Pagination renderer ── */
function renderPagination(containerId, meta, onPage) {
  const el = document.getElementById(containerId);
  if (!el || !meta) return;
  if (meta.total_pages <= 1) { el.innerHTML = ''; return; }
  let html = `<button class="pagination-btn" ${meta.page <= 1 ? 'disabled' : ''} onclick="(${onPage})(${meta.page - 1})">‹</button>`;
  for (let p = Math.max(1, meta.page - 2); p <= Math.min(meta.total_pages, meta.page + 2); p++) {
    html += `<button class="pagination-btn ${p === meta.page ? 'active' : ''}" onclick="(${onPage})(${p})">${p}</button>`;
  }
  html += `<button class="pagination-btn" ${meta.page >= meta.total_pages ? 'disabled' : ''} onclick="(${onPage})(${meta.page + 1})">›</button>`;
  html += `<span class="text-muted text-sm" style="margin-left:8px">${meta.total} total</span>`;
  el.innerHTML = html;
}
