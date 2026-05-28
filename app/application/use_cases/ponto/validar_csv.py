import pandas as pd
from io import BytesIO
from typing import List
from app.application.dto.ponto_dto import ValidacaoCSVOutput, ErroLinhaCSV
from app.domain.ports.funcionario_repository import IFuncionarioRepository

COLUNAS_OBRIGATORIAS = {
    "funcionario_id",
    "nome",
    "setor",
    "data",
    "hora_entrada",
    "hora_saida",
}

class ValidarCSVUseCase:

    def __init__(self, funcionario_repo: IFuncionarioRepository):
        self.funcionario_repo = funcionario_repo

    def executar(self, conteudo: bytes) -> ValidacaoCSVOutput:
        erros: List[ErroLinhaCSV] = []

        # 1. Lê o CSV
        try:
            df = pd.read_csv(BytesIO(conteudo))
        except Exception:
            return ValidacaoCSVOutput(
                valido=False,
                total_linhas=0,
                erros=[ErroLinhaCSV(linha=0, erro="Arquivo inválido ou corrompido.")]
            )

        # 2. Valida colunas obrigatórias
        colunas_faltando = COLUNAS_OBRIGATORIAS - set(df.columns)
        if colunas_faltando:
            return ValidacaoCSVOutput(
                valido=False,
                total_linhas=0,
                erros=[ErroLinhaCSV(
                    linha=0,
                    erro=f"Colunas faltando: {', '.join(colunas_faltando)}"
                )]
            )

        # 3. Valida linha por linha
        for i, row in df.iterrows():
            linha = i + 2  # +2 porque linha 1 é o header

            # data
            try:
                pd.to_datetime(row["data"], format="%Y-%m-%d")
            except Exception:
                erros.append(ErroLinhaCSV(
                    linha=linha,
                    erro=f"Data inválida '{row['data']}'. Use o formato YYYY-MM-DD."
                ))

            # hora_entrada (pode ser vazia em caso de falta)
            if pd.notna(row["hora_entrada"]):
                try:
                    pd.to_datetime(row["hora_entrada"], format="%H:%M")
                except Exception:
                    erros.append(ErroLinhaCSV(
                        linha=linha,
                        erro=f"hora_entrada inválida '{row['hora_entrada']}'. Use HH:MM."
                    ))

            # hora_saida
            if pd.notna(row["hora_saida"]):
                try:
                    pd.to_datetime(row["hora_saida"], format="%H:%M")
                except Exception:
                    erros.append(ErroLinhaCSV(
                        linha=linha,
                        erro=f"hora_saida inválida '{row['hora_saida']}'. Use HH:MM."
                    ))

            # funcionario existe no banco
            funcionario = self.funcionario_repo.buscar_por_id(
                int(row["funcionario_id"])
            )
            if not funcionario:
                erros.append(ErroLinhaCSV(
                    linha=linha,
                    erro=f"Funcionário id '{row['funcionario_id']}' não encontrado."
                ))

        return ValidacaoCSVOutput(
            valido=len(erros) == 0,
            total_linhas=len(df),
            erros=erros,
        )