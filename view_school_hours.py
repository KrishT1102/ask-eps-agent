import json

with open('data/chunks/all_chunks.json') as f:
    chunks = json.load(f)

sh = [c for c in chunks if 'school_hours' in c['id']][0]
print(f"School Hours Chunk Text ({len(sh['text'])} chars):\n")
print(sh['text'][:1000])
print("\n...")
print(sh['text'][-500:])
