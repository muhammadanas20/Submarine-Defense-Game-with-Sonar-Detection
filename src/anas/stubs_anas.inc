; Temporary Anas procedures for incremental integration.
; Delete a matching ANAS_STUB invocation when the real PROC is implemented.
ANAS_STUB MACRO procName
    procName PROC
        ret
    procName ENDP
ENDM

.code
ANAS_STUB HandleInput
ANAS_STUB FireTorpedo
ANAS_STUB UpdateTorpedoes
ANAS_STUB CheckCollisions

PURGE ANAS_STUB
