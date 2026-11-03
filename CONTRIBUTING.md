# Contributing and review rules

The game is now integrated. Use small branches and pull requests for fixes, documentation, and lab-PC test results. Keep the code simple enough for every member to explain in the individual viva.

## Ownership

| Owner | Code | Documents |
|---|---|---|
| Anas | `src/game.asm`, `src/shared/`, `src/anas/` | `docs/progress/anas.md`, `docs/report/anas.md` |
| Alyan | `src/alyan/` | `docs/progress/alyan.md`, `docs/report/alyan.md` |
| Ali | `src/ali/` | `docs/progress/ali.md`, `docs/report/ali.md` |

Shared data, project settings, README, proposal notes, and testing documents are integration files. Discuss changes that affect another member. The completion PR intentionally touches all three areas because it integrates the missing modules; ordinary weekly fixes should stay within owned paths where possible.

## Normal fix workflow

```bash
git checkout main
git pull origin main
git checkout -b fix-short-description
# Make and test one small change.
git status
git add <only-the-files-you-changed>
git commit -m "Describe the fix"
git push -u origin fix-short-description
```

Open a PR against `main`. Include:

- What changed and why.
- Exact build configuration and test steps.
- Actual result, not an assumed pass.
- Any known limitation or follow-up.
- AI/source disclosure when applicable.

Do not commit `.vs/`, `*.user`, `bin/`, `obj/`, `highscore.dat`, access tokens, or another member's unrelated work.

## Build before merge

1. Open `Project.sln` in Visual Studio 2022.
2. Select **Debug | Win32** and build.
3. Run the menu, movement, firing, sonar, pause, collision, game-over, and replay paths affected by the change.
4. Record lab-PC results in `docs/testing/acceptance-checklist.md`.
5. Review the PR diff and merge only after the affected tests pass.

The temporary `stubs_*.inc` files have been removed. Do not reintroduce no-op procedures to hide unfinished work; use a clearly marked branch/PR instead.

## Academic integrity

Every member must review the code they present, personalize their report, and disclose AI assistance according to the instructor's policy. A merged PR is not evidence that a member understands or personally tested the code.
