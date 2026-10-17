;===============================================================
; input.inc - Owner: Muhammad Anas (25K-0899), step A4 / A7
; Procedure: HandleInput
; Non-blocking keyboard controls, submarine movement, fire/sonar/pause/menu.
;===============================================================

.code
;---------------------------------------------------------------
; HandleInput: non-blocking. Called once per frame. Processes
; every key waiting in the buffer so held keys never lag.
;---------------------------------------------------------------
HandleInput PROC USES eax edx
NextKey:
    call ReadKey                 ; ZF = 1 -> no key waiting
    jz   Done

    cmp  al, 0                   ; AL = 0 -> special key (arrows)
    je   Extended
    cmp  al, 1Bh                 ; ESC
    je   KeyEsc
    cmp  al, ' '                 ; SPACE
    je   KeySpace
    or   al, 20h                 ; letters -> lower case
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
    cmp  dx, VK_LEFT             ; DX = virtual-key code
    je   KeyLeft
    cmp  dx, VK_RIGHT
    je   KeyRight
    jmp  NextKey

KeyLeft:
    cmp  gameState, ST_PLAYING
    jne  NextKey
    cmp  subX, MIN_COL           ; boundary check (col 1)
    jbe  NextKey
    dec  subX
    jmp  NextKey

KeyRight:
    cmp  gameState, ST_PLAYING
    jne  NextKey
    cmp  subX, MAX_COL           ; boundary check (col 78)
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
    cmp  eax, sonarReadyAt       ; still cooling down?
    jb   NextKey
    call StartSonar              ; Alyan
    jmp  NextKey

KeyPause:
    cmp  gameState, ST_PLAYING
    je   GoPause
    cmp  gameState, ST_PAUSED
    jne  NextKey
    mov  gameState, ST_PLAYING
    jmp  NextKey

GoPause:
    mov  gameState, ST_PAUSED
    jmp  NextKey

KeyEsc:
    mov  gameState, ST_MENU      ; GameLoop returns to the menu
Done:
    ret
HandleInput ENDP
