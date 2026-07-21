# Türkçe Hugging Face Veri Setleri: Kalite ve Yetenek Alanı Analizi

Bu depo, dokuz Türkçe veya Türkçe odaklı Hugging Face veri setinin kalite
profillerini ve model yetenek alanı eşleştirmesini içerir. Toplam **3.119 satır**;
Identity, Tool Call, Conversation, Instruction, Structured Output, Math ve Coding
alanları açısından incelenmiştir.

## Raporlar ve analiz

| İçerik | Biçim | Bağlantı |
|---|---|---|
| Toplu teknik değerlendirme | Markdown | [Ana raporu aç](raporlar/HuggingFace_Veri_Setleri_Yetenek_Alani_Raporu.md) |
| Model yetenek alanı eşleştirmesi | Markdown | [Eşleştirme raporunu aç](raporlar/Model_Yetenek_Alanlari_Eslestirme_Raporu.md) |
| Proje ve dosya rehberi | Markdown | [Dosya rehberini aç](raporlar/Proje_Dosya_Rehberi.md) |
| Çalıştırılmış kalite analizi | HTML | [Notebook HTML çıktısını aç](notebook/huggingface_dataset_quality_analysis.html) |
| Yeniden çalıştırılabilir analiz | Jupyter Notebook | [Notebook kaynağını aç](notebook/huggingface_dataset_quality_analysis.ipynb) |

## Teknik özet

- Sekiz sohbet veri setinde 3.016, yapılandırılmış katalogda 103 satır vardır.
- Sohbet kayıtlarında boş içerik veya geçersiz rol tespit edilmemiştir.
- Etiketli tool call ve gerçek çok turlu konuşma örneği bulunmamaktadır.
- 1.136 asistan mesajında ayrı `thinking` içeriği vardır.
- Şahin Identity verisinde 462 alan gerçek `null` yerine `"null"` dizesidir.
- Marvel ve felsefe istemlerinde; biyoloji ve Şahin Identity cevaplarında yüksek
  normalleştirilmiş tekrar yoğunluğu görülmüştür.

Ayrıntılı kanıtlar [`outputs/`](outputs/) dosyalarında, alan eşleştirmeleri ise
[`ekler/`](ekler/) altında makinece okunabilir biçimde sunulmuştur.

## İncelenen veri setleri

| Katılımcı | Veri seti | Satır |
|---|---|---:|
| Ali Furkan Ak | [aliFurkan123/cultural-questions-dataset](https://huggingface.co/datasets/aliFurkan123/cultural-questions-dataset) | 500 |
| Ayşe Nur Yeşilova | [Aysenur44/namaz-vakti-identity-tr](https://huggingface.co/datasets/Aysenur44/namaz-vakti-identity-tr) | 4 |
| Ege Ertekin | [Egertekin/marvel-domain-dataset](https://huggingface.co/datasets/Egertekin/marvel-domain-dataset) | 177 |
| Gurur Aşer | [gururaser/ithaki-bilimkurgu-klasikleri](https://huggingface.co/datasets/gururaser/ithaki-bilimkurgu-klasikleri) | 103 |
| Mehmet Emre Öz | [nyzmemre/biyoloji-terimleri-turkce-sa](https://huggingface.co/datasets/nyzmemre/biyoloji-terimleri-turkce-sa) | 1.093 |
| Mert Ali Alkan | [Mer1Alii/TR-ECommerce-CustomerSupport-Instructions](https://huggingface.co/datasets/Mer1Alii/TR-ECommerce-CustomerSupport-Instructions) | 186 |
| Muhammet Yusuf Kaydın | [yoitsmeyusuf/felsefe_finetune](https://huggingface.co/datasets/yoitsmeyusuf/felsefe_finetune) | 529 |
| Mustafa Özdemir | [namruni/meb-ogretmen-soru-cevap](https://huggingface.co/datasets/namruni/meb-ogretmen-soru-cevap) | 450 |
| Serhat Kılıç | [sk75/sahin_identity](https://huggingface.co/datasets/sk75/sahin_identity) | 77 |

## Depo yapısı

```text
.
├── README.md
├── raporlar/
│   ├── HuggingFace_Veri_Setleri_Yetenek_Alani_Raporu.md
│   ├── Model_Yetenek_Alanlari_Eslestirme_Raporu.md
│   ├── Proje_Dosya_Rehberi.md
│   └── gorseller/
├── notebook/
│   ├── huggingface_dataset_quality_analysis.ipynb
│   └── huggingface_dataset_quality_analysis.html
├── outputs/
│   ├── cross_dataset_overlap.json
│   ├── data_quality_profiles.json
│   ├── manual_findings.json
│   └── source_inventory.json
├── ekler/
│   ├── alan_eslestirmesi.csv
│   └── dataset_manifest.json
├── scripts/
│   └── generate_report_charts.py
└── requirements.txt
```

## Notebook'u çalıştırma

Python 3.12 ile depo kökünde:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m jupyter nbconvert --execute --to notebook --inplace notebook\huggingface_dataset_quality_analysis.ipynb
.\.venv\Scripts\python -m jupyter nbconvert --to html --output-dir notebook notebook\huggingface_dataset_quality_analysis.ipynb
```

Notebook, `outputs/` altındaki doğrulanmış JSON dosyalarını okur. Ham veri setleri
bu teslim deposunda yeniden dağıtılmaz; yukarıdaki resmî Hugging Face sayfalarından
erişilir. Veri setlerinin kullanım koşulları kendi kaynak sayfalarındaki bilgilere
tabidir.
