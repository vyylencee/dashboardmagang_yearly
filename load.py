import pandas as pd
import datetime as dt
from datetime import date, timedelta
import streamlit as st
import os

waktuUpload = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
PATH_LOG = "data/log upload.csv"

def save_data (tabel, kolom) :
    hariIni = date.today()
    h_1 = hariIni - timedelta(days=1)
    tahunIni = h_1.year

    tabel[kolom] = pd.to_datetime(tabel[kolom])

    return tabel[tabel[kolom].dt.year == tahunIni]

@st.cache_data
def load_data (oilgas, wip, well) :
    try :
        oilgas = save_data(oilgas, "DATE")
        wip = save_data(wip, "DATE")
        well = save_data(well, "Date")

        oilgas.to_csv("data/oilngas.csv", index=False)
        wip.to_csv("data/wip.csv", index=False)
        well.to_csv("data/well.csv", index=False)

        dataLog = pd.DataFrame([{
            "Waktu Upload" : waktuUpload,
            "File Production Oil & Gas" : "oilngas.csv",
            "File WIP" : "wip.csv",
            "File Well" : "well.csv",
            "Status" : "✅ Berhasil"
        }])

        if os.path.exists(PATH_LOG) :
            dataLog.to_csv("data/log upload.csv", index=False, mode="a", header=False)
        else :
            dataLog.to_csv("data/log upload.csv", index=False, mode="w")
        return True
    except Exception as e :
        dataLog = {
                    "Waktu Upload" : waktuUpload,
                    "File Production Oil & Gas" : "-",
                    "File WIP" : "-",
                    "File Sales" : "-",
                    "Status" : "⚠️ Gagal"
                }
        if os.path.exists(PATH_LOG) :
            dataLog.to_csv("data/log upload.csv", index=False, mode="a", header=False)
        else :
            dataLog.to_csv("data/log upload.csv", index=False, mode="w")