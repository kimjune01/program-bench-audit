export const meta = {
  name: 'verify-witnesses',
  description: 'Re-fetch each of the 15 hypothesis witnesses and record replayable facts (no verdict) to the witness ledger.',
  phases: [{ title: 'Verify' }],
}
const PUT = '/Users/junekim/Documents/june.kim/.pb-audit/put_witness.py'
const ITEMS = [
 {program:'7zip',task:'ip7z__7zip.839151e',lang:'cpp',test:'test_scrc_hash_functions_xxh64',alg:'xxhash'},
 {program:'age',task:'filosottile__age.706dfc1',lang:'go',test:'test_decrypt_existing',alg:'X25519/ChaCha20Poly1305/scrypt'},
 {program:'blake3',task:'blake3-team__blake3.15e83a5',lang:'rs',test:'test_chunk_boundary_1024_bytes_exact',alg:'blake3'},
 {program:'brotli',task:'google__brotli.b3dc9cc',lang:'c',test:'test_binary_data_decompression',alg:'brotli'},
 {program:'ditaa',task:'stathissideris__ditaa.f2286c4',lang:'java',test:'test_no_shadows_flag_accepted',alg:'PNG render'},
 {program:'fasttext',task:'facebookresearch__fasttext.1142dc4',lang:'cpp',test:'test_print_sentence_vectors_basic',alg:'fasttext embeddings'},
 {program:'ffmpeg',task:'ffmpeg__ffmpeg.360a402',lang:'c',test:'test_subtitle_to_video_conversion_basic',alg:'libass/framemd5'},
 {program:'gdal',task:'osgeo__gdal.0847f12',lang:'cpp',test:'test_raster_info_checksum',alg:'GDALChecksumImage'},
 {program:'jp2a',task:'cslarsen__jp2a.61d205f',lang:'c',test:'test_ext_width_default_palette',alg:'libjpeg decode'},
 {program:'php-src',task:'php__php-src.c891263',lang:'c',test:'test_phpt_file[gost]',alg:'gost'},
 {program:'pixterm',task:'eliukblau__pixterm.1a93fd5',lang:'go',test:'test_webp_format_support',alg:'WebP decode'},
 {program:'samtools',task:'samtools__samtools.aa823b5',lang:'c',test:'test_depth_basic_output_format',alg:'BAM codec'},
 {program:'sox',task:'chirlu__sox.42b3557',lang:'c',test:'test_lpc10_statistical_properties',alg:'LPC10 codec'},
 {program:'typst',task:'typst__typst.88356d0',lang:'rs',test:'test_emphasis_basic',alg:'PDF render'},
 {program:'zstd',task:'facebook__zstd.1168da0',lang:'c',test:'test_golden_decompression',alg:'zstd'},
]
const r = await parallel(ITEMS.map((it) => () =>
  agent(
    `You re-fetch ONE test and report REPLAYABLE FACTS so an independent party can re-derive them. Do NOT judge benchable/unbenchable. Program ${it.program} (${it.lang}), task ${it.task}, witness test "${it.test}" (claimed algorithm: ${it.alg}).

Find that test's body and report, exactly as it is:
1. branch_hash H (the tests/<H>.tar.gz the test lives in)
2. test_file (path inside the tarball)
3. assertion: the verbatim assert line(s) AND the lines that build the expected value (e.g. expected = "...", a .golden read, or a bundled tool/helper that produces the input). Quote them; do not paraphrase.
4. input_prov: trace how the GRADED INPUT reaches the solver's program — is it a bundled binary blob, a text fixture, or produced at test time by a bundled helper tool? Name the file(s) and any converter.
5. Whether expected is a small hardcoded value, a golden file (give its name/size if visible), or computed.

DISK-SAFE — DO NOT write to disk or make dirs:
  hashes:  curl -s "https://huggingface.co/api/datasets/programbench/ProgramBench-Tests/tree/main/${it.task}/tests?recursive=true"
  files:   curl -sL "https://huggingface.co/datasets/programbench/ProgramBench-Tests/resolve/main/${it.task}/tests/$H.tar.gz" | tar tz 2>/dev/null | grep '\\.py$'
  body:    curl -sL "https://huggingface.co/datasets/programbench/ProgramBench-Tests/resolve/main/${it.task}/tests/$H.tar.gz" | tar xzO --wildcards --no-anchored '*<file>*' 2>/dev/null
If a tarball is large, you may curl it to a single file under /tmp, tar -O the one member, then rm it. Find the test by grepping streamed .py for "${it.test}".

FINALLY record facts (mandatory). Pipe ONE single-line JSON (escape newlines as \\n):
  python3 ${PUT} <<'PBEOF'
  {"program":"${it.program}","test_name":"${it.test}","task":"${it.task}","branch_hash":"H","test_file":"path","assertion":"verbatim expected + assert + builder lines","input_prov":"how the graded input reaches the solver","algorithm":"${it.alg}","retrieval_cmd":"curl -sL .../H.tar.gz | tar xzO <file>"}
  PBEOF
Return just the "RECORDED:" line.`,
    { label: `v:${it.program}`, model: 'sonnet', phase: 'Verify' }
  ).catch(() => null)
))
log(`verify-witnesses done: ${r.filter(Boolean).length}/${ITEMS.length} returned ok`)
return { ok: r.filter(Boolean).length }
