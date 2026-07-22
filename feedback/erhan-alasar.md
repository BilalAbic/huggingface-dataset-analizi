# Erhan Alasar

2 veri seti, toplam 121 satır, 3 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/erhanalsr/langusta-identity`

<https://huggingface.co/datasets/erhanalsr/langusta-identity>

**Ne için:** LangUsta asistanının kimlik cevaplarını öğretmek.

**Durum:** Küçük kimlik tohumu; cevap tekrarı çok yüksek.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 100 |
| Bunun kaçı farklı cevap | 20 |
| Söz varlığı yoğunlaşması | %53 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | mit |

**Veri setini ayırt eden terimler:** `langusta`, `kpss`, `alasar`, `erhan`, `türkçe`, `cümleyle`, `yanıtla`, `asistanıyım`

### İyi olan

- 100 satır (train=90, test=10); istem tekrarı %0,0; birebir tekrar yok.
- Kart amacı ve kaynağı belirtiyor.

### Ele alınması gerekenler (2)

#### 1. Yüksek

**Tespit.** Normalleştirilmiş cevap tekrarı %80,0 (80/100); en sık cevap 5 kez geçiyor.

**Neden önemli.** Kimlik cevaplarının çeşitliliği çok düşük; model tek cümleyi ezberler.

**Ne yapmalı.** Cevapları çeşitlendir; sınır ve reddetme davranışı ekle.

#### 2. Orta

**Tespit.** Yalnız 100 satır var ve tamamı kimlik sorusu; alan yetkinliği içermiyor.

**Neden önemli.** Tek başına kullanıldığında model yalnız isim ve sahiplik iddialarını öğrenir.

**Ne yapmalı.** Alan verisiyle birlikte düşük ağırlıkta kullan.

## `hf/erhanalsr/langusta-kpss-reasoning`

<https://huggingface.co/datasets/erhanalsr/langusta-kpss-reasoning>

**Ne için:** KPSS sorularında Türkçe muhakeme ve çözüm eğitimi.

**Durum:** Muhakeme örneği olarak kullanılabilir; ölçek çok küçük.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 21 |
| Bunun kaçı farklı cevap | 21 |
| Söz varlığı yoğunlaşması | %15 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | apache-2.0 |

**Veri setini ayırt eden terimler:** `medrese`, `devlet`, `şarkısı`, `antlaşması`, `selçuklu`, `sanatçının`, `cumhurbaşkanı`, `anayasa`

### İyi olan

- 21 satır (train=19, test=2); tekrar yok.
- Tüm 21 asistan mesajında özgün muhakeme izi korunmuş; cevaplar uzun (medyan 200 kelime).
- Kart kaynağı (AhmetSemih/Deepseek-mcq-reasoning-dataset) ve süzme ölçütünü belirtiyor.

### Ele alınması gerekenler (1)

#### 1. Yüksek

**Tespit.** Yalnız 21 satır var ve bunlar bir üst veri setinden süzülmüş alt küme.

**Neden önemli.** Bu hacimle KPSS muhakemesi öğretilemez; özgün katkı süzme işleminden ibaret.

**Ne yapmalı.** Kapsamı genişlet veya kaynak veri setini doğrudan kullan.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
