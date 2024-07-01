import numpy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from tkinter import filedialog, Tk, Button, Text, Label
import matplotlib

matplotlib.use('TkAgg')

# Initialize the Tkinter root window
root = Tk()
root.geometry("800x600")  # Set window size (width x height)
root.title("VSM Analyser")  # Set window title
root.resizable(False, False)  # Make the window non-resizable

# Function to read raw data from the selected file
def read_raw_data(file_path):
    raw_data = numpy.loadtxt(file_path)  # Load data from the file
    field = []  # Initialize field list
    moment = []  # Initialize moment list
    for row in raw_data:
        # Convert Oersted to Tesla (1 Oe = 1e-4 T) and add to field list
        field.append(row[0] / 10000)
        # Convert emu to Am^2 (1 emu = 1e-3 Am^2) and add to moment list
        moment.append(row[1] / 1000)
    return field, moment

# Function to calculate the saturation moment from moment data
def calculate_saturation_moment(moment):
    max_moment = moment[0]  # Initialize with the first value
    for m in moment:
        if m > max_moment:
            max_moment = m  # Update if a larger value is found
    saturation_moment = max_moment  # The maximum value found in the moment array
    return saturation_moment

# Function to calculate the coercivity from field and moment data
def calculate_coercivity(field, moment):
    min_moment = moment[0]  # Initialize with the first value
    min_moment_index = 0  # Initialize the index of minimum moment
    for i in range(len(moment)):
        if moment[i] < min_moment:
            min_moment = moment[i]
            min_moment_index = i  # Update index of minimum moment
    coercivity = field[min_moment_index]  # Field value at the minimum moment
    return coercivity

# Function to calculate the remanence from moment data
def calculate_remanence(moment):
    remanence = moment[-1]  # The last value of the moment array
    return remanence

# Function to calculate the magnetic moment using numerical integration (area under the curve)
def calculate_magnetic_moment(field, moment):
    area = 0  # Initialize the area
    for i in range(1, len(field)):
        # Use trapezoidal rule to approximate the area under the curve
        trapezoid_area = (moment[i] + moment[i - 1]) * (field[i] - field[i - 1]) / 2
        area += trapezoid_area  # Sum the areas of the trapezoids
    magnetic_moment = area  # Total area under the moment vs. field curve
    return magnetic_moment

# Function to fit the data to a model to extract anisotropy constants
def fit_anisotropy_constants(field, moment):
    def anisotropy_model(theta, k1, k2):
        # Anisotropy model as a function of angle (theta) and constants (k1, k2)
        return -k1 * numpy.cos(2 * theta) - k2 * numpy.cos(4 * theta)

    # Generate angles from 0 to 360 degrees, converted to radians
    theta = numpy.radians(numpy.linspace(0, 360, len(field)))  # linspace creates equally spaced values
    initial_guess = [0.001, 0.001]  # Initial guess for k1 and k2 for curve fitting
    fit_params, _ = curve_fit(anisotropy_model, theta, moment, p0=initial_guess)  # Curve fitting
    k1, k2 = fit_params  # Extract fitted parameters
    return k1, k2

# Function to calculate differential magnetic susceptibility
def calculate_differential_susceptibility(moment, field):
    # Initialize lists to hold differences
    diff_moment = []
    diff_field = []
    
    # Calculate changes in moment and field
    for i in range(len(moment) - 1):
        diff_moment.append(moment[i + 1] - moment[i])  # Calculate change in moment (Δmoment)
        diff_field.append(field[i + 1] - field[i])  # Calculate change in field (Δfield)
    
    # Initialize list to hold susceptibility values
    susceptibility = []
    
    # Calculate susceptibility as the ratio of changes
    for i in range(len(diff_moment)):
        dm = diff_moment[i]
        df = diff_field[i]
        susceptibility_value = dm / df  # Differential susceptibility χ = Δmoment / Δfield
        susceptibility.append(susceptibility_value)
    
    return susceptibility

# Function to plot the field vs moment data and mark key parameters
def plot_data(field, moment, saturation_moment, coercivity, remanence):
    plt.plot(field, moment)  # Plot moment vs. field
    plt.axhline(y=saturation_moment, linestyle='--', color='r', label='Saturation moment')  # Horizontal line for saturation moment
    plt.axvline(x=coercivity, linestyle='--', color='g', label='Coercivity')  # Vertical line for coercivity
    plt.axhline(y=remanence, linestyle='--', color='b', label='Remanence')  # Horizontal line for remanence
    
    # Adding grid lines
    plt.grid(True)
    
    # Setting more ticks on the x-axis
    plt.xticks(numpy.arange(min(field), max(field), (max(field) - min(field)) / 10))
    
    plt.xlabel('Magnetic field (T)')  # Label for x-axis
    plt.ylabel('Magnetic moment (Am^2)')  # Label for y-axis
    plt.legend()  # Show legend
    plt.show()  # Display the plot

# Function to display calculated parameters in the Tkinter window
def display_parameters(saturation_moment, coercivity, remanence, magnetic_moment, k1, k2, susceptibility):
    txt_output.delete("1.0", "end")
    txt_output.insert("end", "                           Key Parameters " + "\n\n")
    txt_output.insert("end", f" Saturation moment: {saturation_moment:.3f} Am^2 \n\n")  # Display saturation moment
    txt_output.insert("end", f" Coercivity: {coercivity:.3f} T \n\n")  # Display coercivity
    txt_output.insert("end", f" Remanence: {remanence:.3f} Am^2 \n\n")  # Display remanence
    txt_output.insert("end", f" Magnetic moment: {magnetic_moment:.3f} Am^2 \n\n")  # Display magnetic moment
    txt_output.insert("end", f" Anisotropy constants: k1={k1:.3e} J/m^3, k2={k2:.3e} J/m^3 \n\n")  # Display anisotropy constants
    txt_output.insert("end", f" Differential susceptibility: {numpy.mean(susceptibility):.3e} (unitless) \n")  # Display mean differential susceptibility

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
    display_parameters(saturation_moment, coercivity, remanence, magnetic_moment, k1, k2, susceptibility)  # Display parameters
    plot_data(field, moment, saturation_moment, coercivity, remanence)  # Plot data and key parameters

# Button to select a file and start the analysis
select_file_button = Button(text="Select File (.txt)", font=('Helvetica', 12), bg="#1b6a97", fg="white",
                            width=14, height=1, command=main)
select_file_button.place(x=330, y=30)

# Text widget to display the output
txt_output = Text(root, height=17, width=80, font=("Helvetica", 12))
txt_output.place(x=40, y=200)

# Footer label
footer_label = Label(root, text="Developed by Abhijeetbyte © 2024 ( https://github.com/Abhijeetbyte/VSManalyser )", font=('Helvetica', 12), fg="#1b6a97")
footer_label.place(x=100, y=550)

# Run the Tkinter main loop
root.mainloop()
