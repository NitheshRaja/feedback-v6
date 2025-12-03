# L1 Feedback Sentiment Analysis Application - Requirement Analysis

## 1. Executive Summary

**Project Goal**: Build an automated sentiment analysis system for weekly L1 trainee feedback that replaces manual review processes and provides real-time insights across multiple engagement dimensions.

**Key Value Propositions**:
- Automated sentiment classification and trend analysis
- Category-based insights across 6 engagement dimensions
- Actionable recommendations and risk flagging
- Multi-role dashboard with role-based access control
- Trainee lifecycle sentiment tracking (new joiner → intermediate → graduate)

---

## 2. System Architecture Overview

### 2.1 Technology Stack Recommendation

**Frontend**:
- React.js with TypeScript (for interactive dashboards)
- Chart.js/Recharts (for visualizations)
- Material-UI or Ant Design (for UI components)
- React Router (for navigation)

**Backend**:
- Python FastAPI (for REST API)
- SQLAlchemy (for ORM)
- PostgreSQL (for structured data storage)
- Redis (for caching and session management)

**AI/ML Layer**:
- Transformers (Hugging Face) for sentiment analysis
- spaCy/NLTK for NLP preprocessing
- scikit-learn for classification models
- pandas for data processing

**File Processing**:
- pandas for CSV/Excel parsing
- openpyxl for Excel file handling

**Reporting**:
- ReportLab or WeasyPrint for PDF generation
- Jinja2 for template rendering

### 2.2 System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React.js)                      │
│  - Dashboard UI                                             │
│  - Data Upload Interface                                    │
│  - Role-based Views                                         │
│  - Interactive Charts & Heatmaps                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                 Backend API (FastAPI)                       │
│  - Authentication & Authorization                           │
│  - File Upload & Processing                                 │
│  - Sentiment Analysis Endpoints                             │
│  - Report Generation                                        │
│  - Data Export                                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              AI/ML Processing Layer                         │
│  - Sentiment Classification Engine                          │
│  - Category Mapping Engine                                  │
│  - Trend Analysis Engine                                    │
│  - Insight Generation Engine                                │
│  - Heat Index Calculator                                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              Data Storage Layer                             │
│  - PostgreSQL (Feedback data, users, reports)               │
│  - Redis (Caching, sessions)                                │
│  - File Storage (Uploaded CSV/Excel files)                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Detailed Functional Requirements

### 3.1 Data Input & Processing

**Input Formats**:
- CSV files (comma-separated)
- Excel files (.xlsx, .xls)
- API endpoint for automated sync

**Required Fields**:
- `trainee_id` (masked/anonymized)
- `location` (city/region)
- `training_batch` (batch identifier)
- `category_tags` (optional, comma-separated)
- `rating_score` (1-5 numeric)
- `open_text_feedback` (free text)

**Processing Flow**:
1. File validation (format, required columns)
2. Data cleaning (null handling, encoding issues)
3. Data normalization (standardize locations, batch names)
4. Store raw data in database
5. Trigger sentiment analysis pipeline

### 3.2 Sentiment Analysis Engine

**Classification Levels**:

**Level 1 - Sentiment Categories**:
- **Positive**: Satisfaction, appreciation, enthusiasm
- **Neutral**: Factual statements, no strong emotion
- **Negative**: Complaints, dissatisfaction, concerns

**Level 2 - Emotional Tones**:
- Confusion
- Stress/Anxiety
- Motivation/Enthusiasm
- Satisfaction
- Frustration
- Appreciation

**Implementation Approach**:
- Fine-tuned transformer model (e.g., BERT-based sentiment classifier)
- Multi-label classification for emotional tones
- Confidence scores for each classification

### 3.3 Category Mapping System

**Categories**:
1. **Trainer Feedback** (effectiveness, delivery, clarity, engagement)
2. **Mentor Support** (responsiveness, clarity, availability)
3. **Batch Owner Experience** (process clarity, support, responsiveness)
4. **Infrastructure** (software, hardware, network accessibility)
5. **Training Program** (curriculum pacing, relevance, assessments)
6. **Engagement Experience** (overall environment, communication, onboarding)

