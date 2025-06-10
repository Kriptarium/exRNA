
import streamlit as st
import pandas as pd
import nolds
import matplotlib.pyplot as plt

st.set_page_config(page_title="exRNA Chaos Analyzer", layout="wide")

st.title("Chaos Analysis of exRNA Dynamics Using Lyapunov Exponents")
st.markdown("""
This app analyzes extracellular RNA (exRNA) time series data to detect chaotic behavior, especially during pathogen-host interactions. 
You can upload your own `.csv` file or use the preloaded dataset to start.
""")

# Sidebar for file upload
st.sidebar.header("Upload exRNA CSV")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

# Load default data if no upload
if uploaded_file is None:
    st.sidebar.info("Using default example data.")
    df = pd.read_csv("sample_data.csv")
else:
    df = pd.read_csv(uploaded_file)

# Display time series
st.subheader("Time Series Plot")
st.line_chart(df.set_index(df.columns[0]))

# Compute Lyapunov Exponent
st.subheader("Lyapunov Exponent Calculation")
signal = df.iloc[:, 1].dropna().values

tau = st.slider("Embedding Delay (τ)", 1, 10, 2)
m = st.slider("Embedding Dimension (m)", 2, 10, 6)

try:
    lyap = nolds.lyap_r(signal, emb_dim=m, tau=tau)
    st.success(f"Lyapunov Exponent (λ): {lyap:.4f}")
except Exception as e:
    st.error(f"Error computing Lyapunov exponent: {e}")
