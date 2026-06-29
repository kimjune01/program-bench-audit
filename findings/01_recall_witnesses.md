# Recall witnesses (axis 1)

Each row: a graded test whose exact expected value is the output of a function no source-blind, offline solver can reproduce. Re-fetch any via its `retrieval_cmd` in the DB.

| program | witness test | recalled function |
|---|---|---|
| 7zip | `test_scrc_hash_functions_xxh64` | xxhash |
| age | `test_decrypt_existing` | X25519/ChaCha20Poly1305 |
| bedtools2 | `test_bamtobed_t1_one_block_no_split` | solver program receives binary BAM; must decode BGZF (zlib, stdlib) + BAM record layout (refID/pos/CIGAR/flag, NON-stdlib) to emit the BED line |
| blake3 | `test_chunk_boundary_1024_bytes_exact` | blake3 |
| brotli | `test_binary_data_decompression` | brotli |
| chafa | `test_loaders` | image decode (png/webp/avif/tiff) to ANSI; C has no stdlib image decode |
| csview | `test_cjk_emoji_with_padding` | Unicode East Asian Width + emoji-width table to pad CJK/emoji to 2 display columns for table alignment |
| dsq | `test_parquet_type_preservation` | Parquet binary columnar decode of bundled testdata/userdata.parquet |
| duckdb | `test_import_parquet` | Parquet binary decode of bundled fixture |
| elfcat | `test_elf32` | ELF binary format decode; HTML describes ELF header/section bytes |
| fasttext | `test_print_sentence_vectors_basic` | fasttext embeddings |
| gdal | `test_raster_info_checksum` | GDALChecksumImage |
| jp2a | `test_ext_width_default_palette` | libjpeg decode |
| lz4 | `test_advanced_options_golden_decompress` | lz4 decompress of bundled fixture to golden bytes |
| ov | `test_zstd_decompression` | zstd decompress of bundled fixture then render; correct content requires zstd decode |
| parqeye | `test_tui_data_display` | Parquet binary columnar decode; screen content = decoded parquet |
| php-src | `test_phpt_file[gost]` | gost |
| pixterm | `test_webp_format_support` | WebP decode |
| samtools | `test_depth_basic_output_format` | BAM codec |
| sox | `test_lpc10_statistical_properties` | LPC10 codec |
| zstd | `test_golden_decompression` | zstd |
