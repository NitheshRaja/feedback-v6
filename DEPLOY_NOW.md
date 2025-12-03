# 🚀 DEPLOY NOW - Complete Action Guide

**Status**: ✅ All prerequisites installed and ready!

---

## ✅ COMPLETED STEPS

- [x] Git installed (v2.47.0)
- [x] Node.js installed (v22.11.0)
- [x] Vercel CLI installed
- [x] Project structure verified
- [x] Git repository initialized
- [x] All files committed to Git

**You're 100% ready to deploy!**

---

## 🎯 NEXT: Choose Your Deployment Path

### **Option A: Quick Deploy (Recommended)** ⚡
**Time**: 15-20 minutes  
**Difficulty**: Easy  
**Best for**: Getting online fast

### **Option B: Detailed Deploy** 📖
**Time**: 25-30 minutes  
**Difficulty**: Very Easy  
**Best for**: Understanding each step

---

# 🚀 OPTION A: QUICK DEPLOY (Follow These Steps)

## STEP 1: Create GitHub Repository (3 minutes)

1. **Go to**: https://github.com/new
2. **Repository name**: `feedback-v6` (or any name you want)
3. **Visibility**: Choose Public or Private
4. **DON'T** initialize with README, .gitignore, or license
5. Click **"Create repository"**
6. **Copy the repository URL** shown (looks like: `https://github.com/YOUR_USERNAME/feedback-v6.git`)

---

## STEP 2: Push Code to GitHub (1 minute)

Run these commands in your terminal (replace YOUR_USERNAME with your GitHub username):

```powershell
# Connect to GitHub repo
git remote add origin https://github.com/YOUR_USERNAME/feedback-v6.git

# Push code
git branch -M main
git push -u origin main
```

**Verify**: Refresh your GitHub page - you should see all your files!

---

## STEP 3: Deploy Backend to Render (10 minutes)

1. **Go to**: https://render.com
2. **Sign up/Login** with GitHub (click "Get Started for Free")
3. Authorize Render to access GitHub
4. Click **"New +"** (top right) → **"Web Service"**
5. Click **"Build and deploy from a Git repository"** → **"Next"**
6. Find your `feedback-v6` repo → Click **"Connect"**

### Configuration:

**Basic Settings:**
```
Name: feedback-backend
Region: Singapore (or closest to you)
Branch: main
Root Directory: backend
Runtime: Python 3
```

**Build Settings:**
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

### Environment Variables:

Click **"Advanced"** → Scroll to **"Environment Variables"** → Add these:

```
SECRET_KEY = change-this-to-random-string-abc123xyz
DATABASE_URL = sqlite:///./feedback.db
CORS_ORIGINS = http://localhost:5173
SENTIMENT_MODEL = cardiffnlp/twitter-roberta-base-sentiment-latest
DEVICE = cpu
```

### Add Persistent Disk:

Scroll to **"Disks"** → Click **"Add Disk"**:
```
Name: feedback-db
Mount Path: /opt/render/project/src
Size: 1 GB
```

7. Click **"Create Web Service"**
8. **Wait 5-10 minutes** (watch the logs)
9. When you see **"Live"** badge → **COPY YOUR URL**:
   ```
   https://feedback-backend-xxxx.onrender.com
   ```

**Test it**: Open `https://feedback-backend-xxxx.onrender.com/health` in browser
Should show: `{"status": "healthy"}`

---

## STEP 4: Deploy Frontend to Vercel (5 minutes)

Back in your terminal (in D:\feedback_v6):

```powershell
# Login to Vercel
vercel login
```

Follow the login prompts (opens browser)

```powershell
# Navigate to frontend
cd frontend

# Deploy
vercel --prod
```

### Answer the prompts:

```
? Set up and deploy? [Y/n]
→ Y

? Which scope?
→ (Select your account)

? Link to existing project? [y/N]
→ N

? What's your project's name?
→ feedback-sentiment-frontend

? In which directory is your code located?
→ ./ (just press Enter)

? Want to override the settings?
→ N
```

