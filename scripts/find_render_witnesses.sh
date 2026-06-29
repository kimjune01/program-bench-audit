#!/usr/bin/env bash
# Deterministic, replayable grep for the render/font witness class:
# a graded test that asserts the EXACT bytes of rendered output (image/doc/frame),
# which no offline solver can reproduce without the embedded font/rasterizer.
#
# Signature (exact-content comparison, NOT mere "-o out.png" filename args):
#   read_bytes() ==      |  == ...read_bytes()      (ditaa-style helper, typst)
#   framemd5                                          (ffmpeg frame hashing)
#   == <path>.(png|pdf|svg|ppm|bmp|gif|webp|tiff)     (golden binary compare)
#   hashlib... on rendered output
# Re-run by anyone: the verdict is the grep's, not an agent's.
set -u
API="https://huggingface.co/api/datasets/programbench/ProgramBench-Tests/tree/main"
RES="https://huggingface.co/datasets/programbench/ProgramBench-Tests/resolve/main"
SIG='read_bytes\(\)[[:space:]]*==|==[[:space:]]*[^=]*read_bytes\(\)|framemd5|==[[:space:]]*[^=]*\.(png|pdf|svg|ppm|bmp|gif|webp|tiff)[")'"'"']|hashlib\.[a-z0-9]+\([^)]*\)\.hexdigest\(\)[[:space:]]*=='
OUT="$(dirname "$0")/render_hits.txt"
: > "$OUT"
ALL=/tmp/all201.json
n=$(python3 -c "import json;print(len(json.load(open('$ALL'))))")
for i in $(seq 0 $((n-1))); do
  read -r PROG TASK < <(python3 -c "import json;d=json.load(open('$ALL'))[$i];print(d['program'],d['task'])")
  # first branch hash only (fast pass; witnesses usually live in the primary suite)
  H=$(curl -s "$API/$TASK/tests?recursive=true" | python3 -c "import json,sys
try:
 d=json.load(sys.stdin); print(next(x['path'].split('/')[-1][:-7] for x in d if x['path'].endswith('.tar.gz')))
except Exception: print('')" 2>/dev/null)
  [ -z "$H" ] && { echo "$PROG	NO_BRANCH" >>"$OUT"; continue; }
  hits=$(curl -sL "$RES/$TASK/tests/$H.tar.gz" 2>/dev/null | tar xzO --wildcards --no-anchored '*.py' 2>/dev/null \
         | grep -vE '^[[:space:]]*#' | grep -Ec "$SIG")
  [ "${hits:-0}" -gt 0 ] && echo "$PROG	$hits	$TASK	$H" >>"$OUT"
  echo "[$((i+1))/$n] $PROG hits=${hits:-0}"
done
echo "DONE. Render-witness candidates:"; sort -t$'\t' -k2 -nr "$OUT" | grep -vE 'NO_BRANCH' | head -40
