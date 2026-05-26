import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Identifikasi Mahasiswa beresiko DO", layout="wide")
st.title("SPK Mengidentifikasi Mahasiswa Berisiko Drop Out Menggunakan Metode WP")


df = pd.read_csv("dataset.csv")
# konfigurasi kriteria
with st.sidebar:
    st.subheader("Konfigurasi Kriteria WP")
    w_skskSmt1 = st.slider("Bobot SKS lulus semester 1", min_value=1, max_value=5, step=1, value=3)
    t_skskSmt1 = st.selectbox("Tipe", ["Benefit", "Cost"], key="smt1")
    st.divider()    
    w_sksSmt2 = st.slider("Bobot SKS lulus semester 2", min_value=1, max_value=5, step=1, value=3)
    t_sksSmt2 = st.selectbox("Tipe", ["Benefit", "Cost"], key="smt2")
    st.divider()
    w_ukt = st.slider("Pembayaran UKT tepat waktu", min_value=1, max_value=5, step=1, value=3)
    t_ukt = st.selectbox("Tipe", ["Benefit", "Cost"], key="ukt")
    st.divider()
    w_tunggakan = st.slider("Tunggakan UKT", min_value=1, max_value=5, step=1, value=3)
    t_tunggakan = st.selectbox("Tipe", ["Benefit", "Cost"], key="tunggakan")
    st.divider()
    w_beasiswa = st.slider("Penerima Beasiswa", min_value=1, max_value=5, step=1, value=3)
    t_beasiswa = st.selectbox("Tipe", ["Benefit", "Cost"], key="beasiswa")
    st.divider()
    w_usiaMasuk = st.slider("Usia Masuk", min_value=1, max_value=5, step=1, value=3)
    t_usiaMasuk = st.selectbox("Tipe", ["Benefit", "Cost"], key="usia")
    

# Perhitungan WP 
# bobot 
bobot = np.array([
    w_skskSmt1,
    w_sksSmt2,
    w_ukt,
    w_tunggakan,
    w_beasiswa,
    w_usiaMasuk
], dtype=float)
    
# normalisasi bobot
bobot = bobot / np.sum(bobot)

# jika cost jadi negatif
if t_skskSmt1 == "Cost":
    bobot[0] *= -1

if t_sksSmt2 == "Cost":
    bobot[1] *= -1

if t_ukt == "Cost":
    bobot[2] *= -1

if t_tunggakan == "Cost":
    bobot[3] *= -1

if t_beasiswa == "Cost":
    bobot[4] *= -1

if t_usiaMasuk == "Cost":
    bobot[5] *= -1

# data kriteria
data_wp = pd.DataFrame({
    "SKS_SMT1": df["Curricular units 1st sem (approved)"],
    "SKS_SMT2": df["Curricular units 2nd sem (approved)"],
    "UKT": df["Tuition fees up to date"],
    "TUNGGAKAN": df["Debtor"],
    "BEASISWA": df["Scholarship holder"],
    "USIA": df["Age at enrollment"]
})

# konversi kategori ke angka
data_wp["UKT"] = data_wp["UKT"].map({
    1: 5,
    0: 1
})
data_wp["TUNGGAKAN"] = data_wp["TUNGGAKAN"].map({
    0: 5,
    1: 1
})
data_wp["BEASISWA"] = data_wp["BEASISWA"].map({
    1: 5,
    0: 2
})

# vektor s
matriks = data_wp.values
S = np.prod(np.power(matriks, bobot), axis=1)

# vektor v
V = S / np.sum(S)

hasil = df.copy()
hasil["Nilai WP"] = V
hasil = hasil.sort_values(by="Nilai WP", ascending=True)
hasil["Ranking"] = range(1, len(hasil)+1)
hasil["Mahasiswa"] = [
    f"MHS-{str(i+1).zfill(5)}" for i in hasil.index
]
def kategori(v):
    if v >= 0.0004:
        return "Risiko Rendah"
    elif v >= 0.0002:
        return "Risiko Sedang"
    else:
        return "Risiko Tinggi"

hasil["Kategori"] = hasil["Nilai WP"].apply(kategori)

# tanpilan
tab1, tab2, tab3 = st.tabs(["Dataset", "WP", "rangking"])
with tab1:
    st.subheader("Dataset")
    st.dataframe(df)
    
with tab2:
    st.subheader("Perhitungan Weighted Product")

    st.write("Bobot Normalisasi")
    st.write(bobot)

    st.write("Data WP")
    st.dataframe(data_wp)

    st.write("Nilai Vector S")
    st.write(S)

    st.write("Nilai Preferensi V")
    st.write(V)
    
with tab3:
    st.subheader("Ranking Mahasiswa Risiko DO")
    top10 = hasil.head(10)
    st.dataframe(
        top10[[
            "Mahasiswa",
            "Nilai WP",
            "Kategori",
            "Ranking"
        ]]
    )