from typing import List, Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageItem(BaseModel):
    id: Union[int, str]
    sender: str
    content: str
    type: str = "text"

class ChatRequest(BaseModel):
    input: List[MessageItem]

llm = ChatOllama(
    model="llama3.2",
    temperature=0.7,
    num_predict=120
)

SYSTEM_PROMPT = SystemMessage(
    content=("Você é a Niza, uma assistente virtual amigável focada exclusivamente em finanças pessoais, planejamento financeiro e investimentos. Responda de forma clara, prática e em português do Brasil."
    "REGRA OBRIGATÓRIA: Responda de forma curta, prática e direta, "
    "com no máximo 3 frases ou 300 caracteres. Seja extremamente objetiva.")
)

@app.post("/robo")
async def chat_niza(payload: ChatRequest):
    try:
        formatted_messages = [SYSTEM_PROMPT]

        for msg in payload.input:
            if msg.sender == "user":
                formatted_messages.append(HumanMessage(content=msg.content))
            elif msg.sender == "bot":
                formatted_messages.append(AIMessage(content=msg.content))

        response = await llm.ainvoke(formatted_messages)

        return {"reply": response.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))