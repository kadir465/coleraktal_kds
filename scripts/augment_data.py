import pandas as pd
import random
import os

# Configuration
input_file = r'C:\Users\kadir\OneDrive\Masaüstü\korelaktal\Train_Set_Ham.csv'
output_file = r'C:\Users\kadir\OneDrive\Masaüstü\korelaktal\Train_Set_Balanced.csv'
target_sick_count = 80000

def generate_sick_text():
    age = random.randint(35, 90)
    gender = random.choice(["erkek", "kadın"])
    
    # Attributes
    f_hist = random.choice([
        "ailemde kanser geçmişi var", 
        "aile öykümde kolon kanseri vakaları bulunuyor", 
        "birinci derece akrabalarımda kanser görüldü", 
        "ailemde daha önce kanser öyküsü saptandı",
        "genetik olarak kanser riskim var"
    ])
    
    diab_ibd = random.choice([
        "hem diyabetim var hem de inflamatuar bağırsak hastasıyım",
        "şeker hastalığı ve ülseratif kolit ile mücadele ediyorum",
        "kronik olarak diyabet ve bağırsak iltihabı sorunlarım mevcut",
        "tıbbi geçmişimde diyabet ve IBD kayıtları yer alıyor",
        "insülin kullanıyorum ve bağırsaklarımda kronik inflamasyon var"
    ])
    
    lifestyle = random.choice([
        f"Kilom {random.choice(['obez', 'fazla kilolu'])} seviyesinde ve genelde {random.choice(['hareketsizim', 'sedanter bir yaşamım var'])}",
        f"Fiziksel aktivitem {random.choice(['çok düşük', 'yok denecek kadar az'])}, kilom ise {random.choice(['oldukça yüksek', 'sınırların üzerinde'])}",
        f"Vücut kitle indeksim {random.choice(['riskli grupta', 'yüksek'])}. Gün boyu masa başındayım ve {random.choice(['egzersiz yapmıyorum', 'sporla aram yok'])}"
    ])
    
    habits = random.choice([
        "Sigara ve alkol kullanıyorum",
        "Uzun yıllardır sigara içiyorum, alkol tüketimim de mevcut",
        "Sigara bağımlılığım var, alkolü de sosyal olarak alıyorum",
        "Hem tütün hem de alkol alışkanlıklarım bulunmakta"
    ])
    
    # Specific Symptoms for sick group
    symptoms_pool = [
        "dışkıda parlak kırmızı kan fark ettim",
        "tuvalet düzenim tamamen bozuldu",
        "şiddetli karın ağrıları ve kramplar yaşıyorum",
        "istem dışı ve hızlı bir kilo kaybı yaşıyorum",
        "sürekli yorgunluk ve aşırı halsizlik var",
        "dışkı formunda (kalem gibi incelme) değişiklikler var",
        "bağırsaklarımın tam boşalmadığı hissi oluşuyor",
        "anemi ve demir eksikliği tanısı aldım"
    ]
    selected_symptoms = random.sample(symptoms_pool, random.randint(2, 4))
    symptom_str = " ve ".join(selected_symptoms)

    # Templates
    templates = [
        f"Merhaba hocam, {age} yaşındayım. {f_hist}. Ayrıca {diab_ibd}. {lifestyle}. {habits}. Son dönemde {symptom_str} gibi şikayetlerim oluştu. Durumum ne olabilir?",
        f"İyi günler doktor bey, {age} yaşında bir {gender} hastayım. {f_hist} ve {diab_ibd} şikayetlerim var. {lifestyle}. {habits}. {symptom_str} nedeniyle muayene olmak istiyorum.",
        f"Klinik Not: {age} yaş, {gender} hasta. {f_hist}. {diab_ibd} mevcut. {lifestyle.lower()}. {habits.lower()}. Semptomlar: {symptom_str}.",
        f"Muayene Özeti: {age} yaşındaki {gender} hastanın anamnezi: {f_hist}, {diab_ibd}. Yaşam tarzı: {lifestyle}. Alışkanlıklar: {habits}. Şikayet: {symptom_str}.",
        f"Hocam selamlar, {age} yaşındayım, {gender} cinsiyetindeyim. {f_hist}. {diab_ibd}. {lifestyle}. {habits}. {symptom_str} beni çok endişelendiriyor.",
        f"Hasta Profili: {age} yaşında ({gender}). {f_hist} ile birlikte {diab_ibd} tanısı mevcut. {lifestyle}. Madde kullanımı: {habits}. Mevcut şikayetler: {symptom_str}."
    ]
    
    return random.choice(templates)


def main():
    if not os.path.exists(input_file):
        print(f"Hata: {input_file} bulunamadı.")
        return

    df = pd.read_csv(input_file)
    print("Mevcut dağılım:")
    print(df['Label'].value_counts())

    sick_df = df[df['Label'] == 0]
    current_sick_count = len(sick_df)
    
    if current_sick_count >= target_sick_count:
        print(f"Zaten {current_sick_count} adet hastalıklı kayıt var. Ekleme yapılmadı.")
        return

    to_generate = target_sick_count - current_sick_count
    print(f"{to_generate} adet yeni hastalıklı (Label 0) kaydı üretiliyor...")

    new_rows = []
    for _ in range(to_generate):
        new_rows.append({
            'Hasta_Yorumu': generate_sick_text(),
            'Label': 0
        })

    new_df = pd.DataFrame(new_rows)
    final_df = pd.concat([df, new_df], ignore_index=True)
    
    # Shuffle the dataset to mix new and old rows
    final_df = final_df.sample(frac=1).reset_index(drop=True)

    print("Yeni dağılım:")
    print(final_df['Label'].value_counts())
    
    final_df.to_csv(output_file, index=False)
    print(f"İşlem tamamlandı. Dosya kaydedildi: {output_file}")

if __name__ == "__main__":
    main()
