import streamlit as st
import pandas as pd
import numpy as np
import uuid
from datetime import datetime

st.set_page_config(page_title="AML Monitoring System v4.3", layout="wide")

st.title("AML Monitoring System v4.3")

# =========================
# SAFE SCHEMA
# =========================
CASE_SCHEMA = [
    "case_id", "timestamp", "risk_score",
    "severity", "status", "alert",
    "amount", "sender", "receiver"
]

# =========================
# SAFE INIT (CRITICAL FIX)
# =========================
if "cases" not in st.session_state:
    st.session_state["cases"] = pd.DataFrame(columns=CASE_SCHEMA)

# 🔥 HARD SAFETY RESET (FIXES YOUR ERROR)
if not isinstance(st.session_state["cases"], pd.DataFrame):
    st.session_state["cases"] = pd.DataFrame(columns=CASE_SCHEMA)

# =========================
# INPUT
# =========================
st.header("Transaction Input")

amount = st.number_input("Transaction Amount", 0.0, 1e7, 50000.0)
sender = st.selectbox("Sender Country", ["India", "UK", "USA"])
receiver = st.selectbox("Receiver Country", ["India", "UK", "USA"])

risk = st.slider("Customer Risk Score", 1, 100, 35)
velocity = st.slider("Transaction Velocity", 1, 50, 10)

pep = st.selectbox("PEP", [0, 1])
sanction = st.selectbox("Sanction", [0, 1])
structuring = st.selectbox("Structuring", [0, 1])

# =========================
# RULE ENGINE
# =========================
def rule_engine():
    score = 0
    alerts = []

    if amount > 100000:
        score += 30
        alerts.append("High value transaction")

    if structuring:
        score += 25
        alerts.append("Structuring detected")

    if sender != receiver:
        score += 15
        alerts.append("Cross border risk")

    if pep:
        score += 20
        alerts.append("PEP flagged")

    if sanction:
        score += 40
        alerts.append("Sanction match")

    return min(score, 100), alerts

# =========================
# ML SCORE (SAFE)
# =========================
def ml_score():
    return max(0, min(100,
        risk * 0.4 +
        velocity * 1.5 +
        structuring * 25 +
        pep * 20 +
        sanction * 40
    ))

# =========================
# ANALYSE
# =========================
if st.button("Analyse Transaction"):

    rule_score, alerts = rule_engine()
    ml = ml_score()

    final_score = (rule_score + ml) / 2

    if final_score >= 80:
        severity = "CRITICAL"
    elif final_score >= 60:
        severity = "HIGH"
    elif final_score >= 40:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    st.subheader("Result")
    st.write("Score:", round(final_score, 2))
    st.write("Severity:", severity)

    st.subheader("Alerts")
    st.write(alerts if alerts else "No alerts")

    # =========================
    # SAFE CASE CREATION (NO CONCAT CRASH EVER)
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
        "sender": sender,
        "receiver": receiver
    }

    # 🔥 FINAL SAFE APPEND METHOD (NO PANDAS CONCAT FAILURE)
    df_old = st.session_state["cases"]

    if not isinstance(df_old, pd.DataFrame):
        df_old = pd.DataFrame(columns=CASE_SCHEMA)

    df_new = pd.DataFrame([new_case])

    st.session_state["cases"] = pd.concat([df_old, df_new], ignore_index=True)

    st.success(f"Case Created: {case_id}")

# =========================
# DASHBOARD (SAFE)
# =========================
st.divider()
st.header("Case Dashboard")

df = st.session_state.get("cases", pd.DataFrame(columns=CASE_SCHEMA))

if not isinstance(df, pd.DataFrame):
    df = pd.DataFrame(columns=CASE_SCHEMA)

for c in CASE_SCHEMA:
    if c not in df.columns:
        df[c] = None

df = df[CASE_SCHEMA]

if df.empty:
    st.info("No cases yet")
else:
    st.dataframe(df, use_container_width=True)

    case_ids = df["case_id"].dropna().tolist()

    if case_ids:
        selected = st.selectbox("Select Case", case_ids)

        status = st.selectbox("Status", ["OPEN", "UNDER REVIEW", "CLOSED"])

        if st.button("Update"):
            st.session_state["cases"].loc[
                st.session_state["cases"]["case_id"] == selected,
                "status"
            ] = status

            st.success("Updated successfully")
