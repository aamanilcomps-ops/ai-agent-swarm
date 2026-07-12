def run_autonomous_workflow(agents_dict, user_request: str) -> str:
    manager = agents_dict['manager_agent']
    researcher = agents_dict['research_agent']
    writer = agents_dict['writer_agent']

    print(f"\n[1/3] 🤖 {manager.name} ({manager.provider.upper()}) is breaking down the objective...")
    manager_plan = manager.execute(task_prompt=user_request)

    print(f"\n[2/3] 🔍 {researcher.name} ({researcher.provider.upper()}) is gathering deep insights...")
    research_data = researcher.execute(task_prompt="Audit plan", context=manager_plan)

    print(f"\n[3/3] ✍️ {writer.name} ({writer.provider.upper()}) is synthesizing the final output...")
    final_output = writer.execute(task_prompt="Generate code", context=research_data)
    print("-> Final report completely built.")
    
    return final_output
