; Temporary Alyan procedures for incremental integration.
; Delete a matching ALYAN_STUB invocation when the real PROC is implemented.
ALYAN_STUB MACRO procName
    procName PROC
        ret
    procName ENDP
ENDM

.code
ALYAN_STUB InitSystem
ALYAN_STUB InvalidateScreen
ALYAN_STUB BuildFrame
ALYAN_STUB Render
ALYAN_STUB UpdateExplosions
ALYAN_STUB StartExplosion
ALYAN_STUB StartSonar
ALYAN_STUB UpdateSonar
ALYAN_STUB DrawHUD
ALYAN_STUB DrawExplosions

PURGE ALYAN_STUB
