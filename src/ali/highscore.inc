.data
hsFileName   BYTE "highscore.dat", 0
hsHandle     DWORD ?
newRecord    BYTE 0
saveFailed   BYTE 0

.code

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

SaveHighScore PROC USES eax ebx ecx edx
    mov  newRecord, 0
    mov  saveFailed, 0
    mov  ebx, score
    cmp  ebx, highScore
    jbe  Done

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
    mov  highScore, ebx
    mov  newRecord, 1
    jmp  Done
CloseFailed:
    mov  eax, hsHandle
    call CloseFile
Failed:
    mov  saveFailed, 1
Done:
    ret
SaveHighScore ENDP
