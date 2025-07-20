import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from polcurvefit import polcurvefit, DataImport

st.title("Electrochemical Data Analysis")

uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    
    st.write("Uploaded Data:")
    st.dataframe(df)

    potential_column = df.columns[0]
    current_column = df.columns[2]

    E = df[potential_column].values
    I = df[current_column].values

    Polcurve = polcurvefit(E, I, sample_surface=1E-4)
    
    popt, E_corr, I_corr, anodic_slope, cathodic_slope, r_square = Polcurve.active_pol_fit(window=[-0.07, 0.07])

    st.write("Fitted Parameters:")
    st.write(f"Fitted parameters: {popt}")
    st.write(f"E_corr: {E_corr}")
    st.write(f"I_corr: {I_corr}")
    st.write(f"Anodic slope: {anodic_slope}")
    st.write(f"Cathodic slope: {cathodic_slope}")
    st.write(f"R²: {r_square}")

    # Inline Matplotlib plotting
    fig, ax = plt.subplots()
    Polcurve.plot_polcurve(ax)  # Assuming your Polcurve object has a method to plot directly on a Matplotlib axis
    st.pyplot(fig)
