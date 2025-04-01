from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import chatbot

app = FastAPI()

class Message(BaseModel):
    query: str
    category: str

@app.post("/")
async def send_message(message: Message):
    print(type(message.category))
    response_text = chatbot(message.query, message.category)
    return {"response": response_text}
