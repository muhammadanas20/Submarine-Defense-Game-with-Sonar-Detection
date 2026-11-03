;===============================================================
; sound.inc - Owner: Ali Raza (25K-0827)
; Beep is synchronous: the program waits for each tone.
; Normal play uses short tones; longer tones accompany a freeze
; or a life-lost/game-over event. No music files are needed.
;===============================================================

; The macro saves the general registers around the Windows call.
mPlaySound MACRO frequency, duration
    pushad
    INVOKE Beep, frequency, duration
    popad
ENDM

.code
PlayFireSound PROC
    mPlaySound 1200, 20
    ret
PlayFireSound ENDP

PlayExplosionSound PROC
    mPlaySound 150, 30
    ret
PlayExplosionSound ENDP

PlayLifeLostSound PROC
    mPlaySound 300, 120
    mPlaySound 200, 180
    ret
PlayLifeLostSound ENDP

PlayGameOverSound PROC USES ebx ecx
    mov  ebx, 600
    mov  ecx, 4
NextNote:
    mPlaySound ebx, 150
    sub  ebx, 100
    loop NextNote
    ret
PlayGameOverSound ENDP

PlaySonarSweep PROC USES ebx ecx
    mov  ebx, 400
    mov  ecx, 5
NextNote:
    mPlaySound ebx, 50
    add  ebx, 100
    loop NextNote                ; 400, 500, 600, 700, 800 Hz
    ret
PlaySonarSweep ENDP
