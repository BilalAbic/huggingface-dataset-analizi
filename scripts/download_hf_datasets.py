"""Download fixed Hugging Face dataset snapshots into the local ``data`` folder.

Dataset IDs normally come from ``config/datasets.json``. Raw snapshots are
ignored by Git; only reviewed profiles and presentation artifacts are public.
The script uses Python's standard library so it can run before project
dependencies are installed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "datasets.json"
DEFAULT_DATA_DIR = ROOT / "data"
DEFAULT_INVENTORY = ROOT / "outputs" / "source_inventory.json"
USER_AGENT = "HuggingFace-Dataset-Quality-Audit/2.0"

# Raw-file fallback formats that the standard library can parse losslessly.
# Anything else is recorded as an explicit blocker instead of being sampled.
FALLBACK_SUFFIXES = (".jsonl", ".ndjson", ".json")
PARQUET_SUFFIXES = (".parquet",)
SOURCE_SUFFIXES = FALLBACK_SUFFIXES + PARQUET_SUFFIXES

# Most repositories here publish only auto-converted Parquet, which the standard
# library cannot read. Without a Parquet reader those datasets can only be paged
# through the Dataset Viewer, which is both slow and a single point of failure:
# a repository updated minutes ago answers HTTP 500 until re-indexing finishes.
try:  # pragma: no cover - import guard
    import pyarrow.parquet as _parquet
except ImportError:  # pragma: no cover - optional at runtime
    _parquet = None


def safe_slug(dataset_id: str) -> str:
    """Convert ``owner/name`` into a stable local directory name."""

    return re.sub(r"[^A-Za-z0-9._-]+", "__", dataset_id)


def resolve_path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def auth_headers() -> dict[str, str]:
    """Return request headers, adding a bearer token when one is in the environment.

    The token is read from ``HF_TOKEN`` or ``HUGGINGFACE_HUB_TOKEN`` and is never
    written to a file, printed, or stored in the inventory. Running without a
    token still works; it is only slower and cannot reach gated repositories.
    """

    headers = {"User-Agent": USER_AGENT}
    token = (os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_HUB_TOKEN") or "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def has_token() -> bool:
    return bool(
        (os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_HUB_TOKEN") or "").strip()
    )


# Anonymous Hugging Face API access is rate limited and returns HTTP 429 without
# a Retry-After header. Requests are spaced out, and every 429 both waits out the
# cooldown and widens the spacing, so a long batch settles on a sustainable rate
# instead of hammering the endpoint. An authenticated run starts from a tighter
# interval because its quota is far larger.
_throttle = {"min_interval": 0.15 if has_token() else 0.8, "last_request": 0.0}
RATE_LIMIT_BACKOFF_SECONDS = (45, 90, 150, 240)
MAX_REQUEST_INTERVAL = 4.0
# The Dataset Viewer answers 5xx while it re-indexes a recently updated
# repository ("the response is not ready yet"). That is a wait, not a failure,
# so it gets its own backoff instead of burning the ordinary retries. The wait is
# deliberately short: the revision-pinned source-file path can read the same rows
# without the Viewer, so there is no reason to block for minutes on it.
SERVER_BUSY_BACKOFF_SECONDS = (10, 25)


def _wait_for_slot() -> None:
    elapsed = time.monotonic() - _throttle["last_request"]
    if elapsed < _throttle["min_interval"]:
        time.sleep(_throttle["min_interval"] - elapsed)
    _throttle["last_request"] = time.monotonic()


def request_bytes(url: str, retries: int = 3) -> bytes:
    last_error: Exception | None = None
    rate_limit_hits = 0
    server_busy_hits = 0
    attempt = 0
    while attempt < retries:
        _wait_for_slot()
        try:
            request = urllib.request.Request(url, headers=auth_headers())
            with urllib.request.urlopen(request, timeout=90) as response:
                return response.read()
        except urllib.error.HTTPError as error:
            last_error = error
            if error.code >= 500:
                # A freshly updated repository is still being indexed. Waiting is
                # the documented remedy, so this does not consume a retry.
                if server_busy_hits >= len(SERVER_BUSY_BACKOFF_SECONDS):
                    break
                wait = SERVER_BUSY_BACKOFF_SECONDS[server_busy_hits]
                print(
                    f"Dataset Viewer returned HTTP {error.code} (still indexing). "
                    f"Waiting {wait}s before retrying.",
                    file=sys.stderr,
                    flush=True,
                )
                time.sleep(wait)
                server_busy_hits += 1
                continue
            if error.code != 429:
                if attempt + 1 < retries:
                    time.sleep(2**attempt)
                attempt += 1
                continue
            # A 429 is a pacing problem, not a failed dataset: do not spend a
            # regular retry on it.
            if rate_limit_hits >= len(RATE_LIMIT_BACKOFF_SECONDS):
                break
            _throttle["min_interval"] = min(
                MAX_REQUEST_INTERVAL, _throttle["min_interval"] + 0.5
            )
            wait = RATE_LIMIT_BACKOFF_SECONDS[rate_limit_hits]
            print(
                f"Rate limited (HTTP 429). Waiting {wait}s and slowing to "
                f"{_throttle['min_interval']:.1f}s between requests.",
                file=sys.stderr,
                flush=True,
            )
            time.sleep(wait)
            rate_limit_hits += 1
        except (urllib.error.URLError, TimeoutError) as error:
            last_error = error
            if attempt + 1 < retries:
                time.sleep(2**attempt)
            attempt += 1
    raise RuntimeError(f"Download failed after {retries} attempts: {url}") from last_error


def request_json(url: str) -> dict:
    return json.loads(request_bytes(url).decode("utf-8"))


def probe_status(url: str) -> dict:
    """Return the live HTTP outcome for a URL without raising.

    Declared access blocks are re-verified on every run so a stale blocker
    cannot silently keep a dataset out of scope after it becomes readable.
    """

    _wait_for_slot()
    request = urllib.request.Request(url, headers=auth_headers())
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return {"url": url, "status": response.status}
    except urllib.error.HTTPError as error:
        detail = error.read(400).decode("utf-8", "replace").strip()
        return {"url": url, "status": error.code, "detail": detail}
    except (urllib.error.URLError, TimeoutError) as error:
        return {"url": url, "status": None, "detail": repr(error)}


def write_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_dataset_entries(config_path: Path, explicit_ids: list[str]) -> list[dict]:
    if explicit_ids:
        entries = [{"dataset_id": dataset_id, "contributor": None} for dataset_id in explicit_ids]
    else:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
        entries = [entry for entry in payload.get("datasets", []) if entry.get("enabled", True)]

    seen: set[str] = set()
    normalized: list[dict] = []
    for entry in entries:
        dataset_id = str(entry.get("dataset_id", "")).strip().strip("/")
        if dataset_id.count("/") != 1:
            raise ValueError(f"Invalid Hugging Face dataset ID: {dataset_id!r}")
        if dataset_id in seen:
            continue
        seen.add(dataset_id)
        normalized.append(
            {
                "dataset_id": dataset_id,
                "contributor": entry.get("contributor"),
                "contributor_source": entry.get("contributor_source"),
                "access_block": entry.get("access_block"),
            }
        )
    if not normalized:
        raise ValueError("No enabled datasets were found")
    return normalized


def verify_access_block(dataset_id: str, declared: dict) -> dict:
    """Re-check a declared blocker and return the block record for the inventory."""

    quoted = urllib.parse.quote(dataset_id)
    checks = [
        probe_status(f"https://huggingface.co/api/datasets/{quoted}"),
        probe_status(f"https://datasets-server.huggingface.co/splits?dataset={quoted}"),
    ]
    still_blocked = any(check["status"] != 200 for check in checks)
    return {
        **declared,
        "reverified_on": time.strftime("%Y-%m-%d"),
        "reverified_checks": checks,
        "still_blocked": still_blocked,
    }


def download_repository_files(
    dataset_id: str,
    dataset_dir: Path,
    metadata: dict,
    *,
    download_all: bool,
) -> list[str]:
    revision = metadata.get("sha") or "main"
    downloaded: list[str] = []
    for sibling in metadata.get("siblings", []):
        relative_path = sibling.get("rfilename")
        if not relative_path or relative_path == ".gitattributes":
            continue
        if not download_all and relative_path != "README.md":
            continue
        quoted_path = "/".join(urllib.parse.quote(part) for part in relative_path.split("/"))
        url = (
            f"https://huggingface.co/datasets/{dataset_id}/resolve/"
            f"{revision}/{quoted_path}?download=true"
        )
        write_bytes(dataset_dir / "raw" / relative_path, request_bytes(url))
        downloaded.append(relative_path)
    return downloaded


def download_viewer_rows(
    dataset_id: str,
    dataset_dir: Path,
    *,
    max_viewer_rows: int,
    metadata: dict | None = None,
    prefer_source_files: bool = True,
) -> list[dict]:
    split_url = "https://datasets-server.huggingface.co/splits?" + urllib.parse.urlencode(
        {"dataset": dataset_id}
    )
    try:
        split_payload = request_json(split_url)
        write_json(dataset_dir / "viewer_splits.json", split_payload)
        size_url = "https://datasets-server.huggingface.co/size?" + urllib.parse.urlencode(
            {"dataset": dataset_id}
        )
        size_payload = request_json(size_url)
        write_json(dataset_dir / "viewer_size.json", size_payload)
    except RuntimeError as error:
        return [{"dataset": dataset_id, "complete": False, "viewer_error": str(error)}]

    split_sizes = {
        (item["config"], item["split"]): int(item.get("num_rows") or 0)
        for item in (size_payload.get("size") or {}).get("splits", [])
    }
    receipts: list[dict] = []
    consumed_files: set[str] = set()
    for split_info in split_payload.get("splits", []):
        config = split_info["config"]
        split = split_info["split"]
        expected_rows = split_sizes.get((config, split), 0)
        receipt = {
            "dataset": dataset_id,
            "config": config,
            "split": split,
            "expected_rows": expected_rows,
            "downloaded_rows": 0,
            "complete": False,
        }
        if expected_rows <= 0:
            receipt["viewer_error"] = "Dataset Viewer reported zero rows."
            receipts.append(receipt)
            continue
        if expected_rows > max_viewer_rows:
            receipt["viewer_error"] = (
                f"Split has {expected_rows:,} rows; configured limit is "
                f"{max_viewer_rows:,}. Re-run with --max-viewer-rows to opt in."
            )
            receipts.append(receipt)
            continue

        # Prefer the repository's own JSON file when its row count matches the
        # published split size exactly. One request replaces expected_rows/100
        # rate-limited Viewer calls without weakening the completeness receipt.
        if prefer_source_files and metadata is not None:
            try:
                source_receipts = download_source_file_rows(
                    dataset_id,
                    dataset_dir,
                    metadata,
                    config=config,
                    split=split,
                    expected_rows=expected_rows,
                    consumed_files=consumed_files,
                )
            except RuntimeError:
                source_receipts = None
            if source_receipts:
                for item in source_receipts:
                    consumed_files.update(f["path"] for f in item.get("source_files", []))
                receipts.extend(source_receipts)
                continue

        output_name = f"{safe_slug(config)}__{safe_slug(split)}.jsonl"
        output_path = dataset_dir / "viewer_rows" / output_name
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8", newline="\n") as handle:
            for offset in range(0, expected_rows, 100):
                query = urllib.parse.urlencode(
                    {
                        "dataset": dataset_id,
                        "config": config,
                        "split": split,
                        "offset": offset,
                        "length": min(100, expected_rows - offset),
                    }
                )
                rows_payload = request_json(
                    f"https://datasets-server.huggingface.co/rows?{query}"
                )
                for item in rows_payload.get("rows", []):
                    row = item.get("row", item)
                    handle.write(json.dumps(row, ensure_ascii=False) + "\n")
                    receipt["downloaded_rows"] += 1

        receipt["source"] = "dataset_viewer"
        receipt["row_file"] = f"viewer_rows/{output_name}"
        receipt["complete"] = receipt["downloaded_rows"] == expected_rows
        if not receipt["complete"]:
            receipt["viewer_error"] = "Downloaded row count differs from Dataset Viewer size."
        receipts.append(receipt)

    if not receipts:
        receipts.append(
            {
                "dataset": dataset_id,
                "complete": False,
                "viewer_error": "Dataset Viewer returned no split definitions.",
            }
        )
    return receipts


def clear_row_files(dataset_dir: Path) -> None:
    """Remove previously written row files for one dataset before re-downloading.

    A dataset can switch between the Viewer, source-file, and raw-file paths
    between runs. Without this, an old snapshot from one path would sit beside a
    new snapshot from another and every row would be counted twice.
    """

    for folder in ("viewer_rows", "raw_rows"):
        directory = dataset_dir / folder
        if not directory.exists():
            continue
        for path in directory.glob("*.jsonl"):
            path.unlink()


def parse_parquet_rows(payload: bytes) -> list:
    """Read a Parquet file into plain Python rows.

    Arrow values are converted with ``to_pylist`` so the written JSONL matches
    what the Dataset Viewer would have served, keeping the two download paths
    interchangeable for the profiler.
    """

    if _parquet is None:
        raise ValueError("pyarrow is required to read Parquet sources; install requirements.txt")
    import io

    table = _parquet.read_table(io.BytesIO(payload))
    return table.to_pylist()


def parse_row_values(payload: bytes, relative_path: str = "") -> tuple[list, str]:
    """Parse a raw data file into rows without reshaping any value.

    Returns the parsed rows plus the layout that produced them. Bare JSON
    arrays are preserved as-is; normalizing them into records is the
    profiler's job, where the adapter is visible and testable.
    """

    if relative_path.lower().endswith(PARQUET_SUFFIXES):
        return parse_parquet_rows(payload), "parquet"

    text = payload.decode("utf-8")
    lines = [line for line in text.splitlines() if line.strip()]
    try:
        return [json.loads(line) for line in lines], "line_delimited"
    except json.JSONDecodeError:
        pass
    document = json.loads(text)
    if isinstance(document, list):
        return document, "json_array"
    raise ValueError("Raw file is neither line-delimited JSON nor a JSON array")


def split_matches_filename(split: str, relative_path: str) -> bool:
    """Return True when a data file is named for the given split.

    Recognises the Hugging Face shard convention ``<split>-00000-of-0000N`` and
    the plain ``<split>`` stem, matched case-insensitively on the basename only.
    """

    stem = relative_path.rsplit("/", 1)[-1]
    for suffix in SOURCE_SUFFIXES:
        if stem.lower().endswith(suffix):
            stem = stem[: -len(suffix)]
            break
    stem = stem.casefold()
    target = split.casefold()
    return stem == target or re.fullmatch(rf"{re.escape(target)}-\d+-of-\d+", stem) is not None


def download_source_file_rows(
    dataset_id: str,
    dataset_dir: Path,
    metadata: dict,
    *,
    config: str,
    split: str,
    expected_rows: int,
    consumed_files: set[str] | None = None,
) -> list[dict] | None:
    """Fetch a split from its JSON source file instead of paging the Dataset Viewer.

    The Viewer serves at most 100 rows per request, so a 34,000-row split costs
    343 rate-limited calls while the same rows sit in one downloadable file. This
    path is only taken when the parsed row count provably equals the row count
    the Viewer publishes for the split; otherwise it returns ``None`` and the
    caller pages the Viewer as before. It never guesses which file is the split.
    """

    revision = metadata.get("sha")
    if not revision or expected_rows <= 0:
        return None

    blob_metadata = request_json(
        f"https://huggingface.co/api/datasets/{urllib.parse.quote(dataset_id)}?blobs=true"
    )
    candidates = [
        sibling
        for sibling in blob_metadata.get("siblings", [])
        if str(sibling.get("rfilename", "")).lower().endswith(SOURCE_SUFFIXES)
        and sibling.get("rfilename") != "README.md"
        # One file cannot be two splits. Without this, a repository that ships an
        # unrelated 500-row helper file alongside 500-row splits would hand the
        # same rows to every split.
        and str(sibling.get("rfilename")) not in (consumed_files or set())
    ]
    if not candidates:
        return None

    # Auto-converted Parquet is named "<split>-00000-of-0000N.parquet". Splits can
    # hold identical row counts (a Turkish and English rendering of the same 800
    # rows), so the file must be chosen by name before any count comparison,
    # otherwise a split could silently receive the other split's rows.
    named_for_split = [
        sibling
        for sibling in candidates
        if split_matches_filename(split, str(sibling["rfilename"]))
    ]
    if named_for_split:
        candidates = named_for_split
    elif any(
        split_matches_filename(other, str(sibling["rfilename"]))
        for sibling in candidates
        for other in (split, "train", "test", "validation")
        if other != split
    ):
        # Other splits are name-encoded but this one is not; refuse to guess.
        return None

    downloaded: list[tuple[dict, list, str, bytes]] = []
    for sibling in candidates:
        relative_path = sibling["rfilename"]
        quoted = "/".join(urllib.parse.quote(part) for part in relative_path.split("/"))
        url = (
            f"https://huggingface.co/datasets/{dataset_id}/resolve/"
            f"{revision}/{quoted}?download=true"
        )
        try:
            payload = request_bytes(url)
            rows, layout = parse_row_values(payload, relative_path)
        except (RuntimeError, ValueError, json.JSONDecodeError, UnicodeDecodeError):
            continue
        expected_bytes = sibling.get("size")
        if expected_bytes is not None and len(payload) != expected_bytes:
            continue
        downloaded.append((sibling, rows, layout, payload))

    # Prefer a single file whose own row count equals the published split size.
    # Repositories often ship extra JSON (raw scrape sources, URL manifests) that
    # is not part of the split, so a single exact match is the safest signal.
    single = next((item for item in downloaded if len(item[1]) == expected_rows), None)
    if single is not None:
        selected = [single]
    elif downloaded and sum(len(item[1]) for item in downloaded) == expected_rows:
        # Some repositories store one split across several files, for example two
        # dataset versions the Viewer concatenates. Accepted only because the
        # summed count still matches the published size exactly.
        selected = downloaded
    else:
        return None

    rows = [row for item in selected for row in item[1]]
    output_path = dataset_dir / "viewer_rows" / f"{safe_slug(config)}__{safe_slug(split)}.jsonl"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    return [
        {
            "dataset": dataset_id,
            "config": config,
            "split": split,
            "source": "source_file",
            "source_files": [
                {
                    "path": item[0]["rfilename"],
                    "rows": len(item[1]),
                    "layout": item[2],
                    "expected_bytes": item[0].get("size"),
                    "downloaded_bytes": len(item[3]),
                    "expected_sha256": (item[0].get("lfs") or {}).get("sha256"),
                    "local_sha256": hashlib.sha256(item[3]).hexdigest(),
                }
                for item in selected
            ],
            "revision": revision,
            "expected_rows": expected_rows,
            "downloaded_rows": len(rows),
            "row_count_authority": (
                "Dataset Viewer published split size, matched exactly by the parsed "
                "source file(s) at the pinned revision"
            ),
            "row_file": f"viewer_rows/{output_path.name}",
            "complete": True,
        }
    ]


def download_raw_file_rows(dataset_id: str, dataset_dir: Path, metadata: dict) -> list[dict]:
    """Download revision-pinned raw data files when the Dataset Viewer cannot serve rows.

    Every receipt carries the repository revision, the expected blob size and
    checksum, and the locally recomputed values, so a partial or corrupted
    snapshot can never be mistaken for a complete one.
    """

    revision = metadata.get("sha")
    if not revision:
        return [{"dataset": dataset_id, "complete": False, "viewer_error": "Repository revision is unknown."}]

    blob_metadata = request_json(
        f"https://huggingface.co/api/datasets/{urllib.parse.quote(dataset_id)}?blobs=true"
    )
    candidates = [
        sibling
        for sibling in blob_metadata.get("siblings", [])
        if str(sibling.get("rfilename", "")).lower().endswith(SOURCE_SUFFIXES)
        and sibling.get("rfilename") != "README.md"
    ]
    if not candidates:
        supported = ", ".join(SOURCE_SUFFIXES)
        return [
            {
                "dataset": dataset_id,
                "complete": False,
                "viewer_error": (
                    "Dataset Viewer served no rows and the repository contains no raw data "
                    f"file in a supported fallback format ({supported})."
                ),
            }
        ]

    receipts: list[dict] = []
    for sibling in candidates:
        relative_path = sibling["rfilename"]
        expected_bytes = sibling.get("size")
        expected_sha256 = (sibling.get("lfs") or {}).get("sha256")
        quoted_path = "/".join(urllib.parse.quote(part) for part in relative_path.split("/"))
        url = (
            f"https://huggingface.co/datasets/{dataset_id}/resolve/"
            f"{revision}/{quoted_path}?download=true"
        )
        receipt = {
            "dataset": dataset_id,
            "config": "raw_files",
            "split": relative_path,
            "source": "raw_files",
            "revision": revision,
            "expected_bytes": expected_bytes,
            "expected_sha256": expected_sha256,
            "complete": False,
        }
        try:
            payload = request_bytes(url)
        except RuntimeError as error:
            receipt["viewer_error"] = f"Raw file download failed: {error}"
            receipts.append(receipt)
            continue

        receipt["downloaded_bytes"] = len(payload)
        receipt["local_sha256"] = hashlib.sha256(payload).hexdigest()
        size_matches = expected_bytes is None or len(payload) == expected_bytes
        digest_matches = expected_sha256 is None or receipt["local_sha256"] == expected_sha256
        if not size_matches:
            receipt["viewer_error"] = (
                f"Byte size differs: expected {expected_bytes}, downloaded {len(payload)}."
            )
            receipts.append(receipt)
            continue
        if not digest_matches:
            receipt["viewer_error"] = "SHA-256 checksum differs from the published blob digest."
            receipts.append(receipt)
            continue

        try:
            rows, layout = parse_row_values(payload, relative_path)
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError) as error:
            receipt["viewer_error"] = f"Raw file could not be parsed in full: {error}"
            receipts.append(receipt)
            continue

        output_path = dataset_dir / "raw_rows" / f"{safe_slug(relative_path)}.jsonl"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8", newline="\n") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")

        receipt.update(
            {
                "layout": layout,
                "expected_rows": len(rows),
                "downloaded_rows": len(rows),
                "row_count_authority": (
                    "parsed from the byte- and checksum-verified raw file; the Dataset "
                    "Viewer publishes no independent row count for this repository"
                ),
                "row_file": f"raw_rows/{output_path.name}",
                "complete": True,
            }
        )
        receipts.append(receipt)
    return receipts


def load_existing_inventory(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {item["dataset_id"]: item for item in payload}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="Dataset registry JSON")
    parser.add_argument(
        "--dataset",
        action="append",
        default=[],
        help="Download one owner/name ID; repeat to select multiple datasets",
    )
    parser.add_argument("--data-dir", default=str(DEFAULT_DATA_DIR), help="Local raw-data directory")
    parser.add_argument("--inventory", default=str(DEFAULT_INVENTORY), help="Inventory JSON output")
    parser.add_argument(
        "--max-viewer-rows",
        type=int,
        default=200_000,
        help="Maximum rows downloaded per split (default: 200000)",
    )
    parser.add_argument(
        "--download-repository-files",
        action="store_true",
        help="Download every repository file; by default only README.md is copied",
    )
    parser.add_argument("--fail-fast", action="store_true", help="Stop at the first failed dataset")
    parser.add_argument(
        "--viewer-rows-only",
        action="store_true",
        help=(
            "Always page the Dataset Viewer instead of preferring a matching JSON "
            "source file; useful for cross-checking the two paths against each other"
        ),
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help=(
            "Skip datasets whose recorded snapshot is complete and still matches the "
            "current remote revision; the revision is always re-checked"
        ),
    )
    return parser.parse_args()


def snapshot_is_current(dataset_id: str, item: dict | None, dataset_dir: Path) -> bool:
    """Return True when a recorded snapshot is complete and still on the live revision."""

    if not item or item.get("download_error") or not item.get("sha"):
        return False
    receipts = item.get("viewer_receipts") or []
    if not receipts or any(not receipt.get("complete") for receipt in receipts):
        return False
    metadata_path = dataset_dir / "metadata.json"
    if not metadata_path.exists():
        return False
    row_files = list((dataset_dir / "viewer_rows").glob("*.jsonl")) + list(
        (dataset_dir / "raw_rows").glob("*.jsonl")
    )
    if not row_files:
        return False
    try:
        remote = request_json(f"https://huggingface.co/api/datasets/{dataset_id}")
    except RuntimeError:
        return False
    return remote.get("sha") == item.get("sha")


def main() -> int:
    args = parse_args()
    config_path = resolve_path(args.config)
    data_dir = resolve_path(args.data_dir)
    inventory_path = resolve_path(args.inventory)
    entries = load_dataset_entries(config_path, args.dataset)
    inventory_by_id = load_existing_inventory(inventory_path)
    failures: list[str] = []

    data_dir.mkdir(parents=True, exist_ok=True)
    blocked: list[str] = []
    for entry in entries:
        dataset_id = entry["dataset_id"]
        dataset_dir = data_dir / safe_slug(dataset_id)

        if entry.get("access_block"):
            block = verify_access_block(dataset_id, entry["access_block"])
            inventory_by_id[dataset_id] = {
                "dataset_id": dataset_id,
                "contributor": entry.get("contributor"),
                "contributor_source": entry.get("contributor_source"),
                "access_block": block,
            }
            if block["still_blocked"]:
                blocked.append(dataset_id)
                print(f"BLOCKED {dataset_id}: {block['status']} (declared and re-verified)")
            else:
                failures.append(dataset_id)
                print(
                    f"BLOCK CLEARED {dataset_id}: the declared access block no longer applies; "
                    "remove access_block from config/datasets.json and re-run.",
                    file=sys.stderr,
                )
            continue

        if args.resume and snapshot_is_current(dataset_id, inventory_by_id.get(dataset_id), dataset_dir):
            recorded = inventory_by_id[dataset_id]
            recorded["contributor"] = entry.get("contributor")
            recorded["contributor_source"] = entry.get("contributor_source")
            rows = sum(receipt.get("downloaded_rows", 0) for receipt in recorded["viewer_receipts"])
            print(f"Up to date {dataset_id}: {rows:,} rows at revision {recorded['sha'][:8]}")
            continue

        try:
            metadata = request_json(f"https://huggingface.co/api/datasets/{dataset_id}")
            write_json(dataset_dir / "metadata.json", metadata)
            clear_row_files(dataset_dir)
            downloaded_files = download_repository_files(
                dataset_id,
                dataset_dir,
                metadata,
                download_all=args.download_repository_files,
            )
            viewer_receipts = download_viewer_rows(
                dataset_id,
                dataset_dir,
                max_viewer_rows=args.max_viewer_rows,
                metadata=metadata,
                prefer_source_files=not args.viewer_rows_only,
            )
            if all(not receipt.get("complete") for receipt in viewer_receipts):
                # The Viewer cannot serve this repository. Fall back to the
                # revision-pinned raw files rather than dropping the dataset.
                fallback_receipts = download_raw_file_rows(dataset_id, dataset_dir, metadata)
                if any(receipt.get("complete") for receipt in fallback_receipts):
                    viewer_receipts = fallback_receipts
                else:
                    viewer_receipts = viewer_receipts + fallback_receipts
            inventory_by_id[dataset_id] = {
                "dataset_id": dataset_id,
                "contributor": entry.get("contributor"),
                "contributor_source": entry.get("contributor_source"),
                "sha": metadata.get("sha"),
                "created_at": metadata.get("createdAt"),
                "last_modified": metadata.get("lastModified"),
                "downloads": metadata.get("downloads"),
                "likes": metadata.get("likes"),
                "used_storage": metadata.get("usedStorage"),
                "license": (metadata.get("cardData") or {}).get("license"),
                "private": metadata.get("private"),
                "gated": metadata.get("gated"),
                "files": [item.get("rfilename") for item in metadata.get("siblings", [])],
                "downloaded_repository_files": downloaded_files,
                "viewer_receipts": viewer_receipts,
            }
            incomplete = [receipt for receipt in viewer_receipts if not receipt.get("complete")]
            if incomplete:
                failures.append(dataset_id)
                print(f"INCOMPLETE {dataset_id}: {incomplete[0].get('viewer_error')}", file=sys.stderr)
            else:
                row_count = sum(receipt["downloaded_rows"] for receipt in viewer_receipts)
                via = viewer_receipts[0].get("source", "dataset_viewer")
                print(f"Downloaded {dataset_id}: {row_count:,} rows via {via}")
        except Exception as error:  # Keep the remaining dataset batch auditable.
            failures.append(dataset_id)
            inventory_by_id[dataset_id] = {
                "dataset_id": dataset_id,
                "contributor": entry.get("contributor"),
                "contributor_source": entry.get("contributor_source"),
                "download_error": str(error),
            }
            print(f"FAILED {dataset_id}: {error}", file=sys.stderr)
            if args.fail_fast:
                break

    preferred_order = [entry["dataset_id"] for entry in entries]
    ordered_ids = preferred_order + sorted(set(inventory_by_id) - set(preferred_order))
    write_json(inventory_path, [inventory_by_id[dataset_id] for dataset_id in ordered_ids])
    print(f"Inventory: {inventory_path}")
    if blocked:
        print(f"Declared and re-verified access blocks: {len(set(blocked))}")
    if failures:
        print(f"Datasets requiring attention: {len(set(failures))}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
