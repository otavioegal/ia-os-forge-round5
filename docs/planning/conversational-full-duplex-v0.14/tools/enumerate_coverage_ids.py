#!/usr/bin/env python3
"""Second listing of coverage IDs for v0.14.

This file does not import check_fd_fx03_ack.py. The walk below is a separate
copy of the schema-rule and occurrence listing, made in the same authoring
session. Agreement with the checker is not a human-ratified golden and does
not close NEW-GOV-01. It does not prove the product.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "fixtures" / "CMP-FD-FX-03-ack.schema.json"
FIXTURE = ROOT / "fixtures" / "CMP-FD-FX-03-ack.json"
SYNTHETIC = ROOT / "fixtures" / "CMP-FD-FX-03-ack.synthetic.json"
SEMANTIC = ROOT / "fixtures" / "CMP-FD-FX-05-semantic-reference.json"
OUT = ROOT / "fixtures" / "CMP-FD-FX-07-coverage-ids.json"


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


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


TYPE_WRONG = {
    "uuid": (1, "FAIL_TYPE"),
    "nullable_uuid": (1, "FAIL_TYPE"),
    "int": (True, "FAIL_TYPE"),
    "nullable_int": (True, "FAIL_TYPE"),
    "bool": (0, "FAIL_TYPE"),
    "string": (1, "FAIL_TYPE"),
    "sha256": (1, "FAIL_TYPE"),
    "object": ([], "FAIL_SCHEMA"),
    "array": ({}, "FAIL_SCHEMA"),
    "uuid_map": ([], "FAIL_SCHEMA"),
}
# The v0.12 figures were an internally consistent count of an incomplete catalog.
# They are not evidence for this package.
V12_REJECTED_RULES = 480
V12_REJECTED_OCCURRENCES = 2239


def format_path(path):
    parts = []
    for part in path:
        if isinstance(part, int):
            parts[-1] = f"{parts[-1]}[{part}]"
        else:
            parts.append(str(part))
    return ".".join(parts)


def occ_id(path, suffix):
    rendered = "document" if not path else format_path(path)
    return f"occ:{rendered}.{suffix}"


def rule_id(path, suffix):
    return f"rule:{path}.{suffix}"


def const_opposite(value):
    if value is True:
        return False
    if value is False:
        return True
    return "OTHER"


def delete_path(root, path):
    cursor = root
    for part in path[:-1]:
        cursor = cursor[part]
    del cursor[path[-1]]


def assign_path(root, path, value):
    cursor = root
    for part in path[:-1]:
        cursor = cursor[part]
    cursor[path[-1]] = value


def mutate_container(root, path, op, job):
    if op == "EXTRA":
        target = root
        for part in path:
            target = target[part]
        target["_not_in_schema"] = True
        return
    if op == "ABSENCE":
        delete_path(root, path)
        return
    if op == "SHORTEN":
        cursor = root
        for part in path[:-1]:
            cursor = cursor[part]
        current = cursor[path[-1]]
        cursor[path[-1]] = [current[0]]
        return
    assign_path(root, path, job["value"])


def apply_mutation(host, job):
    path = job["path"]
    try:
        if len(path) >= 2 and path[0] == "cases" and isinstance(path[1], int):
            case = copy.deepcopy(host["cases"][path[1]])
            mutate_container(case, path[2:], job["op"], job)
            return case_schema_error(host, case)
        mutated = copy.deepcopy(host)
        mutate_container(mutated, path, job["op"], job)
        return schema_error(mutated)
    except Exception as exc:
        return exc


def inline_closed(spec):
    def check(rule):
        if not isinstance(rule, dict):
            return False
        if rule.get("type") == "object" and "fields" in rule and "ref" not in rule:
            fields = rule["fields"]
            allowed = rule.get("allowed")
            if allowed is None or set(allowed) != set(fields):
                return False
            if any(name not in fields for name in rule.get("required", [])):
                return False
            return all(check(child) for child in fields.values())
        if rule.get("type") == "array" and isinstance(rule.get("items"), dict):
            return check(rule["items"])
        return True

    for obj in spec["objects"].values():
        for rule in obj["fields"].values():
            if not check(rule):
                return False
    return True


def expected_schema_rules(spec):
    """Schema-only walk. It does not look at jobs or at the fixture."""
    found = {}

    def add(identifier, code):
        if identifier in found:
            raise RuntimeError(identifier)
        found[identifier] = code

    def declare(path, rule, required):
        add(rule_id(path, "TYPE"), TYPE_WRONG[rule["type"]][1])
        if required:
            add(rule_id(path, "ABSENCE"), "FAIL_SCHEMA")
        if rule["type"] in ("uuid", "nullable_uuid"):
            add(rule_id(path, "UUID"), "FAIL_UUID")
        if "const" in rule:
            add(rule_id(path, "CONST"), "FAIL_SCHEMA")
        if rule["type"] == "string" and rule.get("minLength", 0) >= 1:
            add(rule_id(path, "MIN_LENGTH"), "FAIL_SCHEMA")
        if rule["type"] == "sha256":
            add(rule_id(path, "FORMAT"), "FAIL_SCHEMA")
        if rule["type"] == "array":
            add(rule_id(path, "CARDINALITY"), "FAIL_SCHEMA")
            item = rule.get("items") or {}
            item_type = item.get("type")
            if item_type in TYPE_WRONG and item_type != "object":
                add(rule_id(path, "ELEMENT_TYPE"), TYPE_WRONG[item_type][1])
            if item_type == "string" and item.get("minLength", 0) >= 1:
                add(rule_id(path, "ELEMENT_MIN_LENGTH"), "FAIL_SCHEMA")
            if item_type == "object":
                add(rule_id(path, "ELEMENT_SCALAR"), "FAIL_SCHEMA")
                add(rule_id(path, "ELEMENT_LIST"), "FAIL_SCHEMA")
                if "fields" in item and "ref" not in item:
                    for name, child in item["fields"].items():
                        declare(f"{path}.item.{name}", child, name in item.get("required", []))
        if rule["type"] == "object" and "fields" in rule and "ref" not in rule:
            add(rule_id(path, "EXTRA"), "FAIL_EXTRA_KEY")
            for name, child in rule["fields"].items():
                declare(f"{path}.{name}", child, name in rule.get("required", []))
        if rule["type"] == "uuid_map":
            add(rule_id(path, "EMPTY"), "FAIL_SCHEMA")
            add(rule_id(path, "MAP_KEY_TYPE"), "FAIL_TYPE")
            add(rule_id(path, "MAP_KEY_UUID"), "FAIL_UUID")
            add(rule_id(path, "MAP_EMPTY"), "FAIL_SCHEMA")
            add(rule_id(path, "MAP_ELEMENT_TYPE"), "FAIL_TYPE")
            add(rule_id(path, "MAP_ELEMENT_UUID"), "FAIL_UUID")

    for obj_name, obj in spec["objects"].items():
        add(rule_id(obj_name, "EXTRA"), "FAIL_EXTRA_KEY")
        for fname, rule in obj["fields"].items():
            declare(f"{obj_name}.{fname}", rule, fname in obj["required"])
        for index, _group in enumerate(obj.get("groups", [])):
            add(rule_id(f"{obj_name}.GROUP.{index}", "PARTIAL"), "FAIL_SCHEMA")
        for pair in obj.get("same_length", []):
            add(rule_id(f"{obj_name}.SAME_LENGTH.{pair[0]}.{pair[1]}", "SHORTEN"), "FAIL_SCHEMA")
    return found


def expected_occurrences(host, spec):
    """Second walk. Recursive, fixture-shaped, and not used to build jobs."""
    found = {}

    def add(path, suffix, code):
        identifier = occ_id(path, suffix)
        if identifier in found:
            raise RuntimeError(identifier)
        found[identifier] = code

    def walk(value, obj_spec, path):
        if not isinstance(value, dict):
            return
        add(path, "EXTRA", "FAIL_EXTRA_KEY")
        required = obj_spec.get("required", [])
        for fname, rule in obj_spec["fields"].items():
            fpath = path + [fname]
            if fname in required:
                add(fpath, "ABSENCE", "FAIL_SCHEMA")
            if fname not in value:
                continue
            add(fpath, "TYPE", TYPE_WRONG[rule["type"]][1])
            child = value[fname]
            if rule["type"] == "object" and isinstance(child, dict):
                if "ref" in rule:
                    walk(child, spec["objects"][rule["ref"]], fpath)
                elif "fields" in rule:
                    walk(child, {
                        "fields": rule["fields"],
                        "required": rule.get("required", []),
                    }, fpath)
            if rule["type"] == "array" and isinstance(child, list):
                item = rule.get("items") or {}
                if rule.get("minItems", 0) >= 1:
                    add(fpath, "EMPTY", "FAIL_SCHEMA")
                if item.get("type") == "object":
                    for index, element in enumerate(child):
                        ipath = fpath + [index]
                        add(ipath, "ELEMENT_SCALAR", "FAIL_SCHEMA")
                        add(ipath, "ELEMENT_LIST", "FAIL_SCHEMA")
                        if not isinstance(element, dict):
                            continue
                        if "ref" in item:
                            walk(element, spec["objects"][item["ref"]], ipath)
                        elif "fields" in item:
                            walk(element, {
                                "fields": item["fields"],
                                "required": item.get("required", []),
                            }, ipath)
                elif item.get("type") in TYPE_WRONG:
                    for index in range(len(child)):
                        add(fpath + [index], "ELEMENT_TYPE", TYPE_WRONG[item["type"]][1])

    walk(host, spec["objects"]["document"], [])
    for index, row in enumerate(host["cases"]):
        walk(row, spec["objects"][row["kind"]], ["cases", index])
    return found

def digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def rows(identifiers):
    return [{"id": item, "digest": digest(item)} for item in sorted(identifiers)]


def main():
    spec = load(SCHEMA)
    doc = load(FIXTURE)
    synthetic = load(SYNTHETIC)
    host = dict(doc)
    host["cases"] = list(doc["cases"]) + list(synthetic["cases"])
    rules = expected_schema_rules(spec)
    occurrences = expected_occurrences(host, spec)
    document = {
        "id": "cmp.fd.fx07.coverage-ids.v0.14",
        "ratification": "PENDING_HUMAN_APPROVAL",
        "proves_product": False,
        "full_product_coverage": False,
        "pass_label": "PASS_FIXTURE_ONLY",
        "generator": "tools/enumerate_coverage_ids.py",
        "generator_imports_checker": False,
        "note": "Same authoring session as the checker. Not a ratified golden. NEW-GOV-01 stays OPEN. Counts are this package only.",
        "schema_sha256": sha256(SCHEMA),
        "fixture_sha256": sha256(FIXTURE),
        "synthetic_sha256": sha256(SYNTHETIC),
        "semantic_sha256": sha256(SEMANTIC),
        "rule_count": len(rules),
        "occurrence_count": len(occurrences),
        "rules": rows(rules),
        "occurrences": rows(occurrences),
    }
    OUT.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(f"rules={len(rules)} occurrences={len(occurrences)}")


if __name__ == "__main__":
    main()
