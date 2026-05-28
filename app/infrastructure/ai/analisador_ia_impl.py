import os
import requests
from app.domain.ports.analisador_ia import IAnalisadorIA


class AnalisadorIAImpl(IAnalisadorIA):

    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.model   = "claude-sonnet-4-20250514"
        self.url     = "https://api.anthropic.com/v1/messages"

    def gerar_insight_setor(
        self,
        nome_setor: str,
        mes: str,
        total_funcionarios: int,
        media_horas_trabalhadas: float,
        total_atrasos: int,
        total_faltas: int,
        total_horas_extras: float,
    ) -> str:

        prompt = f"""
Você é um analista de RH. Analise os dados de ponto do setor abaixo e gere um
insight objetivo em 2 a 3 frases, destacando pontos de atenção e aspectos positivos.

Setor: {nome_setor}
Mês: {mes}
Total de funcionários: {total_funcionarios}
Média de horas trabalhadas: {media_horas_trabalhadas:.1f}h
Total de atrasos: {total_atrasos}
Total de faltas: {total_faltas}
Total de horas extras: {total_horas_extras:.1f}h

Responda apenas com o texto do insight, sem títulos ou marcadores.
        """.strip()

        response = requests.post(
            self.url,
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": self.model,
                "max_tokens": 300,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30,
        )

        response.raise_for_status()
        data = response.json()
        return data["content"][0]["text"].strip()