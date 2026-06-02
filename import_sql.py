import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import unicodedata
import time

inicio = time.time()

# Limpeza

def limpar_texto(coluna):
    return (
        coluna.astype(str)
        .str.strip()
        .apply(lambda x: unicodedata.normalize('NFKC', x))
    )

# Conectar ao SQL

server = r''
database = 'arxiv_articlesDB'

connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    f'SERVER={server};'
    f'DATABASE={database};'
    'Trusted_Connection=yes;'
)

params = quote_plus(connection_string)

engine = create_engine(f'mssql+pyodbc:///?odbc_connect={params}')

# Obras

df_obras = pd.read_csv(
    r'arxiv_dataset\CSVs\amostra_csv.csv',
    encoding='utf-8',
    dtype={'id_obra': str}
)

df_obras = df_obras.drop(columns=['abstract'], errors='ignore')

df_obras = df_obras.drop_duplicates(
    subset=['id_obra']
)

df_obras.to_sql(
    'obras',
    con=engine,
    if_exists='append',
    index=False,
    chunksize=1000
)

print('Tabela obras importada.')

# Autores

df_autores = pd.read_csv(
    r'arxiv_dataset\CSVs\autores_csv.csv',
    encoding='utf-8'
)

# normaliza unicode
df_autores['nome_autor'] = (
    df_autores['nome_autor']
    .astype(str)
    .str.strip()
    .apply(lambda x: unicodedata.normalize('NFKC', x))
)

# remove duplicados do próprio dataframe
df_autores = df_autores.drop_duplicates(
    subset=['nome_autor']
)

# importa
df_autores.to_sql(
    'autores',
    con=engine,
    if_exists='append',
    index=False,
    chunksize=1000
)

print('Tabela autores importada.')

# Autor-Obra

df_autor_obra = pd.read_csv(
    r'arxiv_dataset\CSVs\autor_obra_csv',
    encoding='utf-8',
    dtype={'id_obra': str}
)

df_autor_obra['nome_autor'] = limpar_texto(
    df_autor_obra['nome_autor']
)

df_autor_obra = df_autor_obra.drop_duplicates(
    subset=['id_obra', 'nome_autor']
)

autor_obra_existente = pd.read_sql(
    """
    SELECT id_obra, nome_autor
    FROM autor_obra
    """,
    engine
)

autor_obra_existente['id_obra'] = (
    autor_obra_existente['id_obra']
    .astype(str)
)

autor_obra_existente['nome_autor'] = limpar_texto(
    autor_obra_existente['nome_autor']
)

df_autor_obra = df_autor_obra.merge(
    autor_obra_existente,
    on=['id_obra', 'nome_autor'],
    how='left',
    indicator=True
)

df_autor_obra = df_autor_obra[
    df_autor_obra['_merge'] == 'left_only'
]

df_autor_obra = df_autor_obra.drop(
    columns=['_merge']
)

df_autor_obra.to_sql(
    'autor_obra',
    con=engine,
    if_exists='append',
    index=False,
    chunksize=1000
)

print('Tabela autor_obra importada.')

# Categorias

df_categorias = pd.read_csv(
    r'arxiv_dataset\CSVs\categorias_csv.csv',
    encoding='utf-8'
)

df_categorias['nome_categoria'] = limpar_texto(
    df_categorias['nome_categoria']
)

df_categorias = df_categorias.drop_duplicates(
    subset=['nome_categoria']
)

categorias_existentes = pd.read_sql(
    "SELECT nome_categoria FROM categorias",
    engine
)

categorias_existentes['nome_categoria'] = limpar_texto(
    categorias_existentes['nome_categoria']
)

df_categorias = df_categorias[
    ~df_categorias['nome_categoria'].isin(
        categorias_existentes['nome_categoria']
    )
]

df_categorias.to_sql(
    'categorias',
    con=engine,
    if_exists='append',
    index=False,
    chunksize=1000
)

print('Tabela categorias importada.')

# Categoria-Obra

df_categoria_obra = pd.read_csv(
    r'arxiv_dataset\CSVs\categoria_obra.csv',
    encoding='utf-8',
    dtype={'id_obra': str}
)

df_categoria_obra['nome_categoria'] = limpar_texto(
    df_categoria_obra['nome_categoria']
)

df_categoria_obra = df_categoria_obra.drop_duplicates(
    subset=['id_obra', 'nome_categoria']
)

categoria_obra_existente = pd.read_sql(
    """
    SELECT id_obra, nome_categoria
    FROM categoria_obra
    """,
    engine
)

categoria_obra_existente['id_obra'] = (
    categoria_obra_existente['id_obra']
    .astype(str)
)

categoria_obra_existente['nome_categoria'] = limpar_texto(
    categoria_obra_existente['nome_categoria']
)

df_categoria_obra = df_categoria_obra.merge(
    categoria_obra_existente,
    on=['id_obra', 'nome_categoria'],
    how='left',
    indicator=True
)

df_categoria_obra = df_categoria_obra[
    df_categoria_obra['_merge'] == 'left_only'
]

df_categoria_obra = df_categoria_obra.drop(
    columns=['_merge']
)

df_categoria_obra.to_sql(
    'categoria_obra',
    con=engine,
    if_exists='append',
    index=False,
    chunksize=1000
)

print('Tabela categoria_obra importada.')

fim = time.time()

print(f'Tempo de execução: {fim - inicio:.2f} segundos')