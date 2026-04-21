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

# ==========================================
# LOGIKA & PARAMETER: INSPEKTORAT DAERAH
# ==========================================

with col1:
    if pilihan_dinas == "Inspektorat Daerah":
        st.subheader("🔍 Audit & Internal Control Panel")
        
        tab_audit, tab_risiko, tab_fraud = st.tabs(["Temuan & PKPT", "Risiko OPD & Kepatuhan", "Fraud & Whistleblowing"])
        
        with tab_audit:
            st.write("### 🚨 1. Temuan Audit & Progres PKPT")
            c1, c2 = st.columns(2)
            with c1:
                temuan_total = st.number_input("Total Temuan Audit", 1, 1000, 50)
                temuan_pending = st.number_input("Temuan Belum Ditindaklanjuti > 60 Hari", 0, 500, 12)
                if temuan_pending > 10:
                    indeks_risiko += 30
                    pesan_peringatan.append(f"CRITICAL: {temuan_pending} temuan audit kadaluarsa (Stagnan).")
            
            with c2:
                target_audit = st.number_input("Target Audit Tahunan (PKPT)", 1, 100, 20)
                realisasi_audit = st.number_input("Audit Selesai", 0, 100, 8)
                persen_pkpt = (realisasi_audit / target_audit) * 100
                st.caption(f"Realisasi PKPT: {persen_pkpt:.1f}%")
                if persen_pkpt < 40:
                    indeks_risiko += 20
                    pesan_peringatan.append("PROGRES RENDAH: Realisasi PKPT di bawah target tahunan.")

        with tab_risiko:
            st.write("### 📊 2. Heatmap Risiko & Kepatuhan OPD")
            # Simulasi Ranking Risiko OPD
            data_opd = pd.DataFrame({
                'OPD': ['Dinas PUPR', 'Dinas Pendidikan', 'Dinas Kesehatan', 'Kec. Raimanuk', 'Kec. Kota'],
                'Skor_Risiko': [85, 70, 45, 30, 20],
                'Status': ['Tinggi', 'Tinggi', 'Sedang', 'Rendah', 'Rendah']
            })
            
            # Menampilkan Heatmap Sederhana
            st.table(data_opd)
            opd_tinggi = len(data_opd[data_opd['Skor_Risiko'] >= 70])
            if opd_tinggi > 2:
                indeks_risiko += 25
                pesan_peringatan.append(f"WARNING: Terdapat {opd_tinggi} OPD dengan kategori Risiko Tinggi.")

            st.write("### 📑 Kepatuhan Laporan (SPJ/LK)")
            kepatuhan = st.slider("Persentase Kepatuhan Pelaporan OPD (%)", 0, 100, 85)
            if kepatuhan < 80:
                indeks_risiko += 15
                pesan_peringatan.append("KEPATUHAN RENDAH: Banyak OPD terlambat menyetor SPJ/Laporan.")

        with tab_fraud:
            st.write("### 🧾 7. Indikasi Fraud & Whistleblowing")
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                aduan_ws = st.number_input("Aduan Masuk (Whistleblowing)", 0, 100, 5)
                aduan_proses = st.number_input("Aduan Belum Diproses", 0, 100, 5)
                if aduan_proses > 0:
                    indeks_risiko += 15
                    pesan_peringatan.append(f"SLA OVER: {aduan_proses} aduan masyarakat belum ditangani.")
            
            with col_f2:
                anomali_keu = st.toggle("Deteksi Transaksi Mencurigakan (Anomali Anggaran)", value=True)
                if anomali_keu:
                    indeks_risiko += 20
                    pesan_peringatan.append("FRAUD ALERT: Terdeteksi pola realisasi anggaran tidak wajar.")

    # ---------------------------------------------------------
    # BLOK INSTANSI LAIN (Contoh Singkat)
    # ---------------------------------------------------------
    else:
        st.info(f"Dashboard untuk {pilihan_dinas} sedang dalam pengembangan.")
        indeks_risiko = 0

# ==========================================
# VISUALISASI OUTPUT (RADAR INSPEKTORAT)
# ==========================================

with col2:
    st.subheader("Radar Pengawasan Internal")
    
    final_score = min(indeks_risiko, 100)
    
    # Warna berdasarkan Level Risiko
    if final_score >= 75:
        color = "#FF0000" # Merah
        status = "KRITIS / BAHAYA"
    elif final_score >= 45:
        color = "#FFA500" # Oranye
        status = "WASPADA"
    else:
        color = "#008000" # Hijau
        status = "AMAN"

    # Gauge Visual
    st.markdown(f"""
        <div style="background-color:{color}; padding:20px; border-radius:10px; text-align:center;">
            <h1 style="color:white; margin:0;">{final_score}%</h1>
            <p style="color:white; margin:0; font-weight:bold;">Status: {status}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if pesan_peringatan:
        st.write("**Daftar Isu Strategis:**")
        for p in pesan_peringatan:
            if "CRITICAL" in p or "FRAUD" in p:
                st.error(p)
            elif "WARNING" in p or "RENDAH" in p:
                st.warning(p)
            else:
                st.info(p)
    
    st.button("📥 Unduh Laporan Rekomendasi Audit")
    st.button("🔔 Kirim Notifikasi ke OPD Terkait")
