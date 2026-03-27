

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

    header = [
        ".global _start",
        ".equ HEX0, 0xFF200020",
        
    ]

    data = [
        ".section .data"
    ]
    
    text = [
        ".section .text",
        "_start:"
    ]

    header.append("\n    /* PAINEL */")
    header.append(f"    ldr r1, =HEX0")
    header.append(f"    mov r0, #{tablePanel['0']}")
    header.append(f"    str r0, [r1]")
    
    for i, token in enumerate(tokens):
        match token:
            case token if token.replace('.', '', 1).isdigit(): # Remove simbolo de dígito
                data.append(f"   val{i}: .double {token}")
                text.append(f"   ldr r0, =val{i}")
                text.append(f"   vldr d0, [r0]")
                text.append("    vpush {d0}")
            case '(': # Só pra saber onde abre.
                text.append("    /* Início de expressão */")
            case ')': # E onde fecha.
                text.append("    /* Fim de expressão */")
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
                data.append(f"   const_1: .double 1.0") # Constante 1.0 para multiplicação inicial
                text.append("    ldr r0, =const_1")    # Carrega 1.0
                text.append("    vldr d2, [r0]")       # d2 = 1.0 (Resultado inicial)
                text.append(f"loop_pot_{i}:")          # Rótulo único usando o índice do token
                text.append("    cmp r1, #0")          # O contador chegou a zero?
                text.append(f"   ble fim_pot_{i}")     # Se sim, sai do loop
                text.append("    vmul.f64 d2, d2, d0") # Multiplica d2 pela base (d0)
                text.append("    sub r1, r1, #1")      # Diminui 1 do contador
                text.append(f"   b loop_pot_{i}")      # Repete
                text.append(f"fim_pot_{i}:")
                text.append("    vpush {d2}")          # Guarda o resultado
            case 'RES': # Volta 2 ultimos passos
                text.append("    vpop {d1}")
                text.append("    vpop {d0}")
                text.append("    vpush {d0}")
                text.append("    vpush {d1}")
            case 'V_MEM': # Salva na memória
                text.append("    vpop {d0}")
                data.append(f"   mem{i}: .double 0.0")
                text.append(f"    ldr r0, =mem{i}")
                text.append("    vstr d0, [r0]")
                text.append("    vpush {d0}")
            case 'MEM': # Pega da memória
                text.append("    vpop {d0}")
                data.append(f"   mem{i}: .double ")
                text.append(f"    ldr r0, =mem{i}")
                text.append("    vldr d0, [r0]")    
                text.append("    vpush {d0}")
                
    text.append("\nfim:")
    text.append("    b fim")

    return "\n".join(header + data + text)

if __name__ == "__main__":

    save = False
    tokens = []
    assemblyCode = ""

    with open("./tokens.txt", "r") as file:
        tokenFile = file.read().splitlines()
        # print(tokens)

    if tokenFile:
        for token in tokenFile:
            if token.strip() != "INVALIDO":
                tokens.append(token)

    
    for token in tokens:
        # print(token)
        assemblyCode = generateAssembly(tokens, assemblyCode)
    print(assemblyCode)


    if save:
        fileName = "output.s"
        with open(fileName, "w") as file:
            file.write(assemblyCode)