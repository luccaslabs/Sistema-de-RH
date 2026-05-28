from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.infrastructure.database.connection import engine
from app.infrastructure.database.base import Base
from app.infrastructure.database.models import (
    SetorModel,
    FuncionarioModel,
    UploadCsvModel,
    RegistroPontoModel,
    RelatorioMensalModel,
)

from app.api.routers import funcionarios, setores, ponto, relatorios

# carrega o .env
load_dotenv()

app = FastAPI(
    title="Sistema de RH",
    description="API para gerenciamento de funcionários e análise de ponto eletrônico.",
    version="1.0.0",
)

# CORS — permite o frontend React acessar a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # porta padrão do Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# cria as tabelas que ainda não existem no banco
Base.metadata.create_all(bind=engine)

# registra os routers
app.include_router(setores.router,      prefix="/api/v1")
app.include_router(funcionarios.router, prefix="/api/v1")
app.include_router(ponto.router,        prefix="/api/v1")
app.include_router(relatorios.router,   prefix="/api/v1")


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "sistema": "RH API v1.0.0"}