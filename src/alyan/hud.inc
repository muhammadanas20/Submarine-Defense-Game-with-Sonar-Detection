.data
strScore  BYTE "SCORE ", 0
strLives  BYTE "LIVES ", 0
strLevel  BYTE "LEVEL ", 0
strSonar  BYTE "SONAR ", 0
strReady  BYTE "READY ", 0
strActive BYTE "ACTIVE", 0
strPaused BYTE "== PAUSED - press P to resume ==", 0
strKeys   BYTE "A/D MOVE  W FIRE  SPACE SONAR  P PAUSE  ESC MENU", 0

.code

PutNumber PROC USES eax ebx ecx edx esi edi
    LOCAL digits[6]:BYTE
    push edx
    lea  edi, digits
    add  edi, 4
    mov  BYTE PTR [edi+1], 0
    mov  esi, 5
    mov  ecx, 10
DigitLoop:
    xor  edx, edx
    div  ecx
    add  dl, '0'
    mov  [edi], dl
    dec  edi
    dec  esi
    jnz  DigitLoop
    pop  edx
    lea  esi, digits
    mov  ah, bl
    call PutString
    ret
PutNumber ENDP

DrawHUD PROC USES eax ebx edx esi
    mov  ah, ATTR_HUD
    mov  bl, ATTR_HUD
    mov  dh, HUD_ROW
    mov  dl, 1
    mov  esi, OFFSET strScore
    call PutString
    mov  dl, 7
    mov  eax, score
    call PutNumber

    mov  ah, ATTR_HUD
    mov  dl, 16
    mov  esi, OFFSET strLives
    call PutString
    mov  dl, 22
    mov  al, lives
    add  al, '0'
    call PutCell

    mov  dl, 27
    mov  esi, OFFSET strLevel
    call PutString
    mov  dl, 33
    mov  al, level
    add  al, '0'
    call PutCell

    mov  dl, 39
    mov  esi, OFFSET strSonar
    call PutString
    mov  dl, 45
    cmp  gameState, ST_SONAR
    je   SonarActive
    call GetMseconds
    cmp  eax, sonarReadyAt
    jae  SonarReady
    mov  ebx, sonarReadyAt
    sub  ebx, eax
    mov  eax, ebx
    add  eax, 999
    xor  edx, edx
    mov  ebx, 1000
    div  ebx
    mov  dh, HUD_ROW
    mov  dl, 45
    mov  bl, ATTR_HUD
    call PutNumber
    jmp  DrawPauseBanner
SonarActive:
    mov  esi, OFFSET strActive
    call PutString
    jmp  DrawPauseBanner
SonarReady:
    mov  ah, ATTR_HUD
    mov  esi, OFFSET strReady
    call PutString
; "PauseMessage" was renamed: keep pause/banner label names clear of MASM
; reserved words (see the note in anas\input.inc).
DrawPauseBanner:
    cmp  gameState, ST_PAUSED
    jne  ShowKeys
    mov  dh, 12
    mov  dl, 24                 ; centres the 32-cell banner in 80 columns
    mov  ah, ATTR_HUD
    mov  esi, OFFSET strPaused
    call PutString
ShowKeys:
    mov  dh, BOTTOM_ROW
    mov  dl, 15
    mov  ah, ATTR_BORDER
    mov  esi, OFFSET strKeys
    call PutString
    ret
DrawHUD ENDP
