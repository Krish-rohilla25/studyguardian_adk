import requests
import os
import json
from utils.observability import AgentLogger

class GeminiClient:
    def __init__(self, model_name="gemini-2.0-flash"):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.model_name = model_name
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.logger = AgentLogger()

    def generate_content(self, prompt: str) -> str:
        if not self.api_key:
            self.logger.error("GeminiClient", "API Key missing")
            return "Error: API Key missing."

        url = f"{self.base_url}/{self.model_name}:generateContent?key={self.api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            # Extract text from response
            # Response structure: candidates[0].content.parts[0].text
            try:
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                return text
            except (KeyError, IndexError) as e:
                self.logger.error("GeminiClient", f"Parsing error: {e}. Response: {result}")
                return "Error parsing model response."
                
        except requests.exceptions.RequestException as e:
            self.logger.error("GeminiClient", f"Request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                 self.logger.error("GeminiClient", f"Details: {e.response.text}")
            return f"Error calling Gemini API: {str(e)}"
