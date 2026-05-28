from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.setor import Setor

class ISetorRepository(ABC):

    @abstractmethod
    def salvar(self, setor: Setor) -> Setor:
        pass

    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[Setor]:
        pass

    @abstractmethod
    def buscar_por_nome(self, nome: str) -> Optional[Setor]:
        pass

    @abstractmethod
    def listar_ativos(self) -> List[Setor]:
        pass