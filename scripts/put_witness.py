#!/usr/bin/env python3
"""Recorder for witness VERIFICATION facts. An agent re-fetches one witness's
coordinate and pipes the replayable facts on stdin. We store the facts and set
status='facts_in'; roots (c)(d) and final verified|fail are set by hand afterward.
Crash-safe (WAL+busy_timeout); bad input preserved to recorder.err."""
import json, sqlite3, sys, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
DB, ERR = os.path.join(HERE,"audit.db"), os.path.join(HERE,"recorder.err")
raw = sys.stdin.read()
try:
    r = json.loads(raw); prog=r["program"]; test=r["test_name"]
except Exception as e:
    open(ERR,"a").write(f"--- {time.strftime('%H:%M:%S')} witness parse-fail {e}\n{raw}\n")
    print("RECORDED: ERROR (recorder.err):", e); sys.exit(0)
con = sqlite3.connect(DB, timeout=30)
con.execute("PRAGMA busy_timeout=30000"); con.execute("PRAGMA journal_mode=WAL")
con.execute("""INSERT INTO witnesses(program,test_name,status) VALUES(?,?,'hypothesis')
               ON CONFLICT(program,test_name) DO NOTHING""", (prog,test))
con.execute("""UPDATE witnesses SET task=?, branch_hash=?, test_file=?, assertion=?,
               input_prov=?, recall_channel=?, retrieval_cmd=?, status='facts_in'
               WHERE program=? AND test_name=?""",
            (r.get("task",""), r.get("branch_hash",""), r.get("test_file",""),
             r.get("assertion",""), r.get("input_prov",""), r.get("algorithm",""),
             r.get("retrieval_cmd",""), prog, test))
con.commit(); con.close()
print(f"RECORDED: witness facts for {prog}/{test}")
