from utils.observability import AgentLogger
import os
from tools.pdf_reader import PDFReaderTool
from tools.google_search import SearchTool
from utils.gemini_client import GeminiClient

class RetrieverAgent:
    def __init__(self):
        self.logger = AgentLogger()
        self.pdf_tool = PDFReaderTool()
        self.search_tool = SearchTool()
        self.client = GeminiClient()

    def run(self, state: dict):
        """
        Retrieves information based on the plan.
        """
        plan = state.get("plan")
        user_input = state.get("user_input")
        self.logger.log("Retriever", "Retrieving content...")
        
        # Check if user provided a PDF path
        pdf_content = ""
        pdf_error = ""
        words = user_input.split()
        for word in words:
            if word.lower().endswith(".pdf"):
                if os.path.exists(word):
                    self.logger.log("Retriever", f"Found PDF file: {word}")
                    pdf_content = self.pdf_tool.read_pdf(word)
                else:
                    self.logger.log("Retriever", f"PDF file not found: {word}")
                    pdf_error = f"⚠️ Error: The file '{word}' was not found. Please check the path."
                break
        
        # If we had a PDF error, we should probably stop or warn, but for now let's include it
        
        if self.search_tool.active:
            search_results = self.search_tool.run(f"Study resources for: {user_input}")
        else:
            # Fallback: Ask LLM to generate a summary of the topic
            # Only use fallback if we didn't try to find a PDF and fail
            if pdf_error:
                search_results = "No external resources found due to file error."
            else:
                self.logger.log("Retriever", "Search inactive, using LLM knowledge.")
                prompt = f"Provide a comprehensive summary of the topic: {user_input}. Include key facts and concepts suitable for studying."
                search_results = self.client.generate_content(prompt)
        
        retrieved_info = f"Source Material:\n{search_results}\n\n"
        if pdf_content:
            retrieved_info += f"PDF Content ({len(pdf_content)} chars):\n{pdf_content[:2000]}..." 
        if pdf_error:
             retrieved_info += f"\n{pdf_error}"
        
        retrieved_info = f"Source Material:\n{search_results}\n\n"
        if pdf_content:
            retrieved_info += f"PDF Content ({len(pdf_content)} chars):\n{pdf_content[:2000]}..." # Limit context
        
        self.logger.log("Retriever", "Content retrieved.")
        return {"retrieved_docs": [retrieved_info]}
