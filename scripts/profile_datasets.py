"""Profile all downloaded Hugging Face datasets with deterministic checks."""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import unicodedata
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "outputs"

CONVERSATION_FIELDS = ("messages", "conversations", "conversation", "train")
# Message text and role aliases seen across ShareGPT, ChatML and ad-hoc exports.
CONTENT_KEYS = ("content", "value", "context", "text")
ROLE_KEYS = ("role", "from", "speaker")
ROLE_ALIASES = {
    "human": "user",
    "gpt": "assistant",
    "bot": "assistant",
    "ai": "assistant",
    "model": "assistant",
    "chatgpt": "assistant",
    "system_prompt": "system",
}
SYSTEM_FIELDS = ("system", "system_prompt")
# "instruction" and "input" are context fields for the same prompt, not
# alternatives: both are kept so an `instruction + input + output` record never
# loses its input silently.
INSTRUCTION_FIELDS = ("instruction", "prompt", "question", "user", "query")
INPUT_FIELDS = ("input", "context", "passage")
PROMPT_FIELDS = INSTRUCTION_FIELDS + INPUT_FIELDS
ANSWER_FIELDS = ("output", "response", "answer", "completion", "assistant", "target")
PROMPT_INPUT_SEPARATOR = "\n\n"
ITHAKI_COLUMNS = {
    "cevirmen", "eski_fiyat", "gorsel_url", "indirim_orani", "isbn",
    "kapak_tipi", "kategori", "kitap_adi", "kitap_url", "olculeri",
    "orijinal_adi", "ozet", "satis_fiyati", "sayfa_sayisi",
    "yayin_tarihi", "yayinevi", "yazar",
}
NULL_STRINGS = {"null", "none", "nil", "n/a", "na"}
# Texts shorter than this share tokens by coincidence, so near-duplicate
# comparison below this length reports noise rather than copying.
MIN_NEAR_DUPLICATE_TOKENS = 4
# Letters that occur in Turkish but not in English. Their share of all letters
# separates Turkish text from English text far more reliably than stopwords.
TURKISH_LETTERS = set("çğıİöşüÇĞÖŞÜ")
URL_RE = re.compile(r"https?://[^\s)\]}>'\"]+", re.IGNORECASE)
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_RE = re.compile(r"(?<!\d)(?:\+?90\s*)?(?:0?5\d{2})[\s.-]*\d{3}[\s.-]*\d{2}[\s.-]*\d{2}(?!\d)")
TR_ID_RE = re.compile(r"(?<!\d)[1-9]\d{10}(?!\d)")
PROFANITY_RE = re.compile(r"\b(?:amk|aq|siktir|orospu|piç|yarrak|salak|aptal)\b", re.IGNORECASE)
TIME_SENSITIVE_RE = re.compile(
    r"\b(?:bugün|yarın|dün|güncel|şu an|bu yıl|son \d+ (?:gün|ay|yıl)|202[4-9])\b",
    re.IGNORECASE,
)
TURKISH_STOPWORDS = {
    "ve", "bir", "bu", "için", "ile", "de", "da", "ne", "nasıl", "çok",
    "ama", "olarak", "olan", "ben", "sen", "mi", "mı", "mu", "mü",
}
ENGLISH_STOPWORDS = {
    "the", "and", "is", "are", "what", "who", "how", "with", "for", "you",
    "your", "my", "can", "do", "does", "a", "an", "of", "to",
}


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def normalized_text(value: object) -> str:
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFC", text).casefold()
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalized_loose(value: object) -> str:
    text = normalized_text(value)
    text = "".join(ch if ch.isalnum() else " " for ch in text)
    return re.sub(r"\s+", " ", text).strip()


