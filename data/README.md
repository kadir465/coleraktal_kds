# Veri Dizini (Data Directory) Dokümantasyonu

Bu dizin, Kolorektal Klinik Karar Destek Sistemi (KDS) için tüm veri boru hattını (data pipeline) barındırır. Ham demografik ve tıbbi verileri, ara işleme durumlarını ve hem makine öğrenmesi sınıflandırması hem de Doğal Dil İşleme (NLP) modelleri için optimize edilmiş nihai yapılandırılmış veri setlerini içerir.

## Dizin Yapısı

| Dizin Adı | Açıklama |
|---|---|
| **raw_predata** | 1999-2000 ve 2001-2002 yılları için National Health and Nutrition Examination Survey (NHANES) kurumundan elde edilen başlangıç, ham SAS (.xpt) dosyalarını içerir. Bu veri setleri kapsamlı anket yanıtlarını ve laboratuvar bulgularını kapsar. |
| **processed** | İlk veri temizleme aşamasından kaynaklanan ara CSV dosyalarını içerir. Bu aşama; eksik değerlerin işlenmesini, kategorik değişkenlerin eşlenmesini ve temel özellik çıkarımını (feature extraction) kapsar. |
| **last_final** | Nihai model eğitiminden hemen önceki veri setini içerir. Bu aşamada, özellik seçimi kesinleşmiş olup sağlıklı denekler ile kanser hastaları arasındaki sınıf dengesizliklerini gidermek için sentetik veri artırımı (SMOTE gibi) uygulanmış olabilir. |
| **final** | Kesin olarak hazırlanmış veri setlerini içerir. Bu dosyalar kesinlikle dengelenmiş ve formatlanmıştır. Özellikle, yapısal tablo verileri, Büyük Dil Modellerinin (LLM'ler) ve ELECTRA gibi transformer mimarilerinin ince ayarını (fine-tuning) kolaylaştırmak için doğal dil "hasta hikayelerine" dönüştürülmüştür. |

## Önemli Dosyalar

- **`tibbi_rehber.txt`**: Tıbbi bağlamı, semptom-teşhis korelasyonlarını ve üretken modellerin doğru klinik bağlam sağlamasına yardımcı olan alana özgü bilgileri içeren temel bir referans belgesi.

## Veri İşleme Akışı

1. **Çıkarma (Extraction):** Ham SAS verileri, ilgili kolorektal risk faktörlerini çıkarmak için `scripts/` dizininde bulunan Python betikleri kullanılarak işlenir.
2. **Dönüşüm (Transformation):** Veriler titiz bir temizleme işleminden geçer. Eksik veri noktaları, alan kısıtlamalarına dayalı olarak atanır (imputation) veya silinir. Sayısal özellikler normalize edilir ve kategorik veriler kodlanır (encoding).
3. **Hikaye Üretimi (Narrative Generation):** NLP veri işleme hattı için kritik bir adım olup yapılandırılmış tıbbi geçmişler, hasta vaka notlarını taklit eden tutarlı metin paragraflarına programatik olarak dönüştürülür.
4. **Dengeleme ve Çıktı:** Azınlık sınıflarının (kanser pozitif) uygun şekilde temsil edilmesini sağlamak ve model sapmasını (bias) önlemek için gelişmiş örnekleme teknikleri uygulanır. Nihai veri seti `final` dizinine dışa aktarılır.
