
def generateAssembly(tokens, assemblyCode):

    depth = 0

    header = [
        ".global _start",
        ".equ HEX0, 0xFF200020", 
        
    ]

    data = [
        ".section .data",
        "   TABELA_HEX: .byte 0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F", # Tabela de mapeamento dos dígitos de 0 a 9 do painel
        "   const_1: .double 1.0", # Constante 1.0 para multiplicação inicial  
        "   const_10: .double 10.0", # Usado no painel de 7 segmentos
        "   history: .space 800", # Espaço para 100 respostas (8 bytes cada)
        "   history_ptr: .word 0" # Ponteiro para o histórico,
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


# Lógica do Painel (Usando _ como separador decimal)
    text.append("    /* --- PAINEL 7 --- */")
    text.append("    vpop {d0}")                # Pega o ultimo resultado calculado
    text.append("    vcvt.s32.f64 s0, d0")      # Converte para int (trunca)
    text.append("    vmov r2, s0")              # R2 = Parte inteira
    text.append("    vcvt.f64.s32 d1, s0")      # Converte de volta pra float
    text.append("    vsub.f64 d2, d0, d1")      # Isola a fracao (Ex: 1.2 - 1.0 = 0.2)
    text.append("    ldr r0, =const_10")        # Carrega 10.0
    text.append("    vldr d3, [r0]")
    text.append("    vmul.f64 d2, d2, d3")      # Multiplica fracao por 10
    text.append("    vcvt.s32.f64 s1, d2")
    text.append("    vmov r3, s1")              # R3 = Parte decimal
    
    text.append("    LDR R4, =TABELA_HEX")
    text.append("    LDRB R5, [R4, r3]")        # Desenho do Decimal (HEX0)
    text.append("    MOV R6, #0x08")            # Desenho do '_' (HEX1)
    text.append("    LDRB R7, [R4, r2]")        # Desenho do Inteiro (HEX2)
    
    text.append("    LSL R6, R6, #8")           # Move o _ para HEX1
    text.append("    ORR R5, R5, R6")           # Junta HEX0 e HEX1
    text.append("    LSL R7, R7, #16")          # Move o Inteiro para HEX2
    text.append("    ORR R5, R5, R7")           # Junta tudo no R5
    
    text.append("    LDR R8, =0xFF200020")      # Endereço base do painel
    text.append("    STR R5, [R8]")             # Acende os displays!

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