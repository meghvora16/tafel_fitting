import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from polcurvefit import polcurvefit  # Assuming this library is correct
# Example data loading function:
from polcurvefit import DataImport

# Application title
st.title("Electrochemical Data Analysis")

# File uploader to support CSV and Excel
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Read file based on type
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)

    st.write("Uploaded Data:")
    st.dataframe(df)

    # Assuming column 0 for potential and column 2 for current
    potential_column = df.columns[0]
    current_column = df.columns[2]

    E = df[potential_column].values
    I = df[current_column].values

    # Initialize fit
    Polcurve = polcurvefit(E, I, sample_surface=1E-4)
    
    # Perform fitting
    popt, E_corr, I_corr, anodic_slope, cathodic_slope, r_square = Polcurve.active_pol_fit(window=[-0.07, 0.07])

    st.write("Fitted Parameters:")
    st.write(f"Fitted parameters: {popt}")
    st.write(f"E_corr: {E_corr}")
    st.write(f"I_corr: {I_corr}")
    st.write(f"Anodic slope: {anodic_slope}")
    st.write(f"Cathodic slope: {cathodic_slope}")
    st.write(f"R²: {r_square}")

    # Plotting with Matplotlib
    fig, ax = plt.subplots()
    ax.plot(E, I, 'o', label='Data')  # Plot the raw data for illustration
    ax.set_xlabel('Potential (V)')
    ax.set_ylabel('Current (A)')
    ax.legend()
    
    # Displaying plots on the Streamlit app
    st.pyplot(fig)
