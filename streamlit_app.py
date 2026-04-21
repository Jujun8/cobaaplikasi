import streamlit as st
import pandas as pd

# Mengatur judul dan lebar halaman
st.set_page_config(page_title="EWS Terpadu Kab. Belu", layout="wide", page_icon="🌐")

st.title("🌐 Command Center & EWS Terpadu")
st.write("Portal Satu Data Pemerintah Kabupaten Belu")
st.markdown("---")

# ==========================================
# SIDEBAR: DAFTAR SELURUH INSTANSI
# ==========================================
st.sidebar.title("Navigasi Instansi")
daftar_dinas = [
    "Sekretariat DPRD", "Inspektorat Daerah", "Dinas Kesehatan", 
    "Dinas Pendidikan, Kepemudaan dan Olahraga", "Dinas Pertanian dan Ketahanan Pangan", 
    "Dinas Peternakan dan Perikanan", "Dinas Pekerjaan Umum dan Perumahan Rakyat", 
    "Badan Penanggulangan Bencana Daerah", "RSUD Mgr. Gabriel Manek, SVD Atambua",
    "Kecamatan Kota Atambua", "Kecamatan Raimanuk" # Tambahkan lainnya sesuai kebutuhan
]

pilihan_dinas = st.sidebar.selectbox("Instansi Pemantau:", daftar_dinas)

col1, col2 = st.columns([1.5, 1])

indeks_risiko = 0
pesan_peringatan = []

# ==========================================
# LOGIKA & PARAMETER BERDASARKAN DINAS
# ==========================================

