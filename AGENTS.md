# Repository Guidance

## Start here

- Treat this directory as the repository root. Read `README.md` and this file
  before making changes.
- Check `git status --short` first. Preserve all user changes and never reset,
  discard, or overwrite unrelated work.
- Respond in the language used by the user. Keep public repository prose and
  filenames in English unless the user explicitly requests another language.
- Read only the report, evidence, notebook, or script files relevant to the
  current task; use the file map below to avoid unnecessary exploration.

## Project purpose

This public repository documents a reproducible quality and capability analysis
of Turkish or Turkish-focused Hugging Face datasets contributed by course
participants. It contains reports, computed evidence, a Jupyter notebook and HTML
render, ten static figures, and machine-readable capability mappings. Raw
datasets are intentionally not redistributed here. The current scope is fixed in
`config/verified_baseline.json`; do not hardcode a dataset or row count in prose
that the baseline does not enforce.

## Source-of-truth order

Use this order when reconciling conflicting statements:

1. `outputs/data_quality_profiles.json` and
   `outputs/cross_dataset_overlap.json` for computed metrics.
2. The executed notebook for calculation logic and displayed tables.
3. `outputs/manual_findings.json` for reviewed qualitative findings.
4. `appendix/dataset_manifest.json` and
   `appendix/capability_mapping.csv` for capability mappings.
5. Markdown reports and README files, which are derived presentation layers.

Do not manually change computed metrics to make a report read better. Correct
the calculation or reviewed evidence first, then update every dependent report,
figure, notebook output, and HTML artifact.

Local raw snapshots live in the Git-ignored `data/` directory. They are
available for row-level reprofiling on this workstation but are never part of
the public Git history. A fresh clone must recreate them with
`scripts/download_hf_datasets.py` before running the profiler.

## Access blocks and snapshot sources

A dataset that is enabled but unreadable is never dropped from scope. It carries
an `access_block` record in `config/datasets.json` with the status, the check
date, and the verbatim HTTP evidence. The downloader re-verifies every declared
block on each run, the profiler records it in `outputs/excluded_datasets.json`
instead of failing, and validation requires the enabled registry scope to equal
the profiled datasets plus the recorded blocks. An *undeclared* incomplete
snapshot still stops the pipeline. If a declared block stops applying, the
pipeline fails until the record is removed and the dataset is downloaded.

When the Dataset Viewer cannot serve a public repository, the downloader falls
back to the revision-pinned raw files and writes a receipt carrying the
repository revision, the published blob size and SHA-256, and the locally
recomputed values. A fallback snapshot counts as complete only when the byte
size and checksum both match and every line parses. Never use `--allow-incomplete`
for a final report, and never present a partial snapshot as a full one.

Anonymous Hugging Face API access is rate limited (HTTP 429 with no
`Retry-After`). The downloader spaces its requests and widens that spacing after
each 429; `--resume` skips datasets whose recorded snapshot is complete and still
matches the live revision, so an interrupted batch does not restart from zero.

The downloader sends a bearer token when `HF_TOKEN` or `HUGGINGFACE_HUB_TOKEN` is
set in the environment, which raises the rate limit and reaches gated
repositories the account has been granted. Set it in your own shell session:

```powershell
$env:HF_TOKEN = "<your token>"
```

Never hardcode a token in a repository file, a command line that gets logged, or
a committed script. This repository is public. If a token is ever pasted into a
shared transcript, issue log, or chat, revoke it at
<https://huggingface.co/settings/tokens> and create a new one. The audit runs
without a token; authentication only changes speed and gated reach, never the
recorded results.

## Verified analytical baseline

The following values were rechecked against all local raw rows on 22 July 2026:

- 45 analyzed datasets and 87,831 total rows, plus 2 datasets recorded as
  access-blocked and excluded from every total.
- 87,228 conversation rows, 500 product-table rows, and 103 catalog rows.
- 175,427 messages, 0 invalid roles, 0 rows whose prompt equals its own answer,
  and 2 empty assistant messages (both in `filiz-yalcin/identity-finetune`).
- 5,033 exact duplicate rows, of which 4,851 are in
  `sedayzc/turkish-electronics-product-comparison-recommendation`, whose
  repository stores two versions of one corpus that the Viewer serves as a
  single split.
- 67,470 assistant messages with a non-empty `thinking` field, plus 29 rows
  carrying it as a row-level column in
  `sadecebirisii/turkish-llm-authority-bypass-safety-sft`.
- 17,454 schema-bound JSON answers in `nursimakgul/meb-soru-uretme`; the other
  3,420 answers in that dataset are not JSON-shaped, and none are malformed JSON.
