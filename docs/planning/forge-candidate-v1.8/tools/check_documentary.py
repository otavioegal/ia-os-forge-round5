#!/usr/bin/env python3
"""Read-only structural check for the v1.8 review dossier.

This is not a product test. It does not open PostgreSQL, a provider, or a deploy.
A zero exit means the cited documents still contain the Round 5 corrections.
It does not mean PASS, READY FOR BUILD, or that any finding was closed.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
if len(sys.argv) == 3 and sys.argv[1] == "--repo":
    ROOT = Path(sys.argv[2]).resolve()

def read(rel):
    path = ROOT / rel
    if not path.is_file():
        print("MISSING", rel)
        return None
    return path.read_text(encoding="utf-8")

def main():
    problems = []
    reg = read("docs/planning/FDP-19A-v1.7-STORY-ACCEPTANCE-REGISTER.md")
    mat = read("docs/planning/FDP-TRACEABILITY-MATRIX-v1.7-CANONICAL.md")
    c16 = read("docs/planning/FDP-16A-v1.7-EXECUTION-CONTRACTS.md")
    f16 = read("docs/planning/FDP-16-v1.7-AIOX-EXECUTION-ENGINES.md")
    f17 = read("docs/planning/FDP-17-v1.7-TESTING-STRATEGY.md")
    f20 = read("docs/planning/FDP-20-v1.3-SPRINT-IMPLEMENTATION-PLAN.md")
    f15 = read("historical/round4/docs/planning/FDP-15-v1.0-INTEGRATION-ADAPTER-SPECIFICATION.md")
    f06 = read("historical/round4/docs/source-material/chat-extracts/FDP-06-v1.0__msg058.md")
    docs = [reg, mat, c16, f16, f17, f20, f15, f06]
    if any(item is None for item in docs):
        print("DOCUMENTARY_STRUCTURE_CHECK FAIL_MISSING")
        return 1
    rows = {}
    for line in mat.splitlines():
        if not line.startswith("| "):
            continue
        parts = [item.strip() for item in line.strip("|").split("|")]
        if len(parts) == 11 and re.match(r"^[A-Z][A-Z0-9-]*-\d+$", parts[0]):
            rows[parts[0]] = parts
    stories = []
    for block in re.split(r"\n(?=## F-)", reg):
        match = re.match(r"## (F-\d+)", block)
        if not match:
            continue
        sid = match.group(1)
        stories.append(sid)
        if "Inherited:" not in block and "- Inherited:" not in block:
            problems.append(sid + " sem fonte herdada")
        if "FDP-14 is not the source" not in block:
            problems.append(sid + " sem separacao FDP-14")
        if "FDP-15 remains pending" not in block and "Pending FDP-15" not in block:
            problems.append(sid + " sem separacao FDP-15")
        if "New in v1." not in block and "New proposal" not in block:
            problems.append(sid + " sem marca de proposta")
        if "Positive acceptance" not in block or "Negative acceptance" not in block:
            problems.append(sid + " sem aceite positivo e negativo")
        if "PENDING HUMAN ASSIGNMENT" not in block or "PENDING CALIBRATION" not in block:
            problems.append(sid + " DoR operacional alterado")
        tests = re.search(r"Tests: ([^\n]+)", block)
        if not tests:
            problems.append(sid + " sem testes")
            continue
        for tid in re.findall(r"[A-Z][A-Z0-9-]*-\d+", tests.group(1)):
            row = rows.get(tid)
            if row is None:
                problems.append(sid + " teste ausente " + tid)
                continue
            steps, positive, negative, status = row[5], row[6], row[7], row[10]
            if len(steps) < 8:
                problems.append(tid + " sem passos")
            if status != "NOT RUN":
                problems.append(tid + " status " + status)
            if tid == "PERF-01":
                if "no PASS" not in positive:
                    problems.append("PERF-01 mudou a recusa de meta")
                continue
            if "PASS" not in positive:
                problems.append(tid + " sem regra positiva")
            if "FAIL" not in negative and "FAIL" not in positive and tid != "PROD-05":
                problems.append(tid + " sem regra reprovada")
            if tid == "PROD-05" and "must not" not in negative:
                problems.append("PROD-05 sem negativo")
    if stories != [f"F-{i:03d}" for i in range(1, 42)]:
        problems.append("historias " + str(len(stories)))
    methods = [
        "start_task", "resume_task", "pause_task", "cancel_task", "get_status",
        "capture_checkpoint", "get_artifacts", "get_diff", "get_test_results",
        "describe", "health", "invoke", "cancel",
    ]
    adapt = rows.get("ADAPT-01")
    for name in methods:
        if name not in reg or name not in f15:
            problems.append("metodo ausente " + name)
        if adapt and name not in adapt[5] and name not in adapt[6] and name not in adapt[7]:
            if name not in (adapt[5] + adapt[6] + adapt[7]):
                problems.append("ADAPT-01 sem " + name)
    if "only supported orchestrator" in (f16 + reg).lower():
        problems.append("AIOX ainda como unica entrada")
    if "FORGE_DIRECT" not in f16 or "FORGE_DIRECT" not in reg:
        problems.append("fallback ausente")
    f06_lines = f06.splitlines()
    if "preferencial" not in f06_lines[371].lower():
        problems.append("FDP-06:372 mudou")
    if "PONTO ÚNICO" not in f06_lines[406] and "PONTO UNICO" not in f06_lines[406]:
        problems.append("FDP-06:407 mudou")
    for tid in [f"DEPLOY-{i:02d}" for i in range(2, 13)] + [f"LEDGER-{i:02d}" for i in range(1, 19)] + ["HANDOFF-01", "AIOX-01", "RHFT-01"]:
        if tid not in rows:
            problems.append("oraculo ausente " + tid)
    if "environment_id | uuid" not in c16:
        problems.append("environment_id nao e uuid")
    if "SETTLED, RELEASED, DENIED and CANCELLED" not in c16 and "SETTLED, RELEASED, DENIED e CANCELLED" not in c16:
        if "Terminal operation statuses are SETTLED, RELEASED, DENIED and CANCELLED" not in c16:
            problems.append("estados terminais ausentes")
    if "CHECKPOINT_INVALID" not in rows["HANDOFF-01"][7]:
        problems.append("HANDOFF sem digest invalido")
    if "Required: F-001" not in f20 or "F-039 is the derivation story" not in f20:
        problems.append("conjunto RHFT ausente")
    if "v1.6 matrix" not in f17.splitlines()[30]:
        problems.append("LOW-01 nao esta mais no arquivo auditado; nao editar FDP-17 por esta pasta")
    if "v1.7" not in f17.splitlines()[2]:
        problems.append("FDP-17:3 nao aponta a matriz v1.7")
    jarvis = [
        "docs/planning/conversational-full-duplex-v0.16/CMP-FD-02-CONVERSA-INDIVIDUAL.md",
        "docs/planning/conversational-full-duplex-v0.16/CMP-FD-03-SALA-DE-CONSELHO.md",
        "docs/planning/conversational-full-duplex-v0.16/CMP-FD-05-FALAR-ENQUANTO-RESPONDE.md",
        "docs/planning/conversational-full-duplex-v0.16/CMP-FD-06-TROCA-E-CONTINUIDADE.md",
        "docs/planning/conversational-full-duplex-v0.16/CMP-FD-07-TELAS-ESTADOS-FALHAS.md",
        "docs/planning/conversational-full-duplex-v0.16/CMP-FD-08-ACEITE-DO-FOUNDER.md",
    ]
    for rel in jarvis:
        text = read(rel)
        if text is None:
            problems.append("jarvis ausente")
            break
    print("DOCUMENTARY_STRUCTURE_CHECK")
    print("stories=%d/41" % len(stories))
    print("oracle_rows=%d" % len(rows))
    print("LOW-01_stale_sentence_still_in_FDP-17_line_31=yes")
    print("tests_executed=no")
    print("postgresql=not_used")
    print("problems=%d" % len(problems))
    for item in problems:
        print("PROBLEM", item)
    if problems:
        print("RESULT FAIL_STRUCTURE")
        return 1
    print("RESULT STRUCTURE_ONLY")
    print("NOT_PRODUCT_PASS")
    print("NOT_READY_FOR_BUILD")
    print("FINDINGS_NOT_CLOSED_BY_THIS_CHECK")
    return 0

if __name__ == "__main__":
    sys.exit(main())
