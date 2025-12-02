# 🔄 Complete Feedback Processing Pipeline

## 📊 **Overview: How Feedback Filtering & Analysis Works**

This document explains the **complete journey** of feedback from CSV upload to insights generation.

---

## 🎯 **Step-by-Step Process**

### **STEP 1: File Upload** 📤
**Location**: `frontend/src/pages/Upload.tsx` → `backend/app/api/v1/endpoints/feedback.py`

```
User uploads CSV → Frontend sends to /api/v1/feedback/upload
```

**What happens:**
- User selects CSV/Excel file
- File sent to backend via HTTP POST
- Backend validates user permissions (Admin/System Owner only)

---

### **STEP 2: File Processing** 📋
**Location**: `backend/app/services/file_processor.py`

**Library Used**: `pandas` (Python Data Analysis Library)

**Why pandas?**
- ✅ Reads CSV/Excel files easily
- ✅ Handles missing data gracefully
- ✅ Validates column structure
- ✅ Cleans and normalizes data

**Process:**

```python
# 1. Read file
df = pd.read_csv(file_path)  # or pd.read_excel()

# 2. Validate required columns
REQUIRED_COLUMNS = [
    "trainee_id",
    "location", 
    "training_batch",
    "rating_score",
    "open_text"  # The feedback text
]

# 3. Clean data
df.columns = df.columns.str.strip().str.lower()  # Normalize column names
record["open_text"] = str(row.get("open_text", "")).strip()  # Clean text

# 4. Parse dates
record["week_start_date"] = pd.to_datetime(week_start)

# 5. Validate each row
if not record["trainee_id"] or not record["open_text"]:
    errors.append("Missing required data")
```

**Output**: Clean, structured data ready for analysis

---

### **STEP 3: Sentiment Analysis** 🧠
**Location**: `backend/app/ml/sentiment_analyzer.py`

**Libraries Used:**
1. **`transformers`** (Hugging Face) - Pre-trained AI models
2. **`torch`** (PyTorch) - Deep learning framework

**Model Used**: `distilbert-base-uncased-finetuned-sst-2-english`

**Why this model?**
- ✅ **Pre-trained** on 67M+ movie reviews (Stanford Sentiment Treebank)
- ✅ **Accurate**: 91% accuracy on sentiment classification
- ✅ **Fast**: Distilled version (40% smaller, 60% faster than BERT)
- ✅ **Production-ready**: Used by thousands of companies

**How it works:**

```python
# 1. Load pre-trained model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# 2. Convert text to numbers (tokenization)
inputs = tokenizer(
    "Trainer is excellent and helpful",  # Input text
    return_tensors="pt",  # Return PyTorch tensors
    truncation=True,      # Limit to 512 tokens
    max_length=512
)

# Result: [101, 7324, 2003, 6581, 1998, 8346, 102]
# Each number represents a word/subword

# 3. Run through neural network
outputs = model(**inputs)
logits = outputs.logits  # Raw scores

# 4. Convert to probabilities
probabilities = torch.softmax(logits, dim=-1)
# Result: [0.02, 0.03, 0.95]  (negative, neutral, positive)

# 5. Get prediction
predicted_class = torch.argmax(probabilities)  # 2 (positive)
confidence = probabilities[0][predicted_class]  # 0.95 (95%)
```

**Output:**
```json
{
    "sentiment": "positive",
    "confidence": 0.95,
    "scores": {
        "negative": 0.02,
        "neutral": 0.03,
        "positive": 0.95
    }
}
```

**Emotional Tone Detection:**
Uses **keyword matching** to detect specific emotions:

```python
tone_keywords = {
    "confusion": ["confused", "unclear", "don't understand"],
    "stress": ["stress", "pressure", "overwhelmed"],
    "motivation": ["motivated", "excited", "enthusiastic"],
    "satisfaction": ["satisfied", "happy", "pleased"],
    "frustration": ["frustrated", "annoyed", "disappointed"],
    "appreciation": ["thank", "appreciate", "grateful"]
}

# Count keyword matches
for tone, keywords in tone_keywords.items():
    score = sum(1 for keyword in keywords if keyword in text.lower())

# Return highest scoring tone
```

