# Berk Birkan

2 veri seti, toplam 2.000 satır, 4 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/berkbirkan/turkish-x-engagement-quotes`

<https://huggingface.co/datasets/berkbirkan/turkish-x-engagement-quotes>

**Ne için:** Türkçe X gönderilerine özgün yorum ekleyen kısa quote üretimi.

**Durum:** Sosyal medya üslubu için kullanılabilir; istem şablonu tekrarı ve platform koşulları dikkate alınmalı.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 1.000 |
| Bunun kaçı farklı cevap | 1.000 |
| Söz varlığı yoğunlaşması | %22 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | other |

**Veri setini ayırt eden terimler:** `quote`, `içgörü`, `alıntılarken`, `özgün`, `yorum`, `aşağıdaki`, `ekleyen`, `gönderisini`

> 68% of prompts repeat, so the user turn is largely a fixed instruction. Terms may describe the instruction rather than the subject.

### İyi olan

- 1.000 satır, üç bölüme ayrılmış (train=854, validation=105, test=41); birebir tekrar yok.
- Kart üretim yöntemini, kategori ve niyet dağılımını, güvenlik elemesini ve kullanıcı adlarının çıkarıldığını belgeliyor.
- Kart, aynı ana gönderinin yalnız tek bölümde tutulduğunu belirtiyor; ölçümler bunu doğruluyor (bölümler arası tekrar yok).

### Ele alınması gerekenler (2)

#### 1. Yüksek

**Tespit.** Normalleştirilmiş istem tekrarı %67,7 (677/1.000) ve 229 istem ailesi farklı cevaplarla eşleşiyor (906 satır). İstemler ortak bir talimat şablonu artı gönderi metninden oluştuğu için aynı gönderi birden çok kez hedefleniyor.

**Neden önemli.** Model şablonu ezberler; aynı gönderiye farklı quote'lar çelişkili hedef olarak görünebilir.

**Ne yapmalı.** Gönderi başına tek örnek tut veya çoklu hedefleri açıkça çeşitlilik örneği olarak etiketle.

#### 2. Orta

**Tespit.** Metinde 414 URL ve 141 zaman hassasiyetli eşleşme var; içerik güncel gündeme bağlı.

**Neden önemli.** Gündem içeriği hızla eskir ve platform koşulları yeniden dağıtımı kısıtlayabilir.

**Ne yapmalı.** Kartta belirtilen X koşulları ve kişisel veri yükümlülüklerini kullanım öncesi doğrula.

## `hf/berkbirkan/turkish-x-engagement-replies`

<https://huggingface.co/datasets/berkbirkan/turkish-x-engagement-replies>

**Ne için:** Türkçe X gönderilerine bağlama uygun kısa reply üretimi.

**Durum:** Sosyal medya üslubu için kullanılabilir; istem şablonu tekrarı ve platform koşulları dikkate alınmalı.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 1.000 |
| Bunun kaçı farklı cevap | 1.000 |
| Söz varlığı yoğunlaşması | %19 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | other |

**Veri setini ayırt eden terimler:** `reply`, `aşağıdaki`, `bağlama`, `doğal`, `gönderisine`, `uygun`, `profdemirtas`, `kısa`

> 70% of prompts repeat, so the user turn is largely a fixed instruction. Terms may describe the instruction rather than the subject.

### İyi olan

- 1.000 satır, üç bölüme ayrılmış (train=823, validation=126, test=51); birebir tekrar yok.
- Kart üretim yöntemini, güvenlik elemesini ve kullanıcı adlarının çıkarıldığını belgeliyor.

### Ele alınması gerekenler (2)

#### 1. Yüksek

**Tespit.** Normalleştirilmiş istem tekrarı %70,1 (701/1.000) ve 212 istem ailesi farklı cevaplarla eşleşiyor (913 satır).

**Neden önemli.** Model talimat şablonunu ezberler; aynı gönderiye farklı yanıtlar çelişkili hedef görünümü verir.

**Ne yapmalı.** Gönderi başına tek örnek tut veya çoklu hedefi çeşitlilik olarak etiketle.

#### 2. Orta

**Tespit.** Metinde 472 URL ve 120 zaman hassasiyetli eşleşme var.

**Neden önemli.** Gündem içeriği hızla eskir; yeniden dağıtım platform koşullarına tabi.

**Ne yapmalı.** Kullanım öncesi X koşullarını ve kişisel veri yükümlülüklerini doğrula.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
