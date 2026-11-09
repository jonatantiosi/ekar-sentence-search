import os

from search import buscar_definicao, conectar, pesquisar_frases


def limpar_menu():
    '''limpa o terminal para windows e linux/mac'''
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    conexao = conectar()
    print('Busca de sentenças em Tupi-Português\n')

    try:
        while True:
            opcao = input(
                "[1] Pesquisar palavra\n"
                "[2] Sair\n"
            )

            match opcao:

                case "1":
                    limpar_menu()
                    palavra = input("Qual palavra deseja pesquisar?:\n")

                    if not palavra.strip():
                        print('Digite uma palavra para pesquisar.\n')
                        continue

                    frases = pesquisar_frases(conexao, palavra)
                    if not frases:
                        print('Nenhuma frase encontrada com essa palavra.\n')
                        continue

                    print()
                    for frase, traducao in frases:
                        print(f"Frase: {frase}\nTradução: {traducao}\n")

                    definicao = buscar_definicao(conexao, palavra)
                    if definicao is None:
                        definicao = 'Palavra sem definição.'
                    print(f"Definição de {palavra}: {definicao}\n")

                case "2":
                    break

                case _:
                    limpar_menu()
                    print('Opção inválida, selecione 1 ou 2.\n')
    finally:
        conexao.close()


if __name__ == '__main__':
    main()
