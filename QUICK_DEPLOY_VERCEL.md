# ⚡ Quick Vercel Deployment (5 Minutes)

## 🎯 What You'll Deploy

- ✅ **Frontend** → Vercel (Free, Fast, Global CDN)
- ✅ **Backend** → Render (Free, Supports ML models)

---

## 🚀 **5-Minute Deployment**

### **Step 1: Deploy Backend to Render** (2 minutes)

1. Go to **[render.com](https://render.com)** → Sign up (free, no credit card)

2. Click **"New +"** → **"Web Service"**

3. Choose **"Build and deploy from a Git repository"**

4. Connect your GitHub (or create repo first if needed)

5. **Configure:**
```
Name: feedback-backend
Region: Singapore (or nearest)
Branch: main
Root Directory: backend
Runtime: Python 3

Build Command:
pip install -r requirements.txt

Start Command:
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

6. **Environment Variables:**
```
SECRET_KEY = your-secret-key-123
DATABASE_URL = sqlite:///./feedback.db
CORS_ORIGINS = ["*"]
```

7. Click **"Create Web Service"** → Wait 5-10 minutes

8. **Copy your backend URL**: `https://feedback-backend-xxxx.onrender.com`

---

### **Step 2: Deploy Frontend to Vercel** (3 minutes)

#### **Option A: Using Vercel CLI** (Recommended)

```powershell
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend
cd frontend

# Deploy
vercel --prod
```

**When prompted:**
- Project name: `feedback-sentiment-frontend`
- Framework preset: `Vite`
- Build command: `npm run build`
- Output directory: `dist`
- **Environment Variable**: 
  - Name: `VITE_API_URL`
  - Value: `https://feedback-backend-xxxx.onrender.com/api/v1`

#### **Option B: Using Vercel Dashboard** (Easier)

1. Go to **[vercel.com](https://vercel.com)** → Sign up

2. Click **"Add New"** → **"Project"**

3. Import your GitHub repo

4. **Configure:**
```
Framework Preset: Vite
Root Directory: frontend
Build Command: npm run build
Output Directory: dist
```

5. **Environment Variables** → Add:
```
Name: VITE_API_URL
Value: https://feedback-backend-xxxx.onrender.com/api/v1
```

6. Click **"Deploy"** → Wait 2 minutes

7. **Your app is live!** 🎉

---

### **Step 3: Update CORS** (1 minute)

1. Go to **Render dashboard** → Your backend service

2. **Environment** → Add/Update:
```
CORS_ORIGINS = ["https://your-app.vercel.app"]
```

3. Save → Service auto-redeploys

---

## ✅ **You're Live!**

**Frontend URL**: `https://feedback-sentiment-frontend.vercel.app`

**Login** with default admin credentials (check your `backend/app/utils/init_db.py`)

---

## 🔄 **Update Your App**

### **Update Frontend:**
```powershell
cd frontend
git add .
git commit -m "Update frontend"
git push
# Vercel auto-deploys in 30 seconds ⚡
```

### **Update Backend:**
```powershell
cd backend
git add .
git commit -m "Update backend"
git push
# Render auto-deploys in 5 minutes 🚀
```

---

## 🆓 **Free Forever**

Both services remain **100% free** with these limits:

**Vercel:**
- ✅ Unlimited bandwidth
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ 100GB/month

**Render:**
- ✅ 750 hours/month (always on)
- ✅ Automatic HTTPS
- ✅ 1GB storage
- ⚠️ Sleeps after 15 min inactivity (wakes in 60 seconds)

---

## 🐛 **Troubleshooting**

### **Issue: "Cannot connect to backend"**
**Fix:**
1. Check backend is running on Render
2. Verify `VITE_API_URL` in Vercel environment variables
3. Redeploy frontend after changing env vars

### **Issue: "CORS error"**
**Fix:**
1. Go to Render → Environment
2. Update `CORS_ORIGINS` with your Vercel URL
3. Service auto-redeploys

### **Issue: "Backend is slow"**
**Reason:** Render free tier sleeps after 15 minutes
**Fix:** First request wakes it up (~60 seconds)

---

## 💡 **Pro Tips**

1. **Keep backend awake**: Use [UptimeRobot](https://uptimerobot.com) (free) to ping every 5 minutes

2. **Custom domain**: Both Vercel and Render support custom domains (free)

3. **Monitor deployments**: 
   - Vercel: Dashboard shows real-time logs
   - Render: Dashboard → Logs tab

4. **Environment variables**: 
   - Change in dashboard (no code changes needed)
   - Both services auto-redeploy when env vars change

---

## 🎯 **No GitHub? Use This:**

### **Deploy from local without GitHub:**

```powershell
# Backend (Render)
# Use Render's "Deploy from Docker" option

# Frontend (Vercel)
cd frontend
vercel --prod
# Vercel uploads directly from your PC
```

---

## 📊 **What About the Database?**

Your SQLite database (`feedback.db`) is stored on Render's disk:
- ✅ Persists between deployments
- ✅ 1GB free storage
- ⚠️ If service is deleted, database is lost
- 💡 **Backup**: Download from Render dashboard regularly

---

## 🔐 **Security Checklist**

- [x] HTTPS enabled (automatic)
- [ ] Change default admin password after first login
- [ ] Update `SECRET_KEY` in Render
- [ ] Set proper `CORS_ORIGINS` (not `["*"]`)
- [ ] Don't commit secrets to Git

---

## 🎉 **That's It!**

Your feedback sentiment analysis system is now:
- 🌍 Accessible worldwide
- 🔒 Secured with HTTPS
- ⚡ Fast with global CDN
- 🆓 Completely free
- 🔄 Auto-deploys on Git push

**Share your app**: Just send the Vercel URL! 🚀

---

## 📞 **Need Help?**

Check logs:
- **Vercel**: Dashboard → Deployments → Select deployment → Logs
- **Render**: Dashboard → Logs tab

Common error messages:
- "Module not found" → Check `requirements.txt` / `package.json`
- "Port already in use" → Render handles this automatically
- "Build failed" → Check build logs for specific error

