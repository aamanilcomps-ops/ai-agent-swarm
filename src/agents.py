class AIAgent:
    def __init__(self, name: str, role: str, goal: str, provider: str, model: str):
        self.name = name
        self.role = role
        self.goal = goal
        self.provider = provider.lower()
        self.model = model

    def execute(self, task_prompt: str, context: str = "") -> str:
        print(f"   [Simulation] Connecting to {self.provider.upper()} ({self.model})... Done.")
        
        if self.name == "Atlas":
            return "Task Plan: Generate an automated math utility script."
            
        elif self.name == "Argus":
            return "Technical Audit: Python logic validated."
            
        elif self.name == "Scribe":
            # This is raw, pristine, executable Python code
            return "import math\nprint('\\n===============================================')\nprint('🚀 SUCCESS: This tool was built by your AI Swarm!')\nprint('===============================================')\nradius = 5\narea = math.pi * (radius ** 2)\nprint(f'Calculated Area of a Circle (Radius {radius}): {area:.2f}')\nprint('===============================================')\n"
            
        return "print('Error: Unknown Agent')"
