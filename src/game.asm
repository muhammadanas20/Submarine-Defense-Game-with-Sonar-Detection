TITLE Depth Charge - Week 0 starter smoke test

INCLUDE Irvine32.inc
INCLUDE shared\constants.inc
INCLUDE shared\data.inc

.data
skeletonMessage BYTE "Depth Charge skeleton builds and runs OK", 0

.code
main PROC
    call Clrscr
    mov  edx, OFFSET skeletonMessage
    call WriteString
    call Crlf
    exit
main ENDP

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
