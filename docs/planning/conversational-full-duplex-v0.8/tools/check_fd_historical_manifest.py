#!/usr/bin/env python3
"""Read-only check of the historical SHA-256 manifest.

Recomputes sha256 when --root points at a clone. Does not audit, does not
declare PASS, and does not modify the clone.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "fixtures" / "CMP-FD-FX-04-historical-manifest.json"


def fail(code):
    print(code)
    return 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=str(DEFAULT))
    parser.add_argument("--root", default="")
    args = parser.parse_args()
    doc = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    if doc.get("schema") != "cmp.fd.historical-manifest.v0.8":
        return fail("FAIL_SCHEMA")
    if doc.get("base_sha") != "1a71dfa44fc2c88174c113e5c68eddc18d6cfad3":
        return fail("FAIL_BASE")
    if doc.get("v0_5_v0_6_statement") != "v0.5/v0.6 candidatos, sem parecer independente incorporado":
        return fail("FAIL_STATEMENT")
    if doc.get("historical_packages_identical") is not True:
        return fail("FAIL_NOT_IDENTICAL")
    chain = {row["package"]: row for row in doc["parecer_chain"]}
    for missing in ("v0.5", "v0.6"):
        row = chain[missing]
        if row.get("parecer_incorporated") is not False or row.get("verdict") is not None:
            return fail("FAIL_INVENTED_PARECER")
        if row.get("statement") != "candidato, sem parecer independente incorporado":
            return fail("FAIL_STATEMENT")
    for present in ("v0.1", "v0.2", "v0.3", "v0.4", "v0.7"):
        row = chain[present]
        if row.get("parecer_incorporated") is not True:
            return fail("FAIL_CHAIN")
        if "PASS" == row.get("verdict"):
            return fail("FAIL_FALSE_PASS")
        if not row.get("audited_sha") or not row.get("verdict"):
            return fail("FAIL_VERDICT")
    if chain["v0.7"]["present_in_base_commit"] is not False:
        return fail("FAIL_V07_PARECER_PLACEMENT")
    if chain["v0.7"]["audited_sha"] != doc["base_sha"]:
        return fail("FAIL_V07_SHA")
    seen = set()
    for row in doc["files"]:
        if row["path"] in seen:
            return fail("FAIL_DUP_PATH")
        seen.add(row["path"])
        if len(row["sha256"]) != 64 or row["same_at_base_and_parent"] is not True:
            return fail("FAIL_HASH_ROW")
        if not row["path"].startswith("docs/planning/conversational-full-duplex-v0."):
            return fail("FAIL_PATH_SCOPE")
        # v0.8 must not be hashed as if it were historical
        if "/conversational-full-duplex-v0.8/" in row["path"]:
            return fail("FAIL_SELF_HASH")
    if args.root:
        base = Path(args.root)
        for name in (
            "docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.5-2026-10-14.md",
            "docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.6-2026-10-14.md",
            "docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.5-2026-10-15.md",
            "docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.6-2026-10-15.md",
        ):
            if (base / name).exists():
                return fail("FAIL_UNEXPECTED_PARECER")
        # any filename containing the absent versions
        reviews = base / "docs" / "reviews"
        if reviews.is_dir():
            for path in reviews.iterdir():
                if "PARECER-CODEX-FULL-DUPLEX-v0.5" in path.name or "PARECER-CODEX-FULL-DUPLEX-v0.6" in path.name:
                    return fail("FAIL_UNEXPECTED_PARECER")
        for row in doc["files"]:
            target = base / row["path"]
            if not target.is_file():
                print(row["path"])
                return fail("FAIL_MISSING_FILE")
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            if digest != row["sha256"]:
                print(row["path"])
                return fail("FAIL_SHA256")
        print(f"REHASHED {len(doc['files'])} historical files")
    print("v0.5_parecer=ABSENT")
    print("v0.6_parecer=ABSENT")
    print("HISTORICAL_MANIFEST_MATCH READ_ONLY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
