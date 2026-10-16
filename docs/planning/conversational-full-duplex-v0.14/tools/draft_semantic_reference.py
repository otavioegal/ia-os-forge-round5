#!/usr/bin/env python3
"""Draft the v0.14 semantic reference from schema literals.

This file does not import check_fd_fx03_ack.py. It does not run mutations.
The result is a candidate anchor, not a human-ratified golden.
NEW-GOV-01 stays OPEN. PENDING_HUMAN_APPROVAL is not an invented approval.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "fixtures" / "CMP-FD-FX-03-ack.schema.json"
FIXTURE = ROOT / "fixtures" / "CMP-FD-FX-03-ack.json"
SYNTHETIC = ROOT / "fixtures" / "CMP-FD-FX-03-ack.synthetic.json"
OUT = ROOT / "fixtures" / "CMP-FD-FX-05-semantic-reference.json"


class DuplicateKeyError(ValueError):
    pass


def strict_pairs(pairs):
    found = {}
    for key, value in pairs:
        if key in found:
            raise DuplicateKeyError(key)
        found[key] = value
    return found


def load(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=strict_pairs)


def draft_bindings(spec):
    """Recursive literal inventory. The checker walks the same literals iteratively."""
    rows = []

    def add(prefix, constraint, expected):
        rows.append({
            "path": f"{prefix}.{constraint}",
            "constraint": constraint,
            "expected": expected,
        })

    def walk_rule(prefix, rule):
        if "type" in rule:
            add(prefix, "type", rule["type"])
        if "const" in rule:
            add(prefix, "const", rule["const"])
        if "minLength" in rule:
            add(prefix, "minLength", rule["minLength"])
        if "minItems" in rule:
            add(prefix, "minItems", rule["minItems"])
        if "ref" in rule:
            add(prefix, "ref", rule["ref"])
        if "required" in rule:
            add(prefix, "required", list(rule["required"]))
        if "allowed" in rule:
            add(prefix, "allowed", list(rule["allowed"]))
        items = rule.get("items")
        if isinstance(items, dict):
            walk_rule(prefix + ".items", items)
        fields = rule.get("fields")
        if isinstance(fields, dict):
            for name, child in fields.items():
                walk_rule(prefix + "." + name, child)

    for name, obj in spec["objects"].items():
        add(name, "required", list(obj["required"]))
        add(name, "allowed", list(obj["allowed"]))
        for index, group in enumerate(obj.get("groups", [])):
            add(f"{name}.GROUP.{index}", "group", list(group))
        for index, pair in enumerate(obj.get("same_length", [])):
            add(f"{name}.SAME_LENGTH.{index}", "same_length", list(pair))
        for fname, rule in obj["fields"].items():
            walk_rule(f"{name}.{fname}", rule)
    return rows


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    spec = load(SCHEMA)
    rows = sorted(draft_bindings(spec), key=lambda row: row["path"])
    payload = json.dumps(rows, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    document = {
        "id": "cmp.fd.fx05.semantic-reference.v0.14",
        "ratification": "PENDING_HUMAN_APPROVAL",
        "independence": "NOT_RATIFIED",
        "proves_product": False,
        "full_product_coverage": False,
        "new_gov_01": "OPEN",
        "generator": "tools/draft_semantic_reference.py",
        "compared_by": "tools/check_fd_fx03_ack.py literal_bindings",
        "same_function_as_checker": False,
        "authority": (
            "Candidate literal anchor drafted in this authoring session from the v0.14 schema text. "
            "Not a Founder-ratified golden. Not produced by the mutation checker. "
            "It binds only the contracts inside this package. It does not prove the product."
        ),
        "what_one_sided_edit_detects": [
            "const", "minItems", "minLength", "ref", "required", "allowed", "type"
        ],
        "what_same_author_edit_of_every_side_does_not_detect": (
            "If the same author changes the schema, the fixture, this file's expected value, "
            "and this file's digests together, the comparator has no external ratified source left. "
            "That residual is SAME_AUTHOR_BOTH_SIDES not_detected. It keeps NEW-GOV-01 OPEN."
        ),
        "schema_sha256": sha256(SCHEMA),
        "fixture_sha256": sha256(FIXTURE),
        "synthetic_sha256": sha256(SYNTHETIC),
        "bindings_sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
        "binding_count": len(rows),
        "bindings": rows,
    }
    OUT.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"bindings={len(rows)} digest={document['bindings_sha256']}")


if __name__ == "__main__":
    main()
