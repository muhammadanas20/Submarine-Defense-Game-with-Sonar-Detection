TITLE Depth Charge - Submarine Defense with Sonar Detection

INCLUDE Irvine32.inc
INCLUDE shared\constants.inc
INCLUDE shared\data.inc

Beep PROTO, dwFreq:DWORD, dwDuration:DWORD

.code
main PROC
    call InitSystem
    call LoadHighScore
MenuLoop:
    call ShowMenu
    cmp  gameState, ST_EXIT
    je   Quit
    call InitGame
    call GameLoop
    jmp  MenuLoop
Quit:
    call Clrscr
    exit
main ENDP

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

    call ReadKeyFlush
    call Clrscr
    call InvalidateScreen
    mov  gameState, ST_PLAYING
    call GetMseconds
    mov  lastFrame, eax
    ret
InitGame ENDP

; har frame mein input, update aur draw
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
    call GameOverScreen
BackToMenu:
    ret
GameLoop ENDP

FrameDelay PROC USES eax
    call GetMseconds
    sub  eax, lastFrame
    cmp  eax, FRAME_MS
    jae  NoWait
    neg  eax
    add  eax, FRAME_MS
    call Delay
NoWait:
    call GetMseconds
    mov  lastFrame, eax
    inc  frameCount
    ret
FrameDelay ENDP

INCLUDE anas\input.inc
INCLUDE anas\torpedo.inc
INCLUDE anas\collision.inc

INCLUDE alyan\render.inc
INCLUDE alyan\hud.inc
INCLUDE alyan\explosion.inc
INCLUDE alyan\sonar.inc

INCLUDE ali\random.inc
INCLUDE ali\screens.inc
INCLUDE ali\charges.inc
INCLUDE ali\sound.inc
INCLUDE ali\score.inc
INCLUDE ali\highscore.inc

END main
