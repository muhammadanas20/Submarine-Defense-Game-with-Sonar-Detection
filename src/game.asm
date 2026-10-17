TITLE Depth Charge - Submarine Defense with Sonar Detection

;===============================================================
; game.asm - Owner: Muhammad Anas (25K-0899)
; Steps: A2 (main, GameLoop), A3 (FrameDelay), A7 (InitGame)
; Main entry point, game state machine, new-game reset, and
; 80 ms frame timing for Depth Charge.
;===============================================================

INCLUDE Irvine32.inc
INCLUDE shared\constants.inc
INCLUDE shared\data.inc

.code
;---------------------------------------------------------------
; main: program entry point and outer menu loop
;---------------------------------------------------------------
main PROC
    call InitSystem              ; Alyan: seed random, hide cursor
    call LoadHighScore           ; Ali  : read highscore.dat
MenuLoop:
    call ShowMenu                ; Ali  : sets gameState = PLAYING or EXIT
    cmp  gameState, ST_EXIT
    je   Quit
    call InitGame                ; Anas : reset variables and arrays
    call GameLoop                ; Anas : run frames until game ends
    jmp  MenuLoop
Quit:
    call Clrscr
    exit
main ENDP

;---------------------------------------------------------------
; InitGame: resets every variable and object array for a new game
;---------------------------------------------------------------
InitGame PROC USES eax ecx edi
    mov  score, 0
    mov  lives, 3
    mov  level, 1
    mov  subX, 40
    mov  fireCooldown, 0
    mov  sonarReadyAt, 0
    call ApplyLevel              ; Ali: sets fallDelay and spawnDelay
    mov  al, fallDelay
    mov  fallTimer, al
    mov  al, spawnDelay
    mov  spawnTimer, al

    ; clear all three object arrays with REP STOSB (AL = 0)
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

    call Clrscr
    call InvalidateScreen        ; Alyan: force a full redraw
    mov  gameState, ST_PLAYING
    call GetMseconds
    mov  lastFrame, eax
    ret
InitGame ENDP

;---------------------------------------------------------------
; GameLoop: one pass = one frame. Returns on GAME OVER or ESC.
;---------------------------------------------------------------
GameLoop PROC
NextFrame:
    call HandleInput             ; Anas: read keys without waiting
    mov  al, gameState
    cmp  al, ST_PLAYING
    je   DoPlaying
    cmp  al, ST_SONAR
    je   DoSonar
    cmp  al, ST_PAUSED
    je   DoDraw                  ; paused: draw only, no updates
    jmp  GameEnded               ; ST_GAMEOVER or ST_MENU

DoPlaying:
    call UpdateTorpedoes         ; Anas
    call UpdateCharges           ; Ali
    call SpawnCharge             ; Ali
    call UpdateExplosions        ; Alyan
    call CheckCollisions         ; Anas (may set ST_GAMEOVER)
    jmp  DoDraw
DoSonar:
    call UpdateSonar             ; Alyan (may set ST_PLAYING)
DoDraw:
    call BuildFrame              ; Alyan
    call Render                  ; Alyan
    call FrameDelay              ; Anas
    jmp  NextFrame

GameEnded:
    cmp  gameState, ST_GAMEOVER
    jne  BackToMenu
    call GameOverScreen          ; Ali (calls SaveHighScore)
BackToMenu:
    ret
GameLoop ENDP

;---------------------------------------------------------------
; FrameDelay: waits until FRAME_MS (80 ms) have passed since lastFrame
;---------------------------------------------------------------
FrameDelay PROC USES eax
    call GetMseconds
    sub  eax, lastFrame          ; eax = elapsed ms this frame
    cmp  eax, FRAME_MS
    jae  NoWait                  ; frame already took 80 ms or more
    neg  eax
    add  eax, FRAME_MS           ; eax = FRAME_MS - elapsed
    call Delay                   ; Irvine32: sleep EAX ms
NoWait:
    call GetMseconds
    mov  lastFrame, eax
    inc  frameCount
    ret
FrameDelay ENDP

; Temporary no-op implementations keep the shared procedure interface linkable.
; Remove an individual *_STUB line as soon as its real implementation is added.
INCLUDE anas\stubs_anas.inc
INCLUDE alyan\stubs_alyan.inc
INCLUDE ali\stubs_ali.inc

; ---- Anas: main loop support ----
INCLUDE anas\input.inc
INCLUDE anas\torpedo.inc
INCLUDE anas\collision.inc

; ---- Alyan: presentation / sonar ----
INCLUDE alyan\render.inc
INCLUDE alyan\hud.inc
INCLUDE alyan\explosion.inc
INCLUDE alyan\sonar.inc

; ---- Ali: game systems / persistence ----
INCLUDE ali\random.inc
INCLUDE ali\screens.inc
INCLUDE ali\charges.inc
INCLUDE ali\sound.inc
INCLUDE ali\score.inc
INCLUDE ali\highscore.inc

END main
