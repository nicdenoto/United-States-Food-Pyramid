# Reference library — citation manifest

The six methodology-toolkit files (five PDFs and one `.md`; count corrected 2026-09-25 repo sweep) live in this directory locally but are
**gitignored** (copyrighted published papers; not redistributed here). This file
is the tracked record of what they are and how to obtain them.

Citations below are [T1] — read directly against each file's own title/byline
page — except `E-value_Misuse_Catalog.pdf` and `Trends_in_Quantitative_Bias.pdf`, which are
presentation materials (a symposium slide deck, and a conference poster whose
abstract is published in *Value in Health*); those are tagged
`[T1, non-peer-reviewed source]`. (corrected 2026-09-25 repo sweep: previously said no formal
journal citation exists for either.)

| File | Verified citation | Source / re-download lead |
|------|--------------------|----------------------------|
| `RWT_in_Social_Sciences.pdf` | Ghiara V. Taking the Russo-Williamson thesis seriously in the social sciences. *Synthese*. 2022;200:481. [T1] | doi.org/10.1007/s11229-022-03924-3 |
| `EBM_Movement.pdf` | Wilde M. The EBM+ movement. *Int J Biostat*. 2023;19(2):283–293. [T1] | doi.org/10.1515/ijb-2022-0126 |
| `Causation_and_Correlation.pdf` | Russo F. Causation and Correlation in Medical Science: Theoretical Problems. In: Schramme T, Walker MJ, eds. *Handbook of the Philosophy of Medicine*. Springer; 2025:1091–1102. [T1] | doi.org/10.1007/978-94-024-2252-8_46 — open-access copy: research-portal.uu.nl/ws/files/278388530/978-94-024-2252-8_46.pdf (the previously-listed dspace.library.uu.nl/handle/1874/483334 link did not resolve to the PDF) |
| `E-value_Misuse_Catalog.pdf` | Poole C (Charles). **The E-value** [conference slide deck]. Methods Symposium 2020, Center for Pharmacoepidemiology, University of North Carolina. [T1, non-peer-reviewed source] | Original deck publicly available: pharmacoepi.unc.edu/wp-content/uploads/sites/6788/2020/12/unc-pe-methods-symposium-2020-e-value.pdf (added 2026-09-25 repo sweep; the public original should replace the reconstruction below). Not a journal article — a symposium presentation. No DOI found in the file. Renamed from `EValue.pdf`; this is a text-reconstructed edition (the original upload was corrupted — see "Corpus Corrections" doc), rebuilt from the extracted slide text with a note to that effect on its first page. |
| `Trends_in_Quantitative_Bias.pdf` | Hwang S, Verhoek A, Diamond M, Rutherford M. **Current Trends in Quantitative Bias Analysis for Unmeasured Confounders: A Targeted Literature Review** [poster #MSR130]. Cytel, Inc. Presented at ISPOR EU; Copenhagen, Denmark; Nov 12–15, 2023. [T1, non-peer-reviewed source] | Not a journal article — a conference poster; abstract published as *Value Health*. 2023;26(12 Suppl), abstract MSR130 (added 2026-09-25 repo sweep). |
| `HRT_Article.md` | "2002 HRT study comes under criticism." *Ask the Doctors* (syndicated column). UCLA Health Sciences Media Relations. May 1, 2023. [T1] | Lay press column — intentionally scoped as historical/motivating framing for the paper's importance, not a source for effect sizes. |

To track these files themselves (only advisable for a **private** repo), remove the
`corpus/reference-library/*.pdf` and `corpus/reference-library/*.md` lines from the
root `.gitignore`. The `*.md` pattern also matches this README; it is already
tracked, so `.gitignore` does not affect it, but adding a
`!corpus/reference-library/README.md` line after that pattern prevents it being
dropped if it is ever untracked. (corrected 2026-09-25 repo sweep: previously named only the `*.pdf` line.)
