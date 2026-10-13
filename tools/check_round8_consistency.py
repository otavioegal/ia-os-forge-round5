#!/usr/bin/env python3
"""Documentary consistency check for Round 8. Does not execute product code."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs/planning"
HIST = ROOT / "historical/round7/docs/planning"
errors = []

def fail(msg):
    errors.append(msg)

def text(path):
    return path.read_text(encoding="utf-8")

matrix = text(PLAN / "FDP-TRACEABILITY-MATRIX-v1.5-CANONICAL.md")
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
if len(ids) != 88:
    fail(f"oracle count {len(ids)} expected 88")
p0 = ["AUTH-01","AUTHZ-01","AUTHZ-02","RLS-01","FS-01","FS-02","TERM-01","SEC-01","SEC-02","ENG-01","ENG-02","PREVIEW-01","DEPLOY-01","DEPLOY-02","AUDIT-01","COST-01","STOP-01"]
for i in p0:
    if ids.count(i) != 1:
        fail(f"P0 count {i}={ids.count(i)}")
for i in ["LEDGER-07","LEDGER-08","LEDGER-09","LEDGER-10","LEDGER-11","LEDGER-12","LEDGER-13","LEDGER-14","LEDGER-15"]:
    if i not in ids:
        fail(f"missing {i}")

old = text(HIST / "FDP-TRACEABILITY-MATRIX-v1.4-CANONICAL.md")

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
    fail("P0 intent changed from v1.4")

def row(src, test_id):
    for line in src.splitlines():
        if line.startswith(f"| {test_id} |"):
            return line
    return ""

for keep in ["LEDGER-01","LEDGER-02","LEDGER-03","LEDGER-04","LEDGER-05","LEDGER-06","LEDGER-07","LEDGER-09","LEDGER-10","DEPLOY-02","HANDOFF-01"]:
    if row(matrix, keep) != row(old, keep):
        fail(f"{keep} oracle text changed")

l8 = row(matrix, "LEDGER-08")
if "or RELEASED" in l8.split("|")[7]:
    fail("LEDGER-08 still treats RELEASED as a positive alternative")
if "CONFLICT" not in l8 or "spent stays 800" not in l8:
    fail("LEDGER-08 missing conflict hold")
if "depends on which transaction acquired the lock" not in l8:
    fail("LEDGER-08 missing lock-independence negative")
for extra in ["LEDGER-13","LEDGER-14","LEDGER-15"]:
    if "NOT RUN" not in row(matrix, extra):
        fail(f"{extra} not NOT RUN")
if "RECEIPT_PRECEDES_RELEASE" not in row(matrix, "LEDGER-13"):
    fail("LEDGER-13 missing receipt precedence")
if "AUTHORIZATION_CONFLICT" not in row(matrix, "LEDGER-14"):
    fail("LEDGER-14 missing authorization conflict")
if "pending_provider_cost" not in row(matrix, "LEDGER-15"):
    fail("LEDGER-15 missing pending cost")

stories = text(PLAN / "FDP-19A-v1.5-STORY-ACCEPTANCE-REGISTER.md")
if stories.count("## F-0") != 41:
    fail(f"story count {stories.count('## F-0')}")
if stories.count("- Inherited:") != 41:
    fail("inherited count")
if stories.count("Not met. Named person") != 41:
    fail("operational DoR count")
f015 = stories.split("## F-016", 1)[0].split("## F-015", 1)[1]
rest = stories.split("## F-016", 1)[1]
if "New in v1.5:" not in f015:
    fail("F-015 missing v1.5 source")
if "New in v1.5:" in rest:
    fail("New in v1.5 leaked past F-015")
if "New in v1.3:" not in f015 or "New in v1.4:" not in f015:
    fail("F-015 dropped an older source bullet")
if "the v1.4 matrix" in stories:
    fail("story register still points at the v1.4 matrix")

cited = []
for block in stories.split("## F-")[1:]:
    for line in block.splitlines():
        if line.startswith("Tests:"):
            cited.extend([x.strip() for x in line.split(":", 1)[1].split(",")])
missing = sorted({c for c in cited if c not in ids})
if missing:
    fail(f"story tests missing from matrix: {missing}")

contract = text(PLAN / "FDP-16A-v1.5-EXECUTION-CONTRACTS.md")
for needle in [
    "Lock order, always",
    "Lock order does not decide which proof is true",
    "ProviderEffectProof",
    "forge.provider_ingest",
    "does not invent one",
    "RECEIPT_PRECEDES_RELEASE",
    "PROOF_CONFLICT",
    "PROOF_INCONCLUSIVE",
    "EVIDENCE_SELF_AUTHORED",
    "pending_provider_cost",
    "SESSION_STALE",
    "AUTHORIZATION_EXPIRED",
    "AUTHORIZATION_CONFLICT",
    "CAPABILITY_REVOKED",
    "EVIDENCE_MISMATCH",
    "IDEMPOTENT_REPLAY",
    "PENDING_COST_HELD",
    "operation_money_movement.operation_id",
    "A RELEASED status is not definitive",
]:
    if needle not in contract:
        fail(f"contract missing {needle}")
for banned in [
    "winner is whichever transaction acquires the operation lock first",
    "defines the winner",
    "winner's actual is stored",
    "human RecordReceipt with evidence ref",
]:
    if banned in contract:
        fail(f"banned phrase still present: {banned}")
for needle in ["approver_actor_ref", "blocked_from", "NOT_EXECUTING", "APPROVAL_MISMATCH"]:
    if needle not in contract:
        fail(f"closed control missing from contract: {needle}")
for s in ["QUEUED", "READY", "RUNNING", "WAITING", "RETRYING", "HANDOFF", "REVIEWING", "BLOCKED", "COMPLETED", "FAILED", "CANCELLED"]:
    if s not in contract:
        fail(f"task state {s} missing")

engines = text(PLAN / "FDP-16-v1.5-AIOX-EXECUTION-ENGINES.md")
if "FORGE_DIRECT" not in engines or "only supported orchestrator" in engines:
    fail("AIOX rule drifted")
if "budget.proof_conflict" not in engines or "budget.proof_inconclusive" not in engines:
    fail("proof audit names missing")
if "start_task" not in stories:
    fail("adapter surface missing")

matrices = sorted(p.name for p in PLAN.glob("FDP-TRACEABILITY-MATRIX-*.md"))
if matrices != ["FDP-TRACEABILITY-MATRIX-v1.5-CANONICAL.md"]:
    fail(f"matrix files in planning: {matrices}")

for name in [
    "FDP-18-v1.3-DEPLOYMENT-ROLLBACK.md",
    "FDP-18A-v1.3-RECOVERY-RUNBOOKS.md",
    "FDP-20-v1.3-SPRINT-IMPLEMENTATION-PLAN.md",
]:
    if (PLAN / name).read_bytes() != (HIST / name).read_bytes():
        fail(f"{name} differs from round7 snapshot")

for name in [
    "FDP-16A-v1.4-EXECUTION-CONTRACTS.md",
    "FDP-TRACEABILITY-MATRIX-v1.4-CANONICAL.md",
    "FDP-19A-v1.4-STORY-ACCEPTANCE-REGISTER.md",
]:
    if not (HIST / name).exists():
        fail(f"v1.4 snapshot missing {name}")

parecer = text(ROOT / "docs/reviews/PARECER-CODEX-ROUND7-2026-10-13.md")
if "HIGH-01" not in parecer or "NEW-HIGH-07" not in parecer or "NEW-HIGH-08" not in parecer or "NEW-HIGH-09" not in parecer:
    fail("parecer missing a finding id")
change = text(ROOT / "docs/reviews/ROUND7-CHANGE-REPORT-2026-10-13.md")
if "4e5783974ca27595c9592e2e6ac55ab23fcbeb5a" not in change:
    fail("original round 7 hash line was removed")
if "decef2809b61d3f1fe84bef74a5162d782cc6231" not in change:
    fail("errata missing the audited round 7 commit")
status = text(PLAN / "FDP-ROUND8-STATUS-INDEX.md")
if "ROUND 8 — CANDIDATE FOR CODEX REVIEW" not in status:
    fail("status index")
if "PASS" in status and "Não é PASS" not in status:
    fail("status index declares PASS")

print(f"oracles {len(ids)}")
print(f"stories cited tests {len(cited)}")
if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("PASS documentary checks")
print("NOT a product test. NOT a Codex verdict. NOT READY FOR BUILD.")
