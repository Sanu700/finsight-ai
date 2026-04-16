import os
import json
import httpx
from models.schema import AnalysisResult, FinancialInsights

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-1.5-flash:generateContent"
)


def _build_prompt(analysis: AnalysisResult, currency: str, user_name: str) -> str:
    category_lines = "\n".join(
        f"  - {cb.category}: {currency} {cb.total} ({cb.percentage}%, {cb.count} txns)"
        for cb in analysis.category_breakdown
    )
    anomaly_lines = "\n".join(
        f"  - [{a.category}] {a.description}: {currency} {a.amount} "
        f"(+{a.deviation_percent:.1f}% above category avg)"
        for a in analysis.anomalies
    ) or "  None detected"

    return f"""
You are FinSight AI, an expert financial risk analyst and advisor.
Analyze the following financial data for {user_name} and provide structured insights.

=== FINANCIAL SUMMARY ===
Period: {analysis.date_range['from']} to {analysis.date_range['to']}
Total Spend: {currency} {analysis.total_spend}
Transactions: {analysis.transaction_count}
Average per Transaction: {currency} {analysis.average_transaction}
Highest Spending Category: {analysis.highest_category}

=== CATEGORY BREAKDOWN ===
{category_lines}

=== ANOMALIES DETECTED ===
{anomaly_lines}

=== YOUR TASK ===
Respond ONLY with a valid JSON object (no markdown, no explanation) with this exact structure:
{{
  "summary": "<2-3 sentence overview of the financial picture>",
  "risk_level": "<one of: LOW, MEDIUM, HIGH>",
  "risk_explanation": "<1-2 sentences explaining the risk level based on anomalies and spending patterns>",
  "suggestions": [
    "<actionable suggestion 1>",
    "<actionable suggestion 2>",
    "<actionable suggestion 3>",
    "<actionable suggestion 4>"
  ],
  "spending_pattern": "<one of: Conservative, Moderate, Aggressive, Impulsive, Balanced>"
}}

Be specific, data-driven, and avoid generic advice. Reference actual numbers and categories.
""".strip()


async def generate_insights(
    analysis: AnalysisResult,
    currency: str = "USD",
    user_name: str = "User",
) -> FinancialInsights:
    if not GEMINI_API_KEY:
        return _fallback_insights(analysis)

    prompt = _build_prompt(analysis, currency, user_name)

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 1024,
        },
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{GEMINI_URL}?key={GEMINI_API_KEY}",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            data = response.json()

        raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
        # Strip potential markdown code fences
        clean = raw_text.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        parsed = json.loads(clean)

        return FinancialInsights(
            summary=parsed.get("summary", "Analysis complete."),
            risk_level=parsed.get("risk_level", "MEDIUM"),
            risk_explanation=parsed.get("risk_explanation", ""),
            suggestions=parsed.get("suggestions", []),
            spending_pattern=parsed.get("spending_pattern", "Moderate"),
        )

    except Exception as e:
        print(f"[LLM ERROR] {e}")
        return _fallback_insights(analysis)


def _fallback_insights(analysis: AnalysisResult) -> FinancialInsights:
    """Rule-based fallback when Gemini API is unavailable."""
    anomaly_count = len(analysis.anomalies)
    risk = "LOW" if anomaly_count == 0 else ("MEDIUM" if anomaly_count <= 2 else "HIGH")

    suggestions = [
        f"Your highest spend is in {analysis.highest_category} — review for optimization.",
        "Set a monthly budget per category to stay on track.",
        "Track daily transactions to catch anomalies early.",
        "Consider automating savings with a fixed monthly transfer.",
    ]

    return FinancialInsights(
        summary=(
            f"You spent {analysis.total_spend} across {analysis.transaction_count} transactions "
            f"between {analysis.date_range['from']} and {analysis.date_range['to']}. "
            f"Your top category is {analysis.highest_category}."
        ),
        risk_level=risk,
        risk_explanation=(
            f"{anomaly_count} anomalous transaction(s) detected above 2x category average."
            if anomaly_count
            else "No significant spending anomalies detected in this period."
        ),
        suggestions=suggestions,
        spending_pattern="Moderate",
    )
