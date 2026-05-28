from dataclasses import dataclass
from typing import Optional

@dataclass
class Setor:
    nome: str
    descricao: Optional[str] = None
    ativo: bool = True
    id: Optional[int] = None