/**
 * shell.js — Shared page shell (sidebar + top-bar)
 * Inject into every protected page via renderShell().
 */

const NAV_ITEMS = [
  { href: 'dashboard.html',    label: 'Dashboard',     icon: '▦' },
  { href: 'organizations.html',label: 'Organizations',  icon: '🏢', section: 'Management' },
  { href: 'warehouses.html',   label: 'Warehouses',     icon: '🏭' },
  { href: 'products.html',     label: 'Products',       icon: '📦' },
  { href: 'inventory.html',    label: 'Inventory',      icon: '📊' },
  { href: 'orders.html',       label: 'Orders',         icon: '🛒' },
  { href: 'ai-insights.html',  label: 'AI Insights',    icon: '🤖', section: 'Intelligence' },
  { href: 'reports.html',      label: 'Reports',        icon: '📋', section: 'Analytics' },
  { href: 'settings.html',     label: 'Settings',       icon: '⚙️', section: 'System' },
];

function renderShell(pageTitle) {
  const currentPage = location.pathname.split('/').pop();

  let navHtml = '';
  let lastSection = null;

  NAV_ITEMS.forEach(item => {
    if (item.section && item.section !== lastSection) {
      navHtml += `<div class="nav-section-label">${item.section}</div>`;
      lastSection = item.section;
    }
    const isActive = item.href === currentPage ? 'active' : '';
    navHtml += `<a href="${item.href}" class="nav-item ${isActive}">${item.icon} ${item.label}</a>`;
  });

  const user = auth.getUser();

  document.body.innerHTML = `
    <div class="app-layout">
      <aside class="sidebar">
        <div class="sidebar-logo">Supply<span>Chain</span> AI</div>
        <nav class="sidebar-nav">${navHtml}</nav>
        <div class="sidebar-footer">v1.0.0 · IBM Bob Challenge</div>
      </aside>

      <div class="main-content">
        <header class="top-bar">
          <div class="page-title">${pageTitle}</div>
          <div class="user-info">
            <span id="user-name" class="text-sm fw-600">${user ? user.full_name : ''}</span>
            <span id="user-role" class="user-badge">${user ? user.role.replace(/_/g, ' ') : ''}</span>
            <button class="btn-logout" onclick="handleLogout()">Logout</button>
          </div>
        </header>
        <main class="page-body" id="page-content"></main>
      </div>
    </div>
  `;
}

async function handleLogout() {
  auth.clear();
  window.location.href = 'login.html';
}
