# Veri Dizini (Data Directory) Dokümantasyonu

Bu dizin, Kolorektal Klinik Karar Destek Sistemi (KDS) için tüm veri boru hattını (data pipeline) barındırır. Ham demografik ve tıbbi verileri, ara işleme durumlarını ve hem makine öğrenmesi sınıflandırması hem de Doğal Dil İşleme (NLP) modelleri için optimize edilmiş nihai yapılandırılmış veri setlerini içerir.

## Veri Kaynakları

Sistem tek bir kaynağa bağlı kalmamış olup, modelin küresel doğruluğunu ve genellenebilirliğini artırmak için üç ana kaynaktan beslenmektedir:
1. **NHANES (National Health and Nutrition Examination Survey):** 1999-2000 ve 2001-2002 dönemi Amerikan nüfus anketleri.
2. **Kaggle Veri Seti 1:** Bağımsız kaynaklardan sağlanan semptomatoloji ve risk faktörleri verisi.
3. **Kaggle Veri Seti 2:** Farklı demografik gruplara ait ek klinik sonuçlar ve laboratuvar parametreleri.

## Dizin Yapısı

| Dizin Adı | Açıklama |
|---|---|
| **raw_predata** | NHANES kurumundan elde edilen başlangıç SAS (.xpt) dosyalarını ve Kaggle'dan indirilen ham CSV veri setlerini içerir. |
| **processed** | İlk veri temizleme aşamasından kaynaklanan ara CSV dosyalarını içerir. Bu aşama; eksik değerlerin işlenmesini, farklı kaynaklardan gelen veri setlerinin (NHANES + Kaggle) şemalarının uyumlaştırılmasını ve kategorik değişkenlerin eşlenmesini kapsar. |
| **last_final** | Nihai model eğitiminden hemen önceki veri setini içerir. Sağlıklı denekler ile kanser hastaları arasındaki sınıf dengesizliklerini gidermek için sentetik veri artırımı (SMOTE) uygulanmıştır. |
| **final** | Kesin olarak hazırlanmış veri setlerini içerir. Bu dosyalar kesinlikle dengelenmiş ve formatlanmıştır. Yapısal tablo verileri, Büyük Dil Modellerinin (LLM'ler) ve ELECTRA gibi transformer mimarilerinin ince ayarını (fine-tuning) kolaylaştırmak için doğal dil "hasta hikayelerine" dönüştürülmüştür. |

## Önemli Dosyalar

- **`tibbi_rehber.txt`**: Retrieval-Augmented Generation (RAG) mimarisinin kalbi olan referans dokümandır. Google Gemini LLM, raporları üretirken sadece hastanın verilerini değil, aynı zamanda bu dosyadan alınan alana özgü tıbbi bağlamı ve semptom-teşhis korelasyonlarını da hesaba katar.

## Veri İşleme Akışı

1. **Çıkarma ve Harmonizasyon:** NHANES SAS verileri ve Kaggle CSV dosyaları `scripts/` dizinindeki betiklerle çıkarılır ve standart bir şema altında birleştirilir.
2. **Dönüşüm:** Veriler titiz bir temizleme işleminden geçer. Eksik veri noktaları atanır veya silinir. Sayısal özellikler normalize edilir.
3. **Hikaye Üretimi:** ELECTRA NLP boru hattı için yapılandırılmış tıbbi geçmişler, hasta vaka notlarını taklit eden tutarlı metin paragraflarına programatik olarak dönüştürülür.
4. **Dengeleme ve Çıktı:** Azınlık sınıflarının (kanser pozitif) uygun şekilde temsil edilmesini sağlamak için SMOTE gibi gelişmiş örnekleme teknikleri uygulanır. Nihai veri seti `final` dizinine dışa aktarılır.
