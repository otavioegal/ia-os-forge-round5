#!/usr/bin/env python3
"""Static check of CMP-FD-FX-03 v0.7.

Implements the v0.6 decision order (CMP-FD-02 v0.6 lines 41-50):
exactly one ACK field null, then both null, then unallocated, zero,
negative, future, regression, duplicate, accept.

Both ACK fields null return NO_ACK. They are not ACK_STREAM_UNALLOCATED
and they do not write. Each one-null direction returns ACK_SCOPE_MISMATCH.

Coverage: fixture decision rows only. This does not walk every media
event. FX03-NO-ACK is a required explicit row, not an omitted event.

Monotonicity is not weakened: regression does not write; accept only
raises the high-water.

This does not execute the protocol, does not run an oracle, and is not
a product test.
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
    "FX03-NO-ACK",
    "FX03-ACK-SCOPE-MISMATCH-SEQUENCE-ONLY",
    "FX03-ACK-SCOPE-MISMATCH-STREAM-ONLY",
}
NULL_CASES = {
    "FX03-NO-ACK",
    "FX03-ACK-SCOPE-MISMATCH-SEQUENCE-ONLY",
    "FX03-ACK-SCOPE-MISMATCH-STREAM-ONLY",
}


def fail(code):
    print(code)
    return 1


def decide(n, ack_stream_id, allocated, current, emitted):
    """First match. Does not write. Does not read the carrier stream_id."""
    seq_missing = n is None
    stream_missing = ack_stream_id is None
    if seq_missing != stream_missing:
        return "ACK_SCOPE_MISMATCH", current, False
    if seq_missing and stream_missing:
        return "NO_ACK", current, False
    if ack_stream_id not in allocated:
        return "ACK_STREAM_UNALLOCATED", current, False
    if isinstance(n, bool) or not isinstance(n, int):
        return "ACK_UNSPECIFIED", current, False
    if n == 0:
        return "ACK_SEQUENCE_ZERO", current, False
    if n < 0:
        return "ACK_REGRESSION", current, False
    if isinstance(emitted, bool) or not isinstance(emitted, int):
        return "ACK_UNSPECIFIED", current, False
    if isinstance(current, bool) or not isinstance(current, int):
        return "ACK_UNSPECIFIED", current, False
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
    illegal = False
    for n in order:
        before = current
        code, after, wrote = decide(n, ack_stream_id, allocated, current, emitted)
        if wrote:
            if code != "ACK_ACCEPT" or after <= before:
                illegal = True
        elif after != before:
            illegal = True
        if after < before:
            illegal = True
        current = after
        steps.append(code)
    return current, steps, illegal


def check_null_shape(row, allocated):
    case_id = row["case_id"]
    if case_id == "FX03-NO-ACK":
        if row["ack_of_sequence"] is not None or row["ack_stream_id"] is not None:
            return "FAIL_NO_ACK_SHAPE"
    elif case_id == "FX03-ACK-SCOPE-MISMATCH-SEQUENCE-ONLY":
        if row["ack_stream_id"] is not None or not isinstance(row["ack_of_sequence"], int):
            return "FAIL_SEQUENCE_ONLY_SHAPE"
        if isinstance(row["ack_of_sequence"], bool) or row["ack_of_sequence"] == 0:
            return "FAIL_SEQUENCE_ONLY_SHAPE"
        if row["stream_id"] not in allocated:
            return "FAIL_SEQUENCE_ONLY_SHAPE"
    elif case_id == "FX03-ACK-SCOPE-MISMATCH-STREAM-ONLY":
        if row["ack_of_sequence"] is not None or row["ack_stream_id"] not in allocated:
            return "FAIL_STREAM_ONLY_SHAPE"
    if row.get("opens_mic") is not False:
        return "FAIL_OPENS_MIC"
    if row.get("zero_money") is not True:
        return "FAIL_MONEY"
    if row.get("writes_high_water") is not False:
        return "FAIL_WRITE"
    if row["peer_ack_high_water_after"] != row["peer_ack_high_water_before"]:
        return "FAIL_HIGH_WATER"
    return None


def main():
    doc = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if doc.get("schema") != "cmp.fd.fx03.ack.v0.7":
        return fail("FAIL_SCHEMA")
    if doc.get("coverage") != "fixture_decision_rows_only":
        return fail("FAIL_COVERAGE")
    if doc.get("half_duplex_allowed") is not False:
        return fail("FAIL_HALF_DUPLEX")
    allocated = set(doc["allocated_stream_ids"].values())
    if len(allocated) != 3 or len(doc["allocated_stream_ids"]) != 3:
        return fail("FAIL_STREAMS")
    cases = doc["cases"]
    ids = [row["case_id"] for row in cases]
    if len(ids) != len(set(ids)) or set(ids) != REQUIRED:
        return fail("FAIL_CASE_SET")
    if not NULL_CASES <= set(ids):
        return fail("FAIL_NULL_CASES_MISSING")
    for row in cases:
        if row["kind"] == "race":
            final, steps, illegal = replay(
                row["commit_order"],
                row["initial_peer_ack_high_water"],
                row["emitted_high_water"],
                allocated,
                row["ack_stream_id"],
            )
            if illegal or row["decreases"] is not False:
                return fail("FAIL_DECREASE")
            if final != row["expected_final"] or final != 2:
                return fail("FAIL_RACE_FINAL")
            if steps != row["expected_steps"]:
                return fail("FAIL_RACE_STEPS")
            if row["commit_order"] == [2, 1] and steps[-1] != "ACK_REGRESSION":
                return fail("FAIL_RACE_REGRESSION")
            if row["ack_stream_id"] not in allocated:
                return fail("FAIL_RACE_STREAM")
            print(f"OK {row['case_id']} final={final} steps={steps}")
            continue
        if "ack_of_sequence" not in row or "ack_stream_id" not in row:
            return fail("FAIL_FIELDS")
        if row["case_id"] in NULL_CASES:
            shape = check_null_shape(row, allocated)
            if shape:
                return fail(shape)
        code, after, wrote = decide(
            row["ack_of_sequence"],
            row["ack_stream_id"],
            allocated,
            row["peer_ack_high_water_before"],
            row["emitted_high_water"],
        )
        if code == "ACK_UNSPECIFIED":
            return fail("FAIL_UNSPECIFIED")
        if row["case_id"] == "FX03-NO-ACK" and code == "ACK_STREAM_UNALLOCATED":
            return fail("FAIL_NO_ACK_AS_UNALLOCATED")
        if code != row["expected_code"]:
            print(code, row["case_id"])
            return fail("FAIL_CODE")
        if after != row["peer_ack_high_water_after"]:
            return fail("FAIL_AFTER")
        if wrote != row["writes_high_water"]:
            return fail("FAIL_WRITE")
        if wrote:
            if code != "ACK_ACCEPT" or after <= row["peer_ack_high_water_before"]:
                return fail("FAIL_ACCEPT_NOT_RAISE")
        elif after != row["peer_ack_high_water_before"]:
            return fail("FAIL_SILENT_CHANGE")
        if after < row["peer_ack_high_water_before"]:
            return fail("FAIL_DECREASE")
        if row["case_id"] == "FX03-REGRESSION" and (wrote or code != "ACK_REGRESSION"):
            return fail("FAIL_REGRESSION_WROTE")
        if row["case_id"] in NULL_CASES:
            if wrote or after != row["peer_ack_high_water_before"]:
                return fail("FAIL_NULL_WROTE")
            print(
                f"OK {row['case_id']} {code} after={after} write={wrote} "
                f"opens_mic=False zero_money=True high_water_unchanged=True"
            )
            continue
        print(f"OK {row['case_id']} {code} after={after} write={wrote}")
    print("COVERAGE fixture_rows_only explicit_NO_ACK=present both_SCOPE_MISMATCH_directions=present")
    print("STATIC_ACK_NULL_PAIR_CHECK PASS_FIXTURE_ONLY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
