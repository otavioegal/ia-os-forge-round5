#!/usr/bin/env python3
"""Static check of CMP-FD-FX-03 v0.15.

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

Coverage uses two walks. The expected set is not the job list.
Inline objects and every object-array element are in the expected set.
A gap is FAIL_COVERAGE_GAP. The v0.12 counts 480 and 2239 are not evidence.
PASS_FIXTURE_ONLY is not a package PASS and is not total coverage.
"""
import copy
import hashlib
import json
import re
import sys
from pathlib import Path

from canonical_json_text import canonical_json_file_sha256, canonical_json_sha256, canonical_json_text

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


class DuplicateKeyError(ValueError):
    pass


def strict_pairs(pairs):
    found = {}
    for key, value in pairs:
        if key in found:
            raise DuplicateKeyError(key)
        found[key] = value
    return found


def load_strict_text(text):
    try:
        return json.loads(text, object_pairs_hook=strict_pairs), None
    except DuplicateKeyError:
        return None, "FAIL_DUPLICATE_KEY"
    except json.JSONDecodeError:
        return None, "FAIL_SCHEMA"


def inject_duplicate_key(text):
    index = text.find("{")
    if index < 0:
        raise ValueError("not-object")
    return text[:index + 1] + '"__duplicate_probe": 1, "__duplicate_probe": 2,' + text[index + 1:]


def load_schema():
    spec, err = load_strict_text(SCHEMA.read_text(encoding="utf-8"))
    if err:
        return err
    if not isinstance(spec, dict) or spec.get("id") != "cmp.fd.fx03.schema.v0.15":
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


def value_error(value, rule):
    kind = rule["type"]
    if kind == "uuid":
        if not isinstance(value, str):
            return "FAIL_TYPE"
        return None if is_uuid(value) else "FAIL_UUID"
    if kind == "nullable_uuid":
        if value is None:
            return None
        if not isinstance(value, str):
            return "FAIL_TYPE"
        return None if is_uuid(value) else "FAIL_UUID"
    if kind == "int":
        if isinstance(value, bool) or not isinstance(value, int):
            return "FAIL_TYPE"
        return None
    if kind == "nullable_int":
        if value is None:
            return None
        if isinstance(value, bool) or not isinstance(value, int):
            return "FAIL_TYPE"
        return None
    if kind == "bool":
        if not isinstance(value, bool):
            return "FAIL_TYPE"
        if "const" in rule and value is not rule["const"]:
            return "FAIL_SCHEMA"
        return None
    if kind == "string":
        if not isinstance(value, str):
            return "FAIL_TYPE"
        if rule.get("minLength", 0) and len(value) < rule["minLength"]:
            return "FAIL_SCHEMA"
        if "const" in rule and value != rule["const"]:
            return "FAIL_SCHEMA"
        return None
    if kind == "sha256":
        if not isinstance(value, str):
            return "FAIL_TYPE"
        if re.fullmatch(r"[0-9a-f]{64}", value) is None:
            return "FAIL_SCHEMA"
        return None
    if kind == "object":
        return None if isinstance(value, dict) else "FAIL_SCHEMA"
    if kind == "array":
        if not isinstance(value, list):
            return "FAIL_SCHEMA"
        if "minItems" in rule and len(value) < rule["minItems"]:
            return "FAIL_SCHEMA"
        return None
    if kind == "uuid_map":
        if not isinstance(value, dict) or not value:
            return "FAIL_SCHEMA"
        for key, items in value.items():
            if not isinstance(key, str):
                return "FAIL_TYPE"
            if not is_uuid(key):
                return "FAIL_UUID"
            if not isinstance(items, list) or not items:
                return "FAIL_SCHEMA"
            for item in items:
                if not isinstance(item, str):
                    return "FAIL_TYPE"
                if not is_uuid(item):
                    return "FAIL_UUID"
        return None
    return "FAIL_SCHEMA"


def fields_error(obj, fields, spec):
    if not isinstance(obj, dict) or not isinstance(fields, dict):
        return "FAIL_SCHEMA"
    for name, rule in fields.items():
        if name not in obj:
            continue
        error = value_error(obj[name], rule)
        if error:
            return error
        if rule["type"] == "object" and "ref" in rule:
            error = nested_object(obj[name], spec["objects"][rule["ref"]], spec)
            if error:
                return error
        if rule["type"] == "object" and "fields" in rule:
            nested = obj[name]
            if "required" in rule and missing_required(nested, rule["required"]):
                return "FAIL_SCHEMA"
            if "allowed" in rule and extra(nested, rule["allowed"]):
                return "FAIL_EXTRA_KEY"
            error = fields_error(nested, rule["fields"], spec)
            if error:
                return error
        if rule["type"] == "array" and "items" in rule:
            item = rule["items"]
            for element in obj[name]:
                error = value_error(element, item)
                if error:
                    return error
                if item.get("type") == "object" and "ref" in item:
                    error = nested_object(element, spec["objects"][item["ref"]], spec)
                    if error:
                        return error
                if item.get("type") == "object" and "fields" in item and "ref" not in item:
                    if "required" in item and missing_required(element, item["required"]):
                        return "FAIL_SCHEMA"
                    if "allowed" in item and extra(element, item["allowed"]):
                        return "FAIL_EXTRA_KEY"
                    error = fields_error(element, item["fields"], spec)
                    if error:
                        return error
    return None


def nested_object(obj, spec_obj, spec):
    if not isinstance(obj, dict):
        return "FAIL_SCHEMA"
    if missing_required(obj, spec_obj["required"]):
        return "FAIL_SCHEMA"
    if extra(obj, spec_obj["allowed"]):
        return "FAIL_EXTRA_KEY"
    grouped = group_error(obj, spec_obj.get("groups", []))
    if grouped:
        return grouped
    return fields_error(obj, spec_obj["fields"], spec)


def schema_types_complete(spec):
    for obj in spec["objects"].values():
        if "fields" not in obj:
            return False
        if any(name not in obj["fields"] for name in obj["allowed"]):
            return False
        if any(name not in obj["allowed"] for name in obj["required"]):
            return False
    return True


def schema_error(doc):
    spec = load_schema()
    if isinstance(spec, str):
        return spec
    if spec is None or not isinstance(doc, dict) or not schema_types_complete(spec):
        return "FAIL_SCHEMA"
    problems = dsl_problems(spec)
    if problems:
        return problems[0]["code"]
    document = spec["objects"]["document"]
    if missing_required(doc, document["required"]):
        return "FAIL_SCHEMA"
    if extra(doc, document["allowed"]):
        return "FAIL_EXTRA_KEY"
    typed = fields_error(doc, document["fields"], spec)
    if typed:
        return typed
    if doc["proves_product"] is not False:
        return "FAIL_PROVES_PRODUCT"
    if doc["schema"] != "cmp.fd.fx03.ack.v0.15":
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
    if isinstance(spec, str):
        return spec
    if spec is None or not isinstance(row, dict) or "kind" not in row:
        return "FAIL_SCHEMA"
    if not isinstance(row["kind"], str):
        return "FAIL_TYPE"
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
    typed = fields_error(row, rule["fields"], spec)
    if typed:
        return typed
    for pair in rule.get("same_length", []):
        if len(row[pair[0]]) != len(row[pair[1]]):
            return "FAIL_SCHEMA"
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




