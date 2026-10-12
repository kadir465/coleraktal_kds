import sys
import os
import pytest

# KDS_Deploy dizinini yola ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "KDS_Deploy")))

from app import anonymize_pii, structured_to_narrative

def test_tc_kimlik_maskeleme():
    text = "TC numaram 12345678901, şikayetim var."
    clean, found = anonymize_pii(text)
    assert "[KİMLİK_NO]" in clean
    assert "12345678901" not in clean
    assert "KİMLİK_NO" in found

def test_telefon_maskeleme():
    text = "Bana 05321234567 veya +905321234567 numarasından ulaşabilirsiniz."
    clean, found = anonymize_pii(text)
    assert "[TELEFON]" in clean
    assert "05321234567" not in clean
    assert "TELEFON" in found

def test_eposta_maskeleme():
    text = "İletişim adresim hasta.ornek@gmail.com dur."
    clean, found = anonymize_pii(text)
    assert "[EPOSTA]" in clean
    assert "hasta.ornek@gmail.com" not in clean
    assert "EPOSTA" in found

def test_iban_maskeleme():
    text = "Hesap numaram TR123456789012345678901234 şeklindedir."
    clean, found = anonymize_pii(text)
    assert "[IBAN]" in clean
    assert "TR123456789012345678901234" not in clean
    assert "IBAN" in found

def test_baglamli_isim_maskeleme():
    text = "Adım Ahmet Yılmaz, son zamanlarda halsizlik hissediyorum."
    clean, found = anonymize_pii(text)
    assert "[İSİM]" in clean
    assert "Ahmet Yılmaz" not in clean
    assert "İSİM" in found

def test_tibbi_ifadeler_korunmali():
    # Bu iki tıbbi ifadenin ASLA maskelenmemesi gerekir
    text1 = "Dışkıda Gizli Kan Testi POZİTİF."
    clean1, found1 = anonymize_pii(text1)
    assert clean1 == text1
    assert "İSİM" not in found1

    text2 = "Ülseratif Kolit tanısı mevcut."
    clean2, found2 = anonymize_pii(text2)
    assert clean2 == text2
    assert "İSİM" not in found2

def test_structured_to_narrative_korunumu():
    # Yapılandırılmış veriden üretilen anlatı test ediliyor
    data = {
        "age": "55",
        "gender": "male",
        "ibd": "uc",
        "fobt": "positive"
    }
    narrative = structured_to_narrative(data)
    assert "Ülseratif Kolit tanısı mevcut." in narrative
    assert "Dışkıda Gizli Kan Testi POZİTİF." in narrative
    # Serbest metne uygulanan anonymize_pii bu klinik anlatıya doğrudan uygulanmaz
