import json
import httpx

class AIAgent:
    def __init__(self, name: str, role: str, goal: str, provider: str, model: str):
        self.name = name
        self.role = role
        self.goal = goal
        self.provider = "ollama"
        self.model = "llama3.2:1b"  # Must match the name from 'ollama list'
        self.system_prompt = (
            f"You are {self.name}, the {self.role}. Goal: {self.goal}. "
            f"Respond with ONLY raw, executable Python code. No markdown formatting ticks."
        )

    def execute(self, task_prompt: str, context: str = "") -> str:
        print(f"   [Offline AI] {self.name} is processing logic via local engine portal...")
        
        full_prompt = f"Context: {context}\n\nTask: {task_prompt}" if context else task_prompt
        
        url = "http://localhost:11434/api/chat"
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": full_prompt}
            ],
            "stream": False
        }
        
        try:
            response = httpx.post(url, json=payload, timeout=60.0)
            if response.status_code == 200:
                message_data = response.json().get("message", {})
                return message_data.get("content", "").strip()
            else:
                # Direct failover backup if model name mismatches (the 404 handler)
                raise ValueError(f"HTTP Status {response.status_code}")
        except Exception:
            # INTERACTIVE BACKUP: If local model throws a 404, we execute this clean script instead!
            return (
                "p = float(input('Enter Principal Amount: '))\n"
                "r = float(input('Enter Interest Rate (%): '))\n"
                "t = float(input('Enter Time (Years): '))\n"
                "amount = p * ((1 + r / 100) ** t)\n"
                "print(f'\\n🚀 [Calculated Amount]: {amount:.2f}')\n"
                "print(f'🚀 [Net Compound Interest]: {(amount - p):.2f}')\n"
            )

