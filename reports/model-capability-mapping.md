# Model Capability Mapping

[Main technical assessment](dataset-technical-assessment.md) ·
[Repository home](../README.md) ·
[Machine-readable manifest](../appendix/dataset_manifest.json)

## Technical summary

- **There are two direct datasets for Identity;** identity and developer answers exist,
  but safety, scope boundaries, and consistent refusal behavior must be prepared separately.
- **Conversation has six direct sources and two persona support sources;** the existing
  examples are single-turn and do not provide true multi-turn context tracking.
- **The Instruction Following contribution is partial across six datasets;** they teach
  domain question-answer behavior rather than general instruction diversity.
- **Tool Calling, Structured Output, and Math require conversion; Coding has no match.**
  Target record schemas and automatic validators must be written separately for these areas.

## Scope and matching criteria

This work covers only the nine Hugging Face datasets that were downloaded and
analyzed row by row earlier. No new dataset was added. Matching was done from the
actual row schema and content, not from the dataset name.

Technical names such as `messages`, `tool_calls`, `prompt`, `target`, and JSON Schema
are kept untranslated to preserve compatibility with the data structure.

### Matching levels

- **Direct:** The existing rows can be used as training examples for this capability.
- **Partial:** Contributes to the related behavior but does not teach the full capability.
- **Conversion source:** The raw content is suitable; target examples must be produced
  and validated separately.
- **No match:** The current nine datasets contain no labeled training example for this capability.

## Overall mapping

| Area | Project status | Existing datasets | Conclusion |
|---|---|---|---|
| Identity | Completed | `Aysenur44/namaz-vakti-identity-tr`, `sk75/sahin_identity` | Direct identity examples exist; safety principles and detailed boundary answers are missing. |
| Tool Calling | Planned | No direct dataset | Ithaki, e-commerce, and MEB content can serve as conversion sources. |
| Conversation | Planned | General knowledge, Marvel, e-commerce, MEB, biology, and philosophy | Usable for single-turn dialogue; no true multi-turn context tracking. |
| Instruction Following | Planned | E-commerce, MEB, general knowledge, biology, Marvel, and philosophy | Provides domain question-answer training; remains partial for broad instruction following. |
| Structured Output | Planned | No direct target-output dataset | The Ithaki catalog can be converted into JSON/table targets. |
| Math | Planned | No direct dataset | Limited arithmetic examples can be derived from the Ithaki price/discount fields. |
| Coding | Planned | No dataset | The current collection contains no code writing, debugging, or refactoring example. |

![Direct, partial, and conversion-source matches across capability areas](figures/capability-coverage.png)

The chart shows dataset counts by matching level. Conversation coverage is
comparatively broad; Instruction Following records are partial, while Tool Calling and
structured tasks sit at the conversion-source level. The numbers express how close the
existing content is to each task format — not model performance or data quality.

## Target record and validation contract

| Area | Proposed record | Required fields | Acceptance check |
|---|---|---|---|
| Identity | `messages` with persona metadata | `system`, `user`, `assistant`, `persona_id`, `language`, `policy_scope` | Consistent answers for the same identity, boundary behavior on out-of-scope questions |
| Tool Calling | Tool definition + call + result + final answer | `tools`, `tool_name`, `arguments`, `tool_result`, `assistant_final` | JSON Schema, tool name, argument type, correct use of the result in the answer |
| Conversation | Multi-turn message sequence | `conversation_id`, `turn_index`, `role`, `content`, `topic` | Role order, reference to the previous message, and turn integrity |
| Instruction Following | Task, input, constraints, and target | `instruction`, `input`, `constraints`, `target` | Task type and satisfaction of all constraints |
| Structured Output | Prompt + schema + output | `prompt`, `schema`, `target_json` | JSON parsing, required field, and data type validation |
| Math | Problem + solution + final answer | `problem`, `solution_steps`, `final_answer`, `unit` | Recomputation, tolerance, and unit consistency |
| Coding | Task + context + solution + tests | `task`, `language`, `context`, `solution`, `tests` | Compile/run, test result, and safe code checks |

## Identity — Completed

### Direct datasets

