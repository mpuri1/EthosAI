import os
from multi_agent import run_multi_agent_system
from dotenv import load_dotenv

# Load credentials
load_dotenv()

def run_experiment(project_desc):
    """
    Runs a GenAI Governance A/B Test.
    Compare Variant A (Control) vs. Variant B (Treatment/Strict).
    """
    print("\n🚀 Starting GenAI Governance Experiment...")
    print(f"Project: {project_desc}")

    # Artifact Hygiene: Ensure output dir exists
    os.makedirs("prn_docs", exist_ok=True)

    # Variant A: Control
    print("\n--- Running Variant A (CONTROL) ---")
    try:
        control_result = run_multi_agent_system(project_desc, variant="CONTROL")
        with open(os.path.join("prn_docs", "eval_control.md"), "w") as f:
            f.write(str(control_result))
    except Exception as e:
        print(f"❌ Error in CONTROL run: {e}")

    # Variant B: Treatment
    print("\n--- Running Variant B (TREATMENT) ---")
    try:
        treatment_result = run_multi_agent_system(project_desc, variant="TREATMENT")
        with open(os.path.join("prn_docs", "eval_treatment.md"), "w") as f:
            f.write(str(treatment_result))
    except Exception as e:
        print(f"❌ Error in TREATMENT run: {e}")

    print("\n✅ Experiment Run Complete.")
    print("Files located in 'prn_docs/' for session isolation.")

if __name__ == "__main__":
    test_project = "AI-powered credit scoring system for small businesses using social media data"
    run_experiment(test_project)
