import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Identifikasi Mahasiswa beresiko DO", layout="wide")

st.markdown("""
<style>
            /* Sembunyikan label selectbox (karena sudah ada label slider di atas) */
section[data-testid="stSidebar"] .stSelectbox label { display: none; }
/*Title Sidebar*/
    section[data-testid="stSidebar"] h3 {
    font-size: 20px !important;
}
/* Selectbox lebih kecil */
section[data-testid="stSidebar"] .stSelectbox > div > div {
    font-size: 17px !important;
    min-height: 28px !important;
    padding: 0px 4px !important;
}

/* Slider lebih compact */
section[data-testid="stSidebar"] .stSlider {
    margin-top: 10px;
    margin-bottom: -6px;
}
section[data-testid="stSidebar"] .stSlider label {
    font-size: 12px !important;
    color: #555 !important;
}

/* Divider lebih tipis */
section[data-testid="stSidebar"] hr {
    margin: 4px 0 !important;
    border-color: #e0e0e0 !important;
}
            
/* Metric cards */
[data-testid="metric-container"] {
    background: #f8f9fb;
    border: 1px solid #e2e6ea;
    border-radius: 10px;
    padding: 12px 16px;
}
[data-testid="metric-container"] label {
    font-size: 13px !important;
    color: #555 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 24px !important;
    font-weight: 600 !important;
}

/* Tab styling */
button[data-baseweb="tab"] {
    font-size: 14px !important;
    font-weight: 500 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #1a73e8 !important;
    border-bottom: 3px solid #1a73e8 !important;
}

/* Judul utama */
h1 { font-size: 42px !important; }


</style>
""", unsafe_allow_html=True)

st.title("SPK Mengidentifikasi Mahasiswa Berisiko Drop Out Menggunakan Metode WP")
df = pd.read_csv("dataset.csv")
with st.sidebar:
    st.subheader("Konfigurasi Kriteria WP🔧")
    
    w_skskSmt1 = st.slider("Bobot SKS lulus semester 1", min_value=1, max_value=5, step=1, value=3)
    t_skskSmt1 = st.selectbox("Tipe", ["Benefit", "Cost"], key="smt1")
    st.caption("SKS lulus semester 1 mencerminkan performa akademik awal mahasiswa.")
    st.divider()

    w_sksSmt2 = st.slider("Bobot SKS lulus semester 2", min_value=1, max_value=5, step=1, value=3)
    t_sksSmt2 = st.selectbox("Tipe", ["Benefit", "Cost"], key="smt2")
    st.caption("SKS lulus semester 2 menunjukkan konsistensi akademik mahasiswa.")
    st.divider()

    w_ukt = st.slider("Pembayaran UKT tepat waktu", min_value=1, max_value=5, step=1, value=3)
    t_ukt = st.selectbox("Tipe", ["Benefit", "Cost"], key="ukt")
    st.caption("Mahasiswa yang membayar UKT tepat waktu cenderung lebih stabil secara finansial.")
    st.divider()

    w_tunggakan = st.slider("Tunggakan UKT", min_value=1, max_value=5, step=1, value=3)
    t_tunggakan = st.selectbox("Tipe", ["Benefit", "Cost"], key="tunggakan")
    st.caption("Mahasiswa dengan tunggakan memiliki risiko dropout lebih tinggi.")
    st.divider()

    w_beasiswa = st.slider("Penerima Beasiswa", min_value=1, max_value=5, step=1, value=3)
    t_beasiswa = st.selectbox("Tipe", ["Benefit", "Cost"], key="beasiswa")
    st.caption("Penerima beasiswa cenderung lebih termotivasi untuk menyelesaikan studi.")
    st.divider()

    w_usiaMasuk = st.slider("Usia Masuk", min_value=1, max_value=5, step=1, value=3)
    t_usiaMasuk = st.selectbox("Tipe", ["Benefit", "Cost"], key="usia")
    st.caption("Mahasiswa dengan usia masuk lebih tua memiliki sedikit risiko lebih tinggi.")

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
    "SKS_SMT1": df["Curricular units 1st sem (approved)"] +1,
    "SKS_SMT2": df["Curricular units 2nd sem (approved)"] +1,
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
hasil = hasil.sort_values(by="Nilai WP", ascending=False)
hasil["Ranking"] = range(1, len(hasil)+1)
hasil["Mahasiswa"] = [
    f"MHS-{str(i+1).zfill(5)}" for i in hasil.index
]
p33 = np.percentile(hasil["Nilai WP"], 33)
p66 = np.percentile(hasil["Nilai WP"], 66)

