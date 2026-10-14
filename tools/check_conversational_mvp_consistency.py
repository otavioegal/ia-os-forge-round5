#!/usr/bin/env python3
"""Documentary consistency check for DELTA CONVERSATIONAL-MVP v0.1.

Does not execute product code, providers, database, staging, or voice APIs.
Does not emit a Codex verdict.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs/planning"
PKG = PLAN / "conversational-mvp"
ENV = os.environ.copy()
ENV["GIT_DISCOVERY_ACROSS_FILESYSTEM"] = "1"

AUDITED = "0c42373d583dec420348efd7bc0b8c6228a66f47"
PRE_DELTA = "acf9e9fd366d5e571e01a1b1a1a99be8fc276991"

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args],
        env=ENV,
        text=True,
    )


PKG_FILES = [
    "CMP-00-PACKAGE-INDEX.md",
    "CMP-01-PRD-UX-JOURNEYS.md",
    "CMP-02-SYSTEM-ARCHITECTURE.md",
    "CMP-03-SECURITY-PRIVACY-AND-REVIEW-INDEPENDENCE.md",
    "CMP-04-OBSERVABILITY-EVIDENCE-AND-COST.md",
    "CMP-05-ADDITIVE-STORIES-AND-ORACLES.md",
    "CMP-06-TRACEABILITY-AND-IMPACT.md",
    "CMP-OPEN-QUESTIONS.md",
    "CMP-RISKS.md",
    "CMP-CONSISTENCY-REPORT.md",
]

for name in PKG_FILES:
    if not (PKG / name).is_file():
        fail(f"missing {name}")

stories = [f"CMP-S{i:02d}" for i in range(1, 14)]
oracles = [f"CMP-O-{i:02d}" for i in range(1, 35)]
reg = text(PKG / "CMP-05-ADDITIVE-STORIES-AND-ORACLES.md") if (PKG / "CMP-05-ADDITIVE-STORIES-AND-ORACLES.md").is_file() else ""
trace = text(PKG / "CMP-06-TRACEABILITY-AND-IMPACT.md") if (PKG / "CMP-06-TRACEABILITY-AND-IMPACT.md").is_file() else ""

for sid in stories:
    if f"## {sid} " not in reg:
        fail(f"missing story heading {sid}")
    else:
        chunk = reg.split(f"## {sid} ", 1)[1].split("\n## ", 1)[0]
        for needle in ("PENDING HUMAN ASSIGNMENT", "PENDING CALIBRATION", "Not met", "NOT RUN"):
            if needle not in chunk:
                fail(f"{sid} missing {needle}")

found_oracles = []
for line in reg.splitlines():
    if line.startswith("| CMP-O-"):
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) != 8:
            fail(f"oracle column count {len(cells)} for {line[:24]}")
            continue
        found_oracles.append(cells[0])
        if cells[7] != "NOT RUN":
            fail(f"{cells[0]} status {cells[7]}")
        blob = " ".join(cells)
        for needle in ("PASS if", "FAIL if", "ABSENT"):
            if needle not in blob:
                fail(f"{cells[0]} missing {needle}")

if found_oracles != oracles:
    fail(f"oracle id sequence {found_oracles} != {oracles}")

for oid in oracles:
    if trace.count(oid) < 1:
        fail(f"CMP-06 does not cite {oid}")

for item in [f"FD-{i}" for i in range(1, 6)] + [f"AC-{i}" for i in range(1, 11)]:
    if f"| {item} |" not in trace:
        fail(f"CMP-06 missing row {item}")

if "FDP-11 gap" not in trace and "## 2. FDP-11 gap" not in trace:
    fail("FDP-11 gap section missing")

banned = (
    "this delta is PASS",
    "DELTA PASS",
    "PASS do delta",
    "BUILD-00 is authorized",
    "BUILD-00 autorizado",
    "voice provider chosen:",
    "provider selected:",
)
for path in PKG.glob("*.md"):
    body = text(path)
    if "CANDIDATE FOR CODEX REVIEW" not in body:
        fail(f"{path.name} missing candidate banner")
    for phrase in banned:
        if phrase in body:
            fail(f"{path.name} contains forbidden phrase {phrase}")

matrix_path = PLAN / "FDP-TRACEABILITY-MATRIX-v1.7-CANONICAL.md"
matrix = text(matrix_path)
ids = []
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
            fail(f"v1.7 column count {len(cells)}")
        else:
            ids.append(cells[0])
            if "NOT RUN" not in line:
                fail(f"v1.7 row not NOT RUN {cells[0]}")
if len(ids) != 91 or len(ids) != len(set(ids)):
    fail(f"v1.7 oracle count {len(ids)}")
for oid in oracles:
    if oid in matrix:
        fail(f"v1.7 matrix contains {oid}")

p0 = [
    "AUTH-01", "AUTHZ-01", "AUTHZ-02", "RLS-01", "FS-01", "FS-02", "TERM-01",
    "SEC-01", "SEC-02", "ENG-01", "ENG-02", "PREVIEW-01", "DEPLOY-01", "DEPLOY-02",
    "AUDIT-01", "COST-01", "STOP-01",
]
fdp17 = text(PLAN / "FDP-17-v1.7-TESTING-STRATEGY.md")
for pid in p0:
    if ids.count(pid) != 1:
        fail(f"matrix P0 {pid} count {ids.count(pid)}")
    if f"| {pid} |" not in fdp17:
        fail(f"FDP-17 missing {pid}")

story_reg = text(PLAN / "FDP-19A-v1.7-STORY-ACCEPTANCE-REGISTER.md")
f_count = sum(1 for line in story_reg.splitlines() if line.startswith("## F-"))
if f_count != 41:
    fail(f"F story count {f_count}")

fdp16a = text(PLAN / "FDP-16A-v1.7-EXECUTION-CONTRACTS.md")
states = "QUEUED, READY, RUNNING, WAITING, RETRYING, HANDOFF, REVIEWING, BLOCKED, COMPLETED, FAILED, CANCELLED"
if states not in fdp16a:
    fail("11 Task states missing")
if "forge.provider_ingest" not in fdp16a:
    fail("capturer sentence missing from v1.7")

# Worktree must not modify the audited baseline or the pre-delta governance sources.
baseline_paths = [
    "docs/planning/FDP-16-v1.7-AIOX-EXECUTION-ENGINES.md",
    "docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md",
    "docs/planning/FDP-17-v1.7-TESTING-STRATEGY.md",
    "docs/planning/FDP-18-v1.3-DEPLOYMENT-ROLLBACK.md",
    "docs/planning/FDP-18A-v1.3-RECOVERY-RUNBOOKS.md",
    "docs/planning/FDP-19-v1.7-PRODUCT-BACKLOG.md",
    "docs/planning/FDP-19A-v1.7-STORY-ACCEPTANCE-REGISTER.md",
    "docs/planning/FDP-20-v1.3-SPRINT-IMPLEMENTATION-PLAN.md",
    "docs/planning/FDP-ROUND10-STATUS-INDEX.md",
    "docs/planning/FDP-TRACEABILITY-MATRIX-v1.7-CANONICAL.md",
]
dirty = git("diff", "--name-only", AUDITED, "--", *baseline_paths).strip()
if dirty:
    fail(f"audited v1.7 bytes changed:\n{dirty}")

pre_delta_paths = [
    "docs/reviews/PARECER-CODEX-ROUND10-2026-10-13.md",
    "docs/governance/FOUNDER-DECISION-JARVIS-VOICE-ALL-AGENTS-MVP-2026-10-13.md",
    "docs/governance/IMPACT-ASSESSMENT-CONVERSATIONAL-MVP-2026-10-13.md",
    "docs/governance/PROMPT-GROK-CONVERSATIONAL-MVP-DELTA-v0.1.md",
    "docs/governance/ADDENDUM-CONVERSATIONAL-COUNCIL-JARVIS-2026-10-13.md",
    "historical",
]
dirty_pre = git("diff", "--name-only", PRE_DELTA, "--", *pre_delta_paths).strip()
if dirty_pre:
    fail(f"pre-delta sources changed:\n{dirty_pre}")

allowed_prefix = (
    "docs/planning/conversational-mvp/",
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

report = text(PKG / "CMP-CONSISTENCY-REPORT.md") if (PKG / "CMP-CONSISTENCY-REPORT.md").is_file() else ""
if "CHECKER_RESULT: NOT_YET_RUN" in report:
    fail("consistency report still says NOT_YET_RUN")
if "CHECKER_RESULT: SATISFIED" not in report and "CHECKER_RESULT: NOT_YET_RUN" not in report:
    fail("consistency report missing CHECKER_RESULT")

print("conversational-mvp documentary check")
print(f"v1.7 oracles={len(ids)} stories={f_count} p0={len(p0)} cmp_stories={len(stories)} cmp_oracles={len(found_oracles)}")
print("product tests: not executed")
print("codex verdict: not issued")
if errors:
    print(f"FAIL {len(errors)}")
    for err in errors:
        print(f"- {err}")
    sys.exit(1)
print("CHECKER_RESULT: SATISFIED")
print("This is not a Codex PASS.")
