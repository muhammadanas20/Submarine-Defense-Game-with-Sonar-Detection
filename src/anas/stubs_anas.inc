; Temporary Anas procedures for incremental integration.
; All four Anas procedures (HandleInput, FireTorpedo, UpdateTorpedoes,
; CheckCollisions) are now implemented in input.inc, torpedo.inc, and
; collision.inc, so their ANAS_STUB lines have been removed.
ANAS_STUB MACRO procName
    procName PROC
        ret
    procName ENDP
ENDM

.code

PURGE ANAS_STUB
