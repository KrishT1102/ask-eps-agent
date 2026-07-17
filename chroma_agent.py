import chromadb
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

# Load ChromaDB
client = chromadb.PersistentClient(path='data/vectordb')
collection = client.get_collection('eps_knowledge')
ai_client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def ask_eps(question):
    # Step 1: Semantic search
    results = collection.query(query_texts=[question], n_results=4)

    # Step 2: Build context with sources
    context = ''
    sources = []
    for i, doc in enumerate(results['documents'][0]):
        meta = results['metadatas'][0][i]
        context += f'[Source: {meta["source_url"]}]\n{doc}\n\n'
        sources.append(meta['source_url'])

    # Step 3: Ask Claude
    message = ai_client.messages.create(
    model='claude-sonnet-4-6',
    max_tokens=600,
    messages=[{'role':'user','content':f'''You are a helpful AI assistant
for Everett Public Schools (Washington State).
Answer using ONLY the context below — do not use your training data.
If the answer is not in the context say:
"I could not find this on the EPS website."
End every answer with: Source: [the URL where you found the answer]
CONTEXT:
{context}
QUESTION: {question}'''}]

    )

    return message.content[0].text

# Run all 20 test questions

print('EPS AI Agent — ChromaDB Version')
print('='*50)
while True:
    q = input('\nAsk a question (or type quit): ')
    if q.lower() == 'quit': break
    print('\n' + ask_eps(q))