/**
 * Vercel Serverless Function - Environment Variables
 * 
 * This endpoint dynamically injects environment variables into the webapp.
 * Configure ENV_BACKEND_URL in Vercel dashboard under Environment Variables.
 */

export default function handler(req, res) {
  // Set CORS headers for API access
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET");
  res.setHeader("Content-Type", "application/javascript");
  
  // Default to localhost for development
  const backendUrl = process.env.ENV_BACKEND_URL || "http://localhost:8000";
  
  // Return JavaScript that sets window variables
  res.send(`
// Environment variables injected by Vercel serverless function
window.ENV_BACKEND_URL = "${backendUrl}";
window.ENV_CONFIG_LOADED = true;

console.log("✅ Environment loaded from Vercel:", {
  BACKEND_URL: window.ENV_BACKEND_URL
});
  `.trim());
}