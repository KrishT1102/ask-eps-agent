from dotenv import find_dotenv, load_dotenv
import os

dotenv_path = find_dotenv()
print(f"Found .env at: {dotenv_path}")

# Check file exists and content
if os.path.exists(dotenv_path):
    with open(dotenv_path, 'r') as f:
        content = f.read()
    print(f"File content:\n{content}")

# Now load and check
load_dotenv(override=True)
api_key = os.getenv('ANTHROPIC_API_KEY')
print(f"\nLoaded API Key: {api_key}")
