import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

def test_model(model_name):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": "Hello"}]}]
    }
    print(f"Testing {model_name}...")
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"✅ {model_name} is WORKING.")
        return True
    else:
        print(f"❌ {model_name} failed: {response.status_code} - {response.text}")
        return False

print("Fetching list of ALL available models...")
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
response = requests.get(url)

if response.status_code == 200:
    models = response.json().get('models', [])
    print(f"Found {len(models)} models.")
    for m in models:
        if 'generateContent' in m.get('supportedGenerationMethods', []):
            print(f"✅ CANDIDATE: {m['name']}")
        else:
            print(f"   (Skipping {m['name']} - methods: {m.get('supportedGenerationMethods')})")
else:
    print(f"❌ ListModels failed: {response.status_code} - {response.text}")
