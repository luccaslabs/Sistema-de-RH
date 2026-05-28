from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class RelatorioMensal:
    setor_id: int
    mes: str                          # formato YYYY-MM
    media_horas_trabalhadas: float = 0.0
    total_atrasos: int = 0
    total_faltas: int = 0
    total_horas_extras: float = 0.0
    insight_llm: Optional[str] = None
    gerado_em: Optional[datetime] = None
    id: Optional[int] = None