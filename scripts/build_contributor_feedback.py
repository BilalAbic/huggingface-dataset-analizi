"""Write one feedback page per contributor from the reviewed findings.

The analysis assesses a cohort of 47 submitted datasets, but every artifact it
produces is organised by dataset. A contributor who wants to know what to fix in
their own work has to read a 5,600-word report and locate themselves in it. These
pages invert that: one page per person, carrying only their datasets, in the
language the findings were written in.

Nothing here is new evidence. Every number is read from the computed profile and
every judgement from the reviewed findings, so a feedback page cannot disagree
with the report it comes from.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "feedback"

# Ordered most to least urgent. The order sets the sequence of work on a page; it
# never compares one contributor's dataset with another's.
SEVERITY = {
    "critical": ("Kritik", 0),
    "high": ("Yüksek", 1),
    "medium": ("Orta", 2),
    "low": ("Düşük", 3),
}
TURKISH_MAP = str.maketrans("çğıİöşüÇĞÖŞÜ", "cgiIosuCGOSU")


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def slug(name: str) -> str:
    """A filename that survives a checkout on any platform."""

    ascii_name = unicodedata.normalize("NFKD", name.translate(TURKISH_MAP))
    ascii_name = ascii_name.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"-+", "-", re.sub(r"[^A-Za-z0-9]+", "-", ascii_name)).strip("-").lower()


def thousands(value: object) -> str:
    """Turkish thousands separator, matching the reviewed findings text.

    The findings are written in Turkish and already use "11.858". Rendering the
    same figure as "11,858" one line above would read as a different number.
    """

    return f"{value:,}".replace(",", ".") if isinstance(value, int) else "—"


def dataset_section(dataset_id: str, profile: dict, card: dict, review: dict) -> list[str]:
    data = profile["profile"]
    answers = data.get("assistant_answer_duplicates") or {}
    topic = data.get("topic_profile") or {}
    lines = [
        f"## `hf/{dataset_id}`",
        "",
        f"<https://huggingface.co/datasets/{dataset_id}>",
        "",
        f"**Ne için:** {review['intended_use']}",
        "",
        f"**Durum:** {review['disposition']}",
        "",
        "| Ölçüm | Değer |",
        "|---|---:|",
        f"| Satır sayısı | {thousands(data['row_count'])} |",
    ]
    if answers.get("distinct_values") is not None:
        lines.append(f"| Bunun kaçı farklı cevap | {thousands(answers['distinct_values'])} |")
    if topic.get("topic_concentration") is not None:
        lines.append(f"| Söz varlığı yoğunlaşması | %{topic['topic_concentration'] * 100:.0f} |")
    lines += [
        f"| Şema | {data['data_shape']} |",
        f"| Veri kartı | {'var' if card.get('readme_has_body') else '**gövdesi yok**'} |",
        f"| Lisans | {card.get('license') or '**beyan edilmemiş**'} |",
        "",
    ]
    if topic.get("distinctive_terms"):
        terms = ", ".join(f"`{t['term']}`" for t in topic["distinctive_terms"][:8])
        lines += [f"**Veri setini ayırt eden terimler:** {terms}", ""]
    if topic.get("template_driven_prompts"):
        # The profile stores this caveat in English because the profile is a
        # public English artifact. On a Turkish page it is restated in Turkish
        # from the same underlying rate.
        rate = (data.get("user_prompt_duplicates") or {}).get("duplicate_rate") or 0
        lines += [
            f"> İstemlerin %{rate * 100:.0f}'i tekrar ediyor, yani kullanıcı turu büyük",
            "> ölçüde sabit bir talimat. Yukarıdaki terimler konuyu değil talimatı",
            "> anlatıyor olabilir.",
            "",
        ]

    lines += ["### İyi olan", ""]
    lines += [f"- {item}" for item in review["strengths"]]
    lines += [""]

    findings = sorted(review["findings"], key=lambda f: SEVERITY.get(f["severity"], ("", 9))[1])
    lines += [f"### Ele alınması gerekenler ({len(findings)})", ""]
    for index, finding in enumerate(findings, start=1):
        label = SEVERITY.get(finding["severity"], (finding["severity"], 9))[0]
        lines += [
            f"#### {index}. {label}",
            "",
            f"**Tespit.** {finding['evidence']}",
            "",
            f"**Neden önemli.** {finding['risk']}",
            "",
            f"**Ne yapmalı.** {finding['remediation']}",
            "",
        ]
    return lines


# The verbatim HTTP evidence lives in config/datasets.json in English, because
# that file is part of the public repository. Restating it here in Turkish keeps
# the feedback page readable without inventing anything: both descriptions are
# generated from the same structured status field.
BLOCK_EXPLANATION = {
    "gated_manual": (
        "Depo herkese açık ve veri kartı okunabiliyor, ancak veri dosyaları "
        "**elle onaylı erişime** kapalı. Denetim hesabı yetkili listede olmadığı için "
        "dosyalar indirilemedi.",
        "Hugging Face'teki depo sayfasından denetim hesabının erişim talebini onaylayın. "
        "Onaydan sonra analiz veri setini otomatik olarak kapsar.",
    ),
    "not_found_or_private": (
        "Depo, kimlik doğrulanmış bir istekle bile görünmüyor. Geçerli bir kimlikle "
        "gelen **404** yanıtı, deponun silinmiş, adının değişmiş veya başka bir hesaba "
        "özel olduğu anlamına gelir.",
        "Depo adresinin doğru olduğunu teyit edin; depo özelse herkese açık hâle "
        "getirin veya denetim hesabına erişim verin.",
    ),
}


def blocked_section(entry: dict) -> list[str]:
    failing = [
        check for check in entry.get("reverified_checks", [])
        if check.get("status") and check["status"] != 200
    ]
    codes = ", ".join(f"HTTP {code}" for code in sorted({c["status"] for c in failing})) or "kayıtlı değil"
    what, todo = BLOCK_EXPLANATION.get(
        entry["status"],
        ("Veri dosyalarına erişilemedi.", "Erişimi açın ve analizi yeniden çalıştırın."),
    )
    return [
        f"## `hf/{entry['dataset_id']}`",
        "",
        f"<https://huggingface.co/datasets/{entry['dataset_id']}>",
        "",
        "**Bu veri seti analiz edilemedi.** Kapsam dışı bırakılmadı; erişilemediği",
        "kanıtıyla birlikte kayda geçirildi.",
        "",
        f"**Ne oldu.** {what}",
        "",
        f"**Doğrulama.** {entry.get('reverified_on')} tarihinde yeniden denendi; başarısız",
        f"isteklerin yanıtı: {codes}. İsteklerin tam adresleri ve yanıt metinleri",
        "[`outputs/excluded_datasets.json`](../outputs/excluded_datasets.json) içinde.",
        "",
        f"**Ne yapmalı.** {todo}",
        "",
        "Erişim açıldığında hiçbir kod değişikliği gerekmez; boru hattı bu veri setini",
        "sonraki koşuda otomatik olarak alır.",
        "",
    ]


def build_pages(output_dir: Path) -> list[tuple[str, str, list[str]]]:
    registry = load("config/datasets.json")["datasets"]
    profiles = {item["dataset_id"]: item for item in load("outputs/data_quality_profiles.json")}
    reviews = load("outputs/manual_findings.json")["datasets"]
    blocked = {item["dataset_id"]: item for item in load("outputs/excluded_datasets.json")["datasets"]}
    as_of = load("outputs/manual_findings.json")["as_of"]

    owned: dict[str, list[dict]] = defaultdict(list)
    for entry in registry:
        owned[entry["contributor"]].append(entry)

    pages = []
    for contributor in sorted(owned, key=str.casefold):
        entries = sorted(owned[contributor], key=lambda e: e["dataset_id"].casefold())
        handle = any(e.get("contributor_source") == "hugging face account handle" for e in entries)
        analyzed = [e for e in entries if e["dataset_id"] not in blocked]
        finding_count = sum(len(reviews[e["dataset_id"]]["findings"]) for e in analyzed)
        rows = sum(profiles[e["dataset_id"]]["profile"]["row_count"] for e in analyzed)

        lines = [f"# {contributor}", ""]
        if handle:
            lines += [
                "> Bu ad, gönderi formunda doğrulanabilir bir tam ad bulunmadığı için",
                "> Hugging Face hesap adıdır. Düzeltmek isterseniz bildirin.",
                "",
            ]
        summary = f"{len(entries)} veri seti"
        if analyzed:
            summary += f", toplam {thousands(rows)} satır, {finding_count} bulgu"
        if len(analyzed) != len(entries):
            summary += f", {len(entries) - len(analyzed)} tanesi erişilemediği için analiz edilemedi"
        lines += [
            f"{summary}. Değerlendirme tarihi {as_of}.",
            "",
            "Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle",
            "karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre",
            "değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir",
            "cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.",
            "",
        ]
        for entry in entries:
            dataset_id = entry["dataset_id"]
            if dataset_id in blocked:
                lines += blocked_section(blocked[dataset_id])
            else:
                lines += dataset_section(
                    dataset_id, profiles[dataset_id], profiles[dataset_id]["card"], reviews[dataset_id]
                )
        lines += [
            "---",
            "",
            "Koleksiyonun tamamı, yöntem ve eşikler:",
            "[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·",
            "[yetenek eşlemesi](../reports/model-capability-mapping.md) ·",
            "[değerlendirme kriterleri](../config/evaluation_criteria.json)",
            "",
        ]
        pages.append((contributor, slug(contributor), lines))
    return pages


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    pages = build_pages(output_dir)
    seen: set[str] = set()
    for contributor, name, lines in pages:
        if name in seen:
            raise RuntimeError(f"Two contributors produced the same filename: {name}")
        seen.add(name)
        (output_dir / f"{name}.md").write_text("\n".join(lines), encoding="utf-8")

    index = [
        "# Katkıcı geri bildirimleri",
        "",
        f"Her katkıcı için tek sayfa. {len(pages)} sayfa, koleksiyondaki her veri setini kapsar.",
        "",
        "Sayfalar [`outputs/manual_findings.json`](../outputs/manual_findings.json) ve",
        "[`outputs/data_quality_profiles.json`](../outputs/data_quality_profiles.json)",
        "dosyalarından üretilir; yeni kanıt içermezler ve raporla çelişemezler.",
        "",
        "| Katkıcı | Veri seti | Bulgu |",
        "|---|---:|---:|",
    ]
    profiles = {i["dataset_id"] for i in load("outputs/data_quality_profiles.json")}
    reviews = load("outputs/manual_findings.json")["datasets"]
    registry = load("config/datasets.json")["datasets"]
    owned: dict[str, list[str]] = defaultdict(list)
    for entry in registry:
        owned[entry["contributor"]].append(entry["dataset_id"])
    for contributor, name, _ in pages:
        ids = owned[contributor]
        findings = sum(len(reviews[i]["findings"]) for i in ids if i in profiles)
        index.append(f"| [{contributor}]({name}.md) | {len(ids)} | {findings} |")
    index.append("")
    (output_dir / "README.md").write_text("\n".join(index), encoding="utf-8")

    print(f"Wrote {len(pages)} contributor pages to {output_dir.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
