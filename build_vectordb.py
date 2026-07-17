import chromadb
import json
import os

# Load all chunks from Week 2
with open('data/chunks/all_chunks.json','r') as f:
    chunks = json.load(f)

print(f'Loaded {len(chunks)} chunks')

# Create persistent database — saved to disk
os.makedirs('data/vectordb', exist_ok=True)
client = chromadb.PersistentClient(path='data/vectordb')
# Delete old collection if rebuilding

try:
    client.delete_collection('eps_knowledge')
    print('Cleared old collection')
except: pass

# Create fresh collection
collection = client.get_or_create_collection(
    name='eps_knowledge',
    metadata={'hnsw:space': 'cosine'}
)

# Add chunks in batches of 50
batch_size = 50
for i in range(0, len(chunks), batch_size):
    batch = chunks[i:i+batch_size]
    collection.add(
        documents=[c['text'] for c in batch],
        ids= [c['id'] for c in batch],
        metadatas=[{'page_name': c['page_name'],
            'source_url': c['source_url']}
            for c in batch],

    )
    print(f' Added batch {i//batch_size + 1} — {min(i+batch_size,len(chunks))}/{len(chunks)} chunks')
    
print(f'Done! {collection.count()} chunks stored in ChromaDB')
