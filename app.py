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
    logging.info(f'Downloading: {url} -> {out.as_posix()}')
    file = requests.get(url, stream=True)
    zipcontent = zipfile.ZipFile(io.BytesIO(file.content))
    zipcontent.extractall(out.as_posix())

    return out

OUTPUT = Path(os.environ.get('OUTPUT_DIR'))
OUTPUT.mkdir(exist_ok=True, parents=True)

BASE_URL = 'http://agencia.tse.jus.br/estatistica/sead/odsele'
URL_CANDIDATOS = BASE_URL + '/consulta_cand/consulta_cand_2018.zip'
URL_PRESTACAO_CONTAS = BASE_URL + '/prestacao_contas/prestacao_de_contas_eleitorais_candidatos_2018.zip'

TEMP = Path('/tmp')
candidatos = download(URL_CANDIDATOS, TEMP)
prestacao_contas = download(URL_PRESTACAO_CONTAS, TEMP)


shutil.move(
    candidatos.joinpath('consulta_cand_2018_BRASIL.csv'),
    OUTPUT.joinpath('consulta_cand_2018_BRASIL.csv')
)
shutil.move(
    prestacao_contas.joinpath('despesas_contratadas_candidatos_2018_BRASIL.csv'),
    OUTPUT.joinpath('despesas_contratadas_candidatos_2018_BRASIL.csv')
)