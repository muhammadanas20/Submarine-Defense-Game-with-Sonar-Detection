;===============================================================
; random.inc - Owner: Ali Raza (25K-0827)
; A small pseudo-random generator. It is not for security use.
;===============================================================

.data
seed DWORD 1

.code
; SeedRandom: use the clock as the starting value.
SeedRandom PROC USES eax
    call GetMseconds
    mov  seed, eax
    ret
SeedRandom ENDP

; Rand: EAX = small positive range (1..65536).
; Returns EAX = 0 .. range-1. This game uses ranges 78 and 5.
Rand PROC USES ebx ecx edx
    cmp  eax, 0
    je   Done                    ; reject a zero divisor
    mov  ebx, eax                ; keep the requested range
    mov  eax, seed
    mov  ecx, 1103515245
    mul  ecx                     ; EDX:EAX = seed * multiplier
    add  eax, 12345              ; keep the low 32 bits
    mov  seed, eax
    shr  eax, 16                 ; use the upper 16 bits
    xor  edx, edx                ; DIV uses EDX:EAX
    div  ebx                     ; remainder is in EDX
    mov  eax, edx
Done:
    ret
Rand ENDP
