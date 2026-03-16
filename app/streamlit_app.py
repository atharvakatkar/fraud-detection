import streamlit as st
import requests

# PAGE CONFIG
st.set_page_config(page_title="Fraud Risk Analyser", page_icon="🔍", layout="centered")

# HEADER
st.title("🔍 Fraud Risk Analyser")
st.markdown(
    "**Internal Analyst Tool** — Enter transaction signal values from the payment system to generate an instant fraud risk assessment."
)
st.divider()

# API URL
API_URL = "https://fraud-detection-api-tg28.onrender.com/predict"

# CONTEXT BOX
st.info(
    "This tool is used by fraud analysts to assess flagged transactions. Enter the signal values from the transaction record below."
)

st.subheader("Transaction Signals")

col1, col2 = st.columns(2)

with col1:
    transaction_amt = st.number_input(
        "Transaction Amount ($)",
        min_value=0.0,
        max_value=50000.0,
        value=150.0,
        step=10.0,
        help="The dollar value of the transaction",
    )
    card3 = st.number_input(
        "Card Network Code (card3)",
        min_value=100,
        max_value=200,
        value=150,
        help="Encoded card network identifier from payment system",
    )
    v57 = st.number_input(
        "Behavioural Signal V57",
        min_value=0.0,
        max_value=10.0,
        value=0.5,
        help="Top predictive behavioural feature — higher values indicate unusual activity",
    )

with col2:
    product_cd = st.selectbox(
        "Product Type",
        options=[0, 1, 2, 3, 4],
        format_func=lambda x: [
            "W — Direct",
            "H — Home",
            "C — Card",
            "S — Service",
            "R — Recurring",
        ][x],
        help="Product category of the transaction",
    )
    c12 = st.number_input(
        "Transaction Frequency Signal (C12)",
        min_value=0.0,
        max_value=100.0,
        value=1.0,
        help="Count-based signal tracking transaction frequency patterns",
    )
    v30 = st.number_input(
        "Behavioural Signal V30",
        min_value=0.0,
        max_value=10.0,
        value=0.5,
        help="Third most predictive behavioural feature from model analysis",
    )

st.divider()

# PREDICT BUTTON
if st.button("Run Risk Assessment", type="primary", use_container_width=True):

    payload = {
        "features": {
            "TransactionAmt": transaction_amt,
            "ProductCD": product_cd,
            "card3": card3,
            "V57": v57,
            "C12": c12,
            "V30": v30,
        }
    }

    with st.spinner(
        "Analysing transaction signals... (first request may take up to 60 seconds as the server wakes up)"
    ):
        try:
            response = requests.post(API_URL, json=payload, timeout=60)
            result = response.json()

            st.divider()
            st.subheader("Risk Assessment Result")

            risk_level = result["risk_level"]
            fraud_prob = result["fraud_probability"]
            is_fraud = result["is_fraud"]

            if is_fraud:
                if risk_level == "CRITICAL":
                    st.error("🚨 CRITICAL RISK — Recommend Immediate Block")
                elif risk_level == "HIGH":
                    st.error("🔴 HIGH RISK — Recommend Manual Review")
                else:
                    st.warning("🟡 MEDIUM RISK — Recommend Additional Verification")
            else:
                st.success("✅ LOW RISK — Transaction Clear to Approve")

            col3, col4, col5 = st.columns(3)
            with col3:
                st.metric("Fraud Probability", f"{fraud_prob*100:.1f}%")
            with col4:
                st.metric("Risk Level", risk_level)
            with col5:
                st.metric("Recommendation", "BLOCK" if is_fraud else "APPROVE")

            st.markdown("**Fraud Risk Score:**")
            st.progress(float(fraud_prob))

            # Analyst notes section
            st.subheader("Analyst Notes")
            notes = st.text_area(
                "Add notes for case file (optional)",
                placeholder="Enter any additional observations about this transaction...",
            )

            with st.expander("View Raw API Response"):
                st.json(result)

        except Exception as e:
            st.error(f"API Error: {str(e)}")

st.divider()
st.caption(
    "Model: XGBoost | ROC-AUC: 0.9262 | Dataset: IEEE-CIS Fraud Detection | For Internal Use Only"
)
