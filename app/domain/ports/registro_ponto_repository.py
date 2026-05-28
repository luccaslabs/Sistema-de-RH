from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional
from app.domain.entities.registro_ponto import RegistroPonto

class IRegistroPontoRepository(ABC):

    @abstractmethod
    def salvar_em_lote(self, registros: List[RegistroPonto]) -> None:
        pass

    @abstractmethod
    def buscar_por_funcionario_data(
        self,
        funcionario_id: int,
        data: date
    ) -> Optional[RegistroPonto]:
        pass