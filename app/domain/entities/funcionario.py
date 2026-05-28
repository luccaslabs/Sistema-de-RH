from dataclasses import dataclass
from datetime import date, time
from typing import Optional

@dataclass
class Funcionario:
    nome: str
    email: str
    setor_id: int
    data_admissao: date
    horario_esperado_entrada: time
    horario_esperado_saida: time
    cargo: Optional[str] = None
    ativo: bool = True
    id: Optional[int] = None