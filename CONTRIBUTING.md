# Contributing and Git workflow

This project uses one source folder per owner to reduce merge conflicts. Confirm the current owner and module contract in `README.md` before editing.

## First-time setup (Week 0)

1. Create/clone the team repository and copy this starter folder into it.
2. Open `Project.sln` in Visual Studio and verify the local Irvine32 path/settings.
3. Build and run the smoke test before inviting the other members to clone.
4. Add collaborators and merge their practice PRs only after checking that each PR contains only its own progress log.

## Weekly branch and pull request

Example for Anas, Week 1:

```bash
git checkout main
git pull origin main
git checkout -b week1-anas
# Make one small, buildable change.
git status
git add src/game.asm src/shared src/anas docs/progress/anas.md docs/report/anas.md
git commit -m "A2: main and GameLoop state machine"
git push -u origin week1-anas
```

Open a PR with a title such as `Week 1 – Anas – A2 A3`. Include the build/test result and any known limitations. Stage only files you own; **do not use `git add .` for weekly work**. Do not commit Visual Studio per-user files, build output, or another member's module.

## Weekly merge order

1. Merge Anas's PR first, then Alyan's, then Ali's.
2. On the integration machine, pull `main`, build in Visual Studio, and play for at least five minutes.
3. Post `Week N merged — sync now` to the group.
4. At M1, M2, M3, and v1.0, tag the verified commit. Do not tag a milestone until the integration build passes.

## Ownership

- Anas: `src/game.asm`, `src/shared/`, `src/anas/`, and Anas's docs.
- Alyan: `src/alyan/` and Alyan's docs.
- Ali: `src/ali/` and Ali's docs.
- Coordinate any shared-data contract change before merging it. Project files are maintained by Anas; members should not commit personal Visual Studio setting changes.

## Naming rules (read before adding a label)

MASM reserves every instruction mnemonic, directive, and operator, and reserved words are **case-insensitive**. A label or variable named after one assembles with the old MASM 6.14 and then stops the newer `ml.exe` in Visual Studio 2022/2026 with `error A2008: syntax error`, which points at the line *after* the label. This already happened with `Pause:`/`Resume:` in `anas\input.inc` (now `PauseGame:`/`UnpauseGame:`) and the old `PauseMessage:` in `alyan\hud.inc` (now `DrawPauseBanner:`).

- Do not name anything `pause`, `resume`, `exit`, `loop`, `int`, `nop`, `wait`, `size`, `width`, `mask`, `record`, `label`, `local`, `title`, `public`, `comment`, `proc`, or any other keyword.
- Prefer a verb-plus-object name (`PauseGame`, `KeyFire`, `FindSlot`); a two-word name cannot collide with a reserved word.
- Sprites: art strings are in `alyan\render.inc`, their widths and hit windows are in `shared\constants.inc`. Keep each sprite an odd number of cells and update both files together, or centring and collisions drift apart.

## Stubs and implementation

The three `stubs_*.inc` files define temporary no-op procedures so the program can be integrated incrementally. As a real procedure is added to its module file, delete its matching stub invocation (for example, after implementing `HandleInput`, remove `ANAS_STUB HandleInput`). Leave the other stubs in place until their implementations are ready.

## If a merge or build breaks

- Check `git status` and the changed-file list before committing.
- Restore accidental project/user-file changes rather than including them in a weekly PR.
- Resolve conflicts only in your own files; ask the owner before editing a teammate's module.
- If a merged PR breaks the build, coordinate a revert or a fix PR; do not silently patch another member's module.
