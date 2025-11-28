# 🔧 Fix Render Deployment Error

## The Problem

Your deployment failed with "Exited with status 3" because the Docker container tried to connect to services (PostgreSQL, ChromaDB) that weren't available during build.

## ✅ Solution

I've simplified the Dockerfile to just run the app without trying to connect to databases during startup.

## 🚀 Redeploy Steps

### 1. Push the Fixed Code

```bash
git add .
git commit -m "Fix Render deployment - simplified Dockerfile"
git push
```

### 2. In Render Dashboard

1. Go to your service: https://dashboard.render.com/
2. Click on `visa-dispute-agent`
3. Click **"Manual Deploy"** → **"Deploy latest commit"**
4. Wait for deployment (5-10 minutes)

### 3. After Deployment Succeeds

Open the **Shell** tab in Render and run:

```bash
# Run migrations
alembic upgrade head

# Seed Visa rules (this might take a few minutes)
python scripts/seed_chromadb.py
```

## 🎯 Alternative: Simpler Deployment

If the above still fails, try this minimal approach:

### Option A: Deploy Without Database First

1. In Render, **remove** the `DATABASE_URL` environment variable temporarily
2. Redeploy
3. Once app is running, add database later

### Option B: Use Render Blueprint

1. Delete the current service
2. Click **"New"** → **"Blueprint"**
3. Connect your GitHub repo
4. Render will auto-detect `render.yaml` and deploy correctly

## 🐛 Common Issues

### Issue: "Module not found"
**Fix**: Make sure `requirements.txt` has all dependencies:
```bash
# Check locally
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### Issue: "Port binding failed"
**Fix**: Render uses dynamic PORT. Update Dockerfile CMD:
```dockerfile
CMD uvicorn app.api.main:app --host 0.0.0.0 --port $PORT
```

### Issue: "Database connection failed"
**Fix**: 
1. Create PostgreSQL database first in Render
2. Copy the **Internal Database URL**
3. Add as `DATABASE_URL` environment variable
4. Redeploy

## 📝 Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Dockerfile simplified (no database connections during build)
- [ ] Environment variables set in Render
- [ ] Service deployed successfully
- [ ] Health check passes: `/health`
- [ ] Migrations run in Shell
- [ ] Visa rules seeded
- [ ] Test the web interface

## 🆘 Still Not Working?

### Quick Test Locally

```bash
# Build Docker image
docker build -t visa-dispute-test .

# Run container
docker run -p 8000:8000 \
  -e SMTP_EMAIL=sk.mohammadshafi3044@gmail.com \
  -e SMTP_PASSWORD=tmicsjfjtkenuszq \
  -e SMTP_SERVER=smtp.gmail.com \
  -e SMTP_PORT=587 \
  visa-dispute-test

# Test
curl http://localhost:8000/health
```

If this works locally, the issue is with Render configuration.

## 💡 Recommended: Use Railway Instead

Railway is often easier for Docker deployments:

1. Go to https://railway.app/
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose `mohammadshafishaik/visa-dispute-agent`
5. Add environment variables
6. Deploy!

Railway auto-detects Docker and handles everything.

---

**The fixed code is ready. Just push and redeploy!** 🚀
