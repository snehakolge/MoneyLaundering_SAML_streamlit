import streamlit as st
import pandas as pd
import joblib

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI AML Monitoring System",
    layout="wide"
)

st.title("AI-Powered AML Transaction Monitoring System")
st.write("RBI/FATF-inspired AML monitoring platform using XGBoost and behavioral analytics.")

# ==========================================
# LOAD MODEL
# ==========================================

model = joblib.load("xgboost_aml_model.pkl")

# ==========================================
# INPUTS
# ==========================================

st.header("Transaction Details")

col1, col2 = st.columns(2)

with col1:

    amount = st.number_input("Transaction Amount", value=50000.0)

    oldbalanceOrg = st.number_input("Old Balance Origin", value=100000.0)

    newbalanceOrig = st.number_input("New Balance Origin", value=50000.0)

    customer_risk_score = st.slider("Customer Risk Score", 1, 100, 80)

    transaction_velocity = st.slider("Transaction Velocity", 1, 50, 10)

    international_transfer = st.selectbox("International Transfer", [0,1])

    high_risk_country = st.selectbox("High Risk Country", [0,1])

    pep_flag = st.selectbox("PEP Flag", [0,1])

    adverse_media_flag = st.selectbox("Adverse Media Flag", [0,1])

    sanction_flag = st.selectbox("Sanction Flag", [0,1])

    shell_company_flag = st.selectbox("Shell Company Flag", [0,1])

    sender_country = st.selectbox(
        "Sender Country",
        ["India","UK","UAE","Russia","Pakistan"]
    )

with col2:

    oldbalanceDest = st.number_input("Old Balance Destination", value=20000.0)

    newbalanceDest = st.number_input("New Balance Destination", value=70000.0)

    cash_intensive_business = st.selectbox("Cash Intensive Business", [0,1])

    round_amount_transaction = st.selectbox("Round Amount Transaction", [0,1])

    structuring_indicator = st.selectbox("Structuring Indicator", [0,1])

    multiple_accounts = st.selectbox("Multiple Accounts", [0,1])

    rapid_movement_funds = st.selectbox("Rapid Movement of Funds", [0,1])

    inactive_account = st.selectbox("Inactive Account", [0,1])

    large_cash_deposit = st.selectbox("Large Cash Deposit", [0,1])

    frequent_small_transactions = st.selectbox("Frequent Small Transactions", [0,1])

    suspicious_narration = st.selectbox("Suspicious Narration", [0,1])

    receiver_country = st.selectbox(
        "Receiver Country",
        ["India","UK","UAE","Russia","Pakistan"]
    )

# ==========================================
# PREDICTION
# ==========================================

