;===============================================================
; input.inc - Owner: Muhammad Anas (25K-0899)
; ReadKey polls without waiting. ZF=1 means no key is available.
;===============================================================

.code
HandleInput PROC USES eax edx
NextKey:
    call ReadKey
    jz   Done
    cmp  al, 0                   ; Irvine32 special-key marker
    je   Extended
    cmp  al, 1Bh                 ; ESC works in play, sonar and pause
    je   KeyEsc
    cmp  al, ' '
    je   KeySpace
    or   al, 20h                 ; accept capital or small letters
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
    cmp  subX, MIN_COL
    jbe  NextKey
    dec  subX
    jmp  NextKey
KeyRight:
    cmp  gameState, ST_PLAYING
    jne  NextKey
    cmp  subX, MAX_COL
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
    jb   NextKey                 ; still recharging
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
    mov  stateBeforePause, al    ; remember PLAYING or SONAR
    call GetMseconds
    mov  pauseStarted, eax
    mov  gameState, ST_PAUSED
    jmp  NextKey
Resume:
    cmp  stateBeforePause, ST_SONAR
    jne  RestoreState
    call GetMseconds
    sub  eax, pauseStarted
    add  sonarStart, eax         ; paused time does not use up sonar
RestoreState:
    mov  al, stateBeforePause
    mov  gameState, al
    jmp  NextKey
KeyEsc:
    mov  gameState, ST_MENU
Done:
    ret
HandleInput ENDP
