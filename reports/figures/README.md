# Figure Guide and Provenance

The nine figures in this directory are generated from the fixed JSON evidence in
the repository. They describe dataset composition, content patterns, preparation
needs, and how the collection relates to its contributors.

| Figure | Analytical question | Form | Evidence | Reading note |
|---|---|---|---|---|
| [`dataset-row-counts.png`](dataset-row-counts.png) | How is the row volume distributed across the collection? | Horizontal bar chart, logarithmic scale | `outputs/data_quality_profiles.json` | The axis is logarithmic because dataset sizes span four orders of magnitude; a bar twice as long is not twice as large. Exact counts are printed beside every bar. Row volume does not imply quality or task fitness. |
| [`duplicate-rates.png`](duplicate-rates.png) | How much of each response dataset repeats itself? | Triple dot plot | `outputs/data_quality_profiles.json` | Three measures per row, labelled `prompt% / answer% / near-duplicate%`. The first two count extra copies after the first occurrence once case and punctuation are normalized. The third counts answers sharing at least **85% of their tokens** with an earlier answer, so it catches rewordings the other two score as unique. The near-duplicate comparison is exact, not hashed or sampled. |
| [`preparation-needs.png`](preparation-needs.png) | What must be fixed in each dataset before use? | Presence matrix | `outputs/data_quality_profiles.json` | A checklist, **not a score**. Rows are ordered by dataset identifier so no ranking is implied, and a filled cell only means the dataset crosses that threshold. Thresholds are printed in the column headers. |
| [`identity-prompt-conflicts.png`](identity-prompt-conflicts.png) | Do the identity datasets agree with one another? | Chord diagram | `outputs/cross_dataset_overlap.json` | Nodes are the nine direct Identity datasets; edge width is the number of shared user prompts. The counts here cover identity-to-identity pairs only and are therefore smaller than the collection-wide overlap totals. Zero shared answers with many shared prompts means the same question is answered differently in each dataset. |
| [`contributor-coverage.png`](contributor-coverage.png) | Which capabilities does each contributor's work reach? | Count matrix | `appendix/dataset_manifest.json` | Cells count a contributor's datasets matched at direct or partial level. Conversion sources are excluded because they are not training data yet, so a contributor with only a conversion source does not appear. Counts are coverage, not quality. |
| [`response-lengths.png`](response-lengths.png) | How different are typical and long-tail assistant responses? | Median-to-p95 interval plot | `outputs/data_quality_profiles.json` | Word count is a formatting and training-budget signal, not a quality measure. Each row is labelled `median / p95`. |
| [`data-preparation-signals.png`](data-preparation-signals.png) | Where are explicit reasoning fields, time-sensitive language, or type errors concentrated? | Three-panel bar chart | `outputs/data_quality_profiles.json` | Panels use different units and independent scales, and panel heights are allocated per panel, so bar lengths must not be compared between panels. Panels switch to a logarithmic axis when their values span more than roughly fifty times. Time-sensitive values are regex matches, not unique row counts. |
| [`catalog-missing-fields.png`](catalog-missing-fields.png) | Which fields of the structured datasets require missing-value handling? | Grouped horizontal percentage bars, one panel per structured dataset | `outputs/data_quality_profiles.json` | Covers every catalog or tabular dataset in scope, not only the first one. Only fields with at least one missing value are shown, up to the eight emptiest per dataset. Source column names are kept verbatim. |
| [`capability-coverage.png`](capability-coverage.png) | How close are the datasets to the seven target capability formats? | Count matrix | `appendix/dataset_manifest.json` | One dataset may support more than one capability; counts are not additive portfolio totals. A conversion source is not ready-made training data. |

## Labels

Every dataset is labelled with its full `hf/owner/name` Hugging Face identifier,
never a shortened nickname, so a bar maps to exactly one repository with no
lookup table. The same form is used in the
[README dataset table](../../README.md#datasets) and in the Markdown reports.

Because identifiers run up to about 64 characters, these charts are wider than
usual and reserve a large left margin for the category axis. Figure heights are
computed from the number of rows each chart draws, so adding or removing datasets
does not compress the labels.

## Scope

The figures show datasets that were actually analyzed. Datasets that could not
be downloaded are not silently omitted: they are listed with their access
evidence in [`outputs/excluded_datasets.json`](../../outputs/excluded_datasets.json)
and in the main report.

## Rebuild

From the repository root:

```bash
python -m pip install -r requirements.txt
python scripts/generate_report_charts.py
```

The script uses Matplotlib and writes all nine PNG files deterministically from
the checked-in evidence. Labels come straight from the dataset identifier, so a
newly added dataset needs no chart code change.
