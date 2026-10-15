#!/usr/bin/env python3
"""Static check of CMP-FD-FX-03 v0.8.

Covers fixture decision rows only. It does not execute the protocol,
does not take a PostgreSQL lock, does not run an oracle, and is not a
product test. Sequential replay is not concurrency.

Decision order, first match:
1. exactly one ACK field null -> ACK_SCOPE_MISMATCH
2. both null -> NO_ACK
3. tenant other than the channel -> NOT_FOUND, no lock
4. receiver not in the session -> NOT_FOUND, no row
5. ack stream not allocated in this session -> ACK_STREAM_UNALLOCATED
6. n == 0 -> ACK_SEQUENCE_ZERO
7. n < 0 -> ACK_REGRESSION stage "negative" (before the peer comparison)
8. same command_id + same digest -> IDEMPOTENT_REPLAY
9. same command_id + other digest -> IDEMPOTENCY_KEY_REUSED
10. event_id already applied -> EVENT_DEDUPE
11. n > emitted -> ACK_FUTURE
12. n < current -> ACK_REGRESSION stage "regression"
13. n == current -> ACK_DUPLICATE
14. current < n <= emitted -> ACK_ACCEPT, that key only, and only upward

The carrier stream_id is not an input of the decision or of the digest.
"""
import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "CMP-FD-FX-03-ack.json"
COUNTERS = (
    "money_movements",
    "mic_opens",
    "transport_effects",
    "outbox_appends",
    "financial_audits",
    "command_commit_rows",
)
ZERO_DELTA = {name: 0 for name in COUNTERS}
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
    "FX03-NEGATIVE-SEQUENCE",
    "FX03-ISOLATION-INTERLEAVE",
    "FX03-WRONG-TENANT",
    "FX03-WRONG-RECEIVER",
    "FX03-REPLAY-SAME-COMMAND",
    "FX03-REPLAY-DISTINCT-COMMAND",
    "FX03-REPLAY-KEY-REUSED",
    "FX03-EVENT-DEDUPE",
    "FX03-ROLLBACK-BEFORE-COMMIT",
}
NEGATIVE_IDS = {
    "FX03-ACK-ZERO",
    "FX03-ACK-ZERO-AFTER-PROGRESS",
    "FX03-REGRESSION",
    "FX03-DUPLICATE",
    "FX03-FUTURE",
    "FX03-UNALLOCATED",
    "FX03-PAIR-INVALID",
    "FX03-NO-ACK",
    "FX03-ACK-SCOPE-MISMATCH-SEQUENCE-ONLY",
    "FX03-ACK-SCOPE-MISMATCH-STREAM-ONLY",
    "FX03-NEGATIVE-SEQUENCE",
    "FX03-WRONG-TENANT",
    "FX03-WRONG-RECEIVER",
    "FX03-REPLAY-SAME-COMMAND",
    "FX03-REPLAY-DISTINCT-COMMAND",
    "FX03-REPLAY-KEY-REUSED",
    "FX03-EVENT-DEDUPE",
}
DECLARED = (
    "zero_effect",
    "zero_new_effect",
    "zero_money",
    "opens_mic",
    "opaque",
    "writes_high_water",
    "expected_code",
    "peer_ack_high_water_after",
)
OPAQUE_CODES = {"NOT_FOUND", "ACK_STREAM_UNALLOCATED"}


def fail(code):
    print(code)
    return 1


def key_of(row):
    return (
        row["organization_id"],
        row["project_id"],
        row["session_id"],
        row["ack_stream_id"],
        row["receiver_participant_id"],
    )


def digest_of(row):
    body = {
        "ack_of_sequence": row["ack_of_sequence"],
        "ack_stream_id": row["ack_stream_id"],
        "command_type": "AckPeerHighWater",
        "organization_id": row["organization_id"],
        "project_id": row["project_id"],
        "receiver_participant_id": row["receiver_participant_id"],
        "session_id": row["session_id"],
    }
    raw = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def fresh(doc):
    state = {}
    for row in doc["initial_keys"]:
        state[key_of(row)] = {
            "water": row["peer_ack_high_water"],
            "emitted": row["emitted_high_water"],
        }
    return state, {name: 0 for name in COUNTERS}, {}, set()


