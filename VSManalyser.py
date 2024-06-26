import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from tkinter import filedialog, Tk, Button, Text
import matplotlib

matplotlib.use('TkAgg')

root = Tk()
root.geometry("400x550")
root.title("VSManalyser")
root.resizable(False, False)

def read_raw_data(file_path):
    raw_data = np.loadtxt(file_path)
    field = raw_data[:, 0] / 1e4  # Convert Oe to T
    moment = raw_data[:, 1] / 1e3  # Convert emu to Am^2
    return field, moment

def calculate_saturation_moment(moment):
    return np.max(moment)

def calculate_coercivity(field, moment):
    return field[np.argmin(moment)]

def calculate_remanence(moment):
    return moment[-1]

def calculate_magnetic_moment(field, moment):
    return np.trapz(moment, field)

def fit_anisotropy_constants(field, moment):
    def anisotropy_model(theta, k1, k2):
        return -k1 * np.cos(2 * theta) - k2 * np.cos(4 * theta)
    theta = np.radians(np.linspace(0, 360, len(field)))
    initial_guess = [1e-3, 1e-3]  # Initial guess for curve_fit
    fit_params, _ = curve_fit(anisotropy_model, theta, moment, p0=initial_guess)
    return fit_params[0], fit_params[1]

def calculate_magnetic_susceptibility(moment, field):
    return np.diff(moment) / np.diff(field)

def plot_data(field, moment, saturation_moment, coercivity, remanence):
    plt.plot(field, moment)
    plt.axhline(saturation_moment, linestyle='--', color='r', label='Saturation moment')
    plt.axvline(coercivity, linestyle='--', color='g', label='Coercivity')
    plt.axhline(remanence, linestyle='--', color='b', label='Remanence')
    plt.xlabel('Magnetic field (T)')
    plt.ylabel('Magnetic moment (Am^2)')
    plt.legend()
    plt.show()

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
