;===============================================================
; explosion.inc - Owner: Syed Alyan Hussain (25K-0648)
; Five fixed slots; each hit shows a five-frame ASCII animation.
;===============================================================

.data
ExplChars  BYTE '.', '+', '*', '#', '@'
ExplColors BYTE ATTR_TEXT, ATTR_HUD, ATTR_CHARGE, ATTR_CHARGE, ATTR_HUD

.code
; StartExplosion: AL = column, AH = row.
StartExplosion PROC USES ebx esi
    mov  esi, OFFSET Explosions
    xor  ebx, ebx
FindSlot:
    cmp  (GameObject PTR [esi+ebx*TYPE GameObject]).active, 0
    je   Found
    inc  ebx
    cmp  ebx, MAX_EXPL
    jb   FindSlot
    ret                          ; no free slot: skip the effect only
Found:
    mov  (GameObject PTR [esi+ebx*TYPE GameObject]).xPos, al
    mov  (GameObject PTR [esi+ebx*TYPE GameObject]).yPos, ah
    mov  (GameObject PTR [esi+ebx*TYPE GameObject]).active, 1
    mov  ExplTimer[ebx], EXPL_FRAMES
    ret
StartExplosion ENDP

UpdateExplosions PROC USES ecx ebx esi
    mov  esi, OFFSET Explosions
    xor  ebx, ebx
NextExplosion:
    cmp  (GameObject PTR [esi+ebx*TYPE GameObject]).active, 0
    je   Skip
    dec  ExplTimer[ebx]
    jnz  Skip
    mov  (GameObject PTR [esi+ebx*TYPE GameObject]).active, 0
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
    cmp  (GameObject PTR [esi+ebx*TYPE GameObject]).active, 0
    je   Skip
    movzx ecx, ExplTimer[ebx]
    dec  ecx                     ; timer 5..1 becomes index 4..0
    mov  al, ExplChars[ecx]
    mov  ah, ExplColors[ecx]
    mov  dh, (GameObject PTR [esi+ebx*TYPE GameObject]).yPos
    mov  dl, (GameObject PTR [esi+ebx*TYPE GameObject]).xPos
    call PutCell
Skip:
    inc  ebx
    cmp  ebx, MAX_EXPL
    jb   NextExplosion
    ret
DrawExplosions ENDP
