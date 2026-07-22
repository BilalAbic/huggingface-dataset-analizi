# Filiz Yalçin

2 veri seti, toplam 2.126 satır, 4 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/filiz-yalcin/identity-finetune`

<https://huggingface.co/datasets/filiz-yalcin/identity-finetune>

**Ne için:** Model kimliğini Filiz Yalçin personasına hizalamak.

**Durum:** Türetilmiş bir kopya; özgün katkı değil, kimlik tohumu olarak değerlendirilmeli.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 1.600 |
| Bunun kaçı farklı cevap | 1.593 |
| Söz varlığı yoğunlaşması | %10 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | gpl-3.0 |

**Veri setini ayırt eden terimler:** `magibu`, `yalçin`, `filiz`, `languages`, `context`, `256k`, `tasks`, `code`

### İyi olan

- 1.600 satır, turkish ve english paralel bölümleriyle iki dilli kimlik kapsamı sağlıyor (turkish=800, english=800).
- Tüm 1.600 asistan mesajında thinking alanı var.
- Veri kartı kaynağı ve yapılan tek değişikliği açıkça belirtiyor.

### Ele alınması gerekenler (3)

#### 1. Yüksek

**Tespit.** Veri kartı, setin alibayram/identity_finetune_magibu_q3 veri setinin birebir kopyası olduğunu ve yalnız model adının Magibu Q3 yerine Filiz Yalçin yapıldığını yazıyor.

**Neden önemli.** Özgün veri üretimi yok; yukarı akıştaki kusurlar doğrudan devralınıyor ve aynı kaynaktan türeyen diğer setlerle çakışıyor.

**Ne yapmalı.** Türetilmiş olduğunu kart başlığında belirt; özgün kimlik ve sınır örnekleriyle genişlet.

#### 2. Yüksek

**Tespit.** İki asistan mesajının içeriği tamamen boş; koleksiyondaki toplam 2 boş mesajın tamamı bu sette. Boş cevaplar 'Who named you and how did they choose the name?' sorusunda ve onun Türkçe paralel satırında.

**Neden önemli.** Boş hedef, modele o istem için sessiz kalmayı öğretir.

**Ne yapmalı.** İki satırı doldur veya çıkar; kusuru yukarı akış deposuna da bildir.

#### 3. Orta

**Tespit.** Metinde 1.038 zaman hassasiyetli eşleşme var; büyük kısmı 2026 yıl ifadesi.

**Neden önemli.** Kimlik cevapları sabit bir yıla demirlenirse model eskimiş bir bugün algısı öğrenir.

**Ne yapmalı.** Yıl ve tarih ifadelerini kimlik cevaplarından çıkar.

## `hf/filiz-yalcin/turkish-figure-skating-qa`

<https://huggingface.co/datasets/filiz-yalcin/turkish-figure-skating-qa>

**Ne için:** Artistik buz pateni alanında Türkçe soru-cevap eğitimi.

**Durum:** Alan eğitimi için kullanılabilir; sentetik üretim payı belgelenmeli.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 526 |
| Bunun kaçı farklı cevap | 522 |
| Söz varlığı yoğunlaşması | %17 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | gpl-3.0 |

**Veri setini ayırt eden terimler:** `pateninde`, `patencinin`, `artistik`, `atlayış`, `yarışma`, `koreografik`, `spin`, `element`

### İyi olan

- 526 satır, istem ve cevap tekrarı %1,9 ve %0,8; birebir tekrar yok.
- Tüm 526 asistan mesajında thinking alanı var.
- Kart ilk 17 satırın elle yazıldığını, kalanının DeepSeek ile üretildiğini açıkça belirtiyor.

### Ele alınması gerekenler (1)

#### 1. Orta

**Tespit.** Kayıtların büyük çoğunluğu model üretimi; satır düzeyinde kaynak veya doğrulama alanı yok. Metinde 47 zaman hassasiyetli eşleşme var.

**Neden önemli.** Sporcu, rekor ve kural bilgisi eskiyebilir ve sentetik hatalar fark edilmeden öğrenilebilir.

**Ne yapmalı.** Kural ve rekor içeren cevaplara tarih ve kaynak alanı ekle.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
