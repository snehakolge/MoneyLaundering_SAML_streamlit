import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI-Powered AML Monitoring System",
    layout="wide"
)

# ==========================================
# LOAD MODEL
# ==========================================

model = joblib.load("xgboost_aml_model.pkl")
feature_columns = joblib.load("feature_columns.pkl")

# ==========================================
# TITLE
# ==========================================

st.title("AI-Powered AML Transaction Monitoring System")

st.markdown("""
RBI/FATF-inspired AML monitoring platform using XGBoost and behavioral analytics.
""")

# ==========================================
# USER INPUTS
# ==========================================

st.sidebar.header("Transaction Details")

amount = st.sidebar.number_input(
    "Transaction Amount",
    min_value=0.0,
    value=50000.0
)

payment_type = st.sidebar.selectbox(
    "Payment Type",
    [
        "Cross-border",
        "Cash Deposit",
        "Cheque",
        "ACH",
        "Wire Transfer"
    ]
)

payment_currency = st.sidebar.selectbox(
    "Payment Currency",
    [
        "UK pounds",
        "US Dollar",
        "Euro",
        "Dirham",
        "Indian Rupee"
    ]
)

sender_country = st.sidebar.selectbox(
    "Sender Country",
    [
        "UK",
        "India",
        "USA",
        "UAE"
    ]
)

receiver_country = st.sidebar.selectbox(
    "Receiver Country",
    [
        "UK",
        "India",
        "USA",
        "UAE",
        "Panama",
        "Cayman Islands"
    ]
)

# ==========================================
# FEATURE ENGINEERING
# ==========================================

is_cross_border = 1 if sender_country != receiver_country else 0

high_risk_country = 1 if receiver_country in [
    "UAE",
    "Panama",
    "Cayman Islands"
] else 0

high_value_transaction = 1 if amount > 1000000 else 0

cash_transaction = 1 if payment_type == "Cash Deposit" else 0

structuring_risk = 1 if (
    payment_type == "Cash Deposit"
    and amount > 200000
) else 0

layering_risk = 1 if (
    payment_type == "Cross-border"
    and amount > 500000
) else 0

offshore_risk = 1 if receiver_country in [
    "Panama",
    "Cayman Islands"
] else 0

# ==========================================
# CREATE INPUT DATAFRAME
# ==========================================

input_data = pd.DataFrame(
    np.zeros((1, len(feature_columns))),
    columns=feature_columns
)

# ==========================================
# MAP FEATURES
# ==========================================

feature_map = {
    "Amount": amount,
    "is_cross_border": is_cross_border,
    "high_risk_country": high_risk_country,
    "high_value_transaction": high_value_transaction,
    "cash_transaction": cash_transaction,
    "structuring_risk": structuring_risk,
    "layering_risk": layering_risk,
    "offshore_risk": offshore_risk
}

for col, value in feature_map.items():
    if col in input_data.columns:
        input_data[col] = value

# ==========================================
# PREDICTION SECTION
# ==========================================

if st.button("Analyze Transaction"):

    prediction = model.predict(input_data)[0]

    probability = model.predict_proba(input_data)[0][1]

    risk_score = round(probability * 100, 2)

    # ==========================================
    # TRANSACTION LABEL
    # ==========================================

    if prediction == 1:
        prediction_label = "Suspicious Transaction"
        st.error("🚨 Suspicious Transaction Detected")
    else:
        prediction_label = "Normal Transaction"
        st.success("✅ Normal Transaction")

    # ==========================================
    # RISK LEVEL
    # ==========================================

    if risk_score > 85:
        risk_level = "CRITICAL"
    elif risk_score > 60:
        risk_level = "HIGH"
    elif risk_score > 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    # ==========================================
    # AML TYPOLOGY
    # ==========================================

    typology = "Normal Activity"

    if payment_type == "Cross-border" and amount > 500000:
        typology = "Layering / Cross-Border Laundering"

    elif payment_type == "Cash Deposit" and amount > 200000:
        typology = "Structuring / Smurfing"

    elif receiver_country in ["UAE", "Panama", "Cayman Islands"]:
        typology = "Offshore / Shell Activity"

    # ==========================================
    # DISPLAY RESULTS
    # ==========================================

    st.subheader("AML Risk Score")
    st.metric("Risk Score", f"{risk_score}%")

    st.subheader("Prediction")
    st.write(prediction_label)

    st.subheader("AML Severity Level")
    st.warning(risk_level)

    st.subheader("Detected AML Typology")
    st.info(typology)

    # ==========================================
    # CUSTOMER RISK
    # ==========================================

    if risk_score > 75:
        customer_risk = "HIGH RISK"
    elif risk_score > 40:
        customer_risk = "MEDIUM RISK"
    else:
        customer_risk = "LOW RISK"

    st.subheader("Customer Risk")
    st.write(customer_risk)

    # ==========================================
    # RBI/FATF COMPLIANCE FLAGS
    # ==========================================

    st.subheader("RBI/FATF Compliance Flags")

    compliance_flags = []

    if amount > 1000000:
        compliance_flags.append(
            "✔ High-value transaction review"
        )

    if payment_type == "Cross-border":
        compliance_flags.append(
            "✔ Cross-border monitoring"
        )

    if risk_score > 70:
        compliance_flags.append(
            "✔ Enhanced Due Diligence triggered"
        )

    if prediction == 1:
        compliance_flags.append(
            "✔ STR review required"
        )

    if receiver_country in [
        "UAE",
        "Panama",
        "Cayman Islands"
    ]:
        compliance_flags.append(
            "✔ FATF high-risk jurisdiction screening"
        )

    for flag in compliance_flags:
        st.write(flag)

    # ==========================================
    # RECOMMENDED ACTIONS
    # ==========================================

    st.subheader("Recommended Actions")

    recommendations = [
        "Source of funds verification",
        "Enhanced transaction monitoring",
        "Additional KYC verification",
        "Compliance review"
    ]

    for action in recommendations:
        st.write(f"- {action}")

    # ==========================================
    # STR RECOMMENDATION
    # ==========================================

    st.subheader("STR Recommendation")

    if prediction == 1:
        st.error(
            "Transaction should be reviewed for STR filing consideration."
        )
    else:
        st.success(
            "No STR filing recommendation."
        )

    # ==========================================
    # AI EXPLANATION
    # ==========================================

    st.subheader("AML Alert Explanation")

    if prediction == 1:
        st.warning(
            "Behavioral anomaly detected by AI model."
        )
    else:
        st.success(
            "No major AML anomalies identified."
        )

    # ==========================================
    # TRANSACTION SUMMARY
    # ==========================================

    st.subheader("Transaction Summary")

    st.write(f"Amount: {amount}")
    st.write(f"Payment Type: {payment_type}")
    st.write(f"Sender Country: {sender_country}")
    st.write(f"Receiver Country: {receiver_country}")
