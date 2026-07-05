import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')
print(f"API Key loaded: {api_key[:20]}..." if api_key else "API Key NOT loaded")
print(f"Key is valid: {api_key.startswith('sk-ant') if api_key else False}")
