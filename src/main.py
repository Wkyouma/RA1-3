import Analisador

import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo.txt>")
        sys.exit(1)

    arquivo = sys.argv[1]
    linhas = Analisador.lerArquivo(arquivo)
    tokensList = []
    memoria = {}
    historico = []

    for linha in linhas:
        tokens = Analisador.parseExpressao(linha)
        resultado = Analisador.executarExpressao(tokens, memoria, historico)
        if isinstance(resultado, (int, float)):
            historico.append((linha, resultado))
        tokensList.append(tokens)

    Analisador.exportarTokens(tokensList, "tokens.txt")

    print("Histórico de Expressões e Resultados:")
    print(historico)
    print('Memoria:', memoria)


 