- 462 string-encoded null fields, all in `sk75/sahin_identity`.
- 3,853 time-sensitive regex matches across the collection, 297 of them in
  `namruni/meb-ogretmen-soru-cevap`. These are match counts, not unique-row counts.
- 1,456 prompt families map to more than one distinct answer.
- 30 cross-dataset pairs share 87 user prompts and 0 assistant answers; the
  overlap concentrates on canonical identity questions.
- 0 rows appear in more than one split of the same dataset.
- 12 datasets ship a data card with no body; 5 have no README at all.
- 82,798 distinct rows after exact deduplication.
- 11,277 near-duplicate answers and 26,475 near-duplicate prompts at a token-set
  Jaccard threshold of 0.85. The comparison is exact, not hashed or sampled.
- Language signal: 43 datasets Turkish, 2 English. This is a heuristic from
  Turkish-only letters plus stopwords, not a classifier.
- Repository validation ran 1,568 checks and all passed. The validator reports
  its own check count, so this number must be taken from a fresh run rather than
  carried forward.

Do not reuse a check count, row total, or duplicate figure from an earlier scope.
Every number above is regenerated by the pipeline and enforced by
`config/verified_baseline.json`.

Definitions:

- Normalized duplicate rate is the number of extra copies after the first item
  in each case- and punctuation-normalized text family divided by all rows.
- Near-duplicate rate counts rows whose text shares at least 85% of its tokens
  with an earlier row. It is a different measure from the normalized duplicate
  rate and the two must not be quoted interchangeably.
- Time-sensitive counts are regex matches and must not be described as unique
  rows unless a separate row-level calculation is performed.
- The language signal is a heuristic. Do not present it as language detection.

Determinism is a requirement, not an aspiration. Any ordering derived from a
`set` or `dict` iteration must carry an explicit tiebreaker, because Python
randomizes string hashing between processes and an unbroken tie silently makes
the profile irreproducible. Verify by running the profiler twice and comparing
`outputs/data_quality_profiles.json` byte for byte.

## Content and editorial rules

- Evaluate task fitness, structure, content patterns, provenance, and required
  preparation. Do not introduce scores, rank positions, or winner/first-place
  language.
- Do not use license status or train/validation/test split availability as
  evaluation criteria. Source metadata may remain in raw evidence, but it is not
  part of the report judgment.
- The provenance-and-rights dimension is the one deliberate exception, and it is
  not a loophole. Recording that a dataset was scraped from a live storefront and
  declares no license is a reuse fact. Writing that it is therefore a weaker
  dataset is the forbidden judgement. Keep licence out of every other dimension.
- A raw pattern count is never a finding. Privacy and register signals must be
  read and classified before they are reported: in this collection the same
  regexes produced a genuine finding, a false positive from log output, and a
  false positive from a proverb.
- Do not attribute the analysis or selections to an automated system.
- Preserve contributor names and official Hugging Face links exactly.
- Use established English capability names: Identity, Tool Calling,
  Conversation, Instruction Following, Structured Output, Math, and Coding.
- Use plain, precise language. Define specialized terms at first use when a
  mixed audience may not know them.
- Keep Markdown as the report format; do not reintroduce Word deliverables.
- Distinguish direct coverage, partial coverage, and conversion sources. A
  conversion source is not a ready-made training dataset for that capability.

## Language and naming

- `README.md`, `reports/*.md`, and `reports/figures/README.md` are English.
- The notebook, generated notebook HTML, and reviewed JSON evidence retain their
  original Turkish analysis text unless a task explicitly requests translation.
- Keep public filenames descriptive, English, lowercase, and hyphenated where
  practical. Do not rename files without updating every local Markdown link,
  script output path, and README tree entry.

## File map

- `README.md`: public entry point, verified summary, dataset links, and commands.
- `config/datasets.json`: enabled dataset IDs, contributor names, contributor
  sources, and declared access blocks.
- `config/verified_baseline.json`: reviewed expectations used by validation.
- `config/evaluation_criteria.json`: the seven assessment dimensions, their
  thresholds, and what each measure cannot tell you.
- `outputs/topic_overlap.json`: TF-IDF vocabulary similarity between datasets.
- `data/`: local raw snapshots, Dataset Viewer rows, and raw-file fallback rows;
  ignored by Git.
- `outputs/excluded_datasets.json`: enabled datasets that cannot be analyzed,
  with the re-verified HTTP evidence for each block.
