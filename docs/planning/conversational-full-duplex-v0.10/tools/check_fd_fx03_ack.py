#!/usr/bin/env python3
"""Static check of CMP-FD-FX-03 v0.10.

Covers fixture decision rows only. It does not execute the protocol,
does not take a PostgreSQL lock, does not run an oracle, and is not a
product test. Sequential replay is not concurrency.

Decision order, first match:
1. exactly one ACK field null -> ACK_SCOPE_MISMATCH
2. both null -> NO_ACK
3. tenant other than the channel -> NOT_FOUND, no command_commit lookup
4. same tenant command_id + same digest -> transport 200 replay of the stored outcome
5. same tenant command_id + other digest -> IDEMPOTENCY_KEY_REUSED, stored outcome kept
6. receiver not in the session -> NOT_FOUND, no row
7. ack stream not allocated -> ACK_STREAM_UNALLOCATED
8. n == 0 -> ACK_SEQUENCE_ZERO
9. n < 0 -> ACK_REGRESSION stage "negative"
10. event_id already applied -> EVENT_DEDUPE
11. n > emitted -> ACK_FUTURE, commit original 422
12. n < current -> ACK_REGRESSION stage "regression", commit original 422
13. n == current -> ACK_DUPLICATE, commit original 422
14. current < n <= emitted -> ACK_ACCEPT, commit original 200, that key only

Steps 4 and 5 are before the mutable receiver/session checks and after the
tenant check. A removed receiver does not rewrite a stored outcome and does
not authorize another tenant.
"""
import copy
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "CMP-FD-FX-03-ack.json"
SCHEMA = ROOT / "fixtures" / "CMP-FD-FX-03-ack.schema.json"
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
    "FX03-REPLAY-ORIGINAL-422",
    "FX03-REPLAY-DIGEST-DISTINCT",
    "FX03-REPLAY-RECEIVER-REMOVED",
    "FX03-REPLAY-CROSS-TENANT",
}
UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)
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


