"""Run read-only integrity checks for the public analysis repository."""

from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = {
    "README.md",
    "AGENTS.md",
    "config/datasets.json",
    "config/verified_baseline.json",
    "config/evaluation_criteria.json",
    "outputs/topic_overlap.json",
    "outputs/source_inventory.json",
    "outputs/data_quality_profiles.json",
    "outputs/cross_dataset_overlap.json",
    "outputs/manual_findings.json",
    "outputs/excluded_datasets.json",
    "appendix/dataset_manifest.json",
    "appendix/capability_mapping.csv",
    "appendix/topic_profile.csv",
    "appendix/provenance.csv",
    "feedback/README.md",
    "reports/dataset-technical-assessment.md",
    "reports/model-capability-mapping.md",
    "reports/file-guide.md",
    "reports/figures/README.md",
    "scripts/download_hf_datasets.py",
    "scripts/profile_datasets.py",
    "scripts/build_notebook.py",
    "scripts/generate_report_charts.py",
    "scripts/validate_repository.py",
}

MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")

# Every require() call is one recorded check, so the report can state how many
# assertions actually ran instead of quoting a number from an earlier scope.
CHECKS_RUN = Counter()


class ValidationError(RuntimeError):
    """Raised when a repository integrity check fails."""


def load_json(relative_path: str):
    path = ROOT / relative_path
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"Cannot parse {relative_path}: {exc}") from exc


def require(condition: bool, message: str) -> None:
    CHECKS_RUN["total"] += 1
    if not condition:
        raise ValidationError(message)


def safe_slug(dataset_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "__", dataset_id)


def enabled_dataset_ids(registry: dict) -> list[str]:
    dataset_ids = [
        str(entry.get("dataset_id", "")).strip()
        for entry in registry.get("datasets", [])
        if entry.get("enabled", True)
    ]
    require(all(dataset_id.count("/") == 1 for dataset_id in dataset_ids), "Invalid dataset ID in registry")
    require(len(dataset_ids) == len(set(dataset_ids)), "Duplicate dataset ID in registry")
    require(dataset_ids, "No enabled datasets in registry")
    return dataset_ids


def nested_value(payload: dict, dotted_path: str):
    value: object = payload
    for part in dotted_path.split("."):
        if not isinstance(value, dict) or part not in value:
            raise ValidationError(f"Missing profile field: {dotted_path}")
        value = value[part]
    return value


