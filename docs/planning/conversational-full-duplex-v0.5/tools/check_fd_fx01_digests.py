#!/usr/bin/env python3
"""Static check of CMP-FD-FX-01 digests.

Not a product test, not an oracle run, and not BUILD-00.
Stdlib only. No network. No database.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVENTS = ROOT / "fixtures" / "CMP-FD-FX-01-events.json"
DEFAULT_VECTORS = ROOT / "fixtures" / "CMP-FD-FX-01-digest-vectors.json"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")


class DuplicateKeyError(ValueError):
    pass


def pairs_hook(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise DuplicateKeyError(key)
        obj[key] = value
    return obj


def load_json(path):
    text = Path(path).read_text(encoding="utf-8")
    return json.loads(text, object_pairs_hook=pairs_hook)


def canonical_bytes(obj):
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def fail(code):
    print(code)
    return 1


def check_pair(events_path, vectors_path, require_count=None):
    try:
        events = load_json(events_path)
    except DuplicateKeyError:
        return fail("FAIL_DUPLICATE_JSON_KEY")
    except (OSError, json.JSONDecodeError, UnicodeError):
        return fail("FAIL_EVENTS_PARSE")
    try:
        vectors = load_json(vectors_path)
    except DuplicateKeyError:
        return fail("FAIL_DUPLICATE_JSON_KEY")
    except (OSError, json.JSONDecodeError, UnicodeError):
        return fail("FAIL_VECTORS_PARSE")
    if not isinstance(events, list) or not isinstance(vectors, list):
        return fail("FAIL_TYPE")
    event_ids = []
    for event in events:
        if not isinstance(event, dict):
            return fail("FAIL_TYPE")
        event_id = event.get("event_id")
        if not isinstance(event_id, str):
            return fail("FAIL_TYPE")
        event_ids.append(event_id)
        digest = event.get("event_digest")
        if not isinstance(digest, str) or SHA_RE.fullmatch(digest) is None:
            return fail("FAIL_BAD_DIGEST_FORMAT")
    if len(event_ids) != len(set(event_ids)):
        return fail("FAIL_DUPLICATE_EVENT_ID")
    vector_ids = []
    by_id = {}
    for row in vectors:
        if not isinstance(row, dict):
            return fail("FAIL_TYPE")
        event_id = row.get("event_id")
        if not isinstance(event_id, str):
            return fail("FAIL_TYPE")
        vector_ids.append(event_id)
        if event_id in by_id:
            return fail("FAIL_DUPLICATE_VECTOR_ID")
        by_id[event_id] = row
        sha = row.get("sha256")
        if not isinstance(sha, str) or SHA_RE.fullmatch(sha) is None:
            return fail("FAIL_BAD_SHA256")
        length = row.get("canonical_byte_length")
        if type(length) is not int:
            return fail("FAIL_BAD_LENGTH")
        if not isinstance(row.get("canonical_utf8"), str):
            return fail("FAIL_TYPE")
        if not isinstance(row.get("label"), str):
            return fail("FAIL_TYPE")
    event_set = set(event_ids)
    vector_set = set(vector_ids)
    if vector_set - event_set:
        return fail("FAIL_ORPHAN_VECTOR")
    if event_set - vector_set:
        return fail("FAIL_MISSING_VECTOR")
    if require_count is not None and (
        len(events) != require_count or len(vectors) != require_count
    ):
        return fail("FAIL_COUNT")
    consumed = []
    for index, event in enumerate(events):
        row = by_id[event["event_id"]]
        stored = event["event_digest"]
        body = dict(event)
        body.pop("event_digest", None)
        canon = canonical_bytes(body)
        digest = hashlib.sha256(canon).hexdigest()
        if row["canonical_utf8"].encode("utf-8") != canon:
            return fail("FAIL_CANONICAL")
        if row["canonical_byte_length"] != len(canon):
            return fail("FAIL_BAD_LENGTH")
        if row["sha256"] != digest or stored != digest:
            return fail("FAIL_DIGEST_MISMATCH")
        consumed.append(event["event_id"])
        print(f"OK {index} {row['label']} {digest}")
    if len(consumed) != len(set(consumed)) or set(consumed) != vector_set:
        return fail("FAIL_BIJECTION")
    print("STATIC_FIXTURE_DIGEST_CHECK PASS_FIXTURE_ONLY")
    return 0


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--events", default=str(DEFAULT_EVENTS))
    parser.add_argument("--vectors", default=str(DEFAULT_VECTORS))
    parser.add_argument("--require-count", type=int, default=8)
    args = parser.parse_args(argv)
    return check_pair(args.events, args.vectors, require_count=args.require_count)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
