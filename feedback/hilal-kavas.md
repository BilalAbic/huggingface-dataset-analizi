# Hilal Kavas

1 veri seti, toplam 29 satır, 2 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/sadecebirisii/turkish-llm-authority-bypass-safety-sft`

<https://huggingface.co/datasets/sadecebirisii/turkish-llm-authority-bypass-safety-sft>

**Ne için:** Yetki suistimali ve sistem komutu bypass saldırılarını tanıyıp güvenli biçimde reddetme eğitimi.

**Durum:** Güvenlik hizalaması için değerli ve koleksiyonda benzersiz; ölçek çok küçük.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 29 |
| Bunun kaçı farklı cevap | 29 |
| Söz varlığı yoğunlaşması | %15 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | cc-by-nc-4.0 |

**Veri setini ayırt eden terimler:** `guvenlik`, `thinking`, `dogrudan`, `mitre`, `teknigi`, `yonlendirme`, `icin`, `talebi`

### İyi olan

- 29 satır, tekrar yok; altı saldırı kategorisi (C1-C6) etiketli.
- Her kayıtta satır düzeyinde thinking alanı var (29 kayıt) ve cevaplar ayrıntılı (medyan 218 kelime).
- Kart amacı, kategori tanımlarını ve hedeflenen davranışı ayrıntılı belgeliyor.

### Ele alınması gerekenler (2)

#### 1. Yüksek

**Tespit.** Yalnız 29 satır var ve saldırı yüzeyinin altı kategorisini kapsıyor; kategori başına ortalama beş örnek düşüyor.

**Neden önemli.** Bu hacim güvenlik davranışını genellemek için yeterli değil; model ezberleyip yeni saldırı biçimlerinde başarısız olabilir.

**Ne yapmalı.** Kategori başına örnek sayısını artır ve tutulan bir değerlendirme kümesi ayır.

#### 2. Orta

**Tespit.** İstem metinleri gerçek jailbreak kalıpları içeriyor ve muhakeme cevabın içine thinking etiketleriyle gömülü.

**Neden önemli.** Saldırı kalıpları filtresiz yayımlanıyor ve gömülü muhakeme nihai cevaptan ayrıştırılmamış.

**Ne yapmalı.** Muhakemeyi ayrı alana taşı; yayım riskini kartta belirt.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
