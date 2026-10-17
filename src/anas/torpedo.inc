;===============================================================
; torpedo.inc - Owner: Muhammad Anas (25K-0899), step A5
; Procedures: FireTorpedo, UpdateTorpedoes
; Torpedo slots use the shared GameObject structure and Torpedoes array.
;===============================================================

.code
;---------------------------------------------------------------
; FireTorpedo: puts a torpedo in the first free slot
;---------------------------------------------------------------
FireTorpedo PROC USES eax ecx esi
    cmp  fireCooldown, 0
    ja   Done
    mov  esi, OFFSET Torpedoes
    mov  ecx, MAX_TORP
FindSlot:
    cmp  (GameObject PTR [esi]).active, 0
    je   Found
    add  esi, TYPE GameObject    ; next element (4 bytes)
    loop FindSlot
    jmp  Done                    ; all 8 torpedoes in flight
Found:
    mov  al, subX
    mov  (GameObject PTR [esi]).xPos, al
    mov  (GameObject PTR [esi]).yPos, SUB_ROW - 1
    mov  (GameObject PTR [esi]).active, 1
    mov  fireCooldown, 3         ; 3 frames between shots
    call PlayFireSound           ; Ali
Done:
    ret
FireTorpedo ENDP

;---------------------------------------------------------------
; UpdateTorpedoes: moves every active torpedo up one row
;---------------------------------------------------------------
UpdateTorpedoes PROC USES ecx esi
    cmp  fireCooldown, 0
    je   StartLoop
    dec  fireCooldown
StartLoop:
    mov  esi, OFFSET Torpedoes
    mov  ecx, MAX_TORP
L1:
    cmp  (GameObject PTR [esi]).active, 0
    je   NextT
    dec  (GameObject PTR [esi]).yPos
    cmp  (GameObject PTR [esi]).yPos, TOP_ROW
    jae  NextT
    mov  (GameObject PTR [esi]).active, 0   ; left the playfield
NextT:
    add  esi, TYPE GameObject
    loop L1
    ret
UpdateTorpedoes ENDP
