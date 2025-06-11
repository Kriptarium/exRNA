
import streamlit as st
import pandas as pd
import nolds
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="exRNA Chaos Analyzer", layout="wide")

st.title("Chaos Analysis of exRNA Dynamics Using Lyapunov Exponents")
st.markdown("This app analyzes extracellular RNA (exRNA) time series data to detect chaotic behavior during pathogen-host interactions.")

@st.cache_data
def load_data():
    return pd.read_csv("exrna_timeseries_full.csv")

df = load_data()
condition = st.sidebar.selectbox("Select Condition", df["condition"].unique())
filtered = df[df["condition"] == condition]
avg_df = filtered.groupby("time")["expression"].mean().reset_index()

st.subheader(f"Time Series - {condition}")
st.line_chart(avg_df.set_index("time"))

# Segmented Lyapunov analysis
st.subheader("Segmented Lyapunov Exponent Analysis")
segment_length = st.slider("Segment Length", 5, 30, 10)
taus = st.slider("Embedding Delay (τ)", 1, 10, 2)
dims = st.slider("Embedding Dimension (m)", 2, 10, 6)

segments = []
lyaps = []
times = []

for start in range(0, len(avg_df) - segment_length + 1, segment_length):
    segment = avg_df.iloc[start:start + segment_length]["expression"].dropna().values
    if len(segment) >= dims * taus:
        try:
            lyap = nolds.lyap_r(segment, emb_dim=dims, tau=taus)
            lyaps.append(lyap)
            times.append(avg_df.iloc[start]["time"])
        except:
            lyaps.append(np.nan)
            times.append(avg_df.iloc[start]["time"])

if lyaps:
    st.line_chart(pd.DataFrame({"Lyapunov Exponent": lyaps}, index=times))

    st.subheader("Interpretation")
    interp_text = ""
    for t, l in zip(times, lyaps):
        if l > 0.5:
            phase = "Chaotic Phase"
        elif l > 0.1:
            phase = "Transition Phase"
        else:
            phase = "Stable Phase"
        interp_text += f"At time {t}, λ = {l:.3f} → **{phase}**\n"

    st.markdown(interp_text)

# Optional Lyapunov Spectrum
st.subheader("Lyapunov Spectrum (Full)")
signal = avg_df["expression"].dropna().values
if len(signal) > dims * taus:
    try:
        lyap_spectrum = nolds.lyap_e(signal, emb_dim=dims, matrix_dim=dims)
        spectrum_df = pd.DataFrame({
            "Index": range(1, len(lyap_spectrum) + 1),
            "Lyapunov Exponent": lyap_spectrum
        })
        st.bar_chart(spectrum_df.set_index("Index"))
    except Exception as e:
        st.error(f"Error computing Lyapunov spectrum: {e}")
