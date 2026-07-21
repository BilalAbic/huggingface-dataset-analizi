# Proje Dosya Rehberi

Bu belge, GitHub teslim deposundaki dosyaların görevini ve birbirleriyle ilişkisini
açıklar. Depo yalnız rapor, analiz çıktısı ve yeniden çalıştırılabilir notebook
içerir; ham Hugging Face veri dosyaları yeniden yayımlanmaz.

## Nereden başlanmalı?

1. Genel sonuçlar, grafikler ve veri seti bazlı değerlendirmeler için [ana teknik raporu](HuggingFace_Veri_Setleri_Yetenek_Alani_Raporu.md) açın.
2. Yedi model yetenek alanının ayrıntıları için [eşleştirme raporunu](Model_Yetenek_Alanlari_Eslestirme_Raporu.md) okuyun.
3. Hesaplama adımları ve tablolar için [notebook kaynağını](../notebook/huggingface_dataset_quality_analysis.ipynb) veya [HTML çıktısını](../notebook/huggingface_dataset_quality_analysis.html) kullanın.
4. Sayısal sonuçları programatik kullanmak için [`outputs/`](../outputs/) ve [`ekler/`](../ekler/) klasörlerine bakın.

## Dosyaların görevleri

| Konum | İçerik |
|---|---|
| `raporlar/HuggingFace_Veri_Setleri_Yetenek_Alani_Raporu.md` | Dokuz katılımcı, üç grafik, veri seti bazlı güçlü/zayıf yönler ve teknik uygulama planı |
| `raporlar/Model_Yetenek_Alanlari_Eslestirme_Raporu.md` | Identity, Tool Call, Conversation, Instruction, Structured Output, Math ve Coding ayrıntıları |
| `raporlar/gorseller/` | JSON analiz çıktılarından üretilen üç GitHub uyumlu PNG grafik |
| `notebook/huggingface_dataset_quality_analysis.ipynb` | Çalıştırılmış analiz kaynağı ve hücre çıktıları |
| `notebook/huggingface_dataset_quality_analysis.html` | Tarayıcıda açılabilen, bağımsız notebook görünümü |
| `outputs/source_inventory.json` | Veri seti kaynakları ve sabit commit envanteri |
| `outputs/data_quality_profiles.json` | Şema, satır, boşluk, rol, tekrar ve içerik profilleri |
| `outputs/manual_findings.json` | Veri seti bazında kanıt, risk ve iyileştirme notları |
| `outputs/cross_dataset_overlap.json` | Veri setleri arasındaki ortak istem ve şablon bulguları |
| `ekler/alan_eslestirmesi.csv` | Yedi yetenek alanının satır tabanlı eşleştirmesi |
| `ekler/dataset_manifest.json` | Eşleştirmenin ayrıntılı JSON manifesti |

## Yeniden üretilebilirlik

Notebook depo kökünden çalıştırıldığında `outputs/` dosyalarını göreli yollarla
okur. Kurulum komutları ana [`README.md`](../README.md) dosyasındadır. HTML,
çalıştırılmış notebook'taki sonuçlardan üretilmiştir; kaynak notebook'ta hata
çıktısı bulunmamaktadır.

Rapor grafiklerini yeniden üretmek için depo kökünde
`python scripts/generate_report_charts.py` komutu çalıştırılabilir.
