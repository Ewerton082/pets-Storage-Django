# Pets

Pets é uma plataforma para controle de estoque e venda de rações feito com o Framework Django.

### Requisitos

Antes de começar, verifique se você tem as seguintes ferramentas instaladas:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Rodando a aplicação

1. **Clone o repositório:**

Se ainda não tiver o repositório, clone-o para sua máquina local:

```bash
 git clone https://github.com/Ewerton082pets-Storage-Django.git
 cd pets-Storage-Django
```

2. **Crie um arquivo .env:**

```bash
# .env

# Credenciais para um banco de dados PostgreSQL.
DATABASE_NAME=pets_dev
DATABASE_USER=postgres_user
DATABASE_PASSWORD=postgres_password
DATABASE_HOST=db
DATABASE_URL=postgres://postgres_user:postgres_password@db:5432/pets_dev

# Auto reload
DEBUG=True
```

3. **Suba a aplicação:**

```bash
docker compose up

# Rode em segundo plano, se preferir
docker compose up -d
```