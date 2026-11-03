TITLE Depth Charge - Submarine Defense with Sonar Detection

;===============================================================
; game.asm - Owner: Muhammad Anas (25K-0899)
; One ASM file includes the three members' small INCLUDE modules.
; Windows x86 / MASM / Irvine32. No DOS or BIOS interrupts.
;===============================================================

INCLUDE Irvine32.inc
INCLUDE shared\constants.inc
INCLUDE shared\data.inc

; Windows sound API; frequency is in Hz and duration in ms.
Beep PROTO, dwFreq:DWORD, dwDuration:DWORD

.code
main PROC
    call InitSystem              ; Alyan: seed random and hide cursor
    call LoadHighScore           ; Ali: read the previous best score
MenuLoop:
    call ShowMenu                ; Ali: choose start or exit
    cmp  gameState, ST_EXIT
    je   Quit
    call InitGame
    call GameLoop
    jmp  MenuLoop
Quit:
    call Clrscr
    exit
main ENDP

; InitGame: reset a round, but keep the saved high score.
InitGame PROC USES eax ecx edi
    mov  score, 0
    mov  lives, 3
    mov  level, 1
    mov  subX, 40
    mov  fireCooldown, 0
    mov  frameCount, 0
    mov  sonarStart, 0
    mov  sonarReadyAt, 0
    mov  sonarPlayed, 0
    mov  stateBeforePause, ST_PLAYING
    mov  pauseStarted, 0
    call ApplyLevel
    mov  al, fallDelay
    mov  fallTimer, al
    mov  al, spawnDelay
    mov  spawnTimer, al

    ; Clear all object arrays and their separate explosion timers.
    cld
    mov  al, 0
    mov  edi, OFFSET Torpedoes
    mov  ecx, SIZEOF Torpedoes
    rep  stosb
    mov  edi, OFFSET Charges
    mov  ecx, SIZEOF Charges
    rep  stosb
    mov  edi, OFFSET Explosions
    mov  ecx, SIZEOF Explosions
    rep  stosb
    mov  edi, OFFSET ExplTimer
    mov  ecx, SIZEOF ExplTimer
    rep  stosb

    call ReadKeyFlush            ; do not carry menu keys into play
    call Clrscr
    call InvalidateScreen
    mov  gameState, ST_PLAYING
    call GetMseconds
    mov  lastFrame, eax
    ret
InitGame ENDP

; GameLoop: input -> update -> collisions -> draw -> wait.
; Sonar and pause skip object updates, not input or drawing.
GameLoop PROC
NextFrame:
    call HandleInput
    mov  al, gameState
    cmp  al, ST_PLAYING
    je   DoPlaying
    cmp  al, ST_SONAR
    je   DoSonar
    cmp  al, ST_PAUSED
    je   DoDraw
    jmp  GameEnded

DoPlaying:
    call UpdateTorpedoes
    call UpdateCharges
    call SpawnCharge
    call UpdateExplosions
    call CheckCollisions
    cmp  gameState, ST_GAMEOVER
    je   GameEnded
    jmp  DoDraw
DoSonar:
    call UpdateSonar
DoDraw:
    call BuildFrame
    call Render
    call FrameDelay
    jmp  NextFrame
GameEnded:
    cmp  gameState, ST_GAMEOVER
    jne  BackToMenu
    call GameOverScreen          ; saves a record and waits for a key
BackToMenu:
    ret
GameLoop ENDP

; FrameDelay: target 80 ms per frame, about 12.5 frames/second.
; A long blocking sound may make one frame longer; we do not try
; to catch up by moving objects several times on the next frame.
FrameDelay PROC USES eax
    call GetMseconds
    sub  eax, lastFrame
    cmp  eax, FRAME_MS
    jae  NoWait
    neg  eax
    add  eax, FRAME_MS           ; remaining = 80 - elapsed
    call Delay
NoWait:
    call GetMseconds
    mov  lastFrame, eax
    inc  frameCount
    ret
FrameDelay ENDP

; ---- Anas: input and game rules ----
INCLUDE anas\input.inc
INCLUDE anas\torpedo.inc
INCLUDE anas\collision.inc

; ---- Alyan: drawing and sonar ----
INCLUDE alyan\render.inc
INCLUDE alyan\hud.inc
INCLUDE alyan\explosion.inc
INCLUDE alyan\sonar.inc

; ---- Ali: enemies, screens, score, sound and file ----
INCLUDE ali\random.inc
INCLUDE ali\screens.inc
INCLUDE ali\charges.inc
INCLUDE ali\sound.inc
INCLUDE ali\score.inc
INCLUDE ali\highscore.inc

END main
