# ProgramBench benchability audit

A model-blind, re-runnable audit of [ProgramBench](https://arxiv.org/abs/2605.03546) (arXiv 2605.03546),
produced by reading **all 201 hidden test suites** (public on Hugging Face at
`programbench/ProgramBench-Tests`) and classifying every exact-output assertion.

## If you are running ProgramBench, start here

This audit is a **conflict-of-interest-free escape hatch**. Reporting Fully Resolved over the full 201
includes tasks no source-blind solver can resolve; excluding them on your own judgment moves the very
score you are reporting, which is a conflict of interest. The escape is to exclude on a list you did
not author and cannot tilt. A runner already did exactly this with the
[SWE-bench Pro determinacy audit](https://github.com/scaleapi/SWE-bench_Pro-os/issues/108), adopting its
subset to skip the unsolvable cases. Two artifacts in `findings/05_runner_subset.md`:

- **Skip-list (24 programs)** — no source-blind, offline solver can resolve these (a recall-only test,
  or a byte-exact render the contract does not fix). Running a model on them spends build budget
  (about $9/task) on a foregone fail. Exclude them, and the headline stops conflating reconstruction
  with recall.
- **Benchable subset (171 programs)** — report Fully Resolved over these instead of the full 201.

Adopting this is **not a discretionary call and carries no conflict of interest**, because the list has
three properties:

1. **Model-blind.** The exclusion criterion is read from the *test bodies*, never from which tasks a
   model failed. The list is fixed before any model runs, so it cannot be reverse-engineered to flatter
   a score.
2. **Replayable.** Each witness ships the `retrieval_cmd` that re-fetches its exact test; the verdict
   belongs to the check, not to the author. You do not have to trust us — re-derive it by grep.
3. **Citable.** It is the same fixed list for everyone, so excluding it is a property of the benchmark,
   not a choice about one model.

A separate **grader-caution list (29 programs, 12 vacuous-risk)** flags suites whose graders write their
own golden from the reference run; do not trust a pass from those as "correct" without confirming the
golden is present and contractual.

You do not need to cite this audit to use it. The method is in `METHODOLOGY.md` and the spine
re-derives by grep over the public suites, so you can reproduce the subset yourself and report it as
your own finding. Citing the artifact simply saves the derivation and puts a model-independent reason
on the record for why you ran a subset rather than the full 201.

## What the audit found

ProgramBench asks a model to reconstruct a program from its execute-only binary and docs, no source, no
internet, graded one-shot on a hidden suite under a conjunctive metric (Fully Resolved = pass every
test). The construct-validity question: does passing measure source-blind reconstruction, or something
else? Three independent answers:

- **Recall (information barrier), 21 programs.** A graded test asserts the exact output of a non-stdlib
  function (hash, cipher, codec, compressor, opaque binary format, Unicode width table) no offline
  solver reconstructs. `findings/01_recall_witnesses.md`.
- **Oracle provenance (the grader), 29 programs.** Graded tests write their own oracle from the
  reference run, so they score byte-identity-to-reference, not a contract; 12 in a form that passes any
  output if the golden is absent. The test oracle problem
  ([Barr et al. 2015](https://doi.org/10.1109/TSE.2014.2372785);
  [Weyuker 1982](https://doi.org/10.1093/comjnl/25.4.465)). `findings/02_oracle_provenance.md`.
- **Coverage (complexity barrier), structural.** Hidden + one-shot + conjunctive grading makes the
  solver's effective target the whole behavioral surface, whose measured size (median 204 distinct
  graded obligations per program, up to 4,064) collapses the pass rate. Completeness is a bar testing
  cannot certify ([Dijkstra 1970](https://www.cs.utexas.edu/~EWD/transcriptions/EWD02xx/EWD249/EWD249.html))
  and is undecidable in general ([Rice 1953](https://doi.org/10.1090/S0002-9947-1953-0053041-6)). This
  explains the reported zero floor without any recall.

The non-determinism classes one would suspect (concurrency, paths, time, locale, float, ordering) were
checked and found benchable or neutralized by the benchmark's sandbox and flaky-filter; recorded in
`findings/03_class_checks.md` so a runner need not re-check.

## Verify any claim

Everything is in `data/audit.db` (SQLite). Regenerate the human-readable findings with
`python3 scripts/export_findings.py`. Re-derive the spine from scratch with the `scripts/` pipeline
(`litmatch_sweep.py` for the complete exact-output inventory, `capture_sweep.py` for the self-capture
census, `find_render_witnesses.sh` for the render class). See `METHODOLOGY.md` for the transferable
method.

## Companion paper

[june.kim/the-unreasonable-largeness-of-behavior](https://june.kim/the-unreasonable-largeness-of-behavior).
This repo is the receipts and the re-runnable method behind it.

## Status

Scoped to construct validity, not contamination. Corrections to any specific verdict are welcome via
issue; every claim is inspectable from the committed receipts and the mechanical spine is re-derivable
by grep without trusting the author. A right-of-reply issue and a Zenodo archive are the next steps.

## License

Dual copyleft. Content (data, findings, docs) under [CC BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt); code (`scripts/`) under [GPL-3.0-or-later](LICENSES/GPL-3.0.txt). See [LICENSE](LICENSE). The audited paper ([arXiv:2605.03546](https://arxiv.org/abs/2605.03546)) is its authors' work, linked not redistributed.
