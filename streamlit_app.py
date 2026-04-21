import streamlit as st
from datetime import datetime

# ==============================
# KONFIGURASI HALAMAN
# ==============================
st.set_page_config(
    page_title="EWS Terpadu Kab. Belu",
    layout="wide",
    page_icon="🌐"
)

st.title("🌐 Command Center & EWS Terpadu")
st.caption("Portal Satu Data Pemerintah Kabupaten Belu")
st.markdown("---")

# ==============================
# DATA DINAS
# ==============================
DAFTAR_DINAS = [
    "Sekretariat DPRD","Inspektorat Daerah",
    "Dinas Kesehatan","Dinas Pendidikan, Kepemudaan dan Olahraga",
    "Dinas Pertanian dan Ketahanan Pangan","Dinas Peternakan dan Perikanan",
    "Dinas Pekerjaan Umum dan Perumahan Rakyat",
    "Dinas Lingkungan Hidup dan Perhubungan",
    "Dinas Kependudukan dan Pencatatan Sipil",
    "Dinas Koperasi, Tenaga Kerja dan Transmigrasi",
    "Dinas Parawisata dan Kebudayaan",
    "Dinas Pemberdayaan Perempuan, Perlindungan Anak, Pengendalian Penduduk dan Keluarga Berencana",
    "Dinas Penanaman Modal dan Pelayanan Terpadu Satu Piintu",
    "Dinas Komunikasi dan Informatika",
    "Dinas Perindustrian dan Perdagangan",
    "Dinas Perpustakaan dan Kearsipan",
    "Dinas Sosial, Pemberdayaan Masyarakat dan Desa",
    "Badan Penanggulangan Bencana Daerah",
    "Badan Perencanaan Pembangunan, Penelitian dan Pengembangan Daerah",
    "Badan Pengelola Keuangan dan Aset Daerah",
    "Badan Pendapatan Daerah",
    "Badan Kesatuan Bangsa dan Politik",
    "Badan Kepegawaian dan Pengembangan Sumber Daya Manusia Daerah",
    "Badan Pengelola Perbatasan Daerah",
    "Satuan Polisi Pamong Praja",
    "RSUD Mgr. Gabriel Manek, SVD Atambua"
]

# ==============================
# SIDEBAR
# ==============================
st.sidebar.title("Navigasi Instansi")
pilihan_dinas = st.sidebar.selectbox("Pilih Instansi:", DAFTAR_DINAS)

# ==============================
# FUNGSI PERHITUNGAN RISIKO
# ==============================
def hitung_risiko_pertanian(suhu, kelembapan, hama):
    skor = 0
    if 28 <= suhu <= 32: skor += 25
    if kelembapan >= 80: skor += 35
    if hama > 20: skor += 40
    return skor

def hitung_risiko_kesehatan(kasus, lingkungan):
    skor = 0
    if kasus >= 10: skor += 60
    elif kasus >= 5: skor += 30
    if lingkungan == "Banyak Genangan Air": skor += 40
    return skor

def hitung_risiko_bpbd(hujan, sungai):
    skor = 0
    if hujan > 100: skor += 50
    elif hujan > 50: skor += 20
    if sungai == "Awas (Meluap)": skor += 50
    elif sungai == "Waspada": skor += 30
    return skor

# ==============================
# LAYOUT
# ==============================
col1, col2 = st.columns([1.2, 1])

indeks_risiko = 0
pesan = ""

# ==============================
# INPUT DINAS
# ==============================
with col1:
    st.subheader(f"📊 Parameter: {pilihan_dinas}")

    if pilihan_dinas == "Dinas Pertanian dan Ketahanan Pangan":
        suhu = st.slider("Suhu (°C)", 20.0, 40.0, 29.0)
        kelembapan = st.slider("Kelembapan (%)", 50, 100, 85)
        hama = st.number_input("Luas Hama (Ha)", 0, 500, 25)

        indeks_risiko = hitung_risiko_pertanian(suhu, kelembapan, hama)
        pesan = "Potensi serangan hama meningkat akibat kondisi cuaca."

    elif pilihan_dinas == "Dinas Kesehatan":
        kasus = st.number_input("Kasus Penyakit", 0, 100, 10)
        lingkungan = st.selectbox("Lingkungan", ["Normal", "Banyak Genangan Air"])

        indeks_risiko = hitung_risiko_kesehatan(kasus, lingkungan)
        pesan = "Potensi KLB penyakit menular."

    elif pilihan_dinas == "Badan Penanggulangan Bencana Daerah":
        hujan = st.slider("Curah Hujan", 0, 200, 80)
        sungai = st.radio("Status Sungai", ["Normal", "Waspada", "Awas (Meluap)"])

        indeks_risiko = hitung_risiko_bpbd(hujan, sungai)
        pesan = "Potensi bencana hidrometeorologi."

    else:
        st.info("Form generik digunakan.")
        kasus = st.number_input("Jumlah Kasus", 0, 500, 5)
        urgensi = st.select_slider("Urgensi", ["Rendah","Sedang","Tinggi","Kritis"])

        if kasus > 50: indeks_risiko += 40
        elif kasus > 10: indeks_risiko += 20

        if urgensi == "Kritis": indeks_risiko += 60
        elif urgensi == "Tinggi": indeks_risiko += 40

        pesan = f"{kasus} kasus dengan urgensi {urgensi}"

# ==============================
# NORMALISASI
# ==============================
indeks_risiko = min(indeks_risiko, 100)

# ==============================
# OUTPUT
# ==============================
with col2:
    st.subheader("🚨 Radar Peringatan Dini")

    st.progress(indeks_risiko / 100)
    st.metric("Level Risiko", f"{indeks_risiko}%")
    st.caption(f"Update: {datetime.now().strftime('%H:%M:%S')}")

    if indeks_risiko >= 70:
        st.error(f"KRITIS\n\n{pesan}")
        st.button("🚀 Kirim Tim / Tindakan Cepat")
    elif indeks_risiko >= 40:
        st.warning(f"WASPADA\n\n{pesan}")
        st.button("📢 Notifikasi Pimpinan")
    else:
        st.success("AMAN - Kondisi stabil")
