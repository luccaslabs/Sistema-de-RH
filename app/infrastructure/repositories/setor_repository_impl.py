from sqlalchemy.orm import Session
from typing import Optional, List
from app.domain.entities.setor import Setor
from app.domain.ports.setor_repository import ISetorRepository
from app.infrastructure.database.models import SetorModel

class SetorRepositoryImpl(ISetorRepository):

    def __init__(self, db: Session):
        self.db = db

    def salvar(self, setor: Setor) -> Setor:
        model = SetorModel(
            nome=setor.nome,
            descricao=setor.descricao,
            ativo=setor.ativo
        )

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        setor.id = model.id
        return setor
    
    def buscar_por_nome(self, nome: str) -> Optional[Setor]:
        model = self.db.query(SetorModel)\
            .filter(SetorModel.nome == nome)\
            .first()
        return self._to_entity(model) if model else None

    def buscar_por_id(self, id: int) -> Optional[Setor]:
        model = self.db.query(SetorModel)\
        .filter(SetorModel.id == id)\
        .first()

        return self._to_entity(model) if model else None

    def listar_ativos(self) -> List[Setor]:
        models = self.db.query(SetorModel)\
            .filter(SetorModel.ativo == True)\
            .all()
        return [self._to_entity(m) for m in models]

    def _to_entity(self, model: SetorModel) -> Setor:
        return Setor(
            id=model.id,
            nome=model.nome,
            descricao=model.descricao,
            ativo=model.ativo,
        )