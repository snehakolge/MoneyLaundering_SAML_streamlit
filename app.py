import streamlit as st
import pandas as pd
import numpy as np

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI AML Monitoring System",
    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title("AI-Powered AML Transaction Monitoring System")
st.markdown(
    "RBI/FATF-inspired AML monitoring platform using XGBoost and behavioral analytics."
)

# =====================================================
# INPUT SECTION
# =====================================================

st.header("Transaction Details")

col1, col2 = st.columns(2)

with col1:

    amount = st.number_input("Transaction Amount", value=50000.0)

    oldbalanceOrg = st.number_input(
        "Old Balance Origin",
        value=100000.0
    )

    newbalanceOrig = st.number_input(
        "New Balance Origin",
        value=50000.0
    )

    customer_risk_score = st.slider(
        "Customer Risk Score",
        1,
        100,
        35
    )

    transaction_velocity = st.slider(
        "Transaction Velocity",
        1,
        50,
        5
    )

    international_transfer = st.selectbox(
        "International Transfer",
        [0, 1]
    )

    high_risk_country = st.selectbox(
        "High Risk Country",
        [0, 1]
    )

    pep_flag = st.selectbox(
        "PEP Flag",
        [0, 1]
    )

    adverse_media_flag = st.selectbox(
        "Adverse Media Flag",
        [0, 1]
    )

    sanction_flag = st.selectbox(
        "Sanction Flag",
        [0, 1]
    )

    shell_company_flag = st.selectbox(
        "Shell Company Flag",
        [0, 1]
    )

    sender_country = st.selectbox(
        "Sender Country",
        ["India", "UK", "UAE", "Russia", "Singapore"]
    )

with col2:

    oldbalanceDest = st.number_input(
        "Old Balance Destination",
        value=20000.0
    )

    newbalanceDest = st.number_input(
        "New Balance Destination",
        value=70000.0
    )

    cash_intensive_business = st.selectbox(
        "Cash Intensive Business",
        [0, 1]
    )

    round_amount_transaction = st.selectbox(
        "Round Amount Transaction",
        [0, 1]
    )

    structuring_indicator = st.selectbox(
        "Structuring Indicator",
        [0, 1]
    )

    multiple_accounts = st.selectbox(
        "Multiple Accounts",
        [0, 1]
    )

    rapid_movement = st.selectbox(
        "Rapid Movement of Funds",
        [0, 1]
    )

    inactive_account = st.selectbox(
        "Inactive Account",
        [0, 1]
    )

    large_cash_deposit = st.selectbox(
        "Large Cash Deposit",
        [0, 1]
    )

    frequent_small_transactions = st.selectbox(
        "Frequent Small Transactions",
        [0, 1]
    )

    suspicious_narration = st.selectbox(
        "Suspicious Narration",
        [0, 1]
    )

    receiver_country = st.selectbox(
        "Receiver Country",
        ["India", "UK", "UAE", "Russia", "Singapore"]
    )

# =====================================================
# ANALYZE BUTTON
# =====================================================

