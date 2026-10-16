"""Canonical SHA-256 for textual JSON.

Line endings are normalized to LF before the digest. CRLF and lone CR
compare equal to LF. This digest is not a Git blob id and must not be
stored as one. Git blob identity stays with git cat-file.
"""
import hashlib
from pathlib import Path


def canonical_json_text(data):
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("textual JSON hash requires bytes")
    return bytes(data).replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def canonical_json_sha256(data):
    return hashlib.sha256(canonical_json_text(data)).hexdigest()


def canonical_json_file_sha256(path):
    return canonical_json_sha256(Path(path).read_bytes())
