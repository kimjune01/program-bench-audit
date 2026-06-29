<!-- Paste into a new issue on the ProgramBench repo (facebookresearch/ProgramBench).
     Title suggestion: "Construct-validity audit: a model-blind benchable subset (right of reply offered)" -->

Thanks for building a source-blind reconstruction benchmark. The no-internet, no-install sandbox and the execute-only binary are a real contribution, and this audit takes the construction seriously rather than looking for contamination. It is scoped to **construct validity**: does the primary Fully Resolved metric measure source-blind reconstruction, or something else? It is not a contamination audit.

I read all 201 hidden test suites from the public `programbench/ProgramBench-Tests` and classified every exact-output assertion. Three independent findings, each with committed, re-fetchable receipts:

- **Recall, ≥21 programs.** A graded test asserts the exact output of a function no source-blind, offline solver can reconstruct: non-stdlib hashes (BLAKE3, GOST, xxHash), ciphers (age), compressors (zstd, brotli, lz4), codecs (LPC10, WebP/libjpeg in C), opaque binary formats (BAM, Parquet, Avro, ELF), embeddings (fastText), the Unicode width table. The value's only offline channel is prior possession of the spec, which the no-internet rule forbids and the system prompt tries to suppress. Because Fully Resolved is conjunctive, one such test forecloses the task.
- **Oracle provenance, ≥29 programs.** Graded tests build their own golden from the reference run (`if not golden.exists(): golden.write_text(result.stdout)` then `assert result.stdout == golden.read_text()`). The oracle is then the reference's own output, so the test grades byte-identity-to-reference rather than a contract; 12 are in a conditional form that passes any output if the golden is absent. This is the test oracle problem (Barr et al. 2015; Weyuker 1982).
- **Coverage.** Hidden + one-shot + conjunctive grading makes the solver's effective target the whole behavioral surface, not the finite suite. The surface is measurable from your own tests: a median of 204 distinct graded exact-output obligations per program, up to 4,064 (gdal). The reported zero Fully Resolved falls out of that surface size under a conjunction, with no appeal to a missing algorithm.

For anyone running the benchmark, the audit ships a **model-blind subset**: a 24-program skip-list (no source-blind solver resolves these) and a 171-program benchable subset to report Fully Resolved over. The list is computed from the test bodies, never from any model's results, so adopting it carries no conflict of interest, and every verdict is re-derivable by grep over the public suites without trusting me.

Repo with the database, per-program receipts, and the re-runnable pipeline: <REPO URL>. Companion write-up: https://june.kim/the-unreasonable-largeness-of-behavior

**Right of reply.** If the team disputes any specific verdict, I will incorporate corrections and cut a new versioned release. The mechanical spine (the literal-match inventory and the witness retrieval commands) is re-derivable by grep, so corrections can be checked against the suites rather than against my word.

Archived for citation at Zenodo: <CONCEPT DOI> (concept, all versions), <v1.0.0 DOI>. <!-- fill after archiving -->
