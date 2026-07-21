# Figure Guide and Provenance

The six figures in this directory are generated from the fixed JSON evidence in
the repository. They describe dataset composition, content patterns, and
preparation needs.

| Figure | Analytical question | Form | Evidence | Reading note |
|---|---|---|---|---|
| [`dataset-row-counts.png`](dataset-row-counts.png) | How is the 3,119-row portfolio distributed? | Horizontal bar chart | `outputs/data_quality_profiles.json` | Row volume does not imply quality or task fitness. |
| [`duplicate-rates.png`](duplicate-rates.png) | Which conversation datasets contain repeated prompt or answer families? | Paired dot plot | `outputs/data_quality_profiles.json` | The rate is extra copies after the first occurrence divided by all rows, after case and punctuation normalization. |
| [`response-lengths.png`](response-lengths.png) | How different are typical and long-tail assistant responses? | Median-to-p95 interval plot | `outputs/data_quality_profiles.json` | Word count is a formatting and training-budget signal, not a quality measure. |
| [`data-preparation-signals.png`](data-preparation-signals.png) | Where are explicit reasoning fields, time-sensitive language, or type errors concentrated? | Three-panel bar chart | `outputs/data_quality_profiles.json` | Panels use different units. Time-sensitive values are regex matches, not unique row counts. |
| [`catalog-missing-fields.png`](catalog-missing-fields.png) | Which Ithaki catalog fields require missing-value handling? | Horizontal percentage bars | `outputs/data_quality_profiles.json` | Only fields with at least one missing value are shown. |
| [`capability-coverage.png`](capability-coverage.png) | How close are the datasets to the seven target capability formats? | Count matrix | `appendix/dataset_manifest.json` | One dataset may support more than one capability; counts are not additive portfolio totals. |

## Rebuild

From the repository root:

```bash
python -m pip install -r requirements.txt
python scripts/generate_report_charts.py
```

The script uses Matplotlib and writes all six PNG files deterministically from the
checked-in evidence. Chart labels are in English; the original Turkish field names of
the Ithaki catalog (`kapak_tipi`, `orijinal_adi`, `cevirmen`, `yayin_tarihi`) are shown
alongside their English labels so the figure can be traced back to the source columns.
