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
        # Só traduz se o idioma de destino for diferente do idioma original
        if target_language == "pt":
            prompt = f"Por favor, traduza o seguinte texto para o português de forma clara e precisa:\n\n{
                text}"
        elif target_language == "es":
            prompt = f"Por favor, traduzca el siguiente texto al español de manera clara y precisa:\n\n{
                text}"
        else:
            # Se for 'en' ou idioma já suportado, retorna o texto original
            return text

        try:
            return self.llm.invoke(prompt).strip()
        except Exception as e:
            raise RuntimeError(f"Erro ao traduzir o texto: {e}")

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
        prompt = (
            f"Você é um assistente especializado em linguagem natural. Seu objetivo é criar um resumo claro e objetivo, "
            f"capturando os principais pontos do texto fornecido. O resumo deve ser no idioma especificado ({
                language}) e "
            f"ter entre 3 e 5 frases curtas, mantendo a essência e o contexto do texto. Certifique-se de não repetir ideias "
            f"ou incluir detalhes desnecessários.\n\nTexto para resumir:\n{
                text}"
        )

        try:
            response = self.llm.invoke(prompt)  # Invoca o modelo para resumo
            return response.strip() if response else "Resumo não encontrado."
        except Exception as e:
            raise RuntimeError(f"Erro ao gerar o resumo: {e}")
