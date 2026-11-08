.code
; sonar se hidden mines dikhao
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
    call BuildFrame
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
