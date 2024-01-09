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

# Criando um dicionário para armazenar os dados dos bancos de dados, schemas e tabelas
dados = {}

# Iterando sobre os bancos de dados
for row in result:
    database_name = row[0]

    # Criando um dicionário para armazenar os schemas e tabelas do banco de dados atual
    dados[database_name] = {}

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

    # Iterando sobre os schemas
    for row in result:
        schema_name = row[1]

        # Criando um dicionário para armazenar as tabelas do schema atual
        dados[database_name][schema_name] = []

        # Definindo a consulta SQL para listar as tabelas do schema atual
        query = text(
            """
            SELECT
                *,
                table_name
            FROM
                information_schema.tables
            WHERE
                table_schema = :schema_name
            """
        )

        # Executando a consulta
        with engine.connect() as connection:
            result = connection.execute(query, {'schema_name': schema_name})

        # Iterando sobre as tabelas
        for row in result:
            table_name = row[1]

            # Adicionando a tabela ao dicionário de tabelas do schema atual
            dados[database_name][schema_name].append(table_name)

# Gravando os resultados em um arquivo JSON
with open("dados_bancos_schemas_tabelas.json", "w") as f:
    json.dump(dados, f)
