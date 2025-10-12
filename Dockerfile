FROM python:3.13-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /app
WORKDIR /app

RUN /bin/uv pip install --no-cache -r requirements.txt

# cria usuario (obrigatorio do choreo)
RUN groupadd -r choreo && useradd --no-log-init -r -g choreo -u 10001 choreo

COPY entrypoint.sh /app/entrypoint.sh

RUN chown -R 10001:choreo /app

RUN chmod +x /app/entrypoint.sh

RUN chmod -R u+rwx /app

USER 10001

ENTRYPOINT ["/app/entrypoint.sh"] 

# Run the application. Tirei por causa do entrypoint; LOCAL: DEIXAR
#  CMD ["/app/.venv/bin/fastapi", "run", "main.py", "--port", "8000", "--host", "0.0.0.0"]