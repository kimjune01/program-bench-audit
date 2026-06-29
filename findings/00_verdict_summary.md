# ProgramBench benchability audit — verdict summary

Complete mechanical read of all 201 task suites (public on HF: `programbench/ProgramBench-Tests`).
Every verdict is re-derivable from the cited test body; the audit is one-sided (a witness proves
unbenchable; "no witness found" is not a clearance).

| verdict | programs |
|---|---|
| Unbenchable, recall witness verified | 21 |
| Unbenchable, oracle implementation-pinned (render bytes) | 3 |
| Self-capturing-golden programs (oracle provenance, axis 2) | 29 (12 in the vacuous-if-absent conditional form) |

Recall floor 21 and the 29-program self-capture finding are independent lower bounds.
The literal-match denominator is 135,740 exact-output assertions.
