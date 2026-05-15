import pandas as pd
import os

# Dosya yollarını tanımla
file1_path = r'data/processed/Final_NHANES_Patient_Narratives_Balanced.csv'
file2_path = r'data/processed/Korelaktal_Tum_Veriler_Merge.csv'
output_path = r'data/final/Korelaktal_Final_Dataset.csv'

print("Veriler yükleniyor...")

# İlk dosyayı oku
# Bu dosyada hem 'Text' hem 'Hasta_Yorumu' sütunları var, bunları birleştireceğiz
df1 = pd.read_csv(file1_path)
df1['hasta yorumu'] = df1['Hasta_Yorumu'].fillna(df1['Text'])
df1 = df1[['Label', 'hasta yorumu']].rename(columns={'Label': 'label'})

# İkinci dosyayı oku
# Bu dosyada 'Text' sütunu hasta yorumu olarak kullanılıyor
df2 = pd.read_csv(file2_path)
df2 = df2[['Label', 'Text']].rename(columns={'Label': 'label', 'Text': 'hasta yorumu'})

print(f"İlk dosya satır sayısı: {len(df1)}")
print(f"İkinci dosya satır sayısı: {len(df2)}")

# Verileri birleştir
df_final = pd.concat([df1, df2], ignore_index=True)

print(f"Toplam satır sayısı: {len(df_final)}")

# Eksik verileri temizle (opsiyonel ama sağlıklı bir dataset için önemli)
df_final = df_final.dropna(subset=['hasta yorumu', 'label'])

print(f"Temizlik sonrası toplam satır sayısı: {len(df_final)}")

# Sonucu kaydet
df_final.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"İşlem tamamlandı. Yeni dosya: {output_path}")
