;===============================================================
; render.inc - Owner: Syed Alyan Hussain (25K-0648)
; Build a frame in memory, then draw only changed console cells.
;===============================================================

.data
titleStr   BYTE "Depth Charge - Submarine Defense", 0
cursorInfo CONSOLE_CURSOR_INFO <25, 0>   ; size 25, visible = false

.code
InitSystem PROC USES eax
    call SeedRandom
    INVOKE SetConsoleTitle, ADDR titleStr
    INVOKE GetStdHandle, STD_OUTPUT_HANDLE
    INVOKE SetConsoleCursorInfo, eax, ADDR cursorInfo
    ret
InitSystem ENDP

; PutCell: DH = row, DL = column, AL = character, AH = colour.
; ScreenBuf[row * 80 + col] = AX. Each cell is a WORD.
PutCell PROC USES ebx ecx
    cmp  dh, SCREEN_H
    jae  Done                    ; ignore positions outside the screen
    cmp  dl, SCREEN_W
    jae  Done
    movzx ebx, dh
    imul ebx, ebx, SCREEN_W
    movzx ecx, dl
    add  ebx, ecx
    mov  ScreenBuf[ebx*2], ax    ; scale 2 converts cells to bytes
Done:
    ret
PutCell ENDP

; PutString: ESI = zero-terminated string, DH/DL = position,
; AH = colour. The string must fit on its row.
PutString PROC USES eax edx esi
NextChar:
    mov  al, [esi]
    cmp  al, 0
    je   Done
    call PutCell
    inc  dl
    inc  esi
    jmp  NextChar
Done:
    ret
PutString ENDP

ClearBuffer PROC USES eax ecx edi
    mov  eax, ATTR_TEXT
    shl  eax, 8                  ; colour in the high byte
    or   eax, ' '                ; ASCII space in the low byte
    cld
    mov  edi, OFFSET ScreenBuf
    mov  ecx, SCREEN_W * SCREEN_H
    rep  stosw                   ; store AX, ECX times
    ret
ClearBuffer ENDP

InvalidateScreen PROC USES eax ecx edi
    cld
    mov  ax, 0FFFFh              ; cannot equal a normal cell
    mov  edi, OFFSET PrevBuf
    mov  ecx, SCREEN_W * SCREEN_H
    rep  stosw
    ret
InvalidateScreen ENDP

DrawBorders PROC USES eax edx
    mov  al, CH_BORDER
    mov  ah, ATTR_BORDER
    mov  dl, 0
NextColumn:
    mov  dh, 1
    call PutCell
    mov  dh, BOTTOM_ROW
    call PutCell
    inc  dl
    cmp  dl, SCREEN_W - 1
    jb   NextColumn              ; leave the bottom-right cell blank
    ret
DrawBorders ENDP

; BuildFrame: clear, HUD, borders, submarine, shots, charges,
; explosions. Hidden mines are drawn only in ST_SONAR.
BuildFrame PROC USES ecx edx esi
    call ClearBuffer
    call DrawBorders
    mov  eax, (ATTR_SUB SHL 8) OR CH_SUB
    mov  dh, SUB_ROW
    mov  dl, subX
    call PutCell

    mov  esi, OFFSET Torpedoes
    mov  ecx, MAX_TORP
NextTorpedo:
    cmp  (GameObject PTR [esi]).active, 0
    je   SkipTorpedo
    mov  dh, (GameObject PTR [esi]).yPos
    mov  dl, (GameObject PTR [esi]).xPos
    mov  eax, (ATTR_TORP SHL 8) OR CH_TORP
    call PutCell
SkipTorpedo:
    add  esi, TYPE GameObject
    loop NextTorpedo

    mov  esi, OFFSET Charges
    mov  ecx, MAX_CHARGE
NextCharge:
    cmp  (GameObject PTR [esi]).active, 0
    je   SkipCharge
    cmp  (GameObject PTR [esi]).hidden, 0
    je   VisibleCharge
    cmp  gameState, ST_SONAR
    jne  SkipCharge
    mov  eax, (ATTR_MINE SHL 8) OR CH_MINE
    jmp  DrawCharge
VisibleCharge:
    mov  eax, (ATTR_CHARGE SHL 8) OR CH_CHARGE
DrawCharge:
    mov  dh, (GameObject PTR [esi]).yPos
    mov  dl, (GameObject PTR [esi]).xPos
    call PutCell
SkipCharge:
    add  esi, TYPE GameObject
    loop NextCharge
    call DrawExplosions
    call DrawHUD                 ; draw last so PAUSED stays readable
    ret
BuildFrame ENDP

; Render: compare the two buffers and update changed cells only.
Render PROC USES eax ebx ecx edx esi edi
    xor  ebx, ebx                ; cell index
NextCell:
    cmp  ebx, SCREEN_W * SCREEN_H - 1
    jae  CopyFrame               ; never write the last console cell
    mov  ax, ScreenBuf[ebx*2]
    cmp  ax, PrevBuf[ebx*2]
    je   SkipCell
    push eax                     ; save character and colour
    mov  eax, ebx
    xor  edx, edx
    mov  ecx, SCREEN_W
    div  ecx                     ; EAX = row, EDX = column
    mov  dh, al
    call Gotoxy                  ; DL already contains the column
    mov  eax, [esp]
    movzx eax, ah
    call SetTextColor
    pop  eax
    call WriteChar
SkipCell:
    inc  ebx
    jmp  NextCell
CopyFrame:
    cld
    mov  esi, OFFSET ScreenBuf
    mov  edi, OFFSET PrevBuf
    mov  ecx, (SCREEN_W * SCREEN_H) / 2   ; 1000 DWORDs = 2000 WORDs
    rep  movsd
    ret
Render ENDP
