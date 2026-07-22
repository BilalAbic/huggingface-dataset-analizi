# Mert Ali Alkan

1 veri seti, toplam 186 satır, 1 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/Mer1Alii/TR-ECommerce-CustomerSupport-Instructions`

<https://huggingface.co/datasets/Mer1Alii/TR-ECommerce-CustomerSupport-Instructions>

**Ne için:** Türkçe e-ticaret müşteri destek talimat-takip eğitimi.

**Durum:** Müşteri hizmetleri davranışı için kullanılabilir; politika içeriği doğrulanmalı.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 186 |
| Bunun kaçı farklı cevap | 186 |
| Söz varlığı yoğunlaşması | %14 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | apache-2.0 |

**Veri setini ayırt eden terimler:** `kargo`, `sipariş`, `fatura`, `iade`, `satıcı`, `size`, `ürünün`, `teslim`

### İyi olan

- 186 satır, istem ve cevap tekrarı %0,0 ve %0,0; birebir tekrar yok.
- Tüm 186 asistan mesajında doğal paragraf biçiminde muhakeme var.
- Kart 20 kategoriyi ve dağılımını belgeliyor.

### Ele alınması gerekenler (1)

#### 1. Orta

**Tespit.** Cevaplar iade süresi ve kargo gibi politika ifadeleri içeriyor; metinde 31 zaman hassasiyetli eşleşme var. Politikalar satıcıya göre değişir.

**Neden önemli.** Model bir mağazanın politikasını genel kural olarak öğrenebilir.

**Ne yapmalı.** Politika değerlerini değişken hâline getir veya araç çağrısına devret.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
