# Run your 20 test questions through both agents

# Score each: 1 = correct, 0.5 = partial, 0 = wrong
test_questions = [
    # Paste your 20 questions from Week 1 here
    "When does school start in September 2026?",
    "When is spring break?",
    "How do I apply for free lunch?",
    "What time does school start?",
    "How do I enroll a new student?",
    "What is the school meal program?",
    "How do I get a bus for my child?",
    "What are the holiday break dates?",
    "What does IB stand for, and how long is the program?",
    "What grade levels does the Advanced Learning program serve?",
    "What distinguishes Sequoia High School from other schools mentioned?",
    "What is the purpose of the 'Family Engagement' program?",
    "What is the 'Student Support Services' program, and who is it for?",
    "What is the 'Special Education' program, and who is it for?",
    "What is the 'English Language Learners' program, and who is it for?",
    "What is the 'Career and Technical Education' program, and who is it for?",
    "What is the 'Athletics' program, and who is it for?",
    "What is the 'Fine Arts' program, and who is it for?",
    "What is the 'Health and Wellness' program, and who is it for?",
    "What is the 'Transportation' program, and who is it for?"

]

# Score manually after running each agent
bm25_scores = [1, 0.5, 1, 1, 0.5, 1, 1, 0.5, 1, 1, 1, 0.5, 0.5, 1, 1, 1, 1, 0.5, 0.5, 1] # Fill in after running search_agent.py
chroma_scores = [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0.5, 1, 0.5, 1, 1, 1, 1] # Filled from the scored transcript above

# Calculate accuracy safely (avoid division by zero when lists are still empty)
def calculate_accuracy(scores):
    if not scores:
        return None
    return sum(scores) / len(scores) * 100

bm25_accuracy = calculate_accuracy(bm25_scores)
chroma_accuracy = calculate_accuracy(chroma_scores)

if bm25_accuracy is None or chroma_accuracy is None:
    print('Add at least one score to both bm25_scores and chroma_scores before calculating accuracy.')
else:
    improvement = chroma_accuracy - bm25_accuracy
    print(f'BM25 Accuracy: {bm25_accuracy:.0f}%')
    print(f'ChromaDB Accuracy: {chroma_accuracy:.0f}%')
    print(f'Improvement: +{improvement:.0f}%')
    print(f'This goes in your college application!')