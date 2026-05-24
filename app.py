import streamlit as st
import pandas as pd
import joblib

# =====================================================
# LOAD MODEL & LABEL ENCODERS
# =====================================================

model = joblib.load("xgboost_aml_model.pkl")

label_encoders = joblib.load(
    "label_encoders.pkl"
)

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI AML Monitoring System",
    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title(
    "AI-Powered AML Transaction Monitoring System"
)

st.markdown("""
RBI/FATF-inspired AML monitoring platform
using XGBoost and behavioral analytics.
""")

st.markdown("---")

# =====================================================
# SIDEBAR INPUTS
# =====================================================

st.sidebar.header(
    "Transaction Details"
)

amount = st.sidebar.number_input(
    "Transaction Amount",
    min_value=0.0,
    value=5000.0
)

payment_currency = st.sidebar.selectbox(
    "Payment Currency",
    [
        'UK pounds',
        'Euro',
        'Dirham'
    ]
)

received_currency = st.sidebar.selectbox(
    "Received Currency",
    [
        'UK pounds',
        'Euro',
        'Dirham'
    ]
)

sender_country = st.sidebar.selectbox(
    "Sender Country",
    [
        'UK',
        'India',
        'UAE'
    ]
)

receiver_country = st.sidebar.selectbox(
    "Receiver Country",
    [
        'UK',
        'India',
        'UAE'
    ]
)

payment_type = st.sidebar.selectbox(
    "Payment Type",
    [
        'Cash Deposit',
        'Cross-border',
        'Cheque',
        'ACH'
    ]
)

# =====================================================
# BASIC AML FLAGS
# =====================================================

cross_border_flag = int(
    sender_country != receiver_country
)

currency_mismatch = int(
    payment_currency != received_currency
)

large_transaction = int(
    amount > 10000
)

# =====================================================
# RISK MAPPING
# =====================================================

payment_risk = {

    'Cash Deposit': 5,

    'Cross-border': 4,

    'Cheque': 1,

    'ACH': 2
}

country_risk = {

    'UK': 1,

    'India': 2,

    'UAE': 4
}

payment_risk_score = payment_risk[
    payment_type
]

sender_country_risk = country_risk[
    sender_country
]

# =====================================================
# LABEL ENCODING
# =====================================================

payment_currency_encoded = label_encoders[
    'Payment_currency'
].transform([payment_currency])[0]

received_currency_encoded = label_encoders[
    'Received_currency'
].transform([received_currency])[0]

sender_country_encoded = label_encoders[
    'Sender_bank_location'
].transform([sender_country])[0]

receiver_country_encoded = label_encoders[
    'Receiver_bank_location'
].transform([receiver_country])[0]

payment_type_encoded = label_encoders[
    'Payment_type'
].transform([payment_type])[0]

# =====================================================
# MODEL INPUT
# IMPORTANT:
# ONLY TRAINED FEATURES
# =====================================================

input_data = pd.DataFrame({

    'Amount': [amount],

    'Payment_currency': [
        payment_currency_encoded
    ],

    'Received_currency': [
        received_currency_encoded
    ],

    'Sender_bank_location': [
        sender_country_encoded
    ],

    'Receiver_bank_location': [
        receiver_country_encoded
    ],

    'Payment_type': [
        payment_type_encoded
    ]
})

# =====================================================
# AML ANALYSIS
# =====================================================

if st.button("Analyze Transaction"):

    prediction = model.predict(
        input_data
    )[0]

    probability = model.predict_proba(
        input_data
    )[0][1]

    risk_score = round(
        probability * 100,
        2
    )

    st.markdown("---")

    # =====================================================
    # METRICS
    # =====================================================

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "AML Risk Score",
        f"{risk_score}%"
    )

    col2.metric(
        "Prediction",
        prediction
    )

    # =====================================================
    # CUSTOMER RISK CLASSIFICATION
    # =====================================================

    if sender_country_risk >= 4 or risk_score > 80:

        customer_risk = "HIGH RISK"

    elif risk_score > 50:

        customer_risk = "MEDIUM RISK"

    else:

        customer_risk = "LOW RISK"

    col3.metric(
        "Customer Risk",
        customer_risk
    )

    # =====================================================
    # AML RESULT
    # =====================================================

    st.subheader(
        "AML Decision"
    )

    if prediction == 1:

        st.error(
            "Suspicious Transaction Detected"
        )

    else:

        st.success(
            "Transaction Appears Normal"
        )

    # =====================================================
    # RBI/FATF ALERTS
    # =====================================================

    st.subheader(
        "RBI/FATF Monitoring Alerts"
    )

    if large_transaction:

        st.warning(
            "Large transaction detected"
        )

    if cross_border_flag:

        st.warning(
            "Cross-border transaction identified"
        )

    if currency_mismatch:

        st.warning(
            "Currency mismatch identified"
        )

    if sender_country_risk >= 4:

        st.warning(
            "High-risk geography identified"
        )

    # =====================================================
    # EDD SECTION
    # =====================================================

    st.subheader(
        "Enhanced Due Diligence"
    )

    if customer_risk == "HIGH RISK":

        st.error("""
Enhanced Due Diligence Required

Recommended Actions:
- Source of funds verification
- Enhanced transaction monitoring
- Additional KYC verification
- Compliance review
""")

    elif customer_risk == "MEDIUM RISK":

        st.warning(
            "Periodic enhanced monitoring recommended"
        )

    else:

        st.success(
            "Standard due diligence sufficient"
        )

    # =====================================================
    # STR RECOMMENDATION
    # =====================================================

    st.subheader(
        "STR Recommendation"
    )

    if risk_score > 85:

        st.error("""
Transaction should be reviewed
for STR filing consideration.
""")

    else:

        st.success(
            "No STR escalation recommended"
        )

    # =====================================================
    # EXPLAINABLE AI
    # =====================================================

    st.subheader(
        "AML Alert Explanation"
    )

    reasons = []

    if cross_border_flag:

        reasons.append(
            "Cross-border transaction"
        )

    if large_transaction:

        reasons.append(
            "Large transaction amount"
        )

    if currency_mismatch:

        reasons.append(
            "Currency mismatch"
        )

    if sender_country_risk >= 4:

        reasons.append(
            "High-risk geography"
        )

    if len(reasons) == 0:

        st.write(
            "No major AML anomalies identified."
        )

    else:

        for reason in reasons:

            st.write(f"• {reason}")

    # =====================================================
    # TRANSACTION SUMMARY
    # =====================================================

    st.subheader(
        "Transaction Summary"
    )

    st.dataframe(input_data)
