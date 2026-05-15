import os
# Tüm olası API key çakışmalarını temizle
for _k in ["GOOGLE_API_KEY", "GEMINI_API_KEY", "GENAI_API_KEY", "GOOGLE_GENAI_API_KEY"]:
    if _k in os.environ:
        del os.environ[_k]
import re
import math
import logging
import numpy as np
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Flask'in kendi loglarını sustur
werkzeug_log = logging.getLogger('werkzeug')
werkzeug_log.setLevel(logging.ERROR)

app = Flask(__name__)
CORS(app)

BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR     = os.path.dirname(BASE_DIR)
MODEL_PATH     = os.path.join(PARENT_DIR, "models", "Kanser_Riski_Modeli_Temiz")
REHBER_PATH    = os.path.join(PARENT_DIR, "tibbi_rehber.txt")
GOOGLE_API_KEY = "AIzaSyDJ6SDiGaNux3SMlpkvtt-ucwXUeSdFOBs"

# Çalışan script'deki pattern: modül seviyesinde configure + model
genai.configure(api_key=GOOGLE_API_KEY)
_llm_model = genai.GenerativeModel('gemini-2.5-flash')

_electra_model     = None
_electra_tokenizer = None
_rag_model         = None
_rag_chunks        = None
_rag_embeddings    = None
# _gemini_model kaldırıldı — artık modül seviyesinde _llm_model kullanılıyor

