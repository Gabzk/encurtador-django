# Encurtador de URL API

Uma API REST desenvolvida em **Django** e **Django REST Framework (DRF)** para encurtamento de URLs, com banco de dados SQLite. Orientada a testes (TDD) e empacotada em **Docker** utilizando gerenciamento moderno de dependências com **uv**.

## 🚀 Tecnologias

- Python 3.12+
- Django 6.0+
- Django REST Framework
- `uv` (Gerenciador ultrarrápido de pacotes Python)
- Docker & Docker Compose
- Banco de dados SQLite (padrão)

## 📋 Pré-requisitos

Para rodar este projeto, você precisa apenas do **Docker** e **Docker Compose** instalados na sua máquina.

*(Opcional: [uv](https://docs.astral.sh/uv/) instalado localmente caso queira rodar o projeto fora do Docker)*

## 🛠️ Como Executar

### Utilizando Docker (Recomendado)

O projeto já está configurado para rodar os testes e a API completamente dentro do Docker.

1. Clone o repositório ou acesse o diretório do projeto.
2. Suba o contêiner com a API:
   ```bash
   docker compose up --build
   ```
3. A API estará acessível em `http://localhost:8000`.

### Rodando Localmente com `uv`

Caso prefira rodar fora do Docker:

1. Instale as dependências e ative o ambiente virtual:
   ```bash
   uv sync
   # Para bash/zsh:
   source .venv/bin/activate
   # Para fish:
   source .venv/bin/activate.fish
   ```
2. Realize as migrações:
   ```bash
   uv run python manage.py migrate
   ```
3. Inicie o servidor:
   ```bash
   uv run python manage.py runserver
   ```

## 🧪 Testes

Todo o projeto foi desenvolvido com metodologia TDD. Para rodar a suite de testes automatizada, execute o seguinte comando:

### Via Docker
```bash
docker compose run web uv run python manage.py test
```

### Localmente
```bash
uv run python manage.py test
```

## 🌐 Endpoints da API

A aplicação possui dois fluxos principais documentados abaixo:

### 1. Encurtar uma URL (`POST`)

Endpoint para criar uma versão curta de uma URL longa.

- **URL:** `/api/urls/`
- **Method:** `POST`
- **Content-Type:** `application/json`

**Corpo da Requisição (Exemplo):**
```json
{
  "original_url": "https://www.google.com/search?q=django+rest+framework"
}
```

**Resposta de Sucesso (201 Created):**
```json
{
  "id": 1,
  "original_url": "https://www.google.com/search?q=django+rest+framework",
  "short_code": "aB3cD4",
  "created_at": "2023-10-27T10:00:00.000000Z"
}
```

### 2. Redirecionamento da URL Encurtada (`GET`)

Esse não é bem um endpoint de API REST tradicional, mas sim a porta de entrada para os usuários. Quando acessado pelo navegador ou cliente, ele valida o código curto e, se encontrar, devolve um redirecionamento HTTP **302** para a URL original.

- **URL:** `/<short_code>` (exemplo: `http://localhost:8000/aB3cD4`)
- **Method:** `GET`

**Respostas:**
- **Status 302 Found:** Redireciona imediatamente para o site original se o código for válido.
- **Status 404 Not Found:** Retorna o erro padrão do Django caso o código curto não exista no banco.
