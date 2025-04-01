from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import chatbot

app = FastAPI()

class Message(BaseModel):
    message: str
    category: str

@app.post("/")
async def send_message(message: Message):
    response_text = chatbot(message.message, message.category)
    return {"response": response_text}
