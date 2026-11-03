# Progress — Muhammad Anas (25K-0899)

The repository previously contained Anas's loop/input/torpedo/collision code and a weekly log. Those historical entries are preserved in Git history. This file now records the verified integration status without claiming that future lab tests already happened.

| Date | Focus | Status | Evidence / next action |
|---|---|---|---|
| Before 2026-11-03 | A1–A7 core scaffold and Anas modules | Present in repository history | See commits `7e10b97` through `0057db3` and PR #1. |
| 2026-11-03 | Completion integration and fixes | Implemented; member review pending | Integrated Alyan/Ali modules, removed stubs, fixed project entry/SafeEH settings, reset all round timers, added pause-during-sonar, limited submarine hits to one per frame, and corrected game-over flow. |
| 2026-11-03 | Compatibility verification | Passed | MASM 6.14 assembly, PE32 link, Wine console smoke test, and 1,090-check harness. See `docs/testing/verification-2026-11-03.md`. |
| Pending | Visual Studio 2022 / lab-PC acceptance | Not tested | Build Win32 on the lab machine and complete the manual checklist. |
| Pending | Individual report/viva preparation | Draft provided | Review `docs/viva/anas.md`, personalize `docs/report/anas.md`, and practise the debugger tasks. |

## Integration fixes to understand

- `InitGame` now clears `ExplTimer`, frame count, sonar variables, and pause variables as well as the object arrays.
- `HandleInput` remembers whether pause interrupted normal play or sonar and extends sonar by the paused duration.
- `CheckCollisions` processes at most one submarine hit per frame.
- `GameLoop` leaves normal play immediately when the last life is lost.
- `Project.vcxproj` sets entry point `main` and disables SafeEH for the legacy assembly objects.
- Temporary stub files were removed after all real procedures were implemented.

## Review checklist for Anas

- [ ] Explain the state machine and frame order.
- [ ] Explain non-blocking input and both boundary checks.
- [ ] Explain the crossing collision check and the two loop counters.
- [ ] Explain pause-during-sonar timestamp adjustment.
- [ ] Explain every `REP STOSB` reset, including `ExplTimer`.
- [ ] Build Win32 in Visual Studio and run the full manual checklist.
- [ ] Record real lab-PC results and disclose AI assistance accurately.
