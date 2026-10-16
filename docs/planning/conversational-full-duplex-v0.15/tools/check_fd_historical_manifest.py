#!/usr/bin/env python3
"""Compare planning blobs at base_sha and parent_sha, and read parecer bytes.

Without --repo this does not open either commit and exits 2 as NOT_RUN.
It does not declare PASS. A nomenclature conflict is reported as NOT_VERIFIED.
Builder output is not an independent audit. v0.2 stays NOT_VERIFIED.
Duplicate JSON keys are rejected before any blob comparison.
"""
import argparse
import copy
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "fixtures" / "CMP-FD-FX-04-historical-manifest.json"
BASE = "2b2adf382b17a22f1372aaf05b7d3bd1a6ba14ba"
PARENT = "2b2adf382b17a22f1372aaf05b7d3bd1a6ba14ba"
PACKAGES = [f"v0.{i}" for i in range(1, 15)]
ABSENT_PACKAGES = {"v0.5", "v0.6"}
NO_PARECER_YET = {"v0.14"}
SHA_RE = re.compile(
    r"\*\*(SHA congelado auditado|SHA declarado do checkout|SHA auditado|Checkout submetido|Checkout auditado|Checkout examinado):\*\*\s*`([0-9a-f]{40})`"
)
HEADER_RE = re.compile(r"\*\*(Veredito exclusivo|Veredito):\*\*\s*\*\*(.+?)\*\*")
FINAL_RE = re.compile(r"\*\*Veredito final:\s*(.+?)\.\*\*")
PATH_RE = re.compile(r"^docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0\.(\d+)-(\d{4}-\d{2}-\d{2})\.md$")


class DuplicateKeyError(ValueError):
    pass


def strict_pairs(pairs):
    found = {}
    for key, value in pairs:
        if key in found:
            raise DuplicateKeyError(key)
        found[key] = value
    return found


def load_strict_text(text):
    try:
        return json.loads(text, object_pairs_hook=strict_pairs), None
    except DuplicateKeyError:
        return None, "FAIL_DUPLICATE_KEY"
    except json.JSONDecodeError:
        return None, "FAIL_SCHEMA"


def inject_duplicate_key(text):
    index = text.find("{")
    if index < 0:
        raise ValueError("not-object")
    return text[:index + 1] + '"__duplicate_probe": 1, "__duplicate_probe": 2,' + text[index + 1:]


def fail(code):
    print(code)
    return code


def git(repo, *args):
    return subprocess.check_output(["git", "-C", repo, *args])


