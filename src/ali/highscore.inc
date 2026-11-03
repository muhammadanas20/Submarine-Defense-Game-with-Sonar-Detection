;===============================================================
; highscore.inc - Owner: Ali Raza (25K-0827)
; highscore.dat contains exactly one 4-byte unsigned DWORD.
; The file is in the program's current working directory.
;===============================================================

.data
hsFileName   BYTE "highscore.dat", 0
hsHandle     DWORD ?
newRecord    BYTE 0              ; read by GameOverScreen
saveFailed   BYTE 0              ; read by GameOverScreen

.code
; LoadHighScore: missing, short, or unreadable files mean zero.
LoadHighScore PROC USES eax ecx edx
    mov  highScore, 0
    mov  edx, OFFSET hsFileName
    call OpenInputFile
    cmp  eax, INVALID_HANDLE_VALUE
    je   Done
    mov  hsHandle, eax
    mov  edx, OFFSET highScore
    mov  ecx, SIZEOF highScore
    call ReadFromFile
    jc   BadRead
    cmp  eax, SIZEOF highScore
    je   CloseRead
BadRead:
    mov  highScore, 0
CloseRead:
    mov  eax, hsHandle
    call CloseFile
Done:
    ret
LoadHighScore ENDP

; SaveHighScore: only a new record is written, at game over.
SaveHighScore PROC USES eax ebx ecx edx
    mov  newRecord, 0
    mov  saveFailed, 0
    mov  ebx, score
    cmp  ebx, highScore
    jbe  Done                    ; unsigned comparison

    mov  edx, OFFSET hsFileName
    call CreateOutputFile
    cmp  eax, INVALID_HANDLE_VALUE
    je   Failed
    mov  hsHandle, eax
    mov  edx, OFFSET score
    mov  ecx, SIZEOF score
    call WriteToFile
    cmp  eax, SIZEOF score
    jne  CloseFailed
    mov  eax, hsHandle
    call CloseFile
    mov  highScore, ebx          ; update memory after a good write
    mov  newRecord, 1
    jmp  Done
CloseFailed:
    mov  eax, hsHandle
    call CloseFile
Failed:
    mov  saveFailed, 1           ; keep the previous valid record
Done:
    ret
SaveHighScore ENDP
