import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from .knowledge_base import load_vectorstore

# Load environment variables
load_dotenv()

# API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

# Validate OpenAI key
if not OPENAI_API_KEY:
    raise ValueError("🚨 ERROR: OPENAI_API_KEY is missing! Please check your .env file.")

# Initialize OpenAI chat model
llm = ChatOpenAI(api_key=OPENAI_API_KEY)

# Load your vectorstore (knowledge base)
vectorstore = load_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": 5, "score_threshold": 0.4})

def search_online(query):
    if not SERP_API_KEY:
        return None

    try:
        url = f"https://serpapi.com/search?q={query}&api_key={SERP_API_KEY}"
        response = requests.get(url)
        data = response.json()
        if "organic_results" in data and len(data["organic_results"]) > 0:
            return data["organic_results"][0].get("snippet", None)
        return None
    except requests.RequestException:
        return None

def get_response(question):
    try:
        # First, try to fetch from your local documents
        results = retriever.invoke(question)
        if results:
            return results[0].page_content

        # If nothing found locally, try OpenAI (like ChatGPT)
        ai_response = llm.invoke(question)
        if hasattr(ai_response, "content"):
            return ai_response.content
        return str(ai_response)

    except Exception as e:
        # If OpenAI fails, try SerpAPI as a fallback
        online_result = search_online(question)
        if online_result:
            return online_result
        return f"⚠️ Sorry, something went wrong: {str(e)}"
