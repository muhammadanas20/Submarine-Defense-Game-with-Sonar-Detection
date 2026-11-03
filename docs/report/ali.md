# Report section draft — Ali Raza (25K-0827)

**Review required:** this is an AI-assisted draft describing the repository code. Personalize it, verify every statement, and add your own build/test evidence before submission.

## Responsibilities and implementation

My area is pseudo-random numbers, charge spawning/movement, menus, scoring, lives, levels, sound, and the high-score file. `Rand` implements a clock-seeded linear congruential generator and returns an exact small range using unsigned division. `SpawnCharge` uses 15 fixed slots, columns 1–78, and a one-in-five hidden flag. `UpdateCharges` moves active charges according to the fall timer.

`AddScore` adds +10/+25 and calculates `score / 200 + 1`, capped at level 9. `ApplyLevel` copies fall/spawn delays from two nine-entry tables. `LoseLife` decrements lives and either recenters the submarine or sets game over. The menu, instructions, and game-over screens use direct console output and flush old keys at transitions. Five Beep effects use one small macro that saves general registers. `LoadHighScore` and `SaveHighScore` handle a four-byte binary record with missing/short-file and write-count checks.

## Design decisions

I kept the random generator simple and suitable for gameplay, not security. Lookup tables make difficulty easy to inspect. Normal-play tones are short because Beep blocks; longer tones accompany sonar or end-of-life events. Only a successful higher write sets the new-record flag, so tying an old score is not misreported. The file write is intentionally simple rather than atomic.

## Testing evidence

The integrated source passed assembly/link and a 1,090-check harness under Wine, including random range, spawn capacity, fall timing, scoring thresholds, level cap, file round trip, lower-score preservation, invalid-write handling, and short-file recovery. Audible tone quality and native Windows file permissions remain lab-PC checks. I will record actual speaker, restart-persistence, and permission results before claiming them.

## Integration and reflection

Anas calls my score/life procedures from collisions and my charge procedures from the loop. Alyan draws my charge array and HUD values. The main lesson is that a hidden object can remain logically active, and that file I/O needs explicit error and byte-count checks.

## AI-use / source disclosure

AI assistance was used to implement and review this module and prepare this draft, following the repository's AI-assisted guides. I will personalize the report, disclose assistance according to course policy, and demonstrate only code I understand. References include the course outline, Irvine32 file procedures, and Microsoft Win32 Beep documentation.
