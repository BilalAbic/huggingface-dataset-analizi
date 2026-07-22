# Semih Silistre

2 veri seti, toplam 1.383 satır, 4 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/ssilistre/carnegie-dost-kazanma-tr`

<https://huggingface.co/datasets/ssilistre/carnegie-dost-kazanma-tr>

**Ne için:** Dale Carnegie'nin ilkelerinden türetilmiş Türkçe talimat-takip ve muhakeme eğitimi.

**Durum:** İletişim ve ikna alanı için kullanılabilir; telif notu doğrulanmalı.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 1.001 |
| Bunun kaçı farklı cevap | 998 |
| Söz varlığı yoğunlaşması | %10 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | cc-by-4.0 |

**Veri setini ayırt eden terimler:** `carnegie`, `lincoln`, `eleştiri`, `nsanlar`, `takdir`, `müşteri`, `samimi`, `schwab`

### İyi olan

- 1.001 satır, birebir tekrar yok, cevap tekrarı %0,3 ile çok düşük.
- Tüm 1.001 asistan mesajında thinking izi var.
- Kart, kayıtların kitap metnini içermediğini ve sıfırdan yazıldığını açıkça belirtiyor.

### Ele alınması gerekenler (2)

#### 1. Orta

**Tespit.** Kart, kitaptan uzun birebir alıntı bulunmadığını beyan ediyor. Bu analiz yapısal kontroller yaptı; kaynak kitapla metin karşılaştırması yapılmadı.

**Neden önemli.** Telif uyumu beyana dayanıyor, bağımsız olarak doğrulanmadı.

**Ne yapmalı.** Kaynak metinle otomatik n-gram örtüşme kontrolü çalıştır ve sonucu karta ekle.

#### 2. Düşük

**Tespit.** Metinde 154 zaman hassasiyetli eşleşme var.

**Neden önemli.** İlkeler zamansız olsa da örnekler tarihe demirlenebilir.

**Ne yapmalı.** Tarihli örnekleri gözden geçir.

## `hf/ssilistre/semih-silistre-ai-identity`

<https://huggingface.co/datasets/ssilistre/semih-silistre-ai-identity>

**Ne için:** Model kimliğini Semih Silistre AI personasına hizalamak.

**Durum:** Kimlik eğitimi için kullanılabilir; koleksiyondaki en iyi belgelenmiş kimlik setlerinden.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 382 |
| Bunun kaçı farklı cevap | 379 |
| Söz varlığı yoğunlaşması | %13 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | cc-by-4.0 |

**Veri setini ayırt eden terimler:** `silistre`, `semih`, `konuşma`, `lora`, `beni`, `eğitildim`, `benim`, `seni`

### İyi olan

- 382 satır, istem tekrarı %0,0, cevap tekrarı %0,8; birebir tekrar yok.
- Tüm 382 asistan mesajında thinking izi var.
- Kart, modelin bilinç, duygu, hafıza ve internet erişimi iddia etmemesi gibi açık dürüstlük sınırları tanımlıyor.

### Ele alınması gerekenler (2)

#### 1. Orta

**Tespit.** Kimlik istemleri diğer kimlik veri setleriyle paylaşılıyor; bu set koleksiyondaki en çok örtüşen kimlik kaynağı.

**Neden önemli.** Birden çok kimlik seti birlikte eğitilirse aynı soruya farklı isim ve geliştirici öğretilir.

**Ne yapmalı.** Kimlik setlerini birleştirme; tek personayı seç.

#### 2. Düşük

**Tespit.** Metinde 43 zaman hassasiyetli eşleşme var.

**Neden önemli.** Kimlik cevaplarının tarihe demirlenmesi eskime yaratır.

**Ne yapmalı.** Tarih ifadelerini kaldır.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
