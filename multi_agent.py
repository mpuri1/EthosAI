import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, Tool
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

# Load variables from .env if present
load_dotenv()

# Tools Setup
import os

# We will implement a custom Chroma Search tool
def search_chroma(query: str) -> str:
    """Searches the local Chroma DB for AI compliance policies"""
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
    results = db.search(query, search_type="similarity", k=3)
    if not results:
        return "No local compliance documents found regarding this query."
    return "\n\n".join([doc.page_content for doc in results])

db_search_tool = Tool.from_function(
    func=search_chroma,
    name="Local Policy DB Search",
    description="Useful for searching internal corporate AI policies and NIST frameworks."
)

serper_tool = SerperDevTool() # Ensure SERPER_API_KEY is in env

# Define Agents
researcher = Agent(
    role='Lead AI Compliance Researcher',
    goal='Search the web and internal databases for the latest AI regulations and frameworks',
    backstory='An expert in AI policy scanning the EU AI Act, NIST frameworks, and corporate rules.',
    verbose=True,
    allow_delegation=False,
    tools=[serper_tool, db_search_tool],
    llm='gpt-5.4-nano'
)

risk_analyst = Agent(
    role='Senior AI Risk Analyst',
    goal='Analyze a proposed AI project against gathered regulations to identify compliance gaps',
    backstory='A rigorous risk mitigator who spots hallucination risks, privacy leaks, and governance violations in AI architectures.',
    verbose=True,
    allow_delegation=False,
    llm='gpt-5.4-nano'
)

governance_writer = Agent(
    role='Governance Report Writer',
    goal='Write an authoritative Markdown PDF report summarizing the risk gaps and recommendations',
    backstory='A clear, concise technical writer who formats legal and technical constraints into actionable engineering tickets and compliance warnings.',
    verbose=True,
    allow_delegation=False,
    llm='gpt-5.4-nano'
)

fairness_auditor = Agent(
    role='Senior Fairness & Ethics Auditor',
    goal='Audit the research and risk analysis specifically for disparate impact and NIST AI 600-1 alignment',
    backstory='A vigilant ethisist who ensures AI systems do not violate fairness principles or introduce discriminatory bias.',
    verbose=True,
    allow_delegation=False,
    llm='gpt-5.4-nano'
)

def run_multi_agent_system(project_description: str):
    # Tasks
    research_task = Task(
        description=f'Find regulations and internal policies relevant to this AI Project: "{project_description}". Use tools to search the web (Serper) and Local DB.',
        expected_output='A bulleted list of the top 5 most critical regulatory requirements for this specific system.',
        agent=researcher
    )

    analysis_task = Task(
        description=f'Review the research and the project: "{project_description}". Identify the top 3 compliance risks and how they might violate the regulations.',
        expected_output='Detailed analysis of the 3 specific risks, their severity, and technical mitigation strategies.',
        agent=risk_analyst
    )

    audit_task = Task(
        description='Audit the research findings and risk analysis. Cross-reference against fairness principles and potential discriminatory impact.',
        expected_output='A definitive fairness audit statement and a Quantitative Risk Score (1-10) for the overall project.',
        agent=fairness_auditor
    )

    report_task = Task(
        description='Compile the research, analysis, and fairness audit into a markdown compliance report.',
        expected_output='A clean markdown report with sections: Executive Summary, Applicable Regulations, Risk Analysis (with Risk Matrix), Fairness Audit, Mitigation Recommendations.',
        agent=governance_writer,
        output_file='final_governance_report.md'
    )

    crew = Crew(
        agents=[researcher, risk_analyst, fairness_auditor, governance_writer],
        tasks=[research_task, analysis_task, audit_task, report_task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()
    return result

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY") or not os.environ.get("SERPER_API_KEY"):
        print("Note: To run fully, set OPENAI_API_KEY and SERPER_API_KEY.")
    
    test_project = "A customer service chatbot that scans user emails to detect tone and recommend insurance policy cancelations"
    print(f"Running CrewAI analysis for project: {test_project}")
    run_multi_agent_system(test_project)