SYNTHETIC = ROOT / "fixtures" / "CMP-FD-FX-03-ack.synthetic.json"
MANIFEST = ROOT / "fixtures" / "CMP-FD-FX-04-historical-manifest.json"

SEMANTIC = ROOT / "fixtures" / "CMP-FD-FX-05-semantic-reference.json"
UNKNOWN = ROOT / "fixtures" / "CMP-FD-FX-06-unknown-keyword.json"
IDS = ROOT / "fixtures" / "CMP-FD-FX-07-coverage-ids.json"
TOP_KEYS = {"id", "authority", "objects"}
OBJECT_KEYS = {"required", "allowed", "fields", "groups", "same_length"}
RULE_KEYS = {"type", "const", "minLength", "minItems", "ref", "items", "fields", "required", "allowed"}
DSL_TYPES = {
    "uuid", "nullable_uuid", "int", "nullable_int", "bool",
    "string", "sha256", "object", "array", "uuid_map",
}
JSON_SCHEMA_NOT_USED = {
    "$ref", "definitions", "allOf", "oneOf", "anyOf", "enum",
    "additionalProperties", "minimum", "maximum", "format", "nullable",
}


def file_sha256(path):
    """Textual JSON digest. Not a Git blob id. LF and CRLF hash the same."""
    return canonical_json_file_sha256(path)


def line_ending_regression():
    """Same text in LF and CRLF shares a digest. A real edit does not.

    Hash comparison stays. This does not accept a checkout-shaped digest
    and it does not delete schema_sha256, fixture_sha256 or synthetic_sha256.
    """
    targets = (
        ("schema", SCHEMA),
        ("fixture", FIXTURE),
        ("synthetic", SYNTHETIC),
        ("semantic", SEMANTIC),
    )
    for label, path in targets:
        raw = path.read_bytes()
        lf = canonical_json_text(raw)
        if b"\n" not in lf:
            print("canonical regression no newline", label)
            return "FAIL_CANONICAL_HASH"
        crlf = lf.replace(b"\n", b"\r\n")
        digest = canonical_json_sha256(lf)
        if canonical_json_sha256(crlf) != digest or canonical_json_sha256(raw) != digest:
            print("canonical regression line ending", label)
            return "FAIL_CANONICAL_HASH"
        if hashlib.sha256(lf).hexdigest() == hashlib.sha256(crlf).hexdigest():
            print("canonical regression raw bytes did not differ", label)
            return "FAIL_CANONICAL_HASH"
        edited = lf[:1] + b" " + lf[1:]
        edited_digest = canonical_json_sha256(edited)
        if edited_digest == digest or canonical_json_sha256(edited.replace(b"\n", b"\r\n")) == digest:
            print("canonical regression content change ignored", label)
            return "FAIL_CANONICAL_HASH"
        if edited_digest != canonical_json_sha256(edited.replace(b"\n", b"\r\n")):
            print("canonical regression edited endings diverged", label)
            return "FAIL_CANONICAL_HASH"
    return None


