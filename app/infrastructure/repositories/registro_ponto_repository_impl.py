from sqlalchemy.orm import Session
from datetime import date
from typing import Optional, List
from app.domain.entities.registro_ponto import RegistroPonto
from app.domain.ports.registro_ponto_repository import IRegistroPontoRepository
from app.infrastructure.database.models.registro_ponto_model import RegistroPontoModel


class RegistroPontoRepositoryImpl(IRegistroPontoRepository):

    def __init__(self, db: Session):
        self.db = db

    def salvar_em_lote(self, registros: List[RegistroPonto]) -> None:
        models = [
            RegistroPontoModel(
                funcionario_id=r.funcionario_id,
                upload_id=r.upload_id,
                data=r.data,
                hora_entrada=r.hora_entrada,
                hora_saida=r.hora_saida,
                minutos_trabalhados=r.minutos_trabalhados,
                minutos_atraso=r.minutos_atraso,
                minutos_hora_extra=r.minutos_hora_extra,
                falta=r.falta,
            )
            for r in registros
        ]
        self.db.bulk_save_objects(models)
        self.db.commit()

    def buscar_por_funcionario_data(
        self,
        funcionario_id: int,
        data: date,
    ) -> Optional[RegistroPonto]:
        model = self.db.query(RegistroPontoModel)\
            .filter(
                RegistroPontoModel.funcionario_id == funcionario_id,
                RegistroPontoModel.data == data,
            ).first()
        return self._to_entity(model) if model else None

    def listar_por_setor_mes(
        self,
        setor_id: int,
        mes: str,  # formato YYYY-MM
    ) -> List[RegistroPonto]:
        """Busca todos os registros de um setor em um mês."""
        from app.infrastructure.database.models.funcionario_model import FuncionarioModel
        from sqlalchemy import extract

        ano, mes_num = mes.split("-")

        models = self.db.query(RegistroPontoModel)\
            .join(FuncionarioModel, RegistroPontoModel.funcionario_id == FuncionarioModel.id)\
            .filter(
                FuncionarioModel.setor_id == setor_id,
                extract("year", RegistroPontoModel.data) == int(ano),
                extract("month", RegistroPontoModel.data) == int(mes_num),
            ).all()

        return [self._to_entity(m) for m in models]

    def _to_entity(self, model: RegistroPontoModel) -> RegistroPonto:
        return RegistroPonto(
            id=model.id,
            funcionario_id=model.funcionario_id,
            upload_id=model.upload_id,
            data=model.data,
            hora_entrada=model.hora_entrada,
            hora_saida=model.hora_saida,
            minutos_trabalhados=model.minutos_trabalhados,
            minutos_atraso=model.minutos_atraso,
            minutos_hora_extra=model.minutos_hora_extra,
            falta=model.falta,
        )