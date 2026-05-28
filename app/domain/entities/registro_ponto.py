from dataclasses import dataclass
from datetime import date, time, datetime
from typing import Optional

@dataclass
class RegistroPonto:
    funcionario_id: int
    upload_id: int
    data: date
    hora_entrada: Optional[time] = None
    hora_saida: Optional[time] = None
    minutos_trabalhados: int = 0
    minutos_atraso: int = 0
    minutos_hora_extra: int = 0
    falta: bool = False
    criado_em: Optional[datetime] = None
    id: Optional[int] = None