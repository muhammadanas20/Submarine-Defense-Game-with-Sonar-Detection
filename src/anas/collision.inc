;===============================================================
; collision.inc - Owner: Muhammad Anas (25K-0899), step A6
; Procedure: CheckCollisions
; Check torpedo/charge hits (including crossing) and charge/submarine hits.
;===============================================================

.code
;---------------------------------------------------------------
; CheckCollisions: checks torpedo vs charge and charge vs submarine
;---------------------------------------------------------------
CheckCollisions PROC USES eax ebx ecx edx esi edi
    ;----- 1) torpedo vs charge : nested loops -----
    mov  esi, OFFSET Torpedoes
    mov  ecx, MAX_TORP                  ; outer counter (LOOP)
TorpLoop:
    cmp  (GameObject PTR [esi]).active, 0
    je   NextTorp
    mov  edi, OFFSET Charges
    mov  edx, MAX_CHARGE                ; inner counter (DEC/JNZ)
ChargeLoop:
    cmp  (GameObject PTR [edi]).active, 0
    je   NextCharge
    mov  al, (GameObject PTR [esi]).xPos
    cmp  al, (GameObject PTR [edi]).xPos
    jne  NextCharge                     ; different column
    mov  al, (GameObject PTR [esi]).yPos     ; torpedo row
    mov  bl, (GameObject PTR [edi]).yPos     ; charge row
    cmp  al, bl
    je   Hit                            ; same cell
    inc  al
    cmp  al, bl                         ; torpedo one row ABOVE charge
    jne  NextCharge                     ; -> they crossed this frame
Hit:
    mov  (GameObject PTR [esi]).active, 0
    mov  (GameObject PTR [edi]).active, 0
    mov  eax, 10                        ; visible charge = 10 points
    cmp  (GameObject PTR [edi]).hidden, 0
    je   AwardPoints
    mov  eax, 25                        ; hidden mine = 25 points
AwardPoints:
    call AddScore
    mov  al, (GameObject PTR [edi]).xPos
    mov  ah, (GameObject PTR [edi]).yPos
    call StartExplosion                 ; Alyan: AL = col, AH = row
    call PlayExplosionSound             ; Ali
    jmp  NextTorp                       ; this torpedo is gone
NextCharge:
    add  edi, TYPE GameObject
    dec  edx
    jnz  ChargeLoop
NextTorp:
    add  esi, TYPE GameObject
    loop TorpLoop

    ;----- 2) charge vs submarine -----
    mov  edi, OFFSET Charges
    mov  ecx, MAX_CHARGE
SubLoop:
    cmp  (GameObject PTR [edi]).active, 0
    je   NextS
    cmp  (GameObject PTR [edi]).yPos, SUB_ROW
    jne  NextS
    mov  al, (GameObject PTR [edi]).xPos
    cmp  al, subX
    jne  NextS
    mov  (GameObject PTR [edi]).active, 0
    mov  ah, SUB_ROW
    call StartExplosion                 ; AL = subX, AH = SUB_ROW
    call LoseLife
    cmp  gameState, ST_GAMEOVER
    je   Done
NextS:
    add  edi, TYPE GameObject
    loop SubLoop
Done:
    ret
CheckCollisions ENDP
