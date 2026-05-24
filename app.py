import streamlit as st
import pandas as pd
import uuid
from datetime import datetime

st.set_page_config(page_title="AML Monitoring System v4.4", layout="wide")

st.title("🏦 AML Monitoring System v4.4 (Safe Upgrade)")

# =========================
# SAFE SESSION STATE INIT
# =========================
if "cases" not in st.session_state:
    st.session_state["cases"] = pd.DataFrame(columns=[
        "case_id", "timestamp", "amount",
        "risk_score", "severity", "status",
        "alerts", "sender", "receiver"
    ])

df_cases = st.session_state["cases"]

# =========================
# INPUT SECTION
# =========================
st.markdown("## 📥 Transaction Input")

amount = st.number_input("Transaction Amount", 0.0, 1e7, 50000.0)

sender = st.selectbox("Sender Country", ["India", "UK", "USA"])
receiver = st.selectbox("Receiver Country", ["India", "UK", "USA"])

risk_score_input = st.slider("Customer Risk Score", 1, 100, 35)
velocity = st.slider("Transaction Velocity", 1, 50, 10)

pep = st.selectbox("PEP", [0, 1])
sanction = st.selectbox("Sanction", [0, 1])
structuring = st.selectbox("Structuring", [0, 1])

# =========================
# SIMPLE RULE ENGINE
# =========================
def rule_engine():
    score = 0
    alerts = []

    if amount > 100000:
        score += 25
        alerts.append("High value transaction")

    if structuring == 1:
        score += 25
        alerts.append("Structuring / smurfing detected")

    if sender != receiver:
        score += 10
        alerts.append("Cross-border transaction risk")

    if pep == 1:
        score += 20
        alerts.append("PEP risk detected")

    if sanction == 1:
        score += 40
        alerts.append("Sanction list match")

    return min(score, 100), alerts


# =========================
# SIMPLE ML SCORE SIMULATION
# =========================
def ml_score():
    return min(100,
        risk_score_input * 0.35 +
        velocity * 1.2 +
        structuring * 25 +
        pep * 20 +
        sanction * 40
    )


# =========================
# ANALYSIS BUTTON
# =========================
if st.button("🔍 Analyse Transaction"):

    rule_score, alerts = rule_engine()
    ml_score_val = ml_score()

    final_score = (rule_score + ml_score_val) / 2

    # severity logic
    if final_score >= 80:
        severity = "🔴 CRITICAL"
    elif final_score >= 60:
        severity = "🟠 HIGH"
    elif final_score >= 40:
        severity = "🟡 MEDIUM"
    else:
        severity = "🟢 LOW"

    # =========================
    # OUTPUT UI (IMPROVED)
    # =========================
    st.markdown("## 📊 Result")

    st.metric("AML Risk Score", round(final_score, 2))
    st.progress(int(final_score))

    st.write("### Severity:", severity)

    st.markdown("## 🚨 Alerts")
    if alerts:
        for a in alerts:
            st.warning("⚠️ " + a)
    else:
        st.success("No suspicious patterns detected")

    # =========================
    # CASE CREATION (SAFE)
    # =========================
    case_id = str(uuid.uuid4())[:8]

    new_case = {
        "case_id": case_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "amount": amount,
        "risk_score": round(final_score, 2),
        "severity": severity,
        "status": "OPEN",
        "alerts": ", ".join(alerts) if alerts else "None",
        "sender": sender,
        "receiver": receiver
    }

    st.session_state["cases"] = pd.concat(
        [df_cases, pd.DataFrame([new_case])],
        ignore_index=True
    )

    st.success(f"📂 Case Created: {case_id}")


# =========================
# CASE DASHBOARD
# =========================
st.markdown("---")
st.markdown("## 📂 Case Management Dashboard")

df = st.session_state["cases"]

# safe check
if df.empty:
    st.info("No cases generated yet")
else:

    st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True)

    case_list = df["case_id"].dropna().tolist()

    selected_case = st.selectbox("Select Case ID", case_list, key="case_select_v44")

    new_status = st.selectbox("Update Status", ["OPEN", "UNDER REVIEW", "CLOSED"], key="status_select_v44")

    if st.button("Update Case Status"):

        st.session_state["cases"].loc[
            st.session_state["cases"]["case_id"] == selected_case,
            "status"
        ] = new_status

        st.success(f"Case {selected_case} updated to {new_status}")
