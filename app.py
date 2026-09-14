import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AMFF Mineral Reagent Optimizer (AMFF-RO)",
    page_icon="⛏️",
    layout="wide"
)

# Custom CSS styling
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

st.title("⛏️ AMFF Mineral Reagent Optimizer (AMFF-RO)")
st.markdown("**Enterprise Decision Support System (DSS) Berbasis Adaptive Mineral Field Formulation (AMFF) untuk Efisiensi Reagen Pengolahan Mineral**")

# Sidebar for Configuration
st.sidebar.header("⚙️ Konfigurasi Parameter AMFF")
k_adaptif = st.sidebar.number_input("Konstanta Adaptif ($K_{\\text{adaptif}}$)", value=1.25, step=0.01, format="%.2f")
kapasitas_pabrik_tpd = st.sidebar.number_input("Kapasitas Pabrik (Ton/Hari - TPD)", value=5000.0, step=500.0)
biaya_reagen_per_kg = st.sidebar.number_input("Biaya Reagen ($ / kg)", value=3.50, step=0.10)

st.sidebar.markdown("---")
st.sidebar.info("""
Rumus Dasar AMFF:
$\\text{Dosis Optima} = \\left(\\frac{A}{B}\\right) \\times K_{\\text{adaptif}}$
""")

# Main Content Area
col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Input Variabel Operasional")
    indeks_fasa_mineral = st.slider(
        "Indeks Fasa Mineral ($A$) - Kompleksitas Kadar & Target Recovery", 
        min_value=10.0, max_value=200.0, value=92.4, step=0.1
    )
    faktor_hambatan_pulp = st.slider(
        "Faktor Hambatan Pulp ($B$) - Viskositas, Suhu & Karakteristik pH", 
        min_value=1.0, max_value=50.0, value=8.5, step=0.1
    )
    dosis_aktual = st.number_input(
        "Konsumsi Reagen Aktual di Lapangan (kg/ton)", 
        value=15.0, step=0.1
    )

with col2:
    st.subheader("📊 Hasil Analisis AMFF & Rekomendasi")
    
    if faktor_hambatan_pulp > 0:
        dosis_optima = (indeks_fasa_mineral / faktor_hambatan_pulp) * k_adaptif
        penghematan_per_ton = max(0.0, dosis_aktual - dosis_optima)
        penghematan_harian = penghematan_per_ton * kapasitas_pabrik_tpd
        penghematan_biaya_tahunan = penghematan_harian * biaya_reagen_per_kg * 365
        
        st.metric(label="Rekomendasi Dosis Optima (kg/ton)", value=f"{dosis_optima:.4f}")
        st.metric(label="Potensi Reduksi Limbah (kg/ton)", value=f"{penghematan_per_ton:.4f}")
        st.metric(label="Proyeksi Penghematan Biaya Tahunan ($)", value=f"${penghematan_biaya_tahunan:,.2f}")
        
        if dosis_optima <= dosis_aktual:
            st.success("Status: Efisiensi Reagen AMFF Optimal & Terkendali")
        else:
            st.warning("Status: Dosis Aktual Di Bawah Rekomendasi AMFF (Risiko Recovery Menurun)")
    else:
        st.error("Faktor Hambatan Pulp (B) tidak boleh bernilai nol.")

# Section for historical log simulation
st.markdown("---")
st.subheader("📈 Simulasi Tren Batch AMFF Operasional")
if st.button("Jalankan Simulasi AMFF"):
    data_simulasi = []
    for i in range(1, 11):
        a_val = indeks_fasa_mineral + (i * 0.5)
        b_val = faktor_hambatan_pulp
        opt = (a_val / b_val) * k_adaptif
        saving = max(0.0, dosis_aktual - opt)
        data_simulasi.append({
            "Batch": f"Batch #{i}",
            "Indeks Fasa A": round(a_val, 2),
            "Dosis Optima (kg/t)": round(opt, 4),
            "Reduksi Limbah (kg/t)": round(saving, 4)
        })
    df_sim = pd.DataFrame(data_simulasi)
    st.dataframe(df_sim, use_container_width=True)
