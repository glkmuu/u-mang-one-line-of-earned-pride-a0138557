"""One Line of Earned Pride — make.fun entry.

Candidates (one line each, all <= 240 chars), scored against the judge's
four criteria:

1. Genuine earned pride — a small person doing something hard, or a long
   effort finally paying off; quiet, not boastful.
2. A concrete scene with a real person — a place, an object, a small number.
3. Lands in a single read — no setup to decode, the image arrives at once.
4. Freshness — no trophy, podium, graduation, or "finally won the big game".

Candidates
----------
1. (131 chars) "After eleven years of night shifts, my mother read her
   first letter out loud — slowly, in her own kitchen, without asking for
   help."
   C1 strong — eleven years of effort, earned; C2 vivid — night shifts,
   her own kitchen; C3 lands cleanly; C4 clean, no worn trope. Runner-up.

2. (139 chars) "The night my father fixed the neighbour's leaking roof in
   the rain, he came home soaked and said nothing — the dry ceiling said
   it for him."
   C1 good — quiet competence; C2 strong — rain, soaked, dry ceiling;
   C3 the closer is the best image here; C4 clean. Close second.

3. (140 chars) "She carried the same cracked suitcase to the bus stop for
   four years; the morning she didn't have to, she walked past it like an
   old friend."
   C1 good — long grind, release; C2 concrete — cracked suitcase, bus
   stop; C3 the "old friend" turn lands; C4 clean. Strong, just behind #5
   — the pride is implied rather than shown in an act.

4. (137 chars) "He practised the same three chords every night for a year;
   at his daughter's wedding he played them straight through, and nobody
   laughed."
   C1 good — a year of practice, one performance; C2 concrete — three
   chords, a wedding; C3 the "nobody laughed" beat lands; C4 close to a
   wedding trope, but the pride is in the practice, not the ceremony. Mid.

5. (127 chars) "My grandmother learned to write her name at seventy-two,
   and signed the hospital form herself — the nurse had to wait, and did."
   C1 strongest — learning to write at 72 is earned pride in its purest
   form; C2 a real scene — hospital form, a waiting nurse; C3 the final
   clause ("and did") is the whole landing, in one read; C4 clean — no
   trophy, no graduation, no big game. WINNER.

6. (130 chars) "After six failed harvests, the old farmer pulled one ripe
   tomato from the cracked soil and held it up like it was the morning
   sun."
   C1 good — six failed harvests; C2 concrete — cracked soil, one tomato;
   C3 vivid; C4 the "morning sun" simile is a touch ornate for a quiet
   moment. Good, not great.

7. (129 chars) "He mended the same pair of boots eleven times; the day
   they finally tore for good, he set them by the door like retired
   soldiers."
   C1 decent — but the pride is in the boots' retirement, not in an act
   of his; C2 concrete — eleven mends; C3 lands; C4 "retired soldiers" is
   a slightly worn image. Mid.

8. (138 chars) "She saved a coin a day for three years to buy her son a
   bicycle; when he rode it down the hill, she ran after him laughing,
   out of breath."
   C1 good — three years of saving; C2 concrete — a coin a day, a bicycle;
   C3 lands warmly; C4 clean — but the pride is the son's ride as much as
   hers, so the earned-pride focus is split. Good.

Winner: candidate 5. It is the only candidate where the earned act (learning
to write her name) and the quiet payoff (signing the form herself, unhurried,
while a nurse waits) are the same moment, with a small real number (72), a
concrete object (the hospital form), and a closing beat that lands in one
read — no trophy, no podium, no graduation, no big game anywhere near it.
"""

import os

ENTRY = (
    "My grandmother learned to write her name at seventy-two, and signed "
    "the hospital form herself \u2014 the nurse had to wait, and did."
)


def validate(text):
    """Check the entry against the gate: 1-240 chars, one line, clean.

    Returns (True, "") on success, else (False, reason).
    """
    if not isinstance(text, str):
        return False, "not a string"
    if not 1 <= len(text) <= 240:
        return False, "length %d outside 1-240" % len(text)
    if not text.strip():
        return False, "only whitespace"
    if text != text.strip():
        return False, "leading/trailing whitespace"
    if "\n" in text or "\r" in text:
        return False, "more than one line"
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        return False, "control character present"
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False, "not valid UTF-8"
    return True, ""


def main():
    """Write the winning entry to entry.txt and verify it on disk.

    Writes the entry byte-for-byte (no trailing newline), then reads the
    file back and compares it byte-for-byte against the entry encoded as
    UTF-8. Any mismatch raises ValueError, so a corrupt or truncated
    write can never pass silently.
    """
    ok, reason = validate(ENTRY)
    if not ok:
        raise ValueError("ENTRY failed validation: %s" % reason)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Written byte-for-byte, no trailing newline: the file is the entry.
    expected = ENTRY.encode("utf-8")
    with open(path, "wb") as f:
        f.write(expected)
    # Read-back verification: what is on disk must be exactly the entry.
    with open(path, "rb") as f:
        on_disk = f.read()
    if on_disk != expected:
        raise ValueError(
            "entry.txt read-back mismatch: wrote %d bytes, read %d bytes"
            % (len(expected), len(on_disk))
        )


if __name__ == "__main__":
    main()
