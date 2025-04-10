# Pets Food Storage

Este projeto é uma plataforma para controle de estoque e venda de rações feito com o Framework Django.

### Requisitos

Antes de começar, verifique se você tem as seguintes ferramentas instaladas:

- [Docker](https://www.docker.com/get-started)  
- [Docker Compose](https://docs.docker.com/compose/install/)

### Rodando a aplicação

1. **Clone o repositório:**

Se ainda não tiver o repositório, clone-o para sua máquina local:

```bash
git clone https://github.com/Ewerton082/pets-Storage-Django.git
cd pets-Storage-Django
```

2. **Crie um arquivo .env:**

```bash
# .env

# Chave secreta do Django. Você pode gerar uma nova em: https://djecrety.ir/
SECRET_KEY=sua_chave_secreta_aqui

# Ativa o modo de depuração (True para desenvolvimento, False para produção)
DEBUG_MODE=True

# Host da aplicação. Para rodar localmente, use 127.0.0.1
HOST=127.0.0.1

# Configurações do PostgreSQL
POSTGRES_DB=nome_do_banco
POSTGRES_USER=usuario
POSTGRES_PASSWORD=senha
DATABASE_HOST=database
DATABASE_PORT=5432
```

3. **Suba a aplicação:**

```bash
docker compose up

# Rode em segundo plano, se preferir
docker compose up -d

# Pare a aplicação, caso necessário
docker compose down
```

4. **Crie um usuário admin**

```bash
docker-compose exec app python manage.py createsuperuser
```

5. **Abra a aplicação no seu navegador**

Acesse: http://localhost:8000

### Seed do banco de dados

Para popular o banco de dados com as marcas e os produtos:

```bash
# Adicionar marcas
python manage.py seed_brand Seeds/new_brands.csv

# Adicionar rações (relacionadas às marcas)
python manage.py seed_pet_food Seeds/new_foods.csv
```
