import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from tkinter import *
from tkinter import filedialog


root=Tk() #call tkinter function
root.geometry("400x550") #Width x Height (320,480)
root.title("VSManalyser") #Title bar
root.resizable(False,False) # window always stay in same size


def Main():

    # Open file
    file_path = filedialog.askopenfilename(initialdir="/") # get the file path
    #print(file_path)

    # Read in raw data from VSM measurement
    raw_data = np.loadtxt(file_path)

    # Convert units to SI units
    field = raw_data[:, 0] / 1e4  # Convert Oe to T
    moment = raw_data[:, 1] / 1e3  # Convert emu to Am^2

    # Calculate key parameters
    saturation_moment = max(moment)
    coercivity = field[np.argmin(moment)]
    remanence = moment[-1]
    magnetic_moment = np.trapz(moment, field)  # calculate magnetic moment by numerical integration

    # Fit the data to a model to extract anisotropy constants
    def anisotropy_model(theta, k1, k2):
        return -k1*np.cos(2*theta) - k2*np.cos(4*theta)

    theta = np.radians(np.linspace(0, 360, len(field)))
    fit_params, _ = curve_fit(anisotropy_model, theta, moment, p0=[1e-3, 1e-3])
    k1, k2 = fit_params

    # Calculate magnetic susceptibility
    magnetic_susceptibility = np.diff(moment) / np.diff(field)

    # Plot the data and key parameters
    plt.plot(field, moment)
    plt.axhline(saturation_moment, linestyle='--', color='r', label='Saturation moment')
    plt.axvline(coercivity, linestyle='--', color='g', label='Coercivity')
    plt.axhline(remanence, linestyle='--', color='b', label='Remanence')
    plt.xlabel('Magnetic field (T)')
    plt.ylabel('Magnetic moment (Am^2)')
    plt.legend()
    

    # Print out as text label on main window
    txt_output = Text(root, height=17, width=43)
    txt_output.place(x=25,y=220)# place
    
    txt_output.insert(END, '               Key Parameters ' + "\n\n")
    txt_output.insert(END, ' Saturation moment: {:.3f} Am^2'.format(saturation_moment) + "\n")
    txt_output.insert(END, ' Coercivity: {:.3f} T'.format(coercivity) + "\n")
    txt_output.insert(END, ' Remanence: {:.3f} Am^2'.format(remanence) + "\n")
    txt_output.insert(END, ' Magnetic moment: {:.3f} Am^2'.format(magnetic_moment) + "\n")
    txt_output.insert(END, ' Anisotropy constants: k1={:.3e} J/m^3, k2={:.3e} J/m^3'.format(k1, k2) + "\n\n")
    txt_output.insert(END, ' Magnetic susceptibility: {:.3e} m^3/kg'.format(np.mean(magnetic_susceptibility)) + "\n")
    
    """ Print out key parameters
    print('\n           Key Parameters \n\n')
    print(' Saturation moment: {:.3f} Am^2'.format(saturation_moment))
    print(' Coercivity: {:.3f} T'.format(coercivity))
    print(' Remanence: {:.3f} Am^2'.format(remanence))
    print(' Magnetic moment: {:.3f} Am^2'.format(magnetic_moment))
    print(' Anisotropy constants: k1={:.3e} J/m^3, k2={:.3e} J/m^3'.format(k1, k2))
    print(' Magnetic susceptibility: {:.3e} m^3/kg'.format(np.mean(magnetic_susceptibility)))
    
    """
    plt.show() # show graph window


Select_file = Button(text ="Select file (.txt)",font=('Helvetica',12), bg="#1b6a97",fg="white",width=14,height=1, command = Main).place(x=130,y=30) #command button & location


root.mainloop()
