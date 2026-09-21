import streamlit as st
import datetime as dt
import pandas as pd
from zoneinfo import ZoneInfo
from load import save_data_to_google_sheets, save_data
import os

waktuUpload = dt.datetime.now(ZoneInfo("Asia/Makassar")).strftime("%Y-%m-%d %H:%M:%S")
PATH_LOG = "data/log upload.csv"

st.set_page_config(
    page_title="Dashboard Team PO PT PEP Bunyu Field",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.title("⬆️ Upload Data Production")
st.divider()

file = st.file_uploader("Upload Data dengan format .xlsx, .xls", type=["xlsx", "xls"])

bar_progress = st.progress(0)
text_progress = st.empty()

if file is not None:
    text_progress.text("Membaca sheet Prod...")
    OilGasData = pd.read_excel(file, sheet_name="PROD")
    bar_progress.progress(13)

    text_progress.text("Membaca sheet Sumur Injeksi...")
    wipData = pd.read_excel(file, sheet_name="SUMUR INJEKSI")
    bar_progress.progress(26)

    text_progress.text("Membaca sheet Well...")
    wellData = pd.read_excel(file, sheet_name="WELL")
    bar_progress.progress(39)

    text_progress.text("Filter data Prod berdasarkan tahun ini...")
    OilGasData = save_data(OilGasData, "DATE")
    bar_progress.progress(52)

    text_progress.text("Filter data Sumur Injeksi berdasarkan tahun ini...")
    wipData = save_data(wipData, "DATE")
    bar_progress.progress(65)

    text_progress.text("Filter data Well berdasarkan tahun ini...")
    wellData = save_data(wellData, "Date")
    bar_progress.progress(78)


    text_progress.text("Mengupload data ke Google Sheets...")
    bar_progress.progress(91)

    try:
        save_data_to_google_sheets(OilGasData, wipData, wellData, "tabelOilGas", "tabelWip", "tabelWell")

        text_progress.text("Data berhasil diupload ke Google Sheets... 100%")
        bar_progress.progress(100)
        st.success("✅ Data berhasil diupload ke Google Sheets")
        
        dataLog = pd.DataFrame([{
                    "Waktu Upload" : waktuUpload,
                    "Production Oil & Gas" : "Sheet Oil Gas",
                    "WIP" : "Sheet WIP",
                    "Well" : "Sheet Well",
                    "Status" : "✅ Berhasil"
                }])
        
        if os.path.exists(PATH_LOG) :
            dataLog.to_csv("assets/log upload.csv", index=False, mode="a", header=False)
        else :
            dataLog.to_csv("assets/log upload.csv", index=False, mode="w")

    except Exception as e :
        dataLog = pd.DataFrame([{
                    "Waktu Upload" : waktuUpload,
                    "Production Oil & Gas" : "-",
                    "WIP" : "-",
                    "Well" : "-",
                    "Status" : "⚠️ Gagal"
                }])
        if os.path.exists(PATH_LOG) :
            dataLog.to_csv("assets/log upload.csv", index=False, mode="a", header=False)
        else :
            dataLog.to_csv("assets/log upload.csv", index=False, mode="w")

st.divider()
st.subheader("Log Data Upload")

if os.path.exists("assets/log upload.csv")  :
    dataLog = pd.read_csv("assets/log upload.csv")
    st.dataframe(dataLog, hide_index=True)
else :
    st.write("Belum ada data yang diupload.")