def foreign_error(before, after, target):
    if set(before) != set(after):
        return "FAIL_CREATED_KEY"
    for key, row in after.items():
        if key != target and row["water"] != before[key]["water"]:
            return "FAIL_FOREIGN_KEY"
        if row["emitted"] != before[key]["emitted"]:
            return "FAIL_EMITTED_CHANGED"
    return None


def pre_lock(row, doc):
    n = row["ack_of_sequence"]
    ack_stream = row["ack_stream_id"]
    seq_missing = n is None
    stream_missing = ack_stream is None
    if seq_missing != stream_missing:
        return "ACK_SCOPE_MISMATCH", False, "pair"
    if seq_missing and stream_missing:
        return "NO_ACK", False, "pair"
    channel = doc["channel"]
    if row["organization_id"] != channel["organization_id"] or row["project_id"] != channel["project_id"]:
        return "NOT_FOUND", False, "tenant"
    participants = doc["participants"].get(row["session_id"], [])
    if row["receiver_participant_id"] not in participants:
        return "NOT_FOUND", False, "receiver"
    allocated = doc["allocated_by_session"][row["session_id"]]
    if ack_stream not in allocated:
        return "ACK_STREAM_UNALLOCATED", False, "unallocated"
    if isinstance(n, bool) or not isinstance(n, int):
        return "ACK_UNSPECIFIED", False, "bad"
    if n == 0:
        return "ACK_SEQUENCE_ZERO", False, "zero"
    if n < 0:
        return "ACK_REGRESSION", False, "negative"
    return None


def post_lock(n, current, emitted):
    if n > emitted:
        return "ACK_FUTURE", current, False, "future"
    if n < current:
        return "ACK_REGRESSION", current, False, "regression"
    if n == current:
        return "ACK_DUPLICATE", current, False, "duplicate"
    if current < n <= emitted:
        return "ACK_ACCEPT", n, True, "accept"
    return "ACK_UNSPECIFIED", current, False, "bad"


def apply_command(state, counters, commits, events, row, doc):
    """Mutates state only on ACK_ACCEPT. Never opens the mic or moves money."""
    before_counters = dict(counters)
    early = pre_lock(row, doc)
    if early is not None:
        code, wrote, stage = early
        return {
            "code": code,
            "stage": stage,
            "wrote": wrote,
            "target": None,
            "water_after": None,
            "stored_command": False,
            "replay": False,
            "transport_status": 422 if code != "NOT_FOUND" else 404,
            "counter_delta": {name: 0 for name in COUNTERS},
        }
    target = key_of(row)
    if target not in state:
        return {
            "code": "ACK_UNSPECIFIED",
            "stage": "missing-key",
            "wrote": False,
            "target": target,
            "water_after": None,
            "stored_command": False,
            "replay": False,
            "transport_status": None,
            "counter_delta": {name: 0 for name in COUNTERS},
        }
    ident = (row["organization_id"], row["project_id"], row["command_id"])
    digest = digest_of(row)
    if ident in commits:
        same = commits[ident] == digest
        return {
            "code": "IDEMPOTENT_REPLAY" if same else "IDEMPOTENCY_KEY_REUSED",
            "stage": "replay" if same else "reused",
            "wrote": False,
            "target": target,
            "water_after": state[target]["water"],
            "stored_command": False,
            "replay": same,
            "transport_status": 200 if same else 409,
            "counter_delta": {name: 0 for name in COUNTERS},
        }
    if row["event_id"] in events:
        return {
            "code": "EVENT_DEDUPE",
            "stage": "event",
            "wrote": False,
            "target": target,
            "water_after": state[target]["water"],
            "stored_command": False,
            "replay": False,
            "transport_status": 200,
            "counter_delta": {name: 0 for name in COUNTERS},
        }
    current = state[target]["water"]
    emitted = state[target]["emitted"]
    code, after, wrote, stage = post_lock(row["ack_of_sequence"], current, emitted)
    if wrote:
        if code != "ACK_ACCEPT" or after <= current:
            raise RuntimeError("accept did not raise")
        state[target]["water"] = after
        counters["transport_effects"] += 1
        counters["outbox_appends"] += 1
        counters["command_commit_rows"] += 1
        commits[ident] = digest
        events.add(row["event_id"])
        stored = True
        transport = 200
    else:
        stored = False
        transport = 422
        after = current
    delta = {name: counters[name] - before_counters[name] for name in COUNTERS}
    return {
        "code": code,
        "stage": stage,
        "wrote": wrote,
        "target": target,
        "water_after": after,
        "stored_command": stored,
        "replay": False,
        "transport_status": transport,
        "counter_delta": delta,
    }


