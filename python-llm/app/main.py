from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from services.llm_service import LLMService
import sys

sys.path = sys.path + ["./app"]


load_dotenv()


app = FastAPI()

llm_service = LLMService()


class TextData(BaseModel):
    text: str
    lang: str = "en"


@app.post("/summarize")
async def summarize(data: TextData):
    text = data.text
    language = data.lang
    print(language)

    summary = llm_service.summarize_text(text, language)

    return {"summary": summary}


# Rota inicial para testar a API
@app.get("/")
async def root():
    return {"message": "API is running"}
