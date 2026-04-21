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

# Daftar Instansi Lengkap sesuai struktur Pemkab Belu
daftar_dinas = [
    # --- Sekretariat & Inspektorat ---
    "Sekretariat DPRD",
    "Inspektorat Daerah",
    
    # --- Dinas Daerah ---
    "Dinas Kesehatan",
    "Dinas Pendidikan, Kepemudaan dan Olahraga",
    "Dinas Pertanian dan Ketahanan Pangan",
    "Dinas Peternakan dan Perikanan",
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
    
    # --- Badan Daerah ---
    "Badan Penanggulangan Bencana Daerah",
    "Badan Perencanaan Pembangunan, Penelitian dan Pengembangan Daerah",
    "Badan Pengelola Keuangan dan Aset Daerah",
    "Badan Pendapatan Daerah",
    "Badan Kesatuan Bangsa dan Politik",
    "Badan Kepegawaian dan Pengembangan Sumber Daya Manusia Daerah",
    "Badan Pengelola Perbatasan Daerah",
    
    # --- Bagian Setda ---
    "Bagian Hukum",
    "Bagian Organisasi Setda Belu",
    "Bagian Kesejahteraan Rakyat Setda Belu",
    "Bagian Pemerintahan Setda Belu",
    "Bagian Pengadaan Barang dan Jasa Setda Belu",
    "Bagian Administrasi Pembangunan Setda Belu",
    "Bagian Perekonomian dan Sumber Daya Alam Setda Belu",
    "Bagian Protokol dan Komunikasi Pimpinan Setda Belu",
    "Bagian Umum Setda Belu",
    
    # --- Unit Lainnya & Kecamatan ---
    "Satuan Polisi Pamong Praja",
    "RSUD Mgr. Gabriel Manek, SVD Atambua",
    "Kecamatan Atambua Barat",
    "Kecamatan Kota Atambua",
    "Kecamatan Atambua Selatan",
    "Kecamatan Tasifeto Timur",
    "Kecamatan Lamaknen",
    "Kecamatan Lamaknen Selatan",
    "Kecamatan Kakuluk Mesak",
    "Kecamatan Lasiolat",
    "Kecamatan Nanaet Duasbesi",
    "Kecamatan Raihat",
    "Kecamatan Raimanuk"
]

pilihan_dinas = st.sidebar.selectbox("Instansi Pemantau:", daftar_dinas)

# Membuat tata letak 2 kolom untuk konten utama
col1, col2 = st.columns([1.2, 1])

# Variabel global penampung hasil
indeks_risiko = 0
lokasi = "Kabupaten Belu"
pesan_peringatan = ""

# ==========================================
# LOGIKA & PARAMETER BERDASARKAN DINAS
# ==========================================

