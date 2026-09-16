import pandas as pd
import datetime as dt
from datetime import date, timedelta
import streamlit as st
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

waktuUpload = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
PATH_LOG = "data/log upload.csv"

SERVICE_ACCOUNT_FILE = 'dashboard-magang-eb8250cdacca.json'
 
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

credential = Credentials.from_service_account_info(dict(st.secrets["gcp_service_account"]), scopes="https://www.googleapis.com/auth/spreadsheets")
 
SPREADSHEET_ID = '1WwBp8XhrDM7WA-emRpvhDfbbRYVX_nWQtPmrwTmxEhA'
RANGE_NAME = 'Sheet1'

def save_data (tabel, kolom) :
    hariIni = date.today()
    h_1 = hariIni - timedelta(days=1)
    tahunIni = h_1.year

    tabel[kolom] = pd.to_datetime(tabel[kolom])

    return tabel[tabel[kolom].dt.year == tahunIni]

@st.cache_data
def save_data_to_google_sheets (data, sheet_table) :
    try:
        service = build('sheets', 'v4', credentials=credential)
        sheet = service.spreadsheets()
        df = data.copy()

        df = df.map(
        lambda x: x.strftime("%Y-%m-%d")
        if isinstance(x, (pd.Timestamp, dt.datetime, dt.date))
        else x
        )

        df = df.fillna("")

        df = df.astype(str)

        values = [df.columns.tolist()] + df.values.tolist()
        body = {
            'values': values
        }

        sheet.values().clear(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{sheet_table}!A1:ZZ"
        ).execute()

 
        sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{sheet_table}!A1",
            valueInputOption='RAW',
            body=body
        ).execute()

        return True
    except Exception as e :
        print('Terjadi kesalahan saat memasukkan data ke Google Sheets : ', e)

# def load_data (oilgas, wip, well) :
#     try :
#         oilgas = save_data(oilgas, "DATE")
#         wip = save_data(wip, "DATE")
#         well = save_data(well, "Date")

#         oilgas.to_csv("data/oilngas.csv", index=False)
#         wip.to_csv("data/wip.csv", index=False)
#         well.to_csv("data/well.csv", index=False)

#         dataLog = pd.DataFrame([{
#             "Waktu Upload" : waktuUpload,
#             "File Production Oil & Gas" : "oilngas.csv",
#             "File WIP" : "wip.csv",
#             "File Well" : "well.csv",
#             "Status" : "✅ Berhasil"
#         }])

#         if os.path.exists(PATH_LOG) :
#             dataLog.to_csv("data/log upload.csv", index=False, mode="a", header=False)
#         else :
#             dataLog.to_csv("data/log upload.csv", index=False, mode="w")
#         return True
#     except Exception as e :
#         dataLog = {
#                     "Waktu Upload" : waktuUpload,
#                     "File Production Oil & Gas" : "-",
#                     "File WIP" : "-",
#                     "File Sales" : "-",
#                     "Status" : "⚠️ Gagal"
#                 }
#         if os.path.exists(PATH_LOG) :
#             dataLog.to_csv("data/log upload.csv", index=False, mode="a", header=False)
#         else :
#             dataLog.to_csv("data/log upload.csv", index=False, mode="w")