import os
import sys
from dotenv import load_dotenv

# Force reload of .env
load_dotenv(override=True)

# Check what we loaded
api_key = os.getenv('ANTHROPIC_API_KEY')
print(f"Loaded key: {api_key[:50]}..." if api_key else "NO KEY")
print(f"Key has newline: {'\\n' in (api_key or '')}")
print(f"Key length: {len(api_key) if api_key else 0}")

# Now test a query
import anthropic

try:
    client = anthropic.Anthropic(api_key=api_key)
    print("\n✓ Client created successfully")
    
    # Try a simple message
    message = client.messages.create(
        model='claude-3-5-sonnet-20241022',
        max_tokens=100,
        messages=[{'role': 'user', 'content': 'Say hello in one word'}]
    )
    print(f"✓ API works! Response: {message.content[0].text}")
except anthropic.AuthenticationError as e:
    print(f"\n✗ Auth failed: {e}")
except Exception as e:
    print(f"\n✗ Error: {type(e).__name__}: {e}")
