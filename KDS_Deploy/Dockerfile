# Temel Python imajini kullaniyoruz
FROM python:3.11-slim

# Hugging Face guvenlik kurallari geregi root olmayan bir kullanici olusturuyoruz
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Calisma dizinini belirliyoruz
WORKDIR /app

# Oncce kutuphane listesini kopyalayip kuruyoruz
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Projedeki tum dosyalari sunucuya kopyaliyoruz
COPY --chown=user . .

# Hugging Face'in varsayilan yayin portu
EXPOSE 7860

# Flask sunucusunu Gunicorn ile baslatiyoruz (Uretim ortami icin en sagliklisi)
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]