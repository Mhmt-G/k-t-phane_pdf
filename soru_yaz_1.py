import os
import shutil
import re
from collections import Counter
from pypdf import PdfReader # pip install pypdf gereklidir

# --- AYARLAR ---
KAYNAK_KLASOR = r"C:\Kullanici\Downloads\Kitaplarim"  # Düzenlenecek klasör
HEDEF_KLASOR = r"C:\Kullanici\Documents\Kutuphanem_Pro"   # Yeni yer

# Kategori Anahtar Kelimeleri (Hem içerik hem dosya adı için)
KATEGORILER = {
    "Yazılım ve Teknoloji": [
        "python", "java", "coding", "algorithm", "html", "css", "yapay zeka", 
        "artificial intelligence", "data science", "machine learning", "kodlama", "software"
    ],
    "Tarih ve Siyaset": [
        "tarih", "savaş", "imparatorluk", "cumhuriyet", "devlet", "history", 
        "war", "politics", "siyaset", "diplomasi", "osmanlı", "atatürk"
    ],
    "Bilim ve Mühendislik": [
        "fizik", "kimya", "biyoloji", "matematik", "mühendislik", "physics", 
        "chemistry", "biology", "math", "integral", "türev", "kuantum", "hücre"
    ],
    "Edebiyat ve Roman": [
        "roman", "hikaye", "öykü", "edebiyat", "novel", "fiction", "şiir", 
        "yazar", "betimleme", "narrative"
    ],
    "Felsefe ve Psikoloji": [
        "felsefe", "psikoloji", "düşünce", "zihin", "davranış", "philosophy", 
        "psychology", "nietzsche", "freud", "bilinç"
    ],
    "Finans ve Ekonomi": [
        "ekonomi", "borsa", "para", "finans", "yatırım", "pazarlama", 
        "economy", "finance", "bitcoin", "trade"
    ]
}

def metin_temizle(metin):
    """Metindeki noktalama işaretlerini kaldırır ve küçük harfe çevirir."""
    return re.sub(r'[^\w\s]', '', metin).lower()

def pdf_icerik_puanla(dosya_yolu):
    """PDF'in ilk sayfalarını okur ve kategori puanlarını hesaplar."""
    puanlar = {kategori: 0 for kategori in KATEGORILER}
    okunan_metin = ""
    
    try:
        reader = PdfReader(dosya_yolu)
        # Sadece ilk 15 sayfayı oku (Performans için)
        sayfa_sayisi = min(len(reader.pages), 15)
        
        for i in range(sayfa_sayisi):
            sayfa_metni = reader.pages[i].extract_text()
            if sayfa_metni:
                okunan_metin += " " + sayfa_metni
        
        if not okunan_metin.strip():
            return None # Metin okunamadı (muhtemelen resim tabanlı PDF)

        temiz_metin = metin_temizle(okunan_metin)
        kelimeler = temiz_metin.split()
        
        # Kelime sayımı yap
        for kategori, anahtar_kelimeler in KATEGORILER.items():
            for anahtar in anahtar_kelimeler:
                # Anahtar kelimenin metinde kaç kere geçtiğini bul
                gecme_sayisi = temiz_metin.count(anahtar)
                puanlar[kategori] += gecme_sayisi

        # En yüksek puanı bul
        en_yuksek_kategori = max(puanlar, key=puanlar.get)
        
        # Eğer hiç puan alınamadıysa veya puan çok düşükse
        if puanlar[en_yuksek_kategori] < 2: 
            return None
            
        return en_yuksek_kategori

    except Exception as e:
        print(f"  [!] PDF okuma hatası: {e}")
        return None

def dosya_adi_puanla(dosya_adi):
    """Eğer içerik okunamadıysa dosya adına bakar."""
    dosya_adi = dosya_adi.lower()
    for kategori, anahtar_kelimeler in KATEGORILER.items():
        for kelime in anahtar_kelimeler:
            if kelime in dosya_adi:
                return kategori
    return "Diğer"

def main():
    if not os.path.exists(HEDEF_KLASOR):
        os.makedirs(HEDEF_KLASOR)

    dosyalar = [f for f in os.listdir(KAYNAK_KLASOR) if f.lower().endswith('.pdf')]
    toplam_dosya = len(dosyalar)
    
    print(f"\n🚀 PRO MODU BAŞLATILDI: {toplam_dosya} kitap analiz ediliyor...\n")
    
    istatistikler = {"İçerikten Bulunan": 0, "İsimden Bulunan": 0, "Bulunamayan": 0}

    for index, dosya in enumerate(dosyalar, 1):
        kaynak_yol = os.path.join(KAYNAK_KLASOR, dosya)
        print(f"[{index}/{toplam_dosya}] Analiz ediliyor: {dosya}...", end="\r")
        
        # 1. YÖNTEM: İçerik Analizi
        kategori = pdf_icerik_puanla(kaynak_yol)
        
        if kategori:
            metod = "İÇERİK ANALİZİ"
            istatistikler["İçerikten Bulunan"] += 1
        else:
            # 2. YÖNTEM: Dosya Adı Analizi (Fallback)
            kategori = dosya_adi_puanla(dosya)
            metod = "İSİM ANALİZİ"
            if kategori == "Diğer":
                istatistikler["Bulunamayan"] += 1
            else:
                istatistikler["İsimden Bulunan"] += 1

        # Taşıma İşlemi
        hedef_kategori_yolu = os.path.join(HEDEF_KLASOR, kategori)
        if not os.path.exists(hedef_kategori_yolu):
            os.makedirs(hedef_kategori_yolu)
            
        try:
            shutil.move(kaynak_yol, os.path.join(hedef_kategori_yolu, dosya))
            # Terminal çıktısını temiz tutalım, sadece sonucu yazalım
            print(f"✅ {dosya[:30]}... -> [{kategori}] ({metod}){' '*20}")
        except Exception as e:
            print(f"❌ HATA: {dosya} taşınamadı. {e}")

    # --- SIRALAMA VE RAPORLAMA ---
    print("\n" + "="*50)
    print("📊 İŞLEM ÖZETİ")
    print("="*50)
    print(f"🧠 İçerik Analizi ile Sınıflandırılan: {istatistikler['İçerikten Bulunan']}")
    print(f"🏷️ İsim Analizi ile Sınıflandırılan: {istatistikler['İsimden Bulunan']}")
    print(f"📂 'Diğer' Klasörüne Atılan: {istatistikler['Bulunamayan']}")
    print("\nKütüphaneniz şu an şurada hazır: " + HEDEF_KLASOR)
    
    # Kullanıcıya klasörü açmak ister misin diye soralım (Windows için)
    os.startfile(HEDEF_KLASOR)

if __name__ == "__main__":
    main()
