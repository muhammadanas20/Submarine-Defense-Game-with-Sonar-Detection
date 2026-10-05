# Project proposal outline — Depth Charge

**Status:** Draft scaffold. Complete the text as a team and submit it through the course's required channel by **Thursday, 15 October 2026**. Do not treat the placeholders as completed research or approved requirements.

## Cover information

- Course: EL-2003 Computer Organization and Assembly Language Lab, Fall 2026
- Section: BCS-3C
- Project: Depth Charge — Submarine Defense with Sonar Detection
- Group leader: Muhammad Anas (25K-0899)
- Members: Syed Alyan Hussain (25K-0648); Ali Raza (25K-0827)
- Instructor: Muhammad Owais

## 1. Problem / motivation

[Explain the educational problem this project addresses: applying x86 assembly concepts to a small interactive program. Write this section in the team's own words.]

## 2. Objectives

- Build an 80 × 25 text-mode game in x86 assembly using the course Irvine32 environment.
- Practice procedure calls, arrays/structures, keyboard polling, timing, comparisons, state machines, and file I/O.
- Integrate separately owned modules through a shared procedure/data contract and Git pull requests.

## 3. Game overview

[Describe the submarine, falling depth charges, torpedoes, scoring, lives, sonar/mines, pause, and game-over/menu flow. Confirm the final controls after implementation.]

## 4. Technical approach

- Target platform: Windows x86 (Win32), Visual Studio with MASM build customizations, Irvine32.
- Screen: 80 columns × 25 rows; planned frame duration: 80 ms.
- State values and shared object arrays: `src/shared/constants.inc` and `src/shared/data.inc`.
- Module boundaries and ownership: `README.md`.

## 5. Team responsibilities

| Member | Planned responsibility | Evidence / deliverables |
|---|---|---|
| Muhammad Anas | Main loop, timing, input, submarine, torpedoes, collisions, integration | [Fill in] |
| Syed Alyan Hussain | Rendering, HUD, explosions, sonar | [Fill in] |
| Ali Raza | Random numbers, menus, charges, sound, scoring, high score | [Fill in] |

## 6. Schedule and milestones

Use the dates and acceptance criteria in `README.md` and the attached guide. Add the team's actual weekly progress, risks, and mitigation actions.

## 7. Testing and evaluation

Use `docs/testing/acceptance-checklist.md`. Record the machine, Visual Studio/Irvine setup, build configuration, test date, expected result, actual result, and any defect for each test.

## 8. Risks and mitigations

[Consider integration conflicts, Irvine/VS setup differences, frame timing, keyboard buffering, collision crossing, and time for lab-PC testing. Add owners and mitigations.]

## 9. References and disclosure

- Cite the course textbook, Irvine32 materials, and any other material actually used.
- Disclose AI assistance accurately in line with the course instructions. See `docs/report/anas.md` for a draft statement to adapt.
