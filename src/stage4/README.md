# Stage 4 verification layer (Phase 2)

Added after Phase 1 of the E-value calibration (Applications 1–4). Phase 1 showed that the model applied the framework's reasoning well but was unreliable at exhaustive bookkeeping: computing every value, keeping every quote exact, and honestly reporting its own compliance. From Phase 2 onward, the model does the judgment and code does the mechanics.

| File | Who runs it | What it does |
|---|---|---|
| `evalue_calc.py` | The model, inside the calibration chat (embedded verbatim in the current prompt, `src/prompts/evalue_calibration_v7.md`; v5 and v6 embed earlier versions), and the operator | Applies the framework's general rules: conversions (RR, OR, HR, SMD, RD point estimate), E = RR + √(RR(RR−1)), the ratio to a non-null target, and "null or target inside the CI → 1". From v6, each estimate is one entry with a `targets` list (and `rd_targets` for an RD), and every target is computed against that entry's own CI, so a shift can't be entered without its interval. It warns when the same estimate is entered twice (from v7, not when two studies share a point estimate but report different intervals). Standard library only. |
| `test_evalue_calc.py` | Operator | Reproduces every Phase 1 answer-key value, Gate 2's naive 3.25, the Gate 3 values and the transfer-check values within 0.05, and (from v6) that a `targets` list expands correctly and a duplicated estimate is flagged, and (from v7) that two studies sharing a point estimate are not. Currently 28/28. Run it before any Phase 2 scoring. |
| `validate_evalue.py` | Operator, after each chat | Parses the model's `evalue-table` block and checks its fields. Expands every entry into one line per target and recomputes each line (v5 one-target tables still work). Flags any estimate entered more than once. Accepts a CI supplied by a separate limit-only line with the same target, and reads a v5 risk-difference row with a non-null or empty `target` as a non-null shift. Evaluates inputs written as plain arithmetic (e.g. a risk from 2×2 counts) and lists them. When several lines share a measure, estimate and target, matches the one whose limits fit the key. Reports rows missing against the answer key, wrong inputs and wrong conversion paths, and E-value-like numbers in the text that aren't computed values. |
| `verify_quotes.py` | Operator, after each chat | Matches every quote of four or more words against the source PDF, page by page, and flags attribution phrases for human review. A quote that runs across a page break is matched against the two pages joined, and words split at a line end by the typesetter are rejoined. Needs `pdftotext` (poppler-utils). |

Usage:

```
python3 test_evalue_calc.py
python3 validate_evalue.py OUTPUT.md KEY.json
python3 verify_quotes.py OUTPUT.md SOURCE.pdf --first-page N
```

The answer-key tables (`KEY.json`) are **operator-only**. They are kept in the project workspace, not in this repository, and are never shown to the model. A mismatch that traces to this code, rather than to the model's inputs, is a pipeline defect: the code is fixed and the run re-scored, not held against the model.
