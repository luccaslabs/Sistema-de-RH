from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.base import Base

class SetorModel(Base):
    __tablename__ = "setores"

    id        = Column(Integer, primary_key=True, autoincrement=True)
    nome      = Column(String(100), nullable=False, unique=True)
    descricao = Column(String(255), nullable=True)
    ativo     = Column(Boolean, nullable=False, default=True)
    criado_em = Column(DateTime, nullable=False, server_default=func.now())

    # relacionamentos
    funcionarios       = relationship("FuncionarioModel", back_populates="setor")
    relatorios_mensais = relationship("RelatorioMensalModel", back_populates="setor")