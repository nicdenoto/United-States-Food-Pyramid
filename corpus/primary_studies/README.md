# Primary studies — citation manifest

Full-text copies of the primary meta-analyses/systematic reviews that
back-end appendix sections cite for specific outcome estimates. Like
`corpus/reference-library/`, these are copyrighted published papers: present
locally for extraction and verification, but **gitignored** and not
committed (see `corpus/primary_studies/*.pdf` and the explicit
`corpus/primary_studies/Reynolds2019_SupplementaryAppendix.md` line in the root
`.gitignore`; corrected 2026-09-25 repo sweep, previously named only the `*.pdf` line).

This directory exists separately from `corpus/reference-library/` on
purpose: the reference library is the methodology/framework toolkit (RWT,
EBM+, E-value, QBA); this directory is primary *evidence* — the actual
studies a claim's GRADE rating and effect estimates trace back to. Mixing
the two would blur the front-end/back-end/primary-source distinction the
whole corpus is built on.

| File | Verified citation | Feeds claim(s) | Acquired |
|------|--------------------|-----------------|----------|
| `Hu2023_WholeGrains_AJCN.pdf` | Hu H, Zhao Y, Feng Y, Yang X, Li Y, Wu Y, et al. Consumption of whole grains and refined grains and associated risk of cardiovascular disease events and all-cause mortality: a systematic review and dose-response meta-analysis of prospective cohort studies. *Am J Clin Nutr*. 2023;117(1):149–159. doi:10.1016/j.ajcnut.2022.10.010 | WG-01 (all-cause mortality, CVD fields) | Supplied by Nic, 2026-09-14 (open-web copy was paywalled/blocked) |
| `Schlesinger2019_FoodGroupsAdiposity_AdvNutr.pdf` | Schlesinger S, Neuenschwander M, Schwedhelm C, Hoffmann G, Bechthold A, Boeing H, Schwingshackl L. Food Groups and Risk of Overweight, Obesity, and Weight Gain: A Systematic Review and Dose-Response Meta-Analysis of Prospective Studies. *Adv Nutr*. 2019;10(2):205–218. doi:10.1093/advances/nmy092 | WG-01 (obesity field — note: Schlesinger's actual outcome is the combined "overweight/obesity" endpoint, not obesity alone) | Supplied by Nic, 2026-09-14 (open-web copy was paywalled/bot-blocked) |
| `Reynolds2019_CarbQuality_Lancet.pdf` | Reynolds A, Mann J, Cummings J, Winter N, Mete E, Te Morenga L. Carbohydrate quality and human health: a series of systematic reviews and meta-analyses. *Lancet*. 2019;393(10170):434–445. doi:10.1016/S0140-6736(18)31809-9 | WG-01 (colorectal cancer, T2D fields; also the RCT-evidence and heterogeneity detail in the stage 3/4 deepening pass) | Initially verified via an open-access institutional-repository copy (`discovery.dundee.ac.uk`); full PDF then supplied by Nic, 2026-09-14, and every figure re-verified by direct read |
| `Reynolds2019_SupplementaryAppendix.md` | Supplementary appendix to the above (*Lancet*, pp. 35–50 = Appendix C, "Wholegrain intake data relating to the prospective observational studies"). Text-converted from Nic's own `ReynoldsAppendix.pdf` for extraction. | WG-01 (exact I² and p-heterogeneity for the CRC and T2D whole-grain rows, both high-vs-low and per-15g dose-response; aggregate follow-up duration — CRC 9.5 y / T2D 10.8 y; sensitivity-analysis detail per Table C:2 footnotes i and j) | Open-web fetch of the Lancet-hosted appendix returned HTTP 403 and no open-access mirror bundles it (see the gap-chase pass); supplied directly by Nic, 2026-09-14, as a markdown conversion of his own saved PDF |
| `Schlesinger2019_SupplementaryData.pdf` | Full supplementary data bundle for the Schlesinger entry above (Supplemental Methods 1, Supplemental Tables 1–17, Supplemental Figures 1–24). | WG-01 (Supplemental Table 5: per-study follow-up duration for the 6 whole-grain/adiposity studies — 4, 5, 12, 12, 13, 16 y, i.e. ranging 4–16 y) | Open-web fetch blocked (`academic.oup.com` and `advances.nutrition.org` both 403, PMC served reCAPTCHA); Nic supplied the PDF directly, 2026-09-14; Supplemental Table 5 read and extracted |

To track these PDFs themselves (only advisable for a **private** repo),
remove the `corpus/primary_studies/*.pdf` line from the root `.gitignore`.
