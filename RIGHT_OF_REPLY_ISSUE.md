<!-- Paste into a new issue on the ProgramBench repo (facebookresearch/ProgramBench).
     Title suggestion: "Construct-validity audit: a model-blind benchable subset (right of reply offered)" -->

Thanks for building this. The no-internet, no-install sandbox and the execute-only binary are a real contribution, and I went in trying to take the construction seriously. My question is a narrow one: does the primary % Resolved metric measure source-blind reconstruction the way the paper frames it, or something else? So this is a construct-validity question. I'm not alleging contamination.

I had a coding agent read all 201 released test directories (your 200 tasks plus one empty placeholder) from the public programbench/ProgramBench-Tests, and classify every exact-output assertion by how a source-blind, offline solver could actually get the value it checks. I adjudicated each verdict, and every one comes with a receipt you can re-fetch and check yourself. Three things fell out.

The first is recall, in at least 21 programs. Some graded tests want the exact output of a function no source-blind solver can reconstruct from running the binary: non-stdlib hashes like BLAKE3, GOST and xxHash, ciphers like age, compressors like zstd, brotli and lz4, codecs like LPC10 and WebP/libjpeg in C, opaque binary formats like BAM, Parquet, Avro and ELF, fastText embeddings, the Unicode width table. The only offline route to that value is already holding the spec, which is what the no-internet rule forbids and the prompt tries to suppress. And since % Resolved is conjunctive, one such test forecloses the whole task.

The second is oracle provenance, in at least 29 programs. These graders write their own golden from the reference run: if the golden file doesn't exist they save result.stdout into it, then assert that stdout equals it. So the oracle becomes the reference's own bytes, and the test checks identity to the reference where a contract is what we'd want. Twelve of them use the conditional form that would pass any output at all if the golden were ever stripped; I checked, and the goldens do ship, so that one is latent rather than live. This is the classic test oracle problem (Barr et al. 2015; Weyuker 1982).

The third is coverage. Even setting recall aside, the hidden, one-shot, conjunctive setup makes the solver's real target the whole behavioral surface, well beyond the finite suite, and that surface is measurable from your own tests: a median of 204 distinct graded exact-output obligations per program, up to 4,064 for gdal. A zero % Resolved floor falls right out of a surface that size under a conjunction, with no missing-algorithm story needed.

So here's what I'd ask, easiest first.

First, spot-check a few of the receipts and tell me where I'm wrong. Every recall witness re-fetches its exact test in one command (the retrieval_cmd in the repo), so if a verdict doesn't hold, I'll correct it and cut a new release. I'd rather be checked than believed.

Second, consider reporting % Resolved over the benchable subset, or alongside the full set. I have a model-blind list of 171 benchable programs, with the 24 recall-gated and render-pinned ones set aside and 6 more held back as contestable. It's computed from the test bodies, never from any model's results, so pointing to it commits you to nothing about any particular model, and a runner can re-derive it by grep without trusting me.

Third, I'd treat the recall tasks as a construct mismatch. The tests aren't broken; they measure a real skill, implementing a known algorithm or format from memory. That's a different thing from the source-blind reconstruction % Resolved claims to measure. A separate knowledge track, or shipping the spec, would capture it honestly, and the self-capturing graders and byte-exact renders have local fixes. The repo also carries a five-class triage rule meant to run at your suite's scale.

You don't have to trust any of this. The database, the per-program receipts, and the re-runnable pipeline are at https://github.com/kimjune01/program-bench-audit, archived at Zenodo (10.5281/zenodo.21083756). The full write-up is at https://june.kim/programbench-measures-recall. Dispute any verdict and I'll fix it and re-release; the spine re-derives by grep, so a correction checks against the suites, not against my word.
