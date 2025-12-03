# CSV Upload Testing Guide

## Sample CSV Files Created

I've created two sample CSV files for testing:

### 1. `sample_feedback.csv` (Full Version)
- **30 rows** of sample feedback data
- Includes all columns including optional `category_tags`
- Variety of feedback types:
  - Positive feedback (rating 4-5)
  - Negative feedback (rating 1-2)
  - Neutral feedback (rating 3)
- Covers all 6 categories:
  - Trainer Feedback
  - Mentor Support
  - Batch Owner Experience
  - Infrastructure
  - Training Program
  - Engagement Experience
- Multiple locations: Bangalore, Chennai, Mumbai, Delhi, Hyderabad
- Multiple batches: Batch-2024-01

### 2. `sample_feedback_simple.csv` (Quick Test)
- **5 rows** of sample feedback
- Only required columns (no category_tags)
- Quick test file for basic functionality

## How to Test Upload

### Step 1: Start the Application

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python -m app.utils.init_db
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Step 2: Login

1. Open browser: `http://localhost:3000`
2. Login with:
   - Email: `admin@example.com`
   - Password: `admin123`

### Step 3: Upload CSV File

1. Navigate to **Upload** page (visible for Admin users)
2. Click **"Select File"** button
3. Choose `sample_feedback.csv` or `sample_feedback_simple.csv`
4. Click **"Upload and Process"**
5. Wait for processing (sentiment analysis happens automatically)

### Step 4: View Results

After upload, you'll see:
- ✅ Success message
- Total rows processed
- Number of records saved
- Any errors (if any)

### Step 5: View Dashboard

1. Go to **Dashboard** page
2. You should see:
   - Sentiment metrics from uploaded data
   - Charts showing sentiment distribution
   - Action items (if negative feedback detected)
   - Executive summary

## Expected Results

### With `sample_feedback.csv` (30 rows):

**Sentiment Distribution:**
- Positive: ~50-60% (ratings 4-5)
- Neutral: ~10-20% (rating 3)
- Negative: ~20-30% (ratings 1-2)

**Categories Detected:**
- Infrastructure (most common in negative feedback)
- Trainer
- Mentor
- Training Program
- Batch Owner
- Engagement

**Action Items Generated:**
- Infrastructure issues (software, hardware, network)
- Training program concerns (pacing, assessments)
- Mentor response time improvements

**Heat Index:**
- Should be around 60-75 (good engagement)

## CSV Format Requirements

### Required Columns:
- `trainee_id` - Unique identifier (string)
- `location` - City/region (string)
- `training_batch` - Batch identifier (string)
- `rating_score` - Numeric rating 1-5 (optional but recommended)
- `open_text` - Feedback text (required)

### Optional Columns:
- `category_tags` - Comma-separated category tags
- `week_start_date` - Date in YYYY-MM-DD format
- `week_end_date` - Date in YYYY-MM-DD format

## Testing Different Scenarios

### Test 1: Valid CSV Upload
- Use `sample_feedback.csv`
- Should succeed with all rows processed

### Test 2: Missing Required Column
- Remove `open_text` column
- Should show error: "Missing required columns: open_text"

### Test 3: Invalid Rating
- Add row with rating_score = 10
- Should be ignored or set to None (validation)

### Test 4: Empty Feedback Text
- Add row with empty `open_text`
- Should show error for that specific row

### Test 5: Excel File
- Convert CSV to Excel (.xlsx)
- Should work the same way

## What Happens After Upload

1. **File Validation**
   - Checks file format (CSV/Excel)
   - Validates required columns
   - Checks data types

2. **Data Processing**
   - Each row is processed individually
   - Data is cleaned and normalized
   - Dates are parsed (if provided)

3. **Sentiment Analysis**
   - Each `open_text` is analyzed
   - Sentiment classified: Positive/Neutral/Negative
   - Emotional tone detected
   - Confidence score calculated

4. **Category Mapping**
   - Feedback mapped to relevant categories
   - Keywords matched
   - Relevance scores calculated

5. **Database Storage**
   - Feedback records saved
   - Sentiment analysis results saved
   - Category mappings saved

6. **Results Returned**
   - Total rows processed
   - Successfully saved count
   - Error list (if any)

## Troubleshooting

### Error: "Not authorized to upload files"
- **Solution**: Login as Admin or System Owner
- Batch Owner and Leadership roles cannot upload

### Error: "Missing required columns"
- **Solution**: Check CSV has all required columns
- Column names are case-insensitive
- Spaces are automatically converted to underscores

### Error: "Unsupported file type"
- **Solution**: Use .csv, .xlsx, or .xls files only

### Processing Takes Long Time
- **Normal**: First upload downloads ML model (5-10 minutes)
- Subsequent uploads are faster
- Large files (>1000 rows) take longer

### No Data in Dashboard
- **Solution**: 
  - Generate weekly report after upload
  - Check if week dates are correct
  - Verify data was saved (check database)

## Next Steps After Upload

1. **Generate Weekly Report**
   - Go to Reports page
   - Generate report for the week
   - View detailed analysis

2. **View Trends**
   - Check Dashboard for sentiment trends
   - Compare with previous weeks (if data exists)

3. **Review Action Items**
   - Check Dashboard for generated action items
   - Prioritize based on urgency

4. **Export Data** (Future)
   - Export filtered feedback
   - Download reports as PDF

## Sample Data Insights

The `sample_feedback.csv` file includes:
- **Infrastructure issues**: 7 mentions (software, hardware, network)
- **Positive trainer feedback**: 4 mentions
- **Mentor appreciation**: 5 mentions
- **Training program concerns**: 4 mentions (pacing, assessments)
- **Engagement activities**: 4 positive mentions

This variety helps test:
- Sentiment classification accuracy
- Category mapping
- Risk flag detection
- Action item generation
- Trend analysis

---

**Ready to test!** Upload the sample CSV files and explore the dashboard! 🚀