**Mapping Logic**:
- **Rule-based**: Use category tags if provided
- **NLP-based**: Keyword extraction and context analysis
- **Hybrid**: Combine rule-based and ML-based classification
- **Multi-category**: Single feedback can map to multiple categories

**Keyword Examples**:
- Trainer: "trainer", "instructor", "teaching", "explanation", "clarity"
- Infrastructure: "software", "laptop", "internet", "access", "system"
- Training Program: "curriculum", "pacing", "assessment", "exam", "syllabus"

### 3.4 Trend Analysis & Comparison

**Weekly Comparison Metrics**:
- Sentiment percentage change (e.g., +12%, -8%)
- Category-wise sentiment shifts
- Volume changes (feedback count)
- Rating score trends

**Visualization Requirements**:
- Line charts for sentiment trends over time
- Bar charts for category comparisons
- Heatmaps for sentiment distribution across categories
- Sparklines for quick trend indicators

**Calculation Logic**:
```
Week-over-week change = ((Current Week - Previous Week) / Previous Week) * 100
```

### 3.5 Actionable Insights Engine

**Insight Types**:

1. **Recommended Action Items**:
   - Based on negative sentiment patterns
   - Frequency of specific issues
   - Urgency scoring

2. **Critical Risk Flags**:
   - Sudden sentiment drops (>15% decrease)
   - High frequency of critical keywords
   - Escalation patterns

3. **Urgent Escalations**:
   - Infrastructure failures
   - Trainer/mentor availability issues
   - Assessment-related stress spikes

4. **Root Cause Predictions**:
   - Pattern matching against historical data
   - Correlation analysis (e.g., assessment week → lower sentiment)
   - Confidence scoring for predictions

**Example Output Format**:
```
Risk Flag: Infrastructure complaints increased by 18%
Confidence: 85%
Root Cause: Software access issues (27 mentions in last 2 weeks)
Recommended Action: Escalate to IT team, prioritize ticket resolution
```

### 3.6 Engagement Heat Index

**Calculation Formula**:
```
Heat Index (0-100) = 
  (Positive Sentiment % × 0.4) +
  (Average Rating Score / 5 × 30) +
  (Participation Volume Score × 0.2) +
  (Engagement Keywords Score × 0.1)
```

**Components**:
- **Sentiment Score** (40%): Percentage of positive feedback
- **Rating Score** (30%): Average rating normalized to 0-30
- **Participation Volume** (20%): Feedback count relative to expected
- **Engagement Keywords** (10%): Frequency of engagement-related terms

**Scoring Scale**:
- 80-100: Excellent engagement
- 60-79: Good engagement
- 40-59: Moderate engagement (needs attention)
- 0-39: Poor engagement (urgent intervention required)

### 3.7 Trainee Lifecycle Sentiment Tracking

**Trainee Stages**:
1. **New Joiner** (0-4 weeks)
2. **Intermediate** (5-12 weeks)
3. **About to Graduate** (13+ weeks or final 4 weeks)

**Tracking Requirements**:
- Weekly sentiment trends per stage
- Monthly aggregated sentiment
- Overall trend analysis (all stages combined)
- Stage-specific insights (e.g., new joiners need more onboarding support)

**Visualization**:
- Stacked area charts showing sentiment distribution across stages
- Stage-wise comparison charts
- Transition analysis (sentiment changes as trainees progress)

---

## 4. Reporting & Dashboard Requirements

### 4.1 Weekly Sentiment Dashboard

**Components**:
1. **Executive Summary Card**:
   - Overall sentiment score
   - Week-over-week change
   - Heat index
   - Total feedback count

2. **Category Sentiment Breakdown**:
   - Sentiment distribution per category (pie/bar chart)
   - Category-wise heatmap
   - Top performing vs. underperforming categories

3. **Trend Visualization**:
   - 8-week sentiment trend line
   - Category-wise trend lines
   - Volume trend

4. **Top Insights Panel**:
   - Top 3 strengths
   - Top 3 concerns
   - Action recommendations
   - Risk flags

5. **Appreciation Tracker**:
   - Positive feedback highlights
   - Trainer/mentor recognition
   - Shoutout quotes

### 4.2 Executive Summary Report

