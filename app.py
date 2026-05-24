import streamlit as st
import random
from datetime import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AML Monitoring System", layout="wide")

st.title("AI-Powered AML Transaction Monitoring System")
st.caption("RBI/FATF aligned rule-based AML alerting engine")

# =========================
# INPUT SECTION
# =========================
st.header("Transaction Details")

amount = st.number_input("Transaction Amount", value=50000.0)

old_bal_orig = st.number_input("Old Balance Origin", value=100000.0)
new_bal_orig = st.number_input("New Balance Origin", value=50000.0)

customer_risk_score = st.slider("Customer Risk Score", 1, 100, 35)
velocity = st.slider("Transaction Velocity", 1, 50, 10)

intl_transfer = st.selectbox("International Transfer", [0, 1])
high_risk_country = st.selectbox("High Risk Country", [0, 1])
pep_flag = st.selectbox("PEP Flag", [0, 1])
adverse_media = st.selectbox("Adverse Media Flag", [0, 1])
sanction_flag = st.selectbox("Sanction Flag", [0, 1])
shell_company = st.selectbox("Shell Company Flag", [0, 1])

sender_country = st.selectbox("Sender Country", ["India", "UK", "USA", "UAE"])
receiver_country = st.selectbox("Receiver Country", ["India", "UK", "USA", "UAE"])

old_bal_dest = st.number_input("Old Balance Destination", value=20000.0)
new_bal_dest = st.number_input("New Balance Destination", value=70000.0)

cash_business = st.selectbox("Cash Intensive Business", [0, 1])
round_txn = st.selectbox("Round Amount Transaction", [0, 1])
structuring = st.selectbox("Structuring Indicator", [0, 1])
multi_accounts = st.selectbox("Multiple Accounts", [0, 1])
rapid_movement = st.selectbox("Rapid Movement of Funds", [0, 1])
inactive_account = st.selectbox("Inactive Account", [0, 1])

# =========================
# ANALYZE BUTTON
# =========================
st.markdown("---")

if st.button("🚨 Analyze Transaction", type="primary"):

    # =========================
    # AML RISK SCORING ENGINE (RBI/FATF STYLE)
    # =========================

    risk_score = 0
    reasons = []

    # Transaction size risk
    if amount > 100000:
        risk_score += 25
        reasons.append("Large transaction (>1L threshold)")

    elif amount > 50000:
        risk_score += 15
        reasons.append("Medium-high transaction amount")

    # Customer risk
    risk_score += customer_risk_score / 10

    # Velocity
    if velocity > 30:
        risk_score += 20
        reasons.append("High transaction velocity detected")

    # Cross border logic (FATF red flag)
    if sender_country != receiver_country:
        risk_score += 20
        reasons.append("Cross-border transaction detected")

    # High risk jurisdiction
    if high_risk_country == 1:
        risk_score += 25
        reasons.append("High-risk jurisdiction involved")

    # PEP / Sanctions / Adverse media (RBI compliance critical flags)
    if pep_flag == 1:
        risk_score += 20
        reasons.append("PEP involvement")

    if sanction_flag == 1:
        risk_score += 40
        reasons.append("Sanction list match risk")

    if adverse_media == 1:
        risk_score += 15
        reasons.append("Adverse media association")

    # Shell company risk
    if shell_company == 1:
        risk_score += 20
        reasons.append("Shell company indicator")

    # Structuring (VERY IMPORTANT AML RULE)
    if structuring == 1:
        risk_score += 25
        reasons.append("Structuring pattern detected")

    # Cash intensive business
    if cash_business == 1:
        risk_score += 10
        reasons.append("Cash intensive business risk")

    # Round transaction (smurfing indicator)
    if round_txn == 1:
        risk_score += 5
        reasons.append("Round amount transaction")

    # Multiple accounts
    if multi_accounts == 1:
        risk_score += 15
        reasons.append("Multiple account usage pattern")

    # Rapid movement of funds
    if rapid_movement == 1:
        risk
