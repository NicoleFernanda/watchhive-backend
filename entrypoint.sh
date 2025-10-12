#!/bin/sh

# Necessário ter o 'netcat' instalado no Dockerfile (como discutido anteriormente)
# Espera o banco de dados 'watchhive_postgres' estar pronto
export UV_CACHE_DIR="/tmp/uv_cache"

cd /app

echo "Rodando migracoes Alembic."
/app/.venv/bin/alembic upgrade head 
echo "Migracoes concluídas."

# 2. Inicia a aplicação (Substituindo 'poetry run uvicorn')
# Usamos 'exec' para garantir que o script seja substituído pelo processo do servidor.
# Adapte este comando para o SEU formato de inicialização:
exec /app/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1
# Chama o binário uvicorn diretamente.