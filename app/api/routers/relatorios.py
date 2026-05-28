from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.application.dto.relatorio_dto import RelatorioSetorOutput, ComparativoOutput
from app.application.use_cases.relatorios.gerar_relatorio_setor import GerarRelatorioSetorUseCase
from app.application.use_cases.relatorios.gerar_comparativo_setores import GerarComparativoSetoresUseCase
from app.infrastructure.repositories.setor_repository_impl import SetorRepositoryImpl
from app.infrastructure.repositories.funcionario_repository_impl import FuncionarioRepositoryImpl
from app.infrastructure.repositories.registro_ponto_repository_impl import RegistroPontoRepositoryImpl
from app.infrastructure.repositories.relatorio_mensal_repository_impl import RelatorioMensalRepositoryImpl
from app.infrastructure.ai.analisador_ia_impl import AnalisadorIAImpl
from app.infrastructure.database.connection import get_db

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])


def _deps(db: Session):
    """Monta as dependências comuns dos use cases de relatório."""
    return dict(
        setor_repo=SetorRepositoryImpl(db),
        funcionario_repo=FuncionarioRepositoryImpl(db),
        registro_repo=RegistroPontoRepositoryImpl(db),
        relatorio_repo=RelatorioMensalRepositoryImpl(db),
        analisador=AnalisadorIAImpl(),
    )


@router.get("/{setor_id}", response_model=RelatorioSetorOutput)
def relatorio_setor(
    setor_id: int,
    mes: str,           # query param — ex: 2026-05
    db: Session = Depends(get_db),
):
    try:
        use_case = GerarRelatorioSetorUseCase(**_deps(db))
        return use_case.executar(setor_id, mes)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/comparativo/setores", response_model=ComparativoOutput)
def comparativo_setores(
    mes: str,           # query param — ex: 2026-05
    db: Session = Depends(get_db),
):
    try:
        use_case = GerarComparativoSetoresUseCase(**_deps(db))
        return use_case.executar(mes)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))