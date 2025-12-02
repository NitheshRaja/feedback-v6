# 🚀 Complete Deployment Guide - Hybrid Approach

## 📋 What We're Deploying

- **Frontend** → Vercel (React + TypeScript + Vite)
- **Backend** → Render (Python FastAPI + ML Models)
- **Database** → SQLite on Render (Persistent disk)

**Total Cost**: $0/month ✨

---

## ✅ Pre-Deployment Checklist

Before starting, make sure you have:

- [ ] GitHub account (free)
- [ ] Vercel account (free, no credit card needed)
- [ ] Render account (free, no credit card needed)
- [ ] Git installed on your PC
- [ ] Node.js installed (for Vercel CLI)

---

# 🎯 PART 1: Deploy Backend to Render (10 minutes)

## Step 1.1: Push Code to GitHub

```powershell
# Initialize Git (if not already done)
cd d:\feedback_v6
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Ready for deployment"

# Create GitHub repo (go to github.com/new)
# Then connect and push:
git remote add origin https://github.com/YOUR_USERNAME/feedback-v6.git
git branch -M main
git push -u origin main
```

---

## Step 1.2: Create Web Service on Render

1. **Go to [render.com](https://render.com)**
2. Sign up with GitHub (authorize access)
3. Click **"New +"** → **"Web Service"**
4. Click **"Build and deploy from a Git repository"**
5. Select your `feedback-v6` repository
6. Click **"Connect"**

---

## Step 1.3: Configure Service

**Basic Settings:**
```
Name: feedback-backend
Region: Singapore (or closest to you)
Branch: main
Root Directory: backend
Runtime: Python 3
```

**Build & Deploy:**
```
Build Command:
pip install -r requirements.txt

Start Command:
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Instance Type:**
```
Free
```

---

## Step 1.4: Add Environment Variables

Click **"Advanced"** → **Environment Variables** → Add these:

```bash
# Required
SECRET_KEY = your-secret-key-change-this-to-random-string-123456789
DATABASE_URL = sqlite:///./feedback.db
CORS_ORIGINS = http://localhost:5173

# Optional (Redis - can skip for now)
# REDIS_URL = redis://localhost:6379/0

# ML Model (default values work)
SENTIMENT_MODEL = cardiffnlp/twitter-roberta-base-sentiment-latest
DEVICE = cpu
```

**Important**: Keep CORS_ORIGINS as `http://localhost:5173` for now. We'll update it after deploying frontend.

---

## Step 1.5: Add Persistent Disk (for Database)

Scroll down to **"Disks"** → Click **"Add Disk"**

```
Name: feedback-db
Mount Path: /opt/render/project/src
Size: 1 GB (free tier)
```

This ensures your database persists between deployments!

---

## Step 1.6: Deploy!

1. Click **"Create Web Service"**
2. Wait 5-10 minutes (ML models are large)
3. Watch the logs scroll by
4. When you see: ✅ **"Live"** - it's ready!

**Copy your backend URL**: 
```
https://feedback-backend-xxxx.onrender.com
```

---

## Step 1.7: Test Backend

Open in browser:
```
https://feedback-backend-xxxx.onrender.com/health
```

Should return:
```json
{"status": "healthy"}
```

✅ **Backend is live!**

---

# 🎨 PART 2: Deploy Frontend to Vercel (5 minutes)

## Step 2.1: Install Vercel CLI

```powershell
npm install -g vercel
```

---

## Step 2.2: Login to Vercel

```powershell
vercel login
```

Follow the prompts to authenticate.

---

## Step 2.3: Deploy Frontend

```powershell
cd d:\feedback_v6\frontend
vercel --prod
```

**Answer the prompts:**

```
? Set up and deploy "feedback_v6"? [Y/n] Y
? Which scope? (Your account name)
? Link to existing project? [y/N] N
? What's your project's name? feedback-sentiment-frontend
? In which directory is your code located? ./
? Want to modify these settings? [y/N] N
```

---

## Step 2.4: Add Environment Variable

**During deployment**, Vercel will ask about environment variables.

**OR** add via dashboard:

1. Go to **[vercel.com/dashboard](https://vercel.com/dashboard)**
2. Click your project → **"Settings"** → **"Environment Variables"**
3. Add:

```
Name: VITE_API_URL
Value: https://feedback-backend-xxxx.onrender.com/api/v1
Environment: Production
```

4. Click **"Save"**

---

## Step 2.5: Redeploy (if you added env var after)

```powershell
vercel --prod
```

Wait 30 seconds... ✅ **Done!**

**Your frontend URL**:
```
https://feedback-sentiment-frontend.vercel.app
```

---

# 🔗 PART 3: Connect Frontend & Backend (2 minutes)

## Step 3.1: Update CORS on Backend

1. Go to **Render dashboard**
2. Click your **"feedback-backend"** service
3. Click **"Environment"** tab
4. Find **"CORS_ORIGINS"**
5. Update to:

```
https://feedback-sentiment-frontend.vercel.app,http://localhost:5173
```

6. Click **"Save Changes"**
7. Service auto-redeploys (2-3 minutes)

---

## Step 3.2: Test Connection

1. Open your Vercel URL:
   ```
   https://feedback-sentiment-frontend.vercel.app
   ```

2. Try to login with default credentials (check `backend/app/utils/init_db.py`)

3. If login works → ✅ **Everything is connected!**

---

# 🎉 YOU'RE LIVE!

Your app is now:
- 🌍 Accessible worldwide
- 🔒 Secured with HTTPS
- ⚡ Fast with global CDN
- 🆓 Completely free
- 🔄 Auto-deploys on Git push

---

## 📊 Your URLs

**Frontend**: `https://feedback-sentiment-frontend.vercel.app`
**Backend**: `https://feedback-backend-xxxx.onrender.com`
**API Docs**: `https://feedback-backend-xxxx.onrender.com/api/v1/docs`

---

# 🔄 Making Updates

## Update Frontend:

```powershell
cd frontend
# Make your changes...
git add .
git commit -m "Update frontend"
git push

# Vercel auto-deploys in 30 seconds!
```

## Update Backend:

```powershell
cd backend
# Make your changes...
git add .
git commit -m "Update backend"
git push

# Render auto-deploys in 3-5 minutes
```

---

# 🐛 Troubleshooting

## Issue: "Cannot connect to backend"

**Check:**
1. Backend is running (green "Live" badge on Render)
2. CORS_ORIGINS includes your Vercel URL
3. VITE_API_URL is correct in Vercel environment variables

**Fix:**
```powershell
# Redeploy frontend
cd frontend
vercel --prod
```

---

## Issue: "CORS error in browser console"

**Fix:**
1. Render dashboard → Environment
2. Update CORS_ORIGINS:
   ```
   https://your-actual-vercel-url.vercel.app,http://localhost:5173
   ```
3. Save → Auto-redeploys

---

## Issue: "Backend is slow (60 seconds)"

**Reason**: Free tier sleeps after 15 min inactivity

**Solutions:**
1. **Accept it** - First request wakes it up
2. **Keep awake** - Use [UptimeRobot](https://uptimerobot.com):
   - Create free account
   - Add monitor: `https://your-backend.onrender.com/health`
   - Check every 5 minutes
   - Backend stays awake! ⏰

---

## Issue: "Database reset after deployment"

**Check**: Did you add the persistent disk?
1. Render dashboard → Your service
2. Scroll to "Disks"
3. Should see: `feedback-db` mounted at `/opt/render/project/src`

**If missing**: Add it now (see Step 1.5)

---

## Issue: "Build failed on Render"

**Common causes:**
1. **Python version mismatch** - Add to environment:
   ```
   PYTHON_VERSION = 3.11.0
   ```

2. **Missing dependencies** - Check `requirements.txt`

3. **Torch too large** - It's 700MB, be patient (10 min first build)

**View logs**: Render dashboard → Logs tab

---

# 💡 Pro Tips

## 1. Custom Domain (Optional)

**Vercel:**
1. Settings → Domains → Add Domain
2. Follow DNS setup instructions
3. Free SSL included!

**Render:**
1. Settings → Custom Domain → Add
2. Update DNS (CNAME or A record)
3. Free SSL included!

---

## 2. Environment Variables

**Change without code changes:**
1. Update in dashboard (Render or Vercel)
2. Service auto-redeploys
3. No Git commit needed!

---

## 3. Monitor Your App

**Vercel Analytics** (free):
- Dashboard → Analytics
- See traffic, performance, geography

**Render Metrics** (free):
- Dashboard → Metrics
- See CPU, memory, response times

---

## 4. Backup Database

**Download from Render:**
1. Connect to shell: Dashboard → Shell tab
2. Run:
   ```bash
   cat feedback.db > /tmp/backup.db
   ```
3. Or use persistent disk backup features

**Recommended**: Weekly backups during development

---

## 5. View Logs

**Vercel Logs:**
- Dashboard → Deployments → Select → Logs
- Real-time frontend errors

**Render Logs:**
- Dashboard → Logs tab
- Real-time backend logs
- Filter by error/warning

---

# 🔐 Security Checklist

After deployment:

- [ ] Change SECRET_KEY in Render environment variables
- [ ] Update default admin password on first login
- [ ] Set proper CORS_ORIGINS (not `*`)
- [ ] Don't commit `.env` files
- [ ] Enable 2FA on GitHub/Vercel/Render accounts
- [ ] Regularly update dependencies

---

# 📈 Scaling (Future)

When you outgrow free tier:

**Vercel Pro** ($20/month):
- Better analytics
- Team collaboration
- Priority support

**Render Paid** ($7-25/month):
- No sleep time
- More resources
- Better performance

**PostgreSQL** (free on Render):
- More robust than SQLite
- Better for multiple users
- Easy migration

---

# 🎯 Success Criteria

✅ Frontend loads at Vercel URL
✅ Can login successfully
✅ Can upload CSV file
✅ Sentiment analysis works
✅ Reports generate
✅ No CORS errors in console

---

# 📞 Need Help?

**Check:**
1. Vercel Status: [vercel-status.com](https://www.vercel-status.com/)
2. Render Status: [status.render.com](https://status.render.com/)
3. View logs in both dashboards

**Common mistakes:**
- Forgot to add VITE_API_URL to Vercel
- Wrong CORS_ORIGINS on Render
- Didn't add persistent disk
- Backend still deploying (check "Live" badge)

---

# 🎉 Congratulations!

You've successfully deployed a **production-grade ML application** with:
- ⚡ React frontend on global CDN
- 🧠 AI-powered sentiment analysis
- 📊 Real-time data processing
- 🔒 Secure authentication
- 💾 Persistent database
- 🆓 Zero cost

**Total deployment time**: ~20 minutes
**Monthly cost**: $0
**Performance**: Production-ready ✨

Share your app URL with the world! 🚀

