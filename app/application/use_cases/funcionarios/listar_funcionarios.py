from math import ceil
from app.application.dto.funcionario_dto import (
    ListarFuncionariosInput,
    ListaFuncionariosOutput,
    FuncionarioOutput
)
from app.domain.ports.funcionario_repository import IFuncionarioRepository


class ListarFuncionariosUseCase:

    def __init__(self, funcionario_repo: IFuncionarioRepository):
        self.funcionario_repo = funcionario_repo

    def executar(self, filtros: ListarFuncionariosInput) -> ListaFuncionariosOutput:

        funcionarios = self.funcionario_repo.listar(
            setor_id=filtros.setor_id,
            apenas_ativos=filtros.apenas_ativos,
            pagina=filtros.pagina,
            por_pagina=filtros.por_pagina,
        )

        total = len(funcionarios)

        paginas = ceil(total / filtros.por_pagina) if total > 0 else 1

        return ListaFuncionariosOutput(
            total=total,
            pagina=filtros.pagina,
            por_pagina=filtros.por_pagina,
            paginas=paginas,
            funcionarios=[
                FuncionarioOutput(
                    id=f.id,
                    nome=f.nome,
                    email=f.email,
                    cargo=f.cargo,
                    setor_id=f.setor_id,
                    data_admissao=f.data_admissao,
                    horario_esperado_entrada=f.horario_esperado_entrada,
                    horario_esperado_saida=f.horario_esperado_saida,
                    ativo=f.ativo,
                )
                for f in funcionarios
            ],
        )