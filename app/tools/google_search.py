from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
import os

class SearchTool:
    def __init__(self):
        # Check if keys exist, otherwise mock
        if os.getenv("GOOGLE_API_KEY") and os.getenv("GOOGLE_CSE_ID"):
            self.search = GoogleSearchAPIWrapper()
            self.active = True
        else:
            self.active = False

    def run(self, query: str) -> str:
        if self.active:
            try:
                return self.search.run(query)
            except Exception as e:
                return f"Search failed: {str(e)}"
        else:
            return f"Simulated search results for: {query}\n- Study Tip 1: Focus on active recall.\n- Study Tip 2: Use spaced repetition."
