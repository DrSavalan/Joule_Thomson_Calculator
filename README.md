# Joule-Thomson Valve Simulator (Python Tkinter & Thermo Library)
![image](https://github.com/user-attachments/assets/41e64764-9a89-41db-ab49-3917a69885c3)

## Overview

This project provides a user-friendly graphical interface (GUI) application, developed with Python's Tkinter, to simulate the **Joule-Thomson expansion process**. It leverages the powerful `thermo` Python library for accurate and rigorous thermodynamic calculations, specifically focusing on single-component fluids using the Peng-Robinson Equation of State.

The simulator allows users to easily input initial conditions (inlet temperature and pressure) and a desired outlet pressure for a selected fluid. It then calculates and displays the resulting outlet temperature, the phase of the fluid (gas, liquid, or a vapor-liquid mixture), as well as its density and molar heat capacity (Cp) under the isenthalpic (constant enthalpy) expansion characteristic of a Joule-Thomson valve. A visual aid of a Joule-Thomson valve is also included to enhance understanding.

## Features

  * **Intuitive GUI:** Built with Tkinter for a straightforward user experience, making input and result display simple.
  * **Fluid Selection:** Offers a convenient dropdown list of common industrial fluids for simulation.
  * **Rigorous Thermodynamic Calculations:** Utilizes the `thermo` library for precise property estimations and phase equilibrium:
      * Implements the **Peng-Robinson (PR) Equation of State** for fluid property modeling.
      * Employs `FlashPureVLS` for robust vapor-liquid flash calculations to determine the outlet state.
      * Simulates the **isenthalpic expansion** (Joule-Thomson effect).
  * **Comprehensive Results:** Displays detailed output including:
      * Inlet temperature and pressure.
      * Calculated outlet temperature.
      * Outlet fluid phase (Gas, Liquid, or Liquid-Vapor).
      * Outlet mass density (kg/m³).
      * Outlet molar heat capacity (Cp) in J/(mol·K).
      * For two-phase outlets, the **vapor mole fraction** is also reported.
  * **Robust Error Handling:** Includes input validation to guide users and provides informative error messages for invalid conditions or computational failures.
  * **Visual Aid:** Features an integrated image to illustrate the concept of a Joule-Thomson valve, showing the inlet and outlet streams.

## How it Works

The simulation's core functionality is powered by the `thermo` library:

1.  **Fluid Property Loading:** The application first loads the critical properties and heat capacity correlations for the selected fluid using `ChemicalConstantsPackage.from_IDs()`.
2.  **Equation of State (EOS) Configuration:** `CEOSLiquid` and `CEOSGas` objects are initialized with the `PRMIX` (Peng-Robinson Mixer) Equation of State, using the fluid's specific critical properties.
3.  **Flash Object Initialization:** A `FlashPureVLS` object is created, configured for vapor-liquid phase equilibrium calculations.
4.  **Inlet State Determination:** A flash calculation is performed at the user-defined inlet temperature ($T\_{in}$) and pressure ($P\_{in}$) to determine the fluid's molar enthalpy ($H\_{in}$) at the inlet.
5.  **Isenthalpic Expansion Calculation:** Since the Joule-Thomson process is isenthalpic (constant enthalpy), a second flash calculation is executed at the user-specified outlet pressure ($P\_{out}$) and the previously calculated inlet enthalpy ($H\_{in}$). This calculation yields the resulting outlet temperature ($T\_{out}$) and the complete outlet phase composition.

## Requirements

To run this application, you need **Python 3.x** and the following libraries:

  * `thermo`
  * `Pillow` (for image handling, installed as `Pillow` but imported as `PIL`)

You can install these dependencies using pip:

```bash
pip install thermo Pillow
```

## Getting Started

Follow these steps to get the Joule-Thomson Valve Simulator up and running on your local machine:

1.  **Clone the repository:**
    Open your terminal or command prompt and run:

    ```bash
    git clone https://github.com/DrSavalan/Joule_Thomson_Calculator.git
    cd Joule_Thomson_Calculator
    ```

2.  **Create and activate a virtual environment (recommended):**
    It's good practice to use a virtual environment to manage project dependencies.

    ```bash
    python -m venv .venv
    ```

      * **On Windows:**
        ```bash
        .\.venv\Scripts\activate
        ```
      * **On macOS/Linux:**
        ```bash
        source ./.venv/bin/activate
        ```

    Your terminal prompt should show `(.venv)` to indicate the environment is active.

3.  **Install the required packages:**
    With your virtual environment activated, install the necessary libraries using the `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Place the Joule-Thomson image:**

      * You need an image file (e.g., `joule_thomson.png`) that visually represents a Joule-Thomson valve or the process.
      * **Place this image file in the same directory as your Python script.**
      * If you name the image file differently, or place it in a sub-directory, remember to update the `image_path` variable in the Python script (`image_path = 'your_image_name.png'`).

5.  **Run the application:**

    ```bash
    python your_script_name.py
    ```

    *(Replace `your_script_name.py` with the actual name of your Python file, e.g., `test2.py` if that's what you named it).*

## Usage

Once the application window appears:

1.  **Select Fluid:** Choose your desired fluid from the "Select Fluid" dropdown menu.
2.  **Enter Inlet Temperature:** Input the initial temperature of the fluid in **Kelvin (K)**.
3.  **Enter Inlet Pressure:** Input the initial pressure of the fluid in **bar**.
4.  **Enter Outlet Pressure:** Input the desired pressure after expansion in **bar**. Ensure this value is **less than the inlet pressure** for a valid expansion.
5.  **Click "Simulate Joule-Thomson (Advanced)":** The application will perform the calculation, and the results will be displayed in the "Calculated Outlet Temperature" field and the "Detailed Results" text area.

## Contributing

Contributions are welcome\! If you have suggestions for improvements, bug fixes, or new features, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name` or `bugfix/your-bug-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add new feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

## License

This project is open-sourced under the [MIT License](https://www.google.com/search?q=LICENSE).

-----
