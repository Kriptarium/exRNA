
import streamlit as st
import pandas as pd
import nolds
import matplotlib.pyplot as plt

st.title("Chaos Analysis of exRNA Dynamics")

uploaded_file = st.file_uploader("Upload your exRNA time series CSV", type=["csv"])
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    signal = data.iloc[:, 1].dropna().values  # assuming 2nd column is expression values

    st.write("## Time Series Plot")
    st.line_chart(signal)

    st.write("## Lyapunov Exponent")
    lyap = nolds.lyap_r(signal, emb_dim=6, tau=2)
    st.write(f"Lyapunov Exponent (λ): {lyap:.4f}")
