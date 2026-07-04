import os
import anthropic

#Read the calendar text we saved yesterday

with open("calendar_page.txt", "r") as f:
    eps_content = f.read()

#Set up the Anthropic client
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

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