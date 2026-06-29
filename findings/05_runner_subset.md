# For a benchmark runner: the model-blind subset

This list is computed from the **test bodies**, never from any model's results, so adopting it is not a discretionary call and carries no conflict of interest. Every row is re-derivable by grep over the public suites (each witness ships a `retrieval_cmd` in the DB); you do not have to trust the author.

## Skip-list: exclude from Fully Resolved (24 programs)

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

## Grader-caution: self-capturing oracle (29 programs, 12 vacuous-risk)

The grader writes its own golden from the reference run. Where the golden is bundled it grades byte-identity-to-reference (a weak check, not a contract); where it is absent (the conditional form, marked) it passes any output. Do not trust a pass from these as correct without confirming the golden is present and contractual.

| program | conditional (vacuous-risk) |
|---|---|
| age | yes |
| argc |  |
| bedtools2 |  |
| blake3 |  |
| chafa | yes |
| clog-cli |  |
| dropbear | yes |
| ffmpeg | yes |
| git-trim | yes |
| goimports-reviser | yes |
| gomplate | yes |
| jplot | yes |
| json-tui |  |
| lz4 |  |
| masscan |  |
| mdbook |  |
| pandoc |  |
| pigz |  |
| rumdl |  |
| samtools | yes |
| solar | yes |
| stgit | yes |
| trdsql |  |
| tree-sitter |  |
| typst | yes |
| walk |  |
| xsv |  |
| xz |  |
| zstd |  |

## Benchable subset: report Fully Resolved over these (171 programs)

No witness found and not contestable. This is a floor on the benchable set, not a certificate (the audit is one-sided).

`amber`, `angle-grinder`, `argc`, `ast-grep`, `atlas`, `bartib`, `bat`, `bat`, `bore`, `broot`, `caesium-clt`, `calculator`, `calcurse`, `caps-log`, `chamber`, `cheat`, `chroma`, `clog-cli`, `cmatrix`, `code-minimap`, `codesnap`, `cppcheck`, `crowbook`, `ctags`, `curlie`, `datasurgeon`, `deadnix`, `delta`, `dep-tree`, `diffr`, `dirble`, `direnv`, `dog`, `doxygen`, `dropbear`, `dstask`, `dua-cli`, `duc`, `dupl`, `dust`, `dutree`, `entr`, `errcheck`, `ethabi`, `eureka`, `eva`, `fblog`, `fd`, `felix`, `figlet`, `flamelens`, `fselect`, `fx`, `fzf`, `gdu`, `genact`, `git-graph`, `git-trim`, `gittype`, `go-critic`, `go-mod-outdated`, `goimports-reviser`, `gomplate`, `gotests`, `gowsdl`, `gping`, `grex`, `gromacs`, `gron`, `halite`, `handlr`, `hashcards`, `hck`, `hex`, `hexyl`, `hostctl`, `html-to-markdown`, `htmlq`, `htop`, `hush`, `hwatch`, `hyperfine`, `i3-style`, `igrep`, `jot`, `jplot`, `jq`, `json-tui`, `jsonschema`, `keifu`, `kiro-editor`, `lazygit`, `lightningcss`, `lnav`, `loop`, `lua`, `marmite`, `masscan`, `mdbook`, `melody`, `miller`, `miniserve`, `monolith`, `muffet`, `ngrrram`, `ninja`, `nnn`, `nomino`, `nsh`, `oha`, `onefetch`, `oranda`, `pandoc`, `parallel-disk-usage`, `pastel`, `peco`, `pier`, `pigz`, `pingu`, `pls`, `pueue`, `quinn`, `revive`, `rhit`, `richgo`, `ripgrep`, `ripsecrets`, `rnr`, `rumdl`, `run`, `rust-sloth`, `rustowl`, `scc`, `sd`, `seqtk`, `serpl`, `shellharden`, `skeema`, `solar`, `sqlite`, `srgn`, `statix`, `stgit`, `svd2rust`, `svgbob`, `tailspin`, `tex-fmt`, `the_silver_searcher`, `thokr`, `tig`, `tokei`, `tparse`, `trdsql`, `tree-sitter`, `treemd`, `tty-clock`, `tuc`, `tui-journal`, `walk`, `wrapcheck`, `xcp`, `xh`, `xplr`, `xq`, `xsv`, `xz`, `yj`, `yq`, `zip-password-finder`, `zk`, `zoxide`

Contestable, held out of both pending inspection: `ascii-image-converter`, `luajit`, `pipr`, `proj`, `quickjs`, `tinycc`.
