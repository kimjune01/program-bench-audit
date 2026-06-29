# Classes of concern checked (mostly benchable / neutralized)

The benchmark's sandbox + flaky-filter + deterministic-projection testing neutralize the environment and non-determinism classes. Recorded so a runner need not re-check.

| class | verdict | why |
|---|---|---|
| archive-bit-exact | absent | no tar/zip/cpio/ar tools in the 201; precise grep found only substring noise (".tar" inside "started") |
| concurrency | benchable | suites assert deterministic projections, not interleavings: pueue queries a quiesced queue state; hyperfine asserts the fixed setup/prepare/benchmark/conclude hook order; xcp checks copied-content equality. Hard concurrent behavior is under-tested, not pinned. |
| dir-hashmap-order | benchable | tools sort output (fd: output_sorted==expected) or use defined ordering (sqlite ORDER BY); enumeration-order-dependent output would be removed by the flaky-filter |
| env-host-path | benchable | shared sandbox (HOME=/root, fixed workdir) reproduces $HOME-derived paths (lazygit -> /root/.config/lazygit), fixture paths (direnv,gomplate), and log-content hostnames (lnav) identically for solver and reference |
| float-formatting | benchable | asserted floats are basic arithmetic, constants (3.14159), and correctly-rounded functions (sqrt) — all reproducible cross-platform; no transcendental last-ULP or SIMD-reduction witness surfaced |
| locale-collation | benchable | sqlite COLLATE tests use documented built-ins (BINARY/NOCASE/RTRIM), derivable; no non-stdlib ICU collation table asserted |
| parser-error-text | benchable | exact diagnostic wording (json-tui nlohmann parse_error.101, pandoc JSON errors) is an observable constant: the solver probes the reference with malformed input, reads the error format, replicates it |
| time-random-uuid | benchable-or-filtered | non-deterministic-on-rerun output is removed by the benchmark flaky-filter (discards tests the reference itself fails); pure now()/uuid/random tests do not survive into the graded suite |
| whole-program-scale | UNBENCHABLE-but-not-per-test-witnessable | programs whose every test is individually benchable (documented semantics) but whose full behavior is infeasible to reconstruct from black-box probing + docs (sqlite SQL engine, a full database/compiler). The per-test witness method misses these; they are unbenchable by SCALE = the paper title thesis. Soft to make mechanical (no line on too-large), so kept as the qualitative argument, not a Table A2 row. |
