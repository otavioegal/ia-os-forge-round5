#!/usr/bin/env python3
"""Static shape check of CMP-FD-FX-02.

Not a protocol execution, not an oracle run, not a product test.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "CMP-FD-FX-02-ack.json"
REQUIRED = {
    "FX02-ACK-CROSS-VALID",
    "FX02-ACK-SAME-STREAM-VALID",
    "FX02-ACK-FUTURE",
    "FX02-ACK-REGRESSION",
    "FX02-ACK-DUPLICATE",
    "FX02-ACK-UNALLOCATED",
    "FX02-PREAMBLE-AUTH",
    "FX02-PREAMBLE-MATCH-NO-OPEN",
}


def fail(code):
    print(code)
    return 1


def main():
    doc = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if doc.get("half_duplex_allowed") is not False:
        return fail("FAIL_HALF_DUPLEX")
    allocated = set(doc["allocated_stream_ids"].values())
    if len(allocated) != 3:
        return fail("FAIL_STREAMS")
    high = doc["emitted_high_water"]
    cases = doc["cases"]
    ids = [row["case_id"] for row in cases]
    if len(ids) != len(set(ids)) or set(ids) != REQUIRED:
        return fail("FAIL_CASE_SET")
    by_id = {row["case_id"]: row for row in cases}
    cross = by_id["FX02-ACK-CROSS-VALID"]
    if cross["ack_stream_id"] == cross["stream_id"]:
        return fail("FAIL_NOT_CROSS")
    if cross["ack_stream_id"] not in allocated or cross["stream_id"] not in allocated:
        return fail("FAIL_NOT_ALLOCATED")
    if cross["ack_of_sequence"] > high[cross["ack_stream_id"]]:
        return fail("FAIL_CROSS_IS_FUTURE")
    if cross["expected_code"] != "ACK_ACCEPT" or cross["opens_mic"] is not False:
        return fail("FAIL_CROSS_EXPECT")
    future = by_id["FX02-ACK-FUTURE"]
    if not (future["ack_of_sequence"] > high[future["ack_stream_id"]]):
        return fail("FAIL_FUTURE_NUMBER")
    if future["expected_code"] != "ACK_FUTURE" or future["zero_effect"] is not True:
        return fail("FAIL_FUTURE_EXPECT")
    reg = by_id["FX02-ACK-REGRESSION"]
    if not (reg["ack_of_sequence"] < reg["peer_ack_high_water_before"]):
        return fail("FAIL_REGRESSION_NUMBER")
    if reg["expected_code"] != "ACK_REGRESSION":
        return fail("FAIL_REGRESSION_EXPECT")
    dup = by_id["FX02-ACK-DUPLICATE"]
    if dup["ack_of_sequence"] != dup["peer_ack_high_water_before"]:
        return fail("FAIL_DUPLICATE_NUMBER")
    if dup["expected_code"] != "ACK_DUPLICATE" or dup["zero_new_effect"] is not True:
        return fail("FAIL_DUPLICATE_EXPECT")
    missing = by_id["FX02-ACK-UNALLOCATED"]
    if missing["ack_stream_id"] in allocated:
        return fail("FAIL_UNALLOCATED_IS_ALLOCATED")
    if missing["expected_code"] != "ACK_STREAM_UNALLOCATED" or missing["opaque"] is not True:
        return fail("FAIL_UNALLOCATED_EXPECT")
    auth = by_id["FX02-PREAMBLE-AUTH"]
    if auth["principal_ref"] == doc["authenticated_principal"]:
        return fail("FAIL_AUTH_MATCHES")
    if auth["expected_code"] != "PREAMBLE_AUTH":
        return fail("FAIL_AUTH_CODE")
    if auth["opens_session"] or auth["opens_mic"] or auth["opens_stream"] or auth["opens_task"]:
        return fail("FAIL_AUTH_EFFECT")
    ok = by_id["FX02-PREAMBLE-MATCH-NO-OPEN"]
    if ok["principal_ref"] != doc["authenticated_principal"]:
        return fail("FAIL_MATCH_PRINCIPAL")
    if ok["opens_session"] or ok["opens_mic"] or ok["creates_reservation"]:
        return fail("FAIL_MATCH_OPENS")
    print("STATIC_ACK_FIXTURE_CHECK PASS_FIXTURE_ONLY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
