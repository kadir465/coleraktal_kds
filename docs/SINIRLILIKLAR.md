# Çalışma ve Sistem Sınırlılıkları (Limitations)

Bu belge, **Kolorektal Klinik Karar Destek Sistemi (KolonKDS)** projesinin bilimsel, metodolojik ve klinik sınırlılıklarını şeffaf bir şekilde belgelemek amacıyla hazırlanmıştır.

---

## 1. Sentetik Metin Üretimi (Synthetic Patient Narratives)
* **Kural Tabanlı Şablonlar:** ELECTRA ve BERT modellerinin eğitiminde kullanılan metin verileri, yapılandırılmış tablo verilerinden (NHANES anketleri ve Kaggle veri setleri) belirli kural tabanlı cümle şablonları (`scripts/transform_datasets_to_text.py`, `notebooks/data_analyses_cancer_dataset.ipynb`) aracılığıyla programatik olarak üretilmiştir.
* **Gerçek Klinik Not Çeşitliliği Eksikliği:** Bu sentetik anlatılar, poliklinik ortamında hekimler veya hastalar tarafından serbestçe kaleme alınan metinlerdeki yazım hatalarını, jargon çeşitliliğini, dolaylı anlatımları ve karmaşık klinik ifadeleri tam olarak yansıtmamaktadır.

---

## 2. Etiket Tanımları ve Vekil (Surrogate) Hedefler
* **Kaggle Veri Seti:** Kaggle veri setinde hedef etiket olarak kullanılan değişkenler (`Cancer_Stage` evreleri veya `Survival_Prediction`) vekildir; doğrudan histopatolojik biyopsi veya kolonoskopik teyit verisiyle birebir klinik doğrulaması yapılmamıştır.
* **NHANES Veri Seti:** NHANES kohortlarındaki etiketler (`MCQ220` ve `MCQ230A`), katılımcıların anket beyanlarına ("Daha önce size hekim tarafından kanser tanısı konuldu mu?") dayanmaktadır. Erken evre asemptomatik lezyonlar veya polipler anket beyanında yer almayabilir.

---

## 3. Veri Ön İşleme, SMOTE ve Ayrı Test Seti Tasarımı
* **Bölme Öncesi Dengeleme ve Sentetik Örnekleme:** Bazı deneysel veri hazırlama betiklerinde veri setleri dengelenirken sentetik örnekleme (SMOTE / rastgele oversampling) adımları uygulanmıştır. Bu durum, veri noktaları arasında sentetik bağıntı yaratabilmekte ve modelin genelleme başarısını olduğundan iyimser gösterebilmektedir.
* **Bağımsız Harici Doğrulama (External Validation):** Model yalnızca mevcut anket/veri seti alt kümeleri üzerinde test edilmiştir. Farklı bir hastaneden, bağımsız bir klinik merkezden veya gerçek hasta başvurularından toplanmış prospektif harici bir doğrulama (external validation) kohortu bulunmamaktadır.

---

## 4. Model Çıktısı, Kalibrasyon ve XAI Mantığı
* **Logit ve Sıcaklık Ayarı:** Dağıtım ortamında (`app.py`), aşırı duyarlılığı dengelemek için lojistik bias çıkartma (`logits[0][1] -= 4`) ve sıcaklık ölçekleme ($T = 2.9$) ampirik olarak uygulanmıştır. Ancak bu işlem resmi bir izotonik regresyon veya Platt kalibrasyonu ile istatistiksel olarak doğrulanmamış ve kalibrasyon hatası (ECE) ölçülmemiştir.
* **Açıklanabilir Yapay Zeka (XAI):** Arayüzde sunulan anahtar kelime vurgulaması modelin dahili dikkat (attention) ağırlıkları veya SHAP değerleri üzerinden değil; tıbbi rehbere dayalı kural tabanlı bir eşleştirme sözlüğü (`RISK_KEYWORDS`) üzerinden çalışmaktadır.

---

## 5. Klinik Doğrulama ve Etik Durum
* **Tanı Aracı Değildir:** Bu sistem bir tanı (teşhis) cihazı veya tıbbi ürün (SaMD) değildir. Yalnızca farkındalık artırma, ön triyaj ve klinik karar destek amaçlı bir prototiptir.
* **Klinik Onay ve Etik Kurul:** Sistem klinik ortamda hasta üzerinde denenmemiştir ve prospektif klinik araştırma etik kurul onayına sahip değildir. Tüm kararlar gastroenteroloji ve genel cerrahi uzman hekimlerinin klinik değerlendirmesine bırakılmalıdır.