with col1:
    st.subheader(f"📊 Parameter Data: {pilihan_dinas}")
    
    # 1. DINAS PERTANIAN
    if pilihan_dinas == "Dinas Pertanian dan Ketahanan Pangan":
        lokasi = st.selectbox("Kecamatan Pantauan", ["Raimanuk", "Tasifeto Timur", "Lamaknen"])
        suhu = st.slider("Suhu Udara (°C)", 20.0, 40.0, 29.0)
        kelembapan = st.slider("Kelembapan (%)", 50, 100, 85)
        serangan_hama = st.number_input("Luas Lahan Terkena Hama (Hektar)", 0, 500, 25)
        
        if 28 <= suhu <= 32: indeks_risiko += 25
        if kelembapan >= 80: indeks_risiko += 35
        if serangan_hama > 20: indeks_risiko += 40
        pesan_peringatan = f"Risiko wabah ulat gerayak/hama di {lokasi} meningkat akibat anomali cuaca."

    # 2. DINAS PETERNAKAN
    elif pilihan_dinas == "Dinas Peternakan dan Perikanan":
        kematian_ternak = st.number_input("Kematian Babi/Ternak Mendadak (Ekor)", 0, 100, 5)
        stok_vaksin = st.radio("Ketersediaan Vaksin/Disinfektan", ["Aman", "Menipis", "Kosong"])
        
        if kematian_ternak >= 10: indeks_risiko += 60
        elif kematian_ternak >= 3: indeks_risiko += 30
        if stok_vaksin == "Kosong": indeks_risiko += 40
        elif stok_vaksin == "Menipis": indeks_risiko += 20
        pesan_peringatan = f"Indikasi penyebaran penyakit ternak. Tingkat kematian: {kematian_ternak} ekor."

    # 3. DINAS KESEHATAN
    elif pilihan_dinas == "Dinas Kesehatan":
        kasus_baru = st.number_input("Tambahan Kasus DBD/Malaria/Penyakit Menular", 0, 100, 12)
        curah_hujan = st.selectbox("Kondisi Lingkungan", ["Normal", "Banyak Genangan Air"])
        
        if kasus_baru >= 10: indeks_risiko += 60
        elif kasus_baru >= 5: indeks_risiko += 30
        if curah_hujan == "Banyak Genangan Air": indeks_risiko += 40
        pesan_peringatan = f"Potensi KLB Penyakit Menular. Segera lakukan intervensi medis dan lingkungan."

    # 4. DINAS PENDIDIKAN
    elif pilihan_dinas == "Dinas Pendidikan, Kepemudaan dan Olahraga":
        laporan_rusak = st.number_input("Laporan Atap/Gedung Sekolah Rusak Berat", 0, 50, 2)
        kehadiran = st.slider("Rata-rata Tingkat Kehadiran Siswa (%)", 0, 100, 80)
        
        if laporan_rusak >= 5: indeks_risiko += 50
        if kehadiran < 75: indeks_risiko += 50
        pesan_peringatan = f"Anomali kehadiran siswa ({kehadiran}%) & {laporan_rusak} gedung rusak. Risiko keselamatan belajar."

    # 5. BPBD (BADAN PENANGGULANGAN BENCANA DAERAH) - *BARU*
    elif pilihan_dinas == "Badan Penanggulangan Bencana Daerah":
        curah_hujan_bpbd = st.slider("Intensitas Curah Hujan (mm/hari)", 0, 200, 80)
        debit_sungai = st.radio("Status Debit Sungai/Bendungan", ["Normal", "Siaga", "Waspada", "Awas (Meluap)"])
        
        if curah_hujan_bpbd > 100: indeks_risiko += 50
        elif curah_hujan_bpbd > 50: indeks_risiko += 20
        if debit_sungai == "Awas (Meluap)": indeks_risiko += 50
        elif debit_sungai == "Waspada": indeks_risiko += 30
        pesan_peringatan = f"Peringatan Dini Bencana Hidrometeorologi! Status sungai: {debit_sungai}."

    # 6. PUPR - *BARU*
    elif pilihan_dinas == "Dinas Pekerjaan Umum dan Perumahan Rakyat":
        jalan_putus = st.radio("Laporan Akses Jalan/Jembatan Putus", ["Tidak Ada", "Ada (Terisolir)"])
        alat_berat = st.radio("Kesiapan Alat Berat (Ekskavator)", ["Siap", "Sedang Digunakan di Lokasi Lain", "Rusak"])
        
        if jalan_putus == "Ada (Terisolir)": indeks_risiko += 70
        if alat_berat == "Rusak": indeks_risiko += 30
        pesan_peringatan = f"Darurat Infrastruktur! Akses terputus sementara status alat berat: {alat_berat}."

    # 7. RSUD MGR GABRIEL MANEK - *BARU*
    elif pilihan_dinas == "RSUD Mgr. Gabriel Manek, SVD Atambua":
        bed_occupancy = st.slider("Tingkat Keterisian Tempat Tidur (BOR) %", 0, 100, 65)
        stok_oksigen = st.radio("Ketersediaan Oksigen/Obat Esensial", ["Aman", "Kritis (< 3 Hari)"])
        
        if bed_occupancy > 85: indeks_risiko += 50
        elif bed_occupancy > 70: indeks_risiko += 25
        if stok_oksigen == "Kritis (< 3 Hari)": indeks_risiko += 50
        pesan_peringatan = f"Terdeteksi penumpukan {jumlah_kasus} kasus/isu terkait {jenis_laporan} dengan tingkat urgensi {tingkat_urgensi}."
