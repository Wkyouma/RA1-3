# Igor Terplak: wkyouma, Kevin Henriques: kevinhag
#Grupo: RA1-3
import sys

# pegar tokens de uma expressão, considerando números, identificadores, operadores e parênteses
def parseExpressao(linha):
    tokens = []
    acum = ""


    for char in linha:
        if char.isalnum() or char == '.':
            acum += char
            continue

        if char == '-' and (not tokens or tokens[-1] in ['(', '+', '-', '*', '/', '//', '%', '^']):
            estado_inicial(tokens, '', acum)
            acum = char
            continue

        if not char.isspace() and char not in ['+', '-', '*', '/', '%', '^', '(', ')']:
            return 'INVALIDO'

        estado_inicial(tokens, char, acum)
        if 'ERRO' in tokens:  
            return 'INVALIDO'
        acum = ""

    estado_inicial(tokens, '', acum)
    if 'ERRO' in tokens:     
        return 'INVALIDO'
    
    if tokens.count('(') != tokens.count(')'):#verificar se os parenteses estão balanceados
        return 'INVALIDO'
    return tokens

# Estados ADF para processar números, identificadores, operadores e parênteses

def estado_inicial(tokens, char, acum):
    if acum:
        if acum[0].isalpha():
            estado_identificador(tokens, acum)
        else:
            estado_numero(tokens, acum)
    if char.isspace():
        return
    elif char in ['+', '-', '*', '/', '%', '^']:
        estado_operador(tokens, char)
    elif char in ['(', ')']:
        estado_parenteses(tokens, char)

def estado_numero(tokens, valor):
    if valor.count('.') > 1:
        tokens.append('ERRO')
        return
    tokens.append(valor)

def estado_identificador(tokens, nome):
    if not nome.isupper():
        tokens.append('ERRO')
        return
    tokens.append(nome)

def estado_operador(tokens, char):
    if char == '/' and tokens and tokens[-1] == '/':
        tokens[-1] = '//'
    else:
        tokens.append(char)

def estado_parenteses(tokens, char):
    tokens.append(char)



# Executar expressão usando uma pilha, considerando variáveis, histórico e operações
def executarExpressao(tokens, memoria, historico):
    if tokens is None: return "ERRO LÉXICO"
    pilha = []

    inner = [t for t in tokens if t not in ['(', ')']]
    ops = {'+', '-', '*', '/', '//', '%', '^'}
    if inner and inner[-1][0].isalpha() and inner[-1] != 'RES' and not any(t in ops for t in inner):
        if len(inner) == 2:
            alvo = inner[-1]   
        elif len(inner) == 1:
            alvo = None        
        else:
            return "OPERAÇÃO INVÁLIDA" 
    else:
        alvo = None

    try:
        for token in tokens:
            if token in ['(', ')']:
                continue

            if token.lstrip('-').replace('.', '', 1).isdigit():
                pilha.append(float(token))
            
            elif token == 'RES':
                idx = int(pilha.pop()) if pilha else 1
                pilha.append(float(historico[-idx][1] if len(historico) >= idx else 0.0))
            
            elif token[0].isalpha():
                if token == alvo:
                    if pilha:
                        memoria[token] = pilha[-1]
                    continue
                pilha.append(float(memoria.get(token, 0.0)))
                
            elif token in ['+', '-', '*', '/', '//', '%', '^']:
                if len(pilha) < 2:
                    raise IndexError
                
                b = pilha.pop()
                a = pilha.pop()
                if token == '+': pilha.append(a + b)
                elif token == '-': pilha.append(a - b)
                elif token == '*': pilha.append(a * b)
                elif token == '/': pilha.append(a / b)
                elif token == '//':
                    if b == 0: 
                        raise ZeroDivisionError
                    pilha.append(int(a) // int(b))
                elif token == '%': pilha.append(a % b)
                elif token == '^': pilha.append(a ** int(abs(b)))

        if pilha: 
            return pilha[-1]
        else:
            return "EXPRESSAO VAZIA"
    except IndexError:
        return "OPERAÇÃO INVÁLIDA"
    except ZeroDivisionError:
        return "DIVISAO POR ZERO"
    except Exception:
        return "ERRO"

# Ler arquivo 
def lerArquivo(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as f:
        return [linha.strip() for linha in f if linha.strip()]

#exportar tokens para txt
def exportarTokens(tokens, nomeArquivo):
    with open(nomeArquivo, "w") as arquivo:
        for linha in tokens:
            arquivo.write(str(linha) + "\n")


def funcaoTeste():
    memoria = {}   
    historico = []  
    
    linhas = ['(15 5 +)',
              '(20 Asa)',
              '(29 1 +)',
              '(29 10 +)',
              '((20 10 +) 20 +)',
              '(Asa 20 +)',
              '((2 RES) 1 -)',
              '(1 2 v)']

    for linha in linhas:
        tokens = parseExpressao(linha)
        resultado = executarExpressao(tokens, memoria, historico)
        historico.append((linha, resultado))
        print(f"Expressão: {linha} -> Tokens: {tokens} -> Resultado: {resultado}")

