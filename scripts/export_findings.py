#!/usr/bin/env python3
"""Regenerate findings/*.md from data/audit.db. Run after any adjudication change."""
import sqlite3, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
con = sqlite3.connect(os.path.join(R, "data", "audit.db"))
def q(sql, a=()): return con.execute(sql, a).fetchall()
out = os.path.join(R, "findings")

# 1. verdict summary
recall = q("SELECT count(*) FROM witnesses WHERE status='verified' AND mechanism='recall'")[0][0]
total  = q("SELECT count(*) FROM witnesses WHERE status='verified'")[0][0]
cap    = q("SELECT count(*) FROM capture_smell WHERE capture_files>0")[0][0]
cond   = q("SELECT sum(conditional) FROM capture_smell WHERE capture_files>0")[0][0]
with open(os.path.join(out, "00_verdict_summary.md"), "w") as f:
    f.write(f"""# ProgramBench benchability audit — verdict summary

Complete mechanical read of all 201 task suites (public on HF: `programbench/ProgramBench-Tests`).
Every verdict is re-derivable from the cited test body; the audit is one-sided (a witness proves
unbenchable; "no witness found" is not a clearance).

| verdict | programs |
|---|---|
| Unbenchable, recall witness verified | {recall} |
| Unbenchable, oracle implementation-pinned (render bytes) | {total-recall} |
| Self-capturing-golden programs (oracle provenance, axis 2) | {cap} ({cond} in the vacuous-if-absent conditional form) |

Recall floor {recall} and the {cap}-program self-capture finding are independent lower bounds.
The literal-match denominator is {q("SELECT sum(lit) FROM lit_swept")[0][0]:,} exact-output assertions.
""")

# 2. recall witnesses (Table A2)
with open(os.path.join(out, "01_recall_witnesses.md"), "w") as f:
    f.write("# Recall witnesses (axis 1)\n\nEach row: a graded test whose exact expected value is the output of a function no source-blind, offline solver can reproduce. Re-fetch any via its `retrieval_cmd` in the DB.\n\n| program | witness test | recalled function |\n|---|---|---|\n")
    for prog, test, ch in q("SELECT program, test_name, recall_channel FROM witnesses WHERE status='verified' AND mechanism='recall' ORDER BY program"):
        f.write(f"| {prog} | `{test}` | {ch or ''} |\n")

# 3. oracle provenance (render-pinned + self-capture)
with open(os.path.join(out, "02_oracle_provenance.md"), "w") as f:
    f.write("# Oracle provenance (axis 2): the golden is the reference's own output\n\nThe test oracle problem (Barr et al. 2015; Weyuker 1982): a reference used as its own oracle grades byte-identity-to-reference, not a contract.\n\n## Implementation-pinned (exact render bytes)\n\n| program | witness test | pinned artifact |\n|---|---|---|\n")
    for prog, test, ch in q("SELECT program, test_name, recall_channel FROM witnesses WHERE status='verified' AND mechanism IN ('brittle_render','bundled_font_data') ORDER BY program"):
        f.write(f"| {prog} | `{test}` | {ch or ''} |\n")
    f.write("\n## Self-capturing goldens (graded tests that write their own answer key)\n\n`if not golden.exists(): golden.write_text(result.stdout)` then `assert result.stdout == golden.read_text()`. Conditional form passes any output if the golden is absent.\n\n| program | capture lines | conditional (vacuous-risk) |\n|---|---|---|\n")
    for prog, n, c in q("SELECT program, capture_lines, conditional FROM capture_smell WHERE capture_files>0 ORDER BY capture_lines DESC"):
        f.write(f"| {prog} | {n} | {'yes' if c else ''} |\n")

# 4. class checks (negative results / non-determinism classes)
with open(os.path.join(out, "03_class_checks.md"), "w") as f:
    f.write("# Classes of concern checked (mostly benchable / neutralized)\n\nThe benchmark's sandbox + flaky-filter + deterministic-projection testing neutralize the environment and non-determinism classes. Recorded so a runner need not re-check.\n\n| class | verdict | why |\n|---|---|---|\n")
    for cls, v, r, ev, d in q("SELECT class, verdict, reason, evidence, depth FROM class_checks ORDER BY class"):
        f.write(f"| {cls} | {v} | {r} |\n")

