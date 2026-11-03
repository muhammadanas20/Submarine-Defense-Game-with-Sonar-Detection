;===============================================================
; charges.inc - Owner: Ali Raza (25K-0827)
; Spawn and move visible charges and hidden mines.
;===============================================================

.code
; SpawnCharge: called only while playing, once per frame.
SpawnCharge PROC USES eax ecx esi
    dec  spawnTimer
    jnz  Done
    mov  al, spawnDelay
    mov  spawnTimer, al

    mov  esi, OFFSET Charges
    mov  ecx, MAX_CHARGE
FindSlot:
    cmp  (GameObject PTR [esi]).active, 0
    je   Found
    add  esi, TYPE GameObject
    loop FindSlot
    jmp  Done                    ; all 15 slots are occupied

Found:
    mov  eax, MAX_COL - MIN_COL + 1
    call Rand                    ; 0 .. 77
    add  al, MIN_COL             ; 1 .. 78
    mov  (GameObject PTR [esi]).xPos, al
    mov  (GameObject PTR [esi]).yPos, TOP_ROW
    mov  (GameObject PTR [esi]).active, 1
    mov  (GameObject PTR [esi]).hidden, 0

    mov  eax, 5
    call Rand                    ; 0 .. 4
    cmp  eax, 0
    jne  Done                    ; one chance in five is hidden
    mov  (GameObject PTR [esi]).hidden, 1
Done:
    ret
SpawnCharge ENDP

; UpdateCharges: all active charges fall together every N frames.
UpdateCharges PROC USES ecx esi
    dec  fallTimer
    jnz  Done
    mov  al, fallDelay
    mov  fallTimer, al

    mov  esi, OFFSET Charges
    mov  ecx, MAX_CHARGE
NextCharge:
    cmp  (GameObject PTR [esi]).active, 0
    je   Skip
    inc  (GameObject PTR [esi]).yPos
    cmp  (GameObject PTR [esi]).yPos, BOTTOM_ROW
    jb   Skip
    mov  (GameObject PTR [esi]).active, 0   ; reached the sea bed
Skip:
    add  esi, TYPE GameObject
    loop NextCharge
Done:
    ret
UpdateCharges ENDP
