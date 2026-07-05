import os, json
from pydoc import text

os.makedirs('data/chunks', exist_ok=True)

def chunk_text(text, chunk_size=400, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        chunk = ' '.join(words[start:start+chunk_size])
        chunks.append(chunk)
        start += chunk_size - overlap # overlap keeps context
    return chunks

all_chunks = []

for filename in os.listdir('data/clean'):
    if not filename.endswith('.txt'): continue
    page_name = filename.replace('.txt','')
    with open(f'data/clean/{filename}', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    source_url = ''
    for line in lines[:3]:
        if 'SOURCE URL:' in line:
            source_url = line.replace('SOURCE URL:','').strip()
    content = ' '.join(lines[3:])
    chunks = chunk_text(content)
    for i, chunk in enumerate(chunks):
        all_chunks.append({
            'id':          f'{page_name}_chunk_{i}',
            'page_name':   page_name,
            'source_url':  source_url,
            'text':        chunk
        })  
    print(f'{page_name}: {len(chunks)} chunks')

with open('data/chunks/all_chunks.json','w') as f:
    json.dump(all_chunks, f, indent=2)
    
print(f'Total: {len(all_chunks)} chunks saved')