def exists(repo, rev, path):
    probe = subprocess.run(
        ["git", "-C", repo, "cat-file", "-e", f"{rev}:{path}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return probe.returncode == 0


def extract_parecer(text):
    sha_hits = SHA_RE.findall(text)
    header_hits = HEADER_RE.findall(text)
    finals = FINAL_RE.findall(text)
    sha_values = {item[1] for item in sha_hits}
    sha_labels = {item[0] for item in sha_hits}
    header_labels = {item[0] for item in header_hits}
    header_verdicts = {item[1] for item in header_hits}
    final_verdicts = set(finals)
    sha_status = "VERIFIED" if len(sha_values) == 1 and len(sha_labels) == 1 else "NOT_VERIFIED"
    if len(header_verdicts) == 1 and len(header_labels) == 1 and (not final_verdicts or final_verdicts == header_verdicts):
        verdict_status = "VERIFIED"
    else:
        verdict_status = "NOT_VERIFIED"
    return {
        "sha_label": next(iter(sha_labels)) if len(sha_labels) == 1 else None,
        "audited_sha": next(iter(sha_values)) if len(sha_values) == 1 else None,
        "sha_status": sha_status,
        "verdict_label": next(iter(header_labels)) if len(header_labels) == 1 else None,
        "header_verdict": next(iter(header_verdicts)) if len(header_verdicts) == 1 else None,
        "final_verdict": next(iter(final_verdicts)) if len(final_verdicts) == 1 else None,
        "verdict_status": verdict_status,
        "duplicate_header_count": len(header_hits),
    }


def planning_paths(repo, rev):
    out = git(repo, "ls-tree", "-r", "--name-only", rev).decode()
    found = []
    allowed = {f"conversational-full-duplex-v0.{i}" for i in range(2, 15)}
    for line in out.splitlines():
        if line.startswith("docs/planning/conversational-full-duplex/"):
            found.append(line)
            continue
        parts = line.split("/")
        if len(parts) > 2 and parts[2] in allowed:
            found.append(line)
    return found


def reviews(repo, rev):
    return git(repo, "ls-tree", "-r", "--name-only", rev, "docs/reviews").decode().splitlines()


def verify(doc, repo):
    if doc.get("schema") != "cmp.fd.historical-manifest.v0.15":
        return "FAIL_SCHEMA"
    if doc.get("base_sha") != BASE or doc.get("parent_sha") != PARENT:
        return "FAIL_SHA"
    if doc.get("v0_1_included") is not True:
        return "FAIL_V01"
    if "same_at_base_and_parent" in doc:
        return "FAIL_BOOLEAN_EVIDENCE"
    chain = doc.get("parecer_chain")
    if not isinstance(chain, list):
        return "FAIL_SCHEMA"
    packages = [row.get("package") for row in chain]
    if packages != PACKAGES:
        return "FAIL_PARECER_OMITTED"
    for row in chain:
        if "same_at_base_and_parent" in row:
            return "FAIL_BOOLEAN_EVIDENCE"
        package = row["package"]
        if package in ABSENT_PACKAGES:
            if row.get("parecer_incorporated") is not False or row.get("path") is not None:
                return "FAIL_INVENTED_PARECER"
            if row.get("audited_sha") is not None or row.get("verdict_status") != "ABSENT_LEGITIMATE":
                return "FAIL_INVENTED_PARECER"
            if row.get("present_in_base_commit") is not False or row.get("present_in_parent_commit") is not False:
                return "FAIL_INVENTED_PARECER"
            continue
        if package in NO_PARECER_YET:
            if row.get("parecer_incorporated") is not False or row.get("path") is not None:
                return "FAIL_INVENTED_PARECER"
            if row.get("audited_sha") is not None or row.get("verdict_status") != "NOT_INCORPORATED":
                return "FAIL_INVENTED_PARECER"
            if row.get("present_in_base_commit") is not False or row.get("present_in_parent_commit") is not False:
                return "FAIL_INVENTED_PARECER"
            continue
        if row.get("parecer_incorporated") is not True or not isinstance(row.get("path"), str):
            return "FAIL_PARECER_PATH"
        match = PATH_RE.match(row["path"])
        if match is None or f"v0.{match.group(1)}" != package:
            return "FAIL_PARECER_PATH"
        for key in ("sha_status", "verdict_status", "present_in_base_commit", "present_in_parent_commit"):
            if key not in row:
                return "FAIL_SCHEMA"
    seen = []
    v01 = 0
    for row in doc["files"]:
        if "same_at_base_and_parent" in row:
            return "FAIL_BOOLEAN_EVIDENCE"
        for key in ("base_sha256", "parent_sha256", "base_git_blob", "parent_git_blob"):
            if not isinstance(row.get(key), str) or len(row[key]) < 40:
                return "FAIL_HASH_ROW"
        if len(row["base_sha256"]) != 64 or len(row["parent_sha256"]) != 64:
            return "FAIL_HASH_ROW"
        if isinstance(row.get("bytes"), bool) or not isinstance(row.get("bytes"), int) or row["bytes"] < 0:
            return "FAIL_SCHEMA"
        if row["path"] in seen:
            return "FAIL_DUP_PATH"
        seen.append(row["path"])
        if row["path"].startswith("docs/planning/conversational-full-duplex/"):
            v01 += 1
        if "/conversational-full-duplex-v0.15/" in row["path"]:
            return "FAIL_SELF_HASH"
    if v01 < 1:
        return "FAIL_V01"
    absent = doc.get("full_duplex_prompts_absent")
    if absent != [
        "docs/reviews/PROMPT-GROK-FULL-DUPLEX-v0.6-CORRECTIVE.md",
        "docs/reviews/PROMPT-GROK-FULL-DUPLEX-v0.7-CORRECTIVE.md",
    ]:
        return "FAIL_PROMPT_CHAIN"
    if not isinstance(doc.get("full_duplex_prompts_present_at_parent"), list):
        return "FAIL_SCHEMA"
    gov = doc.get("v0_2_resolution")
    if not isinstance(gov, dict):
        return "FAIL_SCHEMA"
    for key in (
        "status", "verdict_status", "header_verdict", "final_verdict", "chosen_verdict",
        "blob_path", "git_blob", "sha256", "authority", "approval",
    ):
        if key not in gov:
            return "FAIL_SCHEMA"
    v02 = next(row for row in chain if row["package"] == "v0.2")
    if gov["status"] != "PENDING_HUMAN_APPROVAL" or gov["approval"] != "PENDING" or gov["chosen_verdict"] is not None:
        return "FAIL_NOMENCLATURE"
    if gov["verdict_status"] != "NOT_VERIFIED" or v02.get("verdict_status") != "NOT_VERIFIED":
        return "FAIL_NOMENCLATURE"
    if gov["header_verdict"] != v02.get("header_verdict") or gov["final_verdict"] != v02.get("final_verdict"):
        return "FAIL_NOMENCLATURE"
    if gov["header_verdict"] != "FAIL" or gov["blob_path"] != v02.get("path"):
        return "FAIL_NOMENCLATURE"
    if repo is None:
        return "NOT_RUN"
    base_paths = planning_paths(repo, doc["base_sha"])
    parent_paths = planning_paths(repo, doc["parent_sha"])
    if base_paths != parent_paths or base_paths != [row["path"] for row in doc["files"]]:
        return "FAIL_PATH_SET"
    base_reviews = reviews(repo, doc["base_sha"])
    parent_reviews = reviews(repo, doc["parent_sha"])
    for name in absent:
        if name in base_reviews or name in parent_reviews:
            return "FAIL_UNEXPECTED_PROMPT"
    present = sorted(path for path in parent_reviews if "PROMPT-GROK-FULL-DUPLEX-" in path)
    if present != doc["full_duplex_prompts_present_at_parent"]:
        invented = [path for path in doc["full_duplex_prompts_present_at_parent"] if path not in present]
        if invented:
            return "FAIL_PROMPT_INVENTED"
        return "FAIL_PROMPT_SET"
    for path in (
        "docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.5-2026-10-14.md",
        "docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.6-2026-10-15.md",
    ):
        if path in base_reviews or path in parent_reviews:
            return "FAIL_UNEXPECTED_PARECER"
    for prefix in ("PARECER-CODEX-FULL-DUPLEX-v0.5", "PARECER-CODEX-FULL-DUPLEX-v0.6"):
        if any(prefix in path for path in base_reviews + parent_reviews):
            return "FAIL_UNEXPECTED_PARECER"
    for row in doc["files"]:
        for rev, blob_key, hash_key in (
            (doc["base_sha"], "base_git_blob", "base_sha256"),
            (doc["parent_sha"], "parent_git_blob", "parent_sha256"),
        ):
            blob = git(repo, "rev-parse", f"{rev}:{row['path']}").decode().strip()
            data = git(repo, "cat-file", "blob", f"{rev}:{row['path']}")
            digest = hashlib.sha256(data).hexdigest()
            if blob != row[blob_key] or digest != row[hash_key]:
                return "FAIL_BLOB"
            if len(data) != row["bytes"]:
                return "FAIL_BYTES"
            if row["base_sha256"] != row["parent_sha256"] or row["base_git_blob"] != row["parent_git_blob"]:
                return "FAIL_BLOB_MISMATCH"
    for row in chain:
        if row["package"] in ABSENT_PACKAGES or row["package"] in NO_PARECER_YET:
            if row["package"] in NO_PARECER_YET:
                prefix = f"PARECER-CODEX-FULL-DUPLEX-{row['package']}"
                for rev in (doc["base_sha"], doc["parent_sha"]):
                    if any(prefix in path for path in reviews(repo, rev)):
                        return "FAIL_INVENTED_PARECER"
            continue
        path = row["path"]
        for rev, flag in ((doc["base_sha"], "present_in_base_commit"), (doc["parent_sha"], "present_in_parent_commit")):
            found = exists(repo, rev, path)
            if found != row[flag]:
                return "FAIL_PARECER_PATH"
        if not row["present_in_base_commit"] and not row["present_in_parent_commit"]:
            return "FAIL_PARECER_PATH"
        rev = doc["parent_sha"] if row["present_in_parent_commit"] else doc["base_sha"]
        text = git(repo, "cat-file", "blob", f"{rev}:{path}").decode("utf-8")
        found = extract_parecer(text)
        if row["present_in_base_commit"] and row["present_in_parent_commit"]:
            other = git(repo, "cat-file", "blob", f"{doc['base_sha']}:{path}").decode("utf-8")
            if extract_parecer(other) != found:
                return "FAIL_PARECER_SHA"
        for key in ("sha_label", "audited_sha", "sha_status", "verdict_label", "header_verdict", "final_verdict", "verdict_status", "duplicate_header_count"):
            if row.get(key) != found[key]:
                if key == "verdict_status" and found["verdict_status"] == "NOT_VERIFIED":
                    return "FAIL_NOMENCLATURE"
                if key in {"audited_sha", "sha_status", "sha_label"}:
                    return "FAIL_PARECER_SHA"
                if key in {"header_verdict", "final_verdict", "verdict_status", "verdict_label"}:
                    return "FAIL_PARECER_VERDICT"
                return "FAIL_PARECER_PATH"
        if found["verdict_status"] == "NOT_VERIFIED" and row["verdict_status"] != "NOT_VERIFIED":
            return "FAIL_NOMENCLATURE"
        if found["sha_status"] != "VERIFIED":
            return "FAIL_PARECER_SHA"
        if row["package"] == "v0.2":
            blob = git(repo, "rev-parse", f"{rev}:{path}").decode().strip()
            raw = git(repo, "cat-file", "blob", f"{rev}:{path}")
            if blob != gov["git_blob"] or hashlib.sha256(raw).hexdigest() != gov["sha256"]:
                return "FAIL_BLOB"
    return None


def negative_mutations(doc, repo):
    checks = []

    def expect(mutated, code):
        got = verify(mutated, repo)
        checks.append(got == code)
        if got != code:
            print("negative", code, got)

    mutated = copy.deepcopy(doc)
    mutated["parecer_chain"][6]["audited_sha"] = "0" * 40
    expect(mutated, "FAIL_PARECER_SHA")
    mutated = copy.deepcopy(doc)
    mutated["parecer_chain"][6]["header_verdict"] = "PASS"
    expect(mutated, "FAIL_PARECER_VERDICT")
    mutated = copy.deepcopy(doc)
    mutated["parecer_chain"][6]["path"] = "docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.7-1999-01-01.md"
    expect(mutated, "FAIL_PARECER_PATH")
    mutated = copy.deepcopy(doc)
    del mutated["parecer_chain"][3]
    expect(mutated, "FAIL_PARECER_OMITTED")
    mutated = copy.deepcopy(doc)
    mutated["full_duplex_prompts_present_at_parent"] = list(doc["full_duplex_prompts_present_at_parent"]) + [
        "docs/reviews/PROMPT-GROK-FULL-DUPLEX-v0.6-CORRECTIVE.md"
    ]
    expect(mutated, "FAIL_PROMPT_INVENTED")
    mutated = copy.deepcopy(doc)
    mutated["parecer_chain"][4]["parecer_incorporated"] = True
    mutated["parecer_chain"][4]["path"] = "docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.5-2026-10-14.md"
    expect(mutated, "FAIL_INVENTED_PARECER")
    mutated = copy.deepcopy(doc)
    mutated["parecer_chain"][1]["verdict_status"] = "VERIFIED"
    expect(mutated, "FAIL_NOMENCLATURE")
    mutated = copy.deepcopy(doc)
    mutated["v0_2_resolution"]["chosen_verdict"] = "FAIL"
    expect(mutated, "FAIL_NOMENCLATURE")
    mutated = copy.deepcopy(doc)
    mutated["files"][0]["bytes"] = mutated["files"][0]["bytes"] + 1
    expect(mutated, "FAIL_BYTES")
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=str(DEFAULT))
    parser.add_argument("--repo", default="")
    args = parser.parse_args()
    text = Path(args.manifest).read_text(encoding="utf-8")
    doc, err = load_strict_text(text)
    if err:
        print(err)
        return 1
    mutated = inject_duplicate_key(text)
    _ignored, probe = load_strict_text(mutated)
    if probe != "FAIL_DUPLICATE_KEY":
        print("FAIL_DUPLICATE_KEY")
        return 1
    if not args.repo:
        code = verify(doc, None)
        if code not in (None, "NOT_RUN"):
            print(code)
            return 1
        print("DUPLICATE_KEY manifest=rejected")
        print("GIT_BLOB_COMPARE NOT_RUN")
        print("PARECER_CHAIN NOT_RUN")
        return 2
    code = verify(doc, args.repo)
    if code:
        print(code)
        return 1
    checks = negative_mutations(doc, args.repo)
    if not checks or not all(checks):
        print("FAIL_NEGATIVE")
        return 1
    print(f"REHASHED {len(doc['files'])} paths at both commits")
    print("v0.1_included=YES")
    for row in doc["parecer_chain"]:
        if row["package"] in ABSENT_PACKAGES:
            print(f"PARECER {row['package']} ABSENT_LEGITIMATE")
        elif row["package"] in NO_PARECER_YET:
            print(f"PARECER {row['package']} NOT_INCORPORATED")
        else:
            print(f"PARECER {row['package']} sha={row['sha_status']} verdict={row['verdict_status']}")
    print("PROMPT_SET MATCH")
    print("NEGATIVE sha=rejected verdict=rejected path=rejected omission=rejected invented_prompt=rejected invented_parecer=rejected nomenclature=rejected bytes=rejected")
    print("PLANNING_BLOBS MATCH READ_ONLY")
    print("BYTES MATCH")
    print("PARECER_CHAIN NOT_FULLY_VERIFIED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
