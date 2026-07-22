# Umay Şamlı

2 veri seti, toplam 1.019 satır, 3 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/samliumay/turkish_cyber_security_controls_dataset`

<https://huggingface.co/datasets/samliumay/turkish_cyber_security_controls_dataset>

**Ne için:** Siber güvenlik kontrolleri, kontrol seçimi ve güvenli mimari üzerine Türkçe soru-cevap.

**Durum:** Alan eğitimi için kullanılabilir; koleksiyonun en temiz setlerinden biri.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 800 |
| Bunun kaçı farklı cevap | 800 |
| Söz varlığı yoğunlaşması | %16 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | mit |

**Veri setini ayırt eden terimler:** `erişim`, `veri`, `envanter`, `kimlik`, `doğrulayın`, `yönetim`, `güvenlik`, `edin`

### İyi olan

- 800 satır, istem ve cevap tekrarı %0,0 ve %0,0; birebir tekrar yok.
- Cevaplar tutarlı uzunlukta ve ayrıntılı (medyan 69.0 kelime).
- Kart NIST SP 800-53 Rev. 5 dayanağını, kapsanan konu başlıklarını ve verinin sentetik olduğunu açıkça yazıyor.

### Ele alınması gerekenler (1)

#### 1. Orta

**Tespit.** İçerik tamamen sentetik; satır düzeyinde kontrol kimliği veya standart maddesine bağlantı yok. Metinde 38 zaman hassasiyetli eşleşme var.

**Neden önemli.** Standart sürümleri değiştiğinde cevapların hangi maddeye dayandığı izlenemez.

**Ne yapmalı.** Kontrol kimliği ve standart sürümü alanı ekle.

## `hf/samliumay/umay_samli_identification_dataset`

<https://huggingface.co/datasets/samliumay/umay_samli_identification_dataset>

**Ne için:** gemma_3_umay asistanının kimliğini, yaratıcısını ve sınırlarını tanımlamak.

**Durum:** Kimlik eğitimi için kullanılabilir; cevap tekrarı yüksek.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 219 |
| Bunun kaçı farklı cevap | 73 |
| Söz varlığı yoğunlaşması | %30 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | **beyan edilmemiş** |

**Veri setini ayırt eden terimler:** `umay`, `şamlı`, `kamuya`, `gemma_3_umay`, `nato`, `zekâ`, `güvenlik`, `yapay`

### İyi olan

- 219 satır, istem tekrarı %0,0; birebir tekrar yok.
- Kart, modelin insan olmadığını ve yaratıcısı adına karar veremeyeceğini açıkça işliyor.

### Ele alınması gerekenler (2)

#### 1. Yüksek

**Tespit.** Normalleştirilmiş cevap tekrarı %66,7 (146/219); en sık cevap 3 kez geçiyor.

**Neden önemli.** Kimlik cevaplarının çeşitliliği düşük; model tek kalıbı ezberler.

**Ne yapmalı.** Cevap ifadelerini çeşitlendir.

#### 2. Orta

**Tespit.** Kart, kişinin kamuya açık mesleki geçmişi ve eğitimi hakkında soru-cevap içerdiğini belirtiyor; metinde 62 zaman hassasiyetli eşleşme var.

**Neden önemli.** Kişisel biyografik bilgi eskiyebilir ve kişisel veri yükümlülüğü doğurabilir.

**Ne yapmalı.** Biyografik iddiaları tarihlendir ve kişinin onayını belgele.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
