; Temporary Ali procedures for incremental integration.
; Delete a matching ALI_STUB invocation when the real PROC is implemented.
ALI_STUB MACRO procName
    procName PROC
        ret
    procName ENDP
ENDM

.code
ALI_STUB SeedRandom
ALI_STUB ShowMenu
ALI_STUB GameOverScreen
ALI_STUB LoadHighScore
ALI_STUB SpawnCharge
ALI_STUB UpdateCharges
ALI_STUB AddScore
ALI_STUB LoseLife
ALI_STUB ApplyLevel
ALI_STUB PlayFireSound
ALI_STUB PlayExplosionSound
ALI_STUB PlaySonarSweep
ALI_STUB PlayLifeLostSound
ALI_STUB PlayGameOverSound
ALI_STUB SaveHighScore

PURGE ALI_STUB
