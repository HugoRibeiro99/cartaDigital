venv:
	source .venv/bin/activate 

run: 
	python -m uvicorn main:app --reload

# 1. Aplicar migrações (Atualizar o banco de dados para a versão mais recente)
migrate:
	alembic upgrade head

# 2. Criar uma nova migração automática
# Como usar: make revision m="adicionando coluna uuid"
revision:
	alembic revision --autogenerate -m "$(m)"

