import streamlit as st
import pandas as pd
from pathlib import Path

bulan = st.session_state.get("bulan", "Semua")

BASE_DIR = Path(__file__).resolve().parent
file_path_oil_gas = BASE_DIR / "data" / f"oilngas.csv"
file_path_wip = BASE_DIR / "data" / f"wip.csv"
file_path_well = BASE_DIR / "data" / f"well.csv"

bulan_map = {
    "Januari": 1,
    "Februari": 2,
    "Maret": 3,
    "April": 4,
    "Mei": 5,
    "Juni": 6,
    "Juli": 7,
    "Agustus": 8,
    "September": 9,
    "Oktober": 10,
    "November": 11,
    "Desember": 12
}


@st.cache_data
def read_data() :
    tabelOilGas = pd.read_csv(file_path_oil_gas)
    tabelWip = pd.read_csv(file_path_wip)
    tabelWell = pd.read_csv(file_path_well)

    return tabelOilGas, tabelWip, tabelWell

def transform_data (month):
    tabelOilGas, tabelWip, tabelWell = read_data()

    tabelOilGas["DATE"] = pd.to_datetime(tabelOilGas["DATE"],format="%Y-%m-%d")
    tabelWip["DATE"] = pd.to_datetime(tabelWip["DATE"],format="%Y-%m-%d")
    tabelWell["Date"] = pd.to_datetime(tabelWell["Date"],format="%Y-%m-%d")

    tabelWip["Flowrate (BWPD)"] = pd.to_numeric(tabelWip["Flowrate (BWPD)"], errors="coerce").fillna(0)
    tabelWip["Tekanan (PSI)"] = pd.to_numeric(tabelWip["Tekanan (PSI)"], errors="coerce").fillna(0)

    tabelOilGas["SALES PLN Bunyu"] = pd.to_numeric(tabelOilGas["SALES PLN Bunyu"], errors="coerce")
    tabelOilGas["SALES City Gas Bunyu"] = pd.to_numeric(tabelOilGas["SALES City Gas Bunyu"], errors="coerce")
    tabelOilGas["SALES City Gas Tarakan"] = pd.to_numeric(tabelOilGas["SALES City Gas Tarakan"], errors="coerce")
    tabelOilGas["G-8"] = pd.to_numeric(tabelOilGas["G-8"], errors="coerce")
    tabelOilGas["Binalatung"] = pd.to_numeric(tabelOilGas["Binalatung"], errors="coerce")
    tabelOilGas["Kampung 1"] = pd.to_numeric(tabelOilGas["Kampung 1"], errors="coerce")

    tabelWell["Prod Act Oil"] = pd.to_numeric(tabelWell["Prod Act Oil"], errors="coerce")
    tabelWell["Prod Act Gross"] = pd.to_numeric(tabelWell["Prod Act Gross"], errors="coerce")
    tabelWell["Gas Own (Mscfd)"] = pd.to_numeric(tabelWell["Gas Own (Mscfd)"], errors="coerce")
    tabelWell["Gas Inj (Mscfd)"] = pd.to_numeric(tabelWell["Gas Inj (Mscfd)"], errors="coerce")

    tabelWell["P.csg"] = pd.to_numeric(tabelWell["P.csg"], errors="coerce")
    tabelWell["P.tbg"] = pd.to_numeric(tabelWell["P.tbg"], errors="coerce")
    tabelWell["P.fl"] = pd.to_numeric(tabelWell["P.fl"], errors="coerce")
    tabelWell["P.sep"] = pd.to_numeric(tabelWell["P.sep"], errors="coerce")

    # Medco to City Gas,Medco to PLN
    tabelOilGas["Medco to City Gas"] = tabelOilGas["Medco to City Gas"].astype(float)
    tabelOilGas["Medco to PLN"] = tabelOilGas["Medco to PLN"].astype(float)

    if month == "Semua":
        tabelOilGas = tabelOilGas.sort_values("DATE", ascending=True)
        tabelWip = tabelWip.sort_values("DATE", ascending=True)
        tabelWell = tabelWell.sort_values("Date", ascending=True)
    else :
        tabelOilGas = tabelOilGas[tabelOilGas["DATE"].dt.month == bulan_map[month]]
        tabelWip = tabelWip[tabelWip["DATE"].dt.month == bulan_map[month]]
        tabelWell = tabelWell[tabelWell["Date"].dt.month == bulan_map[month]]

        tabelOilGas = tabelOilGas.sort_values("DATE", ascending=True)
        tabelWip = tabelWip.sort_values("DATE", ascending=True)
        tabelWell = tabelWell.sort_values("Date", ascending=True)
        
    return tabelOilGas, tabelWip, tabelWell