# Ali Furkan Ak

2 veri seti, toplam 530 satır, 3 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/aliFurkan123/cultural-questions-dataset`

<https://huggingface.co/datasets/aliFurkan123/cultural-questions-dataset>

**Ne için:** Türkçe genel bilgi, kültür ve açıklamalı sohbet eğitimi.

**Durum:** Koşullu kullanılabilir; olgusal doğrulama ve konu etiketleri gerekiyor.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 500 |
| Bunun kaçı farklı cevap | 500 |
| Söz varlığı yoğunlaşması | %24 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | mit |

**Veri setini ayırt eden terimler:** `başkenti`, `element`, `katının`, `soracağım`, `şehridir`, `böldüğümüzde`, `kafadan`, `kaçtır`

### İyi olan

- 500 satırın tamamı iki mesajlı, dolu; istem ve cevap tekrarı %0,0 ve %0,0.
- Tüm 500 asistan mesajında thinking alanı var.
- Ayrıntılı veri kartı ve tutarlı Türkçe sohbet şeması var.

### Ele alınması gerekenler (2)

#### 1. Yüksek

**Tespit.** 500 asistan mesajının tamamında thinking alanı var; cevaplarda doğrulanabilir kaynak veya referans alanı yok.

**Neden önemli.** Sentetik olgusal hatalar ve gerekçe hataları birlikte öğrenilebilir.

**Ne yapmalı.** Bağımsız olgu kontrolü, kaynak alanı ve yalnız nihai cevap içeren türev üret.

#### 2. Orta

**Tespit.** Depo adı kültürel soruları ima ederken içerik daha geniş genel bilgi kapsıyor; satır düzeyinde kategori etiketi yok.

**Neden önemli.** Kapsam yanlış anlaşılabilir ve konu dengesi doğrulanamaz.

**Ne yapmalı.** Depo adını içerikle eşleştir; konu, zorluk ve kaynak alanları ekle.

## `hf/aliFurkan123/identity`

<https://huggingface.co/datasets/aliFurkan123/identity>

**Ne için:** Qwen tabanlı modelin kimliğini Ali Furkan personasına hizalamak.

**Durum:** Küçük kimlik tohumu; cevap tekrarı yüksek.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 30 |
| Bunun kaçı farklı cevap | 21 |
| Söz varlığı yoğunlaşması | %86 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | **beyan edilmemiş** |

**Veri setini ayırt eden terimler:** `furkan`, `qwen`, `tuned`, `fine`, `trained`, `model`, `created`, `assist`

### İyi olan

- 30 satır, istem tekrarı %0,0; birebir tekrar yok.
- Kart hedef persona ayrıntılarını tablo hâlinde belgeliyor.

### Ele alınması gerekenler (1)

#### 1. Orta

**Tespit.** Normalleştirilmiş cevap tekrarı %36,4 (12/30) ve yalnız 30 satır var; benzersiz cevap sayısı 21. Yakın-tekrar oranı %46,7, yani tam eşleşmenin gördüğünden daha fazla kopya var. Hesaplanan dil sinyali 'english'.

**Neden önemli.** Kimlik cevaplarının çeşitliliği düşük; Türkçe koleksiyon kapsamına dil olarak uymuyor.

**Ne yapmalı.** Türkçe kimlik örnekleri ekle ve cevapları çeşitlendir.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
