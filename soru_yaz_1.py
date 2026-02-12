import streamlit as st
import json
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="SoruRota Soru Düzenleme Paneli", layout="wide")

st.title("🧪 Fen Bilimleri Soru Düzenleme ve Yönetim Paneli")
st.write("JSON formatındaki soruları yükleyin, düzenleyin ve dışa aktarın.")

# 1. Dosya Yükleme
uploaded_file = st.file_uploader("Soru JSON dosyasını seçiniz", type=['json'])

if uploaded_file is not None:
    data = json.load(uploaded_file)
    
    # Eğer tek bir soruysa listeye çevir
    if isinstance(data, dict):
        questions = [data]
    else:
        questions = data

    # 2. Soru Seçimi
    question_titles = [f"Soru {i+1}: {q.get('konu', 'Adsız Konu')}" for i, q in enumerate(questions)]
    selected_index = st.sidebar.selectbox("Düzenlenecek Soruyu Seçin", range(len(question_titles)), format_func=lambda x: question_titles[x])
    
    curr_q = questions[selected_index]

    # 3. Düzenleme Alanı
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📝 Soru İçeriği")
        curr_q['soruYazari'] = st.text_input("Soru Yazarı", curr_q.get('soruYazari', ''))
        curr_q['kazanim'] = st.text_input("Kazanım No", curr_q.get('kazanim', '')) 
        curr_q['ustMetin'] = st.text_area("Üst Metin / Senaryo", curr_q.get('ustMetin', '')) 
        curr_q['soruMetni'] = st.text_area("Soru Kökü", curr_q.get('soruMetni', '')) 
        
        st.write("**Seçenekler**")
        options = curr_q.get('secenekler', {"A": "", "B": "", "C": "", "D": ""})
        options['A'] = st.text_input("A Şıkkı", options['A'])
        options['B'] = st.text_input("B Şıkkı", options['B'])
        options['C'] = st.text_input("C Şıkkı", options['C'])
        options['D'] = st.text_input("D Şıkkı", options['D'])
        curr_q['secenekler'] = options

    with col2:
        st.subheader("⚙️ Teknik Detaylar & Görsel")
        curr_q['dogruCevap'] = st.selectbox("Doğru Cevap", ["A", "B", "C", "D"], index=["A", "B", "C", "D"].index(curr_q.get('dogruCevap', 'A'))) 
        curr_q['zorluk'] = st.slider("Zorluk (0.0: Zor, 1.0: Kolay)", 0.0, 1.0, float(curr_q.get('zorluk', 0.5))) 
        curr_q['cozum'] = st.text_area("Çözüm Açıklaması", curr_q.get('cozum', '')) 
        
        # Çizim Kodları Alanı
        curr_q['pythonKodu'] = st.text_area("Python Çizim Kodu", curr_q.get('pythonKodu', '')) 
        curr_q['htmlKodu'] = st.text_area("HTML/SVG Kodu", curr_q.get('htmlKodu', '')) 

    # 4. Kaydetme ve Dışa Aktarma
    st.divider()
    updated_json = json.dumps(questions, indent=4, ensure_ascii=False)
    
    st.download_button(
        label="✅ Tüm Soruları JSON Olarak İndir",
        data=updated_json,
        file_name="guncellenen_sorular.json",
        mime="application/json"
    )

else:
    st.info("Lütfen düzenlemek için bir JSON dosyası yükleyin.")