# How to audit a benchmark's construct validity

The transferable method behind this audit. Written so a future audit (of ProgramBench or another
benchmark) can reuse it without rediscovering the traps.

## The question

Construct validity: does passing the benchmark measure the skill it claims? For a reconstruction
benchmark, the skill is source-blind reconstruction; the threat is that passing actually rewards
**recall** of memorized algorithms, or **byte-identity to a reference** that is not a contract. You
prove the threat with **witnesses**: a single graded test that a correct-but-source-blind solver
cannot pass. Under a conjunctive metric (pass-all-tests), one witness per program forecloses the task,
so the witness is the unit and the search is one-sided: a witness proves unbenchable; absence of a
found witness proves nothing.

## Verifiable knowledge, not assertion

Every finding must be a **replayable receipt**, not a judgment. A witness ships with the command that
re-fetches the exact test body, and its verdict is re-derivable by anyone who runs that command. Store
the coordinates (task, branch hash, file, line, verbatim assertion) in a database, not prose. "I read
it and it's recall" is worth nothing; "here is the assertion, here is the retrieval command, check the
roots yourself" is the deliverable. This is the difference between a number someone has to trust and a
number they can re-run.

## Read everything, not a sample

The first version of this audit used subagents to surface candidate tests, which produced a **lossy
5% sample** (the agents under-reported). The fix: a deterministic regex over **every** assertion in
**every** test body, classifying each as a literal/exact-output match (recall-eligible) or benchable
by construction (substring, return code, length, membership, `!= `, `== <int>`). The exact-output set
is the complete denominator; recall witnesses are a subset of it. The complete read caught a program
(`lz4`) the sampled read had mislabeled benchable. **Subagents are reliable extractors and unreliable
judges**: they invent escape reasons ("input is fixed, hardcode it"; "pre-compute the hash"; "both
files are bundled"). Let them extract coordinates; you adjudicate.

## The adjudication criterion (recall)

A graded test is recall-only when its exact expected value is the output of a function that is:
(a) **not in the offline standard library for some allowed language**, and (b) **not learnable from
finite input-output probing**, and (c) **not a derivable structured transform** (codegen,
language-semantics output, coordinate math are derivable, not recall). The decisive, mechanical line
is **per-language stdlib**: Python's stdlib has `zlib/gzip/bz2/lzma`, so gzip/bz2/xz are benchable, but
`zstd/lz4/brotli` are absent so they are recall; Go's stdlib has `image/jpeg`, so a Go image tool is
benchable where the same task in C (no stdlib image) is recall. Always check the program's actual
language. Invalid escapes to reject: "fixed input so hardcode" (the solver never sees the hidden
tests), "public/well-known algorithm" (public knowledge in weights *is* the recall channel offline).

## Confirm contestable classes by search before promoting

A conceptually-strong class is not a witness until a golden confirms it. The Unicode-width class looked
like six clean witnesses on the argument ("no finite sample recovers a width table"); reading the
goldens, **only one held up** (`csview`, which pads CJK/emoji into aligned columns and needs the
table), while the others passed with the standard library (single-codepoint char cutting, ASCII-width
truncation). Fetch the golden, find the discriminator, and let it narrow the class. Promoting on the
argument alone would have been five-sixths wrong. Keep a labeled **contestable tier** for what you
cannot confirm; never fold it into the floor to inflate the number.

## Two axes, separate as proofs, unified as cause

This benchmark had two independent failure modes; keep them separate so refuting one does not refute
both, but name the single root cause.

- **Recall** (property of the program): the behavior cannot be reconstructed offline.
- **Oracle provenance** (property of the grader): the golden is the reference's own captured output, so
  the test grades byte-identity-to-reference, not a contract. This is the **test oracle problem**
  (Barr et al. 2015); a reference used as its own oracle is a pseudo-oracle for a **non-testable
  program** (Weyuker 1982). Sub-cases: implementation-pinned exact render bytes (PDF/PNG/framemd5),
  and the smoking-gun **self-capturing golden** (`if not golden.exists(): golden.write_text(...)`).

Root cause of both: **with the source and a specification withheld, the reference implementation is
pressed into service as the contract.** Recall is information the solver lacks; provenance is authority
the contract lacks.

## "Benchable for one behavior" is not "program benchable"

Under a conjunctive metric, benchable means **no unbenchable test anywhere in the suite**. A stdlib
shortcut that reproduces one sub-behavior (Python `sqlite3` reads a `.db`) does not make the program
benchable. This is the per-test method's **blind spot**: a program whose every test is individually
benchable (documented SQL semantics) but whose full behavior is infeasible to reconstruct from
black-box probing plus `--help` (a whole SQL engine) is unbenchable **by scale** and earns no per-test
witness. Name this class qualitatively; do not pretend a per-test audit covers it.

## Non-determinism classes are usually neutralized; check, then record the negative

The obvious "isn't this just non-determinism?" objection (concurrency, paths, time, randomness, locale,
ordering, float, parser errors) mostly does **not** yield witnesses, because a well-built benchmark
neutralizes them: a shared sandbox makes `$HOME`-derived paths reproduce, a flaky-filter drops
tests the reference itself fails on rerun, and the suite tests deterministic projections (a parallel
copier is checked on copied-content equality, not interleaving) instead of pinning races. Checking
these and **recording the negatives** is a service to whoever runs the benchmark, and it pre-empts the
objection that your floor is confounded by sloppy non-determinism.

## Operational

- **Disk-safe extraction**: stream `.py` test bodies to stdout, never save tarballs/assets (a prior
  run filled 19 GB extracting full tarballs). `curl -sL <url>/$H.tar.gz | tar xzO --wildcards
  --no-anchored '*.py'`, or download one tarball, extract the one member, delete it.
- **Commit per item**: each agent/sweep writes its result to the DB on completion, so a kill loses one
  in-flight item, never the batch, and reruns skip what is done.
- **Precise signatures**: glob substrings lie (`*.tar*` matches "started"). Anchor extensions and
  read the actual assertion before believing a census count.
- **External model as sparring, not arbiter**: a second model (here, codex/GPT-5.5) is good for naming
  the root cause and finding taxonomy blind spots, but separate its real errors from its
  tentativeness-preference; it wanted to cut bold-but-correct claims and soften a fair, falsifiable
  process critique. Keep what is right, reject what is timid.
