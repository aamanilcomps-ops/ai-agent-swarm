def run_autonomous_workflow(agents_dict, user_request: str) -> str:
    # 1. Access the initialized agent instances
    manager = agents_dict['manager_agent']
    researcher = agents_dict['research_agent']
    writer = agents_dict['writer_agent']

    print(f"\n[1/3] 🤖 {manager.name} ({manager.provider.upper()}) is breaking down the objective...")
    manager_plan = manager.execute(
        task_prompt=f"Create a specific execution plan for this request: {user_request}"
    )
    print("-> Plan generated successfully.")

    print(f"\n[2/3] 🔍 {researcher.name} ({researcher.provider.upper()}) is gathering deep insights...")
    research_data = researcher.execute(
        task_prompt="Gather detailed technical data and core facts needed to fulfill this plan.",
        context=manager_plan
    )
    print("-> Research data compiled successfully.")

    print(f"\n[3/3] ✍️ {writer.name} ({writer.provider.upper()}) is synthesizing the final output...")
    final_output = writer.execute(
        task_prompt="Create the final comprehensive project document or output using the provided research data.",
        context=research_data
    )
    print("-> Final report completely built.")
    
    return final_output
