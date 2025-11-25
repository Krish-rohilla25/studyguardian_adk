import sys
import os
import asyncio
from unittest.mock import MagicMock, patch
from dotenv import load_dotenv

# Add app to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from orchestrator import StudyOrchestrator

async def test_flow():
    print("Starting Integration Test (Mocked Mode)...")
    
    # Set dummy API key for testing
    os.environ["GOOGLE_API_KEY"] = "dummy_key"
    
    # Mock GeminiClient
    with patch("utils.gemini_client.requests.post") as MockPost:
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "candidates": [{
                "content": {
                    "parts": [{"text": "Mocked Response Content"}]
                }
            }]
        }
        MockPost.return_value = mock_response

        # We can use side_effect to vary responses based on prompt if needed
        def side_effect(*args, **kwargs):
            data = kwargs.get('json', {})
            prompt = data.get('contents', [{}])[0].get('parts', [{}])[0].get('text', '')
            
            res = MagicMock()
            if "study plan" in prompt or "Planner" in prompt:
                text = "1. Read Chapter 1\n2. Take Quiz\n3. Review"
            elif "Quiz" in prompt or "Multiple Choice" in prompt:
                text = "1. What is X?\nA) Y\nB) Z\nCorrect: A"
            else:
                text = "Generic Response"
            
            res.json.return_value = {
                "candidates": [{
                    "content": {
                        "parts": [{"text": text}]
                    }
                }]
            }
            return res
            
        MockPost.side_effect = side_effect

        orchestrator = StudyOrchestrator()
        
        test_input = "I want to study the basics of Photosynthesis."
        print(f"Test Input: {test_input}")
        
        try:
            response = await orchestrator.process_request(test_input)
            print("\nResponse Received:")
            print(response)
            print("\nTest Passed!")
        except Exception as e:
            print(f"\nTest Failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_flow())
