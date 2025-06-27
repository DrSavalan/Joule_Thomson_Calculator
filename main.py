import tkinter as tk
from tkinter import ttk, messagebox
from thermo import ChemicalConstantsPackage, PRMIX, CEOSLiquid, CEOSGas, FlashPureVLS
from PIL import Image, ImageTk # Import Pillow for image handling

def simulate_joule_thomson_advanced():
    """
    Function to perform the Joule-Thomson calculation using FlashPureVLS and update the GUI.
    """
    fluid_name = fluid_selection.get()

    try:
        T_in = float(inlet_temp_entry.get())
        P_in = float(inlet_pressure_entry.get()) * 1e5  # Convert bar to Pa
        P_out = float(outlet_pressure_entry.get()) * 1e5  # Convert bar to Pa
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numerical values for temperature and pressures.")
        return

    if P_in <= P_out:
        messagebox.showerror("Invalid Input", "Inlet pressure must be greater than outlet pressure for expansion.")
        return
    if T_in <= 0 or P_in <= 0 or P_out <= 0:
        messagebox.showerror("Invalid Input", "Temperature and pressures must be positive.")
        return

    try:
        # Load the constant properties and correlation properties for the selected fluid
        # For a single component, IDs should be a list containing one string
        constants, correlations = ChemicalConstantsPackage.from_IDs([fluid_name])
        # Configure the liquid and gas phase objects using Peng-Robinson (PRMIX)
        # Tcs, Pcs, omegas are lists even for a single component, so access their first element
        eos_kwargs = dict(Tcs=[constants.Tcs[0]], Pcs=[constants.Pcs[0]],
                          omegas=[constants.omegas[0]])  # Still need them in a list for the EOS

        # CORRECTED LINE: Pass the HeatCapacityGases object directly (not indexed)
        # HeatCapacityGases from correlations is an object that contains the correlations for all components in the package
        liquid = CEOSLiquid(PRMIX, HeatCapacityGases=correlations.HeatCapacityGases, eos_kwargs=eos_kwargs)
        gas = CEOSGas(PRMIX, HeatCapacityGases=correlations.HeatCapacityGases, eos_kwargs=eos_kwargs)

        # Create a flash object with possible phases of 1 gas and 1 liquid
        flasher = FlashPureVLS(constants, correlations, gas=gas, liquids=[liquid], solids=[])

        # --- Calculate Inlet State ---
        inlet_res = flasher.flash(T=T_in, P=P_in)
        if inlet_res is None:
            raise ValueError(
                f"Could not determine inlet state for {fluid_name} at {T_in} K, {P_in / 1e5} bar. Check conditions.")

        h_in = inlet_res.H()  # Molar enthalpy at inlet

        # --- Calculate Outlet State (Isenthalpic Flash) ---
        outlet_res = flasher.flash(P=P_out, H=h_in)

        if outlet_res is None:
            raise ValueError(
                f"Could not determine outlet state for {fluid_name} at {P_out / 1e5} bar, H={h_in:.2f} J/mol. Check conditions.")

        # --- Extract and Display Results ---
        T_out = outlet_res.T
        # FlashPureVLS returns 'V' for vapor, 'L' for liquid, or 'V-L' for vapor-liquid mixture
        phase_map = {'V': 'Gas', 'L': 'Liquid', 'V-L': 'Liquid-Vapor'}
        phase_out = phase_map.get(outlet_res.phase, outlet_res.phase)  # Map to more readable names

        rho_out = outlet_res.rho_mass()  # Mass density in kg/m³
        Cp_out = outlet_res.Cp()  # Molar Cp in J/(mol·K)

        result_text = f"Fluid: {fluid_name}\n"
        result_text += f"Inlet Temperature: {T_in:.2f} K\n"
        result_text += f"Inlet Pressure: {P_in / 1e5:.2f} bar\n"
        result_text += f"Outlet Pressure: {P_out / 1e5:.2f} bar\n"
        result_text += f"\n--- Outlet Properties (using FlashPureVLS) ---\n"
        result_text += f"Outlet Temperature: {T_out:.2f} K\n"
        result_text += f"Outlet Phase: {phase_out}\n"
        result_text += f"Outlet Density: {rho_out:.2f} kg/m³\n"
        result_text += f"Outlet Molar Heat Capacity (Cp): {Cp_out:.2f} J/(mol·K)\n"

        if outlet_res.phase == 'V-L':
            # V is molar volume, not vapor fraction directly from these attributes
            # To get vapor fraction (mole basis): moles_vapor / total_moles
            # It can be retrieved from outlet_res.VF or outlet_res.phase_fractions
            # VF is a list of mole fractions for phases, [vapor_fraction, liquid_fraction]
            if outlet_res.VF:  # Check if VF exists and is not empty
                vapor_mole_fraction = outlet_res.VF[0] if outlet_res.VF[0] is not None else 0
                result_text += f"  Vapor mole fraction: {vapor_mole_fraction:.4f}\n"

        # Update the single outlet temperature entry
        # Temporarily set state to normal to allow modification
        outlet_temp_entry.config(state=tk.NORMAL)
        outlet_temp_entry.delete(0, tk.END)
        print(f"{T_out:.2f} K") # This print is for console debugging, not GUI.
        outlet_temp_entry.insert(0, f"{T_out:.2f} K")
        # Set state back to readonly
        outlet_temp_entry.config(state="readonly")

        # Update the detailed results text area
        result_display_text.config(state=tk.NORMAL)
        result_display_text.delete("1.0", tk.END)
        result_display_text.insert(tk.END, result_text)
        result_display_text.config(state=tk.DISABLED)


    except Exception as e:
        messagebox.showerror("Calculation Error", f"An error occurred during calculation: {e}\n"
                                                  "Check input conditions and fluid suitability for Peng-Robinson EOS.")
        import traceback
        traceback.print_exc()  # Print full traceback to console for debugging


