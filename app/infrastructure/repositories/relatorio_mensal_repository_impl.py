from sqlalchemy.orm import Session
from typing import Optional, List
from app.domain.entities.relatorio_mensal import RelatorioMensal
from app.domain.ports.relatorio_mensal_repository import IRelatorioMensalRepository
from app.infrastructure.database.models.relatorio_mensal_model import RelatorioMensalModel


class RelatorioMensalRepositoryImpl(IRelatorioMensalRepository):

    def __init__(self, db: Session):
        self.db = db

    def salvar(self, relatorio: RelatorioMensal) -> RelatorioMensal:
        model = RelatorioMensalModel(
            setor_id=relatorio.setor_id,
            mes=relatorio.mes,
            media_horas_trabalhadas=relatorio.media_horas_trabalhadas,
            total_atrasos=relatorio.total_atrasos,
            total_faltas=relatorio.total_faltas,
            total_horas_extras=relatorio.total_horas_extras,
            insight_llm=relatorio.insight_llm,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        relatorio.id = model.id
        relatorio.gerado_em = model.gerado_em
        return relatorio

    def buscar_por_setor_mes(
        self,
        setor_id: int,
        mes: str,
    ) -> Optional[RelatorioMensal]:
        model = self.db.query(RelatorioMensalModel)\
            .filter(
                RelatorioMensalModel.setor_id == setor_id,
                RelatorioMensalModel.mes == mes,
            ).first()
        return self._to_entity(model) if model else None

    def listar_por_mes(self, mes: str) -> List[RelatorioMensal]:
        models = self.db.query(RelatorioMensalModel)\
            .filter(RelatorioMensalModel.mes == mes)\
            .all()
        return [self._to_entity(m) for m in models]

    def _to_entity(self, model: RelatorioMensalModel) -> RelatorioMensal:
        return RelatorioMensal(
            id=model.id,
            setor_id=model.setor_id,
            mes=model.mes,
            media_horas_trabalhadas=float(model.media_horas_trabalhadas),
            total_atrasos=model.total_atrasos,
            total_faltas=model.total_faltas,
            total_horas_extras=float(model.total_horas_extras),
            insight_llm=model.insight_llm,
            gerado_em=model.gerado_em,
        )