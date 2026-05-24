import streamlit as st
import pandas as pd
import joblib

# ==========================================
# LOAD MODEL
# ==========================================

model = joblib.load("xgboost_aml_model.pkl")

label_encoders = joblib.load(
    "label_encoders.pkl"
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AML Monitoring System",
    layout="wide"
)

st.title(
    "AI-Powered AML Transaction Monitoring System"
)

st.markdown(
    "RBI/FATF-inspired AML monitoring platform"
)

st.markdown("---")

# ==========================================
# SIDEBAR INPUTS
# ==========================================

st.sidebar.header("Transaction Details")

amount = st.sidebar.number_input(
    "Transaction Amount",
    min_value=0.0,
    value=5000.0
)

payment_currency = st.sidebar.selectbox(
    "Payment Currency",
    ['UK pounds', 'Euro', 'Dirham']
)

received_currency = st.sidebar.selectbox(
    "Received Currency",
    ['UK pounds', 'Euro', 'Dirham']
)

sender_country = st.sidebar.selectbox(
    "Sender Country",
    ['UK', 'India', 'UAE']
)

receiver_country = st.sidebar.selectbox(
    "Receiver Country",
    ['UK', 'India', 'UAE']
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

# ==========================================
# FEATURE ENGINEERING
# ==========================================

cross_border_flag = int(
    sender_country != receiver_country
)

currency_mismatch = int(
    payment_currency != received_currency
)

large_transaction = int(
    amount > 10000
)

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

currency_risk = {
    'UK pounds': 2,
    'Euro': 1,
    'Dirham': 3
}

payment_risk_score = payment_risk[
    payment_type
]

sender_country_risk = country_risk[
    sender_country
]

receiver_country_risk = country_risk[
    receiver_country
]

currency_risk_score = currency_risk[
    payment_currency
]

# ==========================================
# ENCODING
# ==========================================

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

# ==========================================
# INPUT DATAFRAME
# ==========================================

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
    ],

    'cross_border_flag': [
        cross_border_flag
    ],

    'currency_mismatch': [
        currency_mismatch
    ],

    'large_transaction': [
        large_transaction
    ],

    'payment_risk_score': [
        payment_risk_score
    ],

    'sender_country_risk': [
        sender_country_risk
    ],

    'receiver_country_risk': [
        receiver_country_risk
    ],

    'currency_risk_score': [
        currency_risk_score
    ]
})

# ==========================================
# PREDICTION
# ==========================================

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

    st.subheader("AML Prediction")

    st.metric(
        "Risk Score",
        f"{risk_score}%"
    )

    if prediction == 1:

        st.error(
            "Suspicious Transaction Detected"
        )

    else:

        st.success(
            "Transaction Appears Normal"
        )

    st.subheader(
        "RBI/FATF AML Alerts"
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
            "High-risk geography"
        )

    st.subheader(
        "Transaction Summary"
    )

    st.dataframe(input_data)
