import sys
import os
import importlib

def check_setup():
    print("Checking StudyGuardian Setup...")
    
    # 1. Check Python Version
    print(f"Python Version: {sys.version}")
    
    # 2. Check Dependencies
    required = ["google.generativeai", "langchain", "dotenv", "termcolor"]
    missing = []
    for pkg in required:
        try:
            importlib.import_module(pkg)
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
    else:
        print("✅ Dependencies installed.")

    # 3. Check API Key
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY is missing in .env file.")
    elif api_key == "your_api_key_here":
        print("❌ GOOGLE_API_KEY is set to default placeholder. Please update it.")
    else:
        print("✅ GOOGLE_API_KEY found.")

    # 4. Check Imports (Catch compatibility issues)
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
        from orchestrator import StudyOrchestrator
        print("✅ Core modules imported successfully.")
    except Exception as e:
        print(f"❌ Import Error: {e}")

if __name__ == "__main__":
    check_setup()
