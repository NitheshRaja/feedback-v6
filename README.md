# L1 Feedback Sentiment Analysis Application

An automated sentiment analysis system for weekly L1 trainee feedback that provides real-time insights, trend analysis, and actionable recommendations.

## Features

- **Automated Sentiment Analysis**: Classify feedback into Positive/Neutral/Negative with emotional tone detection
- **Category-Based Insights**: Analyze feedback across 6 engagement dimensions
- **Trend Analysis**: Weekly comparisons and pattern recognition
- **Actionable Insights**: AI-generated recommendations and risk flags
- **Engagement Heat Index**: 0-100 score based on multiple factors
- **Trainee Lifecycle Tracking**: Monitor sentiment across new joiner → intermediate → graduate stages
- **Role-Based Dashboards**: Customized views for Admin, Batch Owner, Leadership, and System Owner
- **PDF Reports**: Automated executive summary generation

## Technology Stack

### Backend
- Python 3.9+
- FastAPI (REST API)
- PostgreSQL (Database)
- SQLAlchemy (ORM)
- Redis (Caching)
- Transformers/Hugging Face (NLP)
- pandas (Data Processing)

### Frontend
- React 18+ with TypeScript
- Material-UI / Ant Design
- Recharts (Visualizations)
- React Router

## Project Structure

```
feedback_v6/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   ├── ml/             # ML/NLP models
│   │   └── utils/          # Utilities
│   ├── requirements.txt
│   └── main.py
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── utils/          # Utilities
│   ├── package.json
│   └── public/
├── docs/                    # Documentation
└── REQUIREMENT_ANALYSIS.md  # Detailed requirements
```

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Redis (optional, for caching)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

Proprietary - Internal Use Only




