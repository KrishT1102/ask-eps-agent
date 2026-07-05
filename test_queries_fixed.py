import os
from dotenv import load_dotenv

# Fix the .env first before any imports
load_dotenv(override=True)
api_key = os.getenv('ANTHROPIC_API_KEY')
print(f"API Key loaded: {api_key[:50]}...")

# Now import search_agent
from search_agent import ask_eps_agent

print("\nTesting with BETTER search queries:\n")

queries = [
    "What are the school hours?",
    "What time do schools start?", 
    "Elementary school start time",
]

for q in queries:
    print(f"Q: {q}")
    try:
        answer = ask_eps_agent(q)
        print(f"A: {answer[:300]}" + ("...\n" if len(answer) > 300 else "\n"))
    except Exception as e:
        print(f"Error: {str(e)[:150]}\n")
