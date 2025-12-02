# 🚀 Vercel Deployment Guide

## 📋 Overview

This guide deploys:
- **Frontend**: Vercel (React + TypeScript + Vite)
- **Backend**: Render.com (Python FastAPI + ML models)

## Why This Setup?

| Component | Platform | Reason |
|-----------|----------|--------|
| Frontend | Vercel | ⚡ Global CDN, instant deploys, free SSL |
| Backend | Render | 🧠 Supports ML libraries (transformers, PyTorch) |

---

## 🎯 Step-by-Step Deployment

### **Step 1: Deploy Backend to Render** (5 minutes)

1. **Push code to GitHub** (if not already):
```powershell
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/feedback-v6.git
git push -u origin main
```

2. **Go to [render.com](https://render.com)** and sign up (free, no credit card)

3. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Name: `feedback-backend`
   - Region: Choose closest to you
   - Branch: `main`
   - Root Directory: `backend`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables**:
```
SECRET_KEY = your-secret-key-here
DATABASE_URL = sqlite:///./feedback.db
CORS_ORIGINS = ["https://your-frontend.vercel.app"]
```

5. **Deploy** → Wait 5-10 minutes (ML models take time to install)

6. **Copy your backend URL**: `https://feedback-backend.onrender.com`

---

### **Step 2: Deploy Frontend to Vercel** (2 minutes)

1. **Update API URL** in `frontend/.env.production`:
```bash
VITE_API_URL=https://feedback-backend.onrender.com/api/v1
```

2. **Install Vercel CLI**:
```powershell
npm install -g vercel
```

3. **Deploy**:
```powershell
cd frontend
vercel
```

**Follow prompts:**
- Set up and deploy? `Y`
- Which scope? (Your account)
- Link to existing project? `N`
- Project name? `feedback-sentiment-frontend`
- In which directory? `./` (current directory)
- Override settings? `N`

4. **Deploy to production**:
```powershell
vercel --prod
```

**Your frontend URL**: `https://feedback-sentiment-frontend.vercel.app`

---

### **Step 3: Update CORS on Backend**

After frontend deploys, update backend CORS settings:

**Go to Render dashboard** → Your web service → Environment → Add:
```
CORS_ORIGINS = ["https://feedback-sentiment-frontend.vercel.app"]
```

**Or edit** `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://feedback-sentiment-frontend.vercel.app",
        "http://localhost:5173"  # Keep for local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🎉 **You're Live!**

- **Frontend**: `https://feedback-sentiment-frontend.vercel.app`
- **Backend**: `https://feedback-backend.onrender.com`

---

## 🔄 **Auto-Deployment**

### **Vercel** (Frontend):
```powershell
# Just push to GitHub
git add .
git commit -m "Update frontend"
git push

# Vercel auto-deploys in 30 seconds
```

### **Render** (Backend):
```powershell
# Push to GitHub
git add .
git commit -m "Update backend"
git push

# Render auto-deploys in 5 minutes
```

---

## 🆓 **Free Tier Limits**

### **Vercel**:
- ✅ Unlimited bandwidth
- ✅ Unlimited builds
- ✅ 100GB/month
- ✅ Free SSL
- ✅ No credit card needed

### **Render**:
- ✅ 750 hours/month (enough for 1 service)
- ✅ Free SSL
- ⚠️ Sleeps after 15 min inactivity (wakes in ~60 seconds)
- ✅ No credit card needed

---

## ⚡ **Alternative: Vercel Only (Frontend)**

If you want to run backend locally and only deploy frontend:

```powershell
# 1. Start backend locally
cd backend
python start_server.py

# 2. Use ngrok to expose backend
ngrok http 8000

# 3. Update frontend/.env.production with ngrok URL
VITE_API_URL=https://abc123.ngrok.io/api/v1

# 4. Deploy to Vercel
cd frontend
vercel --prod
```

---

## 🐛 **Troubleshooting**

### **Issue: CORS errors**
**Fix**: Update `backend/app/main.py` with your Vercel URL

### **Issue: Backend sleeps on Render**
**Fix**: First request takes ~60 seconds to wake. Keep alive with:
```javascript
// frontend/src/App.tsx
useEffect(() => {
  // Ping backend every 10 minutes
  setInterval(() => {
    fetch('https://feedback-backend.onrender.com/health')
  }, 600000)
}, [])
```

### **Issue: Environment variables not working**
**Fix**: Rebuild both services after changing env vars

---

## 🎯 **Custom Domain** (Optional)

### **Vercel**:
1. Go to project settings → Domains
2. Add your domain (e.g., `feedback.yourdomain.com`)
3. Update DNS records as shown

### **Render**:
1. Go to web service → Settings → Custom Domain
2. Add domain
3. Update DNS

---

## 📊 **Monitoring**

### **Vercel**:
- Dashboard shows: Deployments, Analytics, Logs
- Real-time deployment status

### **Render**:
- Dashboard shows: Logs, Metrics, Events
- Check health: `https://feedback-backend.onrender.com/health`

---

## 💡 **Tips**

1. **First deployment is slow** (10 min) - ML models are large
2. **Subsequent deploys are faster** (cached dependencies)
3. **Keep backend warm**: Add cron job or uptime monitor
4. **Monitor usage**: Both platforms show usage in dashboard

---

## 🔐 **Security Checklist**

- [ ] Update `SECRET_KEY` in Render environment variables
- [ ] Set proper `CORS_ORIGINS`
- [ ] Enable HTTPS only (both platforms do this by default)
- [ ] Don't commit `.env` files to Git
- [ ] Use environment variables for all secrets

---

## 📱 **Share Your App**

Just share the Vercel URL:
```
https://feedback-sentiment-frontend.vercel.app
```

**Default credentials** (as per your system):
- Admin: Check `backend/utils/init_db.py` for default admin credentials

---

## 🚀 **Next Steps**

1. **Deploy backend** → Get URL
2. **Update frontend env** → Add backend URL
3. **Deploy frontend** → Get Vercel URL
4. **Update CORS** → Add Vercel URL to backend
5. **Test** → Open Vercel URL in browser
6. **Share** → Send link to users!

---

**Need help?** Check logs:
- **Vercel**: Dashboard → Deployments → Click deployment → Logs
- **Render**: Dashboard → Logs tab

