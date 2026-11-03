;===============================================================
; screens.inc - Owner: Ali Raza (25K-0827)
; Menus use direct console output. Moving gameplay uses buffers.
;===============================================================

.data
strTitle   BYTE "DEPTH CHARGE - SUBMARINE DEFENSE", 0
strOpt1    BYTE "1. Start game", 0
strOpt2    BYTE "2. Instructions", 0
strOpt3    BYTE "3. Exit", 0
strHigh    BYTE "High score: ", 0
strChoose  BYTE "Choose 1, 2 or 3 (ESC also exits)", 0
strHelpTitle BYTE "HOW TO PLAY", 0
strHelp1   BYTE "A / D or Left / Right : move the submarine", 0
strHelp2   BYTE "W : fire a torpedo       P : pause / resume", 0
strHelp3   BYTE "SPACE : sonar for 2 seconds; 10-second recharge", 0
strHelp4   BYTE "ESC : return to the menu without saving this round", 0
strHelp5   BYTE "* = charge: +10 points. Hidden mine: +25 points.", 0
strHelp6   BYTE "Sonar reveals hidden mines as green ! marks.", 0
strHelp7   BYTE "You have 3 lives. Every 200 points adds a level.", 0
strHelp8   BYTE "Charges fall faster as you reach higher levels.", 0
strAnyKey  BYTE "Press any key to return to the menu", 0
strOver    BYTE "GAME OVER", 0
strFinal   BYTE "Final score: ", 0
strNewHigh BYTE "NEW HIGH SCORE!", 0
strSaveErr BYTE "Could not save. Check folder write permission.", 0

.code
; PrintAt: EAX = colour, DH/DL = row/column, ESI = string.
PrintAt PROC USES eax edx
    call SetTextColor
    call Gotoxy
    mov  edx, esi
    call WriteString
    ret
PrintAt ENDP

WaitAnyKey PROC USES eax
WaitLoop:
    mov  eax, 30
    call Delay                   ; do not busy-wait at full CPU
    call ReadKey
    jz   WaitLoop
    ret
WaitAnyKey ENDP

ShowMenu PROC USES eax edx esi
    call ReadKeyFlush
Redraw:
    mov  gameState, ST_MENU
    mov  eax, ATTR_TEXT
    call SetTextColor
    call Clrscr
    mov  eax, ATTR_HUD
    mov  dh, 5
    mov  dl, 24
    mov  esi, OFFSET strTitle
    call PrintAt

    mov  eax, ATTR_TEXT
    mov  dh, 9
    mov  dl, 32
    mov  esi, OFFSET strOpt1
    call PrintAt
    inc  dh
    mov  esi, OFFSET strOpt2
    call PrintAt
    inc  dh
    mov  esi, OFFSET strOpt3
    call PrintAt

    mov  dh, 14
    mov  esi, OFFSET strHigh
    call PrintAt
    mov  eax, highScore
    call WriteDec
    mov  eax, ATTR_TEXT
    mov  dh, 17
    mov  dl, 23
    mov  esi, OFFSET strChoose
    call PrintAt
WaitChoice:
    mov  eax, 30
    call Delay
    call ReadKey
    jz   WaitChoice
    cmp  al, '1'
    je   StartGame
    cmp  al, '2'
    je   Instructions
    cmp  al, '3'
    je   Quit
    cmp  al, 1Bh
    je   Quit
    jmp  WaitChoice
StartGame:
    mov  gameState, ST_PLAYING
    ret
Instructions:
    call ShowInstructions
    jmp  Redraw
Quit:
    mov  gameState, ST_EXIT
    ret
ShowMenu ENDP

ShowInstructions PROC USES eax edx esi
    call Clrscr
    mov  eax, ATTR_HUD
    mov  dh, 3
    mov  dl, 34
    mov  esi, OFFSET strHelpTitle
    call PrintAt
    mov  eax, ATTR_TEXT
    mov  dh, 6
    mov  dl, 5
    mov  esi, OFFSET strHelp1
    call PrintAt
    add  dh, 2
    mov  esi, OFFSET strHelp2
    call PrintAt
    add  dh, 2
    mov  esi, OFFSET strHelp3
    call PrintAt
    add  dh, 2
    mov  esi, OFFSET strHelp4
    call PrintAt
    add  dh, 2
    mov  esi, OFFSET strHelp5
    call PrintAt
    inc  dh
    mov  esi, OFFSET strHelp6
    call PrintAt
    add  dh, 2
    mov  esi, OFFSET strHelp7
    call PrintAt
    inc  dh
    mov  esi, OFFSET strHelp8
    call PrintAt
    mov  dh, 22
    mov  esi, OFFSET strAnyKey
    call PrintAt
    call ReadKeyFlush            ; do not reuse the menu's '2'
    call WaitAnyKey
    ret
ShowInstructions ENDP

GameOverScreen PROC USES eax edx esi
    call SaveHighScore           ; save before changing highScore
    call PlayGameOverSound
    call Clrscr
    mov  eax, ATTR_CHARGE
    mov  dh, 7
    mov  dl, 35
    mov  esi, OFFSET strOver
    call PrintAt

    mov  eax, ATTR_TEXT
    mov  dh, 10
    mov  dl, 28
    mov  esi, OFFSET strFinal
    call PrintAt
    mov  eax, score
    call WriteDec
    mov  eax, ATTR_TEXT
    mov  dh, 12
    mov  dl, 28
    mov  esi, OFFSET strHigh
    call PrintAt
    mov  eax, highScore
    call WriteDec

    cmp  newRecord, 0
    je   CheckError
    mov  eax, ATTR_HUD
    mov  dh, 14
    mov  dl, 32
    mov  esi, OFFSET strNewHigh
    call PrintAt
CheckError:
    cmp  saveFailed, 0
    je   WaitForPlayer
    mov  eax, ATTR_CHARGE
    mov  dh, 16
    mov  dl, 16
    mov  esi, OFFSET strSaveErr
    call PrintAt
WaitForPlayer:
    mov  eax, ATTR_TEXT
    mov  dh, 20
    mov  dl, 22
    mov  esi, OFFSET strAnyKey
    call PrintAt
    mov  eax, 700
    call Delay
    call ReadKeyFlush            ; discard keys held during play
    call WaitAnyKey
    mov  gameState, ST_MENU
    ret
GameOverScreen ENDP
