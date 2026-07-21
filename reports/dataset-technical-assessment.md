# Hugging Face Datasets: Technical Assessment

## Technical summary

- **3,119 rows across nine datasets were reviewed.** 3,016 of them sit in eight
  conversation datasets and 103 in the 17-field Ithaki book catalog.
- **Structural integrity is generally good, but semantic diversity is uneven.** The
  conversation sets contain no empty content and no invalid roles, yet Marvel and
  philosophy prompts, along with biology and Şahin identity answers, show marked
  normalized duplication.
- **The current collection is usable for Conversation and domain question-answer
  training.** By contrast, true multi-turn conversation, labeled Tool Calling,
  verifiable Structured Output, general Math, and Coding examples are not ready.
- **Data preparation must be handled per task.** The `thinking` (reasoning) content
  has to be separated from the final answer, duplicate families reduced, `"null"`
  values stored as text corrected, and time-sensitive answers tied to current sources.
- **The calculations were re-verified.** Regenerating profiles from the raw rows
  produced identical JSON results, and all 68 independent structural and numerical
  checks passed.

**Scope date:** 20–21 July 2026  
**Unit of analysis:** All rows of the fixed dataset snapshots published on Hugging Face  
**Assessment approach:** Task fit, data structure, content quality, and preparation
requirements

## Table of contents

