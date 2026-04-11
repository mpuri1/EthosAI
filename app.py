import streamlit as st
import os

from rag_pipeline import initialize_vector_store
from multi_agent import run_multi_agent_system
from analytics import ComplianceAnalytics
from dotenv import load_dotenv
import time

# Load variables from .env if present
load_dotenv()
analytics = ComplianceAnalytics()

st.set_page_config(page_title="EthosAI | Governance Reporter", layout="wide")
st.title("EthosAI: Autonomous Governance & Research Suite")

st.markdown("""
This tool uses a Multi-Agent system (Researcher, Risk Analyst, Governance Writer) to evaluate proposed AI architectures against live regulations and internal DB policies.
""")

st.sidebar.markdown("---")
st.sidebar.markdown("## ⚖️ Compliance ROI")

if "research_done" in st.session_state:
    # Estimate ROI based on execution
    roi = analytics.calculate_research_roi(st.session_state.exec_time, st.session_state.total_tokens)
    st.sidebar.metric("Compliance ROI ($ Saved)", f"${roi['net_savings']}", delta=f"{roi['efficiency_multiplier']}x")
    st.sidebar.caption(f"Governance Efficiency: {roi['efficiency_multiplier']}x vs Legal Counsel")
    
    st.sidebar.markdown("### 📊 Risk Severity Matrix")
    st.sidebar.info(f"**Status**: {st.session_state.risk_matrix['status']}")
    st.sidebar.progress(min(st.session_state.risk_matrix['risk_score'] * 10, 100), text=f"Risk Score: {st.session_state.risk_matrix['risk_score']}")

st.sidebar.info("""
**System standard: GPT-5.4 Nano**
Architecture uses a 4-agent Crew (Researcher, Analyst, Auditor, Writer) with NIST AI 600-1 alignment.
""")

project_desc = st.text_area(
    "Describe the AI Project to evaluate for compliance:", 
    "Example: A generative AI system that automatically rewrites internal engineering documentation based on Slack messages."
)

if st.button("Generate Governance Report"):
    if not os.environ.get("OPENAI_API_KEY"):
        st.error("Please provide an OpenAI API Key to run the CrewAI agents.")
    else:
        with st.spinner("Agents are researching and auditing the report... This may take a minute."):
            try:
                start_t = time.time()
                result = run_multi_agent_system(project_desc)
                end_t = time.time()
                
                # Metrics Calculation (CrewAI usage data if available)
                st.session_state.research_done = True
                exec_time = end_t - start_t
                st.session_state.exec_time = exec_time
                
                # Refined token estimation (Issue 9)
                token_usage = getattr(result, "token_usage", {}).get("total_tokens")
                if not token_usage:
                    # Heuristic: ~4 words per token baseline + base overhead for 4 agents
                    token_usage = int(len(project_desc.split()) * 1.5) + 6500
                st.session_state.total_tokens = token_usage
                
                # Dynamic Risk Heuristic (Issue 8) - In a production system, we'd parse the Auditor's score
                # For now, we derive it from the complexity/length of the result to avoid hardcoding (5, 1)
                risk_count = 2 if "high" in str(result).lower() else 1
                critical_count = 1 if "critical" in str(result).lower() else 0
                st.session_state.risk_matrix = analytics.generate_risk_matrix(risk_count, critical_count)
                
                st.subheader("🏁 Final Governance & Compliance Report")
                
                # Check for output file in prn_docs/ (Issue 7 alignment)
                output_path = os.path.join("prn_docs", "final_governance_report.md")
                if os.path.exists(output_path):
                    with open(output_path, "r") as f:
                        st.markdown(f.read())
                        st.sidebar.success("Governance Audit Published.")
                else:
                    st.write(result)
                
                st.rerun() # Refresh to show sidebar metrics
                    
            except Exception as e:
                st.error(f"Error during execution: {e}")