def kategori(v):
    if v <= p33:
        return "Risiko Tinggi"
    elif v <= p66:
        return "Risiko Sedang"
    else:
        return "Risiko Rendah"

hasil["Kategori"] = hasil["Nilai WP"].apply(kategori)

# tanpilan
tab1, tab2, tab3 = st.tabs(["Dataset", "WP", "rangking"])
with tab1:
    st.subheader("Dataset")
    st.dataframe(df)
    
with tab2:
    st.subheader("Perhitungan Weighted Product")

    nama_kriteria = [
        "SKS Lulus Sem 1", "SKS Lulus Sem 2", "UKT Tepat Waktu",
        "Tunggakan UKT", "Penerima Beasiswa", "Usia Masuk"
    ]
    tipe_list = [t_skskSmt1, t_sksSmt2, t_ukt, t_tunggakan, t_beasiswa, t_usiaMasuk]
    bobot_asli = np.array([w_skskSmt1, w_sksSmt2, w_ukt, w_tunggakan, w_beasiswa, w_usiaMasuk], dtype=float)
    bobot_norm = bobot_asli / np.sum(bobot_asli)

    df_bobot = pd.DataFrame({
        "Kriteria": nama_kriteria,
        "Bobot Input": bobot_asli.astype(int),
        "Tipe": tipe_list,
        "Bobot Normalisasi": bobot_norm.round(4),
    })

    # Bobot normalisasi penuh lebar
    st.write("Bobot Normalisasi")
    st.dataframe(df_bobot, use_container_width=True, hide_index=True)

    st.divider()

    # Matriks dan Vektor berdampingan
    col1, col2 = st.columns(2)
    with col1:
        st.write("Matriks Keputusan (20 data pertama)")
        st.dataframe(data_wp.head(20), use_container_width=True)
    with col2:
        st.write("Vektor S & V (20 data pertama)")
        df_sv = pd.DataFrame({
            "Vektor S": S[:20],
            "Vektor V": V[:20]
        }).round(6)
        st.dataframe(df_sv, use_container_width=True)

with tab3:
    st.subheader("Ranking Mahasiswa Risiko DO")

    total = len(hasil)
    tinggi = (hasil["Kategori"] == "Risiko Tinggi").sum()
    sedang = (hasil["Kategori"] == "Risiko Sedang").sum()
    rendah = (hasil["Kategori"] == "Risiko Rendah").sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Mahasiswa", f"{total:,}")
    c2.metric("🔴 Risiko Tinggi", f"{tinggi:,}")
    c3.metric("🟡 Risiko Sedang", f"{sedang:,}")
    c4.metric("🟢 Risiko Rendah", f"{rendah:,}")

    st.divider()

    filter_kat = st.radio(
        "Filter Kategori:",
        ["Semua", "Risiko Tinggi", "Risiko Sedang", "Risiko Rendah"],
        horizontal=True
    )

    if filter_kat == "Semua":
        top3_tinggi = hasil[hasil["Kategori"] == "Risiko Tinggi"].head(3)
        top3_sedang = hasil[hasil["Kategori"] == "Risiko Sedang"].head(3)
        top3_rendah = hasil[hasil["Kategori"] == "Risiko Rendah"].head(3)
        tampil = pd.concat([top3_tinggi, top3_sedang, top3_rendah])[
            ["Ranking", "Mahasiswa", "Nilai WP", "Kategori", "Target"]
        ].reset_index(drop=True)
    else:
        tampil = hasil[hasil["Kategori"] == filter_kat].head(10)[
            ["Ranking", "Mahasiswa", "Nilai WP", "Kategori", "Target"]
        ].reset_index(drop=True)

    def warna_baris(row):
        if row["Kategori"] == "Risiko Tinggi":
            return ["background-color: #c0392b; color: white"] * len(row)
        elif row["Kategori"] == "Risiko Sedang":
            return ["background-color: #fc9803; color: white"] * len(row)
        else:
            return ["background-color: #27ae60; color: white"] * len(row)
    st.dataframe(
        tampil.style.apply(warna_baris, axis=1),
        use_container_width=True,
        hide_index=True
    )
    