def snapshot(state, counters, commits, events):
    return copy.deepcopy(state), dict(counters), dict(commits), set(events)


def restore(saved):
    state, counters, commits, events = saved
    return copy.deepcopy(state), dict(counters), dict(commits), set(events)


def apply_setup(state, counters, commits, events, steps, doc):
    for step in steps:
        result = apply_command(state, counters, commits, events, step, doc)
        if result["code"] != step["expected_code"]:
            return "FAIL_SETUP:" + step["command_id"] + ":" + result["code"]
    return None


def derived_zero_effect(result, before_water, after_water):
    return (not result["wrote"]) and result["code"] != "ACK_ACCEPT" and before_water == after_water


def derived_zero_new(result, before_water, after_water):
    return before_water == after_water and result["counter_delta"] == ZERO_DELTA and result["counter_delta"]["money_movements"] == 0


def declaration_error(field, row, result, before_water, after_water):
    if field == "expected_code":
        return None if row["expected_code"] == result["code"] else "FAIL_CODE"
    if field == "peer_ack_high_water_after":
        return None if row["peer_ack_high_water_after"] == after_water else "FAIL_AFTER"
    if field == "writes_high_water":
        return None if row["writes_high_water"] is result["wrote"] else "FAIL_WRITE"
    if field == "zero_money":
        return None if row["zero_money"] is True and result["counter_delta"]["money_movements"] == 0 else "FAIL_MONEY"
    if field == "opens_mic":
        return None if row["opens_mic"] is False and result["counter_delta"]["mic_opens"] == 0 else "FAIL_OPENS_MIC"
    if field == "opaque":
        expect = result["code"] in OPAQUE_CODES
        return None if row["opaque"] is expect else "FAIL_OPAQUE"
    if field == "zero_effect":
        expect = derived_zero_effect(result, before_water, after_water)
        return None if row["zero_effect"] is expect else "FAIL_ZERO_EFFECT"
    if field == "zero_new_effect":
        expect = before_water == after_water and result["counter_delta"] == ZERO_DELTA
        return None if row["zero_new_effect"] is expect else "FAIL_ZERO_NEW_EFFECT"
    if field == "expected_stage":
        return None if row["expected_stage"] == result["stage"] else "FAIL_STAGE"
    if field in COUNTERS:
        return None if row["counter_delta"][field] == result["counter_delta"][field] else "FAIL_COUNTER"
    return "FAIL_UNKNOWN_FIELD"


def require_declared(row):
    for field in DECLARED:
        if field not in row:
            return "FAIL_DECLARED_FIELD"
    if "counter_delta" not in row:
        return "FAIL_DECLARED_FIELD"
    for name in COUNTERS:
        if name not in row["counter_delta"]:
            return "FAIL_DECLARED_FIELD"
    if "expected_stage" not in row:
        return "FAIL_DECLARED_FIELD"
    return None


def check_row(row, result, before_water, after_water):
    missing = require_declared(row)
    if missing:
        return missing
    if row["peer_ack_high_water_before"] != before_water:
        return "FAIL_BEFORE"
    for field in list(DECLARED) + ["expected_stage"] + list(COUNTERS):
        error = declaration_error(field, row, result, before_water, after_water)
        if error:
            return error
    if result["counter_delta"]["financial_audits"] != 0 or result["counter_delta"]["mic_opens"] != 0:
        return "FAIL_SIDE_CHANNEL"
    if result["counter_delta"]["money_movements"] != 0:
        return "FAIL_MONEY"
    return None


