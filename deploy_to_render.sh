#!/bin/bash

# Automated Render.com Deployment Script
# This script helps automate deployment but requires manual steps for account creation

echo "🚀 Visa Dispute Agent - Render.com Deployment Helper"
echo "=================================================="
echo ""

# Check if render CLI is installed
if ! command -v render &> /dev/null; then
    echo "❌ Render CLI not found. Installing..."
    echo ""
    echo "Please install Render CLI manually:"
    echo "  npm install -g @render-com/cli"
    echo ""
    echo "Or visit: https://render.com/docs/cli"
    exit 1
fi

echo "✅ Render CLI found"
echo ""

# Check if logged in
echo "Checking Render authentication..."
if ! render whoami &> /dev/null; then
    echo "❌ Not logged in to Render"
    echo ""
    echo "Please run: render login"
    echo "Then run this script again"
    exit 1
fi

echo "✅ Authenticated with Render"
echo ""

# Get GitHub repo
GITHUB_REPO="mohammadshafishaik/visa-dispute-agent"
echo "📦 GitHub Repository: $GITHUB_REPO"
echo ""

# Create PostgreSQL database
echo "📊 Creating PostgreSQL database..."
echo ""
echo "Please create database manually in Render dashboard:"
echo "1. Go to: https://dashboard.render.com/new/database"
echo "2. Name: visa-disputes-db"
echo "3. Database: visa_disputes"
echo "4. User: visa_user"
echo "5. Plan: Free"
echo "6. Click 'Create Database'"
echo ""
read -p "Press Enter after creating database and copying Internal Database URL..."
echo ""

read -p "Paste the Internal Database URL: " DATABASE_URL
echo ""

# Create web service
echo "🌐 Creating web service..."
echo ""
echo "Please create web service manually in Render dashboard:"
echo "1. Go to: https://dashboard.render.com/create?type=web"
echo "2. Connect GitHub repository: $GITHUB_REPO"
echo "3. Name: visa-dispute-agent"
echo "4. Runtime: Docker"
echo "5. Plan: Free"
echo ""
echo "Environment Variables to add:"
echo "================================"
echo "DATABASE_URL=$DATABASE_URL"
echo "SMTP_EMAIL=sk.mohammadshafi3044@gmail.com"
echo "SMTP_PASSWORD=tmicsjfjtkenuszq"
echo "SMTP_SERVER=smtp.gmail.com"
echo "SMTP_PORT=587"
echo "CHROMADB_HOST=chromadb"
echo "CHROMADB_PORT=8000"
echo "LLM_MODEL=llama3.2"
echo "LLM_PROVIDER=ollama"
echo "LLM_API_KEY=not-needed"
echo "LOG_LEVEL=INFO"
echo "CONFIDENCE_THRESHOLD=0.85"
echo "SIMILARITY_THRESHOLD=0.7"
echo "MAX_RETRY_ATTEMPTS=3"
echo "================================"
echo ""
read -p "Press Enter after deployment completes..."
echo ""

# Get service URL
read -p "Enter your Render service URL (e.g., https://visa-dispute-agent.onrender.com): " SERVICE_URL
echo ""

# Test deployment
echo "🧪 Testing deployment..."
echo ""
curl -s "$SERVICE_URL/health" | python3 -m json.tool
echo ""

echo "✅ Deployment complete!"
echo ""
echo "📝 Next steps:"
echo "1. Run migrations in Render Shell:"
echo "   alembic upgrade head"
echo ""
echo "2. Seed Visa rules:"
echo "   python scripts/seed_chromadb.py"
echo ""
echo "3. Test your app:"
echo "   $SERVICE_URL"
echo ""
echo "🎉 Your AI-powered dispute resolution system is live!"
