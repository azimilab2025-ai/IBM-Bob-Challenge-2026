/**
 * auth.js — Authentication state management
 * Manages JWT tokens in localStorage and user profile.
 * All pages import this before api.js.
 */

const auth = {
  _TOKEN_KEY:   'sc_access_token',
  _REFRESH_KEY: 'sc_refresh_token',
  _USER_KEY:    'sc_user',

  getToken()    { return localStorage.getItem(this._TOKEN_KEY); },
  getRefresh()  { return localStorage.getItem(this._REFRESH_KEY); },
  getUser()     {
    try { return JSON.parse(localStorage.getItem(this._USER_KEY) || 'null'); }
    catch { return null; }
  },

  setTokens(accessToken, refreshToken) {
    localStorage.setItem(this._TOKEN_KEY,   accessToken);
    localStorage.setItem(this._REFRESH_KEY, refreshToken);
  },

  setUser(user) {
    localStorage.setItem(this._USER_KEY, JSON.stringify(user));
  },

  clear() {
    localStorage.removeItem(this._TOKEN_KEY);
    localStorage.removeItem(this._REFRESH_KEY);
    localStorage.removeItem(this._USER_KEY);
  },

  isAuthenticated() { return !!this.getToken(); },

  /** Redirect to login if not authenticated. Call at top of every protected page. */
  requireAuth() {
    if (!this.isAuthenticated()) {
      window.location.href = 'login.html';
      return false;
    }
    return true;
  },

  /** Redirect to dashboard if already authenticated. Call on login page. */
  redirectIfAuthenticated() {
    if (this.isAuthenticated()) {
      window.location.href = 'dashboard.html';
    }
  },
};
