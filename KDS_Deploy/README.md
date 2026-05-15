# KDS_Deploy Dizini Dokümantasyonu (Üretim Dağıtımı)

Bu dizin, Kolorektal Klinik Karar Destek Sistemini (KDS) bir web uygulaması olarak dağıtmak için gereken üretime hazır (production-ready) kod tabanını kapsar. Mevcut mimari, Dockerize edilmiş bir Flask ortamı kullanılarak Hugging Face Spaces üzerinde barındırılacak şekilde tasarlanmıştır.

## Mimari ve Bileşenler

- **`app.py`**: Flask web sunucusunun ana yürütme noktası. Bu dosya, uygulama yönlendirmesini (routing) başlatmaktan, önceden eğitilmiş makine öğrenmesi modellerini belleğe yüklemekten, Gemini API istemcisini yapılandırmaktan ve HTTP istek ve yanıtlarını işlemekten sorumludur. Kullanıcı arayüzü, öngörücü modeller ve LLM açıklama üretimi arasında orkestratör görevi görür.
- **`Dockerfile`**: Konteynerize edilmiş ortamı tanımlar. Temel işletim sistemi imajını belirler, sistem düzeyindeki bağımlılıkları kurar, proje dosyalarını kopyalar ve Hugging Face Spaces entegrasyonu için gereken gerekli bağlantı noktalarını (ports) açar.
- **`requirements.txt`**: Python bağımlılıklarının kesin bir manifestosu. Flask, Transformers, Torch, Scikit-learn ve Google Generative AI SDK gibi temel kütüphaneleri içererek farklı ortamlar arasında mutlak tekrarlanabilirlik sağlar.
- **`templates/`**: Ön uç (frontend) kullanıcı arayüzünü oluşturan HTML dosyalarını içerir.
- **`static/`**: Şekillendirme için Basamaklı Stil Şablonları (CSS) ve etkileşimli öğeler için istemci tarafı JavaScript dahil olmak üzere statik varlıkları barındırır.
- **`Kanser_Riski_Modeli_Temiz/`**: İnce ayarı yapılmış ELECTRA modelinin, üretim ortamı için özel olarak belirlenmiş yerelleştirilmiş bir kopyasıdır ve web uygulamasının deneysel `models/` dizinine bağımlı olmamasını sağlar.

## Yerel Yürütme Talimatları

Dağıtım ortamını yerel olarak test etmek için:
1. Terminalinizde bu dizine gidin.
2. Gerekli bağımlılıkları yükleyin: `pip install -r requirements.txt`
3. `GEMINI_API_KEY` bilginizi içeren `.env` dosyasının doğru yapılandırıldığından emin olun.
4. Sunucuyu çalıştırın: `python app.py`