---

### **STEP 4: Category Mapping** 🏷️
**Location**: `backend/app/ml/category_mapper.py`

**Library Used**: `re` (Regular Expressions) - Python built-in

**Why regex?**
- ✅ Fast keyword matching
- ✅ Word boundary detection (`\b`)
- ✅ Case-insensitive search
- ✅ No external dependencies

**Categories:**
1. **TRAINER** - Teaching quality, explanations
2. **MENTOR** - Support, guidance, availability
3. **BATCH_OWNER** - Coordination, management
4. **INFRASTRUCTURE** - Technical issues, systems
5. **TRAINING_PROGRAM** - Curriculum, content, pace
6. **ENGAGEMENT** - Environment, culture, interaction

**How it works:**

```python
# 1. Define keywords for each category
category_keywords = {
    "INFRASTRUCTURE": [
        "software", "hardware", "laptop", "computer", 
        "internet", "network", "wifi", "system"
    ],
    "TRAINER": [
        "trainer", "instructor", "teaching", "explanation",
        "clarity", "delivery", "session"
    ]
}

# 2. Search for keywords using regex
text = "Network is unstable and laptop keeps freezing"
for category, keywords in category_keywords.items():
    for keyword in keywords:
        # Word boundary ensures exact match
        pattern = r'\b' + keyword + r'\b'
        matches = re.findall(pattern, text.lower())
        
        if matches:
            # Score based on keyword length (longer = more specific)
            score += len(keyword) * 0.01

# 3. Calculate relevance score
# "network" found (7 chars) → score += 0.07
# "laptop" found (6 chars) → score += 0.06
# Total: 0.13 → INFRASTRUCTURE category

# 4. Filter by threshold (>= 0.2 to be included)
if relevance_score >= 0.2:
    results.append({
        "category": "INFRASTRUCTURE",
        "relevance_score": 0.13,
        "keywords_matched": ["network", "laptop"]
    })
```

**Tag Priority:**
If CSV has `category_tags` column, those get **higher weight**:

```python
if provided_tags:  # e.g., "infrastructure,trainer_feedback"
    for tag in tag_list:
        category_scores[category]["score"] += 0.3  # Boost by 30%
```

**Output:**
```json
[
    {
        "category": "INFRASTRUCTURE",
        "relevance_score": 0.85,
        "keywords_matched": ["network", "laptop", "system"]
    },
    {
        "category": "TRAINER",
        "relevance_score": 0.45,
        "keywords_matched": ["session"]
    }
]
```

---

### **STEP 5: Database Storage** 💾
**Location**: `backend/app/api/v1/endpoints/feedback.py` (lines 78-122)

**Library Used**: `SQLAlchemy` (ORM - Object Relational Mapper)

**Why SQLAlchemy?**
- ✅ Python objects → Database tables
- ✅ Automatic SQL generation
- ✅ Database-agnostic (SQLite/PostgreSQL)
- ✅ Relationship management

**Process:**

```python
# 1. Create Feedback record
feedback = Feedback(
    trainee_id="T001",
    location="Bangalore",
    training_batch="L1-2024-B01",
    week_start_date=datetime(2024, 11, 18),
    rating_score=4,
    open_text="Trainer is excellent!"
)
db.add(feedback)
db.flush()  # Get feedback.id

# 2. Save Sentiment Analysis
sentiment_analysis = SentimentAnalysis(
    feedback_id=feedback.id,  # Link to feedback
    sentiment_category="positive",
    emotional_tone="satisfaction",
    confidence_score=0.95,
    raw_sentiment_scores={"positive": 0.95, "neutral": 0.03, "negative": 0.02}
)
db.add(sentiment_analysis)

# 3. Save Category Mappings (multiple)
for mapping in category_mappings:
    category_mapping = CategoryMapping(
        feedback_id=feedback.id,  # Link to feedback
        category="TRAINER",
        relevance_score=0.85,
        keywords_matched=["trainer", "excellent"]
    )
    db.add(category_mapping)

# 4. Commit all changes
db.commit()
```