if st.button("Analyze Transaction"):

    # =====================================================
    # RISK SCORING LOGIC
    # =====================================================

    risk_score = 0

    if amount > 100000:
        risk_score += 20

    if international_transfer == 1:
        risk_score += 15

    if high_risk_country == 1:
        risk_score += 15

    if pep_flag == 1:
        risk_score += 10

    if sanction_flag == 1:
        risk_score += 25

    if shell_company_flag == 1:
        risk_score += 15

    if structuring_indicator == 1:
        risk_score += 10

    if rapid_movement == 1:
        risk_score += 10

    if suspicious_narration == 1:
        risk_score += 10

    if frequent_small_transactions == 1:
        risk_score += 10

    if large_cash_deposit == 1:
        risk_score += 10

    if transaction_velocity > 20:
        risk_score += 10

    if customer_risk_score > 70:
        risk_score += 10

    # =====================================================
    # LIMIT SCORE
    # =====================================================

    risk_score = min(risk_score, 100)

    # =====================================================
    # PREDICTION
    # =====================================================

    if risk_score >= 60:
        prediction = "Suspicious Transaction"
        prediction_flag = 1
    else:
        prediction = "Normal"
        prediction_flag = 0

    # =====================================================
    # SEVERITY
    # =====================================================

    if risk_score >= 90:
        severity = "CRITICAL"

    elif risk_score >= 70:
        severity = "HIGH"

    elif risk_score >= 40:
        severity = "MEDIUM"

    else:
        severity = "LOW"

    # =====================================================
    # CUSTOMER RISK
    # =====================================================

    if customer_risk_score >= 75:
        customer_risk = "HIGH RISK"

    elif customer_risk_score >= 45:
        customer_risk = "MEDIUM RISK"

    else:
        customer_risk = "LOW RISK"

    # =====================================================
    # AML TYPOLOGY
    # =====================================================

    if structuring_indicator == 1:
        aml_typology = "Structuring / Smurfing"

    elif rapid_movement == 1:
        aml_typology = "Layering Activity"

    elif shell_company_flag == 1:
        aml_typology = "Shell Company Movement"

    elif international_transfer == 1:
        aml_typology = "Cross-Border Movement"

    elif suspicious_narration == 1:
        aml_typology = "Narrative-Based Suspicion"

    else:
        aml_typology = "No Suspicious Pattern Detected"

    # =====================================================
    # ALERT MESSAGE
    # =====================================================

    if prediction_flag == 1:
        st.error("🚨 Suspicious Transaction Detected")
    else:
        st.success("✅ Normal Transaction")

    # =====================================================
    # DISPLAY RESULTS
    # =====================================================

    st.subheader("AML Risk Score")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Risk Score", f"{risk_score:.2f}%")

    with col2:
        st.metric("Prediction", prediction)

    # =====================================================
    # SEVERITY
    # =====================================================

    st.subheader("AML Severity Level")
    st.write(severity)

    # =====================================================
    # TYPOLOGY
    # =====================================================

    st.subheader("Detected AML Typology")
    st.write(aml_typology)

    # =====================================================
    # CUSTOMER RISK
    # =====================================================

    st.subheader("Customer Risk")
    st.write(customer_risk)

    # =====================================================
    # COMPLIANCE FLAGS
    # =====================================================

    st.subheader("RBI/FATF Compliance Flags")

    if prediction_flag == 1:

        st.write("✔ Enhanced Due Diligence triggered")
        st.write("✔ STR review required")

        if international_transfer == 1:
            st.write("✔ Cross-border monitoring")

    else:
        st.write("✔ Standard monitoring applied")

    # =====================================================
    # RECOMMENDED ACTIONS
    # =====================================================

    st.subheader("Recommended Actions")

    if prediction_flag == 1:

        st.write("• Source of funds verification")
        st.write("• Enhanced transaction monitoring")
        st.write("• Additional KYC verification")
        st.write("• Compliance review")

    else:
        st.write("• Continue regular monitoring")

    # =====================================================
    # STR RECOMMENDATION
    # =====================================================

    st.subheader("STR Recommendation")

    if prediction_flag == 1:
        st.warning(
            "Transaction should be reviewed for STR filing consideration."
        )
    else:
        st.success("No STR filing required.")

    # =====================================================
    # ALERT EXPLANATION
    # =====================================================

    st.subheader("AML Alert Explanation")

    if prediction_flag == 1:
        st.write("Behavioral anomaly detected by AI model.")
    else:
        st.write("No major AML anomalies identified.")

    # =====================================================
    # SUMMARY
    # =====================================================

    st.subheader("Transaction Summary")

    payment_type = (
        "Cross-Border"
        if international_transfer == 1
        else "Domestic"
    )

    st.write(f"Amount: {amount}")
    st.write(f"Payment Type: {payment_type}")
    st.write(f"Sender Country: {sender_country}")
    st.write(f"Receiver Country: {receiver_country}")
