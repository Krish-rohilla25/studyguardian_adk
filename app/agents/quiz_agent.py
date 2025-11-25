from utils.observability import AgentLogger
from utils.gemini_client import GeminiClient

class QuizAgent:
    def __init__(self):
        self.logger = AgentLogger()
        self.client = GeminiClient()

    def run(self, state: dict):
        """
        Generates a quiz based on retrieved docs.
        """
        docs = state.get("retrieved_docs", [])
        context = "\n".join(docs)
        
        self.logger.log("QuizAgent", "Generating quiz...")
        
        prompt = f"""
        Based on the following content, generate 3 Multiple Choice Questions (MCQs).
        Content: {context}
        
        Format:
        1. Question
        A) Option
        B) Option
        C) Option
        D) Option
        Correct Answer: X
        """
        
        quiz = self.client.generate_content(prompt)
        
        self.logger.log("QuizAgent", "Quiz generated.")
        return {"quiz": quiz}
