import psycopg2
from sqlalchemy import create_engine, text

# entra com suas credenciais do PostgreSQL
username = 'postgres'
password = 'postgres'
host = 'localhost'
port = '5433'
database = 'EMPRESA'

# Criar a engine de conexão
engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')

# Conectar
connection = engine.connect()

print("Conectado a la base de datos PostgreSQL con éxito.")


# encerra a conexão
connection.close()