def check_required_files(baseline: dict) -> None:
    missing = sorted(path for path in REQUIRED_FILES if not (ROOT / path).is_file())
    require(not missing, f"Missing required files: {', '.join(missing)}")

    required_figures = set(baseline.get("figures", []))
    require(required_figures, "Verified baseline has no required figures")
    figure_dir = ROOT / "reports" / "figures"
    present_figures = {path.name for path in figure_dir.glob("*.png")}
    require(
        present_figures == required_figures,
        "Figure set differs from verified baseline: "
        f"expected={sorted(required_figures)}, present={sorted(present_figures)}",
    )
    for name in required_figures:
        path = figure_dir / name
        require(path.stat().st_size > 1_000, f"Figure appears empty: {path.relative_to(ROOT)}")
        require(path.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n", f"Invalid PNG signature: {name}")


def check_evidence(baseline: dict, registry: dict) -> None:
    profiles = load_json("outputs/data_quality_profiles.json")
    overlaps = load_json("outputs/cross_dataset_overlap.json")
    inventory = load_json("outputs/source_inventory.json")
    manual = load_json("outputs/manual_findings.json")
    excluded_payload = load_json("outputs/excluded_datasets.json")
    manifest = load_json("appendix/dataset_manifest.json")

    dataset_ids = enabled_dataset_ids(registry)
    profile_ids = [item.get("dataset_id") for item in profiles]
    inventory_ids = [item.get("dataset_id") for item in inventory]
    excluded = excluded_payload.get("datasets", [])
    excluded_ids = [item.get("dataset_id") for item in excluded]

    require(len(profile_ids) == len(set(profile_ids)), "Duplicate dataset profile found")
    require(len(inventory_ids) == len(set(inventory_ids)), "Duplicate inventory entry found")
    require(len(excluded_ids) == len(set(excluded_ids)), "Duplicate excluded-dataset entry found")
    require(
        not (set(profile_ids) & set(excluded_ids)),
        "A dataset is recorded both as profiled and as access-blocked",
    )
    # Enabled registry scope must be fully accounted for: every dataset is
    # either analyzed or carries a recorded, evidenced access block.
    require(
        set(profile_ids) | set(excluded_ids) == set(dataset_ids),
        "Registry scope is not fully accounted for by profiles plus recorded access blocks: "
        f"missing={sorted(set(dataset_ids) - set(profile_ids) - set(excluded_ids))}, "
        f"unexpected={sorted(set(profile_ids) | set(excluded_ids) - set(dataset_ids))}",
    )
    require(set(inventory_ids) == set(dataset_ids), "Inventory scope differs from config/datasets.json")
    require(len(profiles) == baseline["dataset_count"], "Dataset count differs from verified baseline")
    require(
        len(excluded) == baseline.get("excluded_dataset_count", 0),
        "Access-block count differs from verified baseline",
    )
    require(
        sum(item["profile"]["row_count"] for item in profiles) == baseline["total_rows"],
        "Total row count differs from verified baseline",
    )

    registry_blocks = {
        entry["dataset_id"]: entry["access_block"]
        for entry in registry.get("datasets", [])
        if entry.get("access_block")
    }
    require(
        set(registry_blocks) == set(excluded_ids),
        "Registry access blocks differ from outputs/excluded_datasets.json",
    )
    for item in excluded:
        label = item.get("dataset_id")
        for field in ("status", "evidence", "declared_on", "reverified_on"):
            require(
                bool(item.get(field)),
                f"Access block for {label} is missing its {field} record",
            )
        require(
            any(check.get("status") != 200 for check in item.get("reverified_checks", [])),
            f"Access block for {label} carries no failing HTTP re-verification",
        )

    # Every response dataset must carry the full metric set. Without this a
    # newly added dataset could silently skip a metric and still validate.
    required_response_fields = (
        "user_prompt_duplicates", "assistant_answer_duplicates",
        "user_prompt_near_duplicates", "assistant_answer_near_duplicates",
        "answer_families", "structured_answers", "distinct_canonical_rows",
    )
    for item in profiles:
        profile = item["profile"]
        require(
            "distinct_canonical_rows" in profile,
            f"{item['dataset_id']} is missing distinct_canonical_rows",
        )
        if profile["data_shape"] not in {"conversation", "instruction_pair"}:
            continue
        for field in required_response_fields:
            require(field in profile, f"{item['dataset_id']} is missing profile field {field}")
        for side in ("user_prompt_near_duplicates", "assistant_answer_near_duplicates"):
            near = profile[side]
            require(
                near.get("threshold") is not None and near.get("method"),
                f"{item['dataset_id']} {side} does not record its threshold and method",
            )
        require(
            profile["assistant_answer_duplicates"].get("distinct_values") is not None,
            f"{item['dataset_id']} does not record distinct answer values",
        )
        require(
            profile.get("text_scan", {}).get("dominant_language_signal") is not None,
            f"{item['dataset_id']} does not record a language signal",
        )

    # Every analyzed dataset must have a reviewed qualitative entry; a computed
    # profile is evidence, not a substitute for reading the data.
    reviewed = set(manual.get("datasets", {}))
    require(
        set(profile_ids) <= reviewed,
        f"manual_findings.json is missing reviewed entries for: {sorted(set(profile_ids) - reviewed)}",
    )
    require(
        reviewed <= set(profile_ids) | set(excluded_ids),
        f"manual_findings.json reviews datasets that are not in scope: {sorted(reviewed - set(profile_ids) - set(excluded_ids))}",
    )

    shape_counts = Counter(item["profile"]["data_shape"] for item in profiles)
    shape_rows = Counter()
    for item in profiles:
        shape_rows[item["profile"]["data_shape"]] += item["profile"]["row_count"]
    require(dict(shape_counts) == baseline["shape_counts"], "Schema counts differ from verified baseline")
    require(dict(shape_rows) == baseline["shape_rows"], "Schema row totals differ from verified baseline")

    for field, expected in baseline.get("quality_totals", {}).items():
        actual = sum(item["profile"].get(field, 0) for item in profiles)
        require(actual == expected, f"Unexpected aggregate {field}: expected={expected}, actual={actual}")

    profile_by_id = {item["dataset_id"]: item["profile"] for item in profiles}
    for dataset_id, metrics in baseline.get("dataset_metrics", {}).items():
        require(dataset_id in profile_by_id, f"Baseline dataset is missing: {dataset_id}")
        for dotted_path, expected in metrics.items():
            actual = nested_value(profile_by_id[dataset_id], dotted_path)
            require(
                actual == expected,
                f"Unexpected {dataset_id} {dotted_path}: expected={expected}, actual={actual}",
            )

    # Near-duplicate totals are baseline-locked because they depend on tie
    # ordering inside the profiler; a silent drift here would mean the profile
    # stopped being reproducible.
    near_baseline = baseline["near_duplicates"]
    actual_near = {
        "answer_rows": sum(
            item["profile"].get("assistant_answer_near_duplicates", {}).get("near_duplicate_rows", 0)
            for item in profiles
        ),
        "prompt_rows": sum(
            item["profile"].get("user_prompt_near_duplicates", {}).get("near_duplicate_rows", 0)
            for item in profiles
        ),
    }
    for field, value in actual_near.items():
        require(
            near_baseline[field] == value,
            f"Near-duplicate {field} differs from baseline: expected={near_baseline[field]}, actual={value}",
        )
    for item in profiles:
        if item["profile"]["data_shape"] not in {"conversation", "instruction_pair"}:
            continue
        require(
            item["profile"]["assistant_answer_near_duplicates"]["threshold"] == near_baseline["threshold"],
            f"{item['dataset_id']} uses a different near-duplicate threshold than the baseline",
        )

    # Thresholds must exist in exactly one place. If a figure or a report quotes a
    # number the criteria file does not define, they have already drifted.
    criteria = load_json("config/evaluation_criteria.json")
    dimensions = {d["id"]: d for d in criteria["dimensions"]}
    for required in ("structural_integrity", "content_distinctness", "topic_coverage",
                     "provenance_and_rights", "privacy_and_register", "task_fitness",
                     "documentation_adequacy"):
        require(required in dimensions, f"Evaluation criteria is missing the {required} dimension")
        entry = dimensions[required]
        require(
            bool(entry.get("does_not_tell_you")),
            f"Criteria dimension {required} does not state its limits",
        )
    require(
        dimensions["content_distinctness"]["detection_parameters"]["near_duplicate_jaccard"]
        == near_baseline["threshold"],
        "Near-duplicate Jaccard threshold in the criteria file does not match the baseline",
    )

    topic_payload = load_json("outputs/topic_overlap.json")
    topic_pairs = topic_payload.get("pairs", [])
    require(topic_pairs, "Topic overlap file records no pairs")
    require(
        all(pair["cosine"] >= 0 and pair["left"] < pair["right"] for pair in topic_pairs),
        "Topic overlap pairs are malformed or unordered",
    )
    profiled = {item["dataset_id"] for item in profiles}
    for pair in topic_pairs:
        require(
            pair["left"] in profiled and pair["right"] in profiled,
            f"Topic overlap references an unprofiled dataset: {pair['left']} / {pair['right']}",
        )
    for item in profiles:
        topic = item["profile"].get("topic_profile")
        require(topic is not None, f"{item['dataset_id']} has no topic_profile")
        if topic.get("analyzable"):
            require(
                topic["distinctive_terms"],
                f"{item['dataset_id']} is marked analyzable but lists no distinctive terms",
            )
            require(
                topic.get("topic_concentration") is not None,
                f"{item['dataset_id']} records no topic concentration",
            )
        else:
            require(
                bool(topic.get("reason")),
                f"{item['dataset_id']} topic analysis was skipped without stating why",
            )
        require(
            "pii_evidence" in item["profile"],
            f"{item['dataset_id']} carries no PII evidence block",
        )

    language_counts = Counter(
        item["profile"].get("text_scan", {}).get("dominant_language_signal") for item in profiles
    )
    require(
        dict(sorted(language_counts.items())) == baseline["language_signal_counts"],
        f"Language signal counts differ from baseline: {dict(sorted(language_counts.items()))}",
    )

    overlap_baseline = baseline["overlap"]
    require(len(overlaps) == overlap_baseline["pair_count"], "Overlap pair count differs from baseline")
    require(
        sum(item.get("shared_user_prompts", 0) for item in overlaps)
        == overlap_baseline["shared_user_prompts"],
        "Shared prompt count differs from baseline",
    )
    require(
        sum(item.get("shared_assistant_answers", 0) for item in overlaps)
        == overlap_baseline["shared_assistant_answers"],
        "Shared answer count differs from baseline",
    )
    require(
        len(manifest.get("capabilities", [])) == baseline["capability_count"],
        "Capability count differs from baseline",
    )

    # Capability mappings may only reference datasets that exist in the registry
    # and were actually profiled, and their row counts must match the profiles.
    profile_rows = {item["dataset_id"]: item["profile"]["row_count"] for item in profiles}

    manifest_references = [
        (capability["capability"], level, entry)
        for capability in manifest.get("capabilities", [])
        for level in ("direct_datasets", "partial_datasets", "conversion_sources")
        for entry in capability.get(level, [])
    ]
    require(manifest_references, "Capability manifest references no datasets")
    for capability, level, entry in manifest_references:
        dataset_id = entry.get("dataset")
        require(
            dataset_id in profile_rows,
            f"Manifest {capability}/{level} references an unprofiled dataset: {dataset_id}",
        )
        require(
            entry.get("rows") == profile_rows[dataset_id],
            f"Manifest row count for {dataset_id} in {capability}/{level} is "
            f"{entry.get('rows')}, but the profile reports {profile_rows[dataset_id]}",
        )

    # The reference appendices must cover exactly the profiled scope: a dataset
    # missing from them is a dataset the report silently stops describing.
    for name in ("topic_profile.csv", "provenance.csv"):
        with (ROOT / "appendix" / name).open(encoding="utf-8-sig", newline="") as handle:
            appendix_rows = list(csv.DictReader(handle))
        listed = [row["dataset"] for row in appendix_rows]
        require(len(listed) == len(set(listed)), f"appendix/{name} has duplicate rows")
        require(
            set(listed) == set(profile_rows),
            f"appendix/{name} scope differs from the profiles: "
            f"missing={sorted(set(profile_rows) - set(listed))}, "
            f"extra={sorted(set(listed) - set(profile_rows))}",
        )

    # One feedback page per contributor, covering every registry dataset. A
    # contributor silently losing their page is a delivery failure, not a detail.
    contributors = {entry["contributor"] for entry in registry.get("datasets", [])}
    feedback_dir = ROOT / "feedback"
    pages = {path.stem for path in feedback_dir.glob("*.md")} - {"README"}
    require(
        len(pages) == len(contributors),
        f"feedback pages ({len(pages)}) do not match contributors ({len(contributors)})",
    )
    covered = " ".join(
        path.read_text(encoding="utf-8") for path in feedback_dir.glob("*.md")
    )
    for dataset_id in enabled_dataset_ids(registry):
        require(
            dataset_id in covered,
            f"No contributor feedback page mentions {dataset_id}",
        )

    # The README dataset tables carry one feedback link per dataset. Checking the
    # count catches a row added without its link, which a broken-link check
    # cannot see because the missing link is not there to be broken.
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    feedback_links = re.findall(r"\[Feedback\]\(feedback/([^)]+)\.md\)", readme)
    require(
        len(feedback_links) == len(registry.get("datasets", [])),
        f"README has {len(feedback_links)} feedback links for "
        f"{len(registry.get('datasets', []))} registry datasets",
    )
    require(
        set(feedback_links) == pages,
        "README feedback links do not cover exactly the generated pages: "
        f"missing={sorted(pages - set(feedback_links))}, "
        f"unknown={sorted(set(feedback_links) - pages)}",
    )

    csv_path = ROOT / "appendix" / "capability_mapping.csv"
    with csv_path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    require(rows, "Capability mapping CSV is empty")
    valid_capabilities = {capability["capability"] for capability in manifest.get("capabilities", [])}
    for index, row in enumerate(rows, start=2):
        dataset_id = (row.get("dataset") or "").strip()
        require(
            dataset_id in profile_rows,
            f"capability_mapping.csv line {index} references an unprofiled dataset: {dataset_id!r}",
        )
        require(
            (row.get("capability") or "").strip() in valid_capabilities,
            f"capability_mapping.csv line {index} uses an unknown capability: {row.get('capability')!r}",
        )
        require(
            (row.get("row_count") or "").strip().replace(",", "") == str(profile_rows[dataset_id]),
            f"capability_mapping.csv line {index} row_count is {row.get('row_count')!r}, "
            f"but the profile reports {profile_rows[dataset_id]}",
        )


def check_local_snapshots(registry: dict) -> None:
    data_dir = ROOT / "data"
    if not data_dir.exists():
        return

    inventory = load_json("outputs/source_inventory.json")
    inventory_by_id = {item["dataset_id"]: item for item in inventory}
    for dataset_id in enabled_dataset_ids(registry):
        require(dataset_id in inventory_by_id, f"Local inventory is missing {dataset_id}")
        item = inventory_by_id[dataset_id]
        if item.get("access_block"):
            require(
                item["access_block"].get("still_blocked") is True,
                f"Access block for {dataset_id} was not re-verified during the last download",
            )
            continue
        receipts = item.get("viewer_receipts", [])
        require(receipts and all(receipt.get("complete") for receipt in receipts), f"Incomplete snapshot: {dataset_id}")

        dataset_dir = data_dir / safe_slug(dataset_id)
        metadata_path = dataset_dir / "metadata.json"
        require(metadata_path.is_file(), f"Missing local metadata: {dataset_id}")
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        require(metadata.get("sha") == item.get("sha"), f"Revision mismatch: {dataset_id}")

        row_files = sorted((dataset_dir / "viewer_rows").glob("*.jsonl")) + sorted(
            (dataset_dir / "raw_rows").glob("*.jsonl")
        )
        require(row_files, f"Missing local snapshot rows: {dataset_id}")
        local_rows = sum(
            sum(1 for line in path.open(encoding="utf-8") if line.strip())
            for path in row_files
        )
        expected_rows = sum(receipt.get("downloaded_rows", 0) for receipt in receipts)
        require(local_rows == expected_rows, f"Local row count mismatch: {dataset_id}")


def check_raw_data_untracked() -> None:
    """Raw snapshots and local private files must never enter Git history."""

    try:
        result = subprocess.run(
            ["git", "-c", f"safe.directory={ROOT.as_posix()}", "ls-files", "--", "data", ".venv"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise ValidationError(f"Cannot query Git for tracked raw data: {exc}") from exc
    require(result.returncode == 0, f"git ls-files failed: {result.stderr.strip()}")
    tracked = [line for line in result.stdout.splitlines() if line.strip()]
    require(not tracked, f"Raw data or environment files are tracked by Git: {tracked[:10]}")


def check_notebook(baseline: dict) -> None:
    notebook = load_json("notebook/huggingface_dataset_quality_analysis.ipynb")
    cells = notebook.get("cells", [])
    code_cells = [cell for cell in cells if cell.get("cell_type") == "code"]
    errors = [
        output
        for cell in code_cells
        for output in cell.get("outputs", [])
        if output.get("output_type") == "error"
    ]
    expected = baseline["notebook"]
    require(len(cells) == expected["cell_count"], f"Unexpected notebook cell count: {len(cells)}")
    require(
        len(code_cells) == expected["code_cell_count"],
        f"Unexpected notebook code-cell count: {len(code_cells)}",
    )
    require(not errors, f"Notebook contains {len(errors)} error outputs")
    require(all(cell.get("execution_count") is not None for cell in code_cells), "Notebook has unexecuted code cells")

    notebook_path = ROOT / "notebook" / "huggingface_dataset_quality_analysis.ipynb"
    html_path = ROOT / "notebook" / "huggingface_dataset_quality_analysis.html"
    require(html_path.is_file() and html_path.stat().st_size > 100_000, "Notebook HTML is missing or unexpectedly small")
    require(
        html_path.stat().st_mtime >= notebook_path.stat().st_mtime,
        "Notebook HTML is older than the notebook; regenerate it with nbconvert",
    )


HEADING = re.compile(r"^#{1,6}\s+(.*)$", re.MULTILINE)


def heading_slugs(path: Path) -> set[str]:
    """Return the anchor slugs a Markdown file exposes, GitHub-style."""

    slugs = set()
    for title in HEADING.findall(path.read_text(encoding="utf-8")):
        text = re.sub(r"[`*_\[\]()]", "", title.lower())
        text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
        slugs.add(re.sub(r"\s+", "-", text.strip()))
    return slugs


def check_markdown_links() -> None:
    failures: list[str] = []
    anchor_failures: list[str] = []
    slug_cache: dict[Path, set[str]] = {}
    excluded_roots = {"data", ".git", ".venv"}
    for markdown_path in sorted(ROOT.rglob("*.md")):
        relative = markdown_path.relative_to(ROOT)
        if relative.parts and relative.parts[0] in excluded_roots:
            continue
        text = markdown_path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK.finditer(text):
            target = match.group(1).strip().strip("<>")
            parsed = urlparse(target)
            if parsed.scheme or target.startswith(("#", "mailto:")):
                continue
            relative_target = unquote(target.split("#", 1)[0])
            if not relative_target:
                continue
            resolved = (markdown_path.parent / relative_target).resolve()
            if not resolved.exists():
                failures.append(f"{relative} -> {target}")
                continue
            # A link to a heading that no longer exists still resolves as a file,
            # so the fragment has to be checked separately or a cross-reference
            # rots silently as soon as a section is renamed.
            _, _, anchor = target.partition("#")
            if not anchor or not resolved.is_file():
                continue
            if resolved not in slug_cache:
                slug_cache[resolved] = heading_slugs(resolved)
            if anchor not in slug_cache[resolved]:
                anchor_failures.append(f"{relative} -> {target}")
    require(not failures, "Broken local Markdown links:\n  " + "\n  ".join(failures))
    require(
        not anchor_failures,
        "Markdown links pointing at a missing heading:\n  " + "\n  ".join(anchor_failures),
    )


def main() -> int:
    try:
        baseline = load_json("config/verified_baseline.json")
        registry = load_json("config/datasets.json")
        checks = [
            ("required files and figures", lambda: check_required_files(baseline)),
            ("JSON and CSV evidence", lambda: check_evidence(baseline, registry)),
            ("local snapshots when present", lambda: check_local_snapshots(registry)),
            ("raw data untracked by Git", check_raw_data_untracked),
            ("executed notebook and HTML", lambda: check_notebook(baseline)),
            ("local Markdown links", check_markdown_links),
        ]
        for label, check in checks:
            before = CHECKS_RUN["total"]
            check()
            ran = CHECKS_RUN["total"] - before
            print(f"PASS: {label} ({ran} check{'' if ran == 1 else 's'})")
    except ValidationError as exc:
        print(f"FAIL after {CHECKS_RUN['total']} checks: {exc}", file=sys.stderr)
        return 1
    total = CHECKS_RUN["total"]
    print(f"Repository validation passed: {total}/{total} checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