**Sections**:
1. **Week Overview**:
   - Date range
   - Overall sentiment score and change
   - Heat index

2. **Top Strengths** (Top 3):
   - Category
   - Key points
   - Supporting quotes

3. **Top Concerns** (Top 3):
   - Category
   - Issue description
   - Frequency/impact
   - Recommended actions

4. **Trend Explanation**:
   - Week-over-week analysis
   - Contextual factors (e.g., assessment week)
   - Pattern recognition insights

5. **Priority Focus for Next Week**:
   - Action items ranked by priority
   - Owner assignments
   - Expected impact

### 4.3 PDF Export Format

**Structure**:
- Cover page with week range and key metrics
- Executive summary (1 page)
- Detailed category analysis (1 page per category)
- Trend charts and graphs
- Action items and recommendations
- Appendix (methodology, data sources)

---

## 5. User Roles & Access Control

### 5.1 Role Definitions

**Admin**:
- Full system access
- Upload/manage feedback data
- View all reports and dashboards
- Export data (CSV, PDF)
- User management
- System configuration

**Batch Owner**:
- View batch-specific reports
- Track batch sentiment trends
- Service line insights
- Export batch reports
- Cannot access other batches' data

**Leadership**:
- Consolidated dashboard view only
- Executive summary reports
- High-level trends and insights
- No detailed feedback access
- No data export (except executive reports)

**System Owner**:
- All admin permissions
- Audit logs access
- Model configuration and tuning
- System performance monitoring
- Data backup and recovery

### 5.2 Access Control Implementation

**Backend**:
- JWT-based authentication
- Role-based middleware for endpoint protection
- Data filtering based on user role

**Frontend**:
- Route guards for protected pages
- Conditional rendering based on permissions
- Role-specific navigation menus

---

## 6. Intelligence Layer Specifications

### 6.1 Sentiment-Shift Detection

**Algorithm**:
- Compare current week sentiment distribution with previous week
- Calculate statistical significance (t-test or chi-square)
- Flag shifts >10% with confidence >80%

**Output**:
```
Sentiment Shift Detected: Negative sentiment increased by 12%
Previous Week: 25% negative
Current Week: 37% negative
Confidence: 87%
```

### 6.2 Repeated Keyword Alerts

**Process**:
1. Extract keywords from negative feedback
2. Track keyword frequency over time windows (2 weeks, 4 weeks)
3. Alert when frequency exceeds threshold (e.g., 20+ mentions)

**Example**:
```
Alert: "Software access" mentioned 27 times in last 2 weeks
Trend: Increasing (15 → 27 mentions)
Category: Infrastructure
Action: Escalate to IT support team
```

### 6.3 Unresolved Feedback Loop Detection

**Logic**:
- Track similar feedback patterns across multiple weeks
- Identify recurring issues that haven't improved
- Flag if sentiment remains negative for 3+ consecutive weeks

**Output**:
```
Unresolved Issue: Infrastructure complaints persist for 4 weeks
Sentiment: Consistently negative (avg: 65% negative)
Recommendation: Immediate escalation required
```

### 6.4 Assessment Stress Detection

**Pattern Recognition**:
- Keywords: "pressure", "difficult", "revision", "exam", "assessment", "stress"
- Timing correlation (before scheduled assessments)
- Sentiment dip pattern

**Output**:
```
Pattern Detected: Assessment stress cycle
Evidence: High frequency of stress-related keywords (42 mentions)
Sentiment Impact: 9% drop in overall sentiment
Recommendation: Pre-assessment support workshop
Confidence: 82%
```

### 6.5 Praise Momentum Tracking

**Purpose**: Identify positive trends for recognition programs

**Metrics**:
- Increase in positive feedback for specific trainers/mentors
- Appreciation keyword frequency
- Rating score improvements

**Output**:
```
Praise Momentum: Trainer "John Doe" received 15 positive mentions this week
Trend: +25% increase from last week
Recommendation: Recognition email/certificate
```

---

## 7. Data Model Design

### 7.1 Core Entities

**Users**:
- id, email, name, role, created_at, updated_at

**Feedback Records**:
- id, trainee_id (masked), location, batch, week_start_date, week_end_date, rating, open_text, created_at

