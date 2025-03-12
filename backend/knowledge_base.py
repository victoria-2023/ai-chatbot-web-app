import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def build_vectorstore(directory):
    """
    Reads documents, extracts text, and stores embeddings in FAISS.
    """
    documents = []

    print(f"📂 Files found in '{directory}': {os.listdir(directory)}")

    for file in os.listdir(directory):
        print(f"🔄 Processing file: {file}")

        if file.endswith(".pdf"):
            loader = PyPDFLoader(f"{directory}/{file}")
        elif file.endswith(".txt"):
            loader = TextLoader(f"{directory}/{file}")
        else:
            print(f"⚠️ Skipping unsupported file: {file}")
            continue

        docs = loader.load()
        print(f"✅ Loaded {len(docs)} document chunks from {file}")
        documents.extend(docs)

    if not documents:
        print("🚨 ERROR: No documents found! Check your files.")
        return None

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    if not docs:
        print("🚨 ERROR: No text extracted! Check file content.")
        return None

    print(f"✅ Successfully processed {len(docs)} text chunks.")

    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    vectorstore = FAISS.from_documents(docs, embeddings)

    vectorstore.save_local("faiss_index")
    print("✅ FAISS index successfully saved!")

    return vectorstore

def load_vectorstore():
    """
    Loads FAISS index with deserialization protection.
    """
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    return FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