**Database Structure:**
```
feedback (main table)
├── id: 1
├── trainee_id: "T001"
├── open_text: "Trainer is excellent!"
└── week_start_date: 2024-11-18

sentiment_analysis (1-to-1)
├── feedback_id: 1 (foreign key)
├── sentiment_category: "positive"
└── confidence_score: 0.95

category_mapping (1-to-many)
├── feedback_id: 1 (foreign key)
├── category: "TRAINER"
└── relevance_score: 0.85
```

---

### **STEP 6: Filtering & Retrieval** 🔍
**Location**: `backend/app/api/v1/endpoints/feedback.py` (lines 140-178)

**Library Used**: `SQLAlchemy` Query API

**How filtering works:**

```python
# Start with base query
query = db.query(Feedback)

# 1. Role-based filtering
if current_user.role == "BATCH_OWNER":
    allowed_batches = ["L1-2024-B01", "L1-2024-B02"]
    query = query.filter(Feedback.training_batch.in_(allowed_batches))

# 2. Date filtering
if week_start:  # e.g., 2024-11-18
    week_end = week_start + timedelta(days=6)  # 2024-11-24
    query = query.filter(
        Feedback.week_start_date >= week_start,
        Feedback.week_start_date <= week_end
    )

# 3. Batch filtering
if batch:  # e.g., "L1-2024-B01"
    query = query.filter(Feedback.training_batch == batch)

# 4. Location filtering
if location:  # e.g., "Bangalore"
    query = query.filter(Feedback.location == location)

# 5. Execute query
feedback_list = query.offset(0).limit(100).all()
```

**Generated SQL:**
```sql
SELECT * FROM feedback 
WHERE training_batch IN ('L1-2024-B01', 'L1-2024-B02')
  AND week_start_date >= '2024-11-18'
  AND week_start_date <= '2024-11-24'
  AND location = 'Bangalore'
LIMIT 100;
```

---

### **STEP 7: Analysis & Insights** 📈
**Location**: `backend/app/api/v1/endpoints/analysis.py`

**Process:**

```python
# 1. Get filtered feedback
feedback_list = db.query(Feedback).filter(...).all()

# 2. Calculate sentiment distribution
positive_count = sum(1 for f in feedback_list 
                     if f.sentiment_analysis.sentiment_category == "positive")
positive_percentage = (positive_count / total) * 100

# 3. Calculate category trends
category_counts = {}
for feedback in feedback_list:
    for mapping in feedback.category_mappings:
        category_counts[mapping.category] = category_counts.get(mapping.category, 0) + 1

# 4. Generate insights
if positive_percentage < 50:
    risk_flags.append("Low satisfaction detected")

if "INFRASTRUCTURE" in top_categories:
    action_items.append("Review technical infrastructure")
```

---

## 🎨 **Visual Flow Diagram**

```
CSV Upload
    ↓
[pandas] Parse & Validate
    ↓
For each row:
    ↓
    ├─→ [transformers + PyTorch] Sentiment Analysis
    │       ↓
    │   "positive" (95% confidence)
    │
    ├─→ [regex] Category Mapping  
    │       ↓
    │   ["TRAINER", "MENTOR"]
    │
    └─→ [SQLAlchemy] Save to Database
            ↓
        feedback table
        sentiment_analysis table
        category_mapping table
            ↓
[SQLAlchemy] Query with Filters
    ↓
    ├─→ Week filter
    ├─→ Batch filter
    ├─→ Location filter
    └─→ Role-based filter
            ↓
Aggregated Results
    ↓
    ├─→ Sentiment Distribution
    ├─→ Category Trends
    ├─→ Action Items
    └─→ Risk Flags
            ↓
Dashboard Display
```

