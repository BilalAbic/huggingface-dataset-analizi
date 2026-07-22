# Ege Ertekin

1 veri seti, toplam 177 satır, 3 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/Egertekin/marvel-domain-dataset`

<https://huggingface.co/datasets/Egertekin/marvel-domain-dataset>

**Ne için:** Marvel evreni ve çizgi roman tarihi üzerine Türkçe soru-cevap.

**Durum:** Mevcut hâliyle eğitim havuzuna alınmamalı; istem çeşitliliği çok düşük.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 177 |
| Bunun kaçı farklı cevap | 153 |
| Söz varlığı yoğunlaşması | %20 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | **beyan edilmemiş** |

**Veri setini ayırt eden terimler:** `örümcek`, `spider`, `marvel`, `adam`, `parker`, `peter`, `wolverine`, `comics`

> 76% of prompts repeat, so the user turn is largely a fixed instruction. Terms may describe the instruction rather than the subject.

### İyi olan

- 177 satırın tamamı geçerli user-assistant sırasına sahip.
- Uzun cevaplar alan terminolojisi ve karakter tarihi açısından zengin (medyan 56 kelime).
- Kart Wikipedia kazıma ve elle genişletme yöntemini açıklıyor.

### Ele alınması gerekenler (3)

#### 1. Yüksek

**Tespit.** Normalleştirilmiş istem tekrarı %75,7 (134/177); tek bir soru 83 kez tekrar ediyor ve yalnız 7 farklı istem ailesi var.

**Neden önemli.** Model soru çeşitliliği öğrenemez; aynı soru eğitimde orantısız ağırlık kazanır.

**Ne yapmalı.** Soru üretimini çeşitlendir, tekrar kümelerini birleştir.

#### 2. Orta

**Tespit.** Veri kartı instruction, input ve output biçimini tarif ediyor; gerçek şema messages.

**Neden önemli.** Kartı temel alan boru hattı hatalı alan adlarıyla çalışır.

**Ne yapmalı.** Kartı gerçek şemaya göre düzelt.

#### 3. Orta

**Tespit.** Kaynak sayfa URL'leri, revizyon kimlikleri ve satır düzeyinde atıf zinciri yok.

**Neden önemli.** Kazınmış içeriğin doğruluğu ve telif durumu izlenemiyor.

**Ne yapmalı.** Kaynak URL ve revizyon alanı ekle.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