def canonical_bindings(rows):
    ordered = sorted(rows, key=lambda row: row["path"])
    payload = json.dumps(ordered, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return payload, hashlib.sha256(payload.encode("utf-8")).hexdigest()


def dsl_problems(spec):
    """Closed DSL check. It does not build mutations and does not read fixtures."""
    problems = []

    def add(path, code, keyword=None):
        item = {"path": path, "code": code}
        if keyword is not None:
            item["keyword"] = keyword
        problems.append(item)

    def names_ok(path, value):
        if not isinstance(value, list) or not value:
            add(path, "FAIL_DSL")
            return False
        if any(not isinstance(name, str) or not name for name in value):
            add(path, "FAIL_DSL")
            return False
        if len(value) != len(set(value)):
            add(path, "FAIL_DSL")
            return False
        return True

    def rule_ok(path, rule, inherited_array=False):
        if not isinstance(rule, dict):
            add(path, "FAIL_DSL")
            return
        for key in rule:
            if key not in RULE_KEYS:
                add(f"{path}.{key}", "FAIL_UNKNOWN_KEYWORD", key)
        if "type" not in rule or rule.get("type") not in DSL_TYPES:
            add(path, "FAIL_DSL")
            return
        kind = rule["type"]
        if "const" in rule:
            if kind == "bool" and not isinstance(rule["const"], bool):
                add(f"{path}.const", "FAIL_DSL")
            if kind == "string" and not isinstance(rule["const"], str):
                add(f"{path}.const", "FAIL_DSL")
            if kind not in ("bool", "string"):
                add(f"{path}.const", "FAIL_DSL")
        if "minLength" in rule:
            if kind != "string" or isinstance(rule["minLength"], bool) or not isinstance(rule["minLength"], int):
                add(f"{path}.minLength", "FAIL_DSL")
            elif rule["minLength"] < 0:
                add(f"{path}.minLength", "FAIL_DSL")
        if "minItems" in rule:
            if kind != "array" or isinstance(rule["minItems"], bool) or not isinstance(rule["minItems"], int):
                add(f"{path}.minItems", "FAIL_DSL")
            elif rule["minItems"] < 0:
                add(f"{path}.minItems", "FAIL_DSL")
        if "ref" in rule:
            if kind != "object" or not isinstance(rule["ref"], str) or rule["ref"] not in spec["objects"]:
                add(f"{path}.ref", "FAIL_UNRESOLVED_REF")
        if "items" in rule:
            if kind != "array" or not isinstance(rule["items"], dict):
                add(f"{path}.items", "FAIL_DSL")
            else:
                rule_ok(f"{path}.items", rule["items"], True)
        if "fields" in rule:
            if kind != "object" or not isinstance(rule["fields"], dict) or not rule["fields"]:
                add(f"{path}.fields", "FAIL_DSL")
            else:
                inline_names(path, rule)
                for name, child in rule["fields"].items():
                    rule_ok(f"{path}.{name}", child)
        if kind == "object" and "ref" not in rule and "fields" not in rule and not inherited_array:
            add(path, "FAIL_DSL")

    def inline_names(path, rule):
        fields = rule.get("fields")
        if not isinstance(fields, dict):
            return
        if "allowed" not in rule or not names_ok(f"{path}.allowed", rule["allowed"]):
            add(f"{path}.allowed", "FAIL_DSL")
            return
        if set(rule["allowed"]) != set(fields):
            add(f"{path}.allowed", "FAIL_DSL")
        required = rule.get("required", [])
        if not isinstance(required, list) or any(name not in fields for name in required):
            add(f"{path}.required", "FAIL_DSL")

    if not isinstance(spec, dict):
        add("$", "FAIL_DSL")
        return problems
    for key in spec:
        if key not in TOP_KEYS:
            add(key, "FAIL_UNKNOWN_KEYWORD", key)
    objects = spec.get("objects")
    if not isinstance(objects, dict) or not objects:
        add("objects", "FAIL_DSL")
        return problems
    seen_types = set()
    for obj_name, obj in objects.items():
        if not isinstance(obj, dict):
            add(obj_name, "FAIL_DSL")
            continue
        for key in obj:
            if key not in OBJECT_KEYS:
                add(f"{obj_name}.{key}", "FAIL_UNKNOWN_KEYWORD", key)
        if not names_ok(f"{obj_name}.required", obj.get("required")):
            continue
        if not names_ok(f"{obj_name}.allowed", obj.get("allowed")):
            continue
        fields = obj.get("fields")
        if not isinstance(fields, dict):
            add(f"{obj_name}.fields", "FAIL_DSL")
            continue
        if any(name not in fields for name in obj["allowed"]):
            add(f"{obj_name}.allowed", "FAIL_DSL")
        if any(name not in obj["allowed"] for name in obj["required"]):
            add(f"{obj_name}.required", "FAIL_DSL")
        for index, group in enumerate(obj.get("groups", [])):
            if not isinstance(group, list) or not names_ok(f"{obj_name}.GROUP.{index}", group):
                add(f"{obj_name}.GROUP.{index}", "FAIL_DSL")
            elif any(name not in fields for name in group):
                add(f"{obj_name}.GROUP.{index}", "FAIL_DSL")
        for index, pair in enumerate(obj.get("same_length", [])):
            if (
                not isinstance(pair, list) or len(pair) != 2
                or any(not isinstance(name, str) for name in pair)
                or any(name not in fields or fields[name].get("type") != "array" for name in pair)
            ):
                add(f"{obj_name}.SAME_LENGTH.{index}", "FAIL_DSL")
        for fname, rule in fields.items():
            if isinstance(rule, dict) and "type" in rule:
                seen_types.add(rule["type"])
            rule_ok(f"{obj_name}.{fname}", rule)
    if "nullable_int" not in seen_types or "nullable_uuid" not in seen_types:
        add("nullable", "FAIL_DSL")
    return problems


def literal_bindings(spec):
    """Iterative literal inventory. Not the mutation walker and not the drafter."""
    rows = []
    stack = [("object", name, obj) for name, obj in reversed(list(spec["objects"].items()))]

    def add(prefix, constraint, expected):
        rows.append({"path": f"{prefix}.{constraint}", "constraint": constraint, "expected": expected})

    def push_rule(prefix, rule):
        if not isinstance(rule, dict):
            return
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
        if isinstance(rule.get("items"), dict):
            stack.append(("rule", prefix + ".items", rule["items"]))
        if isinstance(rule.get("fields"), dict):
            children = list(rule["fields"].items())
            for name, child in reversed(children):
                stack.append(("rule", prefix + "." + name, child))

    while stack:
        kind, prefix, node = stack.pop()
        if kind == "object":
            add(prefix, "required", list(node["required"]))
            add(prefix, "allowed", list(node["allowed"]))
            for index, group in enumerate(node.get("groups", [])):
                add(f"{prefix}.GROUP.{index}", "group", list(group))
            for index, pair in enumerate(node.get("same_length", [])):
                add(f"{prefix}.SAME_LENGTH.{index}", "same_length", list(pair))
            children = list(node["fields"].items())
            for name, rule in reversed(children):
                stack.append(("rule", prefix + "." + name, rule))
        else:
            push_rule(prefix, node)
    return rows


def binding_map(rows):
    found = {}
    for row in rows:
        if row["path"] in found:
            raise RuntimeError(row["path"])
        found[row["path"]] = row["expected"]
    return found


def binding_drift(live_rows, frozen_rows):
    live = binding_map(live_rows)
    frozen = binding_map(frozen_rows)
    drifts = []
    for path in sorted(set(live) | set(frozen)):
        if live.get(path) != frozen.get(path):
            drifts.append(path)
    return drifts


def load_semantic():
    spec, err = load_strict_text(SEMANTIC.read_text(encoding="utf-8"))
    if err:
        return None, err
    if not isinstance(spec, dict):
        return None, "FAIL_SEMANTIC_REFERENCE"
    if spec.get("id") != "cmp.fd.fx05.semantic-reference.v0.15":
        return None, "FAIL_SEMANTIC_REFERENCE"
    if spec.get("ratification") != "PENDING_HUMAN_APPROVAL":
        return None, "FAIL_INVENTED_APPROVAL"
    if spec.get("independence") != "NOT_RATIFIED":
        return None, "FAIL_INVENTED_APPROVAL"
    if spec.get("proves_product") is not False or spec.get("full_product_coverage") is not False:
        return None, "FAIL_PROVES_PRODUCT"
    if spec.get("new_gov_01") != "OPEN":
        return None, "FAIL_INVENTED_APPROVAL"
    if spec.get("generator") == "tools/check_fd_fx03_ack.py":
        return None, "FAIL_SEMANTIC_REFERENCE"
    bindings = spec.get("bindings")
    if not isinstance(bindings, list) or not bindings:
        return None, "FAIL_SEMANTIC_REFERENCE"
    return spec, None


def semantic_file_problems(reference, spec):
    problems = []
    if reference.get("schema_sha256") != file_sha256(SCHEMA):
        problems.append("schema_sha256")
    if reference.get("fixture_sha256") != file_sha256(FIXTURE):
        problems.append("fixture_sha256")
    if reference.get("synthetic_sha256") != file_sha256(SYNTHETIC):
        problems.append("synthetic_sha256")
    _payload, digest = canonical_bindings(reference["bindings"])
    if reference.get("bindings_sha256") != digest:
        problems.append("bindings_sha256")
    drifts = binding_drift(literal_bindings(spec), reference["bindings"])
    problems.extend(drifts)
    return problems


def count_pair(spec, host):
    return len(expected_schema_rules(spec)), len(expected_occurrences(host, spec))


def under_schema(spec, function):
    global load_schema
    saved = load_schema
    load_schema = lambda spec=spec: spec
    try:
        return function()
    finally:
        load_schema = saved


def hosts_still_accept(spec, doc, synthetic_cases):
    def run():
        if schema_error(doc) is not None:
            return False
        for row in list(doc["cases"]) + list(synthetic_cases):
            if case_schema_error(doc, row) is not None:
                return False
        return True
    return under_schema(spec, run)


def cardinality_probes(spec, doc, host, synthetic_cases, reference, base_rules, base_occ):
    """Normative edits that must not be hidden by an unchanged 508/2443."""
    lines = []

    def expect_stable(label, mutated, path):
        rules, occ = count_pair(mutated, host)
        drifts = binding_drift(literal_bindings(mutated), reference["bindings"])
        if rules != base_rules or occ != base_occ:
            print(
                "CARDINALITY_MOVED", label,
                f"rules={rules}/{base_rules}", f"occurrences={occ}/{base_occ}",
            )
            return "FAIL_SEMANTIC_BLIND"
        if path not in drifts:
            print("SEMANTIC_BLIND", label, path)
            return "FAIL_SEMANTIC_BLIND"
        lines.append(
            f"{label} rules={rules}/{base_rules} occurrences={occ}/{base_occ} drift={path}"
        )
        return None

    const_spec = copy.deepcopy(spec)
    const_spec["objects"]["document"]["fields"]["schema"]["const"] = "cmp.fd.fx03.ack.OTHER"
    fixture = copy.deepcopy(doc)
    fixture["schema"] = "cmp.fd.fx03.ack.OTHER"
    rule = const_spec["objects"]["document"]["fields"]["schema"]
    if value_error(fixture["schema"], rule) is not None:
        print("const fixture no longer matches mutated const")
        return "FAIL_SEMANTIC_BLIND"
    error = expect_stable("const", const_spec, "document.schema.const")
    if error:
        return error

    items_spec = copy.deepcopy(spec)
    items_spec["objects"]["document"]["fields"]["initial_keys"]["minItems"] = 5
    if not hosts_still_accept(items_spec, doc, synthetic_cases):
        print("minItems probe rejected a still-valid fixture")
        return "FAIL_SEMANTIC_BLIND"
    error = expect_stable("minItems", items_spec, "document.initial_keys.minItems")
    if error:
        return error

    length_spec = copy.deepcopy(spec)
    length_spec["objects"]["document"]["fields"]["note"]["minLength"] = 2
    if not hosts_still_accept(length_spec, doc, synthetic_cases):
        print("minLength probe rejected a still-valid fixture")
        return "FAIL_SEMANTIC_BLIND"
    error = expect_stable("minLength", length_spec, "document.note.minLength")
    if error:
        return error

    ref_spec = copy.deepcopy(spec)
    ref_spec["objects"]["step"]["fields"]["counter_delta"]["ref"] = "document"
    rules, occ = count_pair(ref_spec, host)
    drifts = binding_drift(literal_bindings(ref_spec), reference["bindings"])
    if rules != base_rules or occ != base_occ or "step.counter_delta.ref" not in drifts:
        print("ref cardinality", rules, occ, "step.counter_delta.ref" in drifts)
        return "FAIL_SEMANTIC_BLIND"
    accepted = hosts_still_accept(ref_spec, doc, synthetic_cases)
    lines.append(
        f"ref rules={rules}/{base_rules} occurrences={occ}/{base_occ} "
        "drift=step.counter_delta.ref host_validation="
        + ("accepted" if accepted else "FAIL_SCHEMA")
    )

    alias = copy.deepcopy(spec)
    alias["objects"]["counter_alias"] = copy.deepcopy(spec["objects"]["counter"])
    pointed = copy.deepcopy(alias)
    pointed["objects"]["step"]["fields"]["counter_delta"]["ref"] = "counter_alias"
    alias_rules, alias_occ = count_pair(alias, host)
    pointed_rules, pointed_occ = count_pair(pointed, host)
    if not hosts_still_accept(pointed, doc, synthetic_cases):
        print("compatible ref rejected a same-shape host")
        return "FAIL_SEMANTIC_BLIND"
    if alias_rules != pointed_rules or alias_occ != pointed_occ or pointed_occ != base_occ:
        print("compatible ref moved counts", alias_rules, pointed_rules, alias_occ, pointed_occ)
        return "FAIL_SEMANTIC_BLIND"
    if "step.counter_delta.ref" not in binding_drift(literal_bindings(pointed), reference["bindings"]):
        print("compatible ref drift missing")
        return "FAIL_SEMANTIC_BLIND"
    lines.append(
        f"ref_compatible rules={pointed_rules}/{alias_rules} occurrences={pointed_occ}/{alias_occ} "
        f"swap_delta_rules=0 swap_delta_occurrences=0 drift=step.counter_delta.ref "
        f"host_validation=accepted alias_rules_above_508={pointed_rules - base_rules}"
    )

    required_spec = copy.deepcopy(spec)
    body = required_spec["objects"]["positive"]["fields"]["expected_original_outcome_body"]
    body["required"] = ["opaque"]
    if not hosts_still_accept(required_spec, doc, synthetic_cases):
        print("required swap rejected a still-valid host")
        return "FAIL_SEMANTIC_BLIND"
    error = expect_stable(
        "required_optional", required_spec,
        "positive.expected_original_outcome_body.required",
    )
    if error:
        return error

    both = copy.deepcopy(reference)
    both_bindings = copy.deepcopy(reference["bindings"])
    for row in both_bindings:
        if row["path"] == "document.schema.const":
            row["expected"] = "cmp.fd.fx03.ack.OTHER"
    if binding_drift(literal_bindings(const_spec), both_bindings):
        print("both-sides probe was detected; the residual must stay explicit")
        return "FAIL_SEMANTIC_BLIND"
    lines.append("SAME_AUTHOR_BOTH_SIDES not_detected path=document.schema.const")
    return lines


def unknown_keyword_problems(spec):
    problems = dsl_problems(spec)
    if problems:
        print("DSL", problems[0]["path"], problems[0]["code"])
        return problems[0]["code"]
    payload, err = load_strict_text(UNKNOWN.read_text(encoding="utf-8"))
    if err:
        return err
    found = dsl_problems(payload)
    if not found or found[0]["code"] != "FAIL_UNKNOWN_KEYWORD" or found[0].get("keyword") != "allOf":
        print("unknown fixture", found[:3])
        return "FAIL_MUTATION_BLIND"
    mutated = copy.deepcopy(spec)
    mutated["objects"]["document"]["fields"]["note"]["nullable"] = True
    found = dsl_problems(mutated)
    if not any(item["code"] == "FAIL_UNKNOWN_KEYWORD" and item.get("keyword") == "nullable" for item in found):
        print("nullable keyword was accepted")
        return "FAIL_MUTATION_BLIND"
    mutated = copy.deepcopy(spec)
    mutated["objects"]["channel"]["fields"]["organization_id"]["allOf"] = []
    found = dsl_problems(mutated)
    if not any(item.get("keyword") == "allOf" for item in found):
        return "FAIL_MUTATION_BLIND"
    if value_error(True, {"type": "int"}) != "FAIL_TYPE":
        return "FAIL_MUTATION_BLIND"
    if value_error(False, {"type": "int"}) != "FAIL_TYPE":
        return "FAIL_MUTATION_BLIND"
    if value_error(0, {"type": "bool"}) != "FAIL_TYPE":
        return "FAIL_MUTATION_BLIND"
    if value_error(1, {"type": "bool"}) != "FAIL_TYPE":
        return "FAIL_MUTATION_BLIND"
    if value_error(None, {"type": "nullable_int"}) is not None:
        return "FAIL_MUTATION_BLIND"
    if value_error(True, {"type": "nullable_int"}) != "FAIL_TYPE":
        return "FAIL_MUTATION_BLIND"
    if value_error(None, {"type": "nullable_uuid"}) is not None:
        return "FAIL_MUTATION_BLIND"
    if value_error(None, {"type": "int"}) != "FAIL_TYPE":
        return "FAIL_MUTATION_BLIND"
    return None


def id_manifest_problems(expected_rules, expected_occ):
    payload, err = load_strict_text(IDS.read_text(encoding="utf-8"))
    if err:
        return err
    if payload.get("id") != "cmp.fd.fx07.coverage-ids.v0.15":
        return "FAIL_ID_MANIFEST"
    if payload.get("proves_product") is not False or payload.get("full_product_coverage") is not False:
        return "FAIL_PROVES_PRODUCT"
    if payload.get("pass_label") != "PASS_FIXTURE_ONLY":
        return "FAIL_ID_MANIFEST"
    if payload.get("generator") == "tools/check_fd_fx03_ack.py":
        return "FAIL_ID_MANIFEST"
    if payload.get("ratification") != "PENDING_HUMAN_APPROVAL":
        return "FAIL_INVENTED_APPROVAL"
    for key, path in (
        ("schema_sha256", SCHEMA),
        ("fixture_sha256", FIXTURE),
        ("synthetic_sha256", SYNTHETIC),
        ("semantic_sha256", SEMANTIC),
    ):
        if payload.get(key) != file_sha256(path):
            print("id manifest hash", key)
            return "FAIL_ID_MANIFEST"
    rules = payload.get("rules")
    occurrences = payload.get("occurrences")
    if not isinstance(rules, list) or not isinstance(occurrences, list):
        return "FAIL_ID_MANIFEST"
    rule_ids = []
    occurrence_ids = []
    for row in rules:
        if hashlib.sha256(row["id"].encode("utf-8")).hexdigest() != row.get("digest"):
            return "FAIL_ID_MANIFEST"
        rule_ids.append(row["id"])
    for row in occurrences:
        if hashlib.sha256(row["id"].encode("utf-8")).hexdigest() != row.get("digest"):
            return "FAIL_ID_MANIFEST"
        occurrence_ids.append(row["id"])
    if rule_ids != sorted(rule_ids) or occurrence_ids != sorted(occurrence_ids):
        return "FAIL_ID_MANIFEST"
    if set(rule_ids) != set(expected_rules) or len(rule_ids) != len(expected_rules):
        print("ID_GAP rules", len(set(rule_ids)), len(expected_rules))
        return "FAIL_ID_MANIFEST"
    if set(occurrence_ids) != set(expected_occ) or len(occurrence_ids) != len(expected_occ):
        print("ID_GAP occurrences", len(set(occurrence_ids)), len(expected_occ))
        return "FAIL_ID_MANIFEST"
    if payload.get("rule_count") != len(expected_rules) or payload.get("occurrence_count") != len(expected_occ):
        return "FAIL_ID_MANIFEST"
    return None


ALLOWED_SCHEMA_CODES = {"FAIL_SCHEMA", "FAIL_TYPE", "FAIL_UUID", "FAIL_EXTRA_KEY", "FAIL_DUPLICATE_KEY"}
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


def raw_slots(host):
    """Counts taken from the JSON values only. No schema walk and no job list."""
    setup = 0
    steps = 0
    bodies = 0
    opaque = 0
    for row in host["cases"]:
        if isinstance(row.get("setup"), list):
            setup += len(row["setup"])
        if isinstance(row.get("steps"), list):
            steps += len(row["steps"])
        body = row.get("expected_original_outcome_body")
        if isinstance(body, dict):
            bodies += 1
            if "opaque" in body:
                opaque += 1
    return {
        "setup": setup,
        "steps": steps,
        "initial_keys": len(host["initial_keys"]),
        "bodies": bodies,
        "opaque": opaque,
    }


def raw_disagrees(host, occurrences):
    slots = raw_slots(host)
    problems = []
    setup_scalar = sum(1 for identifier in occurrences if ".setup[" in identifier and identifier.endswith(".ELEMENT_SCALAR"))
    setup_list = sum(1 for identifier in occurrences if ".setup[" in identifier and identifier.endswith(".ELEMENT_LIST"))
    step_scalar = sum(1 for identifier in occurrences if ".steps[" in identifier and identifier.endswith(".ELEMENT_SCALAR"))
    step_list = sum(1 for identifier in occurrences if ".steps[" in identifier and identifier.endswith(".ELEMENT_LIST"))
    init_scalar = sum(1 for identifier in occurrences if identifier.startswith("occ:initial_keys[") and identifier.endswith(".ELEMENT_SCALAR"))
    init_list = sum(1 for identifier in occurrences if identifier.startswith("occ:initial_keys[") and identifier.endswith(".ELEMENT_LIST"))
    body_absence = sum(1 for identifier in occurrences if identifier.endswith("expected_original_outcome_body.error_code.ABSENCE"))
    opaque_type = sum(1 for identifier in occurrences if identifier.endswith("expected_original_outcome_body.opaque.TYPE"))
    pairs = (
        ("setup_scalar", setup_scalar, slots["setup"]),
        ("setup_list", setup_list, slots["setup"]),
        ("step_scalar", step_scalar, slots["steps"]),
        ("step_list", step_list, slots["steps"]),
        ("initial_scalar", init_scalar, slots["initial_keys"]),
        ("initial_list", init_list, slots["initial_keys"]),
        ("body_error_code_absence", body_absence, slots["bodies"]),
        ("body_opaque_type", opaque_type, slots["opaque"]),
    )
    lines = []
    for name, actual, expected in pairs:
        lines.append(f"{name}={actual}/{expected}")
        if actual != expected:
            problems.append(f"{name} actual={actual} expected={expected}")
    return problems, lines, slots


def stack_jobs(host, spec):
    """Iterative site walk. It does not call expected_schema_rules or expected_occurrences."""
    jobs = []
    sites = {}
    elements = {}
    objects = {}

    def push_site(owner, rel, path):
        sites.setdefault((owner, rel), []).append(path)

    def consider(value, abs_path, obj_spec, owner, rel_prefix, named):
        if not isinstance(value, dict):
            return
        if named:
            objects.setdefault(owner, []).append(abs_path)
        jobs.append({
            "id": occ_id(abs_path, "EXTRA"),
            "class": "OCC_EXTRA",
            "op": "EXTRA",
            "path": list(abs_path),
            "expected": "FAIL_EXTRA_KEY",
        })
        required = obj_spec.get("required", [])
        pending = []
        for fname, rule in obj_spec["fields"].items():
            rel = rel_prefix + (fname,)
            fpath = abs_path + [fname]
            if fname in required:
                jobs.append({
                    "id": occ_id(fpath, "ABSENCE"),
                    "class": "OCC_ABSENCE",
                    "op": "ABSENCE",
                    "path": fpath,
                    "expected": "FAIL_SCHEMA",
                })
            if fname not in value:
                continue
            push_site(owner, rel, fpath)
            bad, code = TYPE_WRONG[rule["type"]]
            jobs.append({
                "id": occ_id(fpath, "TYPE"),
                "class": "OCC_TYPE",
                "op": "ASSIGN",
                "path": fpath,
                "value": bad,
                "expected": code,
            })
            child = value[fname]
            if rule["type"] == "object" and isinstance(child, dict) and "ref" in rule:
                pending.append((child, fpath, spec["objects"][rule["ref"]], rule["ref"], (), True))
            elif rule["type"] == "object" and isinstance(child, dict) and "fields" in rule and "ref" not in rule:
                pending.append((child, fpath, {
                    "fields": rule["fields"],
                    "required": rule.get("required", []),
                }, owner, rel, False))
            elif rule["type"] == "array" and isinstance(child, list):
                item = rule.get("items") or {}
                if rule.get("minItems", 0) >= 1:
                    jobs.append({
                        "id": occ_id(fpath, "EMPTY"),
                        "class": "OCC_EMPTY",
                        "op": "ASSIGN",
                        "path": fpath,
                        "value": [],
                        "expected": "FAIL_SCHEMA",
                    })
                if item.get("type") == "object":
                    for index, element in enumerate(child):
                        ipath = fpath + [index]
                        elements.setdefault((owner, rel), []).append(ipath)
                        jobs.append({
                            "id": occ_id(ipath, "ELEMENT_SCALAR"),
                            "class": "OCC_ELEMENT_SCALAR",
                            "op": "ASSIGN",
                            "path": ipath,
                            "value": 1,
                            "expected": "FAIL_SCHEMA",
                        })
                        jobs.append({
                            "id": occ_id(ipath, "ELEMENT_LIST"),
                            "class": "OCC_ELEMENT_LIST",
                            "op": "ASSIGN",
                            "path": ipath,
                            "value": [],
                            "expected": "FAIL_SCHEMA",
                        })
                        if isinstance(element, dict) and "ref" in item:
                            pending.append((element, ipath, spec["objects"][item["ref"]], item["ref"], (), True))
                        elif isinstance(element, dict) and "fields" in item:
                            pending.append((element, ipath, {
                                "fields": item["fields"],
                                "required": item.get("required", []),
                            }, owner, rel + ("item",), False))
                elif item.get("type") in TYPE_WRONG:
                    element_bad, element_code = TYPE_WRONG[item["type"]]
                    for index in range(len(child)):
                        ipath = fpath + [index]
                        elements.setdefault((owner, rel), []).append(ipath)
                        jobs.append({
                            "id": occ_id(ipath, "ELEMENT_TYPE"),
                            "class": "OCC_ELEMENT_TYPE",
                            "op": "ASSIGN",
                            "path": ipath,
                            "value": element_bad,
                            "expected": element_code,
                        })
        for item in pending:
            consider(*item)

    consider(host, [], spec["objects"]["document"], "document", (), True)
    for index, row in enumerate(host["cases"]):
        consider(row, ["cases", index], spec["objects"][row["kind"]], row["kind"], (), True)

    def emit(identifier, class_name, op, path, expected, value=None):
        job = {
            "id": identifier,
            "class": class_name,
            "op": op,
            "path": path,
            "expected": expected,
        }
        if op == "ASSIGN":
            job["value"] = value
        if path is None:
            job["missing_host"] = True
            job["path"] = []
        jobs.append(job)

    def declare(owner, rel, rule, required):
        dotted = owner + "." + ".".join(rel)
        host_path = sites.get((owner, rel), [None])[0]
        bad, code = TYPE_WRONG[rule["type"]]
        emit(rule_id(dotted, "TYPE"), "TYPE", "ASSIGN", host_path, code, bad)
        if required:
            emit(rule_id(dotted, "ABSENCE"), "ABSENCE", "ABSENCE", host_path, "FAIL_SCHEMA")
        if rule["type"] in ("uuid", "nullable_uuid"):
            emit(rule_id(dotted, "UUID"), "UUID", "ASSIGN", host_path, "FAIL_UUID", "not-a-uuid")
        if "const" in rule:
            emit(rule_id(dotted, "CONST"), "CONST", "ASSIGN", host_path, "FAIL_SCHEMA", const_opposite(rule["const"]))
        if rule["type"] == "string" and rule.get("minLength", 0) >= 1:
            emit(rule_id(dotted, "MIN_LENGTH"), "MIN_LENGTH", "ASSIGN", host_path, "FAIL_SCHEMA", "")
        if rule["type"] == "sha256":
            emit(rule_id(dotted, "FORMAT"), "FORMAT", "ASSIGN", host_path, "FAIL_SCHEMA", "g" * 64)
        if rule["type"] == "array":
            emit(rule_id(dotted, "CARDINALITY"), "CARDINALITY", "ASSIGN", host_path, "FAIL_SCHEMA", [])
            item = rule.get("items") or {}
            item_type = item.get("type")
            element_paths = elements.get((owner, rel), [])
            element_path = element_paths[0] if element_paths else None
            if item_type in TYPE_WRONG and item_type != "object":
                element_bad, element_code = TYPE_WRONG[item_type]
                emit(rule_id(dotted, "ELEMENT_TYPE"), "ELEMENT_TYPE", "ASSIGN", element_path, element_code, element_bad)
            if item_type == "string" and item.get("minLength", 0) >= 1:
                emit(rule_id(dotted, "ELEMENT_MIN_LENGTH"), "ELEMENT_MIN_LENGTH", "ASSIGN", element_path, "FAIL_SCHEMA", "")
            if item_type == "object":
                emit(rule_id(dotted, "ELEMENT_SCALAR"), "ELEMENT_SCALAR", "ASSIGN", element_path, "FAIL_SCHEMA", 1)
                emit(rule_id(dotted, "ELEMENT_LIST"), "ELEMENT_LIST", "ASSIGN", element_path, "FAIL_SCHEMA", [])
                if "fields" in item and "ref" not in item:
                    for name, child in item["fields"].items():
                        declare(owner, rel + ("item", name), child, name in item.get("required", []))
        if rule["type"] == "object" and "fields" in rule and "ref" not in rule:
            emit(rule_id(dotted, "EXTRA"), "INLINE_EXTRA", "EXTRA", host_path, "FAIL_EXTRA_KEY")
            for name, child in rule["fields"].items():
                declare(owner, rel + (name,), child, name in rule.get("required", []))
        if rule["type"] == "uuid_map":
            emit(rule_id(dotted, "EMPTY"), "EMPTY", "ASSIGN", host_path, "FAIL_SCHEMA", {})
            if host_path is None:
                for suffix, map_code in (
                    ("MAP_KEY_TYPE", "FAIL_TYPE"),
                    ("MAP_KEY_UUID", "FAIL_UUID"),
                    ("MAP_EMPTY", "FAIL_SCHEMA"),
                    ("MAP_ELEMENT_TYPE", "FAIL_TYPE"),
                    ("MAP_ELEMENT_UUID", "FAIL_UUID"),
                ):
                    emit(rule_id(dotted, suffix), "MAP", "ASSIGN", None, map_code, None)
            else:
                cursor = host
                for part in host_path:
                    cursor = cursor[part]
                sample_key = next(iter(cursor))
                sample_uuid = cursor[sample_key][0]
                emit(rule_id(dotted, "MAP_KEY_TYPE"), "MAP", "ASSIGN", host_path, "FAIL_TYPE", {1: [sample_uuid]})
                emit(rule_id(dotted, "MAP_KEY_UUID"), "MAP", "ASSIGN", host_path, "FAIL_UUID", {"not-a-uuid": [sample_uuid]})
                emit(rule_id(dotted, "MAP_EMPTY"), "MAP", "ASSIGN", host_path, "FAIL_SCHEMA", {sample_key: []})
                emit(rule_id(dotted, "MAP_ELEMENT_TYPE"), "MAP", "ASSIGN", host_path, "FAIL_TYPE", {sample_key: [1]})
                emit(rule_id(dotted, "MAP_ELEMENT_UUID"), "MAP", "ASSIGN", host_path, "FAIL_UUID", {sample_key: ["not-a-uuid"]})

    for obj_name, obj in spec["objects"].items():
        object_path = objects.get(obj_name, [None])[0]
        emit(rule_id(obj_name, "EXTRA"), "EXTRA", "EXTRA", object_path, "FAIL_EXTRA_KEY")
        for fname, rule in obj["fields"].items():
            declare(obj_name, (fname,), rule, fname in obj["required"])
        for index, group in enumerate(obj.get("groups", [])):
            group_path = None
            member = group[0]
            for case_index, row in enumerate(host["cases"]):
                if row.get("kind") == obj_name and all(name in row for name in group):
                    group_path = ["cases", case_index, member]
                    break
            emit(rule_id(f"{obj_name}.GROUP.{index}", "PARTIAL"), "GROUP", "ABSENCE", group_path, "FAIL_SCHEMA")
        for pair in obj.get("same_length", []):
            same_path = None
            for case_index, row in enumerate(host["cases"]):
                if row.get("kind") != obj_name:
                    continue
                left = row.get(pair[0])
                right = row.get(pair[1])
                if isinstance(left, list) and isinstance(right, list) and len(left) >= 2 and len(left) == len(right):
                    same_path = ["cases", case_index, pair[1]]
                    break
            emit(
                rule_id(f"{obj_name}.SAME_LENGTH.{pair[0]}.{pair[1]}", "SHORTEN"),
                "SAME_LENGTH",
                "SHORTEN",
                same_path,
                "FAIL_SCHEMA",
            )
    return jobs


ANCHORS = (
    "rule:negative.expected_original_outcome_body.error_code.ABSENCE",
    "rule:negative.expected_original_outcome_body.error_code.TYPE",
    "rule:negative.expected_original_outcome_body.error_code.MIN_LENGTH",
    "rule:negative.expected_original_outcome_body.EXTRA",
    "rule:negative.expected_original_outcome_body.opaque.TYPE",
    "rule:negative.expected_original_outcome_body.retryable.TYPE",
    "rule:negative.expected_original_outcome_body.terminal.TYPE",
    "rule:negative.expected_original_outcome_body.peer_ack_high_water.TYPE",
    "rule:positive.expected_original_outcome_body.error_code.ABSENCE",
    "rule:positive.expected_original_outcome_body.error_code.TYPE",
    "rule:positive.expected_original_outcome_body.error_code.MIN_LENGTH",
    "rule:positive.expected_original_outcome_body.EXTRA",
    "rule:positive.expected_original_outcome_body.opaque.TYPE",
    "rule:positive.expected_original_outcome_body.retryable.TYPE",
    "rule:positive.expected_original_outcome_body.terminal.TYPE",
    "rule:positive.expected_original_outcome_body.peer_ack_high_water.TYPE",
    "rule:document.initial_keys.ELEMENT_SCALAR",
    "rule:document.initial_keys.ELEMENT_LIST",
    "rule:negative.setup.ELEMENT_SCALAR",
    "rule:negative.setup.ELEMENT_LIST",
    "rule:positive.setup.ELEMENT_SCALAR",
    "rule:positive.setup.ELEMENT_LIST",
    "rule:interleave.steps.ELEMENT_SCALAR",
    "rule:interleave.steps.ELEMENT_LIST",
    "rule:replay_receiver_removed.setup.ELEMENT_SCALAR",
    "rule:replay_receiver_removed.setup.ELEMENT_LIST",
    "rule:replay_cross_tenant.setup.ELEMENT_SCALAR",
    "rule:replay_cross_tenant.setup.ELEMENT_LIST",
)


def execute_jobs(host, jobs):
    seen = []
    for job in jobs:
        if job.get("missing_host"):
            continue
        if job["expected"] not in ALLOWED_SCHEMA_CODES:
            print("coverage code", job["id"], job["expected"])
            return seen, "FAIL_MUTATION_BLIND"
        got = apply_mutation(host, job)
        if isinstance(got, Exception):
            print("coverage exception", job["id"], type(got).__name__)
            return seen, "FAIL_SCHEMA_EXCEPTION"
        if got != job["expected"]:
            print("coverage", job["id"], job.get("path"), got, job["expected"])
            return seen, "FAIL_MUTATION_BLIND"
        seen.append(job["id"])
    return seen, None


def duplicate_key_probes():
    probes = (
        ("schema", SCHEMA),
        ("fixture", FIXTURE),
        ("synthetic", SYNTHETIC),
        ("manifest", MANIFEST),
        ("semantic", SEMANTIC),
        ("unknown", UNKNOWN),
        ("ids", IDS),
    )
    for label, path in probes:
        text = path.read_text(encoding="utf-8")
        _doc, err = load_strict_text(text)
        if err:
            print("duplicate source", label, err)
            return err
        _doc, err = load_strict_text(inject_duplicate_key(text))
        if err != "FAIL_DUPLICATE_KEY":
            print("duplicate probe", label, err)
            return "FAIL_MUTATION_BLIND"
    fixture = FIXTURE.read_text(encoding="utf-8")
    nested, count = re.subn(
        r'"case_id"\s*:\s*"[^"]*"',
        '"case_id": "dup-a", "case_id": "dup-b"',
        fixture,
        count=1,
    )
    if count != 1:
        print("nested duplicate anchor missing")
        return "FAIL_MUTATION_BLIND"
    _doc, err = load_strict_text(nested)
    if err != "FAIL_DUPLICATE_KEY":
        print("nested duplicate", err)
        return "FAIL_MUTATION_BLIND"
    return None


def coverage_failures(doc):
    from collections import Counter

    spec = load_schema()
    if isinstance(spec, str):
        return spec
    if spec is None or not inline_closed(spec):
        return "FAIL_SCHEMA"
    for obj in spec["objects"].values():
        for rule in obj["fields"].values():
            if rule["type"] not in TYPE_WRONG:
                print("coverage unknown type", rule["type"])
                return "FAIL_SCHEMA"
    probe = duplicate_key_probes()
    if probe:
        return probe
    synthetic, err = load_strict_text(SYNTHETIC.read_text(encoding="utf-8"))
    if err:
        return err
    if synthetic.get("id") != "cmp.fd.fx03.synthetic.v0.15":
        return "FAIL_SYNTHETIC_HOST"
    if synthetic.get("proves_product") is not False or synthetic.get("oracle_status") != "NOT_RUN":
        return "FAIL_SYNTHETIC_HOST"
    if not isinstance(synthetic.get("cases"), list) or not synthetic["cases"]:
        return "FAIL_SYNTHETIC_HOST"
    for row in synthetic["cases"]:
        error = case_schema_error(doc, row)
        if error:
            print("synthetic host", row.get("case_id"), error)
            return "FAIL_SYNTHETIC_HOST"
    for kind in ("negative", "positive"):
        spec_obj = spec["objects"][kind]
        optional = [name for name in spec_obj["allowed"] if name not in spec_obj["required"]]
        hosted = set()
        for row in synthetic["cases"]:
            if row.get("kind") == kind:
                hosted |= set(row)
        missing = [name for name in optional if name not in hosted]
        if missing:
            print("synthetic optional", kind, ",".join(missing))
            return "FAIL_SYNTHETIC_HOST"
        body_rule = spec_obj["fields"]["expected_original_outcome_body"]
        for row in synthetic["cases"]:
            if row.get("kind") != kind:
                continue
            body = row.get("expected_original_outcome_body")
            if not isinstance(body, dict):
                print("synthetic body missing", kind)
                return "FAIL_SYNTHETIC_HOST"
            absent = [name for name in body_rule["fields"] if name not in body]
            if absent:
                print("synthetic inline", kind, ",".join(absent))
                return "FAIL_SYNTHETIC_HOST"
    behavioral_positive = next(row for row in doc["cases"] if row["kind"] == "positive")
    host = copy.deepcopy(doc)
    host["cases"] = list(doc["cases"]) + list(synthetic["cases"])
    try:
        expected_rules = expected_schema_rules(spec)
        expected_occ = expected_occurrences(host, spec)
    except RuntimeError as exc:
        print("expected duplicate", exc)
        return "FAIL_COVERAGE_GAP"
    jobs = stack_jobs(host, spec)
    job_ids = [job["id"] for job in jobs]
    if len(job_ids) != len(set(job_ids)):
        print("job duplicate")
        return "FAIL_COVERAGE_GAP"
    job_set = set(job_ids)
    rule_gap = sorted(set(expected_rules) - job_set)
    occ_gap = sorted(set(expected_occ) - job_set)
    if rule_gap or occ_gap:
        print("COVERAGE_GAP catalog")
        for item in (rule_gap + occ_gap)[:60]:
            print(item)
        return "FAIL_COVERAGE_GAP"
    missing_anchors = [item for item in ANCHORS if item not in expected_rules or item not in job_set]
    if missing_anchors:
        print("COVERAGE_GAP anchor")
        for item in missing_anchors:
            print(item)
        return "FAIL_COVERAGE_GAP"
    problems, raw_lines, _slots = raw_disagrees(host, expected_occ)
    if problems:
        print("RAW_GAP")
        for item in problems:
            print(item)
        return "FAIL_COVERAGE_GAP"
    original_count = len(doc["cases"])
    if "expected_original_outcome_body" not in behavioral_positive:
        for job in jobs:
            if not job["id"].startswith("rule:positive.expected_original_outcome_body."):
                continue
            path = job.get("path") or []
            if job.get("missing_host") or not (len(path) >= 2 and path[0] == "cases" and path[1] >= original_count):
                print("positive inline host", job["id"], path)
                return "FAIL_COVERAGE_GAP"
    exercised, error = execute_jobs(host, jobs)
    if error:
        return error
    missing = [job["id"] for job in jobs if job["id"] not in set(exercised)]
    if missing:
        print("COVERAGE_GAP execution")
        for item in missing[:60]:
            print(item)
        return "FAIL_COVERAGE_GAP"
    classes = Counter(job["class"] for job in jobs)
    rule_count = sum(1 for job in jobs if job["id"].startswith("rule:"))
    occ_count = sum(1 for job in jobs if job["id"].startswith("occ:"))
    if rule_count != len(expected_rules) or occ_count != len(expected_occ):
        print(
            "COVERAGE_GAP count",
            f"rules={rule_count}/{len(expected_rules)}",
            f"occurrences={occ_count}/{len(expected_occ)}",
        )
        return "FAIL_COVERAGE_GAP"
    keyword_error = unknown_keyword_problems(spec)
    if keyword_error:
        return keyword_error
    endings = line_ending_regression()
    if endings:
        return endings
    reference, ref_err = load_semantic()
    if ref_err:
        print(ref_err)
        return ref_err
    drifts = semantic_file_problems(reference, spec)
    if drifts:
        print("SEMANTIC_DRIFT")
        for item in drifts[:40]:
            print(item)
        return "FAIL_SEMANTIC_DRIFT"
    probed = cardinality_probes(
        spec, doc, host, synthetic["cases"], reference, len(expected_rules), len(expected_occ)
    )
    if isinstance(probed, str):
        return probed
    ident_error = id_manifest_problems(expected_rules, expected_occ)
    if ident_error:
        return ident_error
    for line in probed:
        print("CARDINALITY_STABLE " + line)
    print(
        f"SEMANTIC_BINDINGS count={len(reference['bindings'])} "
        f"digest={reference['bindings_sha256']} ratification=PENDING_HUMAN_APPROVAL "
        "independence=NOT_RATIFIED new_gov_01=OPEN"
    )
    print(
        f"ID_MANIFEST rules={len(expected_rules)} occurrences={len(expected_occ)} "
        "enumerated_outside_checker=true"
    )
    print("DSL_CLOSED unknown_keyword=rejected nullable_keyword=rejected json_schema_keywords=rejected")
    print("COERCION int_rejects_bool=true bool_rejects_int=true nullable_accepts_null=true")
    print("CANONICAL_TEXT_SHA256 lf_crlf=equal raw_bytes_differ=true content_edit=detected git_blob_id=not_used")
    print("FULL_PRODUCT_COVERAGE false")
    print(f"COVERAGE_RULES declared={len(expected_rules)} exercised={rule_count} gap=0")
    print(f"COVERAGE_OCCURRENCES declared={len(expected_occ)} exercised={occ_count} gap=0")
    print("COVERAGE_CLASSES " + " ".join(f"{name}={classes[name]}" for name in sorted(classes)))
    print("RAW " + " ".join(raw_lines))
    print(
        f"COVERAGE_HOSTS behavioral_cases={len(doc['cases'])} "
        f"synthetic_cases={len(synthetic['cases'])} synthetic_proves_product=false"
    )
    print(
        "COVERAGE_BASIS expected_walk=independent job_walk=iterative "
        "raw_slot_count=independent product_input_exhaustive=false"
    )
    print(
        f"V12_CATALOG_REJECTED rules={V12_REJECTED_RULES} "
        f"occurrences={V12_REJECTED_OCCURRENCES} "
        "reason=inline_objects_and_object_elements_omitted"
    )
    print("COVERAGE_TOTAL_PASS not_claimed")
    print("DUPLICATE_KEY schema=rejected fixture=rejected synthetic=rejected manifest=rejected semantic=rejected unknown=rejected ids=rejected nested_fixture=rejected")
    print("COVERAGE_SYNTHETIC oracle_status=NOT_RUN")
    print("ORACLE_EXECUTION NOT_RUN")
    print("POSTGRESQL NOT_RUN")
    print("COVERAGE_GAP count=0")
    return None

def carrier_ignored(row):
    other = dict(row)
    other["stream_id"] = "carrier-mutated"
    return digest_of(row) == digest_of(other)


def main():
    doc, error = load_strict_text(FIXTURE.read_text(encoding="utf-8"))
    if error:
        return fail(error)
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
    covered = coverage_failures(doc)
    if covered:
        return fail(covered)
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
    print("SCHEMA required_and_types=enforced missing=FAIL_SCHEMA")
    print("PROVES_PRODUCT false")
    print("STATIC_ACK_V15_CHECK PASS_FIXTURE_ONLY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
