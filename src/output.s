.global _start
.section .data
   const_1: .double 1.0
   const_10: .double 10.0
   history: .space 800
   history_ptr: .word 0
   TABELA_HEX: .byte 0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F
   .balign 8
   val1: .double 15
   val2: .double 5
   val6: .double 29
   val7: .double 1
   val11: .double 29
   val12: .double 10
   val17: .double 20
   val18: .double 10
   val21: .double 20
   val26: .double 2
   val29: .double 1
.section .text
_start:
    /* Início de expressão -- 0 -- */
   ldr r0, =val1
   vldr d0, [r0]
    vpush {d0}
   ldr r0, =val2
   vldr d0, [r0]
    vpush {d0}
    vpop {d1}
    vpop {d0}
    vadd.f64 d2, d0, d1
    vpush {d2}
    /* Fim de expressão -- 0 -- */
    /* Salva no histórico */
    vpop {d0}
    ldr r2, =history_ptr
    ldr r3, [r2]
    ldr r5, =history
    add r5, r5, r3
    vstr d0, [r5]
    add r3, r3, #8
    str r3, [r2]
    vpush {d0}
    vpop {d0}
    vpush {d0}
    vabs.f64 d0, d0
    vcvt.s32.f64 s0, d0
    vmov r2, s0
    vcvt.f64.s32 d1, s0
    vsub.f64 d2, d0, d1
    ldr r0, =const_10
    vldr d3, [r0]
    vmul.f64 d2, d2, d3
    vcvt.s32.f64 s1, d2
    vmov r3, s1
    cmp r3, #9
    movgt r3, #9
    movw R6, #0xCCCD
    movt R6, #0xCCCC
    umull R8, R7, R2, R6
    LSR R7, R7, #3
    mov R6, #10
    mls R8, R7, R6, R2
    cmp r7, #9
    movgt r7, #9
    ldr r4, =TABELA_HEX
    ldrb r5, [r4, r3]
    mov r6, #0x08
    lsl r6, r6, #8
    orr r5, r5, r6
    ldrb r6, [r4, r8]
    lsl r6, r6, #16
    orr r5, r5, r6
    ldrb r6, [r4, r7]
    lsl r6, r6, #24
    orr r5, r5, r6
    ldr r9, =0xFF200020
    str r5, [r9]
    /* Início de expressão -- 0 -- */
   ldr r0, =val6
   vldr d0, [r0]
    vpush {d0}
   ldr r0, =val7
   vldr d0, [r0]
    vpush {d0}
    vpop {d1}
    vpop {d0}
    vadd.f64 d2, d0, d1
    vpush {d2}
    /* Fim de expressão -- 0 -- */
    /* Salva no histórico */
    vpop {d0}
    ldr r2, =history_ptr
    ldr r3, [r2]
    ldr r5, =history
    add r5, r5, r3
    vstr d0, [r5]
    add r3, r3, #8
    str r3, [r2]
    vpush {d0}
    vpop {d0}
    vpush {d0}
    vabs.f64 d0, d0
    vcvt.s32.f64 s0, d0
    vmov r2, s0
    vcvt.f64.s32 d1, s0
    vsub.f64 d2, d0, d1
    ldr r0, =const_10
    vldr d3, [r0]
    vmul.f64 d2, d2, d3
    vcvt.s32.f64 s1, d2
    vmov r3, s1
    cmp r3, #9
    movgt r3, #9
    movw R6, #0xCCCD
    movt R6, #0xCCCC
    umull R8, R7, R2, R6
    LSR R7, R7, #3
    mov R6, #10
    mls R8, R7, R6, R2
    cmp r7, #9
    movgt r7, #9
    ldr r4, =TABELA_HEX
    ldrb r5, [r4, r3]
    mov r6, #0x08
    lsl r6, r6, #8
    orr r5, r5, r6
    ldrb r6, [r4, r8]
    lsl r6, r6, #16
    orr r5, r5, r6
    ldrb r6, [r4, r7]
    lsl r6, r6, #24
    orr r5, r5, r6
    ldr r9, =0xFF200020
    str r5, [r9]
    /* Início de expressão -- 0 -- */
   ldr r0, =val11
   vldr d0, [r0]
    vpush {d0}
   ldr r0, =val12
   vldr d0, [r0]
    vpush {d0}
    vpop {d1}
    vpop {d0}
    vadd.f64 d2, d0, d1
    vpush {d2}
    /* Fim de expressão -- 0 -- */
    /* Salva no histórico */
    vpop {d0}
    ldr r2, =history_ptr
    ldr r3, [r2]
    ldr r5, =history
    add r5, r5, r3
    vstr d0, [r5]
    add r3, r3, #8
    str r3, [r2]
    vpush {d0}
    vpop {d0}
    vpush {d0}
    vabs.f64 d0, d0
    vcvt.s32.f64 s0, d0
    vmov r2, s0
    vcvt.f64.s32 d1, s0
    vsub.f64 d2, d0, d1
    ldr r0, =const_10
    vldr d3, [r0]
    vmul.f64 d2, d2, d3
    vcvt.s32.f64 s1, d2
    vmov r3, s1
    cmp r3, #9
    movgt r3, #9
    movw R6, #0xCCCD
    movt R6, #0xCCCC
    umull R8, R7, R2, R6
    LSR R7, R7, #3
    mov R6, #10
    mls R8, R7, R6, R2
    cmp r7, #9
    movgt r7, #9
    ldr r4, =TABELA_HEX
    ldrb r5, [r4, r3]
    mov r6, #0x08
    lsl r6, r6, #8
    orr r5, r5, r6
    ldrb r6, [r4, r8]
    lsl r6, r6, #16
    orr r5, r5, r6
    ldrb r6, [r4, r7]
    lsl r6, r6, #24
    orr r5, r5, r6
    ldr r9, =0xFF200020
    str r5, [r9]
    /* Início de expressão -- 0 -- */
    /* Início de expressão -- 1 -- */
   ldr r0, =val17
   vldr d0, [r0]
    vpush {d0}
   ldr r0, =val18
   vldr d0, [r0]
    vpush {d0}
    vpop {d1}
    vpop {d0}
    vadd.f64 d2, d0, d1
    vpush {d2}
    /* Fim de expressão -- 1 -- */
   ldr r0, =val21
   vldr d0, [r0]
    vpush {d0}
    vpop {d1}
    vpop {d0}
    vadd.f64 d2, d0, d1
    vpush {d2}
    /* Fim de expressão -- 0 -- */
    /* Salva no histórico */
    vpop {d0}
    ldr r2, =history_ptr
    ldr r3, [r2]
    ldr r5, =history
    add r5, r5, r3
    vstr d0, [r5]
    add r3, r3, #8
    str r3, [r2]
    vpush {d0}
    vpop {d0}
    vpush {d0}
    vabs.f64 d0, d0
    vcvt.s32.f64 s0, d0
    vmov r2, s0
    vcvt.f64.s32 d1, s0
    vsub.f64 d2, d0, d1
    ldr r0, =const_10
    vldr d3, [r0]
    vmul.f64 d2, d2, d3
    vcvt.s32.f64 s1, d2
    vmov r3, s1
    cmp r3, #9
    movgt r3, #9
    movw R6, #0xCCCD
    movt R6, #0xCCCC
    umull R8, R7, R2, R6
    LSR R7, R7, #3
    mov R6, #10
    mls R8, R7, R6, R2
    cmp r7, #9
    movgt r7, #9
    ldr r4, =TABELA_HEX
    ldrb r5, [r4, r3]
    mov r6, #0x08
    lsl r6, r6, #8
    orr r5, r5, r6
    ldrb r6, [r4, r8]
    lsl r6, r6, #16
    orr r5, r5, r6
    ldrb r6, [r4, r7]
    lsl r6, r6, #24
    orr r5, r5, r6
    ldr r9, =0xFF200020
    str r5, [r9]
    /* Início de expressão -- 0 -- */
    /* Início de expressão -- 1 -- */
   ldr r0, =val26
   vldr d0, [r0]
    vpush {d0}
    /* COMANDO RES */
    vpop {d0}
    vcvt.s32.f64 s0, d0
    vmov r1, s0
    ldr r2, =history_ptr
    ldr r3, [r2]
    mov r4, #8
    mul r1, r1, r4
    sub r3, r3, r1
    ldr r5, =history
    add r5, r5, r3
    vldr d1, [r5]
    vpush {d1}
    /* Fim de expressão -- 1 -- */
   ldr r0, =val29
   vldr d0, [r0]
    vpush {d0}
    vpop {d1}
    vpop {d0}
    vsub.f64 d2, d0, d1
    vpush {d2}
    /* Fim de expressão -- 0 -- */
    /* Salva no histórico */
    vpop {d0}
    ldr r2, =history_ptr
    ldr r3, [r2]
    ldr r5, =history
    add r5, r5, r3
    vstr d0, [r5]
    add r3, r3, #8
    str r3, [r2]
    vpush {d0}
    vpop {d0}
    vpush {d0}
    vabs.f64 d0, d0
    vcvt.s32.f64 s0, d0
    vmov r2, s0
    vcvt.f64.s32 d1, s0
    vsub.f64 d2, d0, d1
    ldr r0, =const_10
    vldr d3, [r0]
    vmul.f64 d2, d2, d3
    vcvt.s32.f64 s1, d2
    vmov r3, s1
    cmp r3, #9
    movgt r3, #9
    movw R6, #0xCCCD
    movt R6, #0xCCCC
    umull R8, R7, R2, R6
    LSR R7, R7, #3
    mov R6, #10
    mls R8, R7, R6, R2
    cmp r7, #9
    movgt r7, #9
    ldr r4, =TABELA_HEX
    ldrb r5, [r4, r3]
    mov r6, #0x08
    lsl r6, r6, #8
    orr r5, r5, r6
    ldrb r6, [r4, r8]
    lsl r6, r6, #16
    orr r5, r5, r6
    ldrb r6, [r4, r7]
    lsl r6, r6, #24
    orr r5, r5, r6
    ldr r9, =0xFF200020
    str r5, [r9]

fim:
    b fim