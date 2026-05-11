# Korelaktal Kanser Tespit Projesi

Bu proje, NHANES veri setlerini kullanarak kolorektal kanser tespiti için makine öğrenmesi modelleri geliştirmeyi ve hasta hikayeleri üzerinden doğal dil işleme modelleri eğitmeyi amaçlar.

## Klasör Yapısı

- **data/**: Proje verilerinin saklandığı ana dizin.
    - **raw/**: SAS (.xpt) formatındaki ham NHANES verileri ve yıla göre ayrılmış klasörler.
    - **processed/**: İşleme aşamasındaki ara CSV dosyaları.
    - **final/**: Model eğitimi için hazır hale getirilmiş final veri setleri.
- **scripts/**: Veri işleme, temizleme ve birleştirme scriptleri.
    - **data_processing/**: Yıla özel ham veri işleme scriptleri.
- **notebooks/**: Veri analizi ve model denemelerinin yapıldığı Jupyter notebook'lar.
- **models/**: Eğitilmiş modeller ve vektörleştirici (.pkl) dosyaları.

## Veri İşleme Akışı

1. **Ham Veri İşleme**: `scripts/data_processing/` altındaki scriptler ham .xpt dosyalarını temizler.
2. **Metin Dönüştürme**: `scripts/transform_datasets_to_text.py` yapısal verileri doğal dil anlatılarına dönüştürür.
3. **Veri Artırımı**: `scripts/augment_cancer_data.py` azınlık sınıflar için sentetik veriler üretir.
4. **Birleştirme**: `scripts/merge_and_clean_data.py` tüm verileri birleştirerek final veri setini oluşturur.

## Final Veri Seti
Final veri seti `data/final/Korelaktal_Final_Dataset.csv` konumundadır ve şu kolonları içerir:
- `label`: Kanserin varlığı (0.0 veya 1.0).
- `hasta yorumu`: Hastanın durumunu belirten metinsel anlatı.
