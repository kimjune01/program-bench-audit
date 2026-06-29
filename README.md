# ProgramBench benchability audit

An independent, mechanical, re-runnable audit of [ProgramBench](https://arxiv.org/abs/2605.03546)
(arXiv 2605.03546), produced by reading **all 201 hidden test suites** (public on Hugging Face at
`programbench/ProgramBench-Tests`) and classifying every exact-output assertion.

ProgramBench asks a model to reconstruct a program from its execute-only binary and docs, with no
source and no internet, and grades it on a hidden suite under a conjunctive metric (Fully Resolved =
pass every test). This audit asks the construct-validity question: **does passing measure source-blind
reconstruction, or something else?**

## Headline findings

- **Recall floor = 21 programs** (one-sided lower bound). Each has a graded test whose exact expected
  value is the output of a non-stdlib function (hash, cipher, codec, compressor, opaque binary format,
  Unicode width table) that no offline solver can reconstruct from finite probing. Recall, not
  reconstruction. See `findings/01_recall_witnesses.md`.
- **Self-capturing goldens = 29 programs** (a second, independent axis). Graded tests write their own
  oracle from the reference run (`if not golden.exists(): golden.write_text(result.stdout)`), so the
  test grades byte-identity-to-the-reference, not a contract; 12 are in a conditional form that passes
  any output if the golden is absent. This is the test oracle problem
  ([Barr et al. 2015](https://doi.org/10.1109/TSE.2014.2372785);
  [Weyuker 1982](https://doi.org/10.1093/comjnl/25.4.465)). See `findings/02_oracle_provenance.md`.
- **Classes of concern, checked and cleared.** Non-determinism / environment-coupling classes
  (concurrency, paths, time, locale, float, ordering, parser errors) are benchable or neutralized by
  the benchmark's sandbox + flaky-filter + deterministic-projection testing. Recorded so runners need
  not re-check. See `findings/03_class_checks.md`.

The two axes are independent: recall is a property of the program (cannot be reconstructed); oracle
provenance is a property of the grader (the verdict is uninterpretable). Both make the conjunctive
headline metric not a clean measure of reconstruction.

## For someone running ProgramBench

The actionable unit is the whole program (the metric is conjunctive, so one bad test forecloses a
task; a runner cannot drop individual tests without moving the score being reported). `findings/`
gives a citable per-program verdict. Excluding the unbenchable programs lets you report Fully Resolved
against the benchable subset, so the headline stops conflating reconstruction with recall.

## Verify any claim

Everything is in `data/audit.db` (SQLite). Each witness row carries a `retrieval_cmd` that re-fetches
the exact test body. To regenerate the human-readable findings:

```sh
python3 scripts/export_findings.py
```

Key tables: `witnesses` (adjudicated recall + render witnesses, with replayable coordinates),
`capture_smell` (self-capturing-golden census), `class_checks` (non-determinism classes checked),
`litmatch` (every exact-output assertion, 135,740 rows), `programs` (per-program status).

## Re-run from scratch

`scripts/` holds the pipeline: `seed.py` (program list), `litmatch_sweep.py` (the complete
exact-output inventory), `capture_sweep.py` (self-capture census), `find_render_witnesses.sh` (render
class), plus the subagent extractors (`extract-batch.js`, `verify-witnesses.js`) that surface
candidates for hand-adjudication. See `METHODOLOGY.md` for how the pieces fit and why.

## Companion paper

The argument is written up at
[june.kim/the-unreasonable-largeness-of-behavior](https://june.kim/the-unreasonable-largeness-of-behavior).
This repo is the receipts and the re-runnable method behind it.
