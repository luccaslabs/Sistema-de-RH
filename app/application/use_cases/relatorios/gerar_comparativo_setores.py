from app.application.dto.relatorio_dto import ComparativoOutput, ComparativoSetorOutput
from app.application.use_cases.relatorios.gerar_relatorio_setor import GerarRelatorioSetorUseCase
from app.domain.ports.relatorio_mensal_repository import IRelatorioMensalRepository
from app.domain.ports.setor_repository import ISetorRepository
from app.domain.ports.registro_ponto_repository import IRegistroPontoRepository
from app.domain.ports.funcionario_repository import IFuncionarioRepository
from app.domain.ports.analisador_ia import IAnalisadorIA


class GerarComparativoSetoresUseCase:

    def __init__(
        self,
        setor_repo: ISetorRepository,
        funcionario_repo: IFuncionarioRepository,
        registro_repo: IRegistroPontoRepository,
        relatorio_repo: IRelatorioMensalRepository,
        analisador: IAnalisadorIA,
    ):
        self.setor_repo       = setor_repo
        self.funcionario_repo = funcionario_repo
        self.registro_repo    = registro_repo
        self.relatorio_repo   = relatorio_repo
        self.analisador       = analisador

    def executar(self, mes: str) -> ComparativoOutput:

        setores = self.setor_repo.listar_ativos()
        if not setores:
            raise ValueError("Nenhum setor ativo encontrado.")

        comparativo = []

        for setor in setores:

            # tenta buscar relatório já gerado
            relatorio = self.relatorio_repo.buscar_por_setor_mes(setor.id, mes)

            if relatorio:
                comparativo.append(ComparativoSetorOutput(
                    setor=setor.nome,
                    media_horas=relatorio.media_horas_trabalhadas,
                    total_atrasos=relatorio.total_atrasos,
                    total_faltas=relatorio.total_faltas,
                    total_horas_extras=relatorio.total_horas_extras,
                ))
            else:
                # gera sob demanda se não existir
                try:
                    gerar = GerarRelatorioSetorUseCase(
                        setor_repo=self.setor_repo,
                        funcionario_repo=self.funcionario_repo,
                        registro_repo=self.registro_repo,
                        relatorio_repo=self.relatorio_repo,
                        analisador=self.analisador,
                    )
                    relatorio_gerado = gerar.executar(setor.id, mes)

                    comparativo.append(ComparativoSetorOutput(
                        setor=setor.nome,
                        media_horas=relatorio_gerado.resumo["media_horas_trabalhadas"],
                        total_atrasos=relatorio_gerado.resumo["total_atrasos"],
                        total_faltas=relatorio_gerado.resumo["total_faltas"],
                        total_horas_extras=relatorio_gerado.resumo["total_horas_extras"],
                    ))

                except ValueError:
                    # setor sem registros no mês — ignora
                    continue

        return ComparativoOutput(
            periodo=mes,
            setores=comparativo,
        )