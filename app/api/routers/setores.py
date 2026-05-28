from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.application.dto.setor_dto import CriarSetorInput, SetorOutput, ListaSetoresOutput
from app.application.use_cases.setores.criar_setor import CriarSetorUseCase
from app.application.use_cases.setores.listar_setores import ListarSetoresUseCase
from app.infrastructure.repositories.setor_repository_impl import SetorRepositoryImpl
from app.domain.services.setor_service import SetorService
from app.infrastructure.database.connection import get_db

router = APIRouter(prefix="/setores", tags=["Setores"])

@router.post("/", response_model=SetorOutput, status_code=201)
def criar_setor(
    dados: CriarSetorInput,
    db: Session = Depends(get_db)
):
    try:
        use_case = CriarSetorUseCase(
            setor_repo=SetorRepositoryImpl(db),
            service=SetorService()
        )
        return use_case.executar(dados)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("/", response_model=ListaSetoresOutput)
def listar_setores(db: Session = Depends(get_db)):
    use_case = ListarSetoresUseCase(SetorRepositoryImpl(db))
    return use_case.executar()