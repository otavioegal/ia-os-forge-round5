#!/usr/bin/env python3
"""Static numeric check of CMP-FD-FX-03.

This encodes the v0.6 decision table for fixture numbers only.
It does not execute the protocol, does not run an oracle, and is not a product test.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "CMP-FD-FX-03-ack.json"
REQUIRED = {
    "FX03-ACK-ZERO",
    "FX03-ACK-ZERO-AFTER-PROGRESS",
    "FX03-RACE-1-THEN-2",
    "FX03-RACE-2-THEN-1",
    "FX03-REGRESSION",
    "FX03-DUPLICATE",
    "FX03-FUTURE",
    "FX03-CROSS-VALID",
    "FX03-UNALLOCATED",
    "FX03-PAIR-INVALID",
}


def fail(code):
    print(code)
    return 1


def decide(n, ack_stream_id, stream_present, allocated, current, emitted):
    """First match. Mirrors CMP-FD-02 v0.6. Does not write."""
    if (n is None) ^ (ack_stream_id is None):
        return "ACK_SCOPE_MISMATCH", current, False
    if ack_stream_id not in allocated:
        return "ACK_STREAM_UNALLOCATED", current, False
    if n == 0:
        return "ACK_SEQUENCE_ZERO", current, False
    if n < 0:
        return "ACK_REGRESSION", current, False
    if n > emitted:
        return "ACK_FUTURE", current, False
    if n < current:
        return "ACK_REGRESSION", current, False
    if n == current:
        return "ACK_DUPLICATE", current, False
    if current < n <= emitted:
        return "ACK_ACCEPT", n, True
    return "ACK_UNSPECIFIED", current, False


def replay(order, initial, emitted, allocated, ack_stream_id):
    current = initial
    steps = []
    saw_decrease = False
    for n in order:
        code, after, wrote = decide(n, ack_stream_id, True, allocated, current, emitted)
        if after < current:
            saw_decrease = True
        current = after
        steps.append(code)
        if wrote and current < n:
            saw_decrease = True
    return current, steps, saw_decrease


def main():
    doc = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if doc.get("half_duplex_allowed") is not False:
        return fail("FAIL_HALF_DUPLEX")
    allocated = set(doc["allocated_stream_ids"].values())
    if len(allocated) != 3:
        return fail("FAIL_STREAMS")
    cases = doc["cases"]
    ids = [row["case_id"] for row in cases]
    if len(ids) != len(set(ids)) or set(ids) != REQUIRED:
        return fail("FAIL_CASE_SET")
    for row in cases:
        if row["kind"] == "race":
            final, steps, decreased = replay(
                row["commit_order"],
                row["initial_peer_ack_high_water"],
                row["emitted_high_water"],
                allocated,
                row["ack_stream_id"],
            )
            if decreased or row["decreases"] is not False:
                return fail("FAIL_DECREASE")
            if final != row["expected_final"] or final != 2:
                return fail("FAIL_RACE_FINAL")
            if steps != row["expected_steps"]:
                return fail("FAIL_RACE_STEPS")
            if row["commit_order"] == [2, 1] and steps[-1] != "ACK_REGRESSION":
                return fail("FAIL_RACE_REGRESSION")
            print(f"OK {row['case_id']} final={final} steps={steps}")
            continue
        code, after, wrote = decide(
            row["ack_of_sequence"],
            row["ack_stream_id"],
            True,
            allocated,
            row["peer_ack_high_water_before"],
            row["emitted_high_water"],
        )
        if code == "ACK_UNSPECIFIED":
            return fail("FAIL_UNSPECIFIED")
        if code != row["expected_code"]:
            print(code, row["case_id"])
            return fail("FAIL_CODE")
        if after != row["peer_ack_high_water_after"]:
            return fail("FAIL_AFTER")
        if wrote != row["writes_high_water"]:
            return fail("FAIL_WRITE")
        if after < row["peer_ack_high_water_before"]:
            return fail("FAIL_DECREASE")
        if row["case_id"] == "FX03-CROSS-VALID":
            if row["ack_stream_id"] == row["stream_id"] or row["ack_stream_id"] not in allocated:
                return fail("FAIL_CROSS")
            if row.get("opens_mic") is not False or row.get("zero_money") is not True:
                return fail("FAIL_CROSS_EFFECT")
        if row["case_id"].startswith("FX03-ACK-ZERO") and code != "ACK_SEQUENCE_ZERO":
            return fail("FAIL_ZERO")
        print(f"OK {row['case_id']} {code} after={after} write={wrote}")
    print("STATIC_ACK_MONOTONIC_CHECK PASS_FIXTURE_ONLY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
