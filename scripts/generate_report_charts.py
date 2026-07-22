"""Generate the six static PNG figures embedded in the Markdown reports."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, LogLocator, PercentFormatter


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

# Row pitch in inches. At 40+ datasets a fixed figure height would compress the
# category axis until the labels collide, so every chart sizes itself from the
# number of rows it actually draws.
ROW_PITCH = 0.34
HEADER_INCHES = 2.3
FOOTER_INCHES = 1.0
# Charts label datasets with their full hf/owner/name identifier so a bar can be
# traced to exactly one Hugging Face repository with no lookup table. The longest
# identifier is ~64 characters, so these charts are wider than usual and reserve a
# large left margin for the category axis.
FIGURE_WIDTH = 16.0
LABEL_LEFT_MARGIN = 0.40
LABEL_FONTSIZE = 8.0

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

CAPABILITY_DISPLAY_NAMES = {
    "Identity": "Identity",
    "Tool Call": "Tool Calling",
    "Conversation": "Conversation",
    "Instruction": "Instruction\nFollowing",
    "Structured Output": "Structured\nOutput",
    "Math": "Math",
    "Coding": "Coding",
}

RESPONSE_SHAPES = {"conversation", "instruction_pair"}
STRUCTURED_SHAPES = {"catalog", "tabular"}


def load_json(relative_path: str):
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def display_name(dataset_id: str) -> str:
    """Return the chart label for a dataset: its full hf/owner/name identifier.

    Using the identifier verbatim means every bar maps to exactly one Hugging
    Face repository without a lookup table, at the cost of a wide left margin.
    """

    return f"hf/{dataset_id}"


def format_number(value: float, decimals: int = 0) -> str:
    return f"{value:,.{decimals}f}"


def figure_height(row_count: int, *, minimum: float = 6.0) -> float:
    return max(minimum, HEADER_INCHES + FOOTER_INCHES + row_count * ROW_PITCH)


def add_header(fig: plt.Figure, title: str, subtitle: str) -> None:
    """Place the title block in inches so it does not drift as figures grow."""

    height = fig.get_figheight()
    fig.text(0.04, 1 - 0.55 / height, title, fontsize=19, fontweight="bold", ha="left", va="top", color=INK)
    fig.text(0.04, 1 - 1.05 / height, subtitle, fontsize=10.5, ha="left", va="top", color=MUTED, wrap=True)


def add_source(fig: plt.Figure, source: str) -> None:
    fig.text(
        0.04,
        0.25 / fig.get_figheight(),
        f"Source: {source}",
        fontsize=8.5,
        ha="left",
        va="bottom",
        color=MUTED,
    )


def layout(fig: plt.Figure, *, left: float = LABEL_LEFT_MARGIN, right: float = 0.97) -> None:
    height = fig.get_figheight()
    fig.subplots_adjust(
        left=left,
        right=right,
        top=1 - HEADER_INCHES / height,
        bottom=FOOTER_INCHES / height,
    )


def clean_axis(ax: plt.Axes, *, vertical_grid: bool = True) -> None:
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis="both", length=0)
    if vertical_grid:
        ax.grid(axis="x", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)


def save(fig: plt.Figure, name: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_DIR / name, dpi=150, bbox_inches="tight", pad_inches=0.22)
    plt.close(fig)


def dataset_size_chart(profiles: list[dict]) -> None:
    rows = sorted(
        [(display_name(item["dataset_id"]), int(item["profile"]["row_count"])) for item in profiles],
        key=lambda item: item[1],
        reverse=True,
    )
    labels, values = zip(*rows)
    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, figure_height(len(rows))))
    layout(fig)
    total_rows = sum(values)
    add_header(
        fig,
        "Dataset volumes",
        f"{total_rows:,} rows across {len(rows)} fixed dataset snapshots. "
        f"The axis is logarithmic: sizes span {min(values):,} to {max(values):,} rows, "
        "so a linear axis would flatten most of the collection to nothing.",
    )
    add_source(fig, "outputs/data_quality_profiles.json")

    positions = range(len(rows))
    ax.barh(positions, values, height=0.62, color=BLUE, zorder=3)
    ax.set_yticks(list(positions), labels, fontsize=LABEL_FONTSIZE)
    ax.invert_yaxis()
    ax.set_xscale("log")
    ax.set_xlim(1, max(values) * 3.2)
    ax.xaxis.set_major_locator(LogLocator(base=10))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: format_number(x)))
    ax.set_xlabel("Row count (logarithmic scale)", labelpad=12)
    clean_axis(ax)
    for y, value in enumerate(values):
        ax.text(value * 1.12, y, format_number(value), va="center", fontweight="bold", fontsize=8.5)
    save(fig, "dataset-row-counts.png")


def duplicate_rate_chart(profiles: list[dict]) -> None:
    rows = []
    for item in profiles:
        profile = item["profile"]
        if profile["data_shape"] not in RESPONSE_SHAPES:
            continue
        prompt_rate = 100 * (profile.get("user_prompt_duplicates", {}).get("duplicate_rate") or 0)
        answer_rate = 100 * (profile.get("assistant_answer_duplicates", {}).get("duplicate_rate") or 0)
        rows.append((display_name(item["dataset_id"]), prompt_rate, answer_rate))
    rows.sort(key=lambda item: max(item[1], item[2]), reverse=True)

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, figure_height(len(rows))))
    layout(fig)
    add_header(
        fig,
        "Normalized duplicate density",
        "Rate = extra copies after the first occurrence / all rows; case and punctuation "
        "differences are ignored. Values are printed beside each pair.",
    )
    add_source(fig, "outputs/data_quality_profiles.json")

    for y, (_, prompt, answer) in enumerate(rows):
        ax.plot([prompt, answer], [y, y], color=GRID, linewidth=3, solid_capstyle="round", zorder=1)
        ax.scatter(prompt, y, s=58, color=BLUE, edgecolor=BACKGROUND, linewidth=1.1, zorder=3)
        ax.scatter(answer, y, s=58, color=GOLD, edgecolor=BACKGROUND, linewidth=1.1, zorder=3)

    # At this row density per-point callouts collide, so each row carries a
    # single readout. It sits in a reserved gutter past the largest data point
    # so the text can never overlap a marker.
    largest_rate = max((max(row[1], row[2]) for row in rows), default=0)
    plotted_max = max(10.0, largest_rate)
    gutter = plotted_max * 1.06
    limit = plotted_max * 1.40
    for y, (_, prompt, answer) in enumerate(rows):
        ax.text(gutter, y, f"{prompt:.1f}% / {answer:.1f}%", va="center", ha="left",
                fontsize=8, color=MUTED)

    ax.set_yticks(range(len(rows)), [row[0] for row in rows], fontsize=LABEL_FONTSIZE)
    ax.invert_yaxis()
    ax.set_xlim(-1, limit)
    # Ticks stop at the real data range; the gutter is annotation space, not scale.
    step = 20 if plotted_max > 40 else 5
    ax.set_xticks([t for t in range(0, int(plotted_max) + step, step) if t <= plotted_max + 1])
    ax.xaxis.set_major_formatter(PercentFormatter(100, decimals=0))
    ax.set_xlabel("Extra-copy rate (prompt / answer)", labelpad=12)
    ax.legend(
        handles=[
            Line2D([0], [0], marker="o", color="none", markerfacecolor=BLUE, markeredgecolor=BLUE, markersize=7, label="User prompt"),
            Line2D([0], [0], marker="o", color="none", markerfacecolor=GOLD, markeredgecolor=GOLD, markersize=7, label="Assistant answer"),
        ],
        loc="lower right",
        bbox_to_anchor=(1, 1.005),
        frameon=False,
        ncol=2,
    )
    clean_axis(ax)
    save(fig, "duplicate-rates.png")


def response_length_chart(profiles: list[dict]) -> None:
    rows = []
    for item in profiles:
        profile = item["profile"]
        if profile["data_shape"] not in RESPONSE_SHAPES:
            continue
        lengths = profile["assistant_word_length"]
        if lengths.get("median") is None:
            continue
        rows.append((display_name(item["dataset_id"]), float(lengths["median"]), float(lengths["p95"])))
    rows.sort(key=lambda item: item[2], reverse=True)

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, figure_height(len(rows))))
    layout(fig)
    add_header(
        fig,
        "Assistant response lengths",
        f"Median and 95th percentile (p95) word counts across {len(rows)} response datasets. "
        "Each row is labelled median / p95.",
    )
    add_source(fig, "outputs/data_quality_profiles.json")

    plotted_max = max(row[2] for row in rows)
    gutter = plotted_max * 1.06
    upper = plotted_max * 1.42
    for y, (_, median, p95) in enumerate(rows):
        ax.plot([median, p95], [y, y], color=GRID, linewidth=4, solid_capstyle="round", zorder=1)
        ax.scatter(median, y, s=58, color=BLUE, edgecolor=BACKGROUND, linewidth=1.1, zorder=3)
        ax.scatter(p95, y, s=60, color=GOLD, marker="D", edgecolor=BACKGROUND, linewidth=1.1, zorder=3)
        # Reserved gutter past the largest p95 keeps the readout clear of markers.
        ax.text(gutter, y, f"{median:g} / {p95:g}", va="center", ha="left", fontsize=8, color=MUTED)

    ax.set_yticks(range(len(rows)), [row[0] for row in rows], fontsize=LABEL_FONTSIZE)
    ax.invert_yaxis()
    ax.set_xlim(0, upper)
    step = 200 if plotted_max > 700 else (100 if plotted_max > 300 else 50)
    ax.set_xticks([t for t in range(0, int(plotted_max) + step, step) if t <= plotted_max + step * 0.2])
    ax.set_xlabel("Words per assistant response (median / p95)", labelpad=12)
    ax.legend(
        handles=[
            Line2D([0], [0], marker="o", color="none", markerfacecolor=BLUE, markersize=7, label="Median"),
            Line2D([0], [0], marker="D", color="none", markerfacecolor=GOLD, markersize=7, label="p95"),
        ],
        loc="lower right",
        bbox_to_anchor=(1, 1.005),
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
        if profile["data_shape"] not in RESPONSE_SHAPES:
            continue
        name = display_name(item["dataset_id"])
        assistant_count = profile.get("role_counts", {}).get(
            "assistant", profile.get("row_count", 0)
        ) or profile.get("row_count", 0)
        thinking_count = max(
            profile.get("nonempty_thinking_messages", 0),
            profile.get("row_level_thinking_rows", 0),
        )
        if thinking_count:
            thinking.append((name, 100 * thinking_count / assistant_count))
        match_count = profile.get("text_scan", {}).get("time_sensitive_matches", 0)
        if match_count:
            time_matches.append((name, match_count))
        null_count = profile.get("string_encoded_null_fields", 0)
        if null_count:
            string_nulls.append((name, null_count))

    panels = [
        (sorted(thinking, key=lambda x: x[1], reverse=True), "`thinking` coverage", "Percentage of assistant messages", BLUE, True, False),
        (sorted(time_matches, key=lambda x: x[1], reverse=True), "Time-sensitive phrase matches", "Regex match count, not unique row count", GOLD, False, True),
        (sorted(string_nulls, key=lambda x: x[1], reverse=True), "String-encoded `null` fields", "Field count", CORAL, False, True),
    ]

    # Each panel now holds a different number of datasets, so panel heights are
    # allocated from their own row counts instead of a fixed ratio.
    panel_rows = [max(len(rows), 1) for rows, *_ in panels]
    panel_heights = [count * ROW_PITCH for count in panel_rows]
    # Space for each panel's own title and axis label, plus one gap between panels.
    # The gap must clear the previous panel's x-axis label and this panel's title,
    # otherwise the two collide once the panels are packed tightly.
    title_inches = 0.85
    gap_inches = 1.15
    plot_inches = sum(panel_heights) + len(panels) * title_inches
    total_height = HEADER_INCHES + FOOTER_INCHES + plot_inches + gap_inches * (len(panels) - 1)
    fig, axes = plt.subplots(
        3,
        1,
        figsize=(FIGURE_WIDTH, total_height),
        gridspec_kw={"height_ratios": [h + title_inches for h in panel_heights]},
    )
    # hspace is a fraction of the mean axes height, so convert the intended gap.
    mean_panel = (plot_inches) / len(panels)
    fig.subplots_adjust(
        left=LABEL_LEFT_MARGIN,
        right=0.97,
        top=1 - HEADER_INCHES / total_height,
        bottom=FOOTER_INCHES / total_height,
        hspace=gap_inches / mean_panel,
    )
    add_header(
        fig,
        "Data preparation signals",
        "Only values greater than zero are shown. The three panels use different units "
        "and independent scales; heights are not comparable between panels.",
    )
    add_source(fig, "outputs/data_quality_profiles.json")

    for ax, (rows, title, xlabel, color, percent, log_scale) in zip(axes, panels):
        labels = [row[0] for row in rows]
        values = [row[1] for row in rows]
        y = range(len(rows))
        ax.barh(list(y), values, height=0.62, color=color, zorder=3)
        ax.set_yticks(list(y), labels, fontsize=LABEL_FONTSIZE)
        ax.invert_yaxis()
        ax.set_title(title, loc="left", fontsize=11, fontweight="bold", pad=8)
        ax.set_xlabel(xlabel, labelpad=7, fontsize=9)
        if not values:
            ax.set_xlim(0, 1)
        elif log_scale and max(values) / max(min(values), 1) > 50:
            ax.set_xscale("log")
            ax.set_xlim(1, max(values) * 3.2)
            ax.set_xlabel(f"{xlabel} (logarithmic scale)", labelpad=7, fontsize=9)
        else:
            ax.set_xlim(0, max(values) * 1.24)
        if percent:
            ax.xaxis.set_major_formatter(PercentFormatter(100, decimals=0))
        else:
            ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: format_number(x)))
        for row_y, value in enumerate(values):
            label = f"{value:.0f}%" if percent else format_number(value)
            offset = value * 1.12 if ax.get_xscale() == "log" else value + max(values) * 0.02
            ax.text(offset, row_y, label, va="center", fontweight="bold", fontsize=8.5)
        clean_axis(ax)
    save(fig, "data-preparation-signals.png")


def structured_missingness_chart(profiles: list[dict]) -> None:
    """Field completeness for every structured dataset, not just the first catalog.

    The earlier version hardcoded the four Ithaki columns and picked a single
    catalog record, which silently hid any other structured source in scope.
    """

    entries = []
    for item in profiles:
        profile = item["profile"]
        if profile["data_shape"] not in STRUCTURED_SHAPES:
            continue
        row_count = profile["row_count"]
        missing = profile.get("null_counts", {})
        fields = sorted(
            ((column, count) for column, count in missing.items() if count),
            key=lambda pair: pair[1],
            reverse=True,
        )[:8]
        if fields:
            entries.append((display_name(item["dataset_id"]), row_count, fields))

    if not entries:
        raise RuntimeError("No structured dataset with missing values was found in the profiles.")

    panel_rows = [len(fields) for _, _, fields in entries]
    total_height = HEADER_INCHES + FOOTER_INCHES + sum(
        1.15 + count * 0.42 for count in panel_rows
    )
    fig, axes = plt.subplots(
        len(entries),
        1,
        figsize=(FIGURE_WIDTH, total_height),
        gridspec_kw={"height_ratios": panel_rows},
        squeeze=False,
    )
    fig.subplots_adjust(
        left=LABEL_LEFT_MARGIN,
        right=0.97,
        top=1 - HEADER_INCHES / total_height,
        bottom=FOOTER_INCHES / total_height,
        hspace=max(0.5, 9.0 / total_height),
    )
    add_header(
        fig,
        "Missing fields in the structured datasets",
        "Only fields with at least one missing value are shown. Source column names are "
        "kept verbatim so each bar traces back to the dataset schema.",
    )
    add_source(fig, "outputs/data_quality_profiles.json")

    for ax, (name, row_count, fields) in zip(axes.flat, entries):
        labels = [column for column, _ in fields]
        rates = [100 * count / row_count for _, count in fields]
        counts = [count for _, count in fields]
        positions = range(len(fields))
        ax.barh(list(positions), rates, height=0.6, color=GOLD, zorder=3)
        ax.set_yticks(list(positions), labels, fontsize=LABEL_FONTSIZE)
        ax.invert_yaxis()
        ax.set_xlim(0, 128)
        ax.xaxis.set_major_formatter(PercentFormatter(100, decimals=0))
        ax.set_title(f"{name} — {row_count:,} records", loc="left", fontsize=11, fontweight="bold", pad=8)
        ax.set_xlabel("Missing-value rate", labelpad=7, fontsize=9)
        for y, (rate, count) in enumerate(zip(rates, counts)):
            ax.text(rate + 1.6, y, f"{round(rate, 1)}%  ({count}/{row_count})", va="center", fontweight="bold", fontsize=8.5)
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

    fig, ax = plt.subplots(figsize=(11.8, 7.6))
    fig.subplots_adjust(left=0.24, right=0.92, top=0.76, bottom=0.10)
    add_header(
        fig,
        "Capability coverage matrix",
        "Counts are matched datasets; they do not indicate data volume or model performance.",
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
    structured_missingness_chart(profiles)
    capability_coverage_chart(manifest)
    for path in sorted(OUTPUT_DIR.glob("*.png")):
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
