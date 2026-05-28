from app.application.dto.funcionario_dto import CriarFuncionarioInput, FuncionarioOutput
from app.domain.entities.funcionario import Funcionario
from app.domain.ports.funcionario_repository import IFuncionarioRepository
from app.domain.ports.setor_repository import ISetorRepository
from app.domain.services.funcionario_service import FuncionarioService

class CriarFuncionarioUseCase:

    def __init__(
        self,
        funcionario_repo: IFuncionarioRepository,
        setor_repo: ISetorRepository,
        service: FuncionarioService
    ):
        self.funcionario_repo = funcionario_repo
        self.setor_repo = setor_repo
        self.service = service

    def executar(self, dados: CriarFuncionarioInput) -> FuncionarioOutput:

        # 1. Valida se o setor existe
        setor = self.setor_repo.buscar_por_id(dados.setor_id)
        if not setor:
            raise ValueError(f"Setor com id '{dados.setor_id}' não encontrado.")

        # 2. Valida se o e-mail já está em uso
        self.service.validar_email_disponivel(dados.email, self.funcionario_repo)

        # 3. Valida os horários
        self.service.validar_horarios(
            dados.horario_esperado_entrada,
            dados.horario_esperado_saida
        )

        # 4. Cria a entidade
        funcionario = Funcionario(
            nome=dados.nome,
            email=dados.email,
            setor_id=dados.setor_id,
            cargo=dados.cargo,
            data_admissao=dados.data_admissao,
            horario_esperado_entrada=dados.horario_esperado_entrada,
            horario_esperado_saida=dados.horario_esperado_saida,
        )

        # 5. Persiste
        salvo = self.funcionario_repo.salvar(funcionario)

        return FuncionarioOutput(
            id=salvo.id,
            nome=salvo.nome,
            email=salvo.email,
            cargo=salvo.cargo,
            setor_id=salvo.setor_id,
            data_admissao=salvo.data_admissao,
            horario_esperado_entrada=salvo.horario_esperado_entrada,
            horario_esperado_saida=salvo.horario_esperado_saida,
            ativo=salvo.ativo,
        )