from collections import defaultdict
from typing import List, Tuple
from models.schema import (
    Transaction, AnalysisResult, CategoryBreakdown, Anomaly
)


ANOMALY_MULTIPLIER = 2.0  # flag if > 2x the category average


def compute_date_range(transactions: List[Transaction]) -> dict:
    dates = sorted([t.date for t in transactions])
    return {"from": dates[0], "to": dates[-1]} if dates else {"from": "N/A", "to": "N/A"}


def compute_category_breakdown(
    transactions: List[Transaction], total_spend: float
) -> List[CategoryBreakdown]:
    cat_totals: dict = defaultdict(float)
    cat_counts: dict = defaultdict(int)

    for t in transactions:
        cat_totals[t.category.value] += t.amount
        cat_counts[t.category.value] += 1

    breakdown = []
    for cat, total in sorted(cat_totals.items(), key=lambda x: x[1], reverse=True):
        count = cat_counts[cat]
        breakdown.append(CategoryBreakdown(
            category=cat,
            total=round(total, 2),
            count=count,
            percentage=round((total / total_spend) * 100, 2) if total_spend else 0,
            avg_per_transaction=round(total / count, 2) if count else 0,
        ))

    return breakdown


def detect_anomalies(transactions: List[Transaction]) -> List[Anomaly]:
    # Group by category, compute per-category average
    cat_amounts: dict = defaultdict(list)
    cat_txns: dict = defaultdict(list)

    for t in transactions:
        cat_amounts[t.category.value].append(t.amount)
        cat_txns[t.category.value].append(t)

    anomalies = []
    for cat, amounts in cat_amounts.items():
        if len(amounts) < 2:
            # Not enough data for statistical threshold; use global avg
            avg = sum(amounts) / len(amounts)
        else:
            avg = sum(amounts) / len(amounts)

        threshold = avg * ANOMALY_MULTIPLIER

        for t in cat_txns[cat]:
            if t.amount > threshold:
                deviation = ((t.amount - avg) / avg) * 100
                anomalies.append(Anomaly(
                    transaction_id=t.id,
                    description=t.description,
                    amount=round(t.amount, 2),
                    category=cat,
                    threshold=round(threshold, 2),
                    deviation_percent=round(deviation, 2),
                ))

    return sorted(anomalies, key=lambda a: a.deviation_percent, reverse=True)


def analyze_transactions(transactions: List[Transaction]) -> AnalysisResult:
    total_spend = round(sum(t.amount for t in transactions), 2)
    count = len(transactions)
    avg_txn = round(total_spend / count, 2) if count else 0

    category_breakdown = compute_category_breakdown(transactions, total_spend)
    anomalies = detect_anomalies(transactions)
    date_range = compute_date_range(transactions)

    highest_category = category_breakdown[0].category if category_breakdown else "N/A"

    return AnalysisResult(
        total_spend=total_spend,
        transaction_count=count,
        average_transaction=avg_txn,
        category_breakdown=category_breakdown,
        anomalies=anomalies,
        highest_category=highest_category,
        date_range=date_range,
    )
