

tablePanel = {
    "0": "3F",
    "1": "06",
    "2": "5B",
    "3": "4F",
    "4": "66",
    "5": "6D",
    "6": "7D",
    "7": "07",
    "8": "7F",
    "9": "6F"
} # Tabela de mapeamento dos dígitos de 0 a 9 do painel (temporário?)

def generateAssembly(tokens, assemblyCode):

    depth = 0

    header = [
        ".global _start",
        ".equ HEX0, 0xFF200020",
        
    ]

    data = [
        ".section .data",   
        "const_1: .double 1.0", # Constante 1.0 para multiplicação inicial  
        "history: .space 800", # Espaço para 100 respostas (8 bytes cada)
        "history_ptr: .word 0" # Ponteiro para o histórico,
    ]

    usedVariables = []


    text = [
        ".section .text",
        "_start:"
    ]

    
    for i, token in enumerate(tokens):
        match token:
            case token if token.replace('.', '', 1).lstrip('-').isdigit(): # Permite negativos e decimais
                data.append(f"   val{i}: .double {token}")
                text.append(f"   ldr r0, =val{i}")
                text.append(f"   vldr d0, [r0]")
                text.append("    vpush {d0}")
            case '(': # Pra saber onde abre.
                text.append(f"    /* Início de expressão {depth} */")
                depth += 1
            case ')': # E onde fecha. Usar para saber quando termina a operação e guardar o resultado no d0. (talvez converta pra 32 aqui mesmo)
                depth -= 1
                text.append(f"    /* Fim de expressão {depth} */")  
                if depth == 0:
                    text.append("    vpop {d0} /* Resultado final da expressão */")

            case '+': # Adição
                text.append("    vpop {d1}")
                text.append("    vpop {d0}")
                text.append("    vadd.f64 d2, d0, d1")
                text.append("    vpush {d2}")
            case '-': # Subtração
                text.append("    vpop {d1}")
                text.append("    vpop {d0}")
                text.append("    vsub.f64 d2, d0, d1")
                text.append("    vpush {d2}")
            case '*': # Multiplicação
                text.append("    vpop {d1}")
                text.append("    vpop {d0}")
                text.append("    vmul.f64 d2, d0, d1")
                text.append("    vpush {d2}")
            case '/': # Divisão
                text.append("    vpop {d1}")
                text.append("    vpop {d0}")
                text.append("    vdiv.f64 d2, d0, d1")
                text.append("    vpush {d2}")
            case '//': # Divisão em inteiros
                text.append("    vpop {d1}")
                text.append("    vpop {d0}")
                text.append("    vdiv.f64 d2, d0, d1")
                text.append("    vcvt.s32.f64 s0, d2") # Trunca para int de 32 bits
                text.append("    vcvt.f64.s32 d2, s0") # Volta para float 64 bits
                text.append("    vpush {d2}")
            case '%': # Resto da divisão
                text.append("    vpop {d1}")
                text.append("    vpop {d0}")
                text.append("    vdiv.f64 d2, d0, d1") # A / B
                text.append("    vcvt.s32.f64 s0, d2")
                text.append("    vcvt.f64.s32 d2, s0") # d2 = int(A/B)
                text.append("    vmul.f64 d2, d2, d1") # d2 = B * int(A/B)
                text.append("    vsub.f64 d2, d0, d2") # d2 = A - (B * int(A/B))
                text.append("    vpush {d2}")
            case '^': # Potencia
                text.append("    vpop {d1}") # B (Expoente)
                text.append("    vpop {d0}") # A (Base)
                text.append("    vcvt.s32.f64 s1, d1") # Converte B para inteiro
                text.append("    vmov r1, s1")         # Move B para R1 (Contador do loop)
                text.append("    ldr r0, =const_1")    # Carrega 1.0
                text.append("    vldr d2, [r0]")       # d2 = 1.0 (Resultado inicial)
                text.append(f"loop_pot_{i}:")          # Rótulo único usando o índice do token
                text.append("    cmp r1, #0")          # O contador chegou a zero?
                text.append(f"   ble fim_pot_{i}")     # Se sim, sai do loop
                text.append("    vmul.f64 d2, d2, d0") # Multiplica d2 pela base (d0)
                text.append("    sub r1, r1, #1")      # Diminui 1 do contador
                text.append(f"   b loop_pot_{i}")      # Repete
                text.append(f"fim_pot_{i}:")
                text.append("    vpush {d2}")

            case 'RES':
                text.append("    /* COMANDO RES */")
                text.append("    vpop {d0}")                   # Pega 'N' da pilha
                text.append("    vcvt.s32.f64 s0, d0")         # Converte N para inteiro
                text.append("    vmov r1, s0")                 
                text.append("    ldr r2, =history_ptr")        # Pega o ponteiro do histórico
                text.append("    ldr r3, [r2]")                # r3 = Posição atual do histórico
                text.append("    mov r4, #8")                  
                text.append("    mul r1, r1, r4")              # N * 8 bytes
                text.append("    sub r3, r3, r1")              # Volta N casas no histórico
                text.append("    ldr r5, =history")            # Pega o início do histórico
                text.append("    add r5, r5, r3")              # Encontra o endereço exato
                text.append("    vldr d1, [r5]")               # Carrega a resposta antiga
                text.append("    vpush {d1}")
            
            case _: # Qualquer outro token, quero pegar nomes de variaveis ().
                var = token

                stored = (tokens[i-1] != '(')  # Se o token anterior for ( ou )

                if var not in usedVariables:
                    data.append(f"   {var}: .double 0.0")
                    usedVariables.append(var)

                if not stored:
                    text.append(f"    /* SALVANDO VARIÁVEL: {var} */")
                    text.append("    vpop {d0}")                 # Pega o valor calculado
                    text.append(f"   ldr r0, ={var}")            # Pega endereço da variável
                    text.append("    vstr d0, [r0]")             # Grava na memória RAM
                    text.append("    vpush {d0}")                # Mantém na pilha caso a conta continue
                else:
                    text.append(f"    /* LENDO VARIÁVEL: {var} */")
                    text.append(f"   ldr r0, ={var}")
                    text.append("    vldr d0, [r0]")             # Puxa o valor da memória RAM
                    text.append("    vpush {d0}")                # Joga na pilha FPU para o cálculo

    text.append("\nfim:")
    text.append("    b fim")

    return "\n".join(header + data + text)

if __name__ == "__main__":
    import ast # Não faz nenhuma operação matemática, só converte o formato de string para lista mesmo.
    
    save = True # Mudar para True para salvar em arquivo .s ao invés de imprimir no terminal
    tokens = []
    assemblyCode = ""

    with open("./tokens.txt", "r") as file:
        tokenFile = file.read().splitlines()
        # print(tokens)

    for line in tokenFile:
        if line.strip() != "INVALIDO" and line.strip() != "":
            tokenList = ast.literal_eval(line.strip()) # Converte a string para uma lista de tokens

            tokens.extend(tokenList)
            # print(tokenList)

    assemblyCode = generateAssembly(tokens, assemblyCode)

    if save:
        fileName = "output.s"
        with open(fileName, "w") as file:
            file.write(assemblyCode)
    else:
        print(assemblyCode)