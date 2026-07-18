import streamlit as st
import chromadb
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title='Ask EPS', page_icon='■', layout='centered')

# EPS Brand colors: Blue #003087, White, Gold #FFB81C
st.markdown('''
<style>
    .stApp { background-color: #f0f4ff; }
    .stChatMessage { border-radius: 12px; }
    h1 { color: #003087 !important; }
</style>
''', unsafe_allow_html=True)

# Sidebar with info
with st.sidebar:
    st.image('https://www.everettsd.org/cms/lib/WA01001955/Centricity/Template/GlobalAssets/images/logos/eps-logo.png',
             width=150)
    st.markdown('### About This App')
    st.markdown('Built by **Krish [LastName]**')
    st.markdown('Rising 11th Grade — Everett Public Schools')
    st.markdown('Summer 2025 Project')
    st.divider()
    st.markdown('**How it works:**')
    st.markdown('1. Your question is searched against EPS website content')
    st.markdown('2. Most relevant sections are found using AI')
    st.markdown('3. Claude answers using only official EPS content')
    st.divider()
    if st.button('Clear Conversation'):
        st.session_state.messages = []
        st.rerun()

# Load agent — cached so it only loads once
@st.cache_resource
def load_agent():
    client = chromadb.PersistentClient(path='data/vectordb')
    collection = client.get_collection('eps_knowledge')
    ai = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    return collection, ai

collection, ai_client = load_agent()
def ask_eps(question):
    results = collection.query(query_texts=[question], n_results=4)
    context = ''
    for i, doc in enumerate(results['documents'][0]):
        meta = results['metadatas'][0][i]
        context += f'[Source: {meta["source_url"]}]\n{doc}\n\n'
    msg = ai_client.messages.create(
        model='claude-sonnet-4-6', max_tokens=600,
        messages=[{'role':'user','content':f'''You are a helpful assistant
for Everett Public Schools. Answer ONLY from the context below.
If not found say: I could not find this on the EPS website.
End with the source URL.
CONTEXT: {context}
QUESTION: {question}'''}]
    )
    return msg.content[0].text

# Page header
st.title('■ Ask EPS Agent')
st.caption('Ask anything about Everett Public Schools — answers from the official website')
st.divider()

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        'role':'assistant',
        'content':'Hi! I am the EPS AI assistant. Ask me anything about Everett Public Schools!'
    })

# Show suggested questions only at start
if len(st.session_state.messages) <= 1:
    st.markdown('**Try asking:**')
    cols = st.columns(2)
    suggestions = [
    "When does school start?",
    "How do I apply for free lunch?",
    "What are the school hours?",
    "When is spring break?",
]
for i, s in enumerate(suggestions):
    if cols[i%2].button(s):
        st.session_state.messages.append({'role':'user','content':s})
        with st.chat_message('user'): st.write(s)
        with st.chat_message('assistant'):
            with st.spinner('Searching...'):
                answer = ask_eps(s)
            st.write(answer)
        st.session_state.messages.append({'role':'assistant','content':answer})
        st.rerun()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.write(msg['content'])

# Chat input
if prompt := st.chat_input('Ask about EPS...'):
    # Show user message
    st.session_state.messages.append({'role':'user','content':prompt})
    with st.chat_message('user'):
        st.write(prompt)
    # Get and show agent answer
    with st.chat_message('assistant'):
        with st.spinner('Searching EPS website...'):
            answer = ask_eps(prompt)
        st.write(answer)
    st.session_state.messages.append({'role':'assistant','content':answer})