"""Generate the six static PNG figures embedded in the Markdown reports."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, PercentFormatter


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "reports" / "figures"

INK = "#142B44"
MUTED = "#64748B"
GRID = "#DCE3EA"
BACKGROUND = "#F7F9FC"
BLUE = "#2563EB"
GOLD = "#C58217"
OLIVE = "#738437"
CORAL = "#D9685B"
PALE_BLUE = "#DCE8FF"
PALE_GOLD = "#F3E7CF"
PALE_OLIVE = "#E6EBD8"

plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Arial"],
        "font.size": 10.5,
        "axes.labelcolor": MUTED,
        "xtick.color": MUTED,
        "ytick.color": INK,
        "text.color": INK,
        "axes.titlecolor": INK,
        "figure.facecolor": BACKGROUND,
        "axes.facecolor": BACKGROUND,
        "savefig.facecolor": BACKGROUND,
    }
)

DISPLAY_NAMES = {
    "aliFurkan123/cultural-questions-dataset": "Cultural and general knowledge",
    "Aysenur44/namaz-vakti-identity-tr": "NamazAsistan identity",
    "Egertekin/marvel-domain-dataset": "Marvel",
    "gururaser/ithaki-bilimkurgu-klasikleri": "Ithaki catalog",
    "Mer1Alii/TR-ECommerce-CustomerSupport-Instructions": "E-commerce support",
    "namruni/meb-ogretmen-soru-cevap": "MEB teacher Q&A",
    "nyzmemre/biyoloji-terimleri-turkce-sa": "Biology terms",
    "sk75/sahin_identity": "Şahin identity",
    "yoitsmeyusuf/felsefe_finetune": "Philosophy",
}

CAPABILITY_DISPLAY_NAMES = {
    "Identity": "Identity",
    "Tool Call": "Tool Calling",
    "Conversation": "Conversation",
    "Instruction": "Instruction\nFollowing",
    "Structured Output": "Structured\nOutput",
    "Math": "Math",
    "Coding": "Coding",
}


def load_json(relative_path: str):
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def format_number(value: float, decimals: int = 0) -> str:
    return f"{value:,.{decimals}f}"


def add_header(fig: plt.Figure, title: str, subtitle: str) -> None:
    fig.text(0.04, 0.955, title, fontsize=19, fontweight="bold", ha="left", va="top", color=INK)
    fig.text(0.04, 0.905, subtitle, fontsize=10.5, ha="left", va="top", color=MUTED)


def add_source(fig: plt.Figure, source: str) -> None:
    fig.text(0.04, 0.022, f"Source: {source}", fontsize=8.5, ha="left", va="bottom", color=MUTED)


def clean_axis(ax: plt.Axes, *, vertical_grid: bool = True) -> None:
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis="both", length=0)
    if vertical_grid:
        ax.grid(axis="x", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)


def save(fig: plt.Figure, name: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_DIR / name, dpi=180, bbox_inches="tight", pad_inches=0.22)
    plt.close(fig)


def dataset_size_chart(profiles: list[dict]) -> None:
    rows = sorted(
        [(DISPLAY_NAMES[item["dataset_id"]], int(item["profile"]["row_count"])) for item in profiles],
        key=lambda item: item[1],
        reverse=True,
    )
    labels, values = zip(*rows)
    fig, ax = plt.subplots(figsize=(12, 7.4))
    fig.subplots_adjust(left=0.31, right=0.95, top=0.82, bottom=0.10)
    add_header(fig, "Dataset volumes", "3,119 rows in total across nine fixed dataset snapshots")
    add_source(fig, "outputs/data_quality_profiles.json")

    positions = range(len(rows))
    ax.barh(positions, values, height=0.56, color=BLUE, zorder=3)
    ax.set_yticks(list(positions), labels)
    ax.invert_yaxis()
    ax.set_xlim(0, max(values) * 1.16)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: format_number(x)))
    ax.set_xlabel("Row count", labelpad=12)
    clean_axis(ax)
    for y, value in enumerate(values):
        ax.text(value + max(values) * 0.018, y, format_number(value), va="center", fontweight="bold")
    save(fig, "dataset-row-counts.png")


def duplicate_rate_chart(profiles: list[dict]) -> None:
    rows = []
    for item in profiles:
        profile = item["profile"]
        if profile["data_shape"] != "conversation":
            continue
        prompt_rate = 100 * profile.get("user_prompt_duplicates", {}).get("duplicate_rate", 0)
        answer_rate = 100 * profile.get("assistant_answer_duplicates", {}).get("duplicate_rate", 0)
        rows.append((DISPLAY_NAMES[item["dataset_id"]], prompt_rate, answer_rate))
    rows.sort(key=lambda item: max(item[1], item[2]), reverse=True)

    fig, ax = plt.subplots(figsize=(12, 7.7))
    fig.subplots_adjust(left=0.31, right=0.95, top=0.79, bottom=0.11)
    add_header(
        fig,
        "Normalized duplicate density",
        "Rate = extra copies after the first occurrence / all rows; case and punctuation differences are ignored",
    )
    add_source(fig, "outputs/data_quality_profiles.json")

    for y, (label, prompt, answer) in enumerate(rows):
        ax.plot([prompt, answer], [y, y], color=GRID, linewidth=3, solid_capstyle="round", zorder=1)
        ax.scatter(prompt, y, s=82, color=BLUE, edgecolor=BACKGROUND, linewidth=1.4, zorder=3)
        ax.scatter(answer, y, s=82, color=GOLD, edgecolor=BACKGROUND, linewidth=1.4, zorder=3)
        if prompt == 0 and answer == 0:
            ax.text(1.2, y, "0%", va="center", color=MUTED, fontsize=9)
        else:
            if prompt > 0:
                ax.text(prompt, y - 0.23, f"{prompt:.2f}%", ha="center", va="bottom", color=BLUE, fontsize=8.5)
            if answer > 0:
                ax.text(answer, y + 0.23, f"{answer:.2f}%", ha="center", va="top", color=GOLD, fontsize=8.5)

    ax.set_yticks(range(len(rows)), [row[0] for row in rows])
    ax.invert_yaxis()
    ax.set_xlim(-1, 84)
    ax.xaxis.set_major_formatter(PercentFormatter(100, decimals=0))
    ax.set_xlabel("Extra-copy rate", labelpad=12)
    ax.legend(
        handles=[
            Line2D([0], [0], marker="o", color="none", markerfacecolor=BLUE, markeredgecolor=BLUE, markersize=7, label="User prompt"),
            Line2D([0], [0], marker="o", color="none", markerfacecolor=GOLD, markeredgecolor=GOLD, markersize=7, label="Assistant answer"),
        ],
        loc="upper right",
        bbox_to_anchor=(1, 1.10),
        frameon=False,
        ncol=2,
    )
    clean_axis(ax)
    save(fig, "duplicate-rates.png")


def response_length_chart(profiles: list[dict]) -> None:
    rows = []
    for item in profiles:
        profile = item["profile"]
        if profile["data_shape"] != "conversation":
            continue
        lengths = profile["assistant_word_length"]
        rows.append((DISPLAY_NAMES[item["dataset_id"]], float(lengths["median"]), float(lengths["p95"])))
    rows.sort(key=lambda item: item[2], reverse=True)

    fig, ax = plt.subplots(figsize=(12, 7.5))
    fig.subplots_adjust(left=0.31, right=0.95, top=0.79, bottom=0.11)
    add_header(fig, "Assistant response lengths", "Median and 95th percentile (p95) word counts; eight conversation datasets")
    add_source(fig, "outputs/data_quality_profiles.json")

    for y, (_, median, p95) in enumerate(rows):
        ax.plot([median, p95], [y, y], color=GRID, linewidth=5, solid_capstyle="round", zorder=1)
        ax.scatter(median, y, s=85, color=BLUE, edgecolor=BACKGROUND, linewidth=1.2, zorder=3)
        ax.scatter(p95, y, s=88, color=GOLD, marker="D", edgecolor=BACKGROUND, linewidth=1.2, zorder=3)
        ax.text(median, y - 0.24, format_number(median, 1).rstrip("0").rstrip("."), ha="center", va="bottom", color=BLUE, fontsize=8.5)
        ax.text(p95, y + 0.24, format_number(p95, 1).rstrip("0").rstrip("."), ha="center", va="top", color=GOLD, fontsize=8.5)

    ax.set_yticks(range(len(rows)), [row[0] for row in rows])
    ax.invert_yaxis()
    ax.set_xlim(0, max(row[2] for row in rows) * 1.10)
    ax.set_xlabel("Words per assistant response", labelpad=12)
    ax.legend(
        handles=[
            Line2D([0], [0], marker="o", color="none", markerfacecolor=BLUE, markersize=7, label="Median"),
            Line2D([0], [0], marker="D", color="none", markerfacecolor=GOLD, markersize=7, label="p95"),
        ],
        loc="upper right",
        bbox_to_anchor=(1, 1.10),
        frameon=False,
        ncol=2,
    )
    clean_axis(ax)
    save(fig, "response-lengths.png")


def preparation_signal_chart(profiles: list[dict]) -> None:
    thinking = []
    time_matches = []
    string_nulls = []
    for item in profiles:
        profile = item["profile"]
        if profile["data_shape"] != "conversation":
            continue
        name = DISPLAY_NAMES[item["dataset_id"]]
        assistant_count = profile.get("role_counts", {}).get("assistant", 0)
        thinking_count = profile.get("nonempty_thinking_messages", 0)
        if thinking_count:
            thinking.append((name, 100 * thinking_count / assistant_count))
        match_count = profile.get("text_scan", {}).get("time_sensitive_matches", 0)
        if match_count:
            time_matches.append((name, match_count))
        null_count = profile.get("string_encoded_null_fields", 0)
        if null_count:
            string_nulls.append((name, null_count))

    fig, axes = plt.subplots(3, 1, figsize=(12, 10), gridspec_kw={"height_ratios": [1.0, 1.6, 0.58]})
    fig.subplots_adjust(left=0.31, right=0.95, top=0.82, bottom=0.08, hspace=0.62)
    add_header(
        fig,
        "Data preparation signals",
        "Only values greater than zero are shown; the panels use different units",
    )
    add_source(fig, "outputs/data_quality_profiles.json")

    panels = [
        (axes[0], sorted(thinking, key=lambda x: x[1], reverse=True), "`thinking` coverage", "Percentage of assistant messages", BLUE, True),
        (axes[1], sorted(time_matches, key=lambda x: x[1], reverse=True), "Time-sensitive phrase matches", "Regex match count, not unique row count", GOLD, False),
        (axes[2], sorted(string_nulls, key=lambda x: x[1], reverse=True), "String-encoded `null` fields", "Field count", CORAL, False),
    ]
    for ax, rows, title, xlabel, color, percent in panels:
        labels = [row[0] for row in rows]
        values = [row[1] for row in rows]
        y = range(len(rows))
        ax.barh(list(y), values, height=0.52, color=color, zorder=3)
        ax.set_yticks(list(y), labels)
        ax.invert_yaxis()
        ax.set_title(title, loc="left", fontsize=11, fontweight="bold", pad=8)
        ax.set_xlabel(xlabel, labelpad=7, fontsize=9)
        ax.set_xlim(0, max(values) * 1.20 if values else 1)
        if percent:
            ax.xaxis.set_major_formatter(PercentFormatter(100, decimals=0))
        for row_y, value in enumerate(values):
            label = f"{value:.0f}%" if percent else format_number(value)
            ax.text(value + max(values) * 0.025, row_y, label, va="center", fontweight="bold", fontsize=9)
        clean_axis(ax)
    save(fig, "data-preparation-signals.png")


def catalog_missingness_chart(profiles: list[dict]) -> None:
    catalog = next(item for item in profiles if item["profile"]["data_shape"] == "catalog")
    profile = catalog["profile"]
    row_count = profile["row_count"]
    fields = {
        "Cover type (kapak_tipi)": "kapak_tipi",
        "Original title (orijinal_adi)": "orijinal_adi",
        "Translator (cevirmen)": "cevirmen",
        "Publication date (yayin_tarihi)": "yayin_tarihi",
    }
    missing = profile.get("null_counts", {})
    rows = sorted(
        [(display, 100 * missing.get(source, 0) / row_count, missing.get(source, 0)) for display, source in fields.items()],
        key=lambda item: item[1],
        reverse=True,
    )

    fig, ax = plt.subplots(figsize=(11.5, 5.8))
    fig.subplots_adjust(left=0.27, right=0.95, top=0.76, bottom=0.14)
    add_header(fig, "Missing fields in the Ithaki catalog", "Only fields with at least one missing value, across 103 catalog records")
    add_source(fig, "outputs/data_quality_profiles.json")

    positions = range(len(rows))
    values = [row[1] for row in rows]
    ax.barh(list(positions), values, height=0.55, color=GOLD, zorder=3)
    ax.set_yticks(list(positions), [row[0] for row in rows])
    ax.invert_yaxis()
    ax.set_xlim(0, 104)
    ax.xaxis.set_major_formatter(PercentFormatter(100, decimals=0))
    ax.set_xlabel("Missing-value rate", labelpad=12)
    for y, (_, rate, count) in enumerate(rows):
        ax.text(rate + 1.5, y, f"{round(rate, 1)}%  ({count}/{row_count})", va="center", fontweight="bold")
    clean_axis(ax)
    save(fig, "catalog-missing-fields.png")


def capability_coverage_chart(manifest: dict) -> None:
    rows = []
    for capability in manifest["capabilities"]:
        rows.append(
            (
                CAPABILITY_DISPLAY_NAMES[capability["capability"]],
                len(capability.get("direct_datasets", [])),
                len(capability.get("partial_datasets", [])),
                len(capability.get("conversion_sources", [])),
            )
        )

    fig, ax = plt.subplots(figsize=(11.8, 7.2))
    fig.subplots_adjust(left=0.24, right=0.92, top=0.78, bottom=0.11)
    add_header(
        fig,
        "Capability coverage matrix",
        "Counts are matched datasets; they do not indicate data volume or model performance",
    )
    add_source(fig, "appendix/dataset_manifest.json")

    colors = [BLUE, GOLD, OLIVE]
    pale_colors = [PALE_BLUE, PALE_GOLD, PALE_OLIVE]
    for y, row in enumerate(rows):
        for x, value in enumerate(row[1:]):
            face = colors[x] if value else pale_colors[x]
            text_color = "white" if value else MUTED
            ax.scatter(x, y, s=2300, marker="s", color=face, edgecolor=BACKGROUND, linewidth=2, zorder=2)
            ax.text(x, y, str(value), ha="center", va="center", color=text_color, fontsize=14, fontweight="bold", zorder=3)

    ax.set_xlim(-0.62, 2.62)
    ax.set_ylim(-0.65, len(rows) - 0.35)
    ax.set_xticks([0, 1, 2], ["Direct", "Partial", "Conversion source"])
    ax.xaxis.tick_top()
    ax.tick_params(axis="x", pad=12)
    ax.set_yticks(range(len(rows)), [row[0] for row in rows])
    ax.invert_yaxis()
    clean_axis(ax, vertical_grid=False)
    save(fig, "capability-coverage.png")


def main() -> None:
    profiles = load_json("outputs/data_quality_profiles.json")
    manifest = load_json("appendix/dataset_manifest.json")
    dataset_size_chart(profiles)
    duplicate_rate_chart(profiles)
    response_length_chart(profiles)
    preparation_signal_chart(profiles)
    catalog_missingness_chart(profiles)
    capability_coverage_chart(manifest)
    for path in sorted(OUTPUT_DIR.glob("*.png")):
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
