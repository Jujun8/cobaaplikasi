import streamlit as st
import pandas as pd
import os

# Mengatur judul halaman
st.set_page_config(page_title="EWS Berbasis Data", layout="wide")

st.title("📊 EWS Pertanian Terotomatisasi")
st.write("Membaca data langsung dari file CSV di GitHub")
st.markdown("---")

# 1. MENGECEK DAN MEMBACA FILE DATA
file_path = "data_pertanian.csv"

if os.path.exists(file_path):
    # Membaca data CSV menggunakan Pandas
    df = pd.read_csv(file_path)
    
    st.subheader("1. Data Mentah (Dari GitHub)")
    st.dataframe(df, use_container_width=True) # Menampilkan tabel di web
    
    st.markdown("---")
    
    # Membuat tata letak 2 kolom
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("2. Filter Analisis")
        # Mengambil daftar kecamatan dari kolom data secara otomatis
        daftar_kecamatan = df['Kecamatan'].unique()
        lokasi = st.selectbox("Pilih Kecamatan untuk Dianalisis", daftar_kecamatan)
        
        # Mengambil data KHUSUS untuk kecamatan yang dipilih
        data_lokasi = df[df['Kecamatan'] == lokasi].iloc[-1] # Mengambil baris data terbaru
        
        # Ekstraksi angka dari file CSV (menggantikan slider manual)
        suhu = data_lokasi['Suhu']
        kelembapan = data_lokasi['Kelembapan']
        serangan_lalu = data_lokasi['Serangan_Lalu']
        
        # Menampilkan parameter yang sedang dibaca mesin
        st.info(f"Sistem EWS sedang membaca data {lokasi}:\n\n"
                f"🌡️ Suhu: {suhu} °C\n"
                f"💧 Kelembapan: {kelembapan} %\n"
                f"🐛 Serangan Lalu: {serangan_lalu} Hektar")
        
        # ==========================================
        # LOGIKA PERHITUNGAN EWS
        # ==========================================
        indeks_risiko = 0
        if 28 <= suhu <= 32: indeks_risiko += 30
        if kelembapan >= 80: indeks_risiko += 40
        if serangan_lalu > 10: indeks_risiko += 30
        
        if indeks_risiko > 100: indeks_risiko = 100
        
    with col2:
        st.subheader("3. Hasil Prediksi & Tindakan")
        
        # Menampilkan progress bar risiko
        st.progress(indeks_risiko / 100.0)
        st.metric(label="Level Ancaman", value=f"{indeks_risiko}%")
        
        if indeks_risiko >= 70:
            st.error(f"🚨 AWAS (KRITIS): Risiko ledakan hama di {lokasi} sangat tinggi!")
        elif indeks_risiko >= 40:
            st.warning(f"⚠️ WASPADA: Pantau intensif kondisi lahan di {lokasi}.")
        else:
            st.success(f"✅ AMAN: Ekosistem di {lokasi} tidak mendukung wabah hama.")

else:
    # Pesan error jika file CSV belum diupload ke GitHub
    st.error(f"File {file_path} tidak ditemukan! Pastikan Anda sudah mengunggahnya ke GitHub.")
