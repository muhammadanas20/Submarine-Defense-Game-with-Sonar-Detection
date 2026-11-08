.code

; khali slot mein naya charge rakho
SpawnCharge PROC USES eax ecx esi
    dec  spawnTimer
    jnz  Done
    mov  al, spawnDelay
    mov  spawnTimer, al

    mov  esi, OFFSET Charges
    mov  ecx, MAX_CHARGE
FindSlot:
    cmp  BYTE PTR [esi + 2], 0
    je   Found
    add  esi, 4
    loop FindSlot
    jmp  Done

Found:
    mov  eax, MAX_COL - MIN_COL - 1
    call Rand
    add  al, MIN_COL + 1
    mov  BYTE PTR [esi + 0], al
    mov  BYTE PTR [esi + 1], TOP_ROW
    mov  BYTE PTR [esi + 2], 1
    mov  BYTE PTR [esi + 3], 0

    mov  eax, 5
    call Rand
    cmp  eax, 0
    jne  Done
    mov  BYTE PTR [esi + 3], 1
Done:
    ret
SpawnCharge ENDP

UpdateCharges PROC USES ecx esi
    dec  fallTimer
    jnz  Done
    mov  al, fallDelay
    mov  fallTimer, al

    mov  esi, OFFSET Charges
    mov  ecx, MAX_CHARGE
NextCharge:
    cmp  BYTE PTR [esi + 2], 0
    je   Skip
    inc  BYTE PTR [esi + 1]
    cmp  BYTE PTR [esi + 1], BOTTOM_ROW
    jb   Skip
    mov  BYTE PTR [esi + 2], 0
Skip:
    add  esi, 4
    loop NextCharge
Done:
    ret
UpdateCharges ENDP
