from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.base import Base

class RelatorioMensalModel(Base):
    __tablename__ = "relatorios_mensais"

    id                      = Column(Integer, primary_key=True, autoincrement=True)
    setor_id                = Column(Integer, ForeignKey("setores.id"), nullable=False)
    mes                     = Column(String(7), nullable=False)  # YYYY-MM
    media_horas_trabalhadas = Column(DECIMAL(5, 2), nullable=False, default=0)
    total_atrasos           = Column(Integer, nullable=False, default=0)
    total_faltas            = Column(Integer, nullable=False, default=0)
    total_horas_extras      = Column(DECIMAL(5, 2), nullable=False, default=0)
    insight_llm             = Column(Text, nullable=True)
    gerado_em               = Column(DateTime, nullable=False, server_default=func.now())

    # relacionamentos
    setor = relationship("SetorModel", back_populates="relatorios_mensais")