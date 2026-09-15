import streamlit as st
import pandas as pd
from transform import transform_data

st.set_page_config(
    page_title="Dashboard Team PO PT PEP Bunyu Field",
    layout="wide",
    initial_sidebar_state="expanded"
)

oilGas = pd.read_csv("data/oilngas.csv")
oilGas["DATE"] = pd.to_datetime(oilGas["DATE"])

st.title("📊 Tabel Data Production Operations PT Pertamina EP Asset 5 Bunyu Field")
st.divider()

bulan = st.sidebar.selectbox("Pilih Bulan", 
                            ["Semua", "Januari", "Februari",
                            "Maret", "April", "Mei",
                            "Juni", "Juli", "Agustus",
                            "September", "Oktober",
                            "November", "Desember"], key="month")

tabelOilGas, tabelWip, tabelWell = transform_data(bulan)

if bulan != "Semua":
    st.subheader(f"Tabel Data Production {bulan} {oilGas['DATE'].max().year}")
    st.dataframe(tabelOilGas, hide_index=True)
else :
    st.subheader(f"Tabel Data Production Tahun {oilGas['DATE'].max().year}")
    st.dataframe(tabelOilGas, hide_index=True)

st.divider()

if bulan != "Semua":
    st.subheader(f"Tabel Data Water Injection {bulan} {oilGas['DATE'].max().year}")
    st.dataframe(tabelWip, hide_index=True)
else :
    st.subheader(f"Tabel Data Water Injection Tahun {oilGas['DATE'].max().year}")
    st.dataframe(tabelWip, hide_index=True)

st.divider()

if bulan != "Semua":
    st.subheader(f"Tabel Data Well {bulan} {oilGas['DATE'].max().year}")
    st.dataframe(tabelWell, hide_index=True)
else :
    st.subheader(f"Tabel Data Well Tahun {oilGas['DATE'].max().year}")
    st.dataframe(tabelWell, hide_index=True)
    