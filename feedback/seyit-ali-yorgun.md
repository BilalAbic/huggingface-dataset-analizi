# Seyit Ali Yorğun

1 veri seti, toplam 773 satır, 1 bulgu. Değerlendirme tarihi 2026-07-22.

Aşağıdakiler puan değil, yapılacak iş listesidir. Veri setleri birbiriyle
karşılaştırılmaz ve sıralanmaz; her biri kendi kullanım amacına göre
değerlendirilir. Bulgular yapısal ve içerik desenlerine dayanır — hiçbir
cevabın olgusal doğruluğu alan uzmanı tarafından denetlenmedi.

## `hf/seali/turkce-saglik-qa`

<https://huggingface.co/datasets/seali/turkce-saglik-qa>

**Ne için:** Türkçe genel sağlık sorularını yanıtlama ve gerektiğinde sağlık profesyoneline yönlendirme.

**Durum:** Sağlık alanı için koşullu kullanılabilir; uzman doğrulaması olmadan üretime alınmamalı.

| Ölçüm | Değer |
|---|---:|
| Satır sayısı | 773 |
| Bunun kaçı farklı cevap | 773 |
| Söz varlığı yoğunlaşması | %10 |
| Şema | conversation |
| Veri kartı | var |
| Lisans | cc-by-4.0 |

**Veri setini ayırt eden terimler:** `diyabet`, `hastalığı`, `insülin`, `tedavi`, `besin`, `egzersiz`, `şekeri`, `aktivite`

### İyi olan

- 773 satır, istem ve cevap tekrarı %0,1 ve %0,0; birebir tekrar yok.
- Tüm 773 asistan mesajında thinking alanı var; cevaplar ayrıntılı (medyan 151 kelime).
- Kart amacı, kapsanan konuları ve yönlendirme davranışını belgeliyor.

### Ele alınması gerekenler (1)

#### 1. Yüksek

**Tespit.** Sağlık içeriği; bu analiz yapısal ve istatistiksel kontroller yaptı, cevapların tıbbi doğruluğu bir alan uzmanı tarafından doğrulanmadı.

**Neden önemli.** Yanlış tıbbi bilgi doğrudan zarara yol açabilir.

**Ne yapmalı.** Klinik gözden geçirme süreci uygula; her cevaba kaynak ve sorumluluk reddi alanı ekle.

---

Koleksiyonun tamamı, yöntem ve eşikler:
[teknik değerlendirme](../reports/dataset-technical-assessment.md) ·
[yetenek eşlemesi](../reports/model-capability-mapping.md) ·
[değerlendirme kriterleri](../config/evaluation_criteria.json)
