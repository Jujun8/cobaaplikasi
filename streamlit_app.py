import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd
from datetime import datetime

# ==============================
# KONEKSI GOOGLE SHEETS
# ==============================
def connect_gsheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        st.secrets["gcp_service_account"], scope
    )

    client = gspread.authorize(creds)

    sheet = client.open_by_key("ISI_SPREADSHEET_ID").sheet1
    return sheet

def simpan_data(dinas, parameter, indeks, status):
    sheet = connect_gsheet()

    sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        dinas,
        parameter,
        indeks,
        status
    ])

def ambil_data():
    sheet = connect_gsheet()
    data = sheet.get_all_records()
    return pd.DataFrame(data)

df = ambil_data()

if not df.empty:
    st.dataframe(df)

    st.subheader("📈 Grafik Risiko")
    st.line_chart(df["indeks"])
else:
    st.info("Belum ada data")
