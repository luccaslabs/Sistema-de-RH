from app.application.dto.setor_dto import CriarSetorInput, SetorOutput
from app.domain.entities.setor import Setor
from app.domain.ports.setor_repository import ISetorRepository
from app.domain.services.setor_service import SetorService

class CriarSetorUseCase:

    def __init__(self, setor_repo: ISetorRepository, service: SetorService):
        self.setor_repo = setor_repo
        self.service = service

    def executar(self, dados: CriarSetorInput) -> SetorOutput:

        # Valida nome único

        self.service.validar_nome_disponivel(dados.nome, self.setor_repo)

        # Cria entidade

        setor = Setor(nome=dados.nome, descricao=dados.descricao)
        
        # Salva

        salvo = self.setor_repo.salvar(setor)

        return SetorOutput(
            id=salvo.id,
            nome=salvo.nome,
            descricao=salvo.descricao,
            ativo=salvo.ativo
        )