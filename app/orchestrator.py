from typing import Dict, Any
from termcolor import colored
from agents.planner import PlannerAgent
from agents.retriever import RetrieverAgent
from agents.quiz_agent import QuizAgent
from agents.feedback_agent import FeedbackAgent
from memory.memory_bank import MemoryBank
from utils.observability import AgentLogger

class StudyOrchestrator:
    def __init__(self):
        self.logger = AgentLogger()
        self.memory = MemoryBank()
        
        # Initialize Agents
        self.planner = PlannerAgent()
        self.retriever = RetrieverAgent()
        self.quiz_agent = QuizAgent()
        self.feedback_agent = FeedbackAgent()

    async def process_request(self, user_input: str) -> str:
        """
        Process a user request through the agent workflow (Sequential).
        """
        self.logger.log("Orchestrator", f"Processing: {user_input}")
        
        # 1. Check Memory
        context = self.memory.get_context()
        
        state = {
            "user_input": user_input,
            "context": context,
            "plan": None,
            "retrieved_docs": [],
            "quiz": None
        }
        
        # 2. Planner
        self.logger.log("Orchestrator", "Invoking Planner...")
        print(colored("\n📘 [Planner Agent]: Creating study plan...", "cyan", attrs=['bold']))
        plan_result = self.planner.run(state)
        state.update(plan_result)
        
        # Format and print plan
        plan_text = state['plan']
        print(colored("\n" + "="*40, "blue"))
        print(colored("       📅 STUDY PLAN       ", "blue", attrs=['bold']))
        print(colored("="*40 + "\n", "blue"))
        print(colored(plan_text, "white"))
        print(colored("="*40 + "\n", "blue"))
        
        # 3. Retriever
        self.logger.log("Orchestrator", "Invoking Retriever...")
        print(colored("🔍 [Retriever Agent]: Gathering resources...", "cyan", attrs=['bold']))
        retriever_result = self.retriever.run(state)
        state.update(retriever_result)
        
        # Print retrieval summary
        docs = state.get('retrieved_docs', [])
        if docs:
            print(colored(f"✅ Found {len(docs)} resource(s).", "green"))
            # Optional: Print a snippet
            # print(colored(f"Preview: {docs[0][:100]}...", "dark_grey"))
        else:
            print(colored("⚠️ No specific resources found.", "yellow"))
        
        # 4. Quiz Generator
        self.logger.log("Orchestrator", "Invoking Quiz Agent...")
        print(colored("\n❓ [Quiz Agent]: Generating quiz...", "cyan", attrs=['bold']))
        quiz_result = self.quiz_agent.run(state)
        state.update(quiz_result)
        
        # 5. Format Output
        # 5. Format Output
        final_response = ""
        if state.get("quiz"):
            final_response = f"\n{state['quiz']}"
        elif state.get("plan"):
            final_response = f"Here is the study plan:\n{state['plan']}"
        else:
            final_response = "I'm not sure how to help with that yet."
            
        # Save to memory
        self.memory.add_turn(user_input, final_response)
        
        return final_response
