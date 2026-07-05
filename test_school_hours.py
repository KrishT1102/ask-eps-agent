from search_agent import ask_eps_agent

questions = [
    "What time does school start?",
    "What are the school start times for elementary schools?",
    "When do high schools start?",
    "What time does middle school start?",
]

for q in questions:
    print(f'\nQ: {q}')
    print(f'A: {ask_eps_agent(q)}')
    print('-'*60)
