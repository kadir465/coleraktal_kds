import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn.impute import SimpleImputer
import random

# 1. Veriyi Yükle
path = r'C:\Users\kadir\OneDrive\Masaüstü\korelaktal\2001-2002\NHANES_2001_2002_Korelasyonlu_Veriler.csv'
print(f"{path} yükleniyor...")
df = pd.read_csv(path)

# 2. Ön İşleme ve Dengeleme (SMOTE)
print(f"Eski Dağılım: {df['Hastalik_Durumu_LABEL'].value_counts().to_dict()}")

X = df.drop(columns=['Hastalik_Durumu_LABEL', 'Hasta_ID'], errors='ignore')
y = df['Hastalik_Durumu_LABEL']

imputer = SimpleImputer(strategy='median')
X_imputed = imputer.fit_transform(X)

smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_imputed, y)

df_balanced = pd.DataFrame(X_resampled, columns=X.columns)
df_balanced['Label'] = y_resampled

print(f"Dengelenmiş Dağılım: {df_balanced['Label'].value_counts().to_dict()}")

# 3. Metne Dönüştürme (Patient Story)
def hikaye_olustur(row):
    yas = int(row['Yas'])
    cinsiyet = "erkek" if row['Cinsiyet'] == 1.0 else "kadın"
    hgb = row['Hemoglobin']
    wbc = row['Akyuvar_WBC']
    kilo = row['Kilo_Verme_Durumu']
    label = row['Label']
    
    parcalar = []
    parcalar.append(f"Merhaba, {yas} yaşında bir {cinsiyet} hastayım.")
    
    if kilo > 200:
        parcalar.append(f"Kilom oldukça yüksek ({int(kilo)} lbs).")
    else:
        parcalar.append(f"Vücut ağırlığım {int(kilo)} lbs.")
        
    hgb_limit = 13.5 if row['Cinsiyet'] == 1.0 else 12.0
    if hgb < hgb_limit:
        parcalar.append(f"Hemoglobin değerim {hgb} ile normalin altında çıktı.")
    else:
        parcalar.append(f"Kan tahlillerimde hemoglobin ({hgb}) normal seviyelerde.")
        
    if wbc > 10.0:
        parcalar.append(f"Akyuvar sayım ({wbc}) yüksek, bir enfeksiyon riski olabilir.")

    if label == 1.0:
        belirtiler = [
            "Karın bölgemde geçmeyen kramplar ve şişkinlik var.",
            "Dışkılama alışkanlığımda ciddi bir düzensizlik başladı.",
            "Tuvalette kan gördüm ve bu durum beni endişelendiriyor.",
            "Son zamanlarda iştahsızlık ve halsizlik yaşıyorum.",
            "Doktorum kolon kanseri taraması yaptırmamı önerdi."
        ]
        parcalar.append(random.choice(belirtiler))
    else:
        parcalar.append("Genel sağlık durumumun kontrol edilmesi için başvuruyorum.")

    return " ".join(parcalar)

print("Metin hikayeleri oluşturuluyor...")
df_balanced['Text'] = df_balanced.apply(hikaye_olustur, axis=1)

# Sadeleştir ve Kaydet
df_final = df_balanced[['Text', 'Label']]
output_file = 'NHANES_2001_2002_Stories.csv'
df_final.to_csv(output_file, index=False)

print(f"Tamamlandı! {output_file} oluşturuldu.")
