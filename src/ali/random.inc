.data
seed DWORD 1

.code

SeedRandom PROC USES eax
    call GetMseconds
    mov  seed, eax
    ret
SeedRandom ENDP

Rand PROC USES ebx ecx edx
    cmp  eax, 0
    je   Done
    mov  ebx, eax
    mov  eax, seed
    mov  ecx, 1103515245
    mul  ecx
    add  eax, 12345
    mov  seed, eax
    shr  eax, 16
    xor  edx, edx
    div  ebx
    mov  eax, edx
Done:
    ret
Rand ENDP
