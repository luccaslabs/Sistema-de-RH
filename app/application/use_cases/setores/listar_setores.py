from app.application.dto.setor_dto import ListaSetoresOutput, SetorOutput
from app.domain.ports.setor_repository import ISetorRepository

class ListarSetoresUseCase:

    def __init__(self, setor_repo: ISetorRepository):
        self.setor_repo = setor_repo

    def executar(self) -> ListaSetoresOutput:

        setores = self.setor_repo.listar_ativos()

        return ListaSetoresOutput(
            total=len(setores),
            setores=[
                SetorOutput(
                    id=s.id,
                    nome=s.nome,
                    descricao=s.descricao,
                    ativo=s.ativo,
                )
                for s in setores
            ],
        )