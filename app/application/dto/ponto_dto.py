from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class ErroLinhaCSV(BaseModel):
    linha: int
    erro: str

class ValidacaoCSVOutput(BaseModel):
    valido: bool
    total_linhas: int
    erros: List[ErroLinhaCSV]

class ProcessarCSVOutput(BaseModel):
    upload_id: int
    status: str
    total_registros: int
    periodo_inicio: Optional[date]
    periodo_fim: Optional[date]
    erros: List[ErroLinhaCSV] = []