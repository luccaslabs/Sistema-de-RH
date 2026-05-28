from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

@dataclass
class UploadCsv:
    nome_arquivo: str
    status: str = "processando"     # processando | concluido | erro
    total_registros: int = 0
    periodo_inicio: Optional[date] = None
    periodo_fim: Optional[date] = None
    erro_detalhe: Optional[str] = None
    data_upload: Optional[datetime] = None
    id: Optional[int] = None