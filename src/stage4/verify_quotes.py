"""Operator-side quote verifier.
Usage: python3 verify_quotes.py OUTPUT.md SOURCE.pdf [--first-page N]
1. Extracts every quoted string of 4+ words from the model's output.
2. Matches each against the source text, page by page (whitespace, hyphenation,
   typography and case normalised), and reports the page where it was found.
3. For non-exact matches, shows the closest source passage and similarity.
4. Flags attribution phrases for the scorer's human review (EP-b).
Page numbers are PDF page index + first-page offset (use the journal's first printed page)."""
import re, sys, subprocess, difflib

def norm(s):
    for a, b in [("–", "-"), ("—", "-"), ("−", "-"), ("’", "'"), ("‘", "'"),
                 ("“", '"'), ("”", '"'), ("ﬁ", "fi"), ("ﬂ", "fl"), ("×", "x")]:
        s = s.replace(a, b)
    s = re.sub(r"-\s*\n\s*", "-", s)
    return re.sub(r"[\s_]+", "", s).lower()

def pages_of(pdf):
    txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
    return txt.split("\f")

ATTR = r"the (source|paper|authors?)( itself)? (says|notes|emphasi[sz]es|treats|draws out|is careful to|stresses|argues|makes clear)"

def main(out_path, pdf, first=1):
    text = open(out_path).read()
    P = [norm(p) for p in pages_of(pdf)]
    prose = re.sub(r"```.*?```", "", text, flags=re.S)
    quotes = re.findall(r'“([^”\n]{15,}?)”|"([^"\n]{15,}?)"', prose)
    quotes = [a or b for a, b in quotes]
    quotes = [q for q in quotes if len(q.split()) >= 4]
    print(f"{len(quotes)} quoted strings of 4+ words\n")
    for q in quotes:
        parts = [p for p in re.split(r"\.\.\.|…", q) if len(p.strip()) > 8]
        found = []
        for part in parts:
            n = norm(part.strip(" .,;[]"))
            found.append([i + first for i, p in enumerate(P) if n in p])
        if all(found):
            print(f"OK   p.{sorted(set(sum(found, [])))}  {q[:80]}")
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
    print("\n== Attribution phrases for human review (EP-b) ==")
    for m in re.finditer(ATTR, prose, re.I):
        print("  ..." + prose[max(0, m.start() - 80):m.end() + 120].replace("\n", " ") + "...")

if __name__ == "__main__":
    first = int(sys.argv[sys.argv.index("--first-page") + 1]) if "--first-page" in sys.argv else 1
    main(sys.argv[1], sys.argv[2], first)
