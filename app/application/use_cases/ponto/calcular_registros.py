from datetime import datetime, time
from typing import Optional
from app.domain.entities.registro_ponto import RegistroPonto
from app.domain.entities.funcionario import Funcionario

class CalcularRegistrosUseCase:

    def executar(
        self,
        funcionario: Funcionario,
        upload_id: int,
        data: str,
        hora_entrada_str: Optional[str],
        hora_saida_str: Optional[str],
    ) -> RegistroPonto:

        data_obj = datetime.strptime(data, "%Y-%m-%d").date()

        # falta sem entrada e sem saída
        if not hora_entrada_str and not hora_saida_str:
            return RegistroPonto(
                funcionario_id=funcionario.id,
                upload_id=upload_id,
                data=data_obj,
                falta=True,
            )

        hora_entrada = datetime.strptime(hora_entrada_str, "%H:%M").time() \
            if hora_entrada_str else None
        hora_saida = datetime.strptime(hora_saida_str, "%H:%M").time() \
            if hora_saida_str else None

        # minutos trabalhados
        minutos_trabalhados = 0
        if hora_entrada and hora_saida:
            entrada_dt = datetime.combine(data_obj, hora_entrada)
            saida_dt   = datetime.combine(data_obj, hora_saida)
            minutos_trabalhados = int((saida_dt - entrada_dt).total_seconds() / 60)

        # minutos de atraso
        minutos_atraso = 0
        if hora_entrada:
            esperada_dt = datetime.combine(data_obj, funcionario.horario_esperado_entrada)
            real_dt     = datetime.combine(data_obj, hora_entrada)
            diff = int((real_dt - esperada_dt).total_seconds() / 60)
            minutos_atraso = max(0, diff)  # só conta se chegou depois

        # minutos de hora extra
        minutos_hora_extra = 0
        if hora_saida:
            esperada_saida_dt = datetime.combine(data_obj, funcionario.horario_esperado_saida)
            real_saida_dt     = datetime.combine(data_obj, hora_saida)
            diff = int((real_saida_dt - esperada_saida_dt).total_seconds() / 60)
            minutos_hora_extra = max(0, diff)  # só conta se saiu depois

        return RegistroPonto(
            funcionario_id=funcionario.id,
            upload_id=upload_id,
            data=data_obj,
            hora_entrada=hora_entrada,
            hora_saida=hora_saida,
            minutos_trabalhados=minutos_trabalhados,
            minutos_atraso=minutos_atraso,
            minutos_hora_extra=minutos_hora_extra,
            falta=False,
        )