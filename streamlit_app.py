import streamlit as st

# Mengatur judul dan lebar halaman
st.set_page_config(page_title="EWS Terpadu Kab. Belu", layout="wide", page_icon="🌐")

st.title("🌐 Command Center & EWS Terpadu")
st.write("Portal Satu Data Pemerintah Kabupaten Belu")
st.markdown("---")

# ==========================================
# SIDEBAR: DAFTAR INSTANSI
# ==========================================
st.sidebar.title("Navigasi Instansi")
st.sidebar.write("Pilih sektor untuk memantau data dan peringatan dini:")

daftar_dinas = [
    "Dinas Pertanian dan Ketahanan Pangan",
    "Dinas Peternakan dan Perikanan",
    "Dinas Kesehatan",
    "Dinas Pendidikan, Kepemudaan dan Olah Raga",
    "Dinas Pemberdayaan Perempuan, Perlindungan Anak, PP dan KB",
    "Sekretariat Dewan (DPRD)"
]

pilihan_dinas = st.sidebar.selectbox("Instansi Pemantau:", daftar_dinas)

# Membuat tata letak 2 kolom untuk konten utama
col1, col2 = st.columns([1.2, 1]) # Kolom kiri sedikit lebih lebar

# Variabel global penampung hasil
indeks_risiko = 0
lokasi = "Kabupaten Belu"
pesan_peringatan = ""

# ==========================================
# LOGIKA & PARAMETER BERDASARKAN DINAS
# ==========================================

