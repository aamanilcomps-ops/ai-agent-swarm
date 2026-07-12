import os
import sys
import yaml
import subprocess
from dotenv import load_dotenv

sys.path.append('.')

from src.agents import AIAgent
from src.tasks import run_autonomous_workflow

def execute_generated_code(code_string: str):
    """Saves the generated string as a Python file and executes it locally."""
    os.makedirs('generated_output', exist_ok=True)
    file_path = "generated_output/app.py"
    
    # Write the script
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code_string)
    
    print(f"\n⚙️ [Orchestrator] Saved generated tool code to: {file_path}")
    print("⚙️ [Orchestrator] Booting sandbox environment and executing script...\n")
    
    # Actually execute the generated python file using Termux's background process
    try:
        subprocess.run(["python", file_path], check=True)
    except Exception as e:
        print(f"💥 Failed to execute the generated tool: {e}")

def main():
    load_dotenv()
    
    config_path = os.path.join(os.path.dirname(__file__), '../config/agents.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    agents = {}
    for agent_key, data in config.items():
        agents[agent_key] = AIAgent(
            name=data['name'], role=data['role'], goal=data['goal'], provider=data['provider'], model=data['model']
        )

    print("====================================================")
    print("🧠 SWARMMIND: AUTOMATED CODE-RUNNER ENGAGED")
    print("====================================================")
    
    user_prompt = input("\nEnter what you want the AI swarm to build/analyze:\n> ")
    if not user_prompt.strip(): return

    try:
        # Run the agent pipeline
        result_code = run_autonomous_workflow(agents, user_prompt)
        
        # Pass the code output straight into the terminal runner execution system
        execute_generated_code(result_code)
        
    except Exception as e:
        print(f"\n💥 Execution failed: {e}")

if __name__ == "__main__":
    main()

