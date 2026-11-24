#!/usr/bin/env python3
"""Write one haiku about debugging to /output/entry.txt.

Fixed string, standard library only, deterministic: no network, no
randomness, no time dependence.
"""

import os

HAIKU = (
    "midnight, cursor blinks\n"
    "the log says the tests all passed\n"
    "the users still crash"
)

# Hand-counted syllables per word, so the program can refuse to emit a
# haiku that is not 5-7-5 before it writes anything.
SYLLABLES = {
    "midnight": 2, "cursor": 2, "blinks": 1,
    "the": 1, "log": 1, "says": 1, "tests": 1, "all": 1, "passed": 1,
    "users": 2, "still": 1, "crash": 1,
}


def validate(text):
    lines = text.split("\n")
    if len(lines) != 3:
        raise ValueError(f"expected 3 lines, got {len(lines)}")
    if len(text) > 200:
        raise ValueError(f"haiku is {len(text)} chars, over the 200 limit")
    for line, want in zip(lines, (5, 7, 5)):
        words = line.replace(",", "").split()
        got = sum(SYLLABLES[w] for w in words)
        if got != want:
            raise ValueError(f"line {line!r} has {got} syllables, want {want}")


def main():
    validate(HAIKU)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(HAIKU)
    os.chmod(tmp, 0o644)
    os.replace(tmp, path)


if __name__ == "__main__":
    main()
