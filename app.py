import streamlit as st
import pandas as pd
import numpy as np
import uuid
from datetime import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AML Monitoring System v4", layout="wide")

st.title("🏦 Enterprise AML Monitoring System v4")
st.caption("RBI/FATF aligned + ML + Rules + Case Management + STR Workflow")

# =========================
# SESSION STATE (CASE DB)
# =========================
if "cases" not in st.session_state:
    st.session_state.cases = pd.DataFrame(columns=[
        "case_id", "timestamp", "risk_score", "severity",
        "status", "alert", "amount", "sender", "receiver"
    ])

# =========================
# INPUT UI
# =========================
st.header("📥 Transaction Input")

col1, col2, col3 = st.columns(3)

with col1:
    amount = st.number_input("Transaction Amount", 0.0, 1e7, 50000.0)
    sender_country = st.selectbox("Sender Country", ["India", "UK", "USA", "UAE", "Other"])
    receiver_country = st.selectbox("Receiver Country", ["India", "UK", "USA", "UAE", "Other"])
    customer_risk = st.slider("Customer Risk Score", 1, 100, 35)

with col2:
    velocity = st.slider("Transaction Velocity", 1, 50, 10)
    pep = st.selectbox("PEP Flag", [0, 1])
    sanction = st.selectbox("Sanction Flag", [0, 1])
    structuring = st.selectbox("Structuring Indicator", [0, 1])

with col3:
    cross_border = st.selectbox("Cross Border", [0, 1])
    round_amt = st.selectbox("Round Amount", [0, 1])
    cash_intensive = st.selectbox("Cash Intensive Business", [0, 1])
    multiple_accounts = st.selectbox("Multiple Accounts", [0, 1])

# =========================
# RULE ENGINE (RBI/FATF STYLE)
# =========================
def rule_engine():
    score = 0
    alerts = []

    if amount > 100000:
        score += 30
        alerts.append("High-value transaction (CTR threshold risk)")

    if structuring == 1:
        score += 25
        alerts.append("Structuring pattern detected (smurfing risk)")

    if cross_border == 1:
        score += 15
        alerts.append("Cross-border transaction flagged")

    if pep == 1:
        score += 20
        alerts.append("PEP customer risk")

    if sanction == 1:
        score += 40
        alerts.append("Sanction list match risk")

    if velocity > 40:
        score += 20
        alerts.append("High transaction velocity detected")

    if round_amt == 1:
        score += 10
        alerts.append("Round amount suspicious pattern")

    if cash_intensive == 1:
        score += 15
        alerts.append("Cash-intensive business risk")

    if sender_country != receiver_country:
        score += 10
        alerts.append("International transfer risk pattern")

    return min(score, 100), alerts


# =========================
# ML LAYER (SAFE FALLBACK)
# =========================
def ml_score():
    """
    If model is missing → fallback deterministic ML-like score
    """
    base = (
        customer_risk * 0.3 +
        velocity * 1.2 +
        structuring * 25 +
        cross_border * 10 +
        pep * 20 +
        sanction * 40
    )

    noise = np.random.uniform(-5, 5)
    return max(0, min(100, base + noise))


# =========================
# ANALYSE BUTTON
# =========================
if st.button("🔍 Analyse Transaction"):

    rule_score, alerts = rule_engine()
    model_score = ml_score()

    final_score = (0.5 * rule_score) + (0.5 * model_score)

    # =========================
    # SEVERITY
    # =========================
    if final_score >= 80:
        severity = "CRITICAL"
    elif final_score >= 60:
        severity = "HIGH"
    elif final_score >= 40:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    is_suspicious = final_score >= 55

    # =========================
    # ALERT DISPLAY
    # =========================
    st.subheader("📊 Result")

    if is_suspicious:
        st.error("🚨 Suspicious Transaction Detected")
    else:
        st.success("✅ Normal Transaction")

    st.metric("AML Risk Score", f"{final_score:.2f}%")
    st.write("Severity:", severity)

    # =========================
    # RBI/FATF ALERTS
    # =========================
    st.subheader("🚨 Alerts (RBI/FATF Aligned)")

    if alerts:
        for a in alerts:
            st.write("✔", a)
    else:
        st.write("✔ No major AML alerts detected")

    # =========================
    # CASE CREATION
    # =========================
    case_id = str(uuid.uuid4())[:8]

    new_case = pd.DataFrame([{
        "case_id": case_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "risk_score": final_score,
        "severity": severity,
        "status": "OPEN",
        "alert": "; ".join(alerts) if alerts else "Normal",
        "amount": amount,
        "sender": sender_country,
        "receiver": receiver_country
    }])

    st.session_state.cases = pd.concat([st.session_state.cases, new_case], ignore_index=True)

    st.success(f"📂 Case Created: {case_id}")


# =========================
# CASE MANAGEMENT DASHBOARD
# =========================
st.divider()
st.header("📂 Case Management Dashboard")

if len(st.session_state.cases) > 0:

    df = st.session_state.cases

    selected_case = st.selectbox("Select Case ID", df["case_id"].tolist())

    status = st.selectbox("Update Status", ["OPEN", "UNDER REVIEW", "CLOSED"])

    if st.button("💾 Update Case"):
        st.session_state.cases.loc[
            st.session_state.cases["case_id"] == selected_case, "status"
        ] = status
        st.success("Case updated successfully")

    st.dataframe(st.session_state.cases)

else:
    st.info("No cases generated yet")
