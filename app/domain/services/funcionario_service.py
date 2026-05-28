from app.domain.entities.funcionario import Funcionario
from app.domain.ports.funcionario_repository import IFuncionarioRepository
from datetime import time

class FuncionarioService:

    def validar_horarios(
            self,
            entrada: time,
            saida: time
    ) -> None:
        if entrada >= saida:
            raise ValueError(
                "Horário de entrada deve ser anterior ao horário de saída"
            )
        
    def validar_email_disponivel(
            self,
            email: str,
            repo: IFuncionarioRepository
    ) -> None:
        if repo.buscar_por_email(email):
            raise ValueError(
                f"Já existe um funcionário cadastrado com o e-mail {email}."
            )