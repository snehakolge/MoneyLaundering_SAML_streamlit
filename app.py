import streamlit as st
import pandas as pd
import numpy as np
import uuid
from datetime import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AML Monitoring System v4.2", layout="wide")

st.title("AML Monitoring System v4.2")
st.caption("RBI/FATF aligned AML + ML + Rules + Case Management")

# =========================
# SAFE CASE SCHEMA (VERY IMPORTANT)
# =========================
CASE_SCHEMA = [
    "case_id",
    "timestamp",
    "risk_score",
    "severity",
    "status",
    "alert",
    "amount",
    "sender",
    "receiver"
]

# =========================
# SAFE SESSION INIT
# =========================
if "cases" not in st.session_state:
    st.session_state["cases"] = pd.DataFrame(columns=CASE_SCHEMA)

# =========================
# RESET BUTTON (FIXES OLD BROKEN DEPLOYMENTS)
# =========================
with st.sidebar:
    if st.button("Reset Case Database"):
        st.session_state["cases"] = pd.DataFrame(columns=CASE_SCHEMA)
        st.success("Reset complete")

# =========================
# INPUT UI
# =========================
st.header("Transaction Input")

col1, col2, col3 = st.columns(3)

with col1:
    amount = st.number_input("Transaction Amount", 0.0, 1e7, 50000.0)
    sender_country = st.selectbox("Sender Country", ["India", "UK", "USA", "UAE"])
    receiver_country = st.selectbox("Receiver Country", ["India", "UK", "USA", "UAE"])
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

# =========================
# RULE ENGINE (RBI/FATF STYLE)
# =========================
def rule_engine():
    score = 0
    alerts = []

    if amount > 100000:
        score += 30
        alerts.append("High-value transaction risk")

    if structuring == 1:
        score += 25
        alerts.append("Structuring detected")

    if cross_border == 1 or sender_country != receiver_country:
        score += 15
        alerts.append("Cross-border risk")

    if pep == 1:
        score += 20
        alerts.append("PEP flagged customer")

    if sanction == 1:
        score += 40
        alerts.append("Sanction list hit")

    if velocity > 40:
        score += 15
        alerts.append("High velocity activity")

    if round_amt == 1:
        score += 10
        alerts.append("Round amount pattern")

    if cash_intensive == 1:
        score += 15
        alerts.append("Cash-intensive business risk")

    return min(score, 100), alerts

# =========================
# SAFE ML SCORE (SIMULATED)
# =========================
def ml_score():
    base = (
        customer_risk * 0.35 +
        velocity * 1.2 +
        structuring * 25 +
        cross_border * 10 +
        pep * 20 +
        sanction * 40
    )
    return max(0, min(100, base + np.random.uniform(-2, 2)))

# =========================
# ANALYSE BUTTON (SAFE)
# =========================
if st.button("Analyse Transaction"):

    rule_score, alerts = rule_engine()
    model_score = ml_score()

    final_score = (rule_score * 0.5) + (model_score * 0.5)

    if final_score >= 80:
        severity = "CRITICAL"
    elif final_score >= 60:
        severity = "HIGH"
    elif final_score >= 40:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    suspicious = final_score >= 55

    st.subheader("Result")

    if suspicious:
        st.error("Suspicious Transaction Detected")
    else:
        st.success("Normal Transaction")

    st.write("AML Risk Score:", round(final_score, 2))
    st.write("Severity:", severity)

    st.subheader("Alerts")

    if alerts:
        for a in alerts:
            st.write("-", a)
    else:
        st.write("No AML alerts detected")

    # =========================
    # CREATE SAFE CASE
    # =========================
    case_id = str(uuid.uuid4())[:8]

    new_case = {
        "case_id": case_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "risk_score": float(round(final_score, 2)),
        "severity": severity,
        "status": "OPEN",
        "alert": ", ".join(alerts) if alerts else "Normal",
        "amount": amount,
        "sender": sender_country,
        "receiver": receiver_country
    }

    st.session_state["cases"] = pd.concat(
        [st.session_state["cases"], pd.DataFrame([new_case])],
        ignore_index=True
    )

    st.success(f"Case Created: {case_id}")

# =========================
# CASE DASHBOARD (CRASH-PROOF)
# =========================
st.divider()
st.header("Case Management Dashboard")

df = st.session_state.get("cases", pd.DataFrame(columns=CASE_SCHEMA))

# FORCE STRUCTURE CONSISTENCY
for col in CASE_SCHEMA:
    if col not in df.columns:
        df[col] = None

df = df[CASE_SCHEMA]

if df.empty:
    st.info("No cases generated yet")
else:
    st.dataframe(df, use_container_width=True)

    case_list = df["case_id"].dropna().tolist()

    if case_list:
        selected_case = st.selectbox("Select Case ID", case_list)

        new_status = st.selectbox("Update Status", ["OPEN", "UNDER REVIEW", "CLOSED"])

        if st.button("Update Case Status"):
            st.session_state["cases"].loc[
                st.session_state["cases"]["case_id"] == selected_case,
                "status"
            ] = new_status

            st.success("Status updated successfully")