- `reports/dataset-technical-assessment.md`: main evidence-backed assessment.
- `reports/model-capability-mapping.md`: seven-capability mapping and gaps.
- `reports/file-guide.md`: repository navigation.
- `reports/figures/README.md`: figure definitions, sources, and caveats.
- `reports/figures/*.png`: ten generated report figures.
- `notebook/huggingface_dataset_quality_analysis.ipynb`: executed analysis.
- `notebook/huggingface_dataset_quality_analysis.html`: generated notebook view.
- `outputs/*.json`: fixed inventory, profiles, overlap, and reviewed findings.
- `appendix/*`: machine-readable capability mapping.
- `scripts/download_hf_datasets.py`: snapshot downloader and inventory updater.
- `scripts/profile_datasets.py`: row-level schema and quality profiler.
- `scripts/build_notebook.py`: dynamic notebook builder and executor.
- `scripts/generate_report_charts.py`: deterministic Matplotlib figure builder.
- `scripts/validate_repository.py`: read-only repository integrity check.

## Change workflow

1. Inspect the relevant evidence before editing a claim.
2. Make the smallest coherent change. Preserve unrelated content and binary
   artifacts.
3. If profile or mapping data changes, update all dependent Markdown tables and
   prose.
4. If chart data, labels, or styling changes, run the chart generator and inspect
   all ten PNG files for clipping, collisions, honest scales, and readable labels.
5. If notebook code or source text changes, execute it top to bottom and
   regenerate the HTML from the executed notebook.
6. Run the repository validator and `git diff --check` before handing off.
7. Do not commit or push unless the user explicitly asks. The remote repository
   is public, so never stage credentials, raw datasets, local paths, or private
   working files.

## Adding new datasets

When the user supplies additional Hugging Face datasets, run the complete
workflow from this repository root while keeping raw collection out of Git:

1. Confirm the exact Hugging Face URLs and, when the report requires it, the
   contributor name associated with each dataset.
2. Add the IDs and contributor names to `config/datasets.json`; do not remove or
   rename the existing entries without an explicit scope change.
3. Run `scripts/download_hf_datasets.py`. It stores revision-pinned metadata,
   README snapshots, and Dataset Viewer rows under the ignored `data/` folder
   and updates `outputs/source_inventory.json`.
4. Run `scripts/profile_datasets.py`. Do not use `--allow-incomplete` for a final
   report. Inspect every row and dataset card/repository evidence needed for the task.
   Reconcile schema differences before aggregating metrics.
5. Review and extend `outputs/manual_findings.json`, the capability mapping, and
   the Markdown reports. Computed profiles are evidence, not a substitute for
   reading representative rows and source documentation.
6. Rebuild the executed notebook with `scripts/build_notebook.py`, regenerate
   its HTML and all figures, and visually inspect the outputs.
7. After the expanded analysis is reviewed, update
   `config/verified_baseline.json` so the validator describes the new fixed scope.
8. Update all affected totals, dataset tables, capability mappings, figure labels,
   README text, and validator expectations as one coherent change. Commit only
   reviewed outputs; never force-add `data/`.
9. State any dataset that could not be downloaded or fully parsed. Do not silently
   treat a partial sample as a complete analysis.

## Environment setup

Use Python 3.12 from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

On this workstation, the bare `python` command may resolve to an unconfigured
pyenv shim. In Codex Desktop, load the bundled workspace dependencies and use
the returned Python executable when no configured system interpreter is
available. Do not hardcode a user-cache runtime path into repository files.

Do not add a dependency unless it is necessary for the requested change. Update
`requirements.txt` when a runtime dependency is introduced.

## Build and validation commands

Download or refresh every enabled dataset in `config/datasets.json`:

```powershell
.\.venv\Scripts\python scripts\download_hf_datasets.py
```

Rebuild row-level profiles and overlap evidence:

```powershell
.\.venv\Scripts\python scripts\profile_datasets.py
```

Build and execute the notebook from the current profiles:

```powershell
.\.venv\Scripts\python scripts\build_notebook.py
```

Run the repository integrity check after report, notebook, mapping, or figure
changes:

```powershell
.\.venv\Scripts\python scripts\validate_repository.py
```

Regenerate all figures:

```powershell
.\.venv\Scripts\python scripts\generate_report_charts.py
```

Rebuild the notebook's standalone HTML:

```powershell
.\.venv\Scripts\python -m jupyter nbconvert --to html --output-dir notebook notebook\huggingface_dataset_quality_analysis.ipynb
```

Final Git checks:

```powershell
git diff --check
git status --short
```

## Review expectations

- Every quantitative statement must be traceable to a checked JSON field or a
  clearly documented calculation.
- Charts must state their unit and source; panels with different units must not
  share a misleading scale.
- Local Markdown links must resolve, notebook code cells must have no error
  outputs, JSON must parse, and all ten required PNG files must be present.
- Clearly separate structural validation from domain-expert factual validation.
  The current analysis verifies structure and calculations; it does not claim a
  full subject-matter review of every answer.
