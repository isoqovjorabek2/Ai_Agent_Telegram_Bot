// Backend API URL
const BACKEND_URL = "https://ai-agent-service-uz-lhhv.onrender.com";

// Get user_id from URL
function getUserId() {
    const params = new URLSearchParams(window.location.search);
    return params.get("user_id");
}

// Show status messages
function showStatus(message, type = "loading") {
    const statusDiv = document.getElementById("status");
    statusDiv.textContent = message;
    statusDiv.className = `status ${type}`;

    const spinner = document.getElementById("spinner");
    if (type === "loading") {
        spinner.classList.add("active");
    } else {
        spinner.classList.remove("active");
    }
}

// Handle Google Sign-In click
async function startGoogleLogin() {
    const userId = getUserId();
    if (!userId) {
        showStatus("❌ User ID not found", "error");
        return;
    }

    try {
        showStatus("🔄 Redirecting to Google...", "loading");

        // Redirect to backend for OAuth flow
        window.location.href = `${BACKEND_URL}/api/auth/initiate?user_id=${userId}`;
    } catch (err) {
        console.error(err);
        showStatus("❌ Failed to start Google login", "error");
    }
}

// Init
document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("googleSignIn");
    btn.addEventListener("click", startGoogleLogin);

    // Auto-detect user_id and warn if missing
    if (!getUserId()) {
        showStatus("⚠️ No user ID detected. Opened outside Telegram?", "error");
    }
});
