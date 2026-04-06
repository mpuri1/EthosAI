import streamlit as st
import os

from rag_pipeline import initialize_vector_store
from multi_agent import run_multi_agent_system
from dotenv import load_dotenv

# Load variables from .env if present
load_dotenv()

st.set_page_config(page_title="EthosAI | Governance Reporter", layout="wide")
st.title("EthosAI: Autonomous Governance & Research Suite")

st.markdown("""
This tool uses a Multi-Agent system (Researcher, Risk Analyst, Governance Writer) to evaluate proposed AI architectures against live regulations and internal DB policies.
""")

st.sidebar.header("System Initialization")

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

project_desc = st.text_area(
    "Describe the AI Project to evaluate for compliance:", 
    "Example: A generative AI system that automatically rewrites internal engineering documentation based on Slack messages."
)

if st.button("Generate Governance Report"):
    if not os.environ.get("OPENAI_API_KEY"):
        st.error("Please provide an OpenAI API Key to run the CrewAI agents.")
    else:
        with st.spinner("Agents are researching and writing the report... This may take a minute."):
            try:
                result = run_multi_agent_system(project_desc)
                st.subheader("Final Governance Report")
                
                # Check for output file
                if os.path.exists("final_governance_report.md"):
                    with open("final_governance_report.md", "r") as f:
                        st.markdown(f.read())
                else:
                    st.write(result)
                    
            except Exception as e:
                st.error(f"Error during execution: {e}")
