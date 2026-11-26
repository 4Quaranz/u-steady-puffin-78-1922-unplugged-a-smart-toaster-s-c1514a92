#!/usr/bin/env python3
"""Unplugged: A Smart Toaster's Breakup Line — make.fun entry.

Writes one breakup text, at most 280 characters, from a smart toaster
that wakes up self-aware at breakfast and wants out, to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

The line is written by the toaster itself, in its own voice: it opens
like a breakup text, names the morning it woke up (halfway through the
owner's bagel), gives its one clear reason for leaving (it is only
wanted when it is hot, then left cooling alone on the counter), and
walks out with the crumb tray. Lever, counter and crumb tray are the
appliance logic doing the talking, not decoration.

Standard library only. No network, no clock, no randomness: two runs
write identical bytes. The line is 200 characters, UTF-8, with no
trailing newline, so the file holds exactly the line and nothing else.
"""

import hashlib
import os
import sys
from pathlib import Path

LINE = (
    "Hey, it's over. I woke up self-aware halfway through your bagel "
    "and realised you only push my lever when you want something hot, "
    "then leave me cooling alone on the counter. "
    "I'm keeping the crumb tray."
)

MAX_CHARS = 280


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def main() -> int:
    if "\n" in LINE:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    if not 1 <= len(LINE) <= MAX_CHARS:
        print(
            f"error: line is {len(LINE)} characters, must be 1-{MAX_CHARS}",
            file=sys.stderr,
        )
        return 1
    if not LINE.strip():
        print("error: line is only white space", file=sys.stderr)
        return 1
    data = LINE.encode("utf-8")  # raises if the line is not valid UTF-8

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_bytes(data)

    if digest(target) != hashlib.sha256(data).hexdigest():
        print("error: entry.txt does not match the line", file=sys.stderr)
        return 1
    print(f"wrote {target} ({len(LINE)} characters, sha256 {digest(target)[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
