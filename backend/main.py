import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from models.schema import AnalysisRequest, AnalysisResponse
from services.analyzer import analyze_transactions
from services.llm import generate_insights

app = FastAPI(
    title="FinSight AI — Financial Insights & Risk Assistant",
    description="AI-powered financial transaction analysis with anomaly detection and LLM insights.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "service": "FinSight AI", "version": "1.0.0"}


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy"}


@app.post("/analyze", response_model=AnalysisResponse, tags=["Analysis"])
async def analyze(request: AnalysisRequest):
    if not request.transactions:
        raise HTTPException(status_code=400, detail="No transactions provided.")
    if len(request.transactions) > 500:
        raise HTTPException(status_code=400, detail="Max 500 transactions per request.")

    # Assign IDs if missing
    for i, txn in enumerate(request.transactions):
        if not txn.id:
            txn.id = f"txn_{i+1}_{uuid.uuid4().hex[:6]}"

    try:
        analysis = analyze_transactions(request.transactions)
        insights = await generate_insights(
            analysis,
            currency=request.currency or "USD",
            user_name=request.user_name or "User",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

    return AnalysisResponse(
        status="success",
        analysis=analysis,
        insights=insights,
    )


@app.get("/sample-data", tags=["Utilities"])
async def get_sample_data():
    """Returns sample transaction data for testing."""
    return {
        "user_name": "Alex Morgan",
        "currency": "USD",
        "transactions": [
            {"description": "Grocery Store", "amount": 85.50, "category": "Food & Dining", "date": "2024-01-02"},
            {"description": "Netflix Subscription", "amount": 15.99, "category": "Entertainment", "date": "2024-01-03"},
            {"description": "Uber Ride", "amount": 22.00, "category": "Transport", "date": "2024-01-04"},
            {"description": "Restaurant Dinner", "amount": 320.75, "category": "Food & Dining", "date": "2024-01-05"},
            {"description": "Electricity Bill", "amount": 110.00, "category": "Utilities", "date": "2024-01-06"},
            {"description": "Amazon Shopping", "amount": 450.00, "category": "Shopping", "date": "2024-01-07"},
            {"description": "Coffee Shop", "amount": 12.40, "category": "Food & Dining", "date": "2024-01-08"},
            {"description": "Gym Membership", "amount": 45.00, "category": "Health & Wellness", "date": "2024-01-09"},
            {"description": "Flight Tickets", "amount": 890.00, "category": "Travel", "date": "2024-01-10"},
            {"description": "Online Course", "amount": 199.00, "category": "Education", "date": "2024-01-11"},
            {"description": "Supermarket", "amount": 95.20, "category": "Food & Dining", "date": "2024-01-12"},
            {"description": "Taxi", "amount": 18.00, "category": "Transport", "date": "2024-01-13"},
            {"description": "Luxury Watch", "amount": 1250.00, "category": "Shopping", "date": "2024-01-14"},
            {"description": "Internet Bill", "amount": 60.00, "category": "Utilities", "date": "2024-01-15"},
            {"description": "Movie Tickets", "amount": 35.00, "category": "Entertainment", "date": "2024-01-16"},
            {"description": "Doctor Visit", "amount": 150.00, "category": "Health & Wellness", "date": "2024-01-17"},
            {"description": "Food Delivery", "amount": 48.60, "category": "Food & Dining", "date": "2024-01-18"},
            {"description": "Bus Pass", "amount": 80.00, "category": "Transport", "date": "2024-01-19"},
            {"description": "Clothing Store", "amount": 220.00, "category": "Shopping", "date": "2024-01-20"},
            {"description": "Spotify", "amount": 9.99, "category": "Entertainment", "date": "2024-01-21"},
        ]
    }
