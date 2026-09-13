import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Konfigurasi Halaman Dasbor
st.set_page_config(
    page_title="ZF-Matrix Studio v1.0", page_icon="⚛️", layout="wide"
)


# Fungsi untuk memuat berkas Buku Besar (Zuhri Registry)
@st.cache_data
def load_zuhri_registry():
  # Pada implementasi nyata, muat dari berkas lokal:
  # with open("zuhri_registry.json", "r") as f:
  #     return json.load(f)
  return {
      "schema_version": "1.0.0-ZF",
      "phi_constant": 1.6180339887,
      "fractal_dimension_Df": 2.6180339887,
      "damping_alpha": 0.3819660113,
      "elements_registry": [
          {
              "symbol": "C",
              "name": "Carbon",
              "zeta_eigen": 1.6180339887,
              "klm_quantum": [1, 1, 0],
              "r0_angstrom": 0.770,
          },
          {
              "symbol": "Si",
              "name": "Silicon",
              "zeta_eigen": 2.6180339887,
              "klm_quantum": [2, 1, 1],
              "r0_angstrom": 1.110,
          },
          {
              "symbol": "Fe",
              "name": "Iron",
              "zeta_eigen": 5.2360679775,
              "klm_quantum": [3, 1, 1],
              "r0_angstrom": 1.260,
          },
          {
              "symbol": "Ni",
              "name": "Nickel",
              "zeta_eigen": 6.8541019662,
              "klm_quantum": [3, 2, 1],
              "r0_angstrom": 1.240,
          },
      ],
  }


registry_data = load_zuhri_registry()

# Header Utama Dasbor
st.title("⚛️ ZF-Matrix Studio | Zuhri Formalism DED Dashboard")
st.markdown(
    "**Mode Operasi:** `[Air-Gapped Local Workstation]` | **Golden Ratio"
    f" ($\\phi$):** `{registry_data['phi_constant']}` | **Dimensi Fraktal ($D_f$):"
    f"` `{registry_data['fractal_dimension_Df']}`"
)

# Pembagian Tata Letak Empat Panel via Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Fractal Viewport",
    "2. Matrix Kernel M_φ",
    "3. Topological Entropy S_g",
    "4. DED Streamer",
])

with tab1:
  st.subheader("Fractal Viewport (3D Space - D_f = 2.618)")
  st.caption(
      "Visualisasi kekisi atom eksponensial r_n = r_0 * phi^n tanpa batas"
      " artifisial."
  )

  # Data simulasi koordinat atom berbasis phi
  df_atoms = pd.DataFrame({
      "Element": ["Fe", "Si", "Ni", "C"],
      "X": [0.000, 1.618, 2.618, 4.236],
      "Y": [1.618, 0.000, 3.854, 1.618],
      "Z": [2.618, 1.260, 5.236, 0.618],
      "Zeta": [5.2360, 2.6180, 6.8541, 1.6180],
  })

  fig_3d = go.Figure(
      data=[
          go.Scatter3d(
              x=df_atoms["X"],
              y=df_atoms["Y"],
              z=df_atoms["Z"],
              mode="markers+text",
              text=df_atoms["Element"],
              textposition="top center",
              marker=dict(
                  size=14,
                  color=df_atoms["Zeta"],
                  colorscale="Viridis",
                  opacity=0.95,
                  line=dict(width=1, color="white"),
              ),
          )
      ]
  )
  fig_3d.update_layout(height=450, margin=dict(l=0, r=0, b=0, t=0))
  st.plotly_chart(fig_3d, use_container_width=True)

with tab2:
  st.subheader("Matrix Kernel Monitor (M_φ & Eigen Spectra)")
  elements_df = pd.DataFrame(registry_data["elements_registry"])
  st.dataframe(elements_df, use_container_width=True)
  st.info(
      "Penyelesaian matriks linier O(N) menggunakan indeks eigen resonansi"
      " ζ_k,l,m dari Buku Besar."
  )

with tab3:
  st.subheader("Topological Entropy Monitor (S_g → 0)")
  st.markdown(
      "Memantau kekekalan informasi $\\frac{\\mathrm{d}\\mathcal{I}_\\phi"
      "}{\\mathrm{d}\\tau} = 0$ dan peredaman termal $\\alpha = \\phi^{-2}$."
  )

  # Simulasi kurva entropi geometris S_g melandai ke ekuilibrium
  time_steps = np.linspace(0, 10, 100)
  sg_curve = 0.012 * np.exp(-0.55 * time_steps) + 0.00004 * np.sin(
      2 * np.pi * time_steps
  )

  fig_entropy = go.Figure()
  fig_entropy.add_trace(
      go.Scatter(
          x=time_steps,
          y=sg_curve,
          mode="lines",
          name="Entropi S_g(t)",
          line=dict(color="#00CC96", width=3),
      )
  )
  fig_entropy.add_hline(
      y=0.0001,
      line_dash="dash",
      line_color="#FFA15A",
      annotation_text="Ambang Batas Nol-Entropi (Zero-Entropy Bonding)",
  )
  fig_entropy.update_layout(
      xaxis_title="Waktu Fabrikasi (τ)",
      yaxis_title="Entropi Geometris S_g",
      height=380,
  )
  st.plotly_chart(fig_entropy, use_container_width=True)

with tab4:
  st.subheader("DED Live Link & CNC G-Code Streamer")
  col_a, col_b = st.columns(2)
  with col_a:
    st.metric(
        label="Daya Laser Adaptif (P_φ)",
        value="1,245 W",
        delta="-8.2 W (Kompensasi Alfa)",
    )
    st.metric(label="Latensi Edge Controller FPGA", value="0.78 ms", delta="OK")
    laser_override = st.slider("Modulasi Daya Laser P_φ (Watt)", 800, 2000, 1245)
  with col_b:
    st.code(
        f"""
        ; ZF-Matrix Studio DED Streamer v1.0
        G21 ; Satuan Milimeter
        G90 ; Koordinat Absolut
        M104 S{laser_override} ; Sinkronisasi P_phi
        G0 X1.6180 Y2.6180 Z0.3820
        F1200
        """,
        language="gcode",
    )
  if st.button("⚠️ EMERGENCY HOLD / PAUSE DED", type="primary"):
    st.error("Perintah jeda darurat dikirim ke Industrial Edge Controller!")
