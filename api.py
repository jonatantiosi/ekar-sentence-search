from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse

from search import buscar_definicao, conectar, pesquisar_frases

PASTA_STATIC = Path(__file__).parent / 'static'

app = FastAPI(
    title='Busca de sentenças Tupi-Português',
    description='API somente leitura para pesquisar frases e palavras.',
)


@app.get('/', include_in_schema=False)
def pagina_inicial():
    '''Página de busca'''
    return FileResponse(PASTA_STATIC / 'index.html')


@app.get('/api/search')
def pesquisar(q: str = Query(..., max_length=100, description='Palavra a pesquisar')):
    '''Retorna as frases que contêm a palavra e a definição dela, se existir'''
    if not q.strip():
        raise HTTPException(status_code=400, detail='Informe uma palavra.')

    conexao = conectar()
    try:
        frases = pesquisar_frases(conexao, q)
        definicao = buscar_definicao(conexao, q)
    finally:
        conexao.close()

    return {
        'busca': q,
        'definicao': definicao,
        'frases': [
            {'tupi': tupi, 'traducao': traducao, 'fonte': fonte}
            for tupi, traducao, fonte in frases
        ],
    }


@app.get('/api/words/{palavra}')
def consultar_palavra(palavra: str):
    '''Retorna a definição de uma palavra'''
    conexao = conectar()
    try:
        definicao = buscar_definicao(conexao, palavra)
    finally:
        conexao.close()

    if definicao is None:
        raise HTTPException(status_code=404, detail='Palavra não encontrada.')
    return {'palavra': palavra, 'definicao': definicao}
