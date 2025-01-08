from typing import Optional
import os
from langchain_openai import OpenAI


class LLMService:
    LANGUAGES = ['pt', 'en', 'es']

    def __init__(self):
        # Garantir que HF_TOKEN esteja configurada corretamente
        hf_token = os.getenv("HF_TOKEN")
        if not hf_token:
            raise ValueError(
                "HF_TOKEN não está configurado. Defina a variável de ambiente.")

        # Inicializa o LLM com a chave de API
        self.llm = OpenAI(
            temperature=0.5,
            top_p=0.7,
            api_key=hf_token,  # type: ignore
            base_url="https://api-inference.huggingface.co/models/Qwen/Qwen2.5-72B-Instruct/v1",
        )

    def translate_text(self, text: str, target_language: str) -> str:
        """Traduz o texto para o idioma desejado, se necessário."""
        if target_language not in self.LANGUAGES:
            raise ValueError("Idioma não suportado para tradução.")

        # Só traduz se o idioma de destino for diferente do idioma original
        if target_language == "pt":
            return self.llm.invoke(
                f"Traduza o seguinte texto para o português: {
                    text}"  # Prompt em português
            )
        elif target_language == "es":
            return self.llm.invoke(
                f"Traduza o seguinte texto para o espanhol: {
                    text}"  # Prompt em espanhol
            )

        # Se for 'en', retorna o texto original sem tradução
        return text

    def summarize_text(self, text: str, language: str = "en") -> Optional[str]:
        """Gera um resumo no idioma especificado."""
        if not text:
            raise ValueError("O texto a ser resumido não pode estar vazio.")

        if language not in self.LANGUAGES:
            raise ValueError(
                f"Idioma '{language}' não é suportado para resumo.")

        # Traduz o texto original para o idioma desejado, se necessário
        if language != "en" and language != "es":
            try:
                text = self.translate_text(text, language)
            except Exception as e:
                raise RuntimeError(f"Erro ao traduzir o texto: {e}")

        # Criar o prompt para resumo
        prompt = f"Resuma o seguinte texto em {language}: {text}"

        try:
            response = self.llm.invoke(prompt)  # Invoca o modelo para resumo
            return response.strip() if response else "Resumo não encontrado."
        except Exception as e:
            raise RuntimeError(f"Erro ao gerar o resumo: {e}")
