import os
import requests
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from .knowledge_base import load_vectorstore

# Load environment variables
load_dotenv()

# Get API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

# Validate API key existence
if not OPENAI_API_KEY:
    raise ValueError("🚨 ERROR: OPENAI_API_KEY is missing! Please check your .env file.")

# Initialize LLM
llm = ChatOpenAI(api_key=OPENAI_API_KEY)

# Load FAISS vector store (knowledge base retrieval)
vectorstore = load_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": 5, "score_threshold": 0.4})

def search_online(query):
    """
    Fetches real-time data using SerpAPI (Google Search API).
    """
    if not SERP_API_KEY:
        return "I don't have access to online search at the moment."

    url = f"https://serpapi.com/search?q={query}&api_key={SERP_API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()
        if "organic_results" in data and len(data["organic_results"]) > 0:
            return data["organic_results"][0]["snippet"]
        return "I couldn't find anything online for that."
    except requests.RequestException as e:
        return f"🌐 Online Search Error: {str(e)}"

def get_response(question):
    """
    Combines AI model, knowledge base retrieval, and online search.
    """
    try:
        # 🔹 Try retrieving from FAISS knowledge base
        retrieved_docs = retriever.get_relevant_documents(question)
        if retrieved_docs:
            best_answer = retrieved_docs[0].page_content
            return f"📚 Here's what I found in my knowledge base:\n\n{best_answer}"

        # 🔹 If nothing is found, use online search
        online_result = search_online(question)
        if "I don't have access" not in online_result:
            return f"🌐 Here's what I found online:\n\n{online_result}"

        # 🔹 Default to LLM for open-ended questions
        return llm.predict(question)

    except Exception as e:
        return f"🚨 ERROR: {str(e)}"
