import streamlit as st

# Mengatur judul dan lebar halaman
st.set_page_config(page_title="EWS Terpadu Belu", layout="wide")

st.title("🌐 Pusat Peringatan Dini (EWS) Terpadu")
st.write("Portal Satu Data Pemerintah Kabupaten Belu")
st.markdown("---")

# Membuat menu pilihan dinas di Sidebar (Menu Samping)
st.sidebar.title("Pilih Sektor EWS")
pilihan_dinas = st.sidebar.radio(
    "Navigasi Instansi:",
    ("Dinas Pertanian (Hama)", "Dinas Kesehatan (Wabah DBD)", "BPBD / PUPR (Banjir)", "Dinas Perdagangan (Inflasi)")
)

# Membuat tata letak 2 kolom untuk konten utama
col1, col2 = st.columns(2)

# Variabel global untuk menampung hasil perhitungan
indeks_risiko = 0
status_teks = ""
lokasi = ""
pesan_peringatan = ""

# ==========================================
# LOGIKA & FORM DINAMIS BERDASARKAN DINAS
# ==========================================

with col1:
    st.subheader(f"Input Data: {pilihan_dinas}")
    
    if pilihan_dinas == "Dinas Pertanian (Hama)":
        lokasi = st.selectbox("Pilih Kecamatan", ["Raimanuk", "Tasifeto Timur", "Tasifeto Barat"])
        suhu = st.slider("Suhu Udara (°C)", 20.0, 40.0, 29.0)
        kelembapan = st.slider("Kelembapan (%)", 50, 100, 85)
        serangan_lalu = st.number_input("Serangan Minggu Lalu (Hektar)", 0, 200, 15)
        
        # Logika Pertanian
        if 28 <= suhu <= 32: indeks_risiko += 30
        if kelembapan >= 80: indeks_risiko += 40
        if serangan_lalu > 10: indeks_risiko += 30
        pesan_peringatan = f"Risiko ledakan Ulat Gerayak di {lokasi} tinggi akibat kelembapan {kelembapan}%."

    elif pilihan_dinas == "Dinas Kesehatan (Wabah DBD)":
        lokasi = st.selectbox("Pilih Kecamatan", ["Kota Atambua", "Atambua Barat", "Atambua Selatan"])
        kasus_minggu_lalu = st.number_input("Jumlah Kasus DBD Minggu Lalu", 0, 50, 5)
        curah_hujan = st.selectbox("Intensitas Curah Hujan", ["Rendah", "Sedang", "Tinggi (Genangan Air)"])
        
        # Logika Kesehatan
        if kasus_minggu_lalu >= 5: indeks_risiko += 40
        elif kasus_minggu_lalu > 0: indeks_risiko += 20
        if curah_hujan == "Tinggi (Genangan Air)": indeks_risiko += 60
        pesan_peringatan = f"Potensi KLB DBD di {lokasi}. Segera jadwalkan Fogging dan pembagian Abate."

    elif pilihan_dinas == "BPBD / PUPR (Banjir)":
        lokasi = st.selectbox("Pilih Titik Pantau Sungai", ["Sungai Talau", "Bendungan Rotiklot", "Sungai Benenai"])
        debit_air = st.slider("Ketinggian Air (Meter dari batas normal)", -1.0, 5.0, 1.5)
        status_pompa = st.radio("Kondisi Pompa Air", ["Berfungsi Baik", "Rusak/Mati"])
        
        # Logika Bencana
        if debit_air >= 3.0: indeks_risiko += 60
        elif debit_air >= 1.5: indeks_risiko += 30
        if status_pompa == "Rusak/Mati": indeks_risiko += 40
        pesan_peringatan = f"Siaga Banjir di area {lokasi}! Ketinggian air {debit_air}m. Evakuasi warga bantaran."

    elif pilihan_dinas == "Dinas Perdagangan (Inflasi)":
        lokasi = st.selectbox("Pilih Pasar Pantau", ["Pasar Baru Atambua", "Pasar Senggol"])
        komoditas = st.selectbox("Komoditas Pangan", ["Beras Premium", "Cabai Rawit", "Bawang Merah"])
        lonjakan_harga = st.slider("Lonjakan Harga dari HET (%)", 0, 100, 15)
        stok_gudang = st.radio("Stok Gudang Distributor", ["Aman (>1 Bulan)", "Menipis (<1 Minggu)"])
        
        # Logika Ekonomi
        if lonjakan_harga >= 20: indeks_risiko += 50
        elif lonjakan_harga >= 10: indeks_risiko += 20
        if stok_gudang == "Menipis (<1 Minggu)": indeks_risiko += 50
        pesan_peringatan = f"Ancaman Inflasi: Harga {komoditas} naik {lonjakan_harga}% dan stok menipis. Segera operasi pasar."

# Memastikan indeks maksimal adalah 100%
if indeks_risiko > 100:
    indeks_risiko = 100

# ==========================================
# VISUALISASI OUTPUT (SAMA UNTUK SEMUA DINAS)
# ==========================================

with col2:
    st.subheader("Status & Tindakan")
    
    # Menampilkan progress bar
    st.progress(indeks_risiko / 100.0)
    st.metric(label="Level Ancaman / Risiko", value=f"{indeks_risiko}%")
    
    # Logika warna dan notifikasi
    if indeks_risiko >= 70:
        st.error(f"🚨 AWAS (KRITIS)\n\n{pesan_peringatan}")
        st.button("Kirim Alert Darurat ke Bupati & Kadis", type="primary")
    elif indeks_risiko >= 40:
        st.warning(f"⚠️ WASPADA\n\nPerlu pemantauan intensif di {lokasi}. Siagakan tim lapangan.")
    else:
        st.success(f"✅ AMAN\n\nKondisi {pilihan_dinas} di {lokasi} terpantau stabil dan terkendali.")
