from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import chatbot

app = FastAPI()

class Message(BaseModel):
    message: str

@app.post("/")
async def send_message(message: Message):
    response_text = chatbot(message.message)
    return {"response": response_text}
