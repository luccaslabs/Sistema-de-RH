from app.application.dto.funcionario_dto import AtualizarFuncionarioInput, FuncionarioOutput
from app.domain.ports.funcionario_repository import IFuncionarioRepository
from app.domain.ports.setor_repository import ISetorRepository
from app.domain.services.funcionario_service import FuncionarioService

class AtualizarFuncionarioUseCase:

    def __init__(
        self,
        funcionario_repo: IFuncionarioRepository,
        setor_repo: ISetorRepository,
        service: FuncionarioService
    ):
        self.funcionario_repo = funcionario_repo
        self.setor_repo = setor_repo
        self.service = service

    def executar(self, id: int, dados: AtualizarFuncionarioInput) -> FuncionarioOutput:

        # 1. Verifica se o funcionário existe
        funcionario = self.funcionario_repo.buscar_por_id(id)
        if not funcionario:
            raise ValueError(f"Funcionário com id '{id}' não encontrado.")

        # 2. Valida novo setor se informado
        if dados.setor_id:
            setor = self.setor_repo.buscar_por_id(dados.setor_id)
            if not setor:
                raise ValueError(f"Setor com id '{dados.setor_id}' não encontrado.")

        # 3. Aplica apenas os campos enviados (PATCH)
        if dados.nome:
            funcionario.nome = dados.nome
        if dados.cargo:
            funcionario.cargo = dados.cargo
        if dados.setor_id:
            funcionario.setor_id = dados.setor_id
        if dados.horario_esperado_entrada:
            funcionario.horario_esperado_entrada = dados.horario_esperado_entrada
        if dados.horario_esperado_saida:
            funcionario.horario_esperado_saida = dados.horario_esperado_saida

        # 4. Valida horários após atualização
        self.service.validar_horarios(
            funcionario.horario_esperado_entrada,
            funcionario.horario_esperado_saida,
        )

        # 5. Persiste
        atualizado = self.funcionario_repo.atualizar(funcionario)

        return FuncionarioOutput(
            id=atualizado.id,
            nome=atualizado.nome,
            email=atualizado.email,
            cargo=atualizado.cargo,
            setor_id=atualizado.setor_id,
            data_admissao=atualizado.data_admissao,
            horario_esperado_entrada=atualizado.horario_esperado_entrada,
            horario_esperado_saida=atualizado.horario_esperado_saida,
            ativo=atualizado.ativo,
        )