# --- GUI Setup ---
root = tk.Tk()
root.title("Joule-Thomson Valve Simulator; By DrSavalan: https://github.com/DrSavalan")
root.geometry("700x800") # Increased height to accommodate the image

# --- Image Display ---
try:
    # Load the image using Pillow (Image.open) and convert to ImageTk.PhotoImage
    # Replace 'joule_thomson.png' with the actual path to your image file
    image_path = 'joule_thomson.png' # Make sure this file is in the same directory or provide full path
    original_image = Image.open(image_path)
    # Resize the image if needed (optional)
    # You might need to adjust the size based on your image and desired layout
    resized_image = original_image.resize((300, 100), Image.LANCZOS) # Adjust size as needed
    joule_thomson_image = ImageTk.PhotoImage(resized_image)

    image_label = tk.Label(root, image=joule_thomson_image)
    image_label.grid(row=0, column=2, rowspan=5, padx=10, pady=10, sticky="nsew") # Place image next to inputs
except FileNotFoundError:
    messagebox.showwarning("Image Not Found", f"Could not find '{image_path}'. Please ensure the image file is in the correct directory.")
    joule_thomson_image = None # Set to None to avoid errors if image not loaded
except Exception as e:
    messagebox.showwarning("Image Error", f"An error occurred while loading the image: {e}")
    joule_thomson_image = None

# --- Fluid Selection ---
fluid_label = ttk.Label(root, text="Select Fluid:")
fluid_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

common_fluids = sorted([
    "water", "nitrogen", "oxygen", "argon", "methane", "ethane", "propane",
    "n-butane", "i-butane", "carbon dioxide", "ammonia", "R134a", "R22", "hydrogen",
    "decane"
])
fluid_selection = ttk.Combobox(root, values=common_fluids, state="readonly")
fluid_selection.set("methane")  # Default value
fluid_selection.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

# --- Inlet Temperature ---
inlet_temp_label = ttk.Label(root, text="Inlet Temperature (K):")
inlet_temp_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
inlet_temp_entry = ttk.Entry(root)
inlet_temp_entry.insert(0, "150")  # Default value for methane test
inlet_temp_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

# --- Inlet Pressure ---
inlet_pressure_label = ttk.Label(root, text="Inlet Pressure (bar):")
inlet_pressure_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
inlet_pressure_entry = ttk.Entry(root)
inlet_pressure_entry.insert(0, "50")  # Default value for methane test
inlet_pressure_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

# --- Outlet Pressure ---
outlet_pressure_label = ttk.Label(root, text="Outlet Pressure (bar):")
outlet_pressure_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
outlet_pressure_entry = ttk.Entry(root)
outlet_pressure_entry.insert(0, "1")  # Default value for methane test
outlet_pressure_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

# --- Calculate Button ---
calculate_button = ttk.Button(root, text="Simulate Joule-Thomson (Advanced)", command=simulate_joule_thomson_advanced)
calculate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=15, sticky="ew")

# --- Outlet Temperature Display (single entry for quick view) ---
outlet_temp_label = ttk.Label(root, text="Calculated Outlet Temperature:")
outlet_temp_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
outlet_temp_entry = ttk.Entry(root, state="readonly")  # Readonly
outlet_temp_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

# --- Full Results Display (Text widget for detailed output) ---
results_frame = ttk.LabelFrame(root, text="Detailed Results (FlashPureVLS)")
results_frame.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="nsew") # Span across 3 columns

result_display_text = tk.Text(results_frame, height=15, width=60, wrap="word", state=tk.DISABLED)
result_display_text.pack(padx=5, pady=5, fill="both", expand=True)

# Configure column and row weights for resizing
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1) # Give weight to the new image column
root.grid_rowconfigure(6, weight=1)
results_frame.grid_columnconfigure(0, weight=1)
results_frame.grid_rowconfigure(0, weight=1)

root.mainloop()