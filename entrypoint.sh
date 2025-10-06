#!/bin/sh

# Necessário ter o 'netcat' instalado no Dockerfile (como discutido anteriormente)
# Espera o banco de dados 'watchhive_postgres' estar pronto
uv run alembic upgrade head
echo "Migrações concluídas."

# 2. Inicia a aplicação (Substituindo 'poetry run uvicorn')
# Usamos 'exec' para garantir que o script seja substituído pelo processo do servidor.
# Adapte este comando para o SEU formato de inicialização:
exec uv run fastapi run main.py --port 8000 --host 0.0.0.0