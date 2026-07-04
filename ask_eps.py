import os
from pathlib import Path
from dotenv import load_dotenv
import anthropic

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

#Key comes from .env - never hardcoded 
#Read the calendar text we saved yesterday

with open("calendar_page.txt", "r") as f:
    eps_content = f.read()

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise RuntimeError("ANTHROPIC_API_KEY was not found. Add it to the .env file in the project folder.")

#Set up the Anthropic client
client = anthropic.Anthropic(api_key=api_key)

#The question we want to ask
question = "When does school start in the 2026-2027 school year?"

print(f'Question: {question}')
print("Thinking...\n")

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=500,
    messages=[{
    "role": "user",
    "content": f"""You are a helpful assistant for Everett Public Schools.
Answer using ONLY the information provided below.
If the answer is not in the content, say:
'I could not find this on the EPS website.'
Always mention which page the information came from.
EPS WEBSITE CONTENT:
{eps_content[:8000]}
QUESTION: {question}"""
    }]
)

print('Answer:', message.content[0].text)