# GitHub Deployment Guide

## ✅ System is Ready for Deployment!

All features are working:
- ✅ Bank-style 7-layer validation
- ✅ Real email notifications via Gmail SMTP
- ✅ AI-powered dispute resolution
- ✅ Professional web interface
- ✅ 2,278 Visa rules loaded

## Step 1: Initialize Git Repository

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Visa Dispute Resolution System with AI and Email"
```

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., "visa-dispute-agent")
3. **DO NOT** initialize with README (we already have one)
4. Copy the repository URL

## Step 3: Push to GitHub

```bash
# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/visa-dispute-agent.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Secure Your Secrets

**IMPORTANT**: Before deploying, make sure sensitive data is not in the repository:

### Update .gitignore

The `.gitignore` file should already include:
```
.env
*.pyc
__pycache__/
.venv/
*.log
```

### Environment Variables for Deployment

When deploying to a cloud platform, set these environment variables:

```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Email (Gmail SMTP)
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# LLM
LLM_MODEL=llama3.2
LLM_PROVIDER=ollama

# ChromaDB
CHROMADB_HOST=chromadb
CHROMADB_PORT=8000
```

## Step 5: Deploy Options

### Option A: Deploy to Render.com (Recommended - Free Tier)

1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: visa-dispute-agent
   - **Environment**: Docker
   - **Plan**: Free
5. Add environment variables from above
6. Click "Create Web Service"

### Option B: Deploy to Railway.app

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Add environment variables
5. Deploy!

### Option C: Deploy to Heroku

```bash
# Install Heroku CLI
# Then:
heroku create visa-dispute-agent
heroku stack:set container
git push heroku main
```

## Step 6: Post-Deployment Setup

After deployment:

1. **Run database migrations**:
   ```bash
   # On your deployment platform, run:
   alembic upgrade head
   ```

2. **Seed ChromaDB with Visa rules**:
   ```bash
   python scripts/seed_chromadb.py
   ```

3. **Test the system**:
   - Visit your deployed URL
   - Submit a test dispute
   - Check email delivery

## Testing Your Deployment

```bash
# Health check
curl https://your-app-url.com/health

# Test dispute submission
curl -X POST https://your-app-url.com/webhooks/dispute \
  -H "Content-Type: application/json" \
  -d '{
    "dispute_id": "TEST-001",
    "customer_id": "CUST1234",
    "customer_name": "Test User",
    "customer_email": "test@example.com",
    "transaction_id": "TXN123",
    "transaction_date": "2024-11-25",
    "merchant_name": "Test Merchant",
    "card_number": "1234",
    "amount": 1000.00,
    "currency": "INR",
    "reason_code": "10.4",
    "description": "This is a test dispute for unauthorized transaction",
    "timestamp": "2024-11-29T10:00:00Z"
  }'
```

## Monitoring

- Check logs on your deployment platform
- Monitor email delivery
- Review dispute processing in the database

## Security Checklist

- ✅ `.env` file is in `.gitignore`
- ✅ No hardcoded credentials in code
- ✅ SMTP credentials stored as environment variables
- ✅ Database credentials secured
- ✅ API rate limiting enabled
- ✅ Input validation active

## Support

For issues or questions:
1. Check the logs on your deployment platform
2. Review `TROUBLESHOOTING.md`
3. Check GitHub Issues

---

**Your system is production-ready!** 🚀
