# Seda Nur Yazıcı

2 veri seti, toplam 12.358 satır, 5 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/sedayzc/trendyol-electronics-products-features-and-comments`

<https://huggingface.co/datasets/sedayzc/trendyol-electronics-products-features-and-comments>

**Ne için:** Trendyol elektronik ürünlerinin özellik ve yorum kayıtları; yapılandırılmış dönüşüm kaynağı.

**Durum:** Sohbet verisi değil; ürün karşılaştırma ve Tool Calling için dönüşüm kaynağı.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 500 |
| Söz varlığı yoğunlaşması | %22 |
| Şema | tabular |
| Veri kartı | **gövdesi yok** |
| Lisans | **beyan edilmemiş** |

**Veri setini ayırt eden terimler:** `ürün`, `gayet`, `ederim`, `teşekkür`, `güzel`, `satıcı`, `paketleme`, `geldi`

### İyi olan

- 500 kayıt ve 13 sütunla koleksiyondaki iki yapılandırılmış kaynaktan biri.
- Kayıtlar iç içe yapılar taşıyor: categories listesi, attributes sözlüğü ve reviews listesi.
- Birebir tekrar yok.

### Ele alınması gerekenler (3)

#### 1. Yüksek

**Tespit.** Veri kartı yok. Kazıma tarihi, kapsam ölçütü ve lisans belirtilmemiş; metinde 398 zaman hassasiyetli eşleşme var.

**Neden önemli.** Fiyat, puan ve yorum sayısı kazıma anına aittir ve hızla eskir; kaynağın kullanım koşulları belgelenmemiş.

**Ne yapmalı.** Kazıma tarihi, kapsam ve lisans bilgisini içeren bir veri kartı ekle.

#### 2. Orta

**Tespit.** Eksik değerler alanlara dağılmış: comment_count 137/500, review_page_count 137/500.

**Neden önemli.** Eksik alanlar dönüşüm şablonlarında boş metin üretir.

**Ne yapmalı.** Eksik değer politikası tanımla; zorunlu alanları işaretle.

#### 3. Orta

**Tespit.** Sayısal görünen alanlar (fiyat, puan, yorum sayısı) dize olarak saklanmış; favorite_count alanı yer yer 'Favori Sayısı Bulunamadı' metnini taşıyor.

**Neden önemli.** Sayısal işlem yapan boru hattı bu alanlarda hata verir veya sessizce yanlış sonuç üretir.

**Ne yapmalı.** Sayısal alanları tiplendirip eksik değerleri gerçek null yap.

## `hf/sedayzc/turkish-electronics-product-comparison-recommendation`

<https://huggingface.co/datasets/sedayzc/turkish-electronics-product-comparison-recommendation>

**Ne için:** Türkçe elektronik ürün karşılaştırma ve öneri sohbetleri için SFT.

**Durum:** Olduğu gibi kullanılmamalı; sürüm ayrıştırması ve tekilleştirme yapılmadan satır sayısı yanıltıcı.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 11.858 |
| Bunun kaçı farklı cevap | 5.662 |
| Söz varlığı yoğunlaşması | %32 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | other |

**Veri setini ayırt eden terimler:** `16gb`, `512gb`, `intel`, `ryzen`, `lenovo`, `core`, `freedos`, `gaming`

### İyi olan

- 11.858 satırla üçüncü en büyük kaynak; ürün adı, fiyat ve teknik özellik içeren somut cevaplar.
- Veri kartı V1 ve V2 sürümlerini, üretim yöntemini ve fine-tuning'de hangisinin kullanıldığını açıklıyor.

### Ele alınması gerekenler (2)

#### 1. Kritik

**Tespit.** Depo aynı derlemenin iki sürümünü yan yana tutuyor (data/recommendation_chat_dataset.json ve _v2.json) ve Dataset Viewer bunları tek train split'inde birleştiriyor. Sonuç: 11.858 satırın 4.851 tanesi birebir tekrar; normalleştirilmiş cevap tekrarı %52,2, istem tekrarı %41,4.

**Neden önemli.** Depoyu tek veri seti sayan herkes aynı konuşmaları iki kez eğitime sokar; satır sayısı gerçek içerik hacmini yaklaşık iki katı gösterir.

**Ne yapmalı.** V1 ve V2'yi ayrı config veya ayrı depoya taşı; kartta eğitim için tek geçerli sürümü belirt.

#### 2. Orta

**Tespit.** 55 istem ailesi farklı cevaplarla eşleşiyor (110 satır) ve metinde 699 zaman hassasiyetli eşleşme var; bunlar ağırlıklı olarak fiyat ve model adı ifadeleri.

**Neden önemli.** Fiyat ve stok bilgisi hızla eskir; aynı soruya çelişen öneriler öğretilebilir.

**Ne yapmalı.** Fiyatları tarih damgasıyla ver veya cevaptan çıkarıp araç çağrısına devret.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
