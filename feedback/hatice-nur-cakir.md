# Hatice Nur Çakır

1 veri seti, toplam 220 satır, 2 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/haticenurcakr/turkish-classic-books-qa`

<https://huggingface.co/datasets/haticenurcakr/turkish-classic-books-qa>

**Ne için:** Türk klasik edebiyatı üzerine soru-cevap eğitimi.

**Durum:** Küçük ölçekli alan tohumu; belgelenmeden kullanılmamalı.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 220 |
| Bunun kaçı farklı cevap | 216 |
| Söz varlığı yoğunlaşması | %45 |
| Şema | conversation |
| Veri kartı | **gövdesi yok** |
| Lisans | **beyan edilmemiş** |

**Veri setini ayırt eden terimler:** `eserinin`, `edebiyatında`, `eserde`, `yayımlanmıştır`, `türk`, `eser`, `kimdir`, `yazarı`

### İyi olan

- 220 satır, istem tekrarı %0,0, cevap tekrarı %1,8; birebir tekrar yok.
- Şema sade: yalnız role ve content alanları.

### Ele alınması gerekenler (2)

#### 1. Yüksek

**Tespit.** Veri kartı yok. Kaynak, üretim yöntemi, lisans ve sınırlama bilgisi bulunmuyor.

**Neden önemli.** İçeriğin kökeni ve doğruluğu denetlenemiyor.

**Ne yapmalı.** Kaynak ve üretim yöntemini belgeleyen bir veri kartı ekle.

#### 2. Düşük

**Tespit.** Cevaplar çok kısa (medyan 9.5 kelime, en kısa 26 karakter).

**Neden önemli.** Kısa cevaplar edebiyat sorularında bağlam taşımayabilir.

**Ne yapmalı.** Cevapları eser ve bağlam bilgisiyle genişlet.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