with col1:
    st.subheader(f"📊 Control Panel: {pilihan_dinas}")
    
    if pilihan_dinas == "Sekretariat DPRD":
        # Menggunakan Tabs untuk mengorganisir 10 fitur agar tidak menumpuk
        tab_leg, tab_ops, tab_adm = st.tabs(["Legislasi & Anggaran", "Agenda & Reses", "Aspirasi & Internal"])
        
        with tab_leg:
            st.write("### 📄 Progres Pembahasan Perda & Anggaran")
            col_a, col_b = st.columns(2)
            with col_a:
                raperda_masuk = st.number_input("Jumlah Raperda Masuk", 1, 50, 10)
                raperda_disahkan = st.number_input("Jumlah Raperda Disahkan", 0, 50, 2)
                progres_perda = (raperda_disahkan / raperda_masuk) * 100
                st.caption(f"Capaian Legislasi: {progres_perda:.1f}%")
                if progres_perda < 30: 
                    indeks_risiko += 20
                    pesan_peringatan.append("Bottleneck Legislasi: Rasio pengesahan Raperda rendah.")

            with col_b:
                st.write("### 💰 Realisasi Anggaran")
                serapan = st.slider("Serapan Anggaran Sekretariat (%)", 0, 100, 45)
                if serapan < 20:
                    indeks_risiko += 15
                    pesan_peringatan.append("Serapan Anggaran Terlalu Rendah (Indikasi Program Macet).")
                elif serapan > 90:
                    indeks_risiko += 10
                    pesan_peringatan.append("Serapan Anggaran Mendekati Pagu (Waspada Overbudget).")

        with tab_ops:
            st.write("### ⚠️ Agenda & Kinerja Anggota")
            col_c, col_d = st.columns(2)
            with col_c:
                kehadiran = st.slider("Rata-rata Kehadiran Rapat (%)", 0, 100, 65)
                kuorum_status = "Tercapai" if kehadiran >= 50 else "Tidak Kuorum"
                st.info(f"Status Kuorum: {kuorum_status}")
                if kehadiran < 50:
                    indeks_risiko += 30
                    pesan_peringatan.append("RISIKO KUORUM: Kehadiran di bawah batas minimal (50%).")
            
            with col_d:
                deadline_agenda = st.selectbox("Agenda Terdekat", ["Paripurna LKPJ", "Rapat Komisi", "Badan Anggaran"])
                hari_h = st.number_input("Sisa Hari Menuju Pelaksanaan", 0, 30, 2)
                konfirmasi = st.radio("Konfirmasi Peserta H-1", ["Lengkap", "Belum Lengkap"])
                if hari_h <= 1 and konfirmasi == "Belum Lengkap":
                    indeks_risiko += 25
                    pesan_peringatan.append(f"Agenda {deadline_agenda} H-1 belum terkonfirmasi penuh.")

            st.write("### 📊 Monitoring Reses")
            laporan_reses = st.radio("Status Laporan Reses Anggota", ["Sudah Masuk Semua", "Ada yang Belum Melaporkan"])
            if laporan_reses == "Ada yang Belum Melaporkan":
                indeks_risiko += 15
                pesan_peringatan.append("Keterlambatan Administrasi: Laporan Reses belum lengkap.")

        with tab_adm:
            st.write("### 📬 Aspirasi, Surat & Sistem")
            col_e, col_f = st.columns(2)
            with col_e:
                aduan_masuk = st.number_input("Aduan Masyarakat Baru", 0, 100, 25)
                aduan_tertunda = st.number_input("Aduan Belum Ditindaklanjuti > 7 Hari", 0, 100, 10)
                if aduan_tertunda > 5:
                    indeks_risiko += 20
                    pesan_peringatan.append("Respon Publik Lambat: Aduan masyarakat menumpuk.")

            with col_f:
                st.write("### 🔐 Kepatuhan & IKU")
                iku_capaian = st.slider("Capaian IKU Tahunan (%)", 0, 100, 75)
                status_sistem = st.toggle("Status Server & Database", value=True)
                if not status_sistem:
                    indeks_risiko += 40
                    pesan_peringatan.append("ERROR TEKNIS: Database/Server Sekretariat Down!")
                if iku_capaian < 50:
                    indeks_risiko += 10
                    pesan_peringatan.append("Capaian IKU di bawah target tengah tahun.")

    # ---------------------------------------------------------
    # BLOK DINAS LAIN (Sederhana untuk Contoh)
    # ---------------------------------------------------------
    elif pilihan_dinas == "Dinas Kesehatan":
        st.write("### 🏥 Parameter Kesehatan")
        bor = st.slider("Keterisian RS (BOR) %", 0, 100, 50)
        if bor > 80: 
            indeks_risiko = 90
            pesan_peringatan.append("Kapasitas Rumah Sakit Kritis!")
        else:
            pesan_peringatan.append("Kondisi fasilitas kesehatan normal.")

    else:
        st.info("Form Pelaporan Standar untuk instansi terpilih.")
        urgensi = st.select_slider("Tingkat Urgensi", options=["Rendah", "Sedang", "Tinggi", "Kritis"])
        if urgensi == "Kritis": indeks_risiko = 100
        pesan_peringatan.append(f"Laporan masuk dengan tingkat urgensi {urgensi}.")

# ==========================================
# VISUALISASI OUTPUT (SISTEM EWS)
# ==========================================

with col2:
    st.subheader("Radar Peringatan Dini")
    
    # Normalisasi indeks risiko (max 100)
    final_score = min(indeks_risiko, 100)
    
    # Indikator Visual Berdasarkan Skor
    if final_score >= 70:
        color = "red"
        status_text = "🚨 KRITIS / BAHAYA"
    elif final_score >= 40:
        color = "orange"
        status_text = "⚠️ WASPADA"
    else:
        color = "green"
        status_text = "✅ AMAN"

    st.markdown(f"<h1 style='text-align: center; color: {color};'>{final_score}%</h1>", unsafe_allow_html=True)
    st.progress(final_score / 100)
    st.write(f"**Status:** {status_text}")
    st.markdown("---")

    if pesan_peringatan:
        st.write("**Daftar Isu Terdeteksi:**")
        for p in pesan_peringatan:
            if final_score >= 70:
                st.error(p)
            elif final_score >= 40:
                st.warning(p)
            else:
                st.success(p)
    
    st.button("Cetak Laporan Executive Summary")
    st.button("Kirim Alert ke Grup WhatsApp Pimpinan")