---

## 📚 **Libraries Summary**

| Library | Purpose | Why Used |
|---------|---------|----------|
| **pandas** | Data processing | CSV parsing, validation, cleaning |
| **transformers** | NLP models | Pre-trained sentiment analysis |
| **torch** | Deep learning | Neural network inference |
| **SQLAlchemy** | Database ORM | Data storage & querying |
| **re** | Pattern matching | Keyword extraction |
| **FastAPI** | Web framework | API endpoints |
| **pydantic** | Data validation | Request/response schemas |

---

## 🔑 **Key Concepts**

### **1. Tokenization**
Converting text to numbers that AI can understand:
```
"Trainer is great" → [101, 7324, 2003, 2307, 102]
```

### **2. Transformer Model**
Neural network architecture that understands context:
```
Input: "The trainer is not bad"
Model understands: "not bad" = positive (double negative)
Output: positive (75% confidence)
```

### **3. Softmax**
Converts raw scores to probabilities (0-1, sum=1):
```
Raw scores: [-2.5, 0.1, 3.8]
Softmax: [0.02, 0.03, 0.95]  (negative, neutral, positive)
```

### **4. Word Boundaries**
Ensures exact word matches:
```
Pattern: \bnet\b
"network" → NO match (net is part of network)
"the net is slow" → YES match (net is standalone word)
```

### **5. ORM (Object-Relational Mapping)**
Python objects ↔ Database tables:
```python
feedback = Feedback(trainee_id="T001")  # Python object
db.add(feedback)  # Converts to SQL INSERT
```

---

## 🎯 **Why This Architecture?**

### **Accuracy** 🎯
- Transformer model: 91% accurate
- Pre-trained on 67M+ examples
- Understands context & negation

### **Speed** ⚡
- Batch processing with pandas
- GPU acceleration (if available)
- Efficient database queries

### **Scalability** 📈
- Handles 1000s of feedback entries
- Parallel processing possible
- Database indexing for fast queries

### **Maintainability** 🔧
- Modular design (separate files)
- Clear separation of concerns
- Easy to update models/keywords

### **Flexibility** 🔄
- Multiple filter options
- Role-based access control
- Customizable categories

---

## 🚀 **Real Example**

**Input CSV:**
```csv
trainee_id,location,training_batch,rating_score,open_text
T001,Bangalore,L1-2024-B01,2,"Network is terrible and laptop freezes"
```

**Step 1: Parse** (pandas)
```python
{
    "trainee_id": "T001",
    "location": "Bangalore",
    "open_text": "Network is terrible and laptop freezes"
}
```

**Step 2: Sentiment** (transformers)
```python
{
    "sentiment": "negative",
    "confidence": 0.92,
    "emotional_tone": "frustration"
}
```

**Step 3: Categories** (regex)
```python
[
    {
        "category": "INFRASTRUCTURE",
        "relevance_score": 0.85,
        "keywords": ["network", "laptop"]
    }
]
```

**Step 4: Store** (SQLAlchemy)
```
feedback.id = 1
sentiment_analysis.sentiment_category = "negative"
category_mapping.category = "INFRASTRUCTURE"
```

**Step 5: Analyze**
```
Week: 2024-11-18
Negative: 100%
Top Issue: INFRASTRUCTURE
Action: "Review technical infrastructure urgently"
```

---

## 💡 **Summary**

The system uses **3 main AI/ML techniques**:

1. **Deep Learning** (Transformers) - For accurate sentiment analysis
2. **Keyword Matching** (Regex) - For category classification
3. **Statistical Analysis** (Pandas) - For trend detection

All orchestrated through **FastAPI** and stored in **SQLAlchemy** for efficient retrieval! 🎉


