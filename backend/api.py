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

# Bind the correct PORT for Railway
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # 🚨 Railway assigns a dynamic port
    uvicorn.run(app, host="0.0.0.0", port=port)
