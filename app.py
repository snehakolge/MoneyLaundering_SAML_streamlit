import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import uuid
from datetime import datetime
import time

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Bank Grade AML System", layout="wide")

st.title("🏦 Enterprise AML Monitoring & Case Management System")
st.caption("RBI/FATF aligned + Real-time monitoring + STR workflow")

# =========================
# DATABASE SETUP (SQLite)
# =========================
conn = sqlite3.connect("aml_cases.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS cases (
    case_id TEXT,
    timestamp TEXT,
    amount REAL,
    sender TEXT,
    receiver TEXT,
    risk_score REAL,
    severity TEXT,
    alerts TEXT,
    status TEXT,
    str_required TEXT
)
""")
conn.commit()

# =========================
# AML RULE ENGINE
# =========================
def aml_rules(amount, international, pep, sanction, structuring, velocity, risk_score):
    score = 0
    alerts = []

    if amount > 40000:
        score += 25
        alerts.append("CTR Threshold Breach (RBI Cash Transaction Rule)")

    if international:
        score += 20
        alerts.append("Cross-border Layering Risk")

    if structuring:
        score += 30
        alerts.append("Structuring / Smurfing Pattern")

    if pep:
        score += 25
        alerts.append("PEP - Enhanced Due Diligence Required")

    if sanction:
        score += 50
        alerts.append("Sanction List Match - BLOCK IMMEDIATE")

    if velocity > 30:
        score += 15
        alerts.append("High Velocity Transaction")

    if risk_score > 80:
        score += 20
        alerts.append("High Customer Risk Score")

    return min(score, 100), alerts

# =========================
# INPUT UI
# =========================
st.header("Transaction Input")

col1, col2 = st.columns(2)

with col1:
    amount = st.number_input("Transaction Amount", 50000.0)
    sender = st.text_input("Sender Country", "India")
    receiver = st.text_input("Receiver Country", "UK")
    risk_score_input = st.slider("Customer Risk Score", 1, 100, 40)

with col2:
    velocity = st.slider("Transaction Velocity", 1, 50, 10)
    international = st.selectbox("International Transfer", [0, 1])
    pep = st.selectbox("PEP Flag", [0, 1])
    sanction = st.selectbox("Sanction Flag", [0, 1])
    structuring = st.selectbox("Structuring Indicator", [0, 1])

# =========================
# ANALYSE BUTTON
# =========================
if st.button("🔍 Run AML Analysis"):

    # Risk scoring
    risk_score, alerts = aml_rules(
        amount,
        international,
        pep,
        sanction,
        structuring,
        velocity,
        risk_score_input
    )

    # Severity
    if risk_score >= 80:
        severity = "CRITICAL"
    elif risk_score >= 60:
        severity = "HIGH"
    elif risk_score >= 40:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    # STR decision
    str_required = "YES" if risk_score >= 70 else "NO"

    # Case ID
    case_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save to DB
    cursor.execute("""
        INSERT INTO cases VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        case_id,
        timestamp,
        amount,
        sender,
        receiver,
        risk_score,
        severity,
        ", ".join(alerts),
        "OPEN",
        str_required
    ))
    conn.commit()

    # =========================
    # OUTPUT DASHBOARD
    # =========================
    st.subheader("🚨 AML Risk Result")

    st.metric("Risk Score", f"{risk_score:.2f}%")
    st.write("Severity:", severity)

    if severity in ["HIGH", "CRITICAL"]:
        st.error("⚠️ Suspicious Transaction Detected")
    else:
        st.success("✅ Normal Transaction")

    st.subheader("🚨 Alerts (RBI/FATF Aligned)")
    if alerts:
        for a in alerts:
            st.write("✔", a)
    else:
        st.write("No alerts")

    st.subheader("📌 STR Decision")
    if str_required == "YES":
        st.error("STR Filing REQUIRED")
    else:
        st.success("No STR required")

    st.subheader("📂 Case Created")
    st.write("Case ID:", case_id)
    st.write("Status: OPEN")

# =========================
# CASE MANAGEMENT DASHBOARD
# =========================
st.divider()
st.header("📊 Case Management Dashboard")

df = pd.read_sql("SELECT * FROM cases", conn)

if len(df) > 0:
    st.dataframe(df, use_container_width=True)

    # Update status
    st.subheader("Update Case Status")

    selected_case = st.selectbox("Select Case ID", df["case_id"].tolist())
    new_status = st.selectbox("Change Status", ["OPEN", "UNDER REVIEW", "ESCALATED", "CLOSED"])

    if st.button("Update Case"):
        cursor.execute("""
            UPDATE cases SET status=? WHERE case_id=?
        """, (new_status, selected_case))
        conn.commit()
        st.success("Case Updated Successfully")

    # Download report
    st.download_button(
        "⬇ Download AML Cases Report",
        df.to_csv(index=False),
        file_name="aml_cases.csv"
    )

else:
    st.info("No cases available yet")

# =========================
# SIMPLE REAL-TIME SIMULATION
# =========================
st.divider()
st.header("⏱ Real-Time Monitoring Simulation")

st.write("Auto-refreshing dashboard simulation (manual refresh)")

if st.button("Refresh Cases View"):
    st.rerun()
