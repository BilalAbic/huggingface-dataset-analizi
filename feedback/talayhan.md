# Talayhan

> Bu ad, gönderi formunda doğrulanabilir bir tam ad bulunmadığı için
> Hugging Face hesap adıdır. Düzeltmek isterseniz bildirin.

1 veri seti, toplam 299 satır, 2 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/Talayhan/skatepal_dataset`

<https://huggingface.co/datasets/Talayhan/skatepal_dataset>

**Ne için:** Kaykay antrenörü SkatePal personası ve güvenlik sınırları olan alan eğitimi.

**Durum:** Persona ve alan eğitimi için kullanılabilir.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 299 |
| Bunun kaçı farklı cevap | 299 |
| Söz varlığı yoğunlaşması | %8 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | **beyan edilmemiş** |

**Veri setini ayırt eden terimler:** `kaykay`, `board`, `trick`, `tahtanın`, `skateboarding`, `skate`, `ollie`, `flick`

### İyi olan

- 299 satır (turkish=174, english=125); istem ve cevap tekrarı %0,0 ve %0,0; birebir tekrar yok.
- Tüm 299 asistan mesajında güvenlik ve pedagoji odaklı muhakeme izi var.
- Kart persona hizalamasını ve güvenlik sınırı tasarımını açıklıyor.

### Ele alınması gerekenler (2)

#### 1. Orta

**Tespit.** Mesaj listesi standart messages veya conversations yerine conversation alanında; iki dilli bölümler ayrı (turkish=174, english=125).

**Neden önemli.** Standart yükleyiciler alanı tanımayıp veri setini tablo gibi okuyabilir.

**Ne yapmalı.** Alan adını messages olarak standartlaştır.

#### 2. Orta

**Tespit.** İçerik fiziksel risk taşıyan spor tavsiyesi; bu analiz güvenlik iddialarının doğruluğunu bir alan uzmanına doğrulatmadı.

**Neden önemli.** Hatalı teknik tavsiye yaralanmaya yol açabilir.

**Ne yapmalı.** Antrenör gözden geçirmesi uygula.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
