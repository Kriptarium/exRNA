# exRNA-chaos-analyzer

A Python toolkit for detecting and quantifying chaotic signatures in extracellular RNA (exRNA) dynamics via Lyapunov exponent analysis.

---

## 🚀 Features

- **Raw Time-Series Processing**: Load and pre-process exRNA concentration data.  
- **Delay Embedding**: Automatic selection (or manual override) of embedding dimension _m_ and delay _τ_.  
- **Lyapunov Exponent Calculation**: Implements nearest-neighbor divergence tracking and slope estimation.  
- **Visualization**:  
  - Time-series plots  
  - Phase-space attractors  
  - Divergence / log-divergence charts  
- **Export**: Save numerical results and publication-ready figures.

---

## 📦 Installation

```bash
git clone https://github.com/Kriptarium/exRNA.git
cd exRNA
pip install -r requirements.txt
