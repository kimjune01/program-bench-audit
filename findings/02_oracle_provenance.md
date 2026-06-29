# Oracle provenance (axis 2): the golden is the reference's own output

The test oracle problem (Barr et al. 2015; Weyuker 1982): a reference used as its own oracle grades byte-identity-to-reference, not a contract.

## Implementation-pinned (exact render bytes)

| program | witness test | pinned artifact |
|---|---|---|
| ditaa | `test_no_shadows_flag_accepted` | PNG render |
| ffmpeg | `test_subtitle_to_video_conversion_basic` | libass/framemd5 |
| typst | `test_emphasis_basic` | PDF render |

## Self-capturing goldens (graded tests that write their own answer key)

`if not golden.exists(): golden.write_text(result.stdout)` then `assert result.stdout == golden.read_text()`. Conditional form passes any output if the golden is absent.

| program | capture lines | conditional (vacuous-risk) |
|---|---|---|
| lz4 | 109 |  |
| xz | 52 |  |
| solar | 38 | yes |
| pigz | 20 |  |
| clog-cli | 12 |  |
| blake3 | 10 |  |
| git-trim | 9 | yes |
| chafa | 7 | yes |
| dropbear | 7 | yes |
| trdsql | 6 |  |
| pandoc | 5 |  |
| ffmpeg | 4 | yes |
| samtools | 4 | yes |
| json-tui | 3 |  |
| zstd | 3 |  |
| typst | 3 | yes |
| bedtools2 | 2 |  |
| jplot | 2 | yes |
| walk | 1 |  |
| xsv | 1 |  |
| age | 1 | yes |
| gomplate | 1 | yes |
| goimports-reviser | 1 | yes |
| masscan | 1 |  |
| mdbook | 1 |  |
| rumdl | 1 |  |
| argc | 1 |  |
| stgit | 1 | yes |
| tree-sitter | 1 |  |
