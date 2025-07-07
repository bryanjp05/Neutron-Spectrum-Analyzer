import openmc
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
import re
import os

# Make sure results directory exists
os.makedirs("results", exist_ok=True)

# Find and sort all depletion statepoints
statepoints = sorted(
    glob.glob("openmc_simulation_n*.h5"),
    key=lambda x: int(re.search(r"n(\d+)", x).group(1))
)

if not statepoints:
    raise FileNotFoundError("No depletion statepoint files (openmc_simulation_n*.h5) found.")

# Process each timestep
for i, sp_file in enumerate(statepoints):
    print(f"Processing {sp_file}")
    sp = openmc.StatePoint(sp_file)

    try:
        tally = sp.get_tally(name="flux spectrum")
        flux = tally.get_values(scores=["flux"]).flatten()

        # Extract energy filter and bin structure
        energy_filter = tally.find_filter(openmc.EnergyFilter)
        energy_bins = energy_filter.bins
        energy_mid = np.sqrt(np.multiply(*zip(*energy_bins)))

        # Compute bin widths
        energy_edges = [edge[0] for edge in energy_bins] + [energy_bins[-1][1]]
        dE = np.diff(energy_edges)

        # Normalize flux per eV
        flux_normalized = flux / dE

        # Integration thresholds
        thermal_max = 0.625  # eV
        fast_min = 1e5       # eV

        # Totals
        total_flux = np.sum(flux_normalized * dE)
        thermal_flux = np.sum(flux_normalized[energy_mid < thermal_max] * dE[energy_mid < thermal_max])
        fast_flux = np.sum(flux_normalized[energy_mid > fast_min] * dE[energy_mid > fast_min])

        thermal_frac = thermal_flux / total_flux * 100
        fast_frac = fast_flux / total_flux * 100

        print(f"Step {i}:")
        print(f"  Total flux     = {total_flux:.3e} n/cm²/s")
        print(f"  Thermal flux   = {thermal_flux:.3e} ({thermal_frac:.1f}%)")
        print(f"  Fast flux      = {fast_flux:.3e} ({fast_frac:.1f}%)")

        # Save CSV
        csv_path = f"results/flux_spectrum_step_{i}.csv"
        pd.DataFrame({
            "Energy (eV)": energy_mid,
            "Flux (/cm^2/s/eV)": flux_normalized
        }).to_csv(csv_path, index=False)
        print(f"Saved CSV to {csv_path}")

        # Plot
        plt.figure(figsize=(8, 6))
        plt.loglog(energy_mid, flux_normalized)
        plt.xlabel('Energy (eV)')
        plt.ylabel('Neutron Flux (n/cm²/s/eV)')
        plt.title(f'Neutron Energy Spectrum - Step {i}')
        plt.grid(True, which="both", ls="--")
        plt.axvspan(1e-3, thermal_max, color='blue', alpha=0.1, label='Thermal')
        plt.axvspan(fast_min, 2e6, color='red', alpha=0.1, label='Fast')
        plt.legend()
        plt.tight_layout()
        plt.show()

    except LookupError:
        print(f"Tally 'flux spectrum' not found in {sp_file}. Skipping.")

print("All timesteps processed.")

