from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.application.dto.funcionario_dto import FuncionarioOutput, CriarFuncionarioInput
from app.application.use_cases.funcionarios.criar_funcionario import CriarFuncionarioUseCase
from app.application.use_cases.funcionarios.atualizar_funcionario import AtualizarFuncionarioInput, AtualizarFuncionarioUseCase
from app.application.use_cases.funcionarios.listar_funcionarios import ListaFuncionariosOutput, ListarFuncionariosUseCase, ListarFuncionariosInput
from app.application.use_cases.funcionarios.desativar_funcionario import DesativarFuncionarioUseCase
from app.infrastructure.repositories.funcionario_repository_impl import FuncionarioRepositoryImpl
from app.infrastructure.repositories.setor_repository_impl import SetorRepositoryImpl
from app.domain.services.funcionario_service import FuncionarioService
from app.infrastructure.database.connection import get_db
from typing import Optional

router = APIRouter(prefix="/funcionarios", tags=["Funcionários"])

@router.post("/", response_model=FuncionarioOutput, status_code=201)
def criar_funcionario(
    dados: CriarFuncionarioInput,
    db: Session = Depends(get_db)
):
    try:
        use_case = CriarFuncionarioUseCase(
            funcionario_repo=FuncionarioRepositoryImpl(db),
            setor_repo=SetorRepositoryImpl(db),
            service=FuncionarioService()
        )
        return use_case.executar(dados)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
@router.get("/", response_model=ListaFuncionariosOutput)
def listar_funcionarios(
    setor_id: Optional[int] = None,
    apenas_ativos: bool = True,
    pagina: int = 1,
    por_pagina: int = 20,
    db: Session = Depends(get_db)
):
    use_case = ListarFuncionariosUseCase(FuncionarioRepositoryImpl(db))
    filtros = ListarFuncionariosInput(
        setor_id=setor_id,
        apenas_ativos=apenas_ativos,
        pagina=pagina,
        por_pagina=por_pagina,
    )
    return use_case.executar(filtros)

@router.patch("/{id}", response_model=FuncionarioOutput)
def atualizar_funcionario(
    id: int,
    dados: AtualizarFuncionarioInput,
    db: Session = Depends(get_db)
):
    try:
        use_case = AtualizarFuncionarioUseCase(
            funcionario_repo=FuncionarioRepositoryImpl(db),
            setor_repo=SetorRepositoryImpl(db),
            service=FuncionarioService()
        )
        return use_case.executar(id, dados)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.delete("/{id}", status_code=204)
def desativar_funcionario(
    id: int,
    db: Session = Depends(get_db)
):
    try:
        use_case = DesativarFuncionarioUseCase(FuncionarioRepositoryImpl(db))
        use_case.executar(id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))