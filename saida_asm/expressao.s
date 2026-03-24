.section .data

.section .text
.global _start
_start:
    
    @ linha 1: (15 5 +)
    MOV r1, #5
    @ resultado -> r4
    
    @ linha 2: (20 Asa)
    @ resultado -> r5
    
    @ linha 3: (29 1 +)
    MOV r1, #1
    @ resultado -> r6
    
    @ linha 4: (29 10 +)
    MOV r1, #10
    @ resultado -> r7
    
    @ linha 5: ((20 10 +) 20 +)
    MOV r1, #10
    @ resultado -> r8
    
    @ linha 6: (Asa 20 +)
    MOV r1, #20
    @ resultado -> r10
    
    @ linha 7: ((2 RES) 1 -)
    @ resultado -> r11
    
    @ linha 8: (1 2 v)
    MOV r1, #2
    @ resultado -> r12

loop: B loop