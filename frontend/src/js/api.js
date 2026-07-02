/**
 * api.js — Centralized API client
 * All HTTP calls go through this module.
 * Handles auth headers, error normalization, and response envelope unwrapping.
 */

const API_BASE = '/api/v1';

/**
 * Core request function.
 * Returns the unwrapped `data` field from the success envelope,
 * or throws an Error with the backend message on failure.
 */
async function request(method, path, body = null) {
  const token = auth.getToken();
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const config = { method, headers };
  if (body !== null) config.body = JSON.stringify(body);

  const response = await fetch(`${API_BASE}${path}`, config);

  // Handle 401 — token expired or invalid
  if (response.status === 401) {
    auth.clear();
    window.location.href = '/src/pages/login.html';
    throw new Error('Session expired. Please log in again.');
  }

  const json = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(json.message || `HTTP ${response.status}`);
  }

  return json; // Return full envelope; callers access .data or .meta as needed
}

const api = {
  // ── Auth ──────────────────────────────────────────────
  login:   (email, password)   => request('POST', '/auth/login',   { email, password }),
  refresh: (refresh_token)     => request('POST', '/auth/refresh',  { refresh_token }),
  me:      ()                  => request('GET',  '/auth/me'),

  // ── Dashboard ─────────────────────────────────────────
  dashboardSummary: () => request('GET', '/dashboard/summary'),
  dashboardAlerts:  () => request('GET', '/dashboard/alerts'),

  // ── Organizations ─────────────────────────────────────
  getOrganizations: (page = 1, perPage = 20) =>
    request('GET', `/organizations?page=${page}&per_page=${perPage}`),
  getOrganization:  (id)   => request('GET',  `/organizations/${id}`),
  createOrganization: (data) => request('POST', '/organizations', data),
  updateOrganization: (id, data) => request('PUT', `/organizations/${id}`, data),

  // ── Warehouses ────────────────────────────────────────
  getWarehouses: (page = 1, perPage = 20) =>
    request('GET', `/warehouses?page=${page}&per_page=${perPage}`),
  getWarehouse:  (id)   => request('GET',  `/warehouses/${id}`),
  createWarehouse: (data) => request('POST', '/warehouses', data),
  updateWarehouse: (id, data) => request('PUT', `/warehouses/${id}`, data),
  deleteWarehouse: (id) => request('DELETE', `/warehouses/${id}`),

  // ── Products ──────────────────────────────────────────
  getProducts: (page = 1, perPage = 20) =>
    request('GET', `/products?page=${page}&per_page=${perPage}`),
  getProduct:  (id)   => request('GET',  `/products/${id}`),
  createProduct: (data) => request('POST', '/products', data),
  updateProduct: (id, data) => request('PUT', `/products/${id}`, data),

  // ── Inventory ─────────────────────────────────────────
  getInventory: (page = 1, perPage = 20) =>
    request('GET', `/inventory?page=${page}&per_page=${perPage}`),
  getInventoryItem: (id) => request('GET', `/inventory/${id}`),
  setInventory: (data) => request('POST', '/inventory', data),
  adjustInventory: (id, delta, reason = '') =>
    request('POST', `/inventory/${id}/adjust`, { delta, reason }),
  getLowStock: () => request('GET', '/inventory/alerts/low-stock'),

  // ── Orders ────────────────────────────────────────────
  getOrders: (page = 1, perPage = 20, status = '') =>
    request('GET', `/orders?page=${page}&per_page=${perPage}${status ? `&status=${status}` : ''}`),
  getOrder:  (id)   => request('GET',  `/orders/${id}`),
  createOrder: (data) => request('POST', '/orders', data),
  updateOrder: (id, data) => request('PATCH', `/orders/${id}`, data),
  allocateOrder: (id) => request('POST', `/orders/${id}/allocate`),

  // ── AI ────────────────────────────────────────────────
  forecastDemand: (productId, horizonDays = 30, windowSize = 7) =>
    request('POST', `/ai/forecast/${productId}?horizon_days=${horizonDays}&window_size=${windowSize}`),
  optimizeInventory: (productId, warehouseId) =>
    request('POST', `/ai/optimize-inventory?product_id=${productId}&warehouse_id=${warehouseId}`),
  optimizeRoutes: (warehouseId, orderIds) => {
    const params = orderIds.map(id => `order_ids=${id}`).join('&');
    return request('POST', `/ai/optimize-routes?warehouse_id=${warehouseId}&${params}`);
  },

  // ── Reports ───────────────────────────────────────────
  inventoryReport:  () => request('GET', '/reports/inventory'),
  ordersReport:     () => request('GET', '/reports/orders'),
  forecastsReport:  () => request('GET', '/reports/forecasts'),

  // ── Health ────────────────────────────────────────────
  health: () => fetch('/health').then(r => r.json()),
};
