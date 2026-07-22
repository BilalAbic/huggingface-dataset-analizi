# Uunan

> Bu ad, gönderi formunda doğrulanabilir bir tam ad bulunmadığı için
> Hugging Face hesap adıdır. Düzeltmek isterseniz bildirin.

1 veri seti, toplam 34.244 satır, 2 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/Uunan/turkish-cuisine-qa`

<https://huggingface.co/datasets/Uunan/turkish-cuisine-qa>

**Ne için:** Türk mutfağı yemekleri üzerine soru-cevap ve düşünce zinciri (CoT) eğitimi.

**Durum:** Alan eğitimi için kullanılabilir; olgusal doğrulama ve satır düzeyinde kaynak alanı eklenmeli.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 34.244 |
| Bunun kaçı farklı cevap | 34.227 |
| Söz varlığı yoğunlaşması | %18 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | cc-by-nc-4.0 |

**Veri setini ayırt eden terimler:** `pişirilir`, `tarifinde`, `kaşığı`, `bardağı`, `tereyağı`, `çorbası`, `soğan`, `biber`

### İyi olan

- 34.244 satırla koleksiyonun en büyük kaynağı; birebir satır tekrarı yok.
- Tüm 34.244 asistan mesajında ayrı thinking alanı var; CoT eğitimi için tutarlı.
- Veri kartı üretim zincirini (web scraping, Gemma ile QA, Gemini ile thinking) açıkça yazıyor.

### Ele alınması gerekenler (2)

#### 1. Yüksek

**Tespit.** Kart 2.714 benzersiz yemekten 34.244 soru-cevap üretildiğini belirtiyor; yemek başına ortalama 12,6 kayıt düşüyor. Buna rağmen tekrar düşük: normalleştirilmiş cevap tekrarı %0,1, yakın-tekrar (en az %85 token örtüşmesi) %1,5 (499 satır). Yani yemek başına üretilen sorular birbirinin kopyası değil. Cevaplar yine de sentetik ve satır düzeyinde kaynak veya doğrulama alanı yok.

**Neden önemli.** Bir yemeğe ait hatalı bir olgu onlarca kayıtta tekrarlanarak eğitimde orantısız ağırlık kazanabilir.

**Ne yapmalı.** Yemek kimliğine göre kümele, örneklemi dengele ve bağımsız olgu doğrulaması uygula.

#### 2. Orta

**Tespit.** Asistan cevaplarının medyan uzunluğu 10.0 kelime, p95 78.0 kelime; thinking metinleri nihai cevaptan ayrı alanda tutulmuş.

**Neden önemli.** Thinking alanı doğrudan eğitilirse model gereksiz uzun ve özel muhakeme biçimini ezberleyebilir.

**Ne yapmalı.** Yalnız nihai cevabı içeren türev sürüm üret; thinking'i ayrı aşamada kullan.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
