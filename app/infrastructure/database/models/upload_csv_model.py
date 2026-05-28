from sqlalchemy import Column, Integer, String, DateTime, Date, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.base import Base
import enum

class StatusUpload(str, enum.Enum):
    processando = "processando"
    concluido   = "concluido"
    erro        = "erro"

class UploadCsvModel(Base):
    __tablename__ = "uploads_csv"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    nome_arquivo    = Column(String(255), nullable=False)
    data_upload     = Column(DateTime, nullable=False, server_default=func.now())
    total_registros = Column(Integer, nullable=False, default=0)
    status          = Column(Enum(StatusUpload), nullable=False, default=StatusUpload.processando)
    periodo_inicio  = Column(Date, nullable=True)
    periodo_fim     = Column(Date, nullable=True)
    erro_detalhe    = Column(Text, nullable=True)

    # relacionamentos
    registros_ponto = relationship("RegistroPontoModel", back_populates="upload")