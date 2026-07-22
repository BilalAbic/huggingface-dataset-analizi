# Muhammed Bakır Kurt

1 veri seti, toplam 509 satır, 2 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/Endezyar/siyer_datasets`

<https://huggingface.co/datasets/Endezyar/siyer_datasets>

**Ne için:** Siyer (peygamber tarihi) alanında Türkçe soru-cevap eğitimi.

**Durum:** Alan eğitimi için kullanılabilir; kaynak belgelenmesi gerekiyor.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 509 |
| Bunun kaçı farklı cevap | 507 |
| Söz varlığı yoğunlaşması | %18 |
| Şema | conversation |
| Veri kartı | **gövdesi yok** |
| Lisans | **beyan edilmemiş** |

**Veri setini ayırt eden terimler:** `hicretin`, `müslüman`, `medine`, `efendimiz`, `kabilesi`, `peygamberimiz`, `mekke`, `müşrikler`

### İyi olan

- 509 satır, istem ve cevap tekrarı %1,0 ve %0,4; birebir tekrar yok.
- Cevaplar kısa ve doğrudan (medyan 6 kelime).

### Ele alınması gerekenler (2)

#### 1. Orta

**Tespit.** Veri kartı gövdesi yok; kaynak eser, üretim yöntemi ve mezhep/yorum çerçevesi belgelenmemiş.

**Neden önemli.** Dinî içerikte kaynak ve yorum çerçevesi belirtilmezse tartışmalı bilgi tek doğru gibi öğretilebilir.

**Ne yapmalı.** Kaynak eserleri, üretim yöntemini ve yorum çerçevesini karta yaz.

#### 2. Düşük

**Tespit.** Cevaplar çok kısa; en kısa cevap 5 karakter.

**Neden önemli.** Aşırı kısa cevaplar bağlamsız kalabilir.

**Ne yapmalı.** Kısa cevapları bağlamla genişlet.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
