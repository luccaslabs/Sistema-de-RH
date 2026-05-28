from sqlalchemy import Column, Integer, String, Boolean, Date, Time, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.base import Base

class FuncionarioModel(Base):
    __tablename__ = "funcionarios"

    id                       = Column(Integer, primary_key=True, autoincrement=True)
    nome                     = Column(String(150), nullable=False)
    email                    = Column(String(150), nullable=False, unique=True)
    cargo                    = Column(String(100), nullable=True)
    setor_id                 = Column(Integer, ForeignKey("setores.id"), nullable=False)
    horario_esperado_entrada = Column(Time, nullable=False, default="08:00:00")
    horario_esperado_saida   = Column(Time, nullable=False, default="17:00:00")
    data_admissao            = Column(Date, nullable=False)
    ativo                    = Column(Boolean, nullable=False, default=True)
    criado_em                = Column(DateTime, nullable=False, server_default=func.now())

    # relacionamentos
    setor            = relationship("SetorModel", back_populates="funcionarios")
    registros_ponto  = relationship("RegistroPontoModel", back_populates="funcionario")