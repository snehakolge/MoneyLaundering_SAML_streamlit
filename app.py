import streamlit as st
import pandas as pd
import numpy as np
import joblib

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI AML Monitoring System",
    layout="wide"
)

# =====================================================
# LOAD MODEL
# =====================================================

model = joblib.load("xgboost_aml_model.pkl")

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

    amount = st.number_input(
        "Transaction Amount",
        min_value=0.0,
        value=50000.0
    )

    oldbalanceOrg = st.number_input(
        "Old Balance Origin",
        min_value=0.0,
        value=100000.0
    )

    newbalanceOrig = st.number_input(
        "New Balance Origin",
        min_value=0.0,
        value=50000.0
    )

    customer_risk_score = st.slider(
        "Customer Risk Score",
        1,
        100,
        70
    )

    transaction_velocity = st.slider(
        "Transaction Velocity",
        1,
        50,
        10
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
        ["India", "UAE", "UK", "USA", "Pakistan"]
    )

with col2:

    oldbalanceDest = st.number_input(
        "Old Balance Destination",
        min_value=0.0,
        value=20000.0
    )

    newbalanceDest = st.number_input(
        "New Balance Destination",
        min_value=0.0,
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

    rapid_movement_funds = st.selectbox(
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
        ["India", "UAE", "UK", "USA", "Pakistan"]
    )

# =====================================================
# COUNTRY ENCODING
# =====================================================

country_mapping = {
    "India": 0,
    "UAE": 1,
    "UK": 2,
    "USA": 3,
    "Pakistan": 4
}

sender_country_encoded = country_mapping[sender_country]
receiver_country_encoded = country_mapping[receiver_country]

# =====================================================
# INPUT DATAFRAME
# =====================================================

input_data = pd.DataFrame({

    "amount": [amount],
    "oldbalanceOrg": [oldbalanceOrg],
    "newbalanceOrig": [newbalanceOrig],
    "oldbalanceDest": [oldbalanceDest],
    "newbalanceDest": [newbalanceDest],

    "customer_risk_score": [customer_risk_score],
    "transaction_velocity": [transaction_velocity],

    "international_transfer": [international_transfer],
    "high_risk_country": [high_risk_country],

    "pep_flag": [pep_flag],
    "adverse_media_flag": [adverse_media_flag],
    "sanction_flag": [sanction_flag],
    "shell_company_flag": [shell_company_flag],

    "cash_intensive_business": [cash_intensive_business],
    "round_amount_transaction": [round_amount_transaction],
    "structuring_indicator": [structuring_indicator],
    "multiple_accounts": [multiple_accounts],
    "rapid_movement_funds": [rapid_movement_funds],
    "inactive_account": [inactive_account],
    "large_cash_deposit": [large_cash_deposit],
    "frequent_small_transactions": [frequent_small_transactions],
    "suspicious_narration": [suspicious_narration],

    "sender_country": [sender_country_encoded],
    "receiver_country": [receiver_country_encoded]

})

# =====================================================
# REQUIRED FEATURES
# =====================================================

required_features = [
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
    "customer_risk_score",
    "transaction_velocity",
    "international_transfer",
    "high_risk_country",
    "pep_flag",
    "adverse_media_flag",
    "sanction_flag",
    "shell_company_flag",
    "cash_intensive_business",
    "round_amount_transaction",
    "structuring_indicator",
    "multiple_accounts",
    "rapid_movement_funds",
    "inactive_account",
    "large_cash_deposit",
    "frequent_small_transactions",
    "suspicious_narration",
    "sender_country",
    "receiver_country"
]

for feature in required_features:
    if feature not in input_data.columns:
        input_data[feature] = 0

input_data = input_data[required_features]

# =====================================================
# PREDICTION
# =====================================================

if st.button("Analyze Transaction"):

    prediction = model.predict(input_data)[0]

    probability = model.predict_proba(input_data)[0][1]

    risk_score = probability * 100

    # =================================================
    # AML LOGIC
    # =================================================

    aml_flags = (
        international_transfer
        + high_risk_country
        + pep_flag
        + sanction_flag
        + shell_company_flag
        + structuring_indicator
        + suspicious_narration
        + rapid_movement_funds
    )

    if risk_score >= 85:
        severity = "CRITICAL"
    elif risk_score >= 60:
        severity = "HIGH"
    elif risk_score >= 40:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    if aml_flags >= 4:
        typology = "Layering / Structuring"
    elif international_transfer == 1 and high_risk_country == 1:
        typology = "Cross-Border Risk"
    elif rapid_movement_funds == 1:
        typology = "Rapid Movement of Funds"
    else:
        typology = "Normal Activity"

    # =================================================
    # RESULTS
    # =================================================

    st.markdown("---")

    if prediction == 1:

        st.error("🚨 Suspicious Transaction Detected")

        decision = "Suspicious Transaction"

        alert_text = "Behavioral anomaly detected by AI model."

        str_msg = "Transaction should be reviewed for STR filing consideration."

    else:

        st.success("✅ Normal Transaction")

        decision = "Normal"

        alert_text = "No major AML anomalies identified."

        str_msg = "No STR filing required."

    # =================================================
    # METRICS
    # =================================================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "AML Risk Score",
            f"{risk_score:.2f}%"
        )

    with col2:
        st.metric(
            "Prediction",
            decision
        )

    with col3:
        st.metric(
            "AML Severity Level",
            severity
        )

    # =================================================
    # TYPOLOGY
    # =================================================

    st.subheader("Detected AML Typology")
    st.info(typology)

    # =================================================
    # CUSTOMER RISK
    # =================================================

    st.subheader("Customer Risk")

    if customer_risk_score >= 75:
        st.error("HIGH RISK")
    elif customer_risk_score >= 50:
        st.warning("MEDIUM RISK")
    else:
        st.success("LOW RISK")

    # =================================================
    # RBI/FATF FLAGS
    # =================================================

    st.subheader("RBI/FATF Compliance Flags")

    if prediction == 1:

        st.write("✔ Enhanced Due Diligence triggered")
        st.write("✔ STR review required")

        if international_transfer == 1:
            st.write("✔ Cross-border monitoring")

        if high_risk_country == 1:
            st.write("✔ FATF high-risk jurisdiction identified")

        if pep_flag == 1:
            st.write("✔ Politically Exposed Person monitoring")

    else:

        st.write("✔ Standard monitoring applied")

    # =================================================
    # RECOMMENDED ACTIONS
    # =================================================

    st.subheader("Recommended Actions")

    if prediction == 1:

        st.write("• Source of funds verification")
        st.write("• Enhanced transaction monitoring")
        st.write("• Additional KYC verification")
        st.write("• Compliance review")

    else:

        st.write("• Continue standard monitoring")
        st.write("• Maintain periodic KYC review")

    # =================================================
    # STR
    # =================================================

    st.subheader("STR Recommendation")
    st.info(str_msg)

    # =================================================
    # ALERT EXPLANATION
    # =================================================

    st.subheader("AML Alert Explanation")
    st.warning(alert_text)

    # =================================================
    # SUMMARY
    # =================================================

    st.subheader("Transaction Summary")

    payment_type = (
        "Cross-border"
        if international_transfer == 1
        else "Domestic"
    )

    st.write(f"Amount: {amount}")
    st.write(f"Payment Type: {payment_type}")
    st.write(f"Sender Country: {sender_country}")
    st.write(f"Receiver Country: {receiver_country}")
