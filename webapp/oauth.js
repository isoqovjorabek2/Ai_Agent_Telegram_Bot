//const BACKEND_URL = window.APP_CONFIG.BACKEND_URL;

function getUserId() {
    const params = new URLSearchParams(window.location.search);
    return params.get("user_id");
}

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

async function startGoogleLogin() {
    console.log("▶️ Google login button clicked");

    const userId = getUserId();
    if (!userId) {
        console.warn("⚠️ No user_id found in URL");
        showStatus("❌ User ID not found", "error");
        return;
    }
    console.log("✅ Found user_id:", userId);

    try {
        showStatus("🔄 Connecting to backend...", "loading");
        console.log("🌐 Sending request to:", `${BACKEND_URL}/api/auth/initiate`);

        const response = await fetch(`${BACKEND_URL}/api/auth/initiate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: parseInt(userId) })
        });

        console.log("📩 Response status:", response.status);

        if (!response.ok) {
            throw new Error('Failed to initiate OAuth');
        }

        const data = await response.json();
        console.log("📦 Response data:", data);

        if (data.auth_url) {
            console.log("➡️ Redirecting to Google:", data.auth_url);
            showStatus("🔄 Redirecting to Google...", "loading");
            window.location.href = data.auth_url;
        } else {
            throw new Error('No auth URL received');
        }
    } catch (err) {
        console.error("❌ Google login error:", err.message);
        showStatus("❌ Failed to start Google login: " + err.message, "error");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("googleSignIn");
    btn.addEventListener("click", startGoogleLogin);
    console.log("✅ Google Sign-In button event listener attached");

    if (!getUserId()) {
        console.warn("⚠️ No user ID detected. Opened outside Telegram?");
        showStatus("⚠️ No user ID detected. Opened outside Telegram?", "error");
    }
});
