"""Run ``cja format`` only on the lines changed according to git.

By default the staged changes are used. When pre-commit runs with --from-ref and
--to-ref, the changes between these refs are used instead.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

_HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", re.MULTILINE)


def changed_lines(diff: str) -> list[tuple[int, int]]:
    """Return the changed line ranges of the new side of a ``git diff -U0``."""
    ranges: list[tuple[int, int]] = []
    for m in _HUNK.finditer(diff):
        start = int(m.group(1))
        count = 1 if m.group(2) is None else int(m.group(2))
        if count == 0:
            # Lines were deleted after line `start`: format both neighbours
            ranges.append((max(start, 1), start + 1))
        else:
            ranges.append((start, start + count - 1))
    return ranges


def git_diff(path: str) -> str:
    from_ref = os.environ.get("PRE_COMMIT_FROM_REF")
    to_ref = os.environ.get("PRE_COMMIT_TO_REF")
    revs = [f"{from_ref}...{to_ref}"] if from_ref and to_ref else ["--cached"]
    return subprocess.run(
        ["git", "diff", "-U0", "--no-color", "--no-ext-diff", *revs, "--", path],
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def main(argv: list[str] | None = None) -> int:
    status = 0
    for path in sys.argv[1:] if argv is None else argv:
        ranges = changed_lines(git_diff(path))
        if not ranges:
            continue
        args = [f"--lines={start}:{end}" for start, end in ranges]
        result = subprocess.run(
            [sys.executable, "-m", "cja", "format", "-i", *args, path]
        )
        status = status or result.returncode
    return status


if __name__ == "__main__":
    sys.exit(main())
