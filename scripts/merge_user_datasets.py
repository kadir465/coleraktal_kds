import pandas as pd
import os

# Dosya yolları
data_files = [
    r'C:\Users\kadir\OneDrive\Masaüstü\korelaktal\data\raw\1999-2000\NHANES_1999_2000_Kullanici_Belirtileri_Dataset.csv',
    r'C:\Users\kadir\OneDrive\Masaüstü\korelaktal\data\raw\2001-2002\NHANES_2001_2002_Korelasyonlu_Veriler.csv',
    r'C:\Users\kadir\OneDrive\Masaüstü\korelaktal\data\raw\2003-2004\NHANES_2003_2004_Kullanici_Belirtileri_Dataset.csv',
    r'C:\Users\kadir\OneDrive\Masaüstü\korelaktal\data\raw\2005-2006\NHANES_2005_2006_Kullanici_Belirtileri_Dataset.csv',
    r'C:\Users\kadir\OneDrive\Masaüstü\korelaktal\data\raw\2007-2008\Kullanici_Belirtileri_Yeni.csv',
    r'C:\Users\kadir\OneDrive\Masaüstü\korelaktal\data\raw\2009-2010\Kullanici_Belirtileri_Guncel.csv',
    r'C:\Users\kadir\OneDrive\Masaüstü\korelaktal\data\raw\2011-2012\Kullanici_Belirtileri_Son.csv',
    r'C:\Users\kadir\OneDrive\Masaüstü\korelaktal\data\raw\2013-2014\Kullanici_Belirtileri_Tum_Gecmis_Ve_Sikayetler.csv',
    r'C:\Users\kadir\OneDrive\Masaüstü\korelaktal\data\raw\2015-2016\NHANES_2015_2016_Kullanici_Belirtileri_Full.csv',
    r'C:\Users\kadir\OneDrive\Masaüstü\korelaktal\data\raw\2017-2018\Kullanici_Belirtileri_Final_Set.csv',
    r'C:\Users\kadir\OneDrive\Masaüstü\korelaktal\data\raw\2021-2023\NHANES_Kullanici_Belirtileri_Full_V2.csv'
]

# Çıktı dosyası yolu
output_file = r'C:\Users\kadir\OneDrive\Masaüstü\korelaktal\data\final\Merged_User_Dataset.csv'

# Yeni dosya yolları
additional_files = [
    r'C:\Users\kadir\OneDrive\Masaüstü\korelaktal\colorectal_cancer_dataset.csv',
    r'C:\Users\kadir\OneDrive\Masaüstü\korelaktal\Kullanici_Belirtileri_Risk_Seti.csv'
]

# Yeni çıktı dosyası yolu
additional_output_file = r'C:\Users\kadir\OneDrive\Masaüstü\korelaktal\data\final\Merged_Colorectal_And_Risk_Set.csv'

def merge_datasets(file_list, output_path):
    merged_df = pd.DataFrame()

    for file in file_list:
        if os.path.exists(file):
            print(f"{file} yükleniyor...")
            df = pd.read_csv(file, low_memory=False)
            merged_df = pd.concat([merged_df, df], ignore_index=True)
        else:
            print(f"Uyarı: {file} bulunamadı ve atlandı.")

    # Birleştirilmiş dataset'i kaydet
    merged_df.to_csv(output_path, index=False)
    print(f"\nBirleştirme tamamlandı. Çıktı dosyası: {output_path}")

def merge_additional_datasets(file_list, output_path):
    merged_df = pd.DataFrame()

    for file in file_list:
        if os.path.exists(file):
            print(f"{file} yükleniyor...")
            df = pd.read_csv(file, low_memory=False)
            merged_df = pd.concat([merged_df, df], ignore_index=True)
        else:
            print(f"Uyarı: {file} bulunamadı ve atlandı.")

    # Birleştirilmiş dataset'i kaydet
    merged_df.to_csv(output_path, index=False)
    print(f"\nBirleştirme tamamlandı. Çıktı dosyası: {output_path}")

if __name__ == "__main__":
    # İlk birleştirme işlemi
    merge_datasets(data_files, output_file)

    # İkinci birleştirme işlemi
    merge_additional_datasets(additional_files, additional_output_file)