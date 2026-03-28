import Analisador
import sys
import Transformador64 as t64

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
        historico.append((linha, resultado))
        tokensList.append(tokens)
        
    Analisador.exportarTokens(tokensList, "tokens.txt")

    tokens = t64.readFile("tokens.txt")
    assemblyCode = t64.generateAssembly(tokens, "")
    with open("output.s", "w") as f:
        f.write(assemblyCode)
    print("Assembly gerado em output.s")

    print("Histórico de Expressões e Resultados:")
    print(historico)
    print('Memoria:' ,memoria)

 