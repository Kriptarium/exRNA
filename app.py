
import streamlit as st
import pandas as pd
import nolds
import matplotlib.pyplot as plt

st.set_page_config(page_title="exRNA Chaos Analyzer", layout="wide")

st.title("Chaos Analysis of exRNA Dynamics Using Lyapunov Exponents")
st.markdown("""
This app analyzes extracellular RNA (exRNA) time series data to detect chaotic behavior during pathogen-host interactions.
""")

@st.cache_data
def load_data():
    return pd.read_csv("exrna_timeseries_full.csv")

df = load_data()

# Sidebar to choose condition
condition = st.sidebar.selectbox("Select Condition", df["condition"].unique())
filtered = df[df["condition"] == condition]

# Plot time series
st.subheader(f"Time Series - {condition}")
avg_df = filtered.groupby("time")["expression"].mean().reset_index()
st.line_chart(avg_df.set_index("time"))

# Compute Lyapunov Exponent
st.subheader("Lyapunov Exponent Calculation")
signal = avg_df["expression"].dropna().values

tau = st.slider("Embedding Delay (τ)", 1, 10, 2)
m = st.slider("Embedding Dimension (m)", 2, 10, 6)

try:
    lyap = nolds.lyap_r(signal, emb_dim=m, tau=tau)
    st.success(f"Lyapunov Exponent (λ): {lyap:.4f}")
except Exception as e:
    st.error(f"Error computing Lyapunov exponent: {e}")
