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
    print("wrote %d characters to %s" % (len(written), OUTPUT_PATH))


if __name__ == "__main__":
    main()
