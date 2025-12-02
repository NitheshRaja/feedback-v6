# 🌐 Deployment URLs & Credentials

**Fill this in after deploying!**

---

## 📋 Production URLs

### Frontend (Vercel)
**URL**: `https://_________________________________.vercel.app`

**Dashboard**: https://vercel.com/dashboard

---

### Backend (Render)
**URL**: `https://_________________________________.onrender.com`

**API Docs**: `https://_________________________________.onrender.com/api/v1/docs`

**Health Check**: `https://_________________________________.onrender.com/health`

**Dashboard**: https://dashboard.render.com/

---

## 🔑 Credentials

### Admin User
**Username**: _________________________________

**Email**: _________________________________

**Password**: _________________________________ 
*(Change this immediately after first login!)*

---

### API Keys

**SECRET_KEY**: _________________________________
*(Store securely, never commit to Git)*

---

## 📊 Environment Variables

### Vercel (Frontend)
```
VITE_API_URL = https://_________________________________.onrender.com/api/v1
```

### Render (Backend)
```
SECRET_KEY = _________________________________
DATABASE_URL = sqlite:///./feedback.db
CORS_ORIGINS = https://_________________________________.vercel.app,http://localhost:5173
SENTIMENT_MODEL = cardiffnlp/twitter-roberta-base-sentiment-latest
DEVICE = cpu
```

---

## 🗓️ Deployment Info

**Deployed On**: _________________________________

**Deployed By**: _________________________________

**Git Repository**: https://github.com/_________________________________

**Last Updated**: _________________________________

---

## 🔗 Quick Links

| Service | Link |
|---------|------|
| Frontend | [Open](https://_________________________________.vercel.app) |
| Backend | [Open](https://_________________________________.onrender.com) |
| API Docs | [Open](https://_________________________________.onrender.com/api/v1/docs) |
| Vercel Dashboard | [Open](https://vercel.com/dashboard) |
| Render Dashboard | [Open](https://dashboard.render.com/) |
| GitHub Repo | [Open](https://github.com/_________________________________) |

---

## 📈 Monitoring

### UptimeRobot (Optional - Keep backend awake)
**Monitor URL**: https://_________________________________.onrender.com/health

**Check Interval**: Every 5 minutes

**Dashboard**: https://uptimerobot.com/dashboard

---

## 🔄 Deployment Commands

### Deploy Frontend
```powershell
cd frontend
vercel --prod
```

### Deploy Backend (Auto on Git push)
```powershell
git add .
git commit -m "Update backend"
git push
```

---

## 📞 Support Contacts

**Technical Issues**: _________________________________

**Account Owner**: _________________________________

---

## 🛡️ Security Notes

- [ ] Changed default admin password
- [ ] Updated SECRET_KEY to random string
- [ ] Removed test users (if any)
- [ ] Verified CORS settings
- [ ] Set up 2FA on hosting accounts
- [ ] Database backup schedule: _________________

---

## 📝 Notes

_Add any deployment-specific notes here..._

---

**Last Updated**: _________________________________

