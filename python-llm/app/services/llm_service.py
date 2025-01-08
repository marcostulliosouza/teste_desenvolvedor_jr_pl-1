import os
from langchain_openai import OpenAI
from typing import Optional


class LLMService:
    LANGUAGES = ['pt', 'en', 'es']

    def __init__(self):
        # Garantir que HF_TOKEN esteja configurada corretamente
        hf_token = os.getenv("HF_TOKEN")
        if not hf_token:
            raise ValueError(
                "HF_TOKEN não está configurado. Defina a variável de ambiente.")

        # Aqui assumimos que há uma variável de ambiente HF_TOKEN configurada.
        self.llm = OpenAI(
            temperature=0.5,
            top_p=0.7,
            api_key=hf_token,  # type: ignore
            base_url="https://api-inference.huggingface.co/models/Qwen/Qwen2.5-72B-Instruct/v1",
        )

    def translate_text(self, text: str, target_language: str) -> str:
        """ Função para traduzir o texto para o idioma desejado."""
        if target_language == 'pt':
            translate_text = self.llm.invoke(
                f"Translate the following text to Portuguese: {text}")
        elif target_language == "es":
            translate_text = self.llm.invoke(
                f"Translate the following text to Spanish: {text}")
        else:
            translate_text = text  # Se o idioma for inglês ou não for necessário traduzir
        return translate_text

    def summarize_text(self, text: str, language: str = "en") -> Optional[str]:
        if not text:
            raise ValueError("O texto a ser resumido não pode estar vazio.")

        if language not in self.LANGUAGES:
            raise ValueError("O texto a ser resumido não pode estar vazio.")

        translate_text = self.translate_text(text, language)

        # Formatando o prompt para que o modelo entenda a tarefa
        prompt = f"Resuma o seguinte texto em {language}: {translate_text}"

        try:
            response = self.llm.invoke(prompt)  # Invocando o modelo
            return response.strip() if response else "Resumo não encontrado."
        except Exception as e:
            raise RuntimeError(f"Erro ao gerar o resumo: {e}")
