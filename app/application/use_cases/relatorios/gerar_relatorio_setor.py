from collections import defaultdict
from datetime import datetime
from app.application.dto.relatorio_dto import (
    RelatorioSetorOutput,
    FuncionarioRelatorioOutput,
    GraficoDiarioOutput,
    GraficoSemanalOutput,
)
from app.application.use_cases.relatorios.gerar_insight_llm import GerarInsightLLMUseCase
from app.domain.ports.relatorio_mensal_repository import IRelatorioMensalRepository
from app.domain.ports.registro_ponto_repository import IRegistroPontoRepository
from app.domain.ports.setor_repository import ISetorRepository
from app.domain.ports.funcionario_repository import IFuncionarioRepository
from app.domain.ports.analisador_ia import IAnalisadorIA
from app.domain.entities.relatorio_mensal import RelatorioMensal


class GerarRelatorioSetorUseCase:

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

    def executar(self, setor_id: int, mes: str) -> RelatorioSetorOutput:

        # 1. Valida setor
        setor = self.setor_repo.buscar_por_id(setor_id)
        if not setor:
            raise ValueError(f"Setor com id '{setor_id}' não encontrado.")

        # 2. Verifica se já existe relatório gerado para esse setor/mês
        relatorio_existente = self.relatorio_repo.buscar_por_setor_mes(setor_id, mes)

        # 3. Busca registros do mês para montar gráficos e tabela de funcionários
        registros = self.registro_repo.listar_por_setor_mes(setor_id, mes)

        if not registros:
            raise ValueError(
                f"Nenhum registro encontrado para o setor '{setor.nome}' no período '{mes}'."
            )

        # 4. Busca funcionários do setor
        funcionarios = self.funcionario_repo.listar(setor_id=setor_id, apenas_ativos=False)
        funcionarios_map = {f.id: f for f in funcionarios}

        # 5. Agrega métricas por funcionário
        por_funcionario = defaultdict(lambda: {
            "minutos_trabalhados": 0,
            "atrasos": 0,
            "faltas": 0,
            "minutos_hora_extra": 0,
        })

        for r in registros:
            por_funcionario[r.funcionario_id]["minutos_trabalhados"] += r.minutos_trabalhados
            por_funcionario[r.funcionario_id]["minutos_hora_extra"]  += r.minutos_hora_extra
            if r.falta:
                por_funcionario[r.funcionario_id]["faltas"] += 1
            if r.minutos_atraso > 0:
                por_funcionario[r.funcionario_id]["atrasos"] += 1

        funcionarios_output = [
            FuncionarioRelatorioOutput(
                funcionario_id=fid,
                nome=funcionarios_map[fid].nome if fid in funcionarios_map else "Desconhecido",
                horas_trabalhadas=round(dados["minutos_trabalhados"] / 60, 2),
                atrasos=dados["atrasos"],
                faltas=dados["faltas"],
                horas_extras=round(dados["minutos_hora_extra"] / 60, 2),
            )
            for fid, dados in por_funcionario.items()
        ]

        # 6. Agrega métricas gerais
        total_minutos      = sum(r.minutos_trabalhados for r in registros)
        total_atrasos      = sum(1 for r in registros if r.minutos_atraso > 0)
        total_faltas       = sum(1 for r in registros if r.falta)
        total_horas_extras = sum(r.minutos_hora_extra for r in registros)
        total_funcionarios = len(por_funcionario)
        media_horas        = round((total_minutos / 60) / total_funcionarios, 2) \
            if total_funcionarios > 0 else 0.0

        # 7. Gráfico — média de horas por dia
        por_dia = defaultdict(list)
        for r in registros:
            if not r.falta:
                por_dia[r.data.strftime("%Y-%m-%d")].append(r.minutos_trabalhados)

        grafico_horas_diarias = [
            GraficoDiarioOutput(
                data=data,
                media_horas=round(sum(mins) / len(mins) / 60, 2),
            )
            for data, mins in sorted(por_dia.items())
        ]

        # 8. Gráfico — atrasos por semana
        por_semana = defaultdict(int)
        for r in registros:
            if r.minutos_atraso > 0:
                semana = f"Semana {r.data.isocalendar()[1]}"
                por_semana[semana] += 1

        grafico_atrasos_por_semana = [
            GraficoSemanalOutput(semana=semana, total_atrasos=total)
            for semana, total in sorted(por_semana.items())
        ]

        # 9. Gera ou reutiliza insight da LLM
        if relatorio_existente and relatorio_existente.insight_llm:
            insight = relatorio_existente.insight_llm
            gerado_em = relatorio_existente.gerado_em
        else:
            insight = GerarInsightLLMUseCase(self.analisador).executar(
                nome_setor=setor.nome,
                mes=mes,
                total_funcionarios=total_funcionarios,
                media_horas_trabalhadas=media_horas,
                total_atrasos=total_atrasos,
                total_faltas=total_faltas,
                total_horas_extras=round(total_horas_extras / 60, 2),
            )

            # 10. Salva o relatório consolidado
            relatorio = RelatorioMensal(
                setor_id=setor_id,
                mes=mes,
                media_horas_trabalhadas=media_horas,
                total_atrasos=total_atrasos,
                total_faltas=total_faltas,
                total_horas_extras=round(total_horas_extras / 60, 2),
                insight_llm=insight,
            )
            salvo     = self.relatorio_repo.salvar(relatorio)
            gerado_em = salvo.gerado_em

        return RelatorioSetorOutput(
            setor_id=setor_id,
            setor=setor.nome,
            periodo=mes,
            resumo={
                "total_funcionarios": total_funcionarios,
                "media_horas_trabalhadas": media_horas,
                "total_atrasos": total_atrasos,
                "total_faltas": total_faltas,
                "total_horas_extras": round(total_horas_extras / 60, 2),
            },
            funcionarios=funcionarios_output,
            grafico_horas_diarias=grafico_horas_diarias,
            grafico_atrasos_por_semana=grafico_atrasos_por_semana,
            insight_llm=insight,
            gerado_em=gerado_em,
        )