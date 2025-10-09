// Backend API URL - loaded from config
const BACKEND_URL = window.APP_CONFIG.BACKEND_URL;

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
        showStatus("🔄 Connecting to backend...", "loading");

        // Call backend API to initiate OAuth flow
        const response = await fetch(`${BACKEND_URL}/api/auth/initiate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_id: parseInt(userId) })
        });

        if (!response.ok) {
            throw new Error('Failed to initiate OAuth');
        }

        const data = await response.json();
        
        // Redirect to Google OAuth URL
        if (data.auth_url) {
            showStatus("🔄 Redirecting to Google...", "loading");
            window.location.href = data.auth_url;
        } else {
            throw new Error('No auth URL received');
        }
    } catch (err) {
        console.error(err);
        showStatus("❌ Failed to start Google login: " + err.message, "error");
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