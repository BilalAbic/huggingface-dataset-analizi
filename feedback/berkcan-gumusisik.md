# Berkcan Gümüşışık

2 veri seti, toplam 348 satır, 4 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/berkcangumusisik/voleykoc-antrenorluk-tr`

<https://huggingface.co/datasets/berkcangumusisik/voleykoc-antrenorluk-tr>

**Ne için:** Voleybol antrenörlüğü, teknik, taktik ve kondisyon üzerine Türkçe asistan eğitimi.

**Durum:** Alan eğitimi için kullanılabilir; cevap tekrarı orta düzeyde.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 166 |
| Bunun kaçı farklı cevap | 125 |
| Söz varlığı yoğunlaşması | %19 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | mit |

**Veri setini ayırt eden terimler:** `voleybol`, `ligi`, `şampiyonası`, `sezonunda`, `takımı`, `oyuncu`, `kupası`, `fenerbahçe`

### İyi olan

- 166 satır, istem tekrarı %0,0; birebir tekrar yok.
- Her satırda system ve source alanları var; cevaplar ayrıntılı (medyan 63.0 kelime).
- Kart kaynak, kapsam ve eğitilen modeli belgeliyor.

### Ele alınması gerekenler (2)

#### 1. Orta

**Tespit.** Normalleştirilmiş cevap tekrarı %24,7 (41/166); metinde 66 zaman hassasiyetli eşleşme var (takım ve sezon adları).

**Neden önemli.** Takım ve sezon bilgisi hızla eskir; tekrar eden cevaplar ağırlık dengesizliği yaratır.

**Ne yapmalı.** Sezon bilgisini tarihlendir; tekrarları azalt.

#### 2. Orta

**Tespit.** System istemi ayrı sütunda tutuluyor, mesaj listesinin parçası değil.

**Neden önemli.** Standart yükleyiciler persona bağlamını kaybedebilir.

**Ne yapmalı.** System istemini messages içine taşı.

## `hf/berkcangumusisik/voleykoc-identity-tr`

<https://huggingface.co/datasets/berkcangumusisik/voleykoc-identity-tr>

**Ne için:** VoleykoçAI asistanının kimliğini, yeteneklerini ve sınırlarını öğretmek.

**Durum:** Kimlik tohumu olarak kullanılabilir; cevap tekrarı çok yüksek.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 182 |
| Bunun kaçı farklı cevap | 26 |
| Söz varlığı yoğunlaşması | %27 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | mit |

**Veri setini ayırt eden terimler:** `voleybol`, `volleyball`, `berkcan`, `gümüşışık`, `voleykoçai`, `antrenman`, `turkish`, `training`

### İyi olan

- 182 satır (turkish=105, english=77); istem tekrarı %0,0; birebir tekrar yok.
- Her satırda ayrı bir system sütunu var (182 system mesajı olarak profillendi).
- Kart yapının alibayram/identity_finetune_magibu_q3 referans alınarak kurulduğunu belirtiyor.

### Ele alınması gerekenler (2)

#### 1. Yüksek

**Tespit.** Normalleştirilmiş cevap tekrarı %85,7 (156/182); en sık cevap 7 kez geçiyor.

**Neden önemli.** Kimlik cevaplarının çeşitliliği çok düşük.

**Ne yapmalı.** Cevapları çeşitlendir ve sınır davranışı örnekleri ekle.

#### 2. Orta

**Tespit.** System istemi mesaj listesinin içinde değil, ayrı bir sütunda tutuluyor.

**Neden önemli.** Standart sohbet yükleyicileri system alanını atlayıp persona bağlamını kaybedebilir.

**Ne yapmalı.** System istemini messages listesinin ilk elemanı yap.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
