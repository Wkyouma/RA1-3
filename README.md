# RA1-3 — Analisador Léxico e Gerador de Assembly ARMv7

* **Instituição:** Pontifícia Universidade Católica do Paraná (PUCPR)
* **Curso:** Ciência da Computação
* **Disciplina:** Construção de Interpretadores
* **Professor:** Frank Alcantara
* **Grupo (Canvas):** RA1-3

## Membros do grupo

| Nome | GitHub |
|------|--------|
| Igor Terplak | [@Wkyouma](https://github.com/Wkyouma) |
| Kevin Henriques | [@kevinhag](https://github.com/kevinhag) |

---

## Descrição

Este projeto implementa um **analisador léxico** para expressões matemáticas em notação polonesa prefixada e um **gerador de código Assembly ARMv7** (64 bits / ponto flutuante com VFP).

O pipeline completo é executado por `main.py` em uma única chamada:

```
Arquivo de entrada (.txt)
        ↓
   Analisador.py      → tokeniza e avalia cada expressão → tokens.txt
        ↓
Transformador64.py    → lê tokens.txt → gera output.s (Assembly ARMv7)
```

---

## Formato das Expressões

As expressões seguem a **notação polonesa prefixada** com parênteses:

```
(operando1 operando2 operador)
```

Exemplos:
```
(15 5 +)               → 15 + 5 = 20
(2 10 ^)               → 2 ^ 10 = 1024
((20 10 +) 20 +)      → (20 + 10) + 20 = 50
(100 3 //)             → divisão inteira = 33
(10 3 %)               → resto = 1
((50.5 49.5 +) TOTAL)  → armazena 100.0 na variável TOTAL
(TOTAL 2 /)            → lê TOTAL e divide por 2
(1 RES)                → recupera o último resultado do histórico
```

### Operadores suportados

| Operador | Operação |
|----------|----------|
| `+` | Adição |
| `-` | Subtração |
| `*` | Multiplicação |
| `/` | Divisão real (64 bits) |
| `//` | Divisão inteira (trunca) |
| `%` | Módulo (resto) |
| `^` | Potenciação (expoente inteiro positivo) |

### Recursos especiais

- **Variáveis:** identificadores formados apenas por letras **maiúsculas** (ex: `TOTAL`, `VEA`).
  - Escrita: o identificador aparece como **último token** antes do `)` (ex: `(valor VAR)`).
  - Leitura: o identificador aparece logo após o `(` (ex: `(VAR 2 +)`).
- **`RES N`:** recupera o N-ésimo resultado anterior do histórico. `(1 RES)` = último resultado, `(2 RES)` = penúltimo.
- **Expressões inválidas:** retornam `INVALIDO` (parênteses desbalanceados, identificadores com letras minúsculas, tokens desconhecidos, etc.) e são ignoradas na geração de Assembly.

---

## Estrutura do Projeto

```
RA1-3/
├── data/
│   ├── teste1.txt        # Operações básicas, variável com letra minúscula (INVALIDO) e token inválido
│   ├── teste2.txt        # Operações variadas: aninhamento, RES, variável TOTAL, módulo
│   └── teste3.txt        # Mix de inteiros e decimais, variável VEA
└── src/
    ├── main.py            # Ponto de entrada: executa todo o pipeline
    ├── Analisador.py      # Analisador léxico (ADF) e executor de expressões
    ├── Transformador64.py # Gerador de Assembly ARMv7 com VFP 64 bits
    ├── tokens.txt         # Saída intermediária: lista de tokens por linha
    └── output.s           # Código Assembly ARMv7 gerado
```

---

## Como Executar

### Pipeline completo (análise + avaliação + geração de Assembly)

Execute a partir da pasta `src/`:

```bash
cd src
python main.py ../data/teste1.txt
```

Ou a partir da raiz do projeto:

```bash
python src/main.py data/teste1.txt
```

O comando realiza as seguintes etapas automaticamente:
1. Lê e tokeniza cada expressão do arquivo de entrada.
2. Avalia cada expressão (mantendo histórico e memória de variáveis).
3. Exporta os tokens para `src/tokens.txt`.
4. Gera o código Assembly ARMv7 e salva em `src/output.s`.
5. Imprime o histórico de resultados e o estado da memória de variáveis.

### Saída esperada no terminal

```
Assembly gerado em output.s
Histórico de Expressões e Resultados:
[('(15 5 +)', 20.0), ('(20 Asa)', 'INVALIDO'), ...]
Memoria: {}
```

### Gerar Assembly manualmente a partir de tokens.txt

O `Transformador64.py` também pode ser executado de forma independente:

```bash
python src/Transformador64.py src/tokens.txt
```

---

## Arquivos de Teste

### `data/teste1.txt`

```
(15 5 +)          → 20.0
(20 Asa)          → INVALIDO  (identificador com letra minúscula)
(29 1 +)          → 30.0
(29 10 +)         → 39.0
((20 10 +) 20 +)  → 50.0
(Asa 20 +)        → INVALIDO
((2 RES) 1 -)     → usa o penúltimo resultado do histórico
(1 2 v)           → INVALIDO  (token 'v' inválido)
```

### `data/teste2.txt`

```
(2 3 + 4 5 * +)           → 25.0
((10 2 /) (5 2 *) *)      → 50.0
(100 2 //)                → 50.0  (divisão inteira)
(2 10 ^)                  → 1024.0
(1 RES)                   → último resultado do histórico
(2 RES)                   → penúltimo resultado do histórico
((50.5 49.5 +) TOTAL)     → grava 100.0 em TOTAL
(TOTAL 2 /)               → 50.0
(15 3 % 10 +)             → 10.0  (15%3=0, 0+10=10)
((2 2 +) (2 2 *) (2 2 ^) + +) → 12.0
```

### `data/teste3.txt`

```
(10 5 +)            → 15.0
(20 2 /)            → 10.0
(3.5 2.1 *)         → 7.35
(10 3 %)            → 1.0
(2 3 ^)             → 8.0
(100 50 -)          → 50.0
(45.5 5.5 + 50 *)   → 2550.0
(10.5 2.1 /)        → ~5.0
(88.8 VEA)          → grava 88.8 em VEA
(VEA 11.2 +)        → 100.0
```

---

## Detalhes Técnicos

### Analisador Léxico (`Analisador.py`)

- Implementado como um **Autômato Determinístico Finito (ADF)** com estados para: números, identificadores e operadores.
- Valida parênteses balanceados.
- Suporta números negativos e decimais (ex: `-3.14`).
- Identificadores devem ser compostos **exclusivamente por letras maiúsculas**; qualquer outro caso retorna `INVALIDO`.
- Retorna `INVALIDO` para expressões malformadas (tokens desconhecidos, parênteses desbalanceados, divisão por zero).
- Avalia as expressões com uma **pilha** e mantém **histórico** e **memória de variáveis** entre expressões.

### Gerador de Assembly (`Transformador64.py`)

- Gera seções `.data` e `.text` para ARMv7.
- Usa **registradores VFP** (`d0`–`d7`, `s0`–`s1`) para aritmética de ponto flutuante de 64 bits.
- Utiliza uma **pilha VFP** (`vpush`/`vpop`) para avaliação das expressões.
- **Potenciação** (`^`): implementada via loop com contador em registrador inteiro (`r1`).
- **Histórico (`RES`)**: salvo em array `.space 800` no `.data` (100 entradas × 8 bytes); acessado com aritmética de ponteiro.
- **Variáveis nomeadas**: alocadas como `.double 0.0` no `.data`; leitura e escrita via `vldr`/`vstr`.
- **Painel de 7 segmentos**: ao final de cada expressão completa, atualiza os displays HEX0–HEX2 do DE1-SoC usando `TABELA_HEX` e o endereço `0xFF200020`.
- Expressões marcadas como `INVALIDO` em `tokens.txt` são **ignoradas** na geração do Assembly.
