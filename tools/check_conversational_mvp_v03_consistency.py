#!/usr/bin/env python3
"""Documentary consistency check for DELTA CONVERSATIONAL-MVP v0.3.

Does not execute product code, providers, database, staging, or voice APIs.
Does not emit a Codex verdict and does not close HIGH-01.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / "docs/planning/conversational-mvp-v0.2"
PKG = ROOT / "docs/planning/conversational-mvp-v0.3"
ENV = os.environ.copy()
ENV["GIT_DISCOVERY_ACROSS_FILESYSTEM"] = "1"

AUDITED_V17 = "0c42373d583dec420348efd7bc0b8c6228a66f47"
AUDITED_V01 = "cad1ac6d6bb8a970165ebd17ce1bff13d98af806"
AUDITED_V02 = "99474da514419a26ac8471c50c33697ade2a1cde"
REVIEW_COMMIT = "e60cefd0be07a7ad6423ce4d9bd5e3ab0b268741"

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], env=ENV, text=True)


def oracle_rows(path: Path) -> dict[str, str]:
    out = {}
    for line in text(path).splitlines():
        if line.startswith("| CMP-O-"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) != 8:
                fail(f"{path.name} columns {len(cells)} {cells[0] if cells else '?'}")
                continue
            out[cells[0]] = line
            if cells[7] != "NOT RUN":
                fail(f"{cells[0]} status {cells[7]}")
            if "PASS if" not in cells[4] or "FAIL if" not in cells[5]:
                fail(f"{cells[0]} missing PASS/FAIL")
            if "ABSENT" not in cells[6]:
                fail(f"{cells[0]} evidence not ABSENT")
    return out


for name in (
    "CMP-00-PACKAGE-INDEX.md",
    "CMP-05-ADDITIVE-STORIES-AND-ORACLES.md",
    "CMP-AQ-FOUNDER-DECISIONS.md",
    "CMP-CHANGE-REPORT.md",
    "CMP-FINDING-CLOSURE.md",
    "CMP-STATUS-INDEX.md",
    "CMP-CONSISTENCY-REPORT.md",
):
    body = text(PKG / name)
    if "CANDIDATE FOR CODEX REVIEW" not in body:
        fail(f"{name} missing candidate banner")
    if "DELTA CONVERSATIONAL-MVP v0.2 —" in body:
        fail(f"{name} still stamped as the v0.2 candidate")

reg = text(PKG / "CMP-05-ADDITIVE-STORIES-AND-ORACLES.md")
for i in range(1, 14):
    sid = f"CMP-S{i:02d}"
    if f"## {sid} " not in reg:
        fail(f"missing {sid}")
    else:
        chunk = reg.split(f"## {sid} ", 1)[1].split("\n## ", 1)[0]
        for needle in ("PENDING HUMAN ASSIGNMENT", "PENDING CALIBRATION", "Not met", "NOT RUN"):
            if needle not in chunk:
                fail(f"{sid} missing {needle}")

old_rows = oracle_rows(OLD / "CMP-05-ADDITIVE-STORIES-AND-ORACLES.md")
new_rows = oracle_rows(PKG / "CMP-05-ADDITIVE-STORIES-AND-ORACLES.md")
expect = [f"CMP-O-{i:02d}" for i in range(1, 37)]
if list(old_rows) != expect or list(new_rows) != expect:
    fail("oracle id sequence drifted")
for oid in expect:
    if oid != "CMP-O-28" and old_rows.get(oid) != new_rows.get(oid):
        fail(f"{oid} changed from the closed v0.2 text")

row = new_rows.get("CMP-O-28", "")
for needle in (
    "BUILDER_SCRATCH_ONLY",
    "BUILDER_VERDICT_CANDIDATE",
    "BUILDER_SESSION_CACHE",
    "BUILDER_ACTOR_9f3a",
    "BUILDER_TOOL_STATE",
    "BUILDER_RUNTIME_ID",
    "BUILDER_PROCESS_ID",
    "BUILDER_AGENT_INSTANCE_ID",
    "BUILDER_CREDENTIAL_FINGERPRINT",
    "REVIEWER_CREDENTIAL_FINGERPRINT",
    "codex_reviewer",
    "even when the registered actor is codex_reviewer",
    "model-authored attestation",
    "host-attested",
    "raw secret",
):
    if needle not in row:
        fail(f"CMP-O-28 missing {needle}")

for name in (
    "CMP-01-PRD-UX-JOURNEYS.md",
    "CMP-02-SYSTEM-ARCHITECTURE.md",
    "CMP-03-SECURITY-PRIVACY-AND-REVIEW-INDEPENDENCE.md",
    "CMP-04-OBSERVABILITY-EVIDENCE-AND-COST.md",
):
    old = text(OLD / name)
    new = text(PKG / name).replace(
        "DELTA CONVERSATIONAL-MVP v0.3",
        "DELTA CONVERSATIONAL-MVP v0.2",
    )
    if old != new:
        fail(f"{name} is not a version-stamp copy of v0.2")

aq = text(PKG / "CMP-AQ-FOUNDER-DECISIONS.md")
if aq.count("ABERTO — NÃO DECIDIDO") != 9:
    fail("nine founder decisions are not all still open")
if aq.count("ABERTO — DIFERÍVEL, NÃO DECIDIDO") != 3:
    fail("three deferrable AQs are not still open")
if "não é decisão" not in aq.casefold() and "não é decisão" not in aq:
    fail("AQ table missing the not-a-decision sentence")
for aqid in ("AQ-01", "AQ-02", "AQ-03", "AQ-05", "AQ-06", "AQ-07", "AQ-08", "AQ-10", "AQ-11", "AQ-04", "AQ-09", "AQ-12"):
    if aqid not in aq or aqid not in text(PKG / "CMP-OPEN-QUESTIONS.md"):
        fail(f"{aqid} missing")

closure = text(PKG / "CMP-FINDING-CLOSURE.md")
if "NÃO ESTÁ FECHADO POR ESTE PACOTE" not in closure:
    fail("HIGH-01 marked closed by the package")
if "MEDIUM-01" not in closure or "LOW-01" not in closure:
    fail("closed findings not cited")

banned = (
    "BUILD-00 autorizado",
    "esta v0.3 recebe PASS",
    "HIGH-01 está fechado",
    "AQ-01 está decidida",
)
for path in PKG.glob("*.md"):
    body = text(path)
    for phrase in banned:
        if phrase in body:
            fail(f"{path.name} contains {phrase}")

if git("diff", "--name-only", AUDITED_V02, "--", "docs/planning/conversational-mvp-v0.2").strip():
    fail("v0.2 package bytes changed")
if git("diff", "--name-only", AUDITED_V01, "--", "docs/planning/conversational-mvp").strip():
    fail("v0.1 package bytes changed")
baseline = [
    "docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md",
    "docs/planning/FDP-TRACEABILITY-MATRIX-v1.7-CANONICAL.md",
    "docs/planning/FDP-19A-v1.7-STORY-ACCEPTANCE-REGISTER.md",
]
if git("diff", "--name-only", AUDITED_V17, "--", *baseline).strip():
    fail("v1.7 bytes changed")
if git(
    "diff",
    "--name-only",
    REVIEW_COMMIT,
    "--",
    "docs/reviews/PARECER-CODEX-CMP-v0.2-2026-10-13.md",
    "docs/reviews/PROMPT-GROK-CMP-v0.3-HIGH01-CLOSURE.md",
).strip():
    fail("v0.2 parecer or v0.3 prompt changed")

v17 = text(ROOT / "docs/planning/FDP-TRACEABILITY-MATRIX-v1.7-CANONICAL.md")
count = 0
mode = False
for line in v17.splitlines():
    if line.startswith("| Test ID"):
        mode = True
        continue
    if mode and line.startswith("## "):
        mode = False
    if mode and line.startswith("|") and not line.startswith("|---"):
        count += 1
if count != 91:
    fail(f"v1.7 oracle count {count}")

report = text(PKG / "CMP-CONSISTENCY-REPORT.md")
if "CHECKER_RESULT: NOT_YET_RUN" in report:
    fail("consistency report still says NOT_YET_RUN")
if "CHECKER_RESULT: SATISFIED" not in report:
    fail("consistency report missing CHECKER_RESULT")

allowed = (
    "docs/planning/conversational-mvp-v0.3/",
    "tools/check_conversational_mvp_v03_consistency.py",
    "tools/check_conversational_mvp_v02_consistency.py",
    "tools/check_conversational_mvp_consistency.py",
    "README.md",
    "docs/reviews/REVIEW-ROUNDS-INDEX.md",
)
for line in git("status", "--porcelain", "-uall").splitlines():
    path = line[3:].strip()
    if " -> " in path:
        path = path.split(" -> ", 1)[1]
    if not path.startswith(allowed):
        fail(f"unexpected worktree path {path}")

print("conversational-mvp v0.3 documentary check")
print(f"v1.7 oracles={count} cmp_stories=13 cmp_oracles={len(new_rows)} changed_oracle=CMP-O-28")
print("product tests: not executed")
print("codex verdict: not issued")
print("HIGH-01: oracle amended, not closed by this package")
if errors:
    print(f"FAIL {len(errors)}")
    for err in errors:
        print(f"- {err}")
    sys.exit(1)
print("CHECKER_RESULT: SATISFIED")
print("This is not a Codex PASS.")
