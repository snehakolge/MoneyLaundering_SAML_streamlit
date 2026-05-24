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
# SAFE SESSION INIT
# ===============================
if "cases" not in st.session_state or st.session_state.cases is None:
    st.session_state.cases = []

# ===============================
# INPUT SECTION
# ===============================
st.subheader("Transaction Input")

col1, col2 = st.columns(2)

with col1:
    amount = st.number_input("Transaction Amount", value=50000.0)
    sender_country = st.text_input("Sender Country", "India")
    receiver_country = st.text_input("Receiver Country", "UK")
    customer_risk_score = st.slider("Customer Risk Score", 1, 100, 35)
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
# AML RULE ENGINE
# ===============================
def aml_engine(data):
    score = 0
    alerts = []

    if data["amount"] >= 50000:
        score += 25
        alerts.append("High-value transaction (CTR threshold risk)")

    if data["sender_country"] != data["receiver_country"] or data["international"] == 1:
        score += 20
        alerts.append("Cross-border transaction detected")

    if data["structuring"] == 1:
        score += 25
        alerts.append("Structuring pattern detected")

    if data["pep"] == 1:
        score += 15
        alerts.append("PEP involvement detected")

    if data["sanction"] == 1:
        score += 40
        alerts.append("Sanction list risk detected")

    if data["customer_risk_score"] > 70:
        score += 15
        alerts.append("High customer risk profile")

    if data["velocity"] > 30:
        score += 10
        alerts.append("Unusual transaction velocity")

    if data["cash_intensive"] == 1:
        score += 10
        alerts.append("Cash intensive behavior")

    if data["round_amt"] == 1:
        score += 5
        alerts.append("Round amount pattern detected")

    score = min(score, 100)

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
# ANALYSE BUTTON
# ===============================
if st.button("🔍 Analyse Transaction"):

    input_data = {
        "amount": amount,
        "sender_country": sender_country,
        "receiver_country": receiver_country,
        "customer_risk_score": customer_risk_score,
        "velocity": velocity,
        "international": international,
        "pep": pep,
        "sanction": sanction,
        "structuring": structuring,
        "round_amt": round_amt,
        "cash_intensive": cash_intensive
    }

    score, severity, alerts = aml_engine(input_data)

    # prediction logic
    if score >= 60:
        prediction = "⚠️ Suspicious Transaction"
        customer_risk = "HIGH RISK" if score > 70 else "MEDIUM RISK"
    else:
        prediction = "✅ Normal Transaction"
        customer_risk = "LOW RISK"

    st.subheader("📊 AML Result")

    st.metric("AML Risk Score", f"{score}%")
    st.write("Severity:", severity)
    st.write("Prediction:", prediction)
    st.write("Customer Risk:", customer_risk)

    # alerts
    st.subheader("🚨 Alerts (RBI/FATF Aligned)")

    if alerts:
        for a in alerts:
            st.write("✔", a)
    else:
        st.write("✔ No suspicious patterns detected")

    # recommendation
    st.subheader("📌 Recommendation")

    if score >= 60:
        st.error("STR Filing Recommended (Review Required)")
        st.write("Enhanced Due Diligence required")
    else:
        st.success("No STR required")
        st.write("Continue normal monitoring")

    # case creation
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
# CASE MANAGEMENT (SAFE VERSION)
# ===============================
st.divider()
st.subheader("📂 AML Case Management Dashboard")

cases = st.session_state.get("cases", [])

if cases and len(cases) > 0:

    df = pd.DataFrame(cases)

    if "case_id" in df.columns:

        st.dataframe(df)

        selected_case = st.selectbox("Select Case ID", df["case_id"].tolist())

        new_status = st.selectbox("Update Status", ["OPEN", "UNDER REVIEW", "CLOSED"])

        if st.button("Update Case Status"):

            for c in st.session_state.cases:
                if c.get("case_id") == selected_case:
                    c["status"] = new_status

            st.success("Case updated successfully")

    else:
        st.warning("Case data structure issue detected")

else:
    st.info("No cases created yet. Click 'Analyse Transaction' to generate alerts.")
