#!/bin/bash
# This script generates env.js with environment variables for Vercel deployment
# It should be run as part of the Vercel build process

echo "Generating env.js with environment variables..."

cat > env.js << EOF
// This file is auto-generated during build
// Environment variables are injected here
window.ENV_BACKEND_URL = "${ENV_BACKEND_URL}";
EOF

echo "✅ env.js generated successfully"
cat env.js
