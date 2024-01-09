#Crie um script que, para cada bando de dados existente no retorna da list_database.py, liste os schemas existentes e salve em um arquivo json com banco como chave e um ou mais schemas como valores.

import psycopg2
from sqlalchemy import create_engine, text
import json

# Definindo as variáveis de conexão
HOST = "localhost"
PORT = 5433
DATABASE = "postgres"
USERNAME = "postgres"
PASSWORD = "postgres"

# Criando a conexão com o banco de dados
engine = create_engine(
    f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

# Obtendo a lista de bancos de dados
query = text(
    """
    SELECT datname
    FROM pg_database
    WHERE datname NOT IN ('postgres', 'template0', 'template1')
    """
)

with engine.connect() as connection:
    result = connection.execute(query)

# Criando um dicionário para armazenar os dados dos bancos de dados e seus schemas
databases = {}

# Iterando sobre os bancos de dados
for row in result:
    database_name = row[0]

    # Definindo a consulta SQL para listar os schemas do banco de dados atual
    query = text(
        """
        SELECT
            *,
            schema_name
        FROM
            information_schema.schemata
        WHERE
            schema_name NOT IN ('information_schema', 'pg_catalog')
        """
    )

    # Executando a consulta
    with engine.connect() as connection:
        result = connection.execute(query)

    # Coletando os resultados da consulta
    schemas = []
    for row in result:
        schemas.append({"*": row[0], "schema_name": row[1]})

    # Adicionando os schemas ao dicionário de bancos de dados
    databases[database_name] = schemas

# Gravando os resultados em um arquivo JSON
with open("databases_schemas.json", "w") as f:
    json.dump(databases, f)


