# Turkish Hugging Face Datasets: Quality and Capability Analysis

This public repository contains quality profiles and model-capability mappings
for Turkish or Turkish-focused Hugging Face datasets contributed by course
participants. The current verified scope contains **45 datasets and 87,831
rows**: 87,228 conversation rows, 500 product-table rows, and 103 catalog rows.

The collection is assessed for Identity, Tool Calling, Conversation,
Instruction Following, Structured Output, Math, and Coding. The assessment
describes task fitness, strengths, limitations, and preparation needs; it does
not assign scores or rank positions.

Two further datasets are in scope but could not be analyzed. They are recorded
with live HTTP evidence rather than dropped — see
[Datasets that could not be analyzed](#datasets-that-could-not-be-analyzed).

## Reports and analysis

| Item | Format | Link |
|---|---|---|
| Full technical assessment | Markdown | [Open the main report](reports/dataset-technical-assessment.md) |
| Model-capability mapping | Markdown | [Open the capability report](reports/model-capability-mapping.md) |
| Repository guide | Markdown | [Open the file guide](reports/file-guide.md) |
| Executed quality analysis (Turkish) | HTML | [Open the notebook HTML](notebook/huggingface_dataset_quality_analysis.html) |
| Reproducible analysis (Turkish) | Jupyter Notebook | [Open the notebook source](notebook/huggingface_dataset_quality_analysis.ipynb) |
| Chart definitions and provenance | Markdown | [Open the chart guide](reports/figures/README.md) |
| Row-level capability mapping | CSV | [Open the mapping table](appendix/capability_mapping.csv) |
| Machine-readable capability manifest | JSON | [Open the manifest](appendix/dataset_manifest.json) |
| Per-dataset topics | CSV | [Open the topic profile](appendix/topic_profile.csv) |
| Per-dataset provenance and rights | CSV | [Open the provenance table](appendix/provenance.csv) |
| Recorded access blocks | JSON | [Open the exclusion record](outputs/excluded_datasets.json) |
| Per-contributor feedback (Turkish) | Markdown | [Open the feedback index](feedback/README.md) |
| Evaluation criteria | JSON | [Open the criteria](config/evaluation_criteria.json) |
| Vocabulary similarity | JSON | [Open the topic overlap](outputs/topic_overlap.json) |

## What the analysis found

Each line states a conclusion and links to the evidence behind it. The numbers
themselves live in [the technical assessment](reports/dataset-technical-assessment.md)
and in the JSON under [`outputs/`](outputs/); they are not repeated here.

- **Row count overstates content.** One dataset publishes 1,000 rows built from
  twenty answers. Across the collection, exact matching misses thousands more
  rewordings that only near-duplicate detection catches. Budget from distinct
  content, not from row counts —
  [detail](reports/dataset-technical-assessment.md#row-count-is-not-content-volume-and-exact-matching-understates-repetition).

- **Identity data cannot be merged.** Purpose-built identity datasets from
  different contributors answer the same canonical questions with a different
  name and developer each. Pick one persona before training —
  [detail](reports/dataset-technical-assessment.md#identity-datasets-contradict-one-another).

- **Two capabilities have content but no format.** Nothing in the collection has
  a populated `tool_calls` field, and no conversation runs past a single
  exchange, so Tool Calling and multi-turn behaviour must be authored rather
  than extracted — [mapping](reports/model-capability-mapping.md).

- **Structured Output gained its first direct source**, a dataset whose answers
  are schema-bound JSON. The rest of that dataset ignores the same contract,
  which is the work item —
  [mapping](reports/model-capability-mapping.md#structured-output-one-direct-source-contract-not-enforced).

- **Reuse rights are the largest unresolved risk.** A large share of the
  collection declares no licence, and much of it is scraped from live platforms
  whose terms and whose authors' rights still apply. Recorded as rights facts,
  never as a quality judgement —
  [detail](reports/dataset-technical-assessment.md#provenance-and-reuse-rights).

- **Coverage is narrower than the dataset count implies.** Two independently
  contributed health datasets turn out to cover largely one subject, and several
  datasets have a vocabulary concentrated in a handful of terms —
  [detail](reports/dataset-technical-assessment.md#what-the-collection-is-actually-about).

- **Personal identifiers were read, not counted.** Pattern matches were
  classified individually: some are live customer order references, others are
  log output that only looks like a phone number. Raw counts are not published as
  findings —
  [detail](reports/dataset-technical-assessment.md#personal-identifiers-and-register).

- **Answer quality is not measured, and that is stated rather than implied.**
  Three proxies were built and rejected for flagging good data as defective —
  [why](reports/dataset-technical-assessment.md#answer-quality-is-not-measured-and-here-is-why).

Structural validation is not factual validation. No claim in any dataset has been
checked against an authoritative source by a domain expert.

## Visual evidence

Assessment runs against seven documented dimensions — structural integrity,
content distinctness, topic coverage, provenance and rights, privacy and register,
task fitness, and documentation adequacy. Each records what it measures, the
threshold that marks a preparation need, and what it cannot tell you. Thresholds
live in [`config/evaluation_criteria.json`](config/evaluation_criteria.json) so
the figures, the validator and the prose cannot drift apart. The dimensions are
never combined into a score and datasets are never ranked.

The report uses ten static, reproducible visuals:

1. dataset row counts on a logarithmic scale;
2. duplicate density across three measures, including near-duplicates;
3. median and p95 assistant-response lengths;
4. preparation signals such as `thinking`, time-sensitive matches, and
   string-encoded nulls;
5. missingness across the structured datasets;
6. capability coverage by direct, partial, and conversion-source mapping;
7. preparation needs per dataset as a checklist;
8. shared prompts between the identity datasets;
9. capability reach per contributor;
10. datasets whose vocabulary covers the same ground.

All charts are generated from the checked JSON outputs by
[`scripts/generate_report_charts.py`](scripts/generate_report_charts.py).

## Datasets

| Contributor | Dataset | Rows | Structure |
|---|---|---:|---|
| Ali Furkan Ak | [hf/aliFurkan123/cultural-questions-dataset](https://huggingface.co/datasets/aliFurkan123/cultural-questions-dataset) | 500 | Conversation |
| Ali Furkan Ak | [hf/aliFurkan123/identity](https://huggingface.co/datasets/aliFurkan123/identity) | 30 | Conversation |
| Ayşe Nur Yeşilova | [hf/Aysenur44/namaz-vakti-dua-asistan-tr](https://huggingface.co/datasets/Aysenur44/namaz-vakti-dua-asistan-tr) | 60 | Conversation |
| Ayşe Nur Yeşilova | [hf/Aysenur44/namaz-vakti-identity-tr](https://huggingface.co/datasets/Aysenur44/namaz-vakti-identity-tr) | 4 | Conversation |
| Berk Birkan | [hf/berkbirkan/turkish-x-engagement-quotes](https://huggingface.co/datasets/berkbirkan/turkish-x-engagement-quotes) | 1,000 | Conversation |
| Berk Birkan | [hf/berkbirkan/turkish-x-engagement-replies](https://huggingface.co/datasets/berkbirkan/turkish-x-engagement-replies) | 1,000 | Conversation |
| Berkcan Gümüşışık | [hf/berkcangumusisik/voleykoc-antrenorluk-tr](https://huggingface.co/datasets/berkcangumusisik/voleykoc-antrenorluk-tr) | 166 | Conversation |
| Berkcan Gümüşışık | [hf/berkcangumusisik/voleykoc-identity-tr](https://huggingface.co/datasets/berkcangumusisik/voleykoc-identity-tr) | 182 | Conversation |
| Cihat Yıldız | [hf/cihatyldz/lojistik-soru-cevap](https://huggingface.co/datasets/cihatyldz/lojistik-soru-cevap) | 139 | Conversation |
| Ege Ertekin | [hf/Egertekin/marvel-domain-dataset](https://huggingface.co/datasets/Egertekin/marvel-domain-dataset) | 177 | Conversation |
| Enes Hakan | [hf/enes1863/bilisim-hukuku-domain-dataset](https://huggingface.co/datasets/enes1863/bilisim-hukuku-domain-dataset) | 1,000 | Conversation |
| enesozdemr (account handle) | [hf/enesozdemr/benim_ilk_datasetim](https://huggingface.co/datasets/enesozdemr/benim_ilk_datasetim) | 113 | Conversation |
| Eren Yanic | [hf/Erenyanic/seasoned-advice-dataset](https://huggingface.co/datasets/Erenyanic/seasoned-advice-dataset) | 1,000 | Conversation |
| Erhan Alasar | [hf/erhanalsr/langusta-identity](https://huggingface.co/datasets/erhanalsr/langusta-identity) | 100 | Conversation |
| Erhan Alasar | [hf/erhanalsr/langusta-kpss-reasoning](https://huggingface.co/datasets/erhanalsr/langusta-kpss-reasoning) | 21 | Conversation |
| Filiz Yalçin | [hf/filiz-yalcin/identity-finetune](https://huggingface.co/datasets/filiz-yalcin/identity-finetune) | 1,600 | Conversation |
| Filiz Yalçin | [hf/filiz-yalcin/turkish-figure-skating-qa](https://huggingface.co/datasets/filiz-yalcin/turkish-figure-skating-qa) | 526 | Conversation |
| gmz1234 (account handle) | [hf/gmz1234/stackoverflow_ai](https://huggingface.co/datasets/gmz1234/stackoverflow_ai) | 1,000 | Conversation |
| Görkem Ergüne | [hf/gorkemergune/ayarlicazhocam_finetune](https://huggingface.co/datasets/gorkemergune/ayarlicazhocam_finetune) | 429 | Conversation |
| Gurur Aşer | [hf/gururaser/ithaki-bilimkurgu-klasikleri](https://huggingface.co/datasets/gururaser/ithaki-bilimkurgu-klasikleri) | 103 | Catalog |
| Hatice Nur Çakır | [hf/haticenurcakr/turkish-classic-books-qa](https://huggingface.co/datasets/haticenurcakr/turkish-classic-books-qa) | 220 | Conversation |
| Hilal Kavas | [hf/sadecebirisii/turkish-llm-authority-bypass-safety-sft](https://huggingface.co/datasets/sadecebirisii/turkish-llm-authority-bypass-safety-sft) | 29 | Conversation |
| Mehmet Emre Öz | [hf/nyzmemre/biyoloji-terimleri-turkce-sa](https://huggingface.co/datasets/nyzmemre/biyoloji-terimleri-turkce-sa) | 1,093 | Conversation |
| Melda Kahraman | [hf/meldakahramann/animasyon-domain-dataset](https://huggingface.co/datasets/meldakahramann/animasyon-domain-dataset) | 1,020 | Conversation |
| Mert Ali Alkan | [hf/Mer1Alii/TR-ECommerce-CustomerSupport-Instructions](https://huggingface.co/datasets/Mer1Alii/TR-ECommerce-CustomerSupport-Instructions) | 186 | Conversation |
| Muhammed Bakır Kurt | [hf/Endezyar/siyer_datasets](https://huggingface.co/datasets/Endezyar/siyer_datasets) | 509 | Conversation |
| Muhammet Yusuf Kaydın | [hf/yoitsmeyusuf/felsefe_finetune](https://huggingface.co/datasets/yoitsmeyusuf/felsefe_finetune) | 529 | Conversation |
| Mustafa Özdemir | [hf/namruni/meb-ogretmen-soru-cevap](https://huggingface.co/datasets/namruni/meb-ogretmen-soru-cevap) | 450 | Conversation |
| Nur Sima Akgül | [hf/nursimakgul/meb-soru-uretme](https://huggingface.co/datasets/nursimakgul/meb-soru-uretme) | 20,874 | Conversation |
| Salih Dede | [hf/SalihHub/trendyol-marangoz-urun-asistan-qa](https://huggingface.co/datasets/SalihHub/trendyol-marangoz-urun-asistan-qa) | 1,211 | Conversation |
| Seda Nur Yazıcı | [hf/sedayzc/trendyol-electronics-products-features-and-comments](https://huggingface.co/datasets/sedayzc/trendyol-electronics-products-features-and-comments) | 500 | Product table |
| Seda Nur Yazıcı | [hf/sedayzc/turkish-electronics-product-comparison-recommendation](https://huggingface.co/datasets/sedayzc/turkish-electronics-product-comparison-recommendation) | 11,858 | Conversation |
| Semih Silistre | [hf/ssilistre/carnegie-dost-kazanma-tr](https://huggingface.co/datasets/ssilistre/carnegie-dost-kazanma-tr) | 1,001 | Conversation |
| Semih Silistre | [hf/ssilistre/semih-silistre-ai-identity](https://huggingface.co/datasets/ssilistre/semih-silistre-ai-identity) | 382 | Conversation |
| Senem Deniz | [hf/senemde/saglik-qa-tr](https://huggingface.co/datasets/senemde/saglik-qa-tr) | 553 | Conversation |
| Serhat Kılıç | [hf/sk75/sahin_identity](https://huggingface.co/datasets/sk75/sahin_identity) | 77 | Conversation |
| Seyit Ali Yorğun | [hf/seali/turkce-saglik-qa](https://huggingface.co/datasets/seali/turkce-saglik-qa) | 773 | Conversation |
| Şakir Koç | [hf/srhskrkc/odysseia-destani-tr](https://huggingface.co/datasets/srhskrkc/odysseia-destani-tr) | 10 | Conversation |
| Talayhan (account handle) | [hf/Talayhan/skatepal_dataset](https://huggingface.co/datasets/Talayhan/skatepal_dataset) | 299 | Conversation |
| Umay Şamlı | [hf/samliumay/turkish_cyber_security_controls_dataset](https://huggingface.co/datasets/samliumay/turkish_cyber_security_controls_dataset) | 800 | Conversation |
| Umay Şamlı | [hf/samliumay/umay_samli_identification_dataset](https://huggingface.co/datasets/samliumay/umay_samli_identification_dataset) | 219 | Conversation |
| Umut Kıvanç Sipahioglu | [hf/Toivo0/Turkce-istatistik-reasoning](https://huggingface.co/datasets/Toivo0/Turkce-istatistik-reasoning) | 400 | Conversation |
| Uunan (account handle) | [hf/Uunan/turkish-cuisine-qa](https://huggingface.co/datasets/Uunan/turkish-cuisine-qa) | 34,244 | Conversation |
| Yusuf Şimşek | [hf/YusufSimsek/llm-kisisellestirme](https://huggingface.co/datasets/YusufSimsek/llm-kisisellestirme) | 46 | Conversation |
| Yusuf Şimşek | [hf/YusufSimsek/turkce-atasozleri-dataset](https://huggingface.co/datasets/YusufSimsek/turkce-atasozleri-dataset) | 1,398 | Conversation |

Contributor names come from the assignment submission form. Where a submitter
did not supply a verifiable full name, the Hugging Face account handle is
recorded instead and marked as such; an account handle is not a person's name.

## Datasets that could not be analyzed

These datasets are enabled in the registry and are **not** silently skipped.
Every run re-verifies the block and records the live HTTP result in
[`outputs/excluded_datasets.json`](outputs/excluded_datasets.json). Their rows
are excluded from every total in this repository.

| Contributor | Dataset | Status | Evidence |
|---|---|---|---|
| Muhammet Enes Nas | [hf/menesnas/Pharmacy_Identity_Synthetic_QA](https://huggingface.co/datasets/menesnas/Pharmacy_Identity_Synthetic_QA) | Gated, access not granted | Repository metadata reports `gated: "manual"`. Authenticated requests return `403 "Access to dataset … is restricted and you are not in the authorized list"`. The data card is public; only the data files are withheld. |
| Oguz Caliskan | [hf/uzcaliskan/magibu_dataset_drilling](https://huggingface.co/datasets/uzcaliskan/magibu_dataset_drilling) | Not reachable | Anonymous requests return `401`; authenticated requests return `404 "Repository not found"`. A valid credential turning 401 into 404 means the repository is not visible to the auditing account at all, so it is deleted, renamed, or private to a different owner. |

To bring the first dataset into scope, its owner must approve an access request
for the auditing account; the audit then picks it up with no code change. For
the second, the submitter must confirm the correct URL or grant access.

## Repository structure

```text
.
|-- README.md
|-- AGENTS.md
|-- config/
|   |-- datasets.json
|   `-- verified_baseline.json
|-- reports/
|   |-- dataset-technical-assessment.md
|   |-- model-capability-mapping.md
|   |-- file-guide.md
|   `-- figures/
|-- notebook/
|   |-- huggingface_dataset_quality_analysis.ipynb
|   `-- huggingface_dataset_quality_analysis.html
|-- outputs/
|   |-- source_inventory.json
|   |-- data_quality_profiles.json
|   |-- cross_dataset_overlap.json
|   |-- excluded_datasets.json
|   `-- manual_findings.json
|-- appendix/
|   |-- capability_mapping.csv
|   `-- dataset_manifest.json
|-- scripts/
|   |-- download_hf_datasets.py
|   |-- profile_datasets.py
|   |-- build_notebook.py
|   |-- generate_report_charts.py
|   `-- validate_repository.py
`-- requirements.txt
```

The local `data/` directory contains raw snapshots for row-level work and is
intentionally ignored by Git. A public clone contains the reviewed evidence and
reports but must download raw snapshots again before reprofiling.

The reports and README files are in English. The notebook, its generated HTML,
and reviewed JSON evidence retain their original Turkish analysis text.

## Reproduce or extend the analysis

Run from the repository root with Python 3.12:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

Dataset IDs and contributor names are maintained in
[`config/datasets.json`](config/datasets.json). After adding new entries, run:

```powershell
.\.venv\Scripts\python scripts\download_hf_datasets.py
.\.venv\Scripts\python scripts\profile_datasets.py
.\.venv\Scripts\python scripts\build_notebook.py
.\.venv\Scripts\python -m jupyter nbconvert --to html --output-dir notebook notebook\huggingface_dataset_quality_analysis.ipynb
.\.venv\Scripts\python scripts\generate_report_charts.py
.\.venv\Scripts\python scripts\validate_repository.py
```

The downloader pins every snapshot to a repository revision. It prefers the
repository's own data file when that file's row count exactly matches the size
the Dataset Viewer publishes for the split, and pages the Viewer otherwise; both
paths produce the same rows and a completeness receipt. Anonymous access is rate
limited, so setting `HF_TOKEN` in the environment makes runs faster and reaches
gated repositories the account has been granted. Never commit a token.

The profiler stops on any incomplete snapshot that is not a declared access
block. Before publishing an expanded scope, review the computed evidence, update
qualitative findings and capability mappings, then update
[`config/verified_baseline.json`](config/verified_baseline.json).

See [`AGENTS.md`](AGENTS.md) for the full maintenance and validation workflow.
