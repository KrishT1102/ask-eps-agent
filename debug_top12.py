import os
from dotenv import load_dotenv
from rank_bm25 import BM25Okapi
import json

load_dotenv(override=True)

with open('data/chunks/all_chunks.json') as f:
    chunks = json.load(f)

# Create search index  
tokenized = [c['text'].lower().split() for c in chunks]
bm25 = BM25Okapi(tokenized)

# Simulate what ask_eps_agent does
question = "What are the school hours?"
scores = bm25.get_scores(question.lower().split())
top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:12]
relevant = [chunks[i] for i in top_indices]

print(f"Question: {question}")
print(f"Top 12 retrieved chunks:\n")

school_hours_found = False
for i, chunk in enumerate(relevant, 1):
    print(f"{i}. {chunk['page_name']} ({chunk['id']})")
    if 'school_hours' in chunk['id']:
        school_hours_found = True
        print(f"   ^^^ SCHOOL HOURS FOUND! Preview: {chunk['text'][:100]}")

print(f"\nSchool hours in top 12: {school_hours_found}")

# Find school_hours ranking
for i, chunk in enumerate(chunks):
    if chunk['id'] == 'school_hours_chunk_0':
        rank = sorted(enumerate(scores), key=lambda x: x[1], reverse=True).index((i, scores[i])) + 1
        print(f"Actual rank of school_hours: {rank} out of {len(chunks)}")
        break
