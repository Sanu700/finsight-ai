from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class Category(str, Enum):
    food = "Food & Dining"
    transport = "Transport"
    shopping = "Shopping"
    utilities = "Utilities"
    entertainment = "Entertainment"
    health = "Health & Wellness"
    travel = "Travel"
    education = "Education"
    other = "Other"


class Transaction(BaseModel):
    id: Optional[str] = None
    description: str
    amount: float = Field(..., gt=0, description="Transaction amount in USD")
    category: Category
    date: str  # ISO format: YYYY-MM-DD


class AnalysisRequest(BaseModel):
    transactions: List[Transaction]
    user_name: Optional[str] = "User"
    currency: Optional[str] = "USD"


class Anomaly(BaseModel):
    transaction_id: Optional[str]
    description: str
    amount: float
    category: str
    threshold: float
    deviation_percent: float


class CategoryBreakdown(BaseModel):
    category: str
    total: float
    count: int
    percentage: float
    avg_per_transaction: float


class AnalysisResult(BaseModel):
    total_spend: float
    transaction_count: int
    average_transaction: float
    category_breakdown: List[CategoryBreakdown]
    anomalies: List[Anomaly]
    highest_category: str
    date_range: dict


class FinancialInsights(BaseModel):
    summary: str
    risk_level: str  # LOW / MEDIUM / HIGH
    risk_explanation: str
    suggestions: List[str]
    spending_pattern: str


class AnalysisResponse(BaseModel):
    status: str
    analysis: AnalysisResult
    insights: FinancialInsights
