.code
HandleInput PROC USES eax edx
NextKey:
    call ReadKey
    jz   Done
    cmp  al, 0
    je   Extended
    cmp  al, 1Bh
    je   KeyEsc
    cmp  al, ' '
    je   KeySpace
    or   al, 20h
    cmp  al, 'a'
    je   KeyLeft
    cmp  al, 'd'
    je   KeyRight
    cmp  al, 'w'
    je   KeyFire
    cmp  al, 'p'
    je   KeyPause
    jmp  NextKey
Extended:
    cmp  dx, VK_LEFT
    je   KeyLeft
    cmp  dx, VK_RIGHT
    je   KeyRight
    jmp  NextKey

KeyLeft:
    cmp  gameState, ST_PLAYING
    jne  NextKey
    cmp  subX, MIN_COL + 4
    jbe  NextKey
    dec  subX
    jmp  NextKey
KeyRight:
    cmp  gameState, ST_PLAYING
    jne  NextKey
    cmp  subX, MAX_COL - 4
    jae  NextKey
    inc  subX
    jmp  NextKey
KeyFire:
    cmp  gameState, ST_PLAYING
    jne  NextKey
    call FireTorpedo
    jmp  NextKey
KeySpace:
    cmp  gameState, ST_PLAYING
    jne  NextKey
    call GetMseconds
    cmp  eax, sonarReadyAt
    jb   NextKey
    call StartSonar
    jmp  NextKey

KeyPause:
    cmp  gameState, ST_PAUSED
    je   Resume
    cmp  gameState, ST_PLAYING
    je   Pause
    cmp  gameState, ST_SONAR
    jne  NextKey
Pause:
    mov  al, gameState
    mov  stateBeforePause, al
    call GetMseconds
    mov  pauseStarted, eax
    mov  gameState, ST_PAUSED
    jmp  NextKey
Resume:
    cmp  stateBeforePause, ST_SONAR
    jne  RestoreState
    call GetMseconds
    sub  eax, pauseStarted
    add  sonarStart, eax
RestoreState:
    mov  al, stateBeforePause
    mov  gameState, al
    jmp  NextKey
KeyEsc:
    mov  gameState, ST_MENU
Done:
    ret
HandleInput ENDP
