"""Draw Figure 1 (program flowchart), Figure 2 (state machine) and Figure 3
(module / data interaction) for the Depth Charge final report."""

from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flow import arrow, box, new_figure, polyline, save  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "docs", "submission", "assets"))

MUTED = "#5a5a5a"


# ---------------------------------------------------------------------------
# Figure 1 - complete program flowchart
# ---------------------------------------------------------------------------
def figure_flowchart(path: str) -> None:
    fig, ax = new_figure(6.6, 9.05)

    SX, SW = 1.82, 2.42           # spine (main loop)
    ROW = [1.25, 3.28, 5.31]      # three state boxes
    RW = 1.80
    LEFT_RAIL, RIGHT_RAIL = 0.14, 6.46
    RX, RW2 = 5.05, 2.55          # right column (menu branches)

    def cx(r):
        return (r[0] + r[2]) / 2

    b = {}
    b["start"] = box(ax, SX, 8.72, 0.90, 0.24, "Start", "term", shape="term", fs=7.0)
    b["init"] = box(ax, SX, 8.28, SW, 0.44,
                    "InitSystem: SeedRandom, SetConsoleTitle, hide cursor", "proc")
    b["hs"] = box(ax, SX, 7.74, SW, 0.44,
                  "LoadHighScore: open highscore.dat, read 4 bytes (0 if absent)", "data")
    b["menu"] = box(ax, SX, 7.18, SW, 0.44,
                    "ShowMenu: title, submarine art, options 1/2/3, high score", "proc")
    b["choice"] = box(ax, SX, 6.40, 2.00, 0.60, "Menu choice?", "dec",
                      shape="diamond", bold_first=True)
    b["instr"] = box(ax, RX, 6.60, RW2, 0.48,
                     "2: ShowInstructions, then redraw the menu", "io")
    b["end"] = box(ax, RX, 5.42, 0.95, 0.24, "End", "term", shape="term", fs=7.0)
    b["game"] = box(ax, SX, 5.44, SW, 0.62,
                    "InitGame: score 0, lives 3, level 1; REP STOSB clears the "
                    "three object arrays and the timers", "proc")
    b["input"] = box(ax, SX, 4.70, SW, 0.62,
                     "HandleInput: ReadKey (ZF = 1 means no key); A / D / arrows "
                     "move, W fires, SPACE sonar, P pause, ESC menu", "io")
    b["state"] = box(ax, SX, 3.98, 1.80, 0.54, "gameState?", "dec",
                     shape="diamond", bold_first=True)

    b["play"] = box(ax, ROW[0], 3.16, RW, 0.80,
                    "PLAYING: UpdateTorpedoes, UpdateCharges, SpawnCharge, "
                    "UpdateExplosions, CheckCollisions", "proc", fs=6.9)
    b["sonar"] = box(ax, ROW[1], 3.16, RW, 0.80,
                     "SONAR: UpdateSonar - freeze 2000 ms, play the sweep, "
                     "then a 10 s cooldown", "proc", fs=6.9)
    b["pause"] = box(ax, ROW[2], 3.16, RW, 0.80,
                     "PAUSED: no updates at all, the frame is still redrawn", "proc",
                     fs=6.9)

    b["build"] = box(ax, SX, 2.30, SW, 0.60,
                     "BuildFrame: clear the 80x25 buffer, borders, submarine, "
                     "torpedoes, charges/mines, explosions, HUD", "proc")
    b["render"] = box(ax, SX, 1.62, SW, 0.54,
                      "Render: compare ScreenBuf with PrevBuf, Gotoxy + WriteChar "
                      "for changed cells, copy the frame", "proc")
    b["delay"] = box(ax, SX, 1.04, SW, 0.40,
                     "FrameDelay: GetMseconds, Delay the rest of 80 ms", "proc")
    b["over"] = box(ax, SX, 0.46, 1.75, 0.52, "lives = 0?", "dec",
                    shape="diamond", bold_first=True)
    b["go"] = box(ax, 4.62, 0.46, 2.35, 0.50,
                  "GameOverScreen: SaveHighScore, game-over sound, wait for a key",
                  "proc", fs=6.9)

    def v(a, c, label=None, dx=0.05, dy=0.0):
        arrow(ax, (cx(a), a[1]), (cx(c), c[3]), label=label, label_dx=dx,
              label_dy=dy)

    v(b["start"], b["init"])
    v(b["init"], b["hs"])
    v(b["hs"], b["menu"])
    v(b["menu"], b["choice"])
    v(b["choice"], b["game"], label="1", dx=0.05)

    # menu choice 2 -> instructions -> back to the menu
    polyline(ax, [(2.82, 6.46), (3.14, 6.46), (3.14, 6.60), (b["instr"][0], 6.60)],
             label="2", label_at=(2.84, 6.50), label_dx=0.02, label_dy=0.03)
    polyline(ax, [(cx(b["instr"]), b["instr"][3]), (cx(b["instr"]), 7.02),
                  (3.03, 7.02)],
             label="back to menu", label_at=(4.35, 7.08), label_dx=0.0, label_dy=0.0)

    # menu choice 3 / ESC -> End
    polyline(ax, [(2.70, 6.28), (3.45, 6.28), (3.45, 5.42), (b["end"][0], 5.42)],
             label="3 / ESC", label_at=(3.48, 6.20), label_dx=0.02, label_dy=0.03)

    v(b["game"], b["input"])
    v(b["input"], b["state"])

    # state fan-out (no labels: each box states its own name)
    for i, key in enumerate(("play", "sonar", "pause")):
        arrow(ax, (SX, b["state"][1]), (ROW[i], b[key][3]))

    # state fan-in to the shared drawing pipeline
    bus_y = 2.72
    for i, key in enumerate(("play", "sonar", "pause")):
        ax.plot([ROW[i], ROW[i]], [b[key][1], bus_y], color=MUTED, lw=0.9, zorder=2)
    ax.plot([ROW[0], ROW[2]], [bus_y, bus_y], color=MUTED, lw=0.9, zorder=2)
    arrow(ax, (SX, bus_y), (SX, b["build"][3]))

    v(b["build"], b["render"])
    v(b["render"], b["delay"])
    v(b["delay"], b["over"])

    # "no" -> next frame (left rail up to HandleInput)
    polyline(ax, [(b["over"][0], 0.46), (LEFT_RAIL, 0.46), (LEFT_RAIL, 4.70),
                  (b["input"][0], 4.70)], label=None)
    ax.text(LEFT_RAIL + 0.05, 2.05, "next frame", fontsize=6.0, color=MUTED,
            rotation=90, va="center", ha="center")
    ax.text(b["over"][0] - 0.06, 0.62, "no", fontsize=6.2, color=MUTED,
            ha="right", va="center")

    # "yes" -> game over screen -> back to the menu
    arrow(ax, (b["over"][2], 0.46), (b["go"][0], 0.46), label="yes",
          label_dx=-0.02, label_dy=0.09)
    polyline(ax, [(cx(b["go"]), b["go"][3] + 0.02), (cx(b["go"]), 0.80),
                  (RIGHT_RAIL, 0.80), (RIGHT_RAIL, 7.18), (b["menu"][2], 7.18)],
             label=None)
    ax.text(RIGHT_RAIL - 0.06, 4.30, "next round: back to the menu",
            fontsize=6.0, color=MUTED, rotation=90, va="center", ha="center")

    save(fig, path)


