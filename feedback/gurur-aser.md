# Gurur Aşer

1 veri seti, toplam 103 satır, 2 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/gururaser/ithaki-bilimkurgu-klasikleri`

<https://huggingface.co/datasets/gururaser/ithaki-bilimkurgu-klasikleri>

**Ne için:** İthaki Bilimkurgu Klasikleri serisinin katalog kaydı; yapılandırılmış dönüşüm kaynağı.

**Durum:** Sohbet verisi değil; Tool Calling ve Structured Output için dönüşüm kaynağı olarak değerli.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 103 |
| Söz varlığı yoğunlaşması | %26 |
| Şema | catalog |
| Veri kartı | var |
| Lisans | cc-by-nc-4.0 |

**Veri setini ayırt eden terimler:** `thaki`, `bilimkurgu`, `yayınları`, `klasikleri`, `dune`, `bradbury`, `mars`, `gezegeni`

### İyi olan

- 103 kayıt ve 17 alanla koleksiyondaki tek gerçek katalog şeması.
- ISBN, URL, başlık-yazar ve indirim tutarlılığı kontrolleri geçiyor; birebir tekrar yok.
- Kart kapsamı ve lisansı belirtiyor.

### Ele alınması gerekenler (2)

#### 1. Orta

**Tespit.** Eksik değerler belirli alanlarda yoğunlaşıyor: kapak_tipi 96/103, orijinal_adi 65/103, cevirmen 62/103, yayin_tarihi 12/103.

**Neden önemli.** Eksik alanlar doğrudan şablona doldurulursa boş veya yanıltıcı çıktı üretir.

**Ne yapmalı.** Eksik değer politikası tanımla; zorunlu alanları şema düzeyinde işaretle.

#### 2. Düşük

**Tespit.** Katalog fiyat ve indirim alanları içeriyor; bunlar zamana bağlı değerler.

**Neden önemli.** Fiyatlar eskir.

**Ne yapmalı.** Fiyat alanlarına çekim tarihi ekle.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
