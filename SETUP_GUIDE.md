# L1 Feedback Sentiment Analysis - Setup Guide

## Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- PostgreSQL 12 or higher
- Redis (optional, for caching)

## Backend Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the `backend` directory:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/feedback_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
API_V1_STR=/api/v1
PROJECT_NAME=L1 Feedback Sentiment Analysis
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
MAX_UPLOAD_SIZE=10485760
UPLOAD_DIR=./uploads
SENTIMENT_MODEL=cardiffnlp/twitter-roberta-base-sentiment-latest
DEVICE=cpu
```

### 4. Setup Database

```bash
# Create PostgreSQL database
createdb feedback_db

# Initialize database tables and create admin user
python -m app.utils.init_db
```

Default admin credentials:
- Email: `admin@example.com`
- Password: `admin123`

**⚠️ IMPORTANT: Change the default password in production!**

### 5. Download NLP Models

The sentiment analysis model will be downloaded automatically on first use. This may take a few minutes.

### 6. Run Backend Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment (Optional)

Create a `.env` file in the `frontend` directory:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

### 3. Run Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Usage

### 1. Login

- Navigate to `http://localhost:3000/login`
- Use admin credentials: `admin@example.com` / `admin123`

### 2. Upload Feedback Data

1. Go to the Upload page (Admin only)
2. Select a CSV or Excel file with the following columns:
   - `trainee_id` (required)
   - `location` (required)
   - `training_batch` (required)
   - `rating_score` (optional, 1-5)
   - `open_text` (required)
   - `category_tags` (optional, comma-separated)
   - `week_start_date` (optional)
   - `week_end_date` (optional)

3. Click "Upload and Process"
4. The system will automatically:
   - Process the file
   - Perform sentiment analysis
   - Map categories
   - Store results in database

### 3. View Dashboard

- Navigate to the Dashboard to see:
  - Overall sentiment metrics
  - Week-over-week trends
  - Category breakdowns
  - Action items
  - Executive summary

### 4. Generate Reports

- Go to Reports page
- View weekly reports
- Generate new reports for specific weeks

## File Format Example

### CSV Format

```csv
trainee_id,location,training_batch,rating_score,open_text,category_tags
T001,Bangalore,Batch-2024-01,4,"The trainer explained concepts clearly. Very helpful.",trainer
T002,Chennai,Batch-2024-01,2,"Software access issues. Unable to login.",infrastructure
T003,Mumbai,Batch-2024-01,5,"Great mentor support. Always available for doubts.",mentor
```

### Excel Format

Same columns as CSV, saved as `.xlsx` or `.xls`

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user

### Feedback
- `POST /api/v1/feedback/upload` - Upload feedback file
- `GET /api/v1/feedback/` - List feedback records

### Analysis
- `GET /api/v1/analysis/trends` - Get trend analysis
- `GET /api/v1/analysis/insights` - Get actionable insights
- `GET /api/v1/analysis/lifecycle` - Get lifecycle trends
- `GET /api/v1/analysis/category-trends` - Get category trends

### Reports
- `POST /api/v1/reports/weekly/generate` - Generate weekly report
- `GET /api/v1/reports/weekly/{week_id}` - Get report by ID
- `GET /api/v1/reports/weekly` - List reports

### Users (Admin only)
- `GET /api/v1/users/` - List users
- `POST /api/v1/users/` - Create user
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

## User Roles

### Admin
- Full system access
- Upload/manage feedback
- View all reports
- User management

### Batch Owner
- View batch-specific reports
- Track batch trends
- Limited to assigned batches

### Leadership
- Consolidated dashboard view
- Executive summaries
- High-level insights only

### System Owner
- All admin permissions
- System configuration
- Audit logs access

## Troubleshooting

### Backend Issues

1. **Database Connection Error**
   - Verify PostgreSQL is running
   - Check DATABASE_URL in .env file
   - Ensure database exists

2. **Model Download Fails**
   - Check internet connection
   - Model downloads automatically on first use
   - May take 5-10 minutes

3. **Import Errors**
   - Ensure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`

### Frontend Issues

1. **API Connection Error**
   - Verify backend is running on port 8000
   - Check VITE_API_URL in .env
   - Check CORS settings in backend

2. **Build Errors**
   - Clear node_modules: `rm -rf node_modules && npm install`
   - Check Node.js version (16+)

## Production Deployment

### Backend

1. Set strong SECRET_KEY in .env
2. Use production database (not local)
3. Configure proper CORS_ORIGINS
4. Use process manager (PM2, supervisor)
5. Enable HTTPS
6. Set up proper logging

### Frontend

1. Build production bundle: `npm run build`
2. Serve static files with nginx or similar
3. Configure API URL for production
4. Enable HTTPS

## Next Steps

- [ ] Implement PDF report generation
- [ ] Add trainee lifecycle stage detection
- [ ] Enhance category mapping with ML
- [ ] Add email notifications
- [ ] Implement scheduled report generation
- [ ] Add more visualization options
- [ ] Enhance executive summary generation

## Support

For issues or questions, refer to the REQUIREMENT_ANALYSIS.md document for detailed specifications.



