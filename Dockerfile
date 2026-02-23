FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Primeiro copiamos os arquivos de dependência
COPY pyproject.toml uv.lock ./
# Instalamos as dependências do projeto gerando o .venv
RUN uv sync --frozen

# Em seguida, copiamos o código fonte
COPY . .

EXPOSE 8000
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
