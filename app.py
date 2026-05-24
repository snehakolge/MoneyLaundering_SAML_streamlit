import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# ================================
# PAGE CONFIG
# ================================
st.set_page_config(page_title="AML Monitoring System", layout="wide")

st.title("AI-Powered AML Transaction Monitoring System")
st.markdown("RBI/FATF-inspired AML monitoring platform using XGBoost + behavioral analytics")

# ================================
# LOAD MODEL SAFELY
# ================================

MODEL_PATH = "model.pkl"
FEATURE_PATH = "feature_columns.pkl"

model = None
feature_columns = None

if os.path.exists(MODEL_PATH) and os.path.exists(FEATURE_PATH):
    model = joblib.load(MODEL_PATH)
    feature_columns = joblib.load(FEATURE_PATH)
else:
    st.error("❌ Model files missing. Please upload model.pkl and feature_columns.pkl")
    st.stop()

# ================================
# INPUT UI
# ================================

st.header("Transaction Input")

amount = st.number_input("Transaction Amount", value=50000.0)
oldbalanceOrg = st.number_input("Old Balance Origin", value=100000.0)
newbalanceOrig = st.number_input("New Balance Origin", value=50000.0)

customer_risk_score = st.slider("Customer Risk Score", 1, 100, 35)
transaction_velocity = st.slider("Transaction Velocity", 1, 50, 5)

international_transfer = st.selectbox("International Transfer", [0, 1])
high_risk_country = st.selectbox("High Risk Country", [0, 1])
pep_flag = st.selectbox("PEP Flag", [0, 1])
adverse_media_flag = st.selectbox("Adverse Media Flag", [0, 1])
sanction_flag = st.selectbox("Sanction Flag", [0, 1])
shell_company_flag = st.selectbox("Shell Company Flag", [0, 1])

sender_country = st.selectbox("Sender Country", ["India", "UK", "UAE"])
receiver_country = st.selectbox("Receiver Country", ["India", "UK", "UAE"])

# ================================
# CREATE INPUT DATAFRAME
# ================================

input_dict = {
    "amount": amount,
    "oldbalanceOrg": oldbalanceOrg,
    "newbalanceOrig": newbalanceOrig,
    "customer_risk_score": customer_risk_score,
    "transaction_velocity": transaction_velocity,
    "international_transfer": international_transfer,
    "high_risk_country": high_risk_country,
    "pep_flag": pep_flag,
    "adverse_media_flag": adverse_media_flag,
    "sanction_flag": sanction_flag,
    "shell_company_flag": shell_company_flag,
    "sender_country": sender_country,
    "receiver_country": receiver_country
}

input_df = pd.DataFrame([input_dict])

# ================================
# ALIGN FEATURES (CRITICAL FIX)
# ================================

try:
    input_df = input_df.reindex(columns=feature_columns, fill_value=0)
except Exception as e:
    st.error(f"Feature alignment error: {e}")
    st.stop()

# ================================
# PREDICTION
# ================================

if st.button("Analyze Transaction"):

    try:
        prediction = model.predict(input_df)[0]

        risk_score = model.predict_proba(input_df)[0][1] * 100

    except Exception as e:
        st.error(f"Model prediction error: {e}")
        st.stop()

    # ================================
    # AML LOGIC
    # ================================

    if risk_score >= 80:
        severity = "CRITICAL"
    elif risk_score >= 60:
        severity = "HIGH"
    elif risk_score >= 40:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    label = "Suspicious Transaction" if prediction == 1 else "Normal Transaction"

    customer_risk = (
        "HIGH RISK" if customer_risk_score > 70
        else "MEDIUM RISK" if customer_risk_score > 40
        else "LOW RISK"
    )

    aml_typology = "No Suspicious Pattern Detected"
    if sanction_flag:
        aml_typology = "Sanctioned Entity Activity"
    elif structuring_indicator if "structuring_indicator" in input_df.columns else False:
        aml_typology = "Structuring Pattern"

    # ================================
    # OUTPUT UI
    # ================================

    if prediction == 1:
        st.error("🚨 Suspicious Transaction Detected")
    else:
        st.success("✅ Normal Transaction")

    st.subheader("AML Risk Score")
    st.metric("Risk Score", f"{risk_score:.2f}%")
    st.metric("Prediction", label)

    st.subheader("Severity")
    st.write(severity)

    st.subheader("Customer Risk")
    st.write(customer_risk)

    st.subheader("AML Typology")
    st.write(aml_typology)

    st.subheader("Compliance Output")

    if prediction == 1:
        st.write("✔ Enhanced Due Diligence triggered")
        st.write("✔ STR review required")
    else:
        st.write("✔ Standard monitoring applied")

    st.subheader("STR Recommendation")

    if prediction == 1:
        st.warning("STR filing recommended")
    else:
        st.success("No STR required")

    st.subheader("Transaction Summary")
    st.write(input_df)
