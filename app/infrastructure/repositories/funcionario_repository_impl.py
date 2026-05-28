from sqlalchemy.orm import Session
from typing import Optional
from app.domain.entities.funcionario import Funcionario
from app.domain.ports.funcionario_repository import IFuncionarioRepository
from app.infrastructure.database.models import FuncionarioModel

class FuncionarioRepositoryImpl(IFuncionarioRepository):

    def __init__(self, db: Session):
        self.db = db

    def salvar(self, funcionario: Funcionario) -> Funcionario:
        model = FuncionarioModel(
            nome=funcionario.nome,
            email=funcionario.email,
            setor_id=funcionario.setor_id,
            cargo=funcionario.cargo,
            data_admissao=funcionario.data_admissao,
            horario_esperado_entrada=funcionario.horario_esperado_entrada,
            horario_esperado_saida=funcionario.horario_esperado_saida,
            ativo=funcionario.ativo,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        funcionario.id = model.id
        return funcionario

    def buscar_por_email(self, email: str) -> Optional[Funcionario]:
        model = self.db.query(FuncionarioModel)\
            .filter(FuncionarioModel.email == email)\
            .first()
        return self._to_entity(model) if model else None

    def buscar_por_id(self, id: int) -> Optional[Funcionario]:
        model = self.db.query(FuncionarioModel)\
            .filter(FuncionarioModel.id == id)\
            .first()
        return self._to_entity(model) if model else None

    def _to_entity(self, model: FuncionarioModel) -> Funcionario:
        return Funcionario(
            id=model.id,
            nome=model.nome,
            email=model.email,
            setor_id=model.setor_id,
            cargo=model.cargo,
            data_admissao=model.data_admissao,
            horario_esperado_entrada=model.horario_esperado_entrada,
            horario_esperado_saida=model.horario_esperado_saida,
            ativo=model.ativo,
        )
    def atualizar(self, funcionario: Funcionario) -> Funcionario:
        model = self.db.query(FuncionarioModel)\
            .filter(FuncionarioModel.id == funcionario.id)\
            .first()

        model.nome                     = funcionario.nome
        model.cargo                    = funcionario.cargo
        model.setor_id                 = funcionario.setor_id
        model.horario_esperado_entrada = funcionario.horario_esperado_entrada
        model.horario_esperado_saida   = funcionario.horario_esperado_saida

        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def listar(
        self,
        setor_id=None,
        apenas_ativos=True,
        pagina=1,
        por_pagina=20,
    ) -> list:
        query = self.db.query(FuncionarioModel)

        if apenas_ativos:
            query = query.filter(FuncionarioModel.ativo == True)
        if setor_id:
            query = query.filter(FuncionarioModel.setor_id == setor_id)

        offset = (pagina - 1) * por_pagina
        models = query.offset(offset).limit(por_pagina).all()
        return [self._to_entity(m) for m in models]

    def desativar(self, id: int) -> None:
        self.db.query(FuncionarioModel)\
            .filter(FuncionarioModel.id == id)\
            .update({"ativo": False})
        self.db.commit()
    
                