**Sentiment Analysis Results**:
- id, feedback_id, sentiment_category, emotional_tone, confidence_score, category_mappings, created_at

**Weekly Reports**:
- id, week_start_date, week_end_date, overall_sentiment_score, heat_index, report_data (JSON), pdf_path, created_at

**Category Mappings**:
- id, feedback_id, category_name, relevance_score, created_at

**Trend Data**:
- id, week_start_date, category, sentiment_distribution, volume, created_at

**Action Items**:
- id, report_id, priority, category, description, assigned_to, status, created_at

**Audit Logs**:
- id, user_id, action, resource, timestamp, ip_address

---

## 8. API Endpoints Specification

### 8.1 Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/refresh` - Refresh token

### 8.2 Data Upload
- `POST /api/feedback/upload` - Upload CSV/Excel file
- `GET /api/feedback/upload/status/{job_id}` - Check upload processing status

### 8.3 Sentiment Analysis
- `POST /api/analysis/process` - Trigger sentiment analysis for uploaded data
- `GET /api/analysis/results/{week_id}` - Get analysis results for a week

### 8.4 Reports & Dashboards
- `GET /api/reports/weekly/{week_id}` - Get weekly report data
- `GET /api/reports/executive/{week_id}` - Get executive summary
- `GET /api/reports/trends` - Get trend data (date range)
- `GET /api/reports/lifecycle` - Get trainee lifecycle sentiment data
- `GET /api/reports/export/pdf/{week_id}` - Download PDF report

### 8.5 Category Analysis
- `GET /api/categories/sentiment/{week_id}` - Category-wise sentiment breakdown
- `GET /api/categories/trends` - Category trend analysis

### 8.6 Insights
- `GET /api/insights/actions/{week_id}` - Get action recommendations
- `GET /api/insights/risks/{week_id}` - Get risk flags
- `GET /api/insights/appreciation/{week_id}` - Get appreciation highlights

### 8.7 User Management (Admin only)
- `GET /api/users` - List users
- `POST /api/users` - Create user
- `PUT /api/users/{user_id}` - Update user
- `DELETE /api/users/{user_id}` - Delete user

---

## 9. Implementation Phases

### Phase 1: Core Infrastructure (Week 1-2)
- Project setup and architecture
- Database schema design and setup
- Authentication and authorization
- Basic file upload functionality

### Phase 2: Sentiment Analysis Engine (Week 3-4)
- NLP model integration
- Sentiment classification implementation
- Category mapping system
- Basic trend analysis

### Phase 3: Dashboard & Reporting (Week 5-6)
- Frontend dashboard development
- Chart and visualization components
- Report generation (PDF)
- Executive summary automation

### Phase 4: Intelligence Layer (Week 7-8)
- Pattern recognition algorithms
- Insight generation engine
- Risk flagging system
- Heat index calculation

### Phase 5: Advanced Features (Week 9-10)
- Trainee lifecycle tracking
- Advanced trend analysis
- Multi-role access control
- Performance optimization

### Phase 6: Testing & Deployment (Week 11-12)
- Unit and integration testing
- User acceptance testing
- Deployment and documentation
- Training materials

---

## 10. Success Metrics

**Technical Metrics**:
- Sentiment classification accuracy >85%
- API response time <2 seconds
- Dashboard load time <3 seconds
- System uptime >99%

**Business Metrics**:
- Reduction in manual review time by 80%
- Action item implementation rate
- User adoption rate
- Report generation time <5 minutes

---

## 11. Risk Considerations

**Technical Risks**:
- Model accuracy for domain-specific language
- Scalability with large feedback volumes
- Data privacy and security compliance

**Mitigation**:
- Fine-tune models on training data
- Implement caching and async processing
- Follow data anonymization best practices
- Regular security audits

---

## 12. Next Steps

1. **Review & Approval**: Stakeholder review of this analysis
2. **Technology Stack Finalization**: Confirm tech choices
3. **Development Environment Setup**: Initialize project structure
4. **Sprint Planning**: Break down into development sprints
5. **Begin Implementation**: Start with Phase 1

---

**Document Version**: 1.0  
**Last Updated**: [Current Date]  
**Prepared By**: AI Assistant  
**Status**: Ready for Review




