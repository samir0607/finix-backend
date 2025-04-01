from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import chatbot

app = FastAPI()

class Message(BaseModel):
    message: str
    category: int

@app.post("/")
async def send_message(message: Message, category: Message):
    response_text = chatbot(message.message, category.category)
    return {"response": response_text}
