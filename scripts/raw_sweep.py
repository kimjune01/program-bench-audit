#!/usr/bin/env python3
"""COMPLETE raw-body sweep -> audit.db. Every exact-output assertion in every test
body becomes a row in raw_assertions (program, task, branch, file, line, assertion,
bin_exts_in_file). Exact-output asserts are the only recall-eligible tests; capturing
all of them is the complete relevant inventory (vs the lossy ~12k extractor candidates).
Resumable (skips tasks already swept), crash-safe (commit per task)."""
import json, re, sqlite3, os, sys, tarfile, urllib.request, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.join(HERE, "audit.db")
ALL = json.load(open("/tmp/all201.json"))
API = "https://huggingface.co/api/datasets/programbench/ProgramBench-Tests/tree/main"
RES = "https://huggingface.co/datasets/programbench/ProgramBench-Tests/resolve/main"

EXACT = re.compile(r"assert[^#\n]*==[^#\n]*(golden|expected|read_bytes\(\)|read_text\(\)|fixture|snapshot|hexdigest\(\)|\.out\b)"
                   r"|assert[^#\n]*read_bytes\(\)|hexdigest\(\)\s*==|assertEqual\(")
BINEXT = re.compile(r"\.(bam|cram|bcf|parquet|avro|orc|zst|zstd|lz4|br|snappy|flac|mp3|aac|ogg|opus|wav|webp|jpe?g|png|gif|tiff|bmp|avif|heic|pdf|ttf|otf|woff2?|so|elf|wasm|class|pyc|sqlite|npy|msgpack|ico|psd|ppm)\b", re.I)

con = sqlite3.connect(DB, timeout=60); con.execute("PRAGMA journal_mode=WAL"); con.execute("PRAGMA busy_timeout=30000")
con.execute("""CREATE TABLE IF NOT EXISTS raw_assertions(
  id INTEGER PRIMARY KEY AUTOINCREMENT, program TEXT, task TEXT, branch_hash TEXT,
  test_file TEXT, lineno INTEGER, assertion TEXT, bin_exts TEXT)""")
con.execute("CREATE TABLE IF NOT EXISTS raw_swept(task TEXT PRIMARY KEY, programs INTEGER, exact INTEGER)")
con.commit()
done = {r[0] for r in con.execute("SELECT task FROM raw_swept")}

def get(url, raw=False):
    for _ in range(3):
        try:
            with urllib.request.urlopen(url, timeout=60) as r: return r.read()
        except Exception: time.sleep(2)
    return None

for i, p in enumerate(ALL):
    task, prog, lang = p["task"], p["program"], p["lang"]
    if task in done: continue
    meta = get(f"{API}/{task}/tests?recursive=true")
    hashes = []
    if meta:
        try: hashes = [x["path"].split("/")[-1][:-7] for x in json.loads(meta) if x["path"].endswith(".tar.gz")]
        except Exception: pass
    nrows = 0
    for H in hashes:
        blob = get(f"{RES}/{task}/tests/{H}.tar.gz")
        if not blob: continue
        with tempfile.NamedTemporaryFile(suffix=".tgz", delete=False) as tf: tf.write(blob); path = tf.name
        try:
            with tarfile.open(path) as t:
                for m in t.getmembers():
                    if not m.name.endswith(".py"): continue
                    try: text = t.extractfile(m).read().decode("utf-8", "replace")
                    except Exception: continue
                    exts = ",".join(sorted(set(e.group(0).lower() for e in BINEXT.finditer(text))))
                    for ln, line in enumerate(text.splitlines(), 1):
                        s = line.strip()
                        if s.startswith("#"): continue
                        if EXACT.search(line):
                            con.execute("INSERT INTO raw_assertions(program,task,branch_hash,test_file,lineno,assertion,bin_exts) VALUES(?,?,?,?,?,?,?)",
                                        (prog, task, H, m.name, ln, s[:500], exts))
                            nrows += 1
        finally: os.remove(path)
    con.execute("INSERT OR REPLACE INTO raw_swept(task,programs,exact) VALUES(?,1,?)", (task, nrows))
    con.commit()
    print(f"[{i+1}/{len(ALL)}] {prog}: {nrows} exact-output asserts ({len(hashes)} branches)", flush=True)
print("DONE")
