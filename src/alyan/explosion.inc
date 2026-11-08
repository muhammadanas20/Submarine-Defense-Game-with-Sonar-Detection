.data
ExplChars  BYTE '.', '+', '*', '#', '@'
ExplColors BYTE ATTR_TEXT, ATTR_HUD, ATTR_CHARGE, ATTR_CHARGE, ATTR_HUD

.code

StartExplosion PROC USES ebx esi
    mov  esi, OFFSET Explosions
    xor  ebx, ebx
FindSlot:
    cmp  BYTE PTR [esi+ebx*4 + 2], 0
    je   Found
    inc  ebx
    cmp  ebx, MAX_EXPL
    jb   FindSlot
    ret
Found:
    mov  BYTE PTR [esi+ebx*4 + 0], al
    mov  BYTE PTR [esi+ebx*4 + 1], ah
    mov  BYTE PTR [esi+ebx*4 + 2], 1
    mov  ExplTimer[ebx], EXPL_FRAMES
    ret
StartExplosion ENDP

UpdateExplosions PROC USES ecx ebx esi
    mov  esi, OFFSET Explosions
    xor  ebx, ebx
NextExplosion:
    cmp  BYTE PTR [esi+ebx*4 + 2], 0
    je   Skip
    dec  ExplTimer[ebx]
    jnz  Skip
    mov  BYTE PTR [esi+ebx*4 + 2], 0
Skip:
    inc  ebx
    cmp  ebx, MAX_EXPL
    jb   NextExplosion
    ret
UpdateExplosions ENDP

DrawExplosions PROC USES eax ebx ecx edx esi
    mov  esi, OFFSET Explosions
    xor  ebx, ebx
NextExplosion:
    cmp  BYTE PTR [esi+ebx*4 + 2], 0
    je   Skip
    movzx ecx, ExplTimer[ebx]
    dec  ecx
    mov  al, ExplChars[ecx]
    mov  ah, ExplColors[ecx]
    mov  dh, BYTE PTR [esi+ebx*4 + 1]
    mov  dl, BYTE PTR [esi+ebx*4 + 0]
    call PutCell
Skip:
    inc  ebx
    cmp  ebx, MAX_EXPL
    jb   NextExplosion
    ret
DrawExplosions ENDP
