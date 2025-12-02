# Quick Start Guide

## 5-Minute Setup

### Step 1: Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example or create manually)
# Minimum required:
# DATABASE_URL=postgresql://user:password@localhost:5432/feedback_db
# SECRET_KEY=your-secret-key-here

# Initialize database
python -m app.utils.init_db

# Start server
uvicorn app.main:app --reload
```

Backend will run on: `http://localhost:8000`

### Step 2: Frontend Setup (2 minutes)

```bash
# Open new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on: `http://localhost:3000`

### Step 3: Login (1 minute)

1. Open browser: `http://localhost:3000`
2. Login with:
   - **Email**: `admin@example.com`
   - **Password**: `admin123`

### Step 4: Test Upload

1. Create a test CSV file `test_feedback.csv`:

```csv
trainee_id,location,training_batch,rating_score,open_text
T001,Bangalore,Batch-2024-01,4,"The trainer explained concepts clearly. Very helpful."
T002,Chennai,Batch-2024-01,2,"Software access issues. Unable to login."
T003,Mumbai,Batch-2024-01,5,"Great mentor support. Always available for doubts."
T004,Delhi,Batch-2024-01,3,"The curriculum pace is too fast. Need more time."
T005,Bangalore,Batch-2024-01,5,"Excellent infrastructure. Everything works smoothly."
```

2. Go to Upload page
3. Select the CSV file
4. Click "Upload and Process"
5. Wait for processing (sentiment analysis happens automatically)

### Step 5: View Dashboard

1. Navigate to Dashboard
2. You'll see:
   - Overall sentiment metrics
   - Sentiment distribution charts
   - Action items (if any)
   - Executive summary

### Step 6: Generate Report

1. Go to Reports page
2. Click "Generate Report" (or use API)
3. View weekly analysis

## Troubleshooting

### Database Connection Error

**Error**: `could not connect to server`

**Solution**:
1. Ensure PostgreSQL is running
2. Create database: `createdb feedback_db`
3. Update DATABASE_URL in `.env` file

### Port Already in Use

**Error**: `Address already in use`

**Solution**:
- Backend: Change port in `uvicorn app.main:app --reload --port 8001`
- Frontend: Update `vite.config.ts` port or use `npm run dev -- --port 3001`

### Model Download Takes Time

**First Run**: The sentiment analysis model downloads automatically (5-10 minutes)
- This is normal
- Requires internet connection
- Only happens once

### Frontend Can't Connect to Backend

**Error**: `Network Error` or `CORS Error`

**Solution**:
1. Verify backend is running on port 8000
2. Check `frontend/src/services/api.ts` has correct URL
3. Verify CORS settings in `backend/app/main.py`

## Quick API Test

Test the API directly:

```bash
# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=admin123"

# Get current user (use token from login)
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Next Steps

1. ✅ Upload more feedback data
2. ✅ Explore dashboard visualizations
3. ✅ Generate weekly reports
4. ✅ Review action items and insights
5. ✅ Test different user roles (create via Admin panel)

## Need Help?

- **Detailed Setup**: See `SETUP_GUIDE.md`
- **Requirements**: See `REQUIREMENT_ANALYSIS.md`
- **Project Overview**: See `PROJECT_SUMMARY.md`
- **API Documentation**: http://localhost:8000/docs (when backend is running)

---

**Ready to go!** 🚀



