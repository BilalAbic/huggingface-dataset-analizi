"""Build an executed, data-driven notebook from the checked JSON evidence."""

from __future__ import annotations

import argparse
import json
import textwrap
from collections import Counter
from pathlib import Path

import nbformat as nbf
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_NOTEBOOK = ROOT / "notebook" / "huggingface_dataset_quality_analysis.ipynb"


def markdown(source: str):
    return nbf.v4.new_markdown_cell(textwrap.dedent(source).strip())


def code(source: str):
    return nbf.v4.new_code_cell(textwrap.dedent(source).strip())


def resolve_path(root: Path, value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=str(ROOT), help="Repository root")
    parser.add_argument("--output", default=str(DEFAULT_NOTEBOOK), help="Notebook output path")
    parser.add_argument("--no-execute", action="store_true", help="Write the notebook without executing it")
    parser.add_argument("--timeout", type=int, default=180, help="Per-cell execution timeout")
    return parser.parse_args()


def build_notebook(project_root: Path) -> nbf.NotebookNode:
    profiles = json.loads(
        (project_root / "outputs" / "data_quality_profiles.json").read_text(encoding="utf-8")
    )
    excluded = json.loads(
        (project_root / "outputs" / "excluded_datasets.json").read_text(encoding="utf-8")
    ).get("datasets", [])
    total_rows = sum(item["profile"]["row_count"] for item in profiles)
    shape_counts = Counter(item["profile"]["data_shape"] for item in profiles)
    conversation_like = sum(
        item["profile"]["row_count"]
        for item in profiles
        if item["profile"]["data_shape"] in {"conversation", "instruction_pair"}
    )
    thinking_count = sum(
        item["profile"].get("nonempty_thinking_messages", 0) for item in profiles
    )
    string_null_count = sum(
        item["profile"].get("string_encoded_null_fields", 0) for item in profiles
    )
    shape_text = ", ".join(f"{shape}: {count}" for shape, count in sorted(shape_counts.items()))

    notebook = nbf.v4.new_notebook()
    notebook["metadata"]["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    notebook["metadata"]["language_info"] = {"name": "python", "version": "3.12"}
    notebook["cells"] = [
        markdown(
            f"""
            # Hugging Face Veri Seti Kalite Analizi

            ## tl;dr

            - **{len(profiles):,} veri setinde {total_rows:,} satır** yerel sabit
              kopyalardan profillendi.
            - Şema dağılımı: **{shape_text}**. Sohbet veya düz istem–cevap
              biçimindeki toplam kayıt sayısı **{conversation_like:,}**.
            - Ayrı `thinking` içeren kayıt sayısı **{thinking_count:,}**; metin
              biçiminde saklanan `null` alan sayısı **{string_null_count:,}**.
            - Erişim engeli nedeniyle analiz edilemeyen veri seti sayısı
              **{len(excluded)}**; bunlar sessizce atlanmadı, kanıtlarıyla
              birlikte ayrı bir tabloda listeleniyor.
            - Tekrar, eksik değer, metin uzunluğu ve zaman hassasiyeti ölçümleri
              kullanım amacına göre yorumlanmalı; satır hacmi tek başına kalite
              göstergesi değildir.
            """
        ),
        markdown(
            """
            ## Bağlam ve Yöntem

            Analiz, Hugging Face Dataset Viewer üzerinden indirilen tam yerel
            kopyalar ve sabit kaynak revizyonları üzerinde çalışır. Kontroller;
            şema, tamamlılık, rol sırası, birebir ve normalleştirilmiş tekrar,
            metin uzunluğu, `thinking`, metin biçimindeki `null`, kişisel veri
            biçimleri ve zaman hassasiyeti sinyallerini kapsar.

            ### Temel Varsayımlar

            - Normalleştirilmiş tekrar oranı, her metin ailesindeki ilk örnekten
              sonraki ek kopyaların tüm satırlara bölünmesiyle hesaplanır.
            - Zaman hassasiyeti sayıları regex eşleşmeleridir; benzersiz satır
              sayısı değildir.
            - Regex taraması bağlamsal kişi ve kurum adlarını bütünüyle yakalayamaz.
            - Yapısal doğrulama, her cevabın alan uzmanı tarafından olgusal olarak
              onaylandığı anlamına gelmez.
            """
        ),
        markdown("## Veri"),
        code(
            """
            import json
            from pathlib import Path
            import pandas as pd

            WORKING_DIR = Path.cwd()
            PROJECT_DIR = next(
                (
                    candidate
                    for candidate in (WORKING_DIR, WORKING_DIR.parent)
                    if (candidate / "outputs" / "data_quality_profiles.json").exists()
                ),
                None,
            )
            if PROJECT_DIR is None:
                raise FileNotFoundError(
                    "Project outputs were not found in the working directory or its parent."
                )

            profiles = json.loads(
                (PROJECT_DIR / "outputs" / "data_quality_profiles.json").read_text(encoding="utf-8")
            )
            overlaps = json.loads(
                (PROJECT_DIR / "outputs" / "cross_dataset_overlap.json").read_text(encoding="utf-8")
            )
            manual_path = PROJECT_DIR / "outputs" / "manual_findings.json"
            manual = json.loads(manual_path.read_text(encoding="utf-8")) if manual_path.exists() else {"datasets": {}}
            excluded = json.loads(
                (PROJECT_DIR / "outputs" / "excluded_datasets.json").read_text(encoding="utf-8")
            )["datasets"]

            len(profiles), sum(item["profile"]["row_count"] for item in profiles)
            """
        ),
        markdown(
            """
            ### Analiz edilemeyen veri setleri

            Kayıt defterinde etkin olduğu hâlde erişilemeyen veri setleri kapsam
            dışı bırakılmaz; her biri canlı olarak yeniden doğrulanmış HTTP
            kanıtıyla birlikte burada listelenir. Aşağıdaki satırlar toplam satır
            sayısına dâhil değildir.
            """
        ),
        code(
            """
            pd.DataFrame([
                {
                    "dataset": item["dataset_id"],
                    "contributor": item.get("contributor"),
                    "status": item["status"],
                    "reverified_on": item.get("reverified_on"),
                    "http_status": ", ".join(
                        str(check.get("status")) for check in item.get("reverified_checks", [])
                    ),
                }
                for item in excluded
            ])
            """
        ),
        code(
            """
            summary_rows = []
            for item in profiles:
                profile = item["profile"]
                scan = profile.get("text_scan", {})
                summary_rows.append({
                    "dataset": item["dataset_id"],
                    "contributor": item.get("contributor"),
                    "rows": profile["row_count"],
                    "shape": profile["data_shape"],
                    "exact_duplicates": profile.get("exact_duplicate_rows", 0),
                    "prompt_duplicates_%": round(100 * profile.get("user_prompt_duplicates", {}).get("duplicate_rate", 0), 2),
                    "answer_duplicates_%": round(100 * profile.get("assistant_answer_duplicates", {}).get("duplicate_rate", 0), 2),
                    "thinking": profile.get("nonempty_thinking_messages", 0),
                    "string_nulls": profile.get("string_encoded_null_fields", 0),
                    "time_sensitive_matches": scan.get("time_sensitive_matches", 0),
                    "answer_words_median": profile.get("assistant_word_length", {}).get("median"),
                    "answer_words_p95": profile.get("assistant_word_length", {}).get("p95"),
                    "json_answers": profile.get("structured_answers", {}).get("json_parsable_answers", 0),
                    "json_like_broken": profile.get("structured_answers", {}).get("json_like_but_unparsable_answers", 0),
                    "conflicting_prompt_families": profile.get("answer_families", {}).get(
                        "prompt_families_with_conflicting_answers", 0
                    ),
                    "cross_split_duplicate_rows": profile.get("split_integrity", {}).get(
                        "cross_split_duplicate_rows", 0
                    ),
                })

            summary = pd.DataFrame(summary_rows).sort_values("dataset").reset_index(drop=True)
            summary
            """
        ),
        markdown(
            """
            ## Sonuçlar

            ### Portföy toplamları yeniden hesaplanıyor

            Bu hücre temel toplamları doğrudan profil dosyasından üretir ve
            notebook oluşturulurken gözlenen sabit değerlerle karşılaştırır.
            """
        ),
        code(
            f"""
            portfolio = pd.Series({{
                "dataset_count": len(summary),
                "total_rows": int(summary["rows"].sum()),
                "conversation_rows": int(summary.loc[summary["shape"] == "conversation", "rows"].sum()),
                "instruction_pair_rows": int(summary.loc[summary["shape"] == "instruction_pair", "rows"].sum()),
                "catalog_rows": int(summary.loc[summary["shape"] == "catalog", "rows"].sum()),
                "tabular_rows": int(summary.loc[summary["shape"] == "tabular", "rows"].sum()),
                "thinking_records": int(summary["thinking"].sum()),
                "string_null_fields": int(summary["string_nulls"].sum()),
                "time_sensitive_matches": int(summary["time_sensitive_matches"].sum()),
            }}, name="value")
            assert portfolio["dataset_count"] == {len(profiles)}
            assert portfolio["total_rows"] == {total_rows}
            portfolio.to_frame()
            """
        ),
        markdown(
            """
            ### Tekrar yoğunluğu veri setine göre değişiyor

            Aşağıdaki tablo, sohbet ve düz istem–cevap şemalarında kullanıcı
            istemi ile hedef cevapların normalleştirilmiş ek kopya oranlarını
            birlikte gösterir.
            """
        ),
        code(
            """
            summary.loc[
                summary["shape"].isin(["conversation", "instruction_pair"]),
                ["dataset", "rows", "prompt_duplicates_%", "answer_duplicates_%"],
            ].sort_values(
                ["prompt_duplicates_%", "answer_duplicates_%"], ascending=False
            )
            """
        ),
        markdown(
            """
            ### Yanıt uzunluğu görev biçimini etkiliyor

            Medyan ve p95 kelime sayıları bağlam bütçesi, örnek ağırlığı ve hedef
            yanıt biçimi için kullanılır; tek başına içerik doğruluğu göstermez.
            """
        ),
        code(
            """
            summary.loc[
                summary["answer_words_median"].notna(),
                ["dataset", "answer_words_median", "answer_words_p95"],
            ].sort_values("answer_words_p95", ascending=False)
            """
        ),
        markdown(
            """
            ### Şema ve hazırlık sinyalleri ayrı izleniyor

            Birebir tekrar, `thinking`, metin biçimindeki `null` ve zaman hassas
            eşleşmeleri farklı düzeltme işlemleri gerektirir.
            """
        ),
        code(
            """
            summary[[
                "dataset", "shape", "exact_duplicates", "thinking",
                "string_nulls", "time_sensitive_matches",
            ]].sort_values(
                ["string_nulls", "thinking", "time_sensitive_matches"],
                ascending=False,
            )
            """
        ),
        markdown(
            """
            ### Yapılandırılmış çıktı sözleşmesi ve çelişen hedefler

            Bazı veri setleri cevabı JSON olarak tanımlar. `json_like_broken`,
            JSON gibi başlayıp ayrıştırılamayan cevapları sayar; sözleşmenin
            fiilen ne kadar tutulduğunu gösterir. `conflicting_prompt_families`
            ise aynı normalleştirilmiş istemin birden fazla farklı cevapla
            eşleştiği aile sayısıdır ve basit tekrardan ayrı bir sorundur.
            """
        ),
        code(
            """
            summary.loc[
                (summary["json_answers"] > 0)
                | (summary["json_like_broken"] > 0)
                | (summary["conflicting_prompt_families"] > 0),
                ["dataset", "rows", "json_answers", "json_like_broken", "conflicting_prompt_families"],
            ].sort_values("json_like_broken", ascending=False)
            """
        ),
        markdown(
            """
            ### Veri setleri arası ortak metin aileleri

            Ortak istem veya cevaplar birlikte veri hazırlarken aynı şablon
            ailesi altında incelenmelidir.
            """
        ),
        code("pd.DataFrame(overlaps)"),
        markdown(
            """
            ### İncelenmiş nitel bulgular

            Bu tablo yalnız `manual_findings.json` içinde insan tarafından
            gözden geçirilmiş bulguları gösterir. Yeni veri setleri bu dosyaya
            eklenmeden burada otomatik olarak yorumlanmaz.
            """
        ),
        code(
            """
            finding_rows = []
            for dataset_id, detail in manual.get("datasets", {}).items():
                for finding in detail.get("findings", []):
                    finding_rows.append({
                        "dataset": dataset_id,
                        "severity": finding.get("severity"),
                        "evidence": finding.get("evidence"),
                        "risk": finding.get("risk"),
                        "remediation": finding.get("remediation"),
                    })
            findings = pd.DataFrame(finding_rows)
            findings
            """
        ),
        markdown(
            """
            ## Çıkarımlar

            - Her veri seti kullanım amacı, şeması ve kaynak izlenebilirliğiyle
              birlikte değerlendirilmelidir.
            - Birebir tekrarın düşük olması, normalleştirilmiş istem veya cevap
              ailelerinin dengeli olduğu anlamına gelmez.
            - Zaman hassas içerikler güncel ve doğrulanabilir kaynak katmanına
              bağlanmalıdır.
            - Sohbet, düz istem–cevap, katalog ve genel tablo verileri aynı hedef
              şemaya zorlanmadan önce ayrı hazırlık yollarından geçirilmelidir.
            - Nitel sonuçlar, satır örnekleri ve kaynak kartı incelenmeden yalnız
              otomatik profil değerlerinden türetilmemelidir.
            """
        ),
    ]
    return notebook


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    output_path = resolve_path(project_root, args.output)
    notebook = build_notebook(project_root)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.no_execute:
        nbf.write(notebook, output_path)
        print(f"Notebook written without execution: {output_path}")
        return 0

    client = NotebookClient(
        notebook,
        timeout=args.timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(project_root)}},
    )
    executed = client.execute()
    nbf.write(executed, output_path)
    print(f"Executed notebook: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
