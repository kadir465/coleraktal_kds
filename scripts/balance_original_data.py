import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn.impute import SimpleImputer

# 1. Veriyi Orijinal CSV'den Yükle
print("Veri yükleniyor...")
df = pd.read_csv('NHANES_Kolorektal_Kanser_Verisi.csv')

# 2. Kullanıcı Kolon Eşleştirmesi (set_examinatio.ipynb'den)
kolon_haritasi = {
    'RIDAGEYR': 'Yas',
    'RIAGENDR': 'Cinsiyet',          # 1: Erkek, 2: Kadın
    'BMXBMI': 'Vucut_Kitle_Indeksi', 
    'SMQ020': 'Sigara_Kullanimi',    
    'LBXHGB': 'Hemoglobin',          
    'LBXHCT': 'Hematokrit',
    'LBXWBCSI': 'Akyuvar_WBC',       
    'BAQ080': 'Rektal_Kanama',       
    'BAQ070': 'Bagirsak_Kacirmasi',  
    'WHD020': 'Kilo_Verme_Durumu',   
    'HUQ010': 'Genel_Saglik_Hissi',  
    'MCQ220': 'Kanser_Gecmisi',      
    'MCQ230A': 'Kanser_Turu_1',      
    'MCQ230B': 'Kanser_Turu_2',      
    'MCQ230C': 'Kanser_Turu_3'       
}

# Mevcut kolonları filtrele
mevcut_kolonlar = {k: v for k, v in kolon_haritasi.items() if k in df.columns}
df_temiz = df[list(mevcut_kolonlar.keys())].rename(columns=mevcut_kolonlar)

# 3. Label Oluşturma Mantığı
def etiket_olustur(row):
    if row.get('Kanser_Gecmisi') == 2.0:
        return 0 
    kanser_turleri = [row.get('Kanser_Turu_1'), row.get('Kanser_Turu_2'), row.get('Kanser_Turu_3')]
    if 14.0 in kanser_turleri or 31.0 in kanser_turleri:
        return 1
    return np.nan

df_temiz['Label'] = df_temiz.apply(etiket_olustur, axis=1)
df_temiz = df_temiz.dropna(subset=['Label'])

# Gereksiz kolonları çıkar
for col in ['Kanser_Gecmisi', 'Kanser_Turu_1', 'Kanser_Turu_2', 'Kanser_Turu_3']:
    if col in df_temiz.columns:
        df_temiz = df_temiz.drop(columns=[col])

print(f"Eski Dağılım: {df_temiz['Label'].value_counts().to_dict()}")

# 4. SMOTE için Ön İşleme (Eksik veriler SMOTE ile uyumlu değildir)
imputer = SimpleImputer(strategy='median')
X = df_temiz.drop(columns=['Label'])
y = df_temiz['Label']

X_imputed = imputer.fit_transform(X)

# 5. SMOTE Uygulama (Dengesizliği Giderme)
print("SMOTE uygulanıyor...")
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_imputed, y)

# 6. Dengelenmiş DataFrame Oluşturma
df_balanced = pd.DataFrame(X_resampled, columns=X.columns)
df_balanced['Label'] = y_resampled

print(f"Yeni Dengelenmiş Dağılım: {df_balanced['Label'].value_counts().to_dict()}")

# 7. Kaydet
output_file = 'NHANES_Dengelenmis_Yapisal_Veri.csv'
df_balanced.to_csv(output_file, index=False)
print(f"Başarılı! Dengelenmiş veri seti kaydedildi: {output_file}")
