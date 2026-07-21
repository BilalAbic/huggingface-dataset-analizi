"""Generate the static PNG charts embedded in the Markdown reports."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "raporlar" / "gorseller"

INK = "#102A43"
MUTED = "#627D98"
GRID = "#D9E2EC"
BACKGROUND = "#F8FAFC"
WHITE = "#FFFFFF"
BLUE = "#2563EB"
GOLD = "#B7791F"
OLIVE = "#6B7B2E"

DISPLAY_NAMES = {
    "aliFurkan123/cultural-questions-dataset": "Kültürel / genel bilgi",
    "Aysenur44/namaz-vakti-identity-tr": "NamazAsistan Identity",
    "Egertekin/marvel-domain-dataset": "Marvel",
    "gururaser/ithaki-bilimkurgu-klasikleri": "İthaki kataloğu",
    "Mer1Alii/TR-ECommerce-CustomerSupport-Instructions": "E-ticaret destek",
    "namruni/meb-ogretmen-soru-cevap": "MEB öğretmen S-C",
    "nyzmemre/biyoloji-terimleri-turkce-sa": "Biyoloji terimleri",
    "sk75/sahin_identity": "Şahin Identity",
    "yoitsmeyusuf/felsefe_finetune": "Felsefe",
}


def load_font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("C:/Windows/Fonts/seguisb.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


TITLE_FONT = load_font(38, bold=True)
SUBTITLE_FONT = load_font(21)
LABEL_FONT = load_font(22)
VALUE_FONT = load_font(20, bold=True)
TICK_FONT = load_font(18)
NOTE_FONT = load_font(17)
LEGEND_FONT = load_font(19)


def new_chart(height: int, title: str, subtitle: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (1600, height), BACKGROUND)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((28, 28, 1572, height - 28), radius=24, fill=WHITE, outline=GRID, width=2)
    draw.text((72, 62), title, font=TITLE_FONT, fill=INK)
    draw.text((72, 116), subtitle, font=SUBTITLE_FONT, fill=MUTED)
    return image, draw


def draw_axis(
    draw: ImageDraw.ImageDraw,
    *,
    x0: int,
    y0: int,
    plot_width: int,
    plot_height: int,
    maximum: float,
    ticks: list[float],
    suffix: str = "",
) -> None:
    for tick in ticks:
        x = x0 + int(plot_width * tick / maximum)
        draw.line((x, y0, x, y0 + plot_height), fill=GRID, width=2)
        label = f"{tick:g}{suffix}"
        box = draw.textbbox((0, 0), label, font=TICK_FONT)
        draw.text((x - (box[2] - box[0]) / 2, y0 + plot_height + 12), label, font=TICK_FONT, fill=MUTED)


def save(image: Image.Image, name: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT_DIR / name, format="PNG", optimize=True)


def dataset_size_chart(profiles: list[dict]) -> None:
    rows = sorted(
        [(DISPLAY_NAMES[item["dataset_id"]], int(item["profile"]["row_count"])) for item in profiles],
        key=lambda item: item[1],
        reverse=True,
    )
    image, draw = new_chart(
        880,
        "Veri seti satır sayıları",
        "İncelenen 9 veri seti; toplam 3.119 satır",
    )
    x0, y0, width = 475, 190, 990
    group_height, bar_height = 62, 32
    plot_height = group_height * len(rows)
    maximum = 1250
    draw_axis(draw, x0=x0, y0=y0, plot_width=width, plot_height=plot_height, maximum=maximum, ticks=[0, 250, 500, 750, 1000, 1250])

    for index, (label, value) in enumerate(rows):
        y = y0 + index * group_height + 11
        label_box = draw.textbbox((0, 0), label, font=LABEL_FONT)
        draw.text((x0 - 24 - (label_box[2] - label_box[0]), y + 2), label, font=LABEL_FONT, fill=INK)
        bar_width = int(width * value / maximum)
        draw.rounded_rectangle((x0, y, x0 + bar_width, y + bar_height), radius=8, fill=BLUE)
        draw.text((x0 + bar_width + 12, y + 2), f"{value:,}".replace(",", "."), font=VALUE_FONT, fill=INK)

    draw.text((72, 808), "Kaynak: outputs/data_quality_profiles.json", font=NOTE_FONT, fill=MUTED)
    save(image, "veri_seti_satir_sayilari.png")


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

    image, draw = new_chart(
        970,
        "Normalleştirilmiş tekrar oranları",
        "Sohbet veri setlerinde istem ve cevap düzeyi; noktalama ve harf farkları yok sayılmıştır",
    )
    x0, y0, width = 475, 225, 990
    group_height, bar_height = 82, 24
    plot_height = group_height * len(rows)
    maximum = 80
    draw_axis(draw, x0=x0, y0=y0, plot_width=width, plot_height=plot_height, maximum=maximum, ticks=[0, 20, 40, 60, 80], suffix="%")

    draw.rounded_rectangle((1030, 168, 1054, 192), radius=5, fill=BLUE)
    draw.text((1066, 166), "Kullanıcı istemi", font=LEGEND_FONT, fill=INK)
    draw.rounded_rectangle((1250, 168, 1274, 192), radius=5, fill=GOLD)
    draw.text((1286, 166), "Asistan cevabı", font=LEGEND_FONT, fill=INK)

    for index, (label, prompt_rate, answer_rate) in enumerate(rows):
        y = y0 + index * group_height + 9
        label_box = draw.textbbox((0, 0), label, font=LABEL_FONT)
        draw.text((x0 - 24 - (label_box[2] - label_box[0]), y + 20), label, font=LABEL_FONT, fill=INK)
        for offset, value, color in ((0, prompt_rate, BLUE), (34, answer_rate, GOLD)):
            bar_width = int(width * value / maximum)
            if value > 0:
                draw.rounded_rectangle((x0, y + offset, x0 + bar_width, y + offset + bar_height), radius=6, fill=color)
            value_label = f"{value:.2f}%" if value else "0%"
            draw.text((x0 + max(bar_width, 0) + 10, y + offset), value_label, font=TICK_FONT, fill=INK if value else MUTED)

    draw.text((72, 898), "Kaynak: outputs/data_quality_profiles.json", font=NOTE_FONT, fill=MUTED)
    save(image, "normalizasyon_tekrar_oranlari.png")


def capability_coverage_chart(manifest: dict) -> None:
    rows = []
    for capability in manifest["capabilities"]:
        rows.append(
            (
                capability["capability"],
                len(capability.get("direct_datasets", [])),
                len(capability.get("partial_datasets", [])),
                len(capability.get("conversion_sources", [])),
            )
        )

    image, draw = new_chart(
        890,
        "Yetenek alanı için kullanılabilir veri seti sayısı",
        "Bir veri seti birden fazla alanda sayılabilir; doğrudan, kısmi ve dönüşüm kaynağı ayrımı korunmuştur",
    )
    x0, y0, width = 475, 230, 990
    group_height, bar_height = 82, 20
    plot_height = group_height * len(rows)
    maximum = 6
    draw_axis(draw, x0=x0, y0=y0, plot_width=width, plot_height=plot_height, maximum=maximum, ticks=[0, 1, 2, 3, 4, 5, 6])

    legend = [(BLUE, "Doğrudan"), (GOLD, "Kısmi"), (OLIVE, "Dönüşüm kaynağı")]
    legend_x = 940
    for color, label in legend:
        draw.rounded_rectangle((legend_x, 174, legend_x + 22, 196), radius=5, fill=color)
        draw.text((legend_x + 32, 173), label, font=LEGEND_FONT, fill=INK)
        legend_x += 185 if label != "Dönüşüm kaynağı" else 245

    for index, (label, direct, partial, conversion) in enumerate(rows):
        y = y0 + index * group_height + 4
        label_box = draw.textbbox((0, 0), label, font=LABEL_FONT)
        draw.text((x0 - 24 - (label_box[2] - label_box[0]), y + 22), label, font=LABEL_FONT, fill=INK)
        for offset, value, color in ((0, direct, BLUE), (25, partial, GOLD), (50, conversion, OLIVE)):
            bar_width = int(width * value / maximum)
            if value:
                draw.rounded_rectangle((x0, y + offset, x0 + bar_width, y + offset + bar_height), radius=5, fill=color)
            draw.text((x0 + bar_width + 9, y + offset - 1), str(value), font=TICK_FONT, fill=INK if value else MUTED)

    draw.text((72, 818), "Kaynak: ekler/dataset_manifest.json", font=NOTE_FONT, fill=MUTED)
    save(image, "yetenek_alani_kapsami.png")


def main() -> None:
    profiles = json.loads((ROOT / "outputs" / "data_quality_profiles.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "ekler" / "dataset_manifest.json").read_text(encoding="utf-8"))
    dataset_size_chart(profiles)
    duplicate_rate_chart(profiles)
    capability_coverage_chart(manifest)
    for path in sorted(OUTPUT_DIR.glob("*.png")):
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