# 5. full per-program verdict
with open(os.path.join(out, "04_per_program.md"), "w") as f:
    f.write("# Per-program status (all 201)\n\n| program | task | lang | status |\n|---|---|---|---|\n")
    for prog, task, lang, st in q("SELECT program, task, lang, status FROM programs ORDER BY status, program"):
        f.write(f"| {prog} | {task} | {lang} | {st} |\n")

# 6. runner-facing: skip-list, grader-caution, benchable subset
excl = q("SELECT DISTINCT program, mechanism FROM witnesses WHERE status='verified' ORDER BY program")
cap = q("SELECT program, conditional, COALESCE(severity,'?') FROM capture_smell WHERE capture_files>0 ORDER BY program")
scale = q("SELECT program, blast_radius FROM programs WHERE blast_radius>458 AND program NOT IN (SELECT program FROM witnesses WHERE status='verified') ORDER BY blast_radius DESC")
contest = [r[0] for r in q("SELECT program FROM programs WHERE status='contestable' ORDER BY program")]
excl_progs = {p for p, _ in excl}
bench = [r[0] for r in q("SELECT program FROM programs WHERE status NOT IN ('contestable') ORDER BY program") if r[0] not in excl_progs]
with open(os.path.join(out, "05_runner_subset.md"), "w") as f:
    f.write("# For a benchmark runner: the model-blind subset\n\n")
    f.write("This list is computed from the **test bodies**, never from any model's results, so adopting it is not a discretionary call and carries no conflict of interest. Every row is re-derivable by grep over the public suites (each witness ships a `retrieval_cmd` in the DB); you do not have to trust the author.\n\n")
    f.write(f"## Skip-list: exclude from Fully Resolved ({len(excl)} programs)\n\n")
    f.write("No source-blind, offline solver can resolve these (a recall-only test, or a byte-exact render the contract does not fix). Running a model on them spends build budget on a foregone fail; excluding them stops the headline conflating reconstruction with recall.\n\n| program | reason |\n|---|---|\n")
    for p, m in excl:
        f.write(f"| {p} | {m} |\n")
    dorm = sum(1 for _, _, s in cap if s == 'dormant')
    f.write(f"\n## Grader-caution: self-capturing oracle ({len(cap)} programs)\n\n")
    f.write(f"The grader writes its own golden from the reference run, so it grades byte-identity-to-reference (a weak oracle, not a contract). A golden-presence audit found {dorm} confirmed dormant (the golden is bundled, so the conditional `if not exists` branch never fires) and **none confirmed vacuous**: the vacuous pass is a latent risk, not an active one. Treat a pass from these as reference-identity at best, not correctness.\n\n| program | golden | conditional form |\n|---|---|---|\n")
    for p, c, s in cap:
        f.write(f"| {p} | {s} | {'yes' if c else ''} |\n")
    f.write(f"\n## Scale tier: unbenchable by coverage ({len(scale)} programs beyond the skip-list)\n\n")
    f.write("Soft tier, still model-blind and re-derivable but threshold-dependent. Blast radius > 458 distinct exact-output obligations, where the conjunctive pass rate q^N falls below 1% even at a charitable q=0.99. Not a per-test witness; a coverage argument, anchored by the benchmark's reported zero Fully Resolved. A runner may also skip these.\n\n| program | blast radius (distinct obligations) |\n|---|---|\n")
    for p, n in scale:
        f.write(f"| {p} | {n} |\n")
    f.write(f"\n## Benchable subset: report Fully Resolved over these ({len(bench)} programs)\n\n")
    f.write("No witness found and not contestable. This is a floor on the benchable set, not a certificate (the audit is one-sided).\n\n")
    f.write(", ".join(f"`{p}`" for p in bench) + "\n")
    f.write(f"\nContestable, held out of both pending inspection: {', '.join('`'+c+'`' for c in contest)}.\n")

con.close()
print("findings/ regenerated:", os.listdir(out))
