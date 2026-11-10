import sqlite3

from database import CAMINHO_BANCO, normalizar


def conectar(somente_leitura=True):
    '''Abre o banco. Por padrão em modo somente leitura, para que a busca
    pública nunca consiga alterar os dados.
    '''
    if somente_leitura:
        return sqlite3.connect(CAMINHO_BANCO.as_uri() + '?mode=ro', uri=True)
    return sqlite3.connect(CAMINHO_BANCO)


def pesquisar_frases(conexao, palavra):
    '''Retorna uma lista de (frase, tradução, fonte) com todas as frases
    que contêm a palavra pesquisada. A fonte é None quando não foi informada.
    '''
    termo = normalizar(palavra)
    return conexao.execute(
        'SELECT tupi, translation, fonte FROM sentences '
        'WHERE instr(normalized, ?) > 0 ORDER BY id',
        (termo,),
    ).fetchall()


def buscar_definicao(conexao, palavra):
    '''Retorna a definição da palavra, ou None se ela não existir'''
    linha = conexao.execute(
        'SELECT meaning FROM words WHERE normalized = ?',
        (normalizar(palavra),),
    ).fetchone()
    return linha[0] if linha else None