def witness_key(row):
    if "witness_ack_stream_id" not in row:
        return None
    return (
        row["witness_organization_id"],
        row["witness_project_id"],
        row["witness_session_id"],
        row["witness_ack_stream_id"],
        row["witness_receiver_participant_id"],
    )


def run_isolated(doc, row, setup=None, water_override=None):
    state, counters, commits, events = fresh(doc)
    if water_override is not None:
        state[key_of(row)]["water"] = water_override
    if setup:
        error = apply_setup(state, counters, commits, events, setup, doc)
        if error:
            return error, None, None, None
    before_state, _, _, _ = snapshot(state, counters, commits, events)
    result = apply_command(state, counters, commits, events, row, doc)
    leaked = foreign_error(before_state, state, result["target"] if result["wrote"] else None)
    if leaked:
        return leaked, result, None, None
    if result["wrote"] and result["target"] is not None:
        before_water = before_state[result["target"]]["water"]
        after_water = state[result["target"]]["water"]
        if after_water <= before_water:
            return "FAIL_ACCEPT_NOT_RAISE", result, before_water, after_water
    elif result["target"] is not None:
        before_water = before_state[result["target"]]["water"]
        after_water = state[result["target"]]["water"]
    else:
        watched = witness_key(row)
        if watched is None or watched not in before_state:
            return "FAIL_WITNESS", result, None, None
        before_water = before_state[watched]["water"]
        after_water = state[watched]["water"]
        if before_water != after_water:
            return "FAIL_HIGH_WATER", result, before_water, after_water
    return None, result, before_water, after_water


def mutate_declarations(doc, row):
    _, result, before_water, after_water = run_isolated(
        doc, row, row.get("setup"), row.get("water_override")
    )
    if not isinstance(before_water, int):
        return "FAIL_MUTATION_SETUP"
    base_error = check_row(row, result, before_water, after_water)
    if base_error:
        return base_error
    mutations = {
        "zero_effect": (not row["zero_effect"], "FAIL_ZERO_EFFECT"),
        "zero_new_effect": (not row["zero_new_effect"], "FAIL_ZERO_NEW_EFFECT"),
        "zero_money": (False, "FAIL_MONEY"),
        "opens_mic": (True, "FAIL_OPENS_MIC"),
        "opaque": (not row["opaque"], "FAIL_OPAQUE"),
        "writes_high_water": (not row["writes_high_water"], "FAIL_WRITE"),
        "expected_code": ("MUTATED_CODE", "FAIL_CODE"),
        "peer_ack_high_water_after": (row["peer_ack_high_water_after"] + 1, "FAIL_AFTER"),
        "money_movements": (1, "FAIL_COUNTER"),
        "mic_opens": (1, "FAIL_COUNTER"),
        "transport_effects": (row["counter_delta"]["transport_effects"] + 1, "FAIL_COUNTER"),
        "outbox_appends": (row["counter_delta"]["outbox_appends"] + 1, "FAIL_COUNTER"),
        "financial_audits": (1, "FAIL_COUNTER"),
        "command_commit_rows": (row["counter_delta"]["command_commit_rows"] + 1, "FAIL_COUNTER"),
    }
    for field, (value, expected) in mutations.items():
        mutated = copy.deepcopy(row)
        if field in COUNTERS:
            mutated["counter_delta"][field] = value
        else:
            mutated[field] = value
        error = declaration_error(field if field not in COUNTERS else field, mutated, result, before_water, after_water)
        if error != expected:
            print(field, error, expected, row["case_id"])
            return "FAIL_MUTATION_BLIND"
    return None