# ─────────────────────────────────────────────────────────
# 1. PII FILTER  (KVKK / HIPAA uyum)
# ─────────────────────────────────────────────────────────
PII_PATTERNS = [
    # TC kimlik no (11 hane, ilk hane 0 olamaz)
    (re.compile(r'\b[1-9]\d{10}\b'),                      "[KİMLİK_NO]"),
    # Telefon  05xx / +905xx / 0212 / 0312 ...
    (re.compile(r'(\+90|0)[\s\-]?(\d[\s\-]?){10}'),       "[TELEFON]"),
    # E-posta
    (re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'), "[EPOSTA]"),
    # Tarih (dd.mm.yyyy veya dd/mm/yyyy)
    (re.compile(r'\b\d{1,2}[./]\d{1,2}[./]\d{4}\b'),      "[TARİH]"),
    # IBAN
    (re.compile(r'\bTR\d{2}[\s]?(\d{4}[\s]?){5}\d{2}\b', re.IGNORECASE), "[IBAN]"),
    # İsim-soyisim heuristic: 2-3 büyük harfle başlayan Türkçe kelime dizisi
    (re.compile(r'\b[A-ZÇĞİÖŞÜ][a-zçğışöüA-ZÇĞİÖŞÜ]{1,}\s[A-ZÇĞİÖŞÜ][a-zçğışöüA-ZÇĞİÖŞÜ]{1,}(\s[A-ZÇĞİÖŞÜ][a-zçğışöüA-ZÇĞİÖŞÜ]{1,})?'), "[İSİM]"),
]

def anonymize_pii(text: str) -> tuple[str, list]:
    """PII içeren bilgileri maskele. (temiz_metin, bulunan_pii_tipleri) döndür."""
    found = []
    for pattern, replacement in PII_PATTERNS:
        matches = pattern.findall(text)
        if matches:
            found.append(replacement.strip("[]"))
            text = pattern.sub(replacement, text)
    return text, found

# ─────────────────────────────────────────────────────────
# 2. XAI – Risk anahtar kelimeleri
# ─────────────────────────────────────────────────────────
RISK_KEYWORDS = {
    "critical": [
        "kanama","kan","hematokezi","melena","rektal","dışkıda kan",
        "istemsiz kilo kaybı","kilo kaybı","anemi","demir eksikliği",
        "tam tıkanıklık","ileus","perforasyon","bağırsak delinme",
        "acil","baş dönmesi","bayılma",
    ],
    "high": [
        "ince dışkı","kalem gibi","tuvalet alışkanlığı","kabız","ishal",
        "kramp","karın ağrısı","karın şişliği","tenezm","boşalamama",
        "kolonoskopi","polip","adenom","ülseratif kolit","crohn",
        "inflamatuar bağırsak","aile öyküsü","kanser öyküsü",
        "yorgunluk","halsizlik","iştahsızlık",
    ],
    "medium": [
        "sigara","alkol","obez","kilolu","bmi","diyabet","hipertansiyon",
        "hareketsiz","kırmızı et","işlenmiş gıda","fast food",
        "50 yaş","60 yaş","70 yaş","aile","kardeş","anne","baba",
    ],
}

def extract_keywords(text: str) -> dict:
    """Metindeki risk kelimelerini kategori bazında bul."""
    text_lower = text.lower()
    found = {"critical": [], "high": [], "medium": []}
    for cat, words in RISK_KEYWORDS.items():
        for w in words:
            if w in text_lower:
                found[cat].append(w)
    return found

def highlight_text(text: str, keywords: dict) -> str:
    """Anahtar kelimeleri HTML span ile işaretle (büyük/küçük harf duyarsız)."""
    cat_class = {"critical": "kw-critical", "high": "kw-high", "medium": "kw-medium"}
    # Önce uzun kelimeleri işle (çakışma önleme)
    all_words = []
    for cat, words in keywords.items():
        for w in words:
            all_words.append((w, cat))
    all_words.sort(key=lambda x: -len(x[0]))

    used_spans = []

    def overlaps(start, end):
        for s, e in used_spans:
            if start < e and end > s:
                return True
        return False

    result = text
    offset = 0
    matches_list = []
    for word, cat in all_words:
        for m in re.finditer(re.escape(word), text, re.IGNORECASE):
            if not overlaps(m.start(), m.end()):
                matches_list.append((m.start(), m.end(), word, cat))
                used_spans.append((m.start(), m.end()))

    matches_list.sort(key=lambda x: x[0])
    result = ""
    prev = 0
    for start, end, word, cat in matches_list:
        result += re.sub(r'[<>&]', lambda m: {'<':'&lt;','>':'&gt;','&':'&amp;'}[m.group()], text[prev:start])
        span_word = text[start:end]
        result += f'<span class="{cat_class[cat]}" title="{cat.upper()} RİSK">{span_word}</span>'
        prev = end
    result += re.sub(r'[<>&]', lambda m: {'<':'&lt;','>':'&gt;','&':'&amp;'}[m.group()], text[prev:])
    return result

# ─────────────────────────────────────────────────────────
# 3. Yapılandırılmış veriden anlatı metni üret
# ─────────────────────────────────────────────────────────
def structured_to_narrative(s: dict) -> str:
    """Form alanlarını klinisyene yönelik anlatı metne dönüştür."""
    parts = []
    # Demografi
    age    = s.get("age", "")
    gender = "erkek" if s.get("gender") == "male" else "kadın" if s.get("gender") == "female" else ""
    height = s.get("height", "")
    weight = s.get("weight", "")
    bmi_str = ""
    if height and weight:
        try:
            bmi = float(weight) / ((float(height) / 100) ** 2)
            category = ("zayıf" if bmi < 18.5 else "normal kilolu" if bmi < 25
                        else "fazla kilolu" if bmi < 30 else "obez")
            bmi_str = f" (BMI: {bmi:.1f} – {category})"
        except Exception:
            pass
    if age or gender:
        demo = f"{age} yaşında {gender} hasta.{bmi_str}"
        parts.append(demo.strip())

    # Aile öyküsü
    fam = s.get("family_history", "none")
    fam_age = s.get("family_dx_age", "")
    if fam == "first_degree":
        fa = f"1. derece akrabada (anne/baba/kardeş) kolorektal kanser öyküsü mevcut"
        if fam_age:
            fa += f", tanı yaşı: {fam_age}"
        parts.append(fa + ".")
    elif fam == "second_degree":
        parts.append("2. derece akrabada kolorektal kanser öyküsü var.")
    elif fam == "none":
        parts.append("Ailede kolorektal kanser öyküsü yok.")

    # Tıbbi geçmiş
    colonoscopy = s.get("colonoscopy", "never")
    if colonoscopy == "normal":
        parts.append("Daha önce kolonoskopi yapılmış, sonuç normal.")
    elif colonoscopy == "polyp":
        parts.append("Daha önce kolonoskopide polip saptanmış ve alınmış.")
    elif colonoscopy == "advanced":
        parts.append("Önceki kolonoskopide ileri evre adenom saptanmış.")
    elif colonoscopy == "never":
        parts.append("Daha önce kolonoskopi yapılmamış.")

    fobt = s.get("fobt", "")
    if fobt == "positive":
        parts.append("Dışkıda Gizli Kan Testi (FOBT/FIT) POZİTİF.")
    elif fobt == "negative":
        parts.append("Dışkıda Gizli Kan Testi negatif.")

    ibd = s.get("ibd", "none")
    if ibd == "uc":
        parts.append("Ülseratif Kolit tanısı mevcut (inflamatuar bağırsak hastalığı).")
    elif ibd == "crohn":
        parts.append("Crohn hastalığı tanısı mevcut.")

    # Yaşam tarzı
    lifestyle = []
    if s.get("smoking") == "yes":    lifestyle.append("sigara kullanıyor")
    if s.get("smoking") == "former": lifestyle.append("eski sigara kullanıcısı")
    if s.get("alcohol") == "yes":    lifestyle.append("alkol kullanıyor")
    if s.get("activity") == "low":   lifestyle.append("hareketsiz yaşam tarzı")
    if s.get("diet") == "processed": lifestyle.append("işlenmiş/kırmızı et ağırlıklı beslenme")
    if lifestyle:
        parts.append("Yaşam tarzı: " + ", ".join(lifestyle) + ".")

    # Kronik hastalıklar
    chronic = []
    if s.get("diabetes") == "yes":      chronic.append("tip 2 diyabet")
    if s.get("hypertension") == "yes":  chronic.append("hipertansiyon")
    if chronic:
        parts.append("Kronik hastalıklar: " + ", ".join(chronic) + ".")

    return " ".join(parts)

# ─────────────────────────────────────────────────────────
# Model loaders
# ─────────────────────────────────────────────────────────
def load_electra():
    global _electra_model, _electra_tokenizer
    if _electra_model is None:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        logger.info("ELECTRA yükleniyor…")
        _electra_tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        _electra_model     = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
        _electra_model.eval()
        logger.info("ELECTRA hazır.")
    return _electra_tokenizer, _electra_model

def load_rag():
    global _rag_model, _rag_chunks, _rag_embeddings
    if _rag_model is None:
        from sentence_transformers import SentenceTransformer
        logger.info("RAG yükleniyor…")
        _rag_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        with open(REHBER_PATH, "r", encoding="utf-8") as f:
            text = f.read()
        _rag_chunks     = [c.strip() for c in text.split("\n\n") if len(c.strip()) > 30]
        _rag_embeddings = _rag_model.encode(_rag_chunks, convert_to_numpy=True)
        logger.info(f"RAG hazır: {len(_rag_chunks)} parça.")
    return _rag_model, _rag_chunks, _rag_embeddings

def _gemini_generate(prompt: str) -> str:
    """Çalışan script'deki gibi: modül seviyesi _llm_model ile içerik üret."""
    cevap = _llm_model.generate_content(prompt)
    return cevap.text

def predict_risk(text: str) -> dict:
    import torch
    tokenizer, model = load_electra()
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits.clone()
        
        # Kullanıcı talebi: Logit cezası ve kalibrasyon
        # logits[0][1] -= 4 -> Risk sınıfına (Label 1) ceza puanı (hassasiyeti dengelemek için)
        logits[0][1] -= 4
        T = 2.9 # Sıcaklık kalibrasyonu
        kalibre_logits = logits / T
        
        olasiliklar = torch.softmax(kalibre_logits, dim=-1)
        # Veri seti analizi: Label 1 = Risk/Kanser, Label 0 = Sağlıklı
        # Kullanıcı snippet'ine göre index 1 risk oranıdır.
        risk_prob = olasiliklar[0][1].item()
        healthy_prob = olasiliklar[0][0].item()
        
    return {
        "risk_percent":    round(risk_prob * 100, 1),
        "healthy_percent": round(healthy_prob * 100, 1),
        "confidence":      round(float(max(olasiliklar[0])), 3),
        "label":           1 if risk_prob >= 0.5 else 0,
    }

def retrieve_context(query: str, top_k: int = 3) -> str:
    from sklearn.metrics.pairwise import cosine_similarity
    rag_model, chunks, embeddings = load_rag()
    q_emb = rag_model.encode([query], convert_to_numpy=True)
    sims  = cosine_similarity(q_emb, embeddings)[0]
    idxs  = np.argsort(sims)[::-1][:top_k]
    return "\n\n".join(chunks[i] for i in idxs)

def get_llm_explanation(patient_text: str, risk_result: dict, context: str, keywords: dict) -> str:
    risk  = risk_result["risk_percent"]
    label = "YÜKSEK RİSK" if risk_result["label"] == 1 else "DÜŞÜK RİSK"
    kw_summary = (
        f"Kritik belirtiler: {', '.join(keywords['critical']) or 'yok'} | "
        f"Yüksek risk faktörleri: {', '.join(keywords['high']) or 'yok'} | "
        f"Orta risk faktörleri: {', '.join(keywords['medium']) or 'yok'}"
    )
    prompt = f"""Sen hastaya destek veren empatik bir tıbbi yapay zeka asistanısın. Aşağıdaki formatı ve başlıkları BİREBİR KULLANARAK, hastanın anlayacağı dilde okunaklı bir rapor hazırla. Asla aşırı emoji kullanma (hiç emoji kullanmasan da olur).

HASTA BİLGİSİ:
{patient_text}

SİSTEM SONUÇLARI:
- Risk Skoru: %{risk} ({label})
- Rehber (RAG) Bilgisi: {context}

LÜTFEN SADECE AŞAĞIDAKİ ŞABLONU VE BAŞLIKLARI KULLANARAK YANIT VER:

**Yapay Zeka Değerlendirme Skoru**
(Burada sistemin hastanın şikayetlerini tıbbi rehberlerle karşılaştırdığını ve ön değerlendirme risk skorunu %{risk} olarak bulduğunu yaz. Ardından bunun kesin tanı olmadığını, sadece istatistiksel bir uyarı olduğunu belirten kısa bir paragraf ekle.)

**Dikkate Alınan Önemli Belirtileriniz**
(Burada şu cümleyi kullanarak başla: "Bu değerlendirmenin ortaya çıkmasında rol oynayan ve tıbbi olarak takip edilmesi gereken bulgularınız şunlardır:")
(Ardından hastanın riskli bulgularını alt alta, HER BİRİ YENİ BİR SATIRDA olacak şekilde ve "-" işareti ile başlatarak listele.)
(Maddeler bittikten sonra, bu belirtilerin bir arada görülmesinin ne anlama geldiğini açıklayan kısa bir paragraf ekle.)

**Doktor Yönlendirmesi ve Sonraki Adım**
(Eğer risk yüksekse vakit kaybetmeden, düşükse de kontrol amaçlı bir Gastroenteroloji uzmanına görünmesi gerektiğini, uzman hekimin klinik değerlendirme ve gerekirse kolonoskopi gibi ileri tetkiklerle doğru planı yapacağını anlatan bir paragraf yaz.)
(Son olarak, "Unutmayın; belirtileri erken fark edip uzman kontrolüne başvurmak, sağlığınız için atabileceğiniz en güçlü ve güvenli adımdır." minvalinde rahatlatıcı ve yönlendirici bir kapanış cümlesi yap.)
"""
    return _gemini_generate(prompt)

# ─────────────────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        free_text  = (data.get("text") or "").strip()
        structured = data.get("structured", {})

        # Yapılandırılmış veriden anlatı üret
        narrative = structured_to_narrative(structured)

        # Birleşik metin
        combined = "\n".join(filter(None, [narrative, free_text]))
        if len(combined) < 20:
            return jsonify({"error": "Lütfen daha fazla bilgi girin."}), 400

        # PII anonimleştirme
        clean_text, pii_found = anonymize_pii(combined)
        if pii_found:
            logger.warning(f"PII tespit edildi ve maskelendi: {pii_found}")

        logger.info(f"Analiz | uzunluk={len(clean_text)} | PII={pii_found}")

        # ELECTRA risk tahmini (ham metin üzerinden – daha doğru)
        risk_result = predict_risk(clean_text)
        logger.info(f"Risk: %{risk_result['risk_percent']}")

        # XAI – anahtar kelime tespiti (orijinal birleşik metin üzerinden)
        keywords    = extract_keywords(combined)
        highlighted = highlight_text(combined, keywords)

        # RAG bağlamı
        context = retrieve_context(clean_text)

        # Gemini açıklaması
        llm_text = ""
        if GOOGLE_API_KEY:
            try:
                llm_text = get_llm_explanation(clean_text, risk_result, context, keywords)
            except Exception as e:
                logger.error(f"LLM hatası: {e}")
                llm_text = f"⚠️ LLM açıklaması alınamadı: {e}"
        else:
            llm_text = "⚠️ GOOGLE_API_KEY tanımlı değil. LLM devre dışı."

        return jsonify({
            "success":         True,
            "risk_percent":    risk_result["risk_percent"],
            "healthy_percent": risk_result["healthy_percent"],
            "confidence":      risk_result["confidence"],
            "label":           risk_result["label"],
            "llm_explanation": llm_text,
            "highlighted_text": highlighted,
            "keywords":        keywords,
            "pii_found":       pii_found,
            "pii_masked":      len(pii_found) > 0,
        })

    except Exception as e:
        logger.error(f"Analiz hatası: {e}", exc_info=True)
        return jsonify({"error": f"Sunucu hatası: {str(e)}"}), 500

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "gemini_configured": bool(GOOGLE_API_KEY)})

@app.route("/api/debug_key", methods=["GET"])
def debug_key():
    """Flask process içindeki anahtar ve model durumunu göster."""
    import os
    key_in_code = GOOGLE_API_KEY[:10] + "..." if GOOGLE_API_KEY else "YOK"
    env_keys = {k: (os.environ.get(k, "")[:10] + "...") for k in
                ["GOOGLE_API_KEY","GEMINI_API_KEY","GENAI_API_KEY","GOOGLE_GENAI_API_KEY"]
                if os.environ.get(k)}
    # Canlı Gemini testi
    try:
        result = _llm_model.generate_content("Say OK")
        gemini_live = "OK: " + result.text[:50]
    except Exception as e:
        gemini_live = f"HATA: {e}"
    return jsonify({
        "key_in_code_prefix": key_in_code,
        "env_keys_found": env_keys,
        "gemini_live_test": gemini_live,
        "model_type": str(type(_llm_model))
    })

if __name__ == "__main__":
    logger.info("🏥 KDS Web Uygulaması başlatılıyor…")
    app.run(debug=False, use_reloader=False, host="0.0.0.0", port=5000)
