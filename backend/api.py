import uvicorn
import os
from fastapi import FastAPI
from pydantic import BaseModel
from backend.chatbot import get_response  # Ensure correct import

# Initialize FastAPI
app = FastAPI()

class Query(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "✅ AI Chatbot API is running!"}

@app.post("/chat")
def chat(query: Query):
    response = get_response(query.question)
    return {"response": response}

# Ensure Railway assigns the correct PORT
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Use Railway-assigned port
    uvicorn.run(app, host="0.0.0.0", port=port)
