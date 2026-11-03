;===============================================================
; sonar.inc - Owner: Syed Alyan Hussain (25K-0648)
; Sonar freezes object updates for two seconds. The ten-second
; recharge starts when sonar ends. Input can still pause or exit.
;===============================================================

.code
StartSonar PROC USES eax
    mov  gameState, ST_SONAR
    call GetMseconds
    mov  sonarStart, eax
    mov  sonarPlayed, 0
    ret
StartSonar ENDP

UpdateSonar PROC USES eax
    cmp  sonarPlayed, 0
    jne  CheckTime
    call BuildFrame              ; show mines before the blocking sweep
    call Render
    call PlaySonarSweep
    mov  sonarPlayed, 1
CheckTime:
    call GetMseconds
    sub  eax, sonarStart
    cmp  eax, SONAR_MS
    jb   Done
    mov  gameState, ST_PLAYING
    call GetMseconds
    add  eax, SONAR_COOLDOWN_MS
    mov  sonarReadyAt, eax
Done:
    ret
UpdateSonar ENDP
