# Betikler Dizini (Scripts Directory) Dokümantasyonu

Bu dizin, veri işleme boru hattının (data pipeline), veri artırımının (data augmentation) ve veri seti derlemesinin otomasyonundan sorumlu bağımsız Python betiklerini içerir. Bu betikler, Jupyter Not Defterlerinde geliştirilen mantığı modüler, tekrarlanabilir yürütme birimlerine soyutlar.

## Temel Modüller

### Veri Artırımı (Data Augmentation) ve Dengeleme
- **`augment_cancer_data.py`** / **`augment_data.py`**: Gelişmiş aşırı örnekleme (oversampling) tekniklerini uygular (SMOTE - Sentetik Azınlık Aşırı Örnekleme Tekniği gibi). Bu betikler, eğitim algoritmalarının çoğunluk sınıfına (sağlıklı denekler) karşı bir sapma (bias) geliştirmemesini sağlamak için sentetik azınlık sınıfı örnekleri (kanser pozitif hastalar) üretir.
- **`balance_original_data.py`**: Karmaşık artırımlar uygulanmadan önce ham veri setleri üzerinde istatistiksel dengeleme prosedürlerini yürütür.

### Veri Birleştirme ve Temizleme
- **`merge_and_clean_data.py`** / **`merge_all_data.py`**: Farklı zamansal kohortlar (örneğin, 1999-2000 verilerini 2001-2002 verileriyle birleştirmek) arasında verilerin toplanmasını gerçekleştirir. Şema tutarsızlıklarını çözer ve küresel veri temizliği gerçekleştirir.
- **`merge_user_datasets.py`** / **`merge_final_step.py`**: Ayrı özellik kümelerini (feature sets), model tüketimine uygun birleştirilmiş, düz ilişkisel bir yapıda konsolide eder.

### Doğal Dil İşleme (NLP) Hazırlığı
- **`transform_datasets_to_text.py`**: Tablo şeklindeki veriler ile NLP modelleri arasında köprü görevi gören kritik bir betik. İlişkisel hasta kayıtları üzerinde yinelenir (iterate) ve daha sonra ELECTRA ve BERT modellerine ince ayar (fine-tuning) yapmak için kullanılan sürekli metin anlatıları (hasta geçmişleri) oluşturmak üzere deterministik şablonlar kullanır.
- **`generate_final_dataset.py`**: Önceki modüllerin yürütülmesini düzenleyen ve nihai veri setini `data/final/` dizinine dışa aktaran boru hattındaki son (terminal) betik.
