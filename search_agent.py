import json, os
from xmlrpc import client as xmlrpc_client
from rank_bm25 import BM25Okapi
from dotenv import load_dotenv
import anthropic

load_dotenv(override=True)
with open('data/chunks/all_chunks.json','r') as f:
    chunks = json.load(f)

print('Building search index...')
tokenized = [c['text'].lower().split() for c in chunks]
bm25 =      BM25Okapi(tokenized)
print(f'Index ready with {len(chunks)} chunks')
def find_relevant_chunks(question, top_n=12):
    scores = bm25.get_scores(question.lower().split())
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_n]
    relevant_chunks = [chunks[i] for i in top_indices]
    
    # Manually boost school_hours chunk if question is about times/hours
    keywords = ['school', 'start', 'time', 'hours', 'begin', 'schedule']
    if any(kw in question.lower() for kw in keywords):
        school_hours = [c for c in chunks if c['id'] == 'school_hours_chunk_0']
        if school_hours and school_hours[0] not in relevant_chunks:
            relevant_chunks.append(school_hours[0])
    
    return relevant_chunks
def ask_eps_agent(question):
    relevant = find_relevant_chunks(question)
    context = ''
    for chunk in relevant:
        context += f'\n[Source: {chunk["source_url"]}]\n{chunk["text"]}\n'
    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
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
    # Extract text from response (handle ThinkingBlock if present)
    result = ""
    for block in message.content:
        if hasattr(block, 'text'):
            result += block.text
    return result if result else "No text response generated"

# Test with your 20 questions from Week 1!
test_questions = [
"When is spring break?",
"What time does school start for elementary, middle school, and high school?",
"How do I apply for free lunch?",
"What sports does the district offer?",
"How do I enroll my child?",
]

if __name__ == '__main__':
    for q in test_questions:
        print(f'\nQ: {q}')
        print(f'A: {ask_eps_agent(q)}')
        print('-'*60)