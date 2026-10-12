# Modeller Dizini (Models Directory) Dokümantasyonu

Bu dizin, Kolorektal KDS projesinin araştırma ve geliştirme aşamaları boyunca üretilen tüm eğitilmiş makine öğrenmesi modelleri, ağırlıkları ve tokenlaştırıcıları (tokenizers) için bir depodur.

## Barındırılan Modeller ve Varlıklar (Artifacts)

- **`colorectal_model.pkl`**: Deneysel nitelikteki makine öğrenmesi modeli (Çok Katmanlı Algılayıcı - MLP / Rastgele Orman varyantı). Bu model; yapılandırılmış tablo formatındaki girdileri (yaş, semptom belirteçleri, laboratuvar sonuçları) kabul edecek ve kolorektal kanser riski için bir olasılık skoru üretecek şekilde deneysel olarak tasarlanmıştır (çıkarım aşamasında sıcaklık ölçekleme ve logit ayarı uygulanmıştır; kalibrasyon ayrıca ölçülmemiştir).
- **`Kanser_Riski_Modeli_Temiz/`**: Bu dizin, ince ayarı yapılmış (fine-tuned) ELECTRA transformer modelinin (`dbmdz/electra-base-turkish-cased-discriminator`) durumunu içerir. Yapılandırılmamış klinik metinleri ve hasta anlatılarını işlemek için gerekli olan ağırlıkları, kelime dağarcığı yapılandırmalarını ve tokenlaştırıcıyı barındırır. Bu model, NLP tabanlı risk değerlendirmesi ve klinik yönlendirme boru hattının çekirdeğini oluşturur.
- **`colorectal_cancer_model/`** / **`model_calismasi(MLP)/`**: Kıyaslama (benchmark) karşılaştırmaları için kullanılan deneysel makine öğrenmesi modellerinin önceki yinelemelerini ve arşiv durumlarını içeren dizinler.

**Not:** Büyük model dosyaları ve serileştirilmiş nesneler (`.pkl`, `.bin`, `.h5` veya `.safetensors` gibi) `.gitignore` aracılığıyla standart sürüm kontrolü (version control) takibinin dışında tutulmuş olabilir. Bir üretim veya işbirliği ortamında, bu varlıkların Git Large File Storage (Git LFS) veya harici bir nesne depolama (object storage) çözümü kullanılarak yönetilmesi şiddetle tavsiye edilir.
