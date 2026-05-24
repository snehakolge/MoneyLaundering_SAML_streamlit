import streamlit as st
import pandas as pd
import uuid

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(page_title="AML Monitoring System", layout="wide")

st.title("🏦 Enterprise AML Monitoring System")
st.markdown("RBI/FATF aligned + Real-time monitoring + Case Management")

# ===============================
# CASE STORAGE (SESSION)
# ===============================
if "cases" not in st.session_state:
    st.session_state.cases = []

# ===============================
# INPUT FORM
# ===============================
st.subheader("Transaction Input")

col1, col2 = st.columns(2)

with col1:
    amount = st.number_input("Transaction Amount", value=50000.0)
    sender_country = st.text_input("Sender Country", "India")
    receiver_country = st.text_input("Receiver Country", "UK")
    risk_score = st.slider("Customer Risk Score", 1, 100, 35)
    velocity = st.slider("Transaction Velocity", 1, 50, 10)

with col2:
    old_origin = st.number_input("Old Balance Origin", value=100000.0)
    new_origin = st.number_input("New Balance Origin", value=50000.0)
    old_dest = st.number_input("Old Balance Destination", value=20000.0)
    new_dest = st.number_input("New Balance Destination", value=70000.0)

# flags
international = st.selectbox("International Transfer", [0, 1])
pep = st.selectbox("PEP Flag", [0, 1])
sanction = st.selectbox("Sanction Flag", [0, 1])
structuring = st.selectbox("Structuring Indicator", [0, 1])
round_amt = st.selectbox("Round Amount Transaction", [0, 1])
cash_intensive = st.selectbox("Cash Intensive Business", [0, 1])

# ===============================
# AML ENGINE (RULE BASED + SCORING)
# ===============================
def aml_engine(data):
    score = 0
    alerts = []

    # High value rule (CTR-style)
    if data["amount"] >= 50000:
        score += 25
        alerts.append("High-value transaction (CTR threshold risk)")

    # International transfer risk
    if data["international"] == 1 or data["sender_country"] != data["receiver_country"]:
        score += 20
        alerts.append("Cross-border transaction detected")

    # Structuring
    if data["structuring"] == 1:
        score += 25
        alerts.append("Structuring pattern detected")

    # PEP / Sanctions
    if data["pep"] == 1:
        score += 15
        alerts.append("PEP involvement detected")

    if data["sanction"] == 1:
        score += 40
        alerts.append("Sanction list match risk")

    # Risk score contribution
    if data["risk_score"] > 70:
        score += 15
        alerts.append("High customer risk profile")

    # Velocity anomaly
    if data["velocity"] > 30:
        score += 10
        alerts.append("Unusual transaction velocity")

    # Cash intensive
    if data["cash_intensive"] == 1:
        score += 10
        alerts.append("Cash intensive behavior")

    # Round amount (structuring proxy)
    if data["round_amt"] == 1:
        score += 5
        alerts.append("Round amount pattern detected")

    # Normalize
    score = min(score, 100)

    # Severity
    if score >= 80:
        severity = "CRITICAL"
    elif score >= 60:
        severity = "HIGH"
    elif score >= 40:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return score, severity, alerts


# ===============================
# ANALYSE BUTTON (FIXED)
# ===============================
if st.button("🔍 Analyse Transaction"):

    input_data = {
        "amount": amount,
        "sender_country": sender_country,
        "receiver_country": receiver_country,
        "risk_score": risk_score,
        "velocity": velocity,
        "international": international,
        "pep": pep,
        "sanction": sanction,
        "structuring": structuring,
        "round_amt": round_amt,
        "cash_intensive": cash_intensive
    }

    score, severity, alerts = aml_engine(input_data)

    # prediction label
    if severity in ["CRITICAL", "HIGH", "MEDIUM"]:
        prediction = "⚠️ Suspicious Transaction"
        customer_risk = "HIGH RISK" if score > 70 else "MEDIUM RISK"
    else:
        prediction = "✅ Normal Transaction"
        customer_risk = "LOW RISK"

    # ===============================
    # OUTPUT UI
    # ===============================
    st.subheader("📊 AML Result")

    st.metric("AML Risk Score", f"{score}%")
    st.write("Severity:", severity)
    st.write("Prediction:", prediction)
    st.write("Customer Risk:", customer_risk)

    # Alerts
    st.subheader("🚨 Alerts (RBI/FATF aligned)")
    if alerts:
        for a in alerts:
            st.write("✔", a)
    else:
        st.write("✔ No suspicious patterns detected")

    # Recommendation
    st.subheader("📌 Recommendation")

    if score >= 60:
        st.error("STR Filing Recommended (Review Required)")
        st.write("Enhanced Due Diligence required")
    else:
        st.success("No STR required")
        st.write("Continue normal monitoring")

    # Case creation
    case_id = str(uuid.uuid4())[:8]

    st.session_state.cases.append({
        "case_id": case_id,
        "score": score,
        "severity": severity,
        "status": "OPEN"
    })

    st.subheader("📂 Case Created")
    st.write("Case ID:", case_id)

# ===============================
# CASE MANAGEMENT DASHBOARD
# ===============================
st.divider()
st.subheader("📂 AML Case Management Dashboard")

if st.session_state.cases:
    df = pd.DataFrame(st.session_state.cases)
    st.dataframe(df)

    selected_case = st.selectbox("Select Case ID", df["case_id"])

    new_status = st.selectbox("Update Status", ["OPEN", "UNDER REVIEW", "CLOSED"])

    if st.button("Update Case Status"):
        for c in st.session_state.cases:
            if c["case_id"] == selected_case:
                c["status"] = new_status
        st.success("Case updated successfully")

else:
    st.info("No cases created yet")
