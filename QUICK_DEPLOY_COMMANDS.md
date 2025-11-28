# 🚀 Quick Deploy Commands

Copy and paste these commands to deploy your project!

## Step 1: Configure Git (One-time setup)

```bash
git config --global user.name "Shaik Shafi"
git config --global user.email "sk.mohammadshafi3044@gmail.com"
```

## Step 2: Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `visa-dispute-agent`
3. Click "Create repository"
4. **COPY the commands shown** (they'll include your username)

## Step 3: Push to GitHub

**Replace YOUR_USERNAME with your actual GitHub username!**

```bash
git remote add origin https://github.com/YOUR_USERNAME/visa-dispute-agent.git
git branch -M main
git push -u origin main
```

Example (replace with YOUR username):
```bash
git remote add origin https://github.com/shaikshafi/visa-dispute-agent.git
git branch -M main
git push -u origin main
```

## Step 4: Deploy to Render.com

### 4.1 Create Account
- Go to: https://render.com/
- Sign up with GitHub

### 4.2 Create Database
1. Click "New +" → "PostgreSQL"
2. Name: `visa-disputes-db`
3. Plan: Free
4. Click "Create"
5. **COPY the Internal Database URL**

### 4.3 Deploy Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repo
3. Select `visa-dispute-agent`
4. Settings:
   - Name: `visa-dispute-agent`
   - Runtime: Docker
   - Plan: Free
5. Add environment variables (see below)
6. Click "Create Web Service"

### 4.4 Environment Variables

Add these in Render dashboard:

```
DATABASE_URL=<paste the Internal Database URL from step 4.2>
SMTP_EMAIL=sk.mohammadshafi3044@gmail.com
SMTP_PASSWORD=tmicsjfjtkenuszq
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
CHROMADB_HOST=chromadb
CHROMADB_PORT=8000
LLM_MODEL=llama3.2
LLM_PROVIDER=ollama
LLM_API_KEY=not-needed
LOG_LEVEL=INFO
CONFIDENCE_THRESHOLD=0.85
SIMILARITY_THRESHOLD=0.7
MAX_RETRY_ATTEMPTS=3
```

## Step 5: Post-Deployment

After deployment completes, run these in Render Shell:

```bash
# Run migrations
alembic upgrade head

# Seed Visa rules
python scripts/seed_chromadb.py
```

## Step 6: Test Your Deployment

```bash
# Replace YOUR-APP-NAME with your actual Render app name
curl https://YOUR-APP-NAME.onrender.com/health
```

## 🎉 Done!

Your app is live at: `https://YOUR-APP-NAME.onrender.com`

---

## Troubleshooting

### If git push fails:
```bash
# Check remote
git remote -v

# If wrong, remove and re-add
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/visa-dispute-agent.git
git push -u origin main
```

### If deployment fails:
1. Check logs in Render dashboard
2. Verify all environment variables are set
3. Ensure DATABASE_URL is correct

### If emails don't work:
1. Check SMTP credentials in environment variables
2. Verify Gmail app password is correct
3. Check spam folder

---

**Need help? Check DEPLOY_NOW.md for detailed instructions!**
