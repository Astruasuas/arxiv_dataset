"""
Esse script pega a amostra nova, extrai as informações relevantes e transforma em CSVs.
Os dados estão em LaTeX.
"""

from pylatexenc.latex2text import LatexNodes2Text
import json
import csv
from datetime import datetime
from tqdm import tqdm

barra = tqdm(desc='Processando', unit=" linha")

# Func pra fazer as limpezas
def limpar_texto(texto):
    if not isinstance(texto, str):
        return texto

    try:
        texto = LatexNodes2Text().latex_to_text(texto)

    except Exception:
        pass

    texto = texto.replace('\n', ' ').strip()
    texto = ' '.join(texto.split())

    return texto

with (
    open('amostras/amostra.json', 'r') as a,
    open('CSVs/amostra_csv.csv', 'w', newline='', encoding='utf-8') as amostra_csv,                    # Todas as infos de obras
    open('CSVs/autores_csv.csv', 'w', newline='', encoding='utf-8') as autores_csv,                    # Autor com Id
    open('CSVs/autor_obra_csv', 'w', newline='', encoding='utf-8') as autor_obra_csv,                  # Relação entre autores e obras escritas por eles
    open('CSVs/categorias_csv.csv', 'w', newline='', encoding='utf-8') as categorias_csv,              # Categorias com Id
    open('CSVs/categoria_obra.csv', 'w', newline='', encoding='utf-8') as categoria_obra_csv):         # Relação entre obras e categorias

    writer_amostra = csv.DictWriter(
        amostra_csv,
        fieldnames=[
            'id_obra',
            'titulo',
            'autores',
            'categorias',
            'doi',
            'data_criacao',
            'ultima_atualizacao'
        ]
    )

    writer_autores = csv.DictWriter(
        autores_csv,
        fieldnames=[
            'nome_autor'
        ]
    )

    writer_autorobra = csv.DictWriter(
        autor_obra_csv,
        fieldnames=[
            'id_obra',
            'nome_autor'
        ]
    )

    writer_categoria = csv.DictWriter(
        categorias_csv,
        fieldnames=[
            'nome_categoria'
        ]
    )

    writer_categoriaobra = csv.DictWriter(
        categoria_obra_csv,
        fieldnames=[
            'id_obra',
            'nome_categoria'
        ]
    )

    writer_amostra.writeheader()
    writer_autores.writeheader()
    writer_autorobra.writeheader()
    writer_categoria.writeheader()
    writer_categoriaobra.writeheader()

    for linha in a:
        obra = json.loads(linha)

        id_obra = obra.get('id')
        titulo = limpar_texto(obra.get('title'))
        autores = limpar_texto(obra.get('authors'))
        autores_parsed = obra.get('authors_parsed')
        categorias = limpar_texto(obra.get('categories'))
        doi = limpar_texto(obra.get('doi'))

        data_semform = obra.get('versions')[0]['created']
        data_criacao = datetime.strptime(data_semform, '%a, %d %b %Y %H:%M:%S GMT').strftime('%Y-%m-%d')

        ultima_atualizacao = obra.get('update_date')

        writer_amostra.writerow({
            'id_obra': id_obra,
            'titulo': titulo,
            'autores': autores,
            'categorias': categorias,
            'doi': doi,
            'data_criacao': data_criacao,
            'ultima_atualizacao': ultima_atualizacao
        })

        for autor in autores_parsed:

            nome_autor = f'{autor[0]}, {autor[1]}'

            writer_autores.writerow({
                'nome_autor': nome_autor
            })

            writer_autorobra.writerow({
                'id_obra': id_obra,
                'nome_autor': nome_autor
            })

        categorias_obra = categorias.split()

        for categoria in categorias_obra:

            writer_categoria.writerow({
                'nome_categoria': categoria
            })

            writer_categoriaobra.writerow({
                'id_obra': id_obra,
                'nome_categoria': categoria
            })

        barra.update(1)

barra.close()


# Tempo de processamento: 3h23m10s | 1h01m27s



