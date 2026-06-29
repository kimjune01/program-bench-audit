#!/usr/bin/env python3
"""COMPLETE literal-match sweep -> audit.db `litmatch` table.
Deterministic regex classifies every assertion: LIT (exact literal/golden/fixture
match = recall-ELIGIBLE) vs BENCH (substring/returncode/len/membership = benchable
by construction). Stores every LIT assertion (program,task,branch,file,line,text,
bin_exts) + per-task LIT/BENCH counts. Replayable, resumable, crash-safe.
The recall witnesses are the SUBSET of LIT whose value needs a non-recoverable
function (opaque-binary decode, non-stdlib data table, codec). LIT is the denominator."""
import json, re, sqlite3, os, tarfile, urllib.request, tempfile, time

HERE=os.path.dirname(os.path.abspath(__file__)); DB=os.path.join(HERE,"audit.db")
ALL=json.load(open("/tmp/all201.json"))
API="https://huggingface.co/api/datasets/programbench/ProgramBench-Tests/tree/main"
RES="https://huggingface.co/datasets/programbench/ProgramBench-Tests/resolve/main"

LIT=re.compile(r"""(?:assertEqual\s*\(
 |==\s*[bBrRfFuU]*(['"])
 |==\s*[^#\n]*?\.read_(?:text|bytes)\s*\(\)
 |\.read_(?:text|bytes)\s*\(\)\s*==
 |==\s*[^#\n]*?\.golden
 |==\s*\(?\s*(?:expected|golden|want|EXPECTED|GOLDEN|WANT)\w*
 |hexdigest\s*\(\)\s*==|==\s*[^#\n]*?hexdigest\s*\(\)
 |==\s*['"]{3})""", re.VERBOSE)
BENCH=re.compile(r"""\.returncode|\breturncode\b|\blen\s*\(|\bisinstance\s*\(
 |\bin\s|\bnot\s+in\s|\.startswith\s*\(|\.endswith\s*\(
 |!=|>=|<=|\s>\s|\s<\s|\bis\s+(?:None|True|False)\b
 |assert\s+re\.(?:search|match|findall|fullmatch)
 |==\s*-?\d+\s*(?:[,)#]|$)|==\s*(?:True|False|None|\[\]|\{\}|\(\))""", re.VERBOSE)
BINEXT=re.compile(r"\.(bam|cram|bcf|parquet|avro|orc|zst|zstd|lz4|br|snappy|flac|mp3|aac|ogg|opus|wav|webp|jpe?g|gif|tiff|bmp|avif|heic|pdf|ttf|otf|woff2?|so|elf|wasm|class|pyc|sqlite|npy|msgpack|ico|psd|ppm)\b",re.I)

def cls(line):
    s=line.strip()
    if not s.startswith("assert"): return None
    if BENCH.search(line): return "BENCH"
    if LIT.search(line): return "LIT"
    return None

con=sqlite3.connect(DB,timeout=60); con.execute("PRAGMA journal_mode=WAL"); con.execute("PRAGMA busy_timeout=30000")
con.execute("""CREATE TABLE IF NOT EXISTS litmatch(id INTEGER PRIMARY KEY AUTOINCREMENT,
  program TEXT,task TEXT,branch_hash TEXT,test_file TEXT,lineno INTEGER,assertion TEXT,bin_exts TEXT)""")
con.execute("CREATE TABLE IF NOT EXISTS lit_swept(task TEXT PRIMARY KEY,lit INTEGER,bench INTEGER)")
con.commit()
done={r[0] for r in con.execute("SELECT task FROM lit_swept")}
def get(u):
    for _ in range(3):
        try:
            with urllib.request.urlopen(u,timeout=60) as r: return r.read()
        except Exception: time.sleep(2)
    return None

for i,p in enumerate(ALL):
    task,prog=p["task"],p["program"]
    if task in done: continue
    meta=get(f"{API}/{task}/tests?recursive=true"); hs=[]
    if meta:
        try: hs=[x["path"].split("/")[-1][:-7] for x in json.loads(meta) if x["path"].endswith(".tar.gz")]
        except Exception: pass
    nl=nb=0
    for H in hs:
        blob=get(f"{RES}/{task}/tests/{H}.tar.gz")
        if not blob: continue
        with tempfile.NamedTemporaryFile(suffix=".tgz",delete=False) as tf: tf.write(blob); path=tf.name
        try:
            with tarfile.open(path) as t:
                for m in t.getmembers():
                    if not m.name.endswith(".py"): continue
                    try: text=t.extractfile(m).read().decode("utf-8","replace")
                    except Exception: continue
                    exts=",".join(sorted(set(e.group(0).lower() for e in BINEXT.finditer(text))))
                    for ln,line in enumerate(text.splitlines(),1):
                        c=cls(line)
                        if c=="BENCH": nb+=1
                        elif c=="LIT":
                            nl+=1
                            con.execute("INSERT INTO litmatch(program,task,branch_hash,test_file,lineno,assertion,bin_exts) VALUES(?,?,?,?,?,?,?)",
                                        (prog,task,H,m.name,ln,line.strip()[:500],exts))
        finally: os.remove(path)
    con.execute("INSERT OR REPLACE INTO lit_swept(task,lit,bench) VALUES(?,?,?)",(task,nl,nb))
    con.commit()
    print(f"[{i+1}/{len(ALL)}] {prog}: LIT={nl} BENCH={nb}",flush=True)
print("DONE")
