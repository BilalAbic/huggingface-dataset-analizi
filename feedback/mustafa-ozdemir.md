# Mustafa Özdemir

1 veri seti, toplam 450 satır, 2 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/namruni/meb-ogretmen-soru-cevap`

<https://huggingface.co/datasets/namruni/meb-ogretmen-soru-cevap>

**Ne için:** MEB öğretmenlerinin özlük ve mevzuat sorularına forum üslubuyla cevap.

**Durum:** Gerçek dünya bağlamı güçlü; güncellik katmanı olmadan kullanılmamalı.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 450 |
| Bunun kaçı farklı cevap | 450 |
| Söz varlığı yoğunlaşması | %16 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | **beyan edilmemiş** |

**Veri setini ayırt eden terimler:** `forumdaki`, `hocam`, `ilçe`, `resmî`, `öğretmen`, `tecrübesine`, `millî`, `müdürlüğünden`

### İyi olan

- 450 satır, istem ve cevap tekrarı %0,0 ve %0,0; birebir tekrar yok.
- Tüm 450 asistan mesajında kaynak değerlendirmesi içeren thinking alanı var.
- Kart kazıma sürecini, kaynağı ve istekler arası bekleme süresini belgeliyor.

### Ele alınması gerekenler (2)

#### 1. Yüksek

**Tespit.** Metinde 297 zaman hassasiyetli ifade eşleşmesi var. Bu bir regex eşleşme sayısıdır, benzersiz satır sayısı değildir.

**Neden önemli.** Mevzuat değiştiğinde cevaplar sessizce yanlışa döner ve özlük hakkı konularında somut zarara yol açabilir.

**Ne yapmalı.** Mevzuat maddesi, yürürlük tarihi ve güncel kaynak bağlantısı alanı ekle.

#### 2. Orta

**Tespit.** İçerik forum.memurlar.net üzerinden kazınmış; forum yanıtları resmî mevzuat metni değil.

**Neden önemli.** Forum yorumu resmî kaynak gibi öğrenilebilir.

**Ne yapmalı.** Resmî mevzuat dayanağını satıra bağla.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
