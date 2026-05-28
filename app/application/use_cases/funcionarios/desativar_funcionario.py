from app.domain.ports.funcionario_repository import IFuncionarioRepository

class DesativarFuncionarioUseCase:

    def __init__(self, funcionario_repo: IFuncionarioRepository):
        self.funcionario_repo = funcionario_repo

    def executar(self, id: int) -> None:

        # 1. Verifica se existe
        funcionario = self.funcionario_repo.buscar_por_id(id)
        if not funcionario:
            raise ValueError(f"Funcionário com id '{id}' não encontrado.")

        # 2. Verifica se já está inativo
        if not funcionario.ativo:
            raise ValueError(f"Funcionário com id '{id}' já está inativo.")

        # 3. Desativa
        self.funcionario_repo.desativar(id)