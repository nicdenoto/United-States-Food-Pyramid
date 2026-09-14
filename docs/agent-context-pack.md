# Project Context Pack — DGA Causal-Claims Audit

*A standalone briefing for any AI agent (Claude, GPT, or otherwise) picking up work on this project. Compiled by Claude from the project's saved drafts, memory, the task ledger, and the `Archive.zip` repo shared with GPT (extracted and cross-checked against what already exists in the Claude-side project). Written so an agent with zero prior context can get productive immediately.*

*Compiled: September 13, 2026. Deadline: full submission-ready paper by **October 1, 2026**.*

---

## 1. Who this is for and what the project is

Nic is a high-school researcher (rising senior, upstate NY) holding a research position at SUNY Poly, supervised by the SUNY Poly AIX team. The project is a semi-automated pipeline that audits causal claims in public-health nutrition guidance.

**Core research question:** whether the certainty a guidance document *asserts* for a causal claim matches the *evidence structure* that actually supports it. The project does not try to determine whether a recommendation is correct — it asks whether the confidence behind it is earned.

**Constructive aim:** where certainty outruns support, the project does not stop at naming the gap. It supplies a concrete piece of existing contrary evidence (mechanistic or anthropological) that would run against the claim as stated — supplementing with evidence the guidance omitted, not proposing new research.

**Primary corpus (fixed):** *The Scientific Foundation for the Dietary Guidelines for Americans, 2025–2030* and its appendices. The main report + its Scientific Foundation is the **front-end** (carries GRADE-labeled claims, what a policymaker reads); the appendices are the **back-end** (systematic/umbrella reviews, evidence tables, ROBIS/GRADE assessments — what actually supports those claims). The pipeline audits both layers, since a claim can fail at either independently.

**Project origin note:** the earliest framing (see §7, NotebookLM logs from June 2026) was broader — auditing causal claims across arbitrary epidemiology papers/organizations against a six-dimension rubric (causal inference strength, statistical validity, mechanistic coherence, among others). This narrowed into the current, more tightly scoped DGA-specific audit built around RWT as the single governing framework. Treat the six-dimension-rubric framing as superseded unless Nic says otherwise.

---

## 2. Theoretical framework

The evaluative backbone is the **Russo-Williamson Thesis (RWT)**: a causal claim is established only when there is both (a) **difference-making evidence** (RCTs, cohort studies, clinical opinion — does the outcome vary with the cause) and (b) **mechanistic evidence** (a biological/physiological pathway linking cause to effect). Neither leg alone is sufficient:

- Difference-making evidence alone can't rule out a spurious association (confounding, selection bias, analytical artifact).
- Mechanistic evidence alone is vulnerable to **masking** — a counteracting, concurrent mechanism that cancels the net effect, making the claimed mechanism real but causally inert.

RWT is epistemological, not metaphysical — it's about what evidence is needed to *establish* causation, and it treats establishment as fallible. Its corollary is **evidential pluralism**: causal claims rest on multiple, interdependent evidence types rather than one gold standard. This is also the **EBM+** critique of conventional evidence-based medicine, which the project explicitly invokes: conventional EBM hierarchies rank RCTs above mechanistic/clinical evidence; EBM+ argues both should be appraised together.

**Supporting appraisal apparatus** (used alongside RWT, not instead of it): GRADE (certainty ratings, upgrade/downgrade moves), the Bradford Hill criteria, the Cochrane Collection / RoB 2, the STROBE Statement, the E-value, quantitative bias analysis (QBA), and — where design-specific evaluation is warranted — ROBIS, AMSTAR-2, ROBINS-I, and CONSORT.

**A "finding,"** in this project's specific sense, is: the construction of a document's evidence hierarchy together with how its foundational papers perform against the E-value, the Cochrane Collection, GRADE, and the evaluation LLM.

---

## 3. Methodology / pipeline (the six stages)

This is now consolidated from a previously-produced supervisor-facing methodology proposal found in the shared archive (`Documentation For Maker copy/Methodology and Introduction Proposal.pdf` — see §7, this appears to be the "appraisal-apparatus" document referenced as already-written but missing from the Claude-side project until this archive was shared). The general pipeline:

