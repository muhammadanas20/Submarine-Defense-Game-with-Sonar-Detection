.code

; khali slot dhoondo aur shot banao
FireTorpedo PROC USES eax ecx esi
    cmp  fireCooldown, 0
    ja   Done
    mov  esi, OFFSET Torpedoes
    mov  ecx, MAX_TORP
FindSlot:
    cmp  BYTE PTR [esi + 2], 0
    je   Found
    add  esi, 4
    loop FindSlot
    jmp  Done
Found:
    mov  al, subX
    mov  BYTE PTR [esi + 0], al
    mov  BYTE PTR [esi + 1], SUB_ROW - 2   ; above the sail, so the shot never
                                           ; hides the periscope for a frame
    mov  BYTE PTR [esi + 2], 1
    mov  fireCooldown, 3
    call PlayFireSound
Done:
    ret
FireTorpedo ENDP

UpdateTorpedoes PROC USES ecx esi
    cmp  fireCooldown, 0
    je   StartLoop
    dec  fireCooldown
StartLoop:
    mov  esi, OFFSET Torpedoes
    mov  ecx, MAX_TORP
L1:
    cmp  BYTE PTR [esi + 2], 0
    je   NextT
    dec  BYTE PTR [esi + 1]
    cmp  BYTE PTR [esi + 1], TOP_ROW
    jae  NextT
    mov  BYTE PTR [esi + 2], 0
NextT:
    add  esi, 4
    loop L1
    ret
UpdateTorpedoes ENDP
