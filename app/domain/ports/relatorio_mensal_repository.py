from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.relatorio_mensal import RelatorioMensal


class IRelatorioMensalRepository(ABC):

    @abstractmethod
    def salvar(self, relatorio: RelatorioMensal) -> RelatorioMensal:
        pass

    @abstractmethod
    def buscar_por_setor_mes(
        self,
        setor_id: int,
        mes: str,
    ) -> Optional[RelatorioMensal]:
        pass

    @abstractmethod
    def listar_por_mes(self, mes: str) -> List[RelatorioMensal]:
        pass