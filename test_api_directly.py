import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')
print(f"API Key from env: {api_key[:30]}..." if api_key else "NO KEY FOUND")

# Try creating client directly
try:
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=50,
        messages=[{'role': 'user', 'content': 'Say hello'}]
    )
    print(f"Success! Response: {message.content[0].text}")
except anthropic.AuthenticationError as e:
    print(f"Auth Error: {e}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
