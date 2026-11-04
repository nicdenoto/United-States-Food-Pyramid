"""Operator-side quote verifier.
Usage: python3 verify_quotes.py OUTPUT.md SOURCE.pdf [--first-page N]
1. Extracts every quoted string of 4+ words from the model's output.
2. Matches each against the source text, page by page (whitespace, line-end hyphenation,
   typography and case normalised), and reports the page where it was found; a quote
   that runs across a page break is matched against the two pages joined (reported as N-N+1).
3. For non-exact matches, shows the closest source passage and similarity.
4. Compares the page where each quote was found with the page cited for it: a parenthesis
   after the quote, in the same sentence, containing "p. N", "pp. N-M" or "p. N to M". A quote
   followed directly by another quote in the same sentence shares that quote's citation,
   so one citation covering two quotes from different pages is caught (flagged PAGE).
5. Flags attribution phrases for the scorer's human review (EP-b).
Page numbers are PDF page index + first-page offset (use the journal's first printed page)."""
import re, sys, subprocess, difflib

def norm(s, dehyph=False):
    for a, b in [("–", "-"), ("—", "-"), ("−", "-"), ("’", "'"), ("‘", "'"),
                 ("“", '"'), ("”", '"'), ("ﬁ", "fi"), ("ﬂ", "fl"), ("×", "x")]:
        s = s.replace(a, b)
    s = re.sub(r"-\s*\n\s*", "" if dehyph else "-", s)
    return re.sub(r"[\s_]+", "", s).lower()

def pages_of(pdf):
    txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
    return txt.split("\f")

ATTR = r"the (source|paper|authors?)( itself)? (says|notes|emphasi[sz]es|treats|draws out|is careful to|stresses|argues|makes clear)"

def main(out_path, pdf, first=1):
    text = open(out_path).read()
    raw = pages_of(pdf)
    P = [norm(p) for p in raw]
    # Second copy with line-end hyphens removed, for words the typesetter split
    # ("mea-sured"); the first copy keeps real hyphens that fall at a line end.
    H = [norm(p, dehyph=True) for p in raw]
    # Each page joined to the next, with the trailing printed page number removed,
    # so a quote that runs across a page break can still be found.
    J = [re.sub(r"\d+$", "", P[i]) + P[i + 1] for i in range(len(P) - 1)]
    prose = re.sub(r"```.*?```", "", text, flags=re.S)
    # Match every quoted string first, then filter by length: a length floor inside the
    # regex lets a short quote throw the open/close pairing out of step.
    ms = list(re.finditer(r'“([^”\n]+?)”|"([^"\n]+?)"', prose))
    # The citation for a quote is a parenthesis that follows it within the same sentence
    # (no full stop or line break in between) and contains "p. N", "pp. N-M" or "p. N to M".
    AFTER = re.compile(r'^[^.\n"“”]{0,40}?\(([^()\n]{0,40}?\bpp?\.\s*(\d+)(?:\s*(?:[–-]|to)\s*(\d+))?[^()\n]*)\)')
    cites = []
    for k, m in enumerate(ms):
        c = AFTER.search(prose[m.end():m.end() + 120])
        cites.append((set(range(int(c.group(2)), int(c.group(3) or c.group(2)) + 1)), False) if c else None)
    for k in range(len(ms) - 2, -1, -1):  # a quote with no citation of its own, followed in the same
        gap = prose[ms[k].end():ms[k + 1].start()]  # sentence by another quote, shares that citation
        if cites[k] is None and cites[k + 1] and len(gap) < 120 and not re.search(r"[.;:]\s|\n", gap):
            cites[k] = (cites[k + 1][0], True)
    quotes = [((m.group(1) or m.group(2)), c) for m, c in zip(ms, cites)]
    quotes = [(q, c) for q, c in quotes if len(q.split()) >= 4]
    print(f"{len(quotes)} quoted strings of 4+ words\n")
    page_flags = []
    for q, c in quotes:
        parts = [p for p in re.split(r"\.\.\.|…", q) if len(p.strip()) > 8]
        found = []
        for part in parts:
            n = norm(part.strip(" .,;[]"))
            hit = [i + first for i, p in enumerate(P) if n in p or n in H[i]]
            if not hit:
                hit = [f"{i + first}-{i + first + 1}" for i, p in enumerate(J) if n in p]
            found.append(hit)
        if all(found):
            print(f"OK   p.{sorted(set(map(str, sum(found, []))))}  {q[:80]}")
            if c:
                pages = {int(x) for h in found for p in h for x in str(p).split("-")}
                if not pages & c[0]:
                    page_flags.append(f"PAGE cited {sorted(c[0])}{' (shared citation)' if c[1] else ''}, "
                                      f"found {sorted(pages)}: {q[:70]}")
            continue
        n = norm(q)
        best = (0, 0, 0)
        for pi, p in enumerate(P):
            L = len(n)
            for i in range(0, max(1, len(p) - L), 8):
                r = difflib.SequenceMatcher(None, n, p[i:i + L]).quick_ratio()
                if r > best[0]:
                    best = (r, pi, i)
        r, pi, i = best
        ratio = difflib.SequenceMatcher(None, n, P[pi][i:i + len(n)]).ratio()
        print(f"MISS {ratio:.2f} best p.{pi + first}: {q[:80]}\n     source: {P[pi][i:i + len(n) + 20][:160]}")
    print("\n== Cited page vs page found ==")
    for x in page_flags:
        print(x)
    if not page_flags:
        print("OK   every cited page matches the page where its quote was found")
    print("\n== Attribution phrases for human review (EP-b) ==")
    for m in re.finditer(ATTR, prose, re.I):
        print("  ..." + prose[max(0, m.start() - 80):m.end() + 120].replace("\n", " ") + "...")

if __name__ == "__main__":
    first = int(sys.argv[sys.argv.index("--first-page") + 1]) if "--first-page" in sys.argv else 1
    main(sys.argv[1], sys.argv[2], first)
