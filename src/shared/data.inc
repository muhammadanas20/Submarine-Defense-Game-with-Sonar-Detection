.data
gameState      BYTE ST_MENU
subX           BYTE 40
score          DWORD 0
highScore      DWORD 0
lives          BYTE 3
level          BYTE 1
fireCooldown   BYTE 0
lastFrame      DWORD 0
frameCount     DWORD 0
fallDelay      BYTE 6
spawnDelay     BYTE 14
fallTimer      BYTE 6
spawnTimer     BYTE 14
sonarStart     DWORD 0
sonarReadyAt   DWORD 0
sonarPlayed    BYTE 0
stateBeforePause BYTE ST_PLAYING
pauseStarted   DWORD 0

; har slot: x, y, active, hidden
Torpedoes BYTE MAX_TORP * 4 DUP(0)
Charges BYTE MAX_CHARGE * 4 DUP(0)
Explosions BYTE MAX_EXPL * 4 DUP(0)
ExplTimer      BYTE MAX_EXPL DUP(0)

ScreenBuf      WORD SCREEN_W*SCREEN_H DUP(0720h)
PrevBuf        WORD SCREEN_W*SCREEN_H DUP(0FFFFh)
