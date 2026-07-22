# Enes Hakan

1 veri seti, toplam 1.000 satır, 2 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/enes1863/bilisim-hukuku-domain-dataset`

<https://huggingface.co/datasets/enes1863/bilisim-hukuku-domain-dataset>

**Ne için:** Türkçe bilişim hukuku ve KVKK eğitimi için soru-cevap.

**Durum:** Mevcut hâliyle eğitim havuzuna alınmamalı; cevap çeşitliliği kritik düzeyde düşük.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 1.000 |
| Bunun kaçı farklı cevap | 20 |
| Söz varlığı yoğunlaşması | %25 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | other |

**Veri setini ayırt eden terimler:** `veri`, `rıza`, `kişisel`, `anonim`, `hâle`, `hukuka`, `işlendikleri`, `hukuki`

### İyi olan

- 1.000 satır, birebir tekrar yok, istem tekrarı %0,0.
- Tüm 1.000 asistan mesajında thinking alanı var.
- Kart kaynakları, üretim yöntemini ve hukuki danışmanlık olmadığı uyarısını belgeliyor.

### Ele alınması gerekenler (2)

#### 1. Kritik

**Tespit.** Normalleştirilmiş cevap tekrarı %98,0 (980/1.000) ve veri seti gerçekte yalnız 20 farklı cevap içeriyor. Yakın-tekrar oranı da %98,0, yani kalan cevaplar da yeniden yazılmış kopyalar değil. Kart bunu açıklıyor: yirmi elle yazılmış çekirdek örnek soru varyasyonlarıyla çoğaltılmış.

**Neden önemli.** Veri seti {rows} satır görünse de gerçek bilgi hacmi yirmi çekirdek cevap kadar; model soru çeşitliliğini öğrenirken aynı cevabı ezberler.

**Ne yapmalı.** Çekirdek sayısını artır veya satır sayısı yerine benzersiz cevap sayısını kartta öne çıkar.

#### 2. Orta

**Tespit.** Cevap uzunlukları çok dar bir bantta: en kısa 192, en uzun 296 karakter.

**Neden önemli.** Biçimsel tekdüzelik modele sabit uzunlukta cevap üretmeyi öğretebilir.

**Ne yapmalı.** Cevap uzunluğu ve biçimini çeşitlendir.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
