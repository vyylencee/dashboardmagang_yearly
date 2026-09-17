import streamlit as st
import datetime as dt
import pandas as pd
from load import save_data_to_google_sheets, save_data
import os

waktuUpload = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
PATH_LOG = "data/log upload.csv"

st.set_page_config(
    page_title="Dashboard Team PO PT PEP Bunyu Field",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("⬆️ Upload Data Production")
st.divider()

file = st.file_uploader("Upload Data dengan format .xlsx, .xls", type=["xlsx", "xls"])
try :
    OilGasData = pd.read_excel(file, sheet_name="PROD")
    wipData = pd.read_excel(file, sheet_name="SUMUR INJEKSI")
    wellData = pd.read_excel(file, sheet_name="WELL")

    OilGasData = save_data(OilGasData, "DATE")
    wipData = save_data(wipData, "DATE")
    wellData = save_data(wellData, "Date")

    save_data_to_google_sheets(OilGasData, "tabelOilGas")
    save_data_to_google_sheets(wipData, "tabelWip")
    save_data_to_google_sheets(wellData, "tabelWell")

    dataLog = pd.DataFrame([{
                "Waktu Upload" : waktuUpload,
                "Production Oil & Gas" : "Sheet Oil Gas",
                "WIP" : "Sheet WIP",
                "Well" : "Sheet Well",
                "Status" : "✅ Berhasil"
            }])
    
    if os.path.exists(PATH_LOG) :
        dataLog.to_csv("data/log upload.csv", index=False, mode="a", header=False)
    else :
        dataLog.to_csv("data/log upload.csv", index=False, mode="w")

    st.cache_data.clear()
    st.rerun()
except Exception as e :
    dataLog = pd.DataFrame([{
                "Waktu Upload" : waktuUpload,
                "Production Oil & Gas" : "-",
                "WIP" : "-",
                "Well" : "-",
                "Status" : "⚠️ Gagal"
            }])
    if os.path.exists(PATH_LOG) :
        dataLog.to_csv("data/log upload.csv", index=False, mode="a", header=False)
    else :
        dataLog.to_csv("data/log upload.csv", index=False, mode="w")

st.divider()
st.subheader("Log Data Upload")

if os.path.exists("data/log upload.csv")  :
    dataLog = pd.read_csv("data/log upload.csv")
    st.dataframe(dataLog, hide_index=True)
else :
    st.write("Belum ada data yang diupload.")