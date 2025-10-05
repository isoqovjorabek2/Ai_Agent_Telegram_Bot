// Configuration for the webapp
// Update these URLs for production deployment

// Default to environment variables if available, otherwise use localhost
const BACKEND_URL = window.ENV_BACKEND_URL || "http://localhost:8000";

// Export configuration
window.APP_CONFIG = {
    BACKEND_URL: BACKEND_URL
};