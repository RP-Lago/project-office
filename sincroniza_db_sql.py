# Importar as bibliotecas
from sqlalchemy import text
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

# Constantes
USER = "operador"
PASSWORD = "000000"
SERVER = r"********\SQLEXPRESS"
PRIMARY_DB = "DB_*"
CLONED_DB = "DB_*"
DRIVER_ODBC = "ODBC+Driver+17+for+SQL+Server"


# Configuração do banco de dados
Base = declarative_base()

# Criar uma conexão com o banco de dados padrão
engine_padrao = sa.create_engine(f"mssql+pyodbc://{USER}:{PASSWORD}@{SERVER}/{PRIMARY_DB}?driver={DRIVER_ODBC}")

# Criar uma conexão com o banco de dados clonado
engine_clonado = sa.create_engine(f"mssql+pyodbc://{USER}:{PASSWORD}@{SERVER}/{CLONED_DB}?driver={DRIVER_ODBC}")

# Obter os esquemas dos db's
with engine_padrao.connect() as connection:
    query = text("SELECT name FROM sys.schemas WHERE name IS NOT NULL")
    schema_padrao = connection.execute(query).fetchall()

with engine_clonado.connect() as connection:
    query = text("SELECT name FROM sys.schemas WHERE name IS NOT NULL")
    schema_clonado = connection.execute(query).fetchall()

# Comparar os esquemas nos db's
diff_padrao_to_clonado = set(schema_padrao) - set(schema_clonado)
diff_clonado_to_padrao = set(schema_clonado) - set(schema_padrao)

# Cria o esquema no banco de dados clonado
for schema_name in diff_padrao_to_clonado:
    print(f"Criando o esquema '{schema_name[0]}' no banco de dados clonado...")
    with engine_clonado.connect() as connection:
        query = text(f"CREATE SCHEMA {schema_name[0]}")
        connection.execute(query)
        connection.commit()

# Escluir os esquemas do banco de dados que não estão no db_padrão
for schema_name in diff_clonado_to_padrao:
    print(f"Excluindo o esquema '{schema_name[0]}' do banco de dados clonado...")
    with engine_clonado.connect() as connection:
        query = text(f"DROP SCHEMA {schema_name[0]}")
        connection.execute(query)
        connection.commit()

# Verificar se todos os esquemas estão sincronizados
if not diff_padrao_to_clonado and not diff_clonado_to_padrao:
    print('Todos os esquemas estão sincronizados.')
else:
    print('As alterações foram realizadas para sincronizar os esquemas.')