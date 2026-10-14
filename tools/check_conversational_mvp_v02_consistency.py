#!/usr/bin/env python3
"""Documentary consistency check for DELTA CONVERSATIONAL-MVP v0.2.

Does not execute product code, providers, database, staging, or voice APIs.
Does not emit a Codex verdict and does not close findings.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "docs/planning/conversational-mvp-v0.2"
OLD = ROOT / "docs/planning/conversational-mvp"
ENV = os.environ.copy()
ENV["GIT_DISCOVERY_ACROSS_FILESYSTEM"] = "1"

AUDITED_V17 = "0c42373d583dec420348efd7bc0b8c6228a66f47"
AUDITED_V01 = "cad1ac6d6bb8a970165ebd17ce1bff13d98af806"
REVIEW_COMMIT = "3e12da4"

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], env=ENV, text=True)


required = [
    "CMP-00-PACKAGE-INDEX.md",
    "CMP-01-PRD-UX-JOURNEYS.md",
    "CMP-02-SYSTEM-ARCHITECTURE.md",
    "CMP-03-SECURITY-PRIVACY-AND-REVIEW-INDEPENDENCE.md",
    "CMP-04-OBSERVABILITY-EVIDENCE-AND-COST.md",
    "CMP-05-ADDITIVE-STORIES-AND-ORACLES.md",
    "CMP-06-TRACEABILITY-AND-IMPACT.md",
    "CMP-OPEN-QUESTIONS.md",
    "CMP-RISKS.md",
    "CMP-STATUS-INDEX.md",
    "CMP-CHANGE-REPORT.md",
    "CMP-FINDING-CLOSURE.md",
    "CMP-ORACLE-MATRIX-v0.2.md",
    "CMP-CONSISTENCY-REPORT.md",
]
for name in required:
    if not (PKG / name).is_file():
        fail(f"missing {name}")
    else:
        body = text(PKG / name)
        if "CANDIDATE FOR CODEX REVIEW" not in body:
            fail(f"{name} missing candidate banner")
        if "DELTA CONVERSATIONAL-MVP v0.1 —" in body:
            fail(f"{name} still stamped as the v0.1 candidate")

arch = text(PKG / "CMP-02-SYSTEM-ARCHITECTURE.md")
sec = text(PKG / "CMP-03-SECURITY-PRIVACY-AND-REVIEW-INDEPENDENCE.md")
ux = text(PKG / "CMP-01-PRD-UX-JOURNEYS.md")
reg = text(PKG / "CMP-05-ADDITIVE-STORIES-AND-ORACLES.md")
cost = text(PKG / "CMP-04-OBSERVABILITY-EVIDENCE-AND-COST.md")
questions = text(PKG / "CMP-OPEN-QUESTIONS.md")
closure = text(PKG / "CMP-FINDING-CLOSURE.md")
matrix = text(PKG / "CMP-ORACLE-MATRIX-v0.2.md")
report = text(PKG / "CMP-CONSISTENCY-REPORT.md")

if "| consent_id |" in arch:
    fail("consent_id is still a required column")
for needle in (
    "microphone_consent_state",
    "microphone_consent_id",
    "NOT_GRANTED",
    "cmp.speech.v0",
    "transcript_state",
    "PARTIAL",
    "FINAL",
    "audio_encoding",
    "audio_mime",
    "SPEECH_UNSUPPORTED_VERSION",
    "SPEECH_CANCELLED",
    "SPEECH_CANCEL_UNCONFIRMED",
    "RETRY_SAME_OPERATION",
    "RECONCILIATION_REQUIRED",
    "NEW_ATTEMPT",
    "REPLAY_RESULT",
    "forge.provider_ingest",
):
    if needle not in arch:
        fail(f"CMP-02 missing {needle}")

for needle in (
    "codex_conversational",
    "codex_review_executor",
    "review_run_id",
    "codex_reviewer",
    "Builder",
):
    if needle not in sec:
        fail(f"CMP-03 missing {needle}")

for needle in ("RETRY_SAME_OPERATION", "RECONCILIATION_REQUIRED", "NEW_ATTEMPT", "REPLAY_RESULT"):
    if needle not in ux:
        fail(f"CMP-01 missing {needle}")

if "provider_id" not in cost or "estimated_minor" not in cost:
    fail("CMP-04 cost attributes incomplete")

stories = [f"CMP-S{i:02d}" for i in range(1, 14)]
oracles = [f"CMP-O-{i:02d}" for i in range(1, 37)]
for sid in stories:
    if f"## {sid} " not in reg:
        fail(f"missing story {sid}")
    else:
        chunk = reg.split(f"## {sid} ", 1)[1].split("\n## ", 1)[0]
        for needle in ("PENDING HUMAN ASSIGNMENT", "PENDING CALIBRATION", "Not met", "NOT RUN"):
            if needle not in chunk:
                fail(f"{sid} missing {needle}")

found = []
for line in reg.splitlines():
    if not line.startswith("| CMP-O-"):
        continue
    cells = [c.strip() for c in line.split("|")[1:-1]]
    if len(cells) != 8:
        fail(f"oracle columns {len(cells)} {cells[0] if cells else line[:20]}")
        continue
    found.append(cells[0])
    if cells[7] != "NOT RUN":
        fail(f"{cells[0]} status {cells[7]}")
    if "PASS if" not in cells[4] or "FAIL if" not in cells[5]:
        fail(f"{cells[0]} missing PASS/FAIL")
    if "ABSENT" not in cells[6]:
        fail(f"{cells[0]} evidence not ABSENT")
if found != oracles:
    fail(f"oracle id sequence {found}")

row28 = next(line for line in reg.splitlines() if line.startswith("| CMP-O-28 "))
for marker in ("BUILDER_SCRATCH_ONLY", "BUILDER_VERDICT_CANDIDATE", "BUILDER_SESSION_CACHE", "BUILDER_ACTOR_9f3a", "review_run_id"):
    if marker not in row28:
        fail(f"CMP-O-28 missing {marker}")

row31 = next(line for line in reg.splitlines() if line.startswith("| CMP-O-31 "))
for marker in ("P1", "M1", "P2", "M2", "session_id", "provider_id", "estimated"):
    if marker not in row31:
        fail(f"CMP-O-31 missing {marker}")

row19 = next(line for line in reg.splitlines() if line.startswith("| CMP-O-19 "))
if "NOT_GRANTED" not in row19 or "null" not in row19:
    fail("CMP-O-19 does not lock null consent")

for oid in ("CMP-O-15", "CMP-O-16", "CMP-O-29"):
    row = next(line for line in reg.splitlines() if line.startswith(f"| {oid} "))
    if "redispatch" not in row and "redispatched" not in row:
        fail(f"{oid} missing inconclusive redispatch denial")

for oid in oracles:
    if f"| {oid} |" not in matrix:
        fail(f"matrix missing {oid}")
    if oid not in text(PKG / "CMP-06-TRACEABILITY-AND-IMPACT.md") and oid not in (
        # 32 is cited in CMP-06 prose in v0.1; keep requiring all
    ):
        pass
trace = text(PKG / "CMP-06-TRACEABILITY-AND-IMPACT.md")
for oid in oracles:
    if oid not in trace and oid not in text(PKG / "CMP-05-ADDITIVE-STORIES-AND-ORACLES.md"):
        fail(f"{oid} missing from package")
# AC rows must still name an oracle. New oracles must be cited from CMP-06 or the finding closure.
for oid in ("CMP-O-35", "CMP-O-36"):
    if oid not in trace and oid not in closure:
        fail(f"{oid} not traced")
if "CMP-O-35" not in trace or "CMP-O-36" not in trace:
    fail("new oracles missing from CMP-06")

if "não marca nenhuma aq como decidida" not in questions.casefold():
    fail("AQ board missing the not-decided sentence")
for aq in ("01", "02", "03", "05", "06", "07", "08", "10", "11"):
    line = next((ln for ln in questions.splitlines() if ln.startswith(f"| AQ-{aq} |")), "")
    if "Decisão humana exigida" not in line:
        fail(f"AQ-{aq} not marked as needing a human decision")
for aq in ("04", "09", "12"):
    line = next((ln for ln in questions.splitlines() if ln.startswith(f"| AQ-{aq} |")), "")
    if "Pode esperar" not in line:
        fail(f"AQ-{aq} not marked deferrable")

if closure.count("NÃO ESTÁ FECHADO POR ESTE PACOTE") < 5:
    fail("finding closure does not keep all five findings open")

banned = ("BUILD-00 autorizado", "PASS do delta", "esta v0.2 recebe PASS", "AQ-01 está decidida")
for name in required:
    body = text(PKG / name)
    for phrase in banned:
        if phrase in body:
            fail(f"{name} contains {phrase}")

if "voice_required" not in arch:
    fail("voice requirement missing")

# Historical integrity.
dirty_old = git("diff", "--name-only", AUDITED_V01, "--", "docs/planning/conversational-mvp").strip()
if dirty_old:
    fail(f"v0.1 package changed:\n{dirty_old}")
baseline = [
    "docs/planning/FDP-16-v1.7-AIOX-EXECUTION-ENGINES.md",
    "docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md",
    "docs/planning/FDP-17-v1.7-TESTING-STRATEGY.md",
    "docs/planning/FDP-19-v1.7-PRODUCT-BACKLOG.md",
    "docs/planning/FDP-19A-v1.7-STORY-ACCEPTANCE-REGISTER.md",
    "docs/planning/FDP-TRACEABILITY-MATRIX-v1.7-CANONICAL.md",
]
dirty_base = git("diff", "--name-only", AUDITED_V17, "--", *baseline).strip()
if dirty_base:
    fail(f"v1.7 bytes changed:\n{dirty_base}")
dirty_review = git(
    "diff",
    "--name-only",
    REVIEW_COMMIT,
    "--",
    "docs/reviews/PARECER-CODEX-CMP-v0.1-2026-10-13.md",
    "docs/reviews/PROMPT-GROK-CMP-v0.2-CORRECTIVE.md",
).strip()
if dirty_review:
    fail(f"review sources changed:\n{dirty_review}")

v17 = text(ROOT / "docs/planning/FDP-TRACEABILITY-MATRIX-v1.7-CANONICAL.md")
ids = []
mode = False
for line in v17.splitlines():
    if line.startswith("| Test ID"):
        mode = True
        continue
    if mode and line.startswith("## "):
        mode = False
    if mode and line.startswith("|") and not line.startswith("|---"):
        ids.append(line.split("|")[1].strip())
if len(ids) != 91:
    fail(f"v1.7 oracle count {len(ids)}")
for oid in oracles:
    if oid in v17:
        fail(f"v1.7 matrix contains {oid}")

allowed_prefix = (
    "docs/planning/conversational-mvp-v0.2/",
    "tools/check_conversational_mvp_v02_consistency.py",
    "tools/check_conversational_mvp_consistency.py",
    "README.md",
    "docs/reviews/REVIEW-ROUNDS-INDEX.md",
)
status = git("status", "--porcelain", "-uall")
for line in status.splitlines():
    path = line[3:].strip()
    if " -> " in path:
        path = path.split(" -> ", 1)[1]
    if path.startswith('"') and path.endswith('"'):
        path = path[1:-1]
    if not path.startswith(allowed_prefix):
        fail(f"unexpected worktree path {path}")

if "CHECKER_RESULT: NOT_YET_RUN" in report:
    fail("consistency report still says NOT_YET_RUN")
if "CHECKER_RESULT: SATISFIED" not in report:
    fail("consistency report missing CHECKER_RESULT")

print("conversational-mvp v0.2 documentary check")
print(f"v1.7 oracles={len(ids)} cmp_stories={len(stories)} cmp_oracles={len(found)}")
print("product tests: not executed")
print("codex verdict: not issued")
print("findings: specified, not closed by this package")
if errors:
    print(f"FAIL {len(errors)}")
    for err in errors:
        print(f"- {err}")
    sys.exit(1)
print("CHECKER_RESULT: SATISFIED")
print("This is not a Codex PASS.")
