import streamlit as st
import requests

# Set Page Title & Styling
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")
st.markdown(
    """
    <style>
        .stChatMessage { font-size: 16px; }
        .stTextInput > div > div > input { font-size: 18px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Chatbot Header
st.title("🤖 AI-Powered Virtual Assistant")
st.write("Ask me anything from my knowledge base!")

# Chat Message History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
prompt = st.chat_input("Type your question here...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send to API
    response = requests.post("http://localhost:8000/chat", json={"question": prompt}).json()

    # Display AI Response
    with st.chat_message("assistant"):
        st.markdown(response["response"])

    st.session_state.messages.append({"role": "assistant", "content": response["response"]})