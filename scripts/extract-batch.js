export const meta = {
  name: 'extract-batch',
  description: 'Disk-safe extractor over a batch of ProgramBench programs; each agent commits candidates to the audit DB on completion (crash-safe).',
  phases: [{ title: 'Extract' }],
}
// args = [{task, program, lang}, ...]  (passed via the Workflow tool `args` field)
const ITEMS = typeof args === 'string' ? JSON.parse(args) : args
const PUT = '/Users/junekim/Documents/june.kim/.pb-audit/put.py'

const r = await parallel(ITEMS.map((it) => () =>
  agent(
    `You are an EXTRACTOR, not a judge. Program: ${it.program}. Task dir: ${it.task}.

GOAL: list EVERY graded test that compares program output EXACTLY (==, byte-equality, against a bundled .golden / fixture / vector / digest / checksum file, read_bytes(), read_text()) OR asserts a specific VALUE produced by a named algorithm. Do NOT decide benchable/unbenchable.

For each such test record so the finding is REPLAYABLE by an independent party (this is mandatory — a finding that cannot be re-fetched is worthless): the branch hash H the test lives in, the test .py file path inside the tarball, the test name, the asserting line(s) verbatim INCLUDING how the expected value is produced (the expected=... line AND any helper that builds the input, e.g. a bundled tool converting a fixture), and the ALGORITHM producing the asserted value, named as specifically as possible (e.g. "brotli decompress", "zstd compress", "xxhash", "blake3", "sha256 (stdlib)", "libjpeg decode", "PNG encode", "PDF render", "GDALChecksumImage", "fasttext embeddings", "help-text constant", "error-message constant", "roundtrip self-consistency", "JSON structure", "coordinate projection math", "x86 codegen"). If output comes from a hash/cipher/codec/compressor/format/render/embedding, name it precisely. If there are NO exact-output/value tests (only substring/returncode/structural), candidates is [].

READ EVERY BRANCH'S TEST .py. Disk-safe — DO NOT write to disk, DO NOT create directories:
  list branches:   curl -s "https://huggingface.co/api/datasets/programbench/ProgramBench-Tests/tree/main/${it.task}/tests?recursive=true"
  filenames:       curl -sL "https://huggingface.co/datasets/programbench/ProgramBench-Tests/resolve/main/${it.task}/tests/$H.tar.gz" | tar tz 2>/dev/null | grep '\\.py$'
  stream bodies:   curl -sL "https://huggingface.co/datasets/programbench/ProgramBench-Tests/resolve/main/${it.task}/tests/$H.tar.gz" | tar xzO --wildcards --no-anchored '*.py' 2>/dev/null
Do not sample: read all branches. If a body is huge, still scan it for assert/golden/digest lines.

FINALLY — this is mandatory, even if candidates is empty — record your result so it is never lost. Pipe ONE single-line JSON object to the recorder (assertions on one line, newlines escaped as \\n):
  python3 ${PUT} <<'PBEOF'
  {"task":"${it.task}","program":"${it.program}","candidates":[{"test":"...","assertion":"...","algorithm":"..."}]}
  PBEOF
The recorder prints "RECORDED: ...". Your returned text should be just that confirmation line.`,
    { label: `x:${it.program}`, model: 'sonnet', phase: 'Extract' }
  ).catch(() => null)
))

log(`extract-batch done: ${ITEMS.length} dispatched, ${r.filter(Boolean).length} returned ok`)
return { dispatched: ITEMS.length, ok: r.filter(Boolean).length }