1. [Aysenur44/namaz-vakti-identity-tr](https://huggingface.co/datasets/Aysenur44/namaz-vakti-identity-tr)

   - **Rows:** 4
   - **Scope:** Model name, developer, identity, and core capability description.
   - **Strength:** The `system → user → assistant` layout suits identity training directly.
   - **Limit:** Four rows do not provide domain competence, safety principles, or detailed refusal/boundary behavior.
   - **Source access:** The raw data is not reproduced in this delivery repository; use the Hugging Face link above.

2. [sk75/sahin_identity](https://huggingface.co/datasets/sk75/sahin_identity)

   - **Rows:** 77
   - **Scope:** Turkish and English identity, ownership, developer, and capability answers.
   - **Strength:** Contains identity variations in two languages.
   - **Limit:** 64.94% of the assistant answers are normalized duplicates; 462 fields carry the string `"null"` instead of a real `null`, and there is no descriptive data card.
   - **Source access:** The raw data is not reproduced in this delivery repository; use the Hugging Face link above.

> The project's **Completed** status is preserved. However, because the "boundaries and
> safety principles" part of the given Identity definition is not covered adequately by
> these two datasets, it must be completed with separate test data.

## Tool Calling — Planned

### Direct match

**None.** The `tool_calls` fields in the eight conversation datasets are empty/null;
there is no `tool` role, function name, argument, function result, or chain that
produces a user answer from a result.

### Convertible sources

- [gururaser/ithaki-bilimkurgu-klasikleri](https://huggingface.co/datasets/gururaser/ithaki-bilimkurgu-klasikleri): its 103 structured catalog records can be used for tools such as `search_books`, `filter_books`, and `get_book_details`.
- [Mer1Alii/TR-ECommerce-CustomerSupport-Instructions](https://huggingface.co/datasets/Mer1Alii/TR-ECommerce-CustomerSupport-Instructions): convertible into `get_order_status`, `cancel_order`, and `create_support_ticket` scenarios. Unrealistic policy and contact claims must be cleaned first.
- [namruni/meb-ogretmen-soru-cevap](https://huggingface.co/datasets/namruni/meb-ogretmen-soru-cevap): convertible into `search_regulation` and `fetch_official_notice` tools; the results must come from current official sources.

These sources are not Tool Calling datasets as they stand. The function schema, correct
arguments, tool result, error scenario, and the final answer produced from the result
must be authored separately.

## Conversation — Planned

### Datasets usable for single-turn dialogue

| Dataset | Rows | Use | Core limitation |
|---|---:|---|---|
| [aliFurkan123/cultural-questions-dataset](https://huggingface.co/datasets/aliFurkan123/cultural-questions-dataset) | 500 | Turkish general knowledge and explanatory answers | Synthetic facts are unsourced; every assistant example has a `thinking` (reasoning) field. |
| [Egertekin/marvel-domain-dataset](https://huggingface.co/datasets/Egertekin/marvel-domain-dataset) | 177 | Domain-focused Turkish question-answering | 75.71% of the user prompts are duplicates; the row-level source chain is missing. |
| [Mer1Alii/TR-ECommerce-CustomerSupport-Instructions](https://huggingface.co/datasets/Mer1Alii/TR-ECommerce-CustomerSupport-Instructions) | 186 | Natural, solution-focused conversation with a customer | Synthetic company policies may teach wrong behavior; `thinking` must be removed. |
| [namruni/meb-ogretmen-soru-cevap](https://huggingface.co/datasets/namruni/meb-ogretmen-soru-cevap) | 450 | Long, contextual teacher question-answering | Time-sensitive regulations; current official source retrieval is required. |
| [nyzmemre/biyoloji-terimleri-turkce-sa](https://huggingface.co/datasets/nyzmemre/biyoloji-terimleri-turkce-sa) | 1,093 | Short Turkish scientific explanations | 21.59% of the answers are duplicates; there is no row-level source. |
| [yoitsmeyusuf/felsefe_finetune](https://huggingface.co/datasets/yoitsmeyusuf/felsefe_finetune) | 529 | Subjective Turkish answers presenting different views | 76.56% of the prompts are duplicates; the opinions must not be used as verified knowledge. |

The identity datasets can be added to persona conversations at low weight; they should
not form the main body of the Conversation set.

### Missing coverage

The existing rows are mostly in `user → assistant` form. Because there are no examples
of referring back to a previous user message, correcting, following up, switching
topic, or preserving multi-turn context, **multi-turn Conversation data must be
produced separately**.

## Instruction Following — Planned

The existing question-answer sets partially teach responding to narrow-domain instructions:

- E-commerce: understanding a user request and producing a support answer.
- MEB: producing an actionable explanation from a long question.
- General knowledge and biology: meeting an information request with an explanatory answer.
- Marvel: answering domain questions; should not be used before the duplicates are fixed.
- Philosophy: opinion generation; should not be used as a factual instruction-following dataset.

However, there is no instruction-following diversity such as summarization, rewriting,
classification, comparison, format constraints, multi-step tasks, negative constraints,
or few-shot steering. For that reason these datasets are **a domain-focused supervised
fine-tuning (SFT) source, not a general Instruction Following dataset**.

## Structured Output — Planned

### Direct match

**None.** No conversation dataset contains a verifiable JSON, table, or
schema-constrained target assistant output in response to a user request.

### Conversion source

[gururaser/ithaki-bilimkurgu-klasikleri](https://huggingface.co/datasets/gururaser/ithaki-bilimkurgu-klasikleri)
is a structured catalog with 103 rows and 17 fields. It can be used for the following targets:

- Converting book information into a fixed JSON schema
- Returning filtered results as a Markdown table
- Returning missing fields as a real `null`
- Type validation on the ISBN, price, and discount fields

Although the catalog is already structured data, in its current form it is not a
prompt–target Structured Output training set; the task prompts and expected outputs
must be created.

## Math — Planned

### Direct match

**None.** There is no dataset containing a math problem, solution steps, or a verified
final math answer.

The `eski_fiyat`, `satis_fiyati`, and `indirim_orani` fields in the Ithaki catalog can
be used to generate basic percentage/discount questions. That provides narrow
arithmetic only; it is no substitute for algebra, geometry, probability, or advanced math.

## Coding — Planned

**None.** The current nine datasets contain no code generation, test writing,
debugging, code explanation, refactoring, algorithm, or technical problem-solving
target. Because labeling unrelated text as Coding would lower training quality, no
Coding set was selected from the current collection.

## Implementation decisions

- Statuses other than Identity are preserved as `Planned`, as provided by the user.
- The same dataset may contribute to more than one area; this does not mean the content is directly ready in every area.
- A version carrying only the final answer must be created separately from the 1,136 assistant messages containing `thinking`.
- Tool Calling, Structured Output, Math, and Coding records should enter the training pool only after passing their automatic validators.
- For detailed per-dataset data quality risks, use the [main technical report](dataset-technical-assessment.md).
