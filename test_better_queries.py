from search_agent import ask_eps_agent

print("Building search index...")
print("\nTesting with BETTER search queries:\n")

queries = [
    ("What are the school hours?", "school hours query"),
    ("What time do schools start?", "school time query"),
    ("Elementary school start time", "specific level query"),
    ("When does school start?", "when query"),
]

for q, desc in queries:
    print(f"Q: {q} ({desc})")
    try:
        answer = ask_eps_agent(q)
        print(f"A: {answer[:200]}...\n" if len(answer) > 200 else f"A: {answer}\n")
    except Exception as e:
        print(f"Error: {str(e)[:100]}\n")
