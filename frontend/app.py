import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FinSight AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

BACKEND_URL = "https://finsight-ai-9vef.onrender.com"

CATEGORIES = [
    "Food & Dining", "Transport", "Shopping", "Utilities",
    "Entertainment", "Health & Wellness", "Travel", "Education", "Other"
]

RISK_COLORS = {"LOW": "#22c55e", "MEDIUM": "#f59e0b", "HIGH": "#ef4444"}
RISK_BG = {"LOW": "#052e16", "MEDIUM": "#451a03", "HIGH": "#450a0a"}

# ── Custom CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* Dark theme base */
.stApp {
    background-color: #0a0a0f;
    color: #e2e8f0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0f0f1a !important;
    border-right: 1px solid #1e1e2e;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #13131f 0%, #1a1a2e 100%);
    border: 1px solid #2d2d4e;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15);
}
.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #a5b4fc;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1.2;
}
.metric-label {
    font-size: 0.8rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 6px;
    font-weight: 500;
}
.metric-sub {
    font-size: 0.75rem;
    color: #4b5563;
    margin-top: 4px;
    font-family: 'JetBrains Mono', monospace;
}

/* Section headers */
.section-header {
    font-size: 1.1rem;
    font-weight: 600;
    color: #c7d2fe;
    border-bottom: 1px solid #2d2d4e;
    padding-bottom: 10px;
    margin-bottom: 20px;
    letter-spacing: 0.02em;
}

/* Anomaly cards */
.anomaly-card {
    background: linear-gradient(135deg, #1a0a0a 0%, #2d0f0f 100%);
    border: 1px solid #7f1d1d;
    border-left: 4px solid #ef4444;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.anomaly-title {
    font-weight: 600;
    color: #fca5a5;
    font-size: 0.95rem;
}
.anomaly-meta {
    font-size: 0.78rem;
    color: #6b7280;
    margin-top: 4px;
    font-family: 'JetBrains Mono', monospace;
}
.anomaly-badge {
    background: #7f1d1d;
    color: #fca5a5;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
}

/* Insight box */
.insight-box {
    background: linear-gradient(135deg, #0d1117 0%, #161b27 100%);
    border: 1px solid #2d3748;
    border-radius: 16px;
    padding: 24px;
    line-height: 1.7;
    color: #d1d5db;
    font-size: 0.95rem;
}

/* Risk badge */
.risk-badge {
    display: inline-block;
    padding: 6px 20px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.1em;
    font-family: 'JetBrains Mono', monospace;
}

/* Suggestion items */
.suggestion-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 16px;
    background: #0f1117;
    border: 1px solid #1e2535;
    border-radius: 10px;
    margin-bottom: 8px;
    font-size: 0.9rem;
    color: #cbd5e1;
}
.suggestion-num {
    background: #312e81;
    color: #a5b4fc;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.75rem;
    flex-shrink: 0;
    font-family: 'JetBrains Mono', monospace;
}

/* Logo / Header */
.app-header {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1035 100%);
    border-bottom: 1px solid #2d2d4e;
    padding: 20px 24px;
    margin: -1rem -1rem 2rem -1rem;
    display: flex;
    align-items: center;
    gap: 16px;
}
.app-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #e0e7ff;
    letter-spacing: -0.02em;
}
.app-subtitle {
    font-size: 0.8rem;
    color: #6366f1;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.12em;
}

/* Inputs */
.stTextInput input, .stNumberInput input, .stSelectbox select {
    background: #13131f !important;
    border: 1px solid #2d2d4e !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 10px 24px;
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: 0.02em;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #6366f1 0%, #818cf8 100%);
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
}

/* Tab styling */
.stTabs [data-baseweb="tab"] {
    color: #6b7280;
    font-weight: 500;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: #a5b4fc;
}

/* Data frame */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #2d2d4e; border-radius: 3px; }

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ── Helper functions ─────────────────────────────────────────────────────────

