#!/usr/bin/env python3
"""Documentary consistency check for Round 10. Does not execute product code."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs/planning"
HIST = ROOT / "historical/round9/docs/planning"
errors = []

def fail(msg):
    errors.append(msg)

def text(path):
    return path.read_text(encoding="utf-8")

def row(src, test_id):
    for line in src.splitlines():
        if line.startswith(f"| {test_id} |"):
            return line
    return ""

matrix = text(PLAN / "FDP-TRACEABILITY-MATRIX-v1.7-CANONICAL.md")
old = text(HIST / "FDP-TRACEABILITY-MATRIX-v1.6-CANONICAL.md")
oracle = []
mode = False
for line in matrix.splitlines():
    if line.startswith("| Test ID"):
        mode = True
        continue
    if mode and line.startswith("## "):
        mode = False
    if mode and line.startswith("|") and not line.startswith("|---"):
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) != 11:
            fail(f"column count {len(cells)} for {cells[0] if cells else line[:40]}")
        else:
            oracle.append(cells)
ids = [c[0] for c in oracle]
if len(ids) != len(set(ids)):
    fail("duplicate oracle id")
if len(ids) != 91:
    fail(f"oracle count {len(ids)} expected 91")
p0 = ["AUTH-01","AUTHZ-01","AUTHZ-02","RLS-01","FS-01","FS-02","TERM-01","SEC-01","SEC-02","ENG-01","ENG-02","PREVIEW-01","DEPLOY-01","DEPLOY-02","AUDIT-01","COST-01","STOP-01"]
for i in p0:
    if ids.count(i) != 1:
        fail(f"P0 count {i}={ids.count(i)}")
if "LEDGER-18" not in ids or "LEDGER-17" not in ids:
    fail("missing late-evidence oracle")

def intent_map(src):
    out = {}
    for line in src.splitlines():
        if not line.startswith("| ") or line.startswith("| Test") or line.startswith("|---") or line.startswith("| Story"):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if cells and cells[0] in p0:
            out[cells[0]] = cells[1]
    return out

if intent_map(matrix) != intent_map(old):
    fail("P0 intent changed from v1.6")

changed = []
for line in old.splitlines():
    if not line.startswith("| ") or line.startswith("| Test") or line.startswith("|---") or line.startswith("| Story"):
        continue
    tid = line.split("|")[1].strip()
    if tid != "F-015" and row(matrix, tid) != line:
        changed.append(tid)
if changed:
    fail(f"oracle text changed outside NEW-MEDIUM-12: {changed[:12]}")

l18 = row(matrix, "LEDGER-18")
for needle in ["RELEASE", "amount 30", "amount 40", "NO_EFFECT", "spent 830", "reserved 100", "second movement", "budget.proof_conflict", "NOT RUN"]:
    if needle not in l18:
        fail(f"LEDGER-18 missing {needle}")
if row(matrix, "LEDGER-17") != row(old, "LEDGER-17"):
    fail("LEDGER-17 was rewritten")

stories = text(PLAN / "FDP-19A-v1.7-STORY-ACCEPTANCE-REGISTER.md")
old_stories = text(HIST / "FDP-19A-v1.6-STORY-ACCEPTANCE-REGISTER.md")
if stories.count("## F-0") != 41 or stories.count("- Inherited:") != 41 or stories.count("Not met. Named person") != 41:
    fail("story, inherited, or DoR count")
f015 = stories.split("## F-016", 1)[0].split("## F-015", 1)[1]
if "New in v1.7:" not in f015:
    fail("F-015 missing v1.7 source")
if "New in v1.7:" in stories.split("## F-016", 1)[1]:
    fail("v1.7 source leaked")
rest = stories.split("## F-016", 1)[1].replace("the v1.7 matrix", "the v1.6 matrix").replace(
    "DoD is not satisfied in Round 10.", "DoD is not satisfied in Round 9."
)
if rest != old_stories.split("## F-016", 1)[1]:
    fail("a story after F-015 changed beyond the matrix pointer")
cited = []
for block in stories.split("## F-")[1:]:
    for line in block.splitlines():
        if line.startswith("Tests:"):
            cited.extend([x.strip() for x in line.split(":", 1)[1].split(",")])
missing = sorted({c for c in cited if c not in ids})
if missing:
    fail(f"story tests missing from matrix: {missing}")

contract = text(PLAN / "FDP-16A-v1.7-EXECUTION-CONTRACTS.md")
if "when the movement was a RELEASE" in contract or "when the movement was RELEASE" in contract:
    fail("late evidence still limited to RELEASE")
for needle in [
    "one idempotent pending_provider_cost row per conclusive RECEIPT",
    "RELEASE, then a conclusive receipt of 30",
    "receipt B for 40",
    "then a conclusive NO_EFFECT",
    "not returned to HELD",
    "does not become a receipt row",
    "both `requested_by` and `confirmed_by`",
    "operation_id` alone is not unique",
    "Lock order, always",
    "approver_actor_ref",
    "blocked_from",
    "NOT_EXECUTING",
    "APPROVAL_MISMATCH",
    "forge.provider_ingest",
]:
    if needle not in contract:
        fail(f"contract missing {needle}")
frozen = text(HIST / "FDP-16A-v1.6-EXECUTION-CONTRACTS.md")
if "when the movement was RELEASE" not in frozen:
    fail("v1.6 snapshot lost the audited sentence")
engines = text(PLAN / "FDP-16-v1.7-AIOX-EXECUTION-ENGINES.md")
if "FORGE_DIRECT" not in engines or "only supported orchestrator" in engines:
    fail("AIOX rule drifted")
matrices = sorted(p.name for p in PLAN.glob("FDP-TRACEABILITY-MATRIX-*.md"))
if matrices != ["FDP-TRACEABILITY-MATRIX-v1.7-CANONICAL.md"]:
    fail(f"matrix files in planning: {matrices}")
for name in [
    "FDP-18-v1.3-DEPLOYMENT-ROLLBACK.md",
    "FDP-18A-v1.3-RECOVERY-RUNBOOKS.md",
    "FDP-20-v1.3-SPRINT-IMPLEMENTATION-PLAN.md",
]:
    if (PLAN / name).read_bytes() != (HIST / name).read_bytes():
        fail(f"{name} differs from snapshot")
parecer = text(ROOT / "docs/reviews/PARECER-CODEX-ROUND9-2026-10-13.md")
if "PASS WITH CONDITIONS" not in parecer or "NEW-MEDIUM-12" not in parecer or "C-01" not in parecer:
    fail("parecer missing")
if parecer != text(ROOT / "historical/round9/docs/reviews/PARECER-CODEX-ROUND9-2026-10-13.md"):
    fail("parecer copy differs")
if "ROUND 10 — CANDIDATE FOR CODEX REVIEW" not in text(PLAN / "FDP-ROUND10-STATUS-INDEX.md"):
    fail("status index")
for s in ["QUEUED", "READY", "RUNNING", "WAITING", "RETRYING", "HANDOFF", "REVIEWING", "BLOCKED", "COMPLETED", "FAILED", "CANCELLED"]:
    if s not in contract:
        fail(f"task state {s} missing")

print(f"oracles {len(ids)}")
print(f"stories cited tests {len(cited)}")
if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("PASS documentary checks")
print("NOT a product test. NOT a Codex verdict. NOT READY FOR BUILD.")
