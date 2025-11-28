# 🚀 Deploy to Vercel

## ⚠️ Important Note

Vercel is optimized for serverless functions and frontend apps. For this full-stack application with:
- PostgreSQL database
- ChromaDB vector store
- Long-running AI processes
- Docker containers

**Recommended alternatives:**
1. **Render.com** (Best for this project - see DEPLOY_NOW.md)
2. **Railway.app** (Good Docker support)
3. **Fly.io** (Excellent for Docker)

However, if you want to try Vercel for the API only (without database/ChromaDB), follow these steps:

## 🔧 Vercel Deployment (API Only)

### Prerequisites
- Vercel account
- GitHub repository pushed
- External PostgreSQL database (e.g., Supabase, Neon)
- External ChromaDB instance

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Login to Vercel

```bash
vercel login
```

### Step 3: Configure Environment Variables

Create a `.env.production` file (don't commit this!):

```bash
# Database (use external service like Supabase or Neon)
DATABASE_URL=postgresql://user:password@host/database

# ChromaDB (use external instance or cloud service)
CHROMADB_HOST=your-chromadb-host
CHROMADB_PORT=8000

# Email
SMTP_EMAIL=sk.mohammadshafi3044@gmail.com
SMTP_PASSWORD=tmicsjfjtkenuszq
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

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

### Step 4: Deploy

```bash
# From project root
vercel

# Follow prompts:
# - Link to existing project? No
# - Project name: visa-dispute-agent
# - Directory: ./
# - Override settings? No
```

### Step 5: Add Environment Variables in Vercel Dashboard

1. Go to https://vercel.com/dashboard
2. Select your project
3. Go to **Settings** → **Environment Variables**
4. Add all variables from `.env.production`

### Step 6: Redeploy

```bash
vercel --prod
```

## ⚠️ Limitations on Vercel

1. **No Docker support** - Can't run PostgreSQL or ChromaDB containers
2. **10-second timeout** - Long AI processing may timeout
3. **Serverless architecture** - Not ideal for stateful applications
4. **Cold starts** - First request after inactivity is slow
5. **No persistent storage** - Need external database

## 🎯 Better Alternative: Use Render.com

Render.com is much better suited for this project because:

✅ **Docker support** - Run full stack with containers
✅ **PostgreSQL included** - Free tier database
✅ **No timeouts** - Long-running processes work fine
✅ **Persistent storage** - ChromaDB data persists
✅ **Free tier** - Same as Vercel

### Quick Render Deployment

```bash
# 1. Go to https://render.com
# 2. Sign up with GitHub
# 3. Click "New +" → "Web Service"
# 4. Select your GitHub repo
# 5. Choose Docker runtime
# 6. Add environment variables
# 7. Deploy!
```

See **DEPLOY_NOW.md** for detailed Render instructions.

## 🔄 Hybrid Approach

You could use:
- **Vercel** for frontend/static site
- **Render** for backend API + database
- **Supabase** for PostgreSQL
- **Pinecone** for vector store (instead of ChromaDB)

But this adds complexity. For simplicity, use Render for everything.

## 📝 Vercel Configuration Files

If you still want to try Vercel:

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app/api/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app/api/main.py"
    }
  ]
}
```

### requirements.txt
Already created - Vercel will use this automatically.

## 🚀 Recommended: Deploy to Render

For the best experience with this project, follow:
- **DEPLOY_NOW.md** - Complete Render deployment guide
- **QUICK_DEPLOY_COMMANDS.md** - Copy-paste commands

Render is free, supports Docker, and perfect for this application!

---

**TL;DR: Use Render.com instead of Vercel for this project. It's easier and better suited for full-stack apps with databases.**
