import json
import os
from dotenv import load_dotenv
from rank_bm25 import BM25Okapi

load_dotenv(override=True)

with open('data/chunks/all_chunks.json') as f:
    chunks = json.load(f)

# Create search index
tokenized = [c['text'].lower().split() for c in chunks]
bm25 = BM25Okapi(tokenized)

# Test what chunks are retrieved for school hours
query = "What are the school hours?"
scores = bm25.get_scores(query.lower().split())
top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:6]

print(f"Query: {query}\n")
print("Top 6 retrieved chunks:\n")

for rank, idx in enumerate(top_indices, 1):
    chunk = chunks[idx]
    score = scores[idx]
    text_preview = chunk['text'][:150].replace('\n', ' ')
    print(f"{rank}. [{chunk['page_name']}] Score: {score:.2f}")
    print(f"   {text_preview}...\n")
