;===============================================================
; constants.inc - shared constants (agree as a group before changing)
;===============================================================

; ---- screen layout ----
SCREEN_W    = 80
SCREEN_H    = 25
HUD_ROW     = 0               ; status bar
TOP_ROW     = 2               ; first playfield row
SUB_ROW     = 23              ; submarine row
BOTTOM_ROW  = 24              ; bottom border
MIN_COL     = 1
MAX_COL     = 78

; ---- object limits ----
MAX_TORP    = 8
MAX_CHARGE  = 15
MAX_EXPL    = 5
EXPL_FRAMES = 5

; ---- timing (milliseconds) ----
FRAME_MS          = 80
SONAR_MS          = 2000
SONAR_COOLDOWN_MS = 10000

; ---- game states ----
ST_MENU     = 0
ST_PLAYING  = 1
ST_SONAR    = 2
ST_PAUSED   = 3
ST_GAMEOVER = 4
ST_EXIT     = 5

; ---- screen characters ----
CH_SUB      = 'U'
CH_TORP     = '^'
CH_CHARGE   = '*'
CH_MINE     = '!'
CH_BORDER   = '='

; ---- Irvine32 console colours: foreground + background * 16 ----
; Irvine32.inc supplies the lightGray, black, lightGreen, etc. constants.
ATTR_TEXT   = lightGray  + (black * 16)
ATTR_SUB    = lightGreen + (black * 16)
ATTR_TORP   = lightCyan  + (black * 16)
ATTR_CHARGE = lightRed   + (black * 16)
ATTR_MINE   = lightGreen + (black * 16)
ATTR_HUD    = yellow     + (black * 16)
ATTR_BORDER = lightBlue  + (black * 16)
