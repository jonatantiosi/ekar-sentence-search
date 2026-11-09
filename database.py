import json
import sqlite3
import unicodedata
from pathlib import Path

PASTA = Path(__file__).parent
CAMINHO_BANCO = PASTA / 'tupi.db'
CAMINHO_FRASES = PASTA / 'acervo_frases.json'
CAMINHO_PALAVRAS = PASTA / 'acervo_palavras.json'

SCHEMA = """
CREATE TABLE IF NOT EXISTS words (
    id          INTEGER PRIMARY KEY,
    headword    TEXT NOT NULL UNIQUE,
    normalized  TEXT NOT NULL,
    meaning     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sentences (
    id           INTEGER PRIMARY KEY,
    tupi         TEXT NOT NULL UNIQUE,
    normalized   TEXT NOT NULL,
    translation  TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_words_normalized ON words(normalized);
CREATE INDEX IF NOT EXISTS idx_sentences_normalized ON sentences(normalized);
"""


def normalizar(texto: str) -> str:
    '''Versão de busca do texto: sem acentos, sem diferença de maiúsculas,
    com apóstrofo padronizado. Ex.: "Îasy n’-a" -> "iasy n'-a"
    '''
    texto = texto.strip()

    # padroniza as variações de apóstrofo para o apóstrofo comum (')
    for variante in ('’', '‘', 'ʼ'):
        texto = texto.replace(variante, "'")

    # NFD separa cada letra acentuada em letra base + acento combinante
    # ex.: "î" vira "i" + "◌̂"
    texto = unicodedata.normalize('NFD', texto)

    # remove os acentos combinantes (categoria Unicode "Mn")
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')

    # minúsculas (casefold é uma versão mais forte do lower())
    return texto.casefold()


def criar_tabelas(conexao):
    conexao.executescript(SCHEMA)


def carregar_json(caminho):
    with open(caminho, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)


def importar_json(conexao):
    '''Importa os JSONs para o banco. INSERT OR IGNORE pula duplicatas
    graças aos UNIQUE, então pode ser executado mais de uma vez.
    '''
    novas_palavras = 0
    for item in carregar_json(CAMINHO_PALAVRAS):
        for headword, meaning in item.items():
            cursor = conexao.execute(
                'INSERT OR IGNORE INTO words (headword, normalized, meaning) '
                'VALUES (?, ?, ?)',
                (headword, normalizar(headword), meaning),
            )
            novas_palavras += cursor.rowcount

    novas_frases = 0
    for par in carregar_json(CAMINHO_FRASES):
        tupi = par[0]['Frase']
        traducao = par[1]['Traducao']
        cursor = conexao.execute(
            'INSERT OR IGNORE INTO sentences (tupi, normalized, translation) '
            'VALUES (?, ?, ?)',
            (tupi, normalizar(tupi), traducao),
        )
        novas_frases += cursor.rowcount

    conexao.commit()
    return novas_palavras, novas_frases


if __name__ == '__main__':
    conexao = sqlite3.connect(CAMINHO_BANCO)
    try:
        criar_tabelas(conexao)
        palavras, frases = importar_json(conexao)
        print(f'Banco pronto: {CAMINHO_BANCO.name}')
        print(f'{palavras} palavra(s) e {frases} frase(s) importadas.')
    finally:
        conexao.close()