def fetch_sample_data():
    try:
        r = requests.get(f"{BACKEND_URL}/sample-data", timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Could not fetch sample data: {e}")
        return None


def call_analyze(payload: dict):
    try:
        r = requests.post(f"{BACKEND_URL}/analyze", json=payload, timeout=60)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "❌ Cannot connect to backend. Is it running on port 8000?"
    except requests.exceptions.HTTPError as e:
        detail = e.response.json().get("detail", str(e))
        return None, f"❌ Backend error: {detail}"
    except Exception as e:
        return None, f"❌ Unexpected error: {e}"


def render_metric(value: str, label: str, sub: str = ""):
    sub_html = f'<div class="metric-sub">{sub}</div>' if sub else ""
    return f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {sub_html}
    </div>"""


# ── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 12px 0 24px;">
        <div style="font-size:2.5rem;">📊</div>
        <div style="font-size:1.2rem; font-weight:700; color:#e0e7ff; letter-spacing:-0.02em;">FinSight AI</div>
        <div style="font-size:0.72rem; color:#6366f1; text-transform:uppercase; letter-spacing:0.1em; margin-top:4px;">Financial Risk Assistant</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="font-size:0.75rem; color:#6b7280; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:12px; font-weight:600;">Configuration</div>', unsafe_allow_html=True)

    user_name = st.text_input("Your Name", value="Alex Morgan", placeholder="Enter your name")
    currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "INR", "JPY", "AUD"], index=0)

    st.markdown("---")
    st.markdown('<div style="font-size:0.75rem; color:#6b7280; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:12px; font-weight:600;">About</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.8rem; color:#4b5563; line-height:1.6;">
        FinSight AI analyzes your transactions, detects anomalies, and delivers 
        AI-powered financial insights and risk assessments.
        <br><br>
        <b style="color:#6366f1;">Powered by Gemini AI</b>
    </div>
    """, unsafe_allow_html=True)


# ── Main Content ──────────────────────────────────────────────────────────────

st.markdown("""
<div class="app-header">
    <div>📊</div>
    <div>
        <div class="app-title">FinSight AI</div>
        <div class="app-subtitle">Financial Insights & Risk Assistant</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Input Tabs ────────────────────────────────────────────────────────────────

tab1, tab2 = st.tabs(["📝  Form Input", "📋  JSON Input"])

transactions_payload = []

with tab1:
    st.markdown('<div class="section-header">Transaction Builder</div>', unsafe_allow_html=True)

    col_load, col_clear = st.columns([1, 5])
    with col_load:
        if st.button("Load Sample Data", use_container_width=True):
            sample = fetch_sample_data()
            if sample:
                st.session_state["sample_transactions"] = sample["transactions"]
                st.session_state["user_name_sample"] = sample["user_name"]
                st.success(f"✅ Loaded {len(sample['transactions'])} sample transactions")

    # Initialize session state
    if "form_transactions" not in st.session_state:
        st.session_state["form_transactions"] = []
    if "sample_transactions" in st.session_state:
        if st.session_state["sample_transactions"]:
            transactions_payload = st.session_state["sample_transactions"]
            df_display = pd.DataFrame(transactions_payload)
            st.dataframe(df_display, use_container_width=True, height=250)

    st.markdown("##### Add a Transaction")
    c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
    with c1:
        desc = st.text_input("Description", placeholder="e.g. Grocery Store", key="desc")
    with c2:
        amt = st.number_input("Amount", min_value=0.01, value=50.00, step=0.01, key="amt")
    with c3:
        cat = st.selectbox("Category", CATEGORIES, key="cat")
    with c4:
        date = st.date_input("Date", key="date")

    if st.button("➕ Add Transaction"):
        new_txn = {
            "description": desc,
            "amount": float(amt),
            "category": cat,
            "date": str(date),
        }
        st.session_state["form_transactions"].append(new_txn)
        st.success(f"Added: {desc} — ${amt:.2f}")

    if st.session_state["form_transactions"]:
        st.markdown("##### Added Transactions")
        df_form = pd.DataFrame(st.session_state["form_transactions"])
        st.dataframe(df_form, use_container_width=True, height=200)

        col_use, col_reset = st.columns([1, 5])
        with col_use:
            if st.button("Use These Transactions"):
                transactions_payload = st.session_state["form_transactions"]
        with col_reset:
            if st.button("Clear All"):
                st.session_state["form_transactions"] = []
                st.rerun()

with tab2:
    st.markdown('<div class="section-header">Paste JSON Transactions</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.8rem; color:#6b7280; margin-bottom:12px;">
    Paste an array of transactions. Each object needs: <code style="color:#a5b4fc;">description</code>, 
    <code style="color:#a5b4fc;">amount</code>, <code style="color:#a5b4fc;">category</code>, 
    <code style="color:#a5b4fc;">date</code> (YYYY-MM-DD)
    </div>
    """, unsafe_allow_html=True)

    sample_json = json.dumps([
        {"description": "Grocery Store", "amount": 85.50, "category": "Food & Dining", "date": "2024-01-02"},
        {"description": "Netflix", "amount": 15.99, "category": "Entertainment", "date": "2024-01-03"},
        {"description": "Luxury Watch", "amount": 1250.00, "category": "Shopping", "date": "2024-01-14"},
    ], indent=2)

    json_input = st.text_area("Transaction JSON", value=sample_json, height=250)

    if st.button("Parse JSON"):
        try:
            parsed = json.loads(json_input)
            if isinstance(parsed, list):
                transactions_payload = parsed
                st.success(f"✅ Parsed {len(parsed)} transactions successfully.")
            else:
                st.error("JSON must be an array of transaction objects.")
        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON: {e}")