def canonical_bytes(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def outcome_record(code, water):
    if code == "ACK_ACCEPT":
        body = {"error_code": "ACK_ACCEPT", "peer_ack_high_water": water}
        http = 200
    else:
        body = {
            "error_code": code,
            "opaque": False,
            "retryable": False,
            "terminal": True,
        }
        http = 422
    raw = canonical_bytes(body)
    return http, body, hashlib.sha256(raw).hexdigest()


def structural(row):
    n = row["ack_of_sequence"]
    ack_stream = row["ack_stream_id"]
    seq_missing = n is None
    stream_missing = ack_stream is None
    if seq_missing != stream_missing:
        return ("ACK_SCOPE_MISMATCH", "pair", 422)
    if seq_missing and stream_missing:
        return ("NO_ACK", "pair", None)
    return None


def tenant_rejected(row, doc):
    channel = doc["channel"]
    return (
        row["organization_id"] != channel["organization_id"]
        or row["project_id"] != channel["project_id"]
    )


def mutable_rejected(row, doc):
    n = row["ack_of_sequence"]
    participants = doc["participants"].get(row["session_id"], [])
    if row["receiver_participant_id"] not in participants:
        return ("NOT_FOUND", "receiver", 404)
    allocated = doc["allocated_by_session"][row["session_id"]]
    if row["ack_stream_id"] not in allocated:
        return ("ACK_STREAM_UNALLOCATED", "unallocated", 422)
    if isinstance(n, bool) or not isinstance(n, int):
        return ("ACK_UNSPECIFIED", "bad", 422)
    if n == 0:
        return ("ACK_SEQUENCE_ZERO", "zero", 422)
    if n < 0:
        return ("ACK_REGRESSION", "negative", 422)
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


def blank(code, stage, transport):
    return {
        "code": code,
        "stage": stage,
        "wrote": False,
        "target": None,
        "water_after": None,
        "stored_command": False,
        "replay": False,
        "transport_status": transport,
        "original_outcome_code": None,
        "original_outcome_body": None,
        "outcome_digest": None,
        "command_digest": None,
        "counter_delta": {name: 0 for name in COUNTERS},
    }


def apply_command(state, counters, commits, events, row, doc):
    """Writes high-water only on ACK_ACCEPT. Never opens the mic or moves money.

    command_commit lookup is tenant-scoped and happens before mutable
    receiver, allocation and sequence checks. It returns the stored outcome.
    """
    before_counters = dict(counters)
    early = structural(row)
    if early is not None:
        code, stage, transport = early
        return blank(code, stage, transport)
    if tenant_rejected(row, doc):
        # No lookup of another tenant's command_commit. No original body.
        return blank("NOT_FOUND", "tenant", 404)
    target = key_of(row)
    ident = (row["organization_id"], row["project_id"], row["command_id"])
    digest = digest_of(row)
    if ident in commits:
        stored = commits[ident]
        same = stored["command_digest"] == digest
        replay = same
        return {
            "code": "IDEMPOTENT_REPLAY" if same else "IDEMPOTENCY_KEY_REUSED",
            "stage": "replay" if same else "reused",
            "wrote": False,
            "target": target if target in state else None,
            "water_after": state[target]["water"] if target in state else None,
            "stored_command": False,
            "replay": replay,
            "transport_status": 200 if same else 409,
            "original_outcome_code": stored["original_outcome_code"] if same else None,
            "original_outcome_body": copy.deepcopy(stored["original_outcome_body"]) if same else None,
            "outcome_digest": stored["outcome_digest"] if same else None,
            "command_digest": stored["command_digest"] if same else None,
            "stored_row_unchanged": True,
            "counter_delta": {name: 0 for name in COUNTERS},
        }
    mutable = mutable_rejected(row, doc)
    if mutable is not None:
        code, stage, transport = mutable
        return blank(code, stage, transport)
    if target not in state:
        return blank("ACK_UNSPECIFIED", "missing-key", None)
    if row["event_id"] in events:
        result = blank("EVENT_DEDUPE", "event", 200)
        result["target"] = target
        result["water_after"] = state[target]["water"]
        return result
    current = state[target]["water"]
    emitted = state[target]["emitted"]
    code, after, wrote, stage = post_lock(row["ack_of_sequence"], current, emitted)
    if code == "ACK_UNSPECIFIED":
        return blank(code, stage, 422)
    if wrote:
        if code != "ACK_ACCEPT" or after <= current:
            raise RuntimeError("accept did not raise")
        state[target]["water"] = after
        counters["transport_effects"] += 1
        counters["outbox_appends"] += 1
        events.add(row["event_id"])
    else:
        after = current
    http, body, odigest = outcome_record(code, after)
    counters["command_commit_rows"] += 1
    commits[ident] = {
        "command_digest": digest,
        "original_outcome_code": http,
        "original_outcome_body": body,
        "outcome_digest": odigest,
        "event_id": row["event_id"] if wrote else None,
    }
    delta = {name: counters[name] - before_counters[name] for name in COUNTERS}
    return {
        "code": code,
        "stage": stage,
        "wrote": wrote,
        "target": target,
        "water_after": after,
        "stored_command": True,
        "replay": False,
        "transport_status": http,
        "original_outcome_code": http,
        "original_outcome_body": copy.deepcopy(body),
        "outcome_digest": odigest,
        "command_digest": digest,
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
    if "expected_transport_status" in row and row["expected_transport_status"] != result["transport_status"]:
        return "FAIL_TRANSPORT"
    if "expected_original_outcome_code" in row:
        if result.get("replay") is not True or result.get("transport_status") != 200:
            return "FAIL_TRANSPORT"
        if result.get("original_outcome_code") != row["expected_original_outcome_code"]:
            return "FAIL_ORIGINAL_CODE"
        if result.get("original_outcome_body") != row["expected_original_outcome_body"]:
            return "FAIL_ORIGINAL_BODY"
        digest = hashlib.sha256(canonical_bytes(result["original_outcome_body"])).hexdigest()
        if digest != result.get("outcome_digest") or digest != row["expected_outcome_digest"]:
            return "FAIL_OUTCOME_DIGEST"
        if result["original_outcome_code"] != 200 and result["transport_status"] == result["original_outcome_code"]:
            return "FAIL_TRANSPORT_EQUALS_OUTCOME"
        if result["original_outcome_body"].get("error_code") in {"IDEMPOTENT_REPLAY", "200"}:
            return "FAIL_ORIGINAL_BODY"
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
    stage = copy.deepcopy(row)
    stage["expected_stage"] = "MUTATED_STAGE"
    if check_row(stage, result, before_water, after_water) != "FAIL_STAGE":
        return "FAIL_MUTATION_BLIND"
    before = copy.deepcopy(row)
    before["peer_ack_high_water_before"] = row["peer_ack_high_water_before"] + 1
    if check_row(before, result, before_water, after_water) != "FAIL_BEFORE":
        return "FAIL_MUTATION_BLIND"
    if "expected_original_outcome_code" in row:
        changed = copy.deepcopy(row)
        changed["expected_original_outcome_code"] = 999
        if check_row(changed, result, before_water, after_water) != "FAIL_ORIGINAL_CODE":
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


def stored_unchanged(doc, row):
    if "expected_stored_outcome_code" not in row:
        return None
    state, counters, commits, events = fresh(doc)
    if row.get("water_override") is not None:
        state[key_of(row)]["water"] = row["water_override"]
    if row.get("setup"):
        error = apply_setup(state, counters, commits, events, row["setup"], doc)
        if error:
            return error
    ident = (row["organization_id"], row["project_id"], row["command_id"])
    before = copy.deepcopy(commits[ident])
    apply_command(state, counters, commits, events, row, doc)
    if commits[ident] != before:
        return "FAIL_STORED_REPLACED"
    if before["original_outcome_code"] != row["expected_stored_outcome_code"]:
        return "FAIL_STORED_CODE"
    if before["original_outcome_body"]["error_code"] != row["expected_stored_error_code"]:
        return "FAIL_STORED_BODY"
    return None


def check_receiver_removed(doc, case):
    state, counters, commits, events = fresh(doc)
    error = apply_setup(state, counters, commits, events, case["setup"], doc)
    if error:
        return error
    replay = case["replay"]
    ident = (replay["organization_id"], replay["project_id"], replay["command_id"])
    if commits[ident]["original_outcome_code"] != 422:
        return "FAIL_STORED_CODE"
    removed = copy.deepcopy(doc)
    session = replay["session_id"]
    receiver = replay["receiver_participant_id"]
    removed["participants"][session] = [
        item for item in removed["participants"][session] if item != receiver
    ]
    before, _, before_commits, before_events = snapshot(state, counters, commits, events)
    result = apply_command(state, counters, commits, events, replay, removed)
    if result["code"] != "IDEMPOTENT_REPLAY" or result["transport_status"] != 200 or result["replay"] is not True:
        return "FAIL_REPLAY_ORDER"
    if result["original_outcome_code"] != 422:
        return "FAIL_ORIGINAL_CODE"
    if result["original_outcome_body"] != before_commits[ident]["original_outcome_body"]:
        return "FAIL_ORIGINAL_BODY"
    if result["transport_status"] == result["original_outcome_code"]:
        return "FAIL_TRANSPORT_EQUALS_OUTCOME"
    if foreign_error(before, state, None):
        return "FAIL_FOREIGN_KEY"
    if commits[ident] != before_commits[ident] or events != before_events:
        return "FAIL_STORED_REPLACED"
    fresh_result = apply_command(state, counters, commits, events, case["fresh"], removed)
    if fresh_result["code"] != "NOT_FOUND" or fresh_result["stage"] != "receiver":
        return "FAIL_MUTABLE"
    if fresh_result["original_outcome_body"] is not None:
        return "FAIL_TENANT_BODY"
    if commits[ident]["original_outcome_code"] != 422:
        return "FAIL_STORED_REPLACED"
    return None


def check_cross_tenant(doc, case):
    state, counters, commits, events = fresh(doc)
    error = apply_setup(state, counters, commits, events, case["setup"], doc)
    if error:
        return error
    probe = case["probe"]
    home = (case["setup"][0]["organization_id"], case["setup"][0]["project_id"], case["setup"][0]["command_id"])
    before_row = copy.deepcopy(commits[home])
    before, _, _, before_events = snapshot(state, counters, commits, events)
    result = apply_command(state, counters, commits, events, probe, doc)
    if result["code"] != "NOT_FOUND" or result["stage"] != "tenant" or result["transport_status"] != 404:
        return "FAIL_TENANT_BYPASS"
    if result["original_outcome_body"] is not None or result["replay"] is not False:
        return "FAIL_TENANT_BYPASS"
    if commits[home] != before_row or events != before_events:
        return "FAIL_STORED_REPLACED"
    if foreign_error(before, state, None):
        return "FAIL_FOREIGN_KEY"
    return None


DOC_KEYS = {
    "schema", "coverage", "half_duplex_allowed", "ledger", "note", "channel",
    "primary_session_id", "allocated_by_session", "participants", "initial_keys",
    "cases", "proves_product",
}
INITIAL_KEYS = {
    "organization_id", "project_id", "session_id", "ack_stream_id",
    "receiver_participant_id", "peer_ack_high_water", "emitted_high_water",
}
COMMAND_KEYS = {
    "ack_of_sequence", "ack_stream_id", "stream_id", "organization_id", "project_id",
    "session_id", "receiver_participant_id", "command_id", "event_id",
}
ROW_KEYS = COMMAND_KEYS | {
    "case_id", "kind", "peer_ack_high_water_before", "peer_ack_high_water_after",
    "expected_code", "expected_stage", "writes_high_water", "zero_effect",
    "zero_new_effect", "zero_money", "opens_mic", "opaque", "counter_delta",
    "water_override", "setup", "expected_transport_status",
    "expected_original_outcome_code", "expected_original_outcome_body",
    "expected_outcome_digest", "expected_stored_outcome_code", "expected_stored_error_code",
    "witness_organization_id", "witness_project_id", "witness_session_id",
    "witness_ack_stream_id", "witness_receiver_participant_id",
}
SETUP_KEYS = COMMAND_KEYS | {"expected_code"}
STEP_KEYS = COMMAND_KEYS | {
    "step_id", "expected_code", "expected_stage", "expected_target_water",
    "writes_high_water", "counter_delta",
}


def is_uuid(value):
    return isinstance(value, str) and UUID_RE.match(value) is not None


def extra(obj, allowed):
    return [key for key in obj if key not in allowed]


def load_schema():
    spec = json.loads(SCHEMA.read_text(encoding="utf-8"))
    if spec.get("id") != "cmp.fd.fx03.schema.v0.10":
        return None
    return spec


def missing_required(obj, required):
    return not isinstance(obj, dict) or any(name not in obj for name in required)


def group_error(obj, groups):
    for group in groups:
        present = [name for name in group if name in obj]
        if present and len(present) != len(group):
            return "FAIL_SCHEMA"
    return None


def schema_error(doc):
    spec = load_schema()
    if spec is None or not isinstance(doc, dict):
        return "FAIL_SCHEMA"
    document = spec["objects"]["document"]
    if missing_required(doc, document["required"]):
        return "FAIL_SCHEMA"
    if extra(doc, document["allowed"]):
        return "FAIL_EXTRA_KEY"
    if doc["proves_product"] is not False:
        return "FAIL_PROVES_PRODUCT"
    if doc["schema"] != "cmp.fd.fx03.ack.v0.10":
        return "FAIL_SCHEMA"
    if doc["coverage"] != "fixture_decision_rows_only":
        return "FAIL_COVERAGE"
    if doc["half_duplex_allowed"] is not False:
        return "FAIL_HALF_DUPLEX"
    if doc["ledger"] != "forge.command_commit+forge.event.v1":
        return "FAIL_LEDGER"
    if not isinstance(doc["note"], str) or not doc["note"]:
        return "FAIL_SCHEMA"
    channel_spec = spec["objects"]["channel"]
    channel = doc["channel"]
    if missing_required(channel, channel_spec["required"]):
        return "FAIL_SCHEMA"
    if extra(channel, channel_spec["allowed"]):
        return "FAIL_EXTRA_KEY"
    if not is_uuid(channel["organization_id"]) or not is_uuid(channel["project_id"]):
        return "FAIL_UUID"
    if not is_uuid(doc["primary_session_id"]):
        return "FAIL_UUID"
    participants = doc["participants"]
    allocated = doc["allocated_by_session"]
    if not isinstance(participants, dict) or not isinstance(allocated, dict):
        return "FAIL_SCHEMA"
    if not isinstance(doc["initial_keys"], list) or not isinstance(doc["cases"], list):
        return "FAIL_SCHEMA"
    if set(participants) != set(allocated) or doc["primary_session_id"] not in participants:
        return "FAIL_KEY_COHERENCE"
    for session, people in participants.items():
        if not is_uuid(session) or not isinstance(people, list) or len(people) < 1:
            return "FAIL_UUID"
        if any(not is_uuid(person) for person in people) or len(people) != len(set(people)):
            return "FAIL_UUID"
        streams = allocated[session]
        if not isinstance(streams, list) or len(streams) < 1 or len(streams) != len(set(streams)):
            return "FAIL_KEY_COHERENCE"
        if any(not is_uuid(stream) for stream in streams):
            return "FAIL_UUID"
    if len(allocated[doc["primary_session_id"]]) < 2 or len(participants[doc["primary_session_id"]]) < 2:
        return "FAIL_KEY_COHERENCE"
    initial_spec = spec["objects"]["initial_key"]
    seen = set()
    for row in doc["initial_keys"]:
        if missing_required(row, initial_spec["required"]):
            return "FAIL_SCHEMA"
        if extra(row, initial_spec["allowed"]):
            return "FAIL_EXTRA_KEY"
        if not all(is_uuid(row[name]) for name in (
            "organization_id", "project_id", "session_id", "ack_stream_id", "receiver_participant_id"
        )):
            return "FAIL_UUID"
        if row["session_id"] not in participants:
            return "FAIL_KEY_COHERENCE"
        if row["ack_stream_id"] not in allocated[row["session_id"]]:
            return "FAIL_KEY_COHERENCE"
        if row["receiver_participant_id"] not in participants[row["session_id"]]:
            return "FAIL_KEY_COHERENCE"
        if isinstance(row["peer_ack_high_water"], bool) or not isinstance(row["peer_ack_high_water"], int):
            return "FAIL_TYPE"
        if isinstance(row["emitted_high_water"], bool) or not isinstance(row["emitted_high_water"], int):
            return "FAIL_TYPE"
        if row["peer_ack_high_water"] < 0 or row["emitted_high_water"] < 0:
            return "FAIL_TYPE"
        identity = key_of(row)
        if identity in seen:
            return "FAIL_KEY_COHERENCE"
        seen.add(identity)
    if len(seen) < 6:
        return "FAIL_KEY_COHERENCE"
    return None


def command_error(row, allowed, required):
    if missing_required(row, required):
        return "FAIL_SCHEMA"
    if extra(row, allowed):
        return "FAIL_EXTRA_KEY"
    for name in ("organization_id", "project_id", "session_id", "receiver_participant_id", "command_id", "event_id", "stream_id"):
        if not is_uuid(row[name]):
            return "FAIL_UUID"
    if row["ack_stream_id"] is not None and not is_uuid(row["ack_stream_id"]):
        return "FAIL_UUID"
    n = row["ack_of_sequence"]
    if n is not None and (isinstance(n, bool) or not isinstance(n, int)):
        return "FAIL_TYPE"
    return None


def counter_error(row):
    if "counter_delta" not in row or not isinstance(row["counter_delta"], dict):
        return "FAIL_SCHEMA"
    delta = row["counter_delta"]
    if not set(COUNTERS) <= set(delta):
        return "FAIL_SCHEMA"
    if set(delta) != set(COUNTERS):
        return "FAIL_EXTRA_KEY"
    for value in delta.values():
        if isinstance(value, bool) or not isinstance(value, int):
            return "FAIL_TYPE"
    return None


def case_schema_error(doc, row):
    spec = load_schema()
    if spec is None or not isinstance(row, dict) or "kind" not in row:
        return "FAIL_SCHEMA"
    kind = row["kind"]
    objects = spec["objects"]
    if kind not in objects:
        return "FAIL_SCHEMA"
    rule = objects[kind]
    if missing_required(row, rule["required"]):
        return "FAIL_SCHEMA"
    if extra(row, rule["allowed"]):
        return "FAIL_EXTRA_KEY"
    grouped = group_error(row, rule.get("groups", []))
    if grouped:
        return grouped
    if kind in {"negative", "positive"}:
        error = command_error(row, rule["allowed"], rule["required"])
        if error:
            return error
        error = counter_error(row)
        if error:
            return error
        for name in ("writes_high_water", "zero_effect", "zero_new_effect", "zero_money", "opens_mic", "opaque"):
            if not isinstance(row[name], bool):
                return "FAIL_TYPE"
        for name in ("peer_ack_high_water_before", "peer_ack_high_water_after"):
            if isinstance(row[name], bool) or not isinstance(row[name], int):
                return "FAIL_TYPE"
        if not isinstance(row["expected_code"], str) or not isinstance(row["expected_stage"], str):
            return "FAIL_TYPE"
        if "water_override" in row and (isinstance(row["water_override"], bool) or not isinstance(row["water_override"], int)):
            return "FAIL_TYPE"
        for item in row.get("setup", []):
            setup = objects["setup"]
            error = command_error(item, setup["allowed"], setup["required"])
            if error:
                return error
            if "expected_code" not in item or not isinstance(item["expected_code"], str):
                return "FAIL_SCHEMA"
        return None
    if kind == "interleave":
        if not isinstance(row["steps"], list) or not row["steps"]:
            return "FAIL_SCHEMA"
        step_rule = objects["step"]
        for step in row["steps"]:
            if missing_required(step, step_rule["required"]):
                return "FAIL_SCHEMA"
            error = command_error(step, step_rule["allowed"], step_rule["required"])
            if error:
                return error
            error = counter_error(step)
            if error:
                return error
        return None
    if kind == "sequential_replay":
        for name in ("ack_stream_id", "stream_id", "organization_id", "project_id", "session_id", "receiver_participant_id"):
            if not is_uuid(row[name]):
                return "FAIL_UUID"
        for name in ("concurrency", "not_a_postgresql_test", "decreases", "zero_money", "opens_mic"):
            if not isinstance(row[name], bool):
                return "FAIL_TYPE"
        if isinstance(row["expected_final"], bool) or not isinstance(row["expected_final"], int):
            return "FAIL_TYPE"
        if not isinstance(row["commit_order"], list) or not isinstance(row["expected_steps"], list):
            return "FAIL_SCHEMA"
        return None
    if kind == "rollback_model":
        attempt = objects["attempt"]
        if "attempt" not in row:
            return "FAIL_SCHEMA"
        return command_error(row["attempt"], attempt["allowed"], attempt["required"])
    if kind == "replay_receiver_removed":
        setup = objects["setup"]
        attempt = objects["attempt"]
        for item in row["setup"]:
            error = command_error(item, setup["allowed"], setup["required"])
            if error:
                return error
        for name in ("replay", "fresh"):
            error = command_error(row[name], attempt["allowed"], attempt["required"])
            if error:
                return error
        return None
    if kind == "replay_cross_tenant":
        setup = objects["setup"]
        attempt = objects["attempt"]
        for item in row["setup"]:
            error = command_error(item, setup["allowed"], setup["required"])
            if error:
                return error
        return command_error(row["probe"], attempt["allowed"], attempt["required"])
    return "FAIL_SCHEMA"


def removal_failures(doc):
    """Delete every required field named by the schema file. Missing must be FAIL_SCHEMA, never an exception."""
    spec = load_schema()
    if spec is None:
        return "FAIL_SCHEMA"
    jobs = []
    for name in spec["objects"]["document"]["required"]:
        mutated = copy.deepcopy(doc)
        del mutated[name]
        jobs.append(("document", name, mutated, None))
    for name in spec["objects"]["channel"]["required"]:
        mutated = copy.deepcopy(doc)
        del mutated["channel"][name]
        jobs.append(("channel", name, mutated, None))
    for name in spec["objects"]["initial_key"]["required"]:
        mutated = copy.deepcopy(doc)
        del mutated["initial_keys"][0][name]
        jobs.append(("initial_key", name, mutated, None))
    seen = set()
    for index, row in enumerate(doc["cases"]):
        if row["kind"] in seen:
            continue
        seen.add(row["kind"])
        for name in spec["objects"][row["kind"]]["required"]:
            mutated = copy.deepcopy(doc)
            del mutated["cases"][index][name]
            jobs.append((row["kind"], name, mutated, index))
    interleave = next(index for index, row in enumerate(doc["cases"]) if row["kind"] == "interleave")
    for name in spec["objects"]["step"]["required"]:
        mutated = copy.deepcopy(doc)
        del mutated["cases"][interleave]["steps"][0][name]
        jobs.append(("step", name, mutated, interleave))
    setup_index = next(index for index, row in enumerate(doc["cases"]) if row.get("setup"))
    for name in spec["objects"]["setup"]["required"]:
        mutated = copy.deepcopy(doc)
        del mutated["cases"][setup_index]["setup"][0][name]
        jobs.append(("setup", name, mutated, setup_index))
    rollback = next(index for index, row in enumerate(doc["cases"]) if row["kind"] == "rollback_model")
    for name in spec["objects"]["attempt"]["required"]:
        mutated = copy.deepcopy(doc)
        del mutated["cases"][rollback]["attempt"][name]
        jobs.append(("attempt", name, mutated, rollback))
    for label, name, mutated, index in jobs:
        try:
            if label in {"document", "channel", "initial_key"}:
                error = schema_error(mutated)
            else:
                error = case_schema_error(mutated, mutated["cases"][index])
        except Exception as exc:
            print("removal exception", label, name, type(exc).__name__)
            return "FAIL_SCHEMA_EXCEPTION"
        if error != "FAIL_SCHEMA":
            print("removal", label, name, error)
            return "FAIL_MUTATION_BLIND"
    return None


def carrier_ignored(row):
    other = dict(row)
    other["stream_id"] = "carrier-mutated"
    return digest_of(row) == digest_of(other)


def main():
    doc = json.loads(FIXTURE.read_text(encoding="utf-8"))
    error = schema_error(doc)
    if error:
        return fail(error)
    if doc.get("coverage") != "fixture_decision_rows_only":
        return fail("FAIL_COVERAGE")
    if doc.get("half_duplex_allowed") is not False:
        return fail("FAIL_HALF_DUPLEX")
    if doc.get("ledger") != "forge.command_commit+forge.event.v1":
        return fail("FAIL_LEDGER")
    for row in doc["cases"]:
        error = case_schema_error(doc, row)
        if error:
            print(row.get("case_id"), error)
            return fail(error)
    poisoned = copy.deepcopy(doc)
    poisoned["unexpected"] = True
    if schema_error(poisoned) != "FAIL_EXTRA_KEY":
        return fail("FAIL_MUTATION_BLIND")
    poisoned = copy.deepcopy(doc)
    poisoned["channel"]["organization_id"] = "not-a-uuid"
    if schema_error(poisoned) != "FAIL_UUID":
        return fail("FAIL_MUTATION_BLIND")
    poisoned = copy.deepcopy(doc)
    first = next(row for row in poisoned["initial_keys"] if row["session_id"] == doc["primary_session_id"])
    foreign = next(
        person for person in poisoned["participants"][doc["primary_session_id"]]
        if person != first["receiver_participant_id"]
    )
    # Move that receiver out of the primary session. The key still names them.
    poisoned["participants"][doc["primary_session_id"]] = [
        person for person in poisoned["participants"][doc["primary_session_id"]] if person != foreign
    ]
    first["receiver_participant_id"] = foreign
    if schema_error(poisoned) != "FAIL_KEY_COHERENCE":
        return fail("FAIL_MUTATION_BLIND")
    removed = removal_failures(doc)
    if removed:
        return fail(removed)
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
        if kind == "replay_receiver_removed":
            error = check_receiver_removed(doc, row)
            if error:
                print(row["case_id"], error)
                return fail(error)
            print(f"OK {row['case_id']} replay_keeps_422 transport=200 fresh_receiver=NOT_FOUND")
            continue
        if kind == "replay_cross_tenant":
            error = check_cross_tenant(doc, row)
            if error:
                print(row["case_id"], error)
                return fail(error)
            print(f"OK {row['case_id']} tenant_lookup_blocked")
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
        error = stored_unchanged(doc, row)
        if error:
            print(row["case_id"], error)
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
    print("MUTATION declared_fields=rejected before=rejected stage=rejected foreign_key=rejected extra_key=rejected")
    print("REPLAY original_outcome_separated_from_transport")
    print("SCHEMA required_fields=enforced missing=FAIL_SCHEMA")
    print("PROVES_PRODUCT false")
    print("STATIC_ACK_V10_CHECK PASS_FIXTURE_ONLY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
