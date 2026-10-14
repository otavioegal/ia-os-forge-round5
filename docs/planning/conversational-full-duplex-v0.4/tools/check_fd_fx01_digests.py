#!/usr/bin/env python3
"""Static check of CMP-FD-FX-01 digests.

This is not a product test, not an oracle run, and not BUILD-00.
Stdlib only. It reads the two JSON fixtures next to this script's parent
and exits 0 only when every stored digest matches the canonical SHA-256.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "fixtures" / "CMP-FD-FX-01-events.json"
VECTORS = ROOT / "fixtures" / "CMP-FD-FX-01-digest-vectors.json"


def canonical_bytes(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def main():
    events = json.loads(EVENTS.read_text(encoding="utf-8"))
    vectors = json.loads(VECTORS.read_text(encoding="utf-8"))
    if len(events) != 8 or len(vectors) != 8:
        print("FAIL count", len(events), len(vectors))
        return 1
    by_id = {row["event_id"]: row for row in vectors}
    if len(by_id) != 8:
        print("FAIL duplicate event_id in vectors")
        return 1
    for index, event in enumerate(events):
        stored = event.get("event_digest")
        body = dict(event)
        body.pop("event_digest", None)
        canon = canonical_bytes(body)
        digest = hashlib.sha256(canon).hexdigest()
        row = by_id.get(event.get("event_id"))
        if row is None:
            print("FAIL missing vector", event.get("event_id"))
            return 1
        if row["canonical_utf8"].encode("utf-8") != canon:
            print("FAIL canonical mismatch", row["label"])
            return 1
        if row["sha256"] != digest or stored != digest:
            print("FAIL digest", row["label"])
            return 1
        if row["canonical_byte_length"] != len(canon):
            print("FAIL length", row["label"])
            return 1
        print(f"OK {index} {row['label']} {digest}")
    print("STATIC_FIXTURE_DIGEST_CHECK PASS_FIXTURE_ONLY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
