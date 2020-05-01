from pathlib import Path
import requests
import zipfile
import logging
import io
import os
import shutil

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

def download(url: str, output_dir: Path):
    out = output_dir.joinpath(url.split('/')[-1])
    # logging.info(f'Downloading: {url} -> {out.as_posix()}')
    # file = requests.get(url, stream=True)
    # zipcontent = zipfile.ZipFile(io.BytesIO(file.content))
    # zipcontent.extractall(out.as_posix())

    return out

output = Path(os.environ.get('OUTPUT_DIR'))
output.mkdir(exist_ok=True, parents=True)

base_url = 'http://agencia.tse.jus.br/estatistica/sead/odsele'
url_candidatos = base_url + '/consulta_cand/consulta_cand_2018.zip'
url_prestacao_contas = base_url + '/prestacao_contas/prestacao_de_contas_eleitorais_candidatos_2018.zip'
temp = Path('/tmp')

candidatos = download(url_candidatos, temp)
prestacao_contas = download(url_prestacao_contas, temp)


shutil.move(
    candidatos.joinpath('consulta_cand_2018_AP.csv'),
    output.joinpath('consulta_cand_2018_AP.csv')
)

shutil.move(
    prestacao_contas.joinpath('despesas_contratadas_candidatos_2018_AP.csv'),
    output.joinpath('despesas_contratadas_candidatos_2018_AP.csv')
)

shutil.move(
    prestacao_contas.joinpath('receitas_candidatos_2018_AP.csv'),
    output.joinpath('receitas_candidatos_2018_AP.csv')
)