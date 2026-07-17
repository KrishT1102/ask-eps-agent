import chromadb

# Create a local ChromaDB database
client = chromadb.Client()
collection = client.create_collection('test')

# Add some sample sentences
collection.add(
    documents=[
        "School lunch is served at noon",
        "Spring break starts March 24",
        "Basketball tryouts are in October",
        "Free meals available for qualifying students",
    ],
    ids=["1","2","3","4"]
)

# Search by MEANING not keywords
results = collection.query(
    query_texts=["What time is the student meal?"],
    n_results=2
)

print('Query: What time is the student meal?')
print('Top results:')
for doc in results['documents'][0]:
    print(f' -> {doc}')