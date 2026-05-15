# Modeller Dizini (Models Directory) Dokümantasyonu

Bu dizin, Kolorektal KDS projesinin araştırma ve geliştirme aşamaları boyunca üretilen tüm eğitilmiş makine öğrenmesi modelleri, ağırlıkları ve tokenlaştırıcıları (tokenizers) için bir depodur.

## Barındırılan Modeller ve Varlıklar (Artifacts)

- **`colorectal_model.pkl`**: Serileştirilmiş geleneksel bir makine öğrenmesi modeli (Çok Katmanlı Algılayıcı - MLP / Rastgele Orman varyantı). Bu model; yapılandırılmış tablo formatındaki girdileri (yaş, semptom belirteçleri, laboratuvar sonuçları) kabul edecek ve kolorektal kanser riski için kalibre edilmiş bir olasılık skoru üretecek şekilde tasarlanmıştır.
- **`Kanser_Riski_Modeli_Temiz/`**: Bu dizin, ince ayarı yapılmış (fine-tuned) ELECTRA transformer modelinin eksiksiz durumunu içerir. Yapılandırılmamış klinik metinleri ve hasta hikayelerini işlemek için gerekli olan optimize edilmiş ağırlıkları, kelime dağarcığı yapılandırmalarını ve tokenlaştırıcıyı içerir. Bu model, gelişmiş NLP teşhis boru hattının (pipeline) çekirdeğini oluşturur.
- **`colorectal_cancer_model/`** / **`model_calismasi(MLP)/`**: Kıyaslama (benchmark) karşılaştırmaları için kullanılan çeşitli makine öğrenmesi modellerinin önceki yinelemelerini, deneysel mimarilerini ve yedekleme durumlarını içeren arşiv dizinleri.

**Not:** Büyük model dosyaları ve serileştirilmiş nesneler (`.pkl`, `.bin`, `.h5` veya `.safetensors` gibi) `.gitignore` aracılığıyla standart sürüm kontrolü (version control) takibinin dışında tutulmuş olabilir. Bir üretim veya işbirliği ortamında, bu varlıkların Git Large File Storage (Git LFS) veya harici bir nesne depolama (object storage) çözümü kullanılarak yönetilmesi şiddetle tavsiye edilir.
