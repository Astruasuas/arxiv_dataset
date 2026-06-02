"""
Esse script pega a base original e transforma em uma amostra só com as obras de 2015-2025
"""

import json
from tqdm import tqdm

barra = tqdm(desc='Processando', unit=" linha")


with (open('amostras/arxiv-metadata-oai-snapshot.json', 'r', encoding='utf-8') as a,
      open('amostras/amostra.json', 'w') as teste):
    for linha in a:
        obra = json.loads(linha)
        if any(
                ano in obra['versions'][0]['created']
                for ano in ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']):
            json.dump(obra, teste)
            teste.write('\n')

            barra.update(1)

barra.close()