1. **Organization and claim selection.** Government/public bodies are selected against four criteria: (a) reasoning/evidence is public and accessible; (b) impact is widespread and severe; (c) references are documentable, organized, efficient (DOIs, PMIDs, PDFs, downloadable tables); (d) recommendations are firm/confident claims. Claim identification itself stays a human responsibility — not delegated to a model. For this project, stages 1–2 are already fixed to the DGA corpus rather than run against an open set of organizations.
2. **Reference and sub-reference collection.** References supporting a claim, and their own references ("sub-references"), are collected and stored as Markdown in an organized corpus. **Open question:** whether this collection is code-only, LLM-assisted, or both is still undetermined.
3. **Evidence hierarchy and chain of authority.** An LLM, via custom prompt, reconstructs which evidence types a claim relies on (clinical trial, mechanistic explanation, meta-analysis, expert opinion, systematic review) and to what severity.
4. **Framework appraisal.** Sub-references are evaluated for their contribution to the primary references using GRADE, Cochrane, STROBE, Bradford Hill, E-value, and QBA. The LLM is anchored on pre-existing papers demonstrating correct use of each framework, each paired with a gold-standard study illustrating what makes a study pass or fail under that system, before its judgments on the live corpus are trusted.
5. **Statistical evaluation.** A statistical system applied across the stored references/sub-references. **Fully open:** its exact form is undetermined, and how it should combine with the qualitative framework appraisals (rather than sit beside them, disconnected) is an explicitly unresolved question.
6. **Gap identification and constructive challenge.** Where a claim's certainty outruns its evidence — commonly, resting entirely on difference-making evidence with the mechanistic leg thin or unaddressed — the gap is filled with existing mechanistic/anthropological evidence chosen specifically to run contrary to the claim, mirroring the beta-carotene case (mechanism pointed against the difference-making results that were later overturned).

**Provenance discipline** (a control layered across every stage): every claim is tagged as verified against a primary document, sourced from a secondary reference/search, or inferred from structure. Conflating these tiers is a methodological error independent of whether the claim is later correct.

**Newly surfaced in the archive, not yet in the Claude-side Methodology draft — fold in:**
- **Provenance signals** tracked across the corpus: instances of *author-evidence overlap* (a subject-matter expert rating the certainty of a study they themselves authored) and *disclosed financial ties that co-vary with the direction of a recommendation*. This is a real, distinct methodological control not previously captured in the Claude-side drafts.
- The explicit general-corpus pattern: **almost all DGA claims rest entirely on difference-making evidence** (RCTs/controlled trials), leaving the mechanistic leg thin corpus-wide. Whole grains is flagged elsewhere (see §5) as a notable *exception* to this pattern, not the rule — keep that distinction clear when writing the case sections.

**LLM calibration (Justification / Parameters / Replicability)** — drafted on the Claude side, not in the archive:
- *Justification:* the model's judgments on evidentiary questions don't fail visibly the way code does — a wrong evidentiary call reads as a plausible one — so its output is checked against known-correct human applications of each criterion before being trusted on the live corpus, rather than trusted on fluency alone.
- *Parameters (open):* number/source of gold-standard examples per criterion, exact prompt templates (calibration vs. live analysis), model/version, and the agreement threshold that counts as "calibrated" are all still unset — need Nic's numbers.
- *Replicability (open):* requires versioning the calibration set, exact prompts per stage, model identifier/version, and a research log of every human correction — including the Week 2–3 AI-correction transcripts flagged elsewhere as not yet recovered.

---

## 4. Current state of the DGA application

Work completed so far on the live corpus:
- A structural mapping of the two-layer document (front-end claims/certainty labels vs. back-end evidence).
- An **RWT completeness audit** across major causal claims — which carry both legs, which stand on one alone.
- A **symmetric burden-of-proof check** — holding the document's own stated evidentiary standards back against its own preferred conclusions (it applies a directional standard when supporting its recommendations; the audit applies that same standard back).
- An examination of how selectively Bradford Hill considerations and GRADE upgrades/downgrades are applied across claims.
- Provenance-signal recording (author-evidence overlap, financial ties — see §3).
- Appendix chapters examined: saturated fat (4.6, 4.7), whole grains (4.4), highly processed foods (4.1), added sugars/SSBs (4.2), protein (4.9), processed meats (4.10).

**Case-level findings (analysis done, prose not yet written — see task ledger §8):**
- **Whole grains:** rests on a predominantly observational umbrella review (~85% cohort-based); RCT evidence covers only surrogate markers. Here mechanism is the *stronger* leg — the inversion of the corpus-wide pattern. Internal contradiction: the whole-grains chapter argues a fiber/matrix mechanism, while a crossover trial in the refined-carbohydrate chapter shows milled whole-wheat bread produces glycemic responses nearly identical to white bread. The report acknowledges phytate-mineral binding as a bioavailability concern in its vegetarian chapter but never applies it back to the whole-grains recommendation; zinc absorption is the clearest, most defensible casualty.
- **Vegetables:** the only major food group with no dedicated evidence-review appendix and no GRADE rating at all — accepted on surrogate-marker RCTs, borrowed grain/fiber endpoint data, and mechanism alone.
- **Saturated fat:** positioned as a fourth reversal case, distinct because it is a policy document performing a reversal in real time rather than retrospectively (appendix 4.6/4.7).

---

## 5. The historical reversal cases (HRT / beta-carotene / vitamin E)