- [Terms and usage](#terms-and-usage)
- [Portfolio structure](#portfolio-structure)
- [Core quality findings](#core-quality-findings)
- [Dataset inventory](#dataset-inventory)
- [Dataset-by-dataset assessment](#dataset-by-dataset-assessment)
- [Match against model capability areas](#match-against-model-capability-areas)
- [Proposed target data schemas](#proposed-target-data-schemas)
- [Technical implementation plan](#technical-implementation-plan)
- [Limitations and verification scope](#limitations-and-verification-scope)
- [Evidence and reproducibility](#evidence-and-reproducibility)
- [Questions for further work](#questions-for-further-work)

## Terms and usage

| Report term | Meaning in this report |
|---|---|
| Exact duplicate | Text that is identical under direct comparison |
| Normalized duplicate | The extra copies after the first occurrence among texts that remain identical once formatting differences such as case and punctuation are removed; the rate divides those copies by the total row count |
| Supervised Fine-Tuning (SFT) | Model adaptation using prompt and expected-answer pairs |
| Prompt–target pair | Keeping a user task together with its verifiable expected output |
| Persona | Information defining the model name, developer, role, capabilities, and boundary behavior |

Field names in the data schemas such as `messages`, `tool_calls`, `prompt`, `target`,
and `thinking` are kept untranslated for technical compatibility.

## Portfolio structure

Data volume is concentrated in a few conversation collections. The biology,
philosophy, general knowledge, and MEB datasets together hold 2,572 rows, which is
82.46% of the whole collection. That share reflects volume only; it is not an
indicator of content diversity or task fitness.

![Row counts of the nine datasets](figures/dataset-row-counts.png)

The chart shows which datasets hold the largest content pools for conversation
training. The identity sets being small is expected; those sets target the model
persona and ownership answers rather than general domain knowledge.

## Core quality findings

### Structural checks are clean, but duplicate density shifts task risk

Message roles and content fields are valid across the eight conversation datasets.
No exact row duplication was observed. However, once punctuation and case
differences are ignored, some prompt or answer families turn out to repeat very
frequently.

![Normalized duplicate rates in the conversation datasets](figures/duplicate-rates.png)

**Interpretation:** In the philosophy and Marvel sets, the same prompt family maps to
many different answers. In the Şahin identity dataset, answer diversity is low. In
the biology set, the same definition recurring under different questions can give
certain answer patterns more weight than warranted during training. Values that
appear as zero do not mean the content is factually correct; they mean no duplication
was found under this normalization rule.

![Median and p95 word counts of assistant responses](figures/response-lengths.png)

Response length varies markedly by content type. The philosophy answers have a long
tail, while identity and term explanations are shorter. This picture is not a quality
measure; it is a data preparation signal for context budget, example weighting, and
target answer format.

### Reasoning fields, tool calls, and type integrity require separate data work

| Check | Finding | Technical impact |
|---|---:|---|
| Assistant messages containing `thinking` (reasoning) | 1,136 | The final answer target must be produced separately; private reasoning fields should not be published directly |
| Populated `tool_calls` fields | 0 | Function schemas, arguments, and tool results must be authored separately for Tool Calling training |
| True multi-turn records | 0 | Context tracking and follow-up behavior cannot be measured with the current collection |
| `"null"` stored as text | 462 | Schema validation and type normalization are required |
| Prompt–target JSON/table examples | 0 | Verifiable target records must be produced for Structured Output |

![Thinking, time-sensitive phrasing, and null type signals](figures/data-preparation-signals.png)

The three panels use different units and show only values greater than zero. The
`thinking` coverage is a percentage of messages; the time-sensitive values are regex
match counts, not unique row counts. The `null`-as-text value is a field count.

### Capability coverage is not uniform

![Direct, partial, and conversion-source matches across capability areas](figures/capability-coverage.png)

There are six domain datasets that can be used directly for Conversation. The
Instruction Following contribution is domain question-answer behavior rather than
general instruction diversity. Although content sources exist for Tool Calling,
Structured Output, and Math, the target example schemas do not yet exist. For Coding
there is no suitable record in the current collection.

## Dataset inventory

| Contributor | Dataset | Rows | Structure | Primary use |
|---|---|---:|---|---|
| Ali Furkan Ak | [cultural-questions-dataset](https://huggingface.co/datasets/aliFurkan123/cultural-questions-dataset) | 500 | Two-message conversation | Turkish general knowledge and explanatory answers |
| Ayşe Nur Yeşilova | [namaz-vakti-identity-tr](https://huggingface.co/datasets/Aysenur44/namaz-vakti-identity-tr) | 4 | `system–user–assistant` | Model identity and developer information |
| Ege Ertekin | [marvel-domain-dataset](https://huggingface.co/datasets/Egertekin/marvel-domain-dataset) | 177 | Two-message conversation | Marvel domain question-answering |
| Gurur Aşer | [ithaki-bilimkurgu-klasikleri](https://huggingface.co/datasets/gururaser/ithaki-bilimkurgu-klasikleri) | 103 | 17-field catalog | Book catalog and controlled conversion |
| Mehmet Emre Öz | [biyoloji-terimleri-turkce-sa](https://huggingface.co/datasets/nyzmemre/biyoloji-terimleri-turkce-sa) | 1,093 | Two-message conversation | Turkish biology term explanations |
| Mert Ali Alkan | [TR-ECommerce-CustomerSupport-Instructions](https://huggingface.co/datasets/Mer1Alii/TR-ECommerce-CustomerSupport-Instructions) | 186 | Two-message conversation | E-commerce customer support |
| Muhammet Yusuf Kaydın | [felsefe_finetune](https://huggingface.co/datasets/yoitsmeyusuf/felsefe_finetune) | 529 | Two-message conversation | Subjective philosophical discourse |
| Mustafa Özdemir | [meb-ogretmen-soru-cevap](https://huggingface.co/datasets/namruni/meb-ogretmen-soru-cevap) | 450 | Two-message conversation | Teacher regulations and practice questions |
| Serhat Kılıç | [sahin_identity](https://huggingface.co/datasets/sk75/sahin_identity) | 77 | Two-message conversation | Turkish/English model identity |

## Dataset-by-dataset assessment

### Ali Furkan Ak — a clean core for general knowledge, source verification needed

**What does it do?** Provides Turkish general knowledge, trivia, and explanatory
single-turn dialogues.

**Strengths**

- All 500 rows have populated user and assistant content.
- No exact or normalized prompt/answer duplication was detected.
- The standard conversation schema and manageable response lengths make conversion to
  supervised fine-tuning (SFT) format straightforward.

**Weaknesses and risks**

- The content is synthetic; factual answers carry no row-level source or verification field.
- All 500 assistant messages contain a separate `thinking` field.
- Although the dataset name suggests cultural questions, the content covers broader
  general knowledge.

**Preparation decision:** Usable for Conversation and narrow Instruction Following
tasks once factual verification, topic labels, and a target version carrying only the
final answer have been produced.

### Ayşe Nur Yeşilova — suitable as an identity seed, provides no domain competence

**What does it do?** Defines the NamazAsistan-v1 model name, developer, and core
capability identity through four system–user–assistant records.

**Strengths**

- Message order and content are valid across all four records.
- The standard `messages` field can be adapted directly to persona training.

**Weaknesses and risks**

- Four rows do not teach prayer-time, supplication, or worship domain competence.
- Safety principles, scope boundaries, and detailed refusal behaviors are absent.
- The four user prompts overlap with the Şahin identity dataset.

**Preparation decision:** Should be kept as a low-weight core identity seed rather
than general training data; safety and boundary examples must be supplied by separate
data.

### Ege Ertekin — rich domain content, markedly low prompt diversity

**What does it do?** Answers Turkish questions about the Marvel universe, character
history, and comic book history at length.

**Strengths**

- All 177 rows have a valid user–assistant sequence.
- The long answers are rich in domain terminology and character history.
- The data card explains the Wikipedia scraping and manual expansion approach.

**Weaknesses and risks**

- 134 user prompts are normalized duplicates: **75.71%**.
- A single Spider-Man question recurs 83 times.
- Source page URLs, revision identifiers, and a row-level citation chain are absent.
- The columns described by the data card do not match the actual `messages` schema.

**Preparation decision:** Should not enter the training pool before specific question
generation, duplicate clustering, and source linking are added.

### Gurur Aşer — a strong catalog source for structured conversion

**What does it do?** Presents the Ithaki Science Fiction Classics series as 103
records with 17 catalog fields.

**Strengths**

- There is no exact duplication and no ISBN/URL or book–author key duplication.
- ISBN-13 and URL checks pass.
- Price and discount fields are internally consistent.
- The structured fields suit generating JSON, table, search, and filtering tasks.

**Weaknesses and risks**

- The translator, cover type, original title, and publication date fields have gaps.
- Prices are a snapshot; there is no row-level `collected_at` field.
- The accuracy of the generated summaries must be separately verified against
  row-level sources.

![Missing-field rates in the Ithaki catalog](figures/catalog-missing-fields.png)

The cover type field is empty in 96/103 records, original title in 65/103, translator
in 62/103, and publication date in 12/103. These gaps should be managed with real
`null` values, per-field requirement rules, and explicit "unknown" behavior at task
time rather than by deleting records.

**Preparation decision:** Usable as a conversion source for Structured Output, Tool
Calling for book search, and narrow price/discount Math tasks; in its current form it
is not a prompt–target training set.

### Mehmet Emre Öz — broad coverage, answer-family duplication must be reduced

**What does it do?** Provides short scientific explanations for Turkish biology terms
across 1,093 rows.

**Strengths**

- Offers a broad topic and term volume with 1,093 rows.
- Role and content fields are valid; there is no empty content or exact row duplication.
- The short term-explanation format is clear and easy to convert.

**Weaknesses and risks**

- 236 assistant answers are normalized duplicates: **21.59%**.
- Source book, edition, and generation method fields are absent.
- The same definition repeating under different prompts can overweight certain answer
  patterns.

**Preparation decision:** Usable as Conversation and domain-focused Instruction
Following data after term identifiers, a source field, and answer-family-based
duplicate reduction are added.

### Mert Ali Alkan — good customer support behavior, policy content must be verified

**What does it do?** Produces empathy, explanation, and next-step suggestions in
Turkish e-commerce customer support conversations.

**Strengths**

- All 186 rows are structurally valid, populated, and unique.
- The generation method is documented in detail.
- The customer support tone and problem-solving flow are close to production use.

**Weaknesses and risks**

- All assistant messages contain a `thinking` field.
- Synthetic policy, legal, warranty, and contact information can be learned as if it
  were real company behavior.
- One realistic-looking email address should be converted to a placeholder.

**Preparation decision:** Policy texts must be verified, contact details anonymized,
and — if Tool Calling is the goal — order/support function schemas must be authored
separately.

### Muhammet Yusuf Kaydın — valuable for subjective discourse, unsuitable as factual data

**What does it do?** Contains Turkish philosophy discussions and subjective opinions
sourced from Ekşi Sözlük and Reddit.

**Strengths**

- Across 529 rows there is no empty content, invalid role, or exact row duplication.
- Long answers present different perspectives on the same topic.
- Usable in research on community language and subjective opinion generation.

**Weaknesses and risks**

- 405 user prompts are normalized duplicates: **76.56%**.
- Contradictory opinions can be learned as if they were the single correct answer.
- Row-level source URLs and a content-removal mechanism are absent.
- The data card reports 527 records while the downloaded fixed snapshot contains 529.

**Preparation decision:** Should be used only for opinion-diversity and subjective
dialogue tasks, preserving the source type and opinion label.

### Mustafa Özdemir — strong real-world context, a currency layer is mandatory

**What does it do?** Provides long Turkish answers to teacher appointment, personnel,
leave, and regulation questions.

**Strengths**

- All 450 rows are structurally valid and unique.
- The generation process used forum questions, 23 official sources, a model judge, and
  human sample review.
- The questions are close to real usage context and the answers to an actionable
  explanation format.

**Weaknesses and risks**

- According to the data card, only 41% of the answers carry an official source citation.
- 297 regex matches were found for time-sensitive patterns; this number should not be
  read as a count of unique rows.
- All assistant messages contain a `thinking` field.
- Answers with administrative impact should not be presented as definitive without
  retrieving a current source.

**Preparation decision:** Can serve as a Conversation/Instruction Following source
with current official source retrieval, validity dates, mandatory citation, and
uncertainty language.

### Serhat Kılıç — bilingual identity diversity, type and duplicate cleanup needed

**What does it do?** Answers identity, ownership, developer, and capability questions
in Turkish and English.

**Strengths**

- 77 rows provide identity variations in two languages.
- Directly targets identity and developer questions.

**Weaknesses and risks**

- 50 assistant answers are normalized duplicates: **64.94%**.
- The `images`, `thinking`, and `tool_calls` fields in 154 messages carry the string
  `"null"` instead of a real `null`; there are 462 type errors in total.
- Safety, boundary, and consistent refusal behavior are limited.
- There are four user prompts in common with the NamazAsistan identity dataset.

**Preparation decision:** Usable as a low-weight, bilingual Identity seed after type
correction and duplicate reduction.

## Match against model capability areas

| Area | Current match | Usable sources | What must be prepared |
|---|---|---|---|
| Identity | 2 direct | NamazAsistan identity, Şahin identity | Safety, boundary, consistent refusal, and out-of-scope question examples |
| Tool Calling | 3 conversion sources | Ithaki, e-commerce, MEB | Tool schema, arguments, result, error, and final answer chain |
| Conversation | 6 direct, 2 partial | General knowledge, Marvel, e-commerce, MEB, biology, philosophy; the identity sets provide persona support | Multi-turn follow-up, correction, topic switching, and long context |
| Instruction Following | 6 partial | E-commerce, MEB, general knowledge, biology, Marvel, philosophy | Summarization, rewriting, classification, format constraints, and multi-step tasks |
| Structured Output | 1 conversion source | Ithaki catalog | JSON/table targets verifiable against the prompt |
| Math | 1 narrow conversion source | Ithaki price and discount fields | Solution steps, unit tests, and general math diversity |
| Coding | No match | — | Code generation, testing, debugging, explanation, refactoring, and algorithm data |

For detailed per-area design and record contracts, see the
[Model Capability Mapping](model-capability-mapping.md).

## Proposed target data schemas

| Area | Proposed record format | Required fields | Core validation |
|---|---|---|---|
| Identity | `messages` + persona metadata | `system`, `user`, `assistant`, `persona_id`, `language`, `policy_scope` | Identity consistency, boundary, and refusal behavior tests |
| Tool Calling | Tool definition + call + result + answer | `tools`, `tool_name`, `arguments`, `tool_result`, `assistant_final` | JSON Schema, tool name, argument type, and result dependency |
| Conversation | Multi-turn message sequence | `conversation_id`, `turn_index`, `role`, `content`, `topic` | Role order, context reference, and turn integrity |
| Instruction Following | Prompt–constraint–target triple | `instruction`, `constraints`, `input`, `target` | Constraint satisfaction and task type checks |
| Structured Output | Prompt + schema + output | `prompt`, `schema`, `target_json` | JSON parsing, schema conformance, and field type checks |
| Math | Problem + solution + answer | `problem`, `solution_steps`, `final_answer`, `unit` | Recomputation and unit consistency |
| Coding | Task + context + code + tests | `task`, `language`, `context`, `solution`, `tests` | Compile/run, test, and safe code checks |

## Technical implementation plan

1. **Establish a shared canonical schema.** Preserve the source dataset, revision
   identifier (commit), language, task type, and original row identifier in every
   record.
2. **Normalize message types.** Convert `"null"` strings to real `null` values;
   validate role order and content types with JSON Schema.
3. **Cluster duplicate families.** Alongside exact duplicate checks, use normalized
   prompt and answer keys; balance training weight by cluster size.
4. **Separate `thinking` from the final answer.** Keep only the user-facing final
   answer in the supervised fine-tuning (SFT) target that will be published.
5. **Generate conversion tasks with explicit schemas.** When deriving Tool Calling or
   Structured Output from the Ithaki, e-commerce, and MEB sources, test every target
   with a deterministic validator.
6. **Tie time-sensitive answers to a source layer.** Make validity dates and an
   official source field mandatory for MEB and policy-bearing e-commerce examples.
7. **Write per-area acceptance tests.** JSON Schema, tool arguments, math
   recomputation, code tests, and multi-turn context checks should be separate test
   suites.

## Limitations and verification scope

- Normalized duplicate analysis ignores punctuation and case differences; it is not a
  full semantic similarity model.
- The personal data scan is regex-based; it cannot fully catch contextual personal and
  organization names.
- Not all factual answers have been re-verified by a domain expert.
- The analysis evaluates dataset snapshots; the source repositories may change later.
- This work contains no model training or benchmark results; data quality and task fit
  findings cannot be converted directly into claims about model performance.

## Evidence and reproducibility

In the final check on 21 July 2026, the nine raw dataset snapshots were reprofiled.
The `data_quality_profiles.json` and `cross_dataset_overlap.json` outputs remained
byte-identical to the earlier evidence. In addition, an independent audit covering row
counts, message counts, roles, empty content, `thinking`, `null`-as-text, and
normalized duplicate calculations passed **68/68 checks**. The notebook was re-run top
to bottom and produced no error output.

- [Executed Jupyter notebook](../notebook/huggingface_dataset_quality_analysis.ipynb)
- [Browser-viewable notebook HTML output](../notebook/huggingface_dataset_quality_analysis.html)
- [Full data quality profiles](../outputs/data_quality_profiles.json)
- [Manual findings](../outputs/manual_findings.json)
- [Cross-dataset overlap](../outputs/cross_dataset_overlap.json)
- [Source inventory](../outputs/source_inventory.json)
- [Capability manifest](../appendix/dataset_manifest.json)
- [CSV capability mapping](../appendix/capability_mapping.csv)

The notebook and the JSON files under `outputs/` are written in Turkish; the reports in
this directory are the English presentation layer over the same evidence.

The figures can be regenerated from the JSON outputs in this repository with
[`scripts/generate_report_charts.py`](../scripts/generate_report_charts.py). For figure
definitions and reading notes, see the [figure guide](figures/README.md).

## Questions for further work

- Which capability areas should be trained together, and which need separate adapters or data mixes?
- How should source-retrieval success be measured in time-sensitive areas?
- How should the number of examples to keep in normalized duplicate clusters be decided per task?
- Which scenarios should safety and scope boundary tests for identity behavior include?
- What should the automatic validation threshold be when generating Tool Calling, Structured Output, Math, and Coding data?
