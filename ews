import streamlit as st

# Mengatur judul dan lebar halaman
st.set_page_config(page_title="EWS Pertanian Belu", layout="wide")

st.title("🌾 Radar Pertanian: Kabupaten Belu")
st.write("Sistem Peringatan Dini (EWS) Ancaman Ulat Gerayak")
st.markdown("---")

# Membuat tata letak 2 kolom
col1, col2 = st.columns(2)

# Bagian Input (Di kolom kiri)
with col1:
    st.subheader("Input Data Lapangan & Cuaca")
    lokasi = st.selectbox("Pilih Kecamatan", ["Raimanuk", "Tasifeto Timur", "Tasifeto Barat"])
    suhu = st.slider("Suhu Udara (°C)", 20.0, 40.0, 29.0)
    kelembapan = st.slider("Kelembapan (%)", 50, 100, 85)
    hujan = st.selectbox("Intensitas Hujan", ["Kemarau", "Ringan", "Sedang", "Lebat"])
    serangan_lalu = st.number_input("Luas Serangan Minggu Lalu (Hektar)", 0, 200, 15)

# Bagian Logika (Sistem AI Sederhana di belakang layar)
indeks_risiko = 0

# Hama suka suhu hangat, sangat lembap, dan hujan rintik/sedang
if 28 <= suhu <= 32:
    indeks_risiko += 35
if kelembapan >= 80:
    indeks_risiko += 35
if hujan in ["Ringan", "Sedang"]:
    indeks_risiko += 15
if serangan_lalu > 10:
    indeks_risiko += 15

# Bagian Output / Peringatan (Di kolom kanan)
with col2:
    st.subheader("Status Indeks Risiko")
    
    # Menampilkan progress bar sesuai perhitungan risiko
    st.progress(indeks_risiko / 100.0)
    st.metric(label="Probabilitas Wabah", value=f"{indeks_risiko}%")
    
    # Logika memunculkan pesan warna-warni
    if indeks_risiko >= 70:
        st.error(f"🚨 AWAS: Risiko ledakan Ulat Gerayak di {lokasi} Kritis. PPL harap siaga!")
    elif indeks_risiko >= 30:
        st.warning(f"⚠️ WASPADA: Pantau perkembangan telur hama di {lokasi}.")
    else:
        st.success("✅ AMAN: Kondisi lingkungan tidak mendukung penyebaran hama.")
