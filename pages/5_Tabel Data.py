import streamlit as st
import pandas as pd
from transform import transform_data

st.set_page_config(
    page_title="Dashboard Team PO PT PEP Bunyu Field",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Tabel Data Production Operations PT Pertamina EP Asset 5 Bunyu Field")
st.divider()

bulan = st.sidebar.selectbox("Pilih Bulan", 
                            ["Semua", "Januari", "Februari",
                            "Maret", "April", "Mei",
                            "Juni", "Juli", "Agustus",
                            "September", "Oktober",
                            "November", "Desember"], key="month")

try :
    tabelOilGas, tabelWip, tabelWell = transform_data(bulan)

    if bulan != "Semua":
        st.subheader(f"Tabel Data Production {bulan} {tabelOilGas['DATE'].max().year}")
        st.dataframe(tabelOilGas, hide_index=True)
    else :
        st.subheader(f"Tabel Data Production Tahun {tabelOilGas['DATE'].max().year}")
        st.dataframe(tabelOilGas, hide_index=True)

    st.divider()

    if bulan != "Semua":
        st.subheader(f"Tabel Data Water Injection {bulan} {tabelOilGas['DATE'].max().year}")
        st.dataframe(tabelWip, hide_index=True)
    else :
        st.subheader(f"Tabel Data Water Injection Tahun {tabelOilGas['DATE'].max().year}")
        st.dataframe(tabelWip, hide_index=True)

    st.divider()

    if bulan != "Semua":
        st.subheader(f"Tabel Data Well {bulan} {tabelOilGas['DATE'].max().year}")
        st.dataframe(tabelWell, hide_index=True)
    else :
        st.subheader(f"Tabel Data Well Tahun {tabelOilGas['DATE'].max().year}")
        st.dataframe(tabelWell, hide_index=True)
except KeyError as e :
    st.error("Data tidak tersedia pada database.")