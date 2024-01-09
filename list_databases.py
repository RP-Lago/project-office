#Crie um script que acesse o postgres instalado em sua máquina e liste os bancos de dados existentes e salve em um arquivo JSON.

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

# Definindo a consulta SQL
query = text(
    """
    SELECT
        *,
        schema_name
    FROM
        information_schema.schemata
    """
)

# Executando a consulta
with engine.connect() as connection:
    result = connection.execute(query)

# Coletando os resultados da consulta
schemas = []
for row in result:
    schemas.append({"*": row[0], "schema_name": row[1]})

# Gravando os resultados em um arquivo JSON
with open("schemas_u.json", "w") as f:
    json.dump(schemas, f)
