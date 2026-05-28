from sqlalchemy.orm import Session
from typing import Optional
from app.domain.entities.upload_csv import UploadCsv
from app.domain.ports.upload_csv_repository import IUploadCsvRepository
from app.infrastructure.database.models.upload_csv_model import UploadCsvModel, StatusUpload


class UploadCsvRepositoryImpl(IUploadCsvRepository):

    def __init__(self, db: Session):
        self.db = db

    def salvar(self, upload: UploadCsv) -> UploadCsv:
        model = UploadCsvModel(
            nome_arquivo=upload.nome_arquivo,
            status=StatusUpload(upload.status),
            total_registros=upload.total_registros,
            periodo_inicio=upload.periodo_inicio,
            periodo_fim=upload.periodo_fim,
            erro_detalhe=upload.erro_detalhe,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        upload.id = model.id
        upload.data_upload = model.data_upload
        return upload

    def atualizar(self, upload: UploadCsv) -> UploadCsv:
        model = self.db.query(UploadCsvModel)\
            .filter(UploadCsvModel.id == upload.id)\
            .first()

        model.status          = StatusUpload(upload.status)
        model.total_registros = upload.total_registros
        model.periodo_inicio  = upload.periodo_inicio
        model.periodo_fim     = upload.periodo_fim
        model.erro_detalhe    = upload.erro_detalhe

        self.db.commit()
        self.db.refresh(model)
        return upload

    def buscar_por_id(self, id: int) -> Optional[UploadCsv]:
        model = self.db.query(UploadCsvModel)\
            .filter(UploadCsvModel.id == id)\
            .first()
        return self._to_entity(model) if model else None

    def _to_entity(self, model: UploadCsvModel) -> UploadCsv:
        return UploadCsv(
            id=model.id,
            nome_arquivo=model.nome_arquivo,
            status=model.status.value,
            total_registros=model.total_registros,
            periodo_inicio=model.periodo_inicio,
            periodo_fim=model.periodo_fim,
            erro_detalhe=model.erro_detalhe,
            data_upload=model.data_upload,
        )