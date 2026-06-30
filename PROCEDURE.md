# Reproducing the audit

This reproduces every verdict in `data/audit.db` and `findings/` from the public test suites, using
nothing but the published data. `METHODOLOGY.md` is the transferable method; this file is the exact
steps.

## Prerequisites

- Python 3, SQLite, `curl`, `tar` (the scripts fetch from Hugging Face over plain HTTP, no auth).
- Node is optional, for `scripts/extract-batch.js` and `scripts/verify-witnesses.js`.
- The dataset under audit: [`programbench/ProgramBench-Tests`](https://huggingface.co/datasets/programbench/ProgramBench-Tests),
  201 released test directories (the benchmark's 200 tasks plus one empty placeholder).

## Verify a single claim (no setup)

Every recall witness ships a `retrieval_cmd` that re-fetches its exact test from the public dataset:

```bash
sqlite3 data/audit.db "SELECT program, test_name, retrieval_cmd FROM witnesses WHERE status='verified'"
# run any retrieval_cmd, e.g. for bedtools2:
curl -sL https://huggingface.co/datasets/programbench/ProgramBench-Tests/resolve/main/arq5x__bedtools2.dd57059/tests/b0846e00e790.tar.gz \
  | tar xzO eval/tests/test_harvest_bam_bed_conversions.py
```

The printed test body contains the cited assertion: a byte-exact comparison against a bundled golden
the reference algorithm produced. The verdict *is* that assertion. You do not have to trust the
database, the author, or the model that read it.

## Rebuild from scratch

1. **Inventory every exact-output assertion.** `python3 scripts/litmatch_sweep.py` reads all released
   suites and splits each assertion into the recall-eligible set (byte-exact output comparisons,
   135,740 lines) and the benchable rest (substring, return code, length, membership). A deterministic
   regex, not an LLM.
2. **Self-capture census.** `python3 scripts/capture_sweep.py` flags graded tests that write their own
   golden from the reference run (`if not golden.exists(): golden.write_text(result.stdout)`).
3. **Render witnesses.** `bash scripts/find_render_witnesses.sh` finds byte-exact comparisons against a
   rendered artifact (PNG, PDF, per-frame hash).
4. **Adjudicate.** The author reads each candidate assertion and records a verdict with
   `scripts/put_witness.py`; the model proposes, the author decides (see LLM use, below).
5. **Export findings.** `python3 scripts/export_findings.py` regenerates `findings/*.md` from the DB.

The search is one-sided: a witness proves a program unbenchable; "no witness found" is the absence of a
surfaced witness, not a clearance.

## What is canonical

`data/audit.db` (SQLite) is the source of truth. `findings/` is generated from it by
`export_findings.py`; never hand-edit a findings file. Every recall verdict traces to a cited assertion
re-fetchable by its `retrieval_cmd`.

## LLM use

A large language model (Claude, Anthropic) read the public test suites and proposed a classification for
each graded assertion. The author adjudicated every verdict. Each is a re-fetchable receipt, the cited
test and the bundled golden it checks, re-derivable by grep over the public suites with no trust in the
model or the author (see "Verify a single claim"). The scripts and the companion paper's prose were
written with model assistance under the author's editing. The model's contribution is extraction and
drafting; the warrant for every verdict is the re-derivable receipt, not the model's output. Notably,
the inventory step that anchors the floor is a deterministic regex, run without a model at all.
