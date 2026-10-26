# 🍕 Pizzaria API

API RESTful para gerenciamento e pedidos de pizzaria desenvolvida com **FastAPI**, **SQLAlchemy** e **Alembic**.

## 🚀 Funcionalidades

- **Autenticação & Segurança**:
  - Cadastro de usuários com senhas criptografadas via `bcrypt`.
  - Autenticação e geração de tokens JWT (`access_token` e `refresh_token`).
  - Suporte ao fluxo de formulário OAuth2 (`OAuth2PasswordRequestForm`) para integração direta com o Swagger UI (`/docs`).
- **Gerenciamento de Pedidos**:
  - Criação e consulta de pedidos vinculados a usuários.
  - Controle de status do pedido (`PENDENTE`, `FINALIZADO`, `CANCELADO`).
- **Banco de Dados & Migrations**:
  - SQLite com suporte a migrações gerenciadas pelo Alembic.

---

## 🛠️ Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/) & [SQLAlchemy-Utils](https://sqlalchemy-utils.readthedocs.io/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [python-jose](https://github.com/mpdavis/python-jose) (JWT)
- [passlib](https://passlib.readthedocs.io/) & [bcrypt](https://github.com/pyca/bcrypt/)
- [Pydantic](https://docs.pydantic.dev/)

---

## ⚙️ Instalação e Execução

### 1. Clonar o repositório e acessar a pasta
```bash
git clone https://github.com/allissonsantosdev/Pizzaria.git
cd Pizzaria
```

### 2. Criar e ativar o ambiente virtual
```bash
python -m venv .venv

# No Windows (PowerShell):
.venv\Scripts\activate

# No Linux / macOS:
source .venv/bin/activate
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto baseado no `.env.example`:
```ini
SECRET_KEY=sua_chave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Executar as migrações do banco de dados
```bash
alembic upgrade head
```

### 6. Iniciar o servidor
```bash
uvicorn main:app --reload
```

---

## 📖 Documentação da API

Após iniciar a aplicação, acesse a documentação interativa:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
