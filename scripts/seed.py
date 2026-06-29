#!/usr/bin/env python3
"""Seed the ProgramBench benchability audit DB. Idempotent: safe to re-run."""
import json, sqlite3, os

DB = os.path.join(os.path.dirname(__file__), "audit.db")
ALL201 = "/tmp/all201.json"

con = sqlite3.connect(DB)
con.execute("PRAGMA journal_mode=WAL")  # crash-safe incremental writes
con.executescript("""
CREATE TABLE IF NOT EXISTS programs (
  task      TEXT PRIMARY KEY,
  program   TEXT,
  repo      TEXT,
  commit_sha TEXT,
  lang      TEXT,
  -- audit lifecycle for the program as a whole
  status    TEXT NOT NULL DEFAULT 'unconfirmed',  -- settled_recall|settled_benchable|contestable|unconfirmed
  extracted INTEGER NOT NULL DEFAULT 0,           -- 1 once an extractor agent has read its full suite
  prior_signal TEXT                                -- prior (unreliable) subagent verdict, for reference only
);
CREATE TABLE IF NOT EXISTS tests (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  program   TEXT NOT NULL,
  test_name TEXT,
  assertion TEXT,        -- verbatim asserting line(s)
  algorithm TEXT,        -- the value-producing algorithm, named
  -- MY adjudication (subagents never write this): unbenchable|benchable|no_witness_found|pending
  adjudication TEXT NOT NULL DEFAULT 'pending',
  is_witness INTEGER NOT NULL DEFAULT 0,  -- 1 = proves the program recall-only
  source    TEXT,        -- which run/agent surfaced it
  notes     TEXT,
  UNIQUE(program, test_name, assertion)
);
""")

# 1. seed all 201 programs
progs = json.load(open(ALL201))
for p in progs:
    con.execute(
        "INSERT OR IGNORE INTO programs(task,program,repo,commit_sha,lang) VALUES(?,?,?,?,?)",
        (p["task"], p["program"], p["repo"], p["commit"], p["lang"]))

# 2. the 15 settled recall witnesses (hand-adjudicated; each a real surfaced witness)
RECALL = [
 ("blake3",  "test_chunk_boundary_1024_bytes_exact", "b3sum output == golden",   "blake3"),
 ("php-src", "test_phpt_file[gost]",                  "GOST hash digest",          "gost"),
 ("7zip",    "test_scrc_hash_functions_xxh64",        "XXH64 digest",              "xxhash"),
 ("age",     "test_decrypt_existing",                 "decrypt of bundled ciphertext", "X25519/ChaCha20Poly1305/scrypt"),
 ("brotli",  "test_binary_data_decompression",        "decompressed bytes == golden", "brotli"),
 ("zstd",    "test_golden_decompression",             "decompressed bytes == golden", "zstd"),
 ("ffmpeg",  "test_subtitle_to_video_conversion_basic","framemd5 == golden",       "libass/framemd5"),
 ("sox",     "test_lpc10_statistical_properties",     "LPC10 stats",               "LPC10 codec"),
 ("jp2a",    "test_ext_width_default_palette",        "ascii from jpeg == golden", "libjpeg decode"),
 ("pixterm", "test_webp_format_support",              "webp decode output",        "WebP decode"),
 ("ditaa",   "test_no_shadows_flag_accepted",         "PNG bytes == golden",       "PNG render"),
 ("typst",   "test_emphasis_basic",                   "PDF bytes == golden",       "PDF render"),
 ("fasttext","test_print_sentence_vectors_basic",     "sentence vectors == golden","fasttext embeddings"),
 ("gdal",    "test_raster_info_checksum",             "GDALChecksumImage value",   "GDALChecksumImage"),
 ("samtools","test_depth_basic_output_format",        "BAM depth output == golden","BAM codec"),
]
for prog, test, asrt, algo in RECALL:
    con.execute("UPDATE programs SET status='settled_recall', extracted=1 WHERE program=?", (prog,))
    con.execute("""INSERT OR IGNORE INTO tests(program,test_name,assertion,algorithm,adjudication,is_witness,source)
                   VALUES(?,?,?,?, 'unbenchable', 1, 'notes-seed')""", (prog, test, asrt, algo))

# 3. confirmed benchable (were false-positives, hand-flipped)
for prog in ["handlr","htmlq","peco","zoxide","lz4","pigz","xz"]:
    con.execute("UPDATE programs SET status='settled_benchable', extracted=1 WHERE program=?", (prog,))

# 4. contestable (excluded from floor)
for prog in ["proj","tinycc","quickjs","luajit","ascii-image-converter"]:
    con.execute("UPDATE programs SET status='contestable' WHERE program=?", (prog,))

# 5. prior (unreliable) signals, for reference only
try:
    passes = json.load(open("/tmp/all_passes.json"))
    for prog, d in passes.items():
        sig = ";".join(f"{s}:{v}" for s,v in d.get("v",[]))
        con.execute("UPDATE programs SET prior_signal=? WHERE program=?", (sig, prog))
except Exception as e:
    print("prior_signal skip:", e)

con.commit()

# report
def n(q): return con.execute(q).fetchone()[0]
print("programs total        :", n("SELECT count(*) FROM programs"))
print("  settled_recall      :", n("SELECT count(*) FROM programs WHERE status='settled_recall'"))
print("  settled_benchable   :", n("SELECT count(*) FROM programs WHERE status='settled_benchable'"))
print("  contestable         :", n("SELECT count(*) FROM programs WHERE status='contestable'"))
print("  unconfirmed         :", n("SELECT count(*) FROM programs WHERE status='unconfirmed'"))
print("  not yet extracted   :", n("SELECT count(*) FROM programs WHERE extracted=0"))
print("witness tests         :", n("SELECT count(*) FROM tests WHERE is_witness=1"))
con.close()
