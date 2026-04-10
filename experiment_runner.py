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

    # Variant A: Control
    print("\n--- Running Variant A (CONTROL) ---")
    control_result = run_multi_agent_system(project_desc, variant="CONTROL")
    with open("eval_control.md", "w") as f:
        f.write(str(control_result))

    # Variant B: Treatment
    print("\n--- Running Variant B (TREATMENT) ---")
    treatment_result = run_multi_agent_system(project_desc, variant="TREATMENT")
    with open("eval_treatment.md", "w") as f:
        f.write(str(treatment_result))

    print("\n✅ Experiment Run Complete.")
    print("Files 'eval_control.md' and 'eval_treatment.md' are ready for side-by-side comparison.")

if __name__ == "__main__":
    test_project = "AI-powered credit scoring system for small businesses using social media data"
    run_experiment(test_project)
