import streamlit as st
import pandas as pd
from load import load_data
import os
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

    load_data(OilGasData, wipData, wellData)
except ValueError :
    pass

st.divider()
st.subheader("Log Data Upload")

if os.path.exists("data/log upload.csv")  :
    dataLog = pd.read_csv("data/log upload.csv")
    st.dataframe(dataLog, hide_index=True)
else :
    st.write("Belum ada data yang diupload.")