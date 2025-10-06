// Backend API URL
const BACKEND_URL = 'http://localhost:8000https://ai-agent-service-uz-lhhv.onrender.com';

// Get user_id from URL parameters
function getUserId() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('user_id');
}

// Show status message
function showStatus(message, type) {
    const statusDiv = document.getElementById('status');
    statusDiv.textContent = message;
    statusDiv.className = `status ${type}`;
}

// Show/hide spinner
function toggleSpinner(show) {
    const spinner = document.getElementById('spinner');
    spinner.className = show ? 'spinner active' : 'spinner';
}

// Initiate Google OAuth flow
async function initiateGoogleAuth() {
    const userId = getUserId();
    
    if (!userId) {
        showStatus('❌ User ID not found. Please start from Telegram bot.', 'error');
        return;
    }
    
    toggleSpinner(true);
    showStatus('🔄 Redirecting to Google...', 'loading');
    
    try {
        const response = await fetch(`${BACKEND_URL}/api/auth/initiate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_id: parseInt(userId) })
        });
        
        if (!response.ok) {
            throw new Error('Failed to initiate authentication');
        }
        
        const data = await response.json();
        
        // Redirect to Google OAuth
        window.location.href = data.auth_url;
        
    } catch (error) {
        console.error('Auth error:', error);
        toggleSpinner(false);
        showStatus('❌ Failed to connect. Please try again.', 'error');
    }
}

// Handle OAuth callback
async function handleOAuthCallback() {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    const state = urlParams.get('state'); // This contains user_id
    const error = urlParams.get('error');
    
    if (error) {
        showStatus(`❌ Authorization cancelled: ${error}`, 'error');
        return;
    }
    
    if (!code || !state) {
        return; // Not a callback URL
    }
    
    toggleSpinner(true);
    showStatus('🔄 Completing authorization...', 'loading');
    
    try {
        const response = await fetch(`${BACKEND_URL}/api/auth/callback`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                code: code,
                user_id: parseInt(state)
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to complete authentication');
        }
        
        const data = await response.json();
        
        toggleSpinner(false);
        showStatus(
            `✅ Successfully connected!\n📧 ${data.email}\n\nYou can now return to Telegram.`,
            'success'
        );
        
        // Optional: Send message to Telegram bot
        notifyTelegramBot(state);
        
        // Redirect back to telegram after 3 seconds
        setTimeout(() => {
            window.location.href = 'https://t.me/YOUR_BOT_USERNAME';
        }, 3000);
        
    } catch (error) {
        console.error('Callback error:', error);
        toggleSpinner(false);
        showStatus('❌ Failed to complete authorization. Please try again.', 'error');
    }
}

// Optional: Notify Telegram bot that auth is complete
async function notifyTelegramBot(userId) {
    // This could trigger a welcome message in the bot
    try {
        await fetch(`${BACKEND_URL}/api/auth/notify`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_id: parseInt(userId) })
        });
    } catch (error) {
        console.error('Notification error:', error);
    }
}

// Check if user is already authenticated
async function checkAuthStatus() {
    const userId = getUserId();
    
    if (!userId) {
        return;
    }
    
    try {
        const response = await fetch(`${BACKEND_URL}/api/auth/status/${userId}`);
        const data = await response.json();
        
        if (data.authenticated) {
            showStatus(
                `✅ Already connected!\n📧 ${data.email}\n\nYou can return to Telegram.`,
                'success'
            );
            
            // Hide the sign-in button
            document.getElementById('googleSignIn').style.display = 'none';
        }
    } catch (error) {
        console.error('Status check error:', error);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Check if this is a callback from Google
    const urlParams = new URLSearchParams(window.location.search);
    
    if (urlParams.has('code')) {
        // Handle OAuth callback
        handleOAuthCallback();
    } else {
        // Normal page load
        checkAuthStatus();
        
        // Set up sign-in button
        const signInButton = document.getElementById('googleSignIn');
        if (signInButton) {
            signInButton.addEventListener('click', initiateGoogleAuth);
        }
    }
});

// Handle errors globally
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    showStatus('❌ An error occurred. Please refresh and try again.', 'error');
    toggleSpinner(false);
});