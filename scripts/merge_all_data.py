import pandas as pd

files = [
    'balanced_colorectal_data.csv', 
    'NHANES_Hasta_Hikayeleri_Final.csv', 
    'NHANES_2001_2002_Stories.csv',
    'korelaktal_hasta_hikayeleri.csv'
]

dataframes = []

for f in files:
    try:
        df = pd.read_csv(f)
        # Sütun isimlerini normalize edelim (Hepsini 'Text' ve 'Label' yapalım)
        if 'Hasta_Hikayesi' in df.columns:
            df = df.rename(columns={'Hasta_Hikayesi': 'Text'})
        elif 'Hasta_Yorumu' in df.columns:
            df = df.rename(columns={'Hasta_Yorumu': 'Text'})
            
        # Sadece Text ve Label kalsın
        df = df[['Text', 'Label']]
        dataframes.append(df)
        print(f"{f} yüklendi: {len(df)} satır.")
    except Exception as e:
        print(f"{f} yüklenirken hata oluştu: {e}")

# Birleştir
df_all = pd.concat(dataframes, ignore_index=True)

# Yinelenenleri kaldır (Aynı hikayeler varsa temizleyelim)
eski_boyut = len(df_all)
df_all = df_all.drop_duplicates(subset=['Text'])
yeni_boyut = len(df_all)

# Kaydet
output_file = 'Korelaktal_Tum_Veriler_Merge.csv'
df_all.to_csv(output_file, index=False)

# Durum Bilgisi
print("\n--- BİRLEŞTİRME DURUMU ---")
print(f"Toplam Satır Sayısı: {len(df_all)}")
print(f"Silinen Yinelenen Satır Sayısı: {eski_boyut - yeni_boyut}")
print("\nSınıf Dağılımı:")
print(df_all['Label'].value_counts())

print(f"\nFinal dosyası kaydedildi: {output_file}")
