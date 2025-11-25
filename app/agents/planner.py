from utils.observability import AgentLogger
from utils.gemini_client import GeminiClient

class PlannerAgent:
    def __init__(self):
        self.logger = AgentLogger()
        self.client = GeminiClient()

    def run(self, state: dict):
        """
        Analyzes the user request and creates a study plan.
        """
        user_input = state["user_input"]
        context = state.get("context", "")
        
        self.logger.log("Planner", f"Planning for: {user_input}")
        
        prompt = f"""
        You are an expert study planner and tutor.
        
        CONTEXT:
        {context}
        
        USER GOAL: {user_input}
        
        INSTRUCTIONS:
        1. If the user is asking a follow-up question about the previous quiz or conversation (e.g., "explain Q3", "why is B wrong"), provide a direct explanation. DO NOT generate a new study plan.
        2. If the user mentions a file (e.g., "from notes.pdf", "read a.pdf"), assume the file is available. Create a plan to process it (e.g., "1. Analyze [filename]", "2. Extract key concepts", "3. Generate quiz"). DO NOT say source material is missing.
        3. If the user is asking for a new topic, create a concise 3-step study plan.
        
        Return ONLY the response (Plan or Explanation).
        """
        
        plan = self.client.generate_content(prompt)
        
        self.logger.log("Planner", f"Plan generated: {plan}")
        
        return {"plan": plan}
