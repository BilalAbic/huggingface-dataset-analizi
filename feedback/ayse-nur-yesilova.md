# Ayşe Nur Yeşilova

2 veri seti, toplam 64 satır, 5 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/Aysenur44/namaz-vakti-dua-asistan-tr`

<https://huggingface.co/datasets/Aysenur44/namaz-vakti-dua-asistan-tr>

**Ne için:** Namaz vakitleri ve dua konularında Türkçe asistan eğitimi.

**Durum:** Küçük alan tohumu; kapsam genişletilmeli.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 60 |
| Bunun kaçı farklı cevap | 60 |
| Söz varlığı yoğunlaşması | %40 |
| Şema | conversation |
| Veri kartı | **gövdesi yok** |
| Lisans | **beyan edilmemiş** |

**Veri setini ayırt eden terimler:** `namazı`, `dinî`, `mezhebine`, `kılınabilir`, `hanefi`, `hocam`, `namazlar`, `yatsı`

### İyi olan

- 60 satırın tamamı system, user ve assistant sırasına sahip (60 system mesajı).
- İstem ve cevap tekrarı %0,0 ve %0,0; birebir tekrar yok.

### Ele alınması gerekenler (2)

#### 1. Yüksek

**Tespit.** Yalnız 60 satır var; namaz vakti hesabı gibi konum ve zamana bağlı işlevleri kapsayacak hacim yok.

**Neden önemli.** Alan yetkinliği kazandırmaz.

**Ne yapmalı.** Kapsamı genişlet; vakit hesabını araç çağrısına devret.

#### 2. Orta

**Tespit.** Veri kartı gövdesi yok; mezhep ve hesaplama yöntemi çerçevesi belirtilmemiş.

**Neden önemli.** Mezhebe göre değişen hükümler tek doğru gibi öğretilebilir.

**Ne yapmalı.** Yöntem ve mezhep çerçevesini karta yaz.

## `hf/Aysenur44/namaz-vakti-identity-tr`

<https://huggingface.co/datasets/Aysenur44/namaz-vakti-identity-tr>

**Ne için:** NamazAsistan-v1 kimlik cevaplarını öğretmek.

**Durum:** Yalnız küçük bir kimlik tohumu; alan yetkinliği sağlamıyor.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 4 |
| Bunun kaçı farklı cevap | 4 |
| Söz varlığı yoğunlaşması | %100 |
| Şema | conversation |
| Veri kartı | **gövdesi yok** |
| Lisans | **beyan edilmemiş** |

**Veri setini ayırt eden terimler:** `ayşenur`, `namazasistan`, `vakitleri`, `ibadet`, `namaz`, `yararsın`, `kimsin`, `adın`

### İyi olan

- 4 satırın tamamı geçerli system, user, assistant sırasına ve dolu içeriğe sahip.
- Standart messages alanı doğrudan sohbet eğitim araçlarına uyarlanabilir.

### Ele alınması gerekenler (3)

#### 1. Kritik

**Tespit.** Yalnız 4 satır var ve tamamı kimlik ile yetenek sorusu; namaz vakti, dua veya ibadet bilgisi ölçen içerik yok.

**Neden önemli.** Alan uzmanlığı kazandırmaz; model yalnız isim ve sahiplik iddialarını ezberler.

**Ne yapmalı.** Doğrulanmış ibadet içeriği, konum-zaman bağlamı ve güvenlik sınırları ekle.

#### 2. Yüksek

**Tespit.** Veri kartı gövdesi yok; kaynak, amaç ve sınırlama açıklaması bulunmuyor.

**Neden önemli.** Hedeflenen davranış ve veri kökeni belirsiz.

**Ne yapmalı.** Tam bir veri kartı ekle.

#### 3. Orta

**Tespit.** Dört kullanıcı isteminin tamamı diğer kimlik veri setlerinde de bulunuyor.

**Neden önemli.** Kimlik setleri birleştirilirse aynı soru çelişen cevaplarla eşleşir.

**Ne yapmalı.** Kimlik setlerini birleştirme; tek personayı seç.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
