# Nur Sima Akgül

1 veri seti, toplam 20.874 satır, 4 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/nursimakgul/meb-soru-uretme`

<https://huggingface.co/datasets/nursimakgul/meb-soru-uretme>

**Ne için:** MEB müfredatına göre sınıf, ders ve konu belirtilerek çoktan seçmeli veya açık uçlu soru üretimi.

**Durum:** Structured Output için koleksiyondaki en güçlü kaynak; JSON sözleşmesi tamamlanmadan üretime alınmamalı.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 20.874 |
| Bunun kaçı farklı cevap | 20.609 |
| Söz varlığı yoğunlaşması | %22 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | mit |

**Veri setini ayırt eden terimler:** `üret`, `seçmeli`, `çoktan`, `soru`, `sınıf`, `aşağıdakilerden`, `orta`, `cevap`

> İstemlerin %87'i tekrar ediyor, yani kullanıcı turu büyük
> ölçüde sabit bir talimat. Yukarıdaki terimler konuyu değil talimatı
> anlatıyor olabilir.

### İyi olan

- 20.874 satırın tamamı geçerli user→assistant sırasına sahip, boş içerik yok.
- 17.454 asistan cevabı ayrıştırılabilir JSON nesnesi (metin, secenekler, dogru_cevap, cevap_aciklamasi).
- Tüm 20.874 asistan mesajında kazanım gerekçesini açıklayan thinking alanı var.

### Ele alınması gerekenler (4)

#### 1. Yüksek

**Tespit.** Dataset Viewer bu depoyu sunamıyor: meb_identity_format_temiz.jsonl her satırda JSON nesnesi yerine çıplak JSON dizisi tutuyor, bu yüzden sütun şeması çıkarılamıyor. Analiz, revizyona sabitlenmiş ham dosyanın bayt boyutu ve SHA-256 doğrulamasıyla indirilmesiyle yapıldı.

**Neden önemli.** Veri seti standart yükleyicilerle açılamıyor; kullanıcı hata yerine boş sonuç alabilir.

**Ne yapmalı.** Her satırı messages anahtarlı bir nesneye sar; Viewer otomatik çalışmaya başlar.

#### 2. Yüksek

**Tespit.** Cevapların 17.454/20.874 tanesi JSON; kalan 3.420 kayıt JSON biçiminde değil. JSON gibi başlayıp ayrıştırılamayan kayıt sayısı 0, yani sorun bozuk JSON değil, sözleşmenin bir kısım kayıtta hiç uygulanmamış olması.

**Neden önemli.** Model aynı istem ailesi için bazen JSON bazen düz metin üretmeyi öğrenir.

**Ne yapmalı.** Şemayı zorunlu kıl; JSON olmayan kayıtları ayrı alt kümeye taşı veya dönüştür.

#### 3. Yüksek

**Tespit.** Normalleştirilmiş istem tekrarı %86,6 (18.084/20.874); en sık istem 314 kez geçiyor. Ayrıca 797 istem ailesi farklı cevaplarla eşleşiyor ve bu aileler 18.880 satırı kapsıyor.

**Neden önemli.** Aynı sınıf/ders/konu isteminin farklı sorular üretmesi tasarım gereği olsa da bu ölçekte istem ayırt edici bir sinyal olmaktan çıkıyor.

**Ne yapmalı.** İsteme zorluk, kazanım kodu ve soru tipi gibi ayırt edici alanlar ekle.

#### 4. Orta

**Tespit.** Metinde 560 zaman hassasiyetli ifade eşleşmesi var. Bu bir regex eşleşme sayısıdır, benzersiz satır sayısı değildir.

**Neden önemli.** Müfredat ve mevzuat değiştiğinde sorular sessizce eskir.

**Ne yapmalı.** Müfredat sürümü ve tarih alanı ekle.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
