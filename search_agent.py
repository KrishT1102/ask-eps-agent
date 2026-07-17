import json, os
import re
from pathlib import Path
from rank_bm25 import BM25Okapi
from dotenv import load_dotenv
import anthropic

# Do not override already-set environment variables (for example, shell/session vars).
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')
with open('data/chunks/all_chunks.json','r') as f:
    chunks = json.load(f)

print('Building search index...')


def tokenize(text):
    # Keep only word characters for more stable matching across punctuation/spacing.
    return re.findall(r"[a-z0-9]+", text.lower())


tokenized = [tokenize(c['text']) for c in chunks]
bm25 =      BM25Okapi(tokenized)
print(f'Index ready with {len(chunks)} chunks')


def get_anthropic_api_key():
    api_key = os.getenv('ANTHROPIC_API_KEY', '').strip()
    if not api_key or api_key == 'your_api_key_here':
        raise RuntimeError(
            'Missing or placeholder ANTHROPIC_API_KEY. '
            'Set a valid key in .env or your shell environment.'
        )
    if not api_key.startswith('sk-ant-'):
        raise RuntimeError(
            'ANTHROPIC_API_KEY looks invalid. Expected it to start with "sk-ant-".'
        )
    return api_key


def find_relevant_chunks(question, top_n=12):
    q_lower = question.lower()
    scores = bm25.get_scores(tokenize(question))
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_n]
    relevant_chunks = [chunks[i] for i in top_indices]

    # Boost school-hours chunk only for explicit time-of-day questions.
    hours_keywords = ['what time', 'hours', 'bell schedule', 'start time', 'end time', 'dismissal']
    if any(kw in q_lower for kw in hours_keywords):
        school_hours = [c for c in chunks if c['id'] == 'school_hours_chunk_0']
        if school_hours and school_hours[0] not in relevant_chunks:
            relevant_chunks.append(school_hours[0])

    # Boost calendar chunks for first-day/start-of-school-year questions.
    calendar_keywords = ['first day', 'start of school', 'start school', 'school year start', 'when does school start']
    if any(kw in q_lower for kw in calendar_keywords):
        calendar_chunks = [c for c in chunks if c['page_name'] == 'calendar']
        for chunk in calendar_chunks[:2]:
            if chunk not in relevant_chunks:
                relevant_chunks.append(chunk)
    
    return relevant_chunks
def ask_eps_agent(question):
    relevant = find_relevant_chunks(question)
    context = ''
    for chunk in relevant:
        context += f'\n[Source: {chunk["source_url"]}]\n{chunk["text"]}\n'
    client = anthropic.Anthropic(api_key=get_anthropic_api_key())
    try:
        message = client.messages.create(
            model='claude-sonnet-5',
            max_tokens=600,
            messages=[{'role':'user','content': f'''You are a helpful assistant for Everett Public Schools.
Answer using ONLY the information below. If not found say:
"I could not find this on the EPS website."
Always end with the source URL.
                   
CONTEXT: {context}

QUESTION: {question}'''}]
        )
    except anthropic.AuthenticationError as exc:
        raise RuntimeError(
            'Anthropic authentication failed. Check that ANTHROPIC_API_KEY is valid and active.'
        ) from exc
    # Extract text from response (handle ThinkingBlock if present)
    result = ""
    for block in message.content:
        if hasattr(block, 'text'):
            result += block.text
    return result if result else "No text response generated"

# Test with your 20 questions from Week 1!
test_questions = [
"When is the first day of school?",
"What time does school start for elementary, middle school, and high school?",
"How do I apply for free lunch?",
"What sports does the district offer?",
"How do I enroll my child?",
]

if __name__ == '__main__':  
    try:
        for q in test_questions:
            print(f'\nQ: {q}')
            print(f'A: {ask_eps_agent(q)}')
            print('-'*60)
    except RuntimeError as err:
        print(f'Configuration error: {err}')