# RA1-3
Analisador Léxico e Gerador de Assembly para ARMv7

* **Instituição:** Pontifícia Universidade Católica do Paraná (PUCPR)
* **Curso:** Ciência da Computação
* **Disciplina:** Construção de interpretadores
* **Professor:** Frank Alcantara
* **Grupo (Canvas):** RA1-3

# Membros do grupo:
1. **Igor Terplak** - GitHub: [@Wkyouma](https://github.com/Wkyouma)
2. **Kevin Henriques** - GitHub: [@kevinhag](https://github.com/kevinhag)

# Como usar?

Crie um arquivo de texto (ex: entrada.txt) com uma expressão por linha, usando a sintaxe RPN entre parênteses:
```
(15 5 +)
(10 2 *)
(20 4 /)
(9 3 //)
(10 3 %)
(2 8 ^)
(A 5 +)
(1 RES 1 -)
```

No terminal, rode:
```bash
python main.py entrada.txt
```


# exemplo


**Execução:**
```bash
python main.py entrada.txt
```

**Saída:**
```
Histórico de Expressões e Resultados:
[('(15 5 +)', 20.0), ('(20 A)', 20.0), ('(30 1 +)', 31.0), ('(A 20 +)', 40.0)]
Memoria: {'A': 20.0}
```

**tokens.txt gerado:**
```
['15', '5', '+']
['20', 'A']
['30', '1', '+']
['A', '20', '+']
```