if st.button("Analyze Transaction"):

    # ==========================================
    # CREATE INPUT DATAFRAME
    # ==========================================

    input_data = pd.DataFrame({

        # ORIGINAL FEATURES
        "Amount":[amount],
        "oldbalanceOrg":[oldbalanceOrg],
        "newbalanceOrig":[newbalanceOrig],
        "oldbalanceDest":[oldbalanceDest],
        "newbalanceDest":[newbalanceDest],

        "customer_risk_score":[customer_risk_score],
        "transaction_velocity":[transaction_velocity],

        "international_transfer":[international_transfer],
        "high_risk_country":[high_risk_country],
        "pep_flag":[pep_flag],
        "adverse_media_flag":[adverse_media_flag],
        "sanction_flag":[sanction_flag],
        "shell_company_flag":[shell_company_flag],

        "cash_intensive_business":[cash_intensive_business],
        "round_amount_transaction":[round_amount_transaction],
        "structuring_indicator":[structuring_indicator],
        "multiple_accounts":[multiple_accounts],
        "rapid_movement_funds":[rapid_movement_funds],
        "inactive_account":[inactive_account],
        "large_cash_deposit":[large_cash_deposit],
        "frequent_small_transactions":[frequent_small_transactions],
        "suspicious_narration":[suspicious_narration],

        # ADDITIONAL FEATURES
        "cross_border_flag":[1 if sender_country != receiver_country else 0],

        "large_transaction":[1 if amount > 100000 else 0],

        "night_transaction":[0],

        "currency_mismatch":[0],

        "payment_risk_score":[80 if international_transfer else 20],

        "currency_risk_score":[70 if high_risk_country else 10],

        "sender_transaction_count":[transaction_velocity]

    })

    # ==========================================
    # ADD MISSING FEATURES
    # ==========================================

    required_features = [
        'Amount',
        'oldbalanceOrg',
        'newbalanceOrig',
        'oldbalanceDest',
        'newbalanceDest',
        'customer_risk_score',
        'transaction_velocity',
        'international_transfer',
        'high_risk_country',
        'pep_flag',
        'adverse_media_flag',
        'sanction_flag',
        'shell_company_flag',
        'cash_intensive_business',
        'round_amount_transaction',
        'structuring_indicator',
        'multiple_accounts',
        'rapid_movement_funds',
        'inactive_account',
        'large_cash_deposit',
        'frequent_small_transactions',
        'suspicious_narration',
        'cross_border_flag',
        'large_transaction',
        'night_transaction',
        'currency_mismatch',
        'payment_risk_score',
        'currency_risk_score',
        'sender_transaction_count'
    ]

    for feature in required_features:

        if feature not in input_data.columns:
            input_data[feature] = 0

    input_data = input_data[required_features]

    # ==========================================
    # MODEL PREDICTION
    # ==========================================

    prediction = model.predict(input_data)[0]

    probability = model.predict_proba(input_data)[0][1]

    risk_score = round(probability * 100, 2)

    # ==========================================
    # DECISION
    # ==========================================

    if risk_score >= 75:
        severity = "CRITICAL"
    elif risk_score >= 60:
        severity = "HIGH"
    elif risk_score >= 40:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    if prediction == 1:
        decision = "🚨 Suspicious Transaction Detected"
        decision_color = "red"
        prediction_text = "Suspicious Transaction"
    else:
        decision = "✅ Normal Transaction"
        decision_color = "green"
        prediction_text = "Normal"

    # ==========================================
    # TYPOLOGY
    # ==========================================

    if structuring_indicator == 1:
        typology = "Structuring / Smurfing"

    elif rapid_movement_funds == 1:
        typology = "Layering Activity"

    elif shell_company_flag == 1:
        typology = "Shell Company Activity"

    elif international_transfer == 1:
        typology = "Cross-border Movement"

    else:
        typology = "Normal Activity"

    # ==========================================
    # DISPLAY RESULTS
    # ==========================================

    st.markdown(f"## :{decision_color}[{decision}]")

    st.subheader("AML Risk Score")
    st.metric("Risk Score", f"{risk_score}%")

    st.subheader("Prediction")
    st.write(prediction_text)

    st.subheader("AML Severity Level")
    st.write(severity)

    st.subheader("Detected AML Typology")
    st.write(typology)

    st.subheader("Customer Risk")

    if customer_risk_score >= 70:
        st.error("HIGH RISK")
    elif customer_risk_score >= 40:
        st.warning("MEDIUM RISK")
    else:
        st.success("LOW RISK")

    st.subheader("RBI/FATF Compliance Flags")

    if international_transfer == 1:
        st.write("✔ Cross-border monitoring")

    if risk_score >= 60:
        st.write("✔ Enhanced Due Diligence triggered")
        st.write("✔ STR review required")
    else:
        st.write("✔ Standard monitoring applied")

    st.subheader("Recommended Actions")

    if risk_score >= 60:
        st.write("• Source of funds verification")
        st.write("• Enhanced transaction monitoring")
        st.write("• Additional KYC verification")
        st.write("• Compliance review")
    else:
        st.write("• Continue regular monitoring")

    st.subheader("STR Recommendation")

    if risk_score >= 75:
        st.error("Transaction should be reviewed for STR filing consideration.")
    else:
        st.success("No STR filing required.")

    st.subheader("AML Alert Explanation")

    if prediction == 1:
        st.warning("Behavioral anomaly detected by AI model.")
    else:
        st.success("No major AML anomalies identified.")

    st.subheader("Transaction Summary")

    payment_type = "Cross-border" if international_transfer else "Domestic"

    st.write(f"Amount: {amount}")
    st.write(f"Payment Type: {payment_type}")
    st.write(f"Sender Country: {sender_country}")
    st.write(f"Receiver Country: {receiver_country}")
