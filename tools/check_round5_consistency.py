#!/usr/bin/env python3
"""Consistency checks for the Round 5 candidate. Does not execute product tests."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs/planning"
errors = []
notes = []

files = sorted(PLAN.glob("FDP-*-v1.2-*.md"))
if len(files) < 9:
    errors.append(f"expected >= 9 v1.2 files, found {len(files)}")

p0 = [
    "AUTH-01", "AUTHZ-01", "AUTHZ-02", "RLS-01", "FS-01", "FS-02", "TERM-01",
    "SEC-01", "SEC-02", "ENG-01", "ENG-02", "PREVIEW-01", "DEPLOY-01", "DEPLOY-02",
    "AUDIT-01", "COST-01", "STOP-01",
]
task_states = [
    "QUEUED", "READY", "RUNNING", "WAITING", "RETRYING", "HANDOFF",
    "REVIEWING", "BLOCKED", "COMPLETED", "FAILED", "CANCELLED",
]

for path in files:
    text = path.read_text(encoding="utf-8")
    if "CANDIDATE FOR INDEPENDENT REVIEW" not in text:
        errors.append(f"{path.name}: missing candidate status")
    if "NOT READY FOR BUILD" not in text and "not READY FOR BUILD" not in text:
        errors.append(f"{path.name}: missing NOT READY FOR BUILD")
    if re.search(r"TRACEABILITY-MATRIX-v1\.[01]", text):
        errors.append(f"{path.name}: normative pointer to old matrix")
    if "v1.0 —" in text.splitlines()[0]:
        errors.append(f"{path.name}: title still says v1.0")

reg = (PLAN / "FDP-19A-v1.2-STORY-ACCEPTANCE-REGISTER.md").read_text(encoding="utf-8")
ids = re.findall(r"^## (F-\d{3}) —", reg, re.M)
expect = [f"F-{i:03d}" for i in range(1, 42)]
if ids != expect:
    errors.append(f"story ids mismatch: {ids}")
pos = re.findall(r"### Positive acceptance\n(.+)", reg)
neg = re.findall(r"### Negative acceptance\n(.+)", reg)
if len(set(pos)) != 41:
    errors.append(f"positive acceptances not unique: {len(set(pos))}")
if len(set(neg)) != 41:
    errors.append(f"negative acceptances not unique: {len(set(neg))}")
if "as applicable" in reg.lower():
    errors.append("generic phrase 'as applicable' still present")
sections = re.split(r"(?=^## F-)", reg, flags=re.M)
by_id = {}
for sec in sections:
    m = re.match(r"## (F-\d{3})", sec)
    if m:
        by_id[m.group(1)] = sec
for sid, needle in [("F-001", "AUTHZ-01"), ("F-006", "SEC-01"), ("F-015", "COST-01"), ("F-002", "AUTHZ-02")]:
    if needle not in by_id.get(sid, ""):
        errors.append(f"{sid} does not mention {needle}")
if "cannot satisfy COST-01" not in by_id["F-021"] and "Cannot satisfy COST-01" not in by_id["F-021"]:
    errors.append("F-021 does not explicitly refuse COST-01 ownership")

mx = (PLAN / "FDP-TRACEABILITY-MATRIX-v1.2-CANONICAL.md").read_text(encoding="utf-8")
oracle = mx.split("## Story index")[0]
if "authorized or nominal" in oracle:
    errors.append("generic oracle wording remains")
for tid in p0:
    n = len(re.findall(rf"^\| {tid} \|", oracle, re.M))
    if n != 1:
        errors.append(f"{tid} oracle rows: {n}")
if "SINGLE NORMATIVE TABLE" not in mx:
    errors.append("matrix does not claim single normative table")

contracts = (PLAN / "FDP-16A-v1.2-EXECUTION-CONTRACTS.md").read_text(encoding="utf-8")
for st in task_states:
    if st not in contracts:
        errors.append(f"task state missing from contracts: {st}")
for token in ["max_attempts", "base_delay_ms", "cap_delay_ms", "lease_ttl_ms", "forge.command.v1", "forge.event.v1", "CLAIMED_DONE"]:
    if token not in contracts:
        errors.append(f"contracts missing {token}")
if "future ADR" in contracts and "replaces the v1.1 deferral" not in contracts:
    errors.append("ADR deferral still open")

hist = ROOT / "historical/round4/docs/reviews/PARECER-CODEX-ROUND4-2026-10-13.md"
if not hist.exists():
    errors.append("historical Codex round 4 parecer missing")
else:
    notes.append(f"historical files preserved under historical/round4 ({sum(1 for _ in (ROOT/'historical').rglob('*') if _.is_file())} files)")

print(f"v1.2 files: {len(files)}")
print(f"stories: {len(ids)}")
print(f"unique positive acceptances: {len(set(pos))}")
print(f"unique negative acceptances: {len(set(neg))}")
p0_rows = sum(1 for t in p0 if re.search(rf"^\| {t} \|", oracle, re.M))
print(f"P0 oracle rows: {p0_rows}/17")
print(f"errors: {len(errors)}")
for e in errors:
    print(f"ERROR {e}")
for n in notes:
    print(f"NOTE {n}")
sys.exit(1 if errors else 0)
