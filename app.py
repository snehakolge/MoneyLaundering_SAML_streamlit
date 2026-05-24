import streamlit as st
import sqlite3
import uuid
import pandas as pd
import datetime
import numpy as np

# ===============================
# DB INIT (inside same file)
# ===============================
conn = sqlite3.connect("aml.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS cases (
    case_id TEXT,
    score REAL,
    severity TEXT,
    status TEXT,
    timestamp TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    txn_id TEXT,
    amount REAL,
    score REAL,
    severity TEXT,
    timestamp TEXT
)
""")

conn.commit()

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(layout="wide")
st.title("🏦 Enterprise AML Monitoring System v3")
st.markdown("RBI/FATF aligned + ML + Rules + Case Management + STR workflow")

# ===============================
# INPUT
# ===============================
st.subheader("Transaction Input")

amount = st.number_input("Transaction Amount", value=50000.0)
risk_score = st.slider("Customer Risk Score", 1, 100, 35)
velocity = st.slider("Transaction Velocity", 1, 50, 10)

sender_country = st.text_input("Sender Country", "India")
receiver_country = st.text_input("Receiver Country", "UK")

pep = st.selectbox("PEP Flag", [0,1])
sanction = st.selectbox("Sanction Flag", [0,1])
structuring = st.selectbox("Structuring Indicator", [0,1])
cross = st.selectbox("Cross Border", [0,1])
round_amt = st.selectbox("Round Amount", [0,1])

# ===============================
# RULE ENGINE (RBI/FATF STYLE)
# ===============================
def rule_engine():
    score = 0
    alerts = []

    if amount >= 50000:
        score += 25
        alerts.append("High-value transaction (CTR threshold)")

    if sender_country != receiver_country or cross == 1:
        score += 20
        alerts.append("Cross-border transaction detected")

    if structuring == 1:
        score += 25
        alerts.append("Structuring pattern detected")

    if pep == 1:
        score += 20
        alerts.append("PEP involvement detected")

    if sanction == 1:
        score += 50
        alerts.append("Sanction risk detected")

    if risk_score > 70:
        score += 15
        alerts.append("High-risk customer profile")

    if velocity > 30:
        score += 10
        alerts.append("High transaction velocity")

    if round_amt == 1:
        score += 5
        alerts.append("Round amount pattern detected")

    score = min(score, 100)

    if score >= 80:
        severity = "CRITICAL"
    elif score >= 60:
        severity = "HIGH"
    elif score >= 40:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return score, severity, alerts

# ===============================
# ANALYSE BUTTON
# ===============================
if st.button("🔍 Analyse Transaction"):

    score, severity, alerts = rule_engine()

    txn_id = str(uuid.uuid4())[:8]
    timestamp = str(datetime.datetime.now())

    # store transaction
    cur.execute("""
        INSERT INTO transactions VALUES (?, ?, ?, ?, ?)
    """, (txn_id, amount, score, severity, timestamp))
    conn.commit()

    # CASE CREATION
    case_id = str(uuid.uuid4())[:8]

    cur.execute("""
        INSERT INTO cases VALUES (?, ?, ?, ?, ?)
    """, (case_id, score, severity, "OPEN", timestamp))
    conn.commit()

    # ===============================
    # OUTPUT
    # ===============================
    st.subheader("📊 AML Result")

    st.metric("AML Risk Score", f"{score}%")
    st.write("Severity:", severity)

    if score >= 60:
        st.error("⚠ Suspicious Transaction")
    else:
        st.success("✅ Normal Transaction")

    # ALERTS
    st.subheader("🚨 Alerts (RBI/FATF Aligned)")

    if alerts:
        for a in alerts:
            st.write("✔", a)
    else:
        st.write("No alerts")

    # STR DECISION
    st.subheader("📌 STR Decision")

    if score >= 60:
        st.error("STR REQUIRED")
        st.write("Enhanced Due Diligence required")
    else:
        st.success("NO STR REQUIRED")

    # CASE ID
    st.subheader("📂 Case Created")
    st.write("Case ID:", case_id)

# ===============================
# CASE DASHBOARD
# ===============================
st.divider()
st.subheader("📂 Case Management Dashboard")

df = pd.read_sql_query("SELECT * FROM cases", conn)

if len(df) > 0:

    st.dataframe(df)

    selected_case = st.selectbox("Select Case ID", df["case_id"].tolist())

    new_status = st.selectbox("Update Status", ["OPEN", "UNDER REVIEW", "CLOSED"])

    if st.button("Update Case"):

        cur.execute("""
            UPDATE cases
            SET status = ?
            WHERE case_id = ?
        """, (new_status, selected_case))

        conn.commit()
        st.success("Case updated successfully")

else:
    st.info("No cases found")
