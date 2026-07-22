# Görkem Ergüne

1 veri seti, toplam 429 satır, 3 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/gorkemergune/ayarlicazhocam_finetune`

<https://huggingface.co/datasets/gorkemergune/ayarlicazhocam_finetune>

**Ne için:** Mühendislik, yazılım ve sınav hazırlığı alanında iki dilli asistan eğitimi.

**Durum:** Mevcut hâliyle kullanılmamalı; en az bir kayıtta alan dışı kazınmış içerik var.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 429 |
| Bunun kaçı farklı cevap | 425 |
| Söz varlığı yoğunlaşması | %7 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | mit |

**Veri setini ayırt eden terimler:** `gorkem`, `projects`, `python`, `github`, `görkem`, `learning`, `hugging`, `face`

### İyi olan

- 429 satır ve dil etiketi taşıyan bir language sütunu var.
- Tüm 429 asistan mesajında thinking alanı var.

### Ele alınması gerekenler (3)

#### 1. Kritik

**Tespit.** Bir asistan cevabı 65.074 karakter uzunluğunda ve 'Can you recommend a good HTML project for learning?' sorusuna karşılık GitHub deposundan kazınmış, konuyla ilgisiz siyasi içerik barındırıyor. Aynı sette 4 birebir tekrar satır ve 34 çelişen istem ailesi var.

**Neden önemli.** Alan dışı ve siyasi olarak hassas kazınmış içerik eğitim havuzuna girerse model bunu bir HTML öğrenme önerisi olarak üretebilir.

**Ne yapmalı.** Uzunluk ve alan dışılık filtresi uygula; kazınmış GitHub içeriğini kaldır veya alanla ilgili olanları elle onayla.

#### 2. Yüksek

**Tespit.** Veri kartı örnek biçim olarak instruction, input ve output alanlarını gösteriyor; gerçek şema ise messages ve language sütunları.

**Neden önemli.** Kartı okuyup boru hattı yazan kullanıcı hatalı alan adlarıyla çalışır.

**Ne yapmalı.** Kartı gerçek şemaya göre düzelt.

#### 3. Orta

**Tespit.** Normalleştirilmiş istem tekrarı %10,7 (46/429).

**Neden önemli.** Aynı istemin tekrarı eğitimde ağırlık dengesizliği yaratır.

**Ne yapmalı.** Tekrarları tekilleştir.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
