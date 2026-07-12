import sys
sys.path.append('.')
import os
import yaml
from dotenv import load_dotenv
from src.agents import AIAgent
from src.tasks import run_autonomous_workflow

def main():
    # Load keys from .env
    load_dotenv()
    
    # Read the YAML agent configurations
    config_path = os.path.join(os.path.dirname(__file__), '../config/agents.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    # Initialize the Multi-Model Agent Swarm
    agents = {}
    for agent_key, data in config.items():
        agents[agent_key] = AIAgent(
            name=data['name'],
            role=data['role'],
            goal=data['goal'],
            provider=data['provider'],
            model=data['model']
        )

    print("====================================================")
    print("🧠 SWARMMIND: MULTI-MODEL HYBRID AI ENGINE ACTIVATED")
    print("====================================================")
    
    # Get dynamic input from user inside Termux
    user_prompt = input("\nEnter what you want the AI swarm to build/analyze:\n> ")
    
    if not user_prompt.strip():
        print("Error: Objective cannot be empty.")
        return

    try:
        result = run_autonomous_workflow(agents, user_prompt)
        
        print("\n================ FINAL REPORT ================\n")
        print(result)
        print("\n==============================================")
        
    except Exception as e:
        print(f"\n💥 Execution failed: {e}")
        print("Please check your .env file and ensure API keys are set correctly.")

if __name__ == "__main__":
    main()
