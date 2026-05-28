from pydantic import BaseModel, EmailStr
from datetime import date, time
from typing import Optional, List

class CriarFuncionarioInput(BaseModel):
    nome: str
    email: EmailStr
    setor_id: int
    cargo: Optional[str] = None
    data_admissao: date
    horario_esperado_entrada: time = time(8, 0)
    horario_esperado_saida: time = time(17, 0)

class AtualizarFuncionarioInput(BaseModel):
    nome: Optional[str] = None
    cargo: Optional[str] = None
    setor_id: Optional[int] = None
    horario_esperado_entrada: Optional[time] = None
    horario_esperado_saida: Optional[time] = None

class ListarFuncionariosInput(BaseModel):
    setor_id: Optional[int] = None
    apenas_ativos: bool = True
    pagina: int = 1
    por_pagina: int = 20

class FuncionarioOutput(BaseModel):
    id: int
    nome: str
    email: str
    cargo: Optional[str]
    setor_id: int
    data_admissao: date
    horario_esperado_entrada: time
    horario_esperado_saida: time
    ativo: bool

    class Config:
        from_attributes = True


class ListaFuncionariosOutput(BaseModel):
    total: int       
    pagina: int
    por_pagina: int
    paginas: int      
    funcionarios: List[FuncionarioOutput]