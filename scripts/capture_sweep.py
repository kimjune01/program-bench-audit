#!/usr/bin/env python3
"""Mechanical sweep for the self-capturing-golden anti-pattern in GRADED tests:
a test that writes its own oracle from the program's output, e.g.
    if not golden.exists(): golden.write_text(result.stdout)
    assert result.stdout == golden.read_text()
Two severities: golden BUNDLED -> grades the reference's own bytes (preferential
treatment, no independent oracle); golden ABSENT -> vacuous pass for any output.
Per-program counts -> audit.db `capture_smell`. Mechanical, resumable."""
import json,re,sqlite3,os,tarfile,urllib.request,io,time
HERE=os.path.dirname(os.path.abspath(__file__)); DB=os.path.join(HERE,"audit.db")
ALL=json.load(open("/tmp/all201.json"))
API="https://huggingface.co/api/datasets/programbench/ProgramBench-Tests/tree/main"
RES="https://huggingface.co/datasets/programbench/ProgramBench-Tests/resolve/main"
# write program output to a file (capture); and the conditional-capture guard
WRITE=re.compile(r"(\w[\w.]*)\.write_(?:text|bytes)\s*\(\s*(?:result\.)?(?:stdout|stderr|out)\b")
GUARD=re.compile(r"if\s+not\s+(\w[\w.]*)\.exists\s*\(\s*\)")
con=sqlite3.connect(DB,timeout=60); con.execute("PRAGMA journal_mode=WAL"); con.execute("PRAGMA busy_timeout=30000")
con.execute("""CREATE TABLE IF NOT EXISTS capture_smell(program TEXT PRIMARY KEY, task TEXT,
  graded_files INTEGER, capture_files INTEGER, capture_lines INTEGER, conditional INTEGER, sample TEXT)""")
con.commit()
done={r[0] for r in con.execute("SELECT program FROM capture_smell")}
def get(u):
    for _ in range(3):
        try:
            with urllib.request.urlopen(u,timeout=90) as r: return r.read()
        except Exception: time.sleep(2)
    return None
for i,p in enumerate(ALL):
    task,prog=p["task"],p["program"]
    if prog in done: continue
    meta=get(f"{API}/{task}/tests?recursive=true"); hs=[]
    if meta:
        try: hs=[x["path"].split("/")[-1][:-7] for x in json.loads(meta) if x["path"].endswith(".tar.gz")]
        except Exception: pass
    gradedf=set(); capf=set(); caplines=0; cond=0; sample=""
    for H in hs:
        blob=get(f"{RES}/{task}/tests/{H}.tar.gz")
        if not blob: continue
        try: t=tarfile.open(fileobj=io.BytesIO(blob))
        except Exception: continue
        for m in t.getmembers():
            if not m.name.endswith(".py") or "eval/tests/" not in m.name: continue
            gradedf.add(m.name.split("/")[-1])
            try: body=t.extractfile(m).read().decode("utf-8","replace")
            except Exception: continue
            w=WRITE.findall(body)
            if w:
                capf.add(m.name.split("/")[-1]); caplines+=len(w)
                if GUARD.search(body): cond+=1
                if not sample:
                    for ln in body.splitlines():
                        if WRITE.search(ln): sample=ln.strip()[:160]; break
    con.execute("INSERT OR REPLACE INTO capture_smell VALUES(?,?,?,?,?,?,?)",
                (prog,task,len(gradedf),len(capf),caplines,cond,sample))
    con.commit()
    print(f"[{i+1}/{len(ALL)}] {prog}: capture_files={len(capf)} lines={caplines} cond={cond}",flush=True)
print("DONE")
