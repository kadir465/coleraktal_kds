import pandas as pd
import random

# 1. Veriyi Yükle
print("Dengelenmiş veri yükleniyor...")
df = pd.read_csv('NHANES_Dengelenmis_Yapisal_Veri.csv')

def yorum_olustur(row):
    yas = int(row['Yas'])
    cinsiyet = "erkek" if row['Cinsiyet'] == 1.0 else "kadın"
    sigara = "Sigara kullanıyorum." if row['Sigara_Kullanimi'] == 1.0 else "Sigara kullanmıyorum."
    hgb = row['Hemoglobin']
    wbc = row['Akyuvar_WBC']
    kilo = row['Kilo_Verme_Durumu'] # Bu değerler pound cinsinden ağırlık gibi görünüyor
    label = row['Label']
    
    # Giriş Cümleleri
    giris = [
        f"Merhaba, ben {yas} yaşında bir {cinsiyet} hastayım.",
        f"{yas} yaşındayım, {cinsiyet} hastayım ve şikayetlerimi paylaşmak istiyorum.",
        f"İyi günler, {yas} yaşında bir {cinsiyet} olarak yazıyorum."
    ]
    
    paragraf = [random.choice(giris)]
    
    # Sigara Durumu
    paragraf.append(sigara)
    
    # Kilo Durumu (Tahmini bir ağırlık yorumu)
    if kilo > 200:
        paragraf.append(f"Kilom biraz fazla ({int(kilo)} lbs), bu da beni yoruyor.")
    else:
        paragraf.append(f"Şu anki kilom {int(kilo)} lbs civarında.")
        
    # Kan Değerleri Yorumu
    # Erkek HGB < 13.5, Kadın HGB < 12.0 Anemi belirtisidir
    hgb_limit = 13.5 if row['Cinsiyet'] == 1.0 else 12.0
    if hgb < hgb_limit:
        paragraf.append(f"Yapılan kan tahlilimde hemoglobin değerim {hgb} çıktı, doktorum düşük olduğunu söyledi.")
    else:
        paragraf.append(f"Hemoglobin değerim {hgb}, genel olarak normal görünüyor.")
        
    # WBC (Enflamasyon belirtisi olabilir)
    if wbc > 10.0:
        paragraf.append(f"Akyuvar (WBC) sayım {wbc} ile yüksek çıktı, vücudumda bir iltihap olabilir.")
    
    # Kanser (Label 1) vakalarına özel belirti ekleme (Kullanıcı "belirtiler içeren" dediği için)
    if label == 1.0:
        belirtiler = [
            "Son zamanlarda dışkımda kan görmeye başladım ve bu beni çok korkutuyor.",
            "Bağırsak alışkanlıklarım tamamen değişti, sürekli karın ağrısı ve şişkinlik yaşıyorum.",
            "İştahım yok ve sebepsiz yere çok hızlı kilo verdim.",
            "Sürekli bir yorgunluk halim var ve tuvalete çıktıktan sonra tam boşalamama hissi yaşıyorum.",
            "Dışkı rengimde koyulaşma ve şekil bozukluğu (ince dışkı) fark ettim."
        ]
        # Rastgele 1 veya 2 belirti ekleyelim
        secilen_belirtiler = random.sample(belirtiler, k=random.randint(1, 2))
        paragraf.extend(secilen_belirtiler)
    else:
        # Sağlıklı vakalar için daha rutin şikayetler veya temiz durumlar
        saglikli_ek = [
            "Düzenli kontrollerimi yaptırmak istiyorum.",
            "Şu an için belirgin bir ağrım veya sızım yok.",
            "Genel check-up için bu bilgileri veriyorum.",
            "Kendimi genel olarak sağlıklı hissediyorum ama tedbirli olmakta fayda var."
        ]
        paragraf.append(random.choice(saglikli_ek))
        
    return " ".join(paragraf)

print("Kullanıcı yorumları oluşturuluyor...")
df['Hasta_Yorumu'] = df.apply(yorum_olustur, axis=1)

# Sadeleştirme: Sadece Yorum ve Label kalsın
df_final = df[['Hasta_Yorumu', 'Label']]

# Kaydet
output_file = 'NHANES_Hasta_Hikayeleri_Final.csv'
df_final.to_csv(output_file, index=False)

print(f"İşlem tamamlandı! {len(df_final)} satırlık veri seti oluşturuldu.")
print(f"Dosya yolu: {output_file}")

# Örnek göster
print("\nÖrnek Veriler:")
print(df_final.head())