These are the project's motivating precedents — evidence that mechanistically-plausible, difference-making-supported claims can still fail. Detailed, citable evidence was recovered from a NotebookLM deep-research pass in the archive (`LM Conversations copy/NTBKLM DeepResearch1.md`) that is **not yet in the Claude-side Introduction draft**, which had flagged these as needing sourcing. Tier: **[T2 — secondary/AI-research-sourced; verify against primary trial reports before final citation]**, per the project's own provenance discipline.

**Hormone Replacement Therapy (HRT).** Observational consensus (25-study meta-analysis through 1997: RR 0.70 for estrogen alone, RR 0.66 for combined estrogen-progestin, favoring HRT) collapsed when the Women's Health Initiative (WHI) RCT halted early in 2002, reporting a 29% *increase* in CHD risk (RR 1.29, 95% CI 1.02–1.63) plus increased breast cancer risk. Explanations: the **timing hypothesis** (Nurses' Health Study users started therapy near menopause onset, ~age 50; WHI participants averaged age 63, often 10+ years post-menopause — estrogen is cardioprotective on healthy young arteries but can destabilize plaque on older, already-atherosclerotic ones); the WHI used conjugated equine estrogen + MPA (Premarin/Prempro), structurally different from human estradiol; and detection bias from unblinding due to side effects inflated the raw WHI risk ratio (adjusting for it drops 1.28 to a non-significant 1.02).

**Beta-carotene.** Cohort studies linked high dietary/serum beta-carotene to lower lung cancer and cardiovascular risk. Two RCTs reversed this: **ATBC** (29,133 Finnish male smokers, 20mg/day beta-carotene) found a 16% *increase* in lung cancer (RR 1.16) and 8% increase in all-cause mortality; **CARET** (18,314 smokers/asbestos workers, 30mg beta-carotene + retinyl palmitate) was halted 21 months early after a 28% increase in lung cancer (RR 1.36) and 17% increase in mortality (RR 1.59). Mechanism: pharmacologic doses of beta-carotene oxidize rapidly in the free-radical-rich environment of a smoker's lung, generating pro-oxidant metabolites that upregulate CYP1A1, destroy retinoic acid, impair RAR-β signaling, and increase proliferation (c-Fos/c-Jun upregulation, PCNA increase) — the opposite of the assumed antioxidant-protective mechanism. This is the case where the mechanism, correctly understood, pointed *against* the claim from the start.

**Vitamin E.** Cohort studies showed lower CHD in vitamin E supplement users. The **HOPE trial** (9,541 high-risk patients, 400 IU/day) found no benefit on the primary CV endpoint (RR 1.05, p=0.33) and significantly *more* heart failure (RR 1.17, p=0.02). **GISSI-Prevenzione** (11,000 heart attack survivors) found no protective effect and a 50% increase in heart-failure risk among those with reduced ejection fraction. The **Women's Health Study** (39,815 healthy women, 600 IU every other day) found no overall CV/HF benefit, though prespecified subgroups showed some benefit in older women. Mechanism: alpha-tocopherol becomes a reactive tocopheryl radical after neutralizing a lipid peroxyl radical; without adequate co-antioxidant recycling (vitamin C, ubiquinol — often deficient in advanced cardiovascular disease), the radical accumulates and *propagates* lipid peroxidation instead of stopping it.

Mendelian randomization studies for both beta-carotene and vitamin E later confirmed the RCT direction genetically (vitamin E: OR 1.05 for CAD per 1mg/L increase; beta-carotene: OR 1.10 for MI), reinforcing that the original observational associations were confounded rather than the RCTs being anomalous.

