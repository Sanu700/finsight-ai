# 📊 FinSight AI — Financial Insights & Risk Assistant

> AI-powered financial transaction analysis with anomaly detection, category breakdown, and LLM-generated insights powered by Google Gemini.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red)
![Gemini](https://img.shields.io/badge/Gemini-1.5_Flash-orange)

---

## ✨ Features

- **Transaction Ingestion** — Input via interactive form or raw JSON paste
- **Spend Analytics** — Total spend, per-category breakdown, averages, date range
- **Anomaly Detection** — Statistical threshold (2× category average) flags unusual transactions
- **AI Insights** — Gemini LLM generates financial summaries, risk assessments, and personalized suggestions
- **Risk Scoring** — LOW / MEDIUM / HIGH risk classification with explanation
- **Spending Pattern** — Labels your behavior (Conservative, Balanced, Aggressive, etc.)
- **Interactive Charts** — Donut chart, bar chart, and progress bars via Plotly
- **Graceful Fallback** — Rule-based insights if Gemini API is unavailable

---

## 🗂️ Project Structure

```
finsight-ai/
├── backend/
│   ├── main.py                  # FastAPI app, routes
│   ├── models/
│   │   └── schema.py            # Pydantic request/response models
│   └── services/
│       ├── analyzer.py          # Transaction analysis + anomaly detection
│       └── llm.py               # Gemini API integration
├── frontend/
│   └── app.py                   # Streamlit UI
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

| Layer     | Technology            |
|-----------|----------------------|
| Backend   | FastAPI + Uvicorn    |
| Frontend  | Streamlit + Plotly   |
| LLM       | Google Gemini 1.5 Flash |
| HTTP      | HTTPX (async)        |
| Validation| Pydantic v2          |
| Data      | In-memory (no DB)    |

---

## ⚡ Quick Setup (< 15 minutes)

### 1. Clone / Download

```bash
git clone https://github.com/yourname/finsight-ai.git
cd finsight-ai
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Your Gemini API Key

Get a free key at: https://aistudio.google.com/app/apikey

**Option A — Environment Variable (recommended):**
```bash
# Mac/Linux
export GEMINI_API_KEY="your_api_key_here"

# Windows CMD
set GEMINI_API_KEY=your_api_key_here

# Windows PowerShell
$env:GEMINI_API_KEY="your_api_key_here"
```

**Option B — `.env` file:**
```bash
# Create .env in the backend/ directory
echo GEMINI_API_KEY=your_api_key_here > backend/.env
```
Then add this to the top of `backend/main.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

> ⚠️ Without a Gemini key, the app still works — it falls back to rule-based insights automatically.

---

## 🚀 Running the Application

### Start the Backend (FastAPI)

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Backend runs at: http://localhost:8000  
Swagger docs: http://localhost:8000/docs

### Start the Frontend (Streamlit)

Open a **new terminal**:

```bash
cd frontend
streamlit run app.py
```

Frontend runs at: http://localhost:8501

---

## 🔌 API Reference

### `POST /analyze`

Analyzes a list of financial transactions.

**Request Body:**
```json
{
  "user_name": "Alex Morgan",
  "currency": "USD",
  "transactions": [
    {
      "description": "Grocery Store",
      "amount": 85.50,
      "category": "Food & Dining",
      "date": "2024-01-02"
    }
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "analysis": {
    "total_spend": 85.50,
    "transaction_count": 1,
    "average_transaction": 85.50,
    "category_breakdown": [...],
    "anomalies": [...],
    "highest_category": "Food & Dining",
    "date_range": {"from": "2024-01-02", "to": "2024-01-02"}
  },
  "insights": {
    "summary": "...",
    "risk_level": "LOW",
    "risk_explanation": "...",
    "suggestions": [...],
    "spending_pattern": "Conservative"
  }
}
```

### `GET /sample-data`

Returns 20 pre-built sample transactions for testing.

### `GET /health`

Health check endpoint.

---

## 🧠 How Anomaly Detection Works

For each spending category:
1. Compute the **average transaction amount**
2. Set threshold = **average × 2.0**
3. Any transaction exceeding this threshold is flagged as an anomaly
4. Deviation percentage shows how far above the threshold it is

Example: If average Food & Dining spend is `$80`, any transaction above `$160` is flagged.

---

## 📦 Valid Categories

`Food & Dining`, `Transport`, `Shopping`, `Utilities`, `Entertainment`, `Health & Wellness`, `Travel`, `Education`, `Other`

---

## 🤝 Contributing

Pull requests welcome. For major changes, open an issue first.

---

## 📄 License

MIT — free for personal and commercial use.
