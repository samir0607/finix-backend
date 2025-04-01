from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import chatbot

app = FastAPI()

class Message(BaseModel):
    query: str
    category: int

@app.post("/")
async def send_message(message: Message):
    response_text = chatbot(message.query, message.category)
    return {"response": response_text}
