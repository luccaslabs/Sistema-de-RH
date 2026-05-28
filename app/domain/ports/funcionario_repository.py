from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.funcionario import Funcionario

class IFuncionarioRepository(ABC):

    @abstractmethod
    def salvar(self, funcionario: Funcionario) -> Funcionario:
        pass

    @abstractmethod
    def buscar_por_email(self, email: str) -> Optional[Funcionario]:
        pass

    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[Funcionario]:
        pass

    @abstractmethod
    def atualizar(self, funcionario: Funcionario) -> Funcionario:
        pass

    @abstractmethod
    def listar(
        self,
        setor_id: Optional[int] = None,
        apenas_ativos: bool = True,
        pagina: int = 1,
        por_pagina: int = 20,
    ) -> List[Funcionario]:
        pass

    @abstractmethod
    def desativar(self, id: int) -> None:
        pass