from __future__ import annotations

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "docs", "submission", "assets"))
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

SCREEN_W, SCREEN_H = 80, 25

PALETTE = {
    0: (12, 12, 12),
    7: (170, 170, 170),
    9: (85, 85, 255),
    10: (85, 255, 85),
    11: (85, 255, 255),
    12: (255, 85, 85),
    14: (255, 255, 85),
}
ATTR_TEXT, ATTR_SUB, ATTR_TORP, ATTR_CHARGE, ATTR_MINE = 7, 10, 11, 12, 10
ATTR_HUD, ATTR_BORDER = 14, 9

SUB_ROW, BOTTOM_ROW, HUD_ROW = 23, 24, 0
SUB_HALF, SAIL_HALF, CHG_HALF = 5, 1, 1


class Screen:
    def __init__(self) -> None:
        self.cells = [[(" ", PALETTE[ATTR_TEXT]) for _ in range(SCREEN_W)]
                      for _ in range(SCREEN_H)]

    def put_cell(self, row: int, col: int, ch: str, color: int) -> None:
        if 0 <= row < SCREEN_H and 0 <= col < SCREEN_W:
            self.cells[row][col] = (ch, PALETTE[color])

    def put_string(self, row: int, col: int, text: str, color: int) -> None:
        for i, ch in enumerate(text):
            self.put_cell(row, col + i, ch, color)

    def clear_buffer(self) -> None:
        for r in range(SCREEN_H):
            for c in range(SCREEN_W):
                self.put_cell(r, c, " ", ATTR_TEXT)

    def draw_borders(self) -> None:
        for c in range(0, SCREEN_W - 1):
            self.put_cell(1, c, "=", ATTR_BORDER)
            self.put_cell(BOTTOM_ROW, c, "=", ATTR_BORDER)

    def draw_sub(self, sub_x: int) -> None:
        self.put_string(SUB_ROW - 1, sub_x - SAIL_HALF, "_!_", ATTR_SUB)
        self.put_string(SUB_ROW, sub_x - SUB_HALF, "<=-[ooo]-=>", ATTR_SUB)

    def draw_torpedo(self, x: int, y: int) -> None:
        self.put_cell(y, x, "^", ATTR_TORP)

    def draw_charge(self, x: int, y: int, hidden: bool, sonar: bool) -> None:
        if hidden:
            if sonar:
                self.put_string(y, x - CHG_HALF, "[!]", ATTR_MINE)
            return
        self.put_string(y, x - CHG_HALF, "(@)", ATTR_CHARGE)

    def draw_explosion(self, x: int, y: int, frame: int) -> None:
        chars = ".+*#@"
        colors = [ATTR_TEXT, ATTR_HUD, ATTR_CHARGE, ATTR_CHARGE, ATTR_HUD]
        self.put_cell(y, x, chars[frame], colors[frame])

    def draw_hud(self, score: int, lives: int, level: int, sonar_text: str,
                 paused: bool = False) -> None:
        self.put_string(HUD_ROW, 1, "SCORE ", ATTR_HUD)
        self.put_string(HUD_ROW, 7, f"{score:05d}", ATTR_HUD)
        self.put_string(HUD_ROW, 16, "LIVES ", ATTR_HUD)
        self.put_cell(HUD_ROW, 22, str(lives), ATTR_HUD)
        self.put_string(HUD_ROW, 27, "LEVEL ", ATTR_HUD)
        self.put_cell(HUD_ROW, 33, str(level), ATTR_HUD)
        self.put_string(HUD_ROW, 39, "SONAR ", ATTR_HUD)
        self.put_string(HUD_ROW, 45, sonar_text, ATTR_HUD)
        if paused:
            self.put_string(12, 24, "== PAUSED - press P to resume ==", ATTR_HUD)
        self.put_string(BOTTOM_ROW, 15,
                        "A/D MOVE  W FIRE  SPACE SONAR  P PAUSE  ESC MENU",
                        ATTR_BORDER)

    def to_image(self, path: str, title: str | None = None, scale: int = 2) -> None:
        cw, ch = 9, 19
        pad = 6
        w = SCREEN_W * cw + pad * 2
        h = SCREEN_H * ch + pad * 2
        img = Image.new("RGB", (w * scale, h * scale), (12, 12, 12))
        d = ImageDraw.Draw(img)
        font = ImageFont.truetype(FONT, (ch - 4) * scale)

        for r in range(SCREEN_H):
            for c in range(SCREEN_W):
                chx, col = self.cells[r][c]
                if chx == " ":
                    continue
                d.text(((pad + c * cw) * scale, (pad + r * ch) * scale),
                       chx, font=font, fill=col)
        d.rectangle([0, 0, w * scale - 1, h * scale - 1],
                    outline=(90, 90, 95), width=2 * scale // 2)
        img.save(path)


def figure_menu(path: str) -> None:
    s = Screen()
    s.clear_buffer()
    s.put_string(5, 24, "DEPTH CHARGE - SUBMARINE DEFENSE", ATTR_HUD)
    s.put_string(6, 38, "_!_", ATTR_SUB)
    s.put_string(7, 34, "<=-[ooo]-=>", ATTR_SUB)
    for row, text in ((9, "1. Start game"), (10, "2. Instructions"),
                      (11, "3. Exit")):
        s.put_string(row, 32, text, ATTR_TEXT)
    s.put_string(14, 32, "High score: ", ATTR_TEXT)
    s.put_string(14, 44, "1250", ATTR_TEXT)
    s.put_string(17, 23, "Choose 1, 2 or 3 (ESC also exits)", ATTR_TEXT)
    s.to_image(path, "Depth Charge - Submarine Defense")


def figure_instructions(path: str) -> None:
    s = Screen()
    s.clear_buffer()
    s.put_string(3, 34, "HOW TO PLAY", ATTR_HUD)
    lines = [
        "A / D or Left / Right : move the submarine",
        "W : fire a torpedo       P : pause / resume",
        "SPACE : sonar for 2 seconds; 10-second recharge",
        "ESC : return to the menu without saving this round",
        "(@) depth charge : +10 points",
        "[!] hidden mine (seen with sonar) : +25 points",
        "You have 3 lives. Every 200 points adds a level.",
        "Charges fall faster as you reach higher levels.",
    ]
    rows = [6, 8, 10, 12, 14, 15, 17, 18]
    for row, text in zip(rows, lines):
        s.put_string(row, 5, text, ATTR_TEXT)
    s.put_string(22, 5, "Press any key to return to the menu", ATTR_TEXT)
    s.to_image(path, "Depth Charge - Submarine Defense")


def figure_gameplay(path: str) -> None:
    s = Screen()
    s.clear_buffer()
    s.draw_borders()
    s.draw_sub(40)
    charges = [(12, 4), (30, 6), (52, 5), (68, 8), (22, 12), (44, 10),
               (75, 14), (8, 16), (36, 15), (60, 18), (18, 20), (66, 21)]
    for x, y in charges:
        s.draw_charge(x, y, hidden=False, sonar=False)
    for x, y in ((26, 9), (48, 17), (70, 12)):
        s.draw_charge(x, y, hidden=True, sonar=False)
    for x, y in ((40, 20), (40, 16), (52, 19)):
        s.draw_torpedo(x, y)
    s.draw_explosion(60, 23 - 2, 2)
    s.draw_hud(180, 2, 1, "00007")
    s.to_image(path, "Depth Charge - Submarine Defense")


def figure_sonar(path: str) -> None:
    s = Screen()
    s.clear_buffer()
    s.draw_borders()
    s.draw_sub(40)
    charges = [(12, 4), (30, 6), (52, 5), (68, 8), (22, 12), (44, 10),
               (8, 16), (36, 15), (60, 18), (66, 21)]
    for x, y in charges:
        s.draw_charge(x, y, hidden=False, sonar=True)
    mines = ((26, 9), (48, 17), (70, 12), (75, 14), (18, 20))
    for x, y in mines:
        s.draw_charge(x, y, hidden=True, sonar=True)
    for x, y in ((40, 20), (40, 16)):
        s.draw_torpedo(x, y)
    s.draw_hud(180, 2, 1, "ACTIVE")
    s.to_image(path, "Depth Charge - Submarine Defense")


def figure_pause(path: str) -> None:
    s = Screen()
    s.clear_buffer()
    s.draw_borders()
    s.draw_sub(30)
    for x, y in ((14, 5), (40, 7), (62, 4), (26, 11), (52, 9), (70, 15)):
        s.draw_charge(x, y, hidden=False, sonar=False)
    s.draw_torpedo(30, 18)
    s.draw_hud(240, 1, 2, "READY ", paused=True)
    s.to_image(path, "Depth Charge - Submarine Defense")


def figure_gameover(path: str) -> None:
    s = Screen()
    s.clear_buffer()
    s.put_string(7, 35, "GAME OVER", ATTR_CHARGE)
    s.put_string(10, 28, "Final score: ", ATTR_TEXT)
    s.put_string(10, 41, "180", ATTR_TEXT)
    s.put_string(12, 28, "High score: ", ATTR_TEXT)
    s.put_string(12, 40, "1250", ATTR_TEXT)
    s.put_string(20, 22, "Press any key to return to the menu", ATTR_TEXT)
    s.to_image(path, "Depth Charge - Submarine Defense")


def figure_gameover_record(path: str) -> None:
    s = Screen()
    s.clear_buffer()
    s.put_string(7, 35, "GAME OVER", ATTR_CHARGE)
    s.put_string(10, 28, "Final score: ", ATTR_TEXT)
    s.put_string(10, 41, "1460", ATTR_TEXT)
    s.put_string(12, 28, "High score: ", ATTR_TEXT)
    s.put_string(12, 40, "1460", ATTR_TEXT)
    s.put_string(14, 32, "NEW HIGH SCORE!", ATTR_HUD)
    s.put_string(20, 22, "Press any key to return to the menu", ATTR_TEXT)
    s.to_image(path, "Depth Charge - Submarine Defense")


BUILDERS = {
    "fig_menu.png": figure_menu,
    "fig_instructions.png": figure_instructions,
    "fig_gameplay.png": figure_gameplay,
    "fig_sonar.png": figure_sonar,
    "fig_pause.png": figure_pause,
    "fig_gameover.png": figure_gameover,
    "fig_gameover_record.png": figure_gameover_record,
}


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for name, fn in BUILDERS.items():
        fn(os.path.join(OUT, name))
        print("wrote", os.path.join(OUT, name))


if __name__ == "__main__":
    main()
