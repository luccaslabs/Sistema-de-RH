from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.application.dto.ponto_dto import ProcessarCSVOutput
from app.application.use_cases.ponto.processar_csv import ProcessarCSVUseCase
from app.infrastructure.repositories.upload_csv_repository_impl import UploadCsvRepositoryImpl
from app.infrastructure.repositories.registro_ponto_repository_impl import RegistroPontoRepositoryImpl
from app.infrastructure.repositories.funcionario_repository_impl import FuncionarioRepositoryImpl
from app.infrastructure.database.connection import get_db

router = APIRouter(prefix="/ponto", tags=["Ponto"])

@router.post("/upload", response_model=ProcessarCSVOutput, status_code=201)
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # valida extensão
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Apenas arquivos .csv são aceitos.")

    conteudo = await file.read()

    use_case = ProcessarCSVUseCase(
        upload_repo=UploadCsvRepositoryImpl(db),
        registro_repo=RegistroPontoRepositoryImpl(db),
        funcionario_repo=FuncionarioRepositoryImpl(db),
    )

    return use_case.executar(
        nome_arquivo=file.filename,
        conteudo=conteudo,
    )