import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime

# ==============================
# KONFIGURASI
# ==============================
st.set_page_config(page_title="EWS Belu", layout="wide")

# ==============================
# KONEKSI DATABASE
# ==============================
def get_connection():
    return mysql.connector.connect(
        host="your-host"
        user="your-username"
        password="your-password"
        database="db_dinas"
        user="root",
        password="",
        database="db_dinas"
    )

# ==============================
# SIMPAN DATA
# ==============================
def simpan_data(dinas, parameter, indeks, status):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO ews_data (dinas, parameter, indeks, status)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (dinas, parameter, indeks, status))
    conn.commit()
    conn.close()

# ==============================
# AMBIL DATA
# ==============================
def ambil_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM ews_data ORDER BY waktu DESC", conn)
    conn.close()
    return df

# ==============================
# LOGIN SEDERHANA
# ==============================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 Login Admin")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pw == "123":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Login gagal")
    st.stop()

# ==============================
# DASHBOARD
# ==============================
st.title("🌐 EWS Terpadu Kabupaten Belu")

dinas = st.sidebar.selectbox("Pilih Dinas", [
    "Dinas Pertanian",
    "Dinas Kesehatan",
    "BPBD",
    "Lainnya"
])

col1, col2 = st.columns(2)

indeks = 0
parameter = ""

# ==============================
# INPUT
# ==============================
with col1:
    st.subheader("Input Data")

    if dinas == "Dinas Pertanian":
        suhu = st.slider("Suhu", 20, 40, 30)
        kelembapan = st.slider("Kelembapan", 50, 100, 80)

        if suhu > 30: indeks += 40
        if kelembapan > 80: indeks += 60

        parameter = f"Suhu:{suhu}, Kelembapan:{kelembapan}"

    elif dinas == "Dinas Kesehatan":
        kasus = st.number_input("Kasus", 0, 100, 10)

        if kasus > 10: indeks += 70
        else: indeks += 30

        parameter = f"Kasus:{kasus}"

    elif dinas == "BPBD":
        hujan = st.slider("Curah Hujan", 0, 200, 80)

        if hujan > 100: indeks += 80
        else: indeks += 30

        parameter = f"Hujan:{hujan}"

    else:
        kasus = st.number_input("Jumlah Kasus", 0, 500, 5)
        indeks = min(kasus, 100)
        parameter = f"Kasus:{kasus}"

# ==============================
# OUTPUT
# ==============================
with col2:
    st.subheader("Hasil Analisis")

    indeks = min(indeks, 100)

    if indeks >= 70:
        status = "KRITIS"
        st.error(f"{status} 🚨")
    elif indeks >= 40:
        status = "WASPADA"
        st.warning(f"{status} ⚠️")
    else:
        status = "AMAN"
        st.success(status)

    st.metric("Indeks Risiko", f"{indeks}%")

    if st.button("💾 Simpan Data"):
        simpan_data(dinas, parameter, indeks, status)
        st.success("Data tersimpan!")

# ==============================
# GRAFIK & DATA
# ==============================
st.markdown("---")
st.subheader("📊 Data Monitoring")

df = ambil_data()

if not df.empty:
    st.dataframe(df)

    st.subheader("📈 Grafik Tren Risiko")
    grafik = df.groupby("dinas")["indeks"].mean()
    st.bar_chart(grafik)
else:
    st.info("Belum ada data")
