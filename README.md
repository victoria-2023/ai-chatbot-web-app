# 🤖 AI Chatbot Web App

This is an AI-powered chatbot web application that answers user queries using a combination of a **retrieval-based knowledge system** (FAISS) and **LLM-based responses** (OpenAI API). The frontend is built with **Streamlit**, while the backend runs on **FastAPI**.

## 🚀 Features

- 🔍 **Retrieval-based answers**: Uses FAISS to fetch relevant knowledge from stored documents.
- 🌍 **Online search support**: Can fetch additional answers from the web (if enabled).
- 🧠 **LLM-powered responses**: Uses OpenAI’s GPT model to provide AI-generated answers.
- 📁 **Document-based knowledge retrieval**: Supports knowledge files stored in `.txt` and `.pdf` formats.

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Database**: FAISS (Vector Store)
- **ML & NLP**: OpenAI GPT (via API)
- **Deployment**: Railway (Backend), Streamlit Cloud (Frontend)

## 📂 Project Structure

```
ai-chatbot-web-app/
│── backend/
│   ├── api.py              # FastAPI backend
│   ├── chatbot.py          # Chatbot logic
│   ├── knowledge_base.py   # FAISS vector store and document handling
│── frontend/
│   ├── streamlit_app.py    # Streamlit frontend interface
│── data/
│   ├── documents/          # Knowledge base documents
│── faiss_index/            # FAISS stored index (not pushed to GitHub)
│── .gitignore              # Ignored files (env, faiss_index, venv, etc.)
│── requirements.txt        # Python dependencies
│── Procfile                # Deployment config (if using Railway/Heroku)
│── README.md               # This file
```

## 🔧 Installation & Setup

1. **Clone the Repository**
   ```sh
   git clone https://github.com/your-username/ai-chatbot-web-app.git
   cd ai-chatbot-web-app
   ```

2. **Set up a virtual environment**
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Create a `.env` file in the project root and add:
     ```
     OPENAI_API_KEY=your-openai-api-key
     SERP_API_KEY=your-serp-api-key  # Optional for web search
     ```

5. **Build the FAISS index from documents** (if needed)
   ```sh
   python -c "from backend.knowledge_base import build_vectorstore; build_vectorstore('data/documents/')"
   ```

6. **Run the Backend (FastAPI)**
   ```sh
   uvicorn backend.api:app --reload
   ```

7. **Run the Frontend (Streamlit)**
   ```sh
   streamlit run frontend/streamlit_app.py
   ```

## 🚀 Deployment

- **Backend**: Deploy on **Railway**, **Render**, or **Heroku**.
- **Frontend**: Deploy on **Streamlit Cloud**.

## 🛠️ Troubleshooting

- If FAISS errors occur, ensure `index.faiss` is built and available.
- If `API Error: Unable to connect`, check that the backend is running.
- Ensure `.env` file is correctly set up with API keys.

