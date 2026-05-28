# Sistema de RH

Sistema fullstack para gerenciamento de funcionários e análise de ponto eletrônico.

## Tecnologias

**Backend:** Python 3.11 · FastAPI · SQLAlchemy · MySQL · Pandas · Clean Architecture

**Frontend:** React · Vite

## Funcionalidades

- Cadastro e gerenciamento de setores e funcionários
- Upload de CSV com registros de ponto eletrônico
- Cálculo automático de horas trabalhadas, atrasos e horas extras
- Relatórios mensais por setor com gráficos
- Comparativo entre setores
- Integração com LLM para insights automáticos *(em breve)*

## Como rodar

**Pré-requisitos:** Python 3.11+, Node.js 20+, MySQL 8.0

**Backend**
```bash
cd app
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

**`.env` — crie na raiz do projeto**

DATABASE_URL=mysql+pymysql://root:senha@localhost:3306/rh_sistema


## Formato do CSV de ponto

```csv
funcionario_id,nome,setor,data,hora_entrada,hora_saida
001,Ana Silva,TI,2026-05-01,08:05,17:10
002,Carlos Mendes,Financeiro,2026-05-01,09:20,18:00
```

## API

Documentação interativa disponível em `http://localhost:8000/docs`

## Autor

Lucas Souza
