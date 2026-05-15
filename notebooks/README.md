# Not Defterleri Dizini (Notebooks Directory) Dokümantasyonu

Bu dizin, keşifsel veri analizini (EDA), özellik mühendisliğini (feature engineering) ve yinelemeli model geliştirme sürecini belgeleyen Jupyter Not Defterlerini içerir. Bu not defterleri, proje için birincil araştırma ve geliştirme ortamı olarak hizmet vermektedir.

## Dosya Açıklamaları

### Keşifsel Veri Analizi (EDA) ve Ön İşleme
- **`data_analyses_cancer_dataset.ipynb`**: NHANES veri setleri üzerinde kapsamlı istatistiksel analiz yürütür. Dağılımları, korelasyon matrislerini görselleştirir ve hafifletilmesi gereken kritik sınıf dengesizliklerini (class imbalances) tespit eder.
- **`process_1999_2000_dataset.ipynb`** / **`proceses_2001_2002_dataset.ipynb`**: NHANES uzunlamasına çalışmalarından (longitudinal studies) belirli kohortları ayrıştırmak, filtrelemek ve temizlemek için ayrılmış not defterleri.
- **`set_examination.ipynb`** / **`last_data_pre.ipynb`**: Veri setleri eğitim döngülerine aktarılmadan önce üzerlerinde nihai doğrulamaları gerçekleştirir. Veri sızıntısı (data leakage) olmadığından ve özellik uzayının doğru şekilde yapılandırıldığından emin olur.
- **`data_v2.ipynb`**: Veri dönüşümü deneylerini birleştiren kapsamlı bir inceleme not defteri.

### Model Mimarisi ve Eğitimi
- **`notebook_model.ipynb`**: Temel risk sınıflandırması için geleneksel makine öğrenmesi modelleriyle (ör. Random Forest, Multilayer Perceptrons) yapılan ilk deneyleri detaylandırır.
- **`electra_model_train.ipynb`**: ELECTRA transformer modelinin ince ayar (fine-tuning) sürecini belgeler. Hasta hikayelerinin nasıl tokenize edildiğini ve modelin metinsel klinik verilere dayalı nüanslı risk değerlendirmesi için nasıl eğitildiğini gösterir.
- **`data_analyz_and_bert_model.ipynb`**: ELECTRA ve geleneksel algoritmalara karşı performans metriklerini değerlendirerek BERT tabanlı mimarileri kullanan karşılaştırmalı çalışmaları içerir.
