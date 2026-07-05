import json
from rank_bm25 import BM25Okapi

with open('data/chunks/all_chunks.json') as f:
    chunks = json.load(f)

print(f'Total chunks: {len(chunks)}')

# Create search index
tokenized = [c['text'].lower().split() for c in chunks]
bm25 = BM25Okapi(tokenized)

# Test queries
test_queries = [
    "When is spring break?",
    "What time does school start?",
    "school hours",
    "school start times",
]

for query in test_queries:
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print(f"{'='*60}")
    
    scores = bm25.get_scores(query.lower().split())
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:6]
    
    for rank, idx in enumerate(top_indices, 1):
        chunk = chunks[idx]
        score = scores[idx]
        text_preview = chunk['text'][:120].replace('\n', ' ')
        print(f"\n{rank}. Score: {score:.2f}")
        print(f"   Page: {chunk['page_name']}")
        print(f"   ID: {chunk['id']}")
        print(f"   Text: {text_preview}...")
