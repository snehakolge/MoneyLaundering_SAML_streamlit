import streamlit as st
import pandas as pd
import numpy as np

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI AML Monitoring System",
    layout="wide"
)

st.title("AI-Powered AML Transaction Monitoring System")
st.write("RBI/FATF-inspired AML monitoring platform using behavioral analytics")

# =========================
# INPUTS
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
multi_accounts = st
