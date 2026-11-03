;===============================================================
; score.inc - Owner: Ali Raza (25K-0827)
; Points, lives, and nine difficulty levels.
;===============================================================

.data
; Index = level - 1. Smaller delays mean faster charges.
FallDelayTable  BYTE 6, 5, 5, 4, 4, 3, 3, 2, 2
SpawnDelayTable BYTE 14, 12, 11, 10, 9, 8, 7, 6, 5
MAX_LEVEL = LENGTHOF FallDelayTable

.code
; AddScore: EAX = points to add (10 or 25).
AddScore PROC USES eax ecx edx
    add  score, eax
    mov  eax, score
    xor  edx, edx
    mov  ecx, 200
    div  ecx                     ; EAX = score / 200
    inc  eax                     ; level starts at 1
    cmp  eax, MAX_LEVEL
    jbe  CheckLevel
    mov  eax, MAX_LEVEL
CheckLevel:
    cmp  al, level
    je   Done
    mov  level, al
    call ApplyLevel
Done:
    ret
AddScore ENDP

; LoseLife: called for a charge that hits the submarine.
LoseLife PROC
    call PlayLifeLostSound
    dec  lives
    jnz  StillAlive
    mov  gameState, ST_GAMEOVER
    ret
StillAlive:
    mov  subX, 40                ; recover in the middle
    ret
LoseLife ENDP

; ApplyLevel: copy this level's two delays from the tables.
ApplyLevel PROC USES eax ebx
    movzx ebx, level
    dec  ebx                     ; level 1 uses table index 0
    mov  al, FallDelayTable[ebx]
    mov  fallDelay, al
    mov  al, SpawnDelayTable[ebx]
    mov  spawnDelay, al
    ret
ApplyLevel ENDP
