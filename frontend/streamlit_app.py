import streamlit as st
import requests

# Set the backend API URL
API_URL = "https://ai-chatbot-web-app-production.up.railway.app/chat"

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
    try:
        response = requests.post(API_URL, json={"question": prompt})
        response_data = response.json()

        # Display AI Response
        with st.chat_message("assistant"):
            st.markdown(response_data.get("response", "⚠️ Error: No response received."))

        st.session_state.messages.append({"role": "assistant", "content": response_data.get("response", "⚠️ Error: No response received.")})

    except Exception as e:
        with st.chat_message("assistant"):
            st.markdown(f"⚠️ Error: Unable to connect to API.\n\n{str(e)}")
