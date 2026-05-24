import streamlit as st

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI AML Monitoring System",
    layout="wide"
)

st.title("AI-Powered AML Transaction Monitoring System")
st.caption("RBI/FATF-inspired AML monitoring platform using behavioral analytics")

# =========================
# INPUT SECTION
# =========================
st.header("Transaction Details")

amount = st.number_input("Transaction Amount", value=50000.0)

old_bal_orig = st.number_input("Old Balance Origin", value=100000.0)
new_bal_orig = st.number_input("New Balance Origin", value=50000.0)

customer_risk_score = st.slider("Customer Risk Score", 1, 100, 35)
velocity = st.slider("Transaction Velocity", 1, 50, 10)

intl_transfer = st.selectbox("International Transfer", [0, 1])
high_risk_country = st.selectbox("High Risk Country", [0, 1])
pep_flag = st.selectbox("PEP Flag", [0, 1])
adverse_media = st.selectbox("Adverse Media Flag", [0, 1])
sanction_flag = st.selectbox("Sanction Flag", [0, 1])
shell_company = st.selectbox("Shell Company Flag", [0, 1])

sender_country = st.selectbox("Sender Country", ["India", "UK", "USA", "UAE"])
receiver_country = st.selectbox("Receiver Country", ["India", "UK", "USA", "UAE"])

old_bal_dest = st.number_input("Old Balance Destination", value=20000.0)
new_bal_dest = st.number_input("New Balance Destination", value=70000.0)

cash_business = st.selectbox("Cash Intensive Business", [0, 1])
round_txn = st.selectbox("Round Amount Transaction", [0, 1])
structuring = st.selectbox("Structuring Indicator", [0, 1])
multi_accounts = st.selectbox("Multiple Accounts", [0, 1])
rapid_movement = st.selectbox("Rapid Movement of Funds", [0, 1])
inactive_account = st.selectbox("Inactive Account", [0, 1])

# =========================
# ANALYSIS BUTTON
# =========================
st.markdown("---")
st.subheader("AML Analysis")

if st.button("🚨 Analyze Transaction", type="primary"):

    # =========================
    # AML RISK SCORING ENGINE
    # =========================
    risk_score = 0

    risk_score += amount / 10000
    risk_score += customer_risk_score / 10
    risk_score += velocity * 2

    risk_score += intl_transfer * 15
    risk_score += high_risk_country * 20
    risk_score += pep_flag * 15
    risk_score += sanction_flag * 25
    risk_score += adverse_media * 10
    risk_score += shell_company * 15

    risk_score += structuring * 20
    risk_score += cash_business * 10
    risk_score += round_txn * 5
    risk_score += multi_accounts * 10
    risk_score += rapid_movement * 10
    risk_score += inactive_account * 10

    risk_score = min(100, risk_score)

    # =========================
    # CLASSIFICATION LOGIC
    # =========================
    if risk_score >= 80:
        label = "Suspicious Transaction Detected"
        severity = "CRITICAL"
        risk_level = "HIGH RISK"

    elif risk_score >= 60:
        label = "Suspicious Transaction"
        severity = "HIGH"
        risk_level = "HIGH RISK"

    elif risk_score >= 40:
        label = "Suspicious Pattern"
        severity = "MEDIUM"
        risk_level = "MEDIUM RISK"

    else:
        label = "Normal Transaction"
        severity = "LOW"
        risk_level = "LOW RISK"

    # =========================
    # OUTPUT DASHBOARD
    # =========================
    st.markdown("## 📊 Result")

    if risk_score >= 60:
        st.error(f"🚨 {label}")
    else:
        st.success(f"✅ {label}")

    st.metric("AML Risk Score", f"{risk_score:.2f}%")
    st.metric("Severity Level", severity)
    st.metric("Customer Risk", risk_level)

    st.markdown("## Compliance Summary")

    if risk_score >= 60:
        st.write("✔ Enhanced Due Diligence triggered")
        st.write("✔ STR filing required")
        st.write("✔ Compliance review needed")
    else:
        st.write("✔ Standard monitoring applied")
        st.write("✔ No STR required")

    st.markdown("## Recommended Actions")

    if risk_score >= 60:
        st.write("• Source of funds verification")
        st.write("• Enhanced transaction monitoring")
        st.write("• File STR if required")
    else:
        st.write("• Continue normal monitoring")

    st.markdown("## Transaction Summary")

    st.write(f"Amount: {amount}")
    st.write(f"Sender Country: {sender_country}")
    st.write(f"Receiver Country: {receiver_country}")
