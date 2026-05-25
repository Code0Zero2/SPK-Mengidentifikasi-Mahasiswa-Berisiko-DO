import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Identifikasi Mahasiswa beresiko DO", layout="wide")
st.title("SPK Mengidentifikasi Mahasiswa Berisiko Drop Out Menggunakan Metode WP")

st.divider()

df = pd.read_csv("dataset.csv")
with st.sidebar:
    st.subheader("Konfigurasi Kriteria WP")
    w_skskSmt1 = st.slider("Bobot SKS lulus semester 1", min_value=1, max_value=5, step=1, value=3)
    w_sksSmt2 = st.slider("Bobot SKS lulus semester 2", min_value=1, max_value=5, step=1, value=3)
    w_ukt = st.slider("Pembayaran UKT tepat waktu", min_value=1, max_value=5, step=1, value=3)
    w_tunggakan = st.slider("Tunggakan UKT", min_value=1, max_value=5, step=1, value=3)
    w_beasiswa = st.slider("Penerima Beasiswa", min_value=1, max_value=5, step=1, value=3)
    w_tunggakan = st.slider("Tunggakan UKT", min_value=1, max_value=5, step=1, value=3)