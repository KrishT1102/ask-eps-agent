import chromadb

# Load the persistent database
client = chromadb.PersistentClient(path='data/vectordb')
collection = client.get_collection('eps_knowledge')

def semantic_search(question, top_n=4):
    results = collection.query(
        query_texts=[question],
        n_results=top_n
)
    chunks = []
    for i, doc in enumerate(results['documents'][0]):
        meta = results['metadatas'][0][i]
        chunks.append({
            'text': doc,
            'source_url': meta['source_url'],
            'page_name': meta['page_name'],
        })
    return chunks

# Test with different phrasings of the same question
test_queries = [
    "When does school start?",
    "First day of classes",
    "school meal program",
    "my child needs a bus",
    "holiday break dates",
    "how to register new student",
]

for query in test_queries:
    print(f'\nQuery: {query}')
    results = semantic_search(query)
    for r in results[:2]:
        print(f' Page: {r["page_name"]}')
        print(f' Text: {r["text"][:100]}...')