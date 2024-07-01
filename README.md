# <p align="center">VSM Analyser</p>

**<p align="center">A quick and portable way to analyze VSM data**</p>

This Python script creates a graphical user interface (GUI) using the Tkinter library. The GUI allows the user to select a text file containing magnetic data from a Vibrating Sample Magnetometer (VSM) measurement. The script reads the data, converts the units to SI units, calculates key magnetic parameters (saturation moment, coercivity, remanence, magnetic moment, anisotropy constants, and differential magnetic susceptibility), and then displays the key parameters on both a plot and a text label in the GUI.

## Features:  🌟

* Open VSM measurement data in `.txt` format
* Convert units to SI units
* Calculate key parameters such as:
  * Saturation moment
  * Coercivity
  * Remanence
  * Magnetic moment
  * Anisotropy constants
  * Differential magnetic susceptibility
* Fit the data to a model to extract anisotropy constants
* Plot the data and key parameters
* Save analysis parameters for later use
* Portable, no installation required

  <br/>
  

## Download ⬇

[Latest stable release](https://github.com/abhijeetbyte/VSManalyser/releases/latest)

Releases and prereleases contain links to standalone packages (and installers for full releases) for Windows.

* Portable version [Download v1.0](https://github.com/Abhijeetbyte/VSManalyser/releases/download/v1.0/VSManalyser.exe)

_Your computer must be running Windows 10 or newer._

<br/>



## Working ⚙

The script uses NumPy and SciPy libraries for numerical operations and curve fitting, and the Matplotlib library for plotting. The GUI contains a single button that, when clicked, opens a file dialogue to select a **text file** containing magnetic data. Once the user selects a file, the script reads the data, calculates the key parameters, and displays them on the plot and a text label in the GUI.
<br/>


![image](https://github.com/Abhijeetbyte/VSManalyser/assets/80936610/27e178fd-e1ab-4575-aa56-82402c9e6c35)


<br/>


The key parameters displayed in the text label include the saturation moment, coercivity, remanence, magnetic moment, anisotropy constants, and differential magnetic susceptibility. The plot shows the magnetic moment as a function of the magnetic field and also displays the saturation moment, coercivity, and remanence as horizontal and vertical lines.

The code is organized into several functions, each performing a specific task:

* `read_raw_data(file_path)` - Reads the raw VSM data from the file and converts the units to SI units.
* `calculate_saturation_moment(moment)` - Calculates the saturation moment.
* `calculate_coercivity(field, moment)` - Calculates the coercivity.
* `calculate_remanence(moment)` - Calculates the remanence.
* `calculate_magnetic_moment(field, moment)` - Calculates the magnetic moment using numerical integration.
* `fit_anisotropy_constants(field, moment)` - Fits the data to an anisotropy model to extract anisotropy constants.
* `calculate_differential_susceptibility(moment, field)` - Calculates the differential magnetic susceptibility.
* `plot_data(field, moment, saturation_moment, coercivity, remanence)` - Plots the magnetic moment as a function of the magnetic field and marks key parameters.
* `display_parameters(saturation_moment, coercivity, remanence, magnetic_moment, k1, k2, susceptibility)` - Displays the calculated parameters in the Tkinter window.

**VSM Analyser** provides a simple but powerful tool for analyzing magnetic data from a VSM measurement.

<br/>


## VSM Data File Example

<img src="https://github.com/Abhijeetbyte/VSManalyser/assets/80936610/b59e8b5d-a750-4747-a9f4-fac63f83813d" width="600" alt="Descriptive text">

<br/>
<br/>



## License 📃

Licensed under the [CC0-1.0 License](LICENSE).

© 2024 Abhijeet Kumar. All rights reserved.
