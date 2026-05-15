import pandas as pd
import random
import os

def create_user_comment(row, cols):
    """
    Generates a natural language user comment based on the row data.
    Variety is added to ensure it's not repetitive.
    """
    # Extract data with defaults
    yas = row.get(cols.get('Yas'), None)
    cinsiyet_val = row.get(cols.get('Cinsiyet'), None)
    hgb = row.get(cols.get('HGB'), None)
    wbc = row.get(cols.get('WBC'), None)
    sigara_val = row.get(cols.get('Sigara'), None)
    kilo_kaybi = row.get(cols.get('KiloKaybi'), None)
    label = row.get(cols.get('Label'), 0)

    # Clean values
    yas = int(yas) if pd.notna(yas) else random.randint(20, 80)
    cinsiyet = "erkek" if cinsiyet_val == 1.0 else "kadın"
    
    # Variety in greetings and intros
    greetings = [
        f"Merhaba, {yas} yaşında bir {cinsiyet} olarak durumumu paylaşmak istiyorum.",
        f"İyi günler. Yaşım {yas}, cinsiyetim {cinsiyet}.",
        f"Selamlar, {yas} yaşındayım ve bir {cinsiyet} hastayım.",
        f"Doktor bey/hanım, ben {yas} yaşında bir {cinsiyet} hastanızım.",
        f"Şikayetlerimi anlatmak gerekirse, {yas} yaşında bir {cinsiyet} bireyim."
    ]
    
    comment_parts = [random.choice(greetings)]

    # Smoking
    if pd.notna(sigara_val):
        # NHANES SMQ020: 1=Yes, 2=No
        if sigara_val == 1.0:
            comment_parts.append(random.choice([
                "Uzun süredir sigara kullanıyorum.",
                "Maalesef sigara alışkanlığım var.",
                "Aktif bir sigara kullanıcısıyım."
            ]))
        elif sigara_val == 2.0:
            comment_parts.append(random.choice([
                "Sigara kullanmıyorum.",
                "Hayatım boyunca sigaradan uzak durdum.",
                "Sigara içme alışkanlığım yok."
            ]))

    # Weight Loss / Weight
    if pd.notna(kilo_kaybi):
        # Handle NHANES outliers (9999, 7777, or just huge values)
        if abs(kilo_kaybi) < 150: 
            if abs(kilo_kaybi) > 5:
                if kilo_kaybi > 0:
                    comment_parts.append(f"Son zamanlarda sebepsiz yere {int(kilo_kaybi)} lbs kilo verdim.")
                else:
                    comment_parts.append(f"Kilomda bir artış fark ettim, yaklaşık {int(abs(kilo_kaybi))} lbs aldım.")
            else:
                comment_parts.append("Kilomda pek bir değişiklik yok.")

    # Blood Values
    if pd.notna(hgb):
        hgb_limit = 13.5 if cinsiyet == "erkek" else 12.0
        if hgb < hgb_limit:
            comment_parts.append(f"Kan tahlilimde hemoglobin değerim {hgb} çıktı, doktorum kansızlık olduğunu belirtti.")
        else:
            comment_parts.append(f"Hemoglobin seviyem {hgb} civarında, normal denildi.")

    if pd.notna(wbc):
        if wbc > 10.0:
            comment_parts.append(f"Akyuvar sayım ({wbc}) biraz yüksek, vücudumda iltihap olabilirmiş.")
        elif wbc < 4.0:
            comment_parts.append(f"WBC değerim {wbc} ile düşük çıktı.")

    # Cancer Symptoms (Label based)
    if label == 1.0:
        symptoms = [
            "Dışkımda kan fark ettim ve bu durum beni endişelendiriyor.",
            "Bağırsak düzenim tamamen değişti, bazen ishal bazen kabız oluyorum.",
            "Karın bölgemde sürekli bir şişkinlik ve geçmeyen ağrılar var.",
            "Kendimi aşırı yorgun hissediyorum ve iştahım kapandı.",
            "Tuvalete çıktıktan sonra sanki bağırsaklarım tam boşalmamış gibi bir his var."
        ]
        # Add 1-2 symptoms
        comment_parts.extend(random.sample(symptoms, k=random.randint(1, 2)))
    else:
        healthy_notes = [
            "Genel olarak kendimi iyi hissediyorum, sadece kontrol amaçlı geldim.",
            "Belirgin bir şikayetim yok, rutin tahlillerimi yaptırıyorum.",
            "Sağlığıma dikkat etmeye çalışıyorum, check-up için buradayım.",
            "Herhangi bir ağrım veya sızım bulunmuyor."
        ]
        comment_parts.append(random.choice(healthy_notes))

    return " ".join(comment_parts)

def process_file(file_path):
    print(f"Processing: {file_path}")
    try:
        # Optimization: Use usecols if possible, but for now load all to check columns
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    # Dynamic Column Mapping
    mapping = {}
    cols = df.columns.tolist()
    
    # Yas
    if 'Yas' in cols: mapping['Yas'] = 'Yas'
    elif 'RIDAGEYR' in cols: mapping['Yas'] = 'RIDAGEYR'
    
    # Cinsiyet
    if 'Cinsiyet' in cols: mapping['Cinsiyet'] = 'Cinsiyet'
    elif 'RIAGENDR' in cols: mapping['Cinsiyet'] = 'RIAGENDR'
    
    # HGB
    if 'Hemoglobin_Anemi' in cols: mapping['HGB'] = 'Hemoglobin_Anemi'
    elif 'Hemoglobin' in cols: mapping['HGB'] = 'Hemoglobin'
    elif 'LBXHGB' in cols: mapping['HGB'] = 'LBXHGB'
    
    # WBC
    if 'Akyuvar_WBC' in cols: mapping['WBC'] = 'Akyuvar_WBC'
    elif 'LBXWBCSI' in cols: mapping['WBC'] = 'LBXWBCSI'
    
    # Sigara
    if 'Sigara_Gecmisi' in cols: mapping['Sigara'] = 'Sigara_Gecmisi'
    elif 'Sigara_Kullanimi' in cols: mapping['Sigara'] = 'Sigara_Kullanimi'
    elif 'SMQ020' in cols: mapping['Sigara'] = 'SMQ020'
    
    # Kilo Kaybi
    if 'Ani_Kilo_Kaybi_lbs' in cols: mapping['KiloKaybi'] = 'Ani_Kilo_Kaybi_lbs'
    elif 'Kilo_Verme_Durumu' in cols: mapping['KiloKaybi'] = 'Kilo_Verme_Durumu'
    elif 'WHD050' in cols: mapping['KiloKaybi'] = 'WHD050'
    
    # Label
    if 'Hastalik_Durumu_LABEL' in cols: mapping['Label'] = 'Hastalik_Durumu_LABEL'
    elif 'Label' in cols: mapping['Label'] = 'Label'
    elif 'MCQ230A' in cols:
        # NHANES 1999-2000: 14 is Colon, 30 is Rectum
        df['Hastalik_Durumu_LABEL'] = df['MCQ230A'].apply(lambda x: 1.0 if x in [14.0, 30.0] else 0.0)
        mapping['Label'] = 'Hastalik_Durumu_LABEL'
    else:
        mapping['Label'] = None

    # Check if we have the minimum required columns
    if 'Yas' not in mapping or 'Cinsiyet' not in mapping:
        print(f"Skipping {file_path} - Essential columns not found.")
        return

    # Generate comments
    df['Hasta_Yorumu'] = df.apply(lambda row: create_user_comment(row, mapping), axis=1)
    
    # Keep only Comment and Label
    if mapping.get('Label') and mapping['Label'] in df.columns:
        df_final = df[['Hasta_Yorumu', mapping['Label']]]
        df_final.columns = ['Hasta_Yorumu', 'Label']
    else:
        df_final = df[['Hasta_Yorumu']]
        df_final['Label'] = 0.0 # Default

    # Save output
    base_name = os.path.basename(file_path)
    output_name = base_name.replace('.csv', '_Stories.csv')
    output_path = os.path.join(os.path.dirname(file_path), output_name)
    
    df_final.to_csv(output_path, index=False)
    print(f"Saved to: {output_path}")

# List of files to process
files_to_process = [
    r"data/raw/2021-2023/NHANES_2021_2023_Dengelenmis_Veri.csv",
    r"data/raw/2017-2018/NHANES_2017_2018_Korelasyonlu_Veriler.csv",
    r"data/raw/2015-2016/NHANES_2015_2016_Korelasyonlu_Veriler.csv",
    r"data/raw/2013-2014/NHANES_2013_2014_Korelasyonlu_Veriler.csv",
    r"data/raw/2011-2012/NHANES_2011_2012_Dengelenmis_Veri.csv",
    r"data/raw/2009-2010/NHANES_2009_2010_Dengelenmis_Veri.csv",
    r"data/raw/2007-2008/NHANES_2007_2008_Korelasyonlu_Veriler.csv",
    r"data/raw/2005-2006/NHANES_2005_2006_Korelasyonlu_Veriler.csv",
    r"data/raw/2003-2004/NHANES_2003_2004_Korelasyonlu_Veriler.csv",
    r"data/raw/2001-2002/NHANES_2001_2002_Korelasyonlu_Veriler.csv",
    r"data/raw/1999-2000/NHANES_1999_2000_Kolorektal_Kanser_Verisi.csv"
]

if __name__ == "__main__":
    for f in files_to_process:
        if os.path.exists(f):
            process_file(f)
        else:
            print(f"File not found: {f}")
