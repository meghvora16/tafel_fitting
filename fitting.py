import streamlit as st
import pandas as pd
from polcurvefit import polcurvefit, DataImport
import os
import matplotlib.pyplot as plt

# Set up the Streamlit app
st.title("Electrochemical Data Analysis")

# File uploader widget
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

    # Process columns
    try:
        potential_column = df.columns[0]
        current_column = df.columns[2]

        E = df[potential_column].values
        I = df[current_column].values
    except Exception as e:
        st.error(f"Failed to extract data columns: {e}")
        st.stop()

    # Initialize polcurvefit
    try:
        Polcurve = polcurvefit(E, I, sample_surface=1E-4)
    except Exception as e:
        st.error(f"Initialization failed: {e}")
        st.stop()
    
    # Perform fitting
    try:
        popt, E_corr, I_corr, anodic_slope, cathodic_slope, r_square = Polcurve.active_pol_fit(window=[-0.07, 0.07])
    except Exception as e:
        st.error(f"Fitting failed: {e}")
        st.stop()

    # Display results
    st.write("Fitted Parameters:")
    st.write(f"Fitted parameters: {popt}")
    st.write(f"E_corr: {E_corr}")
    st.write(f"I_corr: {I_corr}")
    st.write(f"Anodic slope: {anodic_slope}")
    st.write(f"Cathodic slope: {cathodic_slope}")
    st.write(f"R²: {r_square}")

    # Attempt to save plots
    try:
        Polcurve.plotting(output_folder=plot_output_folder)
        # Debugging line to confirm file creation
        st.write(f"Plots should be saved to '{plot_output_folder}'")
        st.write(f"Contents of the folder: {os.listdir(plot_output_folder)}")
    except Exception as e:
        st.error(f"Failed to save plots: {e}")
        st.stop()

    # Use Matplotlib to create a manual verification plot
    try:
        fig, ax = plt.subplots()
        ax.plot(E, I, 'o', label='Manual Data Plot')
        ax.set_title('Manual Verification Plot')
        ax.set_xlabel('Potential (V)')
        ax.set_ylabel('Current (A)')
        ax.legend()
        st.pyplot(fig)  # Display the manual plot
    except Exception as e:
        st.error(f"Failed to create manual plot: {e}")

    # Display each plot from directory
    try:
        for plot_file in os.listdir(plot_output_folder):
            if plot_file.endswith('.png') or plot_file.endswith('.jpg'):
                plot_path = os.path.join(plot_output_folder, plot_file)
                st.image(plot_path, caption=plot_file)
    except Exception as e:
        st.error(f"Failed to display plot files: {e}")
