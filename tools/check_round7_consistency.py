#!/usr/bin/env python3
"""Documentary consistency check for Round 7. Does not execute product code."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs/planning"
HIST = ROOT / "historical/round6/docs/planning"
errors = []

def fail(msg):
    errors.append(msg)

def text(path):
    return path.read_text(encoding="utf-8")

matrix = text(PLAN / "FDP-TRACEABILITY-MATRIX-v1.4-CANONICAL.md")
lines = matrix.splitlines()
oracle = []
mode = False
for line in lines:
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
p0 = ["AUTH-01","AUTHZ-01","AUTHZ-02","RLS-01","FS-01","FS-02","TERM-01","SEC-01","SEC-02","ENG-01","ENG-02","PREVIEW-01","DEPLOY-01","DEPLOY-02","AUDIT-01","COST-01","STOP-01"]
for i in p0:
    if ids.count(i) != 1:
        fail(f"P0 count {i}={ids.count(i)}")
for i in ["LEDGER-07","LEDGER-08","LEDGER-09","LEDGER-10","LEDGER-11","LEDGER-12"]:
    if i not in ids:
        fail(f"missing {i}")
# intents unchanged vs v1.3
old = text(HIST / "FDP-TRACEABILITY-MATRIX-v1.3-CANONICAL.md")
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
    fail("P0 intent changed from v1.3")

stories = text(PLAN / "FDP-19A-v1.4-STORY-ACCEPTANCE-REGISTER.md")
if stories.count("## F-0") != 41:
    fail(f"story count {stories.count('## F-0')}")
if stories.count("- Inherited:") != 41:
    fail("inherited count")
if stories.count("Not met. Named person") != 41:
    fail("operational DoR count")
if "New in v1.4:" not in stories.split("## F-016")[0].split("## F-015")[1]:
    fail("F-015 missing v1.4 source")
# other stories should not gain a New in v1.4 line
rest = stories.split("## F-016", 1)[1]
if "New in v1.4:" in rest:
    fail("a story after F-015 was reopened with New in v1.4")

cited = []
for block in stories.split("## F-")[1:]:
    for line in block.splitlines():
        if line.startswith("Tests:"):
            cited.extend([x.strip() for x in line.split(":",1)[1].split(",")])
missing = sorted({c for c in cited if c not in ids})
if missing:
    fail(f"story tests missing from matrix: {missing}")

contract = text(PLAN / "FDP-16A-v1.4-EXECUTION-CONTRACTS.md")
for needle in [
    "Lock order, always",
    "operation_money_movement.operation_id",
    "Two RecordReceipt on one operation",
    "RecordReceipt versus ReleaseReservation",
    "Two ReleaseReservation",
    "Late retry after the winner",
    "IDEMPOTENT_REPLAY",
    "ApproveManualReconciliation",
    "ApplyAuthorizedReconciliation",
    "HUMAN_RECONCILIATION_REQUIRED",
    "EVIDENCE_REQUIRED",
    "SELF_CONFIRM",
    "AMBIGUOUS_RECONCILIATION",
    "ACTOR_FORBIDDEN",
    "FOR UPDATE",
]:
    if needle not in contract:
        fail(f"contract missing {needle}")
if "human RecordReceipt with evidence ref" in contract:
    fail("old human RecordReceipt transition still present")
# closed controls still present
for needle in ["approver_actor_ref", "blocked_from", "NOT_EXECUTING", "APPROVAL_MISMATCH"]:
    if needle not in contract:
        fail(f"closed control missing from contract: {needle}")
engines = text(PLAN / "FDP-16-v1.4-AIOX-EXECUTION-ENGINES.md")
if "FORGE_DIRECT" not in engines or "only supported orchestrator" in engines:
    fail("AIOX rule drifted")
if "start_task" not in stories:
    fail("adapter surface missing")
# single matrix in planning
matrices = list(PLAN.glob("FDP-TRACEABILITY-MATRIX-*.md"))
if [p.name for p in matrices] != ["FDP-TRACEABILITY-MATRIX-v1.4-CANONICAL.md"]:
    fail(f"matrix files in planning: {[p.name for p in matrices]}")
# v1.3 snapshot
if not (HIST / "FDP-16A-v1.3-EXECUTION-CONTRACTS.md").exists():
    fail("v1.3 snapshot missing")
# unchanged files identical
for name in [
    "FDP-18-v1.3-DEPLOYMENT-ROLLBACK.md",
    "FDP-18A-v1.3-RECOVERY-RUNBOOKS.md",
    "FDP-20-v1.3-SPRINT-IMPLEMENTATION-PLAN.md",
]:
    if (PLAN / name).read_bytes() != (HIST / name).read_bytes():
        fail(f"{name} differs from snapshot")
parecer = text(ROOT / "docs/reviews/PARECER-CODEX-ROUND6-2026-10-13.md")
if "HIGH-01" not in parecer or "NEW-HIGH-07" not in parecer:
    fail("parecer missing")
status = text(PLAN / "FDP-ROUND7-STATUS-INDEX.md")
if "ROUND 7 — CANDIDATE FOR CODEX REVIEW" not in status:
    fail("status index")
if "READY FOR BUILD" in status and "Não é READY FOR BUILD" not in status and "NOT READY FOR BUILD" not in status:
    fail("readiness wording")
# task states
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
