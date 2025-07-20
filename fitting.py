import streamlit as st
import pandas as pd
from polcurvefit import polcurvefit, DataImport
import os

# Set up the Streamlit app title
st.title("Electrochemical Data Analysis")

# File uploader widget to support CSV and Excel files
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

# Directory where plots are saved
plot_output_folder = 'Visualization_activation_control_fit'

if uploaded_file is not None:
    # Read the uploaded file (CSV or Excel)
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Failed to read the file: {e}")
        st.stop()

    # Display uploaded data
    st.write("Uploaded Data:")
    st.dataframe(df)

    # Extract potential and current columns
    try:
        potential_column = df.columns[0]
        current_column = df.columns[2]

        E = df[potential_column].values
        I = df[current_column].values
    except Exception as e:
        st.error(f"Failed to extract data columns: {e}")
        st.stop()

    # Initialize polcurvefit with the loaded data
    Polcurve = polcurvefit(E, I, sample_surface=1E-4)
    
    # Perform the active polarization curve fit
    try:
        popt, E_corr, I_corr, anodic_slope, cathodic_slope, r_square = Polcurve.active_pol_fit(window=[-0.07, 0.07])
    except Exception as e:
        st.error(f"Failed during curve fitting: {e}")
        st.stop()

    # Display results
    st.write("Fitted Parameters:")
    st.write(f"Fitted parameters: {popt}")
    st.write(f"E_corr: {E_corr}")
    st.write(f"I_corr: {I_corr}")
    st.write(f"Anodic slope: {anodic_slope}")
    st.write(f"Cathodic slope: {cathodic_slope}")
    st.write(f"R²: {r_square}")

    # Save plots
    try:
        Polcurve.plotting(output_folder=plot_output_folder)
        st.write(f"Plots saved to: {plot_output_folder}")
    except Exception as e:
        st.error(f"Failed to save plots: {e}")
        st.stop()

    # Display each plot in the visualization directory
    st.write("Plots:")
    try:
        files = os.listdir(plot_output_folder)
        if not files:
            st.write("No plot files found.")
        for plot_file in files:
            if plot_file.endswith('.png') or plot_file.endswith('.jpg'):
                plot_path = os.path.join(plot_output_folder, plot_file)
                st.image(plot_path, caption=plot_file)
    except Exception as e:
        st.error(f"Failed to display plot files: {e}")
