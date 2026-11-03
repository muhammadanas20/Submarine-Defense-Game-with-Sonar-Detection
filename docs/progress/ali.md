# Progress — Ali Raza (25K-0827)

Historical weekly entries were not recorded in this file. The table below records the integration work actually present in the completion PR; it does not invent weekly history.

| Date | Focus | Status | Evidence / next action |
|---|---|---|---|
| 2026-11-03 | C1–C7 random, screens, charges, sound, score, levels, file | Implemented in integration PR; member review pending | `src/ali/*.inc`; MASM assembly/link and 1,090-check harness passed under Wine. Ali must review, build in Visual Studio, and run manual/audio/file tests. |
| Pending | Lab-PC acceptance | Not tested | Record OS/VS/Irvine versions and actual results in `docs/testing/acceptance-checklist.md`. |
| Pending | Individual report/viva preparation | Draft provided | Review `docs/viva/ali.md`, personalize `docs/report/ali.md`, and practise the debugger tasks. |

## Integration notes

- Implemented clock-seeded LCG with exact small-range modulo and zero-range guard.
- Implemented menu, instructions, and game-over screens with key flushing.
- Implemented 15-slot charge spawning/falling and approximately 20% hidden mines.
- Implemented five Beep effects through one small register-saving macro.
- Implemented +10/+25 scoring, three lives, and nine lookup-table levels.
- Implemented four-byte high-score load/save with short-file and write-count checks.
- Fixed the guide's tied-score message issue: only a successful higher write sets `newRecord`.

## Review checklist for Ali

- [ ] Explain the LCG, `SHR`, `MUL`, `DIV`, and clearing `EDX`.
- [ ] Explain hidden versus active charge flags.
- [ ] Explain level calculation and the two delay tables.
- [ ] Explain why Beep is blocking and why normal tones are short.
- [ ] Explain the four binary file bytes and first-run behavior.
- [ ] Build Win32 in Visual Studio and run score/file/audio tests.
- [ ] Record real lab-PC results and disclose AI assistance accurately.