**Supporting QBA/confounding-detection frameworks surfaced in this same research** (useful for the Methodology's E-value/QBA discussion): Mendelian randomization, negative controls (the influenza-vaccination/all-cause-mortality example is a strong illustrative case — a "protective" association appeared even in the pre-flu season, when the vaccine could not possibly be working, revealing healthy-user bias), and the three-tier QBA hierarchy (simple / multidimensional / probabilistic bias analysis).

---

## 6. Voice and standards to match

- Formal academic prose, long semicolon-chained sentences building across clauses, parallel "the issue with X is… / the issue with Y is…" constructions, earnest register.
- Characteristic phrases already in use: "evidence structures," "held to a high standard of evidential confidence," "to what severity," "chain of authority," "front-end/back-end distinction."
- Superscript citations, numbered reference list.
- **Provenance-tier discipline is non-negotiable**: every claim gets tagged as primary-verified, secondary-sourced, or structure-inferred. Conflating tiers has previously been flagged as a real evidentiary error, not a style nitpick.
- Constructive, not just diagnostic: every case analysis should end with a proposed evidentiary correction, not only a critique.

---

## 7. Source inventory — what exists where

**In `Archive.zip` (shared with GPT) but not currently in the Claude-side project — bring these in:**
- `Documentation For Maker copy/Methodology and Introduction Proposal.pdf` — a complete, polished methodology/intro proposal; effectively the "appraisal apparatus" document referenced as already-written. Now saved into the Claude project (see below).
- `Documentation For Maker copy/Scientific Report_508.pdf` — the main 90-page DGA front-end report (distinct from the appendices, which the Claude project already has). Not yet uploaded to the Claude project.
- `LM Conversations copy/NTBKLM Conversation 1.md` and `NTBKLM DeepResearch1.md` — NotebookLM research logs; the second contains the sourced HRT/beta-carotene/vitamin E trial data reproduced in §5.
- A screenshot of the Notes app showing the original task list plus sidebar note titles (`The Cochrane Collection`, `PNT DATA`, `Claude Questioning`, `Industry Skills`, and a scraper API key note) — mostly confirms provenance of the existing task notes; the API-key note should stay out of any shared context file.

**In the Claude-side project but not in `Archive.zip` — bring these to GPT if it needs them:**
- `claude/Draft - Introduction and Background.md` — full prose rewrite of the rough intro notes.
- `claude/Draft - Methodology.md` — full pipeline write-up including the RWT-as-operationalizing-lens subsection and the LLM-calibration (Justification/Parameters/Replicability) subsection.
- `claude/Paper Master Outline and Oct 1 Timeline.md` — the master section-by-section outline and week-by-week schedule.
- The **task ledger** itself (see §8) — a live, checkable tracker; not a static document, so it can't be handed to GPT as a file, but its current state is summarized below.

**Present on both sides (no action needed):** the six methodology-toolkit PDFs (RWT in Social Sciences, E-value, Trends in Quantitative Bias, HRT Article, EBM(+) Movement, Causation and Correlation), the DGA appendices PDF, and all of the raw "Task 1A/1B/1Ca," "Methodology Summary," "Very Rough Pipeline," "Defining a Finding," and "Epidemiology Research" notes.

**Still missing on both sides:** an actual itemized **claim inventory** (each DGA claim mapped to its appendix evidence and GRADE rating) — referenced as if it exists, but not found in the archive either. This needs to be rebuilt from the appendix chapters listed in §4, or Nic needs to locate it elsewhere.

---

## 8. Task system (the ledger)

Progress is tracked in a live, checkable web ledger (published as a Claude Artifact, not a static file): **19 tasks**, grouped into three weeks running to the Oct 1 deadline, each broken into individually-checkable subtasks stored in a shared database so state persists across sessions and devices.

- **Week 1 (Sep 13–19) — Framework and methods locked:** Introduction & Background (drafted), locate/rebuild the appraisal-apparatus section (**now substantially resolved** — see §7/§3), locate/rebuild the claim inventory (**still open**), RWT integration into Methodology + outline (done), LLM training write-up in three parts — Justification (done), Parameters (open, needs Nic's numbers), Replicability (open), and resolving remaining to-be-determined pipeline questions.
- **Week 2 (Sep 20–26) — Case analysis written up:** whole grains, vegetables, and saturated fat case analyses (all open — analysis done, prose not written), the HRT/beta-carotene/vitamin E historical section (open, scope still needs Nic's confirmation — full case studies vs. short precedent paragraphs), and an internal-consistency read-through.
- **Week 3 (Sep 27–Oct 1) — Discussion, conclusion, polish:** Discussion, Conclusion/Limitations/Future Work, full reference pass, supervisor review buffer (Dr. Schneider/Dr. Abeya), final proofread and submission.

Each task's pill shows live subtask completion (e.g. "2/6"); a distinct flag marks anything blocked on Nic specifically (a missing file, a numeric answer, a scope decision) versus ordinary open writing work.

---

## 9. Open decisions needing Nic's input

1. **Claim inventory** — locate or authorize a rebuild from the appendix chapters.
2. **LLM calibration parameters** — example counts per criterion, example sourcing, prompt templates, model/version, agreement threshold.
3. **LLM calibration replicability** — what's actually being versioned/logged; recovery status of the Week 2–3 correction transcripts.
4. **Statistical evaluation stage** (§3, stage 5) — its form, and how it combines with the qualitative framework appraisals, is entirely undetermined.
5. **Scope of HRT/beta-carotene/vitamin E** — full case-study treatment or short historical precedent in the Introduction.
6. **Where case-analysis prose should live** — a single running manuscript document, or separate per-case files.
7. **Submission format/venue** — not stated anywhere in either the archive or the Claude-side project; needed to know final formatting requirements.

---

*End of context pack. Any agent picking this up should treat §§1–6 as ground truth for scope and framework, §7 as the map of where source material actually lives, and §§8–9 as the live to-do state as of the compile date above.*
