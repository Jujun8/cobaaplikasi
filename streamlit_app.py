import streamlit as st

# Mengatur judul dan lebar halaman
st.set_page_config(page_title="EWS Terpadu Kab. Belu", layout="wide", page_icon="🌐")

st.title("🌐 Command Center & EWS Terpadu")
st.write("Portal Satu Data Pemerintah Kabupaten Belu")
st.markdown("---")

# ==========================================
# SIDEBAR: DAFTAR SELURUH INSTANSI
# ==========================================
st.sidebar.title("Navigasi Instansi")
st.sidebar.write("Pilih sektor untuk memantau data dan peringatan dini:")

daftar_dinas = [
    "Sekretariat DPRD", "Inspektorat Daerah", "Dinas Kesehatan", 
    "Dinas Pendidikan, Kepemudaan dan Olahraga", "Dinas Pertanian dan Ketahanan Pangan", 
    "Dinas Peternakan dan Perikanan", "Dinas Pekerjaan Umum dan Perumahan Rakyat", 
    "Dinas Lingkungan Hidup dan Perhubungan", "Dinas Kependudukan dan Pencatatan Sipil", 
    "Dinas Koperasi, Tenaga Kerja dan Transmigrasi", "Dinas Parawisata dan Kebudayaan", 
    "Dinas Pemberdayaan Perempuan, Perlindungan Anak, Pengendalian Penduduk dan Keluarga Berencana", 
    "Dinas Penanaman Modal dan Pelayanan Terpadu Satu Piintu", "Dinas Komunikasi dan Informatika", 
    "Dinas Perindustrian dan Perdagangan", "Dinas Perpustakaan dan Kearsipan", 
    "Dinas Sosial, Pemberdayaan Masyarakat dan Desa", "Badan Penanggulangan Bencana Daerah", 
    "Badan Perencanaan Pembangunan, Penelitian dan Pengembangan Daerah", 
    "Badan Pengelola Keuangan dan Aset Daerah", "Badan Pendapatan Daerah", 
    "Badan Kesatuan Bangsa dan Politik", "Badan Kepegawaian dan Pengembangan Sumber Daya Manusia Daerah", 
    "Badan Pengelola Perbatasan Daerah", "Bagian Hukum", "Bagian Organisasi Setda Belu", 
    "Bagian Kesejahteraan Rakyat Setda Belu", "Bagian Pemerintahan Setda Belu", 
    "Bagian Pengadaan Barang dan Jasa Setda Belu", "Bagian Administrasi Pembangunan Setda Belu", 
    "Bagian Perekonomian dan Sumber Daya Alam Setda Belu", "Bagian Protokol dan Komunikasi Pimpinan Setda Belu", 
    "Bagian Umum Setda Belu", "Satuan Polisi Pamong Praja", "RSUD Mgr. Gabriel Manek, SVD Atambua", 
    "Kecamatan Atambua Barat", "Kecamatan Kota Atambua", "Kecamatan Atambua Selatan", 
    "Kecamatan Tasifeto Timur", "Kecamatan Lamaknen", "Kecamatan Lamaknen Selatan", 
    "Kecamatan Kakuluk Mesak", "Kecamatan Lasiolat", "Kecamatan Nanaet Duasbesi", 
    "Kecamatan Raihat", "Kecamatan Raimanuk"
]

pilihan_dinas = st.sidebar.selectbox("Instansi Pemantau:", daftar_dinas)

col1, col2 = st.columns([1.2, 1])

indeks_risiko = 0
pesan_peringatan = ""

# ==========================================
# LOGIKA & PARAMETER BERDASARKAN DINAS
# ==========================================

with col1:
    st.subheader(f"📊 Parameter Data: {pilihan_dinas}")
    
    # 1. SEKRETARIAT DPRD (Menampilkan Data dari PDF yang Anda Upload)
    if pilihan_dinas == "Sekretariat DPRD":
        tab1, tab2 = st.tabs(["Struktur AKD", "Peringatan Sidang"])
        with tab1:
            st.write("**Ketua Komisi DPRD Belu (2024-2029):**")
            st.table({
                "Komisi": ["Komisi I", "Komisi II", "Komisi III"],
                "Bidang": ["Pemerintahan & Hukum", "Ekonomi & Keuangan", "Pembangunan & Kesejahteraan"],
                "Ketua": ["Edmundus Nuak, SE", "Edmundus Yakobus Manek", "Cyprianus Temu, S.IP"]
            })
        with tab2:
            kehadiran = st.slider("Persentase Kehadiran Anggota (%)", 0, 100, 70)
            sisa_hari = st.number_input("Sisa Hari Pembahasan Perda/APBD", 0, 30, 10)
            if kehadiran < 50: indeks_risiko += 50
            if sisa_hari < 7: indeks_risiko += 50
            pesan_peringatan = f"Risiko kuorum tidak tercapai ({kehadiran}%) atau deadline pembahasan ({sisa_hari} hari lagi)."

    # 2. DINAS PERTANIAN
    elif pilihan_dinas == "Dinas Pertanian dan Ketahanan Pangan":
        hama = st.number_input("Luas Lahan Terkena Hama (Hektar)", 0, 500, 10)
        if hama > 20: indeks_risiko = 80
        pesan_peringatan = f"Anomali serangan hama seluas {hama} hektar."

    # 3. RSUD
    elif pilihan_dinas == "RSUD Mgr. Gabriel Manek, SVD Atambua":
        bor = st.slider("Keterisian Bed (BOR) %", 0, 100, 60)
        if bor > 80: indeks_risiko = 90
        pesan_peringatan = f"Kapasitas RSUD hampir penuh (BOR: {bor}%)."

    # 4. DEFAULT UNTUK LAINNYA (Supaya Tidak Kosong)
    else:
        st.info("Form Pelaporan Standar")
        laporan = st.number_input("Jumlah Laporan Masuk", 0, 100, 5)
        urgensi = st.select_slider("Tingkat Urgensi", options=["Rendah", "Sedang", "Tinggi", "Kritis"])
        if urgensi == "Kritis": indeks_risiko = 100
        elif urgensi == "Tinggi": indeks_risiko = 70
        pesan_peringatan = f"Terdapat {laporan} laporan masuk dengan status {urgensi}."

# ==========================================
# VISUALISASI OUTPUT
# ==========================================
with col2:
    st.subheader("Radar Peringatan Dini")
    st.progress(indeks_risiko / 100)
    st.metric("Skor Risiko", f"{indeks_risiko}%")
    
    if indeks_risiko >= 70:
        st.error(f"🚨 KRITIS\n\n{pesan_peringatan}")
    elif indeks_risiko >= 40:
        st.warning(f"⚠️ WASPADA\n\n{pesan_peringatan}")
    else:
        st.success("✅ AMAN: Kondisi operasional normal.")