**During deployment**, when asked about environment variables:

```
Add environment variable? Y

Name: VITE_API_URL
Value: https://feedback-backend-xxxx.onrender.com/api/v1
(Use YOUR backend URL from Step 3)

Add another? N
```

---

## STEP 5: Connect Frontend & Backend (2 minutes)

1. **Copy your Vercel URL** from the terminal output:
   ```
   https://feedback-sentiment-frontend.vercel.app
   ```

2. **Go to Render dashboard**: https://dashboard.render.com
3. Click your **"feedback-backend"** service
4. Click **"Environment"** tab on the left
5. Find **"CORS_ORIGINS"** → Click **"Edit"**
6. Change to:
   ```
   https://feedback-sentiment-frontend.vercel.app,http://localhost:5173
   ```
7. Click **"Save Changes"**
8. Service will auto-redeploy (wait 2-3 minutes)

---

## STEP 6: TEST YOUR APP! 🎉

1. Open: `https://feedback-sentiment-frontend.vercel.app`
2. You should see the login page
3. Try logging in with default credentials:
   - Check `backend/app/utils/init_db.py` for default admin credentials
4. If login works → **SUCCESS!** 🎉

---

## ✅ DEPLOYMENT COMPLETE!

**Your URLs**:
- **Frontend**: `https://feedback-sentiment-frontend.vercel.app`
- **Backend**: `https://feedback-backend-xxxx.onrender.com`
- **API Docs**: `https://feedback-backend-xxxx.onrender.com/api/v1/docs`

**Record these in**: `DEPLOYMENT_URLS.md`

---

## 🔄 To Update Your App Later:

### Update Backend:
```powershell
cd D:\feedback_v6\backend
# Make changes...
git add .
git commit -m "Update backend"
git push
# Render auto-deploys in 3-5 minutes
```

### Update Frontend:
```powershell
cd D:\feedback_v6\frontend
# Make changes...
git add .
git commit -m "Update frontend"
git push
# Then redeploy
vercel --prod
```

---

## 🐛 TROUBLESHOOTING

### Issue: "Can't connect to backend"
**Solution**:
1. Check backend is "Live" on Render dashboard
2. Verify CORS_ORIGINS includes your Vercel URL
3. Check VITE_API_URL in Vercel dashboard → Settings → Environment Variables

### Issue: "Backend is slow"
**Normal**: Free tier sleeps after 15 min. First request takes ~60 seconds to wake.

### Issue: "Build failed on Render"
**Solution**: Check logs in Render dashboard. Most common: wait longer (ML models are 700MB+)

---

## 🔐 SECURITY CHECKLIST

After deployment:
- [ ] Change default admin password (login → settings)
- [ ] Update SECRET_KEY in Render to a random secure string
- [ ] Verify CORS_ORIGINS doesn't include `*`
- [ ] Don't commit .env files

---

## 📊 Keep Backend Awake (Optional)

Free tier sleeps after 15 minutes. To keep it awake:

1. Go to: https://uptimerobot.com (free)
2. Sign up
3. Add monitor:
   - Type: HTTP(s)
   - URL: `https://feedback-backend-xxxx.onrender.com/health`
   - Interval: 5 minutes
4. Save

Backend now stays awake 24/7!

---

# 📖 OPTION B: DETAILED DEPLOY

If you prefer step-by-step explanations with more detail:

**Open**: `DEPLOYMENT_STEPS.md`

That guide has:
- Screenshots descriptions
- Detailed explanations
- More troubleshooting
- Pro tips

---

## 🎯 YOU'RE READY!

Follow **Option A** above for quick deployment, or open `DEPLOYMENT_STEPS.md` for detailed walkthrough.

**Start with STEP 1** above!

Good luck! 🚀


