/**
 * sidebar.js — Shared sidebar component
 * Inject into any page with: renderSidebar('page-id')
 */

const NAV_ITEMS = [
  { section: 'Overview' },
  { id: 'dashboard',      label: 'Dashboard',      href: 'dashboard.html',      icon: '◈' },
  { section: 'Operations' },
  { id: 'warehouses',     label: 'Warehouses',      href: 'warehouses.html',     icon: '🏭' },
  { id: 'products',       label: 'Products',        href: 'products.html',       icon: '📦' },
  { id: 'inventory',      label: 'Inventory',       href: 'inventory.html',      icon: '📊' },
  { id: 'orders',         label: 'Orders',          href: 'orders.html',         icon: '🗒' },
  { section: 'AI Insights' },
  { id: 'ai-insights',    label: 'AI Insights',     href: 'ai-insights.html',    icon: '✦' },
  { section: 'Management' },
  { id: 'organizations',  label: 'Organizations',   href: 'organizations.html',  icon: '🏢' },
  { id: 'reports',        label: 'Reports',         href: 'reports.html',        icon: '📋' },
  { id: 'settings',       label: 'Settings',        href: 'settings.html',       icon: '⚙' },
];

function renderSidebar(activeId) {
  let nav = '';
  for (const item of NAV_ITEMS) {
    if (item.section) {
      nav += `<div class="nav-section-label">${item.section}</div>`;
    } else {
      const active = item.id === activeId ? 'active' : '';
      nav += `<a class="nav-item ${active}" href="${item.href}">${item.icon}&nbsp; ${item.label}</a>`;
    }
  }

  const html = `
    <aside class="sidebar" id="sidebar">
      <div class="sidebar-logo">Supply Chain <span>AI</span></div>
      <nav class="sidebar-nav">${nav}</nav>
      <div class="sidebar-footer">v1.0.0 &nbsp;·&nbsp; IBM Bob</div>
    </aside>`;

  const target = document.getElementById('sidebar-placeholder');
  if (target) target.outerHTML = html;
}
