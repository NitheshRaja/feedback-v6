# ✅ Deployment Checklist - Hybrid Approach

Copy this checklist and check off items as you complete them!

---

## 📦 Pre-Deployment

- [ ] Git installed and configured
- [ ] GitHub account created
- [ ] Node.js installed (for Vercel CLI)
- [ ] Render.com account created (free)
- [ ] Vercel.com account created (free)

---

## 🔧 Code Preparation

- [ ] All code committed locally
- [ ] Database file excluded from Git (already in .gitignore)
- [ ] Environment variables documented
- [ ] Tested app locally (backend + frontend work together)

---

## 🚀 PART 1: Backend Deployment (Render)

### Push to GitHub
- [ ] Created GitHub repository
- [ ] Pushed code to GitHub main branch
- [ ] Verified files are visible on GitHub

### Render Setup
- [ ] Created Render account
- [ ] Authorized GitHub access
- [ ] Created new Web Service
- [ ] Connected to GitHub repository

### Configuration
- [ ] Set Name: `feedback-backend`
- [ ] Set Root Directory: `backend`
- [ ] Set Build Command: `pip install -r requirements.txt`
- [ ] Set Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Environment Variables
- [ ] Added `SECRET_KEY` (use random string)
- [ ] Added `DATABASE_URL` = `sqlite:///./feedback.db`
- [ ] Added `CORS_ORIGINS` = `http://localhost:5173`
- [ ] Added `SENTIMENT_MODEL` = `cardiffnlp/twitter-roberta-base-sentiment-latest`
- [ ] Added `DEVICE` = `cpu`

### Persistent Disk
- [ ] Added disk named: `feedback-db`
- [ ] Set mount path: `/opt/render/project/src`
- [ ] Set size: 1 GB

### Deploy & Test
- [ ] Clicked "Create Web Service"
- [ ] Waited 5-10 minutes for deployment
- [ ] Saw "Live" green badge
- [ ] Copied backend URL: `https://feedback-backend-____.onrender.com`
- [ ] Tested health endpoint: `/health` returns `{"status": "healthy"}`
- [ ] Tested API docs: `/api/v1/docs` loads successfully

---

## 🎨 PART 2: Frontend Deployment (Vercel)

### Vercel CLI Setup
- [ ] Installed Vercel CLI: `npm install -g vercel`
- [ ] Logged in: `vercel login`
- [ ] Verified login successful

### Deploy
- [ ] Navigated to: `cd d:\feedback_v6\frontend`
- [ ] Ran: `vercel --prod`
- [ ] Answered prompts correctly
- [ ] Deployment completed successfully
- [ ] Copied frontend URL: `https://feedback-sentiment-frontend.vercel.app`

### Environment Variable
- [ ] Went to Vercel dashboard
- [ ] Clicked project → Settings → Environment Variables
- [ ] Added `VITE_API_URL` = `https://feedback-backend-____.onrender.com/api/v1`
- [ ] Set Environment: Production
- [ ] Saved changes
- [ ] Redeployed: `vercel --prod`

---

## 🔗 PART 3: Connect Services

### Update CORS
- [ ] Went to Render dashboard
- [ ] Clicked backend service → Environment
- [ ] Updated `CORS_ORIGINS` to: `https://your-vercel-url.vercel.app,http://localhost:5173`
- [ ] Saved changes
- [ ] Waited for auto-redeploy (2-3 minutes)
- [ ] Verified "Live" badge appears again

### Test Connection
- [ ] Opened frontend URL in browser
- [ ] No console errors
- [ ] Login page loads
- [ ] Tried logging in (with default credentials)
- [ ] Login successful
- [ ] Dashboard loads
- [ ] Tested uploading CSV file
- [ ] Sentiment analysis works
- [ ] Report generation works

---

## 🎉 Post-Deployment

### Security
- [ ] Changed default admin password
- [ ] Updated SECRET_KEY to secure random string
- [ ] Verified CORS_ORIGINS doesn't include `*`
- [ ] Confirmed `.env` files not in Git

### Documentation
- [ ] Documented frontend URL
- [ ] Documented backend URL
- [ ] Documented API credentials
- [ ] Saved deployment configuration

### Monitoring
- [ ] Bookmarked Vercel dashboard
- [ ] Bookmarked Render dashboard
- [ ] Set up UptimeRobot (optional - keeps backend awake)
- [ ] Tested auto-deployment (push to GitHub)

---

## 🚨 Troubleshooting Completed

If you encountered issues, check these off once resolved:

- [ ] Fixed CORS errors
- [ ] Fixed environment variable issues
- [ ] Fixed build/deployment failures
- [ ] Fixed database persistence
- [ ] Fixed slow backend response (first wake-up)

---

## 📊 Final Verification

Test all features in production:

- [ ] ✅ User login/logout
- [ ] ✅ CSV file upload
- [ ] ✅ Feedback filtering
- [ ] ✅ Sentiment analysis display
- [ ] ✅ Report generation
- [ ] ✅ PDF download
- [ ] ✅ All pages load correctly
- [ ] ✅ No console errors
- [ ] ✅ Mobile responsive (optional test)

---

## 🎯 Success!

When ALL items are checked:

**Your Feedback Sentiment Analysis System is LIVE! 🚀**

**Frontend**: _____________________________
**Backend**: _____________________________
**Deployed on**: _____________________________
**Deployed by**: _____________________________

---

## 📞 Quick Reference

**Redeploy Frontend:**
```powershell
cd frontend
vercel --prod
```

**Redeploy Backend:**
```powershell
git add .
git commit -m "Update"
git push
# Render auto-deploys
```

**View Logs:**
- Vercel: Dashboard → Deployments → Select → Logs
- Render: Dashboard → Logs tab

**Update Environment Variables:**
- Vercel: Dashboard → Settings → Environment Variables
- Render: Dashboard → Environment tab

---

**Deployment Guide**: See `DEPLOYMENT_STEPS.md` for detailed instructions