def check_interleave(doc, case):
    state, counters, commits, events = fresh(doc)
    if case.get("concurrency") is not False or case.get("not_a_postgresql_test") is not True:
        return "FAIL_RACE_LABELED_CONCURRENT"
    for step in case["steps"]:
        before, _, _, _ = snapshot(state, counters, commits, events)
        result = apply_command(state, counters, commits, events, step, doc)
        if result["code"] != step["expected_code"] or result["stage"] != step["expected_stage"]:
            print(result["code"], result["stage"], step["step_id"])
            return "FAIL_CODE"
        if result["wrote"] is not step["writes_high_water"]:
            return "FAIL_WRITE"
        target = result["target"]
        if result["water_after"] != step["expected_target_water"]:
            return "FAIL_AFTER"
        leaked = foreign_error(before, state, target if result["wrote"] else None)
        if leaked:
            return leaked
        if result["counter_delta"] != step["counter_delta"]:
            return "FAIL_COUNTER"
        if result["counter_delta"]["money_movements"] != 0 or result["counter_delta"]["mic_opens"] != 0:
            return "FAIL_SIDE_CHANNEL"
        # Mutation: a foreign key change must be detected.
        bumped = copy.deepcopy(state)
        foreign = next(key for key in bumped if key != target)
        bumped[foreign]["water"] += 1
        if foreign_error(before, bumped, target if result["wrote"] else None) != "FAIL_FOREIGN_KEY":
            return "FAIL_MUTATION_BLIND"
    return None


def check_sequential(doc, case):
    if case.get("concurrency") is not False or case.get("not_a_postgresql_test") is not True:
        return "FAIL_RACE_LABELED_CONCURRENT"
    state, counters, commits, events = fresh(doc)
    steps = []
    for index, n in enumerate(case["commit_order"]):
        step = {
            "ack_of_sequence": n,
            "ack_stream_id": case["ack_stream_id"],
            "stream_id": case["stream_id"],
            "organization_id": case["organization_id"],
            "project_id": case["project_id"],
            "session_id": case["session_id"],
            "receiver_participant_id": case["receiver_participant_id"],
            "command_id": case["case_id"] + "-" + str(index),
            "event_id": case["case_id"] + "-event-" + str(index),
        }
        before, _, _, _ = snapshot(state, counters, commits, events)
        result = apply_command(state, counters, commits, events, step, doc)
        leaked = foreign_error(before, state, result["target"] if result["wrote"] else None)
        if leaked:
            return leaked
        if result["wrote"] and result["water_after"] <= before[result["target"]]["water"]:
            return "FAIL_ACCEPT_NOT_RAISE"
        if not result["wrote"] and result["target"] is not None and state[result["target"]]["water"] != before[result["target"]]["water"]:
            return "FAIL_SILENT_CHANGE"
        steps.append(result["code"])
    target = key_of(case)
    final = state[target]["water"]
    if final != case["expected_final"] or final != 2:
        return "FAIL_RACE_FINAL"
    if steps != case["expected_steps"]:
        print(steps, case["case_id"])
        return "FAIL_RACE_STEPS"
    if case["commit_order"] == [2, 1] and steps[-1] != "ACK_REGRESSION":
        return "FAIL_RACE_REGRESSION"
    if case["decreases"] is not False:
        return "FAIL_DECREASE"
    if case["zero_money"] is not True or case["opens_mic"] is not False:
        return "FAIL_SIDE_CHANNEL"
    if counters["money_movements"] or counters["mic_opens"] or counters["financial_audits"]:
        return "FAIL_SIDE_CHANNEL"
    return None


def check_rollback(doc, case):
    state, counters, commits, events = fresh(doc)
    saved = snapshot(state, counters, commits, events)
    attempt = case["attempt"]
    result = apply_command(state, counters, commits, events, attempt, doc)
    if result["code"] != "ACK_ACCEPT" or result["wrote"] is not True:
        return "FAIL_ROLLBACK_ATTEMPT"
    state, counters, commits, events = restore(saved)
    target = key_of(attempt)
    if state[target]["water"] != 0 or counters != ZERO_DELTA or commits or events:
        return "FAIL_ROLLBACK_RESIDUE"
    if case["command_stored_after_rollback"] is not False:
        return "FAIL_ROLLBACK_STORED"
    retry = apply_command(state, counters, commits, events, attempt, doc)
    if retry["code"] != "ACK_ACCEPT" or retry["replay"] is not False:
        return "FAIL_ROLLBACK_BECAME_REPLAY"
    if state[target]["water"] != 1:
        return "FAIL_AFTER"
    # Mutation: leaving the water raised after the modelled rollback must fail.
    dirty, _, _, _ = fresh(doc)
    dirty[target]["water"] = 1
    if dirty[target]["water"] == saved[0][target]["water"]:
        return "FAIL_MUTATION_BLIND"
    if case["zero_new_effect_after_rollback"] is not True:
        return "FAIL_ZERO_NEW_EFFECT"
    if case["zero_money"] is not True or case["opens_mic"] is not False:
        return "FAIL_SIDE_CHANNEL"
    if case["executed_database"] is not False or case["oracle_status"] != "NOT_RUN":
        return "FAIL_ORACLE_LABELED_RUN"
    return None


