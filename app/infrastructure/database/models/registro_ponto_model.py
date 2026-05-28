from sqlalchemy import Column, Integer, Boolean, Date, Time, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.base import Base

class RegistroPontoModel(Base):
    __tablename__ = "registros_ponto"

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    funcionario_id      = Column(Integer, ForeignKey("funcionarios.id"), nullable=False)
    upload_id           = Column(Integer, ForeignKey("uploads_csv.id"), nullable=False)
    data                = Column(Date, nullable=False)
    hora_entrada        = Column(Time, nullable=True)
    hora_saida          = Column(Time, nullable=True)
    minutos_trabalhados = Column(Integer, nullable=False, default=0)
    minutos_atraso      = Column(Integer, nullable=False, default=0)
    minutos_hora_extra  = Column(Integer, nullable=False, default=0)
    falta               = Column(Boolean, nullable=False, default=False)
    criado_em           = Column(DateTime, nullable=False, server_default=func.now())

    # relacionamentos
    funcionario = relationship("FuncionarioModel", back_populates="registros_ponto")
    upload      = relationship("UploadCsvModel", back_populates="registros_ponto")