# ---------------------------------------------------------------------------
# Figure 2 - game-state machine
# ---------------------------------------------------------------------------
def figure_state_machine(path: str) -> None:
    fig, ax = new_figure(6.4, 3.55)
    MUTED = "#5a5a5a"

    b = {}
    b["menu"] = box(ax, 0.98, 2.78, 1.45, 0.58, "MENU\nST_MENU = 0", "term",
                    shape="round", fs=7.2, bold_first=True)
    b["play"] = box(ax, 3.20, 2.78, 1.70, 0.58, "PLAYING\nST_PLAYING = 1", "proc",
                    shape="round", fs=7.2, bold_first=True)
    b["sonar"] = box(ax, 5.42, 2.78, 1.58, 0.58, "SONAR\nST_SONAR = 2", "data",
                     shape="round", fs=7.2, bold_first=True)
    b["pause"] = box(ax, 3.20, 1.50, 1.70, 0.50, "PAUSED\nST_PAUSED = 3", "io",
                     shape="round", fs=7.2, bold_first=True)
    b["over"] = box(ax, 1.05, 0.55, 1.70, 0.50, "GAME_OVER\nST_GAMEOVER = 4",
                    "dec", shape="round", fs=7.2, bold_first=True)
    b["exit"] = box(ax, 5.42, 0.55, 1.30, 0.40, "EXIT\nST_EXIT = 5", "term",
                    shape="term", fs=7.2, bold_first=True)

    # MENU -> PLAYING (1) on the upper lane, PLAYING -> SONAR on the same lane
    arrow(ax, (b["menu"][2], 2.92), (b["play"][0], 2.92), label="1",
          label_dx=-0.12, label_dy=0.05)
    arrow(ax, (b["play"][2], 2.92), (b["sonar"][0], 2.92), label="SPACE",
          label_dx=-0.16, label_dy=0.10)
    # SONAR -> PLAYING on the lower lane
    arrow(ax, (b["sonar"][0], 2.64), (b["play"][2], 2.64),
          label="after 2000 ms", label_dx=-0.55, label_dy=-0.11)

    # PLAYING <-> PAUSED
    arrow(ax, (2.90, b["play"][1]), (2.90, b["pause"][3]), label="P",
          label_dx=0.05, label_dy=0.0)
    arrow(ax, (3.52, b["pause"][3]), (3.52, b["play"][1]),
          label="P: restore stateBeforePause", label_dx=0.06, label_dy=0.0)
    # SONAR -> PAUSED
    polyline(ax, [(4.95, b["sonar"][1]), (4.95, 1.50), (b["pause"][2], 1.50)],
             label="P", label_at=(4.97, 1.56), label_dx=0.02, label_dy=0.02)
    # PLAYING -> GAME_OVER (lives = 0)
    polyline(ax, [(b["play"][0], 2.70), (2.10, 2.70), (2.10, 0.55),
                  (b["over"][2], 0.55)], label="lives = 0",
             label_at=(2.12, 1.90), label_dx=0.05, label_dy=0.0)
    # GAME_OVER -> MENU (any key)
    arrow(ax, (0.60, b["over"][3]), (0.60, b["menu"][1]), label="any key",
          label_dx=0.06, label_dy=0.0)
    # MENU -> EXIT
    polyline(ax, [(b["menu"][0], 2.78), (0.10, 2.78), (0.10, 0.20),
                  (5.42, 0.20), (5.42, b["exit"][1])], label="3 or ESC",
             label_at=(0.14, 1.60), label_dx=0.0, label_dy=0.0)

    ax.text(0.15, 3.36, "SPACE enters SONAR only when GetMseconds >= sonarReadyAt "
                        "(10 s recharge); SONAR returns to PLAYING automatically.",
            fontsize=6.3, color=MUTED, ha="left", va="center")
    ax.text(0.15, 3.18, "ESC in PLAYING, SONAR or PAUSED returns to MENU without "
                        "saving the round.", fontsize=6.3, color=MUTED,
            ha="left", va="center")
    save(fig, path)