with col1:
    st.subheader(f"📊 Parameter Data: {pilihan_dinas}")
    st.info("TIPS CSV: Di sinilah Anda nantinya memasukkan kode `pd.read_csv()` untuk menarik data otomatis dari GitHub.")
    
    # 1. DINAS PERTANIAN
    if pilihan_dinas == "Dinas Pertanian dan Ketahanan Pangan":
        lokasi = st.selectbox("Kecamatan Pantauan", ["Raimanuk", "Tasifeto Timur", "Lamaknen"])
        suhu = st.slider("Suhu Udara (°C)", 20.0, 40.0, 29.0)
        kelembapan = st.slider("Kelembapan (%)", 50, 100, 85)
        serangan_hama = st.number_input("Luas Lahan Terkena Hama (Hektar)", 0, 500, 25)
        
        if 28 <= suhu <= 32: indeks_risiko += 25
        if kelembapan >= 80: indeks_risiko += 35
        if serangan_hama > 20: indeks_risiko += 40
        pesan_peringatan = f"Risiko gagal panen/wabah ulat gerayak di {lokasi} meningkat akibat anomali cuaca."

    # 2. DINAS PETERNAKAN (Fokus: Penyakit ASF/Demam Babi Afrika yang rawan di NTT)
    elif pilihan_dinas == "Dinas Peternakan dan Perikanan":
        lokasi = st.selectbox("Desa/Kecamatan Pantauan", ["Atambua Selatan", "Tasifeto Barat", "Kakuluk Mesak"])
        kematian_ternak = st.number_input("Laporan Kematian Babi/Ternak Mendadak (Ekor)", 0, 100, 5)
        stok_vaksin = st.radio("Ketersediaan Vaksin/Disinfektan", ["Aman", "Menipis", "Kosong"])
        
        if kematian_ternak >= 10: indeks_risiko += 60
        elif kematian_ternak >= 3: indeks_risiko += 30
        if stok_vaksin == "Kosong": indeks_risiko += 40
        elif stok_vaksin == "Menipis": indeks_risiko += 20
        pesan_peringatan = f"Indikasi penyebaran virus ASF (Flu Babi) di {lokasi}. Tingkat kematian: {kematian_ternak} ekor."

    # 3. DINAS KESEHATAN (Fokus: KLB DBD/Malaria)
    elif pilihan_dinas == "Dinas Kesehatan":
        lokasi = st.selectbox("Puskesmas Pantauan", ["Puskesmas Kota Atambua", "Puskesmas Umanen", "Puskesmas Silawan"])
        kasus_baru = st.number_input("Tambahan Kasus DBD/Malaria Minggu Ini", 0, 100, 12)
        curah_hujan = st.selectbox("Intensitas Hujan Mingguan", ["Rendah", "Sedang", "Tinggi (Banyak Genangan)"])
        
        if kasus_baru >= 10: indeks_risiko += 50
        elif kasus_baru >= 5: indeks_risiko += 25
        if curah_hujan == "Tinggi (Banyak Genangan)": indeks_risiko += 50
        pesan_peringatan = f"Potensi Kejadian Luar Biasa (KLB) penyakit berbasis nyamuk di wilayah kerja {lokasi}."

    # 4. DINAS PENDIDIKAN (Fokus: Bangunan Rawan Ambruk / Putus Sekolah)
    elif pilihan_dinas == "Dinas Pendidikan, Kepemudaan dan Olah Raga":
        lokasi = st.selectbox("Tingkat Pendidikan", ["SD Negeri", "SMP Negeri"])
        laporan_rusak = st.number_input("Laporan Atap/Gedung Rusak Berat", 0, 50, 2)
        kehadiran = st.slider("Rata-rata Tingkat Kehadiran Siswa (%)", 0, 100, 80)
        
        if laporan_rusak >= 5: indeks_risiko += 50
        elif laporan_rusak >= 1: indeks_risiko += 20
        if kehadiran < 75: indeks_risiko += 50
        pesan_peringatan = f"Terdapat anomali kehadiran siswa ({kehadiran}%) dan {laporan_rusak} gedung rusak di tingkat {lokasi}. Risiko keselamatan/putus sekolah."

    # 5. DINAS DP3AP2KB (Fokus: Stunting & Kekerasan)
    elif pilihan_dinas == "Dinas Pemberdayaan Perempuan, Perlindungan Anak, PP dan KB":
        lokasi = st.selectbox("Fokus Isu", ["Pemantauan Kasus Stunting", "Kekerasan Dalam Rumah Tangga (KDRT)"])
        laporan_masuk = st.number_input("Jumlah Laporan Kasus Baru Bulan Ini", 0, 100, 15)
        target_batas = st.number_input("Batas Maksimal Toleransi (Threshold) Kasus", 1, 50, 10)
        
        if laporan_masuk > target_batas * 2: indeks_risiko += 80
        elif laporan_masuk > target_batas: indeks_risiko += 40
        pesan_peringatan = f"Lonjakan drastis pada {lokasi}. Laporan masuk ({laporan_masuk}) melampaui batas toleransi daerah."

    # 6. SEKRETARIAT DEWAN (Fokus: Deadline Regulasi & Kuorum)
    elif pilihan_dinas == "Sekretariat Dewan (DPRD)":
        lokasi = st.selectbox("Agenda Paripurna Terdekat", ["Pengesahan APBD", "LKPJ Bupati", "Perda Inisiatif"])
        sisa_hari = st.slider("Sisa Waktu Menuju Deadline UU (Hari)", 0, 90, 15)
        konfirmasi_hadir = st.slider("Konfirmasi Kehadiran Anggota Dewan (%)", 0, 100, 65)
        
        if sisa_hari <= 7: indeks_risiko += 50
        elif sisa_hari <= 30: indeks_risiko += 20
        if konfirmasi_hadir < 50: indeks_risiko += 50 # Tidak Kuorum
        pesan_peringatan = f"Risiko penundaan ketok palu {lokasi}. Sisa waktu {sisa_hari} hari & kehadiran anggota ({konfirmasi_hadir}%) mendekati batas kuorum."

# Pastikan indeks risiko tidak lebih dari 100
if indeks_risiko > 100: indeks_risiko = 100

# ==========================================
# VISUALISASI OUTPUT (SISTEM EWS)
# ==========================================

with col2:
    st.subheader("Radar Peringatan Dini")
    
    # Progress bar indikator
    st.progress(indeks_risiko / 100.0)
    st.metric(label="Level Risiko Instansi Terpilih", value=f"{indeks_risiko}%")
    
    # Logika Tampilan Peringatan
    if indeks_risiko >= 70:
        st.error(f"🚨 KRITIS (Tindakan Segera)\n\n{pesan_peringatan}")
        st.button("Terbitkan Surat Perintah Tugas (SPT) Otomatis", type="primary")
    elif indeks_risiko >= 40:
        st.warning(f"⚠️ WASPADA (Pemantauan)\n\n{pesan_peringatan}\nMohon siagakan tim lintas-bidang.")
        st.button("Kirim Notifikasi Pimpinan")
    else:
        st.success(f"✅ AMAN & KONDUSIF\n\nSemua parameter operasional pada {pilihan_dinas} berjalan dalam batas normal.")
