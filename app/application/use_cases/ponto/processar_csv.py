import pandas as pd
from io import BytesIO
from typing import List
from app.application.dto.ponto_dto import ProcessarCSVOutput, ErroLinhaCSV
from app.application.use_cases.ponto.validar_csv import ValidarCSVUseCase
from app.application.use_cases.ponto.calcular_registros import CalcularRegistrosUseCase
from app.domain.entities.upload_csv import UploadCsv
from app.domain.ports.upload_csv_repository import IUploadCsvRepository
from app.domain.ports.registro_ponto_repository import IRegistroPontoRepository
from app.domain.ports.funcionario_repository import IFuncionarioRepository

class ProcessarCSVUseCase:

    def __init__(
        self,
        upload_repo: IUploadCsvRepository,
        registro_repo: IRegistroPontoRepository,
        funcionario_repo: IFuncionarioRepository,
    ):
        self.upload_repo      = upload_repo
        self.registro_repo    = registro_repo
        self.funcionario_repo = funcionario_repo

    def executar(self, nome_arquivo: str, conteudo: bytes) -> ProcessarCSVOutput:
        erros: List[ErroLinhaCSV] = []

        # 1. Cria o upload com status "processando"
        upload = self.upload_repo.salvar(UploadCsv(nome_arquivo=nome_arquivo))

        try:
            # 2. Valida o CSV
            validacao = ValidarCSVUseCase(self.funcionario_repo).executar(conteudo)

            if not validacao.valido:
                upload.status       = "erro"
                upload.erro_detalhe = str([e.dict() for e in validacao.erros])
                self.upload_repo.atualizar(upload)
                return ProcessarCSVOutput(
                    upload_id=upload.id,
                    status="erro",
                    total_registros=0,
                    periodo_inicio=None,
                    periodo_fim=None,
                    erros=validacao.erros,
                )

            # 3. Lê o CSV e processa linha por linha
            df = pd.read_csv(BytesIO(conteudo))
            registros = []
            calcular  = CalcularRegistrosUseCase()

            for i, row in df.iterrows():
                linha = i + 2
                try:
                    funcionario = self.funcionario_repo.buscar_por_id(
                        int(row["funcionario_id"])
                    )
                    registro = calcular.executar(
                        funcionario=funcionario,
                        upload_id=upload.id,
                        data=str(row["data"]),
                        hora_entrada_str=str(row["hora_entrada"])
                            if pd.notna(row["hora_entrada"]) else None,
                        hora_saida_str=str(row["hora_saida"])
                            if pd.notna(row["hora_saida"]) else None,
                    )
                    registros.append(registro)

                except Exception as e:
                    erros.append(ErroLinhaCSV(linha=linha, erro=str(e)))

            # 4. Salva todos os registros em lote
            if registros:
                self.registro_repo.salvar_em_lote(registros)

            # 5. Atualiza o upload como concluído
            datas = df["data"].dropna().tolist()
            upload.status          = "concluido"
            upload.total_registros = len(registros)
            upload.periodo_inicio  = pd.to_datetime(min(datas)).date()
            upload.periodo_fim     = pd.to_datetime(max(datas)).date()
            self.upload_repo.atualizar(upload)

            return ProcessarCSVOutput(
                upload_id=upload.id,
                status="concluido",
                total_registros=len(registros),
                periodo_inicio=upload.periodo_inicio,
                periodo_fim=upload.periodo_fim,
                erros=erros,
            )

        except Exception as e:
            # erro inesperado
            upload.status       = "erro"
            upload.erro_detalhe = str(e)
            self.upload_repo.atualizar(upload)
            raise