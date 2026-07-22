# Salih Dede

1 veri seti, toplam 1.211 satır, 2 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/SalihHub/trendyol-marangoz-urun-asistan-qa`

<https://huggingface.co/datasets/SalihHub/trendyol-marangoz-urun-asistan-qa>

**Ne için:** E-ticaret ürün sorularına satıcı üslubuyla cevap veren asistan eğitimi.

**Durum:** Müşteri hizmetleri davranışı için kullanılabilir; sentetik thinking alanı ayrıştırılmalı.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 1.211 |
| Bunun kaçı farklı cevap | 1.028 |
| Söz varlığı yoğunlaşması | %28 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | other |

**Veri setini ayırt eden terimler:** `merhaba`, `efendim`, `ürün`, `dileriz`, `müşterimiz`, `ölçüleri`, `acaba`, `sena`

### İyi olan

- 1.211 satır gerçek müşteri sorusu ve gerçek satıcı cevabı içeriyor; birebir tekrar yok.
- Kart, thinking alanının LLM ile üretilmiş sentetik muhakeme olduğunu ve satıcının gerçek iç sesi olmadığını açıkça yazıyor.

### Ele alınması gerekenler (2)

#### 1. Orta

**Tespit.** Normalleştirilmiş cevap tekrarı %15,1 (183/1.211); en sık cevap 16 kez geçiyor. Cevaplar kısa: medyan 7 kelime, en kısa cevap 10 karakter.

**Neden önemli.** Kalıplaşmış kısa satıcı cevapları modele bilgi taşımayan genel yanıtlar öğretebilir.

**Ne yapmalı.** Kalıp cevapları tekilleştir; bilgi taşıyan cevapları ayrı ağırlıkla kullan.

#### 2. Orta

**Tespit.** Asistan cevabı gerçek satıcı metni, thinking alanı ise 1.211 kayıtta sentetik üretim.

**Neden önemli.** Sentetik muhakeme gerçek cevabı doğru açıklamayabilir; ikisi birlikte eğitilirse tutarsızlık öğrenilir.

**Ne yapmalı.** Thinking alanını örneklemle doğrula veya yalnız nihai cevapla eğit.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
