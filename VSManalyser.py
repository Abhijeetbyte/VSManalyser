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
    field = raw_data[:, 0] / 10000  # Convert Oersted to Tesla
    moment = raw_data[:, 1] / 1000  # Convert emu to Am^2
    return field, moment

# Calculate saturation moment from moment data
def calculate_saturation_moment(moment):
    max_moment = moment[0]  # Initialize with the first value
    for m in moment:
        if m > max_moment:
            max_moment = m  # Update if a larger value is found
    saturation_moment = max_moment
    return saturation_moment

# Calculate coercivity from field and moment data
def calculate_coercivity(field, moment):
    min_moment = moment[0]  # Initialize with the first value
    min_moment_index = 0  # Initialize the index of minimum moment
    for i in range(len(moment)):
        if moment[i] < min_moment:
            min_moment = moment[i]
            min_moment_index = i  # Update index
    coercivity = field[min_moment_index]  # Field at minimum moment
    return coercivity

# Calculate remanence from moment data
def calculate_remanence(moment):
    remanence = moment[-1]  # Last value of moment
    return remanence

# Calculate magnetic moment using numerical integration
def calculate_magnetic_moment(field, moment):
    area = 0  # Initialize the area
    for i in range(1, len(field)):
        trapezoid_area = (moment[i] + moment[i - 1]) * (field[i] - field[i - 1]) / 2  # Area of trapezoid
        area += trapezoid_area  # Sum the areas
    magnetic_moment = area
    return magnetic_moment

# Fit the data to extract anisotropy constants
def fit_anisotropy_constants(field, moment):
    def anisotropy_model(theta, k1, k2):
        return -k1 * np.cos(2 * theta) - k2 * np.cos(4 * theta)

    theta = np.radians(np.linspace(0, 360, len(field)))
    initial_guess = [0.001, 0.001]  # Initial guess for curve fitting
    fit_params, _ = curve_fit(anisotropy_model, theta, moment, p0=initial_guess)
    k1, k2 = fit_params
    return k1, k2

# Calculate magnetic susceptibility from moment and field data
def calculate_magnetic_susceptibility(moment, field):
    susceptibility = []  # Initialize the list for susceptibility
    for i in range(1, len(moment)):
        delta_moment = moment[i] - moment[i - 1]  # Change in moment
        delta_field = field[i] - field[i - 1]  # Change in field
        if delta_field != 0:  # Avoid division by zero
            susceptibility_value = delta_moment / delta_field
            susceptibility.append(susceptibility_value)
    magnetic_susceptibility = np.array(susceptibility)
    return magnetic_susceptibility

# Plot the field vs moment data and key parameters
def plot_data(field, moment, saturation_moment, coercivity, remanence):
    plt.plot(field, moment)
    plt.axhline(y=saturation_moment, linestyle='--', color='r', label='Saturation moment')
    plt.axvline(x=coercivity, linestyle='--', color='g', label='Coercivity')
    plt.axhline(y=remanence, linestyle='--', color='b', label='Remanence')
    plt.xlabel('Magnetic field (T)')
    plt.ylabel('Magnetic moment (Am^2)')
    plt.legend()
    plt.show()

# Display calculated parameters in the Tkinter window
def display_parameters(saturation_moment, coercivity, remanence, magnetic_moment, k1, k2, magnetic_susceptibility):
    txt_output = Text(root, height=17, width=43)
    txt_output.place(x=25, y=220)
    txt_output.insert("end", "               Key Parameters " + "\n\n")
    txt_output.insert("end", f" Saturation moment: {saturation_moment:.3f} Am^2\n")
    txt_output.insert("end", f" Coercivity: {coercivity:.3f} T\n")
    txt_output.insert("end", f" Remanence: {remanence:.3f} Am^2\n")
    txt_output.insert("end", f" Magnetic moment: {magnetic_moment:.3f} Am^2\n")
    txt_output.insert("end", f" Anisotropy constants: k1={k1:.3e} J/m^3, k2={k2:.3e} J/m^3\n\n")
    txt_output.insert("end", f" Magnetic susceptibility: {np.mean(magnetic_susceptibility):.3e} m^3/kg\n")

# Main function to read file, calculate parameters, and display results
def main():
    file_path = filedialog.askopenfilename(initialdir="/")
    field, moment = read_raw_data(file_path)
    saturation_moment = calculate_saturation_moment(moment)
    coercivity = calculate_coercivity(field, moment)
    remanence = calculate_remanence(moment)
    magnetic_moment = calculate_magnetic_moment(field, moment)
    k1, k2 = fit_anisotropy_constants(field, moment)
    magnetic_susceptibility = calculate_magnetic_susceptibility(moment, field)
    plot_data(field, moment, saturation_moment, coercivity, remanence)
    display_parameters(saturation_moment, coercivity, remanence, magnetic_moment, k1, k2, magnetic_susceptibility)

select_file_button = Button(text="Select file (.txt)", font=('Helvetica', 12), bg="#1b6a97", fg="white",
                            width=14, height=1, command=main)
select_file_button.place(x=130, y=30)

root.mainloop()
