# Eren Yanic

1 veri seti, toplam 1.000 satır, 2 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/Erenyanic/seasoned-advice-dataset`

<https://huggingface.co/datasets/Erenyanic/seasoned-advice-dataset>

**Ne için:** Yemek pişirme ve gıda bilimi alanında iki dilli talimat-takip ve muhakeme eğitimi.

**Durum:** Koleksiyonun en temiz kaynaklarından; paralel çeviri yapısı belgelenerek kullanılabilir.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 1.000 |
| Bunun kaçı farklı cevap | 1.000 |
| Söz varlığı yoğunlaşması | %6 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | cc-by-sa-4.0 |

**Veri setini ayırt eden terimler:** `water`, `cooking`, `pişirme`, `flavor`, `recipe`, `meat`, `food`, `taste`

### İyi olan

- 1.000 satır, istem ve cevap tekrarı %0,0 ve %0,0; birebir tekrar yok.
- İçerik Stack Exchange üzerinden toplanmış gerçek insan sorusu ve cevabı; model üretimi değil.
- Tüm 1.000 asistan mesajında muhakeme izi var; cevaplar ayrıntılı (medyan 121.0 kelime).

### Ele alınması gerekenler (2)

#### 1. Orta

**Tespit.** english ve turkish bölümleri paralel çeviri (english=500, turkish=500); kart n'inci satırın aynı konuşma olduğunu belirtiyor. Ölçüm bunu doğruluyor: bölümler arası birebir tekrar yok, çünkü metinler farklı dillerde.

**Neden önemli.** Toplam satır sayısı benzersiz konuşma sayısının iki katı görünür; iki bölüm birlikte eğitilirse aynı içerik iki kez öğrenilir.

**Ne yapmalı.** Kapsam raporlarında 500 benzersiz konuşma olarak belirt; tek dil eğitiminde tek bölüm kullan.

#### 2. Düşük

**Tespit.** Metinde 894 URL eşleşmesi var; bunlar kaynak Stack Exchange bağlantıları.

**Neden önemli.** Bağlantılar bozulabilir ve cevaplarda dış kaynağa bağımlılık yaratır.

**Ne yapmalı.** URL'leri ayrı bir kaynak alanına taşı.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
