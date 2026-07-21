# Turkish Hugging Face Datasets: Quality and Capability Analysis

This public repository contains quality profiles and model-capability mappings
for nine Turkish or Turkish-focused Hugging Face datasets. The fixed analysis
scope contains **3,119 rows**: 3,016 conversation rows and 103 catalog rows.

The collection is evaluated for Identity, Tool Calling, Conversation,
Instruction Following, Structured Output, Math, and Coding.

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

## Verified findings

- All nine local raw snapshots were reprofiled on 21 July 2026. The regenerated
  profile and overlap JSON files were byte-identical to the existing outputs.
- An independent audit ran 68 checks against the raw rows; all 68 passed.
- Conversation rows contain no empty message content, invalid roles, or exact
  duplicate rows.
- No labeled tool-calling chain or true multi-turn conversation is present.
- 1,136 assistant messages contain a separate `thinking` field.
- The Şahin identity dataset contains 462 string-encoded null fields.
- Normalized duplicate-copy concentration is highest in Marvel and philosophy
  prompts, biology answers, and Şahin identity answers.
- The MEB dataset contains 297 time-sensitive regex matches. This is a match
  count, not a count of unique rows.

Normalized duplicate rate means the number of extra copies after the first item
in each normalized text family divided by the dataset row count. It is not a
measure of full semantic similarity.

## Visual evidence

The report uses six static, reproducible visuals:

1. dataset row counts;
2. normalized prompt and answer duplicate-copy rates;
3. median and p95 assistant-response lengths;
4. preparation signals such as `thinking`, time-sensitive matches, and
   string-encoded nulls;
5. missingness in the structured catalog;
6. capability coverage by direct, partial, and conversion-source mapping.

All charts are generated from the checked JSON outputs by
[`scripts/generate_report_charts.py`](scripts/generate_report_charts.py).

## Datasets

| Contributor | Dataset | Rows |
|---|---|---:|
| Ali Furkan Ak | [aliFurkan123/cultural-questions-dataset](https://huggingface.co/datasets/aliFurkan123/cultural-questions-dataset) | 500 |
| Ayşe Nur Yeşilova | [Aysenur44/namaz-vakti-identity-tr](https://huggingface.co/datasets/Aysenur44/namaz-vakti-identity-tr) | 4 |
| Ege Ertekin | [Egertekin/marvel-domain-dataset](https://huggingface.co/datasets/Egertekin/marvel-domain-dataset) | 177 |
| Gurur Aşer | [gururaser/ithaki-bilimkurgu-klasikleri](https://huggingface.co/datasets/gururaser/ithaki-bilimkurgu-klasikleri) | 103 |
| Mehmet Emre Öz | [nyzmemre/biyoloji-terimleri-turkce-sa](https://huggingface.co/datasets/nyzmemre/biyoloji-terimleri-turkce-sa) | 1,093 |
| Mert Ali Alkan | [Mer1Alii/TR-ECommerce-CustomerSupport-Instructions](https://huggingface.co/datasets/Mer1Alii/TR-ECommerce-CustomerSupport-Instructions) | 186 |
| Muhammet Yusuf Kaydın | [yoitsmeyusuf/felsefe_finetune](https://huggingface.co/datasets/yoitsmeyusuf/felsefe_finetune) | 529 |
| Mustafa Özdemir | [namruni/meb-ogretmen-soru-cevap](https://huggingface.co/datasets/namruni/meb-ogretmen-soru-cevap) | 450 |
| Serhat Kılıç | [sk75/sahin_identity](https://huggingface.co/datasets/sk75/sahin_identity) | 77 |

## Repository structure

```text
.
├── README.md
├── reports/
│   ├── dataset-technical-assessment.md
│   ├── model-capability-mapping.md
│   ├── file-guide.md
│   └── figures/
│       ├── README.md
│       ├── capability-coverage.png
│       ├── catalog-missing-fields.png
│       ├── data-preparation-signals.png
│       ├── dataset-row-counts.png
│       ├── duplicate-rates.png
│       └── response-lengths.png
├── notebook/
│   ├── huggingface_dataset_quality_analysis.ipynb
│   └── huggingface_dataset_quality_analysis.html
├── outputs/
│   ├── cross_dataset_overlap.json
│   ├── data_quality_profiles.json
│   ├── manual_findings.json
│   └── source_inventory.json
├── appendix/
│   ├── capability_mapping.csv
│   └── dataset_manifest.json
├── scripts/
│   └── generate_report_charts.py
└── requirements.txt
```

The reports and this README are in English. The notebook, its generated HTML output,
and the JSON files under `outputs/` are the original Turkish analysis artifacts and are
kept in their source language.

## Reproduce the notebook and charts

Run from the repository root with Python 3.12:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m jupyter nbconvert --execute --to notebook --inplace notebook\huggingface_dataset_quality_analysis.ipynb
.\.venv\Scripts\python -m jupyter nbconvert --to html --output-dir notebook notebook\huggingface_dataset_quality_analysis.ipynb
.\.venv\Scripts\python scripts\generate_report_charts.py
```

The notebook reads the validated JSON files under `outputs/`. Raw datasets are
not redistributed in this public repository; use the official Hugging Face links
above for source access.