# ---------------------------------------------------------------------------
# Figure 3 - module ownership and shared data
# ---------------------------------------------------------------------------
def figure_modules(path: str) -> None:
    fig, ax = new_figure(6.5, 3.10)
    MUTED = "#5a5a5a"

    heads = [
        (0.10, "proc", "Anas - group leader",
         "game.asm, anas\\input.inc\nanas\\torpedo.inc, anas\\collision.inc\n"
         "main, InitGame, GameLoop, FrameDelay,\nHandleInput, FireTorpedo,\n"
         "UpdateTorpedoes, CheckCollisions"),
        (2.25, "data", "Alyan",
         "alyan\\render.inc, hud.inc,\nexplosion.inc, sonar.inc\n"
         "InitSystem, PutCell, PutString,\nBuildFrame, Render, DrawHUD,\n"
         "StartExplosion, UpdateSonar"),
        (4.40, "proc", "Ali Raza",
         "ali\\random.inc, charges.inc,\nscore.inc, sound.inc, screens.inc,\n"
         "highscore.inc\nRand, SpawnCharge, AddScore,\nShowMenu, "
         "PlaySonarSweep, SaveHighScore"),
    ]
    for x0, style, title, body in heads:
        box(ax, x0 + 1.00, 2.35, 2.00, 1.10, title + "\n" + body, style,
            fs=6.1, bold_first=True)

    shared = box(ax, 3.25, 1.05, 6.20, 0.86,
                 "One shared .data segment - shared\\data.inc + "
                 "shared\\constants.inc\n"
                 "gameState, subX, score, lives, level, frameCount, fallDelay, "
                 "spawnDelay, sonarStart, sonarReadyAt\n"
                 "Torpedoes[8], Charges[15], Explosions[5], ExplTimer[5] - four "
                 "bytes per slot: x, y, active, hidden\n"
                 "ScreenBuf[2000] and PrevBuf[2000] WORD cells - low byte "
                 "character, high byte colour", "data", fs=6.1, bold_first=True)

    for i in range(3):
        x = 1.10 + i * 2.15
        arrow(ax, (x, 1.80), (x, shared[3]), style="<|-|>")
    ax.text(2.52, 1.62, "reads / writes", fontsize=6.0, color=MUTED,
            ha="center", va="center")

    ax.text(3.25, 3.00, "One translation unit: game.asm INCLUDEs every module "
                        "file, so any procedure can call any other directly.",
            fontsize=6.3, color=MUTED, ha="center", va="center")
    ax.text(3.25, 0.22, "Ownership rule: a member edits only the files in their "
                        "own folder; the shared contract changes only by agreement.",
            fontsize=6.1, color=MUTED, ha="center", va="center")
    save(fig, path)


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    figure_flowchart(os.path.join(OUT, "fig_flowchart.png"))
    figure_state_machine(os.path.join(OUT, "fig_states.png"))
    figure_modules(os.path.join(OUT, "fig_modules.png"))


if __name__ == "__main__":
    main()