# ── Analyze Button ──────────────────────────────────────────────────────────

st.markdown("<br>", unsafe_allow_html=True)
col_btn, col_info = st.columns([1, 4])
with col_btn:
    analyze_clicked = st.button("🔍 Analyze Finances", use_container_width=True)

if analyze_clicked:
    if not transactions_payload:
        st.warning("⚠️ No transactions to analyze. Add transactions or load sample data first.")
    else:
        payload = {
            "user_name": user_name or "User",
            "currency": currency,
            "transactions": transactions_payload,
        }

        with st.spinner("🤖 FinSight AI is analyzing your finances..."):
            result, error = call_analyze(payload)

        if error:
            st.error(error)
        else:
            st.session_state["result"] = result
            st.session_state["currency"] = currency

# ── Results ───────────────────────────────────────────────────────────────────

if "result" in st.session_state:
    result = st.session_state["result"]
    curr = st.session_state.get("currency", "USD")
    analysis = result["analysis"]
    insights = result["insights"]

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f'<div style="font-size:1.3rem; font-weight:700; color:#e0e7ff; margin-bottom:24px;">📈 Analysis Results — {user_name}</div>', unsafe_allow_html=True)

    # ── Metrics Row ──────────────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(render_metric(
            f"{curr} {analysis['total_spend']:,.2f}",
            "Total Spend",
            f"{analysis['transaction_count']} transactions"
        ), unsafe_allow_html=True)
    with m2:
        st.markdown(render_metric(
            f"{curr} {analysis['average_transaction']:,.2f}",
            "Avg per Transaction",
            f"Period: {analysis['date_range']['from']} → {analysis['date_range']['to']}"
        ), unsafe_allow_html=True)
    with m3:
        st.markdown(render_metric(
            str(len(analysis["anomalies"])),
            "Anomalies Detected",
            "Transactions above 2× avg"
        ), unsafe_allow_html=True)
    with m4:
        risk = insights["risk_level"]
        st.markdown(render_metric(
            risk,
            "Risk Level",
            insights["spending_pattern"]
        ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts + Breakdown ──────────────────────────────────────────────────
    chart_col, breakdown_col = st.columns([3, 2])

    with chart_col:
        st.markdown('<div class="section-header">Spend by Category</div>', unsafe_allow_html=True)
        cats = analysis["category_breakdown"]
        df_cats = pd.DataFrame(cats)

        fig_pie = px.pie(
            df_cats,
            values="total",
            names="category",
            hole=0.55,
            color_discrete_sequence=px.colors.sequential.Plasma_r,
        )
        fig_pie.update_traces(
            textposition="outside",
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>%{value:.2f} %{customdata}",
            customdata=[[curr]] * len(df_cats),
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#9ca3af", family="Space Grotesk"),
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20),
            height=320,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with breakdown_col:
        st.markdown('<div class="section-header">Category Breakdown</div>', unsafe_allow_html=True)
        for cb in cats:
            pct = cb["percentage"]
            st.markdown(f"""
            <div style="margin-bottom:14px;">
                <div style="display:flex; justify-content:space-between; font-size:0.82rem; margin-bottom:5px;">
                    <span style="color:#d1d5db; font-weight:500;">{cb['category']}</span>
                    <span style="color:#a5b4fc; font-family:'JetBrains Mono',monospace;">{curr} {cb['total']:,.2f}</span>
                </div>
                <div style="background:#1e1e2e; border-radius:999px; height:6px;">
                    <div style="background:linear-gradient(90deg,#6366f1,#a5b4fc); width:{pct}%; height:6px; border-radius:999px;"></div>
                </div>
                <div style="font-size:0.72rem; color:#4b5563; margin-top:3px; font-family:'JetBrains Mono',monospace;">{pct}% · {cb['count']} txns</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Bar Chart ───────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Spend Distribution</div>', unsafe_allow_html=True)
    fig_bar = go.Figure(go.Bar(
        x=df_cats["category"],
        y=df_cats["total"],
        marker=dict(
            color=df_cats["total"],
            colorscale="Purples",
            line=dict(width=0),
        ),
        hovertemplate="<b>%{x}</b><br>Total: %{y:,.2f}<extra></extra>",
    ))
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#9ca3af", family="Space Grotesk"),
        xaxis=dict(gridcolor="#1e1e2e", tickangle=-20),
        yaxis=dict(gridcolor="#1e1e2e"),
        margin=dict(l=20, r=20, t=20, b=20),
        height=280,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # ── Anomalies ────────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">⚠️ Anomaly Detection</div>', unsafe_allow_html=True)
    anomalies = analysis["anomalies"]

    if not anomalies:
        st.markdown("""
        <div style="background:#052e16; border:1px solid #166534; border-radius:12px; padding:16px 20px; color:#4ade80; font-size:0.9rem;">
            ✅ No anomalies detected — your spending looks consistent across all categories.
        </div>
        """, unsafe_allow_html=True)
    else:
        for a in anomalies:
            st.markdown(f"""
            <div class="anomaly-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <div class="anomaly-title">⚡ {a['description']}</div>
                        <div class="anomaly-meta">{a['category']} · Threshold: {curr} {a['threshold']:,.2f}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:1.1rem; font-weight:700; color:#f87171; font-family:'JetBrains Mono',monospace;">{curr} {a['amount']:,.2f}</div>
                        <span class="anomaly-badge">+{a['deviation_percent']:.1f}% above avg</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── AI Insights ──────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">🤖 AI Financial Insights</div>', unsafe_allow_html=True)

    risk_col, summary_col = st.columns([1, 3])
    with risk_col:
        risk = insights["risk_level"]
        rc = RISK_COLORS.get(risk, "#6366f1")
        rb = RISK_BG.get(risk, "#1e1b4b")
        st.markdown(f"""
        <div style="background:{rb}; border:1px solid {rc}33; border-radius:16px; padding:28px 20px; text-align:center;">
            <div style="font-size:2.5rem; margin-bottom:8px;">{"🟢" if risk == "LOW" else "🟡" if risk == "MEDIUM" else "🔴"}</div>
            <div style="font-size:0.7rem; color:#9ca3af; text-transform:uppercase; letter-spacing:0.12em; margin-bottom:8px;">Risk Level</div>
            <div style="font-size:1.4rem; font-weight:800; color:{rc}; font-family:'JetBrains Mono',monospace;">{risk}</div>
            <div style="margin-top:16px; font-size:0.72rem; color:#9ca3af; text-transform:uppercase; letter-spacing:0.1em;">Pattern</div>
            <div style="color:#c7d2fe; font-weight:600; font-size:0.9rem; margin-top:4px;">{insights['spending_pattern']}</div>
        </div>
        """, unsafe_allow_html=True)

    with summary_col:
        st.markdown(f"""
        <div class="insight-box">
            <div style="font-size:0.75rem; color:#6366f1; text-transform:uppercase; letter-spacing:0.12em; font-weight:600; margin-bottom:12px;">Summary</div>
            <div style="color:#d1d5db; font-size:0.95rem; line-height:1.75;">{insights['summary']}</div>
            <div style="margin-top:20px; padding-top:16px; border-top:1px solid #1e2535;">
                <div style="font-size:0.75rem; color:#ef4444; text-transform:uppercase; letter-spacing:0.12em; font-weight:600; margin-bottom:8px;">Risk Assessment</div>
                <div style="color:#fca5a5; font-size:0.9rem; line-height:1.65;">{insights['risk_explanation']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">💡 Recommendations</div>', unsafe_allow_html=True)
    for i, suggestion in enumerate(insights.get("suggestions", []), 1):
        st.markdown(f"""
        <div class="suggestion-item">
            <div class="suggestion-num">{i}</div>
            <div>{suggestion}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Raw Data ──────────────────────────────────────────────────────────────
    with st.expander("🗂️  View Full Transaction Data"):
        if transactions_payload:
            df_all = pd.DataFrame(transactions_payload)
            st.dataframe(df_all, use_container_width=True)

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; color:#374151; font-size:0.75rem; border-top:1px solid #1e1e2e; padding-top:20px;">
        FinSight AI · Powered by Gemini AI & FastAPI · Built with Streamlit
    </div>
    """, unsafe_allow_html=True)
