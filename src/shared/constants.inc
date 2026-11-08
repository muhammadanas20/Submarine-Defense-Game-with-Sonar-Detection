SCREEN_W    = 80
SCREEN_H    = 25
HUD_ROW     = 0
TOP_ROW     = 2
SUB_ROW     = 23
BOTTOM_ROW  = 24
MIN_COL     = 1
MAX_COL     = 78

MAX_TORP    = 8
MAX_CHARGE  = 15
MAX_EXPL    = 5
EXPL_FRAMES = 5

FRAME_MS          = 80
SONAR_MS          = 2000
SONAR_COOLDOWN_MS = 10000

ST_MENU     = 0
ST_PLAYING  = 1
ST_SONAR    = 2
ST_PAUSED   = 3
ST_GAMEOVER = 4
ST_EXIT     = 5

CH_TORP     = '^'
CH_BORDER   = '='

; ---------------------------------------------------------------------------
; Sprite geometry.  The art strings themselves live in alyan\render.inc and
; are always drawn centred on the object's x, so every sprite must be an odd
; number of cells wide.  *_HALF is how many cells stick out on each side of
; the stored x; input, rendering and collision all use these values, so a new
; design only needs the art string plus the width changed here.
; The numbers are written out (not derived with /) because MASM constant
; division can complain about a non-integer result.
; ---------------------------------------------------------------------------
SUB_W       = 11      ; '<=-[ooo]-=>'  hull, portholes, propeller, bow
SUB_HALF    = 5       ; SUB_W / 2
SAIL_W      = 3       ; '_!_'  conning tower with periscope, one row up
SAIL_HALF   = 1
SUB_HIT     = 5       ; |chargeX - subX| that sinks you. The two tapered tip
                      ; cells on each side are grace, as in the previous build
CHG_W       = 3       ; '(@)'  falling depth charge
CHG_HALF    = 1
MINE_W      = 3       ; '[!]'  hidden mine, only drawn during sonar
                      ; BuildFrame draws both obstacle arts with CHG_HALF, so
                      ; MINE_W has to stay equal to CHG_W
TORP_HIT    = 1       ; |torpX - chargeX| that detonates a charge (= CHG_HALF)

ATTR_TEXT   = lightGray  + (black * 16)
ATTR_SUB    = lightGreen + (black * 16)
ATTR_TORP   = lightCyan  + (black * 16)
ATTR_CHARGE = lightRed   + (black * 16)
ATTR_MINE   = lightGreen + (black * 16)
ATTR_HUD    = yellow     + (black * 16)
ATTR_BORDER = lightBlue  + (black * 16)
