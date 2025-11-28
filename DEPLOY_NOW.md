# 🚀 Deploy to GitHub & Cloud - Step by Step

## ✅ Your System is Ready!

All code is committed and ready for deployment.

## Step 1: Push to GitHub

### 1.1 Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `visa-dispute-agent` (or your choice)
3. Description: "AI-powered Visa dispute resolution system with email notifications"
4. **Keep it Public** (or Private if you prefer)
5. **DO NOT** check "Initialize with README" (we already have one)
6. Click **Create repository**

### 1.2 Push Your Code

Copy the commands from GitHub (they'll look like this):

```bash
git remote add origin https://github.com/YOUR_USERNAME/visa-dispute-agent.git
git branch -M main
git push -u origin main
```

**Replace YOUR_USERNAME with your actual GitHub username!**

Example:
```bash
git remote add origin https://github.com/shaikshafi/visa-dispute-agent.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Render.com (FREE!)

Render.com offers free hosting perfect for this project.

### 2.1 Create Render Account

1. Go to https://render.com/
2. Click **Get Started**
3. Sign up with GitHub (easiest option)

### 2.2 Create PostgreSQL Database

1. Click **New +** → **PostgreSQL**
2. Name: `visa-disputes-db`
3. Database: `visa_disputes`
4. User: `visa_user`
5. Region: Choose closest to you
6. Plan: **Free**
7. Click **Create Database**
8. **COPY the Internal Database URL** (you'll need this!)

### 2.3 Deploy Web Service

1. Click **New +** → **Web Service**
2. Connect your GitHub repository
3. Select `visa-dispute-agent`
4. Configure:
   - **Name**: `visa-dispute-agent`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Runtime**: `Docker`
   - **Plan**: `Free`

### 2.4 Add Environment Variables

Click **Advanced** → **Add Environment Variable**

Add these variables:

```bash
# Database (use the Internal Database URL from step 2.2)
DATABASE_URL=postgresql://visa_user:password@hostname/visa_disputes

# Email - Gmail SMTP
SMTP_EMAIL=sk.mohammadshafi3044@gmail.com
SMTP_PASSWORD=tmicsjfjtkenuszq
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# ChromaDB
CHROMADB_HOST=chromadb
CHROMADB_PORT=8000

# LLM
LLM_MODEL=llama3.2
LLM_PROVIDER=ollama
LLM_API_KEY=not-needed

# App Config
LOG_LEVEL=INFO
CONFIDENCE_THRESHOLD=0.85
SIMILARITY_THRESHOLD=0.7
MAX_RETRY_ATTEMPTS=3
```

### 2.5 Deploy!

1. Click **Create Web Service**
2. Wait 5-10 minutes for deployment
3. Your app will be live at: `https://visa-dispute-agent.onrender.com`

## Step 3: Post-Deployment Setup

### 3.1 Run Database Migrations

In Render dashboard:
1. Go to your web service
2. Click **Shell** tab
3. Run:
```bash
alembic upgrade head
```

### 3.2 Seed Visa Rules

In the Shell:
```bash
python scripts/seed_chromadb.py
```

### 3.3 Test Your Deployment

```bash
# Health check
curl https://your-app-name.onrender.com/health

# Test dispute
curl -X POST https://your-app-name.onrender.com/webhooks/dispute \
  -H "Content-Type: application/json" \
  -d '{
    "dispute_id": "PROD-TEST-001",
    "customer_id": "CUST1234",
    "customer_name": "Test User",
    "customer_email": "sk.mohammadshafi1@gmail.com",
    "transaction_id": "TXN123456",
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

## Alternative: Deploy to Railway.app

### Quick Deploy

1. Go to https://railway.app/
2. Click **Start a New Project**
3. Select **Deploy from GitHub repo**
4. Choose your repository
5. Add environment variables (same as above)
6. Click **Deploy**

Railway automatically detects Docker and deploys!

## Alternative: Deploy to Fly.io

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Launch app
flyctl launch

# Set secrets
flyctl secrets set SMTP_EMAIL=your-email@gmail.com
flyctl secrets set SMTP_PASSWORD=your-password
# ... add all other env vars

# Deploy
flyctl deploy
```

## 🎉 You're Live!

Your Visa Dispute Resolution System is now:
- ✅ Hosted on the cloud
- ✅ Accessible via public URL
- ✅ Sending real emails
- ✅ Processing disputes with AI
- ✅ Production-ready!

## 📊 Monitor Your App

### Render Dashboard
- View logs
- Monitor CPU/Memory
- Check request metrics
- Restart if needed

### Check Logs
```bash
# In Render Shell
tail -f /var/log/app.log
```

## 🔧 Troubleshooting

### App won't start?
- Check environment variables are set correctly
- View logs in Render dashboard
- Ensure DATABASE_URL is correct

### Emails not sending?
- Verify SMTP credentials
- Check spam folder
- Consider switching to SendGrid (see SENDGRID_SETUP.md)

### Database errors?
- Run migrations: `alembic upgrade head`
- Check DATABASE_URL format
- Ensure PostgreSQL is running

## 🎯 Next Steps

1. **Custom Domain**: Add your own domain in Render settings
2. **SendGrid**: Set up for better email delivery
3. **Monitoring**: Add Sentry or similar for error tracking
4. **Scaling**: Upgrade to paid plan when needed

## 💡 Tips

- **Free tier limitations**: 
  - Render: Spins down after 15 min inactivity
  - First request after sleep takes ~30 seconds
  - Upgrade to paid ($7/month) for always-on

- **Cost optimization**:
  - Use SendGrid free tier (100 emails/day)
  - PostgreSQL free tier is sufficient for testing
  - Upgrade only when you need more resources

---

**Congratulations! Your AI-powered dispute resolution system is live! 🚀**

Share your deployment URL and start processing disputes!
