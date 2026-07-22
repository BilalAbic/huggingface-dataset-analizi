# Muhammet Yusuf Kaydın

1 veri seti, toplam 529 satır, 2 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/yoitsmeyusuf/felsefe_finetune`

<https://huggingface.co/datasets/yoitsmeyusuf/felsefe_finetune>

**Ne için:** Öznel felsefi söylem ve tartışma üslubu eğitimi.

**Durum:** Öznel söylem için kullanılabilir; olgusal kaynak olarak uygun değil.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 529 |
| Bunun kaçı farklı cevap | 529 |
| Söz varlığı yoğunlaşması | %7 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | **beyan edilmemiş** |

**Veri setini ayırt eden terimler:** `felsefe`, `kimdir`, `metafizik`, `voltaire`, `hobbes`, `wittgenstein`, `filozof`, `sartre`

> İstemlerin %77'i tekrar ediyor, yani kullanıcı turu büyük
> ölçüde sabit bir talimat. Yukarıdaki terimler konuyu değil talimatı
> anlatıyor olabilir.

### İyi olan

- 529 satır, birebir tekrar yok, cevap tekrarı %0,0.
- Cevap uzunluğu geniş bir yelpazede (medyan 35 kelime, p95 353.6).

### Ele alınması gerekenler (2)

#### 1. Yüksek

**Tespit.** Normalleştirilmiş istem tekrarı %76,6 (405/529); 58 istem ailesi farklı cevaplarla eşleşiyor ve bu aileler 463 satırı kapsıyor.

**Neden önemli.** Aynı soru farklı ve kimi zaman çelişen felsefi görüşlerle eşleşiyor; model tutarsız hedef öğrenir.

**Ne yapmalı.** Aynı soruya verilen farklı görüşleri açıkça çoklu-bakış örneği olarak etiketle.

#### 2. Orta

**Tespit.** İçerik birinci tekil şahıs görüş bildiriyor; satır düzeyinde kaynak veya filozof atfı yok.

**Neden önemli.** Öznel görüş olgusal bilgi gibi öğrenilebilir.

**Ne yapmalı.** Görüş ve olgu ayrımını alan düzeyinde işaretle.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
