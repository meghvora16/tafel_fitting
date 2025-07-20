from polcurvefit import polcurvefit
from polcurvefit import DataImport

filename = r"C:\Users\VORAMGH\Downloads\lsv.txt"

# Load columns for potential and current
E, I = DataImport.load_txt(filename, lines_header=1, columns_E_I=[0, 2])  # Adjust based on header - header line is at 1

# Initialize polcurvefit with the loaded data
Polcurve = polcurvefit(E, I, sample_surface=1E-4)  # Assuming sample surface area of 1E-4 m^2

# Perform the active polarization curve fit
popt, E_corr, I_corr, anodic_slope, cathodic_slope, r_square = Polcurve.active_pol_fit(window=[-0.07, 0.07])

# Print the results
print("Fitted parameters:", popt)
print("E_corr:", E_corr)
print("I_corr:", I_corr)
print("Anodic slope:", anodic_slope)
print("Cathodic slope:", cathodic_slope)
print("R²:", r_square)

# Save plot
Polcurve.plotting(output_folder='Visualization_fit')
