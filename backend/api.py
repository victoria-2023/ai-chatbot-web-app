from fastapi import FastAPI
from pydantic import BaseModel
from backend.chatbot import get_response  # Correct import

app = FastAPI()

class Query(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "AI Chatbot API is running!"}

@app.post("/chat")
def chat(query: Query):
    response = get_response(query.question)
    return {"response": response}
