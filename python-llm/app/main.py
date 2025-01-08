from services.llm_service import LLMService
from pydantic import BaseModel
from fastapi import FastAPI
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path = sys.path + ["./app"]


app = FastAPI()
llm_service = LLMService()


class TextData(BaseModel):
    text: str
    language: str = "en"  # Valor padrão para o idioma


@app.post("/summarize")
async def summarize(data: TextData):
    text = data.text
    language = data.language

    summary = llm_service.summarize_text(text, language)

    return {"summary": summary}


# Rota inicial para testar a API
@app.get("/")
async def root():
    return {"message": "API is running"}
