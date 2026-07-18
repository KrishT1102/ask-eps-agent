import streamlit as st
from chroma_agent import ask_eps

# Page configuration — always first line
st.set_page_config(
    page_title="Ask EPS",
    page_icon="■",
    layout="centered"

)

# Title and description
st.title("■ Ask EPS Agent")
st.markdown("**Ask anything about Everett Public Schools**")
st.markdown("*Powered by AI — answers come from the official EPS website*")

# Simple input and output
question = st.text_input("Type your question here:", "")
ask_clicked = st.button('Ask')

if ask_clicked and question.strip():
    st.write(f"You asked: {question}")
    with st.spinner('Searching EPS knowledge base...'):
        try:
            answer = ask_eps(question.strip())
            st.success('Answer')
            st.write(answer)
        except Exception as exc:
            st.error(f'Could not generate an answer. {exc}')