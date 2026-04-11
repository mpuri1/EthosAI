import streamlit as st
import os
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

from rag_pipeline import initialize_vector_store
from multi_agent import run_multi_agent_system
from analytics import ComplianceAnalytics, ComplianceForecaster

# Load variables from .env if present
load_dotenv()

st.set_page_config(page_title="EthosAI | Governance Reporter", layout="wide")
st.title("EthosAI: Autonomous Governance & Research Suite")

st.markdown("""
Managed AI governance with real-time risk modeling and predictive maturity forecasting. 
Leveraging multi-agent orchestration to automate legal research and policy auditing.
""")

# Initialize analytics
analytics = ComplianceAnalytics()
forecaster = ComplianceForecaster()

st.sidebar.header("System Settings")

if st.sidebar.button("Rebuild Vector DB"):
    with st.spinner("Rebuilding Vector DB..."):
        initialize_vector_store()
    st.sidebar.success("DB Ready!")

api_key = st.sidebar.text_input("OpenAI API Key (or Use Env)", type="password")
serper_key = st.sidebar.text_input("Serper API Key", type="password")

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
if serper_key:
    os.environ["SERPER_API_KEY"] = serper_key

# --- Predictive Insights Section ---
st.sidebar.markdown("---")
st.sidebar.subheader("📈 Predictive Performance")
# Use simulation data for baseline visualization
hist_data = forecaster.simulate_historical_data()
forecast = forecaster.predict_maturity_drift(hist_data)

st.sidebar.metric("Foreknowledge Risk", f"{forecast['forecast_next_score']}", delta=forecast['drift_rate_per_audit'], delta_color="inverse")
st.sidebar.info(f"Trend: **{forecast['trend']}**")

# Main Input
project_desc = st.text_area(
    "Describe the AI Project to evaluate for compliance:", 
    "Example: A generative AI system that automatically rewrites internal engineering documentation based on Slack messages."
)

col1, col2 = st.columns([2, 1])

with col1:
    if st.button("Generate Governance Report"):
        if not os.environ.get("OPENAI_API_KEY"):
            st.error("Please provide an OpenAI API Key to run the CrewAI agents.")
        else:
            with st.spinner("Agents are researching and writing the report..."):
                try:
                    result = run_multi_agent_system(project_desc)
                    st.subheader("Final Governance Report")
                    
                    # Redirected path to prn_docs/
                    report_path = "prn_docs/final_governance_report.md"
                    if os.path.exists(report_path):
                        with open(report_path, "r") as f:
                            st.markdown(f.read())
                    else:
                        st.write(result)
                        
                except Exception as e:
                    st.error(f"Error during execution: {e}")

with col2:
    st.subheader("Statistical Governance")
    
    # Visualization: Governance Maturity Trend
    df = pd.DataFrame({
        "Audit Session": list(range(len(hist_data))),
        "Risk Score": hist_data
    })
    
    fig = px.line(df, x="Audit Session", y="Risk Score", title="Governance Maturity Trend", markers=True)
    fig.add_scatter(x=[len(hist_data)], y=[forecast['forecast_next_score']], name="Forecast", marker=dict(color='red', size=12))
    
    st.plotly_chart(fig, use_container_width=True)
    
    if forecast['is_risk_alert']:
        st.error("🚨 WARNING: System forecasted to cross critical risk threshold in next audit cycles.")
    
    st.markdown("### Efficiency ROI")
    # Mock some data for first run ROI
    roi = analytics.calculate_research_roi(120, 15000)
    st.metric("Net Savings", f"${roi['net_savings']}")
    st.metric("Efficiency Multiplier", f"{roi['efficiency_multiplier']}x")
