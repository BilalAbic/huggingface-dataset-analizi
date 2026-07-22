# Yusuf Şimşek

2 veri seti, toplam 1.444 satır, 2 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/YusufSimsek/llm-kisisellestirme`

<https://huggingface.co/datasets/YusufSimsek/llm-kisisellestirme>

**Ne için:** Model kimliğini Yusuf Şimşek personasına hizalamak.

**Durum:** Küçük kimlik tohumu; belgelenmesi gerekiyor.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 46 |
| Bunun kaçı farklı cevap | 46 |
| Söz varlığı yoğunlaşması | %44 |
| Şema | conversation |
| Veri kartı | **gövdesi yok** |
| Lisans | **beyan edilmemiş** |

**Veri setini ayırt eden terimler:** `yusuf`, `fırat`, `cumhurbaşkanı`, `proje`, `projelerinin`, `hedefleri`, `modelleri`, `zekâ`

### İyi olan

- 46 satır, istem ve cevap tekrarı %0,0 ve %0,0; birebir tekrar yok.

### Ele alınması gerekenler (1)

#### 1. Orta

**Tespit.** Veri kartı yok ve yalnız 46 satır var.

**Neden önemli.** Amaç ve kapsam belgelenmemiş; tek başına kimlik eğitimi için yetersiz.

**Ne yapmalı.** Veri kartı ekle ve sınır davranışı örnekleriyle genişlet.

## `hf/YusufSimsek/turkce-atasozleri-dataset`

<https://huggingface.co/datasets/YusufSimsek/turkce-atasozleri-dataset>

**Ne için:** Türkçe atasözlerinin anlamını açıklayan soru-cevap eğitimi.

**Durum:** Dil ve kültür alanı için kullanılabilir; cevap tekrarı azaltılmalı.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 1.398 |
| Bunun kaçı farklı cevap | 446 |
| Söz varlığı yoğunlaşması | %18 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | cc-by-sa-4.0 |

**Veri setini ayırt eden terimler:** `atasözünün`, `anlatmaktadır`, `anlamı`, `kimse`, `allah`, `sanır`, `kişi`, `akılsız`

### İyi olan

- 1.398 satır, birebir tekrar yok, tüm mesajlar dolu.
- Tüm 1.398 asistan mesajında thinking alanı var.
- Kart, 466 atasözü ve her biri için üç soru biçimi tasarımını açıkça belgeliyor.

### Ele alınması gerekenler (1)

#### 1. Yüksek

**Tespit.** Normalleştirilmiş cevap tekrarı %68,1 (952/1.398); 446 cevap ailesi tekrar ediyor ve veri seti gerçekte 446 farklı cevap içeriyor. Yakın-tekrar (en az %85 token örtüşmesi) oranı %68,0, yani tekrarlar yeniden yazılarak da gizlenmemiş. Bu, bir atasözü için üç farklı sorunun aynı açıklamayı hedef göstermesinden kaynaklanıyor.

**Neden önemli.** Model soruyu değil atasözünü ezberler ve soru biçimindeki değişime duyarsızlaşır.

**Ne yapmalı.** Her soru biçimi için farklı vurguda cevap yaz veya tekrarları tek kayda indir.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
