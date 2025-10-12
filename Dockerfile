FROM python:3.13-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /app
WORKDIR /app

# --system para instalar no sistema do container.
RUN /bin/uv pip install --no-cache --system -r requirements.txt

# cria usuario (obrigatorio do choreo)
RUN groupadd -r choreo && useradd --no-log-init -r -g choreo -u 10001 choreo

COPY entrypoint.sh /app/entrypoint.sh

# 1. Muda a propriedade de TUDO em /app para o novo usuário.
RUN chown -R 10001:choreo /app

# 2. Garante que o entrypoint.sh é executável.
RUN chmod +x /app/entrypoint.sh

USER 10001

ENTRYPOINT ["/app/entrypoint.sh"]