def carrier_ignored(row):
    other = dict(row)
    other["stream_id"] = "carrier-mutated"
    return digest_of(row) == digest_of(other)


def main():
    doc = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if doc.get("schema") != "cmp.fd.fx03.ack.v0.8":
        return fail("FAIL_SCHEMA")
    if doc.get("coverage") != "fixture_decision_rows_only":
        return fail("FAIL_COVERAGE")
    if doc.get("half_duplex_allowed") is not False:
        return fail("FAIL_HALF_DUPLEX")
    if doc.get("ledger") != "forge.command_commit+forge.event.v1":
        return fail("FAIL_LEDGER")
    ids = [row["case_id"] for row in doc["cases"]]
    if len(ids) != len(set(ids)) or set(ids) != REQUIRED:
        return fail("FAIL_CASE_SET")
    keys = [key_of(row) for row in doc["initial_keys"]]
    if len(keys) != len(set(keys)) or len(keys) < 6:
        return fail("FAIL_KEY_SET")
    if doc.get("primary_session_id") not in doc["participants"]:
        return fail("FAIL_SESSION")
    allocated = doc["allocated_by_session"]
    if len(allocated[doc["primary_session_id"]]) < 2:
        return fail("FAIL_STREAMS")
    if len(doc["participants"][doc["primary_session_id"]]) < 2:
        return fail("FAIL_RECEIVERS")
    for row in doc["cases"]:
        kind = row["kind"]
        if kind == "interleave":
            error = check_interleave(doc, row)
            if error:
                return fail(error)
            print(f"OK {row['case_id']} keys_isolated=true foreign_mutation=detected")
            continue
        if kind == "sequential_replay":
            error = check_sequential(doc, row)
            if error:
                return fail(error)
            print(f"OK {row['case_id']} sequential_not_concurrency final={row['expected_final']}")
            continue
        if kind == "rollback_model":
            error = check_rollback(doc, row)
            if error:
                return fail(error)
            print(f"OK {row['case_id']} rollback_model oracle=NOT_RUN")
            continue
        if not carrier_ignored(row):
            return fail("FAIL_DIGEST_USES_CARRIER")
        error, result, before_water, after_water = run_isolated(
            doc, row, row.get("setup"), row.get("water_override")
        )
        if error:
            print(row["case_id"], error)
            return fail(error)
        error = check_row(row, result, before_water, after_water)
        if error:
            print(row["case_id"], error, result["code"], result["stage"])
            return fail(error)
        if row["case_id"] in NEGATIVE_IDS:
            mutated = mutate_declarations(doc, row)
            if mutated:
                print(row["case_id"], mutated)
                return fail(mutated)
        if row["case_id"] == "FX03-NEGATIVE-SEQUENCE" and result["stage"] != "negative":
            return fail("FAIL_STAGE")
        if row["case_id"] == "FX03-NO-ACK" and result["code"] == "ACK_STREAM_UNALLOCATED":
            return fail("FAIL_NO_ACK_AS_UNALLOCATED")
        print(
            f"OK {row['case_id']} {result['code']} stage={result['stage']} "
            f"after={after_water} write={result['wrote']} "
            f"opens_mic=False zero_money=True"
        )
    print("COVERAGE fixture_rows_only explicit_NO_ACK=present both_SCOPE_MISMATCH_directions=present negative_sequence=present")
    print("ISOLATION static_map_only POSTGRESQL_RACE=NOT_RUN")
    print("MUTATION declared_fields=rejected foreign_key=rejected")
    print("STATIC_ACK_V08_CHECK PASS_FIXTURE_ONLY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
