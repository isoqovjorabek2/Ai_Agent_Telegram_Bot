// Configuration for the webapp
// This loads environment variables from env.js (generated at build time)

// Load backend URL from environment or use localhost as fallback
const BACKEND_URL = (() => {
    // First try window.ENV_BACKEND_URL (from env.js)
    if (window.ENV_BACKEND_URL && window.ENV_BACKEND_URL !== "PLACEHOLDER_BACKEND_URL") {
        return window.ENV_BACKEND_URL;
    }
    
    // Fallback to localhost for development
    return "http://localhost:8000";
})();

// Export configuration
window.APP_CONFIG = {
    BACKEND_URL: BACKEND_URL
};

console.log("🔧 App Config:", window.APP_CONFIG);