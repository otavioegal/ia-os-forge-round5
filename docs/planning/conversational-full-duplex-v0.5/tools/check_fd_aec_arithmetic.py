#!/usr/bin/env python3
"""Static arithmetic of the v0.5 AEC fixture.

Not an AEC implementation, not CMP-FD-O28, not a product test.
"""
import sys


def reference(index):
    if (index // 40) % 2 == 0:
        return 8000
    return -8000


def echo(index):
    if index < 480:
        return 0
    return reference(index - 480) // 2


def clamp(value):
    if value > 32767:
        return 32767
    if value < -32768:
        return -32768
    return value


def main():
    checks = [
        ("i1199_echo", echo(1199), -4000),
        ("i1199_mic", clamp(echo(1199) + 32000), 28000),
        ("i1159_echo", echo(1159), 4000),
        ("i1159_sum", echo(1159) + 32000, 36000),
        ("i1159_mic", clamp(echo(1159) + 32000), 32767),
        ("i1040_mic", clamp(echo(1040) + 16000), 20000),
        ("i1000_mic", clamp(echo(1000) + 16000), 12000),
        ("i480_echo", echo(480), 4000),
    ]
    for name, got, expected in checks:
        if got != expected:
            print(f"FAIL_AEC_ARITHMETIC {name} {got} {expected}")
            return 1
        print(f"OK {name} {got}")
    print("STATIC_AEC_ARITHMETIC PASS_FIXTURE_ONLY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
