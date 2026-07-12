import os
import sys
import yaml
from datetime import datetime
from dotenv import load_dotenv

# Ensure local execution paths resolve seamlessly
sys.path.append('.')

from src.agents import AIAgent
from src.tasks import run_autonomous_workflow

def save_log_to_file(user_prompt: str, result_text: str):
    """Safely saves the swarm results to a timestamped Markdown file."""
    os.makedirs('logs', exist_ok=True)
    
    # Generate an automated clean timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = "".join(x for x in user_prompt[:20] if x.isalnum() or x in " -_").strip()
    filename = f"logs/report_{timestamp}_{safe_title}.md"
    
    log_content = f"""# 🧠 SWARMMIND PIPELINE RUN
**Timestamp:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Original Request:** `{user_prompt}`

----------------------------------------------------
{result_text}
----------------------------------------------------
*End of automated report execution.*
"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(log_content)
    print(f"\n💾 [System] Swarm log successfully saved to: {filename}")

def main():
    load_dotenv()
    
    config_path = os.path.join(os.path.dirname(__file__), '../config/agents.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

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
    
    user_prompt = input("\nEnter what you want the AI swarm to build/analyze:\n> ")
    
    if not user_prompt.strip():
        print("Error: Objective cannot be empty.")
        return

    try:
        result = run_autonomous_workflow(agents, user_prompt)
        
        print("\n================ FINAL REPORT ================\n")
        print(result)
        print("\n==============================================")
        
        # Trigger the automated file logger
        save_log_to_file(user_prompt, result)
        
    except Exception as e:
        print(f"\n💥 Execution failed: {e}")

if __name__ == "__main__":
    main()

