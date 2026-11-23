.code

CheckCollisions PROC USES eax ebx ecx edx esi edi

    mov  esi, OFFSET Torpedoes
    mov  ecx, MAX_TORP
TorpLoop:
    cmp  BYTE PTR [esi + 2], 0
    je   NextTorp
    mov  edi, OFFSET Charges
    mov  edx, MAX_CHARGE
ChargeLoop:
    cmp  BYTE PTR [edi + 2], 0
    je   NextCharge
    movzx eax, BYTE PTR [esi + 0]
    movzx ebx, BYTE PTR [edi + 0]
    sub  eax, ebx
    cmp  eax, -TORP_HIT
    jl   NextCharge
    cmp  eax, TORP_HIT
    jg   NextCharge
    mov  al, BYTE PTR [esi + 1]
    mov  bl, BYTE PTR [edi + 1]
    cmp  al, bl
    je   Hit
    inc  al
    cmp  al, bl
    jne  NextCharge
Hit:
    mov  BYTE PTR [esi + 2], 0
    mov  BYTE PTR [edi + 2], 0
    mov  eax, 10
    cmp  BYTE PTR [edi + 3], 0
    je   AwardPoints
    mov  eax, 25
AwardPoints:
    call AddScore
    mov  al, BYTE PTR [edi + 0]
    mov  ah, BYTE PTR [edi + 1]
    call StartExplosion
    call PlayExplosionSound
    jmp  NextTorp
NextCharge:
    add  edi, 4
    dec  edx
    jnz  ChargeLoop
NextTorp:
    add  esi, 4
    loop TorpLoop

    mov  edi, OFFSET Charges
    mov  ecx, MAX_CHARGE
SubLoop:
    cmp  BYTE PTR [edi + 2], 0
    je   NextS
    cmp  BYTE PTR [edi + 1], SUB_ROW
    jne  NextS
    movzx eax, BYTE PTR [edi + 0]
    movzx ebx, subX
    sub  eax, ebx
    cmp  eax, -SUB_HIT
    jl   NextS
    cmp  eax, SUB_HIT
    jg   NextS
    mov  al, BYTE PTR [edi + 0]
    mov  BYTE PTR [edi + 2], 0
    mov  ah, SUB_ROW
    call StartExplosion
    call LoseLife
    jmp  Done
NextS:
    add  edi, 4
    loop SubLoop
Done:
    ret
CheckCollisions ENDP
