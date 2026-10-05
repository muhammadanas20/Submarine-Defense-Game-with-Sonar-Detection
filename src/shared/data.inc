;===============================================================
; data.inc - shared game data; comments identify the primary writer
;===============================================================

GameObject STRUCT
    xPos    BYTE 0             ; screen column, 0..79
    yPos    BYTE 0             ; screen row, 0..24
    active  BYTE 0             ; 1 = slot is in use
    hidden  BYTE 0             ; 1 = hidden mine (drawn during sonar only)
GameObject ENDS

.data
gameState     BYTE  ST_MENU         ; Anas
subX          BYTE  40              ; Anas
score         DWORD 0               ; Ali
highScore     DWORD 0               ; Ali
lives         BYTE  3               ; Ali
level         BYTE  1               ; Ali
fireCooldown  BYTE  0               ; Anas
lastFrame     DWORD 0               ; Anas
frameCount    DWORD 0               ; Anas
fallDelay     BYTE  6               ; Ali: set per level
spawnDelay    BYTE  14              ; Ali: set per level
fallTimer     BYTE  6               ; Ali
spawnTimer    BYTE  14              ; Ali
sonarStart    DWORD 0               ; Alyan
sonarReadyAt  DWORD 0               ; Alyan
sonarPlayed   BYTE  0               ; Alyan

Torpedoes     GameObject MAX_TORP   DUP(<>)
Charges       GameObject MAX_CHARGE DUP(<>)
Explosions    GameObject MAX_EXPL   DUP(<>)
ExplTimer     BYTE MAX_EXPL DUP(0)

ScreenBuf     WORD SCREEN_W*SCREEN_H DUP(0720h)  ; Alyan: current frame
PrevBuf       WORD SCREEN_W*SCREEN_H DUP(0FFFFh) ; Alyan: previous frame
