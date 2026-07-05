import os
from dotenv import load_dotenv
import anthropic

load_dotenv(override=True)

school_hours_text = """District and School Hours - Everett Public Schools

Elementary Schools: 9:15 a.m. - 3:30 p.m.
Middle Schools: 8:15 a.m. - 2:50 p.m.
High Schools: 7:30 a.m. - 2:05 p.m.
Sequoia High: 8:20 a.m. - 2:55 p.m.

Summer hours:
Hawthorne, Lowell, Madison, Monroe, Whittier and Woodside: 8:35 a.m. - 2:50 p.m.
"""

prompt = f"""You are a helpful assistant for Everett Public Schools.
Answer using ONLY the information below. If not found say:
"I could not find this on the EPS website."
Always end with the source URL.

CONTEXT: {school_hours_text}

QUESTION: What are the school start times for elementary, middle school, and high school?"""

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
message = client.messages.create(
    model='claude-sonnet-5',
    max_tokens=300,
    messages=[{'role': 'user', 'content': prompt}]
)

# Extract text from message
for block in message.content:
    if hasattr(block, 'text'):
        print(block.text)
        break
else:
    print(f"Response type: {type(message.content[0])}")
    print(f"Content: {message.content}")
