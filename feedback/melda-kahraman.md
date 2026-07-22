# Melda Kahraman

1 veri seti, toplam 1.020 satır, 2 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/meldakahramann/animasyon-domain-dataset`

<https://huggingface.co/datasets/meldakahramann/animasyon-domain-dataset>

**Ne için:** Animasyon filmleri ve karakterleri üzerine Türkçe soru-cevap eğitimi.

**Durum:** Alan sohbeti için kullanılabilir; cevap tekrarı yüksek, tekilleştirme gerekli.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 1.020 |
| Bunun kaçı farklı cevap | 420 |
| Söz varlığı yoğunlaşması | %10 |
| Şema | conversation |
| Veri kartı | **gövdesi yok** |
| Lisans | **beyan edilmemiş** |

**Veri setini ayırt eden terimler:** `filminin`, `seslendirme`, `filmi`, `şrek`, `animasyonu`, `kadrosunda`, `prodüksiyonu`, `amansız`

### İyi olan

- 1.020 satır, birebir tekrar yok, tüm mesajlar dolu.
- Tüm 1.020 asistan mesajında thinking alanı var.

### Ele alınması gerekenler (2)

#### 1. Yüksek

**Tespit.** Normalleştirilmiş cevap tekrarı %58,8 (600/1.020); 300 cevap ailesi tekrar ediyor ve en sık cevap 3 kez geçiyor.

**Neden önemli.** Cevap çeşitliliği düşük; model aynı özeti farklı sorulara vermeyi öğrenir.

**Ne yapmalı.** Film ve karakter başına cevapları farklılaştır, tekrarları indir.

#### 2. Orta

**Tespit.** Veri kartı gövdesi yok; kaynak ve üretim yöntemi belgelenmemiş.

**Neden önemli.** Telif ve doğruluk denetimi yapılamıyor.

**Ne yapmalı.** Kaynakları ve üretim yöntemini belgeleyen bir kart ekle.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
