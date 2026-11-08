.data

FallDelayTable  BYTE 6, 5, 5, 4, 4, 3, 3, 2, 2
SpawnDelayTable BYTE 14, 12, 11, 10, 9, 8, 7, 6, 5
MAX_LEVEL = LENGTHOF FallDelayTable

.code

AddScore PROC USES eax ecx edx
    add  score, eax
    mov  eax, score
    xor  edx, edx
    mov  ecx, 200
    div  ecx
    inc  eax
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

LoseLife PROC
    call PlayLifeLostSound
    dec  lives
    jnz  StillAlive
    mov  gameState, ST_GAMEOVER
    ret
StillAlive:
    mov  subX, 40
    ret
LoseLife ENDP

ApplyLevel PROC USES eax ebx
    movzx ebx, level
    dec  ebx
    mov  al, FallDelayTable[ebx]
    mov  fallDelay, al
    mov  al, SpawnDelayTable[ebx]
    mov  spawnDelay, al
    ret
ApplyLevel ENDP
