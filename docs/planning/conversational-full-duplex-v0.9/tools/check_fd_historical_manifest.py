#!/usr/bin/env python3
"""Compare historical blobs at base_sha and parent_sha.

Without --repo this does not open either commit and exits 2 as NOT_RUN.
With --repo it reads git objects only. It does not declare PASS.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "fixtures" / "CMP-FD-FX-04-historical-manifest.json"
BASE = "9fd88bb03e4cca4a1ee5126d5b595e028e2602b2"
PARENT = "aca5101d3684109175269b36c3cace2051a71c91"


def fail(code):
    print(code)
    return 1


def git(repo, *args):
    return subprocess.check_output(["git", "-C", repo, *args])


def paths_at(repo, rev):
    out = git(repo, "ls-tree", "-r", "--name-only", rev).decode()
    found = []
    for line in out.splitlines():
        if line.startswith("docs/planning/conversational-full-duplex/"):
            found.append(line)
        else:
            parts = line.split("/")
            if len(parts) > 2 and parts[2] in {f"conversational-full-duplex-v0.{i}" for i in range(2, 9)}:
                found.append(line)
    return found


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=str(DEFAULT))
    parser.add_argument("--repo", default="")
    args = parser.parse_args()
    doc = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    if doc.get("schema") != "cmp.fd.historical-manifest.v0.9":
        return fail("FAIL_SCHEMA")
    if doc.get("base_sha") != BASE or doc.get("parent_sha") != PARENT:
        return fail("FAIL_SHA")
    if doc.get("v0_1_included") is not True:
        return fail("FAIL_V01")
    if doc.get("v0_5_v0_6_statement") != "v0.5/v0.6 candidatos, sem parecer independente incorporado":
        return fail("FAIL_STATEMENT")
    if "same_at_base_and_parent" in doc:
        return fail("FAIL_BOOLEAN_EVIDENCE")
    chain = {row["package"]: row for row in doc["parecer_chain"]}
    for missing in ("v0.5", "v0.6"):
        if chain[missing]["parecer_incorporated"] is not False or chain[missing]["verdict"] is not None:
            return fail("FAIL_INVENTED_PARECER")
    if chain["v0.8"]["present_in_base_commit"] is not False:
        return fail("FAIL_V08_PARECER_PLACEMENT")
    if chain["v0.8"]["present_in_parent_commit"] is not True:
        return fail("FAIL_V08_PARECER_PLACEMENT")
    if chain["v0.8"]["audited_sha"] != BASE or chain["v0.8"]["verdict"] != "FAIL DOCUMENT-ONLY":
        return fail("FAIL_VERDICT")
    seen = []
    v01 = 0
    for row in doc["files"]:
        if "same_at_base_and_parent" in row:
            return fail("FAIL_BOOLEAN_EVIDENCE")
        for key in ("base_sha256", "parent_sha256", "base_git_blob", "parent_git_blob"):
            if not isinstance(row.get(key), str) or len(row[key]) < 40:
                return fail("FAIL_HASH_ROW")
        if len(row["base_sha256"]) != 64 or len(row["parent_sha256"]) != 64:
            return fail("FAIL_HASH_ROW")
        if row["path"] in seen:
            return fail("FAIL_DUP_PATH")
        seen.append(row["path"])
        if row["path"].startswith("docs/planning/conversational-full-duplex/"):
            v01 += 1
        if "/conversational-full-duplex-v0.9/" in row["path"]:
            return fail("FAIL_SELF_HASH")
    if v01 < 1:
        return fail("FAIL_V01")
    absent = doc.get("full_duplex_prompts_absent") or []
    if "docs/reviews/PROMPT-GROK-FULL-DUPLEX-v0.6-CORRECTIVE.md" not in absent:
        return fail("FAIL_PROMPT_CHAIN")
    if "docs/reviews/PROMPT-GROK-FULL-DUPLEX-v0.7-CORRECTIVE.md" not in absent:
        return fail("FAIL_PROMPT_CHAIN")
    if not args.repo:
        print("GIT_BLOB_COMPARE NOT_RUN")
        return 2
    base_paths = paths_at(args.repo, doc["base_sha"])
    parent_paths = paths_at(args.repo, doc["parent_sha"])
    if base_paths != parent_paths:
        return fail("FAIL_PATH_SET")
    if base_paths != [row["path"] for row in doc["files"]]:
        print("manifest", len(doc["files"]), "git", len(base_paths))
        return fail("FAIL_PATH_SET")
    reviews = git(args.repo, "ls-tree", "-r", "--name-only", doc["parent_sha"], "docs/reviews").decode().splitlines()
    base_reviews = git(args.repo, "ls-tree", "-r", "--name-only", doc["base_sha"], "docs/reviews").decode().splitlines()
    for name in absent:
        if name in reviews or name in base_reviews:
            return fail("FAIL_UNEXPECTED_PROMPT")
    for name in (
        "docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.5-2026-10-14.md",
        "docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.6-2026-10-15.md",
    ):
        if name in reviews or name in base_reviews:
            return fail("FAIL_UNEXPECTED_PARECER")
    for row in doc["files"]:
        for rev, blob_key, hash_key in (
            (doc["base_sha"], "base_git_blob", "base_sha256"),
            (doc["parent_sha"], "parent_git_blob", "parent_sha256"),
        ):
            blob = git(args.repo, "rev-parse", f"{rev}:{row['path']}").decode().strip()
            data = git(args.repo, "cat-file", "blob", f"{rev}:{row['path']}")
            digest = hashlib.sha256(data).hexdigest()
            if blob != row[blob_key] or digest != row[hash_key]:
                print(row["path"], rev)
                return fail("FAIL_BLOB")
            if row["base_sha256"] != row["parent_sha256"] or row["base_git_blob"] != row["parent_git_blob"]:
                return fail("FAIL_BLOB_MISMATCH")
    print(f"REHASHED {len(doc['files'])} paths at both commits")
    print("v0.1_included=YES")
    print("v0.5_parecer=ABSENT")
    print("v0.6_parecer=ABSENT")
    print("GIT_BLOB_COMPARE MATCH READ_ONLY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
