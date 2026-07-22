# Mehmet Emre Öz

1 veri seti, toplam 1.093 satır, 2 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/nyzmemre/biyoloji-terimleri-turkce-sa`

<https://huggingface.co/datasets/nyzmemre/biyoloji-terimleri-turkce-sa>

**Ne için:** Türkçe biyoloji terimlerinin açıklandığı soru-cevap eğitimi.

**Durum:** Alan terminolojisi için kullanılabilir; cevap ailesi tekrarı düşürülmeli.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 1.093 |
| Bunun kaçı farklı cevap | 857 |
| Söz varlığı yoğunlaşması | %14 |
| Şema | conversation |
| Veri kartı | **gövdesi yok** |
| Lisans | **beyan edilmemiş** |

**Veri setini ayırt eden terimler:** `teriminin`, `kitaplarında`, `ders`, `tanım`, `denir`, `millî`, `hücreleri`, `bitkilerde`

### İyi olan

- 1.093 satırın tamamı iki mesajlı ve dolu; birebir tekrar yok.
- Terim açıklamaları kısa ve tutarlı biçimde yazılmış (medyan 15 kelime).

### Ele alınması gerekenler (2)

#### 1. Orta

**Tespit.** Normalleştirilmiş cevap tekrarı %21,6 (236/1.093); 188 cevap ailesi tekrar ediyor.

**Neden önemli.** Farklı sorular aynı tanıma bağlanınca o tanım eğitimde orantısız ağırlık kazanır.

**Ne yapmalı.** Tekrar eden tanımları tekilleştir veya soruya özgü ayrıntı ekle.

#### 2. Orta

**Tespit.** Veri kartı gövdesi yok; yalnız başlık düzeyinde bilgi var. Kaynak, üretim yöntemi ve sınırlama açıklaması bulunmuyor.

**Neden önemli.** Terimlerin kaynağı ve doğruluğu bağımsız olarak denetlenemiyor.

**Ne yapmalı.** Kaynak, üretim yöntemi, kapsam ve sınırlamaları içeren bir veri kartı yaz.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
