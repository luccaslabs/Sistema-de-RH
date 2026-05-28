from app.domain.ports.setor_repository import ISetorRepository

class SetorService:

    def validar_nome_disponivel(
            self,
            nome: str,
            repo: ISetorRepository
    ) -> None:
        if repo.buscar_por_nome(nome):
            raise ValueError(
                f"Já existe um setor cadastrado com o nome {nome}."
            )