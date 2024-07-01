import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from tkinter import filedialog, Tk, Button, Text
import matplotlib

matplotlib.use('TkAgg')

root = Tk()
root.geometry("400x550")
root.title("VSM Analyser")
root.resizable(False, False)

# Read raw data from the selected file
def read_raw_data(file_path):
    raw_data = np.loadtxt(file_path)
    field = raw_data[:, 0] / 10000  # Convert Oersted to Tesla (1 Oe = 1e-4 T)
    moment = raw_data[:, 1] / 1000  # Convert emu to Am^2 (1 emu = 1e-3 Am^2)
    return field, moment

# Calculate the saturation moment from moment data
def calculate_saturation_moment(moment):
    max_moment = moment[0]  # Initialize with the first value
    for m in moment:
        if m > max_moment:
            max_moment = m  # Update if a larger value is found
    saturation_moment = max_moment  # The maximum value found in the moment array
    return saturation_moment

# Calculate the coercivity from field and moment data
def calculate_coercivity(field, moment):
    min_moment = moment[0]  # Initialize with the first value
    min_moment_index = 0  # Initialize the index of minimum moment
    for i in range(len(moment)):
        if moment[i] < min_moment:
            min_moment = moment[i]
            min_moment_index = i  # Update index of minimum moment
    coercivity = field[min_moment_index]  # Field value at the minimum moment
    return coercivity

# Calculate the remanence from moment data
def calculate_remanence(moment):
    remanence = moment[-1]  # The last value of the moment array
    return remanence

# Calculate the magnetic moment using numerical integration (area under the curve)
def calculate_magnetic_moment(field, moment):
    area = 0  # Initialize the area
    for i in range(1, len(field)):
        trapezoid_area = (moment[i] + moment[i - 1]) * (field[i] - field[i - 1]) / 2  # Trapezoidal rule
        area += trapezoid_area  # Sum the areas of the trapezoids
    magnetic_moment = area  # Total area under the moment vs. field curve
    return magnetic_moment

# Fit the data to a model to extract anisotropy constants
def fit_anisotropy_constants(field, moment):
    def anisotropy_model(theta, k1, k2):
        # Anisotropy model as a function of angle (theta) and constants (k1, k2)
        return -k1 * np.cos(2 * theta) - k2 * np.cos(4 * theta)

    # Generate angles from 0 to 360 degrees, converted to radians
    theta = np.radians(np.linspace(0, 360, len(field)))  # linspace creates equally spaced values
    initial_guess = [0.001, 0.001]  # Initial guess for k1 and k2 for curve fitting
    fit_params, _ = curve_fit(anisotropy_model, theta, moment, p0=initial_guess)  # Curve fitting
    k1, k2 = fit_params  # Extract fitted parameters
    return k1, k2

# Calculate differential magnetic susceptibility
def calculate_differential_susceptibility(moment, field):
    diff_moment = np.diff(moment)  # Change in moment
    diff_field = np.diff(field)  # Change in field
    susceptibility = diff_moment / diff_field  # Ratio of changes gives differential susceptibility
    return susceptibility

# Plot the field vs moment data and mark key parameters
def plot_data(field, moment, saturation_moment, coercivity, remanence):
    plt.plot(field, moment)  # Plot moment vs. field
    plt.axhline(y=saturation_moment, linestyle='--', color='r', label='Saturation moment')  # Horizontal line for saturation moment
    plt.axvline(x=coercivity, linestyle='--', color='g', label='Coercivity')  # Vertical line for coercivity
    plt.axhline(y=remanence, linestyle='--', color='b', label='Remanence')  # Horizontal line for remanence
    plt.xlabel('Magnetic field (T)')  # Label for x-axis
    plt.ylabel('Magnetic moment (Am^2)')  # Label for y-axis
    plt.legend()  # Show legend
    plt.show()  # Display the plot

# Display calculated parameters in the Tkinter window
def display_parameters(saturation_moment, coercivity, remanence, magnetic_moment, k1, k2, susceptibility):
    txt_output = Text(root, height=17, width=43)
    txt_output.place(x=25, y=220)
    txt_output.insert("end", "               Key Parameters " + "\n\n")
    txt_output.insert("end", f" Saturation moment: {saturation_moment:.3f} Am^2\n")  # Display saturation moment
    txt_output.insert("end", f" Coercivity: {coercivity:.3f} T\n")  # Display coercivity
    txt_output.insert("end", f" Remanence: {remanence:.3f} Am^2\n")  # Display remanence
    txt_output.insert("end", f" Magnetic moment: {magnetic_moment:.3f} Am^2\n")  # Display magnetic moment
    txt_output.insert("end", f" Anisotropy constants: k1={k1:.3e} J/m^3, k2={k2:.3e} J/m^3\n\n")  # Display anisotropy constants
    txt_output.insert("end", f" Differential susceptibility: {np.mean(susceptibility):.3e} (unitless)\n")  # Display mean differential susceptibility

# Main function to read file, calculate parameters, and display results
def main():
    file_path = filedialog.askopenfilename(initialdir="/")  # Prompt user to select a file
    field, moment = read_raw_data(file_path)  # Read and process the data
    saturation_moment = calculate_saturation_moment(moment)  # Calculate saturation moment
    coercivity = calculate_coercivity(field, moment)  # Calculate coercivity
    remanence = calculate_remanence(moment)  # Calculate remanence
    magnetic_moment = calculate_magnetic_moment(field, moment)  # Calculate total magnetic moment
    k1, k2 = fit_anisotropy_constants(field, moment)  # Fit anisotropy constants
    susceptibility = calculate_differential_susceptibility(moment, field)  # Calculate differential susceptibility
    plot_data(field, moment, saturation_moment, coercivity, remanence)  # Plot data and key parameters
    display_parameters(saturation_moment, coercivity, remanence, magnetic_moment, k1, k2, susceptibility)  # Display parameters

# Button to select a file and start the analysis
select_file_button = Button(text="Select file (.txt)", font=('Helvetica', 12), bg="#1b6a97", fg="white",
                            width=14, height=1, command=main)
select_file_button.place(x=130, y=30)

root.mainloop()  # Run the Tkinter main loop
