# ProgramBench benchability audit

A model-blind, re-runnable audit of [ProgramBench](https://arxiv.org/abs/2605.03546) (arXiv 2605.03546),
produced by reading **all 201 released test directories** (the 200 benchmark tasks plus one empty
placeholder; public on Hugging Face at `programbench/ProgramBench-Tests`) and classifying every
exact-output assertion by whether a source-blind, offline solver could obtain the value it checks.

Companion paper: **[ProgramBench Measures Recall](https://june.kim/programbench-measures-recall)**
(june.kim). This repo is the receipts and the re-runnable method behind it.

## If you are running ProgramBench, start here

This audit is a **conflict-of-interest-free escape hatch.** Reporting % Resolved over all 200 tasks
includes tasks no source-blind solver can resolve; excluding them on your own judgment moves the very
score you report, which is a conflict of interest. The escape is to exclude on a list you did not author
and cannot tilt, the way a runner already did with the
[SWE-bench Pro determinacy audit](https://github.com/scaleapi/SWE-bench_Pro-os/issues/108). Two
artifacts in `findings/05_runner_subset.md`:

- **Skip-list (24 programs).** No source-blind, offline solver can resolve these: each ships a graded
  test demanding a recall-only value (a hash, cipher, codec, compressor, opaque binary format) or a
  byte-exact render the contract does not fix. Running a model on them spends build budget on a
  foregone fail.
- **Benchable subset (171 programs).** Report % Resolved over these instead of all 200 tasks, and the
  headline stops conflating reconstruction with recall.

Adopting the list **carries no conflict of interest**, because it has three properties:

1. **Model-blind.** The criterion is read from the *test bodies*, never from which tasks a model failed,
   and is fixed before any model runs. It cannot be reverse-engineered to flatter a score.
2. **Replayable.** Each witness ships a `retrieval_cmd` that re-fetches its exact test; the verdict
   belongs to the check. You do not have to trust us, re-derive it by grep.
3. **Citable.** It is the same fixed list for everyone, so excluding it is a property of the benchmark.

You do not even need to cite this audit to use it: the method is in `METHODOLOGY.md` and the list
re-derives by grep over the public suites, so you can reproduce it yourself. Citing it just saves the
derivation and puts a model-independent reason on the record for reporting a subset.

A separate **grader-caution list (29 programs)** flags suites whose graders write their own golden from
the reference run, so they score byte-identity-to-reference rather than a contract. A golden-presence
check found the goldens bundled (the capture branch is dormant), so the vacuous-pass is a latent risk,
not an active one; treat a pass from these as reference-identity, not correctness.

## What the audit found

ProgramBench asks a model to reconstruct a program from its execute-only binary and documentation, with
no source and no internet, graded one-shot on a hidden suite under a conjunctive metric (% Resolved =
pass every test). Does passing measure source-blind reconstruction, or something else? Three independent
answers:

- **Recall (information barrier), 21 programs.** A graded test asserts the exact output of a non-stdlib
  function, a hash, cipher, codec, compressor, opaque binary format, or the Unicode width table, that no
  offline solver reconstructs. `findings/01_recall_witnesses.md`.
- **Oracle provenance (the grader), 29 programs.** Graded tests build their own golden from the
  reference run, scoring byte-identity-to-reference rather than a contract: the test oracle problem
  ([Barr et al. 2015](https://doi.org/10.1109/TSE.2014.2372785);
  [Weyuker 1982](https://doi.org/10.1093/comjnl/25.4.465)). `findings/02_oracle_provenance.md`.
- **Coverage (complexity barrier), structural.** Hidden plus one-shot plus conjunctive grading makes
  the solver's effective target the whole behavioral surface, whose measured size (median 204 graded
  obligations per program, up to 4,064) collapses the pass rate. Completeness is a bar testing cannot
  certify ([Dijkstra 1970](https://www.cs.utexas.edu/~EWD/transcriptions/EWD02xx/EWD249/EWD249.html)) and
  is undecidable in general ([Rice 1953](https://doi.org/10.1090/S0002-9947-1953-0053041-6)). This
  explains the reported zero floor without any recall. A soft scale tier of 37 large programs the
  coverage barrier rules out is in `findings/05_runner_subset.md`.

A finding for benchmark makers: recall tracks the **kind** of a program's core and its implementation
language's **standard library**, not program size. A small embedder is recall-gated; a large document
converter is not. `chafa` (C, no stdlib image decoder) earns a witness where its sibling
`ascii-image-converter` (Go, `image/png`) stays benchable. Full per-program verdicts in
`findings/04_per_program.md`.

The non-determinism classes one would suspect (concurrency, paths, time, locale, float, ordering) were
checked and found benchable or neutralized by the benchmark's sandbox and flaky-filter, recorded in
`findings/03_class_checks.md` so a runner need not re-check.

## Verify any claim

Everything is in `data/audit.db` (SQLite). Regenerate the human-readable findings with
`python3 scripts/export_findings.py`. Re-derive the spine from scratch with the `scripts/` pipeline
(`litmatch_sweep.py` for the complete exact-output inventory, `capture_sweep.py` for the self-capture
census, `find_render_witnesses.sh` for the render class). See `METHODOLOGY.md` for the transferable
method.

## Status

Scoped to construct validity, not contamination. Corrections to any specific verdict are welcome via
issue; every claim is inspectable from the committed receipts, and the mechanical spine re-derives by
grep without trusting the author. A right-of-reply issue to the ProgramBench authors (draft in
`RIGHT_OF_REPLY_ISSUE.md`) and a Zenodo archive are the next steps.

## License

Network copyleft, both halves. Content (data, findings, docs) under [CC BY-SA-NS](LICENSES/CC-BY-SA-NS.md) (CC BY-SA 4.0 plus a Network Services clause; canonical at [june.kim/cc-by-sa-ns](https://june.kim/cc-by-sa-ns)); code (`scripts/`) under [AGPL-3.0-or-later](LICENSES/AGPL-3.0.txt). See [LICENSE](LICENSE). Put a derivative behind a network service and the corresponding source goes to its users. The audited paper ([arXiv:2605.03546](https://arxiv.org/abs/2605.03546)) is its authors' work, linked not redistributed.
