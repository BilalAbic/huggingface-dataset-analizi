# Senem Deniz

1 veri seti, toplam 553 satır, 1 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/senemde/saglik-qa-tr`

<https://huggingface.co/datasets/senemde/saglik-qa-tr>

**Ne için:** Türkçe Wikipedia sağlık kategorilerinden türetilmiş soru-cevap eğitimi.

**Durum:** Sağlık alanı için koşullu kullanılabilir; uzman doğrulaması gerekli.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 553 |
| Bunun kaçı farklı cevap | 550 |
| Söz varlığı yoğunlaşması | %14 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | mit |

**Veri setini ayırt eden terimler:** `diyabet`, `glukoz`, `diabetes`, `hastalığı`, `insülin`, `nöropatide`, `şekeri`, `gestasyonel`

### İyi olan

- 553 satır, istem ve cevap tekrarı %0,0 ve %0,5; birebir tekrar yok.
- Her kayıtta system rolü var (553 system mesajı); sorumluluk reddi sistem isteminde tanımlı.
- topic ve source alanları satır düzeyinde kaynak izlenebilirliği sağlıyor.

### Ele alınması gerekenler (1)

#### 1. Yüksek

**Tespit.** İçerik Wikipedia'dan kazınıp bir dil modeliyle soru-cevaba dönüştürülmüş; cevapların tıbbi doğruluğu uzman tarafından doğrulanmadı.

**Neden önemli.** Wikipedia hatası veya model dönüşüm hatası tıbbi içerikte zarara yol açabilir.

**Ne yapmalı.** Klinik gözden geçirme uygula ve kaynak revizyonunu satıra yaz.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
