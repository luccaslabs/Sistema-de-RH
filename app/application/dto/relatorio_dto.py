from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class FuncionarioRelatorioOutput(BaseModel):
    funcionario_id: int
    nome: str
    horas_trabalhadas: float
    atrasos: int
    faltas: int
    horas_extras: float


class GraficoDiarioOutput(BaseModel):
    data: str
    media_horas: float


class GraficoSemanalOutput(BaseModel):
    semana: str
    total_atrasos: int


class RelatorioSetorOutput(BaseModel):
    setor_id: int
    setor: str
    periodo: str
    resumo: dict
    funcionarios: List[FuncionarioRelatorioOutput]
    grafico_horas_diarias: List[GraficoDiarioOutput]
    grafico_atrasos_por_semana: List[GraficoSemanalOutput]
    insight_llm: Optional[str]
    gerado_em: Optional[datetime]


class ComparativoSetorOutput(BaseModel):
    setor: str
    media_horas: float
    total_atrasos: int
    total_faltas: int
    total_horas_extras: float


class ComparativoOutput(BaseModel):
    periodo: str
    setores: List[ComparativoSetorOutput]