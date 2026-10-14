#!/usr/bin/env python3
"""Run the static fixture checks. Not a product test and not an oracle run."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
NEG = ROOT / "fixtures" / "negative"
POS_EVENTS = ROOT / "fixtures" / "CMP-FD-FX-01-events.json"
POS_VECTORS = ROOT / "fixtures" / "CMP-FD-FX-01-digest-vectors.json"
CHECKER = TOOLS / "check_fd_fx01_digests.py"


def run(args):
    proc = subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


def expect(label, args, code_substr, expect_zero):
    status, out, err = run(args)
    text = (out + err).strip()
    ok = (status == 0) if expect_zero else (status != 0 and code_substr in text)
    print(f"CASE {label} exit={status} ok={ok}")
    print(text)
    return ok


def main():
    ok = True
    ok &= expect(
        "positive-digests",
        [str(CHECKER)],
        "PASS_FIXTURE_ONLY",
        True,
    )
    ok &= expect(
        "duplicate-event-id",
        [
            str(CHECKER),
            "--events",
            str(NEG / "duplicate-event-id.json"),
            "--vectors",
            str(POS_VECTORS),
            "--require-count",
            "0",
        ],
        "FAIL_DUPLICATE_EVENT_ID",
        False,
    )
    ok &= expect(
        "orphan-vector",
        [
            str(CHECKER),
            "--events",
            str(POS_EVENTS),
            "--vectors",
            str(NEG / "orphan-vector.json"),
            "--require-count",
            "0",
        ],
        "FAIL_ORPHAN_VECTOR",
        False,
    )
    ok &= expect(
        "duplicate-json-key",
        [
            str(CHECKER),
            "--events",
            str(NEG / "duplicate-key.json"),
            "--vectors",
            str(POS_VECTORS),
            "--require-count",
            "0",
        ],
        "FAIL_DUPLICATE_JSON_KEY",
        False,
    )
    ok &= expect(
        "bad-sha256",
        [
            str(CHECKER),
            "--events",
            str(POS_EVENTS),
            "--vectors",
            str(NEG / "bad-sha256.json"),
            "--require-count",
            "0",
        ],
        "FAIL_BAD_SHA256",
        False,
    )
    ok &= expect(
        "bad-length-type",
        [
            str(CHECKER),
            "--events",
            str(POS_EVENTS),
            "--vectors",
            str(NEG / "bad-length-type.json"),
            "--require-count",
            "0",
        ],
        "FAIL_BAD_LENGTH",
        False,
    )
    ok &= expect(
        "aec-arithmetic",
        [str(TOOLS / "check_fd_aec_arithmetic.py")],
        "STATIC_AEC_ARITHMETIC PASS_FIXTURE_ONLY",
        True,
    )
    ok &= expect(
        "ack-shape",
        [str(TOOLS / "check_fd_fx02_ack.py")],
        "STATIC_ACK_FIXTURE_CHECK PASS_FIXTURE_ONLY",
        True,
    )
    if not ok:
        print("STATIC_FIXTURE_SUITE FAIL_FIXTURE_ONLY")
        return 1
    print("STATIC_FIXTURE_SUITE PASS_FIXTURE_ONLY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
