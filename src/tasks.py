from src.agents import AIAgent
from src.logger import setup_logger

logger = setup_logger(__name__)


def run_autonomous_workflow(agents_dict: dict, user_request: str) -> str:
    """
    Execute autonomous multi-agent workflow.
    
    Args:
        agents_dict: Dictionary of initialized AIAgent instances
        user_request: User's initial request/prompt
    
    Returns:
        Final generated output from the workflow
    """
    try:
        manager = agents_dict['manager_agent']
        researcher = agents_dict['research_agent']
        writer = agents_dict['writer_agent']
        
        # Stage 1: Manager breaks down the objective
        logger.info("Stage 1/3: Manager planning")
        print(f"\n[1/3] 🤖 {manager.name} ({manager.provider_name.upper()}) is breaking down the objective...")
        manager_plan = manager.execute(task_prompt=user_request)
        logger.debug(f"Manager plan: {manager_plan[:200]}...")
        
        # Stage 2: Researcher gathers insights
        logger.info("Stage 2/3: Research gathering")
        print(f"\n[2/3] 🔍 {researcher.name} ({researcher.provider_name.upper()}) is gathering deep insights...")
        research_data = researcher.execute(
            task_prompt="Audit plan and provide technical insights",
            context=manager_plan
        )
        logger.debug(f"Research data: {research_data[:200]}...")
        
        # Stage 3: Writer synthesizes output
        logger.info("Stage 3/3: Output generation")
        print(f"\n[3/3] ✍️ {writer.name} ({writer.provider_name.upper()}) is synthesizing the final output...")
        final_output = writer.execute(
            task_prompt="Generate complete, executable Python code",
            context=research_data
        )
        
        logger.info("Workflow completed successfully")
        print("✅ Final report completely built.\n")
        
        return final_output
    
    except KeyError as e:
        logger.error(f"Missing required agent: {e}")
        raise ValueError(f"Workflow requires 'manager_agent', 'research_agent', and 'writer_agent'. Missing: {e}")
    
    except Exception as e:
        logger.error(f"Workflow execution failed: {e}")
        raise
