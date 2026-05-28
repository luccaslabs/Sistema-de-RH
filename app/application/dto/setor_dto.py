from pydantic import BaseModel
from typing import Optional

class CriarSetorInput(BaseModel):
    nome: str
    descricao: Optional[str] = None

class SetorOutput(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    ativo: bool

    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import Optional, List

class CriarSetorInput(BaseModel):
    nome: str
    descricao: Optional[str] = None

class SetorOutput(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    ativo: bool

    class Config:
        from_attributes = True

class ListaSetoresOutput(BaseModel):
    total: int
    setores: List[SetorOutput]