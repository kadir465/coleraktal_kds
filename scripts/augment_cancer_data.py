import pandas as pd
import random
import os

def generate_synthetic_cancer_narrative():
    """
    Generates a professional and consistent natural language patient narrative 
    specifically for Colorectal Cancer (Label 1.0).
    """
    # Randomly select demographic profile (Cancer is more common in 45+)
    age = random.choices(
        population=[random.randint(18, 44), random.randint(45, 64), random.randint(65, 85)],
        weights=[0.1, 0.4, 0.5] # Weighted towards older population
    )[0]
    
    gender = random.choice(["erkek", "kadın"])
    
    # Intros
    intros = [
        f"Merhaba, {age} yaşında bir {gender} hastayım.",
        f"İyi günler, {age} yaşındayım ({gender}). Belirtilerimi paylaşmak istiyorum.",
        f"Doktor bey, ben {gender} bir hastanızım, yaşım {age}.",
        f"{age} yaşındaki {gender} bir birey olarak son zamanlardaki sağlık durumumu özetlemek gerekirse:",
        f"Şikayetlerimi anlatmak gerekirse; {age} yaşında bir {gender} bireyim."
    ]
    
    # Lab values (Cancer patients often have low HGB due to internal bleeding)
    hgb = round(random.uniform(8.5, 12.5), 1)
    wbc = round(random.uniform(4.0, 15.0), 1) # Sometimes high due to inflammation
    
    lab_notes = [
        f"Kan tahlillerimde hemoglobin değerim {hgb} g/dL olarak ölçüldü, bu durum anemiyi işaret ediyor.",
        f"Hemoglobin seviyem {hgb} civarında, doktorum kan kaybı olabileceğini belirtti.",
        f"Tahlil sonuçlarımda WBC değerim {wbc} çıktı, vücudumda bir inflamasyon olduğu söyleniyor.",
        f"Düşük hemoglobin ({hgb}) ve yüksek sedimentasyon değerlerim var.",
        f"Kansızlık şikayetim var, tahlilde HGB {hgb} çıktı."
    ]
    
    # Weight loss (Common in advanced stages)
    kilo_kaybi = random.randint(10, 45)
    weight_notes = [
        f"Son 6 ayda istemsizce {kilo_kaybi} lbs kilo verdim.",
        f"Diyet yapmamama rağmen {kilo_kaybi} lbs kadar zayıfladım.",
        f"Hızla kilo kaybettiğimi fark ettim, yaklaşık {kilo_kaybi} lbs gitti.",
        f"İştahım azaldı ve {kilo_kaybi} lbs verdim.",
        "Kilomda ani bir düşüş var."
    ]
    
    # Specific Symptoms (Colorectal Focus)
    specific_symptoms = [
        "Dışkımda parlak kırmızı kan fark ediyorum.",
        "Dışkılama alışkanlığımda belirgin bir değişiklik var; bazen çok ince dışkılıyorum.",
        "Karın bölgemde dinmeyen kramplar ve şişkinlik hissi mevcut.",
        "Sürekli bir yorgunluk halindeyim, günlük işlerimi yapmakta zorlanıyorum.",
        "Dışkılamadan sonra bile tam boşalamama hissi yaşıyorum.",
        "Dışkım normalden çok daha koyu renkte, neredeyse siyah (melena) çıkıyor.",
        "Bağırsak hareketlerimde düzensizlik var; sık sık ishal ve kabızlık atakları geçiriyorum.",
        "Alt karın bölgemde geçmeyen künt bir ağrı var.",
        "Rektal bölgede baskı hissi duyuyorum."
    ]
    
    # Smoking status
    smoking = random.choice([
        "Yıllardır sigara kullanıyorum.",
        "Aktif sigara içicisiyim.",
        "Sigara kullanmıyorum.",
        "Eskiden içiyordum ama bıraktım.",
        "" # Blank
    ])
    
    # Assemble narrative
    parts = [random.choice(intros)]
    if smoking: parts.append(smoking)
    if random.random() > 0.3: parts.append(random.choice(weight_notes))
    parts.append(random.choice(lab_notes))
    
    # Add 2-3 specific symptoms
    symptom_count = random.randint(2, 3)
    parts.extend(random.sample(specific_symptoms, symptom_count))
    
    return " ".join([p for p in parts if p])

def augment_dataset(input_file, target_cancer_count=45000):
    print(f"Loading dataset: {input_file}")
    df = pd.read_csv(input_file)
    
    # Handle unnamed columns or mapping
    # The user's request showed empty column name for index and then 1.0 for Label
    # Let's check columns
    print(f"Current columns: {df.columns.tolist()}")
    
    # Identify Label column
    label_col = 'Label'
    if 'Label' not in df.columns:
        # Try to find it by content
        for col in df.columns:
            if df[col].isin([0.0, 1.0]).all():
                label_col = col
                break
    
    comment_col = 'Hasta_Yorumu'
    if 'Hasta_Yorumu' not in df.columns:
        for col in df.columns:
            if df[col].dtype == object and df[col].str.len().mean() > 50:
                comment_col = col
                break

    current_cancer_count = len(df[df[label_col] == 1.0])
    needed_count = target_cancer_count - current_cancer_count
    
    if needed_count <= 0:
        print(f"Dataset already has {current_cancer_count} cancer cases. No augmentation needed.")
        return

    print(f"Current cancer cases: {current_cancer_count}")
    print(f"Generating {needed_count} synthetic cancer cases...")
    
    synthetic_data = []
    for i in range(needed_count):
        narrative = generate_synthetic_cancer_narrative()
        synthetic_data.append({
            comment_col: narrative,
            label_col: 1.0,
            'Source_File': 'Synthetic_Augmentation'
        })
        if (i+1) % 5000 == 0:
            print(f"Generated {i+1} records...")
            
    df_synthetic = pd.DataFrame(synthetic_data)
    
    # Combine
    df_balanced = pd.concat([df, df_synthetic], ignore_index=True)
    
    # Save output
    output_path = input_file.replace('.csv', '_Balanced.csv')
    df_balanced.to_csv(output_path, index=False)
    
    print(f"\nAugmentation Complete!")
    print(f"Original Records: {len(df)}")
    print(f"Synthetic Cancer Added: {needed_count}")
    print(f"Final Total Records: {len(df_balanced)}")
    print(f"Final Class Distribution:\n{df_balanced[label_col].value_counts()}")
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    input_csv = r"data/processed/Final_NHANES_Patient_Narratives.csv"
    if os.path.exists(input_csv):
        augment_dataset(input_csv, target_cancer_count=45000)
    else:
        print(f"File not found: {input_csv}")
