import json
from rank_bm25 import BM25Okapi

with open('data/chunks/all_chunks.json') as f:
    chunks = json.load(f)

# Create search index
tokenized = [c['text'].lower().split() for c in chunks]
bm25 = BM25Okapi(tokenized)

# Test what chunks are retrieved for school hours
query = "What are the school hours?"
scores = bm25.get_scores(query.lower().split())

# Find school_hours chunk
for i, chunk in enumerate(chunks):
    if chunk['id'] == 'school_hours_chunk_0':
        score = scores[i]
        print(f"school_hours_chunk_0 score: {score:.4f}")
        print(f"Rank: {sorted(enumerate(scores), key=lambda x: x[1], reverse=True).index((i, score)) + 1} out of {len(chunks)}")
        print(f"\nFirst 300 chars of school_hours chunk:")
        print(chunk['text'][:300])
