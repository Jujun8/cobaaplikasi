import streamlit as st
import pandas as pd

# Mengatur judul dan lebar halaman
st.set_page_config(page_title="EWS Terpadu Kab. Belu", layout="wide", page_icon="🌐")

st.title("🌐 Command Center & EWS Terpadu")
st.write("Portal Satu Data Pemerintah Kabupaten Belu")
st.markdown("---")

# ==========================================
# SIDEBAR: DAFTAR INSTANSI
# ==========================================
st.sidebar.title("Navigasi Instansi")
daftar_dinas = [
    "Sekretariat DPRD", "Inspektorat Daerah", "Dinas Kesehatan", 
    "Dinas Pendidikan, Kepemudaan dan Olahraga", "Dinas Pertanian dan Ketahanan Pangan", 
    "Dinas Peternakan dan Perikanan", "Badan Penanggulangan Bencana Daerah"
]

pilihan_dinas = st.sidebar.selectbox("Instansi Pemantau:", daftar_dinas)

col1, col2 = st.columns([1.6, 1])

indeks_risiko = 0
pesan_peringatan = []

    
    st.button("📥 Unduh Laporan Rekomendasi Audit")
    st.button("🔔 Kirim Notifikasi ke OPD Terkait")
