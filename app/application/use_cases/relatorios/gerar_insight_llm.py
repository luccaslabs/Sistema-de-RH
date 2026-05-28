from app.domain.ports.analisador_ia import IAnalisadorIA


class GerarInsightLLMUseCase:

    def __init__(self, analisador: IAnalisadorIA):
        self.analisador = analisador

    def executar(
        self,
        nome_setor: str,
        mes: str,
        total_funcionarios: int,
        media_horas_trabalhadas: float,
        total_atrasos: int,
        total_faltas: int,
        total_horas_extras: float,
    ) -> str:

        return self.analisador.gerar_insight_setor(
            nome_setor=nome_setor,
            mes=mes,
            total_funcionarios=total_funcionarios,
            media_horas_trabalhadas=media_horas_trabalhadas,
            total_atrasos=total_atrasos,
            total_faltas=total_faltas,
            total_horas_extras=total_horas_extras,
        )