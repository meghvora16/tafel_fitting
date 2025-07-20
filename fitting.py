import streamlit as st
import pandas as pd
from polcurvefit import polcurvefit, DataImport

# Set up the app title
st.title("Electrochemical Data Analysis")

# File uploader widget
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)
    
    # Display the uploaded data
    st.write("Uploaded Data:")
    st.dataframe(df)

    # Extract columns for potential and current based on your format
    potential_column = df.columns[0]
    current_column = df.columns[2]
    
    E = df[potential_column].values
    I = df[current_column].values

    # Initialize polcurvefit with the loaded data
    Polcurve = polcurvefit(E, I, sample_surface=1E-4)  # Sample surface area
    
    # Perform the active polarization curve fit
    popt, E_corr, I_corr, anodic_slope, cathodic_slope, r_square = Polcurve.active_pol_fit(window=[-0.07, 0.07])

    # Display the results
    st.write("Fitted Parameters:")
    st.write(f"Fitted parameters: {popt}")
    st.write(f"E_corr: {E_corr}")
    st.write(f"I_corr: {I_corr}")
    st.write(f"Anodic slope: {anodic_slope}")
    st.write(f"Cathodic slope: {cathodic_slope}")
    st.write(f"R²: {r_square}")

    # Save plot and display it
    plot_path = 'Visualization_fit/polcurve_plot.png'
    Polcurve.plotting(output_folder='Visualization_fit')

    # Display the plot image
    st.image(plot_path)
