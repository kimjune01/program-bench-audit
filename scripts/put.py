#!/usr/bin/env python3
"""Recorder: one extractor agent pipes its JSON result on stdin; we commit it.

Crash-safe: WAL + busy_timeout so ~10 concurrent agents can each write their own
row without locking each other out. Parameterized inserts (no SQL injection from
assertion text). Bad input is preserved to a .err file, never silently dropped.

Usage (from an agent):
    python3 put.py <<'PBEOF'
    {"task":"...","program":"...","candidates":[{"test":"...","assertion":"...","algorithm":"..."}]}
    PBEOF
"""
import json, sqlite3, sys, os, time

HERE = os.path.dirname(os.path.abspath(__file__))
DB   = os.path.join(HERE, "audit.db")
ERR  = os.path.join(HERE, "recorder.err")

raw = sys.stdin.read()
try:
    rec = json.loads(raw)
    task = rec["task"]; program = rec.get("program", "")
    cands = rec.get("candidates", [])
    assert isinstance(cands, list)
except Exception as e:
    with open(ERR, "a") as f:
        f.write(f"--- {time.strftime('%H:%M:%S')} parse-fail {e}\n{raw}\n")
    print("RECORDED: ERROR (logged to recorder.err):", e)
    sys.exit(0)  # never crash the agent/workflow over a bad line

con = sqlite3.connect(DB, timeout=30)
con.execute("PRAGMA busy_timeout=30000")
con.execute("PRAGMA journal_mode=WAL")
for c in cands:
    con.execute(
        """INSERT OR IGNORE INTO tests(program,test_name,assertion,algorithm,adjudication,source)
           VALUES(?,?,?,?, 'pending', 'extract')""",
        (program, c.get("test",""), c.get("assertion",""), c.get("algorithm","")))
# mark the program as fully read, keyed on task (unique even for the two 'bat's)
con.execute("UPDATE programs SET extracted=1 WHERE task=?", (task,))
con.commit()
con.close()
print(f"RECORDED: {program} ({len(cands)} candidates)")
