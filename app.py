import streamlit as st
import pandas as pd
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
st.write("RBI/FATF-inspired AML monitoring platform using XGBoost and behavioral analytics.")

# =====================================================
# INPUT SECTION
# =====================================================

st.header("Transaction Details")

col1, col2 = st.columns(2)

with col1:

    amount = st.number_input(
        "Transaction Amount",
        value=50000.0
    )

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
        80
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
        ["India", "UK", "UAE", "Pakistan", "USA"]
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

    frequent_small_txns = st.selectbox(
        "Frequent Small Transactions",
        [0, 1]
    )

    suspicious_narration = st.selectbox(
        "Suspicious Narration",
        [0, 1]
    )

    receiver_country = st.selectbox(
        "Receiver Country",
        ["India", "UK", "UAE", "Pakistan", "USA"]
    )

# =====================================================
# COUNTRY ENCODING
# =====================================================

country_mapping = {
    "India": 0,
    "UK": 1,
    "UAE": 2,
    "Pakistan": 3,
    "USA": 4
}

sender_country_encoded = country_mapping[sender_country]
receiver_country_encoded = country_mapping[receiver_country]

# =====================================================
# INPUT DATA
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
    "frequent_small_txns": [frequent_small_txns],
    "suspicious_narration": [suspicious_narration],

    "sender_country": [sender_country_encoded],
    "receiver_country": [receiver_country_encoded]

})

# =====================================================
# ENSURE 29 FEATURES
# =====================================================

required_columns = [

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
    "frequent_small_txns",
    "suspicious_narration",

    "sender_country",
    "receiver_country",

    "feature_25",
    "feature_26",
    "feature_27",
    "feature_28",
    "feature_29"
]

for col in required_columns:
    if col not in input_data.columns:
        input_data[col] = 0

input_data = input_data[required_columns]

# =====================================================
# PREDICTION
# =====================================================

if st.button("Analyze Transaction"):

    # =====================================================
    # MODEL SCORE
    # =====================================================

    model_probability = model.predict_proba(input_data)[0][1] * 100

    # =====================================================
    # BUSINESS RULE CALIBRATION
    # =====================================================

    risk_flags = (

        international_transfer +
        high_risk_country +
        pep_flag +
        adverse_media_flag +
        sanction_flag +
        shell_company_flag +
        cash_intensive_business +
        round_amount_transaction +
        structuring_indicator +
        multiple_accounts +
        rapid_movement_funds +
        inactive_account +
        large_cash_deposit +
        frequent_small_txns +
        suspicious_narration

    )

    probability = (model_probability * 0.4) + (risk_flags * 6)

    probability = max(1, min(probability, 99))

    prediction = 1 if probability >= 65 else 0

    # =====================================================
    # ALERT DISPLAY
    # =====================================================

    if prediction == 1:

        st.error("🚨 Suspicious Transaction Detected")

        severity = "CRITICAL"

        aml_typology = "Behavioral Anomaly"

    else:

        st.success("✅ Normal Transaction")

        severity = "LOW"

        aml_typology = "Normal Activity"

    # =====================================================
    # RESULTS
    # =====================================================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "AML Risk Score",
            f"{probability:.2f}%"
        )

    with col2:
        st.metric(
            "Prediction",
            "Suspicious Transaction" if prediction == 1 else "Normal"
        )

    with col3:
        st.metric(
            "AML Severity Level",
            severity
        )

    # =====================================================
    # TYPOLOGY
    # =====================================================

    st.subheader("Detected AML Typology")
    st.info(aml_typology)

    # =====================================================
    # CUSTOMER RISK
    # =====================================================

    if customer_risk_score >= 75:
        customer_risk = "HIGH RISK"

    elif customer_risk_score >= 40:
        customer_risk = "MEDIUM RISK"

    else:
        customer_risk = "LOW RISK"

    st.subheader("Customer Risk")
    st.warning(customer_risk)

    # =====================================================
    # RBI / FATF FLAGS
    # =====================================================

    st.subheader("RBI/FATF Compliance Flags")

    if international_transfer == 1:
        st.write("✔ Cross-border monitoring")

    if high_risk_country == 1:
        st.write("✔ FATF high-risk jurisdiction detected")

    if pep_flag == 1:
        st.write("✔ Politically Exposed Person monitoring")

    if sanction_flag == 1:
        st.write("✔ Sanction screening alert")

    if structuring_indicator == 1:
        st.write("✔ Structuring / smurfing behavior detected")

    if prediction == 1:

        st.write("✔ Enhanced Due Diligence triggered")
        st.write("✔ STR review required")

    else:

        st.write("✔ Standard monitoring applied")

    # =====================================================
    # RECOMMENDED ACTIONS
    # =====================================================

    st.subheader("Recommended Actions")

    st.write("• Source of funds verification")
    st.write("• Enhanced transaction monitoring")
    st.write("• Additional KYC verification")
    st.write("• Compliance review")

    # =====================================================
    # STR RECOMMENDATION
    # =====================================================

    st.subheader("STR Recommendation")

    if prediction == 1:

        st.error(
            "Transaction should be reviewed for STR filing consideration."
        )

    else:

        st.success("No STR filing required.")

    # =====================================================
    # EXPLANATION
    # =====================================================

    st.subheader("AML Alert Explanation")

    if prediction == 1:

        st.warning(
            "Behavioral anomaly detected by AI model."
        )

    else:

        st.success(
            "No major AML anomalies identified."
        )

    # =====================================================
    # TRANSACTION SUMMARY
    # =====================================================

    st.subheader("Transaction Summary")

    st.write(f"Amount: {amount}")

    if international_transfer == 1:
        st.write("Payment Type: Cross-border")
    else:
        st.write("Payment Type: Domestic")

    st.write(f"Sender Country: {sender_country}")
    st.write(f"Receiver Country: {receiver_country}")
