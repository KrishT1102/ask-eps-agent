import json

with open('data/chunks/all_chunks.json') as f:
    chunks = json.load(f)

school_chunks = [c for c in chunks if 'school_hours' in c['id']]
print(f'School hours chunks: {len(school_chunks)}')
for c in school_chunks:
    print(f"\nID: {c['id']}")
    print(f"Text: {c['text'][:200]}")