def percentile(values: list[float], quantile: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = (len(ordered) - 1) * quantile
    lower = math.floor(index)
    upper = math.ceil(index)
    if lower == upper:
        return float(ordered[lower])
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (index - lower)


def numeric_summary(values: list[float]) -> dict:
    if not values:
        return {"min": None, "median": None, "mean": None, "p95": None, "max": None}
    return {
        "min": min(values),
        "median": statistics.median(values),
        "mean": round(statistics.mean(values), 2),
        "p95": round(percentile(values, 0.95) or 0, 2),
        "max": max(values),
    }


def duplicate_profile(values: list[str]) -> dict:
    """Count extra copies after the first item in each normalized text family.

    Every value is normalized exactly once and the first original spelling per
    family is remembered, so large datasets do not pay a repeated full-list
    rescan just to build the ``top_repeated`` sample.
    """

    counts: Counter[str] = Counter()
    first_original: dict[str, str] = {}
    for value in values:
        key = normalized_loose(value)
        counts[key] += 1
        if key not in first_original:
            first_original[key] = value
    duplicate_rows = sum(count - 1 for key, count in counts.items() if key and count > 1)
    duplicate_groups = sum(1 for key, count in counts.items() if key and count > 1)
    top = [
        {"count": count, "text": first_original[key][:300]}
        for key, count in counts.most_common(10)
        if key and count > 1
    ][:5]
    total = len(values)
    return {
        "duplicate_rows": duplicate_rows,
        "duplicate_rate": round(duplicate_rows / total, 4) if total else None,
        "duplicate_groups": duplicate_groups,
        # How much distinct text the dataset actually holds. Without this a
        # reader has to derive "1,000 rows but 20 distinct answers" by hand.
        "distinct_values": sum(1 for key in counts if key),
        "top_repeated": top,
    }


def near_duplicate_profile(values: list[str], threshold: float = 0.85) -> dict:
    """Count rows that are near-duplicates of an earlier row.

    ``duplicate_profile`` only sees texts that are identical once case and
    punctuation are normalized, so a reworded copy scores as unique. This
    measures token-set Jaccard overlap instead.

    The comparison is exact, not hashed or sampled: each text is indexed under
    its rarest tokens, so only genuinely plausible candidates are compared and a
    full pairwise scan is avoided while the result stays complete.
    """

    token_sets = [
        frozenset(re.findall(r"\w+", normalized_loose(value), flags=re.UNICODE))
        for value in values
    ]
    document_frequency: Counter[str] = Counter()
    for tokens in token_sets:
        document_frequency.update(tokens)

    index: dict[str, list[int]] = {}
    near_duplicate_rows = 0
    examples: list[dict] = []
    for position, tokens in enumerate(token_sets):
        # Very short texts share tokens by chance; comparing them produces noise
        # rather than evidence of copying.
        if len(tokens) < MIN_NEAR_DUPLICATE_TOKENS:
            continue
        # The token itself breaks frequency ties. Without it the order comes from
        # frozenset iteration, which varies with Python's hash randomization and
        # would make the whole profile non-reproducible between runs.
        probes = sorted(tokens, key=lambda token: (document_frequency[token], token))[:3]
        candidates: set[int] = set()
        for token in probes:
            candidates.update(index.get(token, ()))
        matched = None
        for candidate in sorted(candidates):
            other = token_sets[candidate]
            intersection = len(tokens & other)
            if intersection and intersection / len(tokens | other) >= threshold:
                matched = candidate
                break
        if matched is None:
            for token in probes:
                index.setdefault(token, []).append(position)
            continue
        near_duplicate_rows += 1
        if len(examples) < 3:
            examples.append(
                {
                    "text": values[position][:200],
                    "near_match": values[matched][:200],
                }
            )
    total = len(values)
    return {
        "near_duplicate_rows": near_duplicate_rows,
        "near_duplicate_rate": round(near_duplicate_rows / total, 4) if total else None,
        "threshold": threshold,
        "minimum_tokens": MIN_NEAR_DUPLICATE_TOKENS,
        "method": "token-set Jaccard, exact comparison; not hashed and not sampled",
        "examples": examples,
    }


def answer_family_profile(prompts: list[str], answers: list[str]) -> dict:
    """Group answers by normalized prompt to expose conflicting targets.

    A prompt that appears with several different answers is a different data
    problem from a prompt that merely repeats, so the two are reported apart.
    """

    families: dict[str, set[str]] = {}
    for prompt, answer in zip(prompts, answers):
        key = normalized_loose(prompt)
        if not key:
            continue
        families.setdefault(key, set()).add(normalized_loose(answer))
    conflicting = {key for key, variants in families.items() if len(variants) > 1}
    examples = sorted(
        ((key, len(families[key])) for key in conflicting),
        key=lambda item: (-item[1], item[0]),
    )[:5]
    return {
        "distinct_prompt_families": len(families),
        "prompt_families_with_conflicting_answers": len(conflicting),
        "rows_in_conflicting_families": sum(
            1 for prompt in prompts if normalized_loose(prompt) in conflicting
        ),
        "examples": [{"prompt": key[:200], "distinct_answers": count} for key, count in examples],
    }


def text_scan(texts: list[str]) -> dict:
    """Accumulate content signals per text instead of over one joined buffer.

    Scanning incrementally keeps peak memory proportional to the longest single
    text rather than to the whole dataset, which matters at tens of thousands of
    rows. Counts match the joined form because every pattern here matches within
    a single line and the former join character was a newline.
    """

    word_counts: Counter[str] = Counter()
    stopwords = TURKISH_STOPWORDS | ENGLISH_STOPWORDS
    patterns = {
        "url_matches": URL_RE,
        "email_matches": EMAIL_RE,
        "phone_matches": PHONE_RE,
        "turkish_id_like_matches": TR_ID_RE,
        "profanity_matches": PROFANITY_RE,
        "time_sensitive_matches": TIME_SENSITIVE_RE,
    }
    totals = dict.fromkeys(
        ("total_characters", "total_words", "replacement_character_count",
         "mojibake_marker_count", "turkish_letters", "alphabetic_characters"), 0
    )
    totals.update(dict.fromkeys(patterns, 0))
    for text in texts:
        totals["total_characters"] += len(text)
        totals["turkish_letters"] += sum(1 for ch in text if ch in TURKISH_LETTERS)
        totals["alphabetic_characters"] += sum(1 for ch in text if ch.isalpha())
        words = re.findall(r"\b\w+\b", text.casefold(), flags=re.UNICODE)
        totals["total_words"] += len(words)
        word_counts.update(word for word in words if word in stopwords)
        totals["replacement_character_count"] += text.count("�")
        totals["mojibake_marker_count"] += sum(text.count(marker) for marker in ("Ã", "Ä", "Å"))
        for name, pattern in patterns.items():
            totals[name] += len(pattern.findall(text))
    turkish_hits = sum(word_counts[word] for word in TURKISH_STOPWORDS)
    english_hits = sum(word_counts[word] for word in ENGLISH_STOPWORDS)
    # A heuristic, not a language classifier. Turkish-only letters are the
    # stronger of the two signals because they cannot appear in English text at
    # all, whereas stopwords overlap across languages.
    letters = totals.pop("alphabetic_characters")
    turkish_letters = totals.pop("turkish_letters")
    letter_ratio = round(turkish_letters / letters, 4) if letters else None
    if letter_ratio is None:
        dominant = "unknown"
    elif letter_ratio >= 0.01:
        dominant = "turkish"
    elif letter_ratio > 0 or turkish_hits > english_hits:
        dominant = "mixed"
    else:
        dominant = "english"
    return {
        **totals,
        "turkish_stopword_hits": turkish_hits,
        "english_stopword_hits": english_hits,
        "turkish_character_ratio": letter_ratio,
        "dominant_language_signal": dominant,
        "language_signal_note": "heuristic from Turkish-only letters and stopwords; not a classifier",
    }


def is_message_list(value: object) -> bool:
    """Return True when a value is a list of role/content message dicts."""

    return (
        isinstance(value, list)
        and bool(value)
        and all(
            isinstance(message, dict)
            and any(key in message for key in ROLE_KEYS)
            and any(key in message for key in CONTENT_KEYS)
            for message in value
        )
    )


def detect_conversation_field(rows: list) -> str | None:
    """Return the first field that consistently contains role/content messages."""

    dict_rows = [row for row in rows if isinstance(row, dict)]
    if not dict_rows:
        return None
    for field in CONVERSATION_FIELDS:
        populated = [row.get(field) for row in dict_rows if row.get(field) is not None]
        if not populated:
            continue
        if sum(is_message_list(value) for value in populated) / len(populated) >= 0.8:
            return field
    return None


def detect_bare_message_rows(rows: list) -> bool:
    """Return True when each row is itself a message list with no wrapper object.

    Some repositories publish a JSONL file whose lines are bare JSON arrays. The
    Dataset Viewer cannot infer a column schema from that layout, so the rows
    arrive here unwrapped and must be recognised explicitly rather than falling
    through to the generic tabular profile.
    """

    return bool(rows) and sum(is_message_list(row) for row in rows) / len(rows) >= 0.8


def detect_system_field(rows: list) -> str | None:
    """Return a top-level column that holds the system prompt for each row.

    Several datasets keep the system prompt beside the message list instead of
    inside it. Without this the system text would be dropped from every count.
    """

    dict_rows = [row for row in rows if isinstance(row, dict)]
    if not dict_rows:
        return None
    for field in SYSTEM_FIELDS:
        populated = [row.get(field) for row in dict_rows if isinstance(row.get(field), str)]
        if populated and len(populated) / len(dict_rows) >= 0.8:
            if sum(bool(value.strip()) for value in populated) / len(populated) >= 0.8:
                return field
    return None


def normalize_message(message: dict) -> dict:
    """Normalize ShareGPT, ChatML and ad-hoc role/content aliases.

    The raw row is never mutated; the normalized copy keeps every original key so
    per-message extras such as ``thinking`` and ``tool_calls`` stay countable.
    """

    role = next((message[key] for key in ROLE_KEYS if key in message), None)
    content = next((message[key] for key in CONTENT_KEYS if key in message), None)
    normalized = dict(message)
    normalized_role = normalized_text(role)
    normalized["role"] = ROLE_ALIASES.get(normalized_role, normalized_role)
    normalized["content"] = "" if content is None else str(content)
    return normalized


def extract_conversations(
    rows: list, field: str | None, system_field: str | None
) -> tuple[list[list[dict]], int]:
    """Return one normalized message list per row plus the unusable row count."""

    conversations: list[list[dict]] = []
    missing = 0
    for row in rows:
        value = row if field is None else (row.get(field) if isinstance(row, dict) else None)
        if isinstance(value, list):
            conversation = [normalize_message(m) for m in value if isinstance(m, dict)]
        else:
            conversation = []
            missing += 1
        if system_field and isinstance(row, dict):
            system_text = row.get(system_field)
            if isinstance(system_text, str) and system_text.strip():
                conversation = [{"role": "system", "content": system_text}] + conversation
        conversations.append(conversation)
    return conversations, missing


def json_answer_profile(answers: list[str]) -> dict:
    """Measure how far a dataset keeps a JSON-shaped answer contract.

    Reported for every answer set: a dataset whose targets are plain prose simply
    scores zero here, which is itself the meaningful reading.
    """

    parsable = 0
    json_like = 0
    key_counts: Counter[str] = Counter()
    for answer in answers:
        stripped = answer.strip()
        if not stripped.startswith(("{", "[")):
            continue
        json_like += 1
        try:
            parsed = json.loads(stripped)
        except (json.JSONDecodeError, ValueError):
            continue
        parsable += 1
        if isinstance(parsed, dict):
            key_counts.update(parsed.keys())
    total = len(answers)
    return {
        "json_like_answers": json_like,
        "json_parsable_answers": parsable,
        "json_parsable_rate": round(parsable / total, 4) if total else None,
        "json_like_but_unparsable_answers": json_like - parsable,
        "top_answer_schema_keys": dict(key_counts.most_common(10)),
    }


def conversation_profile(rows: list, field: str | None, system_field: str | None = None) -> dict:
    conversations, missing_conversation_rows = extract_conversations(rows, field, system_field)

    messages = [message for conv in conversations for message in conv if isinstance(message, dict)]
    roles = [normalized_text(message.get("role")) for message in messages]
    role_sequences = Counter(tuple(normalized_text(message.get("role")) for message in conv) for conv in conversations)
    user_texts = [
        str(message.get("content") or "")
        for conv in conversations
        for message in conv
        if isinstance(message, dict) and normalized_text(message.get("role")) == "user"
    ]
    assistant_texts = [
        str(message.get("content") or "")
        for conv in conversations
        for message in conv
        if isinstance(message, dict) and normalized_text(message.get("role")) == "assistant"
    ]
    all_texts = [str(message.get("content") or "") for message in messages]

    # One prompt and one answer per row keeps the conflicting-answer analysis
    # aligned even when a conversation carries a system turn or extra messages.
    row_prompts = [
        str(next((m.get("content") for m in conv if normalized_text(m.get("role")) == "user"), "") or "")
        for conv in conversations
    ]
    row_answers = [
        str(next((m.get("content") for m in conv if normalized_text(m.get("role")) == "assistant"), "") or "")
        for conv in conversations
    ]

    canonical_rows = [json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows]
    canonical_normalized = [normalized_text(value) for value in canonical_rows]
    exact_duplicate_rows = len(canonical_rows) - len(set(canonical_rows))
    normalized_duplicate_rows = len(canonical_normalized) - len(set(canonical_normalized))
    empty_content = sum(1 for message in messages if not normalized_text(message.get("content")))
    invalid_role = sum(1 for role in roles if role not in {"system", "user", "assistant"})
    null_string_fields = sum(
        1
        for message in messages
        for key, value in message.items()
        if key != "content" and isinstance(value, str) and value.casefold().strip() in NULL_STRINGS
    )
    nonempty_thinking = sum(
        1 for message in messages if normalized_text(message.get("thinking")) not in {"", "null", "none"}
    )
    # Some datasets carry the reasoning trace as a row-level column instead of a
    # per-message key. Counting only the message form would report those as zero.
    row_level_thinking = sum(
        1
        for row in rows
        if isinstance(row, dict)
        and normalized_text(row.get("thinking")) not in {"", "null", "none"}
    )
    unexpected_turns = sum(1 for conv in conversations if len(conv) not in {2, 3})
    matching_user_assistant = sum(
        1
        for conv in conversations
        if len(conv) >= 2
        and normalized_loose(next((m.get("content") for m in conv if normalized_text(m.get("role")) == "user"), ""))
        == normalized_loose(next((m.get("content") for m in conv if normalized_text(m.get("role")) == "assistant"), ""))
    )

    return {
        "data_shape": "conversation",
        "conversation_field": field if field is not None else "<bare row array>",
        "system_prompt_field": system_field,
        "row_count": len(rows),
        "message_count": len(messages),
        "turn_count_summary": numeric_summary([len(conv) for conv in conversations]),
        "role_counts": dict(Counter(roles)),
        "role_sequences": {" → ".join(sequence): count for sequence, count in role_sequences.items()},
        "missing_conversation_rows": missing_conversation_rows,
        "unexpected_turn_count_rows": unexpected_turns,
        "empty_content_messages": empty_content,
        "invalid_role_messages": invalid_role,
        "string_encoded_null_fields": null_string_fields,
        "nonempty_thinking_messages": nonempty_thinking,
        "row_level_thinking_rows": row_level_thinking,
        "exact_duplicate_rows": exact_duplicate_rows,
        "exact_duplicate_rate": round(exact_duplicate_rows / len(rows), 4) if rows else None,
        "distinct_canonical_rows": len(set(canonical_rows)),
        "normalized_duplicate_rows": normalized_duplicate_rows,
        "user_prompt_duplicates": duplicate_profile(user_texts),
        "assistant_answer_duplicates": duplicate_profile(assistant_texts),
        "user_prompt_near_duplicates": near_duplicate_profile(row_prompts),
        "assistant_answer_near_duplicates": near_duplicate_profile(row_answers),
        "answer_families": answer_family_profile(row_prompts, row_answers),
        "structured_answers": json_answer_profile(row_answers),
        "matching_user_assistant_rows": matching_user_assistant,
        "user_character_length": numeric_summary([len(value) for value in user_texts]),
        "assistant_character_length": numeric_summary([len(value) for value in assistant_texts]),
        "user_word_length": numeric_summary([len(value.split()) for value in user_texts]),
        "assistant_word_length": numeric_summary([len(value.split()) for value in assistant_texts]),
        "text_scan": text_scan(all_texts),
        "user_prompts": user_texts,
        "assistant_answers": assistant_texts,
    }


def detect_instruction_pair(rows: list[dict]) -> tuple[list[str], str] | None:
    """Detect prompt/answer field pairs in flat instruction datasets.

    ``instruction`` and ``input`` describe the same prompt from two angles, so
    every present prompt field is returned rather than only the first match. An
    ``instruction + input + output`` record must never lose its ``input``.
    """

    dict_rows = [row for row in rows if isinstance(row, dict)]
    if not dict_rows:
        return None
    columns = set().union(*(row.keys() for row in dict_rows))
    prompt_fields = [field for field in PROMPT_FIELDS if field in columns]
    answer_field = next((field for field in ANSWER_FIELDS if field in columns), None)
    prompt_fields = [field for field in prompt_fields if field != answer_field]
    if not prompt_fields or not answer_field:
        return None
    usable = sum(
        any(normalized_text(row.get(field)) != "" for field in prompt_fields)
        or normalized_text(row.get(answer_field)) != ""
        for row in dict_rows
    )
    return (prompt_fields, answer_field) if usable / len(dict_rows) >= 0.8 else None


def join_prompt_fields(row: dict, prompt_fields: list[str]) -> str:
    parts = [
        str(row.get(field)) for field in prompt_fields if normalized_text(row.get(field)) != ""
    ]
    return PROMPT_INPUT_SEPARATOR.join(parts)


def instruction_pair_profile(rows: list[dict], prompt_fields: list[str], answer_field: str) -> dict:
    prompts = [join_prompt_fields(row, prompt_fields) for row in rows]
    answers = ["" if row.get(answer_field) is None else str(row.get(answer_field)) for row in rows]
    canonical_rows = [json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows]
    return {
        "data_shape": "instruction_pair",
        "prompt_field": " + ".join(prompt_fields),
        "prompt_fields": prompt_fields,
        "prompt_field_separator": PROMPT_INPUT_SEPARATOR,
        "prompt_fields_dropped": [],
        "answer_field": answer_field,
        "row_count": len(rows),
        "message_count": len(rows) * 2,
        "missing_conversation_rows": 0,
        "unexpected_turn_count_rows": 0,
        "empty_content_messages": sum(
            1 for value in prompts + answers if not normalized_text(value)
        ),
        "invalid_role_messages": 0,
        "string_encoded_null_fields": sum(
            1
            for row in rows
            for value in row.values()
            if isinstance(value, str) and value.casefold().strip() in NULL_STRINGS
        ),
        "nonempty_thinking_messages": sum(
            1
            for row in rows
            if normalized_text(row.get("thinking")) not in {"", "null", "none"}
        ),
        "exact_duplicate_rows": len(canonical_rows) - len(set(canonical_rows)),
        "exact_duplicate_rate": round(
            (len(canonical_rows) - len(set(canonical_rows))) / len(rows), 4
        ) if rows else None,
        "distinct_canonical_rows": len(set(canonical_rows)),
        "user_prompt_duplicates": duplicate_profile(prompts),
        "assistant_answer_duplicates": duplicate_profile(answers),
        "user_prompt_near_duplicates": near_duplicate_profile(prompts),
        "assistant_answer_near_duplicates": near_duplicate_profile(answers),
        "answer_families": answer_family_profile(prompts, answers),
        "structured_answers": json_answer_profile(answers),
        "matching_user_assistant_rows": sum(
            normalized_loose(prompt) == normalized_loose(answer) and bool(normalized_loose(prompt))
            for prompt, answer in zip(prompts, answers)
        ),
        "user_character_length": numeric_summary([len(value) for value in prompts]),
        "assistant_character_length": numeric_summary([len(value) for value in answers]),
        "user_word_length": numeric_summary([len(value.split()) for value in prompts]),
        "assistant_word_length": numeric_summary([len(value.split()) for value in answers]),
        "text_scan": text_scan(prompts + answers),
        "user_prompts": prompts,
        "assistant_answers": answers,
    }


def canonical_value(value: object) -> str:
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    except TypeError:
        return str(value)


def flatten_text_values(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [text for nested in value.values() for text in flatten_text_values(nested)]
    if isinstance(value, list):
        return [text for nested in value for text in flatten_text_values(nested)]
    return [str(value)]


def generic_tabular_profile(rows: list[dict]) -> dict:
    columns = sorted(set().union(*(row.keys() for row in rows))) if rows else []
    null_counts = {
        column: sum(
            1
            for row in rows
            if row.get(column) is None
            or (isinstance(row.get(column), str) and not row.get(column).strip())
        )
        for column in columns
    }
    type_counts = {
        column: dict(Counter(type(row.get(column)).__name__ for row in rows))
        for column in columns
    }
    unique_counts = {
        column: len({canonical_value(row.get(column)) for row in rows})
        for column in columns
    }
    numeric_columns = {}
    for column in columns:
        values = [
            float(row[column])
            for row in rows
            if isinstance(row.get(column), (int, float)) and not isinstance(row.get(column), bool)
        ]
        if values:
            numeric_columns[column] = numeric_summary(values)
    canonical_rows = [json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows]
    texts = [text for row in rows for value in row.values() for text in flatten_text_values(value)]
    return {
        "data_shape": "tabular",
        "row_count": len(rows),
        "column_count": len(columns),
        "columns": columns,
        "null_counts": null_counts,
        "null_rates": {
            column: round(count / len(rows), 4) if rows else None
            for column, count in null_counts.items()
        },
        "type_counts": type_counts,
        "unique_counts": unique_counts,
        "numeric_columns": numeric_columns,
        "exact_duplicate_rows": len(canonical_rows) - len(set(canonical_rows)),
        "exact_duplicate_rate": round(
            (len(canonical_rows) - len(set(canonical_rows))) / len(rows), 4
        ) if rows else None,
        "distinct_canonical_rows": len(set(canonical_rows)),
        "text_scan": text_scan(texts),
    }


def parse_price(value: object) -> float | None:
    if value is None:
        return None
    text = str(value).replace("₺", "").replace(".", "").replace(",", ".").strip()
    try:
        return float(text)
    except ValueError:
        return None


def valid_isbn13(value: object) -> bool:
    digits = re.sub(r"\D", "", str(value or ""))
    if len(digits) != 13:
        return False
    check = sum((1 if index % 2 == 0 else 3) * int(digit) for index, digit in enumerate(digits[:12]))
    return (10 - check % 10) % 10 == int(digits[-1])


def catalog_profile(rows: list[dict]) -> dict:
    columns = sorted(set().union(*(row.keys() for row in rows)))
    null_counts = {
        column: sum(1 for row in rows if row.get(column) is None or str(row.get(column)).strip() == "")
        for column in columns
    }
    old_prices = [parse_price(row.get("eski_fiyat")) for row in rows]
    sale_prices = [parse_price(row.get("satis_fiyati")) for row in rows]
    discounts = []
    inconsistent_discount_rows = 0
    for row, old_price, sale_price in zip(rows, old_prices, sale_prices):
        raw_discount = str(row.get("indirim_orani") or "").replace("%", "").strip()
        try:
            discount = float(raw_discount)
        except ValueError:
            discount = None
        discounts.append(discount)
        if old_price is not None and sale_price is not None and discount is not None:
            expected_sale = old_price * (1 - discount / 100)
            if abs(expected_sale - sale_price) > 1:
                inconsistent_discount_rows += 1

    urls = [str(row.get("kitap_url") or "") for row in rows]
    image_urls = [str(row.get("gorsel_url") or "") for row in rows]
    invalid_urls = sum(1 for value in urls + image_urls if value and urlparse(value).scheme not in {"http", "https"})
    summaries = [str(row.get("ozet") or "") for row in rows]
    canonical_rows = [json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows]

    return {
        "data_shape": "catalog",
        "row_count": len(rows),
        "column_count": len(columns),
        "columns": columns,
        "null_counts": null_counts,
        "null_rates": {column: round(count / len(rows), 4) if rows else None for column, count in null_counts.items()},
        "exact_duplicate_rows": len(canonical_rows) - len(set(canonical_rows)),
        "distinct_canonical_rows": len(set(canonical_rows)),
        "duplicate_isbn_rows": len(rows) - len({str(row.get("isbn")) for row in rows}),
        "duplicate_book_url_rows": len(rows) - len(set(urls)),
        "duplicate_title_author_rows": len(rows) - len({(normalized_loose(row.get("kitap_adi")), normalized_loose(row.get("yazar"))) for row in rows}),
        "invalid_isbn13_rows": sum(1 for row in rows if not valid_isbn13(row.get("isbn"))),
        "invalid_url_rows": invalid_urls,
        "page_count_summary": numeric_summary([int(row["sayfa_sayisi"]) for row in rows if isinstance(row.get("sayfa_sayisi"), (int, float))]),
        "old_price_summary": numeric_summary([round(value) for value in old_prices if value is not None]),
        "sale_price_summary": numeric_summary([round(value) for value in sale_prices if value is not None]),
        "discount_summary": numeric_summary([round(value) for value in discounts if value is not None]),
        "discount_inconsistency_rows": inconsistent_discount_rows,
        "summary_duplicates": duplicate_profile(summaries),
        "summary_character_length": numeric_summary([len(value) for value in summaries]),
        "category_counts": dict(Counter(str(row.get("kategori")) for row in rows)),
        "text_scan": text_scan([str(value) for row in rows for value in row.values() if value is not None]),
    }


def extract_card_summary(metadata: dict, readme: str) -> dict:
    card = metadata.get("cardData") or {}
    description_body = readme.split("---", 2)[-1].strip() if readme.startswith("---") else readme.strip()
    return {
        "license": card.get("license"),
        "language_tags": card.get("language") or [],
        "task_categories": card.get("task_categories") or [],
        "tags": card.get("tags") or [],
        "readme_present": bool(readme),
        "readme_characters": len(readme),
        "readme_has_body": len(description_body) >= 200,
        "readme_mentions_source": bool(re.search(r"kaynak|source|scrap|kazıma|reddit|wikipedia|forum", readme, re.IGNORECASE)),
        "readme_mentions_limitations": bool(re.search(r"sınırlama|limitation|uyarı|güncel olmayabilir", readme, re.IGNORECASE)),
        "readme_mentions_split": bool(re.search(r"test|validation|validasyon|doğrulama", readme, re.IGNORECASE)),
    }


def receipt_row_files(dataset_dir: Path, receipts: list[dict]) -> list[tuple[str, Path]]:
    """Resolve the row file each completed receipt wrote.

    Reading exactly the receipted files, rather than globbing the snapshot
    directory, is what stops a stale snapshot from an earlier download path
    being counted alongside the current one.
    """

    resolved: list[tuple[str, Path]] = []
    for receipt in receipts:
        row_file = receipt.get("row_file")
        if not row_file:
            raise RuntimeError(
                f"Receipt for {receipt.get('dataset')} {receipt.get('config')}/"
                f"{receipt.get('split')} has no row_file; re-run the downloader"
            )
        path = dataset_dir / row_file
        if not path.is_file():
            raise RuntimeError(f"Receipted row file is missing: {path}")
        label = f"{receipt.get('config')}/{receipt.get('split')}"
        resolved.append((label, path))
    return resolved


def find_viewer_rows(dataset_dir: Path, receipts: list[dict]) -> tuple[list, dict[str, int]]:
    """Load every receipted row file, from the Viewer, a source file, or the fallback.

    Rows are returned exactly as downloaded, including bare JSON arrays, so any
    reshaping happens in a named adapter rather than silently at read time. The
    second value maps each split to its row count.
    """

    rows: list = []
    per_source: dict[str, int] = {}
    for label, path in receipt_row_files(dataset_dir, receipts):
        loaded = read_jsonl(path)
        per_source[label] = len(loaded)
        rows.extend(loaded)
    return rows, per_source


def cross_split_duplicate_profile(dataset_dir: Path, receipts: list[dict]) -> dict:
    """Count rows that appear in more than one split of the same dataset.

    Language-variant splits ("turkish"/"english") are alternative renderings of
    the same material, not partitions, so an explicit check is needed before the
    per-split counts are added into one dataset total.
    """

    per_split: dict[str, set[str]] = {}
    for label, path in receipt_row_files(dataset_dir, receipts):
        per_split[label] = {
            json.dumps(row, ensure_ascii=False, sort_keys=True) for row in read_jsonl(path)
        }
    overlaps = []
    names = sorted(per_split)
    for index, left in enumerate(names):
        for right in names[index + 1 :]:
            shared = len(per_split[left] & per_split[right])
            if shared:
                overlaps.append({"left": left, "right": right, "shared_rows": shared})
    return {
        "split_count": len(per_split),
        "split_row_counts": {name: len(values) for name, values in per_split.items()},
        "cross_split_duplicate_pairs": overlaps,
        "cross_split_duplicate_rows": sum(item["shared_rows"] for item in overlaps),
    }


def resolve_path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else PROJECT_DIR / path


def safe_slug(dataset_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "__", dataset_id)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default=str(DATA_DIR), help="Local snapshot directory")
    parser.add_argument(
        "--inventory",
        default=str(OUTPUT_DIR / "source_inventory.json"),
        help="Source inventory JSON",
    )
    parser.add_argument(
        "--profiles",
        default=str(OUTPUT_DIR / "data_quality_profiles.json"),
        help="Profile JSON output",
    )
    parser.add_argument(
        "--overlap",
        default=str(OUTPUT_DIR / "cross_dataset_overlap.json"),
        help="Cross-dataset overlap JSON output",
    )
    parser.add_argument(
        "--excluded",
        default=str(OUTPUT_DIR / "excluded_datasets.json"),
        help="Recorded access-block JSON output",
    )
    parser.add_argument(
        "--allow-incomplete",
        action="store_true",
        help="Profile available rows even when a snapshot receipt is incomplete",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data_dir = resolve_path(args.data_dir)
    inventory_path = resolve_path(args.inventory)
    profiles_path = resolve_path(args.profiles)
    overlap_path = resolve_path(args.overlap)
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    profiles: list[dict] = []
    excluded: list[dict] = []
    prompt_sets: dict[str, set[str]] = {}
    answer_sets: dict[str, set[str]] = {}
    failures: list[str] = []

    # Stable slug order preserves deterministic profile JSON across registry edits.
    for inventory_item in sorted(
        inventory, key=lambda item: safe_slug(item["dataset_id"]).casefold()
    ):
        dataset_id = inventory_item["dataset_id"]
        dataset_dir = data_dir / safe_slug(dataset_id)
        receipts = inventory_item.get("viewer_receipts", [])

        # A declared and re-verified access block is a recorded exclusion, not a
        # silent skip and not a pipeline failure. Anything else that is missing
        # still stops the run.
        block = inventory_item.get("access_block")
        if block:
            if not block.get("still_blocked"):
                failures.append(
                    f"{dataset_id}: access block is declared but no longer applies; "
                    "remove access_block from config/datasets.json and re-download"
                )
                continue
            excluded.append(
                {
                    "dataset_id": dataset_id,
                    "url": f"https://huggingface.co/datasets/{dataset_id}",
                    "contributor": inventory_item.get("contributor"),
                    "contributor_source": inventory_item.get("contributor_source"),
                    "status": block.get("status"),
                    "declared_on": block.get("checked_on"),
                    "reverified_on": block.get("reverified_on"),
                    "evidence": block.get("evidence"),
                    "reverified_checks": block.get("reverified_checks", []),
                    "unblock": block.get("unblock"),
                }
            )
            continue

        if inventory_item.get("download_error"):
            failures.append(f"{dataset_id}: {inventory_item['download_error']}")
            continue
        if not args.allow_incomplete and (
            not receipts or any(not receipt.get("complete") for receipt in receipts)
        ):
            failures.append(f"{dataset_id}: incomplete snapshot download")
            continue
        metadata_path = dataset_dir / "metadata.json"
        if not metadata_path.exists():
            failures.append(f"{dataset_id}: metadata.json is missing")
            continue
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        readme_path = dataset_dir / "raw" / "README.md"
        readme = readme_path.read_text(encoding="utf-8", errors="replace") if readme_path.exists() else ""
        rows, per_source = find_viewer_rows(dataset_dir, receipts)
        if not rows:
            failures.append(f"{dataset_id}: no local rows")
            continue

        conversation_field = detect_conversation_field(rows)
        bare_message_rows = detect_bare_message_rows(rows) if not conversation_field else False
        instruction_pair = (
            detect_instruction_pair(rows)
            if not conversation_field and not bare_message_rows
            else None
        )
        columns = set().union(*(row.keys() for row in rows if isinstance(row, dict))) or set()
        if conversation_field or bare_message_rows:
            system_field = detect_system_field(rows) if conversation_field else None
            data_profile = conversation_profile(rows, conversation_field, system_field)
            prompt_sets[dataset_id] = {normalized_loose(value) for value in data_profile.pop("user_prompts") if normalized_loose(value)}
            answer_sets[dataset_id] = {normalized_loose(value) for value in data_profile.pop("assistant_answers") if normalized_loose(value)}
        elif instruction_pair:
            data_profile = instruction_pair_profile(rows, *instruction_pair)
            prompt_sets[dataset_id] = {
                normalized_loose(value)
                for value in data_profile.pop("user_prompts")
                if normalized_loose(value)
            }
            answer_sets[dataset_id] = {
                normalized_loose(value)
                for value in data_profile.pop("assistant_answers")
                if normalized_loose(value)
            }
        elif ITHAKI_COLUMNS.issubset(columns):
            data_profile = catalog_profile(rows)
        else:
            data_profile = generic_tabular_profile(rows)

        data_profile["row_sources"] = per_source
        data_profile["split_integrity"] = cross_split_duplicate_profile(dataset_dir, receipts)

        profile_entry = {
            "dataset_id": dataset_id,
            "url": f"https://huggingface.co/datasets/{dataset_id}",
            "sha": metadata.get("sha"),
            "created_at": metadata.get("createdAt"),
            "last_modified": metadata.get("lastModified"),
            "downloads": metadata.get("downloads"),
            "likes": metadata.get("likes"),
            "used_storage": metadata.get("usedStorage"),
            "private": metadata.get("private"),
            "gated": metadata.get("gated"),
            "files": inventory_item.get("files", []),
            "splits": receipts,
            "card": extract_card_summary(metadata, readme),
            "profile": data_profile,
        }
        if inventory_item.get("contributor"):
            profile_entry["contributor"] = inventory_item["contributor"]
        if inventory_item.get("contributor_source"):
            profile_entry["contributor_source"] = inventory_item["contributor_source"]
        profiles.append(profile_entry)

    overlaps = []
    dataset_ids = sorted(prompt_sets)
    for index, left in enumerate(dataset_ids):
        for right in dataset_ids[index + 1 :]:
            shared_prompts = prompt_sets[left] & prompt_sets[right]
            shared_answers = answer_sets[left] & answer_sets[right]
            if shared_prompts or shared_answers:
                overlaps.append(
                    {
                        "left": left,
                        "right": right,
                        "shared_user_prompts": len(shared_prompts),
                        "shared_assistant_answers": len(shared_answers),
                        "prompt_examples": sorted(shared_prompts)[:3],
                        "answer_examples": sorted(shared_answers)[:3],
                    }
                )

    if failures:
        details = "\n".join(f"- {failure}" for failure in failures)
        raise RuntimeError(
            "Profiling stopped because one or more configured snapshots are incomplete:\n"
            f"{details}\nUse --allow-incomplete only when partial analysis is explicitly intended."
        )

    profiles_path.parent.mkdir(parents=True, exist_ok=True)
    profiles_path.write_text(
        json.dumps(profiles, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    overlap_path.parent.mkdir(parents=True, exist_ok=True)
    overlap_path.write_text(
        json.dumps(overlaps, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    excluded_path = resolve_path(args.excluded)
    excluded_path.parent.mkdir(parents=True, exist_ok=True)
    excluded_path.write_text(
        json.dumps(
            {
                "note": (
                    "Registry datasets that are enabled but cannot be analyzed. Each entry "
                    "records the live HTTP evidence re-verified during the last download."
                ),
                "datasets": excluded,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    total_rows = sum(item["profile"]["row_count"] for item in profiles)
    print(f"Profiled {len(profiles)} datasets, {total_rows:,} rows")
    print(f"Cross-dataset overlap pairs: {len(overlaps)}")
    if excluded:
        print(f"Recorded access blocks (not analyzed): {len(excluded)}")
        for item in excluded:
            print(f"  - {item['dataset_id']}: {item['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
