"""Make the AI Judge Laugh: Developer Excuses — writes one funny single-line
developer's excuse to /output/entry.txt.

The excuse, in the developer's own voice: production is down not because of
some exotic failure, but because the "temporary" fix — the one everyone
agreed would be replaced properly next sprint — quietly lived in production
for three years and has now, like any long-overlooked employee, handed in
its notice. The twist is the personification: the throwaway hack outlasted
everyone's memory of it and quit on its own schedule.
"""

import os
import sys

# The entry text is also kept in entry.txt next to this file, so the line
# can be read without running the program. When that file is present the
# program cross-checks it against the embedded text and refuses to run
# if they ever drift apart.
SOURCE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")

EXCUSE = (
    "Production is down because the 'temporary' fix I shipped three years "
    "ago just handed in its notice."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def validate(text):
    """Enforce the gate: UTF-8 text of 1 to 200 characters, a single line,
    not only whitespace, with no leading or trailing whitespace. Fail loudly
    instead of writing an invalid entry."""
    if not isinstance(text, str):
        raise ValueError("entry must be text, got %r" % type(text))
    text.encode("utf-8")  # raises if not valid UTF-8-encodable text
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line, got a line break")
    return text


def main():
    excuse = validate(EXCUSE)
    if os.path.exists(SOURCE_FILE):
        with open(SOURCE_FILE, "r", encoding="utf-8") as f:
            filed = f.read()
        if filed != excuse:
            print(
                "entry.txt (%r) does not match embedded excuse (%r)"
                % (filed, excuse),
                file=sys.stderr,
            )
            sys.exit(1)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(excuse)
    # Read back and confirm what landed is exactly the excuse.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        written = f.read()
    if written != excuse:
        print(
            "verification failed: wrote %r, read back %r" % (excuse, written),
            file=sys.stderr,
        )
        sys.exit(1)
    # The gate counts every character, so a stray trailing newline would
    # change the entry; the written file must end exactly on the last word.
    assert not written.endswith("\n"), "output must not end with a newline"
    assert "\n" not in written, "output must be a single line"
    print("wrote %d characters to %s" % (len(written), OUTPUT_PATH))


if __name__ == "__main__":
    main()
