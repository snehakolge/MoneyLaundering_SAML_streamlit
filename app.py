import streamlit as st
import numpy as np
import pandas as pd
import uuid
from datetime import datetime
import os
import joblib

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI AML Monitoring System",
    layout="wide"
)

st.title("AI-Powered AML Transaction Monitoring System")
st.caption("RBI/FATF-inspired AML monitoring + Case Management System")

# =========================
# LOAD MODEL SAFELY
# =========================
MODEL_PATH = "model.pkl"

model = None
if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
    except:
        model = None

# =========================
# SESSION STORAGE (CASE DB)
# =========================
if "cases" not in st.session_state:
    st.session_state.cases = []

# =========================
# INPUT SECTION
# =========================
st.header("Transaction Input")

col1, col2 = st.columns(2)

with col1:
    amount = st.number_input("Transaction Amount", value=50000.0)
    old_origin = st.number_input("Old Balance Origin", value=100000.0)
    new_origin = st.number_input("New Balance Origin", value=50000.0)
    customer_risk_score = st.slider("Customer Risk Score", 1, 100, 35)
    velocity = st.slider("Transaction Velocity", 1, 50, 10)

with col2:
    international = st.selectbox("International Transfer", [0, 1])
    pep = st.selectbox("PEP Flag", [0, 1])
    sanction = st.selectbox("Sanction Flag", [0, 1])
    structuring = st.selectbox("Structuring Indicator", [0, 1])
    round_amount = st.selectbox("Round Amount Transaction", [0, 1])
    cash_intensive = st.selectbox("Cash Intensive Business", [0, 1])

sender_country = st.text_input("Sender Country", "India")
receiver_country = st.text_input("Receiver Country", "India")

# =========================
# RBI / FATF RULE ENGINE
# =========================
def rule_engine():
    score = 0
    alerts = []

    if amount > 40000:
        score += 25
        alerts.append("High-value transaction (CTR threshold risk)")

    if international:
        score += 20
        alerts.append("Cross-border transaction flagged")

    if pep:
        score += 25
        alerts.append("PEP involvement detected (EDD required)")

    if sanction:
        score += 40
        alerts.append("Sanction list match risk")

    if structuring:
        score += 30
        alerts.append("Structuring pattern detected")

    if customer_risk_score > 80:
        score += 20
        alerts.append("High customer risk score")

    if velocity > 30:
        score += 15
        alerts.append("Abnormal transaction velocity")

    return min(score, 100), alerts

# =========================
# ANALYSE BUTTON
# =========================
if st.button("🔍 Analyse Transaction"):

    rule_score, alerts = rule_engine()

    # =========================
    # ML PREDICTION (SAFE)
    # =========================
    ml_score = None

    if model is not None:
        try:
            X = np.array([[
                amount,
                customer_risk_score,
                velocity,
                international,
                pep,
                sanction,
                structuring,
                round_amount,
                cash_intensive
            ]])

            ml_score = float(model.predict_proba(X)[0][1] * 100)

        except Exception:
            ml_score = None

    # =========================
    # FINAL SCORE
    # =========================
    if ml_score is not None:
        final_score = (0.6 * rule_score) + (0.4 * ml_score)
    else:
        final_score = rule_score

    # =========================
    # SEVERITY
    # =========================
    if final_score >= 80:
        severity = "CRITICAL"
        status = "🚨 Suspicious Transaction Detected"
    elif final_score >= 60:
        severity = "HIGH"
        status = "⚠️ Suspicious Pattern Detected"
    elif final_score >= 40:
        severity = "MEDIUM"
        status = "⚠️ Monitor Transaction"
    else:
        severity = "LOW"
        status = "✅ Normal Transaction"

    # =========================
    # STR DECISION
    # =========================
    str_required = final_score >= 70

    # =========================
    # CASE CREATION (BANK-GRADE FEATURE)
    # =========================
    case_id = str(uuid.uuid4())[:8]

    case = {
        "Case ID": case_id,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Amount": amount,
        "Sender": sender_country,
        "Receiver": receiver_country,
        "Risk Score": round(final_score, 2),
        "Severity": severity,
        "STR Required": str_required,
        "Alerts": ", ".join(alerts) if alerts else "No alerts",
        "Status": "OPEN"
    }

    st.session_state.cases.append(case)

    # =========================
    # OUTPUT UI
    # =========================
    st.subheader(status)

    st.metric("AML Risk Score", f"{final_score:.2f}%")
    st.write("Severity:", severity)

    st.subheader("🚨 Alerts (RBI/FATF Aligned)")

    if alerts:
        for a in alerts:
            st.write("✔", a)
    else:
        st.write("✔ No major anomalies detected")

    st.subheader("STR Recommendation")

    if str_required:
        st.error("STR Filing Recommended")
    else:
        st.success("No STR required")

    st.subheader("Case Created")
    st.success(f"Case ID: {case_id}")

# =========================
# CASE DASHBOARD
# =========================
st.divider()

st.header("📂 AML Case Management Dashboard")

if st.session_state.cases:
    df = pd.DataFrame(st.session_state.cases)

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇ Download Cases CSV",
        df.to_csv(index=False),
        file_name="aml_cases.csv",
        mime="text/csv"
    )
else:
    st.info("No cases generated yet. Run analysis to create cases.")
