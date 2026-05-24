import streamlit as st
import pandas as pd
import joblib
import xgboost as xgb

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI AML Monitoring System",
    layout="wide"
)

# =====================================================
# LOAD MODEL FILES
# =====================================================

model = joblib.load("xgboost_aml_model.pkl")
feature_columns = joblib.load("feature_columns.pkl")

# =====================================================
# TITLE
# =====================================================

st.title("🛡 AI-Powered AML Transaction Monitoring System")

st.markdown("""
RBI/FATF-inspired AML monitoring platform using XGBoost and behavioral analytics.
""")

# =====================================================
# USER INPUTS
# =====================================================

st.header("Transaction Details")

col1, col2 = st.columns(2)

with col1:

    amount = st.number_input("Transaction Amount", value=50000.0)

    oldbalanceOrg = st.number_input("Old Balance Origin", value=100000.0)

    newbalanceOrig = st.number_input("New Balance Origin", value=50000.0)

    customer_risk_score = st.slider("Customer Risk Score", 1, 100, 85)

    transaction_velocity = st.slider("Transaction Velocity", 1, 50, 20)

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

    oldbalanceDest = st.number_input("Old Balance Destination", value=20000.0)

    newbalanceDest = st.number_input("New Balance Destination", value=70000.0)

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
        ["India", "UK", "UAE", "Russia", "Singapore"]
    )

# =====================================================
# CREATE INPUT DATA
# =====================================================

input_dict = {

    "amount": amount,
    "oldbalanceOrg": oldbalanceOrg,
    "newbalanceOrig": newbalanceOrig,
    "oldbalanceDest": oldbalanceDest,
    "newbalanceDest": newbalanceDest,
    "customer_risk_score": customer_risk_score,
    "transaction_velocity": transaction_velocity,
    "international_transfer": international_transfer,
    "high_risk_country": high_risk_country,
    "pep_flag": pep_flag,
    "adverse_media_flag": adverse_media_flag,
    "sanction_flag": sanction_flag,
    "cash_intensive_business": cash_intensive_business,
    "round_amount_transaction": round_amount_transaction,
    "structuring_indicator": structuring_indicator,
    "multiple_accounts": multiple_accounts,
    "rapid_movement_funds": rapid_movement_funds,
    "inactive_account": inactive_account,
    "large_cash_deposit": large_cash_deposit,
    "frequent_small_transactions": frequent_small_transactions,
    "device_change_flag": 0,
    "ip_change_flag": 0,
    "kyc_pending": 0,
    "source_of_funds_unverified": 0,
    "beneficiary_risk": customer_risk_score,
    "shell_company_flag": shell_company_flag,
    "transaction_time_risk": 1,
    "high_risk_industry": 0,
    "suspicious_narration": suspicious_narration
}

input_data = pd.DataFrame([input_dict])

# Ensure feature order
input_data = input_data[feature_columns]

# =====================================================
# PREDICTION
# =====================================================

if st.button("Analyze Transaction"):

    prediction = model.predict(input_data)[0]

    probability = model.predict_proba(input_data)[0][1]

    risk_score = probability * 100

    # =================================================
    # AML TYPOLOGY
    # =================================================

    if prediction == 1:

        if international_transfer == 1 and amount > 10000:
            typology = "Cross-Border Layering"

        elif structuring_indicator == 1:
            typology = "Structuring / Smurfing"

        elif rapid_movement_funds == 1:
            typology = "Rapid Movement of Funds"

        elif shell_company_flag == 1:
            typology = "Shell Company Activity"

        elif large_cash_deposit == 1:
            typology = "Large Cash Deposit Pattern"

        else:
            typology = "Behavioral AML Anomaly"

    else:
        typology = "Legitimate Transaction"

    # =================================================
    # SEVERITY
    # =================================================

    if risk_score >= 90:
        severity = "CRITICAL"

    elif risk_score >= 70:
        severity = "HIGH"

    elif risk_score >= 40:
        severity = "MEDIUM"

    else:
        severity = "LOW"

    # =================================================
    # RESULTS
    # =================================================

    st.markdown("---")

    if prediction == 1:
        st.error("🚨 Suspicious Transaction Detected")
    else:
        st.success("✅ Legitimate Transaction")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("AML Risk Score", f"{risk_score:.2f}%")

    with col2:
        st.metric(
            "Prediction",
            "Suspicious Transaction" if prediction == 1 else "Legitimate"
        )

    with col3:
        st.metric("AML Severity Level", severity)

    # =================================================
    # TYPOLOGY
    # =================================================

    st.subheader("Detected AML Typology")

    st.warning(typology)

    # =================================================
    # CUSTOMER RISK
    # =================================================

    if customer_risk_score >= 75:
        customer_risk = "HIGH RISK"
    elif customer_risk_score >= 40:
        customer_risk = "MEDIUM RISK"
    else:
        customer_risk = "LOW RISK"

    st.subheader("Customer Risk")

    st.info(customer_risk)

    # =================================================
    # RBI/FATF FLAGS
    # =================================================

    st.subheader("RBI/FATF Compliance Flags")

    if international_transfer == 1:
        st.write("✔ Cross-border monitoring")

    if high_risk_country == 1:
        st.write("✔ High-risk geography detected")

    if pep_flag == 1:
        st.write("✔ Politically Exposed Person (PEP)")

    if sanction_flag == 1:
        st.write("✔ Sanctions screening alert")

    if prediction == 1:
        st.write("✔ Enhanced Due Diligence triggered")
        st.write("✔ STR review required")

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

    # =================================================
    # STR RECOMMENDATION
    # =================================================

    st.subheader("STR Recommendation")

    if prediction == 1:

        st.error(
            "Transaction should be reviewed for STR filing consideration."
        )

    else:

        st.success(
            "No STR recommendation required."
        )

    # =================================================
    # AML EXPLANATION
    # =================================================

    st.subheader("AML Alert Explanation")

    if prediction == 1:

        explanation = []

        if international_transfer == 1:
            explanation.append("Cross-border transaction pattern detected.")

        if structuring_indicator == 1:
            explanation.append("Possible structuring/smurfing behavior.")

        if rapid_movement_funds == 1:
            explanation.append("Rapid movement of funds observed.")

        if shell_company_flag == 1:
            explanation.append("Shell company indicators identified.")

        if large_cash_deposit == 1:
            explanation.append("Large cash deposit anomaly detected.")

        if len(explanation) == 0:
            explanation.append("Behavioral anomaly detected by AI model.")

        for exp in explanation:
            st.write("•", exp)

    else:

        st.write("No major AML anomalies identified.")

    # =================================================
    # TRANSACTION SUMMARY
    # =================================================

    st.subheader("Transaction Summary")

    st.write(f"Amount: {amount}")

    st.write(
        f"Payment Type: {'Cross-border' if international_transfer == 1 else 'Domestic'}"
    )

    st.write(f"Sender Country: {sender_country}")

    st.write(f"Receiver Country: {receiver_country}")
