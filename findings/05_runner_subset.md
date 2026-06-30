# For a benchmark runner: the model-blind subset

This list is computed from the **test bodies**, never from any model's results, so adopting it is not a discretionary call and carries no conflict of interest. Every row is re-derivable by grep over the public suites (each witness ships a `retrieval_cmd` in the DB); you do not have to trust the author.

## Skip-list: exclude from % Resolved (24 programs)

No source-blind, offline solver can resolve these (a recall-only test, or a byte-exact render the contract does not fix). Running a model on them spends build budget on a foregone fail; excluding them stops the headline conflating reconstruction with recall.

| program | reason |
|---|---|
| 7zip | recall |
| age | recall |
| bedtools2 | recall |
| blake3 | recall |
| brotli | recall |
| chafa | recall |
| csview | recall |
| ditaa | brittle_render |
| dsq | recall |
| duckdb | recall |
| elfcat | recall |
| fasttext | recall |
| ffmpeg | brittle_render |
| gdal | recall |
| jp2a | recall |
| lz4 | recall |
| ov | recall |
| parqeye | recall |
| php-src | recall |
| pixterm | recall |
| samtools | recall |
| sox | recall |
| typst | bundled_font_data |
| zstd | recall |

## Grader-caution: self-capturing oracle (29 programs)

The grader writes its own golden from the reference run, so it grades byte-identity-to-reference (a weak oracle, not a contract). A golden-presence audit found 26 confirmed dormant (the golden is bundled, so the conditional `if not exists` branch never fires) and **none confirmed vacuous**: the vacuous pass is a latent risk, not an active one. Treat a pass from these as reference-identity at best, not correctness.

| program | golden | conditional form |
|---|---|---|
| age | dormant | yes |
| argc | dormant |  |
| bedtools2 | dormant |  |
| blake3 | dormant |  |
| chafa | dormant | yes |
| clog-cli | dormant |  |
| dropbear | dormant | yes |
| ffmpeg | dormant | yes |
| git-trim | dormant | yes |
| goimports-reviser | dormant | yes |
| gomplate | dormant | yes |
| jplot | dormant | yes |
| json-tui | dormant |  |
| lz4 | dormant |  |
| masscan | dormant |  |
| mdbook | inconclusive |  |
| pandoc | dormant |  |
| pigz | dormant |  |
| rumdl | inconclusive |  |
| samtools | dormant | yes |
| solar | dormant | yes |
| stgit | dormant | yes |
| trdsql | dormant |  |
| tree-sitter | dormant |  |
| typst | dormant | yes |
| walk | dormant |  |
| xsv | inconclusive |  |
| xz | dormant |  |
| zstd | dormant |  |

## Scale tier: unbenchable by coverage (38 programs beyond the skip-list)

Soft tier, still model-blind and re-derivable but threshold-dependent. Blast radius > 458 distinct exact-output obligations, where the conjunctive pass rate q^N falls below 1% even at a charitable q=0.99. Not a per-test witness; a coverage argument, anchored by the benchmark's reported zero % Resolved. A runner may also skip these.

| program | blast radius (distinct obligations) |
|---|---|
| pandoc | 2746 |
| quickjs | 2263 |
| miller | 1788 |
| gomplate | 1366 |
| yq | 1264 |
| lightningcss | 1250 |
| jq | 1189 |
| sqlite | 1171 |
| treemd | 1156 |
| fselect | 1032 |
| argc | 1016 |
| srgn | 1008 |
| solar | 796 |
| luajit | 776 |
| fzf | 771 |
| run | 768 |
| trdsql | 763 |
| tinycc | 700 |
| lua | 687 |
| rumdl | 682 |
| xcp | 656 |
| fx | 650 |
| hush | 625 |
| bat | 605 |
| bat | 605 |
| tuc | 594 |
| lnav | 579 |
| nsh | 568 |
| ripgrep | 545 |
| angle-grinder | 537 |
| sd | 536 |
| jsonschema | 530 |
| ninja | 514 |
| melody | 508 |
| hck | 502 |
| amber | 496 |
| stgit | 495 |
| chamber | 470 |

## Benchable subset: report % Resolved over these (171 programs)

No witness found and not contestable. This is a floor on the benchable set, not a certificate (the audit is one-sided).

`amber`, `angle-grinder`, `argc`, `ast-grep`, `atlas`, `bartib`, `bat`, `bat`, `bore`, `broot`, `caesium-clt`, `calculator`, `calcurse`, `caps-log`, `chamber`, `cheat`, `chroma`, `clog-cli`, `cmatrix`, `code-minimap`, `codesnap`, `cppcheck`, `crowbook`, `ctags`, `curlie`, `datasurgeon`, `deadnix`, `delta`, `dep-tree`, `diffr`, `dirble`, `direnv`, `dog`, `doxygen`, `dropbear`, `dstask`, `dua-cli`, `duc`, `dupl`, `dust`, `dutree`, `entr`, `errcheck`, `ethabi`, `eureka`, `eva`, `fblog`, `fd`, `felix`, `figlet`, `flamelens`, `fselect`, `fx`, `fzf`, `gdu`, `genact`, `git-graph`, `git-trim`, `gittype`, `go-critic`, `go-mod-outdated`, `goimports-reviser`, `gomplate`, `gotests`, `gowsdl`, `gping`, `grex`, `gromacs`, `gron`, `halite`, `handlr`, `hashcards`, `hck`, `hex`, `hexyl`, `hostctl`, `html-to-markdown`, `htmlq`, `htop`, `hush`, `hwatch`, `hyperfine`, `i3-style`, `igrep`, `jot`, `jplot`, `jq`, `json-tui`, `jsonschema`, `keifu`, `kiro-editor`, `lazygit`, `lightningcss`, `lnav`, `loop`, `lua`, `marmite`, `masscan`, `mdbook`, `melody`, `miller`, `miniserve`, `monolith`, `muffet`, `ngrrram`, `ninja`, `nnn`, `nomino`, `nsh`, `oha`, `onefetch`, `oranda`, `pandoc`, `parallel-disk-usage`, `pastel`, `peco`, `pier`, `pigz`, `pingu`, `pls`, `pueue`, `quinn`, `revive`, `rhit`, `richgo`, `ripgrep`, `ripsecrets`, `rnr`, `rumdl`, `run`, `rust-sloth`, `rustowl`, `scc`, `sd`, `seqtk`, `serpl`, `shellharden`, `skeema`, `solar`, `sqlite`, `srgn`, `statix`, `stgit`, `svd2rust`, `svgbob`, `tailspin`, `tex-fmt`, `the_silver_searcher`, `thokr`, `tig`, `tokei`, `tparse`, `trdsql`, `tree-sitter`, `treemd`, `tty-clock`, `tuc`, `tui-journal`, `walk`, `wrapcheck`, `xcp`, `xh`, `xplr`, `xq`, `xsv`, `xz`, `yj`, `yq`, `zip-password-finder`, `zk`, `zoxide`

Contestable, held out of both pending inspection: `ascii-image-converter`, `luajit`, `pipr`, `proj`, `quickjs`, `tinycc`.
