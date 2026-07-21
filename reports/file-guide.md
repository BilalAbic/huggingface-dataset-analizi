# File Guide

This document explains what each file in the GitHub delivery repository does and how
the files relate to one another. The repository contains only reports, analysis
outputs, and a re-runnable notebook; the raw Hugging Face data files are not republished.

## Where to start

1. For overall results, figures, and per-dataset assessments, open the [main technical report](dataset-technical-assessment.md).
2. For the details of the seven model capability areas, read the [mapping report](model-capability-mapping.md).
3. For the calculation steps and tables, use the [notebook source](../notebook/huggingface_dataset_quality_analysis.ipynb) or the [HTML output](../notebook/huggingface_dataset_quality_analysis.html).
4. To use the numerical results programmatically, look at the [`outputs/`](../outputs/) and [`appendix/`](../appendix/) directories.

## What each file does

| Location | Contents |
|---|---|
| `reports/dataset-technical-assessment.md` | Nine contributors, six figures, per-dataset strengths and weaknesses, and the technical implementation plan |
| `reports/model-capability-mapping.md` | Details for Identity, Tool Calling, Conversation, Instruction Following, Structured Output, Math, and Coding |
| `reports/file-guide.md` | This document: the map of the repository |
| `reports/figures/` | Six GitHub-friendly PNG figures generated from the JSON analysis outputs, plus the figure guide |
| `notebook/huggingface_dataset_quality_analysis.ipynb` | The executed analysis source with cell outputs |
| `notebook/huggingface_dataset_quality_analysis.html` | A standalone notebook view that opens in a browser |
| `outputs/source_inventory.json` | Inventory of dataset sources and fixed revision identifiers (commits) |
| `outputs/data_quality_profiles.json` | Schema, row, emptiness, role, duplicate, and content profiles |
| `outputs/manual_findings.json` | Per-dataset evidence, risk, and improvement notes |
| `outputs/cross_dataset_overlap.json` | Shared prompt and template findings across datasets |
| `appendix/capability_mapping.csv` | Row-based mapping of the seven capability areas |
| `appendix/dataset_manifest.json` | The detailed, machine-readable JSON manifest of the mapping |
| `scripts/generate_report_charts.py` | The script that regenerates the six report figures from the JSON evidence |

## Language

The reports in `reports/` and the repository [`README.md`](../README.md) are written in
English. The notebook, its generated HTML output, and the JSON files under `outputs/`
are in Turkish; they are the original analysis artifacts and are kept in their source
language so that the notebook and its published HTML stay consistent with each other.

## Reproducibility

When the notebook is run from the repository root, it reads the `outputs/` files
through relative paths. The setup commands are in the main [`README.md`](../README.md).
The HTML was generated from the results in the executed notebook; the source notebook
contains no error output.

To regenerate the report figures, run `python scripts/generate_report_charts.py` from
the repository root. Reading notes for the figures are in the
[figure guide](figures/README.md).
