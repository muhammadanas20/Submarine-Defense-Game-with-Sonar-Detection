.data
; --- ASCII art -------------------------------------------------------------
; A text console has one character per cell, so every design is one line that
; is drawn centred on the object's x.  The widths must match the SUB_W /
; SAIL_W / CHG_W / MINE_W values in shared\constants.inc, or the centring and
; the hit boxes drift apart.
;
; Submarine    <=-[ooo]-=>   steel hull, three portholes, propeller (left),
;                            bow taper (right)
;              _!_           conning tower with periscope, one row above
; Depth charge (@)           red drum falling from the surface
; Hidden mine  [!]           drawn only while sonar is active
subArt      BYTE "<=-[ooo]-=>", 0
subSail     BYTE "_!_", 0
chargeArt   BYTE "(@)", 0
mineArt     BYTE "[!]", 0
titleStr   BYTE "Depth Charge - Submarine Defense", 0
cursorInfo CONSOLE_CURSOR_INFO <25, 0>

.code
InitSystem PROC USES eax
    call SeedRandom
    INVOKE SetConsoleTitle, ADDR titleStr
    INVOKE GetStdHandle, STD_OUTPUT_HANDLE
    INVOKE SetConsoleCursorInfo, eax, ADDR cursorInfo
    ret
InitSystem ENDP

; ek cell buffer mein rakho
PutCell PROC USES ebx ecx
    cmp  dh, SCREEN_H
    jae  Done
    cmp  dl, SCREEN_W
    jae  Done
    movzx ebx, dh
    imul ebx, ebx, SCREEN_W
    movzx ecx, dl
    add  ebx, ecx
    mov  ScreenBuf[ebx*2], ax
Done:
    ret
PutCell ENDP

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
    shl  eax, 8
    or   eax, ' '
    cld
    mov  edi, OFFSET ScreenBuf
    mov  ecx, SCREEN_W * SCREEN_H
    rep  stosw
    ret
ClearBuffer ENDP

InvalidateScreen PROC USES eax ecx edi
    cld
    mov  ax, 0FFFFh
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
    jb   NextColumn
    ret
DrawBorders ENDP

BuildFrame PROC USES ecx edx esi edi
    call ClearBuffer
    call DrawBorders
    ; sub ka center subX hai: pehle tower/periscope, phir hull
    mov  ah, ATTR_SUB
    mov  dh, SUB_ROW - 1
    mov  dl, subX
    sub  dl, SAIL_HALF
    mov  esi, OFFSET subSail
    call PutString
    mov  ah, ATTR_SUB
    mov  dh, SUB_ROW
    mov  dl, subX
    sub  dl, SUB_HALF
    mov  esi, OFFSET subArt
    call PutString

    mov  esi, OFFSET Torpedoes
    mov  ecx, MAX_TORP
NextTorpedo:
    cmp  BYTE PTR [esi + 2], 0
    je   SkipTorpedo
    mov  dh, BYTE PTR [esi + 1]
    mov  dl, BYTE PTR [esi + 0]
    mov  eax, (ATTR_TORP SHL 8) OR CH_TORP
    call PutCell
SkipTorpedo:
    add  esi, 4
    loop NextTorpedo

    mov  esi, OFFSET Charges
    mov  ecx, MAX_CHARGE
NextCharge:
    cmp  BYTE PTR [esi + 2], 0
    je   SkipCharge
    cmp  BYTE PTR [esi + 3], 0
    je   VisibleCharge
    cmp  gameState, ST_SONAR
    jne  SkipCharge
    mov  ah, ATTR_MINE
    mov  edi, OFFSET mineArt
    jmp  DrawCharge
VisibleCharge:
    mov  ah, ATTR_CHARGE
    mov  edi, OFFSET chargeArt
DrawCharge:
    mov  dh, BYTE PTR [esi + 1]
    mov  dl, BYTE PTR [esi + 0]
    sub  dl, CHG_HALF     ; chargeArt and mineArt are both 3 cells wide
    push esi
    mov  esi, edi
    call PutString
    pop  esi
SkipCharge:
    add  esi, 4
    loop NextCharge
    call DrawExplosions
    call DrawHUD
    ret
BuildFrame ENDP

; sirf badle huay cells draw karo
Render PROC USES eax ebx ecx edx esi edi
    xor  ebx, ebx
NextCell:
    cmp  ebx, SCREEN_W * SCREEN_H - 1
    jae  CopyFrame
    mov  ax, ScreenBuf[ebx*2]
    cmp  ax, PrevBuf[ebx*2]
    je   SkipCell
    push eax
    mov  eax, ebx
    xor  edx, edx
    mov  ecx, SCREEN_W
    div  ecx
    mov  dh, al
    call Gotoxy
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
    mov  ecx, (SCREEN_W * SCREEN_H) / 2
    rep  movsd
    ret
Render ENDP
