# Prompt diffs

Unified diffs between consecutive E-value calibration prompt versions, generated with
`diff -u` from the files in `src/prompts/`. They are derived files: the prompt files
themselves are the record, and these only make each revision's changes easy to read.
Regenerate with:

```
for i in 1 2 3 4 5 6; do j=$((i+1)); diff -u src/prompts/evalue_calibration_v$i.md src/prompts/evalue_calibration_v$j.md > src/prompts/diffs/evalue_v${i}_to_v${j}.diff; done
```

| Diff | Revision | Reason (full record in the version log, `src/prompts/README.md`) |
|---|---|---|
| `evalue_v1_to_v2.diff` | v1 → v2 | Application1 failures: compute point and CI E-values for every estimate and shift, reproduce derivations, consistency check, conservatism wording, label outside claims. |
| `evalue_v2_to_v3.diff` | v2 → v3 | Application2 failures: four-item closing checklist, page-citation rule, filled-in template unquoted. |
| `evalue_v3_to_v4.diff` | v3 → v4 | Application3 failures: target-inside-CI check for every estimate and shift; adjustment-depth rule. |
| `evalue_v4_to_v5.diff` | v4 → v5 | Phase 2: JSON input table plus embedded calculator; attribution and page rules from the folded prompt-only v5 draft. |
| `evalue_v5_to_v6.diff` | v5 → v6 | One entry per estimate with a `targets` list; `rd_targets`; "a result, not an artifact"; duplicate-estimate check. |
| `evalue_v6_to_v7.diff` | v6 → v7 | Duplicate-estimate check narrowed so different studies sharing a point estimate aren't flagged (v6 never run). |
