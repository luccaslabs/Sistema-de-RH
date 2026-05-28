from abc import ABC, abstractmethod

class IAnalisadorIA(ABC):

    @abstractmethod
    def gerar_insight_setor(
        self,
        nome_setor: str,
        mes: str,
        total_funcionarios: int,
        media_horas_trabalhadas: float,
        total_atrasos: int,
        total_faltas: int,
        total_horas_extras: float,
    ) -> str:
        pass