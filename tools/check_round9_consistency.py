#!/usr/bin/env python3
"""Documentary consistency check for Round 9. Does not execute product code."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs/planning"
HIST = ROOT / "historical/round8/docs/planning"
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

matrix = text(PLAN / "FDP-TRACEABILITY-MATRIX-v1.6-CANONICAL.md")
old = text(HIST / "FDP-TRACEABILITY-MATRIX-v1.5-CANONICAL.md")
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
if len(ids) != 90:
    fail(f"oracle count {len(ids)} expected 90")
p0 = ["AUTH-01","AUTHZ-01","AUTHZ-02","RLS-01","FS-01","FS-02","TERM-01","SEC-01","SEC-02","ENG-01","ENG-02","PREVIEW-01","DEPLOY-01","DEPLOY-02","AUDIT-01","COST-01","STOP-01"]
for i in p0:
    if ids.count(i) != 1:
        fail(f"P0 count {i}={ids.count(i)}")
for i in ["LEDGER-08","LEDGER-14","LEDGER-15","LEDGER-16","LEDGER-17"]:
    if i not in ids:
        fail(f"missing {i}")

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
    fail("P0 intent changed from v1.5")

old_ids = []
for line in old.splitlines():
    if line.startswith("| ") and not line.startswith("| Test") and not line.startswith("|---") and not line.startswith("| Story"):
        tid = line.split("|")[1].strip()
        if tid and tid not in ("LEDGER-08", "LEDGER-15", "F-015"):
            if row(matrix, tid) != line:
                old_ids.append(tid)
if old_ids:
    fail(f"oracle text changed outside C-01/C-02: {old_ids[:12]}")

l8 = row(matrix, "LEDGER-08")
if "or RELEASED" in l8.split("|")[7]:
    fail("LEDGER-08 treats RELEASED as a pass")
if "pending_provider_cost" not in l8 or "reason CONFLICT" not in l8:
    fail("LEDGER-08 does not require the pending row")
if "no pending_provider_cost row exists" not in l8:
    fail("LEDGER-08 missing missing-row negative")
l15 = row(matrix, "LEDGER-15")
if "DISPATCHED" not in l15 or "HELD" not in l15 or "reserved is 150" not in l15:
    fail("LEDGER-15 fixture still ambiguous")
if "reason OVER_ESTIMATE" not in l15:
    fail("LEDGER-15 missing reason")
l16 = row(matrix, "LEDGER-16")
for needle in ["IDEMPOTENT_REPLAY", "ALREADY_CONFIRMED", "CAPABILITY_REVOKED", "requested_by", "confirmed_by", "unconsumed", "NOT RUN"]:
    if needle not in l16:
        fail(f"LEDGER-16 missing {needle}")
l17 = row(matrix, "LEDGER-17")
for needle in ["amount 30", "amount 40", "two pending_provider_cost", "max(amount_minor)", "lock first", "NOT RUN"]:
    if needle not in l17:
        fail(f"LEDGER-17 missing {needle}")
if row(matrix, "LEDGER-14") != row(old, "LEDGER-14"):
    fail("LEDGER-14 was rewritten")
if row(matrix, "LEDGER-12") != row(old, "LEDGER-12"):
    fail("LEDGER-12 was rewritten")

stories = text(PLAN / "FDP-19A-v1.6-STORY-ACCEPTANCE-REGISTER.md")
old_stories = text(HIST / "FDP-19A-v1.5-STORY-ACCEPTANCE-REGISTER.md")
if stories.count("## F-0") != 41:
    fail(f"story count {stories.count('## F-0')}")
if stories.count("- Inherited:") != 41 or stories.count("Not met. Named person") != 41:
    fail("inherited or DoR count")
f015 = stories.split("## F-016", 1)[0].split("## F-015", 1)[1]
if "New in v1.6:" not in f015:
    fail("F-015 missing v1.6 source")
if "New in v1.6:" in stories.split("## F-016", 1)[1]:
    fail("v1.6 source leaked")
rest = stories.split("## F-016", 1)[1].replace("the v1.6 matrix", "the v1.5 matrix").replace(
    "DoD is not satisfied in Round 9.", "DoD is not satisfied in Round 8."
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

contract = text(PLAN / "FDP-16A-v1.6-EXECUTION-CONTRACTS.md")
if "the human capability used to authorize is still present" in contract:
    fail("ambiguous Apply capability sentence remains")
for needle in [
    "both `requested_by` and `confirmed_by`",
    "403 CAPABILITY_REVOKED",
    "operation_id` alone is not unique",
    "(operation_id, proof_id)",
    "max(amount_minor)",
    "writes no audit event",
    "not `200 IDEMPOTENT_REPLAY`",
    "Lock order, always",
    "approver_actor_ref",
    "blocked_from",
    "NOT_EXECUTING",
    "APPROVAL_MISMATCH",
    "FOR UPDATE",
    "forge.provider_ingest",
]:
    if needle not in contract:
        fail(f"contract missing {needle}")
if "operation_id` unique" in contract:
    fail("pending cost still unique on operation_id alone")
engines = text(PLAN / "FDP-16-v1.6-AIOX-EXECUTION-ENGINES.md")
if "FORGE_DIRECT" not in engines or "only supported orchestrator" in engines:
    fail("AIOX rule drifted")
matrices = list(PLAN.glob("FDP-TRACEABILITY-MATRIX-*.md"))
if [p.name for p in matrices] != ["FDP-TRACEABILITY-MATRIX-v1.6-CANONICAL.md"]:
    fail(f"matrix files in planning: {[p.name for p in matrices]}")
for name in [
    "FDP-18-v1.3-DEPLOYMENT-ROLLBACK.md",
    "FDP-18A-v1.3-RECOVERY-RUNBOOKS.md",
    "FDP-20-v1.3-SPRINT-IMPLEMENTATION-PLAN.md",
]:
    if (PLAN / name).read_bytes() != (HIST / name).read_bytes():
        fail(f"{name} differs from snapshot")
if "the human capability used to authorize is still present" not in text(HIST / "FDP-16A-v1.5-EXECUTION-CONTRACTS.md"):
    fail("v1.5 snapshot was edited")
parecer = text(ROOT / "docs/reviews/PARECER-CODEX-ROUND8-2026-10-13.md")
if "PASS WITH CONDITIONS" not in parecer or "C-01" not in parecer or "HIGH-01" not in parecer:
    fail("parecer missing")
if text(ROOT / "docs/reviews/PARECER-CODEX-ROUND8-2026-10-13.md") != text(ROOT / "historical/round8/docs/reviews/PARECER-CODEX-ROUND8-2026-10-13.md"):
    fail("parecer copy differs")
status = text(PLAN / "FDP-ROUND9-STATUS-INDEX.md")
if "ROUND 9 — CANDIDATE FOR CODEX REVIEW" not in status:
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
