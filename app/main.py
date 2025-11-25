import os
import sys
import asyncio
from dotenv import load_dotenv
from termcolor import colored

# Python 3.8 Compatibility Patch
if sys.version_info < (3, 10):
    try:
        import importlib_metadata
        import importlib.metadata
        if not hasattr(importlib.metadata, "packages_distributions"):
            importlib.metadata.packages_distributions = importlib_metadata.packages_distributions
    except ImportError:
        pass

# Add the current directory to sys.path to ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestrator import StudyOrchestrator
from utils.observability import AgentLogger

# Load environment variables
load_dotenv()

async def main():
    """
    Main entry point for the StudyGuardian CLI.
    """
    logger = AgentLogger()
    logger.log("System", "Initializing StudyGuardian...")

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logger.error("System", "GOOGLE_API_KEY not found in environment variables.")
        print(colored("Error: GOOGLE_API_KEY is missing. Please set it in your .env file.", "red"))
        return
    
    import google.generativeai as genai
    genai.configure(api_key=api_key)

    orchestrator = StudyOrchestrator()
    
    print(colored("\n🎓 Welcome to StudyGuardian! 🎓", "cyan", attrs=["bold"]))
    print(colored("Your AI-powered study companion.", "cyan"))
    print("-" * 50)

    while True:
        try:
            user_input = input(colored("\nYou: ", "green"))
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print(colored("StudyGuardian: Goodbye! Happy studying!", "blue"))
                break

            logger.log("User", f"Input: {user_input}")
            
            # Run the orchestrator
            print(colored("StudyGuardian is thinking...", "yellow"))
            response = await orchestrator.process_request(user_input)
            
            print(colored(f"\nStudyGuardian: {response}", "blue"))
            logger.log("System", "Request processed successfully.")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.error("System", f"An error occurred: {str(e)}")
            print(colored(f"Error: {str(e)}", "red"))

if __name__ == "__main__":
    asyncio